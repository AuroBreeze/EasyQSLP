<template>
  <div class="page">
    <h1>创建项目（最小实现）</h1>

    <form class="form" @submit.prevent="onSubmit">
      <label class="label">
        <span>项目名称</span>
        <input v-model="title" type="text" placeholder="输入项目名称" required />
      </label>

      <label class="label">
        <span>简介（可选，最长50字）</span>
        <input v-model="introduction" type="text" maxlength="50" placeholder="简单介绍该项目" />
      </label>

      <div class="actions">
        <button type="submit" :disabled="submitting">{{ submitting ? '创建中...' : '创建项目' }}</button>
        <router-link to="/main" class="link">返回主界面</router-link>
      </div>

      <p v-if="error" class="error">{{ error }}</p>
      <div v-if="success" class="success">
        <p>创建成功！项目ID：<strong>{{ createdId }}</strong></p>
        <p>在“发布文章”时，请把 <strong>project</strong> 字段设置为这个 ID，或者留空不绑定项目。</p>
        <router-link to="/article/upload" class="link">去发布文章</router-link>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { createProject } from '@/utils/ProjectManage/projectService'

const title = ref('')
const introduction = ref('')
const submitting = ref(false)
const error = ref('')
const success = ref(false)
const createdId = ref<number | null>(null)

async function onSubmit() {
  error.value = ''
  success.value = false
  createdId.value = null
  if (!title.value.trim()) {
    error.value = '项目名称不能为空'
    return
  }
  submitting.value = true
  try {
    const payload: any = { title: title.value.trim() }
    if (introduction.value.trim()) payload.introduction = introduction.value.trim()

    const res = await createProject(payload)
    if (res && res.title) {
      success.value = true
      if (res.id) createdId.value = Number(res.id)
      // 可选：清空表单
      // title.value = ''
      // introduction.value = ''
    } else if (res && res.detail) {
      error.value = res.detail
    } else if (typeof res === 'object') {
      error.value = JSON.stringify(res)
    } else {
      error.value = '未知错误，请稍后重试'
    }
  } catch (e: any) {
    error.value = e?.message || '创建失败'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.page { max-width: 720px; margin: 24px auto; padding: 0 16px; }
.form { display: grid; gap: 16px; }
.label { display: grid; gap: 8px; }
input { width: 100%; border: 1px solid #d9d9d9; border-radius: 8px; padding: 10px 12px; font-size: 14px; }
.actions { display: flex; gap: 12px; align-items: center; }
button { padding: 8px 16px; border: none; border-radius: 8px; background: #1677ff; color: #fff; cursor: pointer; }
.error { color: #d93025; }
.success { color: #1a7f37; }
.link { color: #1677ff; text-decoration: none; }
</style>
