<template>
  <section class="hero" :style="heroStyle">
    <div class="hero-overlay"></div>
    <div class="hero-content">
      <div class="hero-meta">{{ content.tag }}</div>
      <h1>{{ content.title }}</h1>
      <p>{{ content.subtitle }}</p>
      <p class="hero-description">{{ content.description }}</p>
      <div class="hero-actions">
        <button type="button" class="primary">
          📖 开始阅读
        </button>
        <button type="button" class="secondary">
          📝 速查笔记
        </button>
      </div>
      <div class="hero-info">
        <span>{{ content.readingTime }}</span>
        <span>{{ content.difficulty }}</span>
        <span>{{ content.updated }}</span>
      </div>
      <ul class="hero-topics">
        <li v-for="topic in content.topics" :key="topic"># {{ topic }}</li>
      </ul>
      <div v-if="posters.length" class="poster-strip">
        <div class="poster-strip__label">正在浏览</div>
        <div class="poster-track">
          <button
            v-for="item in posters"
            :key="item.id"
            type="button"
            :class="['poster-button', { active: isActive(item.id) }]"
            @click="emit('update:modelValue', item.id)"
          >
            <img :src="item.poster" :alt="item.title" loading="lazy" />
            <span>{{ item.title }}</span>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  content: {
    type: Object,
    required: true,
  },
  items: {
    type: Array,
    default: () => [],
  },
  modelValue: {
    type: String,
    default: null,
  },
})

const emit = defineEmits(['update:modelValue'])

const heroStyle = computed(() => ({
  backgroundImage: `url(${props.content.backdrop})`,
}))

const posters = computed(() => props.items ?? [])

const isActive = (id) => {
  if (props.modelValue) return props.modelValue === id
  return posters.value[0]?.id === id
}
</script>

<style scoped>
.hero {
  position: relative;
  /* 占满视口高度，便于控制上下布局与可见性 */
  min-height: 100vh;
  /* 上移聚焦区：减少顶部内边距，略减底部内边距，确保底部“正在浏览”能完整显示 */
  /* 去掉底部内边距，让下沿贴边 */
  /* 左侧内边距用变量，供下方 track 复用以左向外扩 */
  --left-pad: clamp(32px, 5vw, 64px);
  padding: clamp(28px, 6vw, 64px) 0 0 var(--left-pad);
  overflow: hidden;
  display: flex;
  /* 让子元素拉伸以占满高度，便于内部用 margin-top:auto 贴底 */
  align-items: stretch;
  color: #fff;
  /* 将背景图局限在右上角，不铺满整个容器 */
  /* 向右轻微外扩并右移，避免右侧出现黑边 */
  background-position: right -12px top;
  background-size: auto 105%; /* 略微放大，保证贴边无缝 */
  background-repeat: no-repeat;
}

.hero-overlay {
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
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: clamp(560px, 68vw, 1080px);
  /* 方案B：使用 Grid，将主体内容与“正在浏览”分为上下两行 */
  display: grid;
  grid-template-rows: 1fr auto; /* 上面占满，下面自适应高度 */
  gap: 18px;
  height: 100%;
}

@media (max-width: 768px) {
  .hero {
    /* 小屏进一步上移聚焦区并压缩底部空间 */
    padding: clamp(20px, 6vw, 36px) 0 clamp(12px, 4vw, 20px) clamp(20px, 5vw, 40px);
  }

  .hero h1 {
    font-size: 40px;
  }

  .poster-strip {
    margin-top: clamp(12px, 3vw, 20px);
    gap: clamp(10px, 2vw, 14px);
  }

  .poster-button {
    width: clamp(150px, 40vw, 220px);
  }
}

.hero h1 {
  margin: 0;
  font-size: 52px;
  font-weight: 800;
  line-height: 1.05;
}

.hero p {
  margin: 0;
  font-size: 18px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.78);
}

.hero-description {
  font-size: 15px;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.72);
}

.hero-actions {
  display: flex;
  gap: 16px;
}

.hero-actions button {
  border: none;
  border-radius: 0;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.hero-actions .primary {
  background: #e50914;
  color: #fff;
  box-shadow: 0 16px 32px -16px rgba(229, 9, 20, 0.7);
}

.hero-actions .primary:hover {
  transform: translateY(-2px);
}

.hero-actions .secondary {
  background: rgba(255, 255, 255, 0.16);
  color: #fff;
}

.hero-actions .secondary:hover {
  background: rgba(255, 255, 255, 0.28);
}

.hero-info {
  display: flex;
  gap: 12px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.65);
}

.hero-topics {
  margin: 4px 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  gap: 10px;
  font-size: 12px;
  letter-spacing: 0.6px;
  color: rgba(255, 255, 255, 0.58);
}

.hero-topics li {
  white-space: nowrap;
}

.poster-strip {
  /* 减少与上方内容的间距，保证下方可完全展示 */
  margin-top: auto; /* 推到底部 */
  margin-bottom: 0;
  /* 取消左外边距，交由 track 负责左向外扩展示区域 */
  margin-left: 0;
  display: flex;
  flex-direction: column;
  gap: clamp(12px, 2.2vw, 20px);
  width: min(100%, clamp(680px, 68vw, 1080px));
  padding-bottom: 0; /* 与视口完全贴边 */
}

.poster-strip__label {
  font-size: 12px;
  letter-spacing: 6px;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.55);
}

.poster-track {
  display: flex;
  gap: clamp(12px, 2vw, 20px);
  overflow-x: auto;
  /* 向左扩展可视区域：负外边距覆盖左侧 padding，并用等值内边距保证首张卡片不被裁切 */
  margin-left: calc(-1 * var(--left-pad));
  padding: clamp(8px, 1vw, 14px) 0 0 var(--left-pad);
  scrollbar-width: none;
  position: relative;
}

.poster-track::-webkit-scrollbar {
  display: none;
}

.poster-button {
  /* 缩小卡片尺寸，减少占用高度 */
  width: clamp(180px, 18vw, 280px);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.65);
  cursor: pointer;
  padding: 0;
  transition: color 0.2s ease, transform 0.2s ease;
}

.poster-button img {
  width: 100%;
  aspect-ratio: 2 / 3;
  height: auto;
  object-fit: cover;
  border: 3px solid transparent;
  transition: border-color 0.2s ease, transform 0.2s ease;
}

.poster-button:last-child img {
  mask-image: linear-gradient(
    90deg,
    rgba(0, 0, 0, 0.98) 0%,
    rgba(0, 0, 0, 0.85) 52%,
    rgba(0, 0, 0, 0.55) 74%,
    rgba(0, 0, 0, 0.2) 86%,
    rgba(0, 0, 0, 0) 100%
  );
  -webkit-mask-image: linear-gradient(
    90deg,
    rgba(0, 0, 0, 0.98) 0%,
    rgba(0, 0, 0, 0.85) 52%,
    rgba(0, 0, 0, 0.55) 74%,
    rgba(0, 0, 0, 0.2) 86%,
    rgba(0, 0, 0, 0) 100%
  );
}

.poster-button span {
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.poster-button:hover {
  color: #fff;
  transform: translateY(-2px);
}

.poster-button:hover img {
  transform: scale(1.02);
}

.poster-button.active {
  color: #fff;
}

.poster-button.active img {
  border-color: #ffffff;
}
</style>
