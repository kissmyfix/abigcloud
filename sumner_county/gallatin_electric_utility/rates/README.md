# gallatin_electric_utility/rates/

## Purpose
Gallatin Department of Electricity rate sheets over time, plus one household billing
history. This is the ratepayer-harm instrument: the question of whether ordinary customers
carried infrastructure costs the Meta facility required.

## Contents
17 rate-sheet PDFs, 2016 to 2026. Coverage is standardized on **June** wherever the June
sheet exists, so year-over-year comparisons hold; the off-month files (`2016-jan`,
`2016-dec`, `2017-march`, `2019-jan`, `2019-may`) are where June was unavailable or where a
mid-year change was captured.

`2026-outdoor.pdf` is outdoor lighting, a separate schedule.

`billing-history.csv` is Brandon's own household billing history, supplied as a test case.

## Source Type
**Primary Source** for the rate sheets, published by the utility.
**Working Material** for `billing-history.csv`.

## Handling Instructions
- **The household data is not representative and Brandon said so himself, three separate
  ways:** two adults rather than an average household, service through NES rather than GDE,
  and Meta may not even fall in that jurisdiction. Any use of it must carry those
  qualifications. It is a worked example, not a finding.
- Compare like months. The June standardization exists for that reason.
- A rate increase is not by itself evidence of cost-shifting. Establish what drove it before
  connecting it to anything.
- Any published claim about ratepayer impact needs the substation and infrastructure
  documents, not just these sheets.

## Notes
The TVA in-lieu-of-tax and power agreement material in `usa_federal/tva/` is the other half
of this thread. The open question that connects them is the roughly $9M substation built for
Meta's load, and whether it was rate-base funded.

**Renamed 2026-07-29:** `BillingHistory.csv` is now `billing-history.csv`.
