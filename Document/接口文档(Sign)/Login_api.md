---
title: sign-接口文档
date: 2025-04-12 19:20:00
tags: [Login, API]
---

# sign-接口文档

> [!NOTE]
> **请求与响应格式说明**
> - 请求参数：JSON格式
> - 响应参数：JSON格式
> - 所有接口需携带 `Content-Type: application/json` 请求头

---

## 登录接口 [Login]

### 接口基本信息

| 属性 | 值                     |
|------|-----------------------|
| 接口名称 | 用户登录                  |
| 请求方法 | POST                  |
| 接口版本 | v1                    |
| 接口路径 | `/api/v1/user/login/` |
| 更新时间 | 2025-04-12            |
| 响应字符 | 200 或 400             |

---

### 请求参数说明

#### 请求体参数

| 字段名 | 类型 | 必填 | 描述 | 示例值 |
|--------|------|------|------|-------|
| email | string | 是 | 用户邮箱 | test@test.com |
| password | string | 是 | 用户密码 | 123456 |

#### 请求示例

```json
{
  "email": "test@test.com",
  "password": "123456"
}
```

---

### 响应参数

成功响应参数：

| 字段       | 类型     | 说明   | 存在情况 |
|----------|--------|------| ---- |
| success  | bool   | 状态码  | 总是 |
| message  | string | 状态信息 | 总是 |
| username | string | 用户名称 | 总是 |



成功响应示例：

```json
{
    "success": True, 
    "message": "Login successful", 
    "username": "test"
}
```

失败响应参数：

| 字段              | 类型 | 说明 | 存在情况 |
|-----------------| ---- | ---- | ---- |
| success         | bool | 状态码 | 总是 |
| message         | string | 状态信息 | 总是 |
| errors          | string | 错误信息 | 邮箱错误、密码错误、验证错误 |
| email           | string | 邮箱错误 | 邮箱未填写或邮箱格式错误 |
| password        | string | 密码错误 | 密码未填写 |
| ValidationError | string | 验证错误 | 邮箱或密码错误 |


失败响应示例(未触发验证错误)：
```json
{
    "success": False,
     "message": "Invalid credentials", 
     "errors": {
        "email": "邮箱不能为空", 
        "password": "密码不能为空"
        }
}
```

失败响应示例(触发验证错误)：
```json
{
    "success": False,
    "message": "Invalid credentials",
    "errors": {
        "ValidationError": "邮箱或密码错误"
    }
}
```

## 用户认证toekn获取接口[JWT Token]

### 接口基本信息

| 属性 | 值                     |
|------|-----------------------|
| 接口名称 | 获取用户认证toekn           |
| 请求方法 | POST                  |
| 接口版本 | v1                    |
| 接口路径 | `/api/v1/user/token/` |
| 更新时间 | 2025-04-23            |
| 响应字符 | 200 或 401             |
---

### 请求参数说明
| 字段名 | 类型 | 必填 | 描述 | 示例值 |
|--------|------|------|------|-------|
| email | string | 是 | 用户邮箱 | test@test.com |
| password | string | 是 | 用户密码 | 123456 |
---

### 响应参数
| 字段       | 类型     | 说明   | 存在情况 |
|--------|------|------|------|-------|
| access | string | 访问令牌 | 总是 |
| refresh | string | 刷新令牌 | 总是 |
| detail | string | 提示信息 | 账户不存在 |
---

### 请求示例
```json
{
  "email": "test@test.com",
  "password": "123456"
}
```

### 响应示例

成功响应示例:
```json
{
"access":"hajkajklsdhflkasjdf",
"refres":"fasjkdfjalksfa;sldjk"
}
```

失败响应示例:
```json
{
"detail": "No active account found with the given credentials"
}
```
---

## 用户认证token刷新接口 [JWTRefreshToken]

### 接口基本信息
| 属性 | 值
|------|------|
| 接口名称 | 刷新用户认证token           |
| 请求方法 | POST                  |
| 接口版本 | v1                    |
| 接口路径 | `/api/v1/user/token/refresh/` |
| 更新时间 | 2025-04-23            |
| 响应字符 | 200 或 401             |
---

### 请求体参数
| 字段名 | 类型 | 必填 | 描述 | 示例值 |
|--------|------|-----|------|-------|
| refresh | string | 是 | 刷新令牌 | 刷新令牌 |
---

### 响应参数
| 字段       | 类型     | 说明   | 存在情况 |
|--------|------|------|------|-------|
| access | string | 访问令牌 | 输入正确refresh |
| refresh | string | 是 | 刷新令牌 | 输入正确refresh |
| detail | string | 提示信息 | 输入错误refresh |
| code | string | 错误码 | 输入错误refresh |
---

### 请求示例
```json
{
  "refresh": "refresh_token"
}
```
### 响应示例

成功响应示例:
```json
{
  "access": "access_token",
  "refresh": "refresh_token"
}
```

失败响应示例:
```json
{'detail': 'Token is invalid', 'code': 'token_not_valid'}
```
---

## 用户认证token验证接口 [JWTVerifyToken]

### 接口基本信息

| 属性 | 值                     |
|------|-----------------------|
| 接口名称 | 验证用户认证token           |
| 请求方法 | POST                  |
| 接口版本 | v1                    |
| 接口路径 | `/api/v1/user/token/verify/` |
| 更新时间 | 2025-04-23            |
| 响应字符 | 200 或 401             |
---

### 请求参数说明
| 字段名   | 类型 | 必填 | 描述 | 示例值 |
|-------|------|-----|------|-------|
| token | string | 是 | 访问令牌 | access_token |
---

### 响应参数
| 字段       | 类型     | 说明   | 存在情况 |
|--------|------|------|------|-------|
| detail | string | 提示信息 | 输入错误access |
| code | string | 错误码 | 输入错误access |
| token | string | 访问令牌 | 请求数据未携带token |

---

### 请求示例
```json
{
  "token": "access_token"
}
```

### 响应示例

成功响应示例:
```json
{
}
```

失败响应示例:
```json
  {'detail': 'Token is invalid', 'code': 'token_not_valid'}
```

---

## 验证码接口 [EmailSendCode]

### 接口基本信息

| 属性 | 值                             |
|------|-------------------------------|
| 接口名称 | 获取验证码                         |
| 请求方法 | POST                          |
| 接口版本 | v1                            |
| 接口路径 | `/api/v1/user/emailsendcode/` |
| 更新时间 | 2025-04-23                    |
| 响应字符 | 200 或 401                     |

---

### 请求参数说明

#### 请求体参数

| 字段名 | 类型 | 必填 | 描述 | 示例值                |
|--------|------|------|------|--------------------|
| email | string | 是 | 用户邮箱 | test@test.com      |
| usage | string | 是 | 用途 | Register or ResetPassword |
---

#### 请求示例

```json
{
  "email": "test@test.com",
  "usage": "Register"
}
```

---
### 响应参数

成功响应参数：

| 字段 | 类型 | 说明 | 存在情况 |
| ---- | ---- | ---- | ---- |
| success | bool | 状态码 | 总是 |
| message | string | 状态信息 | 总是 |

成功响应示例：
```json
{
    "success": True,
    "message": "Verification code sent successfully!"
}
```


失败响应参数：

| 字段              | 类型 | 说明 | 存在情况 |
|-----------------| ---- | ---- | ---- |
| success         | bool | 状态码 | 总是 |
| message         | string | 状态信息 | 总是 |



失败响应示例(触发验证错误)：
```json
{
    "success": False,
    "message": "Invalid input",
    "errors": {
        "ValidationError": "邮箱或验证码错误"
    }
}
```

## 注册接口 [Register]

### 接口基本信息

| 属性 | 值                        |
|------|--------------------------|
| 接口名称 | 用户注册                     |
| 请求方法 | POST                     |
| 接口版本 | v1                       |
| 接口路径 | `/api/v1/user/register/` |
| 更新时间 | 2025-04-16               |
| 响应字符 | 200 或 400                |

---

### 请求参数说明

#### 请求体参数

| 字段名 | 类型 | 必填 | 描述 | 示例值 |
|--------|-------|-----|------|-------|
| email | string | 是 | 用户邮箱 | test@test.com |
| password | string | 是 | 用户密码 | 123456 |
| username | string | 是 | 用户昵称 | AuroBree110 |
| code | string | 是 | 验证码 | 495261 |
| usage | string | 是 | 用途 | Register |

---

#### 请求示例

```json
{
    "email": "13122313@qq.com",
    "password": "123123123",
    "username": "AuroBree110",
    "code": "495261",
    "usage": "Register"
}
```
---

### 响应参数

成功响应参数：

| 字段 | 类型 | 说明 | 存在情况 |
| ---- | ---- | ---- | ---- |
| success | bool | 状态码 | 总是 |
| message | string | 状态信息 | 总是 |

成功响应示例：
```json
{"success": True, "message": "User registered successfully!"}
```

失败响应参数：

| 字段              | 类型 | 说明 | 存在情况 |
|-----------------| ---- | ---- | ---- |
| success         | bool | 状态码 | 总是 |
| message         | string | 状态信息 | 总是 |
| errors          | string | 错误信息 | 邮箱错误、密码错误、验证码错误、用户名错误、验证错误 |
| email           | string | 邮箱错误 | 邮箱未填写或邮箱格式错误 |
| password        | string | 密码错误 | 密码未填写 |
| code            | string | 验证码错误 | 验证码未填写或验证码错误 |
| username        | string | 用户名错误 | 用户名未填写或用户名格式错误 |
| ValidationError | string | 验证错误 | 邮箱或密码错误、验证码错误、用户名错误 |

失败响应示例(未触发验证错误)：
```json
{
    "success": False,
    "message": "Invalid input",
    "errors": {
        "email": "邮箱不能为空",
    }
}
```

## 忘记密码接口 [ResetPassword]

### 接口基本信息

| 属性 | 值                             |
|------|----------|
| 接口名称 | 忘记密码                          |
| 请求方法 | POST                          |
| 接口版本 | v1                            |
| 接口路径 | `/api/v1/user/resetpassword/` |
| 更新时间 | 2025-04-17                    |
| 响应字符 | 200 或 400                      |

---

### 请求参数说明

#### 请求体参数

| 字段名 | 类型 | 必填 | 描述 | 示例值 |
|--------|-------|-----|------|-------|
| email | string | 是 | 用户邮箱 | test@test.com |
| code | string | 是 | 验证码 | 495261 |
| password | string | 是 | 用户密码 | 123456 |
| password_confirm | string | 是 | 用户密码确认 | 123456 |

--- 

#### 请求示例

```json
{
    "email": "13122313@qq.com",
    "code": "495261",
    "password": "123123123",
    "password_confirm": "123123123"
}   
```

---

### 响应参数

成功响应参数：

| 字段 | 类型 | 说明 | 存在情况 |
| ---- | ---- |
| success | bool | 状态码 | 总是 |
| message | string | 状态信息 | 总是 |

成功响应示例：
```json
{
    "success": True,
    "message": "Password reset successfully!"
}
```

失败响应参数：

| 字段              | 类型 | 说明 | 存在情况 |
|-----------------| ---- | ---- | ---- |
| success         | bool | 状态码 | 总是 |
| message         | string | 状态信息 | 总是 |
| errors          | string | 错误信息 | 邮箱错误、验证码错误、密码错误、验证错误 |
| email           | string | 邮箱错误 | 邮箱未填写或邮箱格式错误 |
| code            | string | 验证码错误 | 验证码未填写或验证码错误 |
| password        | string | 密码错误 | 密码未填写或密码格式错误 |
| password_confirm | string | 密码确认错误 | 密码确认未填写或密码确认格式错误 |
| ValidationError | string | 验证错误 | 邮箱或验证码错误、密码错误、密码确认错误 |

失败响应示例(未触发验证错误)：
```json
{
    "success": False,
    "message": "Invalid input",
    "errors": {
        "email": ["邮箱不能为空"],
        "password": ["密码不能为空"],
        "password_confirm": ["密码确认不能为空"]
    }
}
```






