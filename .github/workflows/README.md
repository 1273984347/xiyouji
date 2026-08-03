# CI/CD 工作流说明

> **W234-E1 CI/CD 化** — 西游记解读项目（`d:\1\xiyouji`，v2.2.39 → v2.2.40 W234）的 GitHub Actions 工作流层。
> 三轨并行 CI（screenshots 回归 + lighthouse 性能 + a11y 审查）。部署（GitHub Pages）当前未配置（见交接文档「暂不做部署」）。

## 1. 工作流列表

| 工作流 | 文件 | 触发条件 | 用途 |
| --- | --- | --- | --- |
| CI | [`ci.yml`](ci.yml) | `pull_request` on `main` | PR 三轨并行门禁：截图回归 / Lighthouse 性能 / a11y 审查 |

> 当前仅配置 CI 三轨门禁；部署（GitHub Pages）暂未配置（与「暂不做部署」一致）。如需上线，再补 `deploy.yml` 并在本表补回 Deploy 行。

## 2. ci.yml 三轨说明

### Job 1 · `screenshots-regression`（截图回归测试）

- **运行环境**：`ubuntu-latest` + Node 20 + Python 3.12
- **依赖**：`npm install playwright @playwright/test` + `npx playwright install --with-deps chromium`
- **流程**：启动 `python -m http.server 8000 --directory site` → 运行 `node tools/screenshot-baseline.js`
- **降级**：`tools/screenshot-baseline.js` 不存在或失败时，自动 fallback 扫描 `site/data/*.html` 列表（`continue-on-error: true`，不阻断 a11y/lighthouse 两轨）
- **artifact**：`screenshots-${{ github.sha }}`（保留 14 天）；失败时额外上传 `screenshots-diff-${{ github.sha }}`（保留 30 天，含 diff 图）

### Job 2 · `lighthouse-performance`（性能审计）

- **运行环境**：`ubuntu-latest` + Node 20 + Python 3.12
- **流程**：启动 static server → 运行 `npx lighthouse http://localhost:8000/dashboard.html`
- **审计类别**：`performance,accessibility,best-practices,seo`
- **节流方式**：`--throttling-method=simulate`（模拟节流，CI 稳定可复现）
- **输出**：`lighthouse-report.report.json` + `lighthouse-report.report.html`
- **artifact**：`lighthouse-report`（保留 30 天）
- **阈值门禁**：
  - Performance ≥ **0.85**
  - Accessibility ≥ **0.95**
  - 任一不达标 → job 失败（`::error::` 注解在 PR Check 摘要中可见）

### Job 3 · `a11y-audit`（a11y 审查）

- **运行环境**：`ubuntu-latest` + Python 3.12
- **流程**：`python scripts/a11y_audit.py --dir site --quiet`
- **脚本来源**：W234-E2 创建/升级的 a11y 5 规则脚本（继承 W207 a11y 脚本 v2.2.17）
- **退出码语义**：`0` 无 P0/P1 / `1` 存在 P0/P1 / `2` 脚本错误
- **artifact**：`a11y-report`（含 `scripts/output/a11y-report.md` + `a11y-report.json`，保留 30 天）
- **失败条件**：**P0 > 0 时失败**（P1/P2 视为基线可接受残留）

## 3. 触发条件矩阵

| 事件 | 目标分支 | 触发工作流 | 三轨 | 部署 |
| --- | --- | --- | --- | --- |
| `pull_request` opened/synchronize/reopened | `main` | `ci.yml` | ✅ 全跑 | ❌（未配置） |
| `push` | `main` | （无） | ❌ | ❌（暂未部署） |
| `push` 到非 main 分支 | — | ❌ | ❌ | ❌ |
| 手动 `workflow_dispatch` | — | 未启用 | — | — |

> `concurrency` 策略：CI 同 PR 后续 push 取消前次（`cancel-in-progress: true`）。（部署未配置，暂无 CD 并发策略。）

## 4. artifact 列表

| artifact 名 | 来源 job | 内容 | 保留 |
| --- | --- | --- | --- |
| `screenshots-${{ github.sha }}` | screenshots-regression | 截图基线 + 扫描结果 | 14 天 |
| `screenshots-diff-${{ github.sha }}` | screenshots-regression（失败时） | diff 对比图 | 30 天 |
| `lighthouse-report` | lighthouse-performance | JSON + HTML 审计报告 | 30 天 |
| `a11y-report` | a11y-audit | a11y Markdown + JSON 报告 | 30 天 |
| `github-pages` | （部署未配置；启用 Pages 后由系统内置产生） | `./site` 静态产物 | Pages 托管 |

## 5. 阈值与失败条件

| 检查项 | 阈值 | 失败动作 |
| --- | --- | --- |
| Lighthouse Performance | ≥ 0.85 | ci.yml lighthouse-performance job 失败 |
| Lighthouse Accessibility | ≥ 0.95 | ci.yml lighthouse-performance job 失败 |
| a11y P0 计数 | = 0 | ci.yml a11y-audit job 失败（启用部署后亦作前置门禁） |
| a11y P1 计数 | 基线可接受 | 不阻断（持续治理） |
| a11y P2 计数 | 提示性 | 不阻断 |
| 截图回归 diff | 工具就绪时阻断 | 工具未就绪降级为 artifact 提示 |

## 6. 本地复现命令

```powershell
# a11y 审查（Windows 用 py，CI 用 python）
py scripts/a11y_audit.py --dir site --quiet

# Lighthouse 性能审计（需先启动 static server）
python -m http.server 8000 --directory site
npx lighthouse http://localhost:8000/dashboard.html `
  --output=json --output=html --output-path=lighthouse-report `
  --only-categories=performance,accessibility,best-practices,seo `
  --throttling-method=simulate

# 截图基线（工具就绪后）
node tools/screenshot-baseline.js
```

> Windows 本地用 `py`，CI（ubuntu）显式用 `python scripts/a11y_audit.py`。
> Lighthouse 本地建议加 `--chrome-flags="--headless --no-sandbox"`，浏览器路径自动探测。

## 7. 与既有测试体系的关系

| 体系 | 编号 | 关系 |
| --- | --- | --- |
| 测试体系 | **W204 E5** | CI 三轨是 W204 测试体系（pytest + JS syntax + lint_links 等）之上的**可视化质量门禁**补充层；原 `audit` job 的 JS/tables/SVG/links 检查仍可在本地 `scripts/run_all.py` 跑 |
| a11y 脚本 | **W207** | W234-E1 直接调用 W207 的 `scripts/a11y_audit.py`；CI 仅做触发与 artifact 上传，规则定义权在脚本侧 |
| a11y 5 规则 | **W234-E2** | W234-E2 升级脚本（5 规则 + P0/P1/P2 分级 + `--dir`/`--quiet` 参数），W234-E1 CI 是其首个自动化调用方 |
| CI/CD 化 | **W234-E1**（本工作流） | 提供 PR 门禁（部署暂未启用），闭合"开发-验证"循环 |

> E1（CI/CD 工作流）+ E2（a11y 5 规则脚本）= W234 E 方向工程化双产出。
> E1 是"壳"（触发与 artifact），E2 是"芯"（规则与判定）；二者解耦，规则升级无需改 workflow 文件。

## 8. 双索引

- [CHANGELOG.md](../../CHANGELOG.md) — v2.2.40 W234-E1
- [scripts/output/file-index.md](../../scripts/output/file-index.md) — W234-E1
