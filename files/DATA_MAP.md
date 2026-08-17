# DATA_MAP.md
## Project Directory Index | The Data Center Reckoning

---

**NAVIGATION RULE — READ THIS FIRST:**
Do not explore any directory speculatively. Ingest files on an as needed basis; ie: When the subject of a DATA_MAP.md comes up as part of the current discussion.
When directed to a directory, read its `README.md` if it exists before touching any files.
If the directory does not contain a `README.md` copy `files/DIR_README_TEMPLATE.md` into the directory and customize to suit its purpose.
When directed to work on a specific file, read the directory `README.md` first, then the file.

**Exempt from the README rule** — machine-generated directories nobody navigates by hand:
browser-saved `saved_sites/*_files/` asset folders, build output and dependencies
(`www/*/dist/`, `.astro/`, `node_modules/`, `files/venv/`, `__pycache__/`), and empty
directories. Also exempt: uniform per-entity subdirectories whose shape is already described
by the parent, such as each `sumner_entities/<entity>/memory/`. These are described by their
parent's README, not their own.

---

Directories are now grouped by the level of government (or kind of material) they belong to.
All paths in project docs are written relative to the project root.

| Directory | One-Line Description |
|---|---|
| `files/` | project plumbing: this map, the README template, the AI-toolchain changelog, `bin/` (all project scripts) and `venv/` (their Python environment) |
| `files/bin/` | Every project script — PDF extraction/profiling, whisper transcription, the Comptroller master-CSV builders and verifiers, the parcel-assessment parser, the prompt-log hook. Run them with `files/venv/bin/python` |
| `files/venv/` | The project's permanent Python environment (`pdfplumber`, `pandas`, `openpyxl`). Machine-generated, disposable, rebuildable — see `files/bin/README.md` |
| `files/prompt_log/` | Append-only monthly capture of every session prompt, written by the `UserPromptSubmit` hook — chronology only, not citable, not voice reference |
| `files/ai-toolchain-changelog.md` | Deliberate changes to the Claude Code setup (settings, plugins, hooks, memory systems) — each entry carries its own verification checks and reversal steps |
| `.claude/skills/` | Project-local skills — instructions Claude loads on its own when a task matches. `extract-pdf-source/` (reading, quoting, and parsing source PDFs; pairs with `files/bin/pdf-extract.py` and `pdf-profile.py`) and `investigative-journalist/` (investigation context, voice, and evidence map; the snapshots under its `references/` are superseded by `memory/master-reference-w5h.md` and `memory/TIMELINE.md`) |
| `memory/` | Claude's working memory — `MEMORY.md` (theories/findings), `master-reference-w5h.md` (the who/what/when/where/why/how orientation file), `PINBOARD.md` (lightbulb capture), `TIMELINE.md` (two-lane evidence timeline), `UNICORN.md` (outlier scorecard), `dual-status-contradiction.md`, `brandon-schema.md` (collaborator profile) |
| `angles/` | Article raw material — full theory narratives, framings, rebuttals, planned-section specs (textual counterpart to `visualizations/`); theory STATUS stays in `memory/MEMORY.md` |
| `monologues/` | Brandon's captured voice and drafts — do not edit, do not read unless Brandon directs you there. **Authorship of the eight files added 2026-07-29 is unresolved; not safe as voice reference until sorted — see its README** |
| `the_players/` | Profiles of individuals in scope — one flat `name.md` each, no subdirectories. Documents live where they came from; each profile links to the ones that concern it |
| `saved_sites/` | Whole-site Firefox saves due to concern over loss or change | 
| `web_articles/` | Copy-pasted articles from web sources which are snippets or content specific |
| `podcasts/` | Podcast episodes (`mp3s/`) - .mp3 audio files waiting to be parsed, whisper transcripts (`transcripts/`) - parsed podcast textual transcripts, `manifest.csv` - an account of podcast and episode specific source |
| `sumner_county/` | Everything chartered at the city/county level: |
| `sumner_county/gallatin_idb_data/` | Gallatin IDB meeting minutes, agendas, and subject matter specific to the IDB |
| `sumner_county/gallatin_council_meetings/` | PDFs from gallatintn.gov — public documents tied to the IDB, entities, and the_players |
| `sumner_county/gallatin_electric_utility/` | GDE service policies and rate sheets (2016–present) |
| `sumner_county/sumner_entities/` | All known corporations with Sumner County PILOT agreements, 2015–2026; one directory per entity with its own `memory/MEMORY.md` |
| `state_of_tennessee/` | State-level statutes and records |
| `state_of_tennessee/tn_annotated_code/` | Primary statutory text (T.C.A.) |
| `state_of_tennessee/tn_comptroller_pilot_reports/` | Comptroller PILOT reports by county (`sumner_county/`, `hamilton_county/`, `gibson_county/`, statewide in `tn_comptroller_archived/`)|
| `state_of_tennessee/state_audits/` | Comptroller-filed annual audits, one directory per legal entity (`gallatin_city/`, `gallatin_idb/`, `gallatin_hhfb/`, `westmoreland_city/`, `westmoreland_idb/`, `portland_city/`, `sumner_county/`) plus `investigations/`; each has a `derived/` of page-anchored text |
| `state_of_tennessee/tn_sos_filings/` | Secretary of State corporate records (existence, registered agents, status changes) for entities and individuals in scope — filed by source, linked from `the_players/` by aboutness. The IDB's own SOS history stays in `sumner_county/gallatin_idb_data/` |
| `state_of_tennessee/tn_property_assessments/` | PDFs from the Tennessee parcel viewer; `derived/sumner-assessments.json` is the parsed dataset |
| `usa_federal/` | Federal-level records: |
| `usa_federal/irs_990_data/` | All available Gallatin IDB 990 filings (2020–present); `gibson_county_idb/` comparison filings |
| `usa_federal/tva/` | TVA material (in-lieu-of-tax payments, power agreements) |
| `reference/` | Public-facing glossary — plain-language explainers (IDB, PILOT, title-transfer, 501(c)(4) vs instrumentality...), encyclopedia voice, destined for the site |
| `visualizations/` | Draft/prototype charts and layout ideas not yet moved to `www/`; also holds two source PDFs (county budget, Gallatin civics calendar) that are inputs, not output |
| `www/` | Website roots |

---

## Project-wide conventions

**`derived/` — machine-generated, regenerable, never hand-edited.**
Any directory holding source documents may hold a `derived/` subdirectory. Everything in
it was produced by a script from the sources in its parent: page-anchored `.txt` from
`files/bin/pdf-extract.py`, the `pdf-index.csv` that extraction writes, parsed `.json`
datasets, and built master `.csv` files.

- Sources stay in the parent directory. Derived artifacts go in `derived/`. A machine-made
  file sitting next to its own sources is misfiled.
- Never hand-correct a file in `derived/`. Fix the script, re-run it. A hand edit is
  silently destroyed on the next run, and a `derived/` file that cannot be reproduced from
  its source is not evidence of anything.
- Derived text is a reading and searching aid. **Quote from the source document**, and
  cite the source, not the extraction.
- `derived/` is not exempt from the README rule when it holds a dataset others join
  against — say what generated it and how to regenerate it.

Current `derived/` directories: all eight under `state_audits/`, plus `tn_annotated_code/`,
`tn_comptroller_pilot_reports/` (master CSVs), `tn_comptroller_pilot_reports/sumner_county/`,
`tn_property_assessments/`, `gallatin_idb_data/`, `gallatin_council_meetings/` (which also
holds an `ocr/` of re-OCR'd packets), and `web_articles/`.

**Scripts live in `files/bin/`.**
Not in the data directory they serve. A script resolves its data directory from its own
location (`Path(__file__).resolve().parent.parent.parent` is the project root), so it runs
from anywhere. Dashes in script names; name them after what they build
(`build-…` / `parse-…` / `verify-…`).

No exceptions. Every project script is in `files/bin/`.

**Provenance files, aboutness links.**
A document is filed by where it came from — that question has exactly one answer. What it is
*about* has many, so it is expressed as links from the files that care: a profile in
`the_players/`, a theory in `angles/`, an entity's own `memory/MEMORY.md`. When a document
seems to belong in two places, it belongs in neither by subject — file it by source and link
it twice. Significance is a ranking, not an address.

**Naming.** Underscores in directory names, dashes in file names, never spaces or special
characters. (`saved_sites/` predates this and its Firefox-generated folders violate it;
they are browser output, left alone deliberately.) As of 2026-07-29 the rest of the tree is
clean: the podcast audio and transcripts, which had carried publishers' titles verbatim with
spaces and curly apostrophes, were slugified — the publisher's wording is preserved in
`podcasts/manifest.csv`, which is the old-name lookup.

Lowercase throughout. **A dated document leads with its date, ISO-ordered, most specific
component the document actually claims:**

```
YYYY-MM-DD-<body-or-source>-<what-it-is>.pdf   2020-05-12-council-committee-agenda.pdf
YYYY-MM-<what-it-is>.pdf                       2026-07-meetings-public-notice.pdf
YYYY-<what-it-is>.pdf                          2019-gallatin-annual-financial-report.pdf
```

Year-first so the directory sorts chronologically, which is how a paper trail is read. The
date is the meeting's or the document's own date, taken from the document, not from
whenever it was downloaded. Undated documents lead with the source or subject instead
(`sumner-assessment-woolhawk.pdf`).

**Name the document for what it is, not for what you were looking for in it.** Two files in
`gallatin_council_meetings/` were named for the hunt rather than the contents and both were
wrong about themselves: the file once called `gnrc-plan-2018.pdf` is a June 19 2018 council
agenda packet with the GNRC plan buried at p.58, now filed as
`2018-06-19-city-council-agenda.pdf`; the one called `2022-budget.pdf` is the FY2022 annual
financial report and not a budget, now `2022-gallatin-annual-financial-report.pdf`. That
directory's README keeps the full old-name → new-name table.

**But Brandon's own custom filenames are evidence.** Working fast through a 200-page packet
he names the file for the reason he saved it (`the-most-importanat-yet-…`), so a later
session knows what to look for. That prefix is a pointer, not clutter. Before renaming one
to the scheme, carry what it was telling you into `memory/MEMORY.md`, pointed at the new
filename. Rename only after the meaning has somewhere durable to live.

---

**Important files:**
- `CLAUDE.md` — durable working rules; read at session start
- `README.md` — the public-facing front door for the git repo (`quid-pro-no` on GitHub)
- `memory/MEMORY.md` — working theories, framings, and editorial instincts
- `memory/PINBOARD.md` — lightbulb moments captured live; review at investigation-session start
- `files/DATA_MAP.md` — this file
- `files/DIR_README_TEMPLATE.md` — template for new directory READMEs
- `files/bin/verify-docs-paths.py` — checks that every path named in this file, `CLAUDE.md`,
  `README.md`, and every directory README still resolves. Run it after moving or renaming
  anything; it exits non-zero on a broken reference. Names recorded as history (`formerly
  x.pdf`, old-name → new-name tables) are recognized as provenance and skipped
