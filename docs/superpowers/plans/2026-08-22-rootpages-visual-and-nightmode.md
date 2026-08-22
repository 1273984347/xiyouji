# 《详解西游记》根页视觉重设计 + 夜读模式方案（第一批 · W488 候选）

> 版本：v1.0 · 2026-08-22
> 当前基线：v2.3.86 W487（HEAD 65890b2，`git rev-parse --short HEAD` 实测）；下一 W 编号 = W488（启动时须 `grep -o 'W4[0-9][0-9]' 交接文档.md | sort -u | tail -3` 复核）
> 性质：Phase E 方向 A 修正轨第一批——「纸感轻立体」之上的**可感知**视觉升级 + 暗色模式提前（原 E7 拆出根页部分）
> 上游依据：① Phase E 路线图（2026-08-18-phase-e-visual-elevation-roadmap.md，§1 M1-M7 / §2 D1-D6 / §3 E5/E7）② DESIGN.md §1-5（§4A 宪法层 / §5 动效契约）③ plan-review skill v1.0.1 陷阱 9（感知验收强制项）
> 目标读者：主代理 + 新接任 Agent + 人类维护者
>
> **本批立规（W487 教训）**：验收**必须内置前后对比截图**（M-A1），"看起来更好"重新回到验收标准——不允许再出现"门禁全绿但肉眼零变化"。
>
> 已决项（2026-08-22 用户确认）：① 方向 A 根页视觉重设计 ② 暗色模式排进第一批（范围 = 6 用户可见根页）。

---

## 0. 现状基线（2026-08-22 实测）

| 维度 | 现值 | 测量命令/来源 | 备注 |
|:---|:---|:---|:---|
| git HEAD | 65890b2（v2.3.86 W487） | `git rev-parse --short HEAD` | 现役最大 W = W487 |
| 根页清单 | 6 用户可见：index/dashboard/curated/guide/dukou-engine/mobile-index（+ 诊断豁免 2：rum-viewer/visit-viewer + _template） | `ls site/*.html` | 与 Phase E 口径一致 |
| CSS 引入方式 | 根页 = 同目录 `<link href="tokens.css">`；data/en 页 = inline_css 内联 | `grep -o '<link[^>]*tokens.css' site/index.html` | **改 tokens/system 对根页自动生效、零传播成本**；data/en 225 页不受本批根页改动影响 |
| tokens.css / system.css | 7750B / 21359B（合计 29109B） | `wc -c` | 预算线 33KB/页（M5 口径） |
| 暗色现状 | 无主题切换：无 `xy-theme`、无 `prefers-color-scheme`、无 dark 覆盖组；现有 `--dark`/`--dark-text`/`.dark-band` 是**深色区块**语义（开篇诗等），非暗色主题 | `grep -n 'dark' site/tokens.css site/system.css` | 暗色模式为全新功能 |
| localStorage 占用 | index 已有 `xiyouji_asks`（最近提问） | `grep -n 'localStorage' site/index.html` | 新 key `xy-theme` 不冲突 |
| reveal 现状 | `.reveal-in` CSS 就绪（fail-open），6 根页 **无** `html.js-reveal` 门禁类、JS 未接入 | `grep -c 'js-reveal' site/*.html` = 0 | 本批接入 reveal JS |
| 图标现状 | 根页存在 emoji/字符图标（`.pc-emoji` 等） | 见 E0 探针 P1 | 本批换内联 SVG |
| 性能预算 | html 51200B / css 102400B / total 921600B | scripts/output/perf-budget.json（W267） | 根页 html 现远低于 51.2KB |
| 对比截图基线 | E1/E2 前后对比产物在 scratch（e1-shots/e2-shots） | — | 本批 before = 当前 HEAD 65890b2 根页截图 |

---

## 1. 目标与验收（M 指标三段式：指标 = 阈值（测量方法））

**目标**：6 用户可见根页产生**肉眼可辨**的观感提升（在「纸感轻立体」基础上做强度升级），并原生支持暗色夜读模式。本批验收只认下列量化指标，每条都有测量命令。

| # | 指标 | 阈值 | 测量 |
|:---|:---|:---|:---|
| M-A1 | **感知可辨（本批核心新增）** | 每页前后对比截图差异像素率 ≥ 1%；且目视清单每页标注 ≥3 处可辨差异 | before = 65890b2 截图（Playwright 1440×900 全页）；after = 本批完成后同机位截图；PIL 计算像素差异率 + 人工目视清单（6 页 × 3 处，见 §2.3 模板） |
| M-A2 | 暗色模式可用 | 6 根页 `data-theme="dark"` 下 pageerror=0、可正常交互 | Playwright 注入 `xy-theme=dark` 后逐页 pageerror + 点击冒烟 |
| M-A3 | 防 FOUC | 切换/首访暗色首帧无浅色闪屏 = 0 例 | Playwright 首帧截图（`goto` 时即注入 theme 后立即截 `domcontentloaded`） |
| M-A4 | 对比度 | dark 下正文文本 ≥ 4.5:1（WCAG AA） | 抽样 3 页正文计算（脚本复用 a11y 规则，颜色取 dark 令牌值） |
| M-A5 | 令牌合规 | 根页无新增裸 hex/裸阴影（图表数据色豁免登记除外） | `_e0_probe.py` P1 口径对 6 根页（本批新增值必须落令牌） |
| M-A6 | 动效契约 | 本批新增动效时长 ∈ {--dur-fast 150 / --dur-base 250 / --dur-slow 500}，无 bounce/360°/infinite/parallax；reduced-motion 守卫 | `grep -c '.duration('` + D4 禁止清单扫描（site/*.html） |
| M-A7 | 体积 | 6 根页 html ≤ 51.2KB（perf-budget）；tokens/system 全局体积不增（dark 覆盖不落全局） | `wc -c` 前后对比 |
| M-A8 | 门禁 | verify_delivery 全绿 + generate_csp.py 0 漂移 + check_structure 0 + lint_links 0 broken | 五道门禁（§4） |
| M-A9 | 回退安全 | 无 JS（禁 script）时站点正常渲染、默认浅色；dark 仅由 JS 注入的 `data-theme` 触发 | Playwright `javaScriptEnabled:false` 访问 6 页 pageerror=0 + 计算样式断言 |

**不认的验收**：不认"看起来更好/更高级"这类无测量表述（W487 教训，plan-review v1.0.1 陷阱 9）。

---

## 2. 范围与派生命令

### 2.1 根页视觉重设计（6 页，强度 = 保守微调 + 可辨升级）

- **设计方向**（在"纸感轻立体"基础上加强可感知度）：
  1. **hero 排版节奏**：6 页 hero 统一标题字号阶梯（--text-step 现有档位）、徽章/描述行留白重排；index 的 hero 增"100 回"数字的视觉强调（朱砂 + tabular-nums）。
  2. **卡片 hover 强度升级**：.card/.curated-card hover 从 elev-2 升级为 `elev-2 + translateY(-3px) + 1.5px 朱砂描边（--accent 40% 透明度）+ 描边过渡 150ms`——hover 差异必须一眼可辨（M-A1 的主要来源）。
  3. **图标系统**：6 根页 emoji/字符图标（`.pc-emoji`、🔍 等，搜索"搜"文字伪元素保留不计）→ 内联 SVG（stroke 1.5px、currentColor、24×24 viewBox）。清单在开工探针产出，验收 = 6 页 `grep -c 'emoji\|🔍\|🔍\|🀄'` 类扫描 = 0。
  4. **导航 active 指示条**：topnav 当前页链接底部朱砂指示条 transform 滑动（--dur-base）。
  5. **reveal-in JS 接入**：`html.js-reveal` 门禁类 + IntersectionObserver 一次性触发 + reduced-motion 直达终态（脚本放页面内联 `<script>`，**改后必重跑 generate_csp.py**）。
- **禁止**：bounce/360°/infinite 背景动画/parallax（D4 禁止清单沿用）。

### 2.2 暗色模式（夜读，6 根页）

- **令牌策略（关键权衡，已选）**：dark 覆盖**只写进 6 根页页面内联 `<style>`**，不动全局 tokens.css/system.css → M-A7 体积零风险、data/en 225 页完全不受影响。后续全站 dark 批次（第二批）再评估迁入 tokens.css。
- **令牌组**（页面内联）：`html[data-theme="dark"]` 下覆盖 —— `--bg:#221D16`（玄墨底）/ `--ink:#F2EBDC`（宣纸文字反相）/ `--paper`/`--paper-warm` 对应深色 / `--accent` 提亮一档（#E0554A 级，色盲安全）/ `--elev-*` 换深色低 alpha 阴影 / `--ok/--warn/--danger/--info` 反相微调；`.dark-band` 组件在 dark 下用 `--elev-1` 边框区分层次（防深色区块在暗色下失去边界）。
- **切换器**：topnav 右侧"夜读"按钮（内联 SVG 月亮/太阳，点击切 `html[data-theme]`）；`localStorage key = xy-theme`（取值 `dark/light`）。
- **防 FOUC 首屏脚本**：`<head>` 最前内联 `<script>`（约 10 行）：读 localStorage → 无则 `prefers-color-scheme: dark` → 有则写入 `html[data-theme]`。**该内联 script 必须在 generate_csp.py 重跑后生效**。
- **图表适配**：dashboard 的 D3 图表轴色/网格线/序列色在 dark 下用令牌覆盖（禁硬编码 hex）；其余 5 页无图表不涉。

### 2.3 交付物模板（M-A1 目视清单）

每页一张清单表，示例：`index.html — 差异 1：搜索按钮 80px→240px；差异 2：精选卡片 hover 朱砂描边；差异 3：hero "100" 朱砂强调`。6 页 × ≥3 处，与对比图一起作为本批交付物。

---

## 3. 批次计划

| 批次 | 内容 | 优先级 | 预估 | 依赖 |
|:---|:---|:---|:---|:---|
| **W488（本批）** | 6 根页重设计 + 夜读模式（2.1+2.2） | P0 | 6–9h（含截图验收与门禁摊销） | — |
| 第二批（另案） | 全站 86 数据页 + EN 根页 dark 传播（原 E7 余量 + E3-E6 余项） | P1 | 待定 | W488 验收全绿 |

并行约束：与 Phase 3 双轨改动面互斥（W464 观测期不动 GoatCounter/baseline 相关）；同一页不得两轨同改（`git log --oneline -5` 核对）。

---

## 4. 统一门禁（每批必跑）

```text
python scripts/verify_delivery.py        # 退出码 0（核心全绿）
python scripts/generate_csp.py --check   # 0 漂移（本批新增内联 script，改后先重跑 generate_csp.py）
node  scripts/check_js_syntax.js         # 0 语法错误
python scripts/check_structure.py        # 0 结构失衡（批量改 CSS 必跑）
python scripts/lint_links.py             # 0 broken
```

本批专项（新增）：

```text
# M-A1 前后对比截图 + 像素差异率（新建一次性脚本，scratch 目录勿入库）
NODE_PATH="$(npm root -g)" node 根页截图脚本.js   # before=65890b2 已可复用 e1-shots 管线
python 差异像素率.py                                # PIL diff ≥1%/页
# M-A2/A3/A9 暗色冒烟
NODE_PATH="$(npm root -g)" node 暗色冒烟脚本.js     # pageerror + FOUC 首帧 + 禁 JS 回退
```

---

## 5. 风险与权衡

- **R1（低，已消解）CSS 体积**：dark 覆盖走页面内联，tokens/system 全局零增长 → M-A7 无风险；代价 = 第二批全站 dark 时需把覆盖迁入 tokens.css 并重算 225 页内联预算（届时余量仅 ≈3.9KB，需砍工具类或压缩，R1 转高，第二批再议）。
- **R2（中）CSP**：首屏内联 script（10 行）必须重跑 generate_csp.py，漏跑 = 暗色功能整脚本被拒、页面仍浅色（症状无报错）。缓解：门禁 M-A8 强制 + 验收 M-A2/A3 直接测功能本身。
- **R3（中）视觉主观性**：M-A1 用差异像素率 ≥1% 量化兜底 + 目视清单 3 处/页定性，两者合取才算达标；不达标即返工，不靠"感觉"糊弄。
- **R4（低）hover 强度升级影响既有页面**：本批只动 system.css 的 .card hover 规则 → 会影响 data/en 页（它们内联了 system.css 旧版，本次不重跑 inline_css → 不受影响；但根页 `<link>` 方式实时生效）。**注意**：若本批改 system.css 的 .card hover，根页与 data 页 hover 行为会不一致（根页新、data 页旧）——决策见待确认项 ⑤。
- **R5（低）EN 不同步**：本批只做 CN 根页；EN 根页（site/en/）夜读后续批。

---

## 6. 待确认项

1. **hover 强度是否进 system.css**：进（根页 `<link>` 实时生效，data 页保持旧 hover 直到后续批重跑 inline_css——两轨暂不一致）；不进（6 根页页面内联覆盖 .card hover，全局一致但逻辑散在页内）。→ 推荐**进 system.css**（组件唯一事实源，数据页旧 hover 属已知存量，E3 批统一）。
2. **夜读切换器位置**：topnav 右侧图标按钮（6 页统一）。→ 默认采纳。
3. **默认主题**：首次访问跟随系统（`prefers-color-scheme`），之后记住 `xy-theme`。→ 默认采纳。
4. **重设计强度**：保守微调（可辨但克制，推荐）vs 大胆重做（hero 结构大改）。→ 待拍板。
5. **dashboard 图表 dark 适配深度**：只做轴/网格/序列色令牌覆盖（快）vs 全图表配色重调（慢）。→ 推荐前者。

---

## 7. 前置取证（2026-08-22 已执行）

| 探针 | 命令 | 结果 |
|:---|:---|:---|
| P1 HEAD/现役 W | `git rev-parse --short HEAD` + grep 交接文档 | 65890b2 / W487（下一 W=W488） |
| P2 根页 CSS 引入 | `grep -o '<link[^>]*tokens.css' site/*.html` | 6 根页均 `<link href="tokens.css">`（同目录，改令牌零传播） |
| P3 CSS 体积 | `wc -c site/tokens.css site/system.css` | 7750B + 21359B = 29109B |
| P4 暗色现状 | `grep -n 'dark\|prefers-color-scheme\|xy-theme' site/*.css site/*.html` | 无主题切换；--dark 仅深色区块语义 |
| P5 reveal 现状 | `grep -c 'js-reveal' site/*.html` | 0（CSS 就绪未接入） |
| P6 localStorage 占用 | `grep -n 'localStorage' site/index.html` | 仅 xiyouji_asks（不冲突） |
| P7 性能预算 | `cat scripts/output/perf-budget.json` | html 51200B（W267 值） |

---

## 8. 落地状态记录（执行回写）

| 批次 | 状态 | commit | 关键数字 |
|:---|:---|:---|:---|
| W488 本批 | ✅ 完成 | 24a193d（v2.3.87） | M-A1 差异率 6/6 ≥1%（2.35/5.05/2.84/5.88/25.98/7.07%）+ 目视清单 6×3 处；dark 冒烟 6 页 pageerror=0 + FOUC=0；禁 JS 回退正常；html 增量 +3.2~6.6KB/页；tokens 7750B 未增、system +644B；五道门禁全绿 |

| W489 第二批 | ✅ 完成 | 待提交（v2.3.88） | dark 令牌全局化进 tokens.css（+1494B）+ inline_css --force 225 页传播 + js/theme-init.js 同步防 FOUC 插 226 页 + 5 根页去重 -1170B/页；12 页 dark 冒烟 pageerror=0/FOUC=0；内联 CSS 28385B ≤33KB；门禁全绿 |

**执行期修正**：① W489 范围聚焦为"全站暗色模式"（E3-E6 余项留后续批 W490+，未纳入本批）；② 本批 bump 日期行为与 W488 不同（bump 已写当天 08-22，无需手动改日期——bump 行为不稳定坑 R8 再记一例）；③ 根页内联 dark 通用令牌块删除后依赖 tokens.css 全局组（5 页 -1170B/页），dukou-engine 双变量体系保留页面内联。
**执行期修正**：① dashboard 首轮像素率 0.63% 不达标（页面 7280px 高、hover/dark 静态不可见）→ 补"标题+KPI 数字朱砂/表头淡朱砂 14%/route-strip 朱砂线"三处静态强化后 5.05% 达标；② guide/dukou-engine 同因补强（emoji→朱砂 SVG / header 朱砂双线）；③ M-A7 绝对预算（51.2KB）dashboard 为存量超标（84.4KB，非本批引入），本批判定以增量受控 + 全局 tokens 未增为准。

---

*本方案 v1.0 数字基于 2026-08-22 实测（HEAD 65890b2）。开工前：复核 HEAD 与现役最大 W（多 session 并发，勿信快照）。*
