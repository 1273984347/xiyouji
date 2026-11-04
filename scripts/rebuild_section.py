#!/usr/bin/env python3
"""rebuild_section.py — 幂等段重建独立入口（W1120·工具层·不接收官链主链）。

背景：落段后若某一段需要订正/重排，手改正本会踩三类坑——
  ① **段序被破坏**：CHANGELOG / file-index 正本要求段号严格降序，手插位置错即破坏不变量；
  ② **形态漂移**：手写段体 ≠ 工具生成的块形态（同一批两种写法 ⇒ 后续级联与门禁读数打架）；
  ③ **重跑不幂等**：改一次形态又变一次，收官链重跑即产生噪音 diff。

本工具把「重建**本批自己的那一段**」固化为可重复执行的独立入口：
  · 段体一律由 spec 经 backfill_changelog 的块生成函数产出（**单一事实源·只引用不复制**）；
  · **只动本批段**（历史段一字不动——逐段比对断言，违者零落盘）；
  · **幂等**：段体内容一致 ⇒ 零变化（不写盘）⇒ 二次执行零 diff；
  · **两面同 W 号下界对齐检查**（下界取自两面正本的最小 W 号；不对齐则给归档对齐指引）；
  · 行尾按原文件主导行尾归一写回（W960 混行尾 fail-closed 自锁实证）。

**为何是独立入口而不进收官链主链**：收官链主链（batch_closeout.py）属对方 W1119 批已动面，
本批不双改 ⇒ 独立入口 + 收官链外按需调用（与对方批次零重叠·可零冲突合并）。

用法：
  py -3 scripts/rebuild_section.py --batch W1120 --spec scripts/output/_w1120_spec.json
  py -3 scripts/rebuild_section.py --batch W1120 --spec scripts/output/_w1120_spec.json --apply
退出码：0 成功（含零变化幂等）；1 断言失败（零落盘）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import backfill_changelog as bf  # noqa: E402 — 复用块生成函数与插段定位（单一事实源）

CHANGELOG = "CHANGELOG.md"
FILE_INDEX = os.path.join("scripts", "output", "file-index.md")


def load_spec(path):
    """读 spec（JSON）——解析失败即抛（fail-closed·不静默跳过）。"""
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return json.load(f)


def _seg_span(hits, idx, total_len):
    """段体范围 = 段标题起点 → 下一段起点（或文末）。"""
    start = hits[idx][1]
    end = hits[idx + 1][1] if idx + 1 < len(hits) else total_len
    return start, end


def _replace_segment(text, start, end, block):
    """就地替换段体；内容一致 ⇒ (text, False) 零变化（幂等核心）。

    段尾空白（段间分隔）沿用旧段 ⇒ 替换不破坏段间结构；内容判等用 strip()
    ⇒ 首跑替换后二次执行必然零变化。历史段不在替换范围内（只换本批段）。
    """
    old = text[start:end]
    if old.strip() == block.strip():
        return text, False
    tail = re.search(r"\s*$", old).group(0)
    return text[:start] + block.strip() + tail + text[end:], True


def _hits(text, kind):
    """段起点清单 [(W 号, 起点)]——changelog 走 backfill_changelog 的正则·file-index 同源。"""
    if kind == "changelog":
        return bf.segments(text)
    return [(int(m.group(1)[1:]), m.start()) for m in bf.RE_FI_SEG.finditer(text)]


def rebuild_face(text, batch, block, kind):
    """单面重建 → (新文本, 是否变化, 动作说明)。

    已立段 ⇒ 就地替换该段；未立段 ⇒ 用 backfill_changelog 的降序位插段
    （CHANGELOG 用 insert_before_smaller·file-index 用 insert_fi）。
    """
    bnum = int(str(batch).lstrip("Ww"))   # backfill_changelog 的插段函数收 **int** 批号
    hits = _hits(text, kind)
    for i, (w, _st) in enumerate(hits):
        if w == bnum:
            start, end = _seg_span(hits, i, len(text))
            new_text, changed = _replace_segment(text, start, end, block)
            return new_text, changed, ("已立段·就地重建" if changed else "已立段·内容一致·零变化")
    if kind == "changelog":
        new_text, anchor = bf.insert_before_smaller(text, bnum, block)
        return new_text, True, "未立段·插入于 W%d 之前（降序位）" % anchor
    new_text = bf.insert_fi(text, bnum, block)   # 该函数只回文本（非元组）
    return new_text, True, "未立段·插入（数值位）"


def rebuild_changelog(text, batch, block):
    """CHANGELOG 面重建 → (新文本, 是否变化, 动作说明)。"""
    return rebuild_face(text, batch, block, "changelog")


def rebuild_file_index(text, batch, block):
    """file-index 面重建 → (新文本, 是否变化, 动作说明)。"""
    return rebuild_face(text, batch, block, "file-index")


def _min_w(text, kind):
    """正本最小 W 号（下界）；kind: changelog|file-index。"""
    ws = [w for w, _ in _hits(text, kind)]
    return min(ws) if ws else None


def boundary_check(cl_text, fi_text):
    """两面同 W 号下界对齐检查 → (是否对齐, CHANGELOG 下界, file-index 下界, 提示)。"""
    cl_min = _min_w(cl_text, "changelog")
    fi_min = _min_w(fi_text, "file-index")
    if cl_min is None or fi_min is None:
        return False, cl_min, fi_min, "正本无段（结构异常·须先修结构）"
    if cl_min == fi_min:
        return True, cl_min, fi_min, "两面同下界 W%d ✓" % cl_min
    return (False, cl_min, fi_min,
            "两面下界不一致（CHANGELOG W%d / file-index W%d）⇒ 按同一边界对齐："
            "py -3 scripts/archive_segments.py --target both --max-bytes 262144 --chunk 50 --apply"
            "（体积模式内建两面同下界对齐）" % (cl_min, fi_min))


def history_unchanged(old_text, new_text, batch, kind="changelog"):
    """断言：除本批段外，历史段逐段内容不变 → (是否不变, 差异段号列表)。"""
    def segs(text):
        hits = _hits(text, kind)
        out = []
        for i, (w, _st) in enumerate(hits):
            start, end = _seg_span(hits, i, len(text))
            out.append((w, text[start:end]))
        return out

    bnum = int(str(batch).lstrip("Ww"))
    a = {w: c for w, c in segs(old_text) if w != bnum}
    b = {w: c for w, c in segs(new_text) if w != bnum}
    diff = sorted(set(a) ^ set(b))
    diff += sorted(w for w in set(a) & set(b) if a[w] != b[w])
    return (not diff), diff


def _write(path, text, nl):
    """按原主导行尾写回——禁裸 LF 混入 CRLF 文件（W960 混行尾 fail-closed 实证）。

    末尾必须以真实换行收尾（禁字面反斜杠+n 落盘·W1119 事故同族）。
    """
    out = text.replace("\r\n", "\n")
    if nl != "\n":
        out = out.replace("\n", nl)
    if not out.endswith(nl):
        out += nl
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="幂等段重建（W1120·独立入口）")
    ap.add_argument("--batch", required=True, help="批次号·形如 W1120")
    ap.add_argument("--spec", default=None, help="spec 路径（默认 scripts/output/_<批号>_spec.json）")
    ap.add_argument("--apply", action="store_true", help="落盘（默认只报不写）")
    args = ap.parse_args(argv)

    batch = args.batch.upper()
    if not re.fullmatch(r"W\d{3,4}", batch):
        print("FAIL  批次号形态非法：%s（应形如 W1120）" % batch)
        return 1
    spec_path = args.spec or os.path.join("scripts", "output", "_%s_spec.json" % batch.lower())
    spec = load_spec(spec_path)
    if spec.get("batch") != batch:
        print("FAIL  spec 的 batch 字段（%s）与 --batch（%s）不一致" % (spec.get("batch"), batch))
        return 1

    cl_block = bf.changelog_block(spec)
    fi_block = bf.file_index_block(spec)

    cl_text, cl_nl = bf.load(CHANGELOG)
    fi_text, fi_nl = bf.load(FILE_INDEX)

    cl_new, cl_changed, cl_act = rebuild_changelog(cl_text, batch, cl_block)
    fi_new, fi_changed, fi_act = rebuild_file_index(fi_text, batch, fi_block)

    ok_cl, diff_cl = history_unchanged(cl_text, cl_new, batch, "changelog")
    ok_fi, diff_fi = history_unchanged(fi_text, fi_new, batch, "file-index")
    aligned, cl_min, fi_min, bnote = boundary_check(cl_new, fi_new)

    print("[rebuild] 批次 %s · spec %s" % (batch, spec_path))
    print("[rebuild] CHANGELOG：%s（%s）" % (cl_act, "内容变化" if cl_changed else "零变化"))
    print("[rebuild] file-index：%s（%s）" % (fi_act, "内容变化" if fi_changed else "零变化"))
    print("[rebuild] 历史段不变：CHANGELOG %s / file-index %s"
          % ("OK" if ok_cl else "FAIL·差异段 %s" % diff_cl,
             "OK" if ok_fi else "FAIL·差异段 %s" % diff_fi))
    print("[rebuild] 两面下界：%s" % bnote)

    if not (ok_cl and ok_fi):
        print("FAIL  历史段被改动（禁改历史段）——零落盘")
        return 1
    if not aligned:
        print("FAIL  两面同 W 号下界未对齐——先按上行指引对齐再重建（零落盘）")
        return 1
    if not (cl_changed or fi_changed):
        print("[rebuild] 两面均已是目标形态 ⇒ 零变化（幂等）·不写盘")
        return 0
    if not args.apply:
        print("[rebuild] dry-run：未写盘（加 --apply 落盘）")
        return 0
    _write(os.path.join(ROOT, CHANGELOG), cl_new, cl_nl)
    _write(os.path.join(ROOT, FILE_INDEX), fi_new, fi_nl)
    print("[rebuild] 已落盘：%s + %s" % (CHANGELOG, FILE_INDEX))
    return 0


if __name__ == "__main__":
    sys.exit(main())
