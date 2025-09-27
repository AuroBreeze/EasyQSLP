import http from '@/utils/base/http'

export interface ProjectPayload {
  title: string
  introduction?: string
}

export interface ProjectResponse {
  title: string
  introduction: string
  status: string
  create_time: string
  update_time: string
  // id is not included by backend serializer currently
}

// Backend full path resolves to /project/project when included under /project/
export function createProject(data: ProjectPayload) {
  return http.post('/project/project', data)
}
