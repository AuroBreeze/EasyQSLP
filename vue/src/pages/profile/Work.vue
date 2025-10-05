<script setup lang="ts">
</script>

<template>
  <section class="pane">
    <header class="pane__header">
      <h3>工作</h3>
      <p>你的任务、草稿与进行中的内容</p>
    </header>
    <div class="pane__body">
      <ul class="list">
        <li v-for="i in 6" :key="i" class="item">
          <span class="dot" />
          <div class="meta">
            <strong>项目草稿 #{{ i }}</strong>
            <small>最近更新：{{ new Date().toLocaleDateString() }}</small>
          </div>
        </li>
      </ul>
    </div>
  </section>
</template>

<style scoped>
.pane__header h3 { margin: 0 0 6px; font-size: 16px; }
.pane__header p { margin: 0; color: rgba(255,255,255,0.66); font-size: 13px; }
.pane__body { margin-top: 10px; }
.list { display: grid; gap: 10px; padding: 0; margin: 0; list-style: none; }
.item { display: grid; grid-template-columns: 10px 1fr; gap: 10px; align-items: start; padding: 10px 12px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); }
.dot { width: 10px; height: 10px; border-radius: 50%; background: var(--color-primary, #3b82f6); box-shadow: 0 0 8px rgba(59,130,246,0.5); margin-top: 4px; }
.meta strong { display: block; font-size: 14px; }
.meta small { color: rgba(255,255,255,0.55); }
</style>
