#!/usr/bin/env python3
"""Build a one-row-per-document index of the Gallatin council meeting packets.

Reads the page-anchored .txt files that pdf-extract.py already wrote into
derived/, pulls each document's own header date and body name off page 1, and
compares that against the date in the filename. The filenames are Brandon's;
the headers are the city's. Where they disagree, the header wins and the row
says so - that disagreement is the whole reason this file exists.

Nothing here is interpretation. Every column is either read off the document,
counted, or hashed. Tier and subject judgments stay in the directory README.

Writes derived/council-index.csv.

Usage: build-council-index.py [council-meetings-dir]

Stdlib only. No venv, no model, no network.
"""

import csv
import hashlib
import os
import re
import sys

DEFAULT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "sumner_county", "gallatin_council_meetings",
)

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june",
     "july", "august", "september", "october", "november", "december"], 1)}

DATE_RE = re.compile(
    r"\b(" + "|".join(MONTHS) + r")\s+(\d{1,2})\s*,?\s*(\d{4})\b", re.I)
PAGE_RE = re.compile(r"\[\[page (\d+)\]\]")
BLANK_CHARS = 50   # same threshold pdf-extract.py uses for "no real text"

BODIES = [
    ("COUNCIL COMMITTEE MEETING", "council_committee"),
    ("COUNCIL COMMITTEE AGENDA", "council_committee"),
    ("CITY COUNCIL MEETING", "city_council"),
    ("COUNCIL MEETING", "city_council"),
    ("NOTICE OF MEETINGS", "public_notice"),
]


def pages(text):
    """Split page-anchored text into [(page_number, body), ...]."""
    parts = PAGE_RE.split(text)
    return [(int(parts[i]), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def iso(match):
    return "%04d-%02d-%02d" % (
        int(match.group(3)), MONTHS[match.group(1).lower()], int(match.group(2)))


HEADER_LINES = 6   # the date sits in the masthead, not down in the agenda body

# Packets whose own masthead date the scanner destroyed ("April t9,2022").
# These were read off the rendered page-1 image by hand on 2026-07-29 and are
# carried here rather than guessed, so the row says where the date came from.
HAND_READ = {
    "2022-04-19-city-council-agenda.pdf": "2022-04-19",
    "2022-05-17-city-council-agenda.pdf": "2022-05-17",
}


def header_date(page1):
    """The date the city printed in the masthead at the top of page 1.

    Deliberately refuses to look past the masthead. Several packets are OCR
    scans that garbled their own header date ("April t9,2022", "May t7,2022");
    a wider search silently picks up the next date on the page, which is the
    approval-of-minutes date for the PREVIOUS meeting. Wrong by one meeting is
    worse than blank, so those come back UNPARSED and get read off the page.
    """
    lines = [l for l in page1.splitlines() if l.strip()][:HEADER_LINES]
    m = DATE_RE.search("\n".join(lines))
    return iso(m) if m else "UNPARSED"


def filename_date(name):
    """Read the date the filename claims, under the project naming scheme.

    Names lead with the date, most specific first: YYYY-MM-DD for a dated
    document, YYYY-MM for one covering a month, YYYY for a fiscal-year report.
    XX marks a component the filename does not claim, so a less specific name
    never counts as a mismatch against the document's own header.
    """
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})(?!\d)", name)
    if m:
        return "%s-%s-%s" % m.groups()
    m = re.match(r"(\d{4})-(\d{2})(?!\d)", name)
    if m:
        return "%s-%s-XX" % m.groups()
    m = re.match(r"(\d{4})(?!\d)", name)
    return "%s-XX-XX" % m.group(1) if m else ""


def agrees(hdate, fdate):
    """Compare header date to filename date, treating XX as a wildcard.

    Filenames like 2020-sept-... only claim a month, so a full header date is
    not a contradiction - it is the filename being less specific.
    """
    if hdate == "UNPARSED" or not fdate:
        return "check"
    for h, f in zip(hdate.split("-"), fdate.split("-")):
        if f == "XX":
            continue
        if h != f:
            return "NO"
    return "yes"


def body_of(page1):
    head = "\n".join(
        [l for l in page1.splitlines() if l.strip()][:HEADER_LINES]).upper()
    for needle, label in BODIES:
        if needle in head:
            return label
    return "other"


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extraction_kinds(derived):
    """kind column from the pdf-index.csv files pdf-extract.py already wrote.

    Reads the ocr/ index second so a re-OCR'd document reports the class of
    the text actually being used, not the class of the half-blank original.
    Keys from ocr/ are mapped back to the original filename.
    """
    kinds = {}
    for sub, strip in ((".", False), ("ocr", True)):
        path = os.path.join(derived, sub, "pdf-index.csv")
        if not os.path.exists(path):
            continue
        with open(path, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                name = r["source"]
                if strip:
                    name = re.sub(r"-ocr\.pdf$", ".pdf", name)
                kinds[name] = r["kind"]
    return kinds


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR
    derived = os.path.join(base, "derived")
    if not os.path.isdir(derived):
        sys.exit("no derived/ in %s - run pdf-extract.py first" % base)

    kinds = extraction_kinds(derived)
    by_hash, rows = {}, []

    for pdf in sorted(os.listdir(base)):
        if not pdf.lower().endswith(".pdf"):
            continue
        stem = os.path.splitext(pdf)[0]
        # Some packets are scans whose text layer covers only part of the
        # document. Those were re-OCR'd into derived/ocr/; where that exists it
        # is the operative text, and the row measures it rather than the
        # half-blank original.
        txt = os.path.join(derived, "ocr", stem + "-ocr.txt")
        source = "ocrmypdf"
        if not os.path.exists(txt):
            txt, source = os.path.join(derived, stem + ".txt"), "pdftotext"
        if not os.path.exists(txt):
            print("  no text for %s - skipped" % pdf, file=sys.stderr)
            continue

        with open(txt, encoding="utf-8", errors="replace") as fh:
            pgs = pages(fh.read())
        page1 = pgs[0][1] if pgs else ""

        digest = md5(os.path.join(base, pdf))
        dup = by_hash.setdefault(digest, pdf)

        hdate, fdate = header_date(page1), filename_date(pdf)
        dsource = "masthead"
        if hdate == "UNPARSED" and pdf in HAND_READ:
            hdate, dsource = HAND_READ[pdf], "page image (hand-read)"
        elif hdate == "UNPARSED":
            dsource = ""
        blank = sum(1 for _, p in pgs if len(p.strip()) < BLANK_CHARS)
        kind = kinds.get(pdf, "")
        # pdf-profile grades an ocrmypdf output DIGITAL - the text layer is
        # dense and the producer string is not a scanner. It is still a
        # machine's guess at a photograph of a page. Anything we OCR'd is
        # OCR_SCAN by definition, whatever the profiler thinks of it.
        if source == "ocrmypdf":
            kind = "OCR_SCAN"

        rows.append({
            "source_pdf": pdf,
            "text_file": os.path.relpath(txt, base),
            "text_source": source,
            "header_date": hdate,
            "header_date_source": dsource,
            "filename_date": fdate,
            "date_agrees": agrees(hdate, fdate),
            "body": body_of(page1),
            "pages": len(pgs),
            "blank_pages": blank,
            "extraction": kind,
            "quotable": "yes" if kind == "DIGITAL" and source == "pdftotext"
                        else "verify",
            "duplicate_of": "" if dup == pdf else dup,
            "md5": digest,
        })

    out = os.path.join(derived, "council-index.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    print("%d documents -> %s" % (len(rows), out))
    for r in rows:
        if r["header_date"] == "UNPARSED":
            print("  no masthead date read: %s  (filename says %s - confirm "
                  "against page 1 image)" % (r["source_pdf"], r["filename_date"]))
        if r["date_agrees"] == "NO":
            print("  date mismatch: %s  filename %s / header %s"
                  % (r["source_pdf"], r["filename_date"], r["header_date"]))
        if r["duplicate_of"]:
            print("  duplicate: %s == %s" % (r["source_pdf"], r["duplicate_of"]))


if __name__ == "__main__":
    main()
