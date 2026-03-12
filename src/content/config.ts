import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    author: z.string().optional(),
    tags: z.array(z.string()).optional(),
    reading_time: z.number().optional(),
    description: z.string().optional(),
    excerpt: z.string().optional(),
  }),
});

export const collections = {
  blog,
};
