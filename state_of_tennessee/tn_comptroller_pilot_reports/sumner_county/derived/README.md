# tn_comptroller_pilot_reports/sumner_county/derived/

## Purpose
Holds the parsed dataset built from the Comptroller PILOT report excerpts in the parent
directory.

## Contents
- `sumner-pilot.json` — 131 filing lines, 2015 to 2025. Built by `files/bin/parse-sumner-pilot.py`
  from the yearly PDFs and the 2023 to 2025 spreadsheet. Checked by `files/bin/verify-sumner-pilot.py`,
  which recounts every year straight from the source and prints ALL AGREE or the
  disagreement.

## Source Type
**Derived.** Machine output, regenerable, never hand-edited. See the `derived/` convention
in `files/DATA_MAP.md`.

## Handling Instructions
- Regenerate from the project root with `python3 files/bin/parse-sumner-pilot.py`, then
  `python3 files/bin/verify-sumner-pilot.py` to verify.
- `parcel_id` joins to
  `state_of_tennessee/tn_property_assessments/derived/sumner-assessments.json`.
- The registry distinguishes a reported `$0` from a row marked NO INFO, which means
  withheld or unreported without saying which. **Never collapse those into one "no data"
  state**, in analysis, in copy, or in chart color.
- Cite the Comptroller report for any published figure, not this file.

## Notes
Read the parent README first. It explains that these PDFs are not Sumner-only reports but
crops of the statewide roll, which affects what the row counts mean.
