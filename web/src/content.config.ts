import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// One collection for every page on the site. The folder structure under
// content/ is the URL structure: content/tennessee/fisk.md -> /tennessee/fisk/
const content = defineCollection({
	loader: glob({ base: './content', pattern: ['**/*.md', '!**/README.md'] }),
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			// Investigations are dated. Standing reference pages are not.
			pubDate: z.coerce.date().optional(),
			updatedDate: z.coerce.date().optional(),
			draft: z.boolean().default(false),
			// Long pages opt into the inline contents drawer and progress bar.
			toc: z.boolean().default(false),
			/*
			  A multi-part piece sets `series` to a shared slug and `part` to its
			  number. Everything else — the "Part 2 of 4" label, the previous and
			  next links, the list of parts at the foot of each page — is derived
			  from the collection at build time by SeriesNav.astro. Adding a part
			  means adding a file and setting `part`; nothing else is edited, so no
			  two pages can disagree about what the series contains.
			  `partTitle` is the short name used in that navigation, since a page's
			  own `title` usually repeats the series name and reads badly in a link.
			*/
			series: z.string().optional(),
			part: z.number().int().positive().optional(),
			partTitle: z.string().optional(),
			heroImage: z.optional(image()),
			/* A taller crop of the same scene, served to phones. Optional. */
			heroImageNarrow: z.optional(image()),
		}),
});

export const collections = { content };
