<template>
  <div class="page">
    <header class="header">
      <h1 class="title">{{ article?.title || '文章详情' }}</h1>
      <div class="header-actions">
        <router-link to="/article/upload" class="link">发布新文章</router-link>
      </div>
    </header>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else-if="article" class="content-wrap">
      <aside class="toc" v-if="article.toc" v-html="article.toc"></aside>
      <article class="content" v-html="article.content_html"></article>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getArticle, type ArticleResponse } from '@/utils/ProjectManage/articleService'

const route = useRoute()
const article = ref<ArticleResponse | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  loading.value = true
  error.value = ''
  const idParam = route.params.id
  const id = Number(idParam)
  if (!id || Number.isNaN(id)) {
    error.value = '无效的文章ID'
    loading.value = false
    return
  }
  try {
    const res: ArticleResponse = await getArticle(id)
    article.value = res
  } catch (e: any) {
    error.value = e?.message || '加载失败'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page {
  max-width: 1100px;
  margin: 24px auto;
  padding: 0 16px;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.title { font-size: 24px; margin: 0; }
.header-actions .link { color: #1677ff; text-decoration: none; }
.loading { color: #666; }
.error { color: #d93025; }
.content-wrap { display: grid; grid-template-columns: 280px 1fr; gap: 24px; }
.toc { position: sticky; top: 12px; max-height: calc(100vh - 120px); overflow: auto; padding-right: 8px; }
.content :deep(pre) { background: #0e1117; color: #c9d1d9; padding: 12px; border-radius: 8px; overflow: auto; }
.content :deep(code) { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; }
.content :deep(img) { max-width: 100%; }
</style>
