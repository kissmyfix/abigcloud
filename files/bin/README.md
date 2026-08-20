# files/bin/

## Purpose
Home for project scripts — anything executable that builds, transcribes, or processes project data. Rescued/collected here so scripts survive reboots instead of living in /tmp scratchpads.

## Environment
`files/venv/` is the project's permanent Python environment — `pdfplumber`, `pandas`, `openpyxl`. Run scripts with `files/venv/bin/python`, not system `python3` (which has none of these). Add packages with `files/venv/bin/pip install`. Rebuild from scratch with:
`python3 -m venv files/venv && files/venv/bin/pip install pdfplumber pandas openpyxl`

Exceptions: `pdf-profile.py` is stdlib + poppler only and runs anywhere; the whisper scripts need `faster-whisper`, which is not in this venv.

## Contents
- `anchor-prompt-log.sh` — publishes a SHA-256 for each **closed** month of the prompt log into `files/prompt-log-hashes.md`, which is committed. The log stays private; the hash plus the commit date is what proves the content existed then. Only closed months are anchored — the current month is still being appended to, so its hash changes with every prompt. Re-running verifies: a month whose hash no longer matches its published value has been modified since anchoring, and the script says MISMATCH and exits 1. Bash + coreutils, no venv.
- `prompt-log-append.sh` — **no longer here; moved out 2026-08-19.** The prompt-log hook is system-wide now, at `~/.claude/bin/prompt-log-append.sh`, wired in `~/.claude/settings.json`, writing to `~/.claude/prompt_log/<project>/`. It was project-scoped here, which meant a global habit only ran in one directory and its history lived inside the thing it recorded. See `~/.claude/prompt_log/README.md`.
- `pdf-extract.py` — batch-converts source PDFs to page-anchored text: `pdftotext -layout` into a `derived/` subdirectory, `[[page N]]` markers at each page break, automatic `ocrmypdf` on files with no text layer, and a `pdf-index.csv` recording kind/pages/trust per file. Idempotent — re-run after any download; `--force` redoes existing. Stdlib + poppler + ocrmypdf, no venv.
- `pdf-profile.py` — classifies PDFs as DIGITAL / OCR_SCAN / IMAGE_ONLY / SPARSE by chars-per-page and full-page raster share, and prints what to do with each. Run it on any new batch of PDFs before extracting, since the bucket determines whether the text is quotable. See the `extract-pdf-source` skill.
- `build-council-index.py` / `verify-council-index.py` — build and verify
  `sumner_county/gallatin_council_meetings/derived/council-index.csv`, one row per council
  document: the date the city printed in the masthead, the date in the saved filename,
  whether they agree, meeting body, pages, textless pages, extraction class, whether the
  text is quotable without opening the page image, md5, duplicates. Strictly mechanical —
  no tiering or subject judgments (those live in `memory/MEMORY.md`, block 2026-07-29).
  The masthead date is read from the top six non-blank lines of page 1 only: two packets
  scanned their own date into garbage, and a wider search silently returns the previous
  meeting's approval-of-minutes date. Those two are carried in the script as hand-read from
  the page image and pinned as verifier anchors. Stdlib + poppler, no venv.
- `batch-transcribe.py` — faster-whisper batch runner: works through a queue of podcast mp3s, writing transcripts to `podcasts/transcripts/`. Needs a Python venv with `faster-whisper` installed (the July 2026 batch ran from a /tmp venv; rebuild with `python -m venv venv && pip install faster-whisper` if needed).
- `transcribe.py` — single-file whisper transcription (same dependency).
- `narrow.py` — helper used to trim/extract relevant segments from transcripts.
- `parse-assessment.py` / `verify-assessments.py` — build and verify
  `state_of_tennessee/tn_property_assessments/derived/sumner-assessments.json` from the
  parcel-viewer PDFs in that directory. Word-coordinate parsing (`pdftotext -bbox-layout`),
  four independent verification passes. Stdlib + poppler, no venv. Both resolve the data
  directory from their own location, so they run from anywhere. Moved here 2026-07-29; they
  previously lived in a local `tn_property_assessments/bin/`, which no longer exists.
- `parse-sumner-pilot.py` / `verify-sumner-pilot.py` — build and verify
  `state_of_tennessee/tn_comptroller_pilot_reports/sumner_county/derived/sumner-pilot.json`
  (131 filing lines, 2015–2025) from the yearly Comptroller PDFs and the 2023–2025
  spreadsheet. The verifier recounts every year straight from the source and prints ALL
  AGREE or the disagreement. Needs the venv. Moved here 2026-07-29 from a local
  `sumner_county/bin/`, where they were named `parse-pilot.py` and `totals.py`.
- `verify-990.py` — four independent checks against the Gallatin IDB 990 filings in
  `usa_federal/irs_990_data/gallatin_idb/`. Moved here 2026-07-29 from a local `bin/` in
  that directory.
- `build-statewide-pilot-master.py` — builds `state_of_tennessee/tn_comptroller_pilot_reports/derived/tn-statewide-pilot-master-2014-2025.csv` from the Comptroller's statewide annual PILOT reports, 2014–2025, all 95 counties. Handles four distinct source layouts plus the 2023–2025 spreadsheets. Needs `pdfplumber`, `pandas`, `openpyxl` in a venv; takes roughly 8 minutes.
- `build-idb-debt-master.py` / `verify-idb-debt-master.py` — build and verify `state_of_tennessee/tn_comptroller_pilot_reports/derived/tn-idb-debt-master-2021-2023.csv` from `idb_debt-reports.xlsx`. Debt reporting, its own schema, needs `pandas` + `openpyxl` only; runs in seconds.
- `verify-statewide-pilot-master.py` — four-pass verification of the above: coverage and row counts recounted independently from source, column-shift detection, Sumner ground-truth check, and known-anchor reproduction. Exits nonzero on failure. Same dependencies.

## Source Type
**Working Material** — tooling, not source or output data.

## Handling Instructions
- File naming follows project convention: dashes in file names
- Scripts may contain hardcoded paths from where they originally ran — check paths before rerunning
- When a session writes a script worth keeping, it lands here, named with dashes, with a one-line entry added above
