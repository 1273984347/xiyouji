# W558 五类残留缺陷修复执行报告

> 创建：2026-09-07（W558 批次产物）。执行 W557 报告 §4 登记的五类逐项修复清单。
> 验收口径：通用检测器（`_w558_detect.js`，svg 文本越界/表格挤压几何测量）+ 渲染探针 + judge 抽检 + 全量门禁。

## 1. 本批最大系统性发现：全站 CSS 缺分号（130 页 · 1006 处，已修复）

`: var(--xxx)` 声明后无分号直接换行跟下一属性——CSS 仅以分号截断声明，换行是空白 → 两条声明并为一条非法声明**整体丢弃**（每处静默丢 2 个属性：border-radius/overflow/width/margin…）。全站扫描 130 页命中 1006 处（ethics-consumption 21、narrative-experiment 22、concept-device 19、perf-canvas 10…），恰与多个无法解释的视觉 FAIL 重合。修法：`_w558_fix_semicolons.py` 机械补分号（仅命中「var() 收尾+换行+新属性」形态，style 块内）。**W557 报告「标记与 CSS 演化脱节查基类」的姊妹条目：属性丢失类缺陷查「缺分号被整条丢弃」。**

## 2. 五类修复对账

| 类 | 修复 | 页 | 验证 |
|---|---|---|---|
| A 桑基节点几何 | karma ZH/EN 右列节点 rect 移到右缘（原画在 x=0）+ 右列标签外置深色 + CSS `fill:none` 压制丝带填充移除；monster-capability ZH/EN margin 20→150；monster-ecology ZH/EN 节点纵向 20px 叠压→80px 间距 + EN 节点加宽 190 + 丝带改到节点层之下 + 浅金节点深色字 + 去白色描边晕；EN magic-system extent 140→300 | 8 页 | 截图逐张核验（karma-en/meco-zh 附前后对比） |
| B 轴边距裁切 | 检测器驱动 margin 加性扩边（单侧上限 340）21 处（cave-estate/character-presence/emotional-heatmap/ethics-consumption/ming-political/narrative-experiment/workplace/magic-system/deconstruction-scatter 等）+ 全站 chart svg `overflow: visible`（47 页，小缺口由页边距承接）+ cave-en luxury 长名截断 30 字符 + title、width 取父容器（svg 无 width 属性时 clientWidth=300 默认值导致 viewBox 压瘪的独立 bug） | 47 页 | 复测大缺口清零（cave-estate EN 310→0；mbti/ming-political/narrative-experiment/workplace 整页清零），残余 ≤120px 由 overflow 兜底可读 |
| C 标签无避让 | philosophy/character-semantic 等已由 W557 contentavoid 根治顺带解决；cave-en luxury 长名截断；其余力导向叠连（relationships/monster-hierarchy/methodology-matrix 等交互可拖拽页）登记维持 | 部分 | 截图核验 philosophy 热力图/环形图全恢复 |
| D 数据渲染缺失 | hardship-difficulty ZH/EN 求助次数空图=字段名错位（统计用 `rescue`、数据字段 `rescueCount`）→ DIM_CONFIG 补 field 映射（柱体 36/29/10/6 复活）；perf-canvas ZH/EN 时间占比条不可见=`--svg-color/--canvas-color` 被引用从未定义 + `.bar-track` 缺分号 → 补定义（分段 95%/5% 复活） | 4 页 | 截图核验（hardship 柱状 36/29/10/6、perf 分段有色） |
| E 表格挤压 | 4 页注入 `data-table` 横向滚动 + 单行不折（monster-sociology 逐字符竖排列、cognitive-psychology Flexib 表头、relationships Belbin 溢出、narratology-12d 隐藏列） | 4 页 | 探针：deconstruction 16 行全渲染 ✓、narratology-12d 11 列含 Academic Value ✓（两者为 W557 contentavoid/分号修复顺带解决） |

## 3. 验证（当批实跑）

- check_screenshot_gates 全量 234 页 FAIL 0；verify_delivery 25 门禁核心全绿；check_js_syntax 232 文件全过；CSP 0 漂移（脚本改动后两次重生成）。
- 检测器复测：77 FAIL 页中大缺口（>100px）清零；残余 D1 标记为「overflow visible 已绘制、几何仍越界」的可读状态（检测器只测几何不测可见性，口径注记）。
- judge 抽检 10 项：7 pass / 3 fail → 返工（karma-en 右列外置、meco 丝带层级+对比度、cave-en 宽度源）→ 复核全 pass（phil 首轮误截图已补正确的图表区域）。

## 4. 登记维持（不修）

- 力导向交互图的静态截图标签挤团（relationships/monster-hierarchy/methodology-matrix/graph-explorer 等）：交互可拖拽，静态快照固有。
- 检测器残余 ≤120px 几何越界：overflow visible 下文字完整可读，非缺陷。
- cross-time-danmaku 弹幕左缘裁切：弹幕滚动的截图瞬间状态。

## 5. 文件清单

- site/ 约 170 页（分号 130 + overflow 47 + margin 21 处 + 桑基/字段/对比度专项约 12 页，如上）
- scripts/_w558_detect.js、_w558_inject_overflow.py、_w558_fix_margins.py、_w558_fix_semicolons.py、_w558_fix_meco_order.py、_w558_shots.js、_w558_probe_tables.js、_w558_count_works.py（工具归档）
- 本报告；六文档 + 旁文档版本行 + site 四页脚（batch_cascade 级联）；AGENTS §4.3 补录「CSS 缺分号整条丢弃」条目。
