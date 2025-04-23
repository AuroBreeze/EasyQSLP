import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router'

const router = createRouter({
  history: process.env.NODE_ENV === 'production' ? createWebHashHistory() : createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'start',
      component: () => import('../views/StartView.vue'),
      meta: {
        title: '欢迎来到EasyQFLP'
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Loginview.vue'),
      meta: {
        title: '登录EasyQFLP'
    }
  },
  ],
})

export default router
