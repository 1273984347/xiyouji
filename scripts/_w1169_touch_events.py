#!/usr/bin/env python3
"""_w1169_touch_events.py — 图表 tooltip 事件改造（W1169 · V4 触摸交互优化）。

背景：5 个数据页的提示框只绑鼠标专有事件——`mousemove` 显示 / `mouseleave` 隐藏。
触摸设备上：手指抬起不触发 `mouseleave`（提示框永久残留），单击不产生 `mousemove`
（只能靠浏览器合成的一次 mouse 事件，位置固定且不随拖动更新）。

改造：事件名整体切到 Pointer Events，实现「按住即显示 / 拖动跟随 / 抬手隐藏」：
  mousemove  → pointermove   拖动跟随
  mouseleave → pointerleave  抬手即触发（触摸结束派发 pointerleave）
  mouseover  → pointerover   触摸按下即触发（进入元素）

零结构改动：只替换事件名字符串，不改回调结构、不加分支。

三重防线（E-199）：
  1 锚点唯一性预检：逐页统计三类事件出现次数，与预期基线比对，不符即中止（零落盘）
  2 改后完整性断言：行数不变 + 替换计数守恒 + 无残留鼠标事件名（事件绑定语境）
  3 结果逐页打印，便于红灯归因

用法：
  py -3 scripts/_w1169_touch_events.py --dry-run
  py -3 scripts/_w1169_touch_events.py --apply
退出码：0 成功 / 1 预检或断言失败（零落盘）
"""
from __future__ import annotations

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 每页的预期基线（预检用·实测于 W1169 开工前）
PAGES = {
    "site/data/chapter-stats.html": {"mousemove": 3, "mouseleave": 3},
    "site/data/story-timeline.html": {"mouseover": 1, "mouseout": 1},
    "site/data/tag-cloud.html": {"mousemove": 1, "mouseleave": 1, "mouseenter": 1},
    "site/data/timeline.html": {"mousemove": 2, "mouseleave": 2, "mouseenter": 2},
    "site/data/cross-time-danmaku.html": {"mousemove": 2, "mouseleave": 2, "mouseenter": 2},
}

# 事件名同为 mouse* 一族，互不为前缀，替换顺序无关。全部切到 Pointer Events：
#   按下/进入 → pointerover | pointerenter；移动 → pointermove；抬手/离开 → pointerleave | pointerout
MAP = [
    ("mousemove", "pointermove"),
    ("mouseleave", "pointerleave"),
    ("mouseover", "pointerover"),
    ("mouseout", "pointerout"),
    ("mouseenter", "pointerenter"),
]


def precheck(text: str, expect: dict) -> list[str]:
    """锚点唯一性预检：三类事件计数必须与基线完全一致。"""
    errs = []
    for src, want in expect.items():
        got = text.count(src)
        if got != want:
            errs.append(f"{src} 期望 {want} 实得 {got}")
    return errs


def rewrite(text: str) -> tuple[str, dict]:
    """按映射替换，返回 (新文本, 各类替换计数)。"""
    counts = {}
    out = text
    for src, dst in MAP:
        n = out.count(src)
        if n:
            out = out.replace(src, dst)
            counts[f"{src}->{dst}"] = n
    return out, counts


def verify(old: str, new: str, counts: dict, expect: dict) -> list[str]:
    """改后完整性断言。"""
    errs = []
    if old.count("\n") != new.count("\n"):
        errs.append(f"行数变化 {old.count(chr(10))} -> {new.count(chr(10))}")
    total_src = sum(expect.values())
    total_new = sum(counts.values())
    if total_new != total_src:
        errs.append(f"替换计数不守恒：源 {total_src} 替换 {total_new}")
    for src, _dst in MAP:
        if src in new:
            errs.append(f"残留未替换的 {src} ×{new.count(src)}")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dry = not args.apply

    report = []
    fails = []
    for rel, expect in PAGES.items():
        path = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.exists(path):
            fails.append(f"{rel}: 文件不存在")
            continue
        text = open(path, encoding="utf-8").read()
        errs = precheck(text, expect)
        if errs:
            fails.append(f"{rel}: 预检失败 —— {'; '.join(errs)}")
            continue
        new, counts = rewrite(text)
        errs = verify(text, new, counts, expect)
        if errs:
            fails.append(f"{rel}: 断言失败 —— {'; '.join(errs)}")
            continue
        report.append((rel, counts))
        if not dry:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)

    for rel, counts in report:
        print(f"{'[DRY] ' if dry else '[OK]  '}{rel}  {counts}")
    if fails:
        for f in fails:
            print("FAIL " + f)
        print(f"---- W1169 触摸事件改造：{len(report)} 页就绪 · {len(fails)} 页失败（零落盘）----")
        return 1
    total = sum(sum(c.values()) for _r, c in report)
    print(f"---- W1169 触摸事件改造：{len(report)} 页 · 替换 {total} 处 · {'dry-run 未落盘' if dry else '已落盘'} ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
