/**
 * 配置文件统一导出
 */

// 环境配置
export { ENV, getCurrentEnv, getEnvConfig } from './env'

// API配置
export { API_CONFIG, buildApiUrl, getUserApiUrl } from './api'

// 导入配置对象以便重新导出
import { ENV as envConfig } from './env'
import { API_CONFIG as apiConfig } from './api'

// 导出默认配置对象
export default {
  ENV: envConfig,
  API_CONFIG: apiConfig,
}
