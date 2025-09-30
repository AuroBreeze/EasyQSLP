import { createRouter, createWebHistory } from 'vue-router'
import StartView from '../views/StartView.vue'
import Loginview from '../views/Loginview.vue'
import ProfileView from '../views/ProfileView.vue'
import NotFoundView from '../views/404view.vue'
import ArticleUpload from '../views/ArticleUpload.vue'
import ArticleView from '../views/ArticleView.vue'
import MainView from '../views/MainView.vue'
import ProjectCreate from '../views/ProjectCreate.vue'
import ArticleHistory from '../views/ArticleHistory.vue'
import RevisionDiff from '../views/RevisionDiff.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'start',
      component: StartView
    },
    {
      path: '/main',
      name: 'main',
      component: MainView
    },
    {
      path: '/project/create',
      name: 'project-create',
      component: ProjectCreate
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
      props: true
    },
    {
      path: '/article/upload',
      name: 'article-upload',
      component: ArticleUpload,
    },
    {
      path: '/article/:id',
      name: 'article-view',
      component: ArticleView,
      props: true
    },
    {
      path: '/article/:id/history',
      name: 'article-history',
      component: ArticleHistory,
      props: true
    },
    {
      path: '/revision/:id/diff',
      name: 'revision-diff',
      component: RevisionDiff,
      props: true
    },
    {
      path: '/404view',
      name: '404view',
      component: NotFoundView
    },
  ]
})

// 测试阶段：临时关闭登录校验
// router.beforeEach((to, from, next) => {
//   const token = localStorage.getItem('access_token')
//   if (to.meta.requiresAuth && !token) {
//     next('/login')
//   } else {
//     next()
//   }
// })

export default router
