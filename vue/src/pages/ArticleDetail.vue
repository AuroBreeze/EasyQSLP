<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import ArticleIntro from '@/components/ArticleIntro.vue'
import CommentSection from '@/components/CommentSection.vue'

const route = useRoute()
const articleId = route.params.id as string

// 模拟数据
const article = ref({
  id: articleId,
  title: 'Vue 3 组件化开发实战',
  author: 'TechMaster',
  authorAvatar: '',
  cover: '/src/assets/post.webp',
  lastUpdate: '2024-01-15',
  readTime: '15分钟',
  description: '深入学习 Vue 3 的组件化开发模式，包含最佳实践和实战案例。',
  tags: ['Vue.js', '前端', '组件化'],
  stats: {
    views: 1250,
    likes: 89,
    duration: '15分钟'
  }
})
</script>

<template>
  <div class="article-detail">
    <!-- 顶部区域 -->
    <header class="article-header">
      <div class="header__cover">
        <img :src="article.cover" :alt="article.title" />
        <div class="cover__overlay">
          <h1 class="article__title">{{ article.title }}</h1>
        </div>
      </div>
      <div class="header__meta">
        <span class="meta__author">显示（由{{ article.author }}创作）</span>
        <div class="meta__avatar">
          <div class="avatar__circle">作者头像</div>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="article-main">
      <div class="main__content">
        <!-- 操作栏 -->
        <div class="action-bar">
          <button class="btn btn--primary">开始阅读</button>
          <div class="action-meta">
            <div class="meta-group">
              <div class="meta-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <polyline points="8,12 12,8 16,12"/>
                  <line x1="12" y1="8" x2="12" y2="16"/>
                </svg>
              </div>
              <div class="meta-content">
                <span class="meta-label">最后一次更新</span>
                <span class="meta-value">{{ article.lastUpdate }}</span>
              </div>
            </div>
            <div class="meta-group">
              <div class="meta-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12,6 12,12 16,14"/>
                </svg>
              </div>
              <div class="meta-content">
                <span class="meta-label">预计阅读时间</span>
                <span class="meta-value">{{ article.readTime }}</span>
              </div>
            </div>
          </div>
          <div class="action-buttons">
            <button class="btn btn--outline">精版</button>
            <button class="btn btn--outline">章节</button>
          </div>
        </div>

        <!-- 评论区 -->
        <CommentSection :article-id="articleId" />
      </div>

      <!-- 右侧简介 -->
      <aside class="main__sidebar">
        <ArticleIntro 
          :title="article.title"
          :author="article.author"
          :description="article.description"
          :tags="article.tags"
          :stats="article.stats"
        />
      </aside>
    </main>
  </div>
</template>

<style scoped>
.article-detail {
  min-height: 100vh;
  background: var(--bg-base);
  padding: 0;
}

/* 顶部区域 */
.article-header {
  position: relative;
  margin-bottom: 48px;
}
.header__cover {
  position: relative;
  height: 400px;
  overflow: hidden;
}
.header__cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.cover__overlay {
  position: absolute;
  inset: 0;
  /* 使用全局主题变量统一过渡，降低色阶断层 */
  background:
    /* 左下角辐射：与主题色一致 */
    radial-gradient(120% 120% at 0% 100%, rgba(var(--surface-rgb), 1) 0%, rgba(var(--surface-rgb), 0) 60%),
    /* 底部向上：以主题色渐隐，过渡更平滑 */
    linear-gradient(
      to top,
      rgba(var(--surface-rgb), 1) 0%,
      rgba(var(--surface-rgb), 0.16) 55%,
      rgba(var(--surface-rgb), 0.00) 68%
    ),
    /* 左侧向右：非线性多段过渡，配合主题变量，避免与主体背景产生断层 */
    linear-gradient(
      to right,
      rgba(var(--surface-rgb), 1.00) 0%,
      rgba(var(--surface-rgb), 0.96) 14%,
      rgba(var(--surface-rgb), 0.90) 26%,
      rgba(var(--surface-rgb), 0.78) 38%,
      rgba(var(--surface-rgb), 0.62) 50%,
      rgba(var(--surface-rgb), 0.40) 65%,
      rgba(var(--surface-rgb), 0.22) 80%,
      rgba(var(--surface-rgb), 0.10) 90%,
      rgba(var(--surface-rgb), 0.00) 100%
    );
  display: flex;
  align-items: flex-end;
  padding: 40px 2vw;
}
.article__title {
  margin: 0;
  font-size: clamp(28px, 5vw, 56px);
  font-weight: 700;
  color: #fff;
  text-shadow: 0 2px 8px rgba(0,0,0,0.5);
}
.header__meta {
  position: absolute;
  top: 24px;
  right: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(10px);
  padding: 12px 16px;
  border-radius: 50px;
  border: 1px solid rgba(255,255,255,0.1);
}
.meta__author {
  color: rgba(255,255,255,0.95);
  font-size: 13px;
  font-weight: 500;
}
.meta__avatar {
  width: 40px;
  height: 40px;
}
.avatar__circle {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #e50914;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  border: 2px solid rgba(255,255,255,0.3);
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

/* 主要内容 */
.article-main {
  display: grid;
  grid-template-columns: 1fr 520px;
  gap: 24px;
  padding: 0 1vw 48px;
  max-width: none;
  margin: 0;
}

/* 操作栏 */
.action-bar {
  background: #2f2f2f;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}
.action-meta {
  display: grid;
  grid-template-columns: 0.5fr 1fr;
  flex: 1;
}
.meta-group {
  display: flex;
  align-items: center;
  gap: 12px;
}
.meta-icon {
  width: 35px;
  height: 35px;
  color: rgba(255,255,255,0.6);
  flex-shrink: 0;
}
.meta-icon svg {
  width: 100%;
  height: 100%;
}
.meta-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.meta-label {
  font-size: 12px;
  color: rgba(255,255,255,0.6);
  font-weight: 500;
}
.meta-value {
  font-size: 20px;
  color: rgba(255,255,255,0.9);
  font-weight: 700;
}
.action-buttons {
  display: flex;
  gap: 12px;
}

/* 按钮 */
.btn {
  padding: 10px 35px;
  font-size: 20px;
  font-weight: 700;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn--primary {
  background: #e50914;
  color: #fff;
  min-width: 140px;
}
.btn--primary:hover {
  background: #f40612;
  transform: translateY(-1px);
}
.btn--outline {
  background: transparent;
  color: rgba(255,255,255,0.8);
  border: 1px solid rgba(255,255,255,0.3);
}
.btn--outline:hover {
  background: rgba(255,255,255,0.1);
  border-color: rgba(255,255,255,0.5);
}

/* 响应式 */
@media (max-width: 1200px) {
  .article-main {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 0 2vw 48px;
  }
}
@media (max-width: 768px) {
  .cover__overlay {
    padding: 32px 4vw;
  }
  .header__meta {
    top: 16px;
    right: 16px;
    padding: 10px 12px;
  }
  .action-bar {
    flex-direction: column;
    align-items: stretch;
  }
  .action-meta {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  .action-buttons {
    justify-content: center;
  }
  .article-main {
    padding: 0 4vw 48px;
  }
}
</style>
