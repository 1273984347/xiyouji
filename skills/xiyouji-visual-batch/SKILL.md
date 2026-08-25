---
name: xiyouji-visual-batch
description: 西游记项目（D:\1\xiyouji）Phase E 视觉批次执行 playbook（W476/W477/W478 实测管线 + W488 感知验收/暗色扩展）。步骤：仓库状态重验（多 session 并发勿信快照）→ _probe 探针取证（裸色/transition/组件重复）→ system.css/根页令牌化编辑（elev 海拔/radius/color-mix 派生/fail-open 门禁类模式）→ E2/E3 数据页批量走 _w478_migrate.py 脚本迁移管线（六规则：R-SHADOW 选择器上下文分档/R-RADIUS 复合值逐档/R-TRANS 负向后视防截 1.2s/R-FOCUS color-mix/裸色白名单/R-EXEMPT 页顶注释登记；dry-run 审查后应用；批次记录表落 plans/；M5 净行数测量）→ 可感知升级批暗色夜读页面内联实现模式（每页五件套：防 FOUC script + 页内 dark 覆盖 + 夜读按钮 + toggle JS + reveal；xy-theme 防 FOUC；dark 令牌走页内不落全局；新增内联 script 必须 CSP 重跑；禁 JS fail-open 回退浅色）→ wc -c 体积预算复核（tokens ≤+2KB/system ≤+6KB/单页 ≤33KB）→ 字体子集化（archive/w334 管线复用）→ inline_css.py --force 传播 ~225 页（根页无需传播）→ _shot_check.js Playwright 验证（pageerror=0 全批断言清单自 scripts/output 读 + getComputedStyle 断言 + 截图 Read 目视）→ M-A1 前后对比验收（可感知升级批强制：worktree before/after + PIL 差异像素率 ≥1% + 目视清单 ≥3 处/页）→ 五门禁 → 接 version-bump；commit 时 git restore --staged 排除并行会话改动。当用户要求「执行视觉批次」「E1–E7 批次」「令牌化」「传播批次」「system.css v2」「视觉传播」「海拔/圆角迁移」「执行 Phase E」「纸感轻立体落地」「tokens v3 落地」「夜读模式」「暗色模式」「视觉重设计」「M-A1 验收」「前后对比截图」时触发。
version: 1.2.0
---

# 西游记项目 Phase E 视觉批次执行

给 xiyouji 项目（`D:\1\xiyouji`）执行 Phase E 视觉升级批次（E1–E7 / W477 起）的固定管线。W476（E0 宪改+令牌）与 W477（E1 组件+根页）两批跑通「人工编辑」管线；W478（E2 数据页传播 I）起转向「脚本批量迁移」管线（`_w478_migrate.py` 六规则，dry-run 审查后应用）；E3（W479，86 页减 E2 批余量，含 3D/Canvas、时间线/地图、静态/表格页）原样复用同管线。含多处非显然约束，必须逐字执行。

## 何时触发

触发（正向）：

- 用户要求「执行视觉批次」「跑 E1–E7」「继续 Phase E」「视觉传播」「令牌化落地」。
- 用户要求「system.css v2」「根页模板化」「海拔/圆角迁移」「tokens v3 落地」「纸感轻立体落地」。
- 在 `docs/superpowers/plans/2026-08-18-phase-e-visual-elevation-roadmap.md` 方案批准后开始执行任一 Phase 批次。

排除（反向）：

- 写方案/评估方案（用 `xiyouji-plan-authoring` / `xiyouji-plan-review`）。
- 版本 bump 与六文档同步收尾（本技能第 8 步会转交 `xiyouji-version-bump`，不要在这里重复做）。
- 用户尚未确认开工就提前执行——方案写完 ≠ 授权执行，必须等显式确认。

## 前置条件

- 项目在 `D:\1\xiyouji`，git 分支 `main`，remote `origin`。
- 方案文档：`docs/superpowers/plans/2026-08-18-phase-e-visual-elevation-roadmap.md`（分批计划与验收口径）。
- 关键脚本：`scripts/inline_css.py`（传播）、`scripts/verify_delivery.py`（门禁）、`scripts/archive/w334_font_subset.py`（子集化管线）、`scripts/_e0_probe.py`（E0 探针范式）。
- 体积硬预算（wc -c bytes 口径）：tokens.css 增量 ≤ +2KB、system.css 增量 ≤ +6KB、单页内联合计 ≤ 33KB。
- 当前基线（启动时实测复核，勿信文档快照）：tokens.css ~7.7KB / system.css ~21.4KB / 合计 ~29KB。

## 标准流程（前置 + 九步）

严格按顺序执行，不要跳步。

### 第 0 步：仓库状态重验（多 session 并发教训）

```bash
cd /d/1/xiyouji && git status --short && git log --oneline -3
```

- 核对 HEAD 与方案基线；**勿信快照**——项目存在多 session 并行，工作区可能有他人未提交改动。
- 甄别并行 session 文件（如 `新Agent启动Prompt.md`）：读出 diff 确认归属，与本批无关的记入「commit 时排除清单」。
- 按项目规则 Grep 复核现役最大 W 编号，本批编号 = 最大 + 1。

### 第 1 步：探针取证（_probe 脚本）

- 写一次性诊断脚本 `scripts/_<batch>_probe.py`（`_` 前缀 = 不入库、不入门禁、不进 CI，沿用 `_e0_probe.py` 范式）。
- 扫描面（E0 实测口径，页数以 site/ 实际为准随批次校正）：site 根 9（含 _template）+ data 87（含 _shell）+ en 138 = 233 页；_shell 不计入统计页。
- 探针维度（按批次需要裁剪，E0 六项全跑）：P1 页面 `<style>` 裸 hex/rgba 计数、P2 transition 形态统计（var 令牌/all/裸秒值）、P3 根页 hero/nav/footer 结构 diff、P4 字体加载盘点、P5 tokens/system 体积与增量模拟、P6 公共组件选择器页面内联重复面。
- 产出探针报告落 `docs/superpowers/plans/YYYY-MM-DD-phase-e-e<n>-probe-report.md`，数字为准入后续步骤的基线。
- 探针口径铁律：**多数裸色是图表数据色（D3 fill/stroke/渐变止点）**，属豁免类；不要对 1.6 万处裸色搞一刀切清零。

### 第 2 步：system.css / 根页令牌化编辑

按「令牌先行」顺序：tokens.css → system.css → 页面。页面内联 CSS **只减不增**（公共样式迁回 system.css，页面 `<style>` 只留图表特有规则）。

- **elev 海拔**：`--elev-0..4` 四级（发丝线/静止浮起/交互浮起/中层悬浮/高层遮罩），阴影色用墨色低 alpha 非纯黑。
- **radius**：`--radius-sm/md/lg`（2/6/10px，维持小圆角克制风）。
- **color-mix() 派生**：色阶令牌一行定义多档（如 accent/neutral 50–900），禁止逐档硬编码。
- **fail-open 门禁类模式**：`.reveal-in` 必须 fail-open——隐藏态只在 `.js-reveal` 祖先存在时才生效（JS 挂类），JS 禁用或失败时内容默认可见。**禁止写裸 `.reveal-in { opacity: 0 }` 规则**（JS 不跑就白屏）。
- **五态完备**：交互组件必须定义 default/hover/active/focus-visible/disabled 五态。
- **渐变白名单（仅三处）**：hero 玄墨双色微渐变（明度差 ≤6%）、主按钮朱砂微渐变、骨架屏 shimmer；禁止大面积彩色渐变/霓虹光效。
- **动效契约**：时长三档 150/250/≤600ms + RM 双守卫（CSS 走 `prefers-reduced-motion` 覆写，JS 走 MOYUN_RM）；transition 裸值（0.2s/all 等）映射到 `--dur-fast/--dur-base`。
- 根页模板化对象（E1 实测口径）= 6 页（index/dashboard/curated/guide/dukou-engine/mobile-index）+ `_template.html`；rum-viewer/visit-viewer 两个本地诊断页豁免。

> 本步仅适用于 E0/E1（system.css / 根页令牌化）；E2/E3 数据页批量迁移走第 2b 步脚本管线，不要人工逐页 Edit。

### 第 2b 步：E2/E3 批量迁移（_w478_migrate.py 六规则管线）

W478 起数据页批量不再人工逐页 Edit：写一次性脚本 `scripts/_<batch>_migrate.py`（`_` 前缀不入库，直接复刻 `scripts/_w478_migrate.py` 实测范式），**忠实复刻试点人工迁移范式**，六规则：

- **R-SHADOW（选择器上下文分档）**：`box-shadow:` 硬编码阴影按选择器上下文映射——`:hover`→`--elev-2`；`tip/tooltip/popover/modal`→`--elev-3`；`rgba(0,0,0,0.3`→`--elev-3`；其余→`--elev-1`。
- **R-RADIUS（复合值逐档）**：`border-radius` 复合值**逐 token** 拆档映射，1–3px→`--radius-sm`、4–8px→`--radius-md`、9–12px→`--radius-lg`、≥999px 或 50%→`--radius-pill`。
- **R-TRANS（负向后视防截）**：时长令牌映射——`all 0.2s`→`all var(--dur-base)`、`all 0.15s`→`all var(--dur-fast)`、裸 `0.2s`/`0.15s`→`var(--dur-base)`/`var(--dur-fast)`；裸秒值正则**必须**带 `(?<![\d.])` 负向后视 + `(?![\d])` 负向前视，否则 `1.2s` 被截成 `1var(--dur-base)`（E2 实测教训）。
- **R-FOCUS（color-mix 派生）**：`var(--focus-ring…)`→`color-mix(in srgb, var(--accent) 15%, transparent)`。
- **裸色白名单**：仅映射白名单色——`#fff/#ffffff`→`--paper`；`#fff8e7/#fff8ec/#fffdf8/#f5e9d4/#f5efe4/#f5ede0`→`--paper-warm`；`#23201a/#2c2418`→`--ink`；`#6b5e4d/#6b6455`→`--ink-soft`。白名单漏色 → 渐变只映射一半（E2 实测，dry-run 必查）。
- **R-EXEMPT（页顶注释登记）**：迁移后剩余裸 hex/rgba 计数 >0 时，在页私有 style 块顶部插 `/* e-track-exempt: chart-data-colors N 处 */`（图表数据色豁免登记）。

范围铁律：

- **仅页私有 `<style>` 块**：跳过 INLINED tokens+system 块（块前 200 字符含 `INLINED CSS` 标记）、跳过含 `--elev-0: none`/`system.css` 标记的块；**禁全站盲正则**。
- **页面清单派生命成**（非手写）：网络批 `grep -l 'forceSimulation'` + 热力/统计批 `grep -l 'scaleBand|heatmap|histogram'` 去重合并，排除试点页。E2 实测口径：56 页 = 网络批 20 + 热力/统计批 36（比预估 16+20 多 20 页——`cross-time-danmaku/journey-geo-semiotics/perf-canvas-rendering/relationships` 等命中 forceSimulation）。grep 通配需显式文件列表（`xargs`），跨脚本复用改 Python `Path.glob` 读文本匹配（E2 教训）。
- **dry-run 审查后应用**：`python scripts/_w478_migrate.py --dry` 仅输出拟改行（含 `var(--elev-|--radius-|--dur-|--paper|--ink` 与 `e-track-exempt` 的行）供人工审查 → 通过后实际应用。dry-run 阶段必查两坑：白名单漏色、duration 截断。
- **批次记录表**落 `docs/superpowers/plans/YYYY-MM-DD-phase-e-e<n>-batch-record.md`：表头 `| 页 | 批次 | R-SHADOW | R-RADIUS | R-TRANS | R-FOCUS | 裸色→令牌 | tooltip 收编 | 豁免 N | pageerror | 状态 |`，头部含范围口径/规则/验收，备注段含 M5 净行数与门禁数字（范式见 `2026-08-18-phase-e-e2-batch-record.md`）。
- **M5 净行数测量**：迁移完成后测增/删/净行数——E2 实测增 1015/删 913/净 +102 行（≈+2 行/页，均为 e-track-exempt 登记注释与显式 transition 换行）；M5「不增」口径下登记行豁免，数字回填批次记录备注。

### 第 2c 步：暗色夜读模式（页面内联实现模式，可感知升级批）

W488 实测（根页视觉重设计 + 夜读模式第一批）的暗色实现模式。**dark 令牌走页面内联 `<style>`，不落全局 tokens.css**——225 个数据页零波及、体积预算零风险。全站暗色是第二批（W489）的事：dark 令牌组迁入 tokens.css（`html[data-theme="dark"]` 覆盖 15 组变量 + 深色 elev + SVG 数据色提亮）+ 共享 `js/theme-init.js` + inline_css --force 传播 225 页。不要在根页先行批提前全局化。

每页五件套（W488 实测口径，缺一不可）：

1. **head 最前同步防 FOUC script**（viewport meta 后）：同步读 `localStorage['xy-theme']` → 无则 `matchMedia('(prefers-color-scheme: dark)')` 跟随系统 → dark 时在 body 渲染前挂 `document.documentElement.setAttribute('data-theme','dark')`。**fail-open**：禁 JS 或异常时不挂属性、保持浅色（M-A9 验收项）。
2. **页内 dark 覆盖 `<style>`**：`html[data-theme="dark"]` 覆盖 `:root` 变量 + 硬编码色。独立变量体系页（如 dukou-engine 用 `--paper/--ink/--cinnabar` 而非 tokens 变量）必须**双体系覆盖**（自己的变量 + tokens 变量），否则暗色下白底残留。
3. **夜读切换按钮**：topnav 右侧 SVG 按钮（moon/sun 图标）；无 topnav 页按结构放置（header flex 行内 / hero 右上角 absolute）。
4. **toggle JS**：点击切 `data-theme` + 写 `localStorage['xy-theme']`，同步按钮图标。
5. **reveal / 交互 JS**：滚动显现等按 fail-open 规则接入（`.js-reveal` 祖先作用域内）。

dashboard 类图表页另加**图表 dark 适配**：轴/网格/序列色走令牌覆盖（W488 实测只做轴/网格/序列色令牌覆盖，不全图配色重调）。

CSP 铁律：新增任何内联 `<script>`（防 FOUC / toggle / reveal）**必须先重跑 generate_csp.py 再 --check**，否则 CSP 哈希漂移、被浏览器拒绝执行（W488/W492 实测）。

### 第 3 步：体积预算复核

```bash
cd /d/1/xiyouji && wc -c site/tokens.css site/system.css
```

- 硬预算：tokens 增量 ≤ +2KB（上限 ~7.7KB）、system 增量 ≤ +6KB（上限 ~24.9KB）、单页内联合计 ≤ 33KB。
- 超预算处理顺序：先砍微交互工具类，**不砍色彩令牌**。
- 复核后把实际增量回填探针报告「E<n> 落地数字」段。

### 第 4 步：字体子集化（仅当字体文件需更新）

- 复用 `scripts/archive/w334_font_subset.py` 管线：扫 docs/ + site/ 实际用字（CJK + ASCII + 全角标点）→ pyftsubset → 覆写 `site/static/fonts/` 同名文件（文件名不变，`@font-face` 无需改动）。
- 批次封装范式：`scripts/_w477_sans_subset.py`（Noto Sans SC 两档未子集化是最大字体重量点，W477 已处理）。
- 依赖 fontTools；改完用 `wc -c` 确认目标体积下降、无字体缺失。

### 第 5 步：inline_css.py --force 传播

```bash
cd /d/1/xiyouji && python scripts/inline_css.py --force
```

- 只处理含 `../tokens.css` 链接的页面（data 87 + en 138 ≈ **225 页**）。
- **根页无需传播**——根页走同目录 `<link href="tokens.css">` 实时引用、自动跟随；不要尝试「修复」根页的内联行为。

### 第 6 步：_shot_check.js Playwright 视觉验证

- 写批次验证脚本 `scripts/_<batch>_shot_check.js`（范式见 reference.md §3，沿用 `_w477_shot_check.js`）。
- 验证三件套，缺一不可：
  1. **pageerror = 0**：file:// 加载监听 pageerror，每页错误数必须为 0；E2 起按批次验收口径可扩展为**全批断言**（E2 实测 56/56 页）；断言页清单从 `scripts/output/<batch>_list.txt` 动态读取，**不要写死进脚本**——bash 生成的清单必须落 `scripts/output/`（Windows 下 node 读不到 `/tmp`），node 侧用 `require('path').join(__dirname, 'output', 'e2_list.txt')` 读（E2 实测教训）；
  2. **getComputedStyle 断言**：抽查 `.card/.kpi/.chart-block` 等元素的 borderRadius / boxShadow，确认新令牌真实生效（不能只看源码）；
  3. **截图 Read 目视**：截图后**必须用 Read 工具逐张看**，确认视觉无意外（阴影过重/圆角崩坏/布局错位），不能只看断言；全批断言时截图仅保留前 6 页避免产物膨胀。
- 批次内页 + 根页抽样 ≥ 6 页；RM 守卫抽查（CSS media + JS MOYUN_RM 双路径）按 E5 验收口径。

### 第 6b 步：M-A1 前后对比感知验收（可感知升级批强制）

W488 起，「可感知升级批」（根页视觉重设计/暗色/视觉强化）**强制** M-A1：before/after 前后对比截图量化验收——解决 E1/E2 的「肉眼不可辨」伪验收问题。指标：每页差异像素率 ≥ 1% + 目视清单 ≥ 3 处可辨差异，两者缺一不可。

- **before 基线**：在旧基线 commit 上 `git worktree add <tmp> <commit>` 建 before 工作区，不污染当前工作区；after 用当前工作区。
- **截图三套**：Playwright fullPage 逐页截 before / after / dark（各 6 页）；**等待滚动**——fullPage 截图会滚动，触发所有 reveal-in 的 IO（reveal 元素在视口外 opacity:0，不滚动会低估差异），截图前 wait ~2.2s 等动画完成。
- **PIL 差异像素率**：同尺寸 before/after 逐像素比较，任一通道差 > 阈值（W488 实测用 >12）即算差异像素，占比 **每页 ≥ 1%** 强制门槛；页面高度不一致先对齐画布，否则 diff 集中在底部空白。不达标不许过验收。
- **目视清单**：每页 ≥ 3 处可辨差异（如 hero 大数字朱砂/表头淡朱砂/KPI 数字朱砂/导航指示条/夜读按钮/route-strip 朱砂线/emoji→SVG），落 plans/ 对比图（左右拼接 + diff 率标注）。
- **暗色冒烟（M-A2/A3）**：dark 各页 pageerror=0 + FOUC=0（domcontentloaded 时 data-theme=dark 已注入）+ 禁 JS 回退浅色正常（M-A9）。
- W488 实测基准：index 2.35% / dashboard 5.05% / curated 2.84% / guide 5.88% / dukou-engine 25.98% / mobile-index 7.07%，6/6 ≥1%（脚本骨架见 reference.md §4）。

### 第 7 步：五门禁全绿

```bash
cd /d/1/xiyouji && python scripts/verify_delivery.py        # 退出码 0（核心全绿）
cd /d/1/xiyouji && python scripts/generate_csp.py --check   # 0 漂移（改内联 <script> 后先重跑 generate_csp.py 再 check）
cd /d/1/xiyouji && node  scripts/check_js_syntax.js         # 0 语法错误（改内联 JS 时）
cd /d/1/xiyouji && python scripts/check_structure.py        # 0 结构失衡（批量改 CSS 必跑）
cd /d/1/xiyouji && python scripts/lint_links.py             # 0 broken
```

E 轨专项补跑：`a11y_audit.py`（对比度规则，E6 起挂 verify_delivery）、`_token_coverage.py`（页面裸 hex 扫描，E6 转正）、`pre_release_screenshot.py`（前后对照）。任一 FAIL 即阻断，修完重跑。

### 第 8 步：接 version-bump

调用 `xiyouji-version-bump` 技能完成：dukou-engine footer → CHANGELOG/交接文档/file-index → bump_version.py → 版本行修复（规模描述补回）→ verify_delivery → commit/push。**不要在本流程内重复做六文档同步。**

### 第 9 步：commit 排除并行会话改动

```bash
cd /d/1/xiyouji && git status --short                       # 看清改动 + untracked
cd /d/1/xiyouji && git add -u                                # 只暂存 tracked 修改
cd /d/1/xiyouji && git restore --staged <并行会话文件>        # 排除并行 session 改动（第 0 步清单）
cd /d/1/xiyouji && git status --short | grep '^??'           # 确认 _ 前缀脚本/截图未入暂存
```

- `_` 前缀探针/验证脚本按「工具不入库」约定**永不提交**。
- commit message 范式：`feat(w4xx): Phase E<n> <主题> — <一句话落地>`（实测：`feat(w476): Phase E0 纸感轻立体宪改 + tokens v3 — 视觉高级感升级轨启动`）。

## 陷阱清单

- **方案写完 ≠ 授权执行**：写方案后的「确认三问」只是决策确认，不是开工许可；执行前必须单独问「是否开始执行」。这是用户明确纠正过的纪律。
- **多 session 并发**：启动必重验 HEAD 与工作区，勿信快照；发现并行 session 文件先读 diff 判归属再决定是否排除。
- **预算上限**：tokens ≤ +2KB / system ≤ +6KB / 单页 ≤ 33KB，wc -c bytes 口径实测，超预算先砍微交互工具类而非色彩令牌。
- **reveal-in 必须 fail-open**：隐藏态只允许出现在 `.js-reveal` 祖先作用域内，禁止裸 opacity:0 规则——JS 不跑就整页内容不可见。
- **根页无需传播**：inline_css.py 只处理含 `../tokens.css` 链接的 data/en 页；根页同目录链接自动跟随，不要画蛇添足。
- **_ 前缀脚本不入库**：一次性诊断/验证脚本不 commit、不入门禁、不进 CI；提交时确认未被 git add。
- **并行 session 文件排除**：commit 前必须 git restore --staged 第 0 步记录的排除清单，否则污染他人批次。
- **图表数据色豁免**：token 覆盖率验收 = UI 选择器必须走令牌、图表数据色（D3 fill/stroke/渐变止点）登记豁免，不搞一刀切清零（实测裸色 1.6 万处，一刀切不可操作）。
- **transition 正则误判**：扫裸秒值时 `.15s` 会被截成 `15s` 误报超长动效（E0 实测教训），命中可疑值先人工复核再下结论。
- **内联 script 触发 CSP 重算**：新增任何内联 `<script>`（滚动显现/抽屉/夜读切换）必须先重跑 generate_csp.py 再 --check，否则 CSP 漂移；暗色批的防 FOUC/toggle/reveal 三处脚本一起算（详见第 2c 步）。
- **duration 正则误截**：裸秒值映射（0.2s/0.15s→var(--dur-*)）必须带负向后视 `(?<![\d.])` + 负向前视 `(?![\d])`，否则 `1.2s` 被截成 `1var(--dur-base)`（E2 实测；与既有 `.15s→15s` 误报教训同源）。
- **Windows /tmp 不互通**：bash 生成的临时清单 node 读不到；页面/断言清单必须落 `scripts/output/`，node 侧用 `require('path').join(__dirname, 'output', …)` 读。
- **白名单漏色**：裸色白名单漏掉某个渐变止点色（如 `#f5ede0`）会让渐变只映射一半；dry-run 输出与源码比对必查。
- **grep 通配派生清单**：grep 通配展开需显式文件列表（`xargs`）；跨脚本复用改 Python `Path.glob` 读文本匹配（E2 教训）。
- **hover/dark 静态截图不可见**：hover 态与 dark 覆盖在浅色静态截图里不产生像素差异，M-A1 差异率必然 <1%；验收前先确认静态差异面积够（W488 实测 dashboard 首轮 0.63% 不达标）。
- **高页面像素率难达标**：页面越高（dashboard 7280px），同样改动占整页像素比例越低；需补大面积静态差异——大标题/KPI 数字朱砂、表头淡朱砂、route-strip 朱砂线、emoji→SVG 等（W488 补强后 0.63%→5.05%）。
- **数据页无 hover 选择器**：数据页多为图表元素，常无 `.card:hover` 类选择器可改；不要空找 hover 选择器，改找实际存在元素做静态强化。
- **dark 页内 vs 全局两段式**：根页先行批 dark 走页内 `<style>`（225 数据页零波及、预算零风险）；全站暗色另案全局化（tokens.css + theme-init.js + 传播 225 页），不要在本批提前全局化。

## 完成验证清单

- [ ] 第 0 步重验过 HEAD 与工作区，排除清单已记录
- [ ] 探针报告已落 plans/ 且数字齐全
- [ ] tokens/system 增量在预算内（wc -c 实测）
- [ ] reveal-in 等门禁类均为 fail-open 实现
- [ ] inline_css.py --force 已传播 ~225 页，根页未动
- [ ] _shot_check：pageerror=0（全批断言清单自 scripts/output 读）+ getComputedStyle 断言通过 + 截图已 Read 目视
- [ ] 可感知升级批：M-A1 前后对比 6/6 ≥1% + 目视清单 ≥3 处/页已落 plans/
- [ ] 暗色页内模式：五件套齐全 + CSP 重跑 + 禁 JS 回退浅色
- [ ] 批次记录表（页×规则×豁免×pageerror×状态）已落 plans/；M5 净行数已测（增/删/净，登记行豁免口径）并回填备注
- [ ] 五门禁全绿（verify_delivery 退出码 0）
- [ ] 已转交 xiyouji-version-bump 完成 bump 与六文档同步
- [ ] commit 前已 git restore --staged 排除并行会话文件；_ 前缀脚本未入暂存

详细模板（探针报告结构、预算核对表、shot_check 脚本骨架、E2/E3 分型映射、根页清单）见 `reference.md`。
