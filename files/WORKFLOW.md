# WORKFLOW.md — how writing gets from Brandon's screen to abigcloud.com

Written 2026-08-17. Brandon relies on this pipeline without wanting to learn Astro, and
that is a reasonable division of labour — but only if it is written down. This file is
that. It explains the machinery at the level needed to use it, fix it, and explain it.

---

## The one-paragraph version

Everything is a markdown file. Brandon edits markdown in a browser editor. A build step
turns markdown into a folder of plain HTML files. Those files get pushed to GitHub, and
GitHub serves them as the website. There is no server running the site, no database, and
nothing to keep alive.

---

## Editing: mdlive

    files/venv/bin/python files/bin/mdlive.py web/content/investigations/quid_pro_no/index.md 8080

Then open **http://localhost:8080**. Source left, rendered preview right, saves as he types.

- **File picker** in the toolbar lists every `.md` and `.txt` in the project. The URL
  carries `?f=<path>`, so two files can be open in two tabs.
- **`Ctrl+/`** inserts `<!-- @c  -->` — a note to Claude, invisible in the preview and
  stripped at publish time.
- **"copy line ref"** copies selected lines with numbers, to paste into chat.
- Claude's edits to the same file appear within half a second. If Brandon has unsaved
  changes it shows "file changed on disk" rather than overwriting him.

Stop it with `pkill -f mdlive`.

## Live preview of the real site

    cd web && npm run watch

Runs two things at once: `watch-content.mjs`, which re-runs the citation build when anything under `web/content/` changes, and
Astro's dev server on **http://localhost:4321**. Edit in mdlive on :8080, watch the actual
site update on :4321.

Stop it with `cd web && npx astro dev stop` — `pkill -f "astro dev"` does not work, for the reason under "Process gotchas" below.

---

## What Astro actually does

Astro is a **static site generator**. It reads content files and writes a folder of plain
HTML. That is the whole idea. Three rules cover everything here:

**1. Folder structure is the URL.**

    web/content/tennessee/fisk.md        ->  abigcloud.com/tennessee/fisk/
    web/content/about/index.md           ->  abigcloud.com/about/
    web/index.md                         ->  abigcloud.com/

Move a file, the URL moves. There is no routing table to edit.

**2. Every page needs frontmatter** — the block between `---` lines at the top:

    ---
    title: 'TVA'
    description: 'One sentence, used for search results and link previews.'
    ---

`title` and `description` are required; the build fails by name if either is missing.
Optional: `pubDate`, `draft: true` to keep a page out of the public build, `heroImage`.

**3. `npm run build` writes `web/dist/`** — a folder of finished HTML, CSS and images.
That folder *is* the website. Nothing else is needed to serve it.

Images referenced from markdown get optimised automatically (resized, converted to WebP).
Files placed in `web/public/` are copied through untouched — that is where cited source
documents go, because a PDF must be served byte-for-byte.

---

## Publishing

    files/bin/ship.sh "what changed"

That is the whole cycle: publish, commit, push, wait for the GitHub Action, then confirm
the live pages serve 200. It exits non-zero and names the stage that failed. Add
`-v "some phrase"` to also assert that a specific string reached the live article, or
`--dry-run` to build and commit without pushing.

Underneath it is still the two commands, if you want them by hand:

    cd web && npm run publish && git push

`npm run publish` is `node scripts/build-citations.mjs && astro build`.

### `scripts/build-citations.mjs`

Every page is edited directly under `content/`. Nothing is generated from a draft, so the
script has exactly one job: make citations work.

1. **Resolves `@/` citations** on every page under `content/` and on the homepage.
   `@/web_articles/foo.txt` means "from the research archive root". The document is copied
   into `web/public/sources/` and the link rewritten to `/sources/web_articles/foo.txt`.
2. **Handles images by kind.** A screenshot of a filing is evidence and is copied
   byte-for-byte. A decorative image goes through Astro's optimiser instead — the
   difference between an 841KB PNG and a 57KB WebP at the top of an article.
3. **Strips `@c` notes** so unresolved author notes cannot ship.
4. **Renders a page per cited text document.** A citation used to drop the reader onto a
   raw `.txt`. Now `@/podcasts/transcripts/fenton-on-podcast-full.txt` resolves to
   `/sources/fenton-on-podcast-full/` — a real page in the site's layout, with the
   provenance header as a card, a back-link, and a download link to the untouched file.
   `.md` sources render as formatted markdown; `.txt` sources keep their body verbatim in
   `<pre>`, because they are not markdown and formatting them would mangle them; `.pdf`
   sources get no page and link straight to the file. The generated pages live in
   `web/content/sources/` — **generated output, never hand-edited, never cited.** Links
   still pointing at a raw file are migrated on the next publish.
5. **Rebuilds `/sources/`** by scanning what the site actually links, not what this run
   rewrote. The `@/` rewrite is one-way, so a page converted on an earlier run has no `@/`
   left in it. The generated index is excluded from its own scan, or entries would become
   immortal.
6. **Exits non-zero if a cited document is missing**, so a broken citation cannot ship
   silently.

### Then `git push`

`.github/workflows/deploy.yml` runs on every push to `main`: checks out only `web`
(sparse checkout, so the archive is not downloaded), runs `npm ci` and `npm run build`,
and publishes `dist/` to GitHub Pages. The custom domain comes from `web/public/CNAME`.
Takes about a minute.

### Where each page lives

| Page | Edit this |
|---|---|
| The article | `web/content/investigations/quid_pro_no/index.md` |
| About, FAQ, TVA, a topic page | `web/content/<path>.md` |
| Homepage | `web/index.md` |

`monologues/` is Brandon's pen — personal writing, old drafts, voice reference. **Nothing
reads from it.** A draft pipeline that published from there was removed 2026-08-17: one
directory cannot be both the source you edit and the output that overwrites you.

## When something breaks

| Symptom | Cause |
|---|---|
| Publish exits non-zero, names a file | A citation points at a document that is not there. Fix the path or add the document. |
| A page vanished from the site | `draft: true` in its frontmatter, or the build failed. |
| Build fails naming a page | Missing `title` or `description` in frontmatter. |
| Edits do not reach the site | Published but not pushed, or the Action failed. Check the repo's Actions tab. |
| Build fails on a missing `description`/`title` that is plainly there | A `<!-- @c -->` note is sitting on a frontmatter line, so the key is part of the comment. Annotations go in the body, never in the YAML. |
| A citation 404s | The document was never copied. Confirm the `@/` path matches a real file. |
| PDF will not preview on GitHub | GitHub's viewer, not the file. Use Download or Raw. |

Local build output lives in `web/dist/` and is gitignored — it is rebuilt every time and
is never the source of anything.

---

## Process gotchas that have already cost time

**Stopping the dev server.** `pkill -f "astro dev"` does not work — the running process is
`node .../astro/bin/astro.mjs`, so the pattern never matches. Astro also refuses to start a
second server and reports `HTTP 500` while the stale one holds the port, which looks like a
build error and is not. Use its own command:

    cd web && npx astro dev stop

**The dev server does not survive a directory move.** It resolves `node_modules` from where
it was started. Anything that relocates `web/` leaves it serving 500s from a path that no
longer exists. Restart it after any restructuring, and check `:4321` returns 200 before
assuming the site is broken.

**Never wait on a job with `pgrep -f <name>`.** `pgrep -f` matches full command lines
including the waiting shell's own, so a loop like

    until ! pgrep -f pdf-extract; do sleep 10; done

finds itself, concludes the job is still running, and spins forever. Two of these were left
orphaned on 2026-08-17. Capture the PID at launch and wait on that instead.

**Backgrounding from a shell that also greps for the thing it started** has the same
failure. `pkill -f markserv` issued from a command line containing the word `markserv`
kills the shell that issued it (exit 144).

**Ports in use:** `:8080` mdlive, `:4321` Astro dev. Check with
`ss -lntp | grep -E '8080|4321'`.
