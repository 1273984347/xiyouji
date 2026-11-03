#!/usr/bin/env python3
"""check_registration_surface.py — 登记面一致性自检闸（W1116 建）

为什么需要它（W1113~W1115 实证）：加一个 CHANGELOG 段 + 一个台账认领行，会连带
六个登记面必须同步，而收官链八/九步**不覆盖**其中任何一项：
  ① 台账本批行的「CHANGELOG 版段」列（漏回填 ⇒ 永久「—（待回填）」）
  ② HANDOVER「最后更新」链首（漏更新 ⇒ 与现役段不一致·治理契约判红）
  ③ CHANGELOG 编号规则段上限（漏 bump ⇒「W001-W1114」与最新段不一致）
  ④ HANDOVER「最后更新」链条目数（堆太多 ⇒ 体积窗 C7 判红）
  ⑤ file-index 的本批段登记（漏同步 ⇒ 索引健康判红）
  ⑥ 台账正本数据行数（加行前未腾窗 ⇒ 行数窗判红）

本闸把六项做成可执行断言，收官链末位必跑；任一项不符即判红并给出改法。
数据行口径复用 scripts/archive_ledger_rows.py 的 ROW_RE（唯一事实源·不另写正则）。

用法：
    py -3 scripts/check_registration_surface.py --batch W1116
    py -3 scripts/check_registration_surface.py --batch W1116 --json
退出码：0 全绿 / 1 有 FAIL
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys

ROOT = os.environ.get("XIYOUJI_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = "docs/00-导读/W批次编号对账表.md"
CHANGELOG = "CHANGELOG.md"
HANDOVER = "HANDOVER.md"
FILE_INDEX = "scripts/output/file-index.md"
WINDOW = 60


def _read(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def _row_re():
    """复用仓内唯一事实源的行解析（archive_ledger_rows.ROW_RE）·不另写正则。"""
    here = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(here, "archive_ledger_rows.py")
    if not os.path.isfile(p):
        return None
    sp = importlib.util.spec_from_file_location("_alr_row_re", p)
    mod = importlib.util.module_from_spec(sp)
    try:
        sp.loader.exec_module(mod)
    except Exception:
        return None
    return getattr(mod, "ROW_RE", None)


def _top_w(chg):
    m = re.search(r"^### W(\d{4})", chg or "", re.M)
    return int(m.group(1)) if m else None


def _ledger_rows(text, row_re):
    return [ln for ln in (text or "").splitlines() if row_re.match(ln)]


def check_all(batch):
    """返回 (fails, notes)；fails 为可执行改法描述列表。"""
    fails = []
    notes = []
    chg = _read(CHANGELOG)
    led = _read(LEDGER)
    hov = _read(HANDOVER)
    fidx = _read(FILE_INDEX)
    row_re = _row_re()
    if row_re is None:
        return ["行解析唯一事实源不可用（scripts/archive_ledger_rows.py 缺失或不可导入）"], notes
    top = _top_w(chg)
    if top is None:
        return ["CHANGELOG 顶段 W 号不可解析"], notes
    notes.append("现役段 W%d" % top)

    # ① 台账本批行的 CHANGELOG 版段列
    rows = _ledger_rows(led, row_re)
    hit = None
    for ln in rows:
        if re.match(r"^\|\s*W%d\s*\|" % int(batch), ln):
            hit = ln
            break
    if hit is None:
        fails.append("台账无 W%s 行（认领行未登记？）" % batch)
    else:
        cols = [c.strip() for c in hit.split("|")]
        seg = cols[4] if len(cols) > 4 else ""
        if not seg:
            fails.append("台账 W%s 行的 CHANGELOG 版段列为空 ⇒ 跑 ledger_backfill.py --w %s --cascade \"W%s（<日期>）\"" % (batch, batch, batch))
        elif seg.startswith("—"):
            notes.append("台账 W%s 版段列仍待回填（回填发生在收官之后·下一批 precheck 复核）" % batch)
        else:
            notes.append("台账 W%s 版段列 = %s" % (batch, seg))

    # ⑥ 台账正本数据行数 ≤ 窗口
    n = len(rows)
    if n > WINDOW:
        fails.append("台账正本 %d 数据行 > 窗口 %d ⇒ 先 archive_ledger_rows.py --keep %d --apply" % (n, WINDOW, WINDOW - 1))
    else:
        notes.append("台账正本 %d 数据行 ≤ 窗口 %d" % (n, WINDOW))

    # ②④ HANDOVER 最后更新链首与条目数
    # 只取真正的链条目行（「最后更新：<日期>（W#### …」形态）⇒ 排除阅读契约/维护契约里
    # 仅提到「最后更新」字样的说明行（否则把说明行当链条目 ⇒ 假阳）
    upd = [ln for ln in (hov or "").splitlines()
           if re.search(r"最后更新：\d{4}-\d{2}-\d{2}（W\d{4}", ln)]
    if not upd:
        fails.append("HANDOVER 无「最后更新」行 ⇒ 交接链首未维护")
    for i, ln in enumerate(upd, 1):
        # 条目数只数「批次摘要」⇒ 排除「（W#### 及更早批次详见 CHANGELOG.md）」这类指针
        # 条目数 = 该链条目行内「W####」的出现次数（后续条目用「；」或「·」分隔·不带前缀）
        ws = [w for w in re.findall(r"W(\d{4})", ln) if not re.search(r"W%s[^）]*及更早" % w, ln)]
        if not ws:
            fails.append("HANDOVER 第 %d 处「最后更新」行无 W 号" % i)
            continue
        if int(ws[0]) != top:
            fails.append("HANDOVER 第 %d 处「最后更新」链首 W%s ≠ CHANGELOG 现役段 W%d ⇒ 每批须前置最新条目" % (i, ws[0], top))
        if len(ws) > 3:
            fails.append("HANDOVER 第 %d 处「最后更新」链条目 %d 条 > 3 ⇒ 保留最新 3 条其余迁 CHANGELOG" % (i, len(ws)))
    if upd:
        notes.append("HANDOVER 最后更新 %d 处（链首与条目数已核）" % len(upd))

    # ③ CHANGELOG 编号规则段上限
    m = re.search(r"W001-W(\d{4})", chg or "")
    if not m:
        fails.append("CHANGELOG 编号规则段上限不可解析")
    elif int(m.group(1)) != top:
        fails.append("CHANGELOG 编号规则段上限 W001-W%s ≠ 现役段 W%d ⇒ 同步该段" % (m.group(1), top))
    else:
        notes.append("CHANGELOG 编号规则段上限 = W%d" % top)

    # ⑤ file-index 本批段登记
    if fidx is None:
        fails.append("file-index 缺失（scripts/output/file-index.md）")
    elif not re.search(r"^## W%d\s" % int(batch), fidx, re.M):
        fails.append("file-index 无 W%s 段登记 ⇒ 落段时同步（cascade 级联段面负责）" % batch)
    else:
        notes.append("file-index 已含 W%s 段" % batch)

    return fails, notes


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    batch = None
    as_json = "--json" in argv
    for i, a in enumerate(argv):
        if a == "--batch" and i + 1 < len(argv):
            batch = argv[i + 1]
    if not batch:
        print("用法：py -3 scripts/check_registration_surface.py --batch W#### [--json]")
        return 2
    m = re.match(r"^W?(\d{4})$", batch.strip())
    if not m:
        print("批号形态非法：%s" % batch)
        return 2
    batch = m.group(1)
    fails, notes = check_all(batch)
    for n in notes:
        print("NOTE  " + n)
    for f in fails:
        print("FAIL  " + f)
    if as_json:
        print(json.dumps({"fail": len(fails)}, ensure_ascii=False))
    if fails:
        print("---- 登记面一致性闸：%d FAIL ----" % len(fails))
        return 1
    print("---- 登记面一致性闸：六项全通过 ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
