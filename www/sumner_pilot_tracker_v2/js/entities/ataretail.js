// Source data for ATA Retail Services LLC — canonical copy. Symlinked into www/sumner_pilot_tracker_v2/js/entities/ataretail.js
const ENTITY_ATARETAIL = {
 "id": "ataretail",
 "prefix": "ata",
 "name": "ATA Retail Services LLC",
 "navLabel": "ATA Retail",
 "addr": "214 Kirby Drive, Portland TN",
 "defaultYear": "2018",
 "years": {
  "2015": {
   "type": "absent",
   "note": "ATA Retail Services LLC does not appear in the 2015 state PILOT report for Sumner County."
  },
  "2016": {
   "type": "absent",
   "note": "ATA Retail Services LLC does not appear in the 2016 state PILOT report for Sumner County."
  },
  "2017": {
   "type": "absent",
   "note": "ATA Retail Services LLC does not appear in the 2017 state PILOT report for Sumner County."
  },
  "2018": {
   "type": "data",
   "headers": [
    "Lessee",
    "Est. Value",
    "Rent",
    "PILOT/CI",
    "PILOT/CO",
    "Filed",
    "Lease Begin",
    "Lease End"
   ],
   "rows": [
    {
     "Lessee": "ATA RETAIL SERVICES LLC",
     "Est. Value": "$411,760",
     "Rent": "$69,361",
     "PILOT/CI": "$348",
     "PILOT/CO": "$618",
     "Filed": "10/1/2018",
     "Lease Begin": "09/28/2012",
     "Lease End": "01/01/2026"
    }
   ],
   "total": {
    "Lessee": "Total",
    "Est. Value": "$411,760",
    "Rent": "$69,361",
    "PILOT/CI": "$348",
    "PILOT/CO": "$618",
    "Filed": "",
    "Lease Begin": "",
    "Lease End": ""
   },
   "warn": null,
   "totalsLine": "<span style=\"color:var(--blue-text);\">Rent <b>$69,361</b></span><span style=\"color:var(--gold);\">PILOT \u2192 City <b>$348</b></span><span style=\"color:var(--accent);\">PILOT \u2192 County <b>$618</b></span><span style=\"color:var(--ink);\">Est. Value <b>$411,760</b></span>"
  },
  "2019": {
   "type": "absent",
   "note": "ATA Retail Services LLC does not appear in the 2019 state PILOT report for Sumner County."
  },
  "2020": {
   "type": "absent",
   "note": "ATA Retail Services LLC does not appear in the 2020 state PILOT report for Sumner County."
  },
  "2021": {
   "type": "absent",
   "note": "ATA Retail Services LLC does not appear in the 2021 state PILOT report for Sumner County."
  },
  "2022": {
   "type": "absent",
   "note": "ATA Retail Services LLC does not appear in the 2022 state PILOT report for Sumner County."
  },
  "2023": {
   "type": "absent",
   "note": "ATA Retail Services LLC does not appear in the 2023 state PILOT report for Sumner County."
  },
  "2024": {
   "type": "absent",
   "note": "ATA Retail Services LLC does not appear in the 2024 state PILOT report for Sumner County."
  },
  "2025": {
   "type": "absent",
   "note": "ATA Retail Services LLC does not appear in the 2025 state PILOT report for Sumner County."
  }
 },
 "docs": {
  "findings": "<div class=\"doc-section\"><h3>Discovered via a data correction, not the original target list</h3><p>This entity surfaced only after Brandon fixed file-naming inconsistencies in <code>state_of_tennessee/tn_comptroller_pilot_reports/</code> and the real <code>2018-pilot-sumner.pdf</code> (filed 10/1/2018) was properly identified &mdash; it was not part of the original entity list, found while parsing the corrected 2018 filing.</p></div><div class=\"doc-section\"><h3>One year of disclosure against a 14-year lease</h3><p>Appears in the registry for 2018 only, despite a lease running 09/28/2012 to 01/01/2026 &mdash; one of the longer lease terms in the dataset relative to how briefly it has actually been reported on.</p></div>",
  "questions": "<ul class=\"doc-list\"><li>Why a 14-year lease produced exactly one year of state disclosure &mdash; same open question as Archer/Unipres/Stevison Ham/Beretta.</li><li>No assessment PDF pull, no announcement search, no Promises Made/Kept yet.</li></ul>"
 }
};
