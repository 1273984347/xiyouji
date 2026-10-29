# scripts/ 工具脚本说明

> 本目录承载《西游记》文本分析脚本与可视化站点工程化工具。
> 数据分析脚本按 A-AH 34 类分目录组织，详见 [STRUCTURE.md](../STRUCTURE.md)。
> 根级工具脚本（截图审查 / 静态检查 / 批量修复）登记在本文件。
> **历史一次性脚本已归档至 [`archive/scripts/`](../archive/scripts/)（历次治理：W446 · W735 · W977 批量退役；逐组台账见 [archive/README.md](../archive/README.md)），保留 git 历史备查，不再参与日常工作流。**
> **调用形态**：下表 `python <脚本>` 是**可移植形态**（CI 跑 `ubuntu-latest`·Linux/macOS 通用）；**本机 PowerShell 侧** `python`/`python3` 是应用执行存根（命令存在但调用即静默失败）→ 该侧请写 `py -3 <脚本>`（三语境口径见 [AGENTS.md](../AGENTS.md) §4.3）。
> **全量清单**：顶层跟踪态工具逐件清单（含 docstring 摘要·分类分节）由机器生成于 [output/tools-inventory.md](output/tools-inventory.md)——**禁手改**，随 `gen_folder_docs.py --refresh` 刷新链更新；本文件只留场景路由与高频工具精选。

## 场景速查（要做什么 → 用哪个）

| 场景 | 工具 | 典型调用 / 备注 |
|:---|:---|:---|
| 批次开工前核验（取号 / touches 交集 / 体积窗） | `preflight_check.py` | `python scripts/preflight_check.py --touches "<共享面清单>" --self W###` |
| 台账认领 / 收官回填 | `ledger_backfill.py` | `--append-claim --w N --desc … --session …` / `--w N --from-git`（git 反填 hash） |
| 收官级联（版本面十面统一落盘） | `batch_cascade.py` | `--spec output/_wNNN_spec.json --apply`（spec 由各批 tmpe 构建器生成；**禁手写版本面**——C7 契约门禁会拦） |
| 收官自检（段状态 vs git 事实） | `ledger_close_check.py` | 现役段 0 未收官 = 收官干净 |
| CHANGELOG / file-index 超窗回窗 | `archive_segments.py --apply` | 判据=体积窗 C1/C2（110 段）；级联收官 [SIZE] 提示位会点名 |
| 台账对账表超窗修剪 | `archive_ledger_rows.py --apply` | 判据=C3（60 行）；号序切分·守恒五道 |
| **归档件超 1MB 二级归档** | `archive_tier2.py --file changelog\|file-index --apply` | 判据=§11.2 1MB 线（check_archive_health T1·W994 实测双破线首跑回线）；守恒五道 |
| 归档区健康体检（体积/台账对账/冷存储警告） | `check_archive_health.py` | 报告型（`--strict` 门禁候选）；级联收官 [ARCHIVE] 提示位 |
| 单件/小批退役归档 | `archive_file.py` | `--dry-run` 先行；**大批量**按 archive/README「手动组行」条款（W977 先例：语料级引用剔除→批量 git mv→组行） |
| tmpe 临时区盘点 / 清理 / 沉淀扫描 | `tmpe_tidy.py` | 默认盘点 / `--plan --older N` / `--tool-candidates`；删除须主人确认+回收站 |
| 统计口径刷新（含标记自动跟随） | `stats.py --w <批号>` | C5b 对账面 `<!--stats:KEY-->` 标记由 sweep 自动刷——**禁手工刷标记** |
| 复盘触发查询 | `check_review_trigger.py` | 三判据三选一（天数/批次数/提交数·阈值见脚本 THRESHOLDS）；preflight 提示位常驻 |
| 读者数据取数 / 分发判定 | `fetch_gate_stats.py` / `judge_gate.py` | W626 闸门（30 日 UV 判定·判定记录落 11-方案报告/调研与数据复盘） |
| 治理文档体积窗与版本面契约总览 | `check_doc_size_budget.py` | C1-C7（C7=版本面契约·verify+开工双面把守）；`--report` 只报不判 |
| 目录文档 / 工具清单 / docs 索引刷新 | `gen_folder_docs.py --refresh` | 刷新链连带 tools-inventory（W985）；docs 索引另跑 `docs_index.py` |
| 改内联脚本 / 页脚后 | `generate_csp.py` + `_gen_search_index.py` | CSP 哈希失配会整脚本被拒；索引陈旧第 46 门禁拦 |
| 全量门禁 / 测试 / lint | `verify_delivery.py` / `pytest` / `ruff` | 50 槽（pre-commit 自动跑）；本机侧 `py -3 -m pytest` |

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
<!-- W1020：sync_docs.py 已于 W793 退休（职责由第 31 门禁 check_doc_sync 承接），原行删除 -->
| `run_all.py` | 批量运行 A-AH 34 类分析脚本，汇总 PASS/FAIL 报告 | `python scripts/run_all.py` / `python scripts/run_all.py --only A,B,F` |
| `new_page.py` | 基于 `_template.html` 的可视化页面脚手架，自动替换占位符并更新 index.html 导航 | `python scripts/new_page.py --name foo --title "Foo" --category "Z_图表设计" --desc "..."` |
| `release.py` | 版本发布前体检：sync_docs + git 状态 + pytest + 发布 checklist | `python scripts/release.py --target v2.2.16` |
| `drl_spotcheck.py` | DRL 真循环 spot-check 工具（E1 铁律落地·验证修复落地/未改动声明） | `python scripts/drl_spotcheck.py --file README.md --old "v2.2.14" --new "v2.2.15"` |
| `spot_check_nlp.py` | NLP 分析结果抽样校验（人物识别/共现等） | `python spot_check_nlp.py` |
| `verify_chapters.py` | 章节文本完整性校验（回数/字数/标题格式） | `python verify_chapters.py` |
| `data_validate.py` | output/data/ JSON 结构完整性校验（语法/非空/类型契约） | `python data_validate.py --quiet` |
| `docs_index.py` | docs/ 文档索引自动生成（篇数以生成头为准，支持 CI --check 模式） | `python docs_index.py` / `python docs_index.py --check` |
| `archive_file.py` | 文件归档工具（git mv 归位 + 活引用扫描提示 + archive/README.md 台账登记；前置校验 + --dry-run） | `python scripts/archive_file.py <path> --batch W736 --dry-run` |
| `preflight_check.py` | 批次开工前置核验（fetch/远端顶部/对账表取号/touches 在途盘点与交集拒绝/工作树/环境六检；fetch 故障降级 GitHub API 通道） | `python scripts/preflight_check.py [--touches "<逗号分隔的共享文件清单>"] [--self W###]` |
| `release_prep.py` | 批次发布预检（spec 三检 + 消息 W### 形态登记核验 + --init spec 模板生成） | `python scripts/release_prep.py --check-spec output/_w736_spec.json` / `--init W736` |

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
| `utils/path_guard.py` | W536 路径守卫公共模块（W761 建）：`make_guard(root)` 生成 open() 的 root 受限版 + PROJECT_ROOT/SCRIPTS_ROOT 双根常量，收敛 14 处重复内联定义 |

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
