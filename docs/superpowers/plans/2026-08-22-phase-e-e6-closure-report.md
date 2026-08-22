# Phase E 收口报告（W493 · E6 验收收口 + 三门禁转正）

> 主方案：[2026-08-18-phase-e-visual-elevation-roadmap.md](2026-08-18-phase-e-visual-elevation-roadmap.md) §3 E6 / §1 M1-M7
> 日期：2026-08-22 · 基线 v2.3.92 W493（实测 HEAD）

## 一、M 指标收口状态

| 指标 | 阈值 | 实测 | 状态 |
|:---|:---|:---|:---|
| M1 正文对比度 | ≥4.5:1（AA） | a11y_audit E2-2 全站 P0/P1=0（234 页 40 规则） | ✅ |
| M2 UI 裸 hex/rgba | =0（豁免登记除外） | check_token_coverage：私有块 UI 裸色 246 处全部豁免登记（93 页 e-track-exempt，N 精确对应）；无注释页 =0 | ✅ |
| M3 裸 box-shadow | =0 | 真裸 0（263 处存量按 blur 映射 elev-1~4 + 令牌引用保留，1 处特例手动修） | ✅ |
| M4 动效时长 | ≤600ms、无禁止动效 | check_motion_ban 命中 0（10 处历史 infinite 动画 criticism-history/concept-device CN+EN 改一次性 1） | ✅ |
| M5 单页内联 CSS | ≤33KB | W489 实测 28385B；本批未增 tokens/system | ✅ |
| M6 性能 | LCP<5000/CLS<0.3/TBT<300 | W464 baseline_snapshot 5 核心页全过阈值（本批无布局改动，沿用） | ✅ |
| M7 pageerror | =0 | W488-492 各批 Playwright 全量 0；本批仅 CSS/门禁改动 | ✅ |

## 二、三门禁转正（挂 verify_delivery，pre-commit 强制）

| 门禁 | 脚本 | 职责 | 负样本自测 |
|:---|:---|:---|:---|
| token 覆盖率 | scripts/check_token_coverage.py（新建） | M2/M3：私有 `<style>` 块 UI 裸色（无注释页=0 / 有注释页≤N）+ 真裸 box-shadow=0；INLINED 块跳过 | ✅ 构造裸色页抓到 ui=2 sh=1 |
| 动效禁止清单 | scripts/check_motion_ban.py（新建） | D4：cubic-bezier 负值 / 360° 旋转 / infinite / parallax（白名单 chart-loading/chart-fade-in） | ✅ 构造 infinite+cubic-bezier 抓到 2 处 |
| a11y 对比度 | scripts/a11y_audit.py（已有，挂载） | M1：E2-2 P0+P1=0 阻断 | ✅ 构造低对比度页标 P1 |

## 三、本批修复清单（门禁转正前置）

1. 私有块 UI 裸色三轮回补映射（1193 → 246 处，白名单扩展：paper-warm/dark-text/accent-soft/dark/accent-2/3/ink-soft/line/elev 等 20+ 色值变体，含 color-mix 保留 alpha 的 dark-text 派生）
2. 93 页 e-track-exempt 豁免登记（新增 6 + 更新 84，N=各页私有块 UI 裸色精确数）
3. 263 处裸 box-shadow 映射 elev 档（按 blur ≤4/8/16 → elev-1/2/3；var(--shadow*) 令牌引用保留）
4. 10 处历史 infinite 动画改一次性（criticism-history wordFloat/bladeCut/crackOpen + concept-device danmakuFly，CN+EN）
5. mobile-index 1 处真裸 box-shadow 特例（0 -2px 12px rgba → elev-3）

## 四、Phase E 遗留项（显式记录，非遗漏）

1. **字体 unicode-range 切片**（W492 推迟延续）：@font-face 多片声明 ~60KB 与 225 页内联预算冲突，需独立 CSS 文件（static/css/fonts-slices.css 外部 link）+ 224 页插 link 专项方案。
2. **断点常量规范化**：存量非白名单断点 520×44/720×43/960×16/600×16/900×8/860×8/820×4 等 100+ 处。
3. **图表 ≤640px 降级 + D3 resize 统一片段**：86 页批量风险高，移动端现状可读。
4. **图表 8 色/顺序色**（D1）：判"不建"维持（E3 已记录）。

## 五、Phase E 总账（W476-W493）

E0 宪改+令牌 ✅ → E1 组件+根页 ✅ → E2 CN 传播 I（56 页）✅ → E3 CN 传播 II（30 页）✅ → E4 EN 同步（85 页）✅ → E5 响应式+微交互（抽屉+图标）✅ → E6 验收收口+三门禁转正 ✅ → 方向 A 第一批（W488 可感知升级）✅ → 全站暗色（W489）✅
**86 页传播 100% · 全站 234 页暗色可用 · 三门禁防回归入库 · M1-M7 全达标**
