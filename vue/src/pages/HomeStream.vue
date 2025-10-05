<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ContentRow from '@/components/ContentRow.vue'
import { apiGetHistory, apiGetRecommendations } from '@/services/api'

const router = useRouter()

const loading = ref(true)
const historyItems = ref<any[]>([])
const recommendItems = ref<any[]>([])

onMounted(async () => {
  loading.value = true
  const [h, r] = await Promise.all([apiGetHistory(), apiGetRecommendations()])
  if (h.ok) historyItems.value = h.data.map(mapToCard)
  if (r.ok) recommendItems.value = r.data.map(mapToCard)
  loading.value = false
})

function mapToCard(x: any) {
  return {
    id: x.id,
    title: x.title,
    subtitle: x.subtitle,
    poster: x.poster,
    rating: x.difficulty ?? x.readingTime,
    year: x.updated,
  }
}

function toTopic(id: string) {
  router.push({ name: 'topic-detail', params: { id } })
}
</script>

<template>
  <section class="home">
    <header class="home-header">
      <h1>你的首页</h1>
      <p class="desc">上次浏览的专题与为你推荐</p>
    </header>

    <div class="rows">
      <section class="row-wrap">
        <ContentRow title="历史记录" :items="historyItems" />
        <div class="inline-grid">
          <button v-for="item in historyItems" :key="item.id" class="ghost-link" @click="toTopic(item.id)">继续 {{ item.title }}</button>
        </div>
      </section>

      <section class="row-wrap">
        <ContentRow title="为你推荐" :items="recommendItems" />
        <div class="inline-grid">
          <button v-for="item in recommendItems" :key="item.id" class="ghost-link" @click="toTopic(item.id)">查看 {{ item.title }}</button>
        </div>
      </section>

      <div v-if="loading" class="loading">加载中…</div>
    </div>
  </section>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-right: clamp(16px, 3vw, 24px);
}

.home-header h1 {
  margin: 0 0 6px;
  color: #fff;
  font-size: 28px;
}

.home-header .desc {
  margin: 0;
  color: rgba(255,255,255,0.7);
  font-size: 14px;
}

.rows {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.inline-grid {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 8px;
}

.ghost-link {
  background: transparent;
  color: rgba(255,255,255,0.7);
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 0;
  padding: 6px 10px;
  font-size: 12px;
  cursor: pointer;
}

.ghost-link:hover {
  color: #fff;
  border-color: rgba(255,255,255,0.3);
}

.loading {
  color: rgba(255,255,255,0.7);
  font-size: 12px;
}
</style>
