import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Canonical URLs, the sitemap and OpenGraph tags are built from `site`.
export default defineConfig({
  site: 'https://alexeykatin.xyz',
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [sitemap()],
});
