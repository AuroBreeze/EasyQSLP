import http from '@/utils/base/http'

// Note: Ensure the backend includes apps.projectmanage.manage.urls at a proper prefix, e.g., '/project/'.
// Endpoints expected from backend (apps/projectmanage/manage/urls.py):
// - GET /project/article/:id/
// - POST /project/articletest (create)

export interface ArticlePayload {
  title: string
  content_md: string
  project?: number | null
}

export interface ArticleResponse {
  title: string
  content_html: string
  create_time: string
  update_time: string
  toc: string
  word_count: number
  project: number | null
}

export function getArticle(id: number) {
  return http.get(`/project/article/${id}/`)
}

export function createArticle(data: ArticlePayload) {
  return http.post('/project/articletest', data)
}
