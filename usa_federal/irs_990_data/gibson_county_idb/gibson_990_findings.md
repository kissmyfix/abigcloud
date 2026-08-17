# Gibson County IDB — 990 Findings (2026-07-02)

**Source:** ProPublica Nonprofit Explorer public API (`gibson_propublica_api_data.json`, EIN 20-2703372). Direct PDF downloads from ProPublica's S3 bucket returned Access Denied regardless of request method — the line-item financial data below comes from ProPublica's structured API instead, which covers every filing 2012–2024.

## Identity
- Industrial Development Board of Gibson County Tennessee, Trenton, TN.
- **501(c)(6)**, ruling date September 1, 2005 — confirmed directly via API field `subsection_code: 6`, not just inferred.
- Care-of contact on file: **Ronnie Riley**.
- Files every year, going back to at least 2012, without gaps.

## The key structural difference from Gallatin: zero rental income, ever

Every single filing year from 2012 through 2024 reports **$0** in both `grsrntsreal` (gross rents, real property) and `grsrntsprsnl` (gross rents, personal property) — not a small number, an exact zero, every year, no exceptions.

| Year | Total Revenue | Rents (real+personal) | Net gain on sales | Misc. revenue |
|---|---|---|---|---|
| 2024 | $43,535 | $0 | $0 | $36,152 |
| 2023 | $36,762 | $0 | $0 | $30,386 |
| 2022 | $1,952,887 | $0 | $1,882,544 | $68,959 |
| 2021 | $443,210 | $0 | $395,939 | $46,958 |
| 2020 | $42,461 | $0 | $0 | $41,836 |
| 2019 | $33,371 | $0 | $0 | $32,524 |
| 2018 | $51,012 | $0 | $0 | $50,202 |
| 2017 | $51,075 | $0 | $0 | $50,550 |
| 2016 | $57,300 | $0 | $0 | $56,878 |
| 2015 | $75,169 | $0 | $0 | $63,907 |
| 2014 | $72,725 | $0 | $0 | $72,607 |
| 2013 | $65,616 | $0 | $0 | $65,510 |
| 2012 | $52,314 | $0 | $0 | $52,177 |

This is the opposite revenue structure from Gallatin's IDB, where rent is 90.2% of all tracked money across 11 entities. Gibson County's IDB doesn't appear to hold land long-term as a landlord collecting perpetual rent from tenants at all. Its revenue is almost entirely small "miscellaneous revenue" year to year (likely administrative/PILOT-related fee income), punctuated twice — 2021 and 2022 — by large one-time gains on asset sales ($395,939 and $1,882,544 respectively, against gross sale proceeds of $923,338 and $2,088,800). That pattern reads as: acquire land, hold briefly, then **sell the land outright to the company** — converting the property back to private, taxable ownership — rather than retaining title indefinitely as landlord while the tenant pays "rent" that never gets shared or disclosed the way a PILOT payment would be.

If that reading holds, it's a meaningfully more transparent structure: the land eventually returns to the normal tax rolls under private ownership, rather than staying IDB-owned and tax-exempt in perpetuity while cash quietly flows as "rent." Worth confirming against Gibson County's actual PILOT agreements and property records, not just the 990 numbers, before treating this as settled.

## Full revenue/expense/net income/assets table, 2012–2025 (confirmed 2026-07-02)

Cross-checked against Brandon's own manual read of ProPublica's page (2012–2018) against the API pull (2019–2025) — all figures match exactly.

| Year | Revenue | Expenses | Net Income | Net Assets |
|---|---|---|---|---|
| 2012 | $52,314 | $110,306 | -$57,992 | $2,781,661 |
| 2013 | $65,616 | $2,936 | $62,680 | $2,844,341 |
| 2014 | $72,725 | $96,093 | -$23,368 | $2,820,973 |
| 2015 | $75,169 | $5,844 | $69,325 | $2,890,299 |
| 2016 | $57,300 | $12,573 | $44,727 | $2,935,026 |
| 2017 | $51,075 | $58,606 | -$7,531 | $2,927,495 |
| 2018 | $51,012 | $65,447 | -$14,435 | $2,913,060 |
| 2019 | $33,371 | $69,753 | -$36,382 | $2,876,678 |
| 2020 | $42,461 | $13,199 | $29,262 | $2,905,940 |
| 2021 | $443,210 | $663,078 | -$219,868 | $2,686,074 |
| 2022 | $1,952,887 | $559,816 | $1,393,071 | $4,079,148 |
| 2023 | $36,762 | $881,844 | -$845,082 | $3,234,068 |
| 2024 | $43,535 | $54,928 | -$11,393 | $3,228,333 |
| 2025 | $453,617 | $96,530 | $357,087 | $3,585,420 |

Net assets stay roughly in the $2.7–2.9M range for a decade (2012–2020), showing no meaningful growth from tenant activity — consistent with the finding above that the IDB never touches PILOT/rent money. The two big net-asset jumps (2021→2022, then again by 2025) both trace to one-time investment/securities activity, not tenant payments.

## Obtained since initial pass
Raw XML e-file data for FYs 2023 and 2024 (`2019thru2025-gibson-990.xml`, provided by Brandon) gave the qualitative detail the API alone didn't: mission statement text, Schedule O governance narrative, full Part VII board/officer list, and itemized Part IX expense detail. See `gibson_vs_gallatin_comparison.md` for the full breakdown of what that revealed.

## Not yet obtained
- Gibson County government/council meeting records showing how they vote on and manage their PILOT program publicly — likely a richer source than the 990 for finding the actual governance contrast with Gallatin. Still the next step per Brandon's original direction.
