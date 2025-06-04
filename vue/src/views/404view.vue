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
  font-size: 10rem;
  font-weight: 800;
  margin: 0;
  line-height: 1;
  color: var(--color-primary);
  text-shadow: 3px 3px 0 rgba(0,0,0,0.1);
  animation: pulse 2s infinite;
}

.error-message {
  font-size: 2.5rem;
  margin: 1.5rem 0;
  color: #555;
  font-weight: 500;
}

.error-description {
  max-width: 500px;
  margin-bottom: 3rem;
  line-height: 1.8;
  color: #666;
  font-size: 1.1rem;
}

.home-button {
  display: inline-block;
  padding: 1rem 2rem;
  background-color: var(--color-primary);
  color: white;
  border-radius: 50px;
  text-decoration: none;
  transition: all 0.3s;
  font-size: 1.1rem;
  font-weight: 600;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transform: translateY(0);
}

.home-button:hover {
  background-color: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0,0,0,0.15);
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}
</style>
