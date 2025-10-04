<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, defineEmits } from 'vue'
import * as PIXI from 'pixi.js'

const containerRef = ref<HTMLDivElement | null>(null)
const appRef = ref<PIXI.Application | null>(null)

const emit = defineEmits<{
  (e: 'ready', payload: { app: PIXI.Application; root: PIXI.Container }): void
}>()

let resizeObserver: ResizeObserver | null = null

onMounted(async () => {
  const el = containerRef.value!
  const app = new PIXI.Application()
  await app.init({
    backgroundAlpha: 0,
    antialias: true,
    resizeTo: el, // auto fit container
    resolution: Math.max(1, window.devicePixelRatio || 1),
    autoDensity: true,
    preference: 'webgl',
  })
  el.appendChild(app.canvas)

  const root = new PIXI.Container()
  app.stage.addChild(root)

  appRef.value = app

  // resizeTo handles most cases, but ensure pixel ratio density
  const update = () => {
    // no-op because resizeTo handles canvas size
  }
  resizeObserver = new ResizeObserver(update)
  resizeObserver.observe(el)

  emit('ready', { app, root })
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  const app = appRef.value
  if (app) {
    // v8 建议直接销毁 Application；子级容器随 stage 释放
    app.destroy()
    appRef.value = null
  }
})
</script>

<template>
  <div ref="containerRef" class="pixi-stage" />
</template>

<style scoped>
.pixi-stage {
  width: 100%;
  height: 520px; /* 默认高度，可按需通过外层容器控制 */
  display: block;
}
</style>
