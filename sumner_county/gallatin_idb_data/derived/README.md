# gallatin_idb_data/derived/

## Purpose
Plain-text extraction of the Gallatin IDB source documents in the parent directory.

## Contents
- `1994-2026-idb-gallatin.txt` — the full Secretary of State filing history for the
  Industrial Development Board of the City of Gallatin, 1994 to 2026. This is the record
  behind the principal-office and registered-agent chronology in `memory/MEMORY.md`,
  including the 2018-07-19 move from the City Attorney's office to GEDA and the 2021-07-12
  agent change to Preston Stark.
- `pdf-index.csv` — kind, pages, and trust rating per source file.

## Source Type
**Derived.** Machine output from `files/bin/pdf-extract.py`. Regenerable, never
hand-edited. See the `derived/` convention in `files/DATA_MAP.md`.

## Handling Instructions
- Cite `sumner_county/gallatin_idb_data/1994-2026-idb-gallatin.pdf`, the source document,
  not this text file.
- Dates and filing types in this record carry a lot of weight in the case. Confirm any date
  against the page image before it is published.
- Search here freely.

## Notes
The filing history is the single most cited source in `memory/MEMORY.md`. Treat a
discrepancy between this text and the PDF as an extraction fault, not a records fault, and
re-run the extractor.
