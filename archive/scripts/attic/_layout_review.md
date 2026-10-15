# 可视化布局审查报告（候选更优布局）

> 配合"语义级核验 + 49 处轴精修"交付。审查目标：识别哪些图可换更优可视化形式。
> 方法：遍历 42 数据集按结构识别图表类型与规模，结合全站可读性审计标记需优化图。

## 一、图表类型分布（42 数据集）

| 类型 | 数量 | 说明 |
|------|------|------|
| 网络图（力导向） | ~13 | 节点 5–31 不等，是数量最多的类型 |
| 雷达图 | ~10 | 维度 5–13，多数维度适中 |
| 桑基图 | ~7 | 流向/层级，语义合适 |
| 时间轴 | ~8 | 横向时间线，合适 |
| 热力图 | 3 | 合适 |
| 饼图 | 多（部分嵌套） | 顶层仅 poetry 7 扇区被捕获，其余嵌套未计 |
| 散点/柱/弦图 | 少量 | 合适 |

## 二、候选优化清单（按优先级）

### P1 · 密集力导向网络（节点 >20，力导向可读性拐点）
节点超过 20 后力导向的标签拥挤、边交叉急剧上升：
- monster-ecology-network (31)、guanyin-six-roles-network (27)、monster-hierarchy-network (23)、
  character-relationship-3d (22)、four-dimensional-research-network (24)、heaven-power-network (20)、
  underworld-power-network (19)、theological-intervention-network (18)、yuanqi-graph (20)、
  journey-map-interactive (17)

**更优布局建议（任选，均不改数据语义）**：
1. 社区聚类后按簇着色+聚合（按 faction / 类型分组），显著降低边交叉
2. 改矩阵邻接图（node-link → matrix）或多层弧长链接图（hive plot）
3. 保留力导向但加大 `forceCollide` 半径 + 稳定参数 + 缩放/拖拽交互

### P2 · 多类饼图（扇区 >5，小扇区不可读）
- poetry-rhythm-analysis（7 扇区顶层饼图）；其余饼图（美学肆、deconstruction 国家、magic 等）
  多为嵌套，需逐个核对扇区数。

**更优布局建议**：>5 类的饼图改矩形树图（treemap）或环形图（donut）+ 图例，
避免小扇区角度不可辨、标签拥挤。注意：饼图优势是"整体占比直观"，树图改后需在图例保留占比。

### P3 · 残留文字标签重叠（来自可读性审计）
上一轮全站审计 `overlapContent` 残留 16 处，散在 10 页、每页 ≤3，多为力导向图标签 /
密集分类文字标签（**非数字轴**，故未被本轮轴精修覆盖）。本轮已注入通用标签避让
（`audit-labelavoid-all`），但因部分图异步渲染可能漏覆盖。

**更优布局建议**：对残留页增大力导向 `collide` 半径或标签偏移；或对聚合型网络（见 P1）
从源头减少标签密度。

## 三、已确认健康的图
热力图（3）、桑基图（多）、雷达图（维度适中）、时间轴（多）结构合理，无需重构。

## 四、行动建议
- **高价值且低风险（建议直接做）**：P1 密集网络加社区聚类 / 稳定参数（不改图表类型，降拥挤）
- **需确认**：P2 饼图改树图是否影响"占比直观对比"语义——建议先改 poetry（7 类）试点
- **待做**：P3 残留文字标签重叠清零（依赖 P1 聚合从源头缓解）

> 说明：全局重叠/clip/乱码数据待本轮全站回归审计（`_audit_refine.js`，后台运行中）完成后补全，
> 本报告候选清单基于数据集结构静态分析 + 既有审计结论。

## 五、实施状态（2026-08-07）

### P1 聚类
- 第一批（原清单可适用 2D 力导向 6 图 + 试点 1 图）：guanyin / monster-hierarchy / four-dimensional / heaven / underworld / theological / monster-ecology ✅
- 第二批（原清单之外密集网络）：narratology-13d-network(22节点/8类) + six-senses-narratology-network(35节点/7感官) ✅ 注入 cluster-x/cluster-y 锚点，0 JS错误
- 不适用项核实：character-relationship-3d 已是 3D 环形分簇；journey-map 地理地图；yuanqi-graph 无页面；character-dynamic-network 已自聚类；perf-canvas-rendering 为 500 节点压测 demo（聚类会破坏其目的）；其余网络节点 <20 不属密集网络。

### P2 树图
- 多类饼图→矩形树图：aesthetics(7风格流派) / deconstruction(7国) / cultural-misreading(6国) / global-pattern(8国) / game-webnovel(稀有度+元素 2饼) 共 **6 饼图** ✅ 注入统一 `renderTreemap` 助手（面积=占比，保留图例值+占比与 hover tooltip），验证 cells/legends 齐全、areaRatio≈0.99、0 JS错误。
- **排除 karma-reincarnation**：其"饼图"实为 10 个独立案例实例（每个 karma_type 1 例，含 case_name/chapter/cause/effect 富 per-case tooltip），树图会丢失逐案细节，保留饼图。
- 未做（边界，≤6 类且非主占比图）：jurisprudence(6) / four-heavenly-kings-artifacts(5) / 81-hardships(3×3类小饼) 等，可视需要再扩。

### P2 延伸（2026-08-07 续）
- **jurisprudence**：`renderArtifactPie`(5 类产权类型) → treemap ✅；`renderRegistryPie` 仅 2 类且带"37.5% 审计覆盖率(3/8)"中心头条、无图例容器，属二分类特殊 donut，**保留不动**（避免丢失定制头条语义，非"多类"）。
- **81-hardships**：通用 `renderPie`(被 3 次调用) → treemap，覆盖 by_cause(4类) / by_ending(3类) / by_difficulty(2类) 共 **9 格** ✅；原外侧引线标签随树图取消（标签内显+图例即可读），零信息丢失。
- **four-heavenly-kings-artifacts 核实无饼图**：1383 行 `d3.arc` 实为 chord 图（含 `d3.ribbon`），非饼/环图，本项不适用，跳过。
- 注入守卫版 `renderTreemap`（根节点守卫，修正旧脚本源 `._inject_p2_treemaps.py` 仍缺守卫）→ 自包含 `.tm-tooltip` 样式与容器（`tipId:'tm-tooltip'`）。
- 验证 `_verify_p2c.js`：jurisprudence cells=5/legends=5/areaRatio=0.99/tip 存在/jsErr=0；81-hardships cells=9/legends=9/areaRatio=0.99/tip 存在/jsErr=0。

### P3 残留重叠清零（2026-08-07 续）
- philosophy.html 仅剩 1 处 SVG 图内非数字文字轻触：`renderAllegoryPie` donut 中心"八十一难"(y=-8,14px) 与 "81"(y=18,24px) 垂直交叠 6px → 拉开间距(y=-14 / y=22)，零信息丢失。诊断 `_diag_content_philosophy.js` 复测 `overlaps=0`。
