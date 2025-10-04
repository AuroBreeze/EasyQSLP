<template>
  <div class="history-page">
    <h2>文章修订历史</h2>
    <div class="actions">
      <button class="btn" @click="refresh">刷新</button>
      <router-link v-if="articleId" class="btn outline" :to="{ name: 'article-view', params: { id: articleId } }">返回文章</router-link>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else>
      <table class="rev-table" v-if="revisions.length">
        <thead>
          <tr>
            <th>ID</th>
            <th>版本</th>
            <th>状态</th>
            <th>提交者</th>
            <th>创建时间</th>
            <th>合入时间</th>
            <th>说明</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rev in revisions" :key="rev.id">
            <td>{{ rev.id }}</td>
            <td>{{ rev.version }}</td>
            <td>{{ rev.status }}</td>
            <td>{{ rev.submitter }}</td>
            <td>{{ formatTime(rev.create_time) }}</td>
            <td>{{ rev.applied_time ? formatTime(rev.applied_time) : '-' }}</td>
            <td>{{ rev.comment }}</td>
            <td class="ops">
              <router-link class="link" :to="{ name: 'revision-diff', params: { id: rev.id }, query: { against: 'prev', mode: 'unified' } }">查看差异</router-link>
              <button class="link danger" @click="doRevert(rev.id)">回滚</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty">暂无修订</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { listRevisions, revertRevision } from '@/utils/ProjectManage/revisionService'

const route = useRoute()
const articleId = computed<number | null>(() => {
  const v = Number(route.params.id)
  return Number.isFinite(v) ? v : null
})

const loading = ref(false)
const revisions = ref<any[]>([])

function formatTime(t?: string) {
  if (!t) return '-'
  try { return new Date(t).toLocaleString() } catch { return t }
}

async function refresh() {
  if (!articleId.value) return
  loading.value = true
  try {
    const { data } = await listRevisions(articleId.value)
    revisions.value = data
  } finally {
    loading.value = false
  }
}

async function doRevert(id: number) {
  if (!confirm(`确认回滚到修订 #${id} 吗？此操作将创建新的回滚修订并需审批。`)) return
  try {
    await revertRevision(id)
    alert('已创建回滚修订，待维护者审批后自动合入。')
    refresh()
  } catch (e: any) {
    alert(e?.response?.data?.detail || '回滚失败，请检查权限（需维护者）。')
  }
}

onMounted(refresh)
</script>

<style scoped>
.history-page { padding: 16px; }
.actions { display: flex; gap: 8px; margin-bottom: 12px; }
.btn { padding: 6px 12px; border: none; background: #2563eb; color: #fff; border-radius: 6px; cursor: pointer; }
.btn.outline { background: transparent; border: 1px solid #2563eb; color: #2563eb; }
.loading, .empty { color: #666; }
.rev-table { width: 100%; border-collapse: collapse; }
.rev-table th, .rev-table td { border-bottom: 1px solid #eee; text-align: left; padding: 8px; }
.link { background: none; border: none; color: #2563eb; cursor: pointer; margin-right: 8px; }
.link.danger { color: #dc2626; }
.ops { white-space: nowrap; }
</style>
