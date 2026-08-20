# WORKFLOW.md — how writing gets from the editor's screen to abigcloud.com

Written 2026-08-17. This pipeline is relied on without anyone needing to learn Astro, and
that is a reasonable division of labour — but only if it is written down. This file is
that. It explains the machinery at the level needed to use it, fix it, and explain it.

---

## The one-paragraph version

Everything is a markdown file, edited in a browser editor. A build step
turns markdown into a folder of plain HTML files. Those files get pushed to GitHub, and
GitHub serves them as the website. There is no server running the site, no database, and
nothing to keep alive.

---

## Editing: mdlive

    files/venv/bin/python files/bin/mdlive.py web/content/investigations/quid_pro_no/index.md 8080

Opening `http://localhost:8080/` with no `?f=` lists every page under `web/content/` and
waits for one to be picked; the file named on the command line is only the default for a
`?f=` deep link. The picker in the toolbar switches files, and its "all files" entry
returns to the list.

Then open **http://localhost:8080**. Source left, rendered preview right, saves as you type.

- **File picker** in the toolbar lists every `.md` and `.txt` in the project. The URL
  carries `?f=<path>`, so two files can be open in two tabs.
- **`Ctrl+/`** inserts `<!-- @c  -->` — a note to Claude, invisible in the preview and
  stripped at publish time.
- **"copy line ref"** copies selected lines with numbers, to paste into chat.
- Claude's edits to the same file appear within half a second. If the buffer has unsaved
  changes it shows "file changed on disk" rather than overwriting them.

Stop it by PID, in its own command, and never in the same line that restarts it:

    pgrep -f 'bin/mdlive[.]py'      # find it
    kill <pid>                      # then kill it

**`pkill -f mdlive` kills the shell you typed it in.** `pkill -f` matches against whole
command lines, and the shell running the pkill has "mdlive" in its own command line, so it
matches itself. A bracket in the pattern (`'bin/mdlive[.]py'`) is the usual dodge and is
**not enough here** — if the same command line also *starts* mdlive, as a kill-then-restart
one-liner does, the literal path is present and the shell matches anyway. Both failures
happened on 2026-08-20, the second one after the bracket had been written down as the fix.

Two separate commands is the only version that always works.

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
| The article | `web/content/investigations/quid_pro_no/index.md` (Part 1) and `part-2.md`, `part-3.md`, `part-4.md` beside it |
| About, FAQ, TVA, a topic page | `web/content/<path>.md` |
| Homepage | `web/index.md` |

## Writing a page

**The folder is the URL.** There is no routing file to edit and no list of pages to
register. Put a markdown file under `web/content/` and its path becomes its address.

    web/content/tennessee/fisk.md            ->  /tennessee/fisk/
    web/content/investigations/x/index.md    ->  /investigations/x/
    web/content/investigations/x/part-2.md   ->  /investigations/x/part-2/

`index.md` inside a folder is that folder's own page, which is why Part 1 of an
investigation is `index.md` — it keeps the URL a reader may already have bookmarked.

**Frontmatter** is the block between `---` lines at the top. `title` and `description` are
required; every other field is optional and has a sane default. The schema that enforces
this is `web/src/content.config.ts`, and a typo in a field name fails the build rather than
shipping quietly.

| Field | What it does |
|---|---|
| `title` | The `<title>` tag and what search results show. Not printed on the page — the page's own `#` heading does that |
| `description` | The sentence under the title in search results and link previews |
| `pubDate` / `updatedDate` | Printed under the title. Investigations are dated; standing reference pages are not |
| `draft: true` | The page is **not built for the live site at all** — no URL, nothing in the sitemap. It still appears in local preview, flagged with a pill |
| `toc: true` | Adds the floating Contents drawer and the reading-progress bar. The drawer hides itself below three headings, so setting it on a short page does nothing |
| `heroImage` / `heroImageNarrow` | Replace the default banner. Narrow is the phone crop |
| `series` / `part` / `partTitle` | Place the page in a multi-part piece. See below |

**One `#` heading per page.** It is the page's real headline. Everything below it uses `##`
and `###`, which is also what the Contents drawer is built from.

### Adding a part to a multi-part piece

Create the file next to the others and set three fields:

```yaml
series: 'quid_pro_no'     # the same slug on every part
part: 5                   # its number
partTitle: 'Short Name'   # what the navigation calls it
```

That is the whole operation. The "Part 5 of 5" label, the previous and next links, and the
list of parts at the foot of **every** page in the series are all derived at build time by
`web/src/components/SeriesNav.astro`, which reads the collection rather than a list anyone
maintains. No other file is edited, so no two pages can disagree about what the series
contains.

The reason it is built this way: hand-written "next part" links are four separate facts that
rot independently, which is the same failure as a README describing files that are not there.

A draft pipeline that published from a `monologues/` directory was removed 2026-08-17: one
directory cannot be both the source you edit and the output that overwrites you. That
directory was removed from the project entirely on 2026-08-19.

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


## Tooling on this machine

*Moved here 2026-08-19 from `memory/site-work-conventions.md`, which put standing
conventions in the findings directory.*

**Spreadsheets: `pd.read_excel(path)` reads `.ods` directly.** `odfpy` was installed
2026-08-18 into `files/venv`, so the Comptroller's `.ods` workbooks open the same way
`.xlsx` does. Before that they had to be unzipped and parsed as raw XML by hand; do not
write that code again. `libreoffice --headless --convert-to csv` is the fallback if a file
is malformed.

**Image tooling available:** ImageMagick 7 (`magick`, `identify`, `convert`), `exiftool`,
`exifprobe`, `feh`, Python Pillow. **Not** installed: `cwebp`, `jpegoptim`, `chafa`.

**Headless screenshots** of a running preview:

    MOZ_HEADLESS=1 firefox --no-remote --new-instance --profile <dir> \
      --window-size=W,H --screenshot <out.png> <url>

A fresh profile directory is required or it hangs.

**`web/tmp/`** was the shared drop point for source material — originals copied there rather
than sending Claude to hunt for them. It is gitignored and no longer exists as of
2026-08-19; recreate it if that workflow resumes.

**"ELI5" is a global workflow, not a project one.** It lives in `~/.claude/CLAUDE.md` with
pages under `~/.local/share/eli5/`. Never write eli5 pages into this repo.
