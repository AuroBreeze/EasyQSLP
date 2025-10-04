/**
 * Usage参数测试工具
 * 用于测试不同的usage值以找到正确的参数
 */

import { apiSendEmailCode } from '@/services/realApi'

// 可能的usage值列表
const POSSIBLE_USAGE_VALUES = [
  'Regist',
  'Register', 
  'REGIST',
  'REGISTER',
  'regist',
  'register',
  'Registration',
  'REGISTRATION',
  'registration',
  'signup',
  'SIGNUP',
  'SignUp'
]

/**
 * 测试不同的usage值
 * @param email 测试邮箱
 */
export async function testUsageValues(email: string = 'test@example.com') {
  console.log('🧪 开始测试不同的usage值...')
  
  for (const usage of POSSIBLE_USAGE_VALUES) {
    console.log(`\n🔍 测试 usage: "${usage}"`)
    
    try {
      const result = await apiSendEmailCode({
        email,
        usage
      })
      
      console.log(`✅ 成功！正确的usage值是: "${usage}"`)
      console.log('响应:', result)
      return usage
      
    } catch (error: any) {
      if (error.message.includes('usage参数错误')) {
        console.log(`❌ usage: "${usage}" - 参数错误`)
      } else if (error.message.includes('发送频率过快')) {
        console.log(`⚠️ usage: "${usage}" - 可能正确，但发送频率过快`)
        return usage
      } else {
        console.log(`❌ usage: "${usage}" - 其他错误:`, error.message)
      }
    }
    
    // 避免频率限制，等待1秒
    await new Promise(resolve => setTimeout(resolve, 1000))
  }
  
  console.log('❌ 所有usage值都测试失败')
  return null
}

// 导出到全局供控制台使用
if (typeof window !== 'undefined') {
  (window as any).testUsageValues = testUsageValues
}
