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
    return issues


def gather():
    scripts = list_scripts()
    raw = rd(BASELINE) if os.path.exists(BASELINE) else ""
    return {"scripts": scripts, "corpus_text": reference_corpus(), "baseline_raw": raw}


def run_check():
    inp = gather()
    issues = evaluate(inp)
    for it in issues:
        print("FAIL  " + it)
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
