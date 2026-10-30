#!/usr/bin/env python3
"""check_script_coverage.py — 根级工具脚本覆盖门禁（第 42 槽 · W751 挂载）

## 为什么要这道门禁（W751 取证）

W751 前对 scripts/ 根级 101 个非 `_` 前缀脚本做覆盖普查（tests/ ∪ verify_delivery.py ∪
CI workflow ∪ Makefile 四面引用），结论 **46/101 无任何引用**——其中 `new_page.py`（可视化页
脚手架）/ `embed_json.py`（JSON 嵌入 HTML）/ `slice_screenshots.py`（截图切片）等直接生成或改写
站点产物的工具既无专项测试、也不被任何门禁点名。后果：脚手架生成的页面质量完全依赖人工，
没有自动化兜底。本门禁把「根级脚本必须有测试或被显式登记为不可单测」固化为机器防线，
只拦**新增漂移**（存量豁免走基线），形态与第 25/28/29 门禁同源（基线冻结·只增即 FAIL）。

## 覆盖口径（机器引用四面·任一即算被保护）

1. **测试面** `tests/**`（.py/.mjs/.js）——专项单测/E2E
2. **门禁面** `scripts/verify_delivery.py`——被门禁体系调用的脚本每次提交都真跑
3. **CI 面** `.github/workflows/*.yml`——被 workflow 调用的脚本每次推送都真跑
4. **编排面** `Makefile`——被 make 目标封装的脚本有人工入口

四面皆无 = 只能靠人记得跑：本门禁只拦这一类（含新增脚本与「原本有引用后被摘掉」的回归）。

## 判据（三条）

- C1 **覆盖**：每个根级脚本 ∈ 四面包裹集 ∪ 豁免集；两者皆非 = FAIL。
- C2 **基线有效**：豁免清单逐行存在于 scripts/、无重复——陈腐/重复行 = FAIL
  （防「脚本已删却仍挂豁免」的僵尸条目）。
- C3 **判据面非空**：根级脚本数 ≥ 50 · 覆盖集 ≥ 15 · 豁免集 ≥ 10（解析面塌陷 fail-closed，
  防「正则失效导致全量误红/全量豁免」的空真）。
- C4 **一次性脚本归位**（W1002 建·「脚本三档归位」的机器哨兵）：历史批（W 号 < 台账 max）的
  `_w####_*.py|js` 仍在 `scripts/` 根 = FAIL（应随批收官移入 `archive/scripts/batches/wNNN/`）。
  被四面引用的历史 `_` 件判为「转正候选」，允许 ≤ `MAX_RETAINED_UNDERSCORE` 件（棘轮·只降不升；
  W1003 起为 0——W977 的「硬保留 16 件」已全部转正或归档，不再有合法滞留）。超配额 = FAIL。
  台账不可读时 C4 跳过并打印 WARN（禁静默）。

## 豁免登记（scripts/output/script-coverage-baseline.txt）

一行一条，`#` 起首为注释；仅允许两类：
  ① 一次性/取证类（`_` 前缀已天然排除）——如 `acceptance_snapshot.py`（当批现测取证）
  ② 会话直接执行类（人在终端跑，无稳定 argv 契约）——如 `agent_start.py` / `review_sweep.py`
  ③ 产物/人工流程类——如 `gen_og_cover.py`（依赖人工审图）
**禁**把「懒得写测试」登记为豁免：基线行必须能被上表三类之一解释，新增行在 CHANGELOG 说明理由。

## 用法

  python scripts/check_script_coverage.py            # 门禁（exit 1 = 有 C1/C2 FAIL）
  python scripts/check_script_coverage.py --self-test  # 自检 6 例（5 负样本 + 1 好样本）
  python scripts/check_script_coverage.py --list       # 报告模式：打印覆盖/豁免/违例三清单（不判退出码）
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = HERE
BASELINE = os.path.join(SCRIPTS, "output", "script-coverage-baseline.txt")

# 覆盖口径四面（机器引用任一即算被保护）：测试 / 门禁 / CI / Makefile
TEST_DIRS = [os.path.join(ROOT, "tests")]
TEST_EXTS = {".py", ".mjs", ".js"}
GATE_FILE = os.path.join(SCRIPTS, "verify_delivery.py")
CI_DIR = os.path.join(ROOT, ".github", "workflows")
MAKEFILE = os.path.join(ROOT, "Makefile")

MIN_SCRIPTS = 50
MIN_COVERED = 15
MIN_BASELINE = 10
# C4 棘轮：被四面引用的历史批 `_` 件「转正候选」上限（只降不升）
# W1002 建时实测 8 件 → W1003 全部转正清零，配额随之收到 0（任何历史批 `_` 件留在根即红）
MAX_RETAINED_UNDERSCORE = 0
LEDGER = os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md")
DONE_PREFIXES = ("已收官", "已闭环")


def rd(p):
    with open(p, encoding="utf-8", errors="ignore") as f:
        return f.read()


def list_scripts():
    """根级非 `_` 前缀脚本（与 AGENTS §3「_*.py|js 不入库门禁/CI」口径一致）。"""
    out = []
    for name in sorted(os.listdir(SCRIPTS)):
        p = os.path.join(SCRIPTS, name)
        if not os.path.isfile(p):
            continue
        if name.startswith("_"):
            continue
        if os.path.splitext(name)[1] not in {".py", ".js"}:
            continue
        out.append(name)
    return out


def list_test_files():
    out = []
    for d in TEST_DIRS:
        for base, _dirs, files in os.walk(d):
            for f in files:
                if os.path.splitext(f)[1] in TEST_EXTS:
                    out.append(os.path.join(base, f))
    return sorted(out)


def reference_corpus():
    """四面引用文本：测试 ∪ 门禁 ∪ CI ∪ Makefile（缺失面静默跳过·不伪造）。"""
    parts = []
    for p in list_test_files():
        parts.append(rd(p))
    for p in [GATE_FILE, MAKEFILE]:
        if os.path.exists(p):
            parts.append(rd(p))
    if os.path.isdir(CI_DIR):
        for f in sorted(os.listdir(CI_DIR)):
            if f.endswith((".yml", ".yaml")):
                parts.append(rd(os.path.join(CI_DIR, f)))
    return "\n".join(parts)


def covered_set(scripts, corpus):
    """脚本是否被四面引用：命中 `名称` / `scripts/名称` / 模块名（去扩展）任一。

    用「带边界 token 出现」判定，不做语义解析——判据类门禁先做形态普查再写正则（W638 教训）。
    排除自引用：门禁脚本自身文本会命中自己的名字，由调用方从 corpus 语义上规避（本门禁自身
    只可能在测试面被引用，故自名不构成假覆盖——普查已实测 15→15 无自引用污染）。
    """
    hits = set()
    for name in scripts:
        stem = os.path.splitext(name)[0]
        pats = [
            r"(?<![\w.-])" + re.escape(name) + r"(?![\w-])",
            r"scripts/" + re.escape(name),
        ]
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", stem):
            pats.append(r"(?<![\w.])" + re.escape(stem) + r"(?![\w])")
        for pat in pats:
            if re.search(pat, corpus):
                hits.add(name)
                break
    return hits


def baseline_set(raw, scripts):
    """豁免清单：返回 (全部声明行, 已失效行)。

    行内 `#` 之后是分类注释（例如 `gen_rss.py  # ③发布链·gen_rss`），必须剥掉再比对脚本名——
    W751 首版漏剥，导致 35 行豁免全被当成「不存在于 scripts/」→ 门禁自伤 70 FAIL（已回归钉住）。
    """
    declared = []
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        name = s.split("#", 1)[0].strip()
        if name:
            declared.append(name)
    stale = [s for s in declared if s not in scripts]
    return declared, stale


def list_underscore_scripts():
    """根级 `_w####_` 一次性/批次脚本（C4 判据面·与 list_scripts 的排除口径互补）。"""
    out = []
    for name in sorted(os.listdir(SCRIPTS)):
        p = os.path.join(SCRIPTS, name)
        if not os.path.isfile(p) or os.path.splitext(name)[1] not in {".py", ".js"}:
            continue
        if re.match(r"^_w\d{3,4}_", name):
            out.append(name)
    return out


def ledger_max_w(path=None):
    """台账 max(W)——取号权威=表内 max（与 preflight.parse_ledger 同口径）。不可读 → None。"""
    p = path or LEDGER
    try:
        text = rd(p)
    except OSError:
        return None
    ws = [int(m) for m in re.findall(r"^\|\s*W(\d{3,4})\s*\|", text, re.M)]
    return max(ws) if ws else None


def inflight_wnums(path=None):
    """台账里**未收官**（在途）批号的集合——在途批的脚本留在根是合法的，C4 不判。

    为什么需要（W1006 实证）：后批一旦认领（max 前移），前批「还没收官」的脚本
    立即变成「历史批滞留」→ C4 误红，把合法在途当违规。判据必须以**状态列**为准，
    而不是只比 W 号大小。
    """
    p = path or LEDGER
    try:
        text = rd(p)
    except OSError:
        return set()
    out = set()
    for ln in text.split("\n"):
        m = re.match(r"^\|\s*W(\d{3,4})\s*\|", ln)
        if not m:
            continue
        cells = [re.sub(r"[\s*]+", "", c) for c in ln.strip().strip("|").split("|")]
        status = next((c for c in reversed(cells) if c.startswith(DONE_PREFIXES)), "")
        if not status.startswith(DONE_PREFIXES):
            out.add(int(m.group(1)))
    return out


def stray_batch_scripts(names, max_w, covered, inflight=frozenset()):
    """C4 分流：历史批（W < max_w）滞留件 → (必归档, 转正候选)。

    max_w 为 None（台账不可读）时返回空——判据不可执行不伪造红（由调用方打 WARN 留痕）。
    """
    if max_w is None:
        return [], []
    must_archive, promote = [], []
    for n in names:
        m = re.match(r"^_w(\d{3,4})_", n)
        if not m:
            continue
        w = int(m.group(1))
        if w >= max_w or w in inflight:
            continue
        (promote if n in covered else must_archive).append((n, w))
    return must_archive, promote


def c4_corpus():
    """C4 专用引用面：四面 ∪ 全部非 `_` 脚本 ∪ 治理文档（AGENTS/CLAUDE/docs/agent）。

    与 C1 的四面口径**故意不同**：C1 问「有没有测试/门禁/CI/Make 入口」，C4 问「是不是
    跨批/被治理面引用的活件」。被其它门禁脚本调用的 `_` 件（如 `check_page_admission.py`
    → `_w818_file_protocol_probe.py`）四面口径看不见，但确实是活件 ⇒ 判「转正候选」而非「死件归档」。
    """
    parts = [reference_corpus()]
    for name in sorted(os.listdir(SCRIPTS)):
        p = os.path.join(SCRIPTS, name)
        if os.path.isfile(p) and not name.startswith("_") and name.endswith((".py", ".js")):
            parts.append(rd(p))
    for p in [os.path.join(ROOT, "AGENTS.md"), os.path.join(ROOT, "CLAUDE.md")]:
        if os.path.exists(p):
            parts.append(rd(p))
    agent_dir = os.path.join(ROOT, "docs", "agent")
    if os.path.isdir(agent_dir):
        for f in sorted(os.listdir(agent_dir)):
            if f.endswith(".md"):
                parts.append(rd(os.path.join(agent_dir, f)))
    return "\n".join(parts)


def gate_mounted_set():
    """verify_delivery.py 里以 `script="xxx"` 字面挂载的脚本名集合（C2 反向查用）。

    fail-safe：读不到门禁本体返回空集（反向查不触发·绝不误伤）。仅认门禁硬挂载，
    不含 Makefile / preflight / 单测覆盖者——那些仍属「人跑轨」，留豁免合法。
    """
    try:
        text = rd(GATE_FILE)
    except OSError:
        return frozenset()
    return frozenset(re.findall(r'script="([^"]+)"', text))


def evaluate(inp):
    """纯函数判据（gather 注入实测 / self-test 注入构造），返回 issues 列表。"""
    issues = []
    scripts = inp["scripts"]
    corpus = inp["corpus_text"]
    declared, stale = baseline_set(inp["baseline_raw"], scripts)

    if len(scripts) < MIN_SCRIPTS:
        issues.append("C3: 根级脚本仅 %d < 下限 %d（解析面塌陷·fail-closed）" % (len(scripts), MIN_SCRIPTS))
    if not corpus.strip():
        issues.append("C3: 引用面文本为空（测试/门禁/CI/Makefile 四面均未读到内容·fail-closed）")
        return issues

    covered = covered_set(scripts, corpus)
    if len(covered) < MIN_COVERED:
        issues.append("C3: 覆盖集仅 %d < 下限 %d（解析面塌陷·fail-closed）" % (len(covered), MIN_COVERED))
    if len(declared) < MIN_BASELINE and not inp.get("_self_test"):
        issues.append("C3: 豁免集仅 %d < 下限 %d（基线疑似被清空·fail-closed）" % (len(declared), MIN_BASELINE))

    unknown = sorted(set(scripts) - covered - set(declared))
    for n in unknown:
        issues.append("C1: %s 四面无引用且不在豁免清单（新增脚本必须带测试/门禁/CI/Make 引用或登记豁免）" % n)

    dupes = sorted({d for d in declared if declared.count(d) > 1})
    for d in dupes:
        issues.append("C2: 豁免清单重复行 %s" % d)
    for s in stale:
        issues.append("C2: 豁免清单陈腐行 %s（scripts/ 下无此文件·删行或改回原名）" % s)
    # C2 反向查（W1014 接线升格）：已挂 verify 门禁槽的脚本不得仍留豁免——
    # 豁免表语义=「四面无引用·只能靠人记得跑」（文件头自述），挂槽即每次提交真跑，
    # 继续豁免会让登记面腐化（实证：check_gsap_motion.py W961 已挂第 50 槽，基线仍写
    # 「未挂 verify 槽」，原 C2 只拦「脚本已删」拦不住这类漂移）。仅取 verify 挂载集，
    # 不取整个覆盖集（Makefile/preflight 覆盖者仍属人跑轨，留豁免合法）。
    mounted = inp.get("gate_mounted", frozenset())
    for m in sorted(set(declared) & set(mounted)):
        issues.append("C2: 豁免清单与门禁挂载冲突 %s（已挂 verify 槽却仍豁免·删该行）" % m)

    # C4 一次性脚本归位（W1002）：历史批 `_w####_` 件不得滞留 scripts/ 根
    under = inp.get("underscore", [])
    if under:
        covered_under = covered_set(under, inp.get("c4_corpus_text") or corpus)
        must_archive, promote = stray_batch_scripts(under, inp.get("max_w"), covered_under,
                                                    inp.get("inflight", frozenset()))
        for n, w in must_archive:
            issues.append("C4: 历史批脚本滞留 scripts/ 根 %s（W%d < 台账 max W%s）——"
                          "按「脚本三档归位」移入 archive/scripts/batches/w%dxx/（无四面引用 ⇒ 非跨批判据）"
                          % (n, w, inp.get("max_w"), w // 100))
        if len(promote) > MAX_RETAINED_UNDERSCORE:
            issues.append("C4: 转正候选 %d 件 > 上限 %d（棘轮只降不升）——%s"
                          % (len(promote), MAX_RETAINED_UNDERSCORE,
                             ", ".join(sorted(n for n, _w in promote))))
    return issues


def gather():
    scripts = list_scripts()
    raw = rd(BASELINE) if os.path.exists(BASELINE) else ""
    return {"scripts": scripts, "corpus_text": reference_corpus(), "baseline_raw": raw,
            "underscore": list_underscore_scripts(), "max_w": ledger_max_w(),
            "inflight": inflight_wnums(), "gate_mounted": gate_mounted_set(),
            "c4_corpus_text": c4_corpus()}


def run_check():
    inp = gather()
    issues = evaluate(inp)
    for it in issues:
        print("FAIL  " + it)
    if inp.get("max_w") is None:
        print("WARN  C4 跳过：台账不可读（%s）——归位判据本回合不可执行" % os.path.relpath(LEDGER, ROOT))
    elif inp.get("underscore"):
        covered_under = covered_set(inp["underscore"], inp.get("c4_corpus_text") or inp["corpus_text"])
        _must, promote = stray_batch_scripts(inp["underscore"], inp["max_w"], covered_under,
                                             inp.get("inflight", frozenset()))
        if promote:
            print("NOTE  C4 转正候选（%d/%d）：%s——被四面引用，建议去 `_` 前缀转正"
                  % (len(promote), MAX_RETAINED_UNDERSCORE,
                     ", ".join(sorted(n for n, _w in promote))))
    print("---- 第 42 门禁 根级脚本覆盖：%d FAIL ----" % len(issues))
    return 1 if issues else 0


def run_list():
    inp = gather()
    declared, _stale = baseline_set(inp["baseline_raw"], inp["scripts"])
    covered = covered_set(inp["scripts"], inp["corpus_text"])
    unknown = sorted(set(inp["scripts"]) - covered - set(declared))
    print("== 根级脚本覆盖普查（报告模式·不判退出码）==")
    print("根级脚本 %d · 四面引用 %d · 豁免登记 %d · 无引用无豁免 %d"
          % (len(inp["scripts"]), len(covered), len(declared), len(unknown)))
    print("\n-- 无引用无豁免（%d）--" % len(unknown))
    for n in unknown:
        print("  " + n)
    print("\n-- 豁免登记（%d）--" % len(declared))
    for n in declared:
        print("  " + n)
    return 0


def run_self_test():
    """5 例：T1 干净态放行 / T2 新增无引用必红（C1）/ T3 基线陈腐必红（C2）/
    T4 引用面塌陷必红（C3）/ T5 带引用脚本放行（好样本·C1 不误报已覆盖项）。"""
    fill = ["fill%02d.py" % i for i in range(MIN_SCRIPTS)]
    dummy_scripts = ["alpha.py", "beta.py"] + fill
    dummy_declared = "\n".join(["# 注释"] + ["fill%02d.py" % i for i in range(MIN_BASELINE)])
    dummy_corpus = "\n".join(['GUARD = "alpha.py"', "import beta"] + fill)

    clean = {
        "scripts": dummy_scripts,
        "corpus_text": dummy_corpus,
        "baseline_raw": dummy_declared,
        "_self_test": True,
    }
    cases = []
    cases.append(("T1 干净态零误报", clean, None))
    cases.append(("T2 新增脚本四面无引用必红", dict(clean, scripts=dummy_scripts + ["brandnew.py"]), "C1"))
    cases.append(("T3 豁免清单陈腐行必红", dict(clean, baseline_raw=dummy_declared + "\ngone.py\n"), "C2"))
    cases.append(("T4 引用面塌陷必红", dict(clean, corpus_text=""), "C3"))
    cases.append(("T5 有引用脚本放行（好样本）", dict(clean, baseline_raw=dummy_declared), None))
    cases.append(("T6 带行内注释的登记行必须被正确解析（W751 自伤回归）",
                  dict(clean, baseline_raw="\n".join(["fill00.py  # ②会话直接执行"] + ["fill%02d.py" % i for i in range(1, MIN_BASELINE)])), None))
    # C4 一次性脚本归位（W1002）：历史批滞留 / 转正候选配额 / 当前批放行
    cases.append(("T7 历史批 `_` 件无引用滞留必红（C4）",
                  dict(clean, underscore=["_w0901_diag.py"], max_w=1002), "C4"))
    cases.append(("T8 当前批 `_` 件放行（C4 好样本）",
                  dict(clean, underscore=["_w1001_diag.py"], max_w=1001), None))
    nine = ["_w0901_p%d.py" % i for i in range(MAX_RETAINED_UNDERSCORE + 1)]
    cases.append(("T10 在途批脚本放行（C4 不误红合法在途）",
                  dict(clean, underscore=["_w1005_diag.py"], max_w=1006, inflight={1005}), None))
    cases.append(("T9 转正候选超配额必红（C4 棘轮）",
                  dict(clean, underscore=nine, max_w=1002, corpus_text=dummy_corpus + "\n" + "\n".join(nine)), "C4"))
    # C2 反向查（W1014）：已挂 verify 槽却仍豁免必红；仅 Makefile/引用覆盖者留豁免不误伤
    cases.append(("T11 已挂门禁槽却仍豁免必红（C2 反向查）",
                  dict(clean, gate_mounted={"fill00.py"}), "C2"))
    cases.append(("T12 覆盖但非门禁挂载者留豁免放行（C2 不误伤）",
                  dict(clean, gate_mounted={"alpha.py"}), None))

    fails = 0
    for name, inp, expect in cases:
        issues = evaluate(inp)
        ok = (not issues) if expect is None else any(i.startswith(expect) for i in issues)
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            fails += 1
            for i in issues[:5]:
                print("      -> " + i)
    print("---- script-coverage self-test：%d/%d 通过 ----" % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


CATEGORY_OF = {
    # ① 一次性/取证/人工审阅类
    "baseline_snapshot.py": "①取证快照",
    "build_reader.py": "①阅读器构建",
    "extract_datasets.js": "①数据集抽取",
    "extract_strings.py": "①字符串抽取",
    "gen_og_cover.py": "①OG 封面需人工审图",
    "inject_descriptions.py": "①批量注入·人工审形",
    "inject_rum.py": "①RUM 信标注入",
    "inject_visit_log.py": "①访问日志注入",
    "check_untracked.py": "①取证扫描",
    "archive_file.py": "①归档动作",
    "bump_footer_version.py": "①批量页脚版本",
    "source_collate.py": "①原文归集",
    "spot_check_nlp.py": "①NLP 抽查",
    "validate_en.py": "①英文站校验",
    "verify_chapters.py": "①分回校验",
    # ② 会话直接执行类（人在终端跑）
    "agent_start.py": "②开局摘要",
    "review_sweep.py": "②审查扫",
    "safe_commit.py": "②提交重试",
    "worktree_rehearse.py": "②worktree 预演",
    "fetch_gate_stats.py": "②取数",
    "judge_gate.py": "②取数后裁决",
    "perf_monitor.py": "②性能监控",
    "package_analysis_sync.py": "②分析包同步",
    # ③ 发布链/CI 编排类（由发布脚本或 workflow 成组调用）
    "gen_rss.py": "③发布链·gen_rss",
    "inject_chart_a11y.py": "③发布链·a11y 注入",
    "inject_goatcounter.py": "③发布链·计数注入",
    "inject_seo_head.py": "③发布链·SEO 注入",
    "sync_data_json.py": "③发布链·数据同步",
    "check_dual_source_scan.py": "③双源扫描（报告型）",
    # ④ 浏览器/布局类（需真实渲染环境）
    "debug_page.js": "④浏览器调试",
    "diagnose_overflow.js": "④溢出诊断",
    "render_check.js": "④渲染检查",
    "verify_v2_pages.js": "④V2 页面检查",
    "agg_entities.py": "④实体聚合（由数据管线调用）",
    # 后续批次新增脚本（未覆盖时在此登记并注明类别；同批必须给出上面的四类理由）
    "check_chart_values.js": "④浏览器渲染断言（需真实 Chromium·由 pytest 逻辑层与 verify 第 43 槽覆盖）",
    "backfill_changelog.py": "②应急补段（版段递延链断裂时人工触发·非常规流程·W842 建）",
    "reserve_w.py": "②开批占号助手（reserve/list/release 三模式·W1041 建）",
}


def run_save_baseline():
    """把「四面无引用」的现存脚本写成带分类注释的豁免基线。

    人工复核要求：每一行都必须能归入 CATEGORY_OF 的四类之一；未分类的脚本不写进基线
    （留在 FAIL 里促补引用），**禁止直接留白**（豁免不是垃圾桶）。
    """
    inp = gather()
    covered = covered_set(inp["scripts"], inp["corpus_text"])
    unknown = sorted(set(inp["scripts"]) - covered)
    unclassified = [n for n in unknown if n not in CATEGORY_OF]
    if unclassified:
        print("以下脚本四面无引用且未分类，需补引用或先登记分类：")
        for n in unclassified:
            print("  " + n)
        return 2
    header = [
        "# 根级脚本覆盖豁免基线（第 42 门禁 · W751 建）",
        "# 一行一条：<脚本名>  # <分类>",
        "# 语义：这些脚本四面（tests / verify_delivery / CI / Makefile）无引用，属「只能靠人记得跑」类。",
        "# 生成：python scripts/check_script_coverage.py --save-baseline（分类在脚本 CATEGORY_OF 内维护）",
        "# 四类：①一次性/取证/人工审阅 ②会话直接执行（人在终端跑）③发布链/CI 编排（成组调用）",
        "#       ④浏览器/布局（需真实渲染环境）；新增脚本必须带引用或显式登记并注明类别。",
        "# 陈腐行（脚本已删）由门禁 C2 拦下；豁免行数下限由 C3 兜住。",
        "",
    ]
    body = ["%s  # %s" % (n, CATEGORY_OF[n]) for n in unknown]
    os.makedirs(os.path.dirname(BASELINE), exist_ok=True)
    with open(BASELINE, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(header + body) + "\n")
    print("已写入 %s：豁免 %d 条（四面引用 %d 条已受保护）"
          % (os.path.relpath(BASELINE, ROOT), len(unknown), len(covered)))
    for line in body:
        print("  " + line)
    return 0


def main():
    if "--self-test" in sys.argv:
        return run_self_test()
    if "--list" in sys.argv:
        return run_list()
    if "--save-baseline" in sys.argv:
        return run_save_baseline()
    return run_check()


if __name__ == "__main__":
    sys.exit(main())
