// Source data for Unipres USA Inc — canonical copy. Symlinked into www/sumner_pilot_tracker_v2/js/entities/unipres.js
const ENTITY_UNIPRES = {
 "id": "unipres",
 "prefix": "uni",
 "name": "Unipres USA Inc",
 "navLabel": "Unipres",
 "addr": "201 Kirby Drive, Portland TN",
 "defaultYear": "2017",
 "years": {
  "2015": {
   "type": "absent",
   "note": "Unipres USA Inc does not appear in the 2015 state PILOT report for Sumner County."
  },
  "2016": {
   "type": "absent",
   "note": "Unipres USA Inc does not appear in the 2016 state PILOT report for Sumner County."
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
     "Lessee": "UNIPRES USA",
     "Est. Value": "$81,451,449",
     "Rent": "$0",
     "PILOT/CI": "$0",
     "PILOT/CO": "$0",
     "Filed": "10/13/2017",
     "Lease Begin": "12/29/2014",
     "Lease End": "12/31/2017"
    },
    {
     "Lessee": "UNIPRES USA",
     "Est. Value": "$81,451,449",
     "Rent": "$0",
     "PILOT/CI": "$0",
     "PILOT/CO": "$0",
     "Filed": "10/13/2017",
     "Lease Begin": "12/29/2014",
     "Lease End": "12/31/2017"
    }
   ],
   "total": {
    "Lessee": "Total",
    "Est. Value": "$162,902,898",
    "Rent": "$0",
    "PILOT/CI": "$0",
    "PILOT/CO": "$0",
    "Filed": "",
    "Lease Begin": "",
    "Lease End": ""
   },
   "warn": null,
   "totalsLine": "<span style=\"color:var(--blue-text);\">Rent <b>$0</b></span><span style=\"color:var(--accent);\">PILOT \u2192 City <b>$0</b></span><span style=\"color:var(--accent);\">PILOT \u2192 County <b>$0</b></span><span style=\"color:var(--ink);\">Est. Value <b>$162,902,898</b></span>"
  },
  "2018": {
   "type": "absent",
   "note": "Unipres USA Inc does not appear in the 2018 state PILOT report for Sumner County."
  },
  "2019": {
   "type": "absent",
   "note": "Unipres USA Inc does not appear in the 2019 state PILOT report for Sumner County."
  },
  "2020": {
   "type": "absent",
   "note": "Unipres USA Inc does not appear in the 2020 state PILOT report for Sumner County."
  },
  "2021": {
   "type": "absent",
   "note": "Unipres USA Inc does not appear in the 2021 state PILOT report for Sumner County."
  },
  "2022": {
   "type": "absent",
   "note": "Unipres USA Inc does not appear in the 2022 state PILOT report for Sumner County."
  },
  "2023": {
   "type": "absent",
   "note": "Unipres USA Inc does not appear in the 2023 state PILOT report for Sumner County."
  },
  "2024": {
   "type": "absent",
   "note": "Unipres USA Inc does not appear in the 2024 state PILOT report for Sumner County."
  },
  "2025": {
   "type": "absent",
   "note": "Unipres USA Inc does not appear in the 2025 state PILOT report for Sumner County."
  }
 },
 "docs": {
  "findings": "<div class=\"doc-section\"><h3>Single-year filer</h3><p>Appears in the state PILOT registry for 2017 only &mdash; no data on file for any other year, 2015&ndash;2025. Part of the project-level \"single-year/two-year filer\" open question, alongside Archer, ATA Retail, and Beretta.</p></div><div class=\"doc-section\"><h3>Genuine $0s, and a duplicate-row anomaly</h3><p>All payment values for 2017 are confirmed genuine reported $0s, not \"NO INFO\"/non-reporting (different from Beretta's pattern). But the 2017 filing has two parcel rows that are entirely identical in every field &mdash; same lessee, same $81,451,449 assessed value, same $0 payments, same filed date, same lease dates. This looks like a duplicated row rather than two distinct parcels, which would mean this entity's real assessed value is $81.45M, not the $162.9M the raw total currently shows.</p></div>",
  "questions": "<ul class=\"doc-list\"><li>Resolve the duplicate-row anomaly against the original source PDF &mdash; this affects whether $81.45M or $162.9M is the correct assessed value for this entity.</li><li>No assessment PDF pull, no announcement search, no Promises Made/Kept yet.</li></ul>"
 }
};
