# xiyouji-plan-authoring 参考模板与取证速查

本文件供撰写方案时按需取用：§1 骨架模板、§2 基线表示例、§3 取证命令速查、§4 汇报模板。

## 1. 方案文档骨架（§0-§9 + §10 落地状态）

```markdown
# 《...》...方案（Phase X · W###–W###）

> 版本：v1（提案·待用户确认）· YYYY-MM-DD
> 适用基线：vX.Y.Z W###（HEAD xxxxxxx＝git rev-parse --short HEAD 实测值）· YYYY-MM-DD 实测
> 性质：跨批次...路线图（覆盖 W###–W### 候选，编号启动时须 Grep 现役最大 W 复核）；各批次落地时另拆单批 plan/spec
> 上游依据：① ... ② ... ③ ...
> 目标读者：主代理 + 新接任 Agent + 人类维护者
> 待用户确认项：① ... ② ... ③ ...

---

## 0. 现状基线（实测快照）

> 以下数字为 YYYY-MM-DD 实测；「差距项」是本方案要消除的对象。

| 维度 | 现值 | 来源 | 差距项 |
|:---|:---|:---|:---|
| ... | ... | ... | ... |

## 1. 设计目标与原则

## 2. 阶段/维度拆解

### E1 · 名称（W### · P#）

## 3. 批次计划

### Phase X0 · 取证与定稿（W### · P0）

> 每批验收统一为「指标 = 阈值（测量方法）」三段式；主观目标先译 M 代理指标表（如对比度 ≥4.5:1、裸 hex=0、duration ≤600ms、LHCI 三指标、pageerror=0）；无测量命令的条款不得写入。页面清单用派生命令（如 `grep -l 'forceSimulation' site/data/*.html`），不手写名单。

## 4. 工作量与排期

## 5. 统一验收门禁（每批必跑）

## 6. 风险与依赖

## 7. 前置取证（E0 探针清单）

## 8. 与既有方案的关系

## 9. 待用户确认项（启动前三问）

## 10. 落地状态记录（随执行回写）

| 批次 | 状态 | commit | 关键数字 | 偏差说明 |
|:---|:---|:---|:---|:---|
| E0 | ✅ | abc1234 | ... | 无 |
| E1 | ✅ | def5678 | ... | 图标集移 E5 |
| E2 | ⏸ | — | — | 未执行/挂起 |

> ✅ = 已执行（commit 为 git rev-parse --short HEAD 实测）；⏸ = 未执行/挂起；偏差须含移入批次。
```

## 2. 基线表示例（摘自已落库的 Phase E 方案 §0）

| 维度 | 现值 | 来源 | 差距项 |
|:---|:---|:---|:---|
| 设计令牌 | tokens.css 5.7KB · 12 基础色 + 图表五色 + 动效令牌 | tokens.css v2（W334） | 无色阶梯度、无 dark mode |
| 组件层 | system.css 18.9KB · 40+ 组件类（card/btn/badge/kpi 等） | system.css | 部分样式硬编码、页面实现漂移 |
| 页面规模 | CN 86 可视化页 + 9 根页；EN 138 页（85 页与 CN 同名） | 目录实测 | 双站内联样式双倍维护 |
| 性能预算 | html 50KB / css 100KB / js 200KB / total 900KB（bytes） | scripts/output/perf-budget.json | tokens+system 内联，扩充推高全站体积 |
| 门禁体系 | verify_delivery（CSP 0 漂移/结构平衡/JS 语法/链接）+ LHCI + a11y_audit.py | scripts/ | 无对比度/token 覆盖率专项门禁 |

要点：每行必须给「来源」，来源=文件路径或"目录实测/命令"；现值必须是该来源可复现的数字。

## 3. 取证命令速查

| 目的 | 命令（在 D:\1\xiyouji 下） |
|---|---|
| git HEAD 与工作区状态 | `git rev-parse --short HEAD && git status --porcelain` |
| CN 可视化页数（排除 _shell.html） | `ls site/data/*.html | grep -v _shell | wc -l` |
| EN 页数 | `ls site/en/*.html | wc -l` |
| tokens/system 体量 | `wc -c site/tokens.css site/system.css` |
| 脚本存在性 | `ls scripts/<脚本名>` |
| 覆盖扫描（如动效） | `grep -l '.duration(' site/data/*.html | wc -l` |
| 同名页对比（CN vs EN） | `for f in $(ls site/data/*.html | grep -v _shell | xargs -n1 basename); do [ -f "site/en/$f" ] || echo "EN缺: $f"; done` |
| 性能预算 | `cat scripts/output/perf-budget.json` |
| sitemap 计数 | `grep -c '<loc>' site/sitemap.xml` |
| dataset 数 | `ls dataset/*.json | wc -l` |
| 最大 W 编号 | `grep -oE 'W[0-9]{3}' CHANGELOG.md 交接文档.md docs/superpowers/plans/*.md | sort -u | tail -5` |

## 4. 汇报模板（结论先行）

- 方案定位：一句话（名称 + 批次范围 + 与上游的关系）。
- 关键取舍：逐条说明（每条 = 判断依据 + 后果），如宪改先行、体积红线、闸门联动。
- 启动前三问：① ... ② ... ③ ...（与 §9 一致），等用户确认后再开始执行。
