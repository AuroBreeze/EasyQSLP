# API 配置文档

## 概述

本目录包含了项目的API配置文件，支持多环境配置和真实后端接口调用。

## 文件说明

### `env.ts` - 环境配置
- 管理不同环境（开发/生产/测试）的配置
- 自动检测当前运行环境
- 提供环境相关的配置参数

### `api.ts` - API 配置
- 定义API端点和配置信息
- 提供URL构建工具函数
- 整合环境配置

## 使用方法

### 1. 基础API调用

```typescript
import { getUserApiUrl } from '@/config/api'

// 获取登录接口URL
const loginUrl = getUserApiUrl('LOGIN')
// 返回: http://113.44.174.216:8000/api/v1/user/login/
```

### 2. 使用真实API服务

```typescript
import { apiLogin, apiSendRegisterCode } from '@/services/realApi'

// 用户登录
try {
  const result = await apiLogin({
    email: 'user@example.com',
    password: 'password123'
  })
  console.log('登录成功:', result)
} catch (error) {
  console.error('登录失败:', error)
}

// 发送注册验证码
try {
  const result = await apiSendRegisterCode('user@example.com')
  console.log('验证码已发送:', result.code)
} catch (error) {
  console.error('发送失败:', error)
}
```

### 3. 环境配置

在不同环境中，API会自动使用对应的后端地址：

- **开发环境**: `http://113.44.174.216:8000`
- **生产环境**: `https://your-production-api.com` （待配置）
- **测试环境**: `http://localhost:8000`

### 4. 切换环境

修改 `env.ts` 中的配置：

```typescript
const envConfigs: Record<Environment, Partial<EnvConfig>> = {
  development: {
    apiBaseUrl: 'http://新的开发环境地址:8000',
    debugMode: true,
  },
  // ...其他环境配置
}
```

## API 接口列表

根据后端文档，当前支持的接口：

| 功能 | 端点 | 方法 | 说明 |
|------|------|------|------|
| 用户登录 | `/api/v1/user/login/` | POST | 邮箱密码登录 |
| 用户注册 | `/api/v1/user/register/` | POST | 邮箱注册（需验证码） |
| 发送验证码 | `/api/v1/user/emailsendcode/` | POST | 发送邮箱验证码 |
| 获取JWT | `/api/v1/user/token/` | POST | 获取访问令牌 |
| 刷新JWT | `/api/v1/user/token/refresh/` | POST | 刷新访问令牌 |
| 验证JWT | `/api/v1/user/token/verify/` | POST | 验证令牌有效性 |

## 验证码用途类型

```typescript
// 在发送验证码时使用
API_CONFIG.CODE_USAGE.REGISTER        // "Register" - 注册
API_CONFIG.CODE_USAGE.FORGOT_PASSWORD // "ResetPassword" - 忘记密码
API_CONFIG.CODE_USAGE.RESET_PASSWORD  // "ResetPassword" - 重置密码
```

## 错误处理

API调用会返回统一的错误格式：

```typescript
{
  success: false,
  message: "错误描述",
  errors: {
    ValidationError: "具体错误信息"
  }
}
```

常见HTTP状态码：
- `200` - 成功
- `201` - 创建成功
- `400` - 请求参数错误
- `401` - 未授权
- `429` - 请求过于频繁
- `500` - 服务器错误

## 调试模式

在开发环境中，控制台会输出当前环境配置信息，方便调试。

## 注意事项

1. 后端IP地址 `http://113.44.174.216:8000` 是临时地址，后续会更改
2. 生产环境的API地址需要在部署前配置
3. 所有API调用都应该进行适当的错误处理
4. 验证码有效期和频率限制请参考后端API文档
