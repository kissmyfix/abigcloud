# www/idb_comparisons/css/

## Purpose
Styling for the IDB Overview — one file, no build step.

## Contents
`css.css` — design tokens (colors, fonts) ported from abigcloud.com's live CSS, plus all layout/component rules for the overview.

## Source Type

## Handling Instructions
- Color tokens should match abigcloud.com's actual live values — re-pull from the live site if this ever drifts, don't guess
- Default to fixed heights/widths for anything interactive (tabs, years, doc categories) rather than content-derived flex-fill sizing — see the parent README for why
- When adding a scoped override for one feature, double check it overrides every property it needs to, not just the ones that seem relevant — an unset property falls through from a less-specific rule

## Notes
None.
