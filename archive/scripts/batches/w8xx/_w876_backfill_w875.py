#!/usr/bin/env python3
"""_w876_backfill_w875.py — W876 收尾专用：只补 W875 一个递延段（一次性驱动件）。

**为什么不能直接跑 backfill_changelog.py --apply**：它的 collect_pending() 会把
scripts/output/ 下所有未立段 spec 一并补上——此刻 W875/W876/W877/W878 四号全在递延
链上：W877/W878 属并行会话批次（已登记豁免·留待后续补段批处理），W876 要走
batch_cascade 十面级联（本批页脚 token / 交接里程碑 / AGENTS 脚注都在那一面），
不能被补段工具代劳。故本驱动只调补段工具的插入原语补 W875 一段，断言与落盘纪律
（段序严格降序·编号规则只升不降·保持原文件行尾）与原工具逐条对齐。

**前置**：W875 已由本批前的并行提交落库（13a2c62c·内容在库只差段）；本驱动补段后，
batch_cascade 的「批次号 = 顶段 + 1」断言对 W876 即成立。

用法：py -3 scripts/_w876_backfill_w875.py --dry-run | --apply
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import backfill_changelog as bf  # noqa: E402

SPEC = os.path.join(ROOT, "scripts", "output", "_w875_spec.json")
TARGET = 875


def run(apply):
    spec = json.load(open(SPEC, encoding="utf-8"))
    assert spec["batch"] == "W%d" % TARGET, "spec.batch=%s（应为 W875）" % spec["batch"]
    missing = [k for k in bf.SPEC_KEYS if k not in spec]
    assert not missing, "W875 spec 缺字段：%s" % missing

    cl, cl_nl = bf.load("CHANGELOG.md")
    fi, fi_nl = bf.load("scripts/output/file-index.md")
    established = {w for w, _ in bf.segments(cl)}
    assert TARGET not in established, "W875 段已存在（不必补）"

    seg_before = len(bf.segments(cl))
    fi_before = len(bf.RE_FI_SEG.findall(fi))
    cl, anchor = bf.insert_before_smaller(cl, TARGET, bf.changelog_block(spec))
    fi = bf.insert_fi(fi, TARGET, bf.file_index_block(spec))

    # 编号规则只升不降（W001-W### 锚点）
    m = bf.RE_RULE.search(cl)
    assert m, "编号规则「（W001-W###）」锚点缺失"
    old_max = int(m.group(1))
    if old_max < TARGET:
        cl = cl.replace("（W001-W%d）" % old_max, "（W001-W%d）" % TARGET, 1)

    # 落盘前全量断言（与 backfill_changelog 一致）
    segs = bf.segments(cl)
    ws = [w for w, _ in segs]
    assert len(ws) == seg_before + 1, "CHANGELOG 段数不符：%d + 1 != %d" % (seg_before, len(ws))
    assert ws == sorted(ws, reverse=True), "段序非严格降序：%s" % ws[:8]
    assert len(set(ws)) == len(ws), "出现重复段号"
    head = "### W%d（%s）：%s" % (TARGET, spec["date"],
                                 re.sub(r"^W\d+\s+", "", spec["title"]).strip())
    assert cl.count(head) == 1, "W875 段标题命中 %d 次（应为 1）" % cl.count(head)
    fi_ws = [int(x[1:]) for x in bf.RE_FI_SEG.findall(fi)]
    assert len(fi_ws) == fi_before + 1, "file-index 段数不符"
    assert fi_ws == sorted(fi_ws, reverse=True), "file-index 段序非降序"

    print("[DRY-RUN] W875 段将插在 W%d 段之前 · 规则行 W001-W%d → W001-W875"
          % (anchor, old_max))
    if not apply:
        return 0
    for path, text, nl in (("CHANGELOG.md", cl, cl_nl),
                           ("scripts/output/file-index.md", fi, fi_nl)):
        with open(os.path.join(ROOT, path), "w", encoding="utf-8", newline="") as f:
            f.write(text.replace("\n", nl))
        print("  写入 %s（%s）" % (path, "CRLF" if nl == "\r\n" else "LF"))
    print("[APPLY] W875 段已补：CHANGELOG %d→%d 段 · file-index %d→%d 段"
          % (seg_before, len(ws), fi_before, len(fi_ws)))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not (args.apply or args.dry_run):
        ap.error("必须指定 --dry-run 或 --apply")
    return run(args.apply)


if __name__ == "__main__":
    sys.exit(main())
