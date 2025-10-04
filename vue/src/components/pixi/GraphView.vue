<script setup lang="ts">
import { onMounted, ref } from 'vue'
import * as PIXI from 'pixi.js'
import PixiStage from './PixiStage.vue'
import { radialLayout, type LayoutNode } from './useRadialLayout'

const props = defineProps<{
  data: LayoutNode
}>()

// camera container for zoom/pan
const camera = new PIXI.Container()
const depthLayers = [new PIXI.Container(), new PIXI.Container(), new PIXI.Container()]
// 每层节点容器映射，便于找到父节点容器并将下一层挂载其下
const nodeMaps: Array<Map<string, PIXI.Container>> = [
  new Map<string, PIXI.Container>(),
  new Map<string, PIXI.Container>(),
  new Map<string, PIXI.Container>(),
]
// 每层旋转速度（弧度/帧近似，后续用基于时间的方式更稳）
const layerSpeeds = [0.003, -0.002, 0.0015]
const appRef = ref<PIXI.Application | null>(null)
let rafTweenId: number | null = null
let cameraTweening = false
let followTarget: PIXI.Container | null = null
let followDepth: number | null = null
let savedSpeed: number | null = null

// focus path ids
const focusPath = ref<string[]>([])

function mountLevel(
  nodes: LayoutNode[],
  depth: number,
  center: { x: number; y: number },
  radius: number,
  parentId?: string,
) {
  const layer = depthLayers[depth]
  layer.removeChildren()
  // 维护映射
  nodeMaps[depth].clear()

  // 确定层容器的父节点与定位：
  if (depth === 0) {
    // 顶层挂到 camera 下，放到舞台中心
    if (layer.parent !== camera) camera.addChild(layer)
    layer.position.set(center.x, center.y)
  } else {
    // 子层挂到父节点容器下，定位为父局部坐标原点
    const parentContainer = nodeMaps[depth - 1].get(parentId || '')
    if (parentContainer) {
      if (layer.parent !== parentContainer) parentContainer.addChild(layer)
      layer.position.set(0, 0)
    }
  }

  // 对于顶层按世界中心布局；对子层按父局部中心(0,0)布局
  const layoutCenter = depth === 0 ? center : { x: 0, y: 0 }
  const placed = radialLayout(nodes, layoutCenter, radius)
  placed.forEach((n) => {
    const c = new PIXI.Container()

    const g = new PIXI.Graphics()
    const nodeR = 36 - depth * 6 // 放大基准半径
    g.circle(0, 0, nodeR).fill({ color: 0xffffff, alpha: 0.12 }).stroke({ color: 0xffffff, alpha: 0.2, width: 1 })
    c.addChild(g)

    const label = new PIXI.Text({ text: n.label, style: { fill: 0xffffff, fontSize: 12, align: 'center' } })
    label.anchor.set(0.5)
    label.y = nodeR + 16
    c.addChild(label)

    // 设置相对当前层中心的偏移
    if (depth === 0) {
      c.position.set(n.x - center.x, n.y - center.y)
    } else {
      c.position.set(n.x, n.y)
    }
    c.eventMode = 'static'
    c.cursor = 'pointer'
    c.on('pointertap', () => onNodeClick(n, depth))

    // store id
    ;(c as any).__node = n

    layer.addChild(c)
    nodeMaps[depth].set(n.id, c)
  })
}

function onReady(payload: { app: PIXI.Application; root: PIXI.Container }) {
  const { app, root } = payload
  appRef.value = app
  root.addChild(camera)
  depthLayers.forEach((l) => camera.addChild(l))

  layoutAll()
  // Ticker：仅用于相机持续位置跟随（已取消层自转）
  app.ticker.add((ticker) => {
    const d: number = ticker.deltaTime // 60fps 下约为 1

    // 持续跟随（位置）：将相机缓动到目标节点的世界位置
    if (followTarget) {
      const appW = app.renderer.width
      const appH = app.renderer.height
      const center = { x: appW / 2, y: appH / 2 }
      const worldPos = getWorldPosition(followTarget)

      // 位置缓动
      const kPos = 0.12 // 趋近系数（降低避免追逐抖动）
      const dx = center.x - worldPos.x
      const dy = center.y - worldPos.y
      camera.position.x += dx * kPos
      camera.position.y += dy * kPos
    }
  })
}

function currentCenter() {
  const app = appRef.value!
  return { x: app.renderer.width / 2, y: app.renderer.height / 2 }
}

function layoutAll() {
  const center = currentCenter()
  const r0 = Math.min(center.x, center.y) * 0.5
  const r1 = r0 * 0.8
  const r2 = r1 * 0.8

  // level 0
  const roots = props.data.children ?? []
  mountLevel(roots, 0, center, r0)

  // if focusing deeper, mount sublevels
  const findByIds = (root: LayoutNode, path: string[]): LayoutNode | null => {
    let cur: LayoutNode | undefined = root
    for (const id of path) {
      cur = (cur?.children || []).find((n) => n.id === id)
      if (!cur) return null
    }
    return cur || null
  }

  if (focusPath.value.length > 0) {
    const focus0 = findByIds(props.data, [focusPath.value[0]])
    if (focus0?.children) {
      // 确保 nodeMaps[0] 可用后再挂载子层
      mountLevel(focus0.children, 1, { x: 0, y: 0 }, r1, focus0.id)
    }
  } else depthLayers[1].removeChildren()

  if (focusPath.value.length > 1) {
    const focus1 = findByIds(props.data, [focusPath.value[0], focusPath.value[1]])
    if (focus1?.children) {
      mountLevel(focus1.children, 2, { x: 0, y: 0 }, r2, focus1.id)
    }
  } else depthLayers[2].removeChildren()

  // dim siblings
  dimSiblings()

  // 重新绑定相机跟随目标：当容器在重建后，旧引用会失效
  if (focusPath.value.length > 0) {
    const findByIds = (root: LayoutNode, path: string[]): LayoutNode | null => {
      let cur: LayoutNode | undefined = root
      for (const id of path) {
        cur = (cur?.children || []).find((n) => n.id === id)
        if (!cur) return null
      }
      return cur || null
    }
    const depth = focusPath.value.length - 1
    const focused = findByIds(props.data, focusPath.value)
    if (focused && (focused.children || []).length > 0) {
      const container = nodeMaps[depth].get(focusPath.value[depth]) || null
      if (container) followTarget = container
    }
  }
}

function getNodePos(depth: number, id: string) {
  const layer = depthLayers[depth]
  for (const child of layer.children) {
    const node = (child as any).__node as LayoutNode
    if (node?.id === id) {
      // 关键修复：必须返回“世界坐标”，否则下一层会把父节点的“局部坐标”当成世界坐标使用，
      // 导致在父层旋转时子层中心漂移（看起来像乱飞）。
      const gp = (child as any).getGlobalPosition?.() as PIXI.Point | undefined
      if (gp) return gp
      // 兜底（理论上不会走到）
      return new PIXI.Point(child.x, child.y)
    }
  }
  return currentCenter()
}

function dimSiblings() {
  depthLayers.forEach((layer, depth) => {
    for (const child of layer.children) {
      const node = (child as any).__node as LayoutNode
      const isFocused = focusPath.value[depth] === node?.id
      const sameLevelFocused = typeof focusPath.value[depth] === 'string'
      const targetAlpha = sameLevelFocused ? (isFocused ? 1 : 0.2) : 1
      const targetScale = sameLevelFocused ? (isFocused ? 1.1 : 0.9) : 1
      child.alpha = targetAlpha
      child.scale.set(targetScale)
    }
  })
}

function onNodeClick(node: LayoutNode, depth: number) {
  // update focus path
  focusPath.value = focusPath.value.slice(0, depth)
  if (focusPath.value[depth] !== node.id) focusPath.value[depth] = node.id
  layoutAll()

  // 若该节点有子类，触发相机过渡对齐到该节点中心，并跟随其旋转
  if ((node.children || []).length > 0) {
    const target = nodeMaps[depth].get(node.id)
    if (target) {
      // 降低该层自转速度，减少视觉抖动
      if (savedSpeed == null) savedSpeed = layerSpeeds[depth]
      followDepth = depth
      layerSpeeds[depth] = (savedSpeed ?? 0) * 0.2

      // 初次对齐：位置+一次性旋转
      focusCameraOn(target)
      // 一次性角度对齐
      const worldRot = getWorldRotation(target)
      camera.rotation = -worldRot

      followTarget = target
    }
  } else {
    // 叶子节点：取消持续跟随
    followTarget = null
    if (followDepth != null && savedSpeed != null) {
      layerSpeeds[followDepth] = savedSpeed
    }
    followDepth = null
    savedSpeed = null
  }
}

onMounted(() => {
  window.addEventListener('resize', () => layoutAll())
})

// ================= 相机过渡与对齐 =================
function getWorldPosition(container: PIXI.Container) {
  return container.getGlobalPosition()
}

function getWorldRotation(container: PIXI.Container): number {
  // 推导全局旋转角：由世界矩阵 a,b,c,d 计算
  const wt = (container as any).worldTransform
  if (wt && typeof wt.a === 'number' && typeof wt.b === 'number') {
    return Math.atan2(wt.b, wt.a)
  }
  return 0
}

function focusCameraOn(target: PIXI.Container, duration = 500) {
  if (!appRef.value) return
  const app = appRef.value
  const center = { x: app.renderer.width / 2, y: app.renderer.height / 2 }

  // 目标（世界）位置与旋转
  const worldPos = getWorldPosition(target)
  const worldRot = getWorldRotation(target)

  // 期望的相机位置：将目标移到视口中心
  const camStart = { x: camera.position.x, y: camera.position.y, r: camera.rotation }
  const camEnd = {
    x: camStart.x + (center.x - worldPos.x),
    y: camStart.y + (center.y - worldPos.y),
    r: camStart.r, // 旋转不在 tween 中处理，避免反馈抖动
  }

  // tween（基于时间的缓动）
  const start = performance.now()
  const easeInOut = (t: number) => (t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t)
  cameraTweening = true
  if (rafTweenId) cancelAnimationFrame(rafTweenId)

  const step = () => {
    const now = performance.now()
    const p = Math.min(1, (now - start) / duration)
    const k = easeInOut(p)
    camera.position.set(
      camStart.x + (camEnd.x - camStart.x) * k,
      camStart.y + (camEnd.y - camStart.y) * k,
    )
    // rotation tween 去掉，避免与层自转/持续跟随造成反馈
    if (p < 1) {
      rafTweenId = requestAnimationFrame(step)
    } else {
      cameraTweening = false
      rafTweenId = null
    }
  }
  step()
}

function shortestAngleDiff(a: number, b: number) {
  let diff = (b - a) % (Math.PI * 2)
  if (diff > Math.PI) diff -= Math.PI * 2
  if (diff < -Math.PI) diff += Math.PI * 2
  return diff
}
</script>

<template>
  <PixiStage @ready="onReady" />
</template>

<style scoped>
:host, :global(.pane) { position: relative; }
</style>
