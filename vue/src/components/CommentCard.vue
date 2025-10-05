<script setup lang="ts">
defineProps<{
  comment: {
    id: string
    content: string
    rating: 1 | 2 | 3 | 4 // 1:不满意, 2:平庸, 3:还可以, 4:棒极了
    user: {
      name: string
      avatar?: string
    }
    updatedAt: string
    participants?: Array<{
      name: string
      avatar?: string
    }>
  }
}>()

// 表情配置
const ratingConfig = {
  1: { emoji: '😞', color: '#ff4757', label: '不满意' },
  2: { emoji: '😐', color: '#ffa502', label: '平庸' },
  3: { emoji: '😊', color: '#ff9f43', label: '还可以' },
  4: { emoji: '🤩', color: '#2ed573', label: '棒极了' }
}
</script>

<template>
  <article class="comment-card">
    <!-- 上方：表情 + 评论内容 -->
    <div class="comment-main">
      <div class="comment-rating" :style="{ '--rating-color': ratingConfig[comment.rating].color }">
        <span class="rating-emoji">{{ ratingConfig[comment.rating].emoji }}</span>
        <span class="rating-label">{{ ratingConfig[comment.rating].label }}</span>
      </div>
      <div class="comment-content">
        <p>{{ comment.content }}</p>
      </div>
    </div>

    <!-- 下方：用户信息 -->
    <footer class="comment-footer">
      <div class="user-info">
        <div class="user-avatar">
          <img v-if="comment.user.avatar" :src="comment.user.avatar" :alt="comment.user.name" />
          <span v-else class="avatar-placeholder">{{ comment.user.name.charAt(0).toUpperCase() }}</span>
        </div>
        <div class="user-details">
          <span class="user-name">{{ comment.user.name }}</span>
          <time class="update-time">{{ comment.updatedAt }}</time>
        </div>
      </div>
      
      <!-- 参与讨论的用户 -->
      <div v-if="comment.participants && comment.participants.length > 0" class="participants">
        <div class="participant-avatars">
          <div 
            v-for="(participant, index) in comment.participants.slice(0, 5)" 
            :key="participant.name"
            class="participant-avatar"
            :style="{ zIndex: 5 - index }"
          >
            <img v-if="participant.avatar" :src="participant.avatar" :alt="participant.name" />
            <span v-else class="avatar-placeholder">{{ participant.name.charAt(0).toUpperCase() }}</span>
          </div>
          <div v-if="comment.participants.length > 5" class="more-count">
            +{{ comment.participants.length - 5 }}
          </div>
        </div>
        <span class="participants-text">{{ comment.participants.length }}+ 参与了讨论</span>
      </div>
    </footer>
  </article>
</template>

<style scoped>
.comment-card {
  background: rgba(255,255,255,0.03);
  border-radius: 8px;
  padding: 20px;
  border: 1px solid rgba(255,255,255,0.08);
  transition: all 0.2s ease;
}
.comment-card:hover {
  background: rgba(255,255,255,0.05);
  border-color: rgba(255,255,255,0.12);
}

/* 上方主要内容 */
.comment-main {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

/* 表情评分区域 */
.comment-rating {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  min-width: 70px;
  padding: 8px;
  background: rgba(var(--rating-color, 255, 255, 255), 0.1);
  border-radius: 8px;
  border: 1px solid rgba(var(--rating-color, 255, 255, 255), 0.2);
}
.rating-emoji {
  font-size: 24px;
  line-height: 1;
}
.rating-label {
  font-size: 11px;
  font-weight: 600;
  color: rgb(var(--rating-color, 255, 255, 255));
  text-align: center;
  white-space: nowrap;
}

/* 评论内容 */
.comment-content {
  flex: 1;
  padding-top: 4px;
}
.comment-content p {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: rgba(255,255,255,0.9);
}

/* 下方用户信息 */
.comment-footer {
  border-top: 1px solid rgba(255,255,255,0.06);
  padding-top: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}
.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  background: #2f2f2f;
  display: flex;
  align-items: center;
  justify-content: center;
}
.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.avatar-placeholder {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255,255,255,0.8);
}
.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.user-name {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255,255,255,0.9);
}
.update-time {
  font-size: 11px;
  color: rgba(255,255,255,0.5);
}

/* 参与讨论用户 */
.participants {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}
.participant-avatars {
  display: flex;
  align-items: center;
}
.participant-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  overflow: hidden;
  background: #2f2f2f;
  border: 2px solid rgba(255,255,255,0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: -8px;
  transition: transform 0.2s ease;
}
.participant-avatar:first-child {
  margin-left: 0;
}
.participant-avatar:hover {
  transform: scale(1.1);
  border-color: rgba(255,255,255,0.3);
}
.participant-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.participant-avatar .avatar-placeholder {
  font-size: 10px;
  font-weight: 600;
  color: rgba(255,255,255,0.8);
}
.more-count {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  border: 2px solid rgba(255,255,255,0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 600;
  color: rgba(255,255,255,0.7);
  margin-left: -8px;
}
.participants-text {
  font-size: 11px;
  color: rgba(255,255,255,0.5);
  white-space: nowrap;
}

/* 响应式 */
@media (max-width: 768px) {
  .comment-main {
    gap: 12px;
  }
  .comment-rating {
    min-width: 60px;
    padding: 6px;
  }
  .rating-emoji {
    font-size: 20px;
  }
  .rating-label {
    font-size: 10px;
  }
  .comment-footer {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  .participants {
    align-items: flex-start;
  }
}
</style>
