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
			// Long pages opt into the sticky table of contents and progress bar.
			toc: z.boolean().default(false),
			heroImage: z.optional(image()),
			/* A taller crop of the same scene, served to phones. Optional. */
			heroImageNarrow: z.optional(image()),
		}),
});

export const collections = { content };
