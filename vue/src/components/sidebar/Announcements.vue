<template>
  <section class="panel">
    <h3 class="panel-title">📢 平台公告</h3>
    <ul class="list">
      <li v-for="a in items" :key="a.id">
        <div class="title">{{ a.title }}</div>
        <div class="time">{{ a.time }}</div>
        <div class="content">{{ a.content }}</div>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import type { Announcement } from '@/utils/home/homeService'
const props = defineProps<{ items: Announcement[] }>()
</script>

<style scoped>
.panel { background: #fff; border: 1px solid #eee; border-radius: 12px; padding: 12px; }
.panel-title { margin: 0 0 8px; font-size: 16px; }
.list { list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; }
.title { font-weight: 600; }
.time { color: #888; font-size: 12px; }
.content { color: #444; }
</style>
