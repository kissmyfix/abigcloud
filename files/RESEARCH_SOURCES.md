# Research sources

The websites this investigation keeps returning to, and the exact way into each one.

Most of these are hard to get back to not because the site is obscure but because the
useful page is six clicks deep behind a search form that does not put anything in the URL.
Where a direct link works, it is here. Where it does not, the search that works is here
instead.

**Do not treat any of these as ground truth.** An institution's own website is evidence
about that institution. See `CLAUDE.md`, Evidence discipline.

---

## Tennessee state records

**TN Property Assessment Data (TPAD)** — `https://assessment.cot.tn.gov/TPAD/`
Every parcel in the state: owner, appraised value, assessed value, sale history, map.
This is where the $519M-appraised, $0-assessed finding comes from. Jurisdiction codes are
part of every URL: **083 = Sumner County**, **027 = Gibson County**.

Parcels already pulled for this investigation:

| Jur | Parcel | What it is |
|---|---|---|
| 083 | 112 10900 000 | Gallatin Industrial |
| 083 | 112 11100 000 | Gallatin Industrial |
| 083 | 112 11200 000 | Gallatin Industrial |
| 083 | 112 01202 000 | — |
| 083 | 112 01206 000 | — |
| 083 | 125 03900 000 | — |
| 027 | 165 00106 001 | Gibson County comparison |

**TN Secretary of State — business search** — `https://sos.tn.gov/businesses`
Entity filings, registered agents, formation dates, annual reports. The registered-agent
history is what documents the 2018 move from the City Attorney to GEDA. The newer portal,
which returns different results, is separate: `https://tncab.tnsos.gov/business-entity-search`
(all its searches: `https://tncab.tnsos.gov/portal/public-searches`). Check both.

**TN Acts and Resolutions** — `https://sos.tn.gov/publications/services/acts-and-resolutions`
Public chapters as enacted. For a bill's own text, `capitol.tn.gov` serves the PDF directly
by general assembly number and bill id, no search needed:

    https://capitol.tn.gov/Bills/111/Bill/SB0708.PDF     (111th GA, SB0708 -> PC 265)

**TN Professional license verification** — `https://search.cloud.commerce.tn.gov`
Every licensed profession in the state, including CPAs. This is where disciplinary history
on an auditor is checked.

**TN Comptroller** — `https://comptroller.tn.gov/search-results.html#q=pilot`
The site search is the way in; its navigation is not. The pages worth bookmarking directly:

- **Archived PILOT reports, 2014-2025** — the source of the 106-report corpus in
  `state_of_tennessee/tn_comptroller_pilot_reports/`:
  `/boards/state-board-of-equalization/sboe-services/property-tax-incentive-programs/pilot-reporting/filed-idb-h-ed-reports.html`
- **PILOT reporting requirements** —
  `/boards/state-board-of-equalization/sboe-services/property-tax-incentive-programs/pilot-reporting.html`
- **IDB debt reporting** —
  `/office-functions/lgf/debt/industrial-development-corporations-debt-reporting.html`
- **Assessment vs Taxation** — `/office-functions/pa/property-taxes/assessment-vs-taxation.html`
- **Value appeals (SBOE)** — `/boards/state-board-of-equalization/value-appeals.html`
- **Local Government Economic Development Dashboard** —
  `/office-functions/lgf/debt/local-government-economic-development-dashboard.html`
  The Comptroller's own aggregation of local economic development activity.
- **Advanced search** — `/advanced-search.html`, better than the plain site search.

Report PDFs sit under `/content/dam/cot/`, so once you have one path you can guess the rest:

    /content/dam/cot/sboe/documents/tax-incentive-programs/2022PILOTReport.pdf
    /content/dam/cot/sboe/documents/tax-incentive-programs/20150309IDBSummary2014.pdf
    /content/dam/cot/lgf/documents/debt/idbs/FY2024IDBReport.pdf
    /content/dam/cot/slf/documents/policies/sfb/SFBGuidelinesIDBDebtReporting.pdf

**TN Property Viewer (map)** — `https://tnmap.tn.gov/assessment/`
The map counterpart to TPAD, and it takes a parcel key straight in the fragment:

    https://tnmap.tn.gov/assessment/#/parcel/083111%20%20%20%2000100

**CIS / UT Center for Industrial Services capstones** — `https://www.cis.tennessee.edu/`
Where the three IDB capstone reports came from. All three are in the archive at
`sumner_county/gallatin_idb_data/`, but the originals live here:
- `sites/default/files/Leon%2C%20LilibethTCED%20Capstone%202024%20Fall%20FINAL_0.pdf`
- `sites/default/files/John%20Isbell%20FINAL%20Capstone%20Project%20Report.pdf`
- `sites/default/files/Rosemary%20Bates_Final_Capstone%20Paper%20March%202021.pdf`

**CTAS — County Technical Assistance Service** — `https://ctas.tennessee.edu/`
UT's legal reference for TN local government. Plain-language statute explanations with a
`CTAS-###` id per topic. Every topic has a clean printable version by node id, which is far
easier to save or quote than the styled page:

    https://www.ctas.tennessee.edu/node/619/printable/pdf     (IDCs: purpose and authority)
    https://www.ctas.tennessee.edu/node/619/printable/print Captures of the PILOT, TIF, TVA in-lieu, Sunshine Law, and IDC
board pages are in `state_of_tennessee/tn_annotated_code/`.

## Sumner County and Gallatin

**Sumner County property search** — `https://sumnertn.geopowered.com/propertysearch/`
County-side counterpart to TPAD. Different data, same parcels.

**Sumner County boards and committees** — `https://sumnercountytn.gov/government/boards-and-committees/`
**Sumner County municipalities** — `https://sumnercountytn.gov/information/municipalities/`

**Gallatin — site search** — `https://www.gallatintn.gov/Search?searchPhrase=`
The CivicEngage search supports boolean and pagination, both in the URL, which is the only
reliable way through it:

    https://www.gallatintn.gov/Search?searchPhrase=james%20AND%20fenton&pageNumber=2&perPage=50

**Gallatin — Agenda Center** — `https://www.gallatintn.gov/agendacenter/city-council-6/`
Council agendas and packets. The anchor is `#MMDDYYYY-ID`, and the file behind it is at a
different URL:

    page:  https://www.gallatintn.gov/agendacenter/city-council-6/?#06182019-278
    file:  https://www.gallatintn.gov/AgendaCenter/ViewFile/Agenda/_06182019-278

Planning Commission is board `Planning-Commission-Meeting-Open-in-Goog-5`, same pattern.

**TN Code Unannotated, free public access (Lexis)** — `https://advance.lexis.com/container/?pdmfid=1000516`
The statute text itself. Session-scoped URLs with `crid` parameters do not survive, so link
by section number in your notes and re-navigate. Sections this investigation leans on:
§ 7-53-305 (agreement terms), § 7-53-308 (nonprofit, net earnings, transfer of assets),
§ 67-5-502 (the "or instrumentality thereof" amendment).

**Gallatin IDB page** — `https://www.gallatintn.gov/509/Industrial-Development-Board`

**TN AI Advisory Council** — `https://www.tn.gov/finance/ai-council.html`

**Mapping** — `https://apps.nationalmap.gov/viewer/` (USGS National Map; `/3depdem/` for
elevation) and `https://www.tn.gov/twra/gis-maps.html`. For terrain, transmission corridors,
and anything where the land itself is the question.

**NextRequest** — e.g. `https://saltlakecountyut.nextrequest.com/requests`
The public-records-request platform many agencies run. Worth knowing the software when it
comes time to file: requests and responses are usually public on the portal, so other
people's requests to the same agency are readable.

## Federal

**ProPublica Nonprofit Explorer** — `https://projects.propublica.org/nonprofits/`
990 filings by EIN, back years, full PDFs. Per-EIN is the reliable path, and appending a
filing id plus `/full` opens the whole return rather than the summary:

    /nonprofits/organizations/384171308                             (Gallatin IDB)
    /nonprofits/organizations/384171308/202512309349301216/full     (one full filing)
    /nonprofits/organizations/202703372                             (Gibson County IDB)

**IRS Tax Exempt Organization Search** — `https://apps.irs.gov/app/eos/details/`
The authority on whether an organization is actually recognized. Filed 990s are served
directly, named by EIN and period:

    https://apps.irs.gov/pub/epostcard/cor/384171308_202106_990EO_2022080220261586.pdf

**IRS SOI bulk extracts** — `https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data`
Annual financial data for every exempt organization, for comparisons across many EINs at once.

## Newspaper and historical archives

**ProQuest Historical Newspapers — The Nashville Tennessean**
`https://www.proquest.com/hnpnashvilletennesseanshell/`
Requires a library account (`accountid=33208`). This is the source of the scanned Tennessean
pages in `web_articles/`. Pages pulled or opened so far: 1983-11-16 p18 (Stark), 1993-07-04
p40, 2006-10-30 p14, 2008-08-24 p14, 2008-11-06 p6, 2008-12-14 p26 (Assante). Only the two
1983 and 2008 pages are in the archive; the other four were opened and not saved.

**TN State Library and Archives** — `https://sos.tn.gov/tsla`
**TSLA online resources** — `https://sos.tn.gov/library-archives/services/online-resources`
**Tennessee Virtual Archive (TeVA)** — `https://teva.contentdm.oclc.org/`
Searchable by term directly, which beats browsing the collections:

    /digital/search/searchterm/Madison%20(Tenn.)/field/covera/mode/exact/conn/and

**TNGenWeb, Sumner County** — `https://www.tngenweb.org/sumner/`
Volunteer local-history archive. Useful for anything that predates digital records.

## Out of state

**Madison County, Alabama** — the Huntsville comparison, where Project Skillet went.
- Parcel viewer: `https://isv.kcsgis.com/al.madison_revenue/`
- Property details: `https://madisonproperty.countygovservices.com/Property/Property/Summary`

## Subjects' own sites

Evidence about the people who publish them, never ground truth.

**Pascal Jouvence** — `https://www.pascalforgallatin.com/`
Gallatin city council member; a private citizen through the Woolhawk window who spoke in
public comment repeatedly and was later elected. His May 2020 blog post read the Woolhawk
term as 20 years per building, matching R2005-24 and contradicting the Leon report's
"five-year agreement." Pages: `/blog`, `/thetruthroom`, `/thetruthroomtermlimits`.

**Meta Data Centers** — `https://datacenters.atmeta.com/2020/08/hello-gallatin/`
The company's own announcement of the Gallatin campus.

## News archives

**Nashville Business Journal** — the Beretta deal, February 2014:
`https://www.bizjournals.com/nashville/blog/2014/02/behind-the-beretta-deal-workforce.html`

**The Tennessean** — "Gallatin woos Beretta with tax breaks, free land," 2014-09-22:
`https://www.tennessean.com/story/news/local/gallatin/2014/09/22/gallatin-woos-beretta-tax-breaks-free-land/16063295/`

**Data Center Knowledge** — "Facebook Announces Tennessee Data Center":
`https://www.datacenterknowledge.com/hyperscalers/facebook-announces-tennessee-data-center`

**Tennessee Star** — "New Facebook Data Center Could Make Big Impact in Gallatin," 2020-10-03:
`https://tennesseestar.com/news/new-facebook-data-center-could-make-big-impact-in-gallatin-report-says/cbutler/2020/10/03/`

---

*Started 2026-08-19 from two OneTab dumps, replacing a `weblinks.md` that had one URL
in it. Add to this whenever a site takes more than one attempt to get back into — that is
the signal it belongs here.*
