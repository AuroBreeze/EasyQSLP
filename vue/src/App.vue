<template>
  <div :class="['layout', { 'layout--full': hideSideNav }]">
    <SideNav v-if="!hideSideNav" />
    <main class="content">
      <router-view />
    </main>
  </div>
  </template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import SideNav from './components/SideNav.vue'

const route = useRoute()
const hideSideNav = computed(() => route.name === 'workspace')
</script>

<style scoped>
.layout {
  min-height: 100vh;
  width: 100vw;
  padding: 0;
  box-sizing: border-box;
}

/* 移除空的CSS规则集，通过子元素样式处理工作区布局 */

.content {
  margin-left: 72px; /* 为固定侧边栏预留空间 */
  min-height: 100vh;
}

.layout--full .content {
  margin-left: 0; /* 工作区时取消左边距 */
}

@media (max-width: 1024px) {
  .content {
    margin-left: 64px;
  }
}

@media (max-width: 768px) {
  .content {
    margin-left: 56px;
  }
}
</style>
