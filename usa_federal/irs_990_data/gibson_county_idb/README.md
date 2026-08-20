# irs_990_data/gibson_county_idb/

## Purpose
The Gibson County IDB's federal filings and parcel records, held as the **closest available
clean comparison** to Gallatin: another rural Tennessee IDB, another large tenant (Tyson),
a similar land-acquisition sequence, and a 501(c)(6) classification. It is the control that
separates the ordinary IDB mechanism from what is specific to Gallatin.

## Contents
- `2019thru2025-gibson-990.xml` — raw IRS e-file XML, FY2019 through FY2025.
- `gibson_propublica_api_data.json` — ProPublica Nonprofit Explorer API pull, reaching back
  to 2012.
- `assessment-gibson-tyson.pdf`, `assessment-gibson-tyson2.pdf` — Gibson County parcel
  assessments for the Tyson property.
- `gibson_990_findings.md` — findings from the filings.
- `gibson_vs_gallatin_comparison.md` — the comparison itself, 2026-07-02, split into what
  does **not** distinguish Gallatin and what does.

## Source Type
**Primary Source** for the XML, the API pull, and the assessments.
**Working Material** for the two `.md` analyses, which are drafted findings, not sources.

## Handling Instructions
- **This is a control group, not a target.** Nothing here is an allegation about Gibson
  County or Tyson. Its value is in making Gallatin's numbers testable.
- The most useful section is the one listing what does **not** distinguish Gallatin: the
  out-of-state mailing address routed through the tenant, the quitclaim to warranty deed to
  quitclaim sequence, and the absence of an independent audit all appear in Gibson too.
  Anything on that list is unusable as evidence of wrongdoing and should not be argued in
  print.
- What survives the comparison is governance and reporting: filing every year without gaps,
  a consistent verbatim mission statement, real Schedule O governance disclosure, itemized
  expenses, a named licensed CPA firm, and a ten-member independent board.
- Cite figures to the XML or the assessment PDF, never to the two analysis files.

## Notes
Gibson files as a 501(c)(6). Gallatin filed as a 501(c)(4). The question of why that choice
was available and what it required is worked in
`web/content/reference/501c4-vs-instrumentality.md`, and the comparison here is the empirical half of
that argument.

The matching PILOT registry filings were in
~~`state_of_tennessee/tn_comptroller_pilot_reports/gibson_county/`~~ and were **moved out of
the project 2026-08-19**. Some of those files are statewide reports saved under a county name and at least one pair
extracts to byte-identical text, so the filenames do not describe the contents. Re-pull from
the Comptroller before making a direct Gibson comparison in print. The 990 material in this
directory is a separate, verified thread and is unaffected.
