<template>
  <div class="diff-page">
    <h2>修订差异</h2>
    <div class="toolbar">
      <router-link class="btn" :to="{ name: 'article-history', params: { id: articleId } }">返回历史</router-link>
      <select v-model="against" @change="load">
        <option value="prev">与上一个修订</option>
        <option value="current">与当前文章</option>
      </select>
      <select v-model="mode" @change="load">
        <option value="unified">统一 diff</option>
        <option value="html">HTML diff</option>
        <option value="dmp">DMP</option>
      </select>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else>
      <pre v-if="diff?.type === 'unified'" class="unified">{{ diff.patch }}</pre>
      <div v-else-if="diff?.type === 'html'" class="html" v-html="diff.html"></div>
      <pre v-else class="unified">{{ diff?.patch || '无差异数据' }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { getRevision, getRevisionDiff } from '@/utils/ProjectManage/revisionService'

const route = useRoute()
const revId = computed(() => Number(route.params.id))
const articleId = ref<number | null>(null)

const against = ref<'prev' | 'current'>('prev')
const mode = ref<'unified' | 'html' | 'dmp'>('unified')
const loading = ref(false)
const diff = ref<any>(null)

async function load() {
  if (!revId.value) return
  loading.value = true
  try {
    const { data: rev } = await getRevision(revId.value)
    articleId.value = rev.article
    const { data } = await getRevisionDiff(revId.value, { against: against.value, mode: mode.value })
    diff.value = data.diff
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.diff-page { padding: 16px; }
.toolbar { display: flex; gap: 8px; align-items: center; margin-bottom: 12px; }
.btn { padding: 6px 12px; border: 1px solid #2563eb; color: #2563eb; background: transparent; border-radius: 6px; text-decoration: none; }
.unified { background: #0b1021; color: #e5e7eb; padding: 12px; border-radius: 6px; overflow: auto; }
.html :deep(table) { width: 100%; border-collapse: collapse; }
.html :deep(td), .html :deep(th) { border: 1px solid #e5e7eb; padding: 4px; font-size: 12px; }
</style>
