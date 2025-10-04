<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
// 移除AuthBackdrop引用，仅在登录注册页面保留海报墙背景

interface StoredAuthPayload {
  token?: string
  user?: {
    id?: string | number
    name?: string
    nickname?: string
    email?: string
    avatar?: string
    photo?: string
    avatarUrl?: string
    role?: string
    organization?: string
    lastActiveAt?: string
  }
  ts?: number
  remember?: boolean
}

const router = useRouter()
const loading = ref(true)
const errorMsg = ref('')
const auth = ref<StoredAuthPayload | null>(null)

function readAuthPayload() {
  if (typeof window === 'undefined') return null
  const raw = window.localStorage.getItem('mock_auth') ?? window.sessionStorage.getItem('mock_auth')
  if (!raw) return null
  try {
    return JSON.parse(raw) as StoredAuthPayload
  } catch (err) {
    console.warn('[Profile] failed to parse stored auth payload', err)
    return null
  }
}

function ensureAuthenticated() {
  const payload = readAuthPayload()
  if (!payload?.token) {
    router.replace({ name: 'login', query: { redirect: 'profile' } })
    return
  }
  auth.value = payload
}

function onSignOut() {
  if (typeof window !== 'undefined') {
    window.localStorage.removeItem('mock_auth')
    window.sessionStorage.removeItem('mock_auth')
  }
  router.replace({ name: 'login' })
}

const user = computed(() => auth.value?.user ?? null)
const displayName = computed(() => user.value?.name ?? user.value?.nickname ?? '未命名用户')
const displayEmail = computed(() => user.value?.email ?? '未绑定邮箱')
const avatarUrl = computed(
  () => user.value?.avatar ?? user.value?.photo ?? user.value?.avatarUrl ?? null
)
const roleLabel = computed(() => user.value?.role ?? '普通成员')
const organizationLabel = computed(() => user.value?.organization ?? '未加入组织')
const lastActiveLabel = computed(() => {
  const ts = auth.value?.ts
  if (!ts) return '暂无记录'
  try {
    const date = new Date(ts)
    return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`
  } catch (err) {
    return '暂无记录'
  }
})

const profileItems = computed(() => [
  { label: '邮箱', value: displayEmail.value },
  { label: '身份', value: roleLabel.value },
  { label: '组织', value: organizationLabel.value },
  { label: '最近活跃', value: lastActiveLabel.value },
])

onMounted(() => {
  ensureAuthenticated()
  loading.value = false
  if (!auth.value) {
    errorMsg.value = '尚未登录，正在跳转登录页面…'
  }
})
</script>

<template>
  <section class="profile">
    <div class="profile__container">
      <main class="profile__content">
        <section class="profile__card profile__card--child">
          <router-view />
        </section>
      </main>

      <p v-if="loading" class="profile__status">正在加载...</p>
      <p v-if="errorMsg" class="profile__status profile__status--error">{{ errorMsg }}</p>
    </div>
  </section>
</template>

<style scoped>
.profile {
  position: relative;
  min-height: 100vh;
  color: #f8fafc;
  background: #040404;
}

.profile > *:not(.profile__container) {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.profile__container {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 32px;
  padding: clamp(32px, 8vw, 80px) clamp(24px, 8vw, 96px);
  box-sizing: border-box;
}


.profile__content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: clamp(24px, 6vw, 48px);
}

.profile__card {
  background: rgba(0, 0, 0, 0.38);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: clamp(20px, 5vw, 36px);
  display: flex;
  flex-direction: column;
  gap: 18px;
  border-radius: 0;
}

.profile__card--child {
  grid-column: 1 / -1;
}

.profile__card h2 {
  margin: 0;
  font-size: 18px;
  letter-spacing: 0.6px;
}

.profile__card ul {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.profile__card li {
  display: grid;
  grid-template-columns: 120px minmax(0, 1fr);
  gap: 12px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.78);
}

.profile__card .label {
  color: rgba(255, 255, 255, 0.54);
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 1.2px;
}

.profile__card--actions .actions {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.profile__card--actions button {
  border: 1px solid rgba(59, 130, 246, 0.4);
  background: rgba(59, 130, 246, 0.12);
  color: #bfdbfe;
  padding: 10px 16px;
  font-size: 14px;
  cursor: pointer;
  text-align: left;
  transition: background 0.2s ease, border-color 0.2s ease;
}

.profile__card--actions button:hover {
  background: rgba(59, 130, 246, 0.22);
  border-color: rgba(59, 130, 246, 0.72);
}

.profile__status {
  margin: 0;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
}

.profile__status--error {
  color: #f87171;
}

@media (max-width: 960px) {
}
</style>
