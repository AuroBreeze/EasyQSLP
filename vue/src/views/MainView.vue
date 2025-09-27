<template>
  <div class="layout">
    <NavBar @search="onSearch" @createProject="goCreateProject" />
    <Breadcrumbs :items="breadcrumbs" />

    <div class="content">
      <aside class="left">
        <HotProjects :projects="hotProjects" @open="openProject" />
        <Announcements :items="announcements" />
        <Categories :trees="categories" @select="onSelectCategory" />
        <RecentActivities :items="activities" />
      </aside>

      <main class="main">
        <div class="toolbar">
          <router-link class="btn" to="/project/create">+ 创建项目</router-link>
          <router-link class="btn outline" to="/article/upload">发布文章</router-link>
        </div>

        <div class="grid">
          <ProjectCard v-for="p in feed" :key="p.id" :project="p"
                       @open="openProject(p.id)" @like="likeProject(p.id)" @star="starProject(p.id)" />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import NavBar from '@/components/navigation/NavBar.vue'
import Breadcrumbs from '@/components/navigation/Breadcrumbs.vue'
import HotProjects from '@/components/sidebar/HotProjects.vue'
import Announcements from '@/components/sidebar/Announcements.vue'
import Categories from '@/components/sidebar/Categories.vue'
import RecentActivities from '@/components/sidebar/RecentActivities.vue'
import ProjectCard from '@/components/projects/ProjectCard.vue'
import { listProjects, listHotProjects, listAnnouncements, getCategoriesTree, listActivities, type ProjectLite, type Announcement as Ann, type CategoryNode, type ActivityItem } from '@/utils/home/homeService'

const router = useRouter()
const route = useRoute()

const breadcrumbs = ref([{ label: '首页', link: '/main' }])
const hotProjects = ref<ProjectLite[]>([])
const announcements = ref<Ann[]>([])
const categories = ref<CategoryNode[]>([])
const activities = ref<ActivityItem[]>([])
const feed = ref<ProjectLite[]>([])

async function loadData() {
  const kw = String(route.query.keyword || '')
  const cat = Number(route.query.category || 0) || undefined
  const [{ data: hot }, { data: anns }, { data: cats }, { data: acts }, { data: items }] = await Promise.all([
    listHotProjects(),
    listAnnouncements(),
    getCategoriesTree(),
    listActivities(),
    listProjects({ keyword: kw, category: cat })
  ])
  hotProjects.value = hot
  announcements.value = anns
  categories.value = cats
  activities.value = acts
  feed.value = items
}

function onSearch(keyword: string) {
  router.push({ path: '/main', query: { ...route.query, keyword } })
}

function onSelectCategory(id: number) {
  router.push({ path: '/main', query: { ...route.query, category: id } })
}

function goCreateProject() {
  router.push('/project/create')
}

function openProject(id: number) {
  // TODO: 跳转到项目详情（待实现项目详情页），当前先跳到文章上传/列表占位
  alert(`打开项目 #${id}`)
}

function likeProject(id: number) {
  alert(`点赞项目 #${id}（占位）`)
}

function starProject(id: number) {
  alert(`收藏项目 #${id}（占位）`)
}

onMounted(loadData)
</script>

<style scoped>
.layout { max-width: 1200px; margin: 0 auto; }
.content { display: grid; grid-template-columns: 280px 1fr; gap: 16px; padding: 12px 16px; }
.left { display: grid; gap: 12px; align-content: start; }
.main { min-height: 60vh; }
.toolbar { display: flex; gap: 8px; margin-bottom: 12px; }
.btn { padding: 6px 12px; border: 1px solid #2563eb; color: #2563eb; background: transparent; text-decoration: none; border-radius: 6px; }
.btn.outline { border-style: dashed; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; }
@media (max-width: 900px) {
  .content { grid-template-columns: 1fr; }
}
</style>
