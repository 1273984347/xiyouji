# 西游记项目 a11y 审查报告

> 本报告由 `scripts/a11y_audit.py` 自动生成，按 5 条 WCAG 2.1 AA 规则扫描全站 HTML。
> 严重度分级：P0 阻断 / P1 严重 / P2 一般 / P3 提示。退出码 0 表示无 P0 问题。

## 元信息

- 生成时间：2026-07-30 13:41:19
- 扫描目录：`site`
- 扫描文件数：78 个 HTML
- 规则数：5 条 WCAG 2.1 AA
- findings 总数：526

## 规则说明

- **E2-1 键盘导航规则**：检测 tabindex>0、onfocus/onblur 内 alert 陷阱、accesskey 冲突
- **E2-2 色彩对比度规则**：WCAG 2.1 AA 对比度（正常文本 4.5:1，大文本 3:1），解析内联+style 块
- **E2-3 ARIA 标签规则**：role 完整性、aria-label/labelledby 互斥、aria-hidden 与 focusable 冲突
- **E2-4 焦点指示规则**：outline:none 无 :focus-visible 替代、交互元素无 :focus 样式
- **E2-5 屏幕阅读器规则**：img alt、input label、th scope、noscript 完整性

## 规则计数表（P0 / P1 / P2 / P3）

| 规则 ID | 规则名称 | P0 | P1 | P2 | P3 | 合计 |
|---------|----------|----|----|----|----|------|
| E2-1 | 键盘导航规则 | 0 | 0 | 0 | 0 | 0 |
| E2-2 | 色彩对比度规则 | 0 | 6 | 2 | 0 | 8 |
| E2-3 | ARIA 标签规则 | 0 | 0 | 0 | 0 | 0 |
| E2-4 | 焦点指示规则 | 0 | 3 | 9 | 0 | 12 |
| E2-5 | 屏幕阅读器规则 | 0 | 0 | 11 | 495 | 506 |
| **合计** | - | **0** | **9** | **22** | **495** | **526** |

## Top 5 文件问题数

| 文件 | findings 数 |
|------|------------|
| `data\cognitive-psychology.html` | 39 |
| `data\relationships.html` | 39 |
| `data\risk-project.html` | 30 |
| `data\magic-system.html` | 29 |
| `data\karma-reincarnation.html` | 28 |

## Top 10 findings 详情

### 1. [P1] E2-2 色彩对比度规则
- 文件：`en\academic-papers.html`
- 行号：0
- 描述：选择器 '.lang-switch a:hover' 的 color=#fff vs background=rgba(245, 233, 212, 0.15) 对比度 1.20:1 低于 WCAG AA 阈值 4.5:1（正常文本）
- 证据：`color:#fff; background:rgba(245, 233, 212, 0.15); ratio=1.20`

### 2. [P1] E2-2 色彩对比度规则
- 文件：`en\dashboard.html`
- 行号：0
- 描述：选择器 '.lang-switch a:hover' 的 color=#fff vs background=rgba(245, 233, 212, 0.15) 对比度 1.20:1 低于 WCAG AA 阈值 4.5:1（正常文本）
- 证据：`color:#fff; background:rgba(245, 233, 212, 0.15); ratio=1.20`

### 3. [P1] E2-2 色彩对比度规则
- 文件：`en\essay-ai-era.html`
- 行号：0
- 描述：选择器 '.lang-switch a:hover' 的 color=#fff vs background=rgba(245, 233, 212, 0.15) 对比度 1.20:1 低于 WCAG AA 阈值 4.5:1（正常文本）
- 证据：`color:#fff; background:rgba(245, 233, 212, 0.15); ratio=1.20`

### 4. [P1] E2-2 色彩对比度规则
- 文件：`en\essay-information-cocoon.html`
- 行号：0
- 描述：选择器 '.lang-switch a:hover' 的 color=#fff vs background=rgba(245, 233, 212, 0.15) 对比度 1.20:1 低于 WCAG AA 阈值 4.5:1（正常文本）
- 证据：`color:#fff; background:rgba(245, 233, 212, 0.15); ratio=1.20`

### 5. [P1] E2-2 色彩对比度规则
- 文件：`en\essay-modern-management.html`
- 行号：0
- 描述：选择器 '.lang-switch a:hover' 的 color=#fff vs background=rgba(245, 233, 212, 0.15) 对比度 1.20:1 低于 WCAG AA 阈值 4.5:1（正常文本）
- 证据：`color:#fff; background:rgba(245, 233, 212, 0.15); ratio=1.20`

### 6. [P1] E2-2 色彩对比度规则
- 文件：`en\index.html`
- 行号：0
- 描述：选择器 '.lang-switch a:hover' 的 color=#fff vs background=rgba(245, 233, 212, 0.15) 对比度 1.20:1 低于 WCAG AA 阈值 4.5:1（正常文本）
- 证据：`color:#fff; background:rgba(245, 233, 212, 0.15); ratio=1.20`

### 7. [P1] E2-4 焦点指示规则
- 文件：`data\heaven-power-network.html`
- 行号：0
- 描述：选择器 '.node-circle:hover, .node-circle:focus' 设 outline:none 但未见 :focus-visible 替代样式
- 证据：`.node-circle:hover, .node-circle:focus { outline: none; ... }`

### 8. [P1] E2-4 焦点指示规则
- 文件：`data\monster-hierarchy-network.html`
- 行号：0
- 描述：选择器 '.node-circle:hover, .node-circle:focus' 设 outline:none 但未见 :focus-visible 替代样式
- 证据：`.node-circle:hover, .node-circle:focus { outline: none; ... }`

### 9. [P1] E2-4 焦点指示规则
- 文件：`data\underworld-power-network.html`
- 行号：0
- 描述：选择器 '.node-circle:hover, .node-circle:focus' 设 outline:none 但未见 :focus-visible 替代样式
- 证据：`.node-circle:hover, .node-circle:focus { outline: none; ... }`

### 10. [P2] E2-2 色彩对比度规则
- 文件：`data\cross-time-danmaku.html`
- 行号：0
- 描述：选择器 '.danmaku-fly' 的 color=#f5e9d4 vs background=rgba(200, 70, 58, 0.15) 对比度 3.98:1 低于 WCAG AA 阈值 4.5:1（正常文本）
- 证据：`color:#f5e9d4; background:rgba(200, 70, 58, 0.15); ratio=3.98`

## 建议修复优先级

1. **P0 阻断级**：立即修复（aria-hidden 与可聚焦冲突、`<img>` 完全无 alt）
2. **P1 严重**：本轮迭代内修复（role=button 缺键盘事件、对比度 < 3:1、tabindex>0）
3. **P2 一般**：下个版本修复（对比度 3–4.5:1、`<noscript>` 缺失、aria 互斥）
4. **P3 提示**：作为优化项跟踪（`<th>` 缺 scope、`alt=""` 配 `role="presentation"`）

---

由 `scripts/a11y_audit.py` 生成 · W234-E2 a11y 深化 · 5 条 WCAG 2.1 AA 规则
