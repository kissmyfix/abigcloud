// Source data for Stevison Ham Company — canonical copy. Symlinked into www/sumner_pilot_tracker_v2/js/entities/stevisonham.js
const ENTITY_STEVISONHAM = {
 "id": "stevisonham",
 "prefix": "sthm",
 "name": "Stevison Ham Company",
 "navLabel": "Stevison Ham",
 "addr": "125 Stevison Ham Road, Portland TN",
 "defaultYear": "2017",
 "years": {
  "2015": {
   "type": "absent",
   "note": "Stevison Ham Company does not appear in the 2015 state PILOT report for Sumner County."
  },
  "2016": {
   "type": "absent",
   "note": "Stevison Ham Company does not appear in the 2016 state PILOT report for Sumner County."
  },
  "2017": {
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
     "Lessee": "STEVISON HAM COMPANY",
     "Est. Value": "$934,826",
     "Rent": "$87,640",
     "PILOT/CI": "$0",
     "PILOT/CO": "$0",
     "Filed": "10/02/2017",
     "Lease Begin": "12/30/2016",
     "Lease End": "01/01/2027"
    },
    {
     "Lessee": "STEVISON HAM COMPANY",
     "Est. Value": "$1,135,800",
     "Rent": "$577,500",
     "PILOT/CI": "$0",
     "PILOT/CO": "$0",
     "Filed": "10/02/2017",
     "Lease Begin": "04/03/2017",
     "Lease End": "04/03/2027"
    }
   ],
   "total": {
    "Lessee": "Total",
    "Est. Value": "$2,070,626",
    "Rent": "$665,140",
    "PILOT/CI": "$0",
    "PILOT/CO": "$0",
    "Filed": "",
    "Lease Begin": "",
    "Lease End": ""
   },
   "warn": null,
   "totalsLine": "<span style=\"color:var(--blue-text);\">Rent <b>$665,140</b></span><span style=\"color:var(--accent);\">PILOT \u2192 City <b>$0</b></span><span style=\"color:var(--accent);\">PILOT \u2192 County <b>$0</b></span><span style=\"color:var(--ink);\">Est. Value <b>$2,070,626</b></span>"
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
     "Lessee": "STEVISON HAM COMPANY",
     "Est. Value": "$5,440,000",
     "Rent": "$399,044",
     "PILOT/CI": "$0",
     "PILOT/CO": "$0",
     "Filed": "9/20/2018",
     "Lease Begin": "04/03/2017",
     "Lease End": "04/03/2027"
    }
   ],
   "total": {
    "Lessee": "Total",
    "Est. Value": "$5,440,000",
    "Rent": "$399,044",
    "PILOT/CI": "$0",
    "PILOT/CO": "$0",
    "Filed": "",
    "Lease Begin": "",
    "Lease End": ""
   },
   "warn": null,
   "totalsLine": "<span style=\"color:var(--blue-text);\">Rent <b>$399,044</b></span><span style=\"color:var(--accent);\">PILOT \u2192 City <b>$0</b></span><span style=\"color:var(--accent);\">PILOT \u2192 County <b>$0</b></span><span style=\"color:var(--ink);\">Est. Value <b>$5,440,000</b></span>"
  },
  "2019": {
   "type": "absent",
   "note": "Stevison Ham Company does not appear in the 2019 state PILOT report for Sumner County."
  },
  "2020": {
   "type": "absent",
   "note": "Stevison Ham Company does not appear in the 2020 state PILOT report for Sumner County."
  },
  "2021": {
   "type": "absent",
   "note": "Stevison Ham Company does not appear in the 2021 state PILOT report for Sumner County."
  },
  "2022": {
   "type": "absent",
   "note": "Stevison Ham Company does not appear in the 2022 state PILOT report for Sumner County."
  },
  "2023": {
   "type": "absent",
   "note": "Stevison Ham Company does not appear in the 2023 state PILOT report for Sumner County."
  },
  "2024": {
   "type": "absent",
   "note": "Stevison Ham Company does not appear in the 2024 state PILOT report for Sumner County."
  },
  "2025": {
   "type": "absent",
   "note": "Stevison Ham Company does not appear in the 2025 state PILOT report for Sumner County."
  }
 },
 "docs": {
  "findings": "<div class=\"doc-section\"><h3>Two-year filer, then absent</h3><p>Appears in the registry for 2017 ($665,140 rent) and 2018 ($399,044 rent) only &mdash; then absent 2019&ndash;2025, with no indication the underlying lease ended.</p></div><div class=\"doc-section\"><h3>2018 figures recovered from a corrected source file</h3><p>The 2018 data comes from <code>2018-pilot-sumner.pdf</code> (filed 9/20/2018) &mdash; recovered when Brandon caught and fixed file-naming inconsistencies in <code>state_of_tennessee/tn_comptroller_pilot_reports/</code> that had earlier caused a mislabeled 2017 file to be mistaken for 2018.</p></div>",
  "questions": "<ul class=\"doc-list\"><li>Why reporting stops after 2018 &mdash; same open question as Beretta/Archer/Unipres/ATA Retail (the project-level single/two-year filer pattern).</li><li>No assessment PDF pull, no announcement search, no Promises Made/Kept yet.</li></ul>"
 }
};
