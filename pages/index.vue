<script lang="ts" setup>
useHead({
  title: 'Главная',
  meta: [
    {
      name: 'description',
      content:
        'Добро пожаловать на мой блог. Получите веб-разработку, Javascript, Typescript, NodeJs, Vue и Nuxt, соответствующие статьи, советы, обучающие ресурсы и многое другое.',
    },
  ],
  titleTemplate: 'Deni B Blog - %s',
})

// Generate OG Image
defineOgImageComponent('About', {
  headline: 'Приветствую вас 👋',
  title: 'Денис Бычков',
  description: 'Погрузитесь в веб-разработку вместе со мной и изучите Js, Ts, Vue, Nuxt, Docker',
  link: '/Denis.jpg',
})
</script>

<template>
  <main class="container max-w-5xl mx-auto text-zinc-600">
    <MainHero />
    <MainRecent />
    <MainTrending />
  </main>
</template>
