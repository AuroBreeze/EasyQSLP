<template>
  <div>
  <WaveBackground />
  <div class="content-wrapper">
    <h1 class="site-title">EasyQSLP</h1>
    <p class="site-description">
      EasyQSLP 是一个基于项目的知识分享型网站，致力于打破信息差，提供更多的其他领域的<strong>从零开始</strong>的学习项目，让更多的人可以接触到更多的知识，以便寻找到属于自己的方向。🌍
    </p>
    <div class="info-boxes">
      <div class="info-box">
        <h2 class="info-box-title">基于项目</h2>
        <p class="info-box-content">通过实际项目学习，快速掌握技能。</p>
      </div>
      <div class="info-box">
        <h2 class="info-box-title">新手友好</h2>
        <p class="info-box-content">从零开始，适合所有水平的学习者。</p>
      </div>
      <div class="info-box">
        <h2 class="info-box-title">打破信息差</h2>
        <p class="info-box-content">提供全面的知识，消除信息不对称。</p>
      </div>
    </div>
    <div class="action-buttons">
      <a href="index.html" class="action-btn quick-start-btn">
        <span class="btn-text">快速开始</span>
        <span class="btn-icon">→</span>
      </a>
      <a href="#" class="action-btn explore-btn">
        <span class="btn-text">探索更多</span>
        <span class="btn-icon">→</span>
      </a>
    </div>
  </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import WaveBackground from '@/components/background/WaveBackground.vue'
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

.content-wrapper {
  position: absolute;
  top: 10%;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
  max-width: 600px;
  text-align: center;
}

.site-description {
  color: white;
  font-size: 1.2rem;
  font-weight: 400;
  line-height: 1.6;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  margin-top: 20px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.site-description strong {
  font-weight: 600;
}

.site-title {
  color: white;
  font-size: 4rem;
  font-weight: 700;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  letter-spacing: 1px;
  margin-bottom: 0;
}

.info-boxes {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 30px;
}

.info-box {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 20px;
  text-align: center;
  flex: 1;
}

.info-box-title {
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.info-box-content {
  color: white;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.4;
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

.explore-btn {
  background-color: #FF416C;
  color: white;
  border: none;
  border-radius: 25px;
  box-shadow: 0 4px 15px rgba(255, 65, 108, 0.3);
  margin-bottom: 20px;
  padding: 10px 30px;
  font-size: 1rem;
  min-width: 150px;
  transition: all 0.3s ease;
}

.quick-start-btn:hover, .explore-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 75, 43, 0.4);
}

.action-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 30px;
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

  .info-boxes {
    flex-direction: column;
    gap: 10px;
  }

  .info-box {
    width: 100%;
  }
}
</style>