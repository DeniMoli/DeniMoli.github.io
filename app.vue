<script setup>
const description
    = 'Исследуйтем мир веб технологий вместе. Маленький блог о всем что может пригодится разработчику.'
const ogTitle
    = 'Исследуйтем мир веб технологий вместе. Маленький блог о всем что может пригодится разработчику.'
const twitterDescription
    = 'Исследуйтем мир веб технологий вместе. Маленький блог о всем что может пригодится разработчику.'
const image
    = ''
const keywords = 'WEB, Front-end, Back-end, Innovation, Learn, Explore'
const mySite = 'https://denimoli.github.io/'

useHead({
  htmlAttrs: {
    lang: 'ru',
  },
  meta: [
    {
      name: 'description',
      content: description,
    },
    {
      name: 'keywords',
      content: keywords,
    },
    // Test on: https://developers.facebook.com/tools/debug/ or https://socialsharepreview.com/
    {
      property: 'og:site_name',
      content: mySite,
    },
    {
      property: 'og:type',
      content: 'website',
    },
    {
      property: 'og:url',
      content: mySite,
    },
    {
      property: 'og:title',
      content: ogTitle,
    },
    {
      property: 'og:description',
      content: description,
    },
    {
      property: 'og:image',
      content: image,
    },
    // Test on: https://cards-dev.twitter.com/validator or https://socialsharepreview.com/
    {
      name: 'twitter:site',
      content: '',
    },
    {
      name: 'twitter:card',
      content: 'summary_large_image',
    },
    {
      name: 'twitter:url',
      content: mySite,
    },
    {
      name: 'twitter:title',
      content: ogTitle,
    },
    {
      name: 'twitter:description',
      content: twitterDescription,
    },
    {
      name: 'twitter:image',
      content: image,
    },
  ],
})
</script>

<template>
  <div class="bg-[#F1F2F4] dark:text-zinc-300 dark:bg-slate-950">
    <NuxtLoadingIndicator :throttle="0" />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<style>
  .page-enter-active,
  .page-leave-active {
    transition: all 0.4s;
  }

  .page-enter-from,
  .page-leave-to {
    opacity: 0;
    filter: blur(1rem);
  }

  .layout-enter-active,
  .layout-leave-active {
    transition: all 0.4s;
  }

  .layout-enter-from,
  .layout-leave-to {
    opacity: 0;
    filter: blur(1rem);
  }

  html.dark {
    color-scheme: dark;
  }
</style>
