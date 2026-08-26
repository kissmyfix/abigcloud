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
 * GitHub-style callout syntax for coloured blockquotes:
 *
 *     > [!source]
 *     > This blockquote renders with the teal accent.
 *
 * The marker is stripped and the blockquote gets the matching CSS class
 * (.is-source, .is-context, etc.) so global.css colours it.
 */
const CALLOUT_RE = /^\[!(finding|red|context|blue|caution|gold|verified|green|source|teal)\]\s*/i;
const CALLOUT_MAP = {
	finding:'is-finding', red:'is-finding',
	context:'is-context', blue:'is-context',
	caution:'is-caution', gold:'is-caution',
	verified:'is-verified', green:'is-verified',
	source:'is-source', teal:'is-source',
};

function remarkCallouts() {
	return (tree) => {
		const walk = (node) => {
			if (node.type === 'blockquote' && node.children?.length) {
				const first = node.children[0];
				if (first.type === 'paragraph' && first.children?.length) {
					const text = first.children[0];
					if (text.type === 'text') {
						const m = text.value.match(CALLOUT_RE);
						if (m) {
							node.data = node.data || {};
							node.data.hProperties = node.data.hProperties || {};
							node.data.hProperties.className = CALLOUT_MAP[m[1].toLowerCase()];
							text.value = text.value.slice(m[0].length);
							if (!text.value && first.children.length === 1) {
								node.children.shift();
							} else if (!text.value) {
								first.children.shift();
							}
						}
					}
				}
			}
			for (const child of node.children || []) walk(child);
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
	markdown: {
		remarkPlugins: [remarkCallouts, stripClaudeNotes],
		rehypePlugins: [eagerFirstImage],
	},
});
