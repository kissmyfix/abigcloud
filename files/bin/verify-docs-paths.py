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

# Docs whose paths matter: the navigation layer a session reads to find things, plus the
# player profiles, which are dense sets of archive references and nothing else checks them.
# The README glob runs four levels deep because entity, audit and derived directories live
# that far down; stopping at two left 32 of them unchecked until 2026-08-19.
DOCS = [ROOT / "CLAUDE.md", ROOT / "files" / "DATA_MAP.md", ROOT / "README.md"]
for depth in ("*", "*/*", "*/*/*", "*/*/*/*"):
    DOCS += sorted(p for p in ROOT.glob(f"{depth}/README.md")
                   if "node_modules" not in p.parts and ".git" not in p.parts)
DOCS += sorted(p for p in (ROOT / "the_players").glob("*.md") if p.name != "README.md")
DOCS = sorted(set(DOCS))

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


# A line saying a file simply went away has no successor on it; nothing there resolves.
# ~~`retired-name.pdf`~~ — struck through means "this path is not meant to resolve."
STRUCK = re.compile(r"~~[^~]*~~")

FROM = re.compile(r"\bfrom\b(?!.*\b(to|->)\b)", re.I)

GONE = re.compile(r"\bdeleted\b|\bremoved\b|\bno longer\b|\bretired\b|\bnot in the working tree\b|\bdissolved\b", re.I)


# On a history line, what separates the old name from the new one. Everything after the
# last pivot is a live path and gets checked.
PIVOT = re.compile(
    r"->|\u2192"                       # old -> new
    r"|\|"                            # table cell boundary: | was | is |
    r"|\bis now\b|\bnow\b|\bnow at\b"
    r"|\bmoved to\b|\bmoved here\b|\breplaced by\b|\bfolded into\b|\brenamed to\b",
    re.I,
)


def candidates(text):
    """Yield (path, is_historical) for each path-looking span, judged by its line.

    A line recording a rename mentions both the old name and the new one. Only the old
    name is historical: it is the span that must not resolve. The pivot word is what
    separates them ("previously X, now Y" / "X -> Y" / "was X, is Y"), so everything
    before the last pivot on a history line is treated as historical and everything after
    it is checked like any other path. A history line with no pivot is historical
    throughout, which is the old behaviour and the right default for "deleted 2026-07-29".
    """
    section_historical = False
    for line in text.split("\n"):
        # A heading that announces history ("Renamed 2026-07-29 — old -> new") governs the
        # rows beneath it, which carry no keyword of their own. Any other heading ends it.
        if line.lstrip().startswith("#") or line.startswith("**Renamed") or line.startswith("**Deleted"):
            section_historical = bool(HISTORY.search(line))
        # An explicitly retired name is struck through: ~~`old-name.pdf`~~. It renders as
        # struck-out text, which is what it means, and it removes any guessing from prose.
        line_checked = STRUCK.sub(lambda m: " " * len(m.group(0)), line)
        spans = [(m.start(), m.group(1)) for m in BACKTICK.finditer(line_checked)]
        spans += [(m.start(), m.group(1)) for m in MDLINK.finditer(line_checked)]
        spans.sort()
        if not spans:
            continue
        if not (HISTORY.search(line) or section_historical):
            for _, raw in spans:
                yield raw, False
            continue
        # "renamed ... from X" puts the old name after the pivot, so a trailing "from"
        # flips everything after it back to historical.
        frm = FROM.search(line)
        if frm:
            for pos, raw in spans:
                yield raw, pos > frm.start()
            continue
        if GONE.search(line) or (section_historical and not PIVOT.search(line)):
            for _, raw in spans:
                yield raw, True
            continue
        pivots = [m.end() for m in PIVOT.finditer(line)]
        cut = pivots[-1] if pivots else len(line)
        for pos, raw in spans:
            yield raw, pos < cut


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
            # A line-anchored reference (`files/bin/mdlive.py:373`) points at a real
            # file; the line number is not part of the path. Drop it before resolving.
            s = re.sub(r":\d+$", "", s)
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
