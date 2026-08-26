# headline-bot v1

Pulls Tennessee data center and incentive headlines, keeps only the ones whose own article
contradicts them, and writes a corrected headline in Brandon's voice for review.

    files/bin/headline-bot/run.sh            # Claude API, needs ANTHROPIC_API_KEY
    files/bin/headline-bot/run.sh --cli      # local `claude` binary, no key needed

Nothing publishes. Everything lands in `state/queue.json` to be graded by hand.

## The method lives in prompt.md

`prompt.md` is the whole editorial method, derived from three hand-graded sets in
`memory/brandon-voice-notes.md`. Change it there, not in the code. The rules it encodes,
each one from a real failure:

- Triage rejects by default; topic match is not eligibility, and zero pairs is a good run
- The `+` line must be supported by the body of the same article, nothing outside it
- Aim at the government's framing, not the corporation's
- The single-word swap beats a rewrite
- Name the party an exception protects; name concerns as pictures, not categories
- Count the steps between a vote and an effect
- A vote is not an outcome
- Length near the original; going long costs a grade

## Pipeline

| Stage | Script | Writes |
|---|---|---|
| Sweep | `sweep.py` | `state/candidates.json` |
| Extract | `extract.py` | `state/articles.json` |
| Generate | `generate.py` | `state/queue.json`, `state/rejects.json` |

**sweep.py** hits 17 Google News RSS beats in three tiers (statewide, Middle Tennessee,
Quid-Pro-NO mechanisms), no API key required. Beats live in `beats.py`. Geographic queries
carry a topic term, because "Sumner County Tennessee" alone returns lottery results.

**extract.py** resolves each headline to its publisher URL through DuckDuckGo's HTML
endpoint, because Google News RSS links are opaque redirects that need JavaScript. Blocked
domains are listed in `beats.py`; an article that cannot be read is dropped before it
reaches the model.

**generate.py** sends one article per call with `prompt.md` as a cached system block, and
takes back structured JSON. Any pair whose supporting quote does not appear verbatim in the
article body is dropped, which is the guard against an invented finding.

## Dedupe

`state/seen.json` holds the story cluster of every headline already worked, seeded with the
21 from sets one through three. A cluster is the significant words of a headline, sorted, so
two outlets covering one council vote collapse to a single candidate. Clusters are deduped
within a run and against `seen.json`, so a story is never worked twice.

Add worked clusters to `seen.json` as pairs are approved.

## Reading the output

The last line of a run prints the pass rate. **A high rejection rate is the desired state.**
Roughly 5% passed on the hand-graded sweep that produced this bot. A run passing much above
10% has drifted back to correcting headlines that were already honest, and the fix is
triage in `prompt.md`, not the code.

## Not built yet

The GitHub Actions cron, the PR gate Brandon merges from his phone, the approved-pool JSON,
the ticker component on the landing page, and the overflow archive page.
