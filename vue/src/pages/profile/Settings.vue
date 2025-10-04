<script setup lang="ts">
import { ref } from 'vue'

const nickname = ref('')
const emailOptIn = ref(true)

function save() {
  // mock save
  alert('设置已保存（演示）')
}
</script>

<template>
  <section class="pane">
    <header class="pane__header">
      <h3>设置</h3>
      <p>个性化你的个人中心体验</p>
    </header>

    <form class="form" @submit.prevent="save">
      <label class="row">
        <span>昵称</span>
        <input v-model="nickname" type="text" placeholder="输入昵称" />
      </label>
      <label class="row">
        <span>邮件通知</span>
        <input v-model="emailOptIn" type="checkbox" />
      </label>
      <div class="actions">
        <button type="submit">保存设置</button>
      </div>
    </form>
  </section>
</template>

<style scoped>
.pane__header h3 { margin: 0 0 6px; font-size: 16px; }
.pane__header p { margin: 0; color: rgba(255,255,255,0.66); font-size: 13px; }
.form { display: grid; gap: 12px; margin-top: 12px; }
.row { display: grid; grid-template-columns: 120px 1fr; align-items: center; gap: 12px; }
.row input[type="text"] { height: 34px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); color: #fff; padding: 0 10px; }
.actions { margin-top: 6px; }
.actions button { background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.5); color: #bfdbfe; padding: 8px 14px; cursor: pointer; }
</style>
