/**
 * 真实后端API服务
 * 基于后端接口文档实现的API调用
 */

import { getUserApiUrl, API_CONFIG } from '@/config/api'

// 接口响应类型定义
export interface ApiResponse<T = any> {
  success: boolean
  message: string
  data?: T
  errors?: Record<string, string>
}

// 用户相关类型定义
export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  email: string
  password: string
  username: string
  code: string
}

export interface EmailCodePayload {
  email: string
  usage: string
}

export interface EmailExistPayload {
  email: string
}

export interface TokenPayload {
  email: string
  password: string
}

export interface RefreshTokenPayload {
  refresh: string
}

export interface VerifyTokenPayload {
  token: string
}

// 响应数据类型
export interface LoginResponse {
  success: true
  message: string
  username: string
  user_id: number
}

export interface TokenResponse {
  refresh: string
  access: string
}

export interface EmailCodeResponse {
  success: true
  message: string
  code: string
}

export interface EmailExistResponse {
  success: true
  message: string
  data: {
    by: string
    value: string
    exists: boolean
  }
}

// HTTP 请求封装
class HttpClient {
  private baseUrl: string
  private defaultHeaders: Record<string, string>

  constructor() {
    this.baseUrl = API_CONFIG.BASE_URL
    this.defaultHeaders = API_CONFIG.REQUEST_CONFIG.headers
  }

  private async request<T>(
    url: string,
    options: RequestInit = {}
  ): Promise<T> {
    const config: RequestInit = {
      ...options,
      headers: {
        ...this.defaultHeaders,
        ...options.headers,
      },
    }

    try {
      const response = await fetch(url, config)
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || `HTTP ${response.status}`)
      }

      return data
    } catch (error) {
      console.error('API 请求错误:', error)
      throw error
    }
  }

  async get<T>(endpoint: string, params?: Record<string, string>): Promise<T> {
    const url = new URL(endpoint, this.baseUrl)
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        url.searchParams.append(key, value)
      })
    }
    return this.request<T>(url.toString(), { method: 'GET' })
  }

  async post<T>(endpoint: string, body?: any): Promise<T> {
    const url = new URL(endpoint, this.baseUrl).toString()
    return this.request<T>(url, {
      method: 'POST',
      body: JSON.stringify(body),
    })
  }
}

// 创建HTTP客户端实例
const httpClient = new HttpClient()

/**
 * 用户登录
 * @param payload 登录信息
 * @returns 登录响应
 */
export async function apiLogin(payload: LoginPayload): Promise<LoginResponse> {
  const url = getUserApiUrl('LOGIN')
  return httpClient.post<LoginResponse>(url, payload)
}

/**
 * 用户注册
 * @param payload 注册信息
 * @returns 注册响应
 */
export async function apiRegister(payload: RegisterPayload): Promise<ApiResponse> {
  const url = getUserApiUrl('REGISTER')
  return httpClient.post<ApiResponse>(url, payload)
}

/**
 * 发送邮箱验证码
 * @param payload 邮箱和用途信息
 * @returns 发送结果
 */
export async function apiSendEmailCode(payload: EmailCodePayload): Promise<EmailCodeResponse> {
  const url = getUserApiUrl('EMAIL_SEND_CODE')
  console.log('📤 发送验证码API调用:', {
    url,
    method: 'POST',
    payload
  })
  return httpClient.post<EmailCodeResponse>(url, payload)
}

/**
 * 检查邮箱是否存在
 * @param payload 邮箱信息
 * @returns 检查结果
 */
export async function apiCheckEmailExist(payload: EmailExistPayload): Promise<EmailExistResponse> {
  const url = getUserApiUrl('EMAIL_EXIST_CHECK')
  return httpClient.post<EmailExistResponse>(url, payload)
}

/**
 * 获取JWT令牌
 * @param payload 用户凭证
 * @returns JWT令牌
 */
export async function apiGetToken(payload: TokenPayload): Promise<TokenResponse> {
  const url = getUserApiUrl('TOKEN_GET')
  return httpClient.post<TokenResponse>(url, payload)
}

/**
 * 刷新JWT令牌
 * @param payload 刷新令牌
 * @returns 新的JWT令牌
 */
export async function apiRefreshToken(payload: RefreshTokenPayload): Promise<TokenResponse> {
  const url = getUserApiUrl('TOKEN_REFRESH')
  return httpClient.post<TokenResponse>(url, payload)
}

/**
 * 验证JWT令牌
 * @param payload 令牌信息
 * @returns 验证结果
 */
export async function apiVerifyToken(payload: VerifyTokenPayload): Promise<ApiResponse> {
  const url = getUserApiUrl('TOKEN_VERIFY')
  return httpClient.post<ApiResponse>(url, payload)
}

// 便捷方法：注册流程相关

/**
 * 发送注册验证码
 * @param email 邮箱地址
 * @returns 发送结果
 */
export async function apiSendRegisterCode(email: string): Promise<EmailCodeResponse> {
  return apiSendEmailCode({
    email,
    usage: API_CONFIG.CODE_USAGE.REGISTER
  })
}

/**
 * 发送忘记密码验证码
 * @param email 邮箱地址  
 * @returns 发送结果
 */
export async function apiSendForgotPasswordCode(email: string): Promise<EmailCodeResponse> {
  return apiSendEmailCode({
    email,
    usage: API_CONFIG.CODE_USAGE.FORGOT_PASSWORD
  })
}

/**
 * 发送重置密码验证码
 * @param email 邮箱地址
 * @returns 发送结果
 */
export async function apiSendResetPasswordCode(email: string): Promise<EmailCodeResponse> {
  return apiSendEmailCode({
    email,
    usage: API_CONFIG.CODE_USAGE.RESET_PASSWORD
  })
}

/**
 * 检查邮箱是否已存在（便捷方法）
 * @param email 邮箱地址
 * @returns 是否存在
 */
export async function checkEmailExists(email: string): Promise<boolean> {
  try {
    const response = await apiCheckEmailExist({ email })
    return response.data.exists
  } catch (error) {
    console.error('检查邮箱存在性失败:', error)
    return false // 默认返回false，避免阻止用户操作
  }
}

export default {
  apiLogin,
  apiRegister,
  apiSendEmailCode,
  apiCheckEmailExist,
  apiGetToken,
  apiRefreshToken,
  apiVerifyToken,
  apiSendRegisterCode,
  apiSendForgotPasswordCode,
  apiSendResetPasswordCode,
  checkEmailExists,
}
