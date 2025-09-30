<template>
  <header class="navbar">
    <div class="brand" @click="$router.push('/main')">EasyQSLP</div>
    <form class="search" @submit.prevent="doSearch">
      <input v-model="keyword" type="search" placeholder="搜索项目/文章" />
      <button type="submit">搜索</button>
    </form>
    <div class="actions">
      <button class="primary" @click="$emit('createProject')">发布项目</button>
      <router-link to="/login" class="link">登录</router-link>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const keyword = ref('')

function doSearch() {
  const kw = keyword.value.trim()
  if (kw) {
    // 让上层监听该事件或采用路由方式
    // 此处采用事件上抛，MainView 接收后触发刷新
    emit('search', kw)
  }
}

const emit = defineEmits<{ (e: 'search', keyword: string): void; (e: 'createProject'): void }>()
</script>

<style scoped>
.navbar { display: flex; align-items: center; gap: 16px; padding: 12px 16px; border-bottom: 1px solid #eee; }
.brand { font-weight: 700; cursor: pointer; }
.search { display: flex; gap: 8px; flex: 1; }
.search input { flex: 1; padding: 8px 10px; border: 1px solid #ddd; border-radius: 8px; }
.search button { padding: 8px 12px; border: none; border-radius: 8px; background: #2563eb; color: #fff; cursor: pointer; }
.actions { display: flex; gap: 12px; align-items: center; }
.actions .primary { padding: 8px 12px; border: none; border-radius: 8px; background: #2563eb; color: #fff; cursor: pointer; }
.actions .link { text-decoration: none; color: #2563eb; }
</style>
