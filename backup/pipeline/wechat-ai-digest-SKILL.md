---
name: wechat-ai-digest
version: 1.0.0
author: user
description: >
  将AI资讯视频的转录文字重构为结构清晰、排版精美的微信公众号HTML文章。
  融合 Tufte CSS 信息密度原则、W3C 中文排版需求、以及 Notion/Linear/Mintlify 等顶级设计系统的视觉语言。
  所有样式100%内联，零依赖，可直接粘贴至微信公众号编辑器。
metadata:
  hermes:
    tags: [html, css, wechat, 公众号, typography, ai, video, digest, markdown]
    category: creative
    related_skills: [popular-web-designs, concept-diagrams]
---

# WeChat AI Digest — AI资讯视频转录排版Skill

## 设计哲学

> **目标不是"美化"，而是"降低认知负荷"。**

视频转录文字通常口语化、结构松散、信息密度不均。本Skill的核心任务：
1. **重构内容**：从口语中提取结构（核心观点 → 论据 → 细节）
2. **建立层级**：让读者能在15秒内抓住视频的核心价值
3. **视觉锚点**：用颜色块、引用框、分割线帮助快速定位
4. **微信安全**：100%内联样式，粘贴即用

设计灵感来源：
- **Tufte CSS** — 最大化数据-墨水比，装饰必须服务信息
- **Notion** — 温暖极简的编辑体验，适合知识记录
- **Linear** — 精确的暗色美学与信息层级
- **Mintlify** — 开发者文档的清晰与可读性
- **W3C CLReq** — 中文屏幕阅读的字号、行高、字距规范

---

## 微信安全硬约束（不可违反）

| 约束 | 规则 |
|------|------|
| 样式方式 | **仅**内联 `style="..."`，禁止 `<style>` 标签、`<link>`、外部CSS |
| 选择器 | 禁止 `class=""`、`id=""`，微信会忽略或剥离 |
| 布局属性 | 禁止 `flex`、`grid`、`float`、`position:absolute/fixed` |
| 字体 | 禁止 `@font-face`、Google Fonts CDN，仅用系统字体栈 |
| 图片 | 必须 `max-width:100%; display:block;` |
| 嵌套 | `<div>` 不超过3层，防止微信编辑器扁平化破坏结构 |
| 深色模式 | 不强制颜色方案，微信App自带深色模式适配 |

---

## 三主题设计系统

根据AI资讯视频的内容类型，提供三种排版主题。默认使用 `digest`。

### 主题一：digest（速读笔记风）— 默认

**适用场景**：大多数AI资讯视频（产品发布、技术解读、行业动态）
**设计来源**：Notion × Readwise × Tufte
**核心特征**：信息密度高、重点框突出、扫描式阅读友好

#### 色彩令牌
| 令牌 | 值 | 用途 |
|------|-----|------|
| `text-main` | `#1a1a1a` | 标题、核心文字 |
| `text-body` | `#333333` | 正文（非纯黑，降低刺眼） |
| `text-secondary` | `#666666` | 引用、注释、元信息 |
| `text-meta` | `#888888` | 时间戳、标签、脚注 |
| `accent` | `#576b95` | 强调色、重点框边框、链接（微信原生蓝） |
| `accent-light` | `#eef2ff` | 重点框背景 |
| `bg-quote` | `#f9f9f9` | 引用块背景 |
| `border-light` | `#eeeeee` | 分隔线、标题下划线 |
| `border-quote` | `#d9d9d9` | 引用块左边框 |
| `border-accent` | `#576b95` | 重点框左边框 |

#### 排版令牌
| 令牌 | 值 | 用途 |
|------|-----|------|
| `font-stack` | `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif` | 系统字体 |
| `size-h1` | `24px` | 文章标题 |
| `size-h2` | `18px` | 章节标题 |
| `size-h3` | `16px` | 小节标题 |
| `size-body` | `16px` | 正文 |
| `size-small` | `14px` | 元信息、标签、脚注 |
| `line-body` | `1.75` | 正文行高（中文舒适值） |
| `line-heading` | `1.4` | 标题行高 |
| `container-max` | `677px` | 微信文章标准宽度 |

---

### 主题二：magazine（杂志分析风）

**适用场景**：深度AI分析、观点评论、行业趋势研判
**设计来源**：Linear × Stripe × 编辑排版
**核心特征**：更大的呼吸感、精致的引用块、优雅的层级

#### 差异令牌（与digest不同的部分）
| 令牌 | digest值 | magazine值 | 说明 |
|------|----------|------------|------|
| `accent` | `#576b95` | `#7c3aed` | Linear紫，更有品牌感 |
| `accent-light` | `#eef2ff` | `#f5f3ff` | 淡紫背景 |
| `bg-quote` | `#f9f9f9` | `#faf5ff` | 淡紫引用背景 |
| `border-quote` | `#d9d9d9` | `#c4b5fd` | 淡紫引用边框 |
| `size-h1` | `24px` | `26px` | 更大标题，杂志感 |
| `line-body` | `1.75` | `1.8` | 更宽松的阅读节奏 |
| `h2-style` | 下划线 | 左边框+背景色 | H2带左边框强调 |

---

### 主题三：notebook（技术笔记风）

**适用场景**：技术教程、代码演示、API解读、论文速览
**设计来源**：Mintlify × Vercel Docs × GitHub
**核心特征**：代码友好、步骤清晰、深色代码块

#### 差异令牌
| 令牌 | digest值 | notebook值 | 说明 |
|------|----------|------------|------|
| `accent` | `#576b95` | `#10b981` | Mintlify绿，技术感 |
| `accent-light` | `#eef2ff` | `#ecfdf5` | 淡绿背景 |
| `code-bg` | `#f8f8f8` | `#1e1e1e` | 深色代码块 |
| `code-text` | `#333333` | `#e2e2e2` | 代码块浅色文字 |
| `inline-code-bg` | `rgba(27,31,35,0.05)` | `#f0f9ff` | 行内代码背景 |
| `inline-code-color` | `#d63384` | `#0ea5e9` | 行内代码文字色 |

---

## HTML组件模板（100%内联，微信安全）

以下所有模板均使用**digest主题**的默认值。若使用其他主题，直接使用对应的模板部分。

### digest主题（默认）
### 根容器
```html
<div style="max-width:677px;margin:0 auto;padding:24px 18px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;color:#333333;font-size:16px;line-height:1.75;word-wrap:break-word;-webkit-font-smoothing:antialiased;background:#ffffff;">
  {{CONTENT}}
</div>
```

### 文章标题 H1
```html
<h1 style="font-size:24px;font-weight:bold;color:#1a1a1a;line-height:1.4;margin:0 0 12px 0;text-align:center;letter-spacing:0.02em;">
  {{TITLE}}
</h1>
```

### 元信息行（作者/日期/视频来源/阅读时间）
```html
<p style="font-size:14px;color:#888888;text-align:center;margin:0 0 36px 0;line-height:1.5;">
  {{META_INFO}}
</p>
```

### 导语/摘要框（视频核心价值的3句话总结）
```html
<div style="margin:0 0 28px 0;padding:16px 18px;background:linear-gradient(135deg,#f8fafc 0%,#eef2ff 100%);border-left:4px solid #576b95;border-radius:0 8px 8px 0;">
  <p style="margin:0 0 8px 0;font-size:14px;color:#576b95;font-weight:bold;line-height:1.4;">📌 核心摘要</p>
  <p style="margin:0;color:#333333;font-size:15px;line-height:1.7;text-align:justify;">{{SUMMARY}}</p>
</div>
```

### 章节标题 H2
```html
<h2 style="font-size:18px;font-weight:bold;color:#1a1a1a;margin:36px 0 14px 0;line-height:1.4;border-bottom:1px solid #eeeeee;padding-bottom:8px;">
  {{SECTION_TITLE}}
</h2>
```

### 小节标题 H3
```html
<h3 style="font-size:16px;font-weight:bold;color:#2c2c2c;margin:28px 0 10px 0;line-height:1.4;">
  {{SUB_TITLE}}
</h3>
```

### 正文段落
```html
<p style="margin:0 0 16px 0;text-align:justify;letter-spacing:normal;">
  {{BODY_TEXT}}
</p>
```

### 重点框 / 核心观点提取（digest主题的灵魂组件）
```html
<div style="margin:18px 0;padding:14px 16px;background-color:#eef2ff;border-left:4px solid #576b95;border-radius:0 6px 6px 0;">
  <p style="margin:0 0 6px 0;font-size:14px;color:#576b95;font-weight:bold;line-height:1.4;">💡 {{POINT_TITLE}}</p>
  <p style="margin:0;color:#333333;font-size:15px;line-height:1.7;text-align:justify;">{{POINT_CONTENT}}</p>
</div>
```

### 引用块 / 金句摘录
```html
<blockquote style="margin:20px 0;padding:14px 16px;background-color:#f9f9f9;border-left:3px solid #d9d9d9;color:#666666;font-size:15px;line-height:1.7;border-radius:0 4px 4px 0;">
  <p style="margin:0;font-style:italic;">{{QUOTE_TEXT}}</p>
  <p style="margin:8px 0 0 0;font-size:13px;color:#888888;text-align:right;">— {{SOURCE}}</p>
</blockquote>
```

### 无序列表
```html
<ul style="margin:16px 0;padding-left:22px;color:#333333;list-style-type:disc;">
  <li style="margin-bottom:10px;line-height:1.75;">{{ITEM}}</li>
</ul>
```

### 有序列表（步骤/排名）
```html
<ol style="margin:16px 0;padding-left:22px;color:#333333;list-style-type:decimal;">
  <li style="margin-bottom:10px;line-height:1.75;"><strong style="color:#1a1a1a;">{{STEP_TITLE}}</strong> {{STEP_DETAIL}}</li>
</ol>
```

### 图片 + 说明
```html
<figure style="margin:24px 0;text-align:center;">
  <img src="{{IMG_URL}}" alt="{{ALT}}" style="max-width:100%;height:auto;border-radius:6px;display:block;margin:0 auto;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
  <figcaption style="font-size:13px;color:#888888;margin-top:10px;text-align:center;line-height:1.5;">{{CAPTION}}</figcaption>
</figure>
```

### 行内代码
```html
<code style="background:#f4f4f4;padding:2px 5px;border-radius:3px;font-family:'SF Mono',Monaco,Inconsolata,'Fira Code','Courier New',monospace;font-size:14px;color:#d63384;word-wrap:break-word;">
  {{CODE}}
</code>
```

### 代码块（notebook主题使用深色背景）
```html
<pre style="background:#f8f8f8;padding:16px;border-radius:8px;overflow-x:auto;margin:20px 0;border:1px solid #eeeeee;line-height:1.6;font-size:14px;color:#333333;font-family:'SF Mono',Monaco,Inconsolata,'Fira Code','Courier New',monospace;white-space:pre-wrap;word-wrap:break-word;"><code>{{CODE_BLOCK}}</code></pre>
```

### 分隔线
```html
<hr style="border:none;border-top:1px solid #eeeeee;margin:32px 0;">
```

### 标签/话题标记
```html
<span style="display:inline-block;margin:4px 4px 4px 0;padding:3px 10px;background:#f4f4f4;color:#666666;font-size:13px;border-radius:12px;line-height:1.4;">
  {{TAG}}
</span>
```

### 底部信息栏
```html
<div style="margin-top:40px;padding-top:20px;border-top:1px solid #eeeeee;text-align:center;">
  <p style="font-size:13px;color:#888888;line-height:1.6;margin:0 0 8px 0;">{{FOOTER_NOTE}}</p>
  <p style="font-size:13px;color:#aaaaaa;line-height:1.5;margin:0;">{{TIMESTAMP}}</p>
</div>
```

---



### magazine主题
### 根容器
```html
<div style="max-width:677px;margin:0 auto;padding:24px 18px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;color:#333333;font-size:16px;line-height:1.8;word-wrap:break-word;-webkit-font-smoothing:antialiased;background:#ffffff;">
  {{CONTENT}}
</div>
```

### 文章标题 H1
```html
<h1 style="font-size:26px;font-weight:bold;color:#1a1a1a;line-height:1.4;margin:0 0 12px 0;text-align:center;letter-spacing:0.02em;">
  {{TITLE}}
</h1>
```

### 元信息行（作者/日期/视频来源/阅读时间）
```html
<p style="font-size:14px;color:#888888;text-align:center;margin:0 0 36px 0;line-height:1.5;">
  {{META_INFO}}
</p>
```

### 导语/摘要框（视频核心价值的3句话总结）
```html
<div style="margin:0 0 28px 0;padding:16px 18px;background:linear-gradient(135deg,#f8fafc 0%,#f5f3ff 100%);border-left:4px solid #7c3aed;border-radius:0 8px 8px 0;">
  <p style="margin:0 0 8px 0;font-size:14px;color:#7c3aed;font-weight:bold;line-height:1.4;">📌 核心摘要</p>
  <p style="margin:0;color:#333333;font-size:15px;line-height:1.7;text-align:justify;">{{SUMMARY}}</p>
</div>
```

### 章节标题 H2
```html
<h2 style="font-size:18px;font-weight:bold;color:#1a1a1a;margin:36px 0 14px 0;line-height:1.4;border-left:4px solid #7c3aed;padding-left:12px;background-color:#f5f3ff;">
  {{SECTION_TITLE}}
</h2>
```

### 小节标题 H3
```html
<h3 style="font-size:16px;font-weight:bold;color:#2c2c2c;margin:28px 0 10px 0;line-height:1.4;">
  {{SUB_TITLE}}
</h3>
```

### 正文段落
```html
<p style="margin:0 0 16px 0;text-align:justify;letter-spacing:normal;">
  {{BODY_TEXT}}
</p>
```

### 重点框 / 核心观点提取（digest主题的灵魂组件）
```html
<div style="margin:18px 0;padding:14px 16px;background-color:#f5f3ff;border-left:4px solid #7c3aed;border-radius:0 6px 6px 0;">
  <p style="margin:0 0 6px 0;font-size:14px;color:#7c3aed;font-weight:bold;line-height:1.4;">💡 {{POINT_TITLE}}</p>
  <p style="margin:0;color:#333333;font-size:15px;line-height:1.7;text-align:justify;">{{POINT_CONTENT}}</p>
</div>
```

### 引用块 / 金句摘录
```html
<blockquote style="margin:20px 0;padding:14px 16px;background-color:#faf5ff;border-left:3px solid #c4b5fd;color:#666666;font-size:15px;line-height:1.7;border-radius:0 4px 4px 0;">
  <p style="margin:0;font-style:italic;">{{QUOTE_TEXT}}</p>
  <p style="margin:8px 0 0 0;font-size:13px;color:#888888;text-align:right;">— {{SOURCE}}</p>
</blockquote>
```

### 无序列表
```html
<ul style="margin:16px 0;padding-left:22px;color:#333333;list-style-type:disc;">
  <li style="margin-bottom:10px;line-height:1.8;">{{ITEM}}</li>
</ul>
```

### 有序列表（步骤/排名）
```html
<ol style="margin:16px 0;padding-left:22px;color:#333333;list-style-type:decimal;">
  <li style="margin-bottom:10px;line-height:1.8;"><strong style="color:#1a1a1a;">{{STEP_TITLE}}</strong> {{STEP_DETAIL}}</li>
</ol>
```

### 图片 + 说明
```html
<figure style="margin:24px 0;text-align:center;">
  <img src="{{IMG_URL}}" alt="{{ALT}}" style="max-width:100%;height:auto;border-radius:6px;display:block;margin:0 auto;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
  <figcaption style="font-size:13px;color:#888888;margin-top:10px;text-align:center;line-height:1.5;">{{CAPTION}}</figcaption>
</figure>
```

### 行内代码
```html
<code style="background:#f4f4f4;padding:2px 5px;border-radius:3px;font-family:'SF Mono',Monaco,Inconsolata,'Fira Code','Courier New',monospace;font-size:14px;color:#d63384;word-wrap:break-word;">
  {{CODE}}
</code>
```

### 代码块（notebook主题使用深色背景）
```html
<pre style="background:#f8f8f8;padding:16px;border-radius:8px;overflow-x:auto;margin:20px 0;border:1px solid #eeeeee;line-height:1.6;font-size:14px;color:#333333;font-family:'SF Mono',Monaco,Inconsolata,'Fira Code','Courier New',monospace;white-space:pre-wrap;word-wrap:break-word;"><code>{{CODE_BLOCK}}</code></pre>
```

### 分隔线
```html
<hr style="border:none;border-top:1px solid #eeeeee;margin:32px 0;">
```

### 标签/话题标记
```html
<span style="display:inline-block;margin:4px 4px 4px 0;padding:3px 10px;background:#f4f4f4;color:#666666;font-size:13px;border-radius:12px;line-height:1.4;">
  {{TAG}}
</span>
```

### 底部信息栏
```html
<div style="margin-top:40px;padding-top:20px;border-top:1px solid #eeeeee;text-align:center;">
  <p style="font-size:13px;color:#888888;line-height:1.6;margin:0 0 8px 0;">{{FOOTER_NOTE}}</p>
  <p style="font-size:13px;color:#aaaaaa;line-height:1.5;margin:0;">{{TIMESTAMP}}</p>
</div>
```

---



### notebook主题
### 根容器
```html
<div style="max-width:677px;margin:0 auto;padding:24px 18px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;color:#333333;font-size:16px;line-height:1.75;word-wrap:break-word;-webkit-font-smoothing:antialiased;background:#ffffff;">
  {{CONTENT}}
</div>
```

### 文章标题 H1
```html
<h1 style="font-size:24px;font-weight:bold;color:#1a1a1a;line-height:1.4;margin:0 0 12px 0;text-align:center;letter-spacing:0.02em;">
  {{TITLE}}
</h1>
```

### 元信息行（作者/日期/视频来源/阅读时间）
```html
<p style="font-size:14px;color:#888888;text-align:center;margin:0 0 36px 0;line-height:1.5;">
  {{META_INFO}}
</p>
```

### 导语/摘要框（视频核心价值的3句话总结）
```html
<div style="margin:0 0 28px 0;padding:16px 18px;background:linear-gradient(135deg,#f8fafc 0%,#ecfdf5 100%);border-left:4px solid #10b981;border-radius:0 8px 8px 0;">
  <p style="margin:0 0 8px 0;font-size:14px;color:#10b981;font-weight:bold;line-height:1.4;">📌 核心摘要</p>
  <p style="margin:0;color:#333333;font-size:15px;line-height:1.7;text-align:justify;">{{SUMMARY}}</p>
</div>
```

### 章节标题 H2
```html
<h2 style="font-size:18px;font-weight:bold;color:#1a1a1a;margin:36px 0 14px 0;line-height:1.4;border-bottom:1px solid #eeeeee;padding-bottom:8px;">
  {{SECTION_TITLE}}
</h2>
```

### 小节标题 H3
```html
<h3 style="font-size:16px;font-weight:bold;color:#2c2c2c;margin:28px 0 10px 0;line-height:1.4;">
  {{SUB_TITLE}}
</h3>
```

### 正文段落
```html
<p style="margin:0 0 16px 0;text-align:justify;letter-spacing:normal;">
  {{BODY_TEXT}}
</p>
```

### 重点框 / 核心观点提取（digest主题的灵魂组件）
```html
<div style="margin:18px 0;padding:14px 16px;background-color:#ecfdf5;border-left:4px solid #10b981;border-radius:0 6px 6px 0;">
  <p style="margin:0 0 6px 0;font-size:14px;color:#10b981;font-weight:bold;line-height:1.4;">💡 {{POINT_TITLE}}</p>
  <p style="margin:0;color:#333333;font-size:15px;line-height:1.7;text-align:justify;">{{POINT_CONTENT}}</p>
</div>
```

### 引用块 / 金句摘录
```html
<blockquote style="margin:20px 0;padding:14px 16px;background-color:#f8f8f8;border-left:3px solid #d9d9d9;color:#666666;font-size:15px;line-height:1.7;border-radius:0 4px 4px 0;">
  <p style="margin:0;font-style:italic;">{{QUOTE_TEXT}}</p>
  <p style="margin:8px 0 0 0;font-size:13px;color:#888888;text-align:right;">— {{SOURCE}}</p>
</blockquote>
```

### 无序列表
```html
<ul style="margin:16px 0;padding-left:22px;color:#333333;list-style-type:disc;">
  <li style="margin-bottom:10px;line-height:1.75;">{{ITEM}}</li>
</ul>
```

### 有序列表（步骤/排名）
```html
<ol style="margin:16px 0;padding-left:22px;color:#333333;list-style-type:decimal;">
  <li style="margin-bottom:10px;line-height:1.75;"><strong style="color:#1a1a1a;">{{STEP_TITLE}}</strong> {{STEP_DETAIL}}</li>
</ol>
```

### 图片 + 说明
```html
<figure style="margin:24px 0;text-align:center;">
  <img src="{{IMG_URL}}" alt="{{ALT}}" style="max-width:100%;height:auto;border-radius:6px;display:block;margin:0 auto;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
  <figcaption style="font-size:13px;color:#888888;margin-top:10px;text-align:center;line-height:1.5;">{{CAPTION}}</figcaption>
</figure>
```

### 行内代码
```html
<code style="background:#f0f9ff;padding:2px 5px;border-radius:3px;font-family:'SF Mono',Monaco,Inconsolata,'Fira Code','Courier New',monospace;font-size:14px;color:#0ea5e9;word-wrap:break-word;">
  {{CODE}}
</code>
```

### 代码块（notebook主题使用深色背景）
```html
<pre style="background:#1e1e1e;padding:16px;border-radius:8px;overflow-x:auto;margin:20px 0;border:1px solid #333333;line-height:1.6;font-size:14px;color:#e2e2e2;font-family:'SF Mono',Monaco,Inconsolata,'Fira Code','Courier New',monospace;white-space:pre-wrap;word-wrap:break-word;"><code>{{CODE_BLOCK}}</code></pre>
```

### 分隔线
```html
<hr style="border:none;border-top:1px solid #eeeeee;margin:32px 0;">
```

### 标签/话题标记
```html
<span style="display:inline-block;margin:4px 4px 4px 0;padding:3px 10px;background:#f4f4f4;color:#666666;font-size:13px;border-radius:12px;line-height:1.4;">
  {{TAG}}
</span>
```

### 底部信息栏
```html
<div style="margin-top:40px;padding-top:20px;border-top:1px solid #eeeeee;text-align:center;">
  <p style="font-size:13px;color:#888888;line-height:1.6;margin:0 0 8px 0;">{{FOOTER_NOTE}}</p>
  <p style="font-size:13px;color:#aaaaaa;line-height:1.5;margin:0;">{{TIMESTAMP}}</p>
</div>
```

---

## 核心Procedure（内容重构 + 排版映射）

### Step 1: 分析转录文本（内容重构）

视频转录文字通常具有以下特征，需要识别并处理：
- **口语化**："那么"、"然后"、"就是说"、"对吧"等填充词
- **重复**：演讲者会重复强调同一观点
- **结构松散**：逻辑跳跃，缺乏清晰的章节划分
- **信息密度不均**：核心观点淹没在长段叙述中

**处理动作**：
1. 去除口语填充词，转为书面表达
2. 识别并提取 **3-5个核心观点**，每个观点压缩为1-2句话
3. 将剩余内容按逻辑重组为 **3-4个章节**
4. 提取 **1-2条金句/关键引用**，放入引用块
5. 识别技术术语、产品名、API名，用行内代码标记
6. 若有步骤/流程，转为有序列表
7. 若有并列要点，转为无序列表

### Step 2: 选择主题

根据内容类型自动选择或按用户指定：

| 内容特征 | 推荐主题 |
|---------|---------|
| 产品发布、新闻速递、行业动态 | `digest`（默认） |
| 深度分析、观点评论、趋势研判 | `magazine` |
| 技术教程、代码演示、API文档 | `notebook` |

### Step 3: 构建文章结构

标准结构模板：

```
[根容器]
  ├── H1: 文章标题（提炼核心洞察，不是视频原标题）
  ├── 元信息（视频来源、日期、阅读时间）
  ├── 导语/摘要框（3句话总结视频价值）
  ├── 重点框1（核心观点1）
  ├── 重点框2（核心观点2）
  ├── 重点框3（核心观点3）
  ├── 分隔线
  ├── H2: 章节1
  │   ├── 正文段落
  │   ├── 无序/有序列表（如适用）
  │   └── 引用块（如适用）
  ├── H2: 章节2
  │   └── ...
  ├── H2: 章节3
  │   └── ...
  ├── 分隔线
  ├── H2: 关键引用 / 金句摘录
  │   └── 引用块
  ├── 标签行（相关话题标签）
  └── 底部信息栏
```

### Step 4: 映射到HTML模板

将Step 3的结构映射到对应的HTML组件模板：
- 每个元素必须使用选定主题的**设计令牌值**
- **所有样式必须内联**，禁止任何class/id
- 图片URL若来自本地，使用占位符并提示用户手动上传

### Step 5: 微信安全消毒

生成HTML后，执行以下检查：
- [ ] 无 `<style>` 标签
- [ ] 无 `class=""` 或 `id=""` 属性
- [ ] 无 `flex`、`grid`、`float`、`position:absolute/fixed`
- [ ] 无 `@font-face` 或外部字体链接
- [ ] 所有图片有 `max-width:100%; display:block;`
- [ ] 容器为 `max-width:677px`
- [ ] 正文为 `16px`，行高 `1.75`
- [ ] `<div>` 嵌套不超过3层
- [ ] 颜色对比度安全（深色文字在白色背景上）

### Step 6: 输出

返回完整的HTML字符串，包裹在代码块中：

```html
<!-- 完整文章HTML -->
<div style="...">
  ...
</div>
```

---

## 特殊场景处理

### 场景1：视频无明确结构（纯对话/访谈）
- 使用 **引用块** 区分不同发言者
- 用 **重点框** 提取每位发言者的核心观点
- 章节标题使用发言者名或话题标签

### 场景2：技术演示/代码占比高
- 切换到 `notebook` 主题
- 代码块使用深色背景模板
- 步骤使用有序列表，每步标题加粗
- 技术术语统一用行内代码标记

### 场景3：数据/图表密集
- 用 **表格**（极简边框）呈现数据
- 用 **重点框** 提取关键数据结论
- 图表使用图片模板，配详细说明文字

### 场景4：多视频对比/综述
- 使用多个 **H2** 分节，每节一个视频
- 每节开头用 **重点框** 概括该视频核心观点
- 结尾用无序列表做跨视频对比总结

---

## 吸取的Skill优点清单

| 来源Skill | 吸取的优点 | 在我们的Skill中的体现 |
|-----------|-----------|----------------------|
| **iamzifei/wechat-article-formatter** | 微信公众号适配经验；绿色强调色视觉记忆；代码块深色风格 | 解决其id选择器失效问题，全部内联化；保留其代码块配色逻辑 |
| **baoyu-markdown-to-html** | 多主题架构；内容类型适配；CJK中文处理 | 设计3个主题（digest/magazine/notebook）；内置中文排版参数 |
| **popular-web-designs** | 设计令牌化思维；54个顶级品牌的视觉语言 | 从Notion/Linear/Mintlify提炼令牌；可扩展更多主题 |
| **Tufte CSS** | 信息密度最大化；扁平层级；sidenote批注 | 用"重点框"替代sidenote；克制配色；宽栏比例 |
| **W3C CLReq** | 中文屏幕阅读舒适度 | 16px正文、1.75行高、系统字体栈、两端对齐 |
| **claude-design** | 设计流程：scope → structure → verify | Procedure内置分析→重构→映射→消毒→验证五步 |

---

## 常见陷阱与规避

| 陷阱 | 后果 | 规避方法 |
|------|------|---------|
| 使用 `<style>` 标签 | 微信编辑器直接过滤，整篇文章无样式 | 100%内联，本Skill已硬编码 |
| 使用 `class` / `id` | 样式失效，排版崩坏 | Procedure Step 5 强制删除 |
| 使用 `flex` / `grid` | 移动端布局错乱 | 使用 `text-align` + `margin` 替代 |
| 深层 `<div>` 嵌套 | 微信编辑器扁平化，结构丢失 | 限制3层，多用语义标签 `<p>` `<h2>` `<blockquote>` |
| 自定义字体 | iOS/Android 显示为默认宋体 | 使用系统字体栈，覆盖所有平台 |
| 强制深色模式样式 | 微信深色模式下文字可能不可见 | 不添加 `prefers-color-scheme`，让微信App自行适配 |
| 图片无 `display:block` | 图片下方出现多余空白 | 所有图片模板已包含 `display:block` |
| 口语化文字直接排版 | 文章冗长、重点淹没 | Step 1 强制重构，提取核心观点 |

---

## 使用示例

**用户输入**：
> "这是一段关于OpenAI新发布的GPT-5的视频转录文字，大约5000字，口语化严重，帮我整理成公众号文章。"

**Skill执行**：
1. 分析转录文本，识别核心观点（如：多模态能力、推理速度提升、API价格变化）
2. 选择 `digest` 主题（产品发布类）
3. 构建结构：标题 → 摘要框 → 3个重点框 → 详细章节 → 引用块 → 标签
4. 映射到HTML模板，全部内联样式
5. 微信安全消毒
6. 输出完整HTML代码块

**输出特征**：
- 标题提炼核心洞察（非原标题）
- 摘要框3句话概括价值
- 每个重点框一个核心观点，带标题和内容
- 技术术语用行内代码高亮
- 可直接复制粘贴到 `mp.weixin.qq.com`

## ⚠️ 代理使用规范

**代理端口10808**：专门用来访问GitHub（大陆访问不稳定）

**视频下载**：抖音/B站都是大陆网站，**不需要挂代理**

**错误做法**：
- ❌ 下载抖音/B站视频时设置代理端口
- ❌ 在transcribe.py中设置HTTP_PROXY/HTTPS_PROXY

**正确做法**：
- ✅ 访问GitHub时使用代理端口10808
- ✅ 下载抖音/B站视频时不设置任何代理
- ✅ 保持网络环境纯净，避免代理干扰
