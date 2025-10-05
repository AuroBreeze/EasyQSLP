<script setup lang="ts">
const categories = [
  { title: '热门系列', items: Array.from({ length: 8 }, (_, i) => ({ id: i, name: `系列 ${i + 1}` })) },
  { title: '悬疑推理', items: Array.from({ length: 8 }, (_, i) => ({ id: i + 10, name: `悬疑 ${i + 1}` })) },
  { title: '科幻奇幻', items: Array.from({ length: 8 }, (_, i) => ({ id: i + 20, name: `科幻 ${i + 1}` })) },
]
</script>

<template>
  <div class="netflix-series">
    <h1 class="page-title">系列</h1>
    <section v-for="cat in categories" :key="cat.title" class="row">
      <h2 class="row__title">{{ cat.title }}</h2>
      <div class="row__cards">
        <article v-for="item in cat.items" :key="item.id" class="card">
          <div class="card__thumb" />
          <div class="card__info"><strong>{{ item.name }}</strong></div>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.netflix-series { padding: 32px 4vw; background: var(--bg-base); min-height: 100vh; }
.page-title { margin: 0 0 32px; font-size: 32px; font-weight: 700; color: #e5e5e5; }
.row { padding-bottom: 32px; }
.row__title { margin: 0 0 12px; font-size: 20px; font-weight: 600; color: #e5e5e5; }
.row__cards { display: flex; gap: 8px; overflow-x: auto; scroll-behavior: smooth; padding-bottom: 8px; }
.row__cards::-webkit-scrollbar { height: 6px; }
.row__cards::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
.row__cards::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 3px; }
.card { flex: 0 0 auto; width: 280px; border-radius: 4px; overflow: hidden; background: #2f2f2f; cursor: pointer; transition: transform 0.3s ease; }
.card:hover { transform: scale(1.08); }
.card__thumb { width: 100%; height: 158px; background: linear-gradient(135deg, #434343 0%, #000000 100%); }
.card__info { padding: 12px; }
.card__info strong { display: block; font-size: 14px; color: #e5e5e5; }
</style>
