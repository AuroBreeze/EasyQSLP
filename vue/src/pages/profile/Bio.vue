<script setup lang="ts">
import { computed } from 'vue'

// 生成最近 53 周（GitHub 风格）× 7 天的日期与强度
const DAYS = 7
const WEEKS = 53

type Cell = { date: string; count: number }

function generateHeatmapData(): Cell[][] {
  const today = new Date()
  const grid: Cell[][] = Array.from({ length: WEEKS }, () => Array.from({ length: DAYS }, () => ({ date: '', count: 0 })))

  // 从右到左填充（与 GitHub 相似）
  for (let w = WEEKS - 1; w >= 0; w--) {
    for (let d = DAYS - 1; d >= 0; d--) {
      const idx = (WEEKS - 1 - w) * DAYS + (DAYS - 1 - d)
      const date = new Date(today)
      date.setDate(today.getDate() - idx)
      // 简单的伪数据：工作日较活跃，周末较低，叠加轻微噪声
      const day = date.getDay() // 0=Sun
      const base = day === 0 || day === 6 ? 1 : 3
      const noise = Math.random() < 0.5 ? 0 : 1
      const count = Math.max(0, Math.min(4, base + noise - (Math.random() < 0.15 ? 2 : 0)))
      grid[w][d] = { date: date.toISOString().slice(0, 10), count }
    }
  }
  return grid
}

const heatmap = computed(() => generateHeatmapData())

// 学习时间曲线（最近 14 天分钟数），生成简单的折线图
const DAYS_RANGE = 14
const studyMinutes = computed(() => {
  const arr: number[] = []
  for (let i = DAYS_RANGE - 1; i >= 0; i--) {
    // 平日 40-120 分钟，周末 10-60 分钟
    const date = new Date()
    date.setDate(date.getDate() - i)
    const day = date.getDay()
    const base = day === 0 || day === 6 ? 10 : 40
    const span = day === 0 || day === 6 ? 50 : 80
    arr.push(base + Math.floor(Math.random() * span))
  }
  return arr
})

const maxMinutes = computed(() => Math.max(...studyMinutes.value, 1))

function buildSparklinePath(values: number[], width = 560, height = 72, padding = 8) {
  if (!values.length) return ''
  const innerW = width - padding * 2
  const innerH = height - padding * 2
  const stepX = innerW / (values.length - 1)
  const maxV = Math.max(...values)
  const points: [number, number][] = values.map((v, i) => [padding + i * stepX, padding + innerH - (v / maxV) * innerH])
  return points.map(([x, y], i) => (i === 0 ? `M ${x},${y}` : `L ${x},${y}`)).join(' ')
}

const sparkD = computed(() => buildSparklinePath(studyMinutes.value))
</script>

<template>
  <section class="bio">
    <header class="bio__header">
      <h2>个人简介</h2>
      <p>最近的访问频率与学习时长概览</p>
    </header>

    <div class="bio__grid">
      <section class="bio__card">
        <h3>访问频率（近 53 周）</h3>
        <div class="heatmap" role="img" aria-label="访问频率热力图">
          <div v-for="(week, wx) in heatmap" :key="wx" class="heatmap__col">
            <div
              v-for="(cell, dx) in week"
              :key="dx"
              class="heatmap__cell"
              :data-date="cell.date"
              :data-count="cell.count"
              :style="{ '--level': String(cell.count) } as any"
              :title="`${cell.date}: 等级 ${cell.count}`"
            />
          </div>
        </div>
        <div class="legend">
          <span>低</span>
          <div class="legend__scale">
            <i v-for="i in 5" :key="i" :style="{ '--level': String(i - 1) } as any" />
          </div>
          <span>高</span>
        </div>
      </section>

      <section class="bio__card">
        <h3>学习时间（近 14 天）</h3>
        <svg class="spark" viewBox="0 0 560 72" preserveAspectRatio="none" aria-label="学习时间曲线">
          <defs>
            <linearGradient id="spark-grad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#22c55e" stop-opacity="0.8" />
              <stop offset="100%" stop-color="#22c55e" stop-opacity="0.1" />
            </linearGradient>
          </defs>
          <path :d="sparkD" fill="none" stroke="#22c55e" stroke-width="2" />
          <path :d="sparkD + ' V 72 H 0 Z'" fill="url(#spark-grad)" stroke="none" />
        </svg>
        <p class="note">最大值：{{ maxMinutes }} 分钟/日</p>
      </section>
    </div>
  </section>
  
</template>

<style scoped>
.bio {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.bio__header h2 {
  margin: 0 0 6px;
  font-size: 18px;
}

.bio__header p {
  margin: 0;
  color: rgba(255, 255, 255, 0.72);
  font-size: 14px;
}

.bio__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 18px;
}

.bio__card {
  background: rgba(0,0,0,0.38);
  border: 1px solid rgba(255,255,255,0.08);
  padding: 16px;
}

/* Heatmap */
.heatmap {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: min-content;
  gap: 3px;
  overflow-x: auto;
  padding-bottom: 6px;
}
.heatmap__col {
  display: grid;
  grid-template-rows: repeat(7, 10px);
  gap: 3px;
}
.heatmap__cell {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  /* 绿色热力：从深背景到明亮绿色 */
  background: color-mix(in srgb, #22c55e calc(var(--level) * 24%), #0a0a0a);
}

/* Legend */
.legend { display: flex; align-items: center; gap: 8px; color: rgba(255,255,255,0.7); font-size: 12px; }
.legend__scale { display: inline-grid; grid-template-columns: repeat(5, 12px); gap: 4px; }
.legend__scale i { width: 12px; height: 10px; border-radius: 2px; background: color-mix(in srgb, #22c55e calc(var(--level) * 24%), #0a0a0a); }

/* Sparkline */
.spark { width: 100%; height: 72px; display: block; }
.note { color: rgba(255, 255, 255, 0.65); font-size: 12px; margin: 6px 0 0; }

@media (min-width: 960px) {
  .bio__grid { grid-template-columns: 1.2fr 1fr; }
}
</style>
