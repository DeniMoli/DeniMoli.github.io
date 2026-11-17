<h1 align="center">Блог Дениса Бычкова</h1>

<p align="center">
  Личный блог о фронтенде, JavaScript, Vue/Nuxt и веб-разработке.<br>
  <a href="https://denimoli.github.io/">denimoli.github.io</a>
</p>

<p align="center">
  <img src="./assets/images/dark.png" alt="Превью блога">
</p>

## Стек

[Nuxt 3](https://nuxt.com) · [Nuxt Content](https://content.nuxt.com) · [Vue 3](https://vuejs.org) · [TailwindCSS](https://tailwindcss.com) · GitHub Pages

## Возможности

- Посты в Markdown (`content/blogs/`)
- Категории автоматически собираются из тегов постов
- Список статей с поиском и пагинацией
- Оглавление для каждого поста
- Sitemap и OG-превью ссылок (`nuxt-og-image`)
- Тёмная и светлая тема
- SSR и статическая генерация
- `app-ads.txt` для рекламных сетей (`public/app-ads.txt`)

## Запуск

**Требуется Node.js 22+**

```bash
yarn install        # установить зависимости
yarn dev            # dev-сервер на localhost:3000
yarn build          # production-сборка
yarn preview        # просмотр production-сборки
yarn lint           # проверка ESLint
```

## Новый пост

Создайте файл в `content/blogs/` с frontmatter:

```yaml
---
title: "Заголовок"
date: "2026-11-17"
description: "Краткое описание"
image: "/blogs-img/cover.webp"
alt: "Описание картинки"
ogImage: "/blogs-img/cover.webp"
tags: ["javascript", "frontend"]
published: true
---
```

Картинки кладите в `public/blogs-img/`. Показываются только посты с `published: true`.

## Автоматическая публикация постов

В `scripts/` лежит Python-пайплайн: забирает статьи из RSS (Habr, dev.to, CSS-Tricks), фильтрует по темам, переводит, конвертирует в Markdown и публикует в `content/blogs/`.

```bash
pip install -r scripts/requirements.txt
python scripts/main.py --config scripts/config.yaml
```

Источники, темы и лимиты настраиваются в `scripts/config.yaml`. Для тестового прогона без коммита оставьте `pipeline.dry_run: true`.

## Деплой

Каждый push в `master` запускает GitHub Actions (`.github/workflows/deploy.yml`): сборка с `--preset github_pages` и публикация `.output/public` на GitHub Pages.

## Контакты

- GitHub: [DeniMoli](https://github.com/DeniMoli)
- Telegram: [@Deni62](https://t.me/Deni62)
