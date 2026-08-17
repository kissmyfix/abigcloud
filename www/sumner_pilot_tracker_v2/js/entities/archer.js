// Source data for Archer Datacenters — canonical copy. Symlinked into www/sumner_pilot_tracker_v2/js/entities/archer.js
const ENTITY_ARCHER = {
 "id": "archer",
 "prefix": "archer",
 "name": "Archer Datacenters",
 "navLabel": "Archer",
 "addr": "1398 Gateway Drive, Gallatin TN",
 "defaultYear": "2021",
 "years": {
  "2015": {
   "type": "absent",
   "note": "Archer Datacenters does not appear in the 2015 state PILOT report for Sumner County."
  },
  "2016": {
   "type": "absent",
   "note": "Archer Datacenters does not appear in the 2016 state PILOT report for Sumner County."
  },
  "2017": {
   "type": "absent",
   "note": "Archer Datacenters does not appear in the 2017 state PILOT report for Sumner County."
  },
  "2018": {
   "type": "absent",
   "note": "Archer Datacenters does not appear in the 2018 state PILOT report for Sumner County."
  },
  "2019": {
   "type": "absent",
   "note": "Archer Datacenters does not appear in the 2019 state PILOT report for Sumner County."
  },
  "2020": {
   "type": "absent",
   "note": "Archer Datacenters does not appear in the 2020 state PILOT report for Sumner County."
  },
  "2021": {
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
     "Lessee": "ARCHER DATACENTERS",
     "Est. Value": "$10,059,700",
     "Rent": "$0",
     "PILOT/CI": "$0",
     "PILOT/CO": "$53,320",
     "Filed": "9/20/2021",
     "Lease Begin": "02/12/2020",
     "Lease End": "12/31/2028"
    }
   ],
   "total": {
    "Lessee": "Total",
    "Est. Value": "$10,059,700",
    "Rent": "$0",
    "PILOT/CI": "$0",
    "PILOT/CO": "$53,320",
    "Filed": "",
    "Lease Begin": "",
    "Lease End": ""
   },
   "warn": null,
   "totalsLine": "<span style=\"color:var(--blue-text);\">Rent <b>$0</b></span><span style=\"color:var(--accent);\">PILOT \u2192 City <b>$0</b></span><span style=\"color:var(--accent);\">PILOT \u2192 County <b>$53,320</b></span><span style=\"color:var(--ink);\">Est. Value <b>$10,059,700</b></span>"
  },
  "2022": {
   "type": "absent",
   "note": "Archer Datacenters does not appear in the 2022 state PILOT report for Sumner County."
  },
  "2023": {
   "type": "absent",
   "note": "Archer Datacenters does not appear in the 2023 state PILOT report for Sumner County."
  },
  "2024": {
   "type": "absent",
   "note": "Archer Datacenters does not appear in the 2024 state PILOT report for Sumner County."
  },
  "2025": {
   "type": "absent",
   "note": "Archer Datacenters does not appear in the 2025 state PILOT report for Sumner County."
  }
 },
 "docs": {
  "findings": "<div class=\"doc-section\"><h3>Files exactly once, the same year Woolhawk debuts</h3><p>Appears in the PILOT registry for 2021 only &mdash; the exact same year Woolhawk first appears. No data for any other year, 2015&ndash;2025.</p></div><div class=\"doc-section\"><h3>Address one parcel number from Woolhawk</h3><p>1398 Gateway Drive, one parcel off Woolhawk's 1432 Gateway Drive &mdash; same immediate area, same IDB, same debut year. Flagged in CLAUDE.md's Control Groups section as a deliberate comparison point.</p></div><div class=\"doc-section\"><h3>The only nonzero category is county PILOT</h3><p>$0 rent, $0 city, $53,320 county &mdash; the opposite pattern from most other tracked entities, which report $0 to county and something to rent/city instead.</p></div>",
  "questions": "<ul class=\"doc-list\"><li>Why Archer files exactly once, in Woolhawk's debut year, then vanishes &mdash; a related/renamed entity, a shell that stopped being a going concern, or something else?</li><li>No assessment PDF pull, no announcement search, no Promises Made/Kept yet.</li></ul>"
 }
};
