# Gallatin IDB federal filings, FY2020–21 through FY2024–25

Five 990 filings by the Industrial Development Board, EIN 38-4171308, standardized
into one machine-readable file. The wording is the evidence here as much as the
numbers, so every self-description is stored **verbatim, typos included**.

## Files

| File | What it is |
|---|---|
| `gallatin-idb-990.json` | **The dataset.** 5 filings, FY2020–21 to FY2024–25. |
| `files/bin/verify-990.py` | Four independent checks. See below. |
| `idb2020.pdf` – `idb2024.pdf` | Source filings, one per year. |
| `irs-search-results.pdf` | IRS exempt-organization search capture. |

Run `python3 files/bin/verify-990.py` from anywhere.

## This is a transcription, not a parse

**Read this before trusting any figure.** `idb2020` through `idb2023` are
image-only PDFs with no text layer, and this machine has no OCR installed. Those
four filings were read by eye. Only `idb2024.pdf` has machine-readable text (a
ProPublica visual render).

That is a real weakness and the verification is built around it rather than
around a parser:

- **A, internal arithmetic.** Each filing's own lines must close: revenue and
  expense itemizations sum to their totals, expense columns sum across, revenue
  less expenses reconciles, and net assets roll forward through prior-period
  adjustments to the stated end-of-year figure. 23 checks.
- **B, cross-year chain.** End-of-year net assets in each filing must equal
  beginning-of-year in the next. This is the strong one: it spans five separately
  transcribed documents, so one mistyped digit anywhere breaks it. 4 checks.
- **C, restatement check.** Each filing's own prior-year column against what the
  prior filing actually reported. Differences are reported as findings, not
  errors, because a restatement is the filer's doing.
- **D, text layer.** 2024 re-read mechanically from the PDF and matched against
  the transcription line by line. 15 checks.

All checks agree. Pass C surfaces one restatement, below.

**Transcription is complete.** All 80 pages across the five filings have been
read. Remaining `null` values are facts about the forms, not gaps: the 2020
990-EZ has no Part VI governance section at all, `states_filed` is blank on every
return (Part VI line 17), and `volunteers` is blank in 2023 and 2024. Nothing is
guessed.

## What the filings say

| Year | Form | Revenue | Expenses | Net assets, end |
|---|---|---|---|---|
| 2020 | 990-EZ | $100,048 | $114,692 | $88,304 |
| 2021 | 990 | $145,425 | $136,802 | $98,131 |
| 2022 | 990 | $334,268 | $244,797 | $187,602 |
| 2023 | 990 | $1,796,648 | $1,079,908 | $904,342 |
| 2024 | 990 | $2,242,221 | $2,998,536 | $148,027 |

$4,419,400 of PILOT revenue across the five filings. $1,616,159 paid to Sumner
County Schools, all of it in 2022 or later.

## Findings the dataset carries

**The organization's name changes across the filings.** "Industrial Developement
Board of the City of Gallatin Tennessee" (2020, misspelled), "Industrial
Development Board of the City of Gallatin TN" (2021), "INDUSTRIAL DEVELOPMNET
BOARD OF THE GALLATIN TN" (2022, misspelled differently and **"City of" dropped**),
then "INDUSTRIAL DEVELOPMENT BOARD OF THE GALLATIN TN" (2023, 2024). No
`Name change` box is ticked in any year.

**The stated purpose is replaced between 2021 and 2022.** 2020 and 2021 both say
"Recruit and facilitate industrial development in the City of Gallatin." From
2022 the mission line reads "THE IDB IS RESPONSIBLE FOR ADMINSTRATION OF THE
PILOT PROGRAM." Recruiting industry is at least arguable as 501(c)(4) social
welfare. Administering a tax substitute is a government revenue function. Note
that the 2022 filing answers **No** to Part III lines 2 and 3, which ask whether
program services changed; 2023 leaves both blank.

**"The county (Gallatin)."** 2021's Part III reads "payments to the couty
Gallatin in which the City of Gallatin is located." From 2022 the same claim is
in the mission line as "THE COUNTY (GALLATIN)". The county is Sumner. A
parenthetical is an act of clarification, not a typo, so the 2022 edit resolved
the prior year's ambiguity toward the false reading.

**The 2020 filing describes the same money two ways.** Part III reports $70,548
of program services split as Sumner County $17,474, Beretta $39,919, Bradford
$13,155. Schedule O explains line 16 as "Summer County 69549" plus "Legal 5557."
The county's share is $69,549 in one place and $17,474 in the other.

**Two of the three largest 2020 program service accomplishments are payments to
private for-profit corporations.**

**Formation year reported as 2020 in every filing**, and `Initial return` is
ticked in both 2020 and 2021. The 2020 return reports $102,948 of beginning-of-year
net assets. The board executed land transfers in 2014 (see
`state_of_tennessee/tn_property_assessments/`).

**The 2021 filing restates 2020 expenses as $114,690.** The 2020 filing itself
reported $114,692. Caught by pass C.

**2023 is the retention year.** $1,758,136 of PILOT payments came in, $155,475
went out as PILOT distributions, $901,080 went to schools, and $716,740 stayed,
taking net assets from $187,602 to $904,342. In 2024 that reversed: $2,291,692
distributed against $2,210,996 received, drawing the balance down to $148,027.

**The expense line is renamed.** "Property taxes" (2021, 2022) becomes "PILOT
FEES DISTRIBUTED" (2023, 2024), describing the same outbound flow.

**$45,000 consulting and $12,000 management fees in 2024 with zero Forms 1096
filed** (Part V line 1a).

**Part VI line 11a contradicts Schedule O on the same return, three years
running.** Line 11a asks whether a complete copy of the return was given to every
member of the governing body *before filing*. 2021, 2022 and 2023 all answer
**Yes**. Schedule O on those same returns says the opposite: in 2021, "Due to time
constraints, the board reviews the Form 990 after it is filed"; in 2022 and 2023,
"THE BOARD ADMINISTRATOR REVIEWS IT PRIOR TO FILING. THE BOARD REVIEWS THE FORM AT
THE NEXT BOARD MEETING." In 2024 line 11a is answered **No**, which is the first
year the checkbox and the narrative agree.

**Both self-descriptions appear in the same return, in 2022 and 2023.** The
mission line says the IDB administers the PILOT program. Part III line 4a, in the
Additional Data, still says "RECRUIT AND FACILITATE INDUSTRIAL DEVELOPMENT IN TH
ECITY OF GALLATIN TN". The old purpose was never removed, only demoted.

**The board does not review the return before it is filed.** 2021 Schedule O:
"Due to time constraints, the board reviews the Form 990 after it is filed. The
board administrator reviews it prior to filing." Softened by 2024 to "THE BOARD
REVIEWS THE FORM AT THE NEXT BOARD MEETING." Preston Stark signs every filing
under penalty of perjury as Board Administrator.

**The board turns over and Preston Stark joins it.** 2020 and 2021 list seven
members. Stark is not among them; he signs as Board Administrator. From 2022 he
is listed in Part VII as an officer while continuing to sign the return. The 2022
board is ten, 2023 nine, 2024 ten. Allan Ramsey chairs 2020 through 2023, then
drops to board member in 2024 with Neil Burgess taking the chair. Leonard
Assante's surname is spelled "ASSANTTE" from 2022 on, and the chair's given name
appears as both "Allen" (2020) and "Allan" (2021 onward).

**Three preparers in five years.** J Michael Patterson, Knoxville (2020); Joe
Osterfeld CPA, Columbia (2021); John P Young PC, Hendersonville (2022–2024).

**Accounting method changed from cash to accrual** between 2021 and 2022, and the
financial statements went from compiled-not-audited to audited in the same year.

## Handling

- Cite by filing year and part/line number, never from this README alone
- The `flags` array on each record is observation, not conclusion
- Verify any figure against the filing itself before it goes into a draft; four
  of five were read by eye
- `501(c)(4)` requires operation primarily to promote the common good and general
  welfare, not "charity" in the 501(c)(3) sense. Any argument about exempt status
  has to be made on that standard.
