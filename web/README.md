# web/

The Astro site behind [abigcloud.com](https://abigcloud.com). Deployed to GitHub Pages
by `.github/workflows/deploy.yml` on every push to `main`.

Article content lives in `content/`, and the content
collections in `src/content.config.ts` read it from there, so the same markdown
renders on GitHub and on the site.

## Commands

All commands run from this directory.

| Command | Action |
| :--- | :--- |
| `npm install` | Install dependencies |
| `npm run dev` | Local dev server at `localhost:4321` |
| `npm run build` | Build the production site to `./dist/` |
| `npm run preview` | Preview the build locally before deploying |

## Article format

Articles are markdown with frontmatter:

```yaml
---
title: 'Article Title'
description: 'One sentence, used for search results and link previews.'
pubDate: 2026-07-30
updatedDate: 2026-08-15   # optional
draft: true               # optional, keeps it out of the built site
heroImage: './assets/name.png'   # optional
---
```

Images use markdown syntax against the article's own `assets/` folder,
never raw HTML, so the path resolves identically on GitHub and on the site:

```markdown
![Alt text](./assets/name.png)
```

Sizing and alignment belong in `src/styles/global.css`, not in the markdown.
