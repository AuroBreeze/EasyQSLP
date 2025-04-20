<template>
  <div class="wave-background"></div>
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
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');


.wave-background {
  position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    --animation-duration: 10s;
    --animation-direction: -1;
    background: linear-gradient(to right, #FF4B2B, #FF416C);
    overflow: hidden;
}

.wave-background::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 200%;
  height: 100%;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255, 255, 255, 0.2)" fill-opacity="1" d="M0,256L48,261.3C96,267,192,277,288,256C384,235,480,181,576,181.3C672,181,768,235,864,250.7C960,267,1056,245,1152,213.3C1248,181,1344,139,1392,117.3L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
  background-repeat: repeat-x;
  background-size: 50% 100%;
  animation: wave var(--animation-duration) linear infinite;
}

@keyframes wave {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}

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
  background-color: #1e3c72;
  color: white;
  border: none;
  box-shadow: 0 4px 15px rgba(30, 60, 114, 0.3);
  margin-bottom: 20px;
  padding: 10px 30px;
  font-size: 1rem;
  min-width: 150px;
}

.quick-start-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(30, 60, 114, 0.4);
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