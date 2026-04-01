import { defineConfig } from 'astro/config';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default defineConfig({
  site: 'https://ai-referent.github.io',
  base: '/',
  output: 'static',
  build: {
    outDir: './dist'
  },
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
    shikiConfig: {
      theme: 'github-light',
      langs: [],
      wrap: true,
    },
  },
  vite: {
    ssr: {
      external: ['svgo']
    }
  }
});
