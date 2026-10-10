"""check_dual_source_scan.py — 双源对发现器（S-24·W699）。

扫描「py 锚点表（default_output=…json 的分析器）↔ 页面 EMBEDDED_DATA」潜在双源对，
产出候选清单并标注既有校验器覆盖情况。发现器只读；逐对比对沿用
check_story_timeline_sync 模板按对定做。

  python scripts/check_dual_source_scan.py            # 候选清单（Markdown）
  python scripts/check_dual_source_scan.py --self-test
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SITE_DATA = ROOT / "site" / "data"

RE_DEFAULT_OUT = re.compile(r'default_output\s*=\s*"output/data/([\w-]+)\.json"')
RE_FETCH_JSON = re.compile(r"['\"](?:\.\./)?json/([\w-]+)\.json['\"]")
RE_EMBEDDED = re.compile(r"\bEMBEDDED_DATA\b")


def discover():
    """返回 [(json名, 生成器相对路径, 内嵌页面相对路径列表, 已有校验器或'')]。"""
    generators = {}
    for p in sorted(SCRIPTS.rglob("*.py")):
        if p.name.startswith("_"):
            continue
        m = RE_DEFAULT_OUT.search(p.read_text(encoding="utf-8", errors="ignore"))
        if m:
            generators.setdefault(m.group(1), []).append(p.relative_to(ROOT).as_posix())
    checkers = {p.name for p in sorted(SCRIPTS.glob("check_*.py"))
                if p.name != "check_dual_source_scan.py"}  # 排除自身防自指覆盖

    rows = []
    seen = set()
    for page in sorted(SITE_DATA.glob("*.html")):
        if page.name.startswith("_"):
            continue
        html = page.read_text(encoding="utf-8", errors="ignore")
        if not RE_EMBEDDED.search(html):
            continue
        rp = page.relative_to(ROOT).as_posix()
        # 候选信号（收紧）：页面以 .json 引用该输出名，或 EMBEDDED_DATA 顶层键=输出名
        for name, gens in generators.items():
            keyed = re.search(r"EMBEDDED_DATA\s*=\s*\{\s*" + name + r"\s*:", html) is not None
            referenced = (name + ".json") in html
            if not (keyed or referenced):
                continue
            covered = next((c for c in sorted(checkers) if _checker_covers(c, name)), "")
            key = (name, rp)
            if key not in seen:
                seen.add(key)
                rows.append((name, rp, gens, covered))
    return rows


def _checker_covers(checker_name, json_name):
    return json_name in (SCRIPTS / checker_name).read_text(encoding="utf-8", errors="ignore")


def report():
    rows = discover()
    out = ["| 双源 json | 内嵌页面 | 生成器 | 既有校验器 |", "|---|---|---|---|"]
    for name, page, gens, covered in rows:
        out.append("| %s.json | %s | %s | %s |" % (name, page, "、".join(gens), covered or "—"))
    return "\n".join(out), rows


def self_test():
    _, rows = report()
    names = {r[0] for r in rows}
    assert "timeline" in names, "已知 timeline 双源对未被发现：%s" % sorted(names)
    timeline_rows = [r for r in rows if r[0] == "timeline"]
    assert any(r[3] for r in timeline_rows), "timeline 对应有校验器覆盖（check_story_timeline_sync）"
    print("SELF-TEST PASS：发现 %d 个双源候选；timeline 对在册且有校验器覆盖" % len(rows))


def main():
    if "--self-test" in sys.argv:
        self_test()
        return 0
    out, rows = report()
    print(out)
    uncovered = [r for r in rows if not r[3]]
    print("\n[汇总] 候选 %d 对 · 已有校验器覆盖 %d · 待定做 %d" % (len(rows), len(rows) - len(uncovered), len(uncovered)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
