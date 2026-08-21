#!/usr/bin/env node
/**
 * build-citations.mjs — resolve archive citations and rebuild the source index.
 *
 * Every page on this site is edited directly under content/. There are no drafts and
 * no generated pages; what you edit is what ships. This script does one job: it turns
 * citations into working links.
 *
 * Write a citation as @/ followed by a path in the research archive:
 *
 *     [the 2013 Times Free Press piece](@/web_articles/2013-04-07-timesfreepress-....txt)
 *
 * On publish, the document is copied into public/sources/, the link is rewritten to
 * /sources/..., and the page is listed at /sources/. The rewrite is one-way and edits
 * the page in place, which is why the index is rebuilt by scanning what the site
 * actually links rather than what this run happened to change.
 *
 * Evidence images are copied byte-for-byte, because a screenshot of a filing has to be
 * the actual file. Decorative images live beside the page that uses them, under web/, and
 * never pass through here.
 *
 * Exits non-zero if a citation points at a document that does not exist.
 *
 * Usage: node scripts/build-citations.mjs      (npm run publish runs it, then builds)
 */
import { readFileSync, writeFileSync, mkdirSync, copyFileSync, existsSync, readdirSync } from 'node:fs';
import { dirname, join, resolve, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const WEB = resolve(HERE, '..');
const RESEARCH = resolve(WEB, '..');            // ~/Documents/data_center_research
const PUBLIC_SOURCES = join(WEB, 'public', 'sources');

/** Explainers that already exist as pages on this site. */
const EXPLAINER_PAGES = new Set(['what-is-an-idb', 'what-is-a-pilot', 'the-title-transfer-mechanism', '501c4-vs-instrumentality']);

// A citation is written @/ followed by a path in the research archive:
//   @/web_articles/foo.txt
// ../ is still accepted so older pages keep working, but @/ is the form to use --
// ../ means a real relative path inside content/ and is ambiguous there.
const LINK_RE = /\[([^\]]*)\]\(((?:\.\.|@)\/[^)\s]+)\)/g;
const IMG_RE = /!\[([^\]]*)\]\(((?:\.\.|@)\/[^)\s]+)\)/g;
const stripPrefix = (target) => target.replace(/^(?:\.\.|@)\//, '');

/* A cited text document gets a real page on the site — /sources/fenton-on-podcast-full/ —
   rendered in the site's own layout instead of dumping the reader onto a raw .txt in the
   browser's default font. The untouched file is still copied into public/sources/ and
   linked from that page, because "exactly as it was filed" is the promise the sources
   page makes and a styled page is not the file. PDFs cannot be inlined and keep pointing
   at the file itself. */
const isText = (relPath) => /\.(txt|md)$/i.test(relPath);
const slugOf = (relPath) =>
	relPath.split('/').pop().replace(/\.(txt|md)$/i, '')
		.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

/* slug -> archive path, so a /sources/<slug>/ link can be resolved back to the document
   it renders. Filled as documents are published and reused by the index builder. */
const bySlug = new Map();

function sourceUrl(relPath) {
	if (!isText(relPath)) return '/sources/' + relPath.split('/').map(encodeURIComponent).join('/');
	let slug = slugOf(relPath);
	// two archives can hold the same filename; keep the first and qualify the second
	if (bySlug.has(slug) && bySlug.get(slug) !== relPath) {
		slug = slugOf(relPath.split('/').slice(-2).join('-'));
	}
	bySlug.set(slug, relPath);
	return '/sources/' + slug + '/';
}

/* Write only when the bytes actually change. The content watcher watches the same
   directory this script writes into, so an unconditional write is a feedback loop:
   generate -> watcher fires -> generate. */
function writeIfChanged(path, text) {
	if (existsSync(path) && readFileSync(path, 'utf8') === text) return false;
	writeFileSync(path, text, 'utf8');
	return true;
}

let copied = 0;
let currentDest = '';
const missing = [];
const rewrites = [];

function publishSource(relPath) {
	const abs = resolve(RESEARCH, relPath);
	if (!existsSync(abs)) {
		missing.push(relPath);
		return null;
	}
	const out = join(PUBLIC_SOURCES, relPath);
	mkdirSync(dirname(out), { recursive: true });
	copyFileSync(abs, out);
	copied++;
	return sourceUrl(relPath);
}

const SITE = 'https://abigcloud.com';

function rewrite(md) {
	// a link back to our own site should be a path, so it works in preview too
	md = md.replace(new RegExp(`\\]\\(${SITE}(/[^)\\s]*)\\)`, 'g'), (_, path) => {
		rewrites.push([SITE + path, path]);
		return `](${path})`;
	});

	// Images. A screenshot of a filing is evidence and must be served byte-for-byte,
	// so it goes to public/sources/ untouched. Decorative images are not cited with @/ at
	// all — they sit beside the page under web/ and Astro optimises them there.
	md = md.replace(IMG_RE, (whole, alt, target) => {
		const rel = stripPrefix(target);
		const url = publishSource(rel);
		if (!url) return whole;
		rewrites.push([target, url]);
		return `![${alt}](${url})`;
	});

	md = md.replace(LINK_RE, (whole, text, target) => {
		if (whole.startsWith('!')) return whole;             // already handled
		const rel = stripPrefix(target);

		// explainer that lives on this site as its own page
		const m = rel.match(/^explainers\/([^/]+)\.md$/);
		if (m && EXPLAINER_PAGES.has(m[1])) {
			const url = `/explainers/${m[1]}/`;
			rewrites.push([target, url]);
			return `[${text}](${url})`;
		}

		const url = publishSource(rel);
		if (!url) return whole;
		rewrites.push([target, url]);
		return `[${text}](${url})`;
	});

	return md;
}

function yamlValue(v) {
	return typeof v === 'string' ? `'${v.replace(/'/g, "''")}'` : String(v);
}

/* ---- resolve citations on every page ----------------------------------- */
/* Any page written with @/ gets the same treatment: document copied in, link
   rewritten in place. Pages with no citations are left untouched. */

function rewriteSitePages(dir) {
	for (const name of readdirSync(dir, { withFileTypes: true })) {
		const full = join(dir, name.name);
		if (name.isDirectory()) { rewriteSitePages(full); continue; }
		if (!name.name.endsWith('.md')) continue;
		if (full === generatedSourceIndex) continue;      // regenerated below anyway
		const before = readFileSync(full, 'utf8');
		if (!/\]\(@\//.test(before)) continue;             // nothing to do
		currentDest = full;
		const after = rewrite(before);
		if (after !== before) {
			writeFileSync(full, after, 'utf8');
			console.log(`citations rewritten: ${relative(WEB, full)}`);
		}
	}
}

const generatedSourceIndex = join(WEB, 'content', 'sources', 'index.md');
const generatedSourceDir = join(WEB, 'content', 'sources');

/* Slugs must resolve on every run, not only the run that first published a document.
   Walk what has already been copied into public/sources/ and register it, so a page
   that was converted to /sources/<slug>/ on an earlier run still maps back. */
function warmRegistry(dir, base = dir) {
	if (!existsSync(dir)) return;
	for (const e of readdirSync(dir, { withFileTypes: true })) {
		const full = join(dir, e.name);
		if (e.isDirectory()) { warmRegistry(full, base); continue; }
		const rel = relative(base, full).split(sep).join('/');
		if (isText(rel)) sourceUrl(rel);
	}
}
warmRegistry(PUBLIC_SOURCES);

/* Citations written before source pages existed point straight at the raw file.
   Move them onto the page. One-way, like the @/ rewrite above. */
function migrateFileLinks(dir) {
	for (const e of readdirSync(dir, { withFileTypes: true })) {
		const full = join(dir, e.name);
		if (e.isDirectory()) {
			if (full === generatedSourceDir) continue;   // generated, and its download
			migrateFileLinks(full);                      // links must stay file links
			continue;
		}
		if (!e.name.endsWith('.md')) continue;
		const before = readFileSync(full, 'utf8');
		const after = before.replace(/\]\(\/sources\/([^)\s#]+\.(?:txt|md))\)/gi,
			(whole, p) => {
				const rel = decodeURIComponent(p);
				return existsSync(join(PUBLIC_SOURCES, rel)) ? `](${sourceUrl(rel)})` : whole;
			});
		if (after !== before) {
			writeFileSync(full, after, 'utf8');
			console.log(`source links moved to pages: ${relative(WEB, full)}`);
		}
	}
}
migrateFileLinks(join(WEB, 'content'));
{
	const home = join(WEB, 'index.md');
	if (existsSync(home)) {
		const b = readFileSync(home, 'utf8');
		const a = b.replace(/\]\(\/sources\/([^)\s#]+\.(?:txt|md))\)/gi, (whole, p) => {
			const rel = decodeURIComponent(p);
			return existsSync(join(PUBLIC_SOURCES, rel)) ? `](${sourceUrl(rel)})` : whole;
		});
		if (a !== b) writeFileSync(home, a, 'utf8');
	}
}

rewriteSitePages(join(WEB, 'content'));
{
	const home = join(WEB, 'index.md');
	if (existsSync(home) && /\]\(@\//.test(readFileSync(home, 'utf8'))) {
		currentDest = home;
		writeFileSync(home, rewrite(readFileSync(home, 'utf8')), 'utf8');
		console.log('citations rewritten: index.md');
	}
}

/* ---- source index page -------------------------------------------------- */
/* Every document the article cites, listed on one page, so a reader can browse
   the evidence without hunting through the prose for links. */

const GROUPS = {
	web_articles: 'News coverage',
	state_of_tennessee: 'State records and statutes',
	sumner_county: 'County and city records',
	usa_federal: 'Federal filings',
	podcasts: 'Recorded interviews',
};

function describe(relPath) {
	const abs = resolve(RESEARCH, relPath);
	if (!/\.(txt|md)$/i.test(relPath)) return null;
	try {
		const head = readFileSync(abs, 'utf8').slice(0, 2000);
		const get = (k) => (head.match(new RegExp('^' + k + ':\\s*(.+)$', 'm')) || [])[1]?.trim();
		const headline = get('HEADLINE');
		const source = get('SOURCE');
		const date = get('DATE');
		if (headline) return [headline, [source, date].filter(Boolean).join(', ')];
		return null;
	} catch {
		return null;
	}
}

/** Turn a bare filename into something a human wants to read. */
const PRETTY = {
	'tca-7-53-302-corporate-powers.pdf': ['T.C.A. § 7-53-302 — Corporate powers of an Industrial Development Board', 'Tennessee Code Annotated'],
	'tca-7-53-305-tax-exemption-pilot.pdf': ['T.C.A. § 7-53-305 — Tax exemption and payments in lieu of taxes', 'Tennessee Code Annotated'],
	'metas-gallatin-data-center.pdf': ["Meta's Gallatin Data Center (company fact sheet)", 'Meta'],
};

function prettify(relPath) {
	const name = relPath.split('/').pop();
	if (PRETTY[name]) return PRETTY[name];
	if (relPath.startsWith('podcasts/transcripts/')) {
		const t = name.replace(/\.txt$/, '').split('-').join(' ');
		return [`Transcript: ${t.charAt(0).toUpperCase() + t.slice(1)}`, 'Whisper transcript of the episode audio'];
	}
	return null;
}

/* The index must reflect what the site actually links, not what this run happened to
   rewrite. A page whose @/ links were converted on an earlier run contains no @/ any
   more, so its citations would silently drop out. Scan the built content for
   /sources/ links instead, and union that with this run's rewrites. */
function linkedSources(dir, found = new Set()) {
	for (const e of readdirSync(dir, { withFileTypes: true })) {
		const full = join(dir, e.name);
		if (e.isDirectory()) { linkedSources(full, found); continue; }
		if (!e.name.endsWith('.md')) continue;
		if (full === generatedSourceIndex) continue;   // it lists them all; reading it
		                                               // back would make the index immortal
		for (const m of readFileSync(full, 'utf8').matchAll(/\]\(\/sources\/([^)\s#]+)\)/g)) {
			const token = decodeURIComponent(m[1]);
			// a page link is /sources/<slug>/ — map it back to the document it renders
			const asSlug = token.replace(/\/$/, '');
			found.add(bySlug.has(asSlug) ? bySlug.get(asSlug) : token);
		}
	}
	return found;
}

const cited = [...new Set([
	...rewrites.map(([from]) => stripPrefix(from)),
	...linkedSources(join(WEB, 'content')),
])].filter((p) => !p.startsWith('explainers/') && !p.startsWith('/') && !p.startsWith('http'));

/* One page per cited text document, rendered in the site's own layout. The body goes
   inside <pre> rather than being parsed as markdown: a transcript line starting with #
   is not a heading, an audit containing < is not a tag, and a Comptroller table only
   survives as fixed-width text. Escaped, verbatim, with the untouched file one click
   away. */
const esc = (t) => t.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
const yamlQuote = (t) => "'" + String(t).replace(/'/g, "''") + "'";

function splitProvenance(text) {
	// headered captures start KEY: value, then a --- rule, then the document
	const m = text.match(/^((?:[A-Z][A-Z ]+:[\s\S]*?)\n)---\n/);
	if (!m) return [[], text];
	const meta = [];
	for (const line of m[1].split('\n')) {
		const kv = line.match(/^([A-Z][A-Z ]+):\s*(.*)$/);
		if (kv) meta.push([kv[1], kv[2].trim()]);
		else if (meta.length && line.trim()) meta[meta.length - 1][1] += ' ' + line.trim();
	}
	return [meta, text.slice(m[0].length).replace(/^\n+/, '')];
}

let pages = 0;
function writeSourcePage(relPath) {
	const abs = resolve(RESEARCH, relPath);
	if (!existsSync(abs) || !isText(relPath)) return;
	const slug = sourceUrl(relPath).replace(/^\/sources\/|\/$/g, '');
	const raw = readFileSync(abs, 'utf8');
	const [meta, body] = splitProvenance(raw);
	const d = describe(relPath) || prettify(relPath);
	// a derived .md carries its own name in its first heading; better than the filename
	const h1 = raw.match(/^#\s+(.+)$/m);
	const title = d ? d[0] : (h1 ? h1[1].trim() : relPath.split('/').pop());
	const desc = d && d[1] ? d[1] : 'Source document cited in the investigation.';
	const fileUrl = '/sources/' + relPath.split('/').map(encodeURIComponent).join('/');

	let md = `---\ntitle: ${yamlQuote(title)}\ndescription: ${yamlQuote(desc)}\n---\n\n`;
	md += `# **${esc(title)}**\n\n`;
	md += `<p class="src-back"><a href="/sources/">All sources</a></p>\n\n`;
	if (meta.length) {
		md += '<dl class="src-prov">\n';
		for (const [k, v] of meta) {
			const val = /^https?:\/\//.test(v)
				? `<a href="${esc(v)}" rel="nofollow noopener">${esc(v)}</a>` : esc(v);
			md += `<dt>${esc(k.toLowerCase())}</dt><dd>${val}</dd>\n`;
		}
		md += '</dl>\n\n';
	}
	md += `<p class="src-file"><a href="${fileUrl}" download>Download the original file</a>`
	    + ` &middot; <code>${esc(relPath.split('/').pop())}</code></p>\n\n`;
	if (/\.md$/i.test(relPath)) {
		// already markdown — render it, same as any explainer page
		md += body.replace(/^#\s+.+$/m, '').trimStart() + '\n';
	} else {
		md += `<pre class="src-body">${esc(body.trimEnd())}</pre>\n`;
	}

	const out = join(generatedSourceDir, slug + '.md');
	mkdirSync(dirname(out), { recursive: true });
	if (writeIfChanged(out, md)) pages++;
}
for (const p of cited) writeSourcePage(p);

const byGroup = {};
for (const p of cited.sort()) {
	const top = p.split('/')[0];
	(byGroup[GROUPS[top] || 'Other'] ??= []).push(p);
}

let idx =
	`---\ntitle: 'Sources'\ndescription: 'Every document cited in the investigation, in full.'\n---\n\n` +
	`# **Sources**\n\n` +
	`Every document cited in the investigation, exactly as it was filed, published, or recorded. ` +
	`Nothing here is a summary. Click any citation in the article and you land on the same file.\n\n` +
	`Where a document was captured from a page that has since changed or gone behind a block, the ` +
	`file header records the original URL, the archive copy, and the date it was retrieved.\n\n`;

for (const [group, paths] of Object.entries(byGroup)) {
	idx += `## ${group}\n\n`;
	for (const p of paths) {
		const url = sourceUrl(p);
		const d = describe(p) || prettify(p);
		const name = p.split('/').pop();
		idx += d
			? `- [${d[0]}](${url})  \n  <span class="src-meta">${d[1]} · \`${name}\`</span>\n`
			: `- [${name}](${url})\n`;
	}
	idx += '\n';
}

const idxPath = join(WEB, 'content', 'sources', 'index.md');
mkdirSync(dirname(idxPath), { recursive: true });
writeIfChanged(idxPath, idx);
console.log(`published: ${relative(WEB, idxPath)} (${cited.length} documents)`);

console.log(`  ${copied} source file(s) copied into public/sources/`);
console.log(`  ${pages} source page(s) rendered into content/sources/`);
console.log(`  ${rewrites.length} link(s) rewritten`);
if (missing.length) {
	console.error(`\n  MISSING (${missing.length}) — link left as-is:`);
	for (const m of missing) console.error(`    ${m}`);
	process.exitCode = 1;
}

/* The @/ rewrite above only copies documents it is asked to copy. A link already
   written as /sources/... is assumed to have been copied on an earlier run, which is
   true right up until someone edits one by hand to point somewhere else. Then the new
   target was never copied and the page ships a 404, silently, because nothing above
   looks at links that are already in their final form.

   Found 2026-08-19, when a citation was repointed at a different archive file during a
   rename and the build passed anyway. Check every /sources/ link that survived the
   rewrite, and fail the publish the same way a missing @/ document does. */
const deadSourceLinks = [];
function checkSourceLinks(dir) {
	for (const e of readdirSync(dir, { withFileTypes: true })) {
		const full = join(dir, e.name);
		if (e.isDirectory()) { checkSourceLinks(full); continue; }
		if (!e.name.endsWith('.md')) continue;
		const text = readFileSync(full, 'utf8');
		for (const m of text.matchAll(/\]\(\/sources\/([^)\s#]+)\)/g)) {
			const rel = decodeURIComponent(m[1]);
			// A /sources/<slug>/ link resolves to a generated page, not a copied file.
			if (rel.endsWith('/')) {
				if (!existsSync(join(generatedSourceDir, rel.replace(/\/$/, '') + '.md')))
					deadSourceLinks.push(`${relative(WEB, full)} -> /sources/${rel}`);
				continue;
			}
			if (!existsSync(join(PUBLIC_SOURCES, rel)))
				deadSourceLinks.push(`${relative(WEB, full)} -> /sources/${rel}`);
		}
	}
}
checkSourceLinks(join(WEB, 'content'));
if (deadSourceLinks.length) {
	console.error(`\n  DEAD /sources/ LINKS (${deadSourceLinks.length}) — target was never copied:`);
	for (const d of deadSourceLinks) console.error(`    ${d}`);
	process.exitCode = 1;
} else {
	console.log('  every /sources/ link resolves to a copied document or a generated page');
}
