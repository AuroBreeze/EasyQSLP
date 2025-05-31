import { describe, it, expect } from 'vitest'
import tokenService from '../tokenService'

describe('tokenService', () => {
  const testEmail = 'test@example.com'
  const testPassword = '123456789'
  
  it('should get token with valid credentials', async () => {
    const result = await tokenService.GetToken(testEmail, testPassword)
    console.log('GetToken result:', result)
    expect(result).toHaveProperty('accessToken')
    expect(result).toHaveProperty('refreshToken')
  })

  it('should verify valid token', async () => {
    const { accessToken } = await tokenService.GetToken(testEmail, testPassword)
    const result = await tokenService.VerifyToken(accessToken!)
    console.log('VerifyToken result:', result)
    expect(result.verified).toBe(true)
  })

  it('should refresh token', async () => {
    const { refreshToken } = await tokenService.GetToken(testEmail, testPassword)
    const result = await tokenService.RefreshToken(refreshToken!)
    console.log('RefreshToken result:', result)
    expect(result).toHaveProperty('accessToken')
    expect(result).toHaveProperty('refreshToken')
  })
})
