#!/usr/bin/env python3
"""Fetch the beats from Google News RSS, dedupe, write candidates.json.

    files/venv/bin/python files/bin/headline-bot/sweep.py [--days 21]

Dedupe runs at three levels:
  1. exact title, within this run
  2. story cluster, within this run   -- one headline per underlying story
  3. story cluster, against state/seen.json -- never rework a story already worked

A story cluster is a normalized key built from the significant words in the headline.
Two headlines about the same council vote from two outlets collapse to one.
"""
import argparse, datetime, email.utils, json, os, re, sys, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from beats import BEATS, NOISE  # noqa: E402

STATE = os.path.join(HERE, "state")
UA = "Mozilla/5.0 (X11; Linux x86_64) abigcloud-headline-bot/1"

STOP = set("""a an the and or of for in on at to from with as by is are was were be been
this that these those it its their his her our your new more most some any not no than then
after before during over under out up down about into onto near amid says say said could
would should will can may might who what when where why how tn tennessee""".split())


def cluster_key(title: str) -> str:
    words = re.findall(r"[a-z0-9]+", title.lower())
    sig = sorted(w for w in words if w not in STOP and len(w) > 3)
    return " ".join(sig[:6])


def fetch(query: str) -> bytes:
    url = ("https://news.google.com/rss/search?q="
           + urllib.parse.quote(query)
           + "&hl=en-US&gl=US&ceid=US:en")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()


def parse(raw: bytes, tier: str, slug: str, cutoff):
    out = []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return out
    for item in root.findall(".//item"):
        raw_title = (item.findtext("title") or "").strip()
        if not raw_title:
            continue
        title, _, outlet = raw_title.rpartition(" - ")
        if not title:
            title, outlet = raw_title, ""
        try:
            when = email.utils.parsedate_to_datetime(item.findtext("pubDate") or "")
        except (TypeError, ValueError):
            continue
        if when < cutoff:
            continue
        low = title.lower()
        if any(n in low for n in NOISE):
            continue
        out.append({
            "tier": tier, "beat": slug,
            "title": title.strip(), "outlet": outlet.strip(),
            "date": when.date().isoformat(),
            "gnews_link": item.findtext("link") or "",
            "cluster": cluster_key(title),
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=21)
    ap.add_argument("--out", default=os.path.join(STATE, "candidates.json"))
    args = ap.parse_args()

    cutoff = (datetime.datetime.now(datetime.timezone.utc)
              - datetime.timedelta(days=args.days))

    seen_path = os.path.join(STATE, "seen.json")
    seen = set()
    if os.path.exists(seen_path):
        seen = {row["cluster"] for row in json.load(open(seen_path))}

    rows, fetched = [], 0
    for tier, slug, query in BEATS:
        try:
            rows += parse(fetch(query), tier, slug, cutoff)
            fetched += 1
        except Exception as exc:                       # one dead beat must not kill the run
            print(f"  beat {slug}: {exc}", file=sys.stderr)

    kept, titles, clusters = [], set(), set()
    dropped_seen = dropped_dupe = 0
    for row in rows:
        if row["title"] in titles:
            dropped_dupe += 1
            continue
        if row["cluster"] in clusters:
            dropped_dupe += 1
            continue
        if row["cluster"] in seen:
            dropped_seen += 1
            continue
        titles.add(row["title"])
        clusters.add(row["cluster"])
        kept.append(row)

    kept.sort(key=lambda r: r["date"], reverse=True)
    os.makedirs(STATE, exist_ok=True)
    json.dump(kept, open(args.out, "w"), indent=1)

    print(f"beats fetched   {fetched}/{len(BEATS)}")
    print(f"items in window {len(rows)}")
    print(f"dropped dupes   {dropped_dupe}")
    print(f"dropped worked  {dropped_seen}")
    print(f"candidates      {len(kept)} -> {args.out}")


if __name__ == "__main__":
    main()
