# sumner_county/gallatin_council_meetings/derived/

## Purpose
The machine reading of the council packets in the parent directory — page-anchored text so a
600-page scan can be searched in seconds, plus the two index CSVs that say what each document
actually is and whether it can be trusted as text.

## Contents
- `*.txt` — one per source PDF, page-anchored with `[[page N]]` at the top of each page.
- `ocr/` — the packets whose original text layer covered only part of the document, re-OCR'd
  with `ocrmypdf`, plus their extracted text. The PDFs in the parent directory are the record
  and are never modified by this process.
- `pdf-index.csv` — extraction class and text volume per file (`files/bin/pdf-extract.py`).
- `council-index.csv` — one row per document: the date the city printed on it, the date in the
  filename, whether those agree, meeting body, page count, textless pages, extraction class,
  whether it is quotable without opening the page image, md5, and duplicates.

## Source Type
**Derived.** Machine output. Regenerable, never hand-edited — see the `derived/` convention in
`files/DATA_MAP.md`.

## Regenerating
```
files/venv/bin/python files/bin/build-council-index.py     # rebuilds council-index.csv
files/venv/bin/python files/bin/verify-council-index.py    # recounts from source, asserts
                                                           # known anchors, exits nonzero on failure
```
Extraction and OCR are `files/bin/pdf-extract.py` (`--redo-ocr` to force a re-OCR).

## Handling Instructions
- **Quote from the PDF, cite the PDF, with the packet page number.** The text here is a
  reading aid.
- OCR'd text is a machine guess even when it reads cleanly. `council-index.csv` marks which
  documents are quotable straight from text and which are not — check it before quoting.
- A hand edit here is silently destroyed on the next run and makes the file unusable as
  evidence. Fix the script instead.

## Notes
Four documents in the parent are born-digital and quotable from text; everything else is a
scan. The March 7 2023 packet is the case for the OCR pass — page 1 was born-digital and pages
2–62 were image-only, and those pages carry the February 7 2023 council minutes in full.
