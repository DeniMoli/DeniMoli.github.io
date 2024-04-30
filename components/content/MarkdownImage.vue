<script setup lang="ts">
defineProps<{
  src: string
  alt: string
}>()
</script>

<template>
  <img :src="`/blogs-content/${src}`" :alt="alt">
</template>
