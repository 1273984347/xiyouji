#!/usr/bin/env python3
"""archive_ledger_rows.py — 台账对账表行归档常驻工具（W970 建·W968 一次性拆分的工具化）。

职责：台账正本（docs/00-导读/W批次编号对账表.md）超窗时，把最老的行按**号序**迁入
archive/docs/W批次编号对账表-ARCHIVE.md（W968 建容器）。与 archive_segments.py（段式）
互补：台账是表格行且行序有穿插（W968 实证 52 处），必须按号切分而非位置切分。

守恒断言（五道，与 W968 迁移同款）：
  A1 行数守恒：拆前行数 = 留存 + 迁出
  A2 内容守恒：迁出行逐条字节出现在迁后归档
  A3 正本非行内容逐字节不动
  A4 parse_ledger 语义不变：max W 不变、在途行集合不变、迁出最大号 < 留存最小号
  A5 归档行保持原文件相对顺序

窗口：正本 60 行（check_doc_size_budget C5 硬判据）。默认 --keep 59（预留当批认领 +1）。

用法：
  py -3 scripts/archive_ledger_rows.py --dry-run
  py -3 scripts/archive_ledger_rows.py --apply
  py -3 scripts/archive_ledger_rows.py --keep 55 --apply
退出码：0 成功；1 断言失败（零落盘）。
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import preflight_check as pf  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join("docs", "00-导读", "W批次编号对账表.md")
ARC = os.path.join("archive", "docs", "W批次编号对账表-ARCHIVE.md")
ROW_RE = re.compile(r"^\| W(\d{3,4}) ")


def move(keep, apply, src_p=None, arc_p=None):
    src_p = src_p or os.path.join(ROOT, SRC)
    arc_p = arc_p or os.path.join(ROOT, ARC)
    lines = open(src_p, encoding="utf-8", newline="").read().split("\n")
    row_idx = [i for i, ln in enumerate(lines) if ROW_RE.match(ln)]
    assert row_idx, "正本无行（结构异常）"
    ws = {i: int(ROW_RE.match(lines[i]).group(1)) for i in row_idx}
    ordered = sorted(row_idx, key=lambda i: -ws[i])  # 号降序
    keep_set = set(ordered[:keep])
    move_idx = [i for i in row_idx if i not in keep_set]
    if not move_idx:
        print("无迁出行（正本 %d 行 ≤ keep %d）" % (len(row_idx), keep))
        return 0
    moved_lines = [lines[i] for i in move_idx]
    moved_ws = [ws[i] for i in move_idx]
    kept_ws = [ws[i] for i in sorted(keep_set)]
    assert max(moved_ws) < min(kept_ws), "号区间交叠（异常）"

    arc_txt = open(arc_p, encoding="utf-8", newline="").read() if os.path.exists(arc_p) else ""
    anl = "\r\n" if "\r\n" in arc_txt else "\n"
    new_arc = arc_txt
    if new_arc and not new_arc.endswith(anl):
        new_arc += anl
    note = "- %s（修剪迁入 %d 行·W%d-W%d·号序切分）" % (
        datetime.date.today().isoformat(), len(moved_lines), min(moved_ws), max(moved_ws))
    new_arc += note + anl + "\n".join(moved_lines).replace("\n", anl) + anl

    new_lines = [ln for i, ln in enumerate(lines) if i not in set(move_idx)]
    src_text = "\n".join(new_lines)

    # A1 行数守恒
    assert len(row_idx) == len(keep_set) + len(move_idx)
    # A2 内容守恒
    for mln in moved_lines:
        assert mln in new_arc, "迁出行未入档：" + mln[:50]
    # A3 非行内容逐字节不动
    old_nonrow = [ln for i, ln in enumerate(lines) if i not in set(row_idx)]
    new_nonrow = [ln for i, ln in enumerate(new_lines) if not ROW_RE.match(ln)]
    assert old_nonrow == new_nonrow, "非行内容被改动"
    # A4 parse_ledger 语义不变
    led = pf.parse_ledger(src_text)
    led_before = pf.parse_ledger("\n".join(lines))
    assert led["max_w"] == led_before["max_w"] == max(kept_ws), "max W 异常"
    assert pf.duplicate_wnums(led["rows"]) == [], "正本同号多行"
    inflight_before = [r["w"] for r in led_before["rows"] if pf.is_inflight(r["status"]) and r["touches"]]
    inflight_after = [r["w"] for r in led["rows"] if pf.is_inflight(r["status"]) and r["touches"]]
    assert inflight_before == inflight_after, "在途行集合变化"
    # A5 归档内迁出块 = 注记行 + 迁出行按**源文件相对顺序**逐字节一致。
    # 按号切分、不要求号升序——台账行序穿插是常态（W968 实证 52 处）；旧断言
    # moved_ws == sorted(moved_ws) 与此矛盾，迁出段物理序降序时必崩（W976 修）。
    assert new_arc.endswith(note + anl + "\n".join(moved_lines).replace("\n", anl) + anl), \
        "归档内迁出块与源相对顺序不一致"

    print("迁出 %d 行（W%d-W%d）·正本留 %d 行（W%d-W%d）"
          % (len(moved_lines), min(moved_ws), max(moved_ws), len(kept_ws), min(kept_ws), max(kept_ws)))
    if apply:
        with open(src_p, "w", encoding="utf-8", newline="") as f:
            f.write(src_text)
        with open(arc_p, "w", encoding="utf-8", newline="") as f:
            f.write(new_arc)
        print("已落盘 %s + %s" % (SRC, ARC))
    return 0


def _self_test() -> int:
    """自测（W976 重写）：不再复算切分逻辑，直接走 move() 全链路——
    升序穿插（W968 形态）、降序穿插（旧 A5 断言必崩形态）、无迁出三形态都必须成功；
    守恒五道（A1-A5）在 move() 内部生效，rc=0 即全过。旧自测的病根：自建样本的
    迁出集恰好物理升序，测不出判据会失败的最小形态（自测通过≠判据正确）。"""
    import tempfile

    def _run(rows_ws, keep):
        lines = ["| W%d | 行%d | a | b | 已收官 | s | x |" % (w, w) for w in rows_ws]
        txt = "# 台账样本\n\n" + "\n".join(lines) + "\n\n## ASCII\n- W# 三位数零填充（W001 形态）。\n"
        td = tempfile.mkdtemp()
        sp = os.path.join(td, "l.md")
        open(sp, "w", encoding="utf-8", newline="").write(txt)
        ap = os.path.join(td, "a.md")
        rc = move(keep, True, src_p=sp, arc_p=ap)
        src_after = open(sp, encoding="utf-8", newline="").read()
        arc_after = open(ap, encoding="utf-8", newline="").read() if os.path.exists(ap) else ""
        return rc, src_after, arc_after

    fails = []
    # 形态一（W968 实证）：行序≠号序·迁出集 {905,908} 物理序恰升序
    rc, src, arc = _run([910, 905, 912, 908, 911], 3)
    if rc != 0 or not all("| W%d " % w in arc for w in (905, 908)) or "| W905 " in src:
        fails.append("升序穿插形态失败（迁出/留存不符）")
    # 形态二：迁出集物理序**降序**（旧 A5 必崩的形态·W976 实证 914/915 真实台账）
    rc, src, arc = _run([914, 915, 913], 1)
    if rc != 0:
        fails.append("降序穿插形态失败（旧 A5 必崩形态未被修复覆盖）")
    elif arc.find("| W914 ") > arc.find("| W913 ") or "| W915 " not in src:
        fails.append("降序穿插形态归档序/留存错误")
    # 形态三：行数 ≤ keep·无需迁出（不建归档文件）
    rc, src, arc = _run([920, 919], 5)
    if rc != 0 or arc:
        fails.append("无迁出形态失败（不应落归档）")

    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：升序/降序穿插 + 无迁出三形态 move() 全链路（判据可证伪）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="台账对账表行归档（W970）")
    ap.add_argument("--keep", type=int, default=59, help="正本保留行数（默认 59=窗口 60-当批认领 1）")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    if not (args.apply or args.dry_run):
        ap.error("必须指定 --dry-run 或 --apply")
    return move(args.keep, args.apply)


if __name__ == "__main__":
    sys.exit(main())
