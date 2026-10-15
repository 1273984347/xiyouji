"""W703 一次性编辑器：check_doc_sync.py 扩 C5 聚合数字对账（用户方案 A+C 修正形态）。"""


P = "scripts/check_doc_sync.py"
S = open(P, encoding="utf-8", newline="").read()
crlf = "\r\n" in S


def rep(old, new, label):
    global S
    o, n = (old.replace("\n", "\r\n"), new.replace("\n", "\r\n")) if crlf else (old, new)
    assert S.count(o) == 1, "%s :: 命中 %d" % (label, S.count(o))
    S = S.replace(o, n, 1)
    print("[OK] " + label)


# 1. docstring：C5 条目 + 例数
rep(
    "  C4 提交-版段对账：近 15 条 commit subject 中的 W### ⊆ CHANGELOG 版段集合 ∪ 对账表登记行\n"
    "豁免：行级 <!--doc-sync:exempt 原因-->；.git/shallow 存在时 C4 跳过（pre-commit 本地为主执行点）。\n"
    "用法：--check（默认）只读校验，0 FAIL 才过；--self-test 注入式负样本 7 例（纯合成输入，不改真实文件）；",
    "  C4 提交-版段对账：近 15 条 commit subject 中的 W### ⊆ CHANGELOG 版段集合 ∪ 对账表登记行\n"
    "  C5 聚合数字对账（W703）：18 式高危聚合句式 × 现役叙述面（README/STRUCTURE/AGENTS/项目说明全文 +\n"
    "     CHANGELOG 仅「全站页数口径」块行）vs scripts/output/stats.json（scripts/stats.py 磁盘实算·tracked）；\n"
    "     基线/首跑等时点值靠句式表设计豁免（不进句式形态），新聚合量须先登记 stats.py 键表\n"
    "豁免：行级 <!--doc-sync:exempt 原因-->；.git/shallow 存在时 C4 跳过（pre-commit 本地为主执行点）。\n"
    "用法：--check（默认）只读校验，0 FAIL 才过；--self-test 注入式负样本 10 例（纯合成输入，不改真实文件）；",
    "docstring C5+10 例",
)

# 2. 常量：句式表 + 口径块行
rep(
    'EXEMPT_MARK = "<!--doc-sync:exempt"',
    'RE_STATS_PATTERNS = [  # (正则, (键...), 语境词[None=无·小写包含判定]) —— 键值与 scripts/output/stats.json 对账\n'
    '    (re.compile(r"HTML 共 (\\d+) 页"), ("html_total",), None),\n'
    '    (re.compile(r"site/data (\\d+) \\+ site/en (\\d+) \\+ site 根 (\\d+) \\+ site/reader (\\d+)"),\n'
    '     ("site_data_html", "site_en_html", "site_root_html", "site_reader_html"), None),\n'
    '    (re.compile(r"CSP 覆盖 (\\d+) 页"), ("csp_covered",), None),\n'
    '    (re.compile(r"(\\d+) 页哈希 0 漂移"), ("csp_covered",), None),\n'
    '    (re.compile(r"扫 (\\d+) 文件"), ("scan_files",), None),\n'
    '    (re.compile(r"(\\d+) 页扫描"), ("seo_scanned",), "seo"),\n'
    '    (re.compile(r"扫 (\\d+) 页"), ("seo_scanned",), "seo"),\n'
    '    (re.compile(r"同步 (\\d+) 页"), ("inline_css_pages",), None),\n'
    '    (re.compile(r"(\\d+) 个[^，。）]*?可视化页"), ("visualization_pages",), None),\n'
    '    (re.compile(r"(\\d+) 可视化页"), ("visualization_pages",), None),\n'
    '    (re.compile(r"(\\d+) 项自动化门禁"), ("gate_count",), None),\n'
    '    (re.compile(r"共 (\\d+) 篇"), ("a1_a6_docs",), None),\n'
    '    (re.compile(r"已建 (\\d+) 篇"), ("methodology_docs",), "方法论"),\n'
    '    (re.compile(r"(\\d+) 个 JSON 文件"), ("json_count",), None),\n'
    '    (re.compile(r"site/data/ 共 (\\d+) 个 HTML"), ("site_data_html",), None),\n'
    '    (re.compile(r"A-AH (\\d+) 类"), ("script_classes",), None),\n'
    '    (re.compile(r"按 (\\d+) 类组织"), ("script_classes",), None),\n'
    '    (re.compile(r"(\\d+) 类子目录全建"), ("script_classes",), None),\n'
    ']\n'
    'RE_CHANGELOG_SCOPE = re.compile(r"^> \\*\\*全站页数口径\\*\\*.*$", re.M)  # CHANGELOG 扫描域=口径块行\n'
    'C5_DOC_NAMES = {"readme": "README.md", "structure": "STRUCTURE.md", "agents": "AGENTS.md", "xiangmu": "项目说明.md"}\n'
    'EXEMPT_MARK = "<!--doc-sync:exempt"',
    "句式表+扫描域常量",
)

# 3. evaluate() 加 C5 段（C4 之后 return 之前）
rep(
    '                if w not in reg:\n'
    '                    issues.append("C4: 提交「%s」的 W%s 无 CHANGELOG 版段且未在对账表登记" % (s[:60], w))\n'
    '    return issues, notes',
    '                if w not in reg:\n'
    '                    issues.append("C4: 提交「%s」的 W%s 无 CHANGELOG 版段且未在对账表登记" % (s[:60], w))\n'
    '\n'
    '    # C5 聚合数字对账（W703·用户方案 A+C 修正形态）：句式白名单 × 现役叙述面 vs stats.json\n'
    '    stats = inp.get("stats")\n'
    '    if not stats:\n'
    '        issues.append("C5: scripts/output/stats.json 缺失或不可解析——先跑 python scripts/stats.py（fail-closed）")\n'
    '    else:\n'
    '        scans = [("CHANGELOG 口径块", ln) for ln in RE_CHANGELOG_SCOPE.findall(inp["changelog"])]\n'
    '        for key in C5_DOC_NAMES:\n'
    '            for i, ln in enumerate(inp[key].splitlines(), 1):\n'
    '                scans.append(("%s:%d" % (C5_DOC_NAMES[key], i), ln))\n'
    '        for where, ln in scans:\n'
    '            if EXEMPT_MARK in ln:\n'
    '                continue\n'
    '            for pat, keys, ctx in RE_STATS_PATTERNS:\n'
    '                m = pat.search(ln)\n'
    '                if not m or (ctx and ctx not in ln.lower()):\n'
    '                    continue\n'
    '                for gi, key_name in enumerate(keys, 1):\n'
    '                    want = stats.get(key_name)\n'
    '                    got = int(m.group(gi))\n'
    '                    if want is None:\n'
    '                        issues.append(\n'
    '                            "C5: stats.json 缺键 %s（%s 命中「%s」）——新聚合量须先登记 scripts/stats.py"\n'
    '                            % (key_name, where, m.group(0))\n'
    '                        )\n'
    '                    elif got != want:\n'
    '                        issues.append(\n'
    '                            "C5: %s「%s」=%d ≠ stats.json %s=%d（跑 python scripts/stats.py 刷新或修正文档）"\n'
    '                            % (where, m.group(0), got, key_name, want)\n'
    '                        )\n'
    '    return issues, notes',
    "evaluate C5 段",
)

# 4. gather() 加 structure/xiangmu/stats
rep(
    '        "agents": rd(os.path.join(ROOT, "AGENTS.md")),\n'
    '        "verify_src": rd(os.path.join(HERE, "verify_delivery.py")),',
    '        "agents": rd(os.path.join(ROOT, "AGENTS.md")),\n'
    '        "structure": rd(os.path.join(ROOT, "STRUCTURE.md")),\n'
    '        "xiangmu": rd(os.path.join(ROOT, "docs", "00-导读", "项目说明.md")),\n'
    '        "verify_src": rd(os.path.join(HERE, "verify_delivery.py")),\n'
    '        "stats": _load_stats(),',
    "gather 新输入",
)
rep(
    'def gather():\n    def rd(p):',
    'def _load_stats():\n'
    '    try:\n'
    '        with open(os.path.join(ROOT, "scripts", "output", "stats.json"), encoding="utf-8") as f:\n'
    '            return json.load(f)\n'
    '    except (OSError, ValueError):\n'
    '        return None\n'
    '\n'
    '\n'
    'def gather():\n    def rd(p):',
    "_load_stats helper",
)

# 5. 汇总行加 C5
rep(
    '        "---- 第 31 门禁 文档口径体检：%d FAIL · %d NOTE（C1 README 抬头 / C2 交接头链 / C3 门禁清单上限 / C4 提交-版段对账）----"',
    '        "---- 第 31 门禁 文档口径体检：%d FAIL · %d NOTE（C1 README 抬头 / C2 交接头链 / C3 门禁清单上限 / C4 提交-版段对账 / C5 聚合数字对账）----"',
    "汇总行 C5",
)

# 6. self-test：base 补输入 + T8/T9/T10 三例
rep(
    '        "shallow": False,\n    }\n    cases = []',
    '        "structure": "",\n'
    '        "xiangmu": "",\n'
    '        "stats": {"gate_count": 31, "html_total": 100, "a1_a6_docs": 50, "methodology_docs": 6,\n'
    '                  "visualization_pages": 10, "csp_covered": 100, "scan_files": 100, "seo_scanned": 100,\n'
    '                  "inline_css_pages": 10, "json_count": 9, "script_classes": 34,\n'
    '                  "site_data_html": 10, "site_en_html": 10, "site_root_html": 10, "site_reader_html": 70},\n'
    '        "shallow": False,\n    }\n    cases = []',
    "self-test base 补输入",
)
rep(
    '    case("T7 干净输入零误报", lambda d: None)',
    '    case("T7 干净输入零误报", lambda d: None)\n'
    '    case(\n'
    '        "T8 聚合数字失配必红（C5）",\n'
    '        lambda d: d.update(readme=d["readme"] + "每次提交需通过 99 项自动化门禁\\n"),\n'
    '        "C5",\n'
    '    )\n'
    '    case(\n'
    '        "T9 聚合数字行级豁免放行（C5）",\n'
    '        lambda d: d.update(\n'
    '            readme=d["readme"] + "每次提交需通过 99 项自动化门禁 <!--doc-sync:exempt 自测豁免-->\\n"\n'
    '        ),\n'
    '        "C5",\n'
    '        expect_absent=True,\n'
    '    )\n'
    '    case(\n'
    '        "T10 stats.json 缺失 fail-closed（C5）",\n'
    '        lambda d: d.update(stats=None),\n'
    '        "C5",\n'
    '    )',
    "self-test T8/T9/T10",
)

open(P, "w", encoding="utf-8", newline="").write(S)
print("ALL APPLIED")
