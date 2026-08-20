# web/assets/

## Purpose
Images the site displays that are shared across pages, or not yet used by one. An image used
by a single page lives next to that page instead — Astro's colocation pattern — so this
directory is for the exceptions.

## Contents
- `banners/` — hero images, referenced from page frontmatter as `../assets/banners/name.jpg`.
- `img/` — images held for future use. Nothing here is referenced yet.

## Source Type
**Working Material.** Site assets, not evidence. A photograph that documents something is
evidence and belongs in the archive with the records it concerns.

## Handling Instructions
- Reference images relatively from content so Astro optimises them at build. An absolute
  path skips the pipeline and ships the raw file.
- When one page starts using an image here on its own, move it beside that page.
- `@/` citations cannot reach this directory; it is under `web/`, not the research archive.

## Notes
`img/` was created 2026-08-19 for two photographs of 600 Small Street that had been sitting
in the retired `visualizations/` directory.
