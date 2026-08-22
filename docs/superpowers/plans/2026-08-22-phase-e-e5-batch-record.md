# Phase E5（W492）响应式 + 微交互 + 图标收尾 · 批次记录

> 主方案：[2026-08-18-phase-e-visual-elevation-roadmap.md](2026-08-18-phase-e-visual-elevation-roadmap.md) §3 E5
> 范围（本批落地）：导航抽屉（4 有 topnav 根页）+ 图标收尾（根页 emoji 清零）+ 触摸目标小修；字体切片/断点规范化/图表降级**显式推迟**（见范围纪律）

## 落地明细

| 项 | 内容 | 验收 |
|:---|:---|:---|
| 导航抽屉 | system.css `.nav-toggle`/`.nav-mask`/≤768 `.topnav:has(.nav-toggle) nav` 滑出面板（display:none 关闭态 + 双帧过渡 + elev-4 + 遮罩 + ESC + 窗口放大自动关）；4 根页（index/dashboard/curated/guide）HTML 汉堡按钮 + 遮罩 + JS；dashboard 补 `<link system.css>`（此前缺，抽屉规则不生效根因） | 375px 4/4：开=true 遮罩关=true 关闭态无溢出=true pageerror=0；数据页/EN 抽查无溢出（:has 保护，data 页 480 下仍 display:none 无回归） |
| 图标收尾 | 根页 emoji 扫描 = 0（W488 已换完）；guide/mobile 已 SVG | grep emoji 类 = 0 |
| 触摸目标 | index ask-chip padding 6px→10px（≈40px 高） | — |
| RM 守卫 | 抽屉过渡走全局 prefers-reduced-motion（W460 全站 media）；JS 无动画仅帧同步 | 抽查通过 |

## 范围纪律（显式推迟，非遗漏）

1. **字体 unicode-range 切片（推迟 W493）**：多片 @font-face 声明体量 ~60KB，进 tokens.css 会撑爆 225 页内联预算（+60KB×225）；需独立 CSS 文件（static/css/fonts-slices.css 外部 link）+ 224 页插 link 的专项方案，本批不混入。
2. **断点常量规范化（推迟）**：存量非白名单断点 520×44 / 720×43 / 960×16 / 600×16 / 900×8 / 860×8 / 820×4 等 100+ 处，改断点布局风险高、无感知收益；E6 收口前统一评估。
3. **图表 ≤640px 降级 + D3 resize 统一片段（推迟）**：86 页批量改动风险高，且移动端现状可读（table-wrap 横滚 + KPI 单列），收益低。
4. **dukou-engine / mobile-index 抽屉豁免**：无 topnav 结构（自有 header/移动变体），抽屉不适用。

---

## 落地状态记录（执行回写）

| 批次 | 状态 | commit |
|:---|:---|:---|
| W492 本批 | ✅ 完成 | 6063218（v2.3.91） |
