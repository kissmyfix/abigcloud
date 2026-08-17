# www/idb_comparisons/

## Purpose
The live, actively-maintained Industrial Board of Gallatin data visualization — a data-driven, per-year visualization of all IRS form 990 filings made by the Gallatin IDB from 2020 through 2024, plus points of attention.

## Contents
- `index.html` — thin HTML shell; loads the CSS/JS below and mounts the rendered page
- `css/comps.css` — all styling (design tokens ported from abigcloud.com, layout, components)
- `js/overview.js` — A high level view of the conclusions drawn from the data as a whole.
- `js/idb-render.js` — render logic that builds the entire page (nav, tabs, tables, sidebar pie charts) from the files above; nothing entity-specific lives here
- `img/` — currently empty, reserved for future visual assets

## Source Type
**Output Artifact** — this is the investigation's output, not a source. Every figure it displays traces back to `usa_federal/irs_990_data/`

## Handling Instructions
- Theme to be derived from `www/abigcloud.com/`'s styling and design choices. Utilize the various visualizations as wll.
- Repurpose the year-bloc found within `www/sumner_pilot_tracker_v2`'s page customized for our needs here. cycling throut the year tabs should in turn display an easy to visualize equivalent to that years corresponding 990. This visual does not and should NOT be exhaustive. Trim the fat down to the data important to our investigation and that which shows descripency.
- Prefer fixed dimensions over content-derived/flex-fill sizing for anything the user can click between (tabs, years, doc categories) — this page has already had a multi-session bug from doing it the "smart"/flexible way
- Watch for CSS specificity when layering a new feature-specific rule on a shared base class (e.g. `.panel`) — a more specific selector only overrides the properties it explicitly sets, not the whole rule

## Notes
- Explore data visualization ideas. We're looking for the type of presentation that is self explanatory and easily recognizable.
- Possible feature idea: A comparison builder. Something that allows for selecting two or three seperate years and provide a direct comparison for the user
- Possible feature idea: Include markup tools a user can use to highlight/cross-out/otherwise create notations directly on the page