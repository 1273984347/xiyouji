# E 方向 6 产出深化设计（v2.2.47·W263-W268）

> **日期**：2026-07-30
> **版本**：v2.2.47
> **W### 范围**：W263-W268
> **方向**：E 方向（工程化深化）
> **执行模式**：dispatching-parallel-agents 三 subagent 并行

## 一、背景与目标

### 1.1 背景

E 方向已有 E1-E8 全部 8 子方向落地（W234 + W236）：
- **E1 CI/CD**（W234）：ci.yml + deploy.yml + README.md
- **E2 a11y**（W234）：a11y_audit.py 5 规则 + a11y-report.md
- **E3 性能优化**（W236）：optimize-html-size.py + font-subset-guide.md + fix_svg_negative_widths.py
- **E4 i18n**（W234）：site/en/ 7 文件
- **E5 测试深化**（W236）：tests/unit + tests/e2e
- **E6 性能监控**（W236）：perf_monitor.py + perf-report.md
- **E7 SEO 优化**（W236）：structured-data.jsonld + sitemap.xml + robots.txt
- **E8 安全加固**（W236）：security.yml + security_scan.py + security-report.md

### 1.2 目标

深化 E1/E2/E3/E5/E6/E8 六子方向（跳过 E4 i18n + E7 SEO·深化空间相对较小），每个子方向升级一层。6 产出 = 9 文件，dispatching-parallel-agents 三 subagent 并行（每个 subagent 2 产出）。

## 二、执行策略

### 2.1 dispatching-parallel-agents 三 subagent 并行

| Subagent | W### 范围 | 子方向 | 产出数 |
|:---|:---|:---|:---|
| A | W263-W264 | E1 CI/CD 深化 + E2 a11y 深化 | 2 |
| B | W265-W266 | E3 性能深化 + E5 测试深化 | 2 |
| C | W267-W268 | E6 监控深化 + E8 安全深化 | 2 |

### 2.2 分组依据

- **Subagent A（CI/质量门）**：E1 CI/CD + E2 a11y 同属质量门禁·共享 ci.yml 集成
- **Subagent B（性能/测试）**：E3 性能 + E5 测试同属运行时质量·共享 perf 基线
- **Subagent C（监控/安全）**：E6 监控 + E8 安全同属运行时防护·共享 alerting 机制

## 三、6 产出具体内容

### 3.1 Subagent A（W263-W264）

#### W263 E1 CI/CD 深化

**文件**：`.github/workflows/ci.yml`（修改）

**升级内容**：
- matrix 测试：Python 3.10/3.11/3.12 × ubuntu/windows/macos（9 矩阵）
- pip 缓存：`cache: pip` + `cache-dependency-path: scripts/requirements.txt`
- artifact 保留 30 天：`retention-days: 30`
- 失败重试 3 次：`max-attempts: 3`
- 并发取消旧 run：`concurrency: { group: ci-${{ github.ref }}, cancel-in-progress: true }`
- 新增 job：dependency-scan（pip-audit）+ code-quality（ruff + black --check）

#### W264 E2 a11y 深化

**文件**：`scripts/a11y_audit.py`（修改）

**升级内容**：WCAG 2.1 → 2.2 新增 4 规则：
- 规则 6：焦点可见（Focus Visible）- 验证 `:focus-visible` 样式存在
- 规则 7：目标尺寸（Target Size）- 验证按钮/链接最小 24×24px
- 规则 8：拖拽移动（Dragging Movements）- 验证可拖拽元素有替代方案
- 规则 9：一致帮助（Consistent Help）- 验证帮助机制位置一致
- 键盘导航审计：Tab 顺序 + 焦点陷阱检测
- 屏幕阅读器 ARIA 标签验证：`aria-label`/`aria-labelledby`/`aria-describedby` 完整性

### 3.2 Subagent B（W265-W266）

#### W265 E3 性能深化

**文件**：`scripts/perf_optimize.py`（新建）

**内容**：
- LCP 优化：图片懒加载 `loading="lazy"` + 资源预加载 `<link rel="preload">` + 字体子集化实施（调用 font-subset-guide.md 方案）
- Canvas 渲染深化：D3.js SVG → Canvas 转换脚本（大数据集 ≥1000 节点）
- 关键 CSS 内联：提取首屏 CSS + 内联到 `<style>`
- JS 延迟加载：`defer`/`async` 属性自动添加 + 动态 import()
- 资源压缩：HTML/CSS/JS minify + gzip 预压缩
- 输出：`scripts/output/perf-optimization-report.md`

#### W266 E5 测试深化

**文件**：`tests/`（新建/修改）

**内容**：
- 覆盖率提升到 80%：新增 `tests/unit/test_perf_optimize.py` + `tests/unit/test_security_scan.py` + `tests/unit/test_a11y_audit.py`
- 视觉回归 baseline 10→20：新增 10 个 baseline 截图（W233-W236 4 HTML + W236 6 HTML）
- 性能测试 Lighthouse CI：`.github/workflows/perf.yml` 新建（Lighthouse CI + 性能预算断言）
- 端到端测试 17→25 用例：新增 8 用例（跨页面导航 + 暗色模式 + 全局筛选器 + dashboard KPI + 搜索浮层 + 英文站 + 3D 网络 + 交互式地图）

### 3.3 Subagent C（W267-W268）

#### W267 E6 监控深化

**文件**：`scripts/perf_monitor.py`（修改）+ `scripts/output/perf-budget.json`（新建）+ `scripts/output/perf-baseline.json`（新建）

**升级内容**：
- RUM 真实用户监控：`site/js/rum.js` 新建（采集 LCP/CLS/INP/TBT/FCP + 发送至 /api/rum）
- Core Web Vitals alerting 阈值：LCP > 2.5s / CLS > 0.1 / INP > 200ms 触发 alert
- 性能预算 budget.json：HTML < 50KB / CSS < 100KB / JS < 200KB / 图片 < 500KB
- 性能基线 baseline.json：当前各页面 Core Web Vitals 快照
- 历史趋势对比：`scripts/output/perf-trend-{date}.json` 每日快照

#### W268 E8 安全深化

**文件**：`scripts/security_scan.py`（修改）+ `site/_headers`（新建）+ `.env.example`（新建）

**升级内容**：
- CSP 内容安全策略：`site/_headers` 新建（Content-Security-Policy + X-Frame-Options + X-Content-Type-Options + Referrer-Policy + Permissions-Policy）
- SRI 子资源完整性：外部资源（D3.js/Three.js）添加 `integrity` + `crossorigin`
- 依赖扫描：`pip-audit` 集成到 CI/CD + `npm audit` 集成
- 安全头验证：`security_scan.py` 新增 `_headers` 文件验证 + SRI 验证
- 密钥管理：`.env.example` 新建（脱敏模板）+ `.env` 加入 .gitignore 验证

## 四、文件结构

| 文件 | 类型 | 行数估算 |
|:---|:---|---:|
| .github/workflows/ci.yml | 修改 | +80 |
| .github/workflows/perf.yml | 新建 | ~60 |
| scripts/a11y_audit.py | 修改 | +120 |
| scripts/perf_optimize.py | 新建 | ~250 |
| scripts/perf_monitor.py | 修改 | +100 |
| scripts/security_scan.py | 修改 | +80 |
| site/_headers | 新建 | ~40 |
| site/js/rum.js | 新建 | ~80 |
| .env.example | 新建 | ~30 |
| scripts/output/perf-budget.json | 新建 | ~50 |
| scripts/output/perf-baseline.json | 新建 | ~50 |
| tests/unit/test_perf_optimize.py | 新建 | ~150 |
| tests/unit/test_security_scan.py | 新建 | ~120 |
| tests/unit/test_a11y_audit.py | 新建 | ~100 |

**6 产出（按 W### 计）= 14 文件**

## 五、跨方向呼应

- W263 与 W234-E1 CI/CD 形成"基础→深化"双轨
- W264 与 W234-E2 a11y 形成"5 规则→9 规则"升级
- W265 与 W236-E3 性能优化形成"方案→实施"双轨
- W266 与 W236-E5 测试深化形成"三层→四层"升级
- W267 与 W236-E6 性能监控形成"采集→alerting"升级
- W268 与 W236-E8 安全加固形成"扫描→防御"升级

## 六、验证标准

### 6.1 DRL R1b 主代理 spot-check 真收敛

- P0=0/P1=0/P2=0/P3=0
- 6 产出结构完整性（footer 双索引 + W### ID + 版本号 v2.2.47）
- 无 placeholder/TBD/TODO

### 6.2 项目层 6 文档同步

- CHANGELOG.md：新增 v2.2.47 W263-W268 版本段
- README.md：版本号 v2.2.46→v2.2.47 + E 方向深化描述
- STRUCTURE.md：版本号 v2.2.46→v2.2.47 + W### 计数 262→268 + 版本史段
- docs/00-导读/项目说明.md：版本号 v2.2.46→v2.2.47 + E 方向深化描述
- 交接文档.md：顶部最后更新 + 当前进度段 + W263-W268 里程碑段 + 当前版本号 + W### + 下一编号
- scripts/output/file-index.md：新增 W263-W268 反向索引段

### 6.3 memory 层三件套补齐 + user_profile.md E1 计数器更新

- work-log.md：新增 W263-W268 段
- topics.md：新增 W263-W268 专题概要
- retrospective.md：新增 W263-W268 dim 1/5/9/11 复盘
- user_profile.md：E1 计数器 54/3→55/3 + 链尾追加 W263-W268 + 特殊案例段追加
