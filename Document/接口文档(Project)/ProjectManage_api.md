---

#### 示例

请求示例：

```http
POST /project/revision HTTP/1.1
Content-Type: application/json
Authorization: Bearer <token>

{
  "article": 12,
  "content": "# Intro v2\nUpdated.",
  "submitter": 1,
  "comment": "fix typos"
}
```

成功响应（201）：

```json
{
  "id": 34,
  "article": 12,
  "content": "# Intro v2\nUpdated.",
  "submitter": 1,
  "comment": "fix typos",
  "status": "pending",
  "create_time": "2025-09-27T12:10:00",
  "parent": 33,
  "base_content_hash": "a9c4...",
  "version": 0,
  "diff_json": {"type": "unified", "patch": "@@ -1,1 +1,2 @@ ..."},
  "applied_time": null,
  "applied_by": null
}
```
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
| maintainers | array[int] | 维护者用户ID 列表（仅维护者可审批修订） |

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

### 创建文章

#### 接口基本信息

| 属性 | 值 |
|------|----|
| 接口名称 | 创建文章 |
| 请求方法 | POST |
| 接口版本 | v1 |
| 接口路径 | `articletest` |
| 认证 | 需登录（401 未登录） |
| 更新时间 | 2025-09-27 |
| 响应字符 | 201 或 400 |

#### 请求体参数

| 字段名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| title | string | 是 | 文章标题（唯一） |
| content_md | string | 是 | Markdown 原文内容 |
| project | int | 是 | 所属项目ID（必填，后端强校验） |
| category | int | 否 | 类别ID（不传则使用/创建“默认分类”） |
| adminer | int | 否 | 文章管理者用户ID |

---

#### 示例

请求示例：

```http
POST /project/articletest HTTP/1.1
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Test Article",
  "content_md": "# Intro\nThis is content.",
  "project": 1,
  "category": 2,
  "adminer": 1
}
```

成功响应（201）：

```json
{
  "id": 12,
  "title": "Test Article",
  "content_html": "<h1>Intro</h1>...",
  "toc": "<div class=\"toc\">...</div>",
  "word_count": 3,
  "create_time": "2025-09-27T12:00:00",
  "update_time": "2025-09-27T12:00:00",
  "adminer": 1,
  "project": 1,
  "category": 2
}
```

失败响应（400，缺少 project）：

```json
{
  "project": ["文章必须隶属于某个项目"]
}
```

## 文章修订接口 [Article Revision]

> [!NOTE]
> 修订审批需项目 `maintainers` 中的用户执行；同一修订累计 3 个“同意”后自动合入到文章。

### 创建修订

| 属性 | 值 |
|------|----|
| 接口名称 | 创建文章修订 |
| 请求方法 | POST |
| 接口路径 | `revision` |
| 认证 | 需登录 |
| 响应 | 201 或 400 |

请求体：
- `article`: int 文章ID（必填）
- `content`: string 新内容（必填）
- `submitter`: int 提交者用户ID（建议传入）
- `comment`: string 修改说明（建议传入）

返回字段（节选）：`id, article, content, submitter, comment, status, create_time, parent, base_content_hash, version, diff_json, applied_time, applied_by`

说明：
- `parent` 自动设置为该文章最近一次已通过的修订。
- `base_content_hash` 为创建修订时文章内容的 MD5。
- `diff_json` 为与文章当前内容的差异（默认 unified 格式）。

---

### 获取修订详情

| 属性 | 值 |
|------|----|
| 接口名称 | 获取修订详情 |
| 请求方法 | GET |
| 接口路径 | `revision/<int:pk>/` |
| 认证 | 公开 |
| 响应 | 200 或 404 |

---

### 审批修订

| 属性 | 值 |
|------|----|
| 接口名称 | 审批修订 |
| 请求方法 | POST |
| 接口路径 | `revision/approval` |
| 认证 | 需登录（且必须为项目维护者） |
| 响应 | 201 或 400 |

请求体：
- `revision`: int 修订ID（必填）
- `approver`: int 审批人ID（必填，需为维护者）
- `decision`: string 审批结果（`approved`/`rejected`）

规则：
- 同一修订累计 3 个 `approved` 后，后台自动合入：
  - 更新文章 `content_md`
  - 设置修订 `status=approved`、`version=递增`、`applied_time`、`applied_by`

---

#### 示例

请求示例（维护者审批同意）：

```http
POST /project/revision/approval HTTP/1.1
Content-Type: application/json
Authorization: Bearer <token>

{
  "revision": 34,
  "approver": 5,
  "decision": "approved"
}
```

失败响应（400，非维护者审批）：

```json
{
  "approver": ["只有项目维护者可以进行审批"]
}
```

### 列表文章修订

| 属性 | 值 |
|------|----|
| 接口名称 | 列表文章修订 |
| 请求方法 | GET |
| 接口路径 | `article/<int:pk>/revisions` |
| 认证 | 公开 |
| 响应 | 200 |

返回：该文章的所有修订，按 `version`、`create_time` 倒序。

---

#### 示例

```http
GET /project/article/12/revisions HTTP/1.1
```

成功响应（200）：

```json
[
  {"id": 35, "article": 12, "version": 2, "status": "approved", "submitter": 1, "comment": "v2", "create_time": "...", "applied_time": "..."},
  {"id": 34, "article": 12, "version": 1, "status": "approved", "submitter": 1, "comment": "v1", "create_time": "...", "applied_time": "..."}
]
```

### 查看修订差异

| 属性 | 值 |
|------|----|
| 接口名称 | 查看修订差异 |
| 请求方法 | GET |
| 接口路径 | `revision/<int:pk>/diff` |
| Query 参数 | `against=prev|current`（默认 prev）, `mode=unified|html|dmp`（默认 unified） |
| 认证 | 公开 |
| 响应 | 200 或 404 |

说明：
- `against=prev`：与父修订内容对比。
- `against=current`：与文章当前内容对比。
- `mode` 控制差异展示策略，后端采用策略模式（Strategy）实现，可扩展。

---

#### 示例

```http
GET /project/revision/34/diff?against=prev&mode=unified HTTP/1.1
```

成功响应（200）：

```json
{
  "revision": 34,
  "against": "prev",
  "mode": "unified",
  "diff": {"type": "unified", "patch": "@@ -1,1 +1,2 @@ ..."}
}
```

### 回滚到指定修订

| 属性 | 值 |
|------|----|
| 接口名称 | 回滚修订 |
| 请求方法 | POST |
| 接口路径 | `revision/<int:pk>/revert` |
| 认证 | 需登录（且必须为项目维护者） |
| 响应 | 201 或 403 |

说明：创建一个“回滚修订”（内容取目标修订），并走同样的 3 人同意合入流程。合入完成后文章回到目标修订对应的内容。

---

#### 示例

请求示例（维护者触发回滚）：

```http
POST /project/revision/34/revert HTTP/1.1
Authorization: Bearer <token>
```

成功响应（201）：返回新建的“回滚修订”对象（字段同“创建修订”响应）。
失败响应（403）：

```json
{
  "detail": "只有项目维护者可以回滚"
}
```

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
