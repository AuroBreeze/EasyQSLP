/**
 * API调用演示
 * 验证验证码发送API的正确格式
 */

import { apiSendRegisterCode, apiSendEmailCode } from '@/services/realApi'
import { API_CONFIG } from '@/config/api'

// 演示正确的API调用格式
export function demonstrateAPICall() {
  console.log('📋 验证码发送API调用格式演示')
  console.log('==================================')
  
  console.log('🎯 API端点:', '/api/v1/user/emailsendcode/')
  console.log('📤 HTTP方法:', 'POST')
  console.log('📄 请求体格式:')
  
  const demoPayload = {
    email: "test@example.com",
    usage: "Regist"  // 注册验证码
  }
  
  console.log(JSON.stringify(demoPayload, null, 2))
  
  console.log('\n🔧 当前配置:')
  console.log('CODE_USAGE.REGISTER:', API_CONFIG.CODE_USAGE.REGISTER)
  
  console.log('\n✅ 实际调用时会发送:')
  const actualPayload = {
    email: "user@example.com",
    usage: API_CONFIG.CODE_USAGE.REGISTER
  }
  console.log(JSON.stringify(actualPayload, null, 2))
  
  console.log('\n🚀 可以通过以下方式调用:')
  console.log('await apiSendRegisterCode("user@example.com")')
  console.log('或')
  console.log('await apiSendEmailCode({ email: "user@example.com", usage: "Regist" })')
}

// 在浏览器控制台中可用的全局函数
if (typeof window !== 'undefined') {
  (window as any).demonstrateAPI = demonstrateAPICall
}
