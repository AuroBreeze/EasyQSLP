<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  title?: string
  author?: string
  description?: string
  tags?: string[]
  prerequisites?: Array<{id: string, title: string}>
  stats?: {
    views?: number
    likes?: number
    duration?: string
  }
}>()

const activeTab = ref('intro')
const tabs = [
  { id: 'intro', label: '简介' },
  { id: 'prerequisites', label: '前置' },
  { id: 'tags', label: '标签' }
]

// 模拟数据
const mockTags = ['Vue.js', '前端开发', '组件化', 'TypeScript', 'JavaScript']
const mockPrerequisites = [
  { id: '1', title: 'JavaScript 基础语法入门' },
  { id: '2', title: 'HTML/CSS 核心概念' },
  { id: '3', title: 'ES6+ 新特性详解' }
]

const showAddTag = ref(false)

function addNewTag() {
  showAddTag.value = true
}
</script>

<template>
  <div class="article-intro">
    <!-- Tab 导航 -->
    <nav class="intro__tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-btn', { 'tab-btn--active': activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        {{ tab.label }}
      </button>
    </nav>

    <!-- Tab 内容 -->
    <div class="intro__content">
      <!-- 简介 -->
      <div v-if="activeTab === 'intro'" class="tab-panel">
        <p class="intro__desc">
          深入学习 Vue 3 的组件化开发模式，包含最佳实践和实战案例。本文将带你从零开始构建现代化的 Vue 应用，掌握组件设计思路和开发技巧。
        </p>
        <div class="intro__stats">
          <div class="stat-item">
            <span class="stat-label">阅读量</span>
            <span class="stat-value">1,250</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">点赞数</span>
            <span class="stat-value">89</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">预计时长</span>
            <span class="stat-value">15分钟</span>
          </div>
        </div>
      </div>

      <!-- 前置 -->
      <div v-if="activeTab === 'prerequisites'" class="tab-panel">
        <p class="panel-desc">作者建议先阅读以下文章：</p>
        <ul class="prereq-list">
          <li v-for="item in mockPrerequisites" :key="item.id" class="prereq-item">
            <a href="#" class="prereq-link">{{ item.title }}</a>
          </li>
        </ul>
      </div>

      <!-- 标签 -->
      <div v-if="activeTab === 'tags'" class="tab-panel">
        <div class="tags-container">
          <span 
            v-for="(tag, index) in mockTags" 
            :key="tag"
            :class="['tag-bubble', `tag-color-${index % 6}`]"
          >
            {{ tag }}
          </span>
          <button class="add-tag-btn" @click="addNewTag" :class="{ active: showAddTag }">
            <span class="add-icon">+</span>
          </button>
        </div>
        <p class="tags-hint">点击 + 号添加新标签</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.article-intro {
  background: #2f2f2f;
  border-radius: 8px;
  padding: 0;
  height: fit-content;
  overflow: hidden;
}

/* Tab 导航 */
.intro__tabs {
  display: flex;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
.tab-btn {
  flex: 1;
  padding: 16px 20px;
  background: transparent;
  border: none;
  color: rgba(255,255,255,0.6);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}
.tab-btn:hover {
  color: rgba(255,255,255,0.8);
  background: rgba(255,255,255,0.05);
}
.tab-btn--active {
  color: #e5e5e5;
  background: rgba(229, 9, 20, 0.1);
}
.tab-btn--active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: #e50914;
}

/* Tab 内容 */
.intro__content {
  padding: 24px;
}
.tab-panel {
  color: rgba(255,255,255,0.85);
  line-height: 1.6;
}

/* 简介面板 */
.intro__desc {
  margin: 0 0 24px;
  font-size: 14px;
}
.intro__stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.stat-item {
  text-align: center;
  padding: 12px;
  background: rgba(255,255,255,0.05);
  border-radius: 6px;
}
.stat-label {
  display: block;
  font-size: 12px;
  color: rgba(255,255,255,0.6);
  margin-bottom: 4px;
}
.stat-value {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #e5e5e5;
}

/* 前置面板 */
.panel-desc {
  margin: 0 0 16px;
  font-size: 14px;
  color: rgba(255,255,255,0.7);
}
.prereq-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.prereq-item {
  margin-bottom: 12px;
}
.prereq-link {
  color: #e50914;
  text-decoration: none;
  font-size: 14px;
  padding: 8px 12px;
  display: block;
  border-radius: 4px;
  border: 1px solid rgba(229, 9, 20, 0.3);
  transition: all 0.2s ease;
}
.prereq-link:hover {
  background: rgba(229, 9, 20, 0.1);
  border-color: rgba(229, 9, 20, 0.5);
}

/* 标签面板 */
.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}
.tag-bubble {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  color: #fff;
}
.tag-color-0 { background: linear-gradient(135deg, #667eea, #764ba2); }
.tag-color-1 { background: linear-gradient(135deg, #f093fb, #f5576c); }
.tag-color-2 { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.tag-color-3 { background: linear-gradient(135deg, #43e97b, #38f9d7); }
.tag-color-4 { background: linear-gradient(135deg, #fa709a, #fee140); }
.tag-color-5 { background: linear-gradient(135deg, #a8edea, #fed6e3); }

.add-tag-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px dashed rgba(255,255,255,0.4);
  background: transparent;
  color: rgba(255,255,255,0.6);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}
.add-tag-btn:hover, .add-tag-btn.active {
  border-color: #e50914;
  color: #e50914;
  background: rgba(229, 9, 20, 0.1);
}
.add-icon {
  font-size: 16px;
  font-weight: bold;
}
.tags-hint {
  margin: 0;
  font-size: 12px;
  color: rgba(255,255,255,0.5);
  text-align: center;
}
</style>
