# tn_property_assessments/derived/

## Purpose
Holds the parsed dataset built from the Parcel Details Reports in the parent directory.

## Contents
- `sumner-assessments.json` — 4 parcels, Tax Year 2026, one record each. Built by
  `files/bin/parse-assessment.py` from word coordinates, verified four independent ways by
  `files/bin/verify-assessments.py`.

## Source Type
**Derived.** Machine output, regenerable, never hand-edited. See the `derived/` convention
in `files/DATA_MAP.md`.

## Handling Instructions
- Regenerate from the project root with `python3 files/bin/parse-assessment.py`, then
  `python3 files/bin/verify-assessments.py`. Both resolve this directory from their own
  location, so they run from anywhere. The verifier exits nonzero on any disagreement.
- `parcel_id` is written in the same shape the Comptroller PILOT filings use
  (`111 00100 000`), so this dataset joins to
  `tn_comptroller_pilot_reports/sumner_county/derived/sumner-pilot.json` on that key.
- Money keeps its `raw` source string alongside the typed `usd`. `null` means the report
  printed nothing; `0` means it printed zero. Do not collapse the two.
- Cite the parcel report PDF for any published figure, not this file.

## Notes
The full account of what the sources are, how they were parsed, what the verification
passes check, and the unresolved $531M versus $519,189,800 discrepancy lives in the parent
directory's README. Read that before using the data.
