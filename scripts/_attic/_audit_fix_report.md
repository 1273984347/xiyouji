# 全站可视化「全部做」执行报告（修复 + 验证 + 数据审计）

日期: 2026-08-06
范围: site/data/ 84 页；本次针对用户"重叠/乱码/不准确/显示不全"四项质疑，执行三类修复 + 数据审计。

## 已执行的三项修复（均已提交 git）
| Commit | 内容 | 影响页 |
|---|---|---|
| 358208e | 全站图表标签白边光晕（svg text 白色描边，提升重叠可读性）+ 力导向图加大 forceCollide 半径 | 84 页（白边）/ 11 页（碰撞） |
| f03b8e3 | 力导向图注入标签碰撞避让（重叠时隐藏较小次标签，保留重要标签；节点 hover 仍有 tooltip 给全信息） | 18 个力导向图 |

## 验证结果（留痕，符合硬性规矩）
- Playwright 全量复测（84 页）：**0 个 JS 报错、0 个 evalErr**。
- 回归冒烟（我改的 18 图 + 11 碰撞图，20 页）：**0 失败**（link-canvas 边层有像素、节点定位正常）。
- 加大碰撞半径**实测对几何重叠零改善**（节点散开仍不够）→ 改用"标签避让"才见效，已如实记录。

## 重叠修复成效（标签避让前后对比，几何重叠数）
| 指标 | 修复前 | 修复后 |
|---|---|---|
| 全站内容压盖总数 | 329 | **113（-66%）** |
| 内容压盖页数 | 26 | 23 |
| narratology-13d-network | 151 | **0（100%）** |
| narratology-12d-network | 34 | **0（100%）** |
| monster-female-network | 27 | **3（89%）** |

18 个力导向图全部降到 0 / 近 0（仅 graph-explorer 未纳入目标保留 5 处；monster-female 余 3 处为等尺寸标签）。

## 残留问题（需后续定制，非本次引入）
- **23 个非力导向图**（cave-estate 21、emotional-heatmap 18、text-evolution 15、timeline 13、poetry 6 等）
  仅加了白边可读性，**重叠仍几何存在**，需各自定制避让（热力图/时间轴/雷达等不同图表类型，无法一套脚本通吃）。
- 乱码（豆腐块/缺字体）：自动扫描 0 例 U+FFFD；"缺字体"类需你人工看 `scripts/_audit_shots/` 截图确认（模型无法直接看图）。

## 数据准确性审计结论
方法：对 20 个网络图，递归提取 `dataset/*.json` 节点/边数组，对比渲染后 DOM 的 svg circle/line 数。
- **关键限制**：这些页多为"网络+sankey+radar+timeline 多图表同屏"，DOM 计数远大于 JSON 网络节点数属正常；且 `character-dynamic-network`/`relationships`/`character-semantic` 数据**内联在 HTML**，无外部 JSON 可对照 → 自动计数比对不可靠。
- 唯一干净单网络页 `journey-geo-semiotics`：JSON 7/7 = DOM 7/7，**完全吻合 ✓**。
- `character-relationship-3d` DOM 0/0 系 WebGL/three.js 渲染（非 SVG），非数据丢失。
- **未发现任何"数据丢失/数值不一致"证据**；但全站数值是否贴合原著，需人工对照 `source/原文` 做语义核验（自动化无法替代）。

## 下一步（待确认）
1. 非力导向图 Top 重叠页（cave-estate/emotional-heatmap/text-evolution/timeline）逐类定制避让。
2. 指定具体图表/数值，做 `source/原文` 语义级数据核验。
3. 人工核对 `scripts/_audit_shots/` 截图，圈出仍存在的乱码/重叠页。

截图目录：`scripts/_audit_shots/`（84 张全页 PNG，可整体删除）。
审计/修复脚本：`scripts/_inject_halo.py`、`_inject_collide.py`、`_inject_labelavoid.py`、`_audit_refine.js`、`_verify_fix.js`、`_audit_data.js`（均幂等/可复跑）。
