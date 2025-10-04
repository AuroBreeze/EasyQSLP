<script setup lang="ts">
import { ref } from 'vue'
const query = ref('')
const results = ref<any[]>([])
function search() {
  results.value = Array.from({ length: 12 }, (_, i) => ({ id: i, name: `搜索结果 ${i + 1}` }))
}
</script>

<template>
  <div class="netflix-search">
    <div class="search-bar">
      <input v-model="query" type="text" placeholder="搜索影片、剧集、主题..." @keyup.enter="search" />
      <button @click="search">搜索</button>
    </div>
    <div v-if="results.length" class="results">
      <article v-for="item in results" :key="item.id" class="card">
        <div class="card__thumb" />
        <div class="card__info">
          <strong>{{ item.name }}</strong>
        </div>
      </article>
    </div>
  </div>
</template>

<style scoped>
.netflix-search { padding: 32px 4vw; background: var(--bg-base); min-height: 100vh; }
.search-bar { display: flex; gap: 12px; margin-bottom: 32px; }
.search-bar input { flex: 1; padding: 14px 18px; font-size: 16px; background: #2f2f2f; border: 1px solid rgba(255,255,255,0.15); color: #fff; border-radius: 4px; }
.search-bar button { padding: 14px 32px; font-size: 16px; font-weight: 600; background: #e50914; color: #fff; border: none; border-radius: 4px; cursor: pointer; transition: background 0.2s; }
.search-bar button:hover { background: #f40612; }
.results { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }
.card { border-radius: 4px; overflow: hidden; background: #2f2f2f; cursor: pointer; transition: transform 0.3s ease; }
.card:hover { transform: scale(1.05); }
.card__thumb { width: 100%; height: 135px; background: linear-gradient(135deg, #434343 0%, #000000 100%); }
.card__info { padding: 12px; }
.card__info strong { display: block; font-size: 14px; color: #e5e5e5; }
</style>
