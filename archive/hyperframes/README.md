# 详解西游记 · HyperFrames 视频架构

W206 视频化方向：短 + long 并行多视频架构。基于 HyperFrames HTML composition + GSAP 动画，古典宣纸风视觉规范。

## 目录结构

```
hyperframes/
├── index.html                                  # 原始视频（方法论分享，5 场景 40s，保留不动）
├── package.json                                # render 脚本与依赖
├── README.md                                   # 本文件
├── compositions/                               # 多视频 composition 源
│   ├── methodology-sharing.html                # 方法论分享（index.html 同源，版本戳 v2.2.27）
│   ├── dashboard-showcase.html                 # 数据仪表盘展示（longer-form，42s，6 场景）
│   └── d3-visualizations/
│       └── narratology-13d-network.html        # 十三维叙事学网络（短视频，7s，4 场景）
└── output/                                     # MP4 渲染产物（gitkeep 占位）
    └── .gitkeep
```

## Composition 说明

### methodology-sharing.html
- 类型：longer-form 方法论分享
- 时长：40 秒
- 分辨率：1920x1080
- 场景：封面 / 项目规模 KPI / DRL 真循环 / 三 skill 闭环 / 结尾
- 来源：由 `index.html` 复制，版本戳同步至 v2.2.27

### narratology-13d-network.html
- 类型：短视频（video-shortform）
- 时长：7 秒
- 分辨率：1920x1080
- 场景：标题卡 / 力导向图入场 / 关键节点高亮 / 版本戳结尾
- 数据：22 个节点（13 叙事维度 + 9 关键概念）+ 28 条连线

### dashboard-showcase.html
- 类型：longer-form 仪表盘展示
- 时长：42 秒
- 分辨率：1920x1080
- 场景：项目概览 / dashboard hero / KPI 卡片网格 / 分类过滤演示 / 搜索演示 / 结尾

## 视觉规范

古典宣纸风，所有 composition 复用同一组 CSS 变量：

- 背景 `--bg: #faf7f2`
- 纸面 `--paper: #ffffff`
- 墨色 `--ink: #2c2418`
- 主色 `--accent: #c8463a`
- 辅色 `--accent-2: #3a6b8c` / `--accent-3: #7a5230` / `--accent-4: #5a7a3a`
- 深色 hero 渐变 `--hero-1: #1a1410` → `--hero-2: #3a2820` → `--hero-3: #5a3828`

字体：Noto Serif SC（正文）+ JetBrains Mono（数据/标签），均通过 `local()` 加载。

动画：GSAP 3.14.2 CDN，时间线注册至 `window.__timelines["root"]`。

## 依赖安装

```bash
cd hyperframes
npm install
```

## Studio 预览

```bash
npx hyperframes preview
```

在浏览器中打开 Studio，可拖动时间轴逐帧预览各 composition。

## 渲染 MP4

```bash
# 单个渲染
npm run render:methodology    # 方法论分享
npm run render:short          # 十三维叙事学网络（短视频）
npm run render:long           # 数据仪表盘展示（longer-form）

# 全部渲染
npm run render:all
```

渲染产物输出至 `output/` 目录。

## 校验

```bash
npx hyperframes lint          # 语法检查
npx hyperframes validate     # WCAG 对比度审计
npx hyperframes inspect      # 视觉布局检查
```

## 版本

- 当前版本：v2.2.27
- 落地日期：2026-07-29
