<template>
  <div id="app" class="not-found full-screen">
    <TopNavBar />
    <WaveBackground />
    
    <div class="content">
      <h1 class="error-code">404</h1>
      <h2 class="error-message">页面不存在</h2>
      <p class="error-description">
        您访问的页面可能已被移除、重命名或暂时不可用
      </p>
      <router-link to="/" class="home-button">
        返回首页
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import TopNavBar from '@/components/navigation/TopNavBar.vue'
import WaveBackground from '@/components/background/WaveBackground.vue'
</script>

<style scoped>
.not-found {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 1200px;
  padding: 2rem;
  text-align: center;
  color: var(--color-text);
  box-sizing: border-box;
}

.error-code {
  font-size: 8rem;
  font-weight: 700;
  margin: 0;
  line-height: 1;
  color: var(--color-primary);
}

.error-message {
  font-size: 2rem;
  margin: 1rem 0;
}

.error-description {
  max-width: 500px;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.home-button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: var(--color-primary);
  color: white;
  border-radius: 4px;
  text-decoration: none;
  transition: background-color 0.2s;
}

.home-button:hover {
  background-color: var(--color-primary-dark);
}
</style>
