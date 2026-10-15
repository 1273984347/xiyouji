# Phase E · E0 探针取证报告（W476）

> 执行：2026-08-18 · 基线 git fdf439d（v2.3.78 W463）· 脚本：`scripts/_e0_probe.py`（一次性诊断，不入门禁）
> 扫描面：233 页（site 根 9 含 _template + data 87 含 _shell + en 138，探针口径；_shell 不计入统计页）

## P1 · 页面内联 `<style>` 裸色计数

- 裸 hex 共 **9336** 处、`rgb()/rgba()` 共 **6986** 处，hsl 0；**232/233 页含裸 hex**。
- 裸色最多页：concept-device（CN/EN 各 132）、ethics-consumption（各 94）、game-webnovel（各 89）、methodology-matrix / graph-explorer（各 88）。
- **口径判定**：多数裸色为图表数据色（D3 fill/stroke/渐变止点），属「图表特有」豁免类；E2/E3 的 token 覆盖验收按「UI 选择器必须走令牌、图表数据色登记豁免」执行，不搞一刀切清零（否则 1.6 万处不可操作）。

## P2 · transition 形态统计

- 含 transition 声明的页 **230/233**；`var(--dur-*)` 令牌形态 **1568** 处、`transition: all` **244** 处、裸秒值 **1208** 处。
- 秒值分布：0.15s×884 / 0.2s×248 / 0.18s×34 / 0.25s×12 / 0.6s×8 / 0.3s×8 / 0.5s×2——全部 ≤600ms，无契约违规；探针初报的「15s×10」经复核为正则误判（`.15s` 被截为 `15s`），无超长动效。
- **结论**：墨韵体系已把约 50% 过渡令牌化；剩余裸值与 `all` 形态可干净映射到 `--dur-fast(150ms)/--dur-base(250ms)`，E4/E5 微交互收编面 = 244 + 1208 处。

## P3 · 根页结构一致性（修正清单）

真实根页 = **8 页 + `_template.html`**（方案原「9 根页」口径修正：tag-cloud/search 在 data/ 下，academic-papers 仅 EN）。

| 页 | hero | topnav | site-footer | 定位 |
|:---|:---|:---|:---|:---|
| index / curated / guide | - | Y | Y | 主入口三页（无 hero 类，用深色首屏带） |
| dashboard | - | Y | -（自有 footer） | 导航中枢 |
| dukou-engine | - | - | -（长链页脚） | Agent 引擎页，结构全独立 |
| mobile-index | Y | - | - | 移动端入口 |
| rum-viewer / visit-viewer | ±- | - | - | 本地诊断页（不纳入视觉升级范围） |

- **结论**：用户可见根页 6 页（index/dashboard/curated/guide/dukou-engine/mobile-index）结构异质——无统一 hero、footer 三种形态；E1 模板化对象 = 该 6 页 + `_template.html`；两个 viewer 诊断页豁免。
- 根页内联样式合计 **1296 行**（dashboard 427 / mobile-index 348 最重）。

## P4 · 字体静态盘点（运行时抽样延至 E5）

- 7 个 woff2 在库：noto-serif-sc-shared 414KB（VF 子集 ~3700 字）/ noto-serif-sc-micro 223KB / NotoSerifSC-VF 3.6MB（全量备源，未引用可归档评估）/ NotoSansSC-Regular 771KB / NotoSansSC-Medium 783KB / JetBrainsMono×2 各 ~30KB。
- **发现**：Noto Sans SC 两档**未子集化**（正文每页真实下载 771KB），是当前最大的字体重量点；思源宋体已子集化。E1/E5 候选优化：按 w334_font_subset.py 模式子集化 Sans（预计省 ~1.4MB，改善 LCP）。
- 全部 `font-display: optional/swap`，无渲染阻塞；CLS 风险低。

## P5 · tokens/system 体积与增量预算

- 现状：tokens.css **5715B** + system.css **18904B** = 24619B/页；经 `inline_css.py --force` 内联进 **~225 页**（data 87 + en 138，均带 `../tokens.css|system.css` link）；site 根页走同目录 `<link href="tokens.css">` 实时引用、自动跟随。
- **预算判定**：tokens v3 增量 ≤ +2KB（上限 7.7KB）可行——本批实际增量见报告尾「E0 落地数字」；system v2 +6KB 上限留待 E1 草案复核。

## P6 · 公共组件选择器页面内联重复面

| 选择器 | 内联定义页数 |
|:---|:---|
| .hero / .section / footer | 227 |
| .topnav / .card | 225 |
| .site-footer / .chart-tooltip | 224 |
| .kpi-card | 85 |

- **结论**：6-8 个公共组件选择器在 ~225 页内联 CSS 中重复定义（system.css 已有同名组件）——这是页面内联样式的**最大单一膨胀源**，也是 E2/E3「页面内联只减不增」的主攻面：逐批把重复定义迁回 system.css，页面仅留图表特有规则。

## E0 落地数字（本批产出后回填）

- tokens.css：v2 5715B → v3 **7463B**（+1748B，≤ +2KB 预算内）
- DESIGN.md：新增 **§4A 纸感轻立体体系**（8 小节宪改章节）
- inline_css.py --force：225 页重新同步
- 门禁：check_structure / CSP --check / check_js_syntax / lint_links / verify_delivery 全绿

---

*报告由 W476 E0 批次产出；探针脚本 `scripts/_e0_probe.py` 按 `_` 前缀规则不入门禁不参与 CI。*
