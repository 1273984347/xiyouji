#!/usr/bin/env python3
"""
check_public_layer_coverage.py — 公共层样式覆盖率下限与棘轮（W1264 立）

背景（坑位 E-243 / E-245 同族的「判据覆盖不到的那一面」族）：
  「换皮」能不能终结「拼贴感」，不取决于设计多好看，而取决于**新语言的公共层
  能管住多少页面样式**。实测现役：875 页实际使用 953 个 class，公共层
  site/system.css（132 类）只覆盖 91 个 = **9.5%**；其余 862 个类的样式
  落在页面私有层 ⇒ 每次改版都要逐页改 ⇒ 拼贴感必然复现。

  本判据把「样式治理水平」变成**可量化的持续指标**：
  ① 覆盖率不得低于下限（默认 9.5%＝现役基线·棘轮不许退）；
  ② 目标档（默认 40%）未达成时以 WARN 提示（不阻断·逐步抬高）；
  ③ 报告未覆盖的高频类 top-N ⇒ 指出下一步该归并哪一族。

用法：
  py -3 scripts/check_public_layer_coverage.py
  py -3 scripts/check_public_layer_coverage.py --min-ratio 0.40 --target-ratio 0.40
  py -3 scripts/check_public_layer_coverage.py --json

退出码：0 = 通过（或仅 WARN）；1 = 覆盖率低于下限（棘轮破）；2 = 执行异常（fail-closed）
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
SYSTEM_CSS = os.path.join(SITE, "system.css")

# 现役基线（W1264 实测）：公共层覆盖 113 / 953 = 11.9%（选择器口径）
# 注：另有「类定义处计数」的窄口径 91 / 953 = 9.5%——两个口径都对但含义不同：
#   窄口径 = CSS 里以 .class 形式出现的类定义数；宽口径 = 全部选择器里出现的类名。
# 棘轮用宽口径（更贴近「实际有多少页面样式被公共层接管」）。
# 棘轮取**向下取整**的基线（113/953 = 0.11857）⇒ 用 0.118 留余量，避免浮点比较自相矛盾
# （用 0.119 会因 0.11857 < 0.119 而恒判红——棘轮必须 ≤ 实测值）
DEFAULT_MIN_RATIO = 0.118
DEFAULT_TARGET_RATIO = 0.40


def _collect_used_classes():
    """扫全站 HTML 的 class 属性 ⇒ 实际被使用的 class 频次表。"""
    used = collections.Counter()
    pages = 0
    for p in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True):
        try:
            t = open(p, encoding="utf-8").read()
        except Exception:
            continue
        pages += 1
        for m in re.finditer(r'class="([^"]+)"', t):
            for c in m.group(1).split():
                used[c] += 1
    return used, pages


def _classes_in(css_path):
    """取 CSS 里定义的选择器类名（不含伪类/嵌套写法）。"""
    s = open(css_path, encoding="utf-8").read()
    return set(re.findall(r"(?<![-w]).([A-Za-z][A-Za-z0-9_-]*)", s))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-ratio", type=float, default=DEFAULT_MIN_RATIO,
                    help="覆盖率下限（低于此值判红·棘轮）")
    ap.add_argument("--target-ratio", type=float, default=DEFAULT_TARGET_RATIO,
                    help="目标档（未达成仅 WARN）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    if not os.path.exists(SYSTEM_CSS):
        print("FAIL  公共层样式文件不存在：%s" % SYSTEM_CSS)
        return 2

    used, pages = _collect_used_classes()
    if not used:
        print("FAIL  未扫到任何 class（HTML 全空或路径失效）⇒ fail-closed")
        return 2

    pub = _classes_in(SYSTEM_CSS)
    covered = set(used) & pub
    ratio = len(covered) / len(used)
    missing = sorted(((c, n) for c, n in used.items() if c not in pub),
                     key=lambda x: -x[1])

    data = {
        "pages": pages,
        "used_classes": len(used),
        "public_classes": len(pub),
        "covered": len(covered),
        "ratio": round(ratio, 4),
        "min_ratio": args.min_ratio,
        "target_ratio": args.target_ratio,
        "top_missing": [{"class": c, "uses": n} for c, n in missing[:15]],
    }

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0 if ratio >= args.min_ratio else 1

    print("公共层样式覆盖率：%d / %d = %.1f%%（下限 %.1f%% · 目标 %.1f%%）· 扫 %d 页"
          % (len(covered), len(used), ratio * 100, args.min_ratio * 100,
             args.target_ratio * 100, pages))
    print("  公共层类数 %d · 未被覆盖（页面私有层承担）%d 个"
          % (len(pub), len(used) - len(covered)))
    if missing:
        print("  未覆盖且使用最多的类（下一步归并目标）：")
        for c, n in missing[:10]:
            print("    %-28s %d" % (c, n))

    if ratio < args.min_ratio:
        print("---- 公共层覆盖率：FAIL（低于下限 %.1f%%·棘轮破·当前 %.1f%%）----"
              % (args.min_ratio * 100, ratio * 100))
        return 1
    if ratio < args.target_ratio:
        print("---- 公共层覆盖率：0 FAIL · WARN（未达目标 %.1f%%·当前 %.1f%%·归并未完）----"
              % (args.target_ratio * 100, ratio * 100))
        return 0
    print("---- 公共层覆盖率：0 FAIL（%.1f%% ≥ 目标 %.1f%%）----"
          % (ratio * 100, args.target_ratio * 100))
    return 0


if __name__ == "__main__":
    sys.exit(main())
