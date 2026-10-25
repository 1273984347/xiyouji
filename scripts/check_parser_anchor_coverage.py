#!/usr/bin/env python3
"""check_parser_anchor_coverage.py — 解析器锚点覆盖面扫描（W965 沉淀·W964 双虫探针常驻化）。

方法论：拿每个滚动/计数机制的**锚点正则**去对拍目标文件的**原始形态全集**——
凡是「长得像条目/段/行」却不被锚点命中的形态，就是滚动器/计数器的失明区。
W964 用这支探针挖出两只真虫（AGENTS 脚注 52 条中文日期失明 + HANDOVER 里程碑
6 个括注块失明），故沉淀为常驻扫描；报告型（不判退出码），供批收尾与 review 手跑。

机制清单（锚点=各机制现役正则的等价形态）：
  M1 AGENTS 版本脚注条目（batch_cascade 滚动器·双日期形态）
  M2 HANDOVER 里程碑块（旋转器·括注放宽形态）
  M3 HANDOVER 头尾链条目（裁剪计数器·阿拉伯日期形态）
  M4 CHANGELOG/file-index 段标题（级联/补段/触发器共用双形态）
  M5 台账认领行（preflight parse_ledger）
  M6 stats / doc-sync 实体标记（C5b/C5d 与旁文档豁免）

用法：
  py -3 scripts/check_parser_anchor_coverage.py            # 报告（exit 0）
  py -3 scripts/check_parser_anchor_coverage.py --self-test
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CN_DATE = r"[一二三四五六七八九〇零十廿卅]+年[一二三四五六七八九〇零十廿卅]+月[一二三四五六七八九〇零十廿卅]+日"
AR_DATE = r"20\d{2}-\d{2}-\d{2}"
BOTH_DATE = "(?:%s|%s)" % (AR_DATE, CN_DATE)

CHECKS = [
    {
        "name": "M1 AGENTS 脚注条目",
        "files": ["AGENTS.md"],
        "raw": r"；" + BOTH_DATE + r"（W\d{3,4}）",
        "anchor": r"；(?=" + BOTH_DATE + r"（)",  # 滚动器按此切分
        "pos_sensitive": True,
    },
    {
        "name": "M2 HANDOVER 里程碑块",
        "files": ["HANDOVER.md"],
        "raw": r"(?m)^- \*\*(?:v[\d.]+ )?W\d{3,4}",
        "anchor": r"(?m)^- \*\*(?:v[\d.]+ )?W\d{3,4}[^*]*\*+[^\r\n:*]{0,30}：",
        "pos_sensitive": True,
    },
    {
        "name": "M3 HANDOVER 头尾链条目",
        "files": ["HANDOVER.md"],
        "raw": r"[；·]" + BOTH_DATE + r"（W\d{3,4}\b",
        "anchor": r"[；·]" + BOTH_DATE + r"（W\d{3,4}\b",
        "pos_sensitive": True,
    },
    {
        "name": "M4a CHANGELOG 段标题",
        "files": ["CHANGELOG.md",
                  os.path.join("archive", "docs", "CHANGELOG-ARCHIVE.md"),
                  os.path.join("archive", "docs", "CHANGELOG-ARCHIVE-tier2.md")],
        "raw": r"(?m)^### W",
        "anchor": r"(?m)^### (?:v[\d.]+（[^）]*）：W\d+|W\d+（" + BOTH_DATE + r"）：)",
        "pos_sensitive": True,
    },
    {
        "name": "M4b file-index 段标题",
        "files": ["scripts/output/file-index.md",
                  os.path.join("archive", "docs", "file-index-ARCHIVE.md")],
        "raw": r"(?m)^## W\d+ ",
        "anchor": r"(?m)^## W\d+ ",
        "pos_sensitive": True,
    },
    {
        "name": "M5 台账认领行",
        "files": [os.path.join("docs", "00-导读", "W批次编号对账表.md"),
                  os.path.join("archive", "docs", "W批次编号对账表-ARCHIVE.md")],
        "raw": r"(?m)^\|[ 狦]?W\d{3,4}",
        "anchor": r"(?m)^\|\s*W\d{3,4}\s*\|",
        "pos_sensitive": True,
    },
    {
        "name": "M6 实体标记形态",
        "files": ["pytest.ini", "AGENTS.md", "HANDOVER.md"],
        "raw": r"<!--\s*stats:[a-z_]+\s*-->",
        "anchor": r"<!--stats:[a-z_]+-->",
        "pos_sensitive": True,
    },
]


def sweep():
    """跑全部机制 → (报告行, 盲区数)。"""
    lines, blind_total = [], 0
    for c in CHECKS:
        raw_n = anc_n = 0
        samples = []
        for f in c["files"]:
            p = os.path.join(ROOT, f)
            if not os.path.exists(p):
                lines.append("  %-24s 缺文件 %s（跳过）" % (c["name"], f))
                continue
            t = open(p, encoding="utf-8", newline="").read()
            raws = list(re.finditer(c["raw"], t, re.M))
            ancs = list(re.finditer(c["anchor"], t, re.M))
            raw_n += len(raws)
            anc_n += len(ancs)
            if c["pos_sensitive"]:
                anc_starts = {m.start() for m in ancs}
                for m in raws:
                    if m.start() not in anc_starts:
                        ls = t.rfind("\n", 0, m.start()) + 1
                        samples.append("%s :: %s" % (os.path.basename(f), t[ls:ls + 64].replace("\n", "⏎")))
        if raw_n == anc_n and not samples:
            lines.append("  %-24s 覆盖完整（%d/%d）" % (c["name"], anc_n, raw_n))
        else:
            blind_total += len(samples)
            lines.append("  %-24s 盲区 %d 处（原始 %d / 锚点 %d）%s"
                         % (c["name"], len(samples), raw_n, anc_n,
                            ("样本: " + " ┃ ".join(samples[:2])) if samples else ""))
    return lines, blind_total


def _self_test() -> int:
    """自测：注入合成盲区必须被报出（探针可证伪）+ 合成干净树必须全绿。"""
    import tempfile
    fails = []


    def make_pair(src_txt, raw, anchor, fname="f.md"):
        with tempfile.TemporaryDirectory() as td:
            f = os.path.join(td, fname)
            open(f, "w", encoding="utf-8", newline="").write(src_txt)
            raws = list(re.finditer(raw, src_txt, re.M))
            ancs = list(re.finditer(anchor, src_txt, re.M))
            anc_starts = {m.start() for m in ancs}
            blind = [m.start() for m in raws if m.start() not in anc_starts]
        return len(blind)

    # M1 形态：中文日期条目对「仅阿拉伯锚点」必须报盲区（W964 病根复现）
    txt = "头；二〇二六年十月二十日（W808）条目；2026-10-20（W818）条目"
    if make_pair(txt, r"；" + BOTH_DATE + r"（W\d{3,4}）", r"；(?=" + AR_DATE + r"（)") != 1:
        fails.append("中文日期盲区未被探针报出（W964 病根必须可复现）")
    if make_pair(txt, r"；" + BOTH_DATE + r"（W\d{3,4}）", r"；(?=" + BOTH_DATE + r"（)") != 0:
        fails.append("双形态锚点下不应有盲区")
    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：盲区可报出 + 干净形态可放行（探针可证伪）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="解析器锚点覆盖面扫描（W965 沉淀）")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    print("== 解析器锚点覆盖面扫描（W965·报告型不判退出码）==")
    lines, blind_total = sweep()
    for line in lines:
        print(line)
    print("==== 盲区合计 %d 处（0=各滚动/计数机制无形态失明）====" % blind_total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
