# xiyouji-plan-review 参考资料

SKILL.md 的配套参考：① 取证命令库（可逐字复跑）② 声称值 vs 实测对照表模板 ③ 评估文档结构模板 ④ 历史偏差案例。shell 为 git-bash，均在 `cd D:/1/xiyouji` 下执行。

## 1. 取证命令库

### 1.1 git HEAD 与工作区状态

```bash
cd D:/1/xiyouji && git rev-parse --short HEAD && git log -1 --oneline
cd D:/1/xiyouji && git status --porcelain | wc -l && git status --porcelain | head -20
# 有未提交改动时看内容判断归属（可能是并发 session）：
cd D:/1/xiyouji && git --no-pager diff "文件名" | head -40
```

### 1.2 目录/页面实测计数

```bash
# CN 可视化页（含 _shell.html 模板，实际页数 = 结果 - 1）
cd D:/1/xiyouji && ls site/data/*.html | wc -l
# EN 站全部页面（EN 无 data 子目录，可视化页平铺在 site/en/）
cd D:/1/xiyouji && ls site/en/*.html | wc -l
# dataset JSON 数
cd D:/1/xiyouji && ls dataset/*.json | wc -l
# sitemap URL 数
cd D:/1/xiyouji && grep -c '<loc>' site/sitemap.xml
# EN 与 CN 同名可视化页缺失清单（结果应为缺 journey-geo-3d）
cd D:/1/xiyouji && for f in $(ls site/data/*.html | grep -v _shell | xargs -n1 basename); do [ -f "site/en/$f" ] || echo "$f"; done
```

### 1.3 引用脚本/文件存在性（必须用 ls，Glob 会漏）

```bash
# 逐个核实，2>&1 让"不存在"也显式输出
cd D:/1/xiyouji && ls scripts/脚本A.py scripts/脚本B.py scripts/output/产物.json 2>&1
# 声称"已有"的文件还要看内部版本/日期字段：
cd D:/1/xiyouji && head -10 scripts/output/perf-baseline.json
cd D:/1/xiyouji && cat scripts/output/perf-budget.json
```

### 1.4 关键链路 grep 抽查

```bash
# 脚本加载方式（async/defer）
cd D:/1/xiyouji && grep -o '<script[^>]*\(goatcounter\|visit-log\)[^>]*>' site/index.html site/data/81-hardships.html site/en/index.html | head -20
# 特征覆盖率（示例：JS 动效 .duration( 覆盖页数）
cd D:/1/xiyouji && grep -l '\.duration(' site/data/*.html | wc -l
cd D:/1/xiyouji && grep -l '\.duration(' site/en/*.html | wc -l
# SEO 覆盖现状
cd D:/1/xiyouji && grep -rl 'application/ld+json' site/*.html site/data/*.html | wc -l
cd D:/1/xiyouji && grep -rl 'meta name="description"' site/*.html site/data/*.html | wc -l
# 组件引用页数（示例：visit-log）
cd D:/1/xiyouji && grep -rl 'visit-log' site/*.html site/data/*.html site/en/*.html | wc -l
# 门禁结构速览
cd D:/1/xiyouji && grep -n 'def \|CHECK\|EXPECT\|FAIL' scripts/verify_delivery.py | grep -iv '^\s*#' | head -60
```

### 1.5 体积/预算交叉验证

```bash
cd D:/1/xiyouji && wc -c site/tokens.css site/system.css
# 内联放大效应：tokens 每增 1KB × 全站页数 = 全站增量，报体积结论时必须乘页数
cd D:/1/xiyouji && ls -la site/data/text-search.html 2>/dev/null  # 大内嵌数据页单查
```

### 1.6 感知型目标前后渲染差异实测（worktree 截图法）

方案目标为观感/高级感/体验时，用 git worktree 取前后版本截图对比，判断"验收全绿是否等于观感达成"：

```bash
# 1) 建两个 detached worktree（在仓库外路径，避免污染工作区；Windows 下用 C:/ 绝对路径）
cd D:/1/xiyouji && git worktree add --detach "C:/<tmp>/<name>-before" <方案前基线提交>
cd D:/1/xiyouji && git worktree add --detach "C:/<tmp>/<name>-after"  <方案后提交>
# 2) Playwright 全页截图（NODE_PATH 指向全局 npm 包；file:// 直开页面）
NODE_PATH="$(npm root -g)" node 截图脚本.js   # 脚本模式：1440×900 全页 + 关键 hover 局部，脚本放 scratch 目录勿入库
# 3) 目检或 PIL 拼左右对比图；hover 态差异需 hover 元素后截 clip
# 4) 收尾必须清理 worktree
cd D:/1/xiyouji && git worktree remove "C:/<tmp>/<name>-before" && git worktree remove "C:/<tmp>/<name>-after"
```

判读口径：前后截图"肉眼不可辨"即证明该批次的"观感升级"目标未达成（哪怕 M 指标全绿）；仅 index 等个别页面有差异时要如实拆分汇报，不写"整体有提升"。

## 2. 声称值 vs 实测对照表模板

| # | 方案声称（原文摘录） | 声称出处（节/行） | 实测值 | 判定 | 说明 |
|---|---|---|---|---|---|
| 1 | 基线 HEAD=fdf439d | 文首 | `git rev-parse` = fdf439d | ✅ | 一致 |
| 2 | CN 可视化页 86 | §0 | site/data 87 HTML − _shell = 86 | ✅ | 注意口径：87 含模板 |
| 3 | EN 可视化页 N=86 | W471 | EN 同名页实测 85（缺 journey-geo-3d） | ⚠️ | 口径偏差，建议改 85 或注明豁免 |
| … | … | … | … | ❌ | 不符须写影响 |

判定符号约定：✅ 一致 / ⚠️ 口径偏差（数字可解释但表述需修正）/ ❌ 不符（实测否证声称）。

## 3. 评估文档结构模板

```markdown
# 《方案名》评估意见

> 评估对象：① 文档A（性质）② 文档B（性质）
> 评估日期：YYYY-MM-DD · 评估基线：git HEAD `xxxxxxx`（vX.Y.Z W###）——与方案声明基线【一致/不一致：差异说明】
> 评估方法：先取证后下结论——所有关键数字均经仓库实测核实，非文本复述

## 一、评估摘要（结论先行）

总体判断一段话：可执行 / 有条件可执行 / 需返工 + 核心理由（N 项关键数字实测通过/发现 M 处偏差）。
随后列"必须优先处理的点"前三条（每条：问题 + 实测证据 + 影响）。

## 二、证据基线表（声称 vs 实测）

（收录第 2 节模板的完整表格）

## 三、技术可行性
## 四、结构合理性
## 五、可维护性
## 六、性能表现
## 七、潜在风险

（每维度：论断 + 实测证据引用；无证据的写"待验证"）

## 八、核心优势

（具体点名，不空夸）

## 九、不足与改进对照表

| # | 不足 | 实测证据 | 影响 | 改进建议 |
|---|---|---|---|---|

## 十、优先行动建议

1. （可直接回填进方案的修订动作，≤3 条）
```

## 4. 历史偏差案例（Phase 3 路线图评估当次发现，供校准判断尺度）

1. **CI 污染观测数据（高）**：方案只排除了维护者浏览器，未排除 GitHub Actions 的 Playwright/LHCI 真实浏览器访问，GoatCounter 会把 CI 记成访客，决策闸门输入虚高。
2. **SEO 工程量低估（中高）**：实测全站 meta description / JSON-LD 各仅 1 页覆盖，方案要求"0 缺失"实为 200+ 页批量生成，3–6h 工时不现实。
3. **脚本输入来源悬空**：决策脚本的数据输入（API 自动拉取还是人工录入）方案未说清，自动化定位落不了地。
4. **预算冲突**：perf-budget total 900KB 与内嵌 2MB JSON 的数据页直接冲突，不改口径验收必 FAIL。
5. **N 口径偏差**：EN 站同名可视化页实际 85（缺 journey-geo-3d），方案写 86。
6. **"新建 vs 更新"措辞失真**：perf-baseline.json 已存在（W267 版），方案写"新建"，应写"更新"。
7. **视觉目标用工程卫生验收（中高，2026-08-22）**：Phase E「视觉高级感升级」（W476–W478）验收 M1-M7 全为对比度/裸色=0/阴影来源/动效时长/体积/报错，明文"不认看起来更好"；worktree 前后截图实测 E1 仅 index 一页有可见变化、E2 56 页严格等值迁移零感知。教训：观感类方案验收必须含前后对比截图/目视清单/A-B，评估时先用 §1.6 实测渲染差异再下"目标达成"结论。

这些案例说明：偏差多藏在"覆盖率声称、工时估算、新建/已有措辞、预算交叉、**感知型验收**"五类位置——取证时优先扫这五类。
