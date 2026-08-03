# 死链巡检报告（W341 死链专项）

> 生成时间：2026-08-03
> 范围：全仓库 Markdown（`.md`）+ HTML（`.html/.htm`）内部链接
> 工具：`scripts/lint_links.py`（纯标准库，站内相对路径存在性校验）
> 状态：全部完成。A+B+C 已改链/去超链（part3）；D 类 README 陈旧 Deploy 引用已修正；E/F 类经 `--exclude` 接入 CI 排除。最终全仓库 lint（--dir .，排除 32 文件）= **5178 链接 / 0 broken**。

---

## 0. 结论速览

| 指标 | 数值 |
| --- | --- |
| 全仓库扫描内部链接总数 | **5238** |
| 修复前死链（原始巡检） | **120**（项目 112 + 第三方包 8） |
| 本轮机械修复改动 | **约 26 个文件 / 93 处链接写法** |
| 第一轮修复（part1+2 机械）后剩余 | **68**（真实内容 56 + 排除 12）|
| 第二轮修复（part3：A 改链 + B/C 删链） | **55 处链接**（44 A→分回/ + 11 B/C 去超链）|
| **当前剩余死链** | **13** |
| ├─ 第三方包内部链接（排除项） | 9（`scripts/node_modules/playwright/*`） |
| ├─ 生成器模板相对路径（排除项） | 3（`site/_template.html`） |
| └─ 真实内容死链（待核对） | 1（D 类 `.github` deploy.yml，见 §2-D）|
| **CI 接入后最终（--dir . + --exclude）** | **0 broken**（5178 链接，排除 32 文件）|

> **关键发现**：项目已有 `scripts/lint_links.py`，但 `Makefile` 的 `make links` 默认只扫 `site/`，从不扫 `docs/`（真正的互链主体，占全仓库链接绝大多数）。因此历史 CI 的 `make ci` 链接校验是**「假绿」**——`docs/` 内的死链从未被校验过。本轮已手动以 `--dir .` 全仓库扫描，并建议把全仓库（排除项见 §4）纳入 CI。

---

## 1. 机械修复清单（已执行，低风险 / 确定性）

脚本：`scripts/fix_links_w341.py`（part1）、`scripts/fix_links_w341_part2.py`（part2，修复 part1 的回归 + 漏项）。

| # | 修复类别 | 说明 | 涉及文件数（约） |
| --- | --- | --- | --- |
| 1 | 章节导航截断回目名 | 9 处章节导航里被截断的回目名补全为完整回目名 | ~9 |
| 2 | `site/data` 裸 `dashboard.html` | 5 个数据页 `href="dashboard.html"` → `href="../dashboard.html"`（正则 `r'href="dashboard\.html"'`） | 5 |
| 3 | docs 跨目录主题链接 | 路径/文件名错误的跨目录专题链接修正 | 若干 |
| 4 | S2 学术投稿误引 `10-方法论沉淀` | 把裸 `](DRL真循环.md)`/`](Preflight三轨验证.md)` 等改为 `](../10-方法论沉淀/xxx.md)`，保留链接文字（正则） | 若干 |
| 5 | S2/S3 相对层级 off-by-one | 多/少一层 `../` 的相对链接层级修正；含 S3 W302 的 `../../../CHANGELOG.md`→`../../CHANGELOG.md` | 若干 |
| 6 | 归档路径 + 删除样本链接 | `CHANGELOG-ARCHIVE.md` / `file-index-archive.md` 归档路径修正；移除已删除样本链接 | 若干 |
| 7 | 占位符清理 + README 示例 | 去掉 `.trae-cn` 占位符；`scripts/README` 中用于演示的 Markdown 链接写法改为用空格分隔 `]` 与 `(` 以规避 linter 误报 | 若干 |

> 机械修复均保留链接文字与语义，仅修正目标路径。修复后复核：未引入任何新死链（链接总数 5242 → 5239 → 5238，死链 120 → 77 → 68）。part2 另修正了 part1 引入的一处回归：`href="../dashboard.html` 吞掉结尾引号 → `href="../dashboard.html" style=`。part3 再修复 A 类 44 条（改链到 `分回/`）+ B/C 类 11 条（去超链），死链 68 → **13**（均为排除项：D1 + E9 + F3）。配合 D 类 README 修正与 `--exclude` 接入 CI，最终 `make links`（--dir .）验收为 **5178 链接 / 0 broken**。

---

## 2. 剩余 56 条真实内容死链 —— 分类与处置建议

### 类别 A：`source/原文/*.txt` 引用（44 条）—— 因 W286 重组失效 ✅ 已处理（part3 改链到 分回/第0XX回.md）

W286 将 `source/原文/` 顶层文件（`原著逐回深读.txt`、`原著逐回深读二.txt`、`详解.txt`）移除，仅保留 `shendu/` 与 `分回/` 两个子目录。下列 9 个「深化专题」仍指向已不存在的顶层 `.txt`：

| 文件 | 死链数 | 目标 |
| --- | --- | --- |
| `docs/02-人物深度分析/二郎神深化专题.md` | 6 | `../../source/原文/原著逐回深读.txt` |
| `docs/02-人物深度分析/六耳猕猴深化专题.md` | 3 | `../../source/原文/原著逐回深读.txt` |
| `docs/02-人物深度分析/哪吒深化专题.md` | 3 | 2×`原著逐回深读.txt` + 1×`原著逐回深读二.txt` |
| `docs/02-人物深度分析/太上老君深化专题.md` | 5 | `../../source/原文/原著逐回深读.txt` |
| `docs/02-人物深度分析/明代历史原型对照专题.md` | 7 | 6×`原著逐回深读.txt` + 1×`详解.txt` |
| `docs/02-人物深度分析/牛魔王深化专题.md` | 4 | `../../source/原文/原著逐回深读.txt` |
| `docs/02-人物深度分析/玉帝深化专题.md` | 3 | `../../source/原文/原著逐回深读.txt` |
| `docs/02-人物深度分析/红孩儿深化专题.md` | 7 | `../../source/原文/原著逐回深读.txt` |
| `docs/02-人物深度分析/菩提祖师深化专题.md` | 6 | `../../source/原文/原著逐回深读.txt` |

**处置建议（需人工决策，二选一）：**
- **方案 A1（改链）**：将 `.txt` 引用改为指向 W286 后的新位置（`source/原文/shendu/` 或 `source/原文/分回/` 下对应文件）。需先厘清 `shendu/` 与 `分回/` 的实际文件命名与对应关系。
- **方案 A2（删链）**：这些 `.txt` 是原始素材，正文已内嵌引用内容，链接本身仅作溯源。若确认无需跳转，直接删除这些 `](...)` 引用（保留周围文字）。

### 类别 B：缺失的专题文件（9 条）—— 计划内未创建 ✅ 已处理（part3 去超链，保留显示文字）

同一文件引用了 4 个**尚未创建**的专题文档：

| 目标文件 | 死链数 | 链接文字 |
| --- | --- | --- |
| `../04-文化与历史背景/西游与三教合一明代思想史专题.md` | 3 | 三教合一明代思想史 |
| `./西游与弗洛伊德精神分析专题.md` | 2 | 弗洛伊德精神分析 |
| `./西游与荣格分析心理学专题.md` | 2 | 荣格分析心理学 |
| `./西游与拉康精神分析专题.md` | 2 | 拉康精神分析 |

**处置建议（需人工决策，二选一）：**
- **方案 B1（建文件）**：补齐这 4 个专题文档（属内容创作工作量，不在死链修复范围内）。
- **方案 B2（删链）**：暂时删除引用，待专题成文后再回填链接。

### 类别 C：缺失的专题文件（2 条）—— 计划内未创建 ✅ 已处理（part3 去超链，保留显示文字）

| 来源文件 | 行 | 目标 |
| --- | --- | --- |
| `取经神话政治学专题.md` | 7 | `权力五联对照专题.md` |
| `空间政治学专题.md` | 253 | `妖怪身份政治专题.md` |

**处置建议**：同 B1/B2（建文件 / 删链）。

### 类别 D：`.github/workflows/README.md` 陈旧引用（1 条）✅ 已处理（修正 README 删 Deploy 行）

| 来源 | 行 | 目标 |
| --- | --- | --- |
| `.github/workflows/README.md` | 11 | `deploy.yml`（实际 workflow 文件不存在或已改名） |

**处置建议**：核对 `.github/workflows/` 下真实文件名，修正 README 引用；若该 workflow 已移除则删除此引用。

> ✅ 已处理：确认实际仅 `ci.yml` / `perf.yml` / `screenshot-review.yml` / `security.yml` 四个 workflow，无 `deploy.yml`；按「暂不做部署」修正 README（删除 Deploy 表格行 + “CI 与 CD 解耦”说明，触发矩阵 / artifact / 阈值表相应去部署化）。

---

## 3. 排除项（不应计入内容死链）

### 类别 E：第三方包内部链接（9 条）—— 直接排除

`scripts/node_modules/playwright/**` 下的 9 条内部链接（README、SKILL、`vite/dashboard|recorder|traceViewer` 的 HTML 资源路径）。属 npm 包的**自带**内部引用，与本项目内容无关，且 `node_modules` 本就不应纳入校验。

### 类别 F：`site/_template.html` 模板相对路径（3 条）—— 排除 + 生成器复查

| 行 | 目标 | 说明 |
| --- | --- | --- |
| 29 | `d3.v7.min.js` | 模板源引用（注释提示可改 CDN） |
| 239 | `../index.html` | 对生成到 `site/data/` 的页面而言**正确** |
| 241 | `../dashboard.html` | 对生成到 `site/data/` 的页面而言**正确** |

**说明**：`_template.html` 是 `scripts/new_page.py` 的**生成器模板**，本身不是渲染页面；linter 以其自身所在目录（`site/`）为基准解析，产生误报。其中 `../index.html`、`../dashboard.html` 对真正生成的 `site/data/*.html` 页面是正确路径；但 `d3.v7.min.js`（及模板中的 `tokens.css`）对 `site/data/` 页面会解析到 `site/data/d3.v7.min.js`（不存在）——属生成器资源路径问题，建议：
1. 将 `_template.html` 排除出死链校验范围（它是源码/模板，不是交付页面）；
2. 另起一项复查生成器：生成的 `site/data/` 页面应以 CDN（`https://d3js.org/d3.v7.min.js`，模板第 28 行注释已提示）或正确的相对路径引用 `d3.v7.min.js` 与 `tokens.css`。

---

## 4. CI 集成建议 ✅ 已实现

让死链校验真正覆盖 `docs/`，杜绝「假绿」：

1. **扩大扫描范围**：`make links` / `make ci` 中的 `python scripts/lint_links.py` 改为全仓库扫描（`--dir .` 或显式传入需要校验的根目录）。
2. **增加排除逻辑**：已在 `lint_links.py` 增加 `--exclude` 参数（支持多值，默认排除 `node_modules`、`.workbuddy`、`_template.html`），避免第三方包与生成器模板污染结果。
3. **退出码治理**：保持现有 `broken>0 → exit 1`，使 CI 能在引入新死链时失败。
4. **增量可选**：后续可只对 PR 改动文件跑 lint，但首次需做一次全量清零（即消化本报告 §2 的 56 条）。

> ✅ 已实现：① `lint_links.py` 新增 `--exclude`（默认 `node_modules` / `.workbuddy` / `_template.html`）；② `Makefile` 的 `links` 目标改为 `python scripts/lint_links.py --dir .` 并已在 `ci` 目标调用。实测全仓库 **5178 链接 / 0 broken**（排除 32 个文件）。第 1、2、3 点均已落地，退出码沿用既有 `broken>0 → exit 1`。

---

## 5. 附录：剩余 68 条死链完整清单

> 格式：`文件:行  目标 → 解析`（解析为以仓库根为基准的绝对相对路径）

### E.1 类别 A（44 条，`source/原文/*.txt`）

```
docs/02-人物深度分析/二郎神深化专题.md:25  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/二郎神深化专题.md:35  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/二郎神深化专题.md:51  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/二郎神深化专题.md:65  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/二郎神深化专题.md:77  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/二郎神深化专题.md:89  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/六耳猕猴深化专题.md:23  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/六耳猕猴深化专题.md:47  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/六耳猕猴深化专题.md:71  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/哪吒深化专题.md:25  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/哪吒深化专题.md:57  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/哪吒深化专题.md:89  ../../source/原文/原著逐回深读二.txt
docs/02-人物深度分析/太上老君深化专题.md:23  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/太上老君深化专题.md:39  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/太上老君深化专题.md:55  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/太上老君深化专题.md:75  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/太上老君深化专题.md:87  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/明代历史原型对照专题.md:23  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/明代历史原型对照专题.md:24  ../../source/原文/详解.txt
docs/02-人物深度分析/明代历史原型对照专题.md:52  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/明代历史原型对照专题.md:68  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/明代历史原型对照专题.md:100  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/明代历史原型对照专题.md:108  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/明代历史原型对照专题.md:148  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/明代历史原型对照专题.md:156  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/明代历史原型对照专题.md:164  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/牛魔王深化专题.md:23  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/牛魔王深化专题.md:47  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/牛魔王深化专题.md:71  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/牛魔王深化专题.md:95  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/玉帝深化专题.md:22  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/玉帝深化专题.md:86  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/玉帝深化专题.md:102  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/红孩儿深化专题.md:8  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/红孩儿深化专题.md:18  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/红孩儿深化专题.md:26  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/红孩儿深化专题.md:42  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/红孩儿深化专题.md:72  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/红孩儿深化专题.md:74  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/菩提祖师深化专题.md:11  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/菩提祖师深化专题.md:23  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/菩提祖师深化专题.md:47  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/菩提祖师深化专题.md:71  ../../source/原文/原著逐回深读.txt
docs/02-人物深度分析/菩提祖师深化专题.md:97  ../../source/原文/原著逐回深读.txt
```

### E.2 类别 B（9 条，缺失专题文件）

```
docs/02-人物深度分析/明代历史原型对照专题.md:22  ../04-文化与历史背景/西游与三教合一明代思想史专题.md
docs/02-人物深度分析/明代历史原型对照专题.md:22  ./西游与弗洛伊德精神分析专题.md
docs/02-人物深度分析/明代历史原型对照专题.md:22  ./西游与荣格分析心理学专题.md
docs/02-人物深度分析/明代历史原型对照专题.md:22  ./西游与拉康精神分析专题.md
docs/02-人物深度分析/明代历史原型对照专题.md:30  ../04-文化与历史背景/西游与三教合一明代思想史专题.md
docs/02-人物深度分析/明代历史原型对照专题.md:34  ../04-文化与历史背景/西游与三教合一明代思想史专题.md
docs/02-人物深度分析/明代历史原型对照专题.md:223  ./西游与弗洛伊德精神分析专题.md
docs/02-人物深度分析/明代历史原型对照专题.md:223  ./西游与荣格分析心理学专题.md
docs/02-人物深度分析/明代历史原型对照专题.md:223  ./西游与拉康精神分析专题.md
```

### E.3 类别 C（2 条，缺失专题文件）

```
docs/03-主题与情节专题/取经神话政治学专题.md:7  权力五联对照专题.md
docs/03-主题与情节专题/空间政治学专题.md:253  妖怪身份政治专题.md
```

### E.4 类别 D（1 条）

```
.github/workflows/README.md:11  deploy.yml
```

### E.5 类别 E（9 条，第三方包，排除）

```
scripts/node_modules/playwright/README.md:316  CONTRIBUTING.md
scripts/node_modules/playwright-core/lib/tools/cli-client/skill/SKILL.md:260  .playwright-cli/page-2026-02-14T19-22-42-679Z.yml
scripts/node_modules/playwright-core/lib/vite/dashboard/index.html:21  /playwright-logo.svg
scripts/node_modules/playwright-core/lib/vite/dashboard/index.html:23  /assets/index-C_5TMfeg.js
scripts/node_modules/playwright-core/lib/vite/dashboard/index.html:24  /assets/index-BY2S1tHT.css
scripts/node_modules/playwright-core/lib/vite/recorder/index.html:21  /playwright-logo.svg
scripts/node_modules/playwright-core/lib/vite/recorder/index.html:23  /assets/index-Bq-mQf8S.js
scripts/node_modules/playwright-core/lib/vite/recorder/index.html:24  /assets/index-4ZiSSCmn.css
scripts/node_modules/playwright-core/lib/vite/traceViewer/snapshot.html:8  about:blank
```

### E.6 类别 F（3 条，生成器模板，排除）

```
site/_template.html:29  d3.v7.min.js
site/_template.html:239  ../index.html
site/_template.html:241  ../dashboard.html
```

---

## 6. 收尾状态

1. ~~**类别 A（44 条）**：已改链到 `source/原文/分回/第0XX回.md`（part3）。~~
2. ~~**类别 B + C（11 条）**：已去超链、保留显示文字（part3）。~~
3. ~~**类别 D（1 条）**：已修正 `.github/workflows/README.md`（删除不存在的 `deploy.yml` 引用 + CD 解耦说明，按「暂不做部署」去部署化）。~~
4. ~~**类别 E / F（12 条）**：已在 `lint_links.py` 加 `--exclude`（默认 `node_modules`/`.workbuddy`/`_template.html`），CI 排除。~~
5. ~~**CI**：`make links` 改为 `python scripts/lint_links.py --dir .` 并纳入 `make ci`，消除历史「假绿」。最终验收 5178 链接 / 0 broken。~~

> 全部死链专项已闭环：真实内容死链清零，排除项经 CI 排除，全仓库链接校验通过。后续若新增文档，CI 会自动拦截新引入的死链。
