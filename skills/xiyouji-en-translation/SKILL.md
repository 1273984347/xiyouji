---
name: xiyouji-en-translation
description: 西游记项目（D:\1\xiyouji）英文站可视化页英文化标准流程 playbook。覆盖单页与并行 subagent 拆页两种模式：extract_strings.py 穷举中文串 → 按 EN 模板重建导航/页脚 → 翻译 chrome/script 字面量 → validate_en.py 逐页校验（chrome=whitelist-only·script=0）→ generate_csp.py 重建 CSP → sitemap 补录 → 六文档同步（复用 xiyouji-version-bump）。含角色名对照表、EN 模板、并行编排方式与陷阱清单。当用户要求"英文站续译"、"英文化"、"拆页翻译"、"EN 页翻译"、"翻译可视化页"、"site/en 补页"、"batch 翻译"时触发。
version: 1.0.0
---

# 西游记项目英文站英文化流程

给 xiyouji 项目（`D:\1\xiyouji`）的 `site/data/*.html` 可视化页做英文化（输出到 `site/en/*.html`）。已有 W428-W445 全量英化 + W446 旧页清理的实战验证，可单页做、也可并行 subagent 拆页做。

## 何时触发

触发（正向）：

- 用户要求"英文站续译"、"英文化"、"翻译这个页面"、"EN 版"。
- 新增了 site/data 页需要同步英文版。
- 站点做多语言扩展（复用本流程做新语言站）。

排除（反向）：

- 只改英文页的普通文字润色（不走全流程，直接改 + validate_en.py）。
- 版本 bump / 六文档同步（那是 `xiyouji-version-bump` 的活，本流程只引用它收尾）。

## 前置条件

- 项目在 `D:\1\xiyouji`，git 分支 `main`。
- 工具链（已转正，见 scripts/README.md）：
  - `scripts/extract_strings.py <name>` —— 穷举 chrome 文本节点 + script CJK 字面量。
  - `scripts/validate_en.py <path>` —— EN 页门禁（chrome CJK 白名单 + script CJK=0）。
  - `scripts/generate_csp.py` —— 全站 CSP 重建（改脚本后必跑）+ `--check` 零漂移。
  - `scripts/lint_links.py` —— 死链巡检。
  - `scripts/verify_delivery.py` —— 交付总闸。

## 第一步：穷举中文串（必做）

```bash
cd /d/1/xiyouji && python scripts/extract_strings.py <name>
```

输出分两段：`CHROME`（HTML 文本节点）与 `SCRIPT`（JS 字符串字面量）。这决定工作量（script CJK 数量越大越脆）。**没穷举就动手，容易漏翻 script 字面量导致 validate_en.py 反复报错。**

## 第二步：复制并翻译

用 Python 脚本从 `site/data/<name>.html` 复制到 `site/en/<name>.html`，再做这些变换（顺序重要，长串先于短串、整体模板先于散词替换）：

1. `<html lang="zh-CN">` → `<html lang="en">`
2. `<title>` 翻译，`· 详解西游记` → `· Annotated Journey to the West`
3. `<noscript>` 中文 → `This page requires JavaScript to render its charts.`
4. `跳到主要内容` → `Skip to main content`
5. 重建 header（见下方模板）
6. 翻译 hero（breadcrumb / kicker / h1 / subtitle / tagline）
7. 翻译全部 main 区 chrome
8. 翻译全部 script 字面量（含 console 消息、tooltip、空态、图例、数据标签）
9. 重建 footer（见下方模板）

### EN header 模板

```html
<header class="topnav">
    <a class="brand" href="index.html">
        <span class="seal">JTTW<br>Notes</span>
        <span class="wordmark">Annotated Journey to the West</span>
    </a>
    <nav aria-label="Main">
        <a href="index.html">EN Home</a>
        <a href="dashboard.html">Dashboard</a>
        <a href="visualizations.html">Visualizations</a>
        <a href="../data/<name>.html" lang="zh-CN">中文</a>
    </nav>
</header>
```

### EN footer 模板

```html
<footer class="site-footer">
    <div>
        <div class="footer-brand">Annotated Journey to the West</div>
        <div class="footer-meta">vX.Y.Z · W### · Data Visualization</div>
    </div>
    <nav aria-label="Footer">
        <a href="index.html">EN Home</a>
        <a href="dashboard.html">Dashboard</a>
        <a href="visualizations.html">Visualizations</a>
        <a href="../data/<name>.html" lang="zh-CN">中文</a>
    </nav>
</footer>
```

> 版本行 `vX.Y.Z · W###` 为占位符，按当前实际版本替换（勿照抄历史模板值，如 v2.2.86 · W334）。

> 若原 footer-meta 有随笔链接（`<a href="../../docs/.../中文.md">中文标题</a>`），**href 保留中文路径**，只翻译可见文字并追加 `(essay, Chinese)`。

### 工具页（无 topnav/footer）

有些页是工具页（header 是 `<header class="top">` 只有 h1+p，无 footer），如 data-explorer、search、81-hardships-view、graph-explorer、character-relationship-3d-view。这类页**不套 topnav/footer 模板**，只就地翻译 header 文字 + 全站 UI 字面量（`导出 CSV`→`Export CSV`、`没有可导出的数据`→`No data to export` 等）。

## 第三步：逐页校验（硬门禁）

```bash
cd /d/1/xiyouji && python scripts/validate_en.py site/en/<name>.html
```

必须输出 `OK  chrome=whitelist-only  script=0  (<name>.html)`。有违规就修到全过。违规两类：

- `SCRIPT CJK`：script 里漏翻的中文字面量（含 console 消息）。
- `CHROME CJK`：chrome 里非白名单中文。

白名单（可保留的独立中文）：`西游`、`详解`、`详解西游记`、`中文`（回链）、`· 详解西游记`（title 后缀）。其余全部要译掉或去掉。

## 第四步：CSP + 死链 + sitemap

单页或多页完成后统一做：

```bash
cd /d/1/xiyouji
python scripts/generate_csp.py        # 重建 CSP（改了 script 才需要，chrome-only 改无需）
python scripts/generate_csp.py --check  # 必须 0 漂移
python scripts/lint_links.py           # 必须 0 broken
```

sitemap：`site/sitemap.xml` 按字母序补 `<url>` 条目，并把头部注释的页面计数 +N。用脚本锚点插入（插入到 `en/xxx.html` 的前一个字母序条目之前）比手改可靠。

## 第五步：六文档同步

复用 `xiyouji-version-bump` skill 收尾（版本号推进 + 六文档 + commit/push）。**英文站补页属于内容新增，也走同样的 W 批次流程。**

## 并行 subagent 拆页编排

多页批量翻译时用并行 subagent（每 agent 1 页，统一下发 EN 模板 + 角色名对照表 + 校验命令）：

1. 先 `extract_strings.py` 逐页量出 script CJK 数，按从小到大分批（每批 3-5 页）。
2. 给每个 agent 下发改页专属 prompt：任务页名 + EN 模板 + 角色名对照表 + 上述流程 + `validate_en.py` 必须过 + **不许跑 generate_csp / 不许动 sitemap / 不许改文档 / 不许 commit / 不留临时脚本**。
3. agent 返回后**独立复验**（不盲信 subagent）：逐页 `validate_en.py` 再跑一遍，缺文件要重派。
4. 全部通过后统一做第四、五步（CSP/sitemap/六文档只做一次，不要每个 agent 各做一遍）。

## 角色名对照表（保持一致）

孙悟空→Sun Wukong，唐僧→Tang Sanzang（历史语境可 Xuanzang），猪八戒→Zhu Bajie，沙僧→Sha Wujing，白龙马→White Dragon Horse，观音→Guanyin，如来→Tathāgata，玉帝→Jade Emperor，太上老君→Taishang Laojun，太白金星→Taibai Jinxing，二郎神→Erlang Shen，哪吒→Nezha，牛魔王→Bull Demon King，铁扇公主→Princess Iron Fan，红孩儿→Red Boy，蜘蛛精→Spider Demon，白骨精→White Bone Demon，黑熊精→Black Bear Demon，青狮精→Green Lion Demon，白象精→White Elephant Demon，大鹏金翅雕→Golden-Winged Roc，老鼠精→Rat Demon，黄风怪→Yellow Wind Demon，黄袍怪→Yellow Robe Demon，六耳猕猴→Six-Eared Macaque，金角大王→Gold Horn King，银角大王→Silver Horn King，青牛精→Green Ox Demon，九头虫→Nine-Headed Demon，蝎子精→Scorpion Demon，女儿国国王→Queen of the Womanland，镇元大仙→Great Immortal Zhenyuan，菩提祖师→Bodhi Patriarch，王母娘娘→Queen Mother of the West，嫦娥→Chang'e，阎王→King Yama，地藏王→Kṣitigarbha，泾河龙王→Dragon King of the Jing River，文殊→Mañjuśrī，普贤→Samantabhadra，弥勒→Maitreya。其他名字用通行英译并保持一致。

## 陷阱清单

- **漏翻 script 字面量**：最常见。console 消息（`[INFO] 使用嵌入数据：`）、tooltip、空态文案都在 script 里，`extract_strings.py` 会列全，必须逐条译掉。
- **改 href/path**：随笔链接、数据文件路径、`scripts/...` 路径里的中文文件名必须保留，只译可见文字。翻译全局替换时尤其小心 `现代视角解读.md`、`取经团队动力学.md` 这类路径被误伤。
- **跨链指向未译兄弟页**：相关页推荐链到 en 兄弟页时，若该兄弟页还没译，要指回 `../data/<name>.html` + `lang="zh-CN"`，否则 lint_links 报 broken。
- **agent 静默失败**：subagent 返回「Agent execution completed」却没产出文件的情况偶发。必须逐页复验文件存在 + `validate_en.py` 通过，缺了就重派。
- **临时脚本不入库**：agent 生成的 `_translate_*.py` 写到 workspace 临时目录、用完即删，不要留在 `scripts/`（W447 已归档治理，别再制造新的一次性脚本）。
- **版本行 em-dash**：六文档同步时版本行锚点里 `W### 描述 — 收官` 的 `—` 是 em-dash，grep/replace 时别用 `（` 或 `-` 匹配，否则锚点失配（W446 踩过）。
- **`bump_version.py --desc` 吞规模描述**：见 `xiyouji-version-bump` skill 陷阱清单，收尾时别忘补回 `共 N 篇` 那段（值以 README 版本行/verify 输出为准，当前 N=615）。

## 完成验证清单

- [ ] `validate_en.py` 逐页 `OK  chrome=whitelist-only  script=0`
- [ ] `generate_csp.py --check` 0 漂移
- [ ] `lint_links.py` 0 broken
- [ ] sitemap 已补录、计数正确
- [ ] 六文档已同步（复用 xiyouji-version-bump）
- [ ] `verify_delivery.py` 核心全绿
- [ ] 无临时脚本残留、工作区干净
- [ ] commit/push 到 origin main
