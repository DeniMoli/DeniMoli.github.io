<script setup lang="ts">
defineOgImageComponent('About', {
  headline: 'Приветствую вас 👋',
  title: 'Deni B Blog',
  description: 'Full Stack Developer — Vue 3, Nuxt 3, TypeScript, PHP. Пишу о веб-разработке и технологиях.',
  link: '/Denis.png',
})
</script>

<template>
  <div class="py-5">
    <div class="sm:grid grid-cols-8 px-6 py-5 sm:py-9 gap-5 container max-w-5xl  mx-auto">
      <div class="col-span-5  max-w-md">
        <div class="flex justify-between">
          <div>
            <h1 class="text-xl sm:text-4xl  pb-2 font-bold ">
              Денис Бычков
            </h1>

            <div class="my-3 space-x-2 md:space-x-3 pb-10">
              <NuxtLink
                to="https://github.com/DeniMoli"
                target="_blank"
                class="px-2 py-1 lg:px-3 lg:py-2 bg-gray-300 text-gray-800 rounded-md dark:bg-slate-700 dark:text-[#F1F2F4]"
                aria-label="Github"
              >
                <Icon name="fa:github" size="1em" />
              </NuxtLink>
              <NuxtLink
                to="https://t.me/Deni62"
                target="_blank"
                class="px-2 py-1 lg:px-3 lg:py-2 bg-gray-300 text-gray-800 rounded-md dark:bg-slate-700 dark:text-[#F1F2F4]"
                aria-label="Telegram"
              >
                <Icon name="fa:telegram" size="1em" />
              </NuxtLink>
              <NuxtLink
                to="https://hh.ru/resume/6a8a4c8cff032ded650039ed1f646a44784764"
                target="_blank"
                class="px-2 py-1 lg:px-3 lg:py-2 bg-gray-300 text-gray-800 rounded-md dark:bg-slate-700 dark:text-[#F1F2F4]"
                aria-label="HeadHunter"
              >
                <Icon name="fa:briefcase" size="1em" />
              </NuxtLink>
            </div>
          </div>
          <div class="sm:hidden block col-span-3 pb-5 dark:text-[#F1F2F4]">
            <NuxtImg
              src="/Denis.png"
              width="125"
              height="115"
              quality="50"
              class="rounded-md"
            />
          </div>
        </div>
        <h3 class="text-base sm:text-3xl font-semibold pb-7 sm:pb-12">
          Full Stack Developer · Vue · Nuxt · TypeScript
        </h3>

        <p>
          Привет! Я Full Stack Developer с почти 10 годами опыта в разработке. Сейчас работаю в SBX Group, где занимаюсь созданием масштабируемых SPA и SSR приложений на Vue 3 и Nuxt 3, бэкендом на PHP/Symfony/Laravel, настройкой Docker и CI/CD, а также интеграцией AI в продуктовые процессы. Этот блог — место, где я делюсь интересными находками из мира веб-разработки и технологий.
        </p>
      </div>
      <div class="hidden sm:block col-span-3">
        <NuxtImg
          src="/Denis.png"
          width="450"
          height="500"
          quality="50"
          class="rounded-md"
        />
      </div>
    </div>
  </div>
</template>
