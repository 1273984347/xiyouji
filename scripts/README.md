# scripts/ 工具脚本说明

> 本目录承载《西游记》文本分析脚本与可视化站点工程化工具。
> 数据分析脚本按 A-AH 34 类分目录组织，详见 [STRUCTURE.md](../STRUCTURE.md)。
> 根级工具脚本（截图审查 / 静态检查 / 批量修复）登记在本文件。
> **历史一次性脚本已归档至 [`archive/`](archive/)（45 个，W446 治理），保留 git 历史备查，不再参与日常工作流。**

## 根级工具脚本

### Python 工具

| 脚本 | 用途 | 典型调用 |
|:---|:---|:---|
| `check_js_syntax.py` | 检查 HTML 内联 JS 语法（单文件 + 批量两种模式） | `python check_js_syntax.py site/data/cave-estate.html` / `python check_js_syntax.py --all` |
| `detect_unwrapped_tables.py` | 静态扫描无横向滚动容器的 `<table>`（表格溢出双轨检查之一） | `python detect_unwrapped_tables.py` |
| `extract_strings.py` | 穷举 viz 页 chrome 文本节点 + script CJK 字面量（英文站翻译前置枚举·W446 转正去下划线） | `python scripts/extract_strings.py <name>` |
| `validate_en.py` | 校验 EN 页 chrome CJK 白名单 + script CJK=0（英文站翻译门禁·W446 转正去下划线） | `python scripts/validate_en.py <path>` |
| `slice_screenshots.py` | 将全页截图按固定高度切片（Pillow，默认 800px） | `python slice_screenshots.py --output-dir output/screenshots` |
| `embed_json.py` | 统一 JSON 数据嵌入 HTML（EMBEDDED_DATA fallback 模式） | `python embed_json.py site/data/foo.html output/data/foo.json` |
| `lint_links.py` | 链接校验（HTML href/src + Markdown [text] (url) 形式）+ 自动修复 | `python lint_links.py --all` / `python lint_links.py --fix` |
| `sync_docs.py` | 6 文件文档一致性校验（版本号/统计计数/W### 编号/file-index）+ `--fix` 自动修复版本号与统计 | `python sync_docs.py` / `python sync_docs.py --fix` |
| `run_all.py` | 批量运行 A-AH 34 类分析脚本，汇总 PASS/FAIL 报告 | `python scripts/run_all.py` / `python scripts/run_all.py --only A,B,F` |
| `new_page.py` | 基于 `_template.html` 的可视化页面脚手架，自动替换占位符并更新 index.html 导航 | `python scripts/new_page.py --name foo --title "Foo" --category "Z_图表设计" --desc "..."` |
| `release.py` | 版本发布前体检：sync_docs + git 状态 + pytest + 发布 checklist | `python scripts/release.py --target v2.2.16` |
| `drl_spotcheck.py` | DRL 真循环 spot-check 工具（E1 铁律落地·验证修复落地/未改动声明） | `python scripts/drl_spotcheck.py --file README.md --old "v2.2.14" --new "v2.2.15"` |
| `spot_check_nlp.py` | NLP 分析结果抽样校验（人物识别/共现等） | `python spot_check_nlp.py` |
| `verify_chapters.py` | 章节文本完整性校验（回数/字数/标题格式） | `python verify_chapters.py` |
| `data_validate.py` | output/data/ JSON 结构完整性校验（语法/非空/类型契约） | `python data_validate.py --quiet` |
| `docs_index.py` | docs/ 文档索引自动生成（321 篇，支持 CI --check 模式） | `python docs_index.py` / `python docs_index.py --check` |

### Node.js 工具

| 脚本 | 用途 | 典型调用 |
|:---|:---|:---|
| `batch_screenshots.js` | Playwright 批量全页截图 + 布局断言 + 自动切片 | `npm run screenshots` |
| `debug_page.js` | 调试单个页面（console / pageerror / both 三种模式） | `node debug_page.js --url cave-estate.html --mode both` |

## 共享模块

| 模块 | 用途 |
|:---|:---|
| `utils/text_loader.py` | 文本加载与编码处理（多编码尝试 + 分回目录加载） |
| `utils/aliases.py` | 人物别名表单一数据源（35 人物 + resolve_alias 反查），被 B_人物/ 三脚本共享 |
| `utils/analyzer_base.py` | 分析脚本通用入口 `run_analyzer`（argparse / 加载文本 / 写 JSON / 进度日志），消除 34 类脚本样板 |

> **新脚本接入约定**：A-AH 34 类分析脚本应使用 `run_analyzer` 入口，仅需实现 `analyze(chapters, args) -> dict` 函数，无需重复 argparse/load/json 样板。参照 `A_文本基础/chapter_stats.py` 与 `B_人物/character_appearance.py` 模式。

## 测试与 CI

| 路径 | 用途 |
|:---|:---|
| `../tests/` | pytest 测试套件（aliases / text_loader / character_nlp） |
| `../.github/workflows/ci.yml` | GitHub Actions CI（lint + test + audit） |
| `../pyproject.toml` | ruff lint 配置 |
| `../Makefile` | 统一编排入口（`make help` 查看全部目标） |

## 依赖

- Python：见 `requirements.txt`（`jieba` + `Pillow`）
- Node.js：见 `package.json`（`playwright`，`npm install` 自动下载 chromium）

## 工程规范约定

所有根级脚本遵循以下约定（与 A-AH 34 类目录脚本一致）：

1. 入口包装为 `def main():` 无参签名（或直接调用 `run_analyzer`）
2. 文件末尾 `if __name__ == "__main__": main()` / `run_analyzer(...)`
3. 顶部 docstring 描述用途 + 使用方式
4. CLI 参数用 `argparse`，支持 `--help`
5. `--output` 默认指向 `output/data/` 目录（数据脚本）或 `output/screenshots/` 目录（截图脚本）
