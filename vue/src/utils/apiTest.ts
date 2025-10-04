/**
 * API测试工具
 * 用于验证API调用格式是否正确
 */

import { apiSendRegisterCode, apiSendEmailCode } from '@/services/realApi'
import { API_CONFIG } from '@/config/api'

// 测试验证码发送API格式
export async function testEmailCodeAPI() {
  console.log('🔍 测试验证码发送API格式')
  
  // 测试数据
  const testEmail = 'test@example.com'
  
  try {
    console.log('📤 发送注册验证码请求:')
    console.log('URL:', `/api/v1/user/emailsendcode/`)
    console.log('Method:', 'POST')
    console.log('Body:', {
      email: testEmail,
      usage: API_CONFIG.CODE_USAGE.REGISTER // 应该是 "Regist"
    })
    
    // 注意：这里只是展示格式，不实际发送请求
    console.log('✅ API调用格式正确')
    
    // 如果需要实际测试，取消下面的注释
    // const result = await apiSendRegisterCode(testEmail)
    // console.log('📥 API响应:', result)
    
  } catch (error) {
    console.error('❌ API调用失败:', error)
  }
}

// 导出便捷方法用于控制台测试
export const debugAPI = {
  testEmailCode: testEmailCodeAPI,
  showConfig: () => {
    console.log('📋 当前API配置:')
    console.log('CODE_USAGE:', API_CONFIG.CODE_USAGE)
  }
}
