#!/usr/bin/env python3
"""Index an inbox of unprocessed documents.

Answers, for a pile of files nobody has read yet: what is each one, who is it
about, what period does it cover, and can its extracted text be trusted.

Everything except the last two columns is derived from the file itself and gets
recomputed on every run. `status` and `notes` are yours; they are read back out of
the existing index and carried forward, so re-running never loses a note.

Usage: inbox-index.py <inbox-dir> [-o INDEX.csv]

Stdlib + poppler-utils only.
"""

import argparse
import csv
import os
import re
import subprocess
import sys

# Below this, whatever text a page carries is furniture, not content.
IMAGE_ONLY_CPP = 50
# Scans OCR thinner than born-digital text of the same layout.
OCR_SUSPECT_CPP = 1200

# filename prefix -> what the file is about. Longest match wins, so the
# three near-identical daycare names cannot collide.
ENTITY = [
    ("shalomzone",                "Gallatin Shalom Zone"),
    ("shalom2",                   "Gallatin Shalom Zone"),
    ("midcumberland-caa",         "Mid-Cumberland Community Action Agency"),
    ("gallatin-day-care-center",  "Gallatin Day Care Center Inc (EIN 62-6085831)"),
    ("gallatin-child-care-center","Gallatin Child Care Center Inc (EIN 32-0176348)"),
    ("gallatin-daycare-sos",      "Gallatin Day Care Centers I & II Inc"),
    ("SOS-gallatin-day-care",     "Gallatin Day Care Centers I & II Inc"),
    ("good-neighbor-mission",     "Good Neighbor Mission & Crisis Center"),
    ("unionhigh-museum",          "Union High School Museum Council"),
    ("southern-sudanese",         "Southern Sudanese Youth Connection"),
    ("tutlam-foundation",         "Dr Timothy T Tutlam Foundation"),
    ("PAYING-SIDE-idb",           "Gallatin IDB"),
    ("SOS-gallatin-idb",          "Gallatin IDB"),
    ("SOS-preston-stark",         "Preston Stark Inc"),
    ("2002-preston-stark",        "Preston Stark Inc"),
    ("1983-11-16-tennessean",     "Preston Stark (identity unconfirmed)"),
    ("NOTES-preston_stark",       "Preston Stark"),
    ("NOTES-rosemary_bates",      "Rosemary Bates"),
    ("CAPSTONE-bates",            "Rosemary Bates"),
    ("EXCERPT-leon",              "Lilibeth Leon capstone"),
    ("PARCEL-108-southpark",      "108 Southpark Circle"),
    ("PARCEL-112-southpark",      "112 Southpark Circle"),
    ("sumner-assessment-daycare-108", "108 Southpark Circle"),
    ("sumner-assessment-daycare-112", "112 Southpark Circle"),
    ("BMF-600-small",             "600 Small Street (all tenants)"),
]

DOCTYPE = [
    (r"-\d{6}-990EZ",        "IRS Form 990-EZ"),
    (r"-\d{6}-990ER",        "IRS Form 990 (ER)"),
    (r"-\d{6}-990\b",        "IRS Form 990"),
    (r"^shalom20\d\d",       "IRS Form 990"),
    (r"^PAYING-SIDE-idb",    "IRS Form 990"),
    (r"^SOS-|sos-entity",    "TN Secretary of State entity record"),
    (r"^PARCEL-|assessment", "Sumner County assessor parcel record"),
    (r"^BMF-",               "IRS Business Master File extract"),
    (r"^CAPSTONE-",          "UT CIS capstone paper"),
    (r"^EXCERPT-",           "Excerpt from a larger project file"),
    (r"^NOTES",              "Our working notes (not a source)"),
    (r"tennessean",          "Newspaper page"),
    (r"^\d{4}-\d{2}-\d{2}-", "News article"),
]

PERIOD = [
    (r"-(\d{4})(\d{2})-990", lambda m: f"FYE {m.group(2)}/{m.group(1)}"),
    (r"^(\d{4})-(\d{2})-(\d{2})-", lambda m: f"{m.group(1)}-{m.group(2)}-{m.group(3)}"),
    (r"(\d{4})-\d{2}-\d{2}\.pdf$", lambda m: f"pulled {m.group(1)}"),
]


def sh(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=120).stdout
    except Exception:
        return ""


def classify(path):
    """(kind, pages, chars_per_page, trust, producer) for a PDF."""
    info = sh(["pdfinfo", path])
    pages = re.search(r"^Pages:\s+(\d+)", info, re.M)
    pages = int(pages.group(1)) if pages else 0
    producer = re.search(r"^Producer:\s+(.+)$", info, re.M)
    producer = producer.group(1).strip() if producer else ""
    text = sh(["pdftotext", "-layout", path, "-"])
    cpp = len(text) / pages if pages else 0
    # A full-page image on most pages means the text is an OCR guess over a scan.
    images = sh(["pdfimages", "-list", path])
    big = sum(1 for ln in images.splitlines()[2:] if re.search(r"\b1[5-9]\d\d|\b[2-9]\d{3}", ln))
    raster = big / pages if pages else 0
    if cpp < IMAGE_ONLY_CPP:
        return "IMAGE_ONLY", pages, cpp, "no usable text; read the page image", producer
    if raster >= 0.5 or (cpp < OCR_SUSPECT_CPP and raster > 0):
        return "OCR_SCAN", pages, cpp, "verify every figure against the page image", producer
    return "DIGITAL", pages, cpp, "extraction authoritative", producer


def first_match(table, name):
    for key, val in sorted(table, key=lambda kv: -len(kv[0])):
        if key in name:
            return val
    return ""


def regex_match(table, name):
    for pat, val in table:
        m = re.search(pat, name)
        if m:
            return val(m) if callable(val) else val
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inbox")
    ap.add_argument("-o", "--out", default=None)
    a = ap.parse_args()
    out = a.out or os.path.join(os.path.dirname(a.inbox.rstrip("/")), "INDEX.csv")

    # Carry forward anything a human wrote.
    kept = {}
    if os.path.exists(out):
        with open(out, newline="") as f:
            for row in csv.DictReader(f):
                kept[row["file"]] = (row.get("status", ""), row.get("notes", ""))

    rows = []
    for name in sorted(os.listdir(a.inbox)):
        path = os.path.join(a.inbox, name)
        if not os.path.isfile(path):
            continue
        size_kb = round(os.path.getsize(path) / 1024)
        if name.lower().endswith(".pdf"):
            kind, pages, cpp, trust, producer = classify(path)
        else:
            kind, pages, cpp, trust, producer = "TEXT", "", "", "extraction authoritative", ""
        status, notes = kept.get(name, ("unread", ""))
        rows.append({
            "file": name,
            "entity": first_match(ENTITY, name),
            "doc_type": regex_match(DOCTYPE, name),
            "period": regex_match(PERIOD, name),
            "kind": kind,
            "pages": pages,
            "size_kb": size_kb,
            "extract_trust": trust,
            "producer": producer,
            "status": status,
            "notes": notes,
        })

    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    counts = {}
    for r in rows:
        counts[r["kind"]] = counts.get(r["kind"], 0) + 1
    print(f"{len(rows)} files -> {out}")
    print("  " + ", ".join(f"{v} {k}" for k, v in sorted(counts.items())))
    unread = sum(1 for r in rows if r["status"] == "unread")
    print(f"  {unread} unread")


if __name__ == "__main__":
    main()
