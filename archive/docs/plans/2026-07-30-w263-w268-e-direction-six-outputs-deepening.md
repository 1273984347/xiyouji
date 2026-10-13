# E 方向 6 产出深化实施计划（v2.2.47·W263-W268）

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 深化 E1/E2/E3/E5/E6/E8 六子方向，每个子方向升级一层，dispatching-parallel-agents 三 subagent 并行执行 6 产出（14 文件）。

**Architecture:** 三 subagent 独立无共享状态·主代理统一 spot-check。Subagent A（W263-W264 E1+E2）·Subagent B（W265-W266 E3+E5）·Subagent C（W267-W268 E6+E8）。完成后主代理统一同步项目层 6 文档 + memory 层三件套。

**Tech Stack:** Python 3.10+ / GitHub Actions / pytest / Lighthouse CI / pip-audit / WCAG 2.2 / CSP / SRI / RUM

---

## Task 1: Subagent A 创建 W263-W264（E1 CI/CD 深化 + E2 a11y 深化）

**Files:**
- Modify: `.github/workflows/ci.yml`
- Modify: `scripts/a11y_audit.py`

**Subagent A 任务描述：**

创建 Subagent A（subagent_type=general_purpose_task），执行以下任务：

### W263 E1 CI/CD 深化

修改 `.github/workflows/ci.yml`，升级内容：

1. **matrix 测试**：Python 3.10/3.11/3.12 × ubuntu-latest/windows-latest/macos-latest（9 矩阵）
2. **pip 缓存**：`cache: pip` + `cache-dependency-path: scripts/requirements.txt`
3. **artifact 保留 30 天**：`retention-days: 30`
4. **失败重试 3 次**：`max-attempts: 3`
5. **并发取消旧 run**：`concurrency: { group: ci-${{ github.ref }}, cancel-in-progress: true }`
6. **新增 job：dependency-scan**：`pip-audit` 依赖扫描
7. **新增 job：code-quality**：`ruff check` + `black --check`

### W264 E2 a11y 深化

修改 `scripts/a11y_audit.py`，升级内容（WCAG 2.1 → 2.2）：

1. **规则 6：焦点可见（Focus Visible）**：验证 HTML/CSS 中 `:focus-visible` 样式存在
2. **规则 7：目标尺寸（Target Size）**：验证按钮/链接最小 24×24px（WCAG 2.2 SC 2.5.8）
3. **规则 8：拖拽移动（Dragging Movements）**：验证可拖拽元素有替代方案（WCAG 2.2 SC 2.5.7）
4. **规则 9：一致帮助（Consistent Help）**：验证帮助机制位置一致（WCAG 2.2 SC 3.2.6）
5. **键盘导航审计**：Tab 顺序 + 焦点陷阱检测
6. **屏幕阅读器 ARIA 标签验证**：`aria-label`/`aria-labelledby`/`aria-describedby` 完整性

**验收标准：**
- ci.yml 包含 9 矩阵 + 2 新 job（dependency-scan + code-quality）
- a11y_audit.py 包含 9 规则（原 5 + 新 4）
- 无 placeholder/TBD/TODO

---

## Task 2: Subagent B 创建 W265-W266（E3 性能深化 + E5 测试深化）

**Files:**
- Create: `scripts/perf_optimize.py`
- Create: `.github/workflows/perf.yml`
- Create: `tests/unit/test_perf_optimize.py`
- Create: `tests/unit/test_security_scan.py`
- Create: `tests/unit/test_a11y_audit.py`
- Modify: `tests/e2e/`（新增 8 用例）

**Subagent B 任务描述：**

创建 Subagent B（subagent_type=general_purpose_task），执行以下任务：

### W265 E3 性能深化

新建 `scripts/perf_optimize.py`，内容：

1. **LCP 优化**：图片懒加载 `loading="lazy"` 自动添加 + 资源预加载 `<link rel="preload">` 生成 + 字体子集化实施（调用 font-subset-guide.md 方案）
2. **Canvas 渲染深化**：D3.js SVG → Canvas 转换脚本（大数据集 ≥1000 节点时自动切换）
3. **关键 CSS 内联**：提取首屏 CSS + 内联到 `<style>`
4. **JS 延迟加载**：`defer`/`async` 属性自动添加 + 动态 import()
5. **资源压缩**：HTML/CSS/JS minify + gzip 预压缩
6. **输出**：`scripts/output/perf-optimization-report.md`

### W266 E5 测试深化

1. **新建 `tests/unit/test_perf_optimize.py`**：测试 perf_optimize.py 各函数（test_lcp_optimize + test_canvas_render + test_critical_css + test_js_defer + test_minify）
2. **新建 `tests/unit/test_security_scan.py`**：测试 security_scan.py 各函数（test_headers_scan + test_sri_scan + test_dependency_scan）
3. **新建 `tests/unit/test_a11y_audit.py`**：测试 a11y_audit.py 9 规则（test_rule_1-9 + test_keyboard_nav + test_aria）
4. **新建 `.github/workflows/perf.yml`**：Lighthouse CI + 性能预算断言（LCP < 2.5s / CLS < 0.1 / TBT < 300ms）
5. **tests/e2e/ 新增 8 用例**：跨页面导航 + 暗色模式 + 全局筛选器 + dashboard KPI + 搜索浮层 + 英文站 + 3D 网络 + 交互式地图

**验收标准：**
- perf_optimize.py 包含 6 模块（LCP/Canvas/CSS/JS/Minify/Report）
- 3 测试文件通过 `pytest tests/unit/ -v`
- perf.yml 包含 Lighthouse CI + 性能预算
- 无 placeholder/TBD/TODO

---

## Task 3: Subagent C 创建 W267-W268（E6 监控深化 + E8 安全深化）

**Files:**
- Modify: `scripts/perf_monitor.py`
- Modify: `scripts/security_scan.py`
- Create: `site/_headers`
- Create: `site/js/rum.js`
- Create: `.env.example`
- Create: `scripts/output/perf-budget.json`
- Create: `scripts/output/perf-baseline.json`

**Subagent C 任务描述：**

创建 Subagent C（subagent_type=general_purpose_task），执行以下任务：

### W267 E6 监控深化

1. **修改 `scripts/perf_monitor.py`**：新增 RUM 真实用户监控采集 + Core Web Vitals alerting 阈值（LCP > 2.5s / CLS > 0.1 / INP > 200ms 触发 alert）+ 历史趋势对比
2. **新建 `site/js/rum.js`**：浏览器端 RUM 采集（LCP/CLS/INP/TBT/FCP + 发送至 /api/rum）
3. **新建 `scripts/output/perf-budget.json`**：性能预算（HTML < 50KB / CSS < 100KB / JS < 200KB / 图片 < 500KB）
4. **新建 `scripts/output/perf-baseline.json`**：当前各页面 Core Web Vitals 快照

### W268 E8 安全深化

1. **修改 `scripts/security_scan.py`**：新增 `_headers` 文件验证 + SRI 验证 + pip-audit 集成
2. **新建 `site/_headers`**：CSP 内容安全策略 + X-Frame-Options + X-Content-Type-Options + Referrer-Policy + Permissions-Policy
3. **新建 `.env.example`**：脱敏模板（API_KEY=your_api_key_here + DB_PASSWORD=your_password_here）

**验收标准：**
- perf_monitor.py 包含 RUM + alerting + 趋势对比
- rum.js 包含 5 指标采集
- perf-budget.json + perf-baseline.json 结构完整
- security_scan.py 包含 _headers + SRI 验证
- site/_headers 包含 5 安全头
- .env.example 包含脱敏模板
- 无 placeholder/TBD/TODO

---

## Task 4: 主代理 DRL R1b spot-check

**对 6 产出执行主代理 spot-check：**

1. Grep 验证 6 产出文件存在性
2. Grep 验证 ci.yml 9 矩阵 + 2 新 job（dependency-scan + code-quality）
3. Grep 验证 a11y_audit.py 9 规则（原 5 + 新 4）
4. Grep 验证 perf_optimize.py 6 模块
5. Grep 验证 3 测试文件存在
6. Grep 验证 perf.yml Lighthouse CI
7. Grep 验证 perf_monitor.py RUM + alerting
8. Grep 验证 rum.js 5 指标采集
9. Grep 验证 perf-budget.json + perf-baseline.json
10. Grep 验证 security_scan.py _headers + SRI 验证
11. Grep 验证 site/_headers 5 安全头
12. Grep 验证 .env.example 脱敏模板
13. Grep 验证无 placeholder/TBD/TODO（排除描述性文字 false positive）

**收敛判据：P0=0/P1=0/P2=0/P3=0**

---

## Task 5: 主代理同步项目层 6 文档

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `README.md`
- Modify: `STRUCTURE.md`
- Modify: `docs/00-导读/项目说明.md`
- Modify: `交接文档.md`
- Modify: `scripts/output/file-index.md`

### Step 1: CHANGELOG.md

新增 v2.2.47 W263-W268 版本段：

```markdown
### v2.2.47 — 进行中（2026-07-30）：W263-W268 E 方向六产出深化（E1 CI/CD matrix+pip-audit+ruff + E2 a11y WCAG 2.2 四新规则 + E3 perf_optimize.py LCP+Canvas+CSS+JS+Minify + E5 测试覆盖率 80%+Lighthouse CI+8 E2E 用例 + E6 RUM+alerting+perf-budget + E8 CSP+SRI+pip-audit+_headers·dispatching-parallel-agents 三 subagent 并行·6 产出 = 14 文件）

> **W263-W268 E 方向六产出深化**
> - **来源**：用户选择 E 方向 6 产出深化·E1+E2+E3+E5+E6+E8 六子方向·方法 B 三 subagent 并行
> - **文件**：6 产出 = 14 文件
>   - .github/workflows/ci.yml（W263·E1 CI/CD 深化·matrix 9 + pip-audit + ruff）
>   - scripts/a11y_audit.py（W264·E2 a11y 深化·WCAG 2.1→2.2·5→9 规则）
>   - scripts/perf_optimize.py（W265·E3 性能深化·6 模块 LCP/Canvas/CSS/JS/Minify/Report）
>   - tests/unit/test_perf_optimize.py + test_security_scan.py + test_a11y_audit.py（W266·E5 测试深化·3 新建）
>   - .github/workflows/perf.yml（W266·E5·Lighthouse CI + 性能预算）
>   - scripts/perf_monitor.py（W267·E6 监控深化·RUM + alerting + 趋势对比）
>   - site/js/rum.js（W267·E6·RUM 采集 5 指标）
>   - scripts/output/perf-budget.json + perf-baseline.json（W267·E6·预算+基线）
>   - scripts/security_scan.py（W268·E8 安全深化·_headers + SRI 验证）
>   - site/_headers（W268·E8·CSP + 5 安全头）
>   - .env.example（W268·E8·脱敏模板）
>   - README.md / STRUCTURE.md / docs/00-导读/项目说明.md / 交接文档.md（6 项目层文档同步 v2.2.46→v2.2.47 + W262→W268 + E 方向深化描述）
>   - CHANGELOG.md（本段·新增 v2.2.47 W263-W268 版本段）
>   - scripts/output/file-index.md（反向索引新增 W263-W268 段）
> - **验证**：DRL R1b 主代理 spot-check 真收敛·P0=0/P1=0/P2=0/P3=0
```

### Step 2: README.md

版本号 v2.2.46→v2.2.47 + E 方向深化描述（E1 CI/CD matrix + E2 a11y WCAG 2.2 + E3 perf_optimize + E5 测试 80% + E6 RUM + E8 CSP/SRI）

### Step 3: STRUCTURE.md

版本号 v2.2.46→v2.2.47 + W### 计数 262→268 + 版本史段 v2.2.47 条目

### Step 4: docs/00-导读/项目说明.md

版本号 v2.2.46→v2.2.47 + E 方向深化描述

### Step 5: 交接文档.md

顶部最后更新 + 当前进度段标题 v2.2.46→v2.2.47 + W263-W268 里程碑段 + 当前版本号 v2.2.46→v2.2.47 + W### W262→W268 + 下一编号 W268→W269 + 使用说明段

### Step 6: scripts/output/file-index.md

新增 W263-W268 反向索引段（14 新建/修改 + 6 同步 = 20 文件）

---

## Task 6: 主代理 mem-wrap-up（memory 层三件套 + user_profile.md）

### Step 1: work-log.md

新增 W263-W268 段（保留 W232+W233+W234+W235+W236+W237-W244+W245-W252+W253-W256+W257-W262 段）

### Step 2: topics.md

新增 W263-W268 专题概要

### Step 3: retrospective.md

新增 W263-W268 dim 1/5/9/11 复盘 + 收敛曲线 + Self-Disclosure 附加声明

### Step 4: user_profile.md（E1 计数器 54/3→55/3）

- L3 计数器：54/3 → 55/3
- L10 复现统计：50 次新案例 → 51 次新案例·九 session 补登 → 十 session 补登
- L11 链尾：追加 W263-W268
- L12 关键结论：追加 W263-W268
- L13 特殊案例段：追加 W263-W268

---

## 执行模式

**采用 dispatching-parallel-agents 三 subagent 并行执行 Task 1-3，主代理统一执行 Task 4-6。**

- Task 1-3 并行（三 subagent 独立无共享状态）
- Task 4 主代理 DRL R1b spot-check（待 Task 1-3 完成后）
- Task 5 主代理同步项目层 6 文档（待 Task 4 通过后）
- Task 6 主代理 mem-wrap-up（待 Task 5 完成后）
