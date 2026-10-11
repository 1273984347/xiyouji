#!/usr/bin/env python3
"""文档口径体检 doc-sync（第 31 门禁 · W663）——代码/提交是真值源，文档当前态声明是派生物。

移植自 GateKeeper / 千问大赛仓 doc-sync 机制（W663 经验移植批；D2 裁决：对账表登记即豁免）。
四类窄句式白名单（宁窄勿误，防误伤历史叙述——历史段/方案档/复盘档一律不进扫描面）：
  C1 README 抬头「当前版本 vX（日期）**： W###」 ≡ CHANGELOG 顶段三元组
  C2 交接文档头链链首「- **vX W###」 ≡ CHANGELOG 顶段（v + W）
  C3 AGENTS §4.2 门禁清单最高编号 == verify_delivery.py 实况最高槽位
  C4 提交-版段对账：近 15 条 commit subject 中的 W### ⊆ CHANGELOG 版段集合 ∪ 对账表登记行
  C5 聚合数字对账（W703 建·W704 实体化）：18 式高危聚合句式 × 现役叙述面（README/STRUCTURE/AGENTS/项目说明全文 +
     CHANGELOG 仅「全站页数口径」块行）vs scripts/output/stats.json（scripts/stats.py 磁盘实算·实体化 tracked）；
     C5b 数字实体标记：<!--stats:KEY--> 前置数字 == stats.json[KEY].value（键未登记=fail-closed）；
     C5c 裸聚合数字：标记/句式覆盖外的 N[页项篇个类] 记 NOTE 报告型（起步策略·收敛后转 FAIL）；
     基线/首跑等时点值靠句式表设计豁免（不进句式形态），新聚合量须先登记 stats.py META 键表
豁免：行级 <!--doc-sync:exempt 原因-->；.git/shallow 存在时 C4 跳过（pre-commit 本地为主执行点）。
用法：--check（默认）只读校验，0 FAIL 才过；--self-test 注入式负样本 12 例（纯合成输入，不改真实文件）；
     --json 供 CI 消费。本脚本绝不修改任何文件。
"""

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
RE_STATS_MARK = re.compile(r"(\d+)\s*[页项篇个类]?\s*<!--stats:([a-z_0-9]+)-->")  # W704 数字实体标记（紧贴/句尾双形态·key 后置·渲染隐藏）
RE_BARE_AGG = re.compile(r"\d+\s*(?:页|项|篇|个|类)")  # C5c 裸聚合数字（报告型 NOTE·W704 起步）
C5_DOC_NAMES = {"readme": "README.md", "structure": "STRUCTURE.md", "agents": "AGENTS.md", "xiangmu": "项目说明.md", "contributing": "CONTRIBUTING.md"}  # W713 补 CONTRIBUTING（第 27 门禁叙述面已含·C5 面对齐）
EXEMPT_MARK = "<!--doc-sync:exempt"
ARCHIVE_CHANGELOGS = [
    os.path.join(ROOT, "docs", "archive", "CHANGELOG-ARCHIVE.md"),
    os.path.join(ROOT, "docs", "archive", "CHANGELOG-ARCHIVE-tier2.md"),
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


def evaluate(inp):
    """纯函数核对：inputs 为注入真值与文档文本的 dict，返回 (issues, notes)。

    issues 元素以 C1:/C2:/C3:/C4: 前缀定性，供 --self-test 断言。
    """
    issues, notes = [], []
    top = changelog_top(inp["changelog"])
    if not top:
        issues.append("C1: CHANGELOG 未解析出现役顶段（期望 ### W###（日期）：标题 或历史 ### vX.Y.Z（日期）：W###）")
        top = ("?", "?")
    date, wnum = top

    # C1 README 抬头二元组（date+W·W711 双形态）
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

    # C2 交接文档头链链首
    m2 = RE_JIAOJIE_HEAD.search(inp["jiaojie"])
    if not m2:
        issues.append("C2: 交接文档未解析出头链链首「- **W###」")
    elif line_has_exempt(inp["jiaojie"], m2):
        notes.append("C2: 交接头链行带 doc-sync:exempt 豁免，跳过")
    elif int(m2.group(1)) != wnum:
        issues.append(
            "C2: 交接头链 W%s ≠ CHANGELOG 顶段 W%s" % (m2.group(1), wnum)
        )

    # C3 AGENTS §4.2 门禁清单上限 == verify 实况最高槽位
    a_max = agents_gate_list_max(inp["agents"])
    v_max = verify_slot_max(inp["verify_src"])
    if a_max is None or v_max is None:
        issues.append("C3: 解析失败（AGENTS §4.2 清单=%s / verify 槽位=%s·fail-closed）" % (a_max, v_max))
    elif a_max != v_max:
        issues.append("C3: AGENTS §4.2 门禁清单止于 %d，verify 实况最高槽位 %d（声明落后于代码实况）" % (a_max, v_max))

    # C4 提交-版段对账（D2：对账表登记即豁免）
    if inp.get("shallow"):
        notes.append("C4: 浅克隆环境（.git/shallow），提交对账跳过（pre-commit 本地为主执行点）")
    else:
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

    # C5 聚合数字对账（W703·用户方案 A+C 修正形态）：句式白名单 × 现役叙述面 vs stats.json
    stats = inp.get("stats")
    if not stats:
        issues.append("C5: scripts/output/stats.json 缺失或不可解析——先跑 python scripts/stats.py（fail-closed）")
    else:
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
        # C5c 裸聚合数字（报告型 NOTE·标记/句式覆盖位之外·起步策略收敛后转 FAIL）
        bare_hits = []
        for where, ln in scans:
            if EXEMPT_MARK in ln:
                continue
            covered = set()
            for pat, _keys, ctx in RE_STATS_PATTERNS:
                for m in pat.finditer(ln):
                    if not ctx or ctx in ln.lower():
                        covered.update(range(m.start(), m.end()))
            for m in RE_STATS_MARK.finditer(ln):
                covered.update(range(m.start(), m.end()))
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
            for m in RE_BARE_AGG.finditer(ln):
                if m.start() not in covered:
                    bare_hits.append("%s「%s」" % (where, m.group(0)))
        if bare_hits:
            notes.append(
                "C5c: 裸聚合数字 %d 处未实体化（报告型·前 20）：%s%s"
                % (len(bare_hits), "；".join(bare_hits[:20]), "…" if len(bare_hits) > 20 else "")
            )
    return issues, notes


def _load_stats():
    try:
        with open(os.path.join(ROOT, "scripts", "output", "stats.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def gather():
    def rd(p):
        with open(p, encoding="utf-8") as f:
            return f.read()

    inputs = {
        "changelog": rd(os.path.join(ROOT, "CHANGELOG.md")),
        "readme": rd(os.path.join(ROOT, "README.md")),
        "jiaojie": rd(os.path.join(ROOT, "交接文档.md")),
        "agents": rd(os.path.join(ROOT, "AGENTS.md")),
        "structure": rd(os.path.join(ROOT, "STRUCTURE.md")),
        "xiangmu": rd(os.path.join(ROOT, "docs", "00-导读", "项目说明.md")),
        "contributing": rd(os.path.join(ROOT, "CONTRIBUTING.md")),
        "verify_src": rd(os.path.join(HERE, "verify_delivery.py")),
        "stats": _load_stats(),
        "table": rd(os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md")),
        "subjects": [],
        "shallow": os.path.exists(os.path.join(ROOT, ".git", "shallow")),
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
        "---- 第 31 门禁 文档口径体检：%d FAIL · %d NOTE（C1 README 抬头 / C2 交接头链 / C3 门禁清单上限 / C4 提交-版段对账 / C5 聚合数字对账）----"
        % (len(issues), len(notes))
    )
    return (1 if issues else 0), issues, notes


def run_self_test():
    """7 例注入式负样本/正样本（纯合成输入，不改真实文件）。"""
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
