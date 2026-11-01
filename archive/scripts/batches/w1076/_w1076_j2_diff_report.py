#!/usr/bin/env python3
"""_w1076_j2_diff_report.py — W1076 B1：J2 双面差异逐项判读（证据生成件）。

口径：
- **标准面**：before = `scripts/output/_w1076_j2_before`（21 页·前一 session 拍）
            after  = `scripts/output/_w1076_j2_after`（24 页·本 session 拍·含补拍 3 页）
            ⇒ 交集 21 页逐元素逐属性对拍；
- **补拍面**：before = `scripts/output/_w1076_j2_before_root3.json`（dukou-engine / rum-viewer / visit-viewer）
            after  = `scripts/output/_w1076_j2_after`（同上）⇒ 交集 3 页逐属性对拍。

输出：差异按 (页·主题·元素·属性) 聚合的清单 + JSON 证据 + **未列举差异判据**辅助
（每个差异都要能落到手术编号；本脚本只负责「事实清单」，判定由人按规格出处签署）。
"""
import json
import os
import sys
from collections import Counter, defaultdict

def _repo_root():
    """向上找仓库根（带 .git 的目录）——脚本归档到 archive/scripts/batches/w1076/ 后仍可用。"""
    cur = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("未找到仓库根（.git）")
        cur = parent


sys.path.insert(0, os.path.join(_repo_root(), "scripts"))  # 归档后仍能 import 仓内探针
import visual_regression_probe as P  # noqa: E402

ROOT = _repo_root()
OUT = os.path.join(ROOT, "scripts", "output")

def _repo_root():
    """向上找仓库根（带 .git 的目录）——脚本归档到 archive/scripts/batches/w1076/ 后仍可用。"""
    cur = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("未找到仓库根（.git）")
        cur = parent


ROOT = _repo_root()
OUT = os.path.join(ROOT, "scripts", "output")

PAIRS = [
    ("标准面 21 页", os.path.join(OUT, "_w1076_j2_before"), os.path.join(OUT, "_w1076_j2_after")),
    ("补拍面 3 页（同条件重拍）", os.path.join(OUT, "_w1076_j2_before_root3.json"),
     os.path.join(OUT, "_w1076_j2_after_root3.json")),
]


def main():
    report = {"pairs": [], "summary": {}}
    grand = Counter()
    for label, b, a in PAIRS:
        before, after = P._load(b), P._load(a)
        diffs, notes = P._diff_snapshots(before, after, max_report=100000)
        by_page = defaultdict(list)
        for d in diffs:
            by_page[(d.get("page"), d.get("theme"))].append(d)
        print("\n########## %s ##########" % label)
        for nt in notes:
            print("  NOTE %s" % nt)
        print("  差异总数：%d" % len(diffs))
        for (page, theme), items in sorted(by_page.items()):
            props = Counter(i.get("prop") or i.get("kind") for i in items)
            els = Counter(str(i.get("element")) for i in items)
            print("  · %-34s %-6s 差异 %3d 处 · 属性分布 %s"
                  % (page, theme, len(items), dict(props.most_common())))
            for e, n in els.most_common(6):
                print("        元素 %-42s × %d" % (e, n))
            for i in items[:6]:
                print("        └ %s" % json.dumps(i, ensure_ascii=False))
            grand.update(props)
        report["pairs"].append({"label": label, "before": os.path.basename(b),
                                "after": os.path.basename(a), "notes": notes,
                                "diff_count": len(diffs),
                                "diffs": diffs})
    report["summary"] = dict(grand)
    print("\n---- 属性维度合计：%s ----" % dict(grand))
    with open(os.path.join(OUT, "_w1076_j2_diff_report.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("证据已落：scripts/output/_w1076_j2_diff_report.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
