---
title: projectmanage-接口文档
date: 2025-09-27 15:53:00
tags: [Project, Article, API]
---

# projectmanage-接口文档

> [!NOTE]
> 基本说明
> - 请求与响应格式：JSON
> - 默认请求头：`Content-Type: application/json`
> - 认证：GET 接口公开；POST 接口需认证登录（未登录返回 401）。如使用 JWT，请在请求头添加 `Authorization: Bearer <access_token>`。
> - Base Path：本文档接口路径均为相对路径，实际生效路径取决于在 `config/urls.py` 中的挂载位置（例如：`/project/` 或 `/api/v1/project/`）。

---

## 项目接口 [Project]

### 读取项目详情

#### 接口基本信息

| 属性 | 值 |
|------|----|
| 接口名称 | 获取项目详情 |
| 请求方法 | GET |
| 接口版本 | v1 |
| 接口路径 | `project/<int:pk>/` |
| 更新时间 | 2025-09-27 |
| 响应字符 | 200 或 404 |

---

#### 响应参数

由 `ProjectSerializer` 返回，主要字段如下（只读字段见模型与序列化器约束）：

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 项目名称（唯一） |
| cover_image | string | 封面图 URL（如配置） |
| introduction | string | 项目简介 |
| status | string | 项目状态（published/unpublished/suspended/deleted） |
| create_time | datetime | 创建时间 |
| update_time | datetime | 更新时间 |
| owner | int | 项目管理者用户ID |
| collaborator | array[int] | 协作者用户ID 列表（只读） |
| replications | array[int] | 复现用户ID 列表（只读） |
| likes | array[int] | 点赞用户ID 列表（只读） |
| stars | array[int] | 收藏用户ID 列表（只读） |
| short_term_score | float | 短期热度分数（只读） |
| long_term_score | float | 长期热度分数（只读） |
| views | int | 浏览量（只读） |

---

### 创建项目

#### 接口基本信息

| 属性 | 值 |
|------|----|
| 接口名称 | 创建项目 |
| 请求方法 | POST |
| 接口版本 | v1 |
| 接口路径 | `project` |
| 认证 | 需登录（401 未登录） |
| 更新时间 | 2025-09-27 |
| 响应字符 | 201 或 400 |

---

#### 请求体参数

| 字段名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| title | string | 是 | 项目名称（唯一） |
| cover_image | string/file | 否 | 封面图（可为空） |
| introduction | string | 否 | 简介（默认：该项目暂未简介） |
| owner | int | 否 | 项目管理者用户ID |

> 说明：`collaborator/replications/likes/stars` 为只读，不可通过创建请求直接写入。

#### 请求示例

```json
{
  "title": "Test Project",
  "introduction": "This is a test project.",
  "owner": 1
}
```

#### 响应示例（201）

```json
{
  "title": "Test Project",
  "cover_image": null,
  "introduction": "This is a test project.",
  "status": "unpublished",
  "create_time": "2025-09-27T12:00:00",
  "update_time": "2025-09-27T12:00:00",
  "owner": 1,
  "collaborator": [],
  "replications": [],
  "likes": [],
  "stars": [],
  "short_term_score": 0.0,
  "long_term_score": 0.0,
  "views": 0
}
```

---

## 文章接口 [Article]

### 读取文章详情

#### 接口基本信息

| 属性 | 值 |
|------|----|
| 接口名称 | 获取文章详情 |
| 请求方法 | GET |
| 接口版本 | v1 |
| 接口路径 | `article/<int:pk>/` |
| 更新时间 | 2025-09-27 |
| 响应字符 | 200 或 404 |

---

#### 响应参数

由 `ArticleSerializer` 返回，主要字段如下：

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 文章标题（唯一） |
| content_html | string | 根据 Markdown 自动生成并经安全清洗的 HTML |
| toc | string | 目录（由 markdown toc 扩展生成） |
| word_count | int | 字数统计（按空白分割计算） |
| create_time | datetime | 创建时间 |
| update_time | datetime | 更新时间 |
| adminer | int | 文章管理者用户ID |
| project | int | 所属项目ID |

> [!NOTE]
> `content_md` 在 `ArticleSerializer` 中为 `write_only`，不会出现在响应中。

---

## 鉴权与错误码说明

- 认证方式：
  - **登录后 POST**：需携带有效认证信息（如 Cookie Session 或 `Authorization: Bearer <token>`）。
  - **GET**：公开访问。
- 常见状态码：
  - 200：请求成功（GET）。
  - 201：创建成功（POST）。
  - 400：参数错误或校验失败。
  - 401：未认证（需要登录）。
  - 404：资源不存在。

---

## 依赖与自动生成说明

- 文章内容渲染：`Article.save()` 会对 `content_md` 进行 Markdown 渲染并通过 `bleach` 白名单进行安全清洗，生成 `content_html` 与 `content_hash`。
- 目录生成：`ArticleSerializer` 使用 `markdown.extensions.toc` 生成 `toc`。
- 热度计算（项目）：`Project.calculate_hot_score()` 基于视图、点赞、收藏、复现及时间衰减计算热度相关分数。
