import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

// 页面按需加载
const Home = () => import('@/pages/Home.vue')
const HomeMain = () => import('@/pages/home/Main.vue')
const HomeSearch = () => import('@/pages/home/Search.vue')
const HomeSeries = () => import('@/pages/home/Series.vue')
const HomeProject = () => import('@/pages/home/project.vue')
const HomeList = () => import('@/pages/home/MyList.vue')
const ArticleDetail = () => import('@/pages/ArticleDetail.vue')
const TopicDetail = () => import('@/pages/TopicDetail.vue')
const Workspace = () => import('@/pages/Workspace.vue')
const Auth = () => import('@/pages/Auth.vue')
const Profile = () => import('@/pages/Profile.vue')
const ProfileBio = () => import('@/pages/profile/Bio.vue')
const ProfileWork = () => import('@/pages/profile/Work.vue')
const ProfileFavorites = () => import('@/pages/profile/Favorites.vue')
const ProfileHistory = () => import('@/pages/profile/History.vue')
const ProfileSettings = () => import('@/pages/profile/Settings.vue')

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: Home,
    children: [
      { path: '', redirect: { name: 'home-main' } },
      { path: 'main', name: 'home-main', component: HomeMain },
      { path: 'search', name: 'home-search', component: HomeSearch },
      { path: 'series', name: 'home-series', component: HomeSeries },
      { path: 'project', name: 'home-project', component: HomeProject },
      { path: 'list', name: 'home-list', component: HomeList },
    ],
  },
  { path: '/article/:id', name: 'article-detail', component: ArticleDetail },
  { path: '/topic/:id', name: 'topic-detail', component: TopicDetail },
  { path: '/workspace', name: 'workspace', component: Workspace },
  { path: '/login', name: 'login', component: Auth },
  { path: '/register', name: 'register', component: Auth, meta: { mode: 'register' } },
  { path: '/auth', name: 'auth', component: Auth },
  {
    path: '/profile',
    name: 'profile',
    component: Profile,
    children: [
      { path: '', redirect: { name: 'profile-bio' } },
      { path: 'bio', name: 'profile-bio', component: ProfileBio },
      { path: 'work', name: 'profile-work', component: ProfileWork },
      { path: 'favorites', name: 'profile-favorites', component: ProfileFavorites },
      { path: 'history', name: 'profile-history', component: ProfileHistory },
      { path: 'settings', name: 'profile-settings', component: ProfileSettings },
    ],
  },
]

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})
