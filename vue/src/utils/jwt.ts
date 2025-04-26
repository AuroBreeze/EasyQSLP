export const parseJWT = (token: string) => {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16).slice(-2)))
        .join('')
    )
    return JSON.parse(jsonPayload)
  } catch (e) {
    console.error('Failed to parse JWT', e)
    return null
  }
}

let isRefreshing = false
let refreshPromise: Promise<string | null> | null = null

export const refreshToken = async (): Promise<string | null> => {
  if (isRefreshing) {
    return refreshPromise
  }

  isRefreshing = true
  try {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) return null

    refreshPromise = fetch('http://localhost:8000/api/v1/token/refresh/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ refresh: refreshToken })
    })
    .then(async response => {
      if (response.ok) {
        const data = await response.json()
        localStorage.setItem('access_token', data.access)
        return data.access
      }
      return null
    })
    .finally(() => {
      isRefreshing = false
      refreshPromise = null
    })

    return await refreshPromise
  } catch (error) {
    console.error('Token refresh failed:', error)
    isRefreshing = false
    return null
  }
}

export const getValidToken = async (): Promise<string | null> => {
  const token = localStorage.getItem('access_token')
  if (!token) return null

  const payload = parseJWT(token)
  if (!payload) return null

  // 提前5分钟刷新token
  const now = Math.floor(Date.now() / 1000)
  if (payload.exp - now < 300) {
    return await refreshToken()
  }

  return token
}

export const getUserIdFromToken = () => {
  const token = localStorage.getItem('access_token')
  if (!token) return null
  const payload = parseJWT(token)
  return payload?.user_id || null
}
