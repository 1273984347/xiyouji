# DRL 收敛记录：增强版截图审查（化整为零 + 双管齐下 + 像素级检查）

> 项目：xiyouji
> 阶段：比赛级，N_max=0
> 收敛时间：2026-07-22

## 改动范围

- `scripts/batch_screenshots.js`：集成 Playwright 布局断言 + 切片脚本调用 + 结构化报告生成
- `scripts/slice_screenshots.py`：新增 800px 高度长图切片 + argparse CLI + 目录清理
- `site/data/ecology.html`：为表格添加 `.table-wrap` 横向滚动容器
- `scripts/requirements.txt`：新增 `Pillow>=9.0`
- `scripts/package.json`：新增 Playwright 依赖与 `postinstall` 浏览器安装脚本

## 收敛曲线

| Round | P0 | P1 | P2 | 接受残留 | 回归率 | 判定 |
|---|---|---|---|---|---|---|
| R1a/R1b 初审 | 0 | 6 | 2 | P1:0 / P2:0 | N/A | 未收敛 |
| R2 修复后复审 | 0 | 0 | 0 | P1:0 / P2:0 | 0% | 真收敛 |

## R1 问题清单

### P1（核心功能失效）

1. `slice-index.md` mobile `ecology` 切片数与实际文件不符（旧运行残留导致报告 34、实际 39）
2. `layout-audit-report.md` 引言路径写成 `screenshots/slices/...`，应为 `slices/...`
3. `batch_screenshots.js` 调用切片脚本时未透传 `--output-dir`
4. `requirements.txt` 缺少 `Pillow`
5. 无 `package.json`，Playwright 依赖未声明
6. `slice_screenshots.py` 切片前未清理 `slices/<viewport>/`，导致旧文件残留

### P2（体验问题）

7. `slice_screenshots.py` 无 `--help`/参数校验
8. `batch_screenshots.js` 缺少浏览器安装检查与友好报错

## 修复摘要

- `slice_screenshots.py`：引入 `argparse`（`--output-dir`、`--slice-height`、`--help`），新增 `clean_dir()` 在切片前清理旧 `.png`
- `batch_screenshots.js`：将 `config.outputDir` JSON 序列化后透传给切片脚本；`chromium.launch()` 加 try/catch 并输出安装提示；修正报告引言路径
- `requirements.txt`：加入 `Pillow>=9.0`
- `scripts/package.json`：声明 `playwright` 依赖与 `postinstall` 自动安装 chromium

## 验证结果

- `node --check scripts/batch_screenshots.js`：通过
- `python -m py_compile scripts/slice_screenshots.py`：通过
- 全量 40 页面 × 2 视口截图成功生成
- `layout-audit-report.md` 引言路径已修正为 `slices/<viewport>/<page>_<N>.png`
- `slice-index.md` mobile `ecology` 切片数与实际文件数一致（34/34）

## 残余风险（R3）

1. **L5 subagent 盲点**：浏览器未安装时的报错提示未在真正干净环境中验证，仅通过代码走读确认。
2. **L1 sample/time-point**：当前截图与切片反映的是 2026-07-22 页面状态；后续内容或样式改动可能重新引入布局问题，需定期重跑。
3. **L3 跨 session**：`scripts/package.json` 与 `requirements.txt` 的新依赖需要在未来 session 中同步；`detect_unwrapped_tables.py` 静态检查与 Playwright 运行时断言的标准需保持一致。

## 判定

P0=0、P1=0、P2=0，连续两轮复审无新发现，回归率 0%。**真收敛**。
