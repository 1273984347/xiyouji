# 第 82 门禁 · 单系列图图例豁免 · 渲染级复核表（W1266 线 A1）

生成：py -3 scripts/output/_w1266_render_legend.py（Playwright file://·只读渲染·未改任何页面）
机器读副本：scripts/output/chart-legend-render-audit.json（判据输入）

## 分类口径（渲染级实证）

渲染级分类口径 v2（修正 v1「按 id/class 关键词单判」的错误——JS 动态创建的图表 svg 无 chart 类名）：· 尺寸门槛：w ≥ 120 且 h ≥ 80 = 可承载图表的画布；小于此 = 图标尺度；· chart（图表）：画布达标 且（可见文本标签 ≥1 或 数据图元 ≥3 或 id/class 命中图表词表）；· illustration（装饰插画）：画布达标 但（无文本 且 图元 ≤2 且未命中图表词表）⇒ 不计图表；· small_graph（迷你图）：画布不达标 但（文本 ≥1 或图元 ≥3）；· icon（图标）：画布不达标 且（图元 ≤2 且无文本）；· 页面级三分类：has_chart（有图表 svg）/ env_blocked（静态有图表语义但渲染后无图表 svg ⇒环境性未加载·file:// fetch 失败等 ⇒ 不计入真无图）/ no_chart（只有图标或插画且静态无图表语义 ⇒ 真无图）

| 页面 | 页面级结论 | 图表svg | 图例项 | 系列证据 | 可见图例 | 判定 | 依据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| site/about.html | no_chart | 0 | 0 | 0 | 无 | nochart | 渲染后无图表 svg·全部 svg 为图标/插画且静态无图表语义 ⇒ 真无图 ⇒ 本无图·图例判据不适用 |
| site/curated.html | no_chart | 0 | 0 | 0 | 无 | nochart | 渲染后无图表 svg·全部 svg 为图标/插画且静态无图表语义 ⇒ 真无图 ⇒ 本无图·图例判据不适用 |
| site/dashboard.html | has_chart | 3 | 18 | 4 | 有 | multi_legend | 渲染后可见图例 18 项（≥2 ⇒ 多系列且图例齐备） |
| site/data/81-hardships.html | has_chart | 4 | 9 | 5 | 有 | multi_legend | 渲染后可见图例 9 项（≥2 ⇒ 多系列且图例齐备） |
| site/data/ai-dialogue.html | env_blocked | 0 | 0 | 0 | 无 | unknown | 渲染后无图表 svg·但静态有图表语义容器/图表库调用 ⇒ 环境性未加载（file:// fetch 失败等）⇒ 不计入真无图 ⇒ 渲染级不可判定（环境性未加载） |
| site/data/century-dialogue.html | env_blocked | 0 | 0 | 0 | 无 | unknown | 渲染后无图表 svg·但静态有图表语义容器/图表库调用 ⇒ 环境性未加载（file:// fetch 失败等）⇒ 不计入真无图 ⇒ 渲染级不可判定（环境性未加载） |
| site/data/character-relationship-3d-view.html | env_blocked | 0 | 0 | 0 | 无 | unknown | 渲染后无图表 svg·但静态有图表语义容器/图表库调用 ⇒ 环境性未加载（file:// fetch 失败等）⇒ 不计入真无图 ⇒ 渲染级不可判定（环境性未加载） |
| site/data/data-explorer.html | has_chart | 1 | 0 | 4 | 无 | multi_nolegend | 渲染后无可见图例·但系列证据 4 ⇒ 多系列却无图例 |
| site/data/text-search.html | env_blocked | 0 | 0 | 0 | 无 | unknown | 渲染后无图表 svg·但静态有图表语义容器/图表库调用 ⇒ 环境性未加载（file:// fetch 失败等）⇒ 不计入真无图 ⇒ 渲染级不可判定（环境性未加载） |
| site/dukou-engine.html | no_chart | 0 | 0 | 0 | 无 | nochart | 渲染后无图表 svg·全部 svg 为图标/插画且静态无图表语义 ⇒ 真无图 ⇒ 本无图·图例判据不适用 |
| site/en/81-hardships.html | has_chart | 4 | 9 | 5 | 有 | multi_legend | 渲染后可见图例 9 项（≥2 ⇒ 多系列且图例齐备） |
| site/en/ai-dialogue.html | env_blocked | 0 | 0 | 0 | 无 | unknown | 渲染后无图表 svg·但静态有图表语义容器/图表库调用 ⇒ 环境性未加载（file:// fetch 失败等）⇒ 不计入真无图 ⇒ 渲染级不可判定（环境性未加载） |
| site/en/century-dialogue.html | env_blocked | 0 | 0 | 0 | 无 | unknown | 渲染后无图表 svg·但静态有图表语义容器/图表库调用 ⇒ 环境性未加载（file:// fetch 失败等）⇒ 不计入真无图 ⇒ 渲染级不可判定（环境性未加载） |
| site/en/guide.html | no_chart | 0 | 0 | 0 | 无 | nochart | 渲染后无图表 svg·全部 svg 为图标/插画且静态无图表语义 ⇒ 真无图 ⇒ 本无图·图例判据不适用 |
| site/en/text-search.html | no_chart | 0 | 0 | 0 | 无 | nochart | 渲染后无图表 svg·全部 svg 为图标/插画且静态无图表语义 ⇒ 真无图 ⇒ 本无图·图例判据不适用 |
| site/guide.html | no_chart | 0 | 0 | 0 | 无 | nochart | 渲染后无图表 svg·全部 svg 为图标/插画且静态无图表语义 ⇒ 真无图 ⇒ 本无图·图例判据不适用 |
| site/index.html | no_chart | 0 | 0 | 0 | 无 | nochart | 渲染后无图表 svg·全部 svg 为图标/插画且静态无图表语义 ⇒ 真无图 ⇒ 本无图·图例判据不适用 |

判定分布：multi_legend=3、multi_nolegend=1、nochart=7、unknown=6
