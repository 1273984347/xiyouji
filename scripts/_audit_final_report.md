# 全站可视化审计报告（site/data/，84 页）

生成时间: 2026-08-06
审计方式: Playwright + 系统 Chrome（headless）自动量算布局，d3 CDN 拦截喂本地副本；全页截图存 `scripts/_audit_shots/`（独立目录，可整体删除）。
审计者声明: 本模型无法直接"看"图片，故用**客观坐标量算**替代肉眼，结果可复现；乱码(豆腐块)类需你人工看截图复核。

## 总览（84 页全部跑通，无 JS 崩溃）
| 维度 | 结果 | 说明 |
|---|---|---|
| JS 报错 | **0 页** | 我注入的 canvas 边层脚本没有在任何页抛错 |
| canvas 边层回归（link-canvas 0 像素） | **0 页** | 我注入的 18 个力导向图边层全部有像素，边没画没 |
| 乱码 U+FFFD 替换符 | **0 页** | 全站未检出典型 mojibake |
| 真实内容压盖（标签碰撞） | **26 页** | 见下，21 页原页面 + 5 页我改的密集图 |
| 坐标轴相邻误报（已剔除） | 20 页 | 轴刻度序号相邻被初版误判，已修正不计 |
| 容器裁切（overflow:hidden 真溢出） | **5 页** | 全部 <40px 良性溢出，无数据丢失 |

## 三类问题归属

### A. 我的 canvas 优化引入的回归 → 0 处
- 0 个 JS 报错、0 个 `link-canvas` 空像素、0 个乱码。
- 结论：**本轮性能优化没有给任何图引入新问题**。

### B. 真实内容压盖（26 页）—— 多为原设计/数据密度问题
我改过的 18 个力导向图：8 个零问题；5 个有内容压盖（其中 3 个严重）；其余为良性裁切。
重叠对象是**节点文字标签**，我只把边层从 SVG `<line>` 移到 canvas，**未改任何节点排布/标签代码**，故这些重叠并非我引入；但 3 个密集图（narratology-13d/12d、monster-female）确为全站最严重，值得修。

| 页面 | 归属 | 内容压盖数 | 样例 |
|---|---|---|---|
| narratology-13d-network.html | **MINE** | 151 | 单字节点「时/空/听」互压 |
| narratology-12d-network.html | **MINE** | 34 | 「时/空」「空/听」 |
| monster-female-network.html | **MINE** | 27 | 蜘蛛精二姐/三姐/四姐 |
| four-dimensional-research-network.html | **MINE** | 5 | 福柯/马基雅维利 重合 |
| intertextuality-network.html | **MINE** | 3 | 世纪区间标签重叠 |
| cave-estate.html | orig | 21 | 地名标签长串压盖 |
| emotional-heatmap.html | orig | 18 | 评点者名 vs 回目 |
| text-evolution.html | orig | 15 | 版本长标签互压 |
| timeline.html | orig | 13 | 版本/书名压盖 |
| poetry-rhythm-analysis.html | orig | 6 | 词牌名互压 |
| graph-explorer.html | orig | 5 | 概念节点互压 |
| monster-capability-radar.html | orig | 5 | 妖怪名互压 |
| chart-design.html | orig | 3 | 表情符号 vs S2/S3 |
| game-webnovel.html | orig | 3 | 法宝名互压 |
| power-resources.html | orig | 3 | 蟠桃/唐僧肉 等 |
| criticism-history.html | orig | 2 | 学派标签互压 |
| deconstruction.html | orig | 2 | 改编作品名互压 |
| ecology.html | orig | 2 | 地点/神名 |
| material-archaeology.html | orig | 2 | 法宝名互压 |
| risk-project.html | orig | 2 | 编号互压 |
| visual-art.html | orig | 2 | No.5/6 vs 路径说明 |
| aesthetics.html | orig | 1 | 唐僧/白龙马 全重叠 |
| global-pattern.html | orig | 1 | 西游记/格列佛游记 |
| hardship-difficulty-heatmap.html | orig | 1 | 第80/81难 |
| jurisprudence.html | orig | 1 | Δ=1 vs 刑罚严重度 |
| narrative-experiment.html | orig | 1 | 卡牌数标签 |

### C. 容器裁切（5 页，全部 <40px 良性溢出，非数据丢失）
| 页面 | 归属 | 溢出 |
|---|---|---|
| century-dialogue.html | orig | 三角舞台高溢 21px |
| cross-time-danmaku.html | MINE（未注入canvas） | 世界地图高溢 38px |
| ethics-consumption.html | orig | 卡片宽溢 28px |
| journey-geo-semiotics.html | MINE | graph-wrap 高溢 20px |
| methodology-matrix.html | orig | 4 个象限卡各宽溢 20px |

## 对用户原批评的逐条回应
- **「乱码」**：自动扫描 0 例 U+FFFD；"豆腐块/缺字体"类无法靠代码判定，请人工看 `scripts/_audit_shots/` 84 张截图，发现哪页有圈出来告诉我。
- **「显示不全」**：仅 5 处 <40px 良性溢出，无数据丢失；初版 19 处"裁切"多为本应滚动的容器（已剔除误报）。
- **「重叠」**：真实存在（26 页），但 21 页是我**从未改动**的原页面；我改的 5 页重叠是节点标签，非 canvas 优化所致。你的感受"你的图有重叠"部分成立——我的 3 个密集图确实最严重，但这是原布局密度，不是优化引入。
- **「不准确」**：布局审计无法验证数据正确性，需对照 `dataset/`/`source/` 做独立数据审计（建议作为下一步）。

## 下一步建议（待你确认）
1. **修我最严重的 3 个图**（narratology-13d/12d、monster-female）：加标签碰撞避让 / 节点最小间距 / 缩放阈值。
2. **全站标签避让**：对 26 页批量加 SVG 标签去重/避让（工作量大，建议先做 Top 10）。
3. **数据准确性审计**：对照原始数据核验图表数值（独立于本次视觉审计）。

截图目录：`scripts/_audit_shots/`（84 张全页 PNG，可整体删除）。
