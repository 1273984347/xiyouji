# -*- coding: utf-8 -*-
"""_w1001_finish_faces.py — 手工补齐 W1001 的剩余版本面（级联超时留下的半完成态）

现状：级联（batch_cascade）虽超时，但**14 个版本面已落盘**（README / STRUCTURE / 项目说明 /
CITATION.cff / HANDOVER「最后更新」链 / workflows README 头部均已是 W1001），
**唯独 CHANGELOG 的 W1001 段未插入**（_face_changelog 落盘前被杀）⇒ 门禁红 4 处：
  ① HANDOVER.md 不含 W1001 里程碑 token
  ② CHANGELOG 编号规则（W001-W1000）!= 现役 W1001
  ③ 治理文档「最后更新」链首（W1000）!= 现役 W1001
  ④ 索引健康：CHANGELOG 编号规则段上限 != 最新段

本脚本补齐这 4 处（**只动版本面，不动内容面**）：
  ① 插入 CHANGELOG 的 `### W1001` 段（内容取本批 spec 的 changelog_body）
  ② CHANGELOG 编号规则 → （W001-W1001）
  ③ HANDOVER.md「一、当前进度」的里程碑列表加 W1001 行（仿 W1000 行格式）
  ④ 复核 4 处

用法：py -3 scripts/_w1001_finish_faces.py [--dry-run]
"""
from __future__ import annotations

import io
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
CH = os.path.join(REPO, "CHANGELOG.md")
HAND = os.path.join(REPO, "HANDOVER.md")
SPEC = os.path.join(OUT, "_w1001_spec.json")

MY_HDR = "### W1001（2026-10-28）：回次 og:image 全覆盖批·第一轮试点（12 张线描立像/场面）"
HAND_MILE = ("- **W1001 回次 og:image 全覆盖批·第一轮**：12 张线描立像/场面接入 12 个回目页 + "
              "专属 1200×630 og:image（回目覆盖 8 → 20 回）+ 母版段派两变体（立像段逐字 249 字符 · "
              "场面段仅改 3 处）+ 裁切判据改主体口径（连通簇）消除假红")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in sys.argv
    with open(SPEC, encoding="utf-8") as fh:
        spec = json.load(fh)
    body = spec["changelog_body"]

    # ① 插入 CHANGELOG 的 W1001 段
    t, n = read(CH)
    if MY_HDR in t:
        print("SKIP  CHANGELOG 已有 W1001 段")
    else:
        seg = MY_HDR + body + "\n"
        heads = [(int(m.group(1)), m.start()) for m in re.finditer(r"^### W(\d{3,4}) ", t, re.M)]
        pos = None
        for w, s in heads:
            if w < 1001:
                pos = s
                break
        if pos is None:
            pos = 0
        t = t[:pos] + seg + t[pos:]
        if dry:
            print("DRY  CHANGELOG 将插入 W1001 段")
        else:
            write(CH, t, n)
            print("OK   CHANGELOG W1001 段已插入")

    # ② 编号规则 → （W001-W1001）
    t, n = read(CH)
    lines = t.split("\n")
    changed = 0
    for i, ln in enumerate(lines):
        if "编号规则" in ln:
            new = re.sub(r"[（(]W001-W\d{3,4}[)）]", "（W001-W1001）", ln)
            if new != ln:
                lines[i] = new
                changed += 1
    t = "\n".join(lines)
    if changed:
        if dry:
            print("DRY  编号规则 → （W001-W1001）")
        else:
            write(CH, t, n)
            print("OK   编号规则已推进到 （W001-W1001）")

    # ③ HANDOVER 里程碑行
    t, n = read(HAND)
    if "W1001 回次 og:image 全覆盖批·第一轮**：" in t:
        print("SKIP  HANDOVER 已有 W1001 里程碑行")
    else:
        lines = t.split("\n")
        pos = None
        for i, ln in enumerate(lines):
            if ln.startswith("- **W1000 "):
                pos = i
                break
        if pos is None:
            print("FAIL  HANDOVER 未找到 W1000 里程碑行（锚点失配）")
            return 1
        lines.insert(pos, HAND_MILE)
        t = "\n".join(lines)
        if dry:
            print("DRY  HANDOVER 将加 W1001 里程碑行")
        else:
            write(HAND, t, n)
            print("OK   HANDOVER 已加 W1001 里程碑行")

    # ④ 复核
    t, _ = read(CH)
    print("CHANGELOG 现役段：", re.findall(r"^### (W\d{3,4})", t, re.M)[:4])
    print("编号规则：", re.findall(r"（W001-W\d{4}）", t))
    t, _ = read(HAND)
    print("HANDOVER W1001 token：", "W1001" in t,
          "· 里程碑行：", [l[:60] for l in t.split("\n") if "W1001 回次 og:image" in l][:1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
