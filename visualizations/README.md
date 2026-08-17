# visualizations/

## Purpose
Draft/prototype HTML documents used to work out chart and layout ideas before they move into the real site. The Sumner PILOT tracker itself no longer lives here — see `www/sumner_pilot_tracker_v2/`.

## Contents
`idb-990-comparisons.html`, plus source images and PDFs used in early drafts. Currently described as crude but functional.

Filenames here were renamed to the project convention (lowercase, dashes) on 2026-07-29:

| was | is |
|---|---|
| `idb_990_comparisons.html` | `idb-990-comparisons.html` |
| `shawshank_meme_template.html` | `shawshank-meme-template.html` |
| `shawshank_vs_gallatin.html` | `shawshank-vs-gallatin.html` |
| `COUNTY-BUDGET-2023-2024-draft-4-Jun-12-2023.pdf` | `2023-06-12-sumner-county-budget-fy2024-draft-4.pdf` |
| `static-assets-upload8711893708569538415.jpeg` | `shawshank-still-unlabeled.jpeg` |
| `shawshawnk-redemption-shoes-1024x509.jpg` | `shawshank-redemption-shoes-1024x509.jpg` |
| `top.png` | deleted — byte-identical to `andy-dufresne-and-red-reddington-in-the-shawshank-redemption.jpg` |
| `bot.png` | deleted — byte-identical to `warden-norton-holding-out-his-hand-in-the-shawshank-redemption.jpg` |

Two PDFs here are **source documents, not output** — they contradict the Source Type below and should be read that way: `2023-06-12-sumner-county-budget-fy2024-draft-4.pdf`, and `calendar-gallatin-civics.pdf` (moved here 2026-07-29 from the dissolved `files/claude_ignore/`; a Gallatin civics/meeting calendar, unread and unindexed as of that date).

## Source Type
**Output Artifact**

These are products of prior analysis, not source material. The data they display originates in other directories.

## Handling Instructions
- Do not treat as a source — go to the underlying data directory for facts
- Review before building new visualizations to avoid duplicating work or contradicting existing visuals
- Visual philosophy: visuals should create an instinctive "aha" without editorializing — accurately presented data does the argumentative work
- Always develop a visualization strategy with Brandon before executing; confirm approach before rendering
- Publication-ready versions will need design polish beyond what's here

## Notes
Existing visualizations represent prior analytical decisions about how to present the data. Understanding those decisions is useful context before building anything new.

## Design System (established on the Sumner PILOT tracker, June–July 2026; now applies to `www/sumner_pilot_tracker_v2/`)

These HTML pages are destined for abigcloud.com, so they're built to match its actual live CSS, not a generic palette guessed from scratch. Pull the current values from the live site if this ever drifts — don't assume these are still current forever.

**Fonts:** DM Sans (body/UI), DM Mono (numbers/data — ledger-style monospace for anything dollar-denominated), DM Serif Display (headlines/corp names only — used with restraint, one role).

**Color tokens** — defined as CSS custom properties in `:root`, with a matching `@media (prefers-color-scheme: dark)` override block copied verbatim from the live site. Never hardcode hex for anything that's page chrome (backgrounds, borders, text, warning/callout colors) — always reference the token so dark mode "just works" for free, no JS toggle needed:
- `--bg`, `--bg2`, `--bg3` — cream/paper tones, darkest to lightest use gets progressively more saturated. **No pure white or pure black anywhere** — the live site never uses either; every "card" background is one of these tonal creams (or their dark-mode charcoal equivalents).
- `--ink`, `--ink2`, `--ink3` — text, dark to muted.
- `--accent` (red-orange), `--gold`, `--teal` — brand accents.
- `--red-bg`/`--red-text`, `--gold-bg`/`--gold-text`, `--green-bg`/`--green-text`, `--blue-bg`/`--blue-text` — semantic callout pairs (e.g. warning boxes, status tags). Match the *meaning* to the right pair — gold/warning for "uncertain," red/accent for "confirmed problem," not just whichever looks good.

**Data-viz colors (pie wedges, bar fills, chart-specific palettes) are the one exception** — those stay fixed across light/dark mode intentionally, same as abigcloud.com keeps its status-tag colors constant. Don't tokenize those; they're deliberately decoupled from page theme so a color always means the same category regardless of mode.

**Layout patterns that came out of this work:**
- Donut charts (not solid pies) with the category total in the center hole — a category with zero data still gets a full-size donut with a striped fill (color-mixed between a semantic bg token and its accent), never an invisible sliver or missing chart. Distinguish *confirmed zero* (e.g. "No Data Reported") from *withheld/unreported* (e.g. "NO INFO") with genuinely different colors — they're different facts, not the same "nothing here."
- When a page has both a variable-height content area (year tabs/panels) and a fixed-content sidebar (charts), put them in a flex row with the main column and sidebar as siblings — never stack the chart below content that changes height on interaction. Stacking causes visible "jumping" every time the user clicks a tab.
- Flex rows with mixed content (e.g. a headline next to a tab strip) need `flex-wrap: nowrap` plus `min-width: 0; overflow-x: auto` on whichever child might overflow — otherwise it silently wraps to its own line instead of overflowing gracefully, which looks like a layout bug.

**Working method:** build in a scratch/comparison file first (e.g. `chart-variants-draft.html` — a tabbed file holding multiple design variants side by side over the same real data) before touching the live page. Screenshot every variant with headless Firefox to actually see it before describing it back — don't describe a design without having rendered it. `chart-variants-draft.html` in this directory is disposable once a design lands in the real page; safe to delete or leave as reference.

**Accuracy note specific to this dataset:** PILOT filings distinguish a *reported $0* from a row marked "NO INFO" (withheld or unreported — the source doesn't say which). Don't collapse those into one "no data" state, in copy or in color.

## Where the tracker actually lives now (moved July 2026)

The Sumner PILOT tracker started here as a single monolithic file (`sumner_pilot_tracker.html`), then got rebuilt as a data-driven version (`sumner_pilot_tracker_v2.html` + `tracker.css`/`tracker-data.js`/`tracker-render.js`) for the reasons described above (the design-system notes in this file still apply). Both the original and the interim v2 files that lived in this directory have been deleted — the original because it was fully superseded and hand-editing 1,200 divs was never worth returning to, the interim copies because they're now duplicates of the real thing.

The live, actively-maintained version is at **`www/sumner_pilot_tracker_v2/`** — `index.html` + `css/tracker.css` + `js/county-data.js` + one `js/entities/` file per entity + `js/tracker-render.js`. See that directory's own README for specifics. This directory (`visualizations/`) is now just for draft/prototype work that hasn't graduated to the real site yet.
