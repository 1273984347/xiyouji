# WP-D2 阅读器扩量 · 实施蓝图（PD 档惯例 · W659 规划入档）

> **档别**：实施蓝图（登记 + 规则固化 + 验收机判），**本档不直接改页面**——实现批 W660 按 §4 执行。
> **上游**：master plan WP-D2（2026-09-21 入档·§L172）·W626 归档裁决经用户 2026-10-03「全部启动」点名解除（工程呈现层非内容生产）·W651 入档。
> **取证时点**：2026-10-04，HEAD = 1fa0794 后（W656 已落地）。数据随批现测。

## 1. 范围（现状实测）

| 板块 | 源目录 | 篇数（md 含 README） | reader 目标子目录 |
|---|---|---|---|
| 01 逐回解读 | docs/01-全书逐回解读 | 100 + README | reader/（已有 · W593） |
| 02 人物深度 | docs/02-人物深度分析 | 216 | reader/people/ |
| 03 主题专题 | docs/03-主题与情节专题 | 210 | reader/themes/ |
| 04 文化背景 | docs/04-文化与历史背景 | 35 | reader/culture/ |
| 05 诗词歌赋 | docs/05-诗词歌赋 | 14 | reader/poetry/ |
| 06 个人随笔 | docs/06-个人随笔 | 45 | reader/essays/ |

520 篇（README 除外）/ 五板块全量实测。chNNN.html 现网 100 页保留不动。

## 2. 链接形态普查结论（520 篇·W659 现测）

| 形态 | 量级 | 改写策略 |
|---|---|---|
| 板块内 md 相对互链 | 主体 | → 同目录 .html（W593 规则①同构） |
| 跨板块 0x 互链 | 549 | → reader 内板块路径（../people/… 等） |
| 跨板块 01 互链 | 4 | → reader/chNNN.html |
| ../../site/data/*.html 可视化 | 多 | → ../../data/xxx.html（W593 规则③同构） |
| ../../site/index.html | 多 | → ../../index.html |
| ../../source/…、GitHub blob | 少量 | → 保持外链（源文本不在站内） |
| README / _templates / 根治理 | 少量 | README 不渲染；模板/治理链接 → GitHub blob |
| 图片 | 待查 | 有则复制进 reader/assets/（W593 规则④） |

## 3. 架构决策（三条硬约束沿 W593 先例）

1. **file:// 直开零依赖**：reader 内相对路径；无外域；d3 无关（纯文本页）。
2. **token 全量**：页面内联 tokens.css+system.css（inline_css --force 覆盖 site/reader/**）。
3. **每板块独立子目录 + 板块内 prev/next 按文件名排序**；跨板块链接按 §2 改写。

## 4. 实现批拆分（W660 起依序）

| 批 | 内容 | 验收（机判） |
|---|---|---|
| W660 | build_reader.py 多板块改造（映射表驱动）+ 520 篇渲染 + 六板块目录 + sitemap/INDEX 补录 | 页数=520+100+目录；lint_links 0 broken（reader 域）；js 语法过 |
| W661 | 搜索索引站内化扩量（docs/01-06 615 条→对应 reader 页）+ footer-meta blob 改链收敛 + blob 预算复核（master plan ≤1000） | blob 引用实测 ≤1000；搜索黄金查询过 |
| W662 | 暗色审计 S2 全量（reader 新页入基线）+ Screenshot Review 定向 + 遗漏收敛 | CI 五工作流绿 |

## 5. 风险与依赖（沿 W593 执行记录）

- 02/03 板块 md 内互链密度高（板块内专题互引）——板块内排序 prev/next 按文件名排序可能与互链语义不一致（已知取舍·W593 同款）。
- 04/05/06 板块含 README.md 与 _templates 引用——渲染时跳过 README、治理/模板链接转 GitHub blob。
- inline_css --force 重分发后 336+621=957 页（新增 621=520+100+目录）——token 覆盖率门禁分母变化需核对（以脚本输出为准）。
- sitemap 229→~750 条（D-1 口径行维持 W650 批注·差额查因挂 PD-1a）。
