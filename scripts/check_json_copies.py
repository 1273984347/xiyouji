#!/usr/bin/env python3
"""check_json_copies.py — 第 81 门禁 · 页面引用 → 已部署 闭合性（W1265 批一·判据补盲 1-10）

原职责（W563/A-3·旧名 scripts/_check_json_copies.py）：site/data/json/ 部署副本 ↔ scripts/output/data/ 原件对账。
  断言：部署副本逐一字节相等（副本数不再硬断言·部署面随批增长）。
  （第 9 门禁的副本对账子检查只比数组长度＝CI 跨平台安全版；**字节级强对账由本脚本承担**·
  W770 自 archive 恢复——W770 实证：副本曾含 W678/W691 修复而原件未回灌。）

新增职责（W1265 批一 · 判据补盲 1-10）：**页面引用 → 已部署**闭合性校验。
  背景（《全站网页可视化图表审查报告 2026-11-16 · W1259》P2-5）：页面在 http 下会 fetch
  部署副本；副本不存在 ⇒ 404 ⇒ 页面**静默回退**内嵌数据（用户以为看到实时数据，实际全部落空）。
  真值原件 135 件·审查时仅部署 47 件 ⇒ 88 件从未部署；旧口径只对账「副本 ↔ 原件」，
  不检查「页面引用的目标是否已部署」⇒ 全站漏检。

  判据 C1：页面 JSON 装载目标（http 语义解析后）必须存在于部署面。
    口径：目标 = (fetch | d3.json | loadJson | load_json | fetchJSON | fetchJson | getJSON) 的
          **第一个实参**（含路径常量 + 文件名表的动态拼接解析·见 scripts/lib/json_refs.py）；
          http 语义：页面 site/en/x.html 引用 '../data/json/y.json' → /data/json/y.json，
          以 site/ 为站根解析；目标不存在 ⇒ 违例。

模式：门禁默认「基线冻结」（基线内记「存量基线」不计 FAIL·基线外新增 = FAIL）；
      零容忍 --strict；报告档 --report（退出码 0）；基线生成 --generate-baseline。
用法：py -3 scripts/check_json_copies.py [--strict|--report|--generate-baseline|--self-test]
      py -3 scripts/check_json_copies.py --closure-only   # 只判闭合面（副本对账另跑）
"""
from __future__ import annotations

import filecmp
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from lib import freeze_gate, json_refs  # noqa: E402

SRC = ROOT / "scripts" / "output" / "data"
DST = ROOT / "site" / "data" / "json"
MARKER = "---- 第 81 门禁 页面引用闭合性："
CLOSURE_BASELINE = ROOT / "scripts" / "output" / "fetch-closure-baseline.txt"
SCAN_DIRS = ("site/data", "site/en")
SKIP_STEMS = ("_shell", "_template")


def copy_reconciliation() -> list[str]:
    """原 W563 职责：部署副本 ↔ 原件字节级对账。"""
    problems: list[str] = []
    if not DST.is_dir():
        return ["部署副本目录缺失: %s" % DST]
    copies = sorted(f for f in os.listdir(DST) if f.endswith(".json"))
    for f in copies:
        src = SRC / f
        if not src.exists():
            problems.append("副本无原件: " + f)
        elif not filecmp.cmp(str(DST / f), str(src), shallow=False):
            problems.append("内容漂移: " + f)
    return problems


def closure_violations() -> tuple[list[str], int, int]:
    """C1：页面引用 → 已部署闭合性。返回 (违例键, 目标总数, 未解析实参数)。"""
    viol: list[str] = []
    total = 0
    unresolved = 0
    for d in SCAN_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for f in sorted(base.glob("*.html")):
            if f.stem in SKIP_STEMS:
                continue
            page_rel = d + "/" + f.name
            html = f.read_text(encoding="utf-8", errors="ignore")
            targets, unres = json_refs.extract_targets(html)
            unresolved += len([u for u in unres if ".json" in u or u.isidentifier()])
            for target, rule in targets:
                total += 1
                resolved = json_refs.norm_path(json_refs.resolve_http_path(page_rel, target))
                cand = ROOT / resolved
                if not cand.is_file():
                    viol.append("%s|%s|%s（解析后 %s·未部署）" % (page_rel, rule, target, resolved))
    root_dir = ROOT / "site"
    for f in sorted(root_dir.glob("*.html")):
        page_rel = "site/" + f.name
        html = f.read_text(encoding="utf-8", errors="ignore")
        targets, unres = json_refs.extract_targets(html)
        unresolved += len([u for u in unres if ".json" in u or u.isidentifier()])
        for target, rule in targets:
            total += 1
            resolved = json_refs.norm_path(json_refs.resolve_http_path(page_rel, target))
            if not (ROOT / resolved).is_file():
                viol.append("%s|%s|%s（解析后 %s·未部署）" % (page_rel, rule, target, resolved))
    return viol, total, unresolved


def self_test() -> int:
    """负样本自测：闭合性违例必红·可达目标必绿·基线语义正确。"""
    import tempfile

    bad = 0
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        (tmp / "site" / "en").mkdir(parents=True)
        (tmp / "site" / "data" / "json").mkdir(parents=True)
        (tmp / "site" / "data" / "json" / "ok.json").write_text("{}", encoding="utf-8")
        (tmp / "site" / "en" / "a.html").write_text(
            "<script>fetch('../data/json/ok.json');fetch('../data/json/missing.json');</script>", encoding="utf-8"
        )
        html = (tmp / "site" / "en" / "a.html").read_text(encoding="utf-8")
        targets, _ = json_refs.extract_targets(html)
        reach = 0
        miss = 0
        for target, _rule in targets:
            resolved = json_refs.norm_path(json_refs.resolve_http_path("site/en/a.html", target))
            if (tmp / resolved).is_file():
                reach += 1
            else:
                miss += 1
        ok = reach == 1 and miss == 1
        print("%s 负样本-已部署目标可达 + 未部署目标判红（可达 %d·不可达 %d）" % ("OK  " if ok else "FAIL", reach, miss))
        bad += 0 if ok else 1

        html2 = '<script>const D="../data/json/";const F={a:"ok.json"};fetch(D+f);</script>'
        t2, _ = json_refs.extract_targets(html2)
        ok = len(t2) == 1 and t2[0][0] == "../data/json/ok.json"
        print("%s 动态拼接目标解析（%s）" % ("OK  " if ok else "FAIL", t2))
        bad += 0 if ok else 1

    viol = ["site/en/a.html|L1|../data/json/missing.json（解析后 site/data/json/missing.json·未部署）"]
    res = freeze_gate.evaluate(viol, set(viol), strict=False)
    ok = not res["new_fail"] and len(res["frozen"]) == 1
    print("%s 基线内违例不计 FAIL（frozen=%d）" % ("OK  " if ok else "FAIL", len(res["frozen"])))
    bad += 0 if ok else 1
    res = freeze_gate.evaluate(viol, set(), strict=False)
    ok = len(res["new_fail"]) == 1
    print("%s 基线外新增违例计 FAIL（new_fail=%d）" % ("OK  " if ok else "FAIL", len(res["new_fail"])))
    bad += 0 if ok else 1
    res = freeze_gate.evaluate(viol, set(viol), strict=True)
    ok = len(res["new_fail"]) == 1
    print("%s 零容忍模式存量全红（new_fail=%d）" % ("OK  " if ok else "FAIL", len(res["new_fail"])))
    bad += 0 if ok else 1
    print("自测 %d/5 通过" % (5 - bad))
    return 0 if bad == 0 else 2


def main() -> int:
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return self_test()

    strict = "--strict" in argv
    report_only = "--report" in argv
    closure_only = "--closure-only" in argv

    problems = [] if closure_only else copy_reconciliation()
    copies = len([f for f in os.listdir(DST) if f.endswith(".json")]) if DST.is_dir() else 0
    viol, total, unresolved = closure_violations()

    if "--generate-baseline" in argv:
        n = freeze_gate.write_baseline(
            CLOSURE_BASELINE,
            viol,
            [
                "# 第 81 门禁 · 页面引用闭合性基线（W1265 建立·存量违例冻结）",
                "# 生成命令：py -3 scripts/check_json_copies.py --generate-baseline",
                "# 格式：<页面>|<解析规则>|<目标>|<细节>；解析规则 L1=字面量·L2..L5=动态拼接",
                "# 语义：基线内违例记「存量基线」不计 FAIL；基线外新增 = FAIL；零容忍：--strict",
            ],
        )
        print("基线已写入 %s（%d 条）" % (CLOSURE_BASELINE, n))
        return 0

    baseline, baseline_problems = freeze_gate.read_baseline(CLOSURE_BASELINE)
    if baseline_problems and not report_only:
        for p in baseline_problems:
            print("FAIL " + p)
        print("%s 基线缺失/不可读·fail-closed·拒绝通过 ----" % MARKER)
        return 1
    if baseline_problems:
        baseline = set()

    res = freeze_gate.evaluate(viol, baseline, strict=strict)
    print("副本对账：副本 %d 个 · 问题 %d 条" % (copies, len(problems)))
    for p in problems[:10]:
        print("  FAIL " + p)
    print("页面引用闭合性：扫描目标 %d 个 · 不可达 %d 条 · 违例页 %d 页 · 未解析实参 %d 个"
          % (total, len(viol), len({v.split("|")[0] for v in viol}), unresolved))
    freeze_gate.print_eval(res, MARKER, strict=strict)
    print("%s ----" % MARKER)
    fail_count = len(res["new_fail"]) + len(problems)
    if report_only:
        return 0
    return 1 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())
