#!/usr/bin/env python3
"""Independently re-check derived/council-index.csv against the source PDFs.

Does not trust anything the build script wrote, and does not read the
pdf-index.csv the build script leaned on. Page counts come back from pdfinfo,
hashes are recomputed, and a set of known anchors is asserted against the
extracted text. Exits nonzero on any failure.

The anchors are the point. The mechanical checks catch a broken rebuild; the
anchors catch a rebuild that succeeds while quietly pointing at the wrong
document - the failure mode that actually reaches print.

Usage: verify-council-index.py [council-meetings-dir]

Stdlib + poppler.
"""

import csv
import hashlib
import os
import re
import subprocess
import sys

DEFAULT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "sumner_county", "gallatin_council_meetings",
)

# Facts checked by hand against the page images, 2026-07-29. Each is a claim
# the investigation actually leans on, so a rebuild that breaks one fails loud.
ANCHORS = [
    ("2020-05-12-r2005-24-woolhawk-pilot-terms.pdf", "header_date", "2020-05-12"),
    ("2020-05-12-r2005-24-woolhawk-pilot-terms.pdf", "body", "council_committee"),
    ("2020-05-12-r2005-24-woolhawk-pilot-terms.pdf", "quotable", "yes"),
    ("2020-05-12-council-committee-agenda.pdf", "body", "council_committee"),
    ("2020-09-15-city-council-agenda.pdf", "header_date", "2020-09-15"),
    ("2020-06-16-city-council-agenda.pdf", "header_date", "2020-06-16"),
    # Filed for years as gnrc-plan-2018.pdf. It is a council agenda packet; the
    # GNRC regional plan is an attachment inside it, from p.58.
    ("2018-06-19-city-council-agenda.pdf", "header_date", "2018-06-19"),
    ("2018-06-19-city-council-agenda.pdf", "body", "city_council"),
    # Mastheads destroyed by the scanner, read off the page-1 image by hand.
    # The scanned text says 2022-04-05 and 2022-05-03 - the previous meeting's
    # approval-of-minutes dates - so these two must never revert to machine
    # reads without someone looking at the image again.
    ("2022-04-19-city-council-agenda.pdf", "header_date", "2022-04-19"),
    ("2022-04-19-city-council-agenda.pdf",
     "header_date_source", "page image (hand-read)"),
    ("2022-05-17-city-council-agenda.pdf", "header_date", "2022-05-17"),
    ("2022-05-17-city-council-agenda.pdf",
     "header_date_source", "page image (hand-read)"),
]

# (file, must-appear string) - the text is genuinely the document it claims.
TEXT_ANCHORS = [
    ("2020-05-12-r2005-24-woolhawk-pilot-terms.txt", "R2005-24"),
    ("2020-05-12-r2005-24-woolhawk-pilot-terms.txt",
     "05/12/2020 Council Work Session Agenda-Page 40"),
    ("ocr/2020-05-12-council-committee-agenda-ocr.txt", "R2005-24"),
    ("2020-09-15-city-council-agenda.txt", "Woolhawk"),
]

# The two prefixed copies Brandon had flagged ("important-", "the-most-
# importanat-yet-") were byte-identical to these and were removed on
# 2026-07-29 once their meaning was carried into memory/MEMORY.md. Nothing in
# this directory should be a duplicate of anything else in it.
KNOWN_DUPES = {}

fails = []


def check(ok, msg):
    if not ok:
        fails.append(msg)


def pdf_pages(path):
    out = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else -1


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR
    index = os.path.join(base, "derived", "council-index.csv")
    if not os.path.exists(index):
        sys.exit("no council-index.csv - run build-council-index.py first")

    with open(index, newline="", encoding="utf-8") as fh:
        rows = {r["source_pdf"]: r for r in csv.DictReader(fh)}

    on_disk = {f for f in os.listdir(base) if f.lower().endswith(".pdf")}
    check(on_disk == set(rows), "index does not cover the directory: missing %s, "
          "extra %s" % (sorted(on_disk - set(rows)), sorted(set(rows) - on_disk)))

    for name, row in rows.items():
        pdf = os.path.join(base, name)
        if not os.path.exists(pdf):
            continue

        pages = pdf_pages(pdf)
        check(pages == int(row["pages"]),
              "%s: index says %s pages, pdfinfo says %d" % (name, row["pages"], pages))

        check(md5(pdf) == row["md5"], "%s: md5 changed since the index was built" % name)

        txt = os.path.join(base, row["text_file"])
        check(os.path.exists(txt), "%s: text_file missing (%s)" % (name, row["text_file"]))

        if os.path.exists(txt):
            with open(txt, encoding="utf-8", errors="replace") as fh:
                anchors = len(re.findall(r"\[\[page \d+\]\]", fh.read()))
            check(anchors == pages,
                  "%s: %d page anchors in text, %d pages in pdf" % (name, anchors, pages))

        # Negative assertion: quotable=yes is reserved for born-digital text.
        # If an OCR scan ever gets marked quotable, a guessed figure walks
        # straight into an article without anyone re-reading the page image.
        # Both halves matter. pdf-profile grades ocrmypdf output DIGITAL on the
        # strength of its dense text layer, so extraction alone would let a
        # scan we OCR'd ourselves pass as born-digital.
        check(not (row["quotable"] == "yes" and row["extraction"] != "DIGITAL"),
              "%s: marked quotable but extraction is %s" % (name, row["extraction"]))
        check(not (row["quotable"] == "yes" and row["text_source"] != "pdftotext"),
              "%s: marked quotable but its text came from %s"
              % (name, row["text_source"]))
        check(not (row["text_source"] == "ocrmypdf" and row["extraction"] == "DIGITAL"),
              "%s: OCR'd text graded DIGITAL - it is a machine guess" % name)

        check(int(row["blank_pages"]) <= pages,
              "%s: more blank pages than pages" % name)

    for name, original in KNOWN_DUPES.items():
        if name in rows:
            check(rows[name]["duplicate_of"] == original,
                  "%s: expected duplicate_of %s, got %r"
                  % (name, original, rows[name]["duplicate_of"]))
    dupes = {n for n, r in rows.items() if r["duplicate_of"]}
    check(dupes == set(KNOWN_DUPES),
          "duplicate set changed: %s" % sorted(dupes ^ set(KNOWN_DUPES)))

    for name, field, expected in ANCHORS:
        if name not in rows:
            fails.append("anchor file absent from index: %s" % name)
            continue
        check(rows[name][field] == expected,
              "%s: %s should be %r, index says %r"
              % (name, field, expected, rows[name][field]))

    for txt, needle in TEXT_ANCHORS:
        path = os.path.join(base, "derived", txt)
        if not os.path.exists(path):
            fails.append("anchor text absent: %s" % txt)
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            check(needle in fh.read(), "%s: expected to contain %r" % (txt, needle))

    if fails:
        print("FAIL (%d)" % len(fails))
        for f in fails:
            print("  " + f)
        sys.exit(1)
    print("OK: %d documents, %d anchors, %d text anchors"
          % (len(rows), len(ANCHORS), len(TEXT_ANCHORS)))


if __name__ == "__main__":
    main()
