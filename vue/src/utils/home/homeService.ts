// Mock home service for main UI. Replace with real API calls later.
export type ProjectLite = {
  id: number
  title: string
  cover_image?: string | null
  introduction?: string
  likes_count?: number
  stars_count?: number
  views?: number
  owner?: { id: number; username: string }
  maintainers?: number[]
  tags?: string[]
}

export type Announcement = { id: number; title: string; content: string; link?: string; time: string }
export type CategoryNode = { id: number; name: string; children?: CategoryNode[] }
export type ActivityItem = { id: number; type: string; title: string; time: string; link: string }

const mockProjects: ProjectLite[] = Array.from({ length: 12 }).map((_, i) => ({
  id: i + 1,
  title: `示例项目 ${i + 1}`,
  cover_image: null,
  introduction: '这是项目的简短描述，展示前 100 字。',
  likes_count: Math.floor(Math.random() * 100),
  stars_count: Math.floor(Math.random() * 100),
  views: Math.floor(Math.random() * 1000),
  owner: { id: 1, username: 'owner' },
  maintainers: [2, 3, 4],
  tags: ['Python', '前端', '教程'].slice(0, 1 + (i % 3))
}))

const mockHot: ProjectLite[] = mockProjects.slice(0, 5)

const mockAnnouncements: Announcement[] = [
  { id: 1, title: '平台升级维护', content: '本周末进行系统维护...', time: '2025-09-27 12:00', link: '#' },
  { id: 2, title: '新功能上线', content: '文章历史与回滚功能已上线。', time: '2025-09-27 10:00', link: '#' },
]

const mockCategories: CategoryNode[] = [
  { id: 1, name: '技术栈', children: [
    { id: 11, name: 'Python' },
    { id: 12, name: 'JavaScript' },
    { id: 13, name: 'Java' },
  ]},
  { id: 2, name: '项目类型', children: [
    { id: 21, name: '开源' },
    { id: 22, name: '教程' },
    { id: 23, name: '实战' },
  ]},
]

const mockActivities: ActivityItem[] = [
  { id: 1, type: 'create', title: '新项目「EasyQSLP」上线', time: '刚刚', link: '#' },
  { id: 2, type: 'update', title: '项目 A 发布 v1.1', time: '1 小时前', link: '#' },
  { id: 3, type: 'comment', title: '项目 B 收到新评论', time: '昨天', link: '#' },
]

export async function listProjects(params?: { keyword?: string; category?: number; page?: number }) {
  // Simply filter by keyword for mock
  const kw = params?.keyword?.toLowerCase() || ''
  return Promise.resolve({ data: mockProjects.filter(p => p.title.toLowerCase().includes(kw)) })
}

export async function listHotProjects() {
  return Promise.resolve({ data: mockHot })
}

export async function listAnnouncements() {
  return Promise.resolve({ data: mockAnnouncements })
}

export async function getCategoriesTree() {
  return Promise.resolve({ data: mockCategories })
}

export async function listActivities() {
  return Promise.resolve({ data: mockActivities })
}
