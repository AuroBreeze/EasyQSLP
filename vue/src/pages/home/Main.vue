<script setup lang="ts">
const hero = { title: '推荐精选', desc: '本周热门内容与编辑推荐', bg: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }
const rows = [
  { title: '热门推荐', items: Array.from({ length: 8 }, (_, i) => ({ id: i, name: `热门 ${i + 1}` })) },
  { title: '最新上线', items: Array.from({ length: 8 }, (_, i) => ({ id: i + 10, name: `新品 ${i + 1}` })) },
  { title: '编辑精选', items: Array.from({ length: 8 }, (_, i) => ({ id: i + 20, name: `精选 ${i + 1}` })) },
]
</script>

<template>
  <div class="netflix-main">
    <!-- Hero 横幅 -->
    <section class="hero" :style="{ background: hero.bg }">
      <div class="hero__content">
        <h1>{{ hero.title }}</h1>
        <p>{{ hero.desc }}</p>
        <div class="hero__actions">
          <button class="btn btn--primary">立即播放</button>
          <button class="btn btn--secondary">更多信息</button>
        </div>
      </div>
    </section>

    <!-- 横向滚动卡片行 -->
    <section v-for="row in rows" :key="row.title" class="row">
      <h2 class="row__title">{{ row.title }}</h2>
      <div class="row__cards">
        <article v-for="item in row.items" :key="item.id" class="card">
          <div class="card__thumb" />
          <div class="card__info">
            <strong>{{ item.name }}</strong>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.netflix-main {
  padding: 0;
  background: var(--bg-base);
  min-height: 100vh;
}

/* Hero 横幅 */
.hero {
  height: 70vh;
  display: flex;
  align-items: flex-end;
  padding: 0 4vw 8vh;
  position: relative;
  background-size: cover !important;
  background-position: center !important;
}
.hero::before {
  content: '';
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
.hero__content {
  position: relative;
  z-index: 1;
  max-width: 540px;
}
.hero__content h1 {
  margin: 0 0 12px;
  font-size: clamp(32px, 5vw, 56px);
  font-weight: 700;
  color: #fff;
}
.hero__content p {
  margin: 0 0 24px;
  font-size: 18px;
  line-height: 1.5;
  color: rgba(255,255,255,0.9);
}
.hero__actions {
  display: flex;
  gap: 12px;
}
.btn {
  padding: 12px 28px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.2s ease, background 0.2s ease;
}
.btn:hover { transform: scale(1.05); }
.btn--primary {
  background: #fff;
  color: #000;
}
.btn--primary:hover { background: rgba(255,255,255,0.85); }
.btn--secondary {
  background: rgba(109,109,110,0.7);
  color: #fff;
}
.btn--secondary:hover { background: rgba(109,109,110,0.5); }

/* 横向滚动行 */
.row {
  padding: 0 4vw 32px;
}
.row__title {
  margin: 0 0 12px;
  font-size: 20px;
  font-weight: 600;
  color: #e5e5e5;
}
.row__cards {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-behavior: smooth;
  padding-bottom: 8px;
}
.row__cards::-webkit-scrollbar { height: 6px; }
.row__cards::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
.row__cards::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 3px; }

/* 卡片 */
.card {
  flex: 0 0 auto;
  width: 280px;
  border-radius: 4px;
  overflow: hidden;
  background: #2f2f2f;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
  transform: scale(1.08);
  box-shadow: 0 8px 24px rgba(0,0,0,0.6);
  z-index: 10;
}
.card__thumb {
  width: 100%;
  height: 158px;
  background: linear-gradient(135deg, #434343 0%, #000000 100%);
}
.card__info {
  padding: 12px;
}
.card__info strong {
  display: block;
  font-size: 14px;
  color: #e5e5e5;
}
</style>
