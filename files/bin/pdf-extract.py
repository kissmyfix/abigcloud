#!/usr/bin/env python3
"""Batch-convert source PDFs to page-anchored text, OCR'ing the ones that need it.

For every PDF, writes a .txt into a derived/ subdirectory beside it, with an
explicit [[page N]] marker at the top of each page so a grep hit maps straight
back to a page in the original. OCRs anything with no text layer (needs
ocrmypdf), writing the OCR'd copy to derived/ too - the original is the record
and is never modified. Skips files already converted unless the PDF is newer or
--force is given.

Source directories stay pure primary source; everything this script produces is
regenerable output and lives in derived/, matching the convention already used
by tn_comptroller_pilot_reports/derived/.

Also writes derived/pdf-index.csv: what each file is, how much text it has, and
whether that text is trustworthy or a machine's guess.

Usage: pdf-extract.py <file-or-directory> [...] [--force]

Stdlib + poppler + ocrmypdf. No venv, no model, no network.
"""

import csv
import os
import re
import subprocess
import sys

FULL_PAGE_PX = 1500      # a page image this wide is the page, not a logo
IMAGE_ONLY_CPP = 50      # below this there is no real text layer
OCR_SUSPECT_CPP = 1200   # scans OCR thinner than born-digital text


def run(cmd, timeout=1200):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except (subprocess.SubprocessError, OSError) as e:
        return 1, "", str(e)


def pdfinfo(path):
    _, out, _ = run(["pdfinfo", path], timeout=120)
    pages = re.search(r"^Pages:\s+(\d+)", out, re.M)
    prod = (re.search(r"^Producer:\s+(.+)$", out, re.M) or
            re.search(r"^Creator:\s+(.+)$", out, re.M))
    return (int(pages.group(1)) if pages else 0,
            prod.group(1).strip() if prod else "?")


def raster_share(path, pages):
    """Fraction of pages carrying a full-page image - the scan signature."""
    if not pages:
        return 0.0
    _, out, _ = run(["pdfimages", "-list", path], timeout=300)
    scanned = set()
    for line in out.splitlines()[2:]:
        f = line.split()
        if len(f) > 3 and f[0].isdigit() and f[3].isdigit():
            if int(f[3]) >= FULL_PAGE_PX:
                scanned.add(int(f[0]))
    return len(scanned) / pages


def to_text(path):
    """-layout keeps table columns aligned, which is the whole point on audits."""
    code, out, _ = run(["pdftotext", "-layout", path, "-"])
    return out if code == 0 else ""


def anchor(text):
    """Replace poppler's form feeds with greppable page markers."""
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return "\n".join(f"[[page {i}]]\n{p}" for i, p in enumerate(pages, 1))


def derived_dir(path):
    d = os.path.join(os.path.dirname(path) or ".", "derived")
    os.makedirs(d, exist_ok=True)
    return d


def ocr(path):
    """Returns the path to an OCR'd copy, or None. Original is never modified."""
    out = os.path.join(derived_dir(path),
                       re.sub(r"\.pdf$", "-ocr.pdf", os.path.basename(path),
                              flags=re.I))
    if os.path.exists(out):
        return out
    code, _, err = run(["ocrmypdf", "--output-type", "pdf", "--quiet", path, out])
    if code != 0:
        print(f"    ocr failed: {err.strip()[:120]}", file=sys.stderr)
        return None
    return out


def process(path, force):
    txt_path = os.path.join(derived_dir(path),
                            re.sub(r"\.pdf$", ".txt", os.path.basename(path),
                                   flags=re.I))
    if (not force and os.path.exists(txt_path)
            and os.path.getmtime(txt_path) >= os.path.getmtime(path)):
        return None

    pages, producer = pdfinfo(path)
    text = to_text(path)
    cpp = len(text) / pages if pages else 0
    share = raster_share(path, pages)
    source = os.path.basename(path)

    if cpp < IMAGE_ONLY_CPP:
        print(f"    no text layer - OCR'ing {pages}p (slow)")
        ocr_path = ocr(path)
        if ocr_path:
            text = to_text(ocr_path)
            cpp = len(text) / pages if pages else 0
            source = os.path.basename(ocr_path)
            kind = "OCR_SCAN"
        else:
            kind = "IMAGE_ONLY"
    elif share > 0.5:
        kind = "OCR_SCAN"
    elif cpp < OCR_SUSPECT_CPP:
        kind = "SPARSE"
    else:
        kind = "DIGITAL"

    with open(txt_path, "w") as fh:
        fh.write(anchor(text))

    return dict(text_file=os.path.basename(txt_path), source=source, pages=pages,
                chars=len(text), chars_per_page=round(cpp),
                raster_share=round(share, 2), kind=kind,
                trust=("verify figures against page image"
                       if kind in ("OCR_SCAN", "SPARSE", "IMAGE_ONLY")
                       else "extraction authoritative"),
                producer=producer)


def collect(args):
    out = []
    for a in args:
        if os.path.isdir(a):
            for root, dirs, files in os.walk(a):
                dirs[:] = [d for d in dirs if d != "derived"]
                out += [os.path.join(root, f) for f in sorted(files)
                        if f.lower().endswith(".pdf")]
        elif a.lower().endswith(".pdf"):
            out.append(a)
    return out


def main():
    args = [a for a in sys.argv[1:] if a != "--force"]
    force = "--force" in sys.argv[1:]
    paths = collect(args)
    if not paths:
        sys.exit("usage: pdf-extract.py <file-or-directory> [...] [--force]")

    by_dir, done, skipped = {}, 0, 0
    for p in paths:
        print(os.path.basename(p))
        row = process(p, force)
        if row is None:
            print("    up to date")
            skipped += 1
            continue
        print(f"    {row['kind']}  {row['pages']}p  {row['chars_per_page']} ch/pg")
        by_dir.setdefault(derived_dir(p), []).append(row)
        done += 1

    cols = ["text_file", "source", "kind", "pages", "chars", "chars_per_page",
            "raster_share", "trust", "producer"]
    for d, rows in by_dir.items():
        index = os.path.join(d, "pdf-index.csv")
        existing = []
        if os.path.exists(index):
            with open(index) as fh:
                existing = [r for r in csv.DictReader(fh)
                            if r["text_file"] not in {x["text_file"] for x in rows}]
        with open(index, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(sorted(existing + rows, key=lambda r: r["text_file"]))
        print(f"\nindex: {index}")

    print(f"{done} converted, {skipped} already current")


if __name__ == "__main__":
    main()
