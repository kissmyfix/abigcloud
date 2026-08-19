#!/usr/bin/env python3
"""Verify that every project path named in the project's docs actually exists.

Scans the reference documents (CLAUDE.md, files/DATA_MAP.md, README.md, and every
directory README.md) for backtick-quoted paths and markdown links, then checks each
one against the filesystem.

Exits non-zero if any path does not resolve, so it can gate a commit.

    files/venv/bin/python files/bin/verify-docs-paths.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Docs whose paths are load-bearing: the navigation layer a session reads to find things.
DOCS = [ROOT / "CLAUDE.md", ROOT / "files" / "DATA_MAP.md", ROOT / "README.md"]
DOCS += sorted(p for p in ROOT.glob("*/README.md"))
DOCS += sorted(p for p in ROOT.glob("*/*/README.md"))

# A path-looking backtick span: has a slash or a known project file extension.
BACKTICK = re.compile(r"`([^`\n]+)`")
MDLINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
EXTS = {".md", ".py", ".sh", ".pdf", ".csv", ".json", ".html", ".xlsx", ".ods", ".jsonl"}

# Spans that look like paths but aren't: prose, globs, statute cites, external URLs.
SKIP = re.compile(
    r"^(https?:|mailto:|#)"          # links off the filesystem
    r"|[*?\[\]{}]"                   # globs, character classes, {entity} placeholders
    r"|^[A-Z]\.C\.A\."               # statute citations
    r"|^\.{3}"                       # ellipses
    r"|<|>"                          # placeholder brackets like <entity>
    r"|^\d+$"
    r"|\s"                           # command lines and legacy names with spaces
    r"|YYYY|MM-DD"                   # filename-pattern templates, not filenames
    r"|^(python3?|bash|sh|files/venv)\b"
    r"|^/"                           # site routes (/report/), not filesystem paths
    r"|^\.\./"                       # links out of the repo (GitHub ../../issues)
    r"|^(underscored_)?name\.md$"    # naming-scheme placeholders
    r"|^~/"                          # paths outside the repo (~/.claude/...)
    r"|^origin/"                     # git refs, not files
    r"|^[a-z0-9.-]+\.(com|org|net|gov|io)(/|$)"   # bare hostnames, not paths
    r"|\.\.\.\."                     # an elided example path (foo-....txt)
    r"|^\./assets/name\."             # frontmatter example in web/README
)


# A line recording what a file USED to be called, or that it is gone, is provenance —
# the rename history this project deliberately keeps. Those names must not resolve.
HISTORY = re.compile(
    r"formerly|renamed|w(as|ere) named|named for|filed for years as|previously"
    r"|deleted|removed|deduplicated|superseded|no longer|dissolved|disposable|retired"
    r"|used to|old name|before they move|started here as|moved here"
    r"|once called|one called|commit `?[0-9a-f]{7}|not in the working tree",
    re.I,
)


def candidates(text):
    """Yield (path, is_historical) for each path-looking span, judged by its line.

    Prose wraps, so a name can sit on the line after the phrase that retires it
    ("Moved here 2026-07-29 from\\n a local `x/bin/`"). Read both lines.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        window = (lines[i - 1] if i else "") + " " + line
        historical = bool(HISTORY.search(window))
        # A two-column old→new mapping row: the left cell is the retired name.
        cells = [c.strip() for c in line.split("|")] if line.count("|") >= 3 else []
        for m in BACKTICK.finditer(line):
            raw = m.group(1).strip()
            retired = any(c.startswith(f"`{raw}`") for c in cells[1:2])
            yield raw, historical or retired
        for m in MDLINK.finditer(line):
            yield m.group(1).strip(), historical


def is_pathlike(s):
    if not s or SKIP.search(s):
        return False
    return "/" in s or Path(s).suffix in EXTS


def build_suffixes():
    """Every trailing path fragment in the project.

    Docs name things at whatever depth reads clearly — a bare `transcribe.py`, a
    partial `tn_comptroller_pilot_reports/sumner_county/`. Any of those is a valid
    reference so long as some real path ends with it.
    """
    suffixes = set()
    for p in ROOT.rglob("*"):
        parts = p.relative_to(ROOT).parts
        if set(parts) & {".git", "venv", "node_modules", "__pycache__", "dist", ".remember"}:
            continue
        for i in range(len(parts)):
            suffixes.add("/".join(parts[i:]))
    return suffixes


def main():
    failures = []
    checked = 0
    historical_count = 0
    suffixes = build_suffixes()
    for doc in DOCS:
        if not doc.exists():
            failures.append((doc.relative_to(ROOT), "<doc itself missing>"))
            continue
        text = doc.read_text(encoding="utf-8", errors="replace")
        seen = set()
        for raw, historical in candidates(text):
            s = raw.rstrip("/")
            if not is_pathlike(s) or s in seen:
                continue
            seen.add(s)
            if historical:
                historical_count += 1
                continue
            # Paths are written relative to the project root; also allow relative
            # to the doc's own directory, which is how directory READMEs read. A bare
            # filename counts if the project holds a file by that name anywhere —
            # READMEs routinely name a script or dataset without repeating its path.
            if (
                (ROOT / s).exists()
                or (doc.parent / s).exists()
                or s in suffixes
            ):
                checked += 1
            else:
                failures.append((doc.relative_to(ROOT), raw))

    for doc, path in failures:
        print(f"MISSING  {doc}: {path}")
    print(
        f"\n{checked} paths resolved, {historical_count} historical (skipped), "
        f"{len(failures)} missing, across {len(DOCS)} docs."
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
