# 主界面实现计划（基于 apps/projectmanage/主界面设计.md）

本计划按阶段列出主界面（首页/Main）的实现步骤，包含要创建的文件、组件、接口与联调要点。实现过程中，可逐项勾选完成。

## 阶段一：脚手架与 Mock 数据
- [ ] 新建服务：`utils/home/homeService.ts`（先返回本地 Mock 数据）
  - `listProjects`（推荐流/主列表）
  - `listHotProjects`（热门项目）
  - `listAnnouncements`（平台公告）
  - `getCategoriesTree`（分类树）
  - `listActivities`（近期动态）
- [ ] 创建组件骨架（仅 props/占位 UI）
  - `components/navigation/NavBar.vue`
  - `components/navigation/Breadcrumbs.vue`
  - `components/projects/ProjectCard.vue`
  - `components/sidebar/HotProjects.vue`
  - `components/sidebar/Announcements.vue`
  - `components/sidebar/Categories.vue`
  - `components/sidebar/RecentActivities.vue`
- [ ] 重构 `views/MainView.vue` 为三列布局，接入 Mock 数据跑通页面框架

## 阶段二：交互与状态管理
- [ ] `NavBar.vue` 增加搜索输入与回车/点击触发；与路由参数联动（`/main?keyword=...`）
- [ ] `Categories.vue` 选择分类后通过事件上抛，主页面监听后刷新推荐流
- [ ] `ProjectCard.vue` 实现点赞/收藏按钮（前端乐观更新，后端暂占位）
- [ ] 增加加载骨架与空状态；完善响应式布局（移动端折叠侧栏）

## 阶段三：后端接口接入（替换 Mock）
- [ ] 替换为真实接口（与后端约定）：
  - `GET /project/projects?sort=hot|time|stars&tag=&page=`（推荐流/主列表）
  - `GET /project/projects/hot?limit=10`（热门）
  - `GET /project/announcements?limit=5`（公告）
  - `GET /project/categories/tree`（分类树）
  - `GET /project/activities?limit=10`（近期动态）
- [ ] 增加错误处理与重试；必要时做本地短期缓存（公告/分类）

## 阶段四：打磨与扩展
- [ ] 推荐流分页/无限滚动（IntersectionObserver）
- [ ] 更多筛选（标签、排序条件）与可视化标签云
- [ ] 点赞/收藏后端打通与节流/防抖
- [ ] 单元测试/E2E 冒烟测试

## 文件与目录清单（新增/改动）
- 服务：`vue/src/utils/home/homeService.ts`
- 组件：
  - `vue/src/components/navigation/NavBar.vue`
  - `vue/src/components/navigation/Breadcrumbs.vue`
  - `vue/src/components/projects/ProjectCard.vue`
  - `vue/src/components/sidebar/HotProjects.vue`
  - `vue/src/components/sidebar/Announcements.vue`
  - `vue/src/components/sidebar/Categories.vue`
  - `vue/src/components/sidebar/RecentActivities.vue`
- 页面：`vue/src/views/MainView.vue`（重构三列布局并接入数据）

## 说明
- 现有内容可复用：`ProjectCreate.vue`、`ArticleView.vue`、`ArticleHistory.vue`、`RevisionDiff.vue`。
- 接口前缀建议统一为 `/project/`，与后端路由保持一致。
