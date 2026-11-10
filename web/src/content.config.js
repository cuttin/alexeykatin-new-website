import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// Old travel notes from japanforayear.ru (Russian), one folder per post: index.md plus its photos.
// The folder name is the old post's URL stem, so japanforayear.ru/<stem>.html maps to /memories/<stem>/.
const memories = defineCollection({
  loader: glob({ pattern: '*/index.md', base: './src/content/memories', generateId: ({ entry }) => entry.split('/')[0] }),
  schema: ({ image }) => z.object({
    title: z.string(),
    date: z.coerce.date(),
    category: z.enum(['Япония', 'Азия', 'США', 'Полезное']),
    cover: image().optional(),
  }),
});

export const collections = { memories };
