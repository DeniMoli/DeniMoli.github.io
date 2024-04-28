// https://nuxt.com/docs/api/configuration/nuxt-config
// only add `router.base = '/<repository-name>/'` if `DEPLOY_ENV` is `GH_PAGES`
// eslint-disable-next-line n/prefer-global/process
const routerBase = process.env.DEPLOY_ENV === 'GH_PAGES'
  ? {
      generate: {
        routes: '/d-blog/',
      },
    }
  : {}

export default defineNuxtConfig({
  ...routerBase,
  app: {
    head: {
      charset: 'utf-16',
      viewport: 'width=device-width,initial-scale=1',
      title: 'D-blog',
      titleTemplate: '%s - D-Blog',
      meta: [
        {
          name: 'description',
          content:
            'D-Blog Исследуйтем мир веб технологий вместе. Маленький блог о всем что может пригодится разработчику.',
        },
      ],
    },
    pageTransition: {
      name: 'page',
      mode: 'out-in',
    },
    layoutTransition: {
      name: 'layout',
      mode: 'out-in',
    },
  },

  sitemap: {
    strictNuxtContentPaths: true,
  },

  site: {
    url: 'https://denimoli.github.io/',
    identity: {
      type: 'Person',
    },
    twitter: '',
  },

  typescript: {
    strict: true,
  },

  nitro: {
    prerender: {
      crawlLinks: true,
      routes: ['/'],
    },
  },

  colorMode: {
    classSuffix: '',
    preference: 'dark',
    fallback: 'light',
  },

  modules: [
    'nuxt-icon',
    '@nuxt/image',
    '@vueuse/nuxt',
    'nuxt-og-image',
    '@nuxt/content',
    '@nuxtjs/robots',
    '@nuxtjs/fontaine',
    '@nuxtjs/color-mode',
    'nuxt-simple-sitemap',
    '@nuxtjs/tailwindcss',
  ],

  content: {
    highlight: {
      theme: 'dracula',
    },
  },
})
