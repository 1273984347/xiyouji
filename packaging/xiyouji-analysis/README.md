# xiyouji-analysis

《详解西游记》34 类文本分析方法工具包——把可视化站点背后的分析脚本带给研究者，对任意《西游记》文本语料复现同一套分析（词频/共现/情感/术语 NLP/结构化解读数据等）。

> 上游仓库：https://github.com/1273984347/xiyouji （代码 MIT·文本内容 CC BY-NC 4.0）
> 脚本以仓库原样分发（单一事实源 = `scripts/` A-H 类目·由 `package_analysis_sync.py` 同步）。

## 安装

```bash
pip install xiyouji-analysis   # 发布后；本地构建：pip install packaging/xiyouji-analysis/
```

## 使用

```bash
xiyouji-analysis list                      # 列出全部分析（coupled 标注 = 需仓库语料）
xiyouji-analysis run G_哲学/philosophy     # 执行单个分析
xiyouji-analysis run G_哲学/philosophy --out ./my-out
xiyouji-analysis run-all --out ./my-out    # 依序全部执行（失败不中断）
```

输出为 JSON（写入 `--out` 目录），结构与站点 `dataset/`、`scripts/output/data/` 一致。

## 范围与限制（0.1.0）

- **32 个自包含分析脚本**开箱即用（数据内嵌·纯 stdlib 零第三方依赖）。
- **5 个 coupled 脚本未入包**（chapter_stats / word_frequency / character_appearance / character_nlp / timeline）：依赖 `scripts/utils/`（jieba 分词·别名归并）与仓库 `source/`、`dataset/` 语料，待参数化（`--text-dir`/`--data-root`）后随 0.2 版入包。
- 各脚本的数据与口径说明见仓库 `docs/`（对应主题页与 `DESIGN.md`）。
- 同步机制：脚本单一事实源为仓库 `scripts/` A-H 类目，改动后跑 `python scripts/package_analysis_sync.py` 同步入包（注意清 setuptools `build/` 缓存目录后再构建——旧拷贝会混入 wheel）。

## 引用

```
《详解西游记》项目. (2026). xiyouji-analysis 0.1.0 [计算机软件].
https://github.com/1273984347/xiyouji
```
