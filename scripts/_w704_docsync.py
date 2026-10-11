# -*- coding: utf-8 -*-
"""W704 一次性编辑器：check_doc_sync.py 扩 C5b 数字实体标记对账 + C5c 裸聚合数字报告（用户方案第二阶段）。"""

import io

P = "scripts/check_doc_sync.py"
S = io.open(P, encoding="utf-8", newline="").read()


def rep(old, new, label):
    global S
    assert S.count(old) == 1, "%s :: 命中 %d" % (label, S.count(old))
    S = S.replace(old, new, 1)
    print("[OK] " + label)


# 1. docstring 更新
rep(
    "  C5 聚合数字对账（W703）：18 式高危聚合句式 × 现役叙述面（README/STRUCTURE/AGENTS/项目说明全文 +\n"
    "     CHANGELOG 仅「全站页数口径」块行）vs scripts/output/stats.json（scripts/stats.py 磁盘实算·tracked）；\n"
    "     基线/首跑等时点值靠句式表设计豁免（不进句式形态），新聚合量须先登记 stats.py 键表\n"
    "豁免：行级 <!--doc-sync:exempt 原因-->；.git/shallow 存在时 C4 跳过（pre-commit 本地为主执行点）。\n"
    "用法：--check（默认）只读校验，0 FAIL 才过；--self-test 注入式负样本 10 例（纯合成输入，不改真实文件）；",
    "  C5 聚合数字对账（W703 建·W704 实体化）：18 式高危聚合句式 × 现役叙述面（README/STRUCTURE/AGENTS/项目说明全文 +\n"
    "     CHANGELOG 仅「全站页数口径」块行）vs scripts/output/stats.json（scripts/stats.py 磁盘实算·实体化 tracked）；\n"
    "     C5b 数字实体标记：<!--stats:KEY--> 前置数字 == stats.json[KEY].value（键未登记=fail-closed）；\n"
    "     C5c 裸聚合数字：标记/句式覆盖外的 N[页项篇个类] 记 NOTE 报告型（起步策略·收敛后转 FAIL）；\n"
    "     基线/首跑等时点值靠句式表设计豁免（不进句式形态），新聚合量须先登记 stats.py META 键表\n"
    "豁免：行级 <!--doc-sync:exempt 原因-->；.git/shallow 存在时 C4 跳过（pre-commit 本地为主执行点）。\n"
    "用法：--check（默认）只读校验，0 FAIL 才过；--self-test 注入式负样本 12 例（纯合成输入，不改真实文件）；",
    "docstring C5b/C5c+12 例",
)

# 2. 常量：标记正则 + 裸数字正则
rep(
    'RE_CHANGELOG_SCOPE = re.compile(r"^> \\*\\*全站页数口径\\*\\*.*$", re.M)  # CHANGELOG 扫描域=口径块行',
    'RE_CHANGELOG_SCOPE = re.compile(r"^> \\*\\*全站页数口径\\*\\*.*$", re.M)  # CHANGELOG 扫描域=口径块行\n'
    'RE_STATS_MARK = re.compile(r"(\\d+)<!--stats:([a-z_0-9]+)-->")  # W704 数字实体标记（数字前置·key 后置·渲染隐藏）\n'
    'RE_BARE_AGG = re.compile(r"\\d+\\s*(?:页|项|篇|个|类)")  # C5c 裸聚合数字（报告型 NOTE·W704 起步）',
    "标记/裸数字正则",
)

# 3. stats_value helper（实体形态适配）
rep(
    "def line_has_exempt(text, match):",
    'def stats_value(stats, key):\n'
    '    """stats.json 实体形态（W704 {value,...}）兼容平面值（W703 过渡）。"""\n'
    "    e = stats.get(key)\n"
    "    return e.get(\"value\") if isinstance(e, dict) else e\n"
    "\n"
    "\n"
    "def line_has_exempt(text, match):",
    "stats_value helper",
)

# 4. C5a 循环内取值改 helper
rep(
    "                for gi, key_name in enumerate(keys, 1):\n"
    "                    want = stats.get(key_name)",
    "                for gi, key_name in enumerate(keys, 1):\n"
    "                    want = stats_value(stats, key_name)",
    "C5a 实体取值",
)

# 5. C5b/C5c 段（插在 C5a for 循环后、C5 issues 返回前）
rep(
    "                    elif got != want:\n"
    "                        issues.append(\n"
    '                            "C5: %s「%s」=%d ≠ stats.json %s=%d（跑 python scripts/stats.py 刷新或修正文档）"\n'
    "                            % (where, m.group(0), got, key_name, want)\n"
    "                        )\n"
    "    return issues, notes",
    "                    elif got != want:\n"
    "                        issues.append(\n"
    '                            "C5: %s「%s」=%d ≠ stats.json %s=%d（跑 python scripts/stats.py --w <批号> 刷新或修正文档）"\n'
    "                            % (where, m.group(0), got, key_name, want)\n"
    "                        )\n"
    "\n"
    "        # C5b 数字实体标记对账（W704）：<!--stats:KEY--> 前置数字 == stats.json[KEY].value；键未登记 fail-closed\n"
    "        # C5c 裸聚合数字（报告型 NOTE·标记/句式覆盖位之外·起步策略收敛后转 FAIL）\n"
    "        bare_hits = []\n"
    "        for where, ln in scans:\n"
    "            if EXEMPT_MARK in ln:\n"
    "                continue\n"
    "            covered = set()\n"
    "            for pat, keys, ctx in RE_STATS_PATTERNS:\n"
    "                for m in pat.finditer(ln):\n"
    "                    if not ctx or ctx in ln.lower():\n"
    "                        covered.update(range(m.start(), m.end()))\n"
    "            for m in RE_STATS_MARK.finditer(ln):\n"
    "                covered.update(range(m.start(), m.end()))\n"
    "                key_name = m.group(2)\n"
    "                want = stats_value(stats, key_name)\n"
    "                got = int(m.group(1))\n"
    "                if want is None:\n"
    '                    issues.append("C5b: %s 标记 <!--stats:%s--> 键未登记——先登记 scripts/stats.py META" % (where, key_name))\n'
    "                elif got != want:\n"
    "                    issues.append(\n"
    '                        "C5b: %s 标记数字 %d ≠ stats.json %s=%s（跑 python scripts/stats.py --w <批号> 刷新）"\n'
    "                        % (where, got, key_name, want)\n"
    "                    )\n"
    "            for m in RE_BARE_AGG.finditer(ln):\n"
    "                if m.start() not in covered:\n"
    '                    bare_hits.append("%s「%s」" % (where, m.group(0)))\n'
    "        if bare_hits:\n"
    "            notes.append(\n"
    '                "C5c: 裸聚合数字 %d 处未实体化（报告型·前 20）：%s%s"\n'
    '                % (len(bare_hits), "；".join(bare_hits[:20]), "…" if len(bare_hits) > 20 else "")\n'
    "            )\n"
    "    return issues, notes",
    "C5b/C5c 段",
)

# 6. self-test 合成 stats 实体形态
rep(
    '        "stats": {"gate_count": 31, "html_total": 100, "a1_a6_docs": 50, "methodology_docs": 6,\n'
    '                  "visualization_pages": 10, "csp_covered": 100, "scan_files": 100, "seo_scanned": 100,\n'
    '                  "inline_css_pages": 10, "json_count": 9, "script_classes": 34,\n'
    '                  "site_data_html": 10, "site_en_html": 10, "site_root_html": 10, "site_reader_html": 70},',
    '        "stats": {\n'
    '            k: {"value": v}\n'
    '            for k, v in {\n'
    '                "gate_count": 31, "html_total": 100, "a1_a6_docs": 50, "methodology_docs": 6,\n'
    '                "visualization_pages": 10, "csp_covered": 100, "scan_files": 100, "seo_scanned": 100,\n'
    '                "inline_css_pages": 10, "json_count": 9, "script_classes": 34,\n'
    '                "site_data_html": 10, "site_en_html": 10, "site_root_html": 10, "site_reader_html": 70,\n'
    '            }.items()\n'
    '        },',
    "self-test 合成 stats 实体形态",
)

# 7. self-test T11/T12
rep(
    '    case(\n'
    '        "T10 stats.json 缺失 fail-closed（C5）",\n'
    '        lambda d: d.update(stats=None),\n'
    '        "C5",\n'
    '    )',
    '    case(\n'
    '        "T10 stats.json 缺失 fail-closed（C5）",\n'
    '        lambda d: d.update(stats=None),\n'
    '        "C5",\n'
    '    )\n'
    '    case(\n'
    '        "T11 实体标记失配必红（C5b）",\n'
    '        lambda d: d.update(readme=d["readme"] + "HTML 共 200 页<!--stats:html_total-->\\n"),\n'
    '        "C5b",\n'
    '    )\n'
    '    case(\n'
    '        "T12 实体标记未登记键必红（C5b）",\n'
    '        lambda d: d.update(readme=d["readme"] + "共 9 个<!--stats:unknown_key-->\\n"),\n'
    '        "C5b",\n'
    '    )',
    "self-test T11/T12",
)

io.open(P, "w", encoding="utf-8", newline="").write(S)
print("ALL APPLIED")
