<script setup lang="ts">
import { computed } from 'vue'
import { highlights } from '@/data/shows'

const ROW_COUNT = 4
const LOOP_COUNT = 4

const rows = computed(() => {
  const base = highlights
    .map((item, index) => ({
      id: item.id ?? `highlight-${index}`,
      poster: item.poster,
    }))
    .filter((item) => !!item.poster)

  if (!base.length) {
    return Array.from({ length: ROW_COUNT }, () => [])
  }

  return Array.from({ length: ROW_COUNT }, (_, rowIndex) => {
    const row: { uid: string; poster: string }[] = []
    for (let loop = 0; loop < LOOP_COUNT; loop++) {
      base.forEach((item, itemIndex) => {
        row.push({
          uid: `${rowIndex}-${loop}-${item.id}-${itemIndex}`,
          poster: item.poster!,
        })
      })
    }
    return row
  })
})
</script>

<template>
  <div class="auth-backdrop">
    <div class="auth-backdrop__layers" aria-hidden="true">
      <div
        v-for="(row, rowIndex) in rows"
        :key="rowIndex"
        class="auth-backdrop__track"
        :class="{ 'auth-backdrop__track--reverse': rowIndex % 2 === 1 }"
      >
        <img
          v-for="poster in row"
          :key="poster.uid"
          :src="poster.poster"
          alt=""
          loading="lazy"
          class="auth-backdrop__image"
        />
      </div>
    </div>
    <div class="auth-backdrop__vignette-left" aria-hidden="true"></div>
  </div>
</template>

<style scoped>
.auth-backdrop {
  position: absolute;
  inset: 0;
  overflow: hidden;
  background: #000;
  pointer-events: none;
}

.auth-backdrop__layers {
  position: absolute;
  inset: -16% -12%;
  display: grid;
  gap: clamp(8px, 2vw, 18px);
  transform: rotate(-10deg);
}

.auth-backdrop__track {
  display: flex;
  gap: clamp(12px, 4vw, 32px);
  animation: auth-marquee 28s linear infinite;
  will-change: transform;
  opacity: 0.72;
}

.auth-backdrop__track--reverse {
  animation-direction: reverse;
  opacity: 0.56;
}

.auth-backdrop__track:nth-child(2) {
  animation-duration: 34s;
}

.auth-backdrop__track:nth-child(3) {
  animation-duration: 42s;
  opacity: 0.65;
}

.auth-backdrop__image {
  width: clamp(220px, 30vw, 340px);
  height: auto;
  object-fit: contain;
  display: block;
  flex: 0 0 auto;
  filter: brightness(0.92) contrast(1.15) saturate(1.05);
  box-shadow: 0 42px 68px -36px rgba(0,0,0,0.85);
}

@keyframes auth-marquee {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-50%);
  }
}

/* 左侧黑色渐变遮罩（压在动效图层之上） */
.auth-backdrop__vignette-left {
  position: absolute;
  inset: 0 auto 0 0;
  width: clamp(180px, 28vw, 520px);
  /* Fallback: 黑色非线性渐变（左侧保持更长时间的满色） */
  background: linear-gradient(
    90deg,
    rgba(0, 0, 0, 1) 0%,
    rgba(0, 0, 0, 1) 22%,
    rgba(0, 0, 0, 0.72) 35%,
    rgba(0, 0, 0, 0.38) 52%,
    rgba(0, 0, 0, 0.16) 70%,
    rgba(0, 0, 0, 0.06) 85%,
    rgba(0, 0, 0, 0) 100%
  );
  z-index: 2;
  pointer-events: none;
}

/* 如果支持 color-mix，用主题色（--color-primary）生成遮罩 */
@supports (background: color-mix(in srgb, red, transparent)) {
  .auth-backdrop__vignette-left {
    --mask-color: var(--color-primary, #0ea5e9);
    /* 主题色非线性渐变（左侧更长满色，再快速衰减，后段平滑过渡） */
    background: linear-gradient(
      90deg,
      color-mix(in srgb, var(--mask-color) 100%, transparent) 0%,
      color-mix(in srgb, var(--mask-color) 100%, transparent) 22%,
      color-mix(in srgb, var(--mask-color) 72%, transparent) 35%,
      color-mix(in srgb, var(--mask-color) 38%, transparent) 52%,
      color-mix(in srgb, var(--mask-color) 16%, transparent) 70%,
      color-mix(in srgb, var(--mask-color) 6%, transparent) 85%,
      color-mix(in srgb, var(--mask-color) 0%, transparent) 100%
    );
  }
}

@media (max-width: 960px) {
  .auth-backdrop__image {
    width: clamp(180px, 52vw, 260px);
  }
}
</style>
