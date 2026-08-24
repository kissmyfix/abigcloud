# Finding Aid — gallatin_electric_utility/rates/

Seventeen City of Gallatin Department of Electricity rate summary sheets, January 2016
through June 2026. `pdf-index.csv` records extraction trust. This file records what is in
them, and `rate-history.csv` beside it holds the numbers as a table.

Built 2026-08-24.

---

## rate-history.csv

Every rate line from every sheet, 641 rows.

`file, effective, rate_class, line, base_rate, fuel_cost, effective_rate`

Rate classes as the sheets name them:

| Class | Scope |
|---|---|
| `RESIDENTIAL` | households |
| `GSA1` | under 50 kW, not more than 15,000 kWh |
| `GSA2` | 50–1,000 kW, or under 50 kW with usage over 15,000 kWh |
| `GSA3` | 1,000–5,000 kW |
| `TD_GSA` | time-of-day general service; first appears in the 2020 sheet |
| `GSB` | 5,001–15,000 kW |
| `MSB` | greater than 5,000 kW |
| `MSD` | **greater than 25,000 kW** |
| `OUTDOOR` | outdoor and street lighting |

Rebuild by re-running the extraction in this directory's history; the CSV is derived output
and safe to regenerate.

---

## What the series shows

### The residential fixed charge has nearly doubled, and the rise accelerates in 2024

The customer charge is billed before a single kilowatt-hour is used, so it falls hardest on
low-usage households.

| Sheet | Customer charge |
|---|---|
| Jan 2016 – Jun 2018 | $13.55 |
| Jan 2019 – Jun 2023 | $16.55 |
| Jun 2024 | $19.61 |
| Jun 2025 | $22.61 |
| Jun 2026 | $25.61 |

Flat for three years, one $3.00 step in 2019, flat for five more, then **$3.00 every year
from 2024**. From $13.55 to $25.61 is a rise of 89% across the series, and two thirds of it
lands in the last three sheets.

### The energy rate moves far less

Residential summer rates, cents per kWh:

| Sheet | Base | Fuel | Effective |
|---|---|---|---|
| Jun 2016 | 6.713 | 1.901 | 8.614 |
| Jun 2018 | 7.026 | 1.946 | 8.972 |
| Jun 2020 | 7.246 | 1.476 | 8.722 |
| Jun 2022 | 7.246 | 2.809 | 10.055 |
| Jun 2023 | 7.246 | 2.526 | 9.772 |
| Jun 2024 | 7.707 | 2.013 | 9.720 |
| Jun 2025 | 8.202 | 2.784 | 10.986 |
| Jun 2026 | 8.388 | 2.741 | 11.129 |

The base rate sat at 7.246₵ from 2019 through 2023, then rose in each of the last three
sheets. The fuel cost is volatile in both directions and is a pass-through, so movement
there is not a local decision. **Read the base rate, not the effective rate, when the
question is what the utility chose to charge.**

### Commercial fixed charges over the same span

| Class | Jan 2016 | Jun 2026 |
|---|---|---|
| GSA1 | $16.60 | $28.60 |
| GSA2 | $40.00 | $78.00 |
| GSA3 | $150.00 | $218.00 |
| GSB / MSB / MSD | — | $1,500.00 |

GSA3 rose 45% while residential rose 89%. Whether the largest classes moved at all across
the series has **not** been established: the $1,500.00 charge is confirmed present in the
2025 and 2026 sheets, and the earlier sheets have not been checked line by line for the
same figure. That comparison is the obvious next question and it is not answered here.

---

## What this directory cannot tell you

- **Which class the data center is billed under.** MSD covers demand greater than 25,000 kW
  and existed in the 2016 sheets, well before the facility. The rate schedule is a published
  tariff and names no customer.
- **What any customer actually paid.** These are posted rates, not bills or contracts.
- **Whether a special contract exists.** A negotiated large-load arrangement would not
  appear on a summary rate sheet.

## Gaps and shape of the series

Annual June sheets run unbroken 2016–2026. Extra sheets exist for January and December
2016, March 2017, and January and May 2019, which is where mid-year changes are visible.
`2019-june.txt` is 2.7KB against ~15KB for its neighbours and is not a full schedule; check
the PDF before relying on it. `2026-outdoor.pdf` is a standalone outdoor-lighting sheet and
is excluded from the CSV.

Several older sheets carry `TBA` in the fuel cost and effective rate columns; those are
recorded as `TBA` rather than dropped.
