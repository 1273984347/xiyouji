# tools

> 文件角色：目录导读（人读·与 index.md 分工：本文件讲用途约定、index.md 列清单）

## 这个目录装什么

《取经录》Logo 的**可复算工具链**：改字重、换配色、出新尺寸、重出概念稿，
全部从这里重跑，不依赖任何临时区、不依赖本机装字体（字标已路径化）。

| 文件 | 作用 |
| --- | --- |
| `brush.py` | 楔形笔触引擎：中线 + 宽度函数 + 左右轮廓 → 毛笔笔锋的 SVG path |
| `svgkit.py` | 字标路径化（fontTools → SVG path，零字体依赖） |
| `svgkit2.py` | 四个方向的图形库 + 组合标 + 应用图标构造 |
| `build_assets.py` | 生成全部方向资产 + 预览页 + **三道自检**（包围盒 / 视觉体量 / 笔画数） |
| `build_landing.py` | 生成落地资产（应用图标多档 + favicon + 组合标 SVG） |
| `export_png.py` | SVG → PNG（透明底）+ favicon.ico |
| `preview_png.py` | 四方向 × 深浅底拼版（不依赖浏览器，最快的视觉回路） |
| `probe_font.py` | 字体字形覆盖探针（缺字形则退出码 1） |
| `gen_concepts.py` | 分批调用生成模型出概念稿 + 下载归一 |
| `concept_args.json` / `concept_args2.json` | 两批概念稿的提示词原文 |

## 自检口径

`build_assets.py --check` 覆盖：

1. **路径包围盒**：图形必须完整落在 64×64 视口内 —— 自动抓「笔画出界 / 贴边 / 画歪」。
2. **视觉体量均衡**：各方向归一化后面积差 ≤ 15% —— 否则并排时扁的那个会明显显小
   （首轮实测：扁的棒只有方的山一半体量）。
3. **笔画数下限**：按各方向构造声明（云是「闭合轮廓 + 内部涡卷」两笔构造，故下限为 2）。

## 维护约定

- 工具链自包含：只依赖 `fontTools` / `Pillow` / `cairosvg` 三个库，不读临时区。
- 改图形请改 `svgkit2.py` 后重跑 `build_assets.py --check` + `build_landing.py`，
  产出同步到 `../logo/` 与 `site/static/icons/`。
