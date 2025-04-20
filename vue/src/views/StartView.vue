<template>
  <div class="start-page">
    <div class="wave-background"></div>
    <h1 class="site-title">EasyQFLP</h1>
    <div class="main-content">
      <h2 class="quick-start-title">快速开始</h2>
      <div class="action-buttons">
        <RouterLink to="/login" class="action-btn login-btn">
          <span class="btn-text">登录</span>
          <span class="btn-icon">→</span>
        </RouterLink>
        <RouterLink to="/register" class="action-btn register-btn">
          <span class="btn-text">注册</span>
          <span class="btn-icon">→</span>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<style scoped>
/* 添加字体导入 */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

.start-page {
  position: relative;
  height: 100vh;
  overflow: hidden;
  font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
              Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.wave-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 100%);
  z-index: -1;
  animation: gradientShift 8s ease infinite;
  background-size: 200% 200%;
}

.site-title {
  position: absolute;
  top: 40px;
  left: 50px;
  color: white;
  font-size: 2.5rem;
  font-weight: 700;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  letter-spacing: 1px;
}

.main-content {
  position: absolute;
  right: 15%;
  top: 50%;
  transform: translateY(-50%);
  text-align: right;
}

.quick-start-title {
  color: white;
  font-size: 3.5rem;
  margin-bottom: 50px;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  font-weight: 700;
  letter-spacing: 1px;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.action-btn {
  padding: 18px 60px;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  text-align: center;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-width: 220px;
}

.login-btn {
  background-color: white;
  color: #FF4B2B;
  border: none;
  box-shadow: 0 4px 15px rgba(255, 75, 43, 0.3);
}

.login-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 75, 43, 0.4);
}

.register-btn {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(5px);
}

.register-btn:hover {
  background-color: rgba(255, 255, 255, 0.25);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.2);
}

.btn-icon {
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s ease;
}

.action-btn:hover .btn-icon {
  opacity: 1;
  transform: translateX(0);
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>