<template>
  <header class="top-navbar">
    <div class="navbar-container">
      <!-- 当前位置显示 -->
      <div class="location-indicator">
        <span class="current-location">{{ currentLocation }}</span>
      </div>

      <!-- 搜索框 -->
      <div class="search-container">
        <input 
          type="text" 
          placeholder="搜索..." 
          v-model="searchQuery"
          @keyup.enter="handleSearch"
          class="search-input"
        >
        <button @click="handleSearch" class="search-button">
          <svg class="search-icon" viewBox="0 0 24 24">
            <path d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 0 0 1.48-5.34c-.47-2.78-2.79-5-5.59-5.34a6.505 6.505 0 0 0-7.27 7.27c.34 2.8 2.56 5.12 5.34 5.59a6.5 6.5 0 0 0 5.34-1.48l.27.28v.79l4.25 4.25c.41.41 1.08.41 1.49 0 .41-.41.41-1.08 0-1.49L15.5 14zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
          </svg>
        </button>
      </div>

      <!-- 用户入口 -->
      <div class="user-menu">
        <div class="user-avatar" @click="toggleUserMenu">
          <img :src="userAvatar" alt="用户头像" class="avatar-image">
        </div>
        <div v-if="showUserMenu" class="dropdown-menu">
          <router-link to="/profile" class="dropdown-item">个人中心</router-link>
          <router-link to="/settings" class="dropdown-item">设置</router-link>
          <div class="dropdown-divider"></div>
          <button @click="handleLogout" class="dropdown-item logout">退出登录</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 搜索功能
const searchQuery = ref('')
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ path: '/search', query: { q: searchQuery.value } })
  }
}

// 用户菜单
const showUserMenu = ref(false)
const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

// 用户头像 - 从store或props获取
const userAvatar = computed(() => {
  return '/public/avatar/default.png' // 默认头像路径
})

// 当前位置
const currentLocation = computed(() => {
  const nameMap: Record<string, string> = {
    'profile': '个人中心',
    'settings': '设置',
    'search': '搜索结果',
    'home': '首页'
  }
  return nameMap[route.name as string] || '未知位置'
})

// 退出登录
const handleLogout = () => {
  localStorage.removeItem('access_token')
  router.push('/login')
}
</script>

<style scoped>
.top-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: linear-gradient(to right, #FF4B2B, #FF416C);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  color: white;
}

.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.location-indicator {
  font-weight: bold;
  font-size: 18px;
}

.search-container {
  display: flex;
  align-items: center;
  width: 40%;
  max-width: 500px;
}

.search-input {
  flex: 1;
  padding: 8px 15px;
  border: none;
  border-radius: 20px 0 0 20px;
  outline: none;
  font-size: 14px;
}

.search-button {
  background: white;
  border: none;
  border-radius: 0 20px 20px 0;
  padding: 8px 15px;
  cursor: pointer;
  transition: background 0.3s;
}

.search-button:hover {
  background: #f0f0f0;
}

.search-icon {
  width: 20px;
  height: 20px;
  fill: #FF4B2B;
}

.user-menu {
  position: relative;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid white;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: 50px;
  background: white;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  min-width: 150px;
  z-index: 1001;
}

.dropdown-item {
  display: block;
  padding: 10px 15px;
  color: #333;
  text-decoration: none;
  transition: background 0.3s;
}

.dropdown-item:hover {
  background: #f5f5f5;
  color: #FF4B2B;
}

.dropdown-divider {
  height: 1px;
  background: #eee;
  margin: 5px 0;
}

.logout {
  color: #ff4b2b;
}
</style>
