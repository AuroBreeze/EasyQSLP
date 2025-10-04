<script setup lang="ts">
import GraphView from '@/components/pixi/GraphView.vue'

type Node = { id: string; label: string; children?: Node[] }

const tree: Node = {
  id: 'root',
  label: 'root',
  children: [
    {
      id: 'fe',
      label: '前端',
      children: [
        { id: 'vue', label: 'Vue' },
        { id: 'react', label: 'React' },
        { id: 'svelte', label: 'Svelte' },
        { id: 'ts', label: 'TypeScript' },
      ],
    },
    {
      id: 'be',
      label: '后端',
      children: [
        { id: 'django', label: 'Django' },
        { id: 'spring', label: 'Spring' },
        { id: 'node', label: 'Node.js' },
      ],
    },
    {
      id: 'algo',
      label: '算法',
      children: [
        {
          id: 'cpp',
          label: 'C++',
          children: [
            { id: 'stl', label: 'STL' },
            { id: 'opt', label: '优化' },
          ],
        },
        {
          id: 'java',
          label: 'Java',
          children: [
            { id: 'concurrency', label: '并发' },
            { id: 'jvm', label: 'JVM' },
          ],
        },
        {
          id: 'py',
          label: 'Python',
          children: [
            { id: 'ml', label: '机器学习' },
            { id: 'dl', label: '深度学习' },
          ],
        },
      ],
    },
  ],
}
</script>

<template>
  <section class="pane">
    <header class="pane__header">
      <h3>展演空间</h3>
      <p>你的作品展示与灵感陈列区</p>
    </header>
    <GraphView :data="tree" />
  </section>
</template>

<style scoped>
.pane__header h3 { margin: 0 0 6px; font-size: 16px; }
.pane__header p { margin: 0; color: rgba(255,255,255,0.66); font-size: 13px; }
.pane :deep(.pixi-stage) { height: 560px; }
</style>
