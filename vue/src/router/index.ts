import { createRouter, createWebHistory } from 'vue-router'
import StartView from '../views/StartView.vue'
import Loginview from '../views/Loginview.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'start',
      component: StartView
    },
    {
      path: '/login',
      name: 'login',
      component: Loginview
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true },
      props: true
    }
  ]
})

// 添加路由守卫检查认证
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
