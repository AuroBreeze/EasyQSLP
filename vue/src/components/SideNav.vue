<template>
  <nav class="side-nav">
    <button
      type="button"
      class="profile"
      :class="{ 'profile--active': isProfileActive }"
      aria-label="用户中心"
      @click="goProfile"
    >
      <img
        v-if="avatarUrl && !avatarError"
        :src="avatarUrl"
        alt="用户头像"
        @error="onAvatarError"
      />
      <svg v-else viewBox="0 0 48 48" aria-hidden="true">
        <circle cx="24" cy="16" r="10" />
        <path d="M8 42c2-8 9-14 16-14s14 6 16 14" />
      </svg>
    </button>
    <ul class="nav-items">
      <li
        v-for="(item, i) in navItems"
        :key="i"
        class="nav-item"
        :class="{ 'nav-item--active': activeIcon === item.icon }"
      >
        <button
          type="button"
          :aria-label="item.label"
          @click="onNavItemClick(item)"
        >
          <Transition name="navicon" mode="out-in">
            <span class="nav-icon" :class="{ 'nav-icon--large': item.icon === 'favorites' }" :key="item.icon">
          <!-- 极简单色 SVG，与主题形成对比（currentColor） -->
          <svg v-if="item.icon === 'search'" viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="11" cy="11" r="7"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <svg v-else-if="item.icon === 'home'" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M3 10.5L12 3l9 7.5"/>
            <path d="M5 10.5V21h14V10.5"/>
          </svg>
          <svg v-else-if="item.icon === 'series'" viewBox="0 0 24 24" aria-hidden="true">
            <rect x="3" y="6" width="18" height="12" rx="2"/>
            <line x1="8" y1="3" x2="12" y2="6"/>
            <line x1="16" y1="3" x2="12" y2="6"/>
          </svg>
          <svg v-else-if="item.icon === 'film'" viewBox="0 0 24 24" aria-hidden="true">
            <rect x="3" y="7" width="18" height="14" rx="2"/>
            <path d="M3 7l4-4h7l-4 4"/>
            <line x1="11" y1="11" x2="17" y2="11"/>
          </svg>
          <svg v-else-if="item.icon === 'list'" viewBox="0 0 24 24" aria-hidden="true">
            <line x1="5" y1="7" x2="19" y2="7"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
            <line x1="5" y1="17" x2="19" y2="17"/>
          </svg>
          <svg v-else-if="item.icon === 'bio'" viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="12" cy="8" r="4" />
            <path d="M4 20c1.5-4 4-6 8-6s6.5 2 8 6" />
          </svg>
          <svg v-else-if="item.icon === 'work'" viewBox="0 0 24 24" aria-hidden="true">
            <rect x="3" y="8" width="18" height="12" rx="2" />
            <path d="M9 8V6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2" />
            <path d="M3 13h18" />
          </svg>
          <svg v-else-if="item.icon === 'favorites'" viewBox="0 0 24 24" aria-hidden="true">
            <!-- 中心点 -->
            <circle cx="12" cy="12" r="1.6" fill="currentColor" stroke="none" />
            <!-- 第一圈辐射点 -->
            <circle cx="12" cy="6.5" r="1" fill="currentColor" stroke="none" />
            <circle cx="17.5" cy="12" r="1" fill="currentColor" stroke="none" />
            <circle cx="12" cy="17.5" r="1" fill="currentColor" stroke="none" />
            <circle cx="6.5" cy="12" r="1" fill="currentColor" stroke="none" />
            <!-- 第二圈辐射点（对角） -->
            <circle cx="16.2" cy="7.8" r="0.9" fill="currentColor" stroke="none" />
            <circle cx="16.2" cy="16.2" r="0.9" fill="currentColor" stroke="none" />
            <circle cx="7.8" cy="16.2" r="0.9" fill="currentColor" stroke="none" />
            <circle cx="7.8" cy="7.8" r="0.9" fill="currentColor" stroke="none" />
            <!-- 环形辅助线（细） -->
            <circle cx="12" cy="12" r="6" stroke="currentColor" stroke-width="0.8" fill="none" opacity="0.5" />
            <!-- 第三圈：更外层辐射点与细环 -->
            <circle cx="12" cy="2.5" r="0.8" fill="currentColor" stroke="none" />
            <circle cx="21.5" cy="12" r="0.8" fill="currentColor" stroke="none" />
            <circle cx="12" cy="21.5" r="0.8" fill="currentColor" stroke="none" />
            <circle cx="2.5" cy="12" r="0.8" fill="currentColor" stroke="none" />
            <circle cx="19.2" cy="4.8" r="0.7" fill="currentColor" stroke="none" />
            <circle cx="19.2" cy="19.2" r="0.7" fill="currentColor" stroke="none" />
            <circle cx="4.8" cy="19.2" r="0.7" fill="currentColor" stroke="none" />
            <circle cx="4.8" cy="4.8" r="0.7" fill="currentColor" stroke="none" />
            <circle cx="12" cy="12" r="9.5" stroke="currentColor" stroke-width="0.6" fill="none" opacity="0.35" />
          </svg>
          <svg v-else-if="item.icon === 'history'" viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="12" cy="12" r="8" />
            <path d="M12 8v5l3 2" />
            <path d="M4 4v4h4" />
          </svg>
          <svg v-else-if="item.icon === 'settings'" viewBox="0 0 24 24" aria-hidden="true">
            <!-- 设置：滑杆样式（简洁线性） -->
            <line x1="4" y1="7" x2="20" y2="7" />
            <circle cx="9" cy="7" r="2.2" fill="none" />
            
            <line x1="4" y1="12" x2="20" y2="12" />
            <circle cx="14" cy="12" r="2.2" fill="none" />
            
            <line x1="4" y1="17" x2="20" y2="17" />
            <circle cx="7" cy="17" r="2.2" fill="none" />
          </svg>
            </span>
          </Transition>
        </button>
      </li>
    </ul>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const avatarUrl = ref<string | null>(null)
const avatarError = ref(false)
const hasAuth = ref(false)
const router = useRouter()
const route = useRoute()
const refererRoute = ref<string | null>(null)

function refreshAuth() {
  if (typeof window === 'undefined') return

  const stored =
    window.localStorage.getItem('mock_auth') ?? window.sessionStorage.getItem('mock_auth')

  if (!stored) {
    hasAuth.value = false
    avatarUrl.value = null
    avatarError.value = false
    return
  }

  try {
    const parsed = JSON.parse(stored)
    hasAuth.value = Boolean(parsed?.token)
    const candidate = parsed?.user?.avatar ?? parsed?.user?.photo ?? parsed?.user?.avatarUrl
    avatarUrl.value = typeof candidate === 'string' && candidate.length > 0 ? candidate : null
    avatarError.value = false
  } catch (err) {
    console.warn('[SideNav] failed to parse stored auth payload', err)
    hasAuth.value = false
    avatarUrl.value = null
    avatarError.value = false
  }
}

onMounted(() => {
  refreshAuth()
  refererRoute.value = window.sessionStorage.getItem('side_nav_profile_referer')
})

function onAvatarError() {
  avatarError.value = true
}

function goProfile() {
  refreshAuth()
  if (hasAuth.value) {
    if (isProfileActive.value) {
      if (refererRoute.value) {
        router.push(refererRoute.value)
      } else {
        router.back()
      }
      return
    }
    window.sessionStorage.setItem('side_nav_profile_referer', route.fullPath)
    router.push({ name: 'profile-bio' })
    return
  }
  router.push({ name: 'login' })
}

const isProfileActive = computed(() => (route.path ?? '').startsWith('/profile'))
const isHomeActive = computed(() => {
  const p = route.path || ''
  // 主页含父子路由：/ (重定向到 /main)、/main、/search、/series、/film、/list
  return (
    p === '/' || p.startsWith('/main') || p.startsWith('/search') || p.startsWith('/series') || p.startsWith('/project') || p.startsWith('/list')
  )
})

watch(
  () => route.fullPath,
  (path: string, oldPath: string | undefined) => {
    if (typeof window === 'undefined') return
    const nowInProfile = path.startsWith('/profile')
    const wasInProfile = !!oldPath && oldPath.startsWith('/profile')
    // 刚进入 profile 区域时记录来源
    if (nowInProfile && oldPath && !wasInProfile) {
      window.sessionStorage.setItem('side_nav_profile_referer', oldPath)
      refererRoute.value = oldPath
    }
  },
)

// 极简 SVG 图标，使用 stroke 与 currentColor，自动与主题对比
const defaultNavItems = [
  { label: '搜索', icon: 'search' },
  { label: '首页', icon: 'home' },
  { label: '系列', icon: 'series' },
  { label: '项目', icon: 'film' },
  { label: '我的列表', icon: 'list' },
]

const profileNavItems = [
  { label: '简介', icon: 'bio' },
  { label: '工作', icon: 'work' },
  { label: '展演空间', icon: 'favorites' },
  { label: '历史', icon: 'history' },
  { label: '设置', icon: 'settings' },
]

const navItems = computed(() => (isProfileActive.value ? profileNavItems : defaultNavItems))

// 当前激活图标
const activeIcon = computed(() => {
  const p = route.path || ''
  if (isProfileActive.value) {
    if (p.startsWith('/profile/bio')) return 'bio'
    if (p.startsWith('/profile/work')) return 'work'
    if (p.startsWith('/profile/favorites')) return 'favorites'
    if (p.startsWith('/profile/history')) return 'history'
    if (p.startsWith('/profile/settings')) return 'settings'
  } else if (isHomeActive.value) {
    if (p === '/' || p.startsWith('/main')) return 'home'
    if (p.startsWith('/search')) return 'search'
    if (p.startsWith('/series')) return 'series'
    if (p.startsWith('/project')) return 'film'
    if (p.startsWith('/list')) return 'list'
  }
  return null
})

type NavItem = { label: string; icon: string }

function onNavItemClick(item: NavItem) {
  if (isProfileActive.value) {
    const map: Record<string, { name: string }> = {
      bio: { name: 'profile-bio' },
      work: { name: 'profile-work' },
      favorites: { name: 'profile-favorites' },
      history: { name: 'profile-history' },
      settings: { name: 'profile-settings' },
    }
    const target = map[item.icon]
    if (target) router.push(target)
  } else if (isHomeActive.value) {
    const map: Record<string, { name: string }> = {
      home: { name: 'home-main' },
      search: { name: 'home-search' },
      series: { name: 'home-series' },
      film: { name: 'home-project' },
      list: { name: 'home-list' },
    }
    const target = map[item.icon]
    if (target) router.push(target)
  }
}
</script>

<style scoped>
.side-nav {
  width: 72px;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* 垂直居中 */
  gap: 16px;
  /* 使用深色纯背景，消除灰阶偏色 */
  background: var(--bg-deep);
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  box-sizing: border-box;
  z-index: 1000;
}

.profile {
  width: 52px;
  height: 52px;
  border: 2px solid rgba(255, 255, 255, 0.18);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.04);
  color: rgba(255, 255, 255, 0.82);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  cursor: pointer;
  transition: border-color 0.15s ease, background 0.15s ease, color 0.15s ease;
}

.profile:hover {
  border-color: rgba(255, 255, 255, 0.32);
  background: rgba(255, 255, 255, 0.08);
}

.profile--active {
  border-color: rgba(250, 204, 21, 0.9);
  box-shadow: 0 0 0 3px rgba(250, 204, 21, 0.22), 0 0 18px rgba(250, 204, 21, 0.6);
  background: rgba(250, 204, 21, 0.09);
  color: #fde68a;
}

.profile img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: inherit;
}

.profile svg {
  width: 26px;
  height: 26px;
  stroke: currentColor;
  stroke-width: 2;
  fill: none;
}

.nav-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item button {
  width: 44px;
  height: 44px;
  border: 1px solid transparent;
  border-radius: 0;
  background: transparent;
  color: rgba(255, 255, 255, 0.82); /* 与纯黑形成对比 */
  font-size: 18px;
  cursor: pointer;
  transition: color 0.15s ease, background-color 0.15s ease, border-color 0.15s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 选中项右侧红线指示（带动效） */
.nav-item { position: relative; }
.nav-item::after {
  content: '';
  position: absolute;
  right: -6px;
  top: 50%;
  width: 3px;
  height: 28px;
  border-radius: 2px;
  background: #ef4444; /* red-500 */
  box-shadow: 0 0 0 rgba(239, 68, 68, 0);
  transform: translateY(-50%) scaleY(0.4);
  opacity: 0;
  transition: opacity 180ms ease, transform 180ms ease, box-shadow 300ms ease;
}
.nav-item--active::after {
  opacity: 1;
  transform: translateY(-50%) scaleY(1);
  box-shadow: 0 0 10px rgba(239, 68, 68, 0.55);
  animation: sidenav-indicator-pulse 1.8s ease-in-out infinite;
}

@keyframes sidenav-indicator-pulse {
  0%, 100% { box-shadow: 0 0 8px rgba(239, 68, 68, 0.45); }
  50% { box-shadow: 0 0 14px rgba(239, 68, 68, 0.75); }
}

.nav-item button:hover {
  background: rgba(255, 255, 255, 0.08); /* 灰白悬停 */
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.12);
}

/* 统一极简线性图标样式 */
.nav-item svg {
  width: 22px;
  height: 22px;
  stroke: currentColor;
  stroke-width: 1.8;
  fill: none;
  display: block; /* 避免行内元素的基线偏移影响居中 */
}

/* 展演空间图标放大版本 */
.nav-icon--large { width: 28px; height: 28px; }
.nav-icon--large svg { width: 28px; height: 28px; }

/* 图标切换过渡 */
.nav-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
}

:deep(.navicon-enter-active),
:deep(.navicon-leave-active) {
  transition: opacity 220ms ease, transform 220ms ease;
  will-change: opacity, transform;
}
:deep(.navicon-enter-from) {
  opacity: 0;
  transform: scale(0.85) rotate(-8deg);
}
:deep(.navicon-enter-to) {
  opacity: 1;
  transform: none;
}
:deep(.navicon-leave-from) {
  opacity: 1;
  transform: none;
}
:deep(.navicon-leave-to) {
  opacity: 0;
  transform: scale(0.85) rotate(8deg);
}

@media (prefers-reduced-motion: reduce) {
  :deep(.navicon-enter-active),
  :deep(.navicon-leave-active) {
    transition: none;
  }
}
</style>
