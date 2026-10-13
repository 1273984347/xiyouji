# 前端性能与部署正确性优化计划（方案 A/B/C）

> 创建：2026-09-08。本文档自包含：全部背景、现象、代码定位、执行步骤、验收标准内嵌于正文，全部基线数字为 2026-09-08 在本仓库 HEAD `f3d7d5d` 工作树实测并附复现命令，执行者无需回溯本次会话即可独立执行。
>
> 批号说明：本计划文档随下一个文档批次入库（可单独立批，也可与方案 A 同批）。三个方案的执行批号执行时按「CHANGELOG 现役段 max+1」重新领取；文中「建议批号 W563/W564/W565」仅为预设，以实际领取为准。新写的一次性脚本一律不带 W 号（用 `_fix_d3_position.py` 等功能名），防止批号漂移后名实不符。
>
> 背景压缩（30 秒版）：2026-09-08 对 site/ 做了一次前端视角量化体检，确认四类问题——① 154 页在 `<head>` 内同步加载 280KB 的 d3.v7.min.js（解析阻塞，perf.yml 自记 LCP 实测 4.73–4.87s、预算已放宽到 5000ms「性能债登记」）；② `site/sw.js` 预缓存了一个全站 0 页面引用的 3.5MB 字体，且静态资源 cache-first 配手工版本号、无 bump 机制（陈旧缓存风险）；③ 37 个页面在 JS 里 fetch `../../scripts/output/data/*.json`——部署根是 `site/`，这些请求在 GitHub Pages 部署态全部 404，其中 chapter-stats 两页（中/英）连 EMBEDDED 回退都没有、直接落到 mock 数据（生产环境展示假数据）；④ 字体未按站点实际字符集子集化（正文仅 2181 个不同字符，却带 754KB+765KB 的中文字体）。
>
> 复审修订（2026-09-08 当日对抗性复审）：取证推翻/细化了初稿三处设计并新增一项存量缺陷发现——A-1 扩为 d3.v7 + d3-sankey 双标签链式移动（F19，初稿只移 d3.v7 会让 24 页炸）、A-3 的 γ 类拆为 γ-1/γ-2 并确认 character-appearance 两页从来没有任何数据源（F20）、B 方案新增 B-0 字体路径正常化（F18：225 个子页面自定义字体从未加载过）；B-1 字符集口径改为不剥离 script/style。标注「（复审补充/新增）」的条目均为本轮产出。
>
> **用户裁决（2026-09-08）**：① A-3 决策点 D1 采用根治方案——副本对账并入第 9 门禁 `check_data_drift.js`（门禁扩展已获确认，不再是「待裁决」）；② B-0（字体路径正常化）提前，与方案 A 同批最先执行。执行批次据此划分：建议 W563 = A-1…A-4 + B-0，建议 W564 = B-1 + B-2，建议 W565 = C（批号仍以领取为准）。

> 生成来源：人工撰写
> 生成模型：GLM-5.3-Flash
> 生成日期：2026-09-08
> 核验状态：未核验

---

## 〇、全局事实基线（执行前无需重测；执行后用于对账）

以下数字全部可由右列命令在仓库根目录复现（Git Bash）。「现状值」即验收时要变成的目标值的对照组。

| # | 事实 | 现状值 | 复现方式 |
|---|------|--------|---------|
| F1 | site/ HTML 总数 | 234 | `find site -name '*.html' \| wc -l` |
| F2 | d3 同步加载于 `<head>` 内的页 | 154（data/ 77 + en/ 76 + site/_template.html 1） | 末尾注①脚本 |
| F3 | d3 同步加载于 body 内的页（合规，不动） | 2（site/dashboard.html + en/ 下 1 页） | 同上 |
| F4 | d3 带 defer 的页（合规，不动） | 5（data/ 3 + en/ 2） | 同上 |
| F5 | 154 页的 d3 标签字面量 | 完全一致，均为 `<script src="../static/js/d3.v7.min.js">`（en 页同为此字面量，`../static/` 从 site/en/ 解析即 site/static/） | `grep -c '<script src="\.\./static/js/d3\.v7\.min\.js">' site/data/*.html site/en/*.html` |
| F6 | 154 页中 head 内存在内联 `<script>`（无 src）的页 | 0 —— 移位变换零风险的根据 | 末尾注①脚本 |
| F7 | 154 页中用 DOMContentLoaded 包裹初始化的页 | 仅 22 —— **直接加 defer 不安全**的证据：defer 脚本在解析完成后才执行，其余 132 页 body 末尾的内联脚本执行时 d3 尚未定义，会整页报 `d3 is not defined` | `grep -l DOMContentLoaded site/data/*.html site/en/*.html \| wc -l` |
| F8 | JS 字符串字面量指向 `../..\/scripts/output/data/`（越界 fetch）的页 | 37（data/ 19 + en/ 17 + site/dashboard.html 1）；去重目标 JSON 共 49 个、磁盘总体积 345KB | 末尾注②脚本 |
| F9 | 目标 JSON 在 `scripts/output/data/` 缺失的 | 2 个：`geo_semiotics.json`、`character_appearance.json`（波及 4 页：data/en 两对）——这些页的 fetch 在任何模式下都 404 | 同上 |
| F10 | chapter-stats 两页（data/en）无 EMBEDDED、mock 回退 | data 版 1693–1706 行 try/catch 落 mock；en 版 1270 行 `fallback mock 数据（10 回示例）` | `grep -n 'mock' site/data/chapter-stats.html site/en/chapter-stats.html` |
| F11 | relationships 页双源 | HTML 413KB，其中 `const EMBEDDED = {...}` 281.8KB（6 组数据）；`baseUrl = '../../scripts/output/data/'`（5422 行）+ 6 次 loadJson fetch | `grep -n 'baseUrl\|loadJson(' site/data/relationships.html` |
| F12 | sw.js SHELL 清单 14 项 | 全部存在于磁盘；其中 `NotoSerifSC-VF.woff2` 3551KB 全站 0 页面引用（唯一引用方是 sw.js 自身），实际 @font-face 用的是 `noto-serif-sc-shared.woff2` 414KB | `grep -rl 'NotoSerifSC-VF' site/`（应只剩 site/sw.js） |
| F13 | 字体映射（site/tokens.css 内联进各页） | `'Noto Serif SC'` ← noto-serif-sc-shared.woff2（414KB，display:optional）；`'Noto Sans SC'` 400 ← NotoSansSC-Regular.woff2（754KB，optional）；`'Noto Sans SC'` 500 ← NotoSansSC-Medium.woff2（765KB，optional）；JetBrains Mono 400/500 ← 29/30KB（swap） | `grep -n "url(\|font-family\|font-display" site/tokens.css` |
| F14 | 站点正文不同字符数 | 2181（其中 CJK 2003）——全部 HTML 去除 script/style/注释后取并集 | 末尾注③脚本 |
| F15 | Lighthouse 现行预算（perf.yml） | 非 3D 页：LCP error 5000ms / CLS 0.3 / TBT 300ms / FCP warn 4800ms；3D 页（character-relationship-3d）：LCP 12000 / TBT 900。受测 URL 固定 5 个：dashboard、index、data/timeline、data/character-relationship-3d、data/text-search，各 3 runs | `.github/workflows/perf.yml` |
| F16 | INLINED 状态 | 226 页已内联 tokens（inline_css.py 输出 skip-inlined 226 / skip-no-link 8） | `python scripts/inline_css.py`（只读跑一次看计数） |
| F17 | agent-web 误入库的编译产物 | `xiyouji-agent-web/vite.config.js`、`vite.config.d.ts`（`tsc -b` 生成物，git tracked） | `git ls-files xiyouji-agent-web \| grep vite.config` |
| F18 | **（复审补充）内联页 @font-face 路径缺陷** | 226 个含 INLINED 标记的页中，**225 页**的内联 @font-face url 为 `url('static/fonts/…')` 且全部位于 data/ 或 en/——CSS 内联块的相对 url 以**文档**为基解析，解析到 `site/data/static/`、`site/en/static/`（均不存在，已验证无 `<base>` 标签、`site/data/static` 不存在）→ **这两级全部子页面的自定义字体从未加载过**，一直渲染系统回退字体；另 1 个 INLINED 页不含 @font-face，8 个无内联标记的页与本缺陷无关 | 末尾注④脚本（现值 `url正确=0 url错误=225 无font-face=1`） |
| F19 | **（复审补充）d3-sankey 链式依赖** | 154 页中 24 页在 head 内、且在 d3.v7 之后还同步加载 `d3-sankey.min.js`（24/24 均位于 d3.v7 之后，已验证顺序）；d3-sankey 依赖 d3 全局——A-1 若只移 d3.v7，sankey 会先于 d3 执行而炸 | 末尾注⑤脚本 |
| F20 | **（复审补充）γ 类拆分依据** | 目标 JSON 缺失的 4 页中：journey-geo-semiotics data/en 两页**有** `const EMBEDDED`（可安全删 fetch）；character-appearance data/en 两页**没有 EMBEDDED**、且仓库内无其生成器（`grep -rln character_appearance scripts/*.py` 仅 data_validate.py 校验器提及）→ 这两页在 file:// 与部署态**从来没有任何数据源**，属存量内容缺陷 | `grep -c 'const EMBEDDED' <4 页路径>` |

注①（F2/F3/F4/F6 判定脚本，一次粘贴执行）：

```bash
python -c "
import re, glob
c = {}
for p in glob.glob('site/**/*.html', recursive=True):
    s = open(p, encoding='utf-8', errors='ignore').read()
    m = re.search(r'<script[^>]*src=\"[^\"]*d3\.v7[^\"]*\"[^>]*>', s)
    if not m: k = 'NO_D3'
    elif 'defer' in m.group(0): k = 'DEFER'
    elif 0 <= s.find('</head>') and m.start() < s.find('</head>'): k = 'SYNC_HEAD'
    else: k = 'SYNC_BODY'
    c[k] = c.get(k, 0) + 1
    if k == 'SYNC_HEAD':
        head = s[:s.find('</head>')]
        assert not re.search(r'<script(?![^>]*src=)[^>]*>', head), p
print(c)
"
```

注②（F8/F9 判定脚本）：

```bash
python -c "
import re, glob, os
files = set()
for p in glob.glob('site/**/*.html', recursive=True):
    s = open(p, encoding='utf-8', errors='ignore').read()
    files |= set(re.findall(r\"['\\\"](?:\.\./)+scripts/output/data/([\w.-]+)['\\\"]\", s))
print(len(files), sorted(f for f in files if not os.path.exists('scripts/output/data/'+f)))
"
```

注③（F14 判定脚本）：

```bash
python -c "
import re, glob
chars = set()
for p in glob.glob('site/**/*.html', recursive=True):
    s = open(p, encoding='utf-8', errors='ignore').read()
    chars |= set(re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', '', s, flags=re.S))
print(len(chars))
"
```

注④（F18 判定脚本；「正确」指 url 前缀与页面层级匹配——data/ 与 en/ 页须 `../static/`，根页须 `static/`）：

```bash
python -c "
import re, glob
ok = bad = norule = 0; badl = []
for p in glob.glob('site/**/*.html', recursive=True):
    s = open(p, encoding='utf-8', errors='ignore').read()
    if 'INLINED CSS' not in s: continue
    urls = re.findall(r\"@font-face[^}]*?url\('([^']*woff2)'\)\", s, re.S)
    if not urls: norule += 1; continue
    lvl = '../' if '/data/' in p.replace(chr(92), '/') or '/en/' in p.replace(chr(92), '/') else ''
    if all(u.startswith(lvl + 'static/fonts/') for u in urls): ok += 1
    else: bad += 1; badl.append(p)
print(f'url正确={ok} url错误={bad} 无font-face={norule}'); print(badl[:3])
"
```

注⑤（F19 判定脚本）：

```bash
python -c "
import glob
after = before = 0
for p in glob.glob('site/**/*.html', recursive=True):
    s = open(p, encoding='utf-8', errors='ignore').read()
    if 'd3-sankey' not in s: continue
    if s.find('d3-sankey.min.js') > s.find('d3.v7.min.js'): after += 1
    else: before += 1; print('BEFORE:', p)
print(f'sankey在d3之后={after} 之前={before}')
"
```

---

## 方案 A（建议批号 W563）：关键路径与部署正确性快赢包

| 项 | 值 |
|---|---|
| 优先级 | 高（三方案中唯一建议近期执行；A-1 是全项目性价比最高单项；**B-0 已获用户确认并入本批最先执行**） |
| 前置依赖 | 无 |
| 预计改动 | A-1 154 个 HTML；A-2 3 个文件（sw.js、pages.yml、1 个 git mv）；A-3 37 个 HTML + 新增 `site/data/json/` 47 个 JSON + `scripts/check_data_drift.js` 扩展（D1-a）；A-4 2 个 git rm --cached + 1 个 .gitignore；**B-0 `scripts/inline_css.py` 路径重写 + 225 个 HTML 重新内联** |
| 预计工作量 | 5.5–7 小时（含 B-0 约 1 小时；若嫌单批过大，拆批建议：A-1+A-2+B-0 一批，A-3+A-4 一批） |
| 涉及工具 | Python（批量变换脚本）、inline_css.py --force（B-0）、`node scripts/check_screenshot_gates.js`（回归）、`node scripts/check_data_drift.js`（D1-a 扩展与回归）、`generate_csp.py`、`verify_delivery.py`、batch_cascade.py（登记） |

### A-1 D3 加载位置治理（154 页）

- **现象**：F2——154 页在 `<head>` 内同步加载 280KB 的 d3.v7.min.js，解析器在 D3 下载+执行完成前不处理后续任何内容，LCP 被整体推迟。perf.yml 已把 LCP 预算放宽到 5000ms 登记性能债（F15）。
- **为什么不是加 defer**：F7——defer 脚本在 HTML 解析完成后才执行，而 154 页中 132 页的图表初始化内联脚本没有 DOMContentLoaded 包裹、在解析途中即执行，defer 化后执行时 d3 未定义，全站图表会白屏（G1 pageerror 门禁会大面积变红）。因此采用**移位**方案：语义零变更、不依赖任何页面的初始化写法。
- **执行步骤**：
  1. 写一次性脚本 `scripts/_fix_d3_position.py`，对 F2 判定出的 154 页逐页做字符串变换（用 Write 工具落盘脚本文件，禁 heredoc）。**移动集合是两个标签而不仅是 d3.v7**（F19：24 页 head 内还有依赖 d3 全局的 d3-sankey，24/24 位于 d3.v7 之后，必须与之保持相对顺序一起移动，否则 sankey 先执行即炸）：
     a. 在 head 内删除整行 `<script src="../static/js/d3.v7.min.js"></script>`；若该页 head 内存在 `<script src="../static/js/d3-sankey.min.js"></script>`（24 页），一并删除（连同行首缩进；两字面量全站完全一致）；
     b. 在首个被删标签的原位置插入对应 preload 行（129 页 1 行、24 页 2 行，顺序 d3.v7 在前）：
        `<link rel="preload" href="../static/js/d3.v7.min.js" as="script" />` 与 `<link rel="preload" href="../static/js/d3-sankey.min.js" as="script" />`；
     c. 把删除的 `<script>` 标签按原相对顺序（d3.v7 → sankey）插入到 `<body>` 之后**第一个内联 `<script>` 开标签之前**（即：找到 `s.find('<body')` 之后第一个匹配 `<script` 且该开标签不含 `src=` 的位置，把标签插到它前面，保留原缩进风格）。若某页找不到这样的内联脚本位置（与 F6 矛盾），该页跳过并打印，**不得盲插**，留人工清单。
  2. 明确不动：F3 两页（已在 body）、F4 五页（已有 defer）、`site/data/_shell.html`（无 d3）；154 页中 1 页 head 内另有 `three.r128.min.js`（无 d3 依赖，**留在 head 不动**）；24 页之外的其余 sankey 引用（若存在）不受影响。
  3. 落盘后 `git diff --stat` 核对：改动 HTML 文件数 == 154。
- **验收（全部满足才算完成）**：
  1. 注①脚本重跑：`SYNC_HEAD: 0`，`SYNC_BODY: 156`，`DEFER: 5`（数量不变即未误伤）；注⑤脚本重跑：`sankey在d3之后=24 之前=0` 且全部 24 个 sankey 标签已不在 head 内（配合注① SYNC_HEAD:0 即覆盖）；
  2. 129 页 head 内恰 1 条 d3 preload、24 页恰 2 条（d3.v7 与 d3-sankey 各一），由变换脚本断言；
  3. `node scripts/check_screenshot_gates.js` 全站 FAIL 0（G1 pageerror 抓 `d3 is not defined` 类回归；含 reveal-in 页面的滚动穿透由该脚本内置处理）；
  4. `python scripts/generate_csp.py --check` 0 漂移（外部脚本不参与哈希，理论上无漂移；按铁律仍必跑）；
  5. `python scripts/verify_delivery.py` 核心全绿；
  6. push 后 perf.yml 自动触发（paths 含 site/**），5 个受测 URL 的 LCP 全部 ≤ 变更前同 URL 数值，实测数字照抄进 CHANGELOG（W496 铁律：先测后写）。
- **明确非目标**：不改任何内联初始化代码；不引入 ES module 改造；不动 3D 页的 Three.js 加载方式。

### A-2 Service Worker 治理（site/sw.js + pages.yml）

- **现象**：F12——sw.js 第 28 行把 `NotoSerifSC-VF.woff2`（3551KB）列入 install 预缓存，但该字体全站 0 页面引用（@font-face 实际用的是 414KB 的 shared 子集），等于每个开启 PWA 的访客首访后台白下 3.5MB，仓库与 Pages 部署也各背一份死重。另外 sw.js 静态资源分支是 cache-first、缓存名 `xiyouji-shell-v1` 手工维护无 bump 机制——HTML 是 network-first 会更新，但它引用的外链 JS（rag-chat.js / vis-tools.js）老访客可能永久拿旧缓存。
- **执行步骤**：
  1. `mkdir -p` 不需要（目录已存在）：`git mv site/static/fonts/NotoSerifSC-VF.woff2 assets/fonts/source/NotoSerifSC-VF.woff2`（归档到字体源目录，与 NotoSansSC 源文件同级，保留将来子集化能力；不物理删除）。
  2. `site/sw.js` 三处修改：
     a. SHELL 数组删除行 `"./static/fonts/NotoSerifSC-VF.woff2",`；
     b. 缓存名改 `const CACHE = "xiyouji-shell-v2";`（本地占位；线上实际版本由下一步的部署期覆写保证）；
     c. 静态资源分支由 cache-first 改为 stale-while-revalidate——`if (isStatic(req))` 分支整段替换为：
     ```js
     if (isStatic(req)) {
       e.respondWith(
         caches.match(req).then(function (hit) {
           var fetched = fetch(req).then(function (res) {
             var copy = res.clone();
             caches.open(CACHE).then(function (c) { c.put(req, copy); });
             return res;
           });
           fetched.catch(function () { /* 后台刷新失败静默（离线时命中缓存无感） */ });
           return hit || fetched;
         })
       );
       return;
     }
     ```
     （命中缓存立即返回、同时后台刷新；后台刷新单独挂 no-op catch 防未处理的 promise 拒绝告警，缓存未命中且网络失败时仍按原样向浏览器传播错误；导航与 API 分支维持原状；文件头注释的「策略」段同步改一行说明。）
  3. `.github/workflows/pages.yml` 的 `Build & Upload` job 内、Checkout 与 Upload artifact 两步之间插入：
     ```yaml
     - name: Stamp SW cache version with commit SHA
       run: |
         sed -i "s/const CACHE = \"xiyouji-shell-[^\"]*\"/const CACHE = \"xiyouji-shell-${GITHUB_SHA::7}\"/" site/sw.js
         grep -q "xiyouji-shell-${GITHUB_SHA::7}" site/sw.js
     ```
     （sed 只作用于 CI 工作副本，随 artifact 上传，不污染仓库；行尾 grep 是步内断言，替换失败即红灯。每次部署 SHA 变化 → 缓存名变化 → activate 分支自动清理旧缓存，SHELL 变更必然生效。）
- **验收**：
  1. `grep -c 'NotoSerifSC-VF' site/sw.js` == 0，且 `grep -rl 'NotoSerifSC-VF' site/` 输出为空；
  2. `git ls-files | grep NotoSerifSC-VF` == `assets/fonts/source/NotoSerifSC-VF.woff2`；`ls site/static/fonts/NotoSerifSC-VF.woff2` 报不存在；
  3. `node --check site/sw.js` 通过；
  4. SHELL 其余条目存在性断言（`./` 为根目录不需断言，12 个文件）：`python -c "import os;shell=['./index.html','./mobile-index.html','./manifest.webmanifest','./tokens.css','./system.css','./static/js/vis-tools.js','./static/js/rag-chat.js','./static/fonts/NotoSansSC-Regular.woff2','./static/fonts/NotoSansSC-Medium.woff2','./static/images/ink-mountains-hero.webp','./static/icons/icon-192.png','./static/icons/icon-512.png'];assert all(os.path.exists('site/'+s[2:]) for s in shell), [s for s in shell if not os.path.exists('site/'+s[2:])];print('12/12 OK')"`；
  5. push 后 `gh run list --workflow pages.yml` 绿；部署完成后人工执行一次 `curl -s https://1273984347.github.io/xiyouji/sw.js | grep 'const CACHE'`，输出应含当前 HEAD 短哈希（此步写进 CHANGELOG「验证」栏作为凭证）。
- **回滚**：`git checkout -- site/sw.js .github/workflows/pages.yml && git mv assets/fonts/source/NotoSerifSC-VF.woff2 site/static/fonts/`。
- **明确非目标**：不做 PWA 离线页面级策略改造；不动 manifest.webmanifest；不为 file:// 做任何事（sw.js 本就不注册于 file://）。

### A-3 越界 fetch 治理（37 页 / 49 个目标 JSON）

- **现象**：F8/F9/F10/F20——37 个页面的 JS 以字符串字面量 fetch `../../scripts/output/data/*.json`（dashboard.html 为 `../scripts/...`），部署根是 site/，这些请求在生产环境全部 404，页面全靠 EMBEDDED 回退渲染；其中 chapter-stats 两页没有 EMBEDDED，生产环境展示的是 mock 假数据。目标 JSON 缺失的 4 页分两态（F20）：journey-geo-semiotics 两页有 EMBEDDED（可删 fetch）；character-appearance 两页无任何数据源（存量内容缺陷，本方案仅做字面量清理并登记）。
- **执行步骤**：
  1. 写一次性脚本 `scripts/_fix_oob_fetch.py`，按页内字面量自动分派**四类**改法：
     - **α 类（目标 JSON 在磁盘存在，31 页）**：把页面内前缀字面量整体替换——site/data/*.html：`../../scripts/output/data/` → `json/`；site/en/*.html：`../../scripts/output/data/` → `../data/json/`；site/dashboard.html：`../scripts/output/data/` → `./data/json/`。同时把该页引用的全部 JSON 复制到 `site/data/json/`（`cp` 保留字节一致，验收用 sha256 对账）。
     - **β 类（chapter-stats data/en 两页，无 EMBEDDED、目标 JSON 存在且仅 237B）**：把其内容内联为页内 `const EMBEDDED_DATA = {...}`，loader 改为直接使用 EMBEDDED（仿 site/en/81-hardships.html 1689 行 `return EMBEDDED_DATA;` 的 W554 先例），删除越界 fetch；`dataSource` 文案同步改写（去掉 `实时加载自 .../chapter_stats.json（http server 模式）` 字样，en 版同）。此两页改完必须满足门禁口径「EMBEDDED 含完整数据」。
     - **γ-1 类（journey-geo-semiotics data/en 两页：目标 JSON 磁盘缺失，但有 EMBEDDED，F20）**：断言 `const EMBEDDED` 存在（已预验证 = 1），然后删除该 fetch 调用、直接以 EMBEDDED 渲染（同 β 类模式）。
     - **γ-2 类（character-appearance data/en 两页：目标 JSON 磁盘缺失、无 EMBEDDED、仓库无生成器，F20）**：这两页在 file:// 与部署态**从来没有过任何数据源**（fetch 恒 404 → catch 空态），属**存量内容缺陷，不在本方案修复范围**。本方案内仅做的处置：同样删除该 fetch 调用与越界字面量（行为与现状生产态等价——都是走空态分支——但 console 不再产生死请求，注②全局清零口径得以成立），并在 CHANGELOG 单独登记该缺陷（后续由内容批次决定：新写生成器补数据，或评估页面去留）。**禁止**在缺乏数据源的情况下伪造数据。
  2. 落盘后 `git status` 核对：37 个 HTML 修改 + `site/data/json/` 下 47 个新 JSON（49 减 2 个缺失）。
  3. 写对账脚本 `scripts/_check_json_copies.py`：对 47 个副本逐一断言 `sha256(scripts/output/data/X) == sha256(site/data/json/X)`，输出 `47/47 OK`。
  4. **副本漂移常驻化（D1-a，经用户 2026-09-08 确认并入第 9 门禁）**：α 类生效后，部署态页面渲染的是 `site/data/json/` 副本的数据而非 EMBEDDED；现有数据漂移门禁只对账「EMBEDDED ↔ scripts/output」，不覆盖副本。本步扩展 `scripts/check_data_drift.js`：新增副本对账子检查——(a) 对 `site/data/json/` 下每个文件断言 `scripts/output/data/` 存在同名文件且字节相等（逐字节比较即可，不必引入 sha256 依赖）；(b) 反向断言：扫描各页改写后的 fetch 目标字面量（`json/`、`../data/json/`、`./data/json/` 前缀），每个目标文件必须存在于 `site/data/json/`（防「新增 fetch 目标但漏复制」的静默 404）。任一不满足 = 门禁 FAIL。落地要求：
     - 与 A-3 同批实施；`node scripts/check_data_drift.js` 默认参数实跑应输出原有「可比 44 页（71 个 JSON 对比项）/ 0 漂移」+ 新增副本对账段 `47/47 OK`（W537 新规④：JS 工具脚本改动推送前必须真实参数冒烟）；
     - **负样本冒烟**：临时篡改任一副本 1 字节 → 门禁必须 FAIL → `git checkout` 还原 → 复跑全绿（防「建置即绿」假门禁，W555 --self-test 同精神）；
     - 同批在 AGENTS §4.2 第 9 条与 docs/00-导读/文档规范.md §8 门禁表登记该子检查（随 batch_cascade 级联完成）。
- **验收**：
  1. 注②脚本重跑：页面命中数 37 → **0**，缺失文件列表为空；
  2. `grep -rn "scripts/output" site/data/*.html site/en/*.html site/*.html` 逐条过目：JS 字符串字面量必须为 0 处；纯描述性文案（如 relationships 页「数据来源：scripts/D_关系网络/ 生成脚本」）允许保留但逐条登记处置说明；
  3. `node scripts/check_data_drift.js` 默认跑，仍为「可比 44 页（71 个 JSON 对比项）/ 0 漂移」+ 新增副本对账段 `47/47 OK`（步骤 4 的扩展生效后此命令即覆盖两段）；负样本冒烟（篡改副本 1 字节 → FAIL → 还原 → 复跑绿）通过；
  4. `node scripts/check_screenshot_gates.js` FAIL 0；
  5. 部署态冒烟：`python -m http.server 8000 -d site` 后 `curl -sf http://127.0.0.1:8000/data/json/hardships_81.json -o /dev/null -w '%{http_code}'` 输出 200；Playwright 打开 data/chapter-stats、data/81-hardships、en/social-media 三页断言 console 无 404/失败请求（一次探针即可）；
  6. `python scripts/verify_delivery.py` 核心全绿（新增 JSON 不触发 sitemap/回退模式门禁，若有意外 FAIL 逐条裁决，不得改门禁放行）。
- **体量影响**：site/ 体积增加 ≤345KB（47 个 JSON 去重后实测），换来生产环境 0 个数据 404 + chapter-stats 两页从 mock 假数据变为真实数据。
- **回滚**：`git checkout -- <37 页>` + `git rm -r site/data/json/`，无其他耦合。
- **明确非目标**：不把「EMBEDDED 双份传输」在本项解决（归方案 C）；不给 scripts/output/data 与 site/data/json 建自动同步管道（一次性快照 + sha256 对账脚本足够，两条源各司其职：前者是生成器输出，后者是部署副本）。

### A-4 agent-web 构建产物出库

- **现象**：F17——`xiyouji-agent-web/vite.config.js` 与 `vite.config.d.ts` 是 `tsc -b` 的生成物，被误提交进仓库，与源文件 vite.config.ts 并存，后续极易出现「改了 ts 忘了 js」的双源漂移。
- **执行步骤**：`git rm --cached xiyouji-agent-web/vite.config.js xiyouji-agent-web/vite.config.d.ts`（磁盘文件保留）；在 `xiyouji-agent-web/.gitignore` 追加两行 `vite.config.js`、`vite.config.d.ts`；`cd xiyouji-agent-web && npm run build` 冒烟（W537 新规④：构建链改动推送前必须真实跑一次）——build 会重新生成这两个文件且 git status 保持干净。
- **验收**：`git ls-files xiyouji-agent-web | grep vite.config` 仅剩 `vite.config.ts`；`npm run build` 成功且 `git status --short xiyouji-agent-web` 无新增未跟踪项。
- **回滚**：`git restore --staged` 两个文件 + 还原 .gitignore。

### 方案 A 收尾（通用）

1. `python scripts/generate_csp.py && python scripts/generate_csp.py --check`（A-1/A-3/B-0 均未触碰内联**脚本**内容，预期 0 漂移；按铁律必跑）。
2. `python scripts/verify_delivery.py` 核心全绿。
3. batch_cascade 登记（desc 建议「前端关键路径与部署正确性快赢包」，file_index_rows 列：本方案文档、`_fix_d3_position.py`、`_fix_oob_fetch.py`、`_check_json_copies.py`、site/data/json/ 47 个 JSON 逐个登记或以目录说明 + sw.js + pages.yml）。
4. 提交推送后 `gh run list` 确认含 perf.yml 在内的 workflow 全绿，把 perf 实测 LCP 五个数字抄进 CHANGELOG「验证」栏（W537 新规①：以实跑输出为准）。

---

## 方案 B（建议批号 W564）：字体字节治理（子集化 + preload）

| 项 | 值 |
|---|---|
| 优先级 | 高/中拆分：**B-0 为正确性缺陷修复，经用户 2026-09-08 确认提前、与方案 A 同批最先执行**；B-1/B-2 为字节与加载优化，随方案 B 后续批次 |
| 前置依赖 | 无硬依赖（建议在 A 之后跑 LHCI 对比更干净）；B-1 依赖 B-0，B-2 依赖 B-0+B-1 |
| 预计改动 | B-0（已前移至方案 A 批执行）：scripts/inline_css.py 增加 url 深度重写 + 225 个 HTML（--force 重新内联）；B-1：site/tokens.css 3 行 url + 3 个新 .subset.woff2 + scripts/requirements.txt 1 行；B-2：226 个 HTML 的 preload 插入 |
| 预计工作量 | 2–3 小时（B-0 约 1 小时已计入方案 A 批） |
| 涉及工具 | fonttools + brotli（pip）、inline_css.py --force、generate_csp.py、LHCI（本地可跑 `npx @lhci/cli@0.13.x autorun`，或直接看 push 后 perf.yml） |

### B-0（复审新增，正确性缺陷修复）：内联 @font-face 路径正常化

- **现象**：F18——226 个 INLINED 页中 225 页的内联 @font-face url 为 `url('static/fonts/…')`，以文档为基解析后，data/ 与 en/ 两级全部子页面解析到不存在的 `…/static/` 路径 → **这些页面的自定义字体（Noto Serif SC / Noto Sans SC / JetBrains Mono）从未加载成功过**，一直渲染系统回退字体。仅根目录页与 8 个以 `<link>` 引用 tokens.css 的页路径正确（CSS 文件内相对 url 以 CSS 文件位置为基）。这是 inline_css.py 内联时未做路径深度重写的工具链缺陷。
- **执行步骤**：
  1. 修改 `scripts/inline_css.py`：内联落盘时按目标页相对 site/ 的深度重写 INLINED 块内的 `url('static/…` → `url('../static/…`（data/ 与 en/ 页一层 `../`；根页不变）。重写只作用于 INLINED 标记块内，不碰页面其余内容；tokens.css 源文件**不改**（其对 `<link>` 页与根页本就正确）。
  2. W537 新规④冒烟：先 `python scripts/inline_css.py --dry` 看计数，再对单页手工核验（data 页应出现 `../static/fonts/`，根页保持 `static/fonts/`），最后 `python scripts/inline_css.py --force` 全量重新内联 226 页。
  3. `python scripts/generate_csp.py --check`（纯 CSS url 变更，预期 0 漂移）。
- **验收**：
  1. 注④脚本重跑：`url正确=225 url错误=0 无font-face=1`（无 font-face 的那 1 页维持原状，不计入正确列）；
  2. Playwright 抽 index、data/relationships、en/relationships 三页，断言 `document.fonts` 中 `Noto Serif SC` 与 `Noto Sans SC` 两个 Face 的 status 为 loaded（**修复前基线为 unloaded——本项落地后这两族字体在子页面首次真正生效，截图字形会有可见变化，属预期修复效果**，CHANGELOG 注明，避免被误判为回归）；
  3. `python scripts/verify_delivery.py` 全绿（第 12/15 门禁复跑）。
- **回滚**：`git checkout -- scripts/inline_css.py` + 对 226 页 `git checkout` + `generate_csp.py --check`。
- **明确非目标**：不改任何页面的 font-family 栈；不动 8 个 `<link>` 页。

### B-1 按站点字符集子集化中文字体

- **现象**：F13/F14——正文实际只用到 2181 个不同字符（CJK 2003），但每个页面挂着的 @font-face 指向 754KB + 765KB + 414KB 三个未按需裁剪的中文字体文件；浏览器虽按字形懒下载，woff2 全量文件的下载仍以整个文件为单位，首屏文本字体命中即拉数百 KB。
- **执行步骤**：
  1. 环境准备：`pip install fonttools brotli`，并把 `fonttools`、`brotli` 追加进 `scripts/requirements.txt`（进 pip-audit 扫描面，两包均主流维护中）。
  2. 写 `scripts/_gen_font_charset.py`，字符集来源**精确定义**为三者并集：(a) 全部 `site/**/*.html` 的**完整原文、不做任何标签剥离**——注意与 F14 的口径差异：F14 的 2181 是「正文可见文本」口径，只用于度量；字体子集必须覆盖 JS 字符串里的 CJK（tooltip 前缀、图例文案、`第${d}回` 类模板串都在 `<script>` 内，剥离会把它们漏掉，渲染时逐字形回退系统字体）；(b) 全部 `scripts/output/data/*.json` 原文（图表标签来自这些数据）；(c) 全部 `dataset/*.json` 原文。另无条件并入 ASCII 0x20–0x7E 全段。输出到 `scripts/output/font-charset.txt`（该目录不参与部署）。
  3. 子集化三条命令（输入优先用 assets/fonts/source/ 下的源；`noto-serif-sc-shared` 若源目录无对应文件，则直接以 `site/static/fonts/noto-serif-sc-shared.woff2` 为输入，效果等同）：
     ```bash
     pyftsubset assets/fonts/source/NotoSansSC-Regular.woff2 --text-file=scripts/output/font-charset.txt --flavor=woff2 --output-file=site/static/fonts/NotoSansSC-Regular.subset.woff2 --layout-features='*' --no-hinting
     pyftsubset assets/fonts/source/NotoSansSC-Medium.woff2   --text-file=scripts/output/font-charset.txt --flavor=woff2 --output-file=site/static/fonts/NotoSansSC-Medium.subset.woff2   --layout-features='*' --no-hinting
     pyftsubset site/static/fonts/noto-serif-sc-shared.woff2  --text-file=scripts/output/font-charset.txt --flavor=woff2 --output-file=site/static/fonts/noto-serif-sc-shared.subset.woff2 --layout-features='*' --no-hinting
     ```
  4. **尺寸门槛（机判）**：三个产物各自 ≤300KB（字符集仅 2181 字，754KB 源预期落到 150–250KB，300KB 是留了余量的验收上限；实测数字登记 CHANGELOG）。任一超限则停下排查（通常是字符集混入了整段 JSON 的键名转义噪声，属正常，超限只说明字符集远超预期），不得放宽门槛继续。
  5. `site/tokens.css` 三处 url 改指向 `.subset.woff2`（第 26/33/40 行；第 47/54 行 JetBrains 不动）。
  6. **同步内联**：`python scripts/inline_css.py --force`（226 页 re-sync；不加 --force 会全部 skip-inlined 什么都不发生）。随后 `python scripts/generate_csp.py --check`（纯 CSS url 变更不改任何脚本哈希，预期 0 漂移）。
  7. 写覆盖守卫 `scripts/_check_font_coverage.py`：用与步骤 2 完全相同的口径重新提取字符集，用 fonttools 读三个 subset 文件的 cmap，断言覆盖率 100%，输出 `coverage N/N OK`（N 为步骤 2 产出的实数字符数，执行时登记，勿预写死）；**另加一条 fvar 断言**——noto-serif-sc-shared 源为可变字体（@font-face 声明 weight 200–900），subset 产物必须保留 `fvar` 表，否则字重轴塌缩、Medium/标题字重全部退化为默认字重且不会被任何门禁拦住。此脚本**留档常驻**，并在交接文档「三、方法论沉淀」登记一句：后续新增内容/数据的批次，收尾时重跑一次该脚本。
- **验收**：
  1. 三个产物存在且各 ≤300KB（`ls -l site/static/fonts/*.subset.woff2`）；
  2. `_check_font_coverage.py` 输出 100% 覆盖；
  3. `python scripts/verify_delivery.py` 全绿——重点确认第 15 门禁（INLINED 块 ≥20KB）与第 12 门禁（token 覆盖率）不受 url 替换影响；
  4. `node scripts/check_screenshot_gates.js` FAIL 0（截图比对可暴露字体缺失导致的明显版式变化）；
  5. 抽 3 页（index、data/relationships、en/relationships）Playwright 断言 `document.fonts` 中两个 Noto 家族 loaded 且无 `xatoshi` 类缺字探针——简化口径：页面渲染文本取样 50 个 CJK 字符的 `getBoundingClientRect().width > 0` 且 fontFamily 解析到 Noto。
- **残余风险声明（诚实边界）**：本批之后新写入站点的字符若未重跑子集管线，该字形按 font-family 栈回退到系统字体——浏览器是逐字形回退，**不会出现豆腐块**，表现为该字与周围字体不同（宋黑混排）。拦截手段即步骤 7 的常驻守卫，由后续内容批次触发重跑。
- **回滚**：`git checkout -- site/tokens.css` + `python scripts/inline_css.py --force` + 删除 3 个 subset 文件 + `generate_csp.py --check`。
- **明确非目标**：不删任何现有字体文件（含 3.5MB VF，其处置在方案 A-2 完成）；不做 unicode-range 分片；不引入 Font Loading API。

### B-2 主字体 preload

- **执行步骤**：写 `scripts/_add_font_preload.py`：对 F16 判定的 226 个含 INLINED 标记的 HTML，在 `</head>` 前插入两行（路径按页面层级取 `static/`、`../static/`，与该页 d3 引用路径规则一致；无 d3 引用的页按目录推断：site/ 根 `static/`，data/ 与 en/ 均 `../static/`）：
  ```html
  <link rel="preload" href="<prefix>/fonts/NotoSansSC-Regular.subset.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="<prefix>/fonts/noto-serif-sc-shared.subset.woff2" as="font" type="font/woff2" crossorigin>
  ```
  **crossorigin 属性不可省**（字体请求无论同源与否都走 CORS 模式，漏写会导致 preload 失配、字体被下载两次，反向优化）。8 个无 INLINED 标记的页跳过（无 @font-face，preload 无意义）。
- **验收**：
  1. 脚本断言：226 页每页恰 2 条字体 preload，8 页 0 条；preload 的 href 形态必须与 B-0 修正后的 @font-face url 同形态（data/en 页 `../static/fonts/`，根页 `static/fonts/`），否则 preload 与 font-face 各拉一份、同一字体双重下载反向优化；
  2. LHCI 受测 URL 的 network 面板断言：两个 subset 字体各**恰好出现 1 次**请求（出现 2 次即 preload 失配实锤，须修 href/crossorigin 后复测）；
  3. perf.yml 五项 error 阈值全部保持绿（LCP/CLS/TBT 非回归）。字节收益已由 B-1 的产物尺寸门槛背书，不再以「相对某基线下降 ≥50%」为验收——B-0 落地前子页面字体字节为 0（坏路径），任何「相对基线下降」的口径在此都是错的。
- **回滚**：`_add_font_preload.py` 写一个 `--remove` 逆操作，或对 226 页 `git checkout` 后重跑 A 批已入库的其他变换（若 A、B 已同库，直接按提交粒度 revert）。

---

## 方案 C（建议批号 W565）：EMBEDDED 单源化治理 + 性能预算收紧

| 项 | 值 |
|---|---|
| 优先级 | 中低（收益集中在最大两页 + 长期预算健康） |
| 前置依赖 | C-1/C-2 无依赖；C-3 依赖方案 A 合并后 perf.yml 至少完整跑过一次 |
| 预计改动 | C-1 一份枚举清单；C-2 起步 2 个 HTML（data/en relationships，后续按枚举结果逐页同法）；C-3 perf.yml 内 1–2 行阈值 + Summary 表 1 行 |
| 预计工作量 | 2–3 小时 |

### C-1 枚举「EMBEDDED 完整 + fetch 同源」双源页

- **判定规则（可照抄进脚本）**：页面同时满足 ① 存在 `const EMBEDDED`（或 `EMBEDDED_DATA`）且其键覆盖该页全部 `loadJson(` 调用的 fallback 实参；② 存在指向 `scripts/output/data/` 的 fetch/baseUrl 字面量（即方案 A 处理过的形态，A-3 完成后该字面量已指向 `json/`，本项以「指向 json/ 副本」的新形态为准）。写 `scripts/_enum_dual_source.py` 输出清单到 `scripts/output/dual-source-pages.txt`。
- **已知样本**：site/data/relationships.html 与 site/en/relationships.html（6 组数据全量内嵌 + fetch 同源 6 份 JSON，HTML 413KB/450KB 中 281.8KB 是内嵌数据）。
- **验收**：清单落盘；每行可追溯到页面文件与 EMBEDDED 键名。

### C-2 relationships 两页（及枚举清单各页）去 fetch 化

- **动机**：部署态下 HTML 里 281.8KB 的 EMBEDDED 与 fetch 回来的 6 份 JSON（合计约 188KB）双份传输；file:// 下 fetch 失败再回退。既然 EMBEDDED 与 JSON 由同一生成器产出、且 W560 的 L2 对账保证两者一致，部署态 fetch 属纯浪费；pageerror 面上还省 6 次请求。
- **执行步骤（每页最小 diff，两处改动）**：
  1. `loadJson` 函数体（data 版 5391–5404 行附近）改为直接返回 fallback 并保留日志：
     ```js
     async function loadJson(path, fallback) {
         // W<批>: EMBEDDED 单源化——数据与页面同源生成，部署态不再重复 fetch
         console.info('[DATA] EMBEDDED 单源:', path);
         return fallback;
     }
     ```
     六处 `loadJson(baseUrl + ...)` 调用**保持不动**；随后删除 5422 行 `const baseUrl = '../../scripts/output/data/';`（成为死变量，删除以通过字面量验收）。
  2. 页面可见文案两处同步：1416 行 badge `fetch + EMBEDDED fallback` → `EMBEDDED 内嵌单源`；1447 行数据来源说明去掉「本页 fetch 失败时自动回退到内嵌 EMBEDDED 数据」改为「数据内嵌于页面（EMBEDDED 单源），file:// 双击可用」。en 版对应位置同法。
- **铁律对齐声明**：W554 规则「EMBEDDED 必须含完整数据」不受违反——EMBEDDED 升级为唯一数据源仍含完整数据；「fetch 相对路径不得越出 site/」自动满足（无 fetch）。本项**不需要**任何门禁/规则修订。
- **验收**：
  1. `node scripts/check_screenshot_gates.js --only relationships` FAIL 0，两页渲染与改动前截图逐像素无差异（图表数据未变）；
  2. `node scripts/_w560_runtime_extract.js` 生成运行时抽取（输出目录见该脚本内常量），随后 `python scripts/check_content_consistency.py --dataset-runtime <该输出目录>` 复跑保持 39/39（该对账比对的是页面运行时渲染值与 dataset，数据未变故必然保持；若口径变化，以当批实跑输出为准填写 CHANGELOG）；
  3. `python scripts/verify_delivery.py` 核心全绿；
  4. 枚举清单内其余页面逐页同法处置或明确登记「保留 fetch（原因）」，一行一裁决。
- **回滚**：单页 `git checkout -- <page>`。
- **明确非目标**：不做「部署态剥离 EMBEDDED」的构建变体（动 file:// 自包含铁律，明确不做）；不动 text-search 页的动态注入模式（那是正面样板）。

### C-3 Lighthouse 预算收紧（依赖 A-1 落地后的实测）

- **规则（机判，无自由裁量）**：取方案 A 合并后首个 perf.yml 运行的 Summary/artifact 中 4 个非 3D URL（dashboard、index、timeline、text-search）各 3 runs 的 p75 LCP：若全部 ≤4000ms → 修改 perf.yml 中非 3D 断言 `largest-contentful-paint` 的 `maxNumericValue` 5000 → 4000，并把工作流底部 Summary 表与注释的来源标注更新为「W<批> 实测校准」；只要有一个 URL >4000ms → 不改阈值，把四个实测数字登记进当批 CHANGELOG「性能债」段。CLS/TBT/FCP/3D 页阈值一律不动。
- **验收**：改了阈值 → CI 绿即通过；没改 → CHANGELOG 有四个实测数字。两者都算完成，禁止「既不改阈值也不留数字」的不了了之。

---

## 执行顺序与依赖图

```
批次 1（建议 W563，5.5-7h）＝ A-1…A-4 + B-0 ── 经用户 2026-09-08 确认的执行划分
  内部顺序：B-0（字体路径）→ A-1（d3 移位）→ A-2（sw.js）→ A-3（越界 fetch + 第 9 门禁扩展）→ A-4（agent-web）
  四项间无技术耦合，B-0 放首位的理由：它是 225 页可见视觉变化项，放最前使后续各项的截图回归基线即「修复后字体态」，避免 A-1 等项验收截图在字体变更前后各截一遍。
批次 2（建议 W564，2-3h）＝ B-1 + B-2 ── 依赖批次 1 的 B-0
批次 3（建议 W565，2-3h）＝ C-1 + C-2 + C-3 ── C-3 必须等批次 1 合并后 perf.yml 首跑完成
```

语义变更声明（诚实边界）：A-3 β 类是唯一「数据变真实」项（chapter-stats 两页从 mock 变真数据）；**B-0 是唯一有全站可见视觉变化的项**——data/ 与 en/ 两级子页面的自定义字体首次真正生效（此前一直是系统回退字体），截图对比会看到字形全面变化，属修复效果而非回归，CHANGELOG 必须写明以免后续审查误判。其余各项不改变内容与图表语义；全部可在现有 25 道门禁 + 动态五类门禁框架内验收。门禁变更仅一处且已获用户确认：第 9 门禁 `check_data_drift.js` 扩展副本对账子检查（A-3 步骤 4，随批次 1 落地并在 AGENTS §4.2/文档规范 §8 登记）；`_check_json_copies.py` 并入门禁后仅留作批内自检，`_check_font_coverage.py` 以留档脚本形态存在、是否转正按 W551 先例在缺陷清零后另议。

## 全批通用约束（执行者必读）

1. 批量落盘前确认 `git status` 干净；批量脚本落盘后立即 `git diff --stat` 核对改动文件数与本方案「预计改动」一致，超出即回查。
2. 同一文件多处修改必须串行 Edit（并行 Edit 基于同一原始内容，后写覆盖先写——W505 四次实证）；批量修改一律走 Python 脚本落盘，禁用 PowerShell Set-Content。
3. Windows 多行脚本/文本一律 Write 工具落盘后执行，禁 `cat <<'EOF'`。
4. 改任何内联脚本后必跑 `generate_csp.py`（本计划各步均为外部资源/CSS 变更，预期 0 漂移，但必须实跑留证）。
5. CHANGELOG「验证」栏数字一律当批实跑取得（W496/W537①），禁止从本文档基线表直接抄——本文档数字是 2026-09-08 的现状值，执行时页面数（234）与门禁数（25）若已因其他批次变化，以执行时点实测为准。
6. 提交信息用 `git commit -F <文件>`，不用 heredoc。
7. 本文中 `W<批>` 为占位符，含义是「实际执行该方案的批次号」（按约束 5 的规则领取后填入代码注释、workflow 注释与 CHANGELOG 引用），不是字面文本。

---

## 执行实录（W563 · 2026-09-10 · 批次 1 = A-1…A-4 + B-0）

与方案的偏差与新增发现（全部已验证落地，详见 CHANGELOG W563 段）：

| # | 偏差/新增 | 说明 |
|---|---|---|
| 1 | A-3 范围 37 → **107 页** | F8 正则只识别「引号+文件名」形态，漏 baseUrl 变量赋值与徽标/注释/文案变体——以「包含子串」广扫后按上下文分级改写；site 全树 `scripts/output/data` 残留 0 |
| 2 | β 类前提修正 | chapter_stats.json 实为**全零空壳**（非 237B 真数据）；根治须先修 `scripts/utils/text_loader.py`（只匹配 `第*.txt` 而分回实为 `第*.md`，全部批分析器空转）再跑生成器——100 回/740,093 字首次产出 |
| 3 | γ-2 拆分再修正 | F20「character-appearance 无生成器」错误（顶层 grep 漏了 `scripts/B_人物/` 递归）——生成器存在，产出 59KB 真实数据后两页升级为 α（站内 fetch + 部署副本），file:// 保留诚实 mock 兜底 |
| 4 | γ-1 如期 | journey-geo-semiotics 中英两页 EMBEDDED 单源化（geo_semiotics.json 确无生成器） |
| 5 | inline_css.py 追加修复 | W536 写路径守卫根目录少算一层（`dirname` 一层 → 需两层，W550 generate_csp.py 同款）——W536 后首次 `--force` 即触发，守卫修复后 226 页重内联成功 |
| 6 | A-4 作废 | vite.config.js/.d.ts 从未入库（F17 系误读 `grep -n` 行号为 `git ls-files` 输出），根 .gitignore 已覆盖——零改动 |
| 7 | 门禁 9 实测口径 | 对账面 44→46 页/71→74 项（+EMBEDDED 单源页页名回退），47 副本基线，负样本冒烟通过 |
| 8 | 门禁实战记录 | 动态死链门禁当批拦获本批注释中「第*.md」字面量（已改写措辞放行）；截图门禁 234 页 FAIL 0；部署态冒烟 6/6；字体探针 3/3 |

批次 2（B-1 字体子集化 + B-2 preload）与批次 3（C-1/C-2/C-3）按依赖图另行领取批号执行。
