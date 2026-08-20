#!/usr/bin/env python3
"""Rewrite the status marker on every note in memory/brandon-voice-notes.md.

The status is a DERIVED field, not a stored one. A note is open if and only if
its comment still exists somewhere under web/content/; once it is resolved the
comment is deleted from the page and only the copy in the notes file remains.
Storing that fact in two places is what let it drift: on 2026-08-20 eleven notes
were still marked OPEN months after being closed, because closing one is an edit
to the article and nobody came back to the notes file.

So nothing here is typed by hand. Run it and the file matches the article.
Called by files/bin/ship.sh on every publish; safe to run any time.

Exits 0 always -- a stale marker is not a reason to block a publish.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
NOTES = ROOT / "memory" / "brandon-voice-notes.md"
CONTENT = ROOT / "web" / "content"

HEAD = re.compile(r"^(## \d+\..*?) — \*(OPEN|resolved)\*$", re.M)
COMMENT = re.compile(r"<!--\s*@c(.*?)-->", re.S)


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def main():
    if not NOTES.exists():
        print("sync-voice-notes: no notes file, nothing to do")
        return 0
    if not CONTENT.is_dir():
        print("sync-voice-notes: no web/content/, refusing to guess", file=sys.stderr)
        return 0

    live = []
    for f in CONTENT.rglob("*.md"):
        for m in COMMENT.finditer(f.read_text(encoding="utf-8", errors="replace")):
            live.append(norm(m.group(1)))

    text = NOTES.read_text(encoding="utf-8")
    blocks = HEAD.split(text)
    # blocks = [preamble, title, status, body, title, status, body, ...]
    out, changed = [blocks[0]], []
    for i in range(1, len(blocks), 3):
        title, was, body = blocks[i], blocks[i + 1], blocks[i + 2]
        quoted = " ".join(
            ln.lstrip("> ").strip() for ln in body.splitlines() if ln.startswith(">")
        )
        key = norm(quoted)[:60]
        now = "OPEN" if key and any(key in c for c in live) else "resolved"
        if now != was:
            changed.append(f"{title.strip()[3:]}: {was} -> {now}")
        out.append(f"{title} — *{now}*{body}")

    new = "".join(out)
    if new != text:
        NOTES.write_text(new, encoding="utf-8")
    n_open = new.count(" — *OPEN*")
    print(f"sync-voice-notes: {n_open} open, {new.count(' — *resolved*')} resolved"
          + (f" ({len(changed)} updated)" if changed else ""))
    for c in changed:
        print(f"  {c}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
