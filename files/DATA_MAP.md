# DATA_MAP.md
## Project directory index — abigcloud.com

*abigcloud.com covers data centers broadly, focused on Middle Tennessee. Quid-Pro-NO
(Meta / Gallatin / the IDB) is one deep dive hosted on it, not the site's purpose.*

*Rewritten 2026-08-17 against the tree as it actually exists. The previous version
described `www/`, five site codebases, and a repo named `quid-pro-no`. None of that is
true any more.*

---

**NAVIGATION RULE — READ THIS FIRST**

Do not explore speculatively. Ingest files on an as-needed basis: when the subject of an
entry below comes up in the work.

When directed to a directory, read its `README.md` before touching any file. If it has no
`README.md`, copy `files/DIR_README_TEMPLATE.md` in and customise it. When directed to a
specific file, read the directory `README.md` first, then the file.

**Exempt from the README rule** — machine-generated directories nobody navigates by hand:
`saved_sites/*_files/`, build output and dependencies (`web/dist/`, `.astro/`,
`node_modules/`, `files/venv/`, `__pycache__/`), and empty directories. Also exempt:
uniform per-entity subdirectories described by their parent, such as each
`sumner_county/sumner_entities/<entity>/memory/`.

---

## One repository, one website

Everything lives in **`github.com/kissmyfix/abigcloud`**. There is no second repo.

- The website is **`web/`**. It is the *only* site; earlier versions and an
  unshipped prototype were deleted 2026-08-17.
- Everything else in this tree is the research the site was built from.
- The repo was called `quid-pro-no` before the two projects merged. GitHub still redirects
  the old name. It is one repo that was renamed, not two things.

**Publishing:** `cd web && npm run publish && git push`. See "Site" below.

---

## Directories

| Directory | What it is |
|---|---|
| `web/` | **The live website.** Astro, deployed to GitHub Pages by an Action on push to `main`. Custom domain via `web/public/CNAME`. |
| `web/content/` | **Every site page, edited directly.** Folder structure *is* URL structure: `content/tennessee/fisk.md` → `/tennessee/fisk/`. What you edit is what ships. |
| `web/scripts/` | `build-citations.mjs` resolves `@/` citations and rebuilds the source index; `watch-content.mjs` re-runs it on save. |
| `web/content/sources/` | **Generated, never hand-edited.** One page per cited text document, rendered in the site's layout: `.md` formatted, `.txt` verbatim in `<pre>`, PDFs skipped. Written by the publish step; a document appears here the first time a page cites it. |
| `web/public/sources/` | **Generated, never hand-edited.** Cited documents copied in by the publish step so a reader clicking a citation gets the actual file. |
| `files/` | Project plumbing: this map, the README template, `bin/` (all project scripts), `venv/` (their Python environment). |
| `files/WORKFLOW.md` | **How writing reaches the site**: mdlive, what Astro does, the publish pipeline, and what to check when it breaks. |
| `files/bin/mdlive.py` | Brandon's browser markdown editor. |
| `files/cold-read/` | **The cold read** — the test of whether this project explains itself to a session that starts with nothing. `PROTOCOL.md` (procedure and scoring), `prompt.md` (the ten questions, verbatim), `answer-key.md` (the agreed baseline, stamped with the commit it is valid for), `runs/` (one file per run). |
| `files/bin/cold-read.sh` | Sets up a cold read: warns if the answer key is stale, stamps a run file, prints the agent prompt. `--check` to see whether the key has gone stale. |
| `files/bin/whos-editing.sh` | Exits non-zero if mdlive has a given file open. Run it before any scripted edit to a content file; writing behind him races his autosave. |
| `files/bin/ship.sh` | **Publishing, in one command.** Build, commit, push, wait on the Action, confirm the live pages serve 200. On a failed deploy it prints the failing step and the log lines that explain it, via `gh`. Use it instead of running the steps by hand. |
| `files/bin/` | Every project script — PDF extraction and profiling, whisper transcription, Comptroller CSV builders and verifiers, the parcel-assessment parser. Run with `files/venv/bin/python`. |
| `.claude/agents/` | Subagent definitions. `archive-researcher.md` sweeps large `derived/` documents and returns line-anchored quotes, keeping the raw text out of the main conversation. |
| `memory/` | Working memory. **Gitignored — private.** `MEMORY.md` (theories/findings), `master-reference-w5h.md`, `PINBOARD.md`, `TIMELINE.md` (two-lane evidence timeline), `UNICORN.md`, `dual-status-contradiction.md` (the public-agency/private-corporation workup), `brandon-schema.md`, `site-work-conventions.md` (standing conventions for working on the site itself), `site-data-salvage/`. |
| `memory/brandon-voice-notes.md` | Every `@c` annotation Brandon wrote into the draft, verbatim, resolved and open alike. Voice reference and his reasoning in his own words. Never cleaned up; a note deleted from the draft stays here. |
| `memory/site-data-salvage/` | Rescued from the deleted prototype: `records.ts` (27 entity records), `events.json` (42 timeline events), `SITE_PLAN-archived.md` (the wiki design). Compiled artifacts, not sources. |
| `angles/` | Article raw material: theory narratives, framings, rebuttals in reserve, the citation worklist, and `visualization-queue.md` (the data-story backlog, moved out of the public FAQ 2026-08-18). **Gitignored** — pre-publication strategy, withheld pending the AI-disclosure rewrite. |
| `monologues/` | Brandon's pen: personal writing, old drafts, voice reference. **Nothing reads from it.** Not part of any pipeline. **Gitignored.** Do not edit unless directed there. |
| `reference/` | Public-facing glossary — plain-language explainers. Several are published as site pages. |
| `the_players/` | Profiles of individuals in scope, one flat `name.md` each. Documents live where they came from; each profile links to what concerns it. |
| `sumner_county/` | City and county records. |
| `sumner_county/gallatin_idb_data/` | IDB minutes, agendas, Secretary of State filing history. |
| `sumner_county/gallatin_council_meetings/` | Council packets from gallatintn.gov. |
| `sumner_county/sumner_entities/` | One directory per company with a Sumner County PILOT, 2015–2026, each with its own `memory/MEMORY.md`. |
| `state_of_tennessee/tn_annotated_code/` | Statutes (T.C.A.), plus SB 708 as introduced, as enacted, and its fiscal memo. |
| `state_of_tennessee/tn_comptroller_pilot_reports/` | Comptroller PILOT reports by county. `sumner_county/derived/woolhawk-pilot-reporting.md` is the parsed finding. |
| `state_of_tennessee/state_audits/` | Comptroller-filed annual audits, one directory per legal entity. |
| `state_of_tennessee/tn_professional_licenses/` | State licence records for the CPAs who sign this investigation's documents. Poole (auditor of the Gallatin IDB, the HHFB and Westmoreland's IDB) carries a public **"Has Been Disciplined"** alert; Young prepares the IDB's and the Shalom Zone's 990s. Captured by hand — the state tool is behind a CAPTCHA. |
| `state_of_tennessee/tn_property_assessments/` | Parcel records from the state viewer. |
| `usa_federal/irs_990_data/` | IRS filings. `gallatin_idb/` holds 2020–2024 plus the verified dataset; `verify-990.py` checks it. |
| `usa_federal/tva/` | TVA material. |
| `podcasts/` | `transcripts/` (24 whisper transcripts, 13.2 hours), `mp3s/` (**gitignored**, 1.2GB), `manifest.csv`. |
| `web_articles/` | News coverage saved as text with a provenance header: source, headline, byline, date, original URL, archive URL, retrieval date, and why it was saved. |
| `visualizations/` | Draft charts, layout ideas, and images used in articles. |
| `saved_sites/` | Whole-page browser saves, kept against loss or change. **Gitignored.** |

---

## Project-wide conventions

**`derived/` — machine-generated, regenerable, never hand-edited.**
Any directory holding source documents may hold a `derived/`. Everything in it was produced
by a script from the sources in its parent: page-anchored `.txt` from
`files/bin/pdf-extract.py`, the `pdf-index.csv` extraction writes, parsed `.json`, built
master `.csv`.

- Sources stay in the parent. Derived artifacts go in `derived/`. A machine-made file
  sitting next to its own sources is misfiled.
- Never hand-correct a file in `derived/`. Fix the script and re-run. A hand edit is
  silently destroyed on the next run.

**Naming.** Underscores in directory names, dashes in file names, never spaces or special
characters. Scripts live in `files/bin/`.

**Custom filenames are a clue.** Digging through 200-page packets at speed, Brandon names
a file for the reason he saved it. Read those prefixes as a pointer, not clutter. Never
rename or delete one without carrying its meaning somewhere durable.

**Provenance headers on saved articles.** Anything pulled from the web gets SOURCE,
HEADLINE, BYLINE, DATE, URL, ARCHIVE, RETRIEVED, and WHY SAVED at the top. The publish
step reads those headers to build the site's source index, so the format is load-bearing.

---

## What is gitignored, and why

The repo is public. These stay local:

| Path | Why |
|---|---|
| `monologues/`, `memory/`, `.remember/` | Working notes and drafts, not evidence |
| `angles/` | Pre-publication strategy, including rebuttals held in reserve |
| `CLAUDE.md`, `.claude/` | Agent operating instructions |
| `files/voice-and-method-web.md` | Voice analysis built from private chat logs |
| `podcasts/mp3s/`, `saved_sites/` | Large binaries; transcripts and text are published instead |
| `web/{dist,node_modules,.astro}/` | Build output |

Withheld deliberately, not hidden — revisit each when the AI-disclosure policy is rewritten.
