<template>
  <div class="container">
    <header class="header">
      <h1 class="title">主界面</h1>
      <p class="subtitle">请选择你要进行的操作</p>
    </header>

    <section class="grid">
      <router-link class="card upload" to="/article/upload">
        <h2>发布文章</h2>
        <p>上传 Markdown 内容，后端自动生成安全的 HTML。</p>
      </router-link>

      <router-link class="card create" to="/project/create">
        <h2>创建项目</h2>
        <p>最小实现：只需填写项目名称（可选简介）。</p>
      </router-link>

      <div class="card view">
        <h2>查看文章</h2>
        <p>输入文章 ID 跳转到详情页</p>
        <form class="inline" @submit.prevent="goView">
          <input v-model.number="articleId" type="number" placeholder="文章ID" min="1" />
          <button type="submit" :disabled="!articleId">前往</button>
        </form>
      </div>

      <router-link class="card profile" to="/profile/1">
        <h2>个人中心</h2>
        <p>示例入口，实际请替换为真实用户 ID。</p>
      </router-link>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const articleId = ref<number | null>(null)

function goView() {
  if (articleId.value) {
    router.push(`/article/${articleId.value}`)
  }
}
</script>

<style scoped>
.container {
  max-width: 1100px;
  margin: 24px auto;
  padding: 0 16px;
}
.header { margin-bottom: 16px; }
.title { margin: 0; font-size: 28px; }
.subtitle { margin: 6px 0 0; color: #666; }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}
.card {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 16px;
  text-decoration: none;
  color: inherit;
  transition: box-shadow .2s ease, transform .2s ease;
}
.card:hover { box-shadow: 0 8px 24px rgba(0,0,0,.08); transform: translateY(-2px); }
.card h2 { margin: 0 0 8px; font-size: 20px; }
.card p { margin: 0; color: #666; }
.inline { display: flex; gap: 8px; margin-top: 12px; }
input { flex: 1; padding: 8px 10px; border: 1px solid #ddd; border-radius: 8px; }
button { padding: 8px 14px; border: none; border-radius: 8px; background: #1677ff; color: #fff; cursor: pointer; }
button[disabled] { opacity: .6; cursor: not-allowed; }
</style>
