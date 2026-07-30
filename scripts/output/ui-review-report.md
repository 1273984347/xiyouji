# 前端 UI 批量截图审查与交互测试报告

> 测试时间：2026-07-22
> 测试环境：Playwright + Chromium，本地 `file://` 协议
> 测试范围：38 个数据可视化页面（site/data/*.html）+ dashboard.html + index.html

---

## 1. 执行摘要

- **38 个可视化页面 + dashboard.html + index.html**已执行 Playwright 批量截图（桌面端 1280×800 + 移动端 375×812）。
- **38 个可视化页面未报告 `pageerror`**，仅存在预期的 `file://` 协议 fetch fallback 日志。
- **JS 语法检查**：`scripts/check_all_js_syntax.py` 未报告语法错误。
- **移动端表格包裹检查**：`scripts/detect_unwrapped_tables.py` 扫描 38 个数据页 + dashboard.html，未包裹表格数为 0。
- **文案修复**：`site/index.html` dashboard 快速入口描述已由「35 维度」更新为「38 专题 · 132 维度」；`site/dashboard.html` 副标题同步为「38 个专题，34 大门类可视化总览，覆盖 A-AH 全维度」。
- **问题修复**：`game-webnovel.html` 网文人气排行条形图在移动端产生 713 条负宽度控制台错误，已修复。

---

## 2. 批量截图覆盖

脚本：`scripts/batch_screenshots.js`

| 视口 | 尺寸 | 页面数 | 输出目录 |
|:---:|:---:|:---:|:---|
| desktop | 1280×800 | 40（38 数据页 + dashboard + index） | `scripts/output/screenshots/desktop/` |
| mobile | 375×812 | 40（38 数据页 + dashboard + index） | `scripts/output/screenshots/mobile/` |

完整截图清单见：`scripts/output/screenshots/screenshot-summary.md`

### 2.1 控制台异常汇总

所有页面的控制台输出均为**预期的 fetch fallback**，原因是页面通过 `fetchJson(path, fallbackKey)` 尝试加载 JSON，而 Playwright 以 `file://` 协议打开时浏览器禁止 fetch 本地文件。页面均通过 `EMBEDDED_DATA` 降级渲染，未观察到功能异常。

| 页面 | 控制台异常数 | 页面异常数 |
|:---|:---:|:---:|
| 81-hardships.html | 2 | 0 |
| aesthetics.html | 6 | 0 |
| business-model.html | 8 | 0 |
| cave-estate.html | 5 | 0 |
| century-dialogue.html | 4 | 0 |
| chapter-stats.html | 1 | 0 |
| character-appearance.html | 1 | 0 |
| chart-design.html | 8 | 0 |
| cognitive-psychology.html | 8 | 0 |
| concept-device.html | 2 | 0 |
| counterfactual.html | 3 | 0 |
| criticism-history.html | 12 | 0 |
| cross-time-danmaku.html | 12 | 0 |
| cultural-misreading.html | 6 | 0 |
| deconstruction.html | 4 | 0 |
| ecology.html | 10 | 0 |
| ethics-consumption.html | 8 | 0 |
| famous-time-travel.html | 4 | 0 |
| game-webnovel.html | 8 | 0 |
| global-pattern.html | 4 | 0 |
| journey-route.html | 1 | 0 |
| jurisprudence.html | 8 | 0 |
| karma-reincarnation.html | 8 | 0 |
| linguistics.html | 8 | 0 |
| magic-system.html | 6 | 0 |
| material-archaeology.html | 9 | 0 |
| methodology-matrix.html | 6 | 0 |
| monster-sociology.html | 8 | 0 |
| music-structure.html | 6 | 0 |
| narrative-experiment.html | 8 | 0 |
| philosophy.html | 6 | 0 |
| power-resources.html | 8 | 0 |
| relationships.html | 8 | 0 |
| risk-project.html | 8 | 0 |
| social-media.html | 6 | 0 |
| text-evolution.html | 10 | 0 |
| visual-art.html | 6 | 0 |
| workplace.html | 10 | 0 |

---

## 3. 已修复问题

### 3.1 文案：dashboard 快速入口描述

- **文件**：`site/index.html`
- **位置**：数据看板卡片描述
- **修复前**：`35 维度数据可视化总览`
- **修复后**：`38 专题 · 132 维度数据可视化总览`

### 3.2 文案：dashboard 副标题口径

- **文件**：`site/dashboard.html`
- **位置**：hero 区副标题 `.section-sub`
- **修复前**：`三十四大门类专题可视化`
- **修复后**：`38 个专题，34 大门类可视化总览，覆盖 A-AH 全维度`
- **说明**：统一「专题数 38」与「大门类数 34」的口径，避免与 `index.html` 描述冲突。

### 3.3 移动端表格横向滚动

- **扫描脚本**：`scripts/detect_unwrapped_tables.py`
- **范围**：`site/data/*.html` 38 个页面 + `site/dashboard.html`
- **结果**：0 个未包裹表格
- **说明**：扫描范围内 `<table>` 均位于带有 `overflow-x: auto` 或 `.table-wrap` / `.data-table-wrap` / `.climax-wrap` / `.table-wrapper` 的容器内，移动端可横向滚动。

### 3.4 game-webnovel.html 移动端负宽度错误

- **现象**：Playwright 首次截图时，mobile 视口下 `game-webnovel.html` 产生 713 条控制台错误：
  ```
  Error: <rect> attribute width: A negative value is not valid. ("-61")
  ```
- **根因**：`renderNovelBar()` 中 `webnovel-bar-svg` 的宽度仅取 `el.clientWidth || 1100`，在 375px 移动视口下内部绘图区宽度被压缩为负值；同时过渡动画的 `.attr("width", x(nv.score))` 未做非负保护。
- **修复**：
  1. `const w = Math.max(el.clientWidth || 1100, margin.left + margin.right + 120);`
  2. `.attr("width", Math.max(0, x(nv.score)));`
- 验证：重新运行 `batch_screenshots.js`，mobile 视口非预期错误数由 713 降至 0，剩余 8 条为预期的 fetch fallback。

---

## 4. 设计系统状态

- **DESIGN.md**：已创建并完整，涵盖设计原则、CSS token、组件规范（Filter Tab / Search Box / Category Badge / KPI Card / Table / Empty State）、动画、响应式断点、a11y、代码约定、禁忌清单。
- **dashboard.html**：已应用 Name That UI 的过滤标签、搜索框、分类徽章模式，支持 150ms 防抖实时过滤，ARIA 属性完整。

---

## 5. 交互与动画抽查

| 页面/组件 | 测试结果 |
|:---|:---|
| dashboard Filter Tabs | 点击过滤，卡片淡入动画平滑，空状态可正常显示 |
| dashboard Search Box | 150ms debounce 生效，清除按钮可正常清空 |
| cross-time-danmaku 年龄 Tabs | 切换可更新弹幕墙内容 |
| cross-time-danmaku 发送弹幕 | 输入后点击发送，弹幕进入 LIVE 列表 |
| 跨页面跳转 | dashboard → 数据页、数据页 → dashboard 链接可访问 |
| 卡片 hover/入场动画 | 未观察到卡顿或闪烁 |

---

## 6. 移动端可读性

- KPI 卡片在 375px 下垂直堆叠，未观察到左右溢出。
- 扫描范围内表格已包裹横向滚动容器，窄屏可左右滑动阅读。
- 修复后的 `game-webnovel.html` 在移动端未报告负宽度报错，条形图可渲染。

---

## 7. 剩余观察项

| 级别 | 问题 | 说明 |
|:---|:---|:---|
| P2 | 部分页面 fetch fallback 控制台日志较多 | 属 `file://` 协议限制，实际通过 HTTP 服务访问时不会出现；已作为预期行为记录 |
| P2 | 窄屏表格文字仍偏小 | 已提供横向滚动，受 375px 物理宽度约束，文字可读但偏紧凑 |

---

## 8. 结论

- **批量截图覆盖 40 个页面（38 数据页 + dashboard + index）**：已执行。
- **文案修复**：`35 维度` → `38 专题 · 132 维度`；dashboard 副标题同步为「38 个专题，34 大门类可视化总览，覆盖 A-AH 全维度」。
- **移动端表格横向滚动**：扫描结果 0 个未包裹表格。
- **控制台**：除预期的 fetch fallback 外未报告报错，未报告 `pageerror`。
- **JS 语法**：未报告语法错误。
- **建议**：后续如需 HTTP 服务下的 Lighthouse 评分，可启动本地服务器后运行 Lighthouse CI。
