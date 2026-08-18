#!/usr/bin/env node
/**
 * build-article.mjs — publish a draft from the research tree onto the site.
 *
 * The draft in the research tree uses filesystem-relative links, e.g.
 *   [$1.1 billion overhaul](../web_articles/2013-04-07-timesfreepress-....txt)
 * so Brandon can click them in his local editor. Those paths mean nothing to a
 * visitor. This script is the bridge: it copies every cited document into
 * web/public/sources/ and rewrites the link to a public URL, so a reader who
 * clicks a citation lands on the actual document without leaving the site.
 *
 * Two rules:
 *   ../reference/foo.md  -> /reference/foo/   (a page that already exists here)
 *   ../anything/else.pdf -> /sources/anything/else.pdf  (copied in)
 *
 * Absolute URLs pass through untouched.
 *
 * Usage: node scripts/build-article.mjs
 */
import { readFileSync, writeFileSync, mkdirSync, copyFileSync, existsSync, readdirSync } from 'node:fs';
import { dirname, join, resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const WEB = resolve(HERE, '..');
const RESEARCH = resolve(WEB, '..');            // ~/Documents/data_center_research
const PUBLIC_SOURCES = join(WEB, 'public', 'sources');

/**
 * Drafts are discovered, not hard-coded. Any markdown file under monologues/ that
 * carries a publish directive gets published. Rename or add files freely; nothing
 * here needs editing.
 *
 * Put this anywhere in the draft (an HTML comment, so it is invisible in the
 * rendered preview and stripped from the published copy):
 *
 *   <!-- publish
 *        to: investigations/quid_pro_no
 *        title: Quid-Pro-NO!
 *        description: How every level of government has failed Tennesseans...
 *        date: 2026-08-17
 *        draft: false
 *   -->
 *
 * `to:` is the path under content/, so it becomes the URL. Everything else is
 * frontmatter for the site page.
 */
const DRAFTS_DIR = join(RESEARCH, 'monologues');
const PUBLISH_RE = /<!--\s*publish\s*\n([\s\S]*?)-->/;

function findDrafts() {
	if (!existsSync(DRAFTS_DIR)) return [];
	const out = [];
	for (const name of readdirSync(DRAFTS_DIR)) {
		if (!name.endsWith('.md')) continue;
		const src = join(DRAFTS_DIR, name);
		const m = PUBLISH_RE.exec(readFileSync(src, 'utf8'));
		if (!m) continue;
		const fm = {};
		let to = null;
		for (const line of m[1].split('\n')) {
			const kv = line.match(/^\s*([a-z]+)\s*:\s*(.+?)\s*$/i);
			if (!kv) continue;
			if (kv[1].toLowerCase() === 'to') to = kv[2].replace(/^\/+|\/+$/g, '');
			else fm[kv[1]] = kv[2] === 'true' ? true : kv[2] === 'false' ? false : kv[2];
		}
		if (!to) {
			console.error(`  ! ${name} has a publish block with no "to:" — skipped`);
			continue;
		}
		if (fm.date) { fm.pubDate = fm.date; delete fm.date; }
		if (fm.draft === undefined) fm.draft = false;
		out.push({ src, dest: join(WEB, 'content', to, 'index.md'), frontmatter: fm, name });
	}
	return out;
}

const ARTICLES = findDrafts();
if (!ARTICLES.length) {
	console.error(`No drafts found. Add a <!-- publish ... --> block to a file in ${relative(RESEARCH, DRAFTS_DIR)}/`);
	process.exitCode = 1;
}

/** Reference explainers that already exist as pages on this site. */
const REFERENCE_PAGES = new Set(['what-is-an-idb', 'what-is-a-pilot', 'the-title-transfer-mechanism', '501c4-vs-instrumentality']);

// A citation can be written two ways:
//   @/web_articles/foo.txt   -- from the research archive root. Works in ANY file,
//                               including site pages under content/. Preferred.
//   ../web_articles/foo.txt  -- filesystem-relative, only meaningful in a draft under
//                               monologues/, where it is clickable in Brandon's editor.
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

for (const article of ARTICLES) {
	if (!existsSync(article.src)) {
		console.error(`SKIP (no source): ${article.src}`);
		continue;
	}
	currentDest = article.dest;
	let body = readFileSync(article.src, 'utf8');

	body = body.replace(PUBLISH_RE, '');          // directive is for the build, not the reader

	// strip any leftover author notes before publishing
	const notes = body.match(/<!--\s*@c[\s\S]*?-->/g) || [];
	if (notes.length) {
		console.warn(`  ! ${notes.length} unresolved @c note(s) stripped from published copy`);
		body = body.replace(/<!--\s*@c[\s\S]*?-->\n?/g, '');
	}

	body = rewrite(body);

	const fm =
		'---\n' +
		Object.entries(article.frontmatter)
			.map(([k, v]) => `${k}: ${yamlValue(v)}`)
			.join('\n') +
		'\n---\n\n';

	mkdirSync(dirname(article.dest), { recursive: true });
	writeFileSync(article.dest, fm + body.trimStart() + '\n', 'utf8');
	console.log(`published: ${article.name} -> ${relative(WEB, article.dest)}`);
}

/* ---- site pages -------------------------------------------------------- */
/* Drafts are not the only thing that cites documents. An About page, an explainer,
   a topic page may all want to point at the archive. Any page written with @/ gets
   the same treatment: document copied in, link rewritten. Pages with no citations
   are left untouched. */

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
