// https://nuxt.com/docs/api/configuration/nuxt-config
// only add `router.base = '/<repository-name>/'` if `DEPLOY_ENV` is `GH_PAGES`

export default defineNuxtConfig({
  app: {
    head: {
      charset: 'utf-16',
      viewport: 'width=device-width,initial-scale=1',
      title: 'Deni B Blog',
      titleTemplate: '%s - Deni B Blog',
      meta: [
        {
          name: 'description',
          content:
            'Deni B Blog. Исследуйтем мир веб технологий вместе. Маленький блог о всем что может пригодится разработчику.',
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
    // unenv@2 changed its path structure — nuxt-og-image@3 uses the old paths
    alias: {
      'unenv/runtime/mock/empty': 'unenv/mock/empty',
      'unenv/runtime/mock/proxy-cjs': 'unenv/mock/proxy-cjs',
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
