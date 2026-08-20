# files/

## Purpose
Project plumbing — the navigation index, the directory-README template, the scripts that
build and process project data, and the machine-written capture logs. Nothing in here is
investigation material; it is the machinery the investigation runs on.

## Contents

**Files**
- `DATA_MAP.md` — the directory index for the whole project, and the navigation rule read
  at session start. Every directory gets one row. Update it whenever a directory or
- `RESEARCH_SOURCES.md` — the external sites this investigation depends on, with the
  URL pattern that actually reaches the useful page on each.
  notable top-level file is added.
- `DIR_README_TEMPLATE.md` — the rigid template copied into any directory lacking a
  `README.md`. Purpose / Contents / Source Type / Handling Instructions / Notes.
- `ai-toolchain-changelog.md` — deliberate changes to the Claude Code setup (settings,
  plugins, hooks, memory systems), newest first. Each entry carries its own verification
  checks and reversal steps.

**Subdirectories**
- `bin/` — project scripts: PDF extraction and profiling, whisper transcription, the
  Comptroller PILOT/debt master-CSV builders and their verifiers.
  See its own README for what each script does and its dependencies.
- `venv/` — the project's permanent Python environment (`pdfplumber`, `pandas`,
  `openpyxl`), ~215 MB. Scripts in `bin/` run against `files/venv/bin/python`, not system
  `python3`. Rebuild instructions in `bin/README.md`.
`claude_ignore/` is gone (dissolved 2026-07-29). It had been a staging area for large
duplicated transcripts and unfiled material, walled off behind a no-AI rule. Its contents
were triaged and either deleted, moved to a real home, or condensed into a single archive
Brandon moved out of the project. Nothing about the directory survives except this note.

## Source Type
**Working Material** — tooling, indexes, and capture streams. Nothing here is a source or
a citable output. The derived data these scripts produce lives with the source material it
came from, not in this directory.

## Handling Instructions
- Scripts land in `bin/`, never loose in `files/` and never left in a `/tmp` scratchpad.
  Dashes in file names, underscores in directory names.
- Run project scripts with `files/venv/bin/python`. System `python3` has none of the
  dependencies.
- The prompt log moved out of here 2026-08-19. It is system-wide now, at
  `~/.claude/prompt_log/<project>/`, written by a hook in `~/.claude/settings.json`.
  Append-only: never edit past entries, never add unmarked AI text.
- When a new directory is created anywhere in the project, add its row to `DATA_MAP.md`
  and copy `DIR_README_TEMPLATE.md` into it. Both, not one. Exempt: machine-generated
  directories nobody navigates by hand — browser-saved `*_files/` asset folders, build
  output and dependencies, empty directories.
- Machine-generated artifacts belong in a `derived/` subdirectory of the directory holding
  their sources, never beside the sources themselves. Full convention in `DATA_MAP.md`.
- Config or toolchain changes get an entry in `ai-toolchain-changelog.md` with reversal
  steps, so any change can be undone later without reconstructing what it was.

## Notes
`venv/` is large and machine-generated — it is disposable and rebuildable, unlike
everything else in this directory.
