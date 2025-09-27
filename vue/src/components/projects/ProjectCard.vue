<template>
  <div class="card" @click="$emit('open')">
    <div class="cover" v-if="project.cover_image">
      <img :src="project.cover_image" alt="cover" />
    </div>
    <div class="body">
      <h3 class="title">{{ project.title }}</h3>
      <p class="intro" v-if="project.introduction">{{ project.introduction }}</p>
      <div class="meta">
        <span>👍 {{ project.likes_count ?? 0 }}</span>
        <span>⭐ {{ project.stars_count ?? 0 }}</span>
        <span>👁️ {{ project.views ?? 0 }}</span>
      </div>
      <div class="tags" v-if="project.tags?.length">
        <span v-for="(t, i) in project.tags" :key="i" class="tag">{{ t }}</span>
      </div>
    </div>
    <div class="ops" @click.stop>
      <button class="link" @click="$emit('like')">点赞</button>
      <button class="link" @click="$emit('star')">收藏</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ProjectLite } from '@/utils/home/homeService'

const props = defineProps<{ project: ProjectLite }>()
const emit = defineEmits<{ (e: 'like'): void; (e: 'star'): void; (e: 'open'): void }>()
</script>

<style scoped>
.card { background: #fff; border: 1px solid #eee; border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; }
.cover img { width: 100%; height: 160px; object-fit: cover; display: block; }
.body { padding: 12px; }
.title { margin: 0 0 6px; font-size: 16px; }
.intro { margin: 0 0 8px; color: #666; font-size: 13px; }
.meta { display: flex; gap: 12px; color: #888; font-size: 12px; }
.tags { margin-top: 8px; display: flex; flex-wrap: wrap; gap: 6px; }
.tag { background: #f3f4f6; color: #374151; padding: 2px 6px; border-radius: 999px; font-size: 12px; }
.ops { display: flex; gap: 8px; padding: 8px 12px; border-top: 1px solid #eee; }
.link { border: none; background: transparent; color: #2563eb; cursor: pointer; }
</style>
