<template>
  <div class="page">
    <h1>发布文章（Markdown）</h1>
    <form class="form" @submit.prevent="onSubmit">
      <label class="label">
        <span>标题</span>
        <input v-model="form.title" type="text" placeholder="输入标题" required />
      </label>

      <label class="label">
        <span>项目ID（可选）</span>
        <input v-model.number="form.project" type="number" placeholder="例如 1" min="0" />
      </label>

      <label class="label">
        <span>Markdown 内容</span>
        <textarea v-model="form.content_md" rows="16" placeholder="# Hello Markdown" required />
      </label>

      <div class="actions">
        <button type="submit" :disabled="submitting">{{ submitting ? '提交中...' : '提交' }}</button>
        <button type="button" @click="reset" :disabled="submitting">重置</button>
      </div>

      <p v-if="error" class="error">{{ error }}</p>
      <div v-if="success" class="success">
        <p>发布成功！文章ID：<strong>{{ createdId }}</strong></p>
        <router-link v-if="createdId" :to="`/article/${createdId}`" class="link">前往文章详情</router-link>
      </div>
    </form>

    <section v-if="form.content_md" class="preview">
      <h2>实时预览（原始 Markdown）</h2>
      <pre class="md"><code>{{ form.content_md }}</code></pre>
    </section>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { createArticle, type ArticlePayload } from '@/utils/ProjectManage/articleService'

const form = reactive<ArticlePayload>({
  title: '',
  content_md: '',
  project: undefined,
})

const submitting = ref(false)
const error = ref('')
const success = ref(false)
const createdId = ref<number | null>(null)

function reset() {
  form.title = ''
  form.content_md = ''
  form.project = undefined
  error.value = ''
  success.value = false
  createdId.value = null
}

async function onSubmit() {
  error.value = ''
  success.value = false
  createdId.value = null
  if (!form.title.trim() || !form.content_md.trim()) {
    error.value = '标题和内容不能为空'
    return
  }
  submitting.value = true
  try {
    const payload: any = {
      title: form.title.trim(),
      content_md: form.content_md,
    }
    // 仅当 project 为正整数时才发送该字段，避免无效外键
    if (typeof form.project === 'number' && Number.isInteger(form.project) && form.project > 0) {
      payload.project = form.project
    }
    const res = await createArticle(payload)
    if (res && res.title) {
      success.value = true
      if (res.id) createdId.value = Number(res.id)
    } else if (res && res.detail) {
      error.value = res.detail
    } else if (typeof res === 'object') {
      error.value = JSON.stringify(res)
    } else {
      error.value = '未知错误，请稍后重试'
    }
  } catch (e: any) {
    error.value = e?.message || '提交失败'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.page {
  max-width: 960px;
  margin: 24px auto;
  padding: 0 16px;
}
.form {
  display: grid;
  gap: 16px;
}
.label {
  display: grid;
  gap: 8px;
}
input,
textarea {
  width: 100%;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
}
.actions {
  display: flex;
  gap: 12px;
}
button {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: #1677ff;
  color: #fff;
  cursor: pointer;
}
button[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}
.error { color: #d93025; }
.success { color: #1a7f37; }
.preview { margin-top: 24px; }
.md {
  white-space: pre-wrap;
  background: #0e1117;
  color: #c9d1d9;
  padding: 16px;
  border-radius: 8px;
}
.link { color: #1677ff; text-decoration: none; margin-left: 8px; }
</style>
