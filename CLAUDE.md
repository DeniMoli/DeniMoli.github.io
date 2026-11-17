# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
yarn dev          # Dev server with hot reload at localhost:3000
yarn build        # Production build (SSR)
yarn generate     # Static site generation
yarn preview      # Preview production build
yarn lint         # ESLint check
yarn lint:fix     # ESLint auto-fix
```

For GitHub Pages deployment specifically:
```bash
yarn build:gh-pages   # Build with DEPLOY_ENV=GH_PAGES
```

## Architecture

This is a **Nuxt 3** personal blog with **SSR** and static generation support, deployed to GitHub Pages via CI.

**Content layer** (`@nuxt/content`): Blog posts live in `content/blogs/` as Markdown files. Each post requires frontmatter:
```yaml
title, date, description, image, alt, ogImage, tags (array), published (boolean)
```
Posts in `content/old/` are archived. Only posts with `published: true` are shown.

**Routing**:
- `/` — home page (`pages/index.vue`)
- `/blogs` — paginated blog list with search (`pages/blogs/index.vue`)
- `/blogs/[blog]` — single post (`pages/blogs/[blog].vue`)
- `/categories` — all categories auto-derived from post tags (`pages/categories/`)
- `/about` — about page
- `[...slug].vue` — catch-all for content routes

**Styling**: TailwindCSS with `@tailwindcss/typography` (for Markdown rendering) and `@tailwindcss/forms`. Dark mode uses `class` strategy, defaulting to dark. Custom font: Space Grotesk.

**Key modules**: `nuxt-og-image` for OG previews, `nuxt-simple-sitemap` for sitemap, `nuxt-icon` for icons, `@nuxtjs/color-mode` for dark/light toggle, `@nuxt/image` for optimized images.

**Types**: `BlogPost` interface is defined in `types/blog.ts`.

**Deployment**: GitHub Actions (`.github/workflows/deploy.yml`) builds with `--preset github_pages` and deploys `.output/public` to GitHub Pages on every push to `master`.
