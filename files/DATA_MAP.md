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
Build output and dependencies (`web/dist/`, `.astro/`,
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
| `README.md` | The repository's front door, and the only orientation file a stranger arriving from GitHub will read. It explains why the archive is public, then walks the evidence by jurisdiction. Public-facing: when a fact changes, this file has to change with it. |
| `.remember/` | **Gitignored.** Session-continuity notes written by the Remember plugin, not by hand: `.remember/now.md` (the live buffer), plus dailies, a seven-day `recent`, rotated archives and a `core-memories` file beside it. Injected automatically at session start, so there is normally no reason to open it. Grep the rotated archives only when a question reaches further back than what was injected. Not evidence, and never cited. |
| `web/` | **The live website.** Astro, deployed to GitHub Pages by an Action on push to `main`. Custom domain via `web/public/CNAME`. |
| `web/content/` | **Every site page, edited directly.** Folder structure *is* URL structure: `content/tennessee/fisk.md` → `/tennessee/fisk/`. What you edit is what ships. |
| `web/scripts/` | `build-citations.mjs` resolves `@/` citations and rebuilds the source index; `watch-content.mjs` re-runs it on save. |
| `web/content/sources/` | **Generated, never hand-edited.** One page per cited text document, rendered in the site's layout: `.md` formatted, `.txt` verbatim in `<pre>`, PDFs skipped. Written by the publish step; a document appears here the first time a page cites it. |
| `web/assets/` | Site images. `banners/` for page heroes referenced from frontmatter, `img/` for images held for future use. A one-page image colocates with its page instead. Not evidence, and unreachable by `@/`. |
| `web/src/` | The Astro site: layouts, components, content config, styles. Hand-edited. |
| `web/content/reference/` | Standing explainers a reader can be sent to mid-article rather than having the argument stop to define a term: what an IDB is, what a PILOT is, the title-transfer mechanism, 501(c)(4) versus instrumentality, confirmed falsehoods, open threads. Edited like any other page. |
| `podcasts/transcripts/` | Whisper transcripts of every episode in `manifest.csv`, one `.txt` each. |
| `sumner_county/gallatin_electric_utility/` | Gallatin Department of Electricity rate sheets, 2016–2026, standardised on June. The ratepayer-cost instrument. |
| `.claude/skills/` | Project-local skills. `investigative-journalist/` defines the five working modes. |
| `web/public/sources/` | **Generated, never hand-edited.** Cited documents copied in by the publish step so a reader clicking a citation gets the actual file. |
| `files/` | Project plumbing: this map, the README template, `bin/` (all project scripts), `venv/` (their Python environment). |
| `files/prompt-log-hashes.md` | Published SHA-256 per closed month of the private prompt log. The log is not in this repo; the hash and the date of the commit that added it are what make the log's age provable. Written by `files/bin/anchor-prompt-log.sh`. |
| `files/RESEARCH_SOURCES.md` | The websites this investigation returns to, and the exact URL pattern into each: TPAD parcel lookups with their jurisdiction codes, the TN SOS and Comptroller searches, CIS capstone originals, the Gallatin CivicEngage search and Agenda Center anchors, ProPublica per-EIN. |
| `files/WORKFLOW.md` | **How writing reaches the site**: mdlive, what Astro does, the publish pipeline, and what to check when it breaks. |
| `files/bin/mdlive.py` | The browser markdown editor used to write every page. |
| `files/ai-toolchain-changelog.md` | Deliberate changes to the Claude Code setup — settings, plugins, hooks, memory systems. One entry per change session, newest first, each carrying its own verification checks and reversal steps. Not investigation content. |
| `files/cold-read/` | **Gitignored 2026-08-19**, with `CLAUDE.md` and `.claude/`, as agent-operating material pending the AI-disclosure rewrite. **The cold read** — the test of whether this project explains itself to a session that starts with nothing. `PROTOCOL.md` (procedure and scoring), `prompt.md` (the thirteen questions, verbatim), `answer-key.md` (the agreed baseline, stamped with the commit it is valid for), `runs/` (one file per run). |
| `files/hooks/` | Git hooks kept in the repo rather than in `.git/hooks/`, which is not versioned. `pre-commit` refuses a commit carrying a private person's details, a credential, or documentation pointing at a file that does not exist. |
| `files/bin/install-hooks.sh` | Points git at `files/hooks/` by setting `core.hooksPath`, and seeds the deny list. Run once per clone. |
| `files/bin/cold-read.sh` | Runs a cold read end to end: warns if the answer key is stale, builds the sandbox and verifies the key is absent from it, stamps a run file, then launches the agent as its own `claude` process rooted in the sandbox and saves its report beside the run file. A subagent would inherit the live project's `CLAUDE.md` and defeat the control, which is why the script does not use one. `--check` to see whether the key has gone stale. |
| `files/bin/whos-editing.sh` | Exits non-zero if mdlive has a given file open. Run it when it is unclear whether he is mid-sentence in a file. A file merely being open is fine; what matters is whether his buffer is dirty. See the mdlive rule in `CLAUDE.md`. |
| `files/bin/ship.sh` | **Publishing, in one command.** Build, commit, push, wait on the Action, confirm the live pages serve 200. On a failed deploy it prints the failing step and the log lines that explain it, via `gh`. Use it instead of running the steps by hand. |
| `files/bin/` | Every project script — PDF extraction and profiling, whisper transcription, Comptroller CSV builders and verifiers, the parcel-assessment parser. Run with `files/venv/bin/python`. |
| `.claude/agents/` | Subagent definitions. `archive-researcher.md` sweeps large `derived/` documents and returns line-anchored quotes, keeping the raw text out of the main conversation. |
| `.github/workflows/deploy.yml` | The GitHub Action that builds `web/` and publishes to Pages on every push to `main`. `ship.sh` waits on this run and reads its log when it fails. |
| `LICENSE`, `LICENSE-MIT`, `LICENSE-CC-BY-4.0` | `LICENSE` sorts the repository into four kinds of material and gives the terms for each: original writing CC BY 4.0, original code MIT, public records not copyrightable, third-party material under its own terms. The two full licence texts sit beside it. |
| `memory/` | Working memory. **Gitignored — private.** `MEMORY.md` is the entry point: scope, settled findings, working theories, and an index to the rest. Findings are split by subject into `money.md`, `structure.md`, `deal.md`, `open.md`, and `method.md`, so answering one question costs one file. Alongside them: `master-reference-w5h.md` (who/what/when/where/why), `TIMELINE.md` (two-lane SAID/PAPER event chain), `PINBOARD.md` (parked leads), `UNICORN.md` (the outlier scorecard), `dual-status-contradiction.md`. Split and reorganised 2026-08-19; `memory/README.md` records what moved where. |
| `memory/citation-worklist.md` | The sourcing ledger: every claim in the article against the document that carries it, marked DONE / RESOLVED / READY / PARTIAL / GAP, plus the parked threads. **Read before assuming any published claim is sourced.** Gitignored — it is a list of what is not yet proven. |
| `memory/brandon-voice-notes.md` | Every `@c` annotation written into the draft, verbatim, resolved and open alike. Voice reference and the author's reasoning in his own words. Never cleaned up; a note deleted from the draft stays here. |
| ~~`angles/`~~ | **Removed from the project 2026-08-19.** Held the article raw material: theory narratives, framings, rebuttals in reserve, the visualization backlog, and the citation worklist that mapped every unsourced claim in the draft to the document carrying it. |
| `the_players/` | Profiles of individuals in scope, one flat `name.md` each. Documents live where they came from; each profile links to what concerns it. |
| `sumner_county/` | City and county records. |
| `sumner_county/gallatin_idb_data/` | The IDB's Secretary of State corporate history and the three TCED capstone papers. No minutes or agendas exist; the board does not publish them. |
| `sumner_county/gallatin_council_meetings/` | Council packets from gallatintn.gov, plus six dated captures of the city's own Boards and Commissions pages. `derived/ocr/` holds re-OCR'd **text** for six scanned packets; the OCR'd PDFs were removed 2026-08-19 as 65 MB of duplicated page images, regenerable with `ocrmypdf`. |
| `sumner_county/sumner_entities/` | One directory per company with a Sumner County PILOT, 2015–2026, each with its own `memory/MEMORY.md`. |
| `state_of_tennessee/` | State records: statutes, comptroller filings, audits, SOS filings, licences, parcels. |
| `state_of_tennessee/tn_annotated_code/` | Statutes (T.C.A.), plus SB 708 as introduced, as enacted, and its fiscal memo. |
| `state_of_tennessee/tn_comptroller_pilot_reports/` | Comptroller PILOT reports. Sumner County plus the statewide annual set in `tn_comptroller_archived/`; `sumner_county/derived/woolhawk-pilot-reporting.md` inside it is the parsed finding. The Gibson and Hamilton peer sets moved out of the project 2026-08-19. |
| `state_of_tennessee/state_audits/` | Comptroller-filed annual audits, one directory per legal entity. |
| `state_of_tennessee/tn_sos_filings/` | Secretary of State business-entity filings and the derived counting method behind the "roughly 400 IDBs" figure. |
| `state_of_tennessee/tn_professional_licenses/` | State licence records for the CPAs who sign this investigation's documents. Poole (auditor of the Gallatin IDB, the HHFB and Westmoreland's IDB) carries a public **"Has Been Disciplined"** alert; Young prepares the IDB's and the Shalom Zone's 990s. Captured by hand — the state tool is behind a CAPTCHA. |
| `state_of_tennessee/tn_property_assessments/` | Parcel records from the state viewer. |
| `usa_federal/` | Federal records. |
| `usa_federal/irs_990_data/` | IRS filings. `gallatin_idb/` holds 2020–2024 plus the verified dataset; `verify-990.py` checks it. `gallatin_shalom_zone/` holds 2023–2024 filings by the IDB's same 990 preparer. |
| `usa_federal/tva/` | TVA material: the FY2024 annual FOIA report and the 2025 and 2026 Chief FOIA Officer reports. Thin, and the TVA records angle is not yet worked. |
| `podcasts/` | `transcripts/` (23 whisper transcripts plus one video-sourced transcript with no mp3), `mp3s/` (**gitignored**), `manifest.csv`. |
| `web_articles/` | News coverage saved as text with a provenance header: source, headline, byline, date, original URL, archive URL, retrieval date, and why it was saved. |

---

## Project-wide conventions

**Paths in documentation never climb out with a parent reference.**
Write a bare filename for something in the same directory, or the full path from the project
root for anything else. Never reach upward into a sibling directory.

The point is that every path then has one reading, and that a grep for a document's path
finds every mention of it rather than scattering them across a bare filename, an upward
reference, and a partial path. It also means moving a README cannot silently break its own
links. `files/bin/verify-docs-paths.py` enforces this and prints the root-relative rewrite
for anything that breaks it.

Links that leave the repository, such as a GitHub issues URL, are exempt: they are not paths
into this tree. Adopted 2026-08-19, after `web/README.md` spent months pointing article
content at a directory that never existed, because the checker skipped every upward path
wholesale and so never looked.

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

**Custom filenames are a clue.** Digging through 200-page packets at speed, a file gets
named for the reason it was saved. Read those prefixes as a pointer, not clutter. Never
rename or delete one without carrying its meaning somewhere durable.

**Provenance headers on saved articles.** Anything pulled from the web gets SOURCE,
HEADLINE, BYLINE, DATE, URL, ARCHIVE, RETRIEVED, and WHY SAVED at the top. The publish
step reads those headers to build the site's source index, so the format is load-bearing.

---

## What is gitignored, and why

The repo is public. These stay local:

| Path | Why |
|---|---|
| `memory/`, `.remember/` | Working notes, not evidence |
| ~~`angles/`~~ | Pre-publication strategy, including rebuttals held in reserve. Removed from the project 2026-08-19 |
| `CLAUDE.md`, `.claude/`, `files/cold-read/` | Agent operating instructions |
| `podcasts/mp3s/` | Large binaries; transcripts are published instead |
| `web/{dist,node_modules,.astro}/` | Build output |

Withheld deliberately, not hidden — revisit each when the AI-disclosure policy is rewritten.
