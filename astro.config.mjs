import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://ai-referent.github.io',
  base: '/',
  output: 'static',
  build: {
    outDir: './dist'
  },
  markdown: {
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
