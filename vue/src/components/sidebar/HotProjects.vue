<template>
  <section class="panel">
    <h3 class="panel-title">🔥 热门项目</h3>
    <ul class="list">
      <li v-for="p in projects" :key="p.id" @click="$emit('open', p.id)">
        <div class="title">{{ p.title }}</div>
        <div class="stats">👍 {{ p.likes_count ?? 0 }} · ⭐ {{ p.stars_count ?? 0 }}</div>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import type { ProjectLite } from '@/utils/home/homeService'
const props = defineProps<{ projects: ProjectLite[] }>()
const emit = defineEmits<{ (e: 'open', id: number): void }>()
</script>

<style scoped>
.panel { background: #fff; border: 1px solid #eee; border-radius: 12px; padding: 12px; }
.panel-title { margin: 0 0 8px; font-size: 16px; }
.list { list-style: none; margin: 0; padding: 0; }
.list li { padding: 8px 6px; border-radius: 8px; cursor: pointer; }
.list li:hover { background: #f9fafb; }
.title { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.stats { color: #888; font-size: 12px; }
</style>
