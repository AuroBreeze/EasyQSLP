<template>
  <WaveBackground />
  <div class="content-wrapper">
    <h1 class="site-title">EasyQFLP</h1>
  </div>
  <div class="main-content-wrapper">
    <div class="main-content">
      <div class="action-buttons">
        <a href="index.html" class="action-btn quick-start-btn">
          <span class="btn-text">快速开始</span>
          <span class="btn-icon">→</span>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import WaveBackground from '@/components/wave_background.vue'
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');


.content-wrapper {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 1;
}

.main-content-wrapper {
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
  z-index: 1;
}

.site-title {
  color: white;
  font-size: 3rem;
  font-weight: 700;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  letter-spacing: 1px;
  margin-bottom: 0;
}

.main-content {
  text-align: center;
}

.quick-start-btn {
  background-color: white;
  color: #FF416C;
  border: none;
  border-radius: 25px;
  box-shadow: 0 4px 15px rgba(255, 65, 108, 0.3);
  margin-bottom: 20px;
  padding: 10px 30px;
  font-size: 1rem;
  min-width: 150px;
  transition: all 0.3s ease;
}

.quick-start-btn:hover {
  background-color: white; /* 保持背景颜色不变 */
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 75, 43, 0.4);
}

.sub-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.action-btn {
  padding: 15px 50px;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  text-align: center;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-width: 200px;
  cursor: pointer;
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

/* 响应式设计 */
@media (max-width: 768px) {
  .content-wrapper {
    top: 10px;
    left: 10px;
  }

  .main-content-wrapper {
    right: 10px;
  }

  .site-title {
    font-size: 2rem;
  }

  .quick-start-title {
    font-size: 1.5rem;
    margin-bottom: 20px;
  }

  .action-buttons {
    gap: 10px;
  }

  .action-btn {
    padding: 10px 30px;
    font-size: 1rem;
    min-width: 150px;
  }
}
</style>