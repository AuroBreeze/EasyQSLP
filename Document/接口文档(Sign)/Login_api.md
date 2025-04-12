---
title: 用户登录接口文档
date: 2025-04-12 19:20:00
tags: [Login, API]
---

# 用户登录接口文档

> [!NOTE]
> **请求与响应格式说明**
> - 请求参数：JSON格式
> - 响应参数：JSON格式
> - 所有接口需携带 `Content-Type: application/json` 请求头

---

## 登录接口 [Login]

### 接口基本信息

| 属性 | 值 |
|------|----|
| 接口名称 | 用户登录 |
| 请求方法 | POST |
| 接口版本 | v1 |
| 接口路径 | `/api/v1/user/login/` |
| 更新时间 | 2025-04-12 |

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

| 字段 | 类型 | 说明 | 存在情况 |
| ---- | ---- | ---- | ---- |
| success | bool | 状态码 | 总是 |
| message | string | 状态信息 | 总是 |
| user_id | int | 用户ID | 总是 |

成功响应示例：

```json
{
    "success": True, 
    "message": "Login successful", 
    "user_id": 1
}
```

失败响应参数：

| 字段 | 类型 | 说明 | 存在情况 |
| ---- | ---- | ---- | ---- |
| success | bool | 状态码 | 总是 |
| message | string | 状态信息 | 总是 |
| error | string | 错误信息 | 邮箱错误、密码错误、验证错误 |
| email | string | 邮箱错误 | 邮箱未填写或邮箱格式错误 |
| password | string | 密码错误 | 密码未填写 |
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

