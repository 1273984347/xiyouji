#!/usr/bin/env python3
"""_w876_baseline_probe.py — W876 24 页基准面对拍（一次性件·收尾验证第四轨）。

**做什么**：复用 W851 J2 视觉回归探针（_w851_visual_regression_probe.py）的采集与
diff 机制，对 W876 改动做「前后计算样式对拍」——
  before = HEAD 快照树（git archive 提取·迁移完好 + 旧令牌值的最后已知良好态）
  after  = 在役工作树（C 渠换色 + 两处令牌值切换后的重建态）
24 页（J2 21 页 + philosophy / workplace / heaven-power-network 三页换色重点页）
× 浅暗双主题 × 15s 地板（覆盖 chart-audit 修复波）逐元素逐属性对拍。

**判据不是零差异**（W876 是**有据变化**·不是 W851 的纯加法）：每一处差异必须归入
三类预期变迁，归入不了即 FAIL：
  T1 C 渠（仅浅色·仅 color）：rgb(200,70,58) → rgb(199,70,58)
  T2 chart-3 值切换（color / border-*-color / background-color）：
     rgb(201,160,99) → rgb(179,143,88)
  T3 暗色 --accent 值切换（仅暗色·color / border-*-color / background-color）：
     rgb(224,96,79) → rgb(228,98,80)
（暗色主题下 C 渠不产生差异——暗色 --accent-text 与旧 --accent 同值 #E0604F；
元素数 / 元素身份差异一律 FAIL——那意味着换色之外的渲染变动。）

**这一轨的独特价值**：静态 diff 审计证明「文件里只变了三类」；对拍证明「浏览器里
也只渲染出三类」——两者合起来闭环「零意外视觉变动」。inline_css --force 回吞迁移
成果的重大回归（.seal 淡底→实底等）在这一轨下必现形。

用法：py -3 scripts/_w876_baseline_probe.py [--before <dir>] [--floor 15000]
产物：scripts/output/_w876_baseline_before.json / _after.json / _baseline_diff.json
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import _w851_visual_regression_probe as probe  # noqa: E402

EXTRA_PAGES = ("data/philosophy.html", "data/workplace.html",
               "data/heaven-power-network.html")
PAGES = list(probe.PROBE_PAGES) + list(EXTRA_PAGES)

COLOR_PROPS = {"color", "background-color", "border-top-color", "border-right-color",
               "border-bottom-color", "border-left-color"}

# 三类预期变迁：(prop 限定 or None=任意 color 系属性, before, after, 允许主题)
TRANSITIONS = [
    ({"color"}, "rgb(200, 70, 58)", "rgb(199, 70, 58)", {"light"}),
    (None, "rgb(201, 160, 99)", "rgb(179, 143, 88)", {"light", "dark"}),
    (None, "rgb(224, 96, 79)", "rgb(228, 98, 80)", {"dark"}),
]

# T1 的 currentColor 传播扩展：文本色被换（--accent→--accent-text）后，
# border-*-color 为 currentColor 初始值（含零宽边·Chromium 仍计算其色）的边随行——
# 故 T1 色对允许出现在 border-*-color 上（background-color 不跟随 currentColor·不在内）。
T1_CURRENTCOLOR_PROPS = {"border-top-color", "border-right-color",
                         "border-bottom-color", "border-left-color"}
T1_OLD, T1_NEW = "rgb(200, 70, 58)", "rgb(199, 70, 58)"

# T4 混色派生：暗色 --accent 改值（#E0604F→#E46250）经 color-mix 派生的色微移
# （如 dashboard --cross-table-header-bg: color-mix(in srgb, var(--accent) 14%, var(--paper))）。
# 判据：Δ 三通道与 Δaccent 成同一比例（=混色百分比·通道间一致·实测恰为 0.14）。
_ACCENT_DELTA = (0.894118 - 0.878431, 0.384314 - 0.376471, 0.313725 - 0.309804)
_SRGB_RE = re.compile(r"color\(srgb ([\d.]+) ([\d.]+) ([\d.]+)\)")


def _mix_derived(before, after):
    """before/after 为 color(srgb …) 时，判 Δ 是否与 Δaccent 成同一正比例。"""
    mb, ma = _SRGB_RE.match(str(before)), _SRGB_RE.match(str(after))
    if not (mb and ma):
        return False
    b = [float(x) for x in mb.groups()]
    a = [float(x) for x in ma.groups()]
    ratios = [(a[i] - b[i]) / _ACCENT_DELTA[i] for i in range(3)]
    p = sum(ratios) / 3.0
    if not 0 < p <= 1.0001:
        return False
    return all(abs(r - p) < 0.005 for r in ratios)


def classify(diff):
    """diff 条目 → 变迁编号（1/2/3/4）或 None（未预期）。"""
    if diff.get("kind") != "属性":
        return None
    prop, before, after = diff.get("prop"), diff.get("before"), diff.get("after")
    if prop not in COLOR_PROPS:
        return None
    for i, (props, b, a, themes) in enumerate(TRANSITIONS, 1):
        if diff.get("theme") not in themes:
            continue
        if props is not None and prop not in props:
            continue
        if before == b and after == a:
            return i
    # T1 扩展：色对落在 border-*-color 上（currentColor 传播·浅色）
    if (diff.get("theme") == "light" and prop in T1_CURRENTCOLOR_PROPS
            and before == T1_OLD and after == T1_NEW):
        return 1
    # T4：暗色 color-mix 派生微移（Δ 与 Δaccent 成同一比例）
    if diff.get("theme") == "dark" and _mix_derived(before, after):
        return 4
    return None


def main(argv):
    ap = argparse.ArgumentParser(description="W876 24 页基准面对拍")
    ap.add_argument("--before", default="/tmp/w876_head/site",
                    help="HEAD 快照站点根（git archive 提取）")
    ap.add_argument("--floor", type=int, default=15000)
    ap.add_argument("--rediff", action="store_true",
                    help="不重新采集·加载已落盘 before/after 快照重 diff"
                         "（_diff_snapshots 默认 20 条截断会漏检切断点之后的差异·"
                         "重 diff 用 max_report=10**7 取全量）")
    args = ap.parse_args(argv[1:])

    outdir = os.path.join(ROOT, "scripts", "output")
    os.makedirs(outdir, exist_ok=True)
    bp_path = os.path.join(outdir, "_w876_baseline_before.json")
    ap_path = os.path.join(outdir, "_w876_baseline_after.json")

    if args.rediff:
        with open(bp_path, encoding="utf-8") as f:
            snap_before = json.load(f)
        with open(ap_path, encoding="utf-8") as f:
            snap_after = json.load(f)
        print("[REDIFF] 加载已落盘快照（%d 页 × %s）·全量重 diff（无截断）"
              % (len(snap_before["pages"]), "+".join(snap_before["themes"])))
    else:
        before_root = os.path.abspath(args.before)
        after_root = os.path.join(ROOT, "site")

        before_paths, after_paths, missing = [], [], []
        for rel in PAGES:
            bp = os.path.join(before_root, rel.replace("/", os.sep))
            ap_ = os.path.join(after_root, rel.replace("/", os.sep))
            if os.path.isfile(bp) and os.path.isfile(ap_):
                before_paths.append((rel, bp))
                after_paths.append((rel, ap_))
            else:
                missing.append(rel)
        if missing:
            print("FAIL 对拍面缺页（before=%s）：%s" % (before_root, "、".join(missing)))
            return 1
        print("对拍面：%d 页 × 双主题（before=%s）" % (len(PAGES), before_root))

        snap_before = probe.capture(before_paths, themes=("light", "dark"),
                                    floor_ms=args.floor)
        with open(bp_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(snap_before, f, ensure_ascii=False, separators=(",", ":"))
        print("before 快照完成（%d 页）" % len(snap_before["pages"]))

        snap_after = probe.capture(after_paths, themes=("light", "dark"),
                                   floor_ms=args.floor)
        with open(ap_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(snap_after, f, ensure_ascii=False, separators=(",", ":"))
        print("after 快照完成（%d 页）" % len(snap_after["pages"]))

    diffs, notes = probe._diff_snapshots(snap_before, snap_after, max_report=10 ** 7)
    classified, unexplained = {}, []
    for d in diffs:
        t = classify(d)
        if t:
            classified[t] = classified.get(t, 0) + 1
        else:
            unexplained.append(d)

    report = {"pages": len(PAGES), "diffs_total": len(diffs),
              "classified": classified, "unexplained": unexplained[:50],
              "unexplained_count": len(unexplained), "notes": notes}
    with open(os.path.join(outdir, "_w876_baseline_diff.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)

    for nt in notes:
        print("NOTE", nt)
    print("=== 24 页基准对拍：差异 %d 处 · 归三类 %d · 未预期 %d"
          % (len(diffs), sum(classified.values()), len(unexplained)))
    for t, n in sorted(classified.items()):
        names = {1: "T1·C渠(浅·含currentColor传播)", 2: "T2·chart-3值",
                 3: "T3·暗色accent值", 4: "T4·暗色color-mix派生"}
        print("  %-16s %d 处" % (names.get(t, t), n))
    if unexplained:
        print("[FAIL] 未预期差异 %d 处（前 10 条）：" % len(unexplained))
        for d in unexplained[:10]:
            print("  %s" % json.dumps(d, ensure_ascii=False))
        return 1
    print("[PASS] 全部差异归四类预期变迁·四类之外渲染零变动")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
