#!/usr/bin/env python3
"""文档口径体检 doc-sync（第 31 门禁 · W663）——代码/提交是真值源，文档当前态声明是派生物。

移植自 GateKeeper / 千问大赛仓 doc-sync 机制（W663 经验移植批；D2 裁决：对账表登记即豁免）。
四类窄句式白名单（宁窄勿误，防误伤历史叙述——历史段/方案档/复盘档一律不进扫描面）：
  C1 README 抬头「当前版本 vX（日期）**： W###」 ≡ CHANGELOG 顶段三元组
  C2 交接文档头链链首「- **vX W###」 ≡ CHANGELOG 顶段（v + W）
  C3 AGENTS §4.2 门禁清单最高编号 == verify_delivery.py 实况最高槽位
     C4 提交-版段对账：近 15 条 commit subject 中的 W### ⊆ CHANGELOG 版段集合 ∪ 对账表登记行；
     认领行强制（W720）：CHANGELOG 现役段 W 号须有对账表「表格行」——预留豁免 bullet 不算认领；
     C4-e 级联清单强校验（W722）：pre-commit staged ⊇ 当批 _cascade_files 清单（无清单 NOTE·staged 空不适用）；
     C4-f 文件清单入库对账（W723）：现役段「文件」行路径 ⊆ HEAD 树 且 无工作树残留（W537③ 清偿·手工件唯一防线·缺行 NOTE）；
          W906 三态：残留为「他方批次登记行纯追加」（| WNNN 形态·零删改）时降 NOTE——并行在途非漏 add（W904 实录）
  C5 聚合数字对账（W703 建·W704 实体化）：18 式高危聚合句式 × 现役叙述面（README/STRUCTURE/AGENTS/项目说明全文 +
     CHANGELOG 仅「全站页数口径」块行）vs scripts/output/stats.json（scripts/stats.py 磁盘实算·实体化 tracked）；
     C5b 数字实体标记：<!--stats:KEY--> 前置数字 == stats.json[KEY].value（键未登记=fail-closed；
          W830 扩展面：docs/11-方案报告 现役报告 *.md（W830-W900 根层·W901 起递归）+ pytest.ini
          亦入标记对账——只跑标记、
          不跑句式白名单与 C5c 裸数字（辅助叙述面宁窄勿误）；计划方案/ 子目录刻意除外：计划件为
          时点快照，其引用的基线数字随批次冻结（同 CHANGELOG 历史段纪律·禁回溯改写），由计划自身的
          「聚合数字当批现测」条款在开工批复核（T04 AC-07 34/35 vs 现役 37 实例））；
     C5c 裸聚合数字：标记/句式覆盖外的 N[页项篇个类] 判红（W904 收口——W703 起步策略的终态·74 处清零后转；
          实体化加 <!--stats:KEY--> 或豁免：整行 EXEMPT_MARK 前缀 / 命中后置紧跟 EXEMPT_MARK·W904 新增只豁免该命中）；
     C5d stats 实算对账（W718）：scripts/stats.py --check（stats.json vs 磁盘实算）零差异——
     「检查过零差异」有机器背书，漂移未刷新（漏跑 --w）当场 FAIL（W715 实例的防线）；
     基线/首跑等时点值靠句式表设计豁免（不进句式形态），新聚合量须先登记 stats.py META 键表
  C6 版本行 desc 分隔符体检（W841）：README / STRUCTURE / 项目说明三处「当前批次」版本行的 desc 段
     禁含 · ； —。缺口来源——batch_cascade.precheck() 早已 fail-closed 禁这些字符，但只管「走
     batch_cascade 的 spec」；W826 的段是手工写入的（无 _w826_spec.json），precheck 从未被调用，
     于是 desc 里的「·」把三处锚点正则（·A1-A6 / —A1-A6 / ·详细变更见）全部顶掉，此后任何批
     都级联不了。版本行是 desc 的唯一落点，扫它就把手工路径一并闭上。文档非空但版本行形态不识别
     按 FAIL 计（形态变更会让本支静默失效）。
豁免：行级 <!--doc-sync:exempt 原因-->；.git/shallow 存在时 C4 跳过（pre-commit 本地为主执行点）。
用法：--check（默认）只读校验，0 FAIL 才过；--self-test 注入式负样本 24 例（纯合成输入，不改真实文件）；
     --json 供 CI 消费。本脚本绝不修改任何文件。
"""

import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RE_CHANGELOG_TOP = re.compile(r"^###\s+(?:v(\d+\.\d+\.\d+)|W(\d+))（([^）]*)）：\s*(?:W(\d+))?", re.M)  # W711 双形态：历史 vX.Y.Z（date）：W### / 新段 W###（date）：标题
RE_CHANGELOG_SECT = re.compile(r"^###\s+(?:v\d+\.\d+\.\d+（[^）]*）：\s*W(\d+)|W(\d+)（[^）]*）：)", re.M)  # wnum = g1(历史) or g2(新)
RE_README_HEAD = re.compile(r"当前(?:版本\s*v\d+\.\d+\.\d+|批次\s*W(\d+))（([^）]+)）\*\*：\s*(?:W(\d+))?", re.M)  # wnum = g1(新·批次后) or g3(历史·冒号后)
RE_JIAOJIE_HEAD = re.compile(r"^-\s*\*\*(?:v\d+\.\d+\.\d+\s+)?W(\d+)", re.M)  # W711 双形态（ver 可选·wnum 捕获）
RE_AGENTS_ITEM = re.compile(r"^(\d+)\.\s\*\*", re.M)
RE_VERIFY_SLOT = re.compile(r"第\s*(\d+)\s*(?:槽|门禁)")
RE_COMMIT_W = re.compile(r"(?<![A-Za-z0-9])[Ww](\d{3})(?!\d)")
RE_TABLE_ROW_W = re.compile(r"^\|\s*W(\d{3})\s*\|", re.M)
RE_TABLE_DEFER = re.compile(r"^-\s*\*\*((?:W\d{3})(?:\s*/\s*W\d{3})*)\*\*", re.M)
RE_STATS_PATTERNS = [  # (正则, (键...), 语境词[None=无·小写包含判定]) —— 键值与 scripts/output/stats.json 对账
    (re.compile(r"HTML 共 (\d+) 页"), ("html_total",), None),
    (re.compile(r"site/data (\d+) \+ site/en (\d+) \+ site 根 (\d+) \+ site/reader (\d+)"),
     ("site_data_html", "site_en_html", "site_root_html", "site_reader_html"), None),
    (re.compile(r"CSP 覆盖 (\d+) 页"), ("csp_covered",), None),
    (re.compile(r"(\d+) 页哈希 0 漂移"), ("csp_covered",), None),
    (re.compile(r"扫 (\d+) 文件"), ("scan_files",), None),
    (re.compile(r"(\d+) 页扫描"), ("seo_scanned",), "seo"),
    (re.compile(r"扫 (\d+) 页"), ("seo_scanned",), "seo"),
    (re.compile(r"同步 (\d+) 页"), ("inline_css_pages",), None),
    (re.compile(r"(\d+) 个[^，。）]*?可视化页"), ("visualization_pages",), None),
    (re.compile(r"(\d+) 可视化页"), ("visualization_pages",), None),
    (re.compile(r"(\d+) 项自动化门禁"), ("gate_count",), None),
    (re.compile(r"共 (\d+) 篇"), ("a1_a6_docs",), None),
    (re.compile(r"已建 (\d+) 篇"), ("methodology_docs",), "方法论"),
    (re.compile(r"(\d+) 个 JSON 文件"), ("json_count",), None),
    (re.compile(r"site/data/ 共 (\d+) 个 HTML"), ("site_data_html",), None),
    (re.compile(r"A-AH (\d+) 类"), ("script_classes",), None),
    (re.compile(r"按 (\d+) 类组织"), ("script_classes",), None),
    (re.compile(r"(\d+) 类子目录全建"), ("script_classes",), None),
]
RE_CHANGELOG_SCOPE = re.compile(r"^> \*\*全站页数口径\*\*.*$", re.M)  # CHANGELOG 扫描域=口径块行
RE_FILE_LIST_LINE = re.compile(r"^> - \*\*文件\*\*：(.+)$", re.M)  # W723 C4-f：四件套「文件」行
RE_BATCH_REGISTRY_ROW = re.compile(r"^\| W\d{3} ")  # W906 C4-f 三态：他方批次登记行形态
RE_FILE_TOKEN = re.compile(
    r"^(?:CHANGELOG|README|STRUCTURE|AGENTS|CLAUDE|CONTRIBUTING|CITATION)\.cff?$"
    r"|.+\.(?:py|js|mjs|cjs|ts|tsx|jsx|md|json|jsonl|cff|txt|html|css|xml|yml|yaml|toml|ini|cfg|sh|ps1|csv|svg|example)$"
)  # 路径 token 判定：根级治理文件白名单 或 带已知后缀（含 / 的子目录路径）
# W813 扩面：原正则只认 .py/.js/.mjs/.md/.json/.cff/.txt/.html/.css/.xml/.yml，
# .ts/.tsx/.cjs/.jsonl/.yaml/.toml/.ini/.cfg/.sh/.ps1/.csv/.svg/.example 全部被**静默滤除**——
# 而滤除即「不被校验」：W808 声明 34 项，C4-f 实际只认 5 项（丢弃 29 项·全是 .ts/.tsx），
# 于是「手工件漏 add」这条防线在 W808 这类前端批上等于不存在。
# 实证（负样本对照）：同一漏 add 形态，.py 被判红、.ts 只出 NOTE 静默放行。
# 覆盖面判据：凡仓内实际存在且会被手工编辑的文本类文件，其后缀都须在列；
# 二进制资产（.png/.woff2/.ttf 等）不列——「文件」行本就只登记手工编辑件。
RE_STATS_MARK = re.compile(r"(\d+)\s*[页项篇个类]?\s*<!--stats:([a-z_0-9]+)-->")  # W704 数字实体标记（紧贴/句尾双形态·key 后置·渲染隐藏）
RE_BARE_AGG = re.compile(r"(?<![A-Za-z])\d+\s*(?:页|项|篇|个|类)")  # C5c 裸聚合数字（W704 起步·W904 起判红；W904 补词边界——「S1 项目/A2 个人随笔」类编号假阳性实证·字母后邻数字不计）
C5_DOC_NAMES = {"readme": "README.md", "structure": "STRUCTURE.md", "agents": "AGENTS.md", "xiangmu": "项目说明.md", "contributing": "CONTRIBUTING.md", "koujing": "统计口径说明.md"}  # W713 补 CONTRIBUTING（第 27 门禁叙述面已含·C5 面对齐）；W769 补统计口径说明（自称「唯一口径来源」却不在扫描域·W760 F-9 实证）

# C6 版本行 desc 分隔符体检（W841）——手工写段绕过 batch_cascade.precheck 的兜底。
# 缺口实证：batch_cascade.precheck() 早已 fail-closed 禁 desc 含 · ； —，但那只覆盖「走 batch_cascade 的 spec」；
# W826 的段是**手工写入**的（output 下仅三个 _w826_*.py 审计脚本·无 _w826_spec.json），precheck 从未被调用，
# 于是 desc 里的「·」把三处版本行锚点正则（·A1-A6 / —A1-A6 / ·详细变更见）全部顶掉，
# 之后任何批都级联不了（W827 施工时撞上，改 · 为 、后十面断言立过）。
# 版本行是 desc 的唯一落点，扫它就把手工路径一并闭上——这是 precheck 之外必须有的第二道。
# 形态： (输入键, 显示名, 版本行正则·捕获组 1 为 desc 起至行尾, 尾锚点元组)
C6_SURFACES = (
    ("readme", "README.md",
     re.compile(r"^>\s*\*\*当前批次\s*W\d+（[^）]*）\*\*：(.+)$", re.M),
     ("·A1-A6",)),
    ("structure", "STRUCTURE.md",
     re.compile(r"^>\s*当前批次：W\d+（[^）]*）—\s*(.+)$", re.M),
     ("—A1-A6",)),
    ("xiangmu", "项目说明.md",
     re.compile(r"^>\s*当前批次\s*W\d+（[^）]*）：(.+)$", re.M),
     ("·详细变更见",)),
)
C6_BANNED_SEPS = ("·", "；", "—")  # 与 batch_cascade.precheck 的 desc 黑名单同口径（双源一致性由本支兜底）



def _foreign_append_only(paths):
    """W906：判定哪些 dirty 文件的未暂存改动是「他方批次登记行的纯追加」。

    口径：`git diff -- <path>` 正文行中零「-」行，且全部非空「+」行 strip 后匹配
    RE_BATCH_REGISTRY_ROW（台账认领行「| WNNN 」形态）。只认纯追加——他方在位
    编辑（改状态列等）含删改行，仍属真残留照旧判红。git 探测不可用（None）时该
    文件不计入（判据保守回退原 FAIL 语义·fail-closed 方向）。
    """
    out = set()
    for p in paths:
        lines = _git_output_lines(["diff", "--", p], strip=False)
        if lines is None:
            continue
        adds, dels = [], 0
        for ln in lines:
            if ln.startswith("---") or ln.startswith("+++"):
                continue
            if ln.startswith("-"):
                dels += 1
            elif ln.startswith("+"):
                adds.append(ln[1:].strip())
        if dels == 0 and adds and all(RE_BATCH_REGISTRY_ROW.match(a) for a in adds):
            out.add(p)
    return out


def c5b_extra_surfaces():
    """W830：C5b 实体标记对账扩展面（只跑标记·不跑句式与裸数字·宁窄勿误）。

    ① pytest.ini：头注 collected 计数实体化——原 602 字面量无任何对账，W830 审查实证其已漂移至 770；
    ② docs/11-方案报告/**/*.md 递归（W901 起随目录分区改递归·W830-W900 为根层非递归 glob）：
       现役报告自称「当前态盘点」，其 stats 实体标记须随 stats.json 活——W830 审查实证系统架构方案
       report_docs=30 过期（现役 37）却无门禁兜底；W900 目录分区把带标记件移入子目录后根层 glob
       失明（披露于 W900 段），W901 经用户批准改递归恢复覆盖。
    **计划方案/ 子目录刻意除外**：计划件是时点快照，其引用的基线数字随批次冻结（同 CHANGELOG 历史段
    纪律·禁回溯改写），由计划自身的「聚合数字当批现测」条款在开工批复核（T04 AC-07 34/35 实例；
    W901 实测该子目录 8 件带冻结 stats 标记·入面即假红·除外条款随递归化原样保留）。
    """
    paths = [os.path.join(ROOT, "pytest.ini"), os.path.join(ROOT, "site", "index.html")]  # W913：站点聚合数字失真面（B-W855-01·772 篇漂移实证）纳入标记对账
    paths += sorted(
        p for p in glob.glob(
            os.path.join(ROOT, "docs", "11-方案报告", "**", "*.md"), recursive=True)
        if os.sep + "计划方案" + os.sep not in p
    )
    return paths
EXEMPT_MARK = "<!--doc-sync:exempt"
ARCHIVE_CHANGELOGS = [
    os.path.join(ROOT, "archive", "docs", "CHANGELOG-ARCHIVE.md"),
    os.path.join(ROOT, "archive", "docs", "CHANGELOG-ARCHIVE-tier2.md"),
]


def changelog_top(text):
    """现役顶段 → (date, wnum)。W711 方案 D：新段 wnum 在「### W###」处、历史段在「：W###」处。"""
    m = RE_CHANGELOG_TOP.search(text)
    if not m:
        return None
    return (m.group(3), int(m.group(2) or m.group(4)))


def changelog_section_ws(text):
    out = set()
    for a, b in RE_CHANGELOG_SECT.findall(text):
        out.add(a or b)  # 字符串契约（C4 的 RE_COMMIT_W 提取物为字符串）
    return out


def table_registered_ws(text):
    ws = set(RE_TABLE_ROW_W.findall(text))
    for m in RE_TABLE_DEFER.finditer(text):
        ws |= set(RE_COMMIT_W.findall(m.group(1)))
    return ws


def agents_gate_list_max(agents_text):
    m = re.search(r"### 4\.2[^\n]*\n(.*?)### 4\.3", agents_text, re.S)
    if not m:
        return None
    nums = [int(x) for x in RE_AGENTS_ITEM.findall(m.group(1))]
    return max(nums) if nums else None


def verify_slot_max(verify_src):
    nums = [int(x) for x in RE_VERIFY_SLOT.findall(verify_src)]
    return max(nums) if nums else None


def file_list_paths(changelog, wnum):
    """W723 C4-f：解析现役段「文件」行的 repo 相对路径清单（W537③ 清偿）。
    token 按分隔符切分+剥全角括号注释；非路径 token（描述词）滤除。段缺失/行缺失返回 (None, [])。"""
    seg = re.search(rf"^### W{wnum:03d}（.*?(?=^### |\Z)", changelog, re.M | re.S)
    if not seg:
        return None, []
    m = RE_FILE_LIST_LINE.search(seg.group(0))
    if not m:
        return None, []
    out = []
    for tok in re.split(r"[、；;，,\s]+", m.group(1)):
        tok = re.sub(r"（[^）]*）", "", tok).strip("·。")
        if tok and RE_FILE_TOKEN.match(tok):
            out.append(tok)
    return True, out


def stats_value(stats, key):
    """stats.json 实体形态（W704 {value,...}）兼容平面值（W703 过渡）。"""
    e = stats.get(key)
    return e.get("value") if isinstance(e, dict) else e


def line_has_exempt(text, match):
    line_start = text.rfind("\n", 0, match.start()) + 1
    line_end = text.find("\n", match.end())
    if line_end == -1:
        line_end = len(text)
    return EXEMPT_MARK in text[line_start:line_end]


def _check_c6_version_desc_seps(inp, issues, notes):
    """C6：三处版本行的 desc 段禁含分隔符（W841）。

    为什么要有这一支：batch_cascade.precheck() 早就 fail-closed 地禁 desc 含 · ； —，
    但那只管「走 batch_cascade 的 spec」；段一旦手工写入（W826 实证）就完全绕过 precheck。
    版本行是 desc 的唯一落点，扫它能把手工路径一并闭上。

    fail-closed 口径：文档非空但版本行形态不识别 → 报 FAIL（形态变更会让本支静默失效，
    这正是 W813 记过的「滤除即不被校验」同族）；文档为空 → 跳过（合成输入场景）。
    """
    for key, name, pat, tails in C6_SURFACES:
        text = inp.get(key) or ""
        if not text.strip():
            continue
        m = pat.search(text)
        if not m:
            issues.append("C6: %s 版本行形态未识别（期望「当前批次 W###（日期）」抬头）——"
                          "形态变更会使本支静默失效，须同步正则" % name)
            continue
        raw = m.group(1)
        cut = len(raw)
        for t in tails:
            i = raw.find(t)
            if i != -1:
                cut = min(cut, i)
        desc = raw[:cut]
        hit = [s for s in C6_BANNED_SEPS if s in desc]
        if hit:
            issues.append("C6: %s 版本行 desc 含分隔符「%s」——写入后会使下一批级联锚点正则失配"
                          "（W826 实证：三处全断·任何批都无法落段）。改用「、」或空格分隔"
                          % (name, "".join(hit)))


def _check_c7_homepage_showcase(inp, issues, notes):
    """C7：GitHub 仓库主页展示位断言（W889）。

    GitHub 查找 README 的优先级是 `.github/` > 根目录 > `docs/`——`.github/README.md`
    一旦存在即**抢占仓库主页展示位**，真实项目门面（根 README.md）永远上不了主页。
    W889 抓线上渲染 HTML 实证：主页渲染的是 `.github/` 目录导读（"这个目录装什么"），
    而非项目门面（在线体验/桌面版下载/内容规模）。
    故：根 README.md 在位时，`.github/README.md` 必须不存在。

    `docs/README.md` 在优先级链第三位：根 README.md 在位时它不抢位（不判红）；根 README.md
    若被删则它上位——记 NOTE 提示，不判红（本仓 `docs/README.md` 为 W779 生成物·超出本批处置范围）。
    """
    sc = inp.get("showcase")
    if not sc:
        return
    if sc.get("root_readme") and sc.get("github_readme"):
        issues.append("C7: `.github/README.md` 存在且根 README.md 在位——GitHub 主页 README 优先级为"
                      "`.github/` > 根目录 > `docs/`，该文件会抢占仓库主页展示位（真实门面永不上主页）。"
                      "改名 `.github/README-internal.md` 或删除（社区解法·GitHub 讨论 #163997）")
    if sc.get("docs_readme") and sc.get("root_readme"):
        notes.append("C7: `docs/README.md` 处于优先级链第三位——根 README.md 在位时它不抢位；"
                     "若根 README.md 被删则它上位，须同步处置")


def evaluate(inp):
    """纯函数核对：inputs 为注入真值与文档文本的 dict，返回 (issues, notes)。

    issues 元素以 C1:/C2:/C3:/C4: 前缀定性，供 --self-test 断言。
    W730 重构：177 行单体拆为 C1-C5d 六个检查函数（见下方 _check_*）+ 本编排体。
    """
    issues, notes = [], []
    top = changelog_top(inp["changelog"])
    if not top:
        issues.append("C1: CHANGELOG 未解析出现役顶段（期望 ### W###（日期）：标题 或历史 ### vX.Y.Z（日期）：W###）")
        top = ("?", "?")
    date, wnum = top

    _check_c1_readme_head(inp, date, wnum, issues, notes)
    _check_c2_jiaojie_head(inp, wnum, issues, notes)
    _check_c3_agents_slots(inp, issues)
    _check_c4_commit_ledger(inp, issues, notes)
    _check_c5_aggregate_stats(inp, issues, notes)
    _check_c5d_stats_recheck(inp, issues)
    _check_c6_version_desc_seps(inp, issues, notes)
    _check_c7_homepage_showcase(inp, issues, notes)
    return issues, notes


def _check_c1_readme_head(inp, date, wnum, issues, notes):
    """C1：README 抬头 (W, date) == CHANGELOG 顶段（W711 双形态·行级豁免）。W730 提取。"""
    m1 = RE_README_HEAD.search(inp["readme"])
    if not m1:
        issues.append("C1: README 未解析出「当前批次 W###（日期）**：」抬头句")
    elif line_has_exempt(inp["readme"], m1):
        notes.append("C1: README 抬头行带 doc-sync:exempt 豁免，跳过")
    elif (int(m1.group(1) or m1.group(3)), m1.group(2)) != (wnum, date):
        issues.append(
            "C1: README 抬头（%s）W%s ≠ CHANGELOG 顶段（%s）W%s"
            % (m1.group(2), m1.group(1) or m1.group(3), date, wnum)
        )


def _check_c2_jiaojie_head(inp, wnum, issues, notes):
    """C2：交接文档头链链首 W == CHANGELOG 顶段。W730 提取。"""
    m2 = RE_JIAOJIE_HEAD.search(inp["jiaojie"])
    if not m2:
        issues.append("C2: 交接文档未解析出头链链首「- **W###」")
    elif line_has_exempt(inp["jiaojie"], m2):
        notes.append("C2: 交接头链行带 doc-sync:exempt 豁免，跳过")
    elif int(m2.group(1)) != wnum:
        issues.append(
            "C2: 交接头链 W%s ≠ CHANGELOG 顶段 W%s" % (m2.group(1), wnum)
        )


def _check_c3_agents_slots(inp, issues):
    """C3：AGENTS §4.2 门禁清单上限 == verify_delivery 实况最高槽位。W730 提取。"""
    a_max = agents_gate_list_max(inp["agents"])
    v_max = verify_slot_max(inp["verify_src"])
    if a_max is None or v_max is None:
        issues.append("C3: 解析失败（AGENTS §4.2 清单=%s / verify 槽位=%s·fail-closed）" % (a_max, v_max))
    elif a_max != v_max:
        issues.append("C3: AGENTS §4.2 门禁清单止于 %d，verify 实况最高槽位 %d（声明落后于代码实况）" % (a_max, v_max))


def _check_c4_commit_ledger(inp, issues, notes):
    """C4：提交-版段对账 + 认领行强制（W720）+ 级联清单（C4-e·W722）+ 文件清单入库（C4-f·W723）。

    W730 提取：浅克隆早退（仅 NOTE）；对账表登记即豁免（D2）。
    """
    if inp.get("shallow"):
        notes.append("C4: 浅克隆环境（.git/shallow），提交对账跳过（pre-commit 本地为主执行点）")
        return
    reg = changelog_section_ws(inp["changelog"])
    for p in ARCHIVE_CHANGELOGS:
        if os.path.exists(p):
            reg |= changelog_section_ws(open(p, encoding="utf-8").read())
    reg |= table_registered_ws(inp["table"])
    for s in inp["subjects"]:
        s2 = re.sub(r"W\d{3}\s*[-–—]\s*W\d{3}", "", s)  # W711：区间形态（W001-W710 等）下限非实体号·剔除后再提取
        for w in RE_COMMIT_W.findall(s2):
            if w not in reg:
                issues.append("C4: 提交「%s」的 W%s 无 CHANGELOG 版段且未在对账表登记" % (s[:60], w))
    # C4 认领行强制（W720·W719 流程遗漏根修）：现役段 W 号须有对账表「表格行」登记——
    # 预留豁免 bullet（- **WXXX**：现势下一自由号…）不算认领；此前 C4 只查 W 号在登记集合，
    # 两种形态不可区分，动工未先登记认领行不会被拦（W719 实证被豁免 bullet 救场）
    top = changelog_top(inp["changelog"])
    if top and ("%03d" % top[1]) not in set(RE_TABLE_ROW_W.findall(inp["table"])):
        issues.append(
            "C4: CHANGELOG 现役段 W%03d 无对账表认领行（动工前须先在本表登记·预留豁免 bullet 不算认领·W719 流程遗漏实例）"
            % top[1]
        )
    # C4-e 级联清单强校验（W722·用户裁决 2A·W649 漏 add 族机械化）：最终提交树（HEAD 树 ∪ staged·
    # amend 补件场景 staged 仅含新增·本门禁自证修正）⊇ 当批级联清单；
    # 清单不存在→NOTE（手工级联批须自建清单·pitfalls git 类义务）；
    # staged 空（CI/普通跑）→本项不适用
    staged = inp.get("staged") or []
    if staged:
        mf = inp.get("cascade_manifest")
        if mf is None:
            notes.append("C4-e: 当批级联清单不存在（手工级联批须自建 scripts/output/_cascade_files_*.txt·pitfalls git 类义务）")
        else:
            _tree = set(staged) | set(inp.get("head_tree") or [])
            _missing = [ln for ln in mf if ln and ln not in _tree]
            if _missing:
                issues.append(
                    "C4-e: %d 个级联面未入提交树（漏 add·W649）：/%s"
                    % (len(_missing), "、/".join(_missing[:5]))
                )
    # C4-f 文件清单入库对账（W723·W537③ 八批旧账清偿·手工件漏 add 三犯根修）：
    # 现役段「文件」行的路径 token ⊆ HEAD 树 且 无工作树未提交残留——
    # 级联清单只列级联面，手工编辑件（脚本/文档）唯此防线（W721/W722 三处漏 add 实证）；
    # 缺「文件」行/无路径 token → NOTE（四件套缺件或形态不合规·起步策略，成文 pitfalls）
    if top:
        has_line, fl = file_list_paths(inp["changelog"], top[1])
        if has_line is None:
            notes.append("C4-f: 现役段缺「文件」行（四件套缺件·W723 起级联 precheck 强制）")
        elif not fl:
            notes.append("C4-f: 「文件」行无可解析路径 token（须写 repo 相对路径·见 pitfalls git 类）")
        else:
            _tree2 = set(inp.get("head_tree") or []) | set(inp.get("staged") or [])  # pre-commit 首提场景与 C4-e 同语义
            _dirty = set(inp.get("dirty") or [])
            for f in fl:
                if f not in _tree2:
                    issues.append("C4-f: 文件清单 %s 未入提交树（W537③·手工件漏 add 族）" % f)
                elif f in _dirty:
                    if f in (inp.get("foreign_append_only") or set()):
                        notes.append(
                            "C4-f: 文件清单 %s 工作树残留为并行批次登记行纯追加"
                            "（他方在途·非漏 add·W906 三态——以 HEAD 为准不重做）" % f)
                    else:
                        issues.append("C4-f: 文件清单 %s 有工作树未提交残留（漏 add）" % f)


def _check_stats_marker(m, where, stats, issues):
    """C5b 单标记对账（W830 提取：主叙述面与扩展面共用·判据一致防双源漂移）。"""
    key_name = m.group(2)
    want = stats_value(stats, key_name)
    got = int(m.group(1))
    if want is None:
        issues.append("C5b: %s 标记 <!--stats:%s--> 键未登记——先登记 scripts/stats.py META" % (where, key_name))
    elif got != want:
        issues.append(
            "C5b: %s 标记数字 %d ≠ stats.json %s=%s（跑 python scripts/stats.py --w <批号> 刷新）"
            % (where, got, key_name, want)
        )


def _check_c5_aggregate_stats(inp, issues, notes):
    """C5 聚合数字对账 + C5b 实体标记 + C5c 裸数字报告（W703/W704）。

    W730 提取：句式白名单 × 现役叙述面（README/STRUCTURE/AGENTS/项目说明/CONTRIBUTING +
    CHANGELOG 口径块）vs stats.json；标记键未登记/数字失配 fail-closed；裸聚合数字 W904 起判红。
    stats 缺失 fail-closed 早退（原 else 分支等价）。
    """
    stats = inp.get("stats")
    if not stats:
        issues.append("C5: scripts/output/stats.json 缺失或不可解析——先跑 python scripts/stats.py（fail-closed）")
        return
    scans = [("CHANGELOG 口径块", ln) for ln in RE_CHANGELOG_SCOPE.findall(inp["changelog"])]
    for key in C5_DOC_NAMES:
        text = inp[key]
        if key == "agents":
            cut = text.find(chr(10) + "*本文件由")  # 版本脚注=历史沿革记录（W514 时点实况等）·不在扫描域
            if cut != -1:
                text = text[:cut]
        for i, ln in enumerate(text.splitlines(), 1):
            scans.append(("%s:%d" % (C5_DOC_NAMES[key], i), ln))
    for where, ln in scans:
        if EXEMPT_MARK in ln:
            continue
        for pat, keys, ctx in RE_STATS_PATTERNS:
            m = pat.search(ln)
            if not m or (ctx and ctx not in ln.lower()):
                continue
            for gi, key_name in enumerate(keys, 1):
                want = stats_value(stats, key_name)
                got = int(m.group(gi))
                if want is None:
                    issues.append(
                        "C5: stats.json 缺键 %s（%s 命中「%s」）——新聚合量须先登记 scripts/stats.py"
                        % (key_name, where, m.group(0))
                    )
                elif got != want:
                    issues.append(
                        "C5: %s「%s」=%d ≠ stats.json %s=%d（跑 python scripts/stats.py --w <批号> 刷新或修正文档）"
                        % (where, m.group(0), got, key_name, want)
                    )

    # C5b 数字实体标记对账（W704）：<!--stats:KEY--> 前置数字 == stats.json[KEY].value；键未登记 fail-closed
    # C5c 裸聚合数字（W904 起判红·W703「收敛后转 FAIL」终态；标记/句式覆盖位之外）
    # 豁免两形态：①整行前缀 EXEMPT_MARK（W704 起的行级豁免·跳过整行一切判定；W904 收紧为**行首**形态——
    #              原「行内含即整行跳」会吞掉后置豁免行上的标记对账·T30 负样本实证·现存零使用零迁移）
    #            ②命中后置豁免（W904 新增）：裸命中后紧跟（可隔空白）EXEMPT_MARK 只豁免该命中，
    #              行内其余判定（句式/标记对账）照跑——供「混排行」（如既有 stats 标记又含常量数字）精确豁免。
    bare_hits = []
    for where, ln in scans:
        if ln.lstrip().startswith(EXEMPT_MARK):
            continue
        covered = set()
        for pat, _keys, ctx in RE_STATS_PATTERNS:
            for m in pat.finditer(ln):
                if not ctx or ctx in ln.lower():
                    covered.update(range(m.start(), m.end()))
        for m in RE_STATS_MARK.finditer(ln):
            covered.update(range(m.start(), m.end()))
            _check_stats_marker(m, where, stats, issues)
        for m in RE_BARE_AGG.finditer(ln):
            if m.start() in covered:
                continue
            if ln[m.end():].lstrip().startswith(EXEMPT_MARK):
                continue  # 后置精确豁免（W904）：只豁免本命中
            bare_hits.append("%s「%s」" % (where, m.group(0)))
    if bare_hits:
        issues.append(
            "C5c: 裸聚合数字 %d 处未实体化（W904 起判红——实体化加 <!--stats:KEY-->；豁免：整行或命中后置 "
            "<!--doc-sync:exempt-->·常量/历史时点/功能描述适用·前 20）：%s%s"
            % (len(bare_hits), "；".join(bare_hits[:20]), "…" if len(bare_hits) > 20 else "")
        )

    # W830 扩展面 C5b 标记对账（只标记·不句式·不裸数字·rationale 见 c5b_extra_surfaces docstring）
    for rel, text in (inp.get("reports_extra") or {}).items():
        for i, ln in enumerate(text.splitlines(), 1):
            if EXEMPT_MARK in ln:
                continue
            for m in RE_STATS_MARK.finditer(ln):
                _check_stats_marker(m, "%s:%d" % (rel, i), stats, issues)


def _check_c5d_stats_recheck(inp, issues):
    """C5d：stats.py --check（stats.json vs 磁盘实算）零差异背书（W718）。W730 提取。"""
    if not inp.get("stats_check_ok", False):
        issues.append(
            "C5d: stats.json 与磁盘实算漂移（%s）——跑 python scripts/stats.py --w <批号> 刷新"
            % inp.get("stats_check_tail", "stats --check 未通过")
        )


def _load_stats():
    try:
        with open(os.path.join(ROOT, "scripts", "output", "stats.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _git_output_lines(args, strip=True, timeout=30):
    """运行 git 命令并返回 stdout 行列表（strip=True 逐行剥空/去空行；False 原样保留）；
    非零退出或异常返回 None（W730 提取：gather 内三处同构 subprocess 块合一）。"""
    try:
        r = subprocess.run(["git", "-c", "core.quotePath=false"] + args,
                           cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="ignore", timeout=timeout)
    except Exception:  # noqa: BLE001
        return None
    if r.returncode != 0:
        return None
    if strip:
        return [ln.strip() for ln in (r.stdout or "").splitlines() if ln.strip()]
    return (r.stdout or "").splitlines()


def gather():
    def rd(p):
        with open(p, encoding="utf-8") as f:
            return f.read()

    inputs = {
        "changelog": rd(os.path.join(ROOT, "CHANGELOG.md")),
        "readme": rd(os.path.join(ROOT, "README.md")),
        "jiaojie": rd(os.path.join(ROOT, "HANDOVER.md")),
        "agents": rd(os.path.join(ROOT, "AGENTS.md")),
        "structure": rd(os.path.join(ROOT, "STRUCTURE.md")),
        "xiangmu": rd(os.path.join(ROOT, "docs", "00-导读", "项目说明.md")),
        "contributing": rd(os.path.join(ROOT, "CONTRIBUTING.md")),
        "koujing": rd(os.path.join(ROOT, "docs", "00-导读", "统计口径说明.md")),
        "verify_src": rd(os.path.join(HERE, "verify_delivery.py")),
        "stats": _load_stats(),
        "table": rd(os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md")),
        # W830：C5b 扩展面（pytest.ini + 11-方案报告根层·只跑标记对账·见 c5b_extra_surfaces）
        "reports_extra": {
            os.path.relpath(p, ROOT).replace(os.sep, "/"): rd(p)
            for p in c5b_extra_surfaces()
            if os.path.exists(p)
        },
        "subjects": [],
        "shallow": os.path.exists(os.path.join(ROOT, ".git", "shallow")),
        # W889：GitHub 仓库主页展示位实况（.github/README.md 存在即抢占仓库主页）
        "showcase": {
            "root_readme": os.path.isfile(os.path.join(ROOT, "README.md")),
            "github_readme": os.path.isfile(os.path.join(ROOT, ".github", "README.md")),
            "docs_readme": os.path.isfile(os.path.join(ROOT, "docs", "README.md")),
        },
    }
    try:
        r = subprocess.run(
            ["git", "log", "--format=%s", "-15"], cwd=ROOT, capture_output=True, text=True, timeout=30
        )
        if r.returncode != 0:
            inputs.setdefault("git_err", r.stderr.strip()[:120])
        else:
            inputs["subjects"] = [ln for ln in r.stdout.splitlines() if ln.strip()]
    except Exception as e:  # noqa: BLE001 —— 环境无 git 时 fail-closed
        inputs["git_err"] = str(e)[:120]
    try:
        r = subprocess.run(  # W718 C5d：stats.py --check（stats.json vs 磁盘实算·实测 0.3s）
            # W830：timeout 60→180——stats --check 自 W830 起含 pytest --collect-only 实算（本机 0.3s·CI 留裕量）
            [sys.executable, os.path.join(HERE, "stats.py"), "--check"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=180,
        )
        inputs["stats_check_ok"] = r.returncode == 0
        _tail = ((r.stdout or "") + (r.stderr or "")).strip().splitlines()
        inputs["stats_check_tail"] = _tail[-1][:160] if _tail else ""
    except (OSError, subprocess.TimeoutExpired) as exc:
        inputs["stats_check_ok"] = False
        inputs["stats_check_tail"] = "stats --check 执行失败: %s" % exc
    # W722/W723 git 探测（W730 去重）：staged（C4-e）/ HEAD 树（C4-e 补件语义）/ 工作树残留（C4-f）
    staged_lines = _git_output_lines(["diff", "--cached", "--name-only"])
    inputs["staged"] = staged_lines if staged_lines is not None else []
    head_lines = _git_output_lines(["ls-tree", "-r", "HEAD", "--name-only"])
    inputs["head_tree"] = head_lines if head_lines is not None else []
    raw_status = _git_output_lines(["status", "--porcelain"], strip=False)
    _dirty = []
    if raw_status is not None:
        for ln in raw_status:
            if len(ln) > 3 and (ln[1] != " " or ln[:2] == "??"):
                _dirty.append(ln[3:].strip().strip('"'))
    inputs["dirty"] = _dirty
    # W906 C4-f 三态：dirty 文件中未暂存 diff 为「他方批次登记行纯追加」者单列——
    # 并行会话在台账落认领行属他方在途（W904 收官提交被此形态拦停的实录），非本方漏 add
    inputs["foreign_append_only"] = _foreign_append_only(_dirty)
    try:
        _top = changelog_top(inputs["changelog"])
        _mp = os.path.join(ROOT, "scripts", "output", "_cascade_files_W%03d.txt" % _top[1]) if _top else None
        inputs["cascade_manifest"] = (
            [ln.strip() for ln in open(_mp, encoding="utf-8").read().splitlines() if ln.strip()]
            if _mp and os.path.exists(_mp) else None
        )
    except Exception:  # noqa: BLE001
        inputs["cascade_manifest"] = None
    if inputs.get("git_err") and not inputs["shallow"]:
        # 无 git 且非浅克隆：无法对账即 fail-closed（浅克隆已有跳过通道）
        inputs["force_c4_fail"] = inputs["git_err"]
    return inputs


def run_check():
    inp = gather()
    if inp.get("force_c4_fail"):
        print("FAIL  C4: git log 不可得且非浅克隆，提交对账 fail-closed：%s" % inp["force_c4_fail"])
        print("---- 第 31 门禁 文档口径体检：1 FAIL（C4 fail-closed）----")
        return 1, ["C4: git log 不可得"], []
    issues, notes = evaluate(inp)
    for it in issues:
        print("FAIL  " + it)
    for nt in notes:
        print("NOTE  " + nt)
    print(
        "---- 第 31 门禁 文档口径体检：%d FAIL · %d NOTE（C1 README 抬头 / C2 交接头链 / C3 门禁清单上限 / C4 提交-版段对账 / C5 聚合数字对账 / C5d stats 实算对账）----"
        % (len(issues), len(notes))
    )
    return (1 if issues else 0), issues, notes


def run_self_test():
    """26 例注入式负样本/正样本（纯合成输入，不改真实文件）。"""
    base = {
        "changelog": "### W999（2026-10-05）：自测顶段\n\n### v9.9.8（2026-10-04）：W998 旧段\n",
        "readme": "> **当前批次 W999（2026-10-05）**：自测抬头行\n",
        "jiaojie": "- **W999 自测链首**：\n",
        "agents": "### 4.2 交付门禁\n\n30. **甲门**\n31. **乙门**\n\n### 4.3 其他\n",
        "verify_src": "# ---- 第 30 槽 ----\n# ---- 第 31 槽 ----\n",
        "subjects": ["feat(w999): 自测提交"],
        "table": "| W999 | x | y | z | s | c |\n- **W659 / W660**：递延登记\n",
        "structure": "",
        "xiangmu": "",
        "contributing": "",
        "koujing": "",
        "reports_extra": {},
        "stats_check_ok": True,
        "stats_check_tail": "",
        "staged": [],
        "head_tree": [],
        "cascade_manifest": None,
        "stats": {
            k: {"value": v}
            for k, v in {
                "gate_count": 31, "html_total": 100, "a1_a6_docs": 50, "methodology_docs": 6,
                "visualization_pages": 10, "csp_covered": 100, "scan_files": 100, "seo_scanned": 100,
                "inline_css_pages": 10, "json_count": 9, "script_classes": 34,
                "site_data_html": 10, "site_en_html": 10, "site_root_html": 10, "site_reader_html": 70,
            }.items()
        },
        "shallow": False,
        "showcase": {"root_readme": True, "github_readme": False, "docs_readme": False},
    }
    cases = []

    def case(name, mutate, expect_prefix=None, expect_absent=False):
        cases.append((name, mutate, expect_prefix, expect_absent))

    case("T1 README 抬头改值必红", lambda d: d.update(readme=d["readme"].replace("W999", "W998")), "C1")
    case("T2 交接头链改值必红", lambda d: d.update(jiaojie=d["jiaojie"].replace("W999", "W997")), "C2")
    case(
        "T3 门禁清单上限失配必红",
        lambda d: d.update(agents=d["agents"].replace("31. **乙门**", "")),
        "C3",
    )
    case(
        "T4 提交带未登记 W 必红",
        lambda d: d.update(subjects=d["subjects"] + ["test(w777): 伪造未登记提交"]),
        "C4",
    )
    case(
        "T5 对账表登记即豁免（D2）",
        lambda d: d.update(subjects=["chore(w659): 递延批提交"]),
        "C4",
        expect_absent=True,
    )
    case(
        "T6 行级豁免标记生效",
        lambda d: d.update(readme="> **当前批次 W996（2026-10-05）**：自测抬头行 <!--doc-sync:exempt 历史时点事实-->\n"),
        "C1",
        expect_absent=True,
    )
    case("T7 干净输入零误报", lambda d: None)
    case(
        "T8 聚合数字失配必红（C5）",
        lambda d: d.update(readme=d["readme"] + "每次提交需通过 99 项自动化门禁\n"),
        "C5",
    )
    case(
        "T9 聚合数字行级豁免放行（C5）",
        lambda d: d.update(
            readme=d["readme"] + "每次提交需通过 99 项自动化门禁 <!--doc-sync:exempt 自测豁免-->\n"
        ),
        "C5",
        expect_absent=True,
    )
    case(
        "T10 stats.json 缺失 fail-closed（C5）",
        lambda d: d.update(stats=None),
        "C5",
    )
    case(
        "T11 实体标记失配必红（C5b）",
        lambda d: d.update(readme=d["readme"] + "HTML 共 200<!--stats:html_total--> 页\n"),
        "C5b",
    )
    case(
        "T12 实体标记未登记键必红（C5b）",
        lambda d: d.update(readme=d["readme"] + "共 9<!--stats:unknown_key--> 个\n"),
        "C5b",
    )
    case(
        "T13 stats 实算漂移必红（C5d）",
        lambda d: d.update(stats_check_ok=False, stats_check_tail="DRIFT methodology_docs: stats.json=33 磁盘实算=34"),
        "C5d",
    )
    case(
        "T14 现役段无对账表认领行必红（C4·W720）",
        lambda d: d.update(table="- **W999**：现势下一自由号（递延豁免 bullet·非认领行）\n"),
        "C4",
    )
    case(
        "T15 级联面漏 add 必红（C4-e·W722）",
        lambda d: d.update(staged=["CHANGELOG.md"], cascade_manifest=["CHANGELOG.md", "README.md", "AGENTS.md"]),
        "C4-e",
    )
    case(
        "T16 amend 补件场景不误报（C4-e 语义修正·W722 实证）",
        lambda d: d.update(staged=["scripts/output/_cascade_files_W999.txt"], head_tree=["CHANGELOG.md", "README.md", "AGENTS.md"],
                           cascade_manifest=["CHANGELOG.md", "README.md", "AGENTS.md", "scripts/output/_cascade_files_W999.txt"]),
        "C4-e",
        expect_absent=True,
    )
    case(
        "T17 文件清单漏 add 必红（C4-f·W723）",
        lambda d: d.update(
            changelog=d["changelog"].replace("### W999（2026-10-05）：自测顶段\n",
                                             "### W999（2026-10-05）：自测顶段\n\n> - **文件**：docs/a.md、docs/b.md（注）\n"),
            head_tree=["docs/a.md"], dirty=[],
        ),
        "C4-f",
    )
    case(
        "T18 文件清单工作树残留必红（C4-f·W723）",
        lambda d: d.update(
            changelog=d["changelog"].replace("### W999（2026-10-05）：自测顶段\n",
                                             "### W999（2026-10-05）：自测顶段\n\n> - **文件**：docs/a.md\n"),
            head_tree=["docs/a.md"], dirty=["docs/a.md"],
        ),
        "C4-f",
    )
    # W813：.ts/.tsx 扩面用例——原 RE_FILE_TOKEN 静默滤除 .ts/.tsx，
    # 于是「前端件漏 add」只出 NOTE 放行（实测：同一形态 .py 判红、.ts 放行）。
    # T19 钉住「.ts 漏 add 必红」，T20 钉住「多扩展名均被识别为路径 token」。
    case(
        "T19 .ts 文件清单漏 add 必红（C4-f·W813 扩面）",
        lambda d: d.update(
            changelog=d["changelog"].replace("### W999（2026-10-05）：自测顶段\n",
                                             "### W999（2026-10-05）：自测顶段\n\n> - **文件**：xiyouji-agent-web/server/errors.ts\n"),
            head_tree=[], dirty=[],
        ),
        "C4-f",
    )
    case(
        "T20 .ts/.tsx/.jsonl/.yaml 等扩展名均被识别为路径 token（W813 覆盖面回归锁）",
        lambda d: d.update(
            changelog=d["changelog"].replace("### W999（2026-10-05）：自测顶段\n",
                                             "### W999（2026-10-05）：自测顶段\n\n> - **文件**：a.ts、b.tsx、c.jsonl、d.yaml、e.toml、f.ini\n"),
            head_tree=[], dirty=[],
        ),
        "C4-f",
    )
    # W830：C5b 扩展面（11-方案报告根层 + pytest.ini·只跑标记对账）双向锁——
    # 失配必红（现役报告过期标记无门禁兜底的根修）+ 一致放行（不误伤时点快照外的新叙述面）
    case(
        "T21 报告扩展面标记失配必红（C5b·W830）",
        lambda d: d.update(reports_extra={"docs/11-方案报告/x.md": "全站 HTML 共 200<!--stats:html_total--> 页\n"}),
        "C5b",
    )
    case(
        "T22 报告扩展面标记一致放行（C5b·W830）",
        lambda d: d.update(reports_extra={"docs/11-方案报告/x.md": "全站 HTML 共 100<!--stats:html_total--> 页\n"}),
        "C5b",
        expect_absent=True,
    )
    # W904：C5c 转 FAIL 双向锁 + 后置精确豁免两向（豁免命中不红 / 同行既有标记对账不被豁免拆掉）
    case(
        "T27 裸聚合数字必红（C5c·W904 转判红）",
        lambda d: d.update(readme=d["readme"] + "另有 9 篇文档\n"),
        "C5c",
    )
    case(
        "T28 命中后置豁免放行（C5c·W904）",
        lambda d: d.update(readme=d["readme"] + "另有 9 篇<!--doc-sync:exempt--> 常量文档\n"),
        "C5c",
        expect_absent=True,
    )
    case(
        "T29 后置豁免不拆同行标记对账（C5b 照跑·W904）",
        lambda d: d.update(readme=d["readme"] + "共 100<!--stats:html_total--> 页 + 9 篇<!--doc-sync:exempt--> 常量\n"),
        "C5c",
        expect_absent=True,
    )
    case(
        "T30 后置豁免行内标记失配仍红（C5b 不受豁免影响·W904）",
        lambda d: d.update(readme=d["readme"] + "共 200<!--stats:html_total--> 页 + 9 篇<!--doc-sync:exempt--> 常量\n"),
        "C5b",
    )
    case(
        "T31 编号假阳性不计（C5c·W904 词边界——S1 项目/A2 个人随笔类）",
        lambda d: d.update(readme=d["readme"] + "S1 项目方法论 + A2 个人随笔板块\n"),
        "C5c",
        expect_absent=True,
    )
    # W906：C4-f 三态双向锁——他方登记行纯追加残留放行（W904 被并行 W905 认领行
    # 拦停的实录）/ 非追加形态（foreign 集不含）照旧必红
    case(
        "T32 他方登记行纯追加残留放行（C4-f·W906 三态）",
        lambda d: d.update(
            changelog=d["changelog"].replace("### W999（2026-10-05）：自测顶段\n",
                                             "### W999（2026-10-05）：自测顶段\n\n> - **文件**：docs/00-导读/W批次编号对账表.md\n"),
            head_tree=["docs/00-导读/W批次编号对账表.md"],
            dirty=["docs/00-导读/W批次编号对账表.md"],
            foreign_append_only={"docs/00-导读/W批次编号对账表.md"},
        ),
        "C4-f",
        expect_absent=True,
    )
    case(
        "T33 残留非纯追加形态仍红（C4-f·W906 防误放——foreign 集不含即回退原语义）",
        lambda d: d.update(
            changelog=d["changelog"].replace("### W999（2026-10-05）：自测顶段\n",
                                             "### W999（2026-10-05）：自测顶段\n\n> - **文件**：docs/a.md\n"),
            head_tree=["docs/a.md"], dirty=["docs/a.md"], foreign_append_only=set(),
        ),
        "C4-f",
    )

    # W841：C6 版本行 desc 分隔符体检双向锁——含分隔符必红（手工写段绕过 batch_cascade.precheck 的兜底）
    # + 「、」分隔放行（防误伤正常 desc）
    case(
        "T23 版本行 desc 含分隔符必红（C6·W841）",
        lambda d: d.update(readme=d["readme"].replace("自测抬头行", "自测·抬头行")),
        "C6",
    )
    case(
        "T24 版本行 desc 用「、」分隔放行（C6·W841 防误伤）",
        lambda d: d.update(
            readme="> **当前批次 W999（2026-10-05）**：甲、乙、丙·A1-A6 共 50 篇\n",
            structure="> 当前批次：W999（2026-10-05）— 甲、乙、丙—A1-A6 共 50 篇\n",
            xiangmu="> 当前批次 W999（2026-10-05）：甲、乙、丙·详细变更见 CHANGELOG\n",
        ),
        "C6",
        expect_absent=True,
    )
    # W889：C7 主页展示位——`.github/README.md` 存在即抢占 GitHub 仓库主页
    case(
        "T25 主页展示位被抢必红（C7·W889）",
        lambda d: d.update(
            showcase={"root_readme": True, "github_readme": True, "docs_readme": False}),
        "C7",
    )
    case(
        "T26 主页展示位已改名则放行（C7·W889 防误伤）",
        lambda d: d.update(
            showcase={"root_readme": True, "github_readme": False, "docs_readme": True}),
        "C7",
        expect_absent=True,
    )

    fails = 0
    for name, mutate, expect_prefix, expect_absent in cases:
        data = dict(base)
        mutate(data)
        issues, _notes = evaluate(data)
        if expect_prefix is None:
            ok = not issues
        elif expect_absent:
            ok = not any(i.startswith(expect_prefix) for i in issues)
        else:
            ok = any(i.startswith(expect_prefix) for i in issues)
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            fails += 1
            for i in issues:
                print("      -> " + i)
    print("---- doc-sync self-test：%d/%d 通过 ----" % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


def main():
    if "--self-test" in sys.argv:
        return run_self_test()
    code, issues, notes = run_check()
    if "--json" in sys.argv:
        print(json.dumps({"issues": issues, "notes": notes}))
    return code


if __name__ == "__main__":
    sys.exit(main())
