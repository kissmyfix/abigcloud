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

// https://astro.build/config
export default defineConfig({
	site: 'https://abigcloud.com',
	integrations: [mdx(), sitemap()],
	markdown: {
		rehypePlugins: [eagerFirstImage],
	},
});
