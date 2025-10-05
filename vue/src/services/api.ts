/*
  虚构 API（前端模拟后端调用）
  - 所有函数返回 Promise，并带可配置延迟
  - 便于在不改动后端（Django）情况下联调前端
*/

import { highlights } from '@/data/shows'
import { mockUsers, MockUser } from '@/database/users'

// 简单的数据类型（可按需扩展）
export interface TopicItem {
  id: string
  tag: string
  title: string
  subtitle: string
  description: string
  backdrop: string
  poster: string
  readingTime: string
  difficulty: string
  updated: string
  topics: string[]
}

// 通用的延迟封装
export function simulate<T>(data: T, delay = 500): Promise<T> {
  return new Promise((resolve) => setTimeout(() => resolve(structuredClone(data)), delay))
}

// 生成占位响应（成功）
export function ok<T>(data: T) {
  return { ok: true as const, data }
}

// 生成占位响应（失败）
export function fail(message = '暂不可用', code = 500) {
  return { ok: false as const, error: { code, message } }
}

export interface AuthUser {
  id: string
  name: string
  email: string
  avatar?: string
  role?: string
  organization?: string
  lastActiveAt?: string
}

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  name: string
  email: string
  password: string
}

function sanitizeUser(user: MockUser): AuthUser {
  const { id, name, email, avatar, role, organization, lastActiveAt } = user
  return { id, name, email, avatar, role, organization, lastActiveAt }
}

function createToken(user: MockUser) {
  return `token_${user.id}_${Math.random().toString(36).slice(2, 10)}`
}

export async function apiLogin(payload: LoginPayload, delay = 600) {
  const { email, password } = payload
  const user = mockUsers.find((u) => u.email === email.toLowerCase())
  if (!user || user.password !== password) {
    return simulate(fail('邮箱或密码错误', 401), delay)
  }
  return simulate(ok({ token: createToken(user), user: sanitizeUser(user) }), delay)
}

export async function apiRegister(payload: RegisterPayload, delay = 700) {
  const email = payload.email.toLowerCase()
  const exists = mockUsers.some((u) => u.email === email)
  if (exists) {
    return simulate(fail('该邮箱已被注册', 409), delay)
  }
  const newUser: MockUser = {
    id: `u-${Date.now()}`,
    name: payload.name,
    email,
    password: payload.password,
    avatar: `https://i.pravatar.cc/120?u=${encodeURIComponent(email)}`,
    role: '新晋创作者',
    organization: '自由节点网络',
    lastActiveAt: new Date().toISOString(),
  }
  mockUsers.push(newUser)
  return simulate(ok({ token: createToken(newUser), user: sanitizeUser(newUser) }), delay)
}

// 示例：获取首页高亮专题
export async function apiGetHighlights(delay = 500) {
  return simulate(ok(highlights as TopicItem[]), delay)
}

// 示例：获取历史记录（取前 6 个作为占位）
export async function apiGetHistory(delay = 400) {
  const data = (highlights as TopicItem[]).slice(0, 6)
  return simulate(ok(data), delay)
}

// 示例：获取推荐（简单打乱顺序后取 12 个）
export async function apiGetRecommendations(delay = 500) {
  const arr = [...(highlights as TopicItem[])]
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[arr[i], arr[j]] = [arr[j], arr[i]]
  }
  return simulate(ok(arr.slice(0, 12)), delay)
}

// 示例：根据 ID 获取专题详情
export async function apiGetTopicById(id: string, delay = 400) {
  const item = (highlights as TopicItem[]).find((x) => x.id === id)
  if (!item) return simulate(fail('未找到专题', 404), delay)
  return simulate(ok(item), delay)
}

// 示例：搜索（简单标题/副标题包含）
export async function apiSearchTopics(query: string, delay = 600) {
  const q = (query || '').trim().toLowerCase()
  if (!q) return simulate(ok([] as TopicItem[]), delay)
  const res = (highlights as TopicItem[]).filter(
    (x) => x.title.toLowerCase().includes(q) || x.subtitle.toLowerCase().includes(q),
  )
  return simulate(ok(res), delay)
}

// 通用占位：GET/POST（便于未来替换为真实 http 客户端）
export async function get<T = unknown>(url: string, params?: Record<string, unknown>, delay = 300) {
  console.debug('[mock:get]', url, params)
  return simulate(ok({ url, params }) as unknown as T, delay)
}

export async function post<T = unknown>(url: string, body?: unknown, delay = 300) {
  console.debug('[mock:post]', url, body)
  return simulate(ok({ url, body }) as unknown as T, delay)
}
