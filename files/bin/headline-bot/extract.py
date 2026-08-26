#!/usr/bin/env python3
"""Resolve each candidate to its publisher URL and pull the article body.

    files/venv/bin/python files/bin/headline-bot/extract.py

Google News RSS links are opaque redirects. They are resolved against Google News' own
batchexecute endpoint: the article page carries a signature and timestamp, and those plus
the article id return the publisher URL. No search engine sits in the path.

A candidate with no resolvable URL, or a body under MIN_BODY characters, is dropped here
rather than sent to the model. The model cannot convict an article it cannot read.
"""
import argparse, html, json, os, re, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from beats import BLOCKED  # noqa: E402

STATE = os.path.join(HERE, "state")
UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
MIN_BODY = 900
MAX_BODY = 14000


def get(url, data=None, timeout=25):
    req = urllib.request.Request(
        url, data=data,
        headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


GNEWS_RPC = "https://news.google.com/_/DotsSplashUi/data/batchexecute"


def resolve(gnews_link):
    """Turn a Google News RSS link into the publisher URL, or None."""
    if "/articles/" not in gnews_link:
        return None
    article_id = gnews_link.rstrip("/").split("/articles/")[1].split("?")[0]
    try:
        page = get(gnews_link)
        sig = re.search(r'data-n-a-sg="([^"]+)"', page)
        stamp = re.search(r'data-n-a-ts="([^"]+)"', page)
        if not sig or not stamp:
            return None
        inner = json.dumps([
            "garturlreq",
            [["X", "X", ["X", "X"], None, None, 1, 1, "US:en", None, 1,
              None, None, None, None, None, 0, 1],
             "X", "X", 1, [1, 1, 1], 1, 1, None, 0, 0, None, 0],
            article_id, int(stamp.group(1)), sig.group(1),
        ])
        payload = json.dumps([[["Fbv4je", inner, None, "generic"]]])
        resp = get(GNEWS_RPC, data=urllib.parse.urlencode({"f.req": payload}).encode())
    except Exception:
        return None

    found = re.search(r'https?://(?!news\.google)[^\\"\s]+', resp)
    if not found:
        return None
    url = found.group(0)
    host = urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")
    if not host or any(host.endswith(b) for b in BLOCKED):
        return None
    return url


def body_text(page):
    page = re.sub(r"(?is)<(script|style|nav|header|footer|svg|aside|form|figure)\b.*?</\1>",
                  " ", page)
    page = re.sub(r"(?s)<[^>]+>", " ", page)
    page = html.unescape(page)
    page = re.sub(r"[ \t]+", " ", page)
    page = re.sub(r"\n\s*\n+", "\n", page).strip()
    return page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default=os.path.join(STATE, "candidates.json"))
    ap.add_argument("--out", default=os.path.join(STATE, "articles.json"))
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--sleep", type=float, default=1.5)
    args = ap.parse_args()

    rows = json.load(open(args.src))[: args.limit]
    out, no_url, thin = [], 0, 0

    for row in rows:
        url = resolve(row["gnews_link"])
        time.sleep(args.sleep)
        if not url:
            no_url += 1
            continue
        try:
            text = body_text(get(url))
        except Exception:
            no_url += 1
            continue
        if len(text) < MIN_BODY:
            thin += 1
            continue
        row["url"] = url
        row["body"] = text[:MAX_BODY]
        out.append(row)

    json.dump(out, open(args.out, "w"), indent=1)
    print(f"tried        {len(rows)}")
    print(f"no url/fetch {no_url}")
    print(f"body too thin {thin}")
    print(f"readable     {len(out)} -> {args.out}")


if __name__ == "__main__":
    main()
