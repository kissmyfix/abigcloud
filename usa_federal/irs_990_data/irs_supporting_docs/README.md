# irs_990_data/irs_supporting_docs/

## Purpose
The IRS's own bulk exempt-organization data files, held so that questions about the whole
population of Tennessee nonprofits can be answered locally instead of one lookup at a time.
This is what makes claims like "eight IDBs in Tennessee, six filing as 501(c)(6), one as a
501(c)(4)" checkable rather than anecdotal.

## Contents
Nine years of IRS Exempt Organizations Financial Extracts, 2016 through 2024, two files per
year:
- `NNeoextract990.zip` / `NNeofinextract990.zip` — the extract archives, plus `...ez.zip`
  for the 990-EZ population in 2019 and 2020.
- `NNeofinextractdoc.xls` / `.xlsx` — the record layout for that year. **Read the layout
  before parsing the data.** Column positions and field names change between years.

`irs990-501c-tn.png` is a screenshot of a Tennessee 501(c) search result.

## Source Type
**Primary Source.** Published bulk data from the IRS.

## Handling Instructions
- **Population data, not entity evidence.** Use it to establish what is normal, how many
  organizations do a thing, and where an entity sits in a distribution. A single
  organization's specifics come from its own filings in the sibling directories.
- The layout documents are not optional. A year parsed against the wrong layout produces
  numbers that look plausible and are wrong.
- These are compressed archives. Extract to a scratch directory, not into this one, and do
  not commit expanded copies back here.
- No `derived/` yet. Anything built from these belongs in one, with the script in
  `files/bin/`.

## Notes
Bulk extracts are filing-year based and lag the fiscal years they describe. When comparing
against Comptroller PILOT registry data, confirm the year alignment first. That correction
has already changed a conclusion once in this investigation.
