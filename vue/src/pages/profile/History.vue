<script setup lang="ts">
</script>

<template>
  <section class="pane">
    <header class="pane__header">
      <h3>历史</h3>
      <p>你最近浏览与学习的记录</p>
    </header>
    <table class="table">
      <thead>
        <tr><th>标题</th><th>上次访问</th><th>进度</th></tr>
      </thead>
      <tbody>
        <tr v-for="i in 8" :key="i">
          <td>学习记录 #{{ i }}</td>
          <td>{{ new Date().toLocaleString() }}</td>
          <td>
            <div class="bar"><i :style="{ width: (10 + i*10) + '%' }" /></div>
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<style scoped>
.pane__header h3 { margin: 0 0 6px; font-size: 16px; }
.pane__header p { margin: 0; color: rgba(255,255,255,0.66); font-size: 13px; }
.table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px; }
th, td { text-align: left; padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.08); }
.bar { width: 160px; height: 8px; background: rgba(255,255,255,0.08); border-radius: 4px; overflow: hidden; }
.bar i { display: block; height: 100%; background: linear-gradient(90deg, #22c55e, #0ea5e9); }
</style>
