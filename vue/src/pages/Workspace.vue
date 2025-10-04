<script setup lang="ts">
import { computed } from 'vue'
// 使用 Vite 原生 ?raw 导入 markdown 文本
import sampleMd from '@/content/sample.md?raw'

// 极简 Markdown 转 HTML（覆盖标题/段落/列表/代码块），仅供占位演示
function renderMarkdown(md: string): string {
  // 处理围栏代码块 ```lang\n...\n```
  md = md.replace(/```([\w-]*)\n([\s\S]*?)```/g, (_m, lang: string, code: string) => {
    const safe = code.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    const langClass = lang ? ` class="language-${lang}"` : ''
    return `<pre><code${langClass}>${safe}</code></pre>`
  })

  // 标题 #..######
  for (let i = 6; i >= 1; i--) {
    const re = new RegExp(`^${'#'.repeat(i)}\\s+(.+)$`, 'gm')
    md = md.replace(re, (_m, text: string) => `<h${i}>${text}</h${i}>`)
  }

  // 无序列表（连续的 - 项）
  md = md.replace(/(^-\s+.+(?:\n-\s+.+)*)/gm, (block: string) => {
    const items = block.split(/\n/).map(l => l.replace(/^-[\s]+/, '').trim()).map(t => `<li>${t}</li>`).join('')
    return `<ul>${items}</ul>`
  })

  // 引用块 >
  md = md.replace(/^(>\s+.+)$/gm, (_m, line: string) => `<blockquote>${line.replace(/^>\s+/, '')}</blockquote>`)

  // 段落：将单行文本包裹为 p（跳过已转为 HTML 的行）
  md = md.replace(/^(?!<h\d>|<ul>|<li>|<pre>|<blockquote>)([^\n<>][^\n]*)$/gm, '<p>$1</p>')

  return md
}

const html = computed(() => renderMarkdown(sampleMd))
</script>

<template>
  <section class="workspace">
    <aside class="tool left">
      <div class="tool-card">左侧工具（占位）</div>
      <div class="tool-card muted">目录 / 书签 / 搜索</div>
    </aside>

    <main class="article">
      <article class="doc" v-html="html" />
    </main>

    <aside class="tool right">
      <div class="tool-card">右侧工具（占位）</div>
      <div class="tool-card muted">批注 / 评论 / 相关资源</div>
    </aside>
  </section>
</template>

<style scoped>
.workspace {
  height: 100%;
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr) 280px;
  gap: 16px;
  padding-right: clamp(12px, 3vw, 24px);
}

.tool {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tool-card {
  background: rgba(var(--surface-rgb), 0.06);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0;
  padding: 12px;
  color: rgba(255,255,255,0.85);
  font-size: 13px;
}

.tool-card.muted {
  color: rgba(255,255,255,0.65);
}

.article {
  background: rgba(0,0,0,0.02);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0;
  padding: clamp(12px, 3vw, 28px);
  overflow: auto;
}

.doc :is(h1,h2,h3) { color: #fff; margin: 0 0 12px; }
.doc h1 { font-size: 28px; }
.doc h2 { font-size: 20px; }
.doc h3 { font-size: 16px; }
.doc p { color: rgba(255,255,255,0.85); line-height: 1.7; margin: 0 0 10px; }
.doc ul { margin: 8px 0 12px; padding-left: 18px; color: rgba(255,255,255,0.85); }
.doc li { margin: 4px 0; }
.doc blockquote { margin: 10px 0; padding: 8px 12px; border-left: 3px solid rgba(255,255,255,0.18); color: rgba(255,255,255,0.78); background: rgba(255,255,255,0.04); }
.doc pre { background: rgba(255,255,255,0.04); padding: 10px 12px; border-radius: 0; overflow: auto; }
.doc code { color: #e9eef5; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }

@media (max-width: 1200px) {
  .workspace { grid-template-columns: 200px minmax(0, 1fr) 240px; }
}
@media (max-width: 920px) {
  .workspace { grid-template-columns: minmax(0, 1fr); }
  .tool.left, .tool.right { display: none; }
}
</style>
