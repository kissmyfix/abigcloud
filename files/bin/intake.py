#!/usr/bin/env python3
"""Intake worker for inbox/ — the deterministic half of filing a new document.

Does everything that needs no judgment: hashes the file, checks it against
every document already in the archive, profiles and extracts it, records a
manifest row, and writes what it could not decide into inbox/NEEDS-FILING.md
for a session to resolve.

Never moves a file into the archive. Deciding where a document belongs and
what it should be called is the model's half, and it happens under review.

    files/bin/intake.py            process everything new in inbox/
    files/bin/intake.py <path>     process one file
    files/bin/intake.py --rescan   rebuild the archive hash index first

Stdlib + poppler + ocrmypdf. No venv, no model, no network.
"""
import csv, hashlib, os, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT     = Path(__file__).resolve().parents[2]
INBOX    = ROOT / "inbox"
QUEUE    = INBOX / "NEEDS-FILING.md"
MANIFEST = ROOT / "files" / "MANIFEST.csv"
HASHES   = ROOT / "files" / ".archive-hashes"     # cache, gitignored

EXTS = {".pdf", ".txt", ".xml", ".csv", ".html", ".htm", ".png", ".jpg", ".json"}
SKIP_DIRS = {".git", "web", "venv", "node_modules", "__pycache__", ".astro",
             "derived", "inbox", ".remember", "memory"}

DATE = re.compile(r"(?:19|20)\d{2}-\d{2}-\d{2}")
YEAR = re.compile(r"(?<!\d)(?:19[89]\d|20[0-4]\d)(?!\d)")
EIN  = re.compile(r"\b(\d{2})-?(\d{7})\b")
# TPAD names its downloads by county+map+parcel: ...-083111++++00200+000.pdf
PARCEL = re.compile(r"-(\d{3})([0-9A-Z]{3,4})\+*([A-Z]?)\+*(\d{5})\+(\d{3})")
URL  = re.compile(r"https?://[^\s)>\]\"']+")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def archive_files():
    for d, subs, files in os.walk(ROOT):
        subs[:] = [s for s in subs if s not in SKIP_DIRS and not s.startswith(".")]
        for f in files:
            p = Path(d) / f
            if p.suffix.lower() in EXTS:
                yield p


def build_index(force=False):
    """path -> sha256 for everything already filed. Cached; cheap to rebuild."""
    idx = {}
    if HASHES.exists() and not force:
        for line in HASHES.read_text().splitlines():
            h, _, rel = line.partition("  ")
            if h and (ROOT / rel).exists():
                idx[rel] = h
    known = set(idx)
    for p in archive_files():
        rel = str(p.relative_to(ROOT))
        if rel not in known:
            idx[rel] = sha256(p)
    HASHES.write_text("".join(f"{h}  {r}\n" for r, h in sorted(idx.items())))
    return idx


def pdf_facts(p):
    """Page count, trust bucket, and a first-page snippet, via the project profiler."""
    r = subprocess.run([sys.executable, str(ROOT / "files/bin/pdf-profile.py"), str(p)],
                       capture_output=True, text=True)
    line = next((l for l in r.stdout.splitlines() if l.strip()), "")
    kind = line.split()[0] if line else "?"
    pages = re.search(r"(\d+)p\b", line)
    snip = subprocess.run(["pdftotext", "-f", "1", "-l", "2", "-layout", str(p), "-"],
                          capture_output=True, text=True).stdout
    return kind, (pages.group(1) if pages else "?"), snip


def xml_facts(p):
    """A 990 XML says who filed it and for what period. Read those, not the filename."""
    s = p.read_text(errors="ignore")
    def g(tag):
        m = re.search(rf"<{tag}>([^<]+)</{tag}>", s)
        return m.group(1).strip() if m else ""
    filer = re.search(r"<Filer>.*?<BusinessNameLine1Txt>([^<]+)", s, re.S)
    return {
        "filer": filer.group(1).strip() if filer else "",
        "ein": g("EIN"),
        "period_begin": g("TaxPeriodBeginDt"),
        "period_end": g("TaxPeriodEndDt"),
        "form": g("ReturnTypeCd"),
    }


def hints(p, text):
    """Everything a filename should have carried, read off the document instead."""
    out = {}
    # A government PDF usually prints the system it came from across the header.
    if m := URL.search(text):
        out["url_in_doc"] = m.group(0).rstrip(".,;")
    if m := DATE.search(text):
        out["date_in_doc"] = m.group(0)
    yrs = sorted(set(YEAR.findall(text)))
    if yrs:
        out["years_seen"] = ", ".join(yrs[:6])
    if m := EIN.search(text):
        out["ein_in_doc"] = f"{m.group(1)}-{m.group(2)}"
    return out


def manifest_write(rows):
    """Upsert by sha256. A row already in the ledger keeps every field a human
    filled in — status, filed_to, source_url, why_saved — because re-running the
    worker must never destroy filing work already done."""
    cols = ["retrieved", "original_name", "inbox_path", "sha256", "ext", "bytes",
            "kind", "pages", "parcel_id", "status", "filed_to", "source_url",
            "why_saved", "note"]
    HUMAN = ("status", "filed_to", "source_url", "why_saved")

    existing = {}
    order = []
    if MANIFEST.exists():
        for r in csv.DictReader(open(MANIFEST)):
            existing[r["sha256"]] = r
            order.append(r["sha256"])

    for src in rows:
        # Work on a copy. The caller still needs these rows to render the queue,
        # and merging a filed row's status back over them hid duplicates once.
        new = {c: src.get(c, "") for c in cols}
        k = new["sha256"]
        old = existing.get(k)
        if old:
            for c in HUMAN:
                # a human answer outranks the worker's default
                if old.get(c) and old[c] != "NEEDS FILING":
                    new[c] = old[c]
        else:
            order.append(k)
        existing[k] = new

    with open(MANIFEST, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for k in order:
            w.writerow(existing[k])


def reconcile(idx):
    """Close out rows whose inbox file is gone.

    A document leaves the inbox two ways: it gets filed into the archive, or it
    is deleted as redundant. Neither one told the ledger, so rows sat at
    NEEDS FILING forever and a completeness query counted ghosts. Identity is
    the sha256, so if the archive now holds those bytes the row is FILED and we
    can say where; if nothing holds them, it was discarded."""
    if not MANIFEST.exists():
        return 0, 0
    by_hash = {}
    for rel, h in idx.items():
        by_hash.setdefault(h[:16], []).append(rel)

    rows = list(csv.DictReader(open(MANIFEST)))
    filed = gone = 0
    for r in rows:
        if r["status"] in ("FILED", "DISCARDED"):
            continue
        if (ROOT / r["inbox_path"]).exists():
            continue
        hit = by_hash.get(r["sha256"])
        if hit:
            r["status"], r["filed_to"] = "FILED", hit[0]
            filed += 1
        else:
            r["status"] = "DISCARDED"
            r["note"] = r.get("note") or "left the inbox without being filed; no copy in the archive"
            gone += 1
    if filed or gone:
        with open(MANIFEST, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
    return filed, gone


def process(paths, idx):
    by_hash = {}
    for rel, h in idx.items():
        by_hash.setdefault(h, []).append(rel)

    entries, rows = [], []
    for p in paths:
        h = sha256(p)
        rel = str(p.relative_to(ROOT))
        stat = p.stat()
        row = dict(retrieved=datetime.fromtimestamp(stat.st_mtime, timezone.utc)
                              .strftime("%Y-%m-%d"),
                   original_name=p.name, inbox_path=rel, sha256=h[:16],
                   ext=p.suffix.lower().lstrip("."), bytes=stat.st_size)

        if h in by_hash:
            row["status"] = "DUPLICATE"
            row["note"] = by_hash[h][0]
            rows.append(row)
            entries.append((p, row, {"duplicate_of": by_hash[h][0]}, ""))
            continue

        row["status"] = "NEEDS FILING"
        # A re-download of the same parcel is a different file with different
        # bytes. The TPAD filename carries the canonical id, so group on that.
        if m := PARCEL.search(p.name):
            cty, cmap, grp, par, pi = m.groups()
            row["parcel_id"] = f"{cty}-{cmap}{'-'+grp if grp else ''}-{par}-{pi}"
        # Brandon's habit: the reason for the download, typed into the filename.
        # Anything after a double dash is a note to a later reader, not part of
        # the document's identity. It moves to the ledger and off the filename.
        if "--" in p.stem:
            row["why_saved"] = p.stem.split("--", 1)[1].replace("-", " ").strip()
        extra, snip = {}, ""
        if p.suffix.lower() == ".pdf":
            kind, pages, snip = pdf_facts(p)
            row["kind"], row["pages"] = kind, pages
            if kind == "IMAGE_ONLY":
                subprocess.run([sys.executable, str(ROOT / "files/bin/pdf-extract.py"),
                                str(p)], capture_output=True)
                d = p.parent / "derived" / f"{p.stem}.txt"
                if d.exists():
                    snip = d.read_text(errors="ignore")[:3000]
                    row["note"] = "OCR'd on intake"
        elif p.suffix.lower() == ".xml":
            extra = xml_facts(p)
            row["kind"] = "XML-990" if extra.get("ein") else "XML"
        else:
            try:
                snip = p.read_text(errors="ignore")[:3000]
            except Exception:
                pass

        extra.update(hints(p, snip))
        rows.append(row)
        entries.append((p, row, extra, snip))
    return entries, rows


def write_queue(entries):
    pend = [e for e in entries if e[1]["status"] == "NEEDS FILING"]
    dups = [e for e in entries if e[1]["status"] == "DUPLICATE"]

    L = ["# Needs filing",
         "",
         f"*Written by `files/bin/intake.py`, {datetime.now():%Y-%m-%d %H:%M}. "
         "Everything mechanical is done: hashed, deduped, profiled, extracted. "
         "What is left needs a decision.*",
         "",
         "**For whoever picks this up (Claude or Brandon).** For each entry below: "
         "decide the destination directory and the filename, move it, add the "
         "provenance header, write the README entry, and set `status` and `filed_to` "
         "on its row in `files/MANIFEST.csv`. Conventions are in "
         "`.claude/skills/extract-pdf-source/SKILL.md` under Intake. "
         "Do not guess a source URL — if it is unknown, record it as unknown.",
         "",
         "**`original_name` is already recorded for every file, so rename freely.** The "
         "gibberish a site hands you is provenance and the manifest keeps it. The one thing "
         "only Brandon knows is `why_saved` — what he was chasing when he downloaded it. "
         "Ask him for it if it is not obvious, and put the answer in the manifest, not in "
         "the filename.",
         ""]

    if not pend and not dups:
        L += ["Inbox is empty. Nothing to file.", ""]

    for p, row, extra, snip in pend:
        L += [f"## `{p.name}`", ""]
        L += [f"- **{k}**: {v}" for k, v in [
            ("size", f"{row['bytes']:,} bytes"), ("sha256", row["sha256"]),
            ("kind", row.get("kind", "")), ("pages", row.get("pages", "")),
            ("retrieved", row["retrieved"]), ("note", row.get("note", ""))] if v]
        L += [f"- **{k}**: {v}" for k, v in extra.items() if v]
        L += [f"- **why saved**: {row['why_saved']}" if row.get("why_saved")
              else "- **why saved**: _blank — type it on this line, or just say it in chat_"]
        if snip.strip():
            head = "\n".join(snip.strip().splitlines()[:14])
            L += ["", "```", head, "```"]
        L += ["", "- [ ] filed", ""]

    # Same parcel, more than one download. Not byte-identical, so the hash
    # check cannot see them; the parcel id can.
    seen = {}
    for _, row, _, _ in pend:
        if pid := row.get("parcel_id"):
            seen.setdefault(pid, []).append(row["original_name"])
    repeats = {k: v for k, v in seen.items() if len(v) > 1}
    if repeats:
        L += ["## Same parcel, downloaded more than once", "",
              "Different bytes each time, so the hash check does not catch these. "
              "Keep one, delete the rest.", ""]
        for pid, names in sorted(repeats.items()):
            L.append(f"- **{pid}** — {len(names)} copies")
            for n in names:
                L.append(f"  - `{n}`")
        L.append("")

    if dups:
        L += ["## Duplicates — already in the archive", "",
              "Byte-identical to a filed document. Delete from the inbox once confirmed.",
              ""]
        for p, row, extra, _ in dups:
            L.append(f"- `{p.name}` → `{extra['duplicate_of']}`")
        L += ["", "*These are already in the archive. The ledger row for each keeps its "
              "original `FILED` status — one document, one row, regardless of how many "
              "times a copy lands in the inbox.*"]
        L.append("")

    QUEUE.write_text("\n".join(L))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    idx = build_index(force="--rescan" in sys.argv)
    rf, rg = reconcile(idx)
    if rf or rg:
        print(f"reconciled: {rf} now filed, {rg} discarded")

    if args:
        paths = [Path(a).resolve() for a in args]
    else:
        paths = [p for p in sorted(INBOX.rglob("*"))
                 if p.is_file() and p.suffix.lower() in EXTS
                 and "derived" not in p.parts and p.name != QUEUE.name]

    if not paths:
        write_queue([])
        print("inbox empty")
        return

    entries, rows = process(paths, idx)
    manifest_write(rows)
    write_queue(entries)

    n_dup = sum(1 for r in rows if r["status"] == "DUPLICATE")
    print(f"{len(rows)} file(s): {len(rows)-n_dup} need filing, {n_dup} duplicate")
    print(f"queue:    {QUEUE.relative_to(ROOT)}")
    print(f"manifest: {MANIFEST.relative_to(ROOT)}")


main()
