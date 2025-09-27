import http from '@/utils/base/http'

// Backend endpoints are assumed mounted under /project/ per apps/projectmanage/manage/urls.py

export interface RevisionPayload {
  article: number
  content: string
  submitter?: number
  comment?: string
}

export interface ApprovalPayload {
  revision: number
  approver: number
  decision: 'approved' | 'rejected'
}

export function createRevision(data: RevisionPayload) {
  return http.post('/project/revision', data)
}

export function getRevision(id: number) {
  return http.get(`/project/revision/${id}/`)
}

export function approveRevision(data: ApprovalPayload) {
  return http.post('/project/revision/approval', data)
}

export function listRevisions(articleId: number) {
  return http.get(`/project/article/${articleId}/revisions`)
}

export function getRevisionDiff(id: number, params?: { against?: 'prev' | 'current'; mode?: 'unified' | 'html' | 'dmp' }) {
  const against = params?.against ?? 'prev'
  const mode = params?.mode ?? 'unified'
  const qs = `?against=${encodeURIComponent(against)}&mode=${encodeURIComponent(mode)}`
  return http.get(`/project/revision/${id}/diff${qs}`)
}

export function revertRevision(id: number) {
  return http.post(`/project/revision/${id}/revert`, {})
}
