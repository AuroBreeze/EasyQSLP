// API 配置文件
import { ENV } from './env'

export const API_CONFIG = {
  // 后端基础URL（根据环境自动配置）
  BASE_URL: ENV.apiBaseUrl,
  
  // API 版本前缀
  API_PREFIX: '/api/v1',
  
  // 用户相关接口
  USER_ENDPOINTS: {
    LOGIN: '/user/login/',
    REGISTER: '/user/register/',
    EMAIL_SEND_CODE: '/user/emailsendcode/',
    EMAIL_EXIST_CHECK: '/user/account/exist/',
    TOKEN_GET: '/user/token/',
    TOKEN_REFRESH: '/user/token/refresh/',
    TOKEN_VERIFY: '/user/token/verify/',
  },
  
  // 请求配置
  REQUEST_CONFIG: {
    timeout: 10000, // 10秒超时
    headers: {
      'Content-Type': 'application/json',
    },
  },
  
  // 验证码用途类型
  CODE_USAGE: {
    REGISTER: 'Register', // 根据更新的API文档
    FORGOT_PASSWORD: 'ResetPassword', // 根据更新的API文档
    RESET_PASSWORD: 'ResetPassword', // 根据更新的API文档
  },
  
  // HTTP状态码
  STATUS_CODES: {
    SUCCESS: 200,
    CREATED: 201,
    BAD_REQUEST: 400,
    UNAUTHORIZED: 401,
    FORBIDDEN: 403,
    NOT_FOUND: 404,
    TOO_MANY_REQUESTS: 429,
    INTERNAL_SERVER_ERROR: 500,
  },
}

// 构建完整的API URL
export const buildApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.BASE_URL}${API_CONFIG.API_PREFIX}${endpoint}`
}

// 获取用户接口URL
export const getUserApiUrl = (endpointKey: keyof typeof API_CONFIG.USER_ENDPOINTS): string => {
  return buildApiUrl(API_CONFIG.USER_ENDPOINTS[endpointKey])
}

// 导出默认配置
export default API_CONFIG
