# tn_comptroller_pilot_reports/gibson_county/

## Purpose
Gibson County's PILOT filings, held as a **control group**. Gibson's IDB runs a comparable
arrangement with Tyson and files as a 501(c)(6), which is the classification the Gallatin
IDB did not use. This directory exists so Gallatin's numbers can be tested against a
working example rather than asserted as abnormal.

## Contents
- `2015-pilot-gibson.pdf` through `2022-pilot-gibson.pdf` — one report per year.
- `2023-2025-pilot-gibson.ods` — the later years, published as a spreadsheet rather than a
  PDF.

## Source Type
**Primary Source.** Tennessee Comptroller of the Treasury PILOT registry filings.

## Handling Instructions
- This is a baseline, not evidence against Gibson County. Nothing here is an allegation
  about Gibson.
- The registry is self-reported by the boards. It records what an IDB told the state, which
  is a different fact from what happened.
- Reported `$0` and NO INFO are different states. Do not merge them.
- Nine files, no `derived/` yet. Run `files/bin/pdf-extract.py` if these need searching at
  volume.

## Notes
The comparison that makes this directory matter is in `usa_federal/irs_990_data/
gibson_county_idb/`, which holds Gibson's 990 filings and the Gibson versus Gallatin
writeup. Read the two together.
