#!/usr/bin/env python3
"""gen_version_footer.py — dukou 页脚批次链生成器（W1336 建·用户 2026-11-27「页脚改脚本生成」）

为什么需要单独一件：四页脚此前由 `batch_cascade._face_footers` 在**收官链**里统一前插；
但手工改 dukou 页脚（或漏跑级联）会让页脚版本落后 ⇒ verify 只报 WARN、无人收口，且
**任何一次页面改动都会让第 80/82 槽的探针报告陈旧**（页 sha 失配 fail-closed）。
本件把「页脚链 + 探针刷新」收成一条命令，供批次内随时对齐。

单一写入逻辑：复用 `batch_cascade._foot_upsert`（W1122 幂等版），**不自建第二套插链实现**——
避免同号双 token / 链长失控两个历史缺陷重演（W724 / W1122 实证）。

用法：
  py -3 scripts/gen_version_footer.py --apply     # 按 CHANGELOG 现役段前插/替换本批 token
  py -3 scripts/gen_version_footer.py --check     # 页脚链头 token 是否等于现役 W（滞后即 exit 1）
  py -3 scripts/gen_version_footer.py --self-test
  make dukou-footer                               # apply + 重跑第 80/82 槽探针与渲染档案
"""
from __future__ import annotations

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import batch_cascade as bc  # noqa: E402

PAGE = "site/dukou-engine.html"
TOKEN_RE = re.compile(r"<footer>.{0,200}?(?:v[\d.]+(?:\s*·\s*)?)?W(\d{3,4})", re.S)
CL_TOP = re.compile(r"(?m)^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（)")


def current_batch():
    """现役批次号：CHANGELOG 顶段（与 verify 的期望版本同源）。"""
    text = open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8").read()
    m = CL_TOP.search(text)
    if not m:
        raise SystemExit("FAIL CHANGELOG 顶段未解析出 W 号")
    return "W%s" % (m.group(1) or m.group(2))


def footer_batch(html):
    """页脚 `<footer>` 内首个 W 号（链头）。返回 int 或 None。"""
    m = TOKEN_RE.search(html)
    return int(m.group(1)) if m else None


def apply(batch=None):
    batch = batch or current_batch()
    s, nl = bc.load(PAGE)
    nxt = bc._foot_upsert(s, batch, batch)  # noqa: SLF001 — 复用单一写入逻辑（见模块 docstring）
    if nxt == s:
        print("[OK] 页脚链已是 %s（幂等·零变化）" % batch)
        return 0
    with open(os.path.join(ROOT, PAGE), "w", encoding="utf-8", newline=nl) as f:
        f.write(nxt)
    print("[OK] 页脚链已前插 %s（%s）" % (batch, PAGE))
    return 0


def check(batch=None):
    batch = batch or current_batch()
    html = open(os.path.join(ROOT, PAGE), encoding="utf-8").read()
    cur = footer_batch(html)
    if cur is None:
        print("FAIL  %s 的 <footer> 内未解析出 W 号（链头丢失）" % PAGE)
        return 1
    want = int(batch.lstrip("W"))
    if cur < want:
        print("FAIL  页脚链头 W%d 落后于现役 W%d（修法=--apply 或 make dukou-footer）" % (cur, want))
        return 1
    print("---- dukou 页脚链：W%d == 现役 W%d · OK ----" % (cur, want))
    return 0


def self_test():
    fails = []
    # 链头解析：v 前缀 / W-only / 链长 12 + 尾注
    assert footer_batch("<footer>v2.3.259 W600 · W599</footer>") == 600
    assert footer_batch("<footer>W700 · W699 · …更早批次详见 CHANGELOG.md</footer>") == 700
    if footer_batch("<footer>无版本</footer>") is not None:
        fails.append("无 W 时应返回 None")
    # 幂等：同一批号重复 apply 不得产生第二个同号 token（复用 cascade 的 W724 防线）
    # 注意：_FOOT_TOKEN 只认 3-4 位 W 号（W10 这类两位号在真实链里不存在）
    html = ("<p>x</p><footer>W110 · W109 · W108 · W107 · W106 · W105 · W104 · W103 · W102 · W101 · W100 · W099"
            " · …更早批次详见 CHANGELOG.md</footer>")
    once = bc._foot_upsert(html, "W111", "W111")  # noqa: SLF001
    twice = bc._foot_upsert(once, "W111", "W111")  # noqa: SLF001
    if once != twice:
        fails.append("重复 apply 非幂等（同号 token 重复插入）")
    if len(re.findall(r"\bW111\b", once)) != 1:
        fails.append("同号 token 重复：%d" % len(re.findall(r"\bW111\b", once)))
    if "…更早批次详见 CHANGELOG.md" not in once:
        fails.append("链长治理尾注丢失")
    print("---- 自测：%s ----" % ("3/3 通过" if not fails else "FAIL " + "；".join(fails)))
    return 0 if not fails else 2


def main():
    ap = argparse.ArgumentParser(description="dukou 页脚批次链生成器（W1336）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--apply", action="store_true")
    g.add_argument("--check", action="store_true")
    g.add_argument("--self-test", action="store_true")
    ap.add_argument("--batch", default=None, help="覆盖现役批次（默认取 CHANGELOG 顶段）")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    return apply(args.batch) if args.apply else check(args.batch)


if __name__ == "__main__":
    sys.exit(main())
