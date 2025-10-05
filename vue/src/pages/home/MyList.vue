<script setup lang="ts">
const myList = Array.from({ length: 12 }, (_, i) => ({ id: i, name: `我的收藏 ${i + 1}` }))
</script>

<template>
  <div class="netflix-list">
    <h1 class="page-title">我的列表</h1>
    <div class="grid">
      <article v-for="item in myList" :key="item.id" class="card">
        <div class="card__thumb" />
        <div class="card__info"><strong>{{ item.name }}</strong></div>
      </article>
    </div>
  </div>
</template>

<style scoped>
.netflix-list { padding: 32px 4vw; background: var(--bg-base); min-height: 100vh; }
.page-title { margin: 0 0 32px; font-size: 32px; font-weight: 700; color: #e5e5e5; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }
.card { border-radius: 4px; overflow: hidden; background: #2f2f2f; cursor: pointer; transition: transform 0.3s ease; }
.card:hover { transform: scale(1.05); }
.card__thumb { width: 100%; height: 135px; background: linear-gradient(135deg, #434343 0%, #000000 100%); }
.card__info { padding: 12px; }
.card__info strong { display: block; font-size: 14px; color: #e5e5e5; }
</style>
