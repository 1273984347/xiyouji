#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_motion_ban.py — Phase E E6 转正门禁（D4 动效禁止清单）

扫描 site/ 全部 HTML（含 data/、en/）内联 CSS 与内联 JS 中的禁止动效模式：
- cubic-bezier 负值（回弹/过冲）
- rotate(360/720（旋转动画）
- animation 无限循环（infinite）
- parallax（视差滚动）

白名单（功能性/一次性）：
- .chart-loading 呼吸骨架（功能加载指示）
- .chart-fade-in 一次性入场
- 已登记豁免的动画（输出时注明）

用法：python scripts/check_motion_ban.py
退出码：0 = 通过；1 = FAIL
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BAN = [
    (re.compile(r"cubic-bezier\([^)]*-\d"), "cubic-bezier 负值（回弹）"),
    (re.compile(r"rotate\(36\d|rotate\(72\d"), "360°/720° 旋转"),
    (re.compile(r"animation\s*:\s*[^;]*infinite"), "无限循环动画"),
    (re.compile(r"parallax", re.I), "parallax 视差"),
]
WHITELIST_HINTS = ["chart-loading", "chart-fade-in"]


def main():
    fails = []
    for f in sorted(ROOT.glob("site/**/*.html")):
        rel = str(f.relative_to(ROOT))
        s = f.read_text(encoding="utf-8", errors="ignore")
        # 剔除白名单上下文行后再扫
        lines = [ln for ln in s.splitlines() if not any(h in ln for h in WHITELIST_HINTS)]
        body = "\n".join(lines)
        for pat, desc in BAN:
            for m in pat.finditer(body):
                ctx = body[max(0, m.start() - 40):m.end() + 20].replace("\n", " ")
                fails.append(f"{rel}: {desc} → …{ctx}…")
    print(f"动效禁止清单门禁：命中 {len(fails)}")
    for msg in fails[:15]:
        print("  FAIL", msg)
    if fails:
        print("FAIL 详情见上（超 15 条仅显示前 15）")
        return 1
    print("OK   动效禁止清单门禁通过（无 bounce/旋转/无限循环/parallax）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
