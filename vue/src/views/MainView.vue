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

      <main class="main" ref="mainRef">
        <div class="toolbar">
          <router-link class="btn" to="/project/create">+ 创建项目</router-link>
          <router-link class="btn outline" to="/article/upload">发布文章</router-link>
        </div>

        <div class="grid" ref="gridRef">
          <ProjectCard v-for="p in feed" :key="p.id" :project="p"
                       @open="openProject(p.id)" @like="likeProject(p.id)" @star="starProject(p.id)"
                       @hover="onCardHover" />
          <div v-if="hoverProject" class="hover-panel" :style="hoverStyle">
            <h4 class="hp-title">{{ hoverProject.title }}</h4>
            <p class="hp-intro">{{ hoverProject.introduction || '暂无简介' }}</p>
            <div class="hp-meta">
              <span>👍 {{ hoverProject.likes_count ?? 0 }}</span>
              <span>⭐ {{ hoverProject.stars_count ?? 0 }}</span>
              <span>👁️ {{ hoverProject.views ?? 0 }}</span>
            </div>
            <div v-if="hoverProject.tags?.length" class="hp-tags">
              <span v-for="(t,i) in hoverProject.tags" :key="i" class="hp-tag">{{ t }}</span>
            </div>
          </div>
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
const mainRef = ref<HTMLElement | null>(null)
const gridRef = ref<HTMLElement | null>(null)
const hoverProject = ref<ProjectLite | null>(null)
const hoverStyle = ref<Record<string, string>>({})

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

function onCardHover(payload: { project: ProjectLite | null; rect?: DOMRect }) {
  if (!mainRef.value || !gridRef.value) return
  const container = mainRef.value
  const containerRect = container.getBoundingClientRect()
  if (!payload.project || !payload.rect) {
    hoverProject.value = null
    return
  }
  hoverProject.value = payload.project
  const scrollTop = container.scrollTop
  const scrollLeft = container.scrollLeft
  const top = payload.rect.top - containerRect.top + scrollTop
  const left = payload.rect.right - containerRect.left + scrollLeft + 12
  const panelWidth = 320
  // 边界处理：若超出容器右侧，则贴在卡片左侧
  const maxLeft = container.scrollWidth - panelWidth - 12
  const finalLeft = Math.min(left, maxLeft)
  hoverStyle.value = {
    position: 'absolute',
    top: `${Math.max(top, 0)}px`,
    left: `${finalLeft}px`,
    width: `${panelWidth}px`,
  }
}
</script>

<style scoped>
.layout { width: 95vw; max-width: 1440px; margin: 0 auto; }
.content { display: grid; grid-template-columns: 320px 1fr; gap: 20px; padding: 16px 20px; }
.left { display: grid; gap: 12px; align-content: start; }
.main { min-height: calc(100vh - 112px); max-height: calc(100vh - 112px); overflow: auto; position: relative; background: #f8fafc; border: 1px solid #eef2f7; border-radius: 12px; padding: 12px; }
.toolbar { display: flex; gap: 8px; margin-bottom: 12px; }
.btn { padding: 6px 12px; border: 1px solid #2563eb; color: #2563eb; background: transparent; text-decoration: none; border-radius: 6px; }
.btn.outline { border-style: dashed; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; position: relative; }
.hover-panel { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; box-shadow: 0 12px 28px rgba(0,0,0,.12); padding: 14px; pointer-events: none; }
.hp-title { margin: 0 0 6px; font-size: 16px; }
.hp-intro { margin: 0 0 8px; color: #444; font-size: 14px; line-height: 1.5; }
.hp-meta { display: flex; gap: 12px; color: #888; font-size: 12px; margin-bottom: 6px; }
.hp-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.hp-tag { background: #f3f4f6; color: #374151; padding: 2px 6px; border-radius: 999px; font-size: 12px; }
@media (max-width: 900px) {
  .layout { width: 100vw; max-width: 100%; }
  .content { grid-template-columns: 1fr; padding: 12px; }
  .grid { grid-template-columns: 1fr; }
}
</style>
