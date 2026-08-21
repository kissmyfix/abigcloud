// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

/**
 * Astro marks every markdown image `loading="lazy"`, which is wrong for the first
 * image on a page: the browser delays the most visible thing on screen. Mark the
 * first one eager and leave the rest lazy.
 */
function eagerFirstImage() {
	return (tree) => {
		let found = false;
		const walk = (node) => {
			if (found || !node) return;
			if (node.tagName === 'img' && node.properties) {
				node.properties.loading = 'eager';
				node.properties.fetchpriority = 'high';
				found = true;
				return;
			}
			for (const child of node.children ?? []) walk(child);
		};
		walk(tree);
	};
}

/**
 * `<!-- @c ... -->` notes are messages to Claude, not content. Markdown passes HTML
 * comments straight through, so without this they land in the shipped HTML and anyone
 * reading View Source reads the author's working notes. Stripped here, at render, so
 * the source file keeps every note and this runs in CI too — the deploy workflow runs
 * `astro build` directly and never sees `npm run publish`.
 *
 * Substring removal, not node removal: a paragraph whose first line opens with a
 * comment is parsed as one raw-HTML block containing the prose as well, so dropping
 * the node would take the writing with it.
 */
const NOTE = /<!--\s*@c\b[\s\S]*?-->/g;

function stripClaudeNotes() {
	return (tree) => {
		const walk = (node) => {
			if (node.type === 'html' && typeof node.value === 'string') {
				node.value = node.value.replace(NOTE, '');
			}
			if (!node.children) return;
			node.children = node.children.filter(
				(c) => !(c.type === 'html' && !(c.value ?? '').trim()),
			);
			for (const child of node.children) walk(child);
		};
		walk(tree);
	};
}

// https://astro.build/config
export default defineConfig({
	site: 'https://abigcloud.com',
	integrations: [mdx(), sitemap()],
	// The Reference section became Explainers on 2026-08-21. Anything already
	// pointing at the old paths keeps working instead of 404ing.
	redirects: {
		'/reference': '/explainers',
		'/reference/501c4-vs-instrumentality': '/explainers/501c4-vs-instrumentality',
		'/reference/confirmed-falsehoods': '/explainers/confirmed-falsehoods',
		'/reference/open-threads': '/explainers/open-threads',
		'/reference/the-title-transfer-mechanism': '/explainers/the-title-transfer-mechanism',
		'/reference/what-is-a-pilot': '/explainers/what-is-a-pilot',
		'/reference/what-is-an-idb': '/explainers/what-is-an-idb',
	},
	markdown: {
		remarkPlugins: [stripClaudeNotes],
		rehypePlugins: [eagerFirstImage],
	},
});
