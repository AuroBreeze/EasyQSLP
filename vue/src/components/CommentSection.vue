<script setup lang="ts">
import CommentCard from './CommentCard.vue'

defineProps<{
  articleId?: string
  comments?: any[]
}>()

// 模拟评论数据
const mockComments = [
  {
    id: '1',
    content: '这篇文章写得非常详细，Vue 3 的组件化思路讲解得很清楚，特别是 Composition API 的部分让我受益匪浅。作者的代码示例也很实用，直接可以应用到项目中。',
    rating: 4 as const,
    user: {
      name: '前端小白',
      avatar: ''
    },
    updatedAt: '2天前',
    participants: [
      { name: 'Vue大师', avatar: '' },
      { name: '代码小白', avatar: '' },
      { name: '学习者A', avatar: '' },
      { name: '开发者B', avatar: '' },
      { name: '前端爱好者', avatar: '' },
      { name: '技术宅', avatar: '' },
      { name: '程序猿', avatar: '' }
    ]
  },
  {
    id: '2', 
    content: '内容还行，但是感觉有些地方讲得不够深入，希望能补充更多实战案例。',
    rating: 3 as const,
    user: {
      name: 'CodeMaster',
      avatar: ''
    },
    updatedAt: '1周前',
    participants: [
      { name: '实战派', avatar: '' },
      { name: '案例分析师', avatar: '' },
      { name: '深度学习者', avatar: '' }
    ]
  },
  {
    id: '3',
    content: '看完了，感觉一般般，没有想象中那么有用。可能是我期望太高了吧。',
    rating: 2 as const,
    user: {
      name: '学习者',
      avatar: ''
    },
    updatedAt: '3天前'
  },
  {
    id: '4',
    content: '这种基础内容网上到处都有，没什么新意，浪费时间。',
    rating: 1 as const,
    user: {
      name: '资深开发',
      avatar: ''
    },
    updatedAt: '5天前'
  }
]
</script>

<template>
  <div class="comment-section">
    <header class="comment__header">
      <h3 class="comment__title">评论区</h3>
      <div class="comment__stats">
        <span class="stats-item">{{ mockComments.length }} 条评论</span>
        <span class="stats-item">平均评分 3.2/4.0</span>
      </div>
    </header>
    
    <div class="comment__content">
      <!-- 评论列表 -->
      <div class="comment-list">
        <CommentCard 
          v-for="comment in mockComments" 
          :key="comment.id" 
          :comment="comment" 
        />
      </div>
      
      <!-- 发表评论 -->
      <div class="comment-form">
        <h4 class="form-title">发表评论</h4>
        <textarea 
          class="comment-input" 
          placeholder="写下你的想法..."
          rows="3"
        ></textarea>
        <div class="form-actions">
          <div class="rating-selector">
            <span class="selector-label">评分：</span>
            <button class="rating-btn" data-rating="1">😞 不满意</button>
            <button class="rating-btn" data-rating="2">😐 平庸</button>
            <button class="rating-btn" data-rating="3">😊 还可以</button>
            <button class="rating-btn active" data-rating="4">🤩 棒极了</button>
          </div>
          <button class="submit-btn">发布评论</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.comment-section {
  background: #2f2f2f;
  border-radius: 8px;
  padding: 24px;
  min-height: 400px;
}

/* 标题区域 */
.comment__header {
  display: flex;
  justify-content: between;
  align-items: flex-start;
  margin-bottom: 24px;
  gap: 16px;
}
.comment__title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #e5e5e5;
  flex: 1;
}
.comment__stats {
  display: flex;
  flex-direction: column;
  gap: 4px;
  text-align: right;
}
.stats-item {
  font-size: 12px;
  color: rgba(255,255,255,0.6);
}

/* 评论列表 */
.comment-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

/* 发表评论表单 */
.comment-form {
  border-top: 1px solid rgba(255,255,255,0.1);
  padding-top: 24px;
}
.form-title {
  margin: 0 0 16px;
  font-size: 16px;
  font-weight: 600;
  color: #e5e5e5;
}
.comment-input {
  width: 100%;
  padding: 12px 16px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 6px;
  color: rgba(255,255,255,0.9);
  font-size: 14px;
  line-height: 1.5;
  resize: vertical;
  margin-bottom: 16px;
}
.comment-input:focus {
  outline: none;
  border-color: #e50914;
  background: rgba(255,255,255,0.08);
}
.comment-input::placeholder {
  color: rgba(255,255,255,0.4);
}

/* 表单操作区 */
.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}
.rating-selector {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.selector-label {
  font-size: 14px;
  color: rgba(255,255,255,0.7);
  margin-right: 4px;
}
.rating-btn {
  padding: 6px 12px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 20px;
  color: rgba(255,255,255,0.7);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.rating-btn:hover {
  background: rgba(255,255,255,0.12);
  border-color: rgba(255,255,255,0.25);
}
.rating-btn.active {
  background: rgba(42, 213, 115, 0.2);
  border-color: #2ed573;
  color: #2ed573;
}
.submit-btn {
  padding: 10px 24px;
  background: #e50914;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.submit-btn:hover {
  background: #f40612;
  transform: translateY(-1px);
}

/* 响应式 */
@media (max-width: 768px) {
  .comment__header {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  .comment__stats {
    text-align: left;
  }
  .form-actions {
    flex-direction: column;
    align-items: stretch;
  }
  .rating-selector {
    justify-content: center;
  }
}
</style>
