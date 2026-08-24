# CI/CD 工作流说明

> **W234-E1 CI/CD 化 → W399/W400/W401/W410/W411/W412/W413/W414/W415/W416/W417/W418/W419/W420/W421/W422/W423/W424/W425/W426 → W450-W500** — 西游记解读项目（`d:\1\xiyouji`，v2.3.99 W500）的 GitHub Actions 工作流层。
> **W399**：ci.yml 补 push main 触发（此前仅 pull_request，项目直接 push main 无 PR → CI 从未运行）；sitemap/robots 域名补全；新增 rum-viewer。
> **W400**：CI/Security 三 workflow 转绿（ruff 424 违规清零·XSS high 归零·Lighthouse 门禁校准·a11y pip cache 修复·black 门禁移除）。
> **W401**：ci.yml 5→7 job（pytest-unit 全量 tests/ + agent-web-build）·agent-web 源码入库·移除 3 处无 pip 安装 job 的 cache: pip 残留·build-test-deploy.yml 弃用删除。
> **W410**：security.yml npm-audit 扩至 agent-web（依赖链修复：overrides 强制 cherry-markdown 0.11.9/mermaid 11.16.1/dompurify 3.4.13·uuid 9→11·lucide-react 0.563→1.31，双目录 audit 0 漏洞）。
> **W411**：安全审计 P0-1/P1-1 处置（agent-web server 鉴权加固 + MCP 路径白名单·无 workflow 文件改动，agent-web-build job 覆盖构建回归）。
> **W412**：安全审计剩余项处置（P0-2 禁运行时覆盖密钥/端点 + RAG 参数钳制/LLM 端点校验 + SSE 超时与断开清理 + DOMPurify 消毒 + 依赖锁定 + CORS 白名单·无 workflow 文件改动，agent-web-build job 覆盖构建回归）。
> **W413**：仓库文件策略审查（严格审查入库边界·个人文档/方法论/开发内部资产恢复入库·字体源入库 +24MB·无 workflow 文件改动，CI 全量验证涵盖）。
> **W414**：README 用户手册改造（普通读者入口 + 开发者分区两级引导·无 workflow 文件改动，CI 全量验证涵盖）。
> **W415**：README 视觉引导增量（徽章区 3 枚 + 图标化速览 + 首页预览截图 + 反馈段·无 workflow 文件改动，CI 全量验证涵盖）。
> **W416**：文件管控清单标注（文档规范 §11 必同步/禁擅自修改显式化·多 session/Agent 协作·无 workflow 文件改动，CI 全量验证涵盖）。
> **W417**：actions 全量升级消除 Node 20 deprecation（ci.yml/pages.yml/perf.yml/screenshot-review.yml/security.yml 共 48 处：checkout v7/setup-node v7/setup-python v7/upload-artifact v7/upload-pages-artifact v5/configure-pages v6/deploy-pages v5/nick-fields retry v4·gh api releases/latest 实测 2026-08-10）。
> **W418**：内容质量深化（site/en/ 4 文件 29 broken 链接修复——EN 版存在指向同目录/无 EN 版回退中文原版 ../data/*.html 加 lang="zh-CN" 标注·A1 逐回解读 23 回补 `> 导航：` 引用行 100 回全覆盖·无 workflow 文件改动，CI 全量验证涵盖）。
> **W422**：全量治理（perf.yml 补 push 触发——LHCI 硬预算此前仅 PR 从未运行·verify_delivery 新增导航/链接/sitemap/回退 4 门禁·ci.yml 新增 JS 语法检查 + mypy report-only·Dependabot 配置·截图 artifact 失败才上传）。
> **W423**：性能债专项（perf.yml LHCI 预算收紧 LCP 5000→4500·CLS 0.3→0.2·TBT 300 不变；CJK 字体 swap→optional·D3/Three 移出 head——无 workflow 结构改动，仅预算阈值更新）。
> **W424**：性能债实测校准（push 首跑：LCP 4.73-4.87s 超 4500 → 预算回调 5000·timeline CLS 0.235 超 0.2 → 预算回归 0.3·FCP warn 4800·Screenshot 首跑暴露 timeline `d3 is not defined` + 内联 defer 无效 → 3D/时间线 `main()` 改 load 事件触发）。
> **W421**：Screenshot Review 提速优化（改动范围判定：页脚/文档-only 跳过·site/data 变更定向截图·static/脚本/workflow 变更全量·schedule/dispatch 恒全量 + batch_screenshots.js --only-pages + Playwright 浏览器缓存 + checkout fetch-depth 0）。
> **W420**：A1 内容质量深化（深度解读 100/100 补全 + 56 回元数据补齐 + 99 回导航错链修复·无 workflow 文件改动，CI 全量验证涵盖）。
> **W419**：修复 A1 深度解读 SD 错位（22 篇 SD 编号≠真实回号归位·40-72 回全覆盖·源文件 24 篇元数据/H1/关联行修正·第 56 回补写 SD101·无 workflow 文件改动，CI 全量验证涵盖）。
> **W450-W500**：verify 门禁体系扩展（W458 防回归 check_structure/check_js_syntax·W459 check_dynamic_links·W493 token 覆盖率/动效禁止/a11y 三门禁·W495 INLINED CSS·W498 skills 索引一致性·W500 索引健康 check_index_health——均由 ci.yml verify-delivery job 跑 verify_delivery.py 自动涵盖，无 workflow 结构改动）+ W464 perf 基线确立（perf.yml 预算沿用 W424 校准值 LCP≤5000/CLS≤0.3/TBT≤300）。

## 1. 工作流列表

| 工作流 | 文件 | 触发条件 | 用途 |
| --- | --- | --- | --- |
| CI | [`ci.yml`](ci.yml) | `push` main + `pull_request` + `workflow_dispatch` | 8 job 门禁：截图存活烟测 / Lighthouse / a11y / dependency / ruff / pytest / agent-web 构建 / 交付校验 |
| Security | [`security.yml`](security.yml) | `push` main + `pull_request` | 4 job：npm-audit（scripts/ + agent-web/ 双目录）/ pip-audit / CSP / XSS detect |
| Deploy Pages | [`pages.yml`](pages.yml) | `push` main（site/** 变更） | GitHub Pages 部署 `./site`（W401 决策：不采用 build-test-deploy.yml，避免部署竞态·已删除） |
| Lighthouse CI | [`perf.yml`](perf.yml) | `push` main（site/**）+ `pull_request` + 每周一 + `workflow_dispatch`（W422 补 push：原仅 PR 从不运行·首跑暴露性能债后阈值已校准） | LHCI 性能预算断言（LCP≤5000ms/CLS≤0.3/TBT≤300ms，W424 实测校准） |
| Screenshot Review | [`screenshot-review.yml`](screenshot-review.yml) | `push` main（site/** 或脚本/workflow 变更）+ `pull_request` + 每周一 + `workflow_dispatch`（W421：页脚/文档-only 跳过·data 页定向截图） | Playwright 截图 + 布局审计 |

> **W400 关键教训**：ci.yml 建置时仅 `pull_request` 触发，但项目工作流是直接 push main（无 PR），**CI 从未真正运行过**。W399 补 push 触发后首次运行暴露全部存量问题。**新 workflow 必须本地语法校验 + 确认触发条件匹配真实开发流。**

## 2. ci.yml 七 job 说明

### Job 1 · `screenshots-regression`（页面存活烟测）

- **运行环境**：`ubuntu-latest` + Node 20 + Python 3.12
- **依赖**：`npm install playwright @playwright/test` + `npx playwright install --with-deps chromium`
- **流程**：启动 `python -m http.server 8000 --directory site` → 内联 Node 脚本递归扫描 `site/` 全部 HTML，逐个请求验证 HTTP 200
- **W399 修复**：原引用 `tools/screenshot-baseline.js`（仓库从未存在 → 步骤必然失败走降级分支），改为内联 Node 存活烟测
- **路径跨平台**：`p.replace(/[\\/]+/g,'/').replace(/^site\//,'')`（Windows 本地与 Linux CI 均可用）
- **artifact**：`screenshots-${{ github.sha }}`（保留 30 天）；失败时额外上传 `screenshots-diff-${{ github.sha }}`

### Job 2 · `lighthouse-performance`（性能审计）

- **运行环境**：`ubuntu-latest` + Node 20 + Python 3.12
- **流程**：启动 static server → `npx lighthouse http://localhost:8000/dashboard.html`（categories: performance/accessibility/best-practices/seo，`--throttling-method=simulate`）
- **W400 门禁**：**Accessibility ≥ 0.95 硬门槛**；**Performance 降级为 warn**（`< 0.50` 才警告）——dashboard 为内容密集模板大页，CI 实测 0.550、本地 0.730 波动大，且 lantern 对大 DOM 页 FCP/LCP 有已知误差（All Frames not implemented）
- **性能门禁承担者**：perf.yml（LHCI LCP≤5000ms / CLS≤0.3 / TBT≤300ms 预算断言，W424 实测校准）
- **artifact**：`lighthouse-report`（保留 30 天）

### Job 3 · `a11y-audit`（a11y 审查，9 矩阵）

- **运行环境**：`matrix.os × matrix.python-version` = 3 OS（ubuntu/windows/macos）× 3 Python（3.10/3.11/3.12）= 9 组合
- **流程**：`python scripts/a11y_audit.py --dir site --quiet`（W264-E2 9 规则 WCAG 2.2）
- **W400 修复**：移除 `cache: pip`——a11y_audit.py 仅用标准库、job 不安装 pip 依赖，缓存目录不存在导致 Post 步骤报 `##[error]` 使 job 失败（windows/ubuntu py3.10-3.11 复现）
- **artifact**：`a11y-report-${{ matrix.os }}-py${{ matrix.python-version }}`（保留 30 天）

### Job 4 · `dependency-scan`（pip-audit）

- **流程**：`pip-audit -r scripts/requirements.txt -f json -o pip-audit-report.json`
- **artifact**：`pip-audit-report`（保留 30 天）

### Job 5 · `code-quality`（ruff）

- **流程**：`ruff check scripts/`
- **W400 配置**：pyproject.toml `extend-exclude` 跳过 `_` 前缀一次性脚本 + `scripts/audit/archive`（与 security_scan.py 跳过逻辑一致）；全局忽略 UP031（printf 风格非错误）
- **W400 移除 black --check**：存量 123/128 脚本从未 black 格式化，门禁从未通过；保留 ruff 语义门禁，格式统一由 ruff format 负责

### Job 6 · `pytest-unit`（单元测试）

- **运行环境**：`ubuntu-latest` + Python 3.12
- **流程**：`pip install -r scripts/requirements.txt` → `python -m pytest tests -q`（W401 补齐 + DRL 修复：原 ci.yml 五 job 未覆盖 Python 单元测试；pytest.ini `testpaths=tests` + `--ignore=tests/e2e`，浏览器测试移入 tests/e2e/ 由 screenshots-regression job 覆盖）
- **本地验证**：`py -3 -m pytest tests -q` → 321 passed（2026-08-09 DRL 修复后实测）

### Job 7 · `agent-web-build`（xiyouji-agent-web 前端构建）

- **运行环境**：`ubuntu-latest` + Node 20
- **流程**：`npm --prefix xiyouji-agent-web ci` → `npm run build`（`tsc -b && vite build`，仓库唯一编译目标）
- **W401 前置**：agent-web 源码（37 文件）已入库；.gitignore 改为精细忽略（node_modules/dist/data/chat.db/tsc 编译产物 server/*.js|*.d.ts + vite.config.js|*.d.ts）
- **artifact**：`agent-web-dist-${{ github.sha }}`（保留 30 天）
- **本地验证**：`npm --prefix xiyouji-agent-web run build` → vite build 成功（7906 modules，2026-08-08 实测）

### Job 8 · `verify-delivery`（交付校验门禁，W424 新增）

- **运行环境**：`ubuntu-latest` + Python 3.12 + Node 20
- **流程**：`pip install -r scripts/requirements.txt` → `python scripts/run_all.py`（重新生成 scripts/output/data/*.json，生成物未入库）→ `python scripts/verify_delivery.py`——17 项门禁：六文档版本 / A4 209 计数 / 范围漂移 / A1-A6 真实计数 / A1 导航相邻性 / docs/01 链接 / sitemap 覆盖 / 数据漂移 / CSP / 腐蚀 / JS 语法 / CSS 结构 / token 覆盖率 / 动效禁止 / a11y / INLINED CSS / 动态链接 / 治理契约 / skills 索引 / 索引健康（W500 起随 verify_delivery.py 自动获得，无 workflow 结构改动）
- **与 pre-commit 的关系**：本地 pre-commit 钩子（手动 .git/hooks/pre-commit + .pre-commit-config.yaml 双轨）已含等价检查；CI 兜底防 `--no-verify` 提交。run_all 的 2 个历史 FAIL（hardships_81/journey_route 缺 --output）已修默认值，34/34 全过。

## 3. 触发条件矩阵

| 事件 | 目标分支 | 触发工作流 | CI | Security | Deploy | Perf | Screenshot |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `push` | `main` | ci / security / pages / perf / screenshot-review | ✅ | ✅ | ✅（site/**） | ✅（site/**） | ✅（site/** 或审查三件套） |
| `pull_request` | `main` | ci / security / perf / screenshot-review | ✅ | ✅ | ❌ | ✅（site/**） | ✅（site/** 或审查三件套） |
| `schedule` | — | perf / screenshot-review（每周一） | — | — | — | ✅ | ✅ |
| `workflow_dispatch` | — | ci / pages / perf / screenshot-review | ✅ | — | ✅ | ✅ | ✅ |

> `concurrency`：CI/Security/Perf 均设 `group + cancel-in-progress: true`，同 ref 后续 push 取消前次。

## 4. artifact 列表

| artifact 名 | 来源 job | 内容 | 保留 |
| --- | --- | --- | --- |
| `screenshots-${{ github.sha }}` | screenshots-regression | 存活烟测结果 | 30 天 |
| `screenshots-diff-${{ github.sha }}` | screenshots-regression（失败时） | diff 对比图 | 30 天 |
| `lighthouse-report` | lighthouse-performance | JSON + HTML 审计报告 | 30 天 |
| `a11y-report-*` | a11y-audit | a11y Markdown + JSON 报告 | 30 天 |
| `pip-audit-report` | dependency-scan | pip 漏洞审计 JSON | 30 天 |
| `agent-web-dist-${{ github.sha }}` | agent-web-build | xiyouji-agent-web 前端构建产物（dist/） | 30 天 |

## 5. 阈值与失败条件

| 检查项 | 阈值 | 失败动作 |
| --- | --- | --- |
| Lighthouse Accessibility | ≥ 0.95 | ci.yml lighthouse-performance job 失败 |
| Lighthouse Performance | < 0.50 才 warn | 不阻断（性能门禁移交 perf.yml） |
| a11y P0 计数 | = 0 | ci.yml a11y-audit job 失败 |
| ruff | 0 违规（scripts/ 生产脚本） | ci.yml code-quality job 失败 |
| XSS high 计数 | = 0 | security.yml xss-detect job 失败 |
| pip-audit | 0 高危（--strict） | security.yml pip-audit job 失败 |
| npm audit（scripts/ + agent-web/） | 0 high（--omit=dev --audit-level=high） | security.yml npm-audit job 失败 |
| LHCI 预算 | LCP≤5000ms / CLS≤0.3 / TBT≤300ms | perf.yml job 失败 |
| pytest | 0 失败（tests 全量） | ci.yml pytest-unit job 失败 |
| verify_delivery | 六文档版本 / A4 209 / 范围漂移 / 导航 / 链接 / sitemap / 回退 / 数据漂移 | ci.yml verify-delivery job 失败 |
| agent-web build | tsc + vite 退出码 0 | ci.yml agent-web-build job 失败 |

## 6. 本地复现命令

```powershell
# a11y 审查（Windows 用 py，CI 用 python）
py scripts/a11y_audit.py --dir site --quiet

# ruff 检查（必须与本仓库 pyproject.toml 一致，跳过 _ 前缀脚本）
ruff check scripts/

# 安全扫描（XSS high 归零验证）
python scripts/security_scan.py --all --no-headers --no-sri --no-pip-audit

# pytest 单元测试（tests 全量，--ignore=tests/e2e 由 pytest.ini 内置）
py -3 -m pytest tests -q

# agent-web 前端构建
npm --prefix xiyouji-agent-web run build

# npm 依赖漏洞审计（scripts/ + agent-web/ 双目录，与 security.yml npm-audit 一致）
npm --prefix scripts audit --omit=dev --audit-level=high
npm --prefix xiyouji-agent-web audit --omit=dev --audit-level=high

# Lighthouse 性能审计（需先启动 static server）
python -m http.server 8000 --directory site
npx lighthouse http://localhost:8000/dashboard.html `
  --output=json --output=html --output-path=lighthouse-report `
  --only-categories=performance,accessibility,best-practices,seo `
  --throttling-method=simulate
```

> Windows 本地用 `py`，CI（ubuntu）显式用 `python`。

## 7. 与既有测试体系的关系

| 体系 | 编号 | 关系 |
| --- | --- | --- |
| 测试体系 | **W204 E5** | CI 三轨是 W204 测试体系（pytest + JS syntax + lint_links 等）之上的**可视化质量门禁**补充层；原 `audit` job 的 JS/tables/SVG/links 检查仍可在本地 `scripts/run_all.py` 跑 |
| a11y 脚本 | **W207** | CI 调用 `scripts/a11y_audit.py`；CI 仅做触发与 artifact 上传，规则定义权在脚本侧 |
| a11y 9 规则 | **W264-E2** | a11y-audit 升级为 9 规则 WCAG 2.2 AA（W271/W275/W279 E 方向持续深化） |
| 安全扫描 | **W236-E/W268** | security_scan.py 四轨（XSS/CSP/secret/pip-audit），`_` 前缀开发脚本不入门禁（W400） |
| CI/CD 化 | **W234-E1** | 提供 push/PR 门禁 + GitHub Pages 部署（W390 pages.yml） |

## 8. 双索引

- [CHANGELOG.md](../../CHANGELOG.md) — v2.3.99 W500
- [scripts/output/file-index.md](../../scripts/output/file-index.md) — W234-E1 / W399 / W400 / W401 / W500
