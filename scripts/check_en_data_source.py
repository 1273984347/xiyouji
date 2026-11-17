#!/usr/bin/env python3
"""check_en_data_source.py — 第 78 门禁 · EN 数据源语言隔离（W1265 批一·判据补盲 1-2）。

背景（《全站网页可视化图表审查报告 2026-11-16 · W1259》P0-1）：
  EN 站（site/en·138 页）在 http(s) 生产部署形态下**整段渲染中文**——根因是 EN 页的
  fetch 目标指向 ../data/json/（那是**中文**数据集目录）。既有门禁全绿是因为第 43/29/30/66/44
  槽要么只扫 site/data·要么只做静态文本扫描（不模拟 fetch）。

判据（方向：EN 页的数据装载目标**不得**落在中文数据集目录 site/data/json/）：
  E1 字面量装载调用点指向中文数据集 → 违例
     口径：装载调用 = fetch | d3.json | loadJson | load_json | fetchJSON | fetchJson | getJSON
           的**第一个实参**是字符串字面量且以 .json 结尾（loadJson(path, fallback) 的第二参
           是回退值不是路径——审查报告《被证伪的初判》第 1 条已实证这一点）。
  E2 动态拼接装载调用点指向中文数据集 → 违例
     口径：路径常量 + 文件名表拼接（DATA_DIR + f·f 来自 FILES 表）——审查报告 13 页/38 调用点
           用的是字面量口径（E1），动态拼接（E2）是探针盲区·本槽补上。
  合法目标：../en/json/*.json（英文部署副本）——不违规。

存量基线：审查报告实测 13 页 / 38 个字面量调用点（E1 口径）；E2 另计。
  本门禁默认走「基线冻结」形态：基线内违例记「存量基线」不计 FAIL（页面线修复后自动归零），
  基线外新增违例照样 FAIL。零容忍：--strict（基线不参与判定·全部违例计 FAIL）。

用法：
  py -3 scripts/check_en_data_source.py                 # 门禁（基线冻结）
  py -3 scripts/check_en_data_source.py --strict        # 零容忍（存量全红）
  py -3 scripts/check_en_data_source.py --report        # 只报数·退出码 0
  py -3 scripts/check_en_data_source.py --generate-baseline
  py -3 scripts/check_en_data_source.py --self-test
退出码：0 通过（违例全在基线内）/ 1 违例或基线缺失（fail-closed）/ 2 自测失败
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from lib import freeze_gate, json_refs  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EN_DIR = ROOT / "site" / "en"
MARKER = "---- 第 78 门禁 EN 数据源语言隔离："
BASELINE = ROOT / "scripts" / "output" / "en-data-source-baseline.txt"
CN_DATA_PREFIX = "site/data/json/"  # 页相对路径解析后仍以 site/ 为根（site/en/x.html → site/data/json/…）
SKIP_STEMS = ("_shell", "_template")

RULE_CODES = {"L1": "E1", "L2": "E2", "L3": "E2", "L4": "E2", "L5": "E2"}


def scan_text(page_rel: str, html: str) -> tuple[list[str], list[str]]:
    """扫描一页 → (违例键列表, 未解析实参列表)。"""
    viol: list[str] = []
    unresolved: list[str] = []
    targets, unres = json_refs.extract_targets(html)
    unresolved.extend(a for a in unres if ".json" in a or re.fullmatch(r"[A-Za-z_$][\w$]*", a))
    for target, rule in targets:
        resolved = json_refs.norm_path(json_refs.resolve_http_path(page_rel, target))
        if resolved.startswith(CN_DATA_PREFIX):
            code = RULE_CODES.get(rule, "E2")
            viol.append("%s|%s|指向中文数据集 %s（解析后 %s）" % (page_rel, code, target, resolved))
    return viol, unresolved


def scan_site() -> tuple[list[str], list[str], dict[str, list[str]]]:
    """扫全站 EN 面 → (违例键, 未解析实参, 页→违例键映射)。"""
    viol: list[str] = []
    unresolved: list[str] = []
    per_page: dict[str, list[str]] = {}
    if not EN_DIR.is_dir():
        return viol, unresolved, per_page
    for f in sorted(EN_DIR.glob("*.html")):
        if f.stem in SKIP_STEMS:
            continue
        page_rel = "site/en/" + f.name
        html = f.read_text(encoding="utf-8", errors="ignore")
        v, u = scan_text(page_rel, html)
        viol.extend(v)
        unresolved.extend(u)
        if v:
            per_page[page_rel] = v
    return viol, unresolved, per_page


def self_test() -> int:
    """负样本自测：违例必红·恢复必绿·基线语义正确。"""
    cases = [
        ("正样本-EN 引用英文部署副本", "site/en/a.html", "loadJson('../en/json/x.json', EMBEDDED.x)", 0),
        ("负样本-E1 字面量指向中文数据集", "site/en/b.html", "fetch('../data/json/y.json')", 1),
        (
            "负样本-E2 动态拼接指向中文数据集",
            "site/en/c.html",
            'const DATA_DIR = "../data/json/";\nconst FILES = { a: "a.json", b: "b.json" };\n'
            'fetch(DATA_DIR + f);',
            2,
        ),
        ("负样本-注释里的中文路径不算调用点", "site/en/d.html", "<!-- 说明：数据来自 ../data/json/z.json -->", 0),
        (
            "负样本-第二实参是回退值不是路径",
            "site/en/e.html",
            "loadJson('../en/json/ok.json', '../data/json/not_a_path.json')",
            0,
        ),
        ("负样本-英文站根页也受判", "site/en/root.html", "fetch('../data/json/q.json')", 1),
    ]
    bad = 0
    for name, page, snippet, expect in cases:
        viol, _ = scan_text(page, "<html><script>" + snippet + "</script></html>")
        ok = len(viol) == expect
        print("%s %s：期望 %d 条违例·实得 %d 条 %s" % ("OK  " if ok else "FAIL", name, expect, len(viol), viol))
        bad += 0 if ok else 1

    # 基线语义：基线内 → 不计 FAIL；基线外 → FAIL；strict → 全红
    viol, _ = scan_text("site/en/b.html", "<html><script>fetch('../data/json/y.json')</script></html>")
    key = viol[0]
    res = freeze_gate.evaluate(viol, {key}, strict=False)
    ok = not res["new_fail"] and len(res["frozen"]) == 1
    print("%s 基线内违例不计 FAIL（frozen=%d·new_fail=%d）" % ("OK  " if ok else "FAIL", len(res["frozen"]), len(res["new_fail"])))
    bad += 0 if ok else 1
    res = freeze_gate.evaluate(viol, set(), strict=False)
    ok = len(res["new_fail"]) == 1
    print("%s 基线外新增违例计 FAIL（new_fail=%d）" % ("OK  " if ok else "FAIL", len(res["new_fail"])))
    bad += 0 if ok else 1
    res = freeze_gate.evaluate(viol, {key}, strict=True)
    ok = len(res["new_fail"]) == 1
    print("%s 零容忍模式存量全红（new_fail=%d）" % ("OK  " if ok else "FAIL", len(res["new_fail"])))
    bad += 0 if ok else 1

    print("自测 %d/%d 通过" % (len(cases) + 3 - bad, len(cases) + 3))
    return 0 if bad == 0 else 2


def main() -> int:
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return self_test()

    strict = "--strict" in argv
    report_only = "--report" in argv
    baseline_path = BASELINE
    if "--baseline" in argv:
        i = argv.index("--baseline")
        if i + 1 < len(argv):
            baseline_path = Path(argv[i + 1])
            if not baseline_path.is_absolute():
                baseline_path = ROOT / baseline_path

    viol, unresolved, per_page = scan_site()
    e1 = [v for v in viol if "|E1|" in v]
    e2 = [v for v in viol if "|E2|" in v]

    if "--generate-baseline" in argv:
        n = freeze_gate.write_baseline(
            baseline_path,
            viol,
            [
                "# 第 78 门禁 · EN 数据源语言隔离基线（W1265 建立·存量违例冻结）",
                "# 生成命令：py -3 scripts/check_en_data_source.py --generate-baseline",
                "# 格式：<页面>|<E1|E2>|<细节>；E1=字面量装载调用点·E2=动态拼接装载调用点",
                "# 语义：基线内违例记「存量基线」不计 FAIL；基线外新增 = FAIL；",
                "#       零容忍（页面修完后）：--strict（基线不参与判定）",
            ],
        )
        print("基线已写入 %s（%d 条）" % (baseline_path, n))
        return 0

    baseline, problems = freeze_gate.read_baseline(baseline_path)
    if problems:
        if report_only:
            for p in problems:
                print("NOTE " + p + "（报告档不判红）")
            baseline = set()
        else:
            for p in problems:
                print("FAIL " + p)
            print("%s 基线缺失/不可读·fail-closed·拒绝通过 ----" % MARKER)
            return 1

    res = freeze_gate.evaluate(viol, baseline, strict=strict)
    e1_pages = sorted({v.split("|")[0] for v in e1})
    e2_pages = sorted({v.split("|")[0] for v in e2})
    print("EN 页 %d · E1 字面量调用点 %d 条 / %d 页 · E2 动态调用点 %d 条 / %d 页 · 未解析实参 %d 个"
          % (len(list(EN_DIR.glob("*.html"))) if EN_DIR.is_dir() else 0, len(e1), len(e1_pages),
             len(e2), len(e2_pages), len(unresolved)))
    if unresolved:
        print("  · 未解析实参样例（不计违例·探针盲区·须人工确认）：%s" % " / ".join(sorted(set(unresolved))[:5]))
    print("违例页 %d 页：%s" % (len(per_page), " ".join(sorted(p.split("/")[-1] for p in per_page))))
    freeze_gate.print_eval(res, MARKER, strict=strict)
    print("%s ----" % MARKER)
    if report_only:
        return 0
    return 1 if res["new_fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
