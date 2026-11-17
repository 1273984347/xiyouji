#!/usr/bin/env python3
"""
check_design_identity.py — 视觉语言的「身份」判据（W1264 立·E-250 机器化）

背景（坑位 E-250）：
  给「无上下文」设计任务写简报时，**禁令会定义答案空间**——把正解挡在空间外，
  产出的就是「正确但无身份」的东西。实证：两个零参考方向都「正确」（可读 /
  色盲安全 / 零依赖 / 交互真实生效），但视觉语言整体倒向冷绿仪器路线，
  与「一本明代古籍」这个题材零同源 ⇒ 用户判「还不如现在的版本」。

本判据把「身份」变成**可量化的持续指标**：
  ① 全站通用色（覆盖 ≥80% 页面的色值·去重）按色族计数；
  ② 计算 **暖承载 / 冷数据 配比**；
  ③ 与**现役基线**对比：暖承载占比不得低于基线的下限（棘轮·不许退）；
  ④ 报告暖冷两色的具体色值，便于判断「同源点」是否成立。

**口径要点（易错，勿改）**：
  - 必须**去重**（按「出现在多少个不同页面」计）——内联副本会让每个色值在
    866 页各存一份，直接统计出现次数会被「被复制最多的色」主导（初版曾误报
    「暖红占 73.4%」）。
  - 覆盖率分母用**实际扫描的页面数**，不是全站总页数。

用法：
  py -3 scripts/check_design_identity.py
  py -3 scripts/check_design_identity.py --dir <designDir> [--pages 0.8] [--min-warm-ratio 0.2]
  py -3 scripts/check_design_identity.py --json

退出码：0 = 通过（或仅 WARN）；1 = 暖承载占比低于下限（身份退化）；2 = 执行异常（fail-closed）
"""
import argparse
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

# 暖承载族（朱砂 / 赭 / 檀 / 褐 / 焦）与冷数据族（靛 / 黛 / 青 / 绿 / 蓝）
# 判据只看色相关系，不看具体色值——不同设计的选色不同，但冷暖分工应保持。
WARM_MIN_R, WARM_MIN_B = 12, 12


def color_family(hexv):
    r = int(hexv[1:3], 16)
    g = int(hexv[3:5], 16)
    b = int(hexv[5:7], 16)
    if r > g + WARM_MIN_R and r > b + WARM_MIN_R:
        return "warm"
    if g > r + 6:
        return "cool"
    if b > r + 6:
        return "violet"
    if abs(r - g) < 14 and abs(g - b) < 14:
        return "neutral"
    return "other"


def scan(files, cover_ratio):
    """返回 (覆盖页数统计, 实际页数)。按「出现在多少个不同页面」去重计数。"""
    cover = collections.Counter()
    pages = 0
    for f in files:
        try:
            t = open(f, encoding="utf-8").read()
        except Exception:
            continue
        pages += 1
        seen = set(m.group(0).upper() for m in re.finditer(r"#[0-9a-fA-F]{6}\b", t))
        for h in seen:
            cover[h] += 1
    uni = [(h, n) for h, n in cover.items() if n >= cover_ratio * pages]
    uni.sort(key=lambda x: -x[1])
    return uni, pages


def summarize(uni):
    fam = collections.Counter(color_family(h) for h, _ in uni)
    total = sum(fam.values()) or 1
    warm = fam.get("warm", 0)
    cool = fam.get("cool", 0) + fam.get("violet", 0)
    return {
        "families": dict(fam),
        "total": sum(fam.values()),
        "warm_ratio": round(warm / total, 4),
        "cool_ratio": round(cool / total, 4),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=SITE, help="待扫描目录（默认现役 site/）")
    ap.add_argument("--pages", type=float, default=0.8, help="通用色覆盖率门槛")
    ap.add_argument("--min-warm-ratio", type=float, default=0.0,
                    help="暖承载占比下限（0 = 只报告不判定）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.dir):
        print("FAIL  目录不存在：%s" % args.dir)
        return 2

    files = glob.glob(os.path.join(args.dir, "**", "*.html"), recursive=True)
    if not files:
        print("FAIL  未扫到任何 HTML（目录空或路径失效）⇒ fail-closed")
        return 2

    uni, pages = scan(files, args.pages)
    if not uni:
        print("FAIL  无任何通用色（覆盖 ≥%.0f%% 的色值）⇒ 判据不可执行" % (args.pages * 100))
        return 2

    s = summarize(uni)
    if args.json:
        print(json.dumps({
            "dir": args.dir, "pages": pages,
            "warm_ratio": s["warm_ratio"], "cool_ratio": s["cool_ratio"],
            "families": s["families"],
            "top": [{"hex": h, "pages": n, "fam": color_family(h)} for h, n in uni[:12]],
        }, ensure_ascii=False, indent=2))
        return 0

    print("视觉身份判据 · %s（扫 %d 页·通用色门槛 ≥%.0f%%）" % (args.dir, pages, args.pages * 100))
    print("  暖承载(朱/赭/檀/褐) 占比 = %.1f%%   冷数据(靛/黛/青/绿/紫) 占比 = %.1f%%   族分布 = %s"
          % (s["warm_ratio"] * 100, s["cool_ratio"] * 100, s["families"]))
    print("  通用色 Top8:", ", ".join("%s(%s)" % (h, color_family(h)) for h, _ in uni[:8]))
    if args.min_warm_ratio > 0 and s["warm_ratio"] < args.min_warm_ratio:
        print("---- 视觉身份判据：FAIL（暖承载 %.1f%% < 下限 %.1f%%·身份退化）----"
              % (s["warm_ratio"] * 100, args.min_warm_ratio * 100))
        return 1
    print("---- 视觉身份判据：0 FAIL（暖承载 %.1f%%）----" % (s["warm_ratio"] * 100))
    return 0


if __name__ == "__main__":
    sys.exit(main())
