<template>
  <section class="panel">
    <h3 class="panel-title">🕒 近期动态</h3>
    <ul class="list">
      <li v-for="it in items" :key="it.id">
        <a :href="it.link" target="_blank" rel="noopener" class="link">{{ it.title }}</a>
        <span class="time">{{ it.time }}</span>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import type { ActivityItem } from '@/utils/home/homeService'
const props = defineProps<{ items: ActivityItem[] }>()
</script>

<style scoped>
.panel { background: #fff; border: 1px solid #eee; border-radius: 12px; padding: 12px; }
.panel-title { margin: 0 0 8px; font-size: 16px; }
.list { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
.link { color: #2563eb; text-decoration: none; }
.time { color: #888; font-size: 12px; margin-left: 6px; }
</style>
