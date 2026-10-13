# W-b 样板批 Critique 评审报告（墨韵动效 · 6 页）

> 评审框架：uicraft critique.md（10 视角 + Nielsen 10 启发式 0-4 评分）
> 评审对象：site/index.html · dashboard.html · data/{chapter-stats, character-appearance, 81-hardships, emotional-heatmap}.html
> 证据：Playwright 断言 20/20 通过（①-⑥ + ⑦⑧⑨）、6 页截图（scripts/output/screenshots/w460-wb-*.png）、代码全量走查
> 日期：2026-08-17 · W460 · 评审人：主代理（GLM-5.3）

## 判定结论

**通过 B 批启动门禁：Nielsen 总分 33/40（≥28），动效相关 finding 无 P0/P1。**

## Nielsen 启发式评分表

| # | 启发式 | 分 | 依据 |
|---|--------|----|------|
| 1 | 系统状态可见性 | 3 | tooltip 统一淡入/hover 反馈/入场编排；fetch 期间无 loading 态（-1） |
| 2 | 匹配真实世界 | 4 | 朱砂/宣纸/玄墨隐喻贯穿动效语言；「墨韵」与内容气质一致 |
| 3 | 用户控制与自由 | 3 | 筛选可重置；无显式"减少动效"控件（依赖系统 reduced-motion，隐式） |
| 4 | 一致性与标准 | 4 | 6 页统一：轴 200ms/网格 100+300ms/标记 500ms stagger 封顶 400ms/easeCubicOut；tooltip 单一样式源 |
| 5 | 错误预防 | 3 | fail-open 全覆盖（JS 失败/IO 缺失/reduced-motion → 内容直达终态）；tooltip 视口钳制 |
| 6 | 识别而非回忆 | 3 | emotional-heatmap 有 interaction-hint；其余页依赖惯例 hover 探索 |
| 7 | 灵活与效率 | 3 | focus-visible 全站；图表数据点不可键盘遍历（SVG title 部分弥补） |
| 8 | 美学与极简 | 4 | 零弹跳/零视差/时长全在预算（反馈≤150 状态≤250 入场≤500，白名单仅 count-up 900ms）；每处动效有明确目的 |
| 9 | 错误恢复 | 3 | 空数据态/mock 降级提示齐全 |
| 10 | 帮助与文档 | 3 | DESIGN.md §5 规范重写排期在 W-g（本批未写，-1） |
| **总分** | | **33/40** | 通过（≥28） |

## 10 视角快扫（关键项）

- **AI 通用感检测**：PASS——无渐变文字/玻璃拟态/发光暗色面板/克隆卡片网格；宣纸+朱砂+宋体+玄墨 hero 是强差异化视觉指纹
- **视线落点**：hero mega 数字（900 字重）→ stats count-up → KPI 卡浮起，注意力路径清晰
- **认知负荷**：决策点选项数均在 4-6 内；复杂度渐进披露（treemap→交叉表→81 难表 sticky 滚动）
- **构图平衡**：入场 stagger 封顶 400ms 防止长表/大图拖沓；退出不演（display:none）防布局抖动
- **非常态路径**：mock 数据提示、空匹配行（"无匹配项"）、暂无数据 SVG 文本均存在

## Keep（保留强化）

1. 统一 tooltip（.chart-tooltip + 视口钳制 + .visible 类切换）——6 页样式源唯一，B-E 批直接复用
2. ANIMATE 首帧门控 + reduced-motion 双守卫——resize 不重播、系统减弱动效直达终态（断言⑤⑥实证）
3. count-up 的 MutationObserver 断言法——B-E 批可复用（注意：addInitScript 会被页面 CSP 拦截，须 DCL 后 evaluate）

## Fix（分批处置，均非阻塞）

- **[P2] fetch 加载间隙无 loading 态**：6 页 fetch→render 期间图表区空白。B 批起统一 skeleton pattern（纯 CSS 呼吸底块，fail-open）
- **[P2] 图表页内嵌 KPI 无 count-up**：chapter-stats/character-appearance 的 renderKPI 与 index/dashboard 行为不一致。B 批决策：抽公共 countUp() 或维持两级差异
- **[P3] 桑基图原生 `<title>` 与 .chart-tooltip 并存**：样式不统一但键盘/读屏可达性更佳，保留现状
- **[P3] sticky 表头仅 81 难表启用**：交叉表 4 行正确跳过（>30 行才启用），符合规则

## 过程缺陷记录（B 批防复发）

1. **E20 并行 Edit 竞态复现**：81-hardships 两处 Edit 并行发出，后者覆盖前者（cross-table 的 table-anim 丢失），串行重发修复——同文件多编辑必须串行（铁律重申）
2. **断言④两次误判**：a) load 时序（动画在 load 前已开始）b) stats 在初始视口外（IO 按设计未触发）——断言必须先 scrollIntoView 再采样
3. **D3 transition 不受 CSS reduced-motion 覆写**：自查发现 4 图表页补 `matchMedia` 守卫——B 批每页必带
