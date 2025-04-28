const BASE_URL = 'http://localhost:8000'

interface ApiError {
  success: boolean;
  message: string;
  error?: any;
}
async function request(url: string, options: RequestInit = {}): Promise<any> {
  // 设置请求头
  const headers = new Headers(options.headers || {});
  const token = localStorage.getItem('token');
  if (token) {
    headers.append('Authorization', `Bearer ${token}`);
  }
  
  // 添加超时处理
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000);
  
  try {
    const response = await fetch(`${BASE_URL}${url}`, {
      ...options,
      headers,
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    // 统一处理响应
    const data = await response.json();
    if (response.status === 400) {
      return data; // 返回400响应数据，不抛出错误
    }
    
    if (!response.ok) {
      let errorData;
      try {
        errorData = data;
      } catch {
        errorData = { message: `HTTP错误: ${response.status}` };
      }
      const error: ApiError = errorData;
      throw error;
    }
    
    return data;
  } catch (error) {
    clearTimeout(timeoutId);
    
    // 处理AbortError (超时)
    if (error instanceof DOMException && error.name === 'AbortError') {
      console.error('请求超时');
      throw new Error('请求超时');
    }
    
    // 处理ApiError
    if (error instanceof Error) {
      // 处理401未授权
      if (error.message.includes('401')) {
        // 跳转到登录页的逻辑
      }
      
      //console.error('API Error:', error);
      throw error;
    }
    //console.error('未知错误1231231:'+ error);
    throw error
    
  }
}

export default {
  get(url: string) {
    return request(url, { method: 'GET' })
  },
  post(url: string, data: any) {
    return request(url, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-Type': 'application/json' }
    })
  }
}
