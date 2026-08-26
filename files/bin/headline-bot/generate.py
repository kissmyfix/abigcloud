#!/usr/bin/env python3
"""Run each readable article past the model and queue the pairs it does not reject.

    files/venv/bin/python files/bin/headline-bot/generate.py                # Claude API
    files/venv/bin/python files/bin/headline-bot/generate.py --backend cli  # local `claude`

The API backend needs ANTHROPIC_API_KEY (or an `ant auth login` profile). The cli backend
shells out to the `claude` binary already authenticated on this machine, so the bot can be
run and graded before any key exists.

prompt.md is the whole method and is sent as a cached system block: it is identical on every
call, so it is billed once per run rather than once per article.
"""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state")
MODEL = "claude-opus-5"

SCHEMA = {
    "type": "object",
    "properties": {
        "verdict":   {"type": "string", "enum": ["pair", "reject"]},
        "reason":    {"type": "string"},
        "corrected": {"type": "string"},
        "findings":  {"type": "array", "items": {"type": "string"}},
        "quote":     {"type": "string"},
    },
    "required": ["verdict", "reason", "corrected", "findings", "quote"],
    "additionalProperties": False,
}


def article_block(row):
    return (f"HEADLINE: {row['title']}\n"
            f"OUTLET: {row['outlet']}\n"
            f"DATE: {row['date']}\n\n"
            f"BODY:\n{row['body']}")


def via_api(system, rows):
    import anthropic
    client = anthropic.Anthropic()
    for row in rows:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=4000,
            system=[{"type": "text", "text": system,
                     "cache_control": {"type": "ephemeral", "ttl": "1h"}}],
            output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
            messages=[{"role": "user", "content": article_block(row)}],
        )
        text = next(b.text for b in resp.content if b.type == "text")
        yield row, json.loads(text)


def via_cli(system, rows):
    for row in rows:
        prompt = (system
                  + "\n\n---\n\n" + article_block(row)
                  + "\n\n---\n\nReturn ONLY the JSON object. No prose, no code fence.")
        proc = subprocess.run(
            ["claude", "-p", prompt, "--model", MODEL],
            capture_output=True, text=True, timeout=300,
        )
        raw = proc.stdout.strip()
        start, end = raw.find("{"), raw.rfind("}")
        if start < 0 or end < 0:
            yield row, {"verdict": "reject", "reason": "model returned no JSON",
                        "corrected": "", "findings": [], "quote": ""}
            continue
        yield row, json.loads(raw[start:end + 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["api", "cli"], default="api")
    ap.add_argument("--in", dest="src", default=os.path.join(STATE, "articles.json"))
    ap.add_argument("--limit", type=int, default=25)
    args = ap.parse_args()

    system = open(os.path.join(HERE, "prompt.md")).read()
    rows = json.load(open(args.src))[: args.limit]
    runner = via_api if args.backend == "api" else via_cli

    pairs, rejects, unverified = [], [], 0
    for row, out in runner(system, rows):
        if out.get("verdict") != "pair":
            rejects.append({"title": row["title"], "outlet": row["outlet"],
                            "reason": out.get("reason", "")})
            print(f"reject  {row['title'][:70]}\n        {out.get('reason','')}")
            continue

        # The quote must actually appear in the body. A quote the article does not
        # contain means the model wrote from somewhere other than the article.
        quote = (out.get("quote") or "").strip()
        if quote and quote.lower() not in row["body"].lower():
            unverified += 1
            rejects.append({"title": row["title"], "outlet": row["outlet"],
                            "reason": "quote not found in body; dropped"})
            print(f"DROP    {row['title'][:70]}\n        quote not in article body")
            continue

        pairs.append({
            "cluster": row["cluster"], "date": row["date"], "outlet": row["outlet"],
            "url": row["url"], "original": row["title"],
            "corrected": out["corrected"], "operative": out.get("reason", ""),
            "findings": out.get("findings", []), "quote": quote,
        })
        print(f"PAIR    {row['title'][:70]}\n     +  {out['corrected']}")

    os.makedirs(STATE, exist_ok=True)
    json.dump(pairs, open(os.path.join(STATE, "queue.json"), "w"), indent=1)
    json.dump(rejects, open(os.path.join(STATE, "rejects.json"), "w"), indent=1)

    total = len(pairs) + len(rejects)
    rate = (100.0 * len(pairs) / total) if total else 0.0
    print(f"\nread {total}  pairs {len(pairs)}  rejected {len(rejects)}"
          f"  quote-failed {unverified}  pass rate {rate:.0f}%")
    print("A pass rate much above 10% means triage has drifted. Check for honest headlines"
          " being corrected.")


if __name__ == "__main__":
    main()
