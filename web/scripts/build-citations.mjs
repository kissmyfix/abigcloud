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
 * Decorative images (visualizations/) are routed through Astro's optimiser instead of
 * being copied raw. Evidence images are copied byte-for-byte, because a screenshot of
 * a filing has to be the actual file.
 *
 * Exits non-zero if a citation points at a document that does not exist.
 *
 * Usage: node scripts/build-citations.mjs      (npm run publish runs it, then builds)
 */
import { readFileSync, writeFileSync, mkdirSync, copyFileSync, existsSync, readdirSync } from 'node:fs';
import { dirname, join, resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const WEB = resolve(HERE, '..');
const RESEARCH = resolve(WEB, '..');            // ~/Documents/data_center_research
const PUBLIC_SOURCES = join(WEB, 'public', 'sources');

/** Reference explainers that already exist as pages on this site. */
const REFERENCE_PAGES = new Set(['what-is-an-idb', 'what-is-a-pilot', 'the-title-transfer-mechanism', '501c4-vs-instrumentality']);

// A citation is written @/ followed by a path in the research archive:
//   @/web_articles/foo.txt
// ../ is still accepted so older pages keep working, but @/ is the form to use --
// ../ means a real relative path inside content/ and is ambiguous there.
const LINK_RE = /\[([^\]]*)\]\(((?:\.\.|@)\/[^)\s]+)\)/g;
const IMG_RE = /!\[([^\]]*)\]\(((?:\.\.|@)\/[^)\s]+)\)/g;
const stripPrefix = (target) => target.replace(/^(?:\.\.|@)\//, '');

let copied = 0;
let optimised = 0;
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
	return '/sources/' + relPath.split('/').map(encodeURIComponent).join('/');
}

const SITE = 'https://abigcloud.com';

function rewrite(md) {
	// a link back to our own site should be a path, so it works in preview too
	md = md.replace(new RegExp(`\\]\\(${SITE}(/[^)\\s]*)\\)`, 'g'), (_, path) => {
		rewrites.push([SITE + path, path]);
		return `](${path})`;
	});

	// Images. A screenshot of a filing is evidence and must be served byte-for-byte,
	// so it goes to public/sources/ untouched. A decorative image is not evidence, so
	// it sits beside the page and goes through Astro's optimiser like every other
	// image on the site — otherwise an 841KB PNG lands at the top of the article.
	md = md.replace(IMG_RE, (whole, alt, target) => {
		const rel = stripPrefix(target);
		if (rel.startsWith('visualizations/')) {
			const abs = resolve(RESEARCH, rel);
			if (!existsSync(abs)) {
				missing.push(rel);
				return whole;
			}
			const name = rel.split('/').pop();
			const out = join(dirname(currentDest), name);
			mkdirSync(dirname(out), { recursive: true });
			copyFileSync(abs, out);
			optimised++;
			rewrites.push([target, './' + name]);
			return `![${alt}](./${name})`;
		}
		const url = publishSource(rel);
		if (!url) return whole;
		rewrites.push([target, url]);
		return `![${alt}](${url})`;
	});

	md = md.replace(LINK_RE, (whole, text, target) => {
		if (whole.startsWith('!')) return whole;             // already handled
		const rel = stripPrefix(target);

		// reference explainer that lives on this site as its own page
		const m = rel.match(/^reference\/([^/]+)\.md$/);
		if (m && REFERENCE_PAGES.has(m[1])) {
			const url = `/reference/${m[1]}/`;
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
	visualizations: 'Images',
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
			found.add(decodeURIComponent(m[1]));
		}
	}
	return found;
}

const cited = [...new Set([
	...rewrites.map(([from]) => stripPrefix(from)),
	...linkedSources(join(WEB, 'content')),
])].filter((p) => !p.startsWith('reference/') && !p.startsWith('/') && !p.startsWith('http') && !p.startsWith('visualizations/'));

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
		const url = '/sources/' + p.split('/').map(encodeURIComponent).join('/');
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
writeFileSync(idxPath, idx, 'utf8');
console.log(`published: ${relative(WEB, idxPath)} (${cited.length} documents)`);

console.log(`  ${copied} source file(s) copied into public/sources/`);
console.log(`  ${optimised} image(s) routed through the asset pipeline`);
console.log(`  ${rewrites.length} link(s) rewritten`);
if (missing.length) {
	console.error(`\n  MISSING (${missing.length}) — link left as-is:`);
	for (const m of missing) console.error(`    ${m}`);
	process.exitCode = 1;
}
