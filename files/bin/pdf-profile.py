#!/usr/bin/env python3
"""Classify PDFs by how they were manufactured, so extraction can be trusted.

File size says nothing about content. What matters is whether a PDF carries real
digital text, an OCR guess laid over a scan, or no text at all. This reads that
off poppler's output and says what to do with each file.

Usage: pdf-profile.py <file-or-directory> [...]

Stdlib + poppler-utils only - runs without the project venv.
"""

import os
import re
import subprocess
import sys

# A page image this wide at letter size is the whole page, not a logo.
FULL_PAGE_PX = 1500
# Below this, whatever text exists is furniture, not content.
IMAGE_ONLY_CPP = 50
# Scans OCR thinner than born-digital text of the same layout.
OCR_SUSPECT_CPP = 1200


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True,
                              timeout=180).stdout
    except (subprocess.SubprocessError, OSError):
        return ""


def profile(path):
    info = run(["pdfinfo", path])
    pages = int(next((m.group(1) for m in
                      [re.search(r"^Pages:\s+(\d+)", info, re.M)] if m), 0) or 0)
    producer = (re.search(r"^Producer:\s+(.+)$", info, re.M) or
                re.search(r"^Creator:\s+(.+)$", info, re.M))
    producer = producer.group(1).strip() if producer else "?"

    chars = len(run(["pdftotext", path, "-"]))
    size_mb = os.path.getsize(path) / 1048576
    cpp = chars / pages if pages else 0

    # How many pages carry a full-page raster?
    scanned_pages = set()
    for line in run(["pdfimages", "-list", path]).splitlines()[2:]:
        f = line.split()
        if len(f) > 3 and f[0].isdigit() and f[3].isdigit():
            if int(f[3]) >= FULL_PAGE_PX:
                scanned_pages.add(int(f[0]))
    raster_share = len(scanned_pages) / pages if pages else 0

    if cpp < IMAGE_ONLY_CPP:
        kind, action = "IMAGE_ONLY", "OCR required: ocrmypdf in.pdf out.pdf"
    elif raster_share > 0.5:
        kind, action = "OCR_SCAN", "verify every figure against the page image"
    elif cpp < OCR_SUSPECT_CPP:
        kind, action = "SPARSE", "thin text - check a page before trusting it"
    else:
        kind, action = "DIGITAL", "pdftotext -layout is authoritative"

    if pages and pages <= 3:
        action += "  [SHORT - confirm this is the whole document]"

    return dict(path=path, pages=pages, size_mb=size_mb, chars=chars, cpp=cpp,
                raster_share=raster_share, producer=producer, kind=kind,
                action=action)


def collect(args):
    out = []
    for a in args:
        if os.path.isdir(a):
            for root, _, files in os.walk(a):
                out += [os.path.join(root, f) for f in sorted(files)
                        if f.lower().endswith(".pdf")]
        elif a.lower().endswith(".pdf"):
            out.append(a)
    return out


def main():
    paths = collect(sys.argv[1:])
    if not paths:
        sys.exit("usage: pdf-profile.py <file-or-directory> [...]")

    rows = [profile(p) for p in paths]
    rows.sort(key=lambda r: (r["kind"], r["path"]))

    for r in rows:
        print(f"{r['kind']:<10} {r['size_mb']:>6.1f}MB {r['pages']:>4}p "
              f"{r['cpp']:>6.0f} ch/pg  raster {r['raster_share']:>4.0%}  "
              f"{os.path.basename(r['path'])}")
        print(f"{'':<10} {r['producer'][:60]}")
        print(f"{'':<10} -> {r['action']}\n")

    tally = {}
    for r in rows:
        tally[r["kind"]] = tally.get(r["kind"], 0) + 1
    print(f"{len(rows)} files: " +
          ", ".join(f"{v} {k}" for k, v in sorted(tally.items())))


if __name__ == "__main__":
    main()
