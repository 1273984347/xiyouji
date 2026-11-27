#!/usr/bin/env python3
"""archive_segments.py — 治理文档版段滚动归档常驻工具（W960 建 · W921 三道守恒断言沉淀）。

背景：CHANGELOG/file-index 的版段归档此前只有一次性脚本（W417/W511/W921 三次人工批），
W921 的搬段脚本（三道守恒断言）跑完即弃 ⇒ 同样的搬家每次都要重写。本工具把那次的经验
沉淀为常驻工具，配 check_doc_size_budget.py 的窗口门禁形成「超窗即被点名 + 点名即有工具」闭环。

做什么：把正本**最尾部的**（=最老的）N 个版段整块迁入归档容器——
  - CHANGELOG.md      → archive/docs/CHANGELOG-ARCHIVE.md（插在归档文件首个段之前·归档 newest-at-top 约定）
  - file-index.md     → archive/docs/file-index-ARCHIVE.md（追加在归档文件末尾·按迁移批次记账约定
                        + 头部「> 归档时间：」链追加本次迁移注记；W1228 修：原名误写大写
                        FILE-INDEX-ARCHIVE.md——Windows 大小写不敏感掩盖，Linux fresh clone 收官链死）

守恒断言（W921 三道 + 两条新增，任何一条不过零落盘）：
  A1 段数守恒：正本段数 = 留存段数 + 迁出段数；归档段数 + 迁出段数 = 迁后归档段数
  A2 内容守恒：迁出文本块逐字节出现在迁后归档文件中（原封不动·禁改写）
  A3 锚点不动：正本留存前缀逐字节不变；编号规则行不变；顶段标题行不变
  A4 降序完好：正本留存段严格降序；迁出块内部严格降序
  A5 归档序：CHANGELOG-ARCHIVE 既有段最大号 < 迁出块最小号（top 插入不破坏 newest-at-top 语义）

行尾：经 batch_cascade.load 读入（混行尾 fail-closed），按原文件行尾写回。

用法：
  py -3 scripts/archive_segments.py --dry-run                 # 两面都演练
  py -3 scripts/archive_segments.py --apply                   # 两面都落盘
  py -3 scripts/archive_segments.py --target changelog --keep 109 --apply
退出码：0 成功；1 断言失败（零落盘）。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import batch_cascade as bc  # noqa: E402 — 复用 load()（混行尾 fail-closed）与段正则
from utils import gate_common as gc  # noqa: E402 — 体积上限单一事实源（W1315 下沉）

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RE_CL_SEG = re.compile(r"^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（[^）]*）：)", re.M)
RE_FI_SEG = re.compile(r"^## (W\d+) ", re.M)

# W1340（P1-2）：迁移台账——每次 --apply 追加（每面一条），用于回答「这批段是什么时候、
# 按什么水位迁走的」。只追加不改写；与归档容器同目录，随批入库。
ARCHIVE_LOG = os.path.join("archive", "docs", "archive-log.jsonl")

TARGETS = {
    "changelog": {
        "src": "CHANGELOG.md",
        "arc": os.path.join("archive", "docs", "CHANGELOG-ARCHIVE.md"),
        "re_seg": RE_CL_SEG,
        "arc_mode": "top",
    },
    "file-index": {
        "src": os.path.join("scripts", "output", "file-index.md"),
        "arc": os.path.join("archive", "docs", "file-index-ARCHIVE.md"),  # W1228 修：与 tracked 实名一致（原大写 FILE-INDEX 在 Linux 下解析为另一文件）
        "re_seg": RE_FI_SEG,
        "arc_mode": "append",
    },
}


def _wnum(m):
    """段号统一解析：changelog 双形态（v 前缀形态 group(1)=纯数字·新形态 group(2)=纯数字）与
    file-index 单组形态（group(1)=W 前缀）通吃。"""
    g1 = m.group(1)
    if g1 is not None:
        return int(g1[1:] if g1.startswith("W") else g1)
    g2 = m.group(2) if m.re.groups >= 2 else None
    return int(g2)


def plan(src_text, re_seg, keep):
    """计算切分点：保留前 keep 个段（最新），迁出其余（最老）。返回 (cut, moved_ws)。

    W1014 修「未超窗即断言失败」：原实现 `assert len(hits) > keep`——段数**恰等于** keep
    （级联插入一段后正本正好 110 = 窗口 110）时抛 AssertionError，被 batch_cascade 的
    `_refresh_window()` 判为「回窗 FAIL」⇒ 级联 exit 2，但体积判据实测三项全 ok（未超窗）。
    即回窗把「无需回窗」误报成失败，徒令级联收尾返红。改：未超窗时返回 (None, [])（无迁出）。
    """
    hits = [(_wnum(m), m.start()) for m in re_seg.finditer(src_text)]
    assert hits, "正本未找到任何段（结构异常）"
    ws = [w for w, _ in hits]
    assert ws == sorted(ws, reverse=True), "正本段序非严格降序（先修复再归档）"
    assert len(set(ws)) == len(ws), "正本出现重复段号（先修复再归档）"
    if len(hits) <= keep:
        return None, []  # 未超窗 → 无段可迁（非失败）
    cut = hits[keep][1]
    moved_ws = [w for w, _ in hits[keep:]]
    # W1292 根修：moved_ws 必须与**实际迁出块**同源（口径不一致 ⇒ 断言恒触发）。
    # 病根（实测）：CHANGELOG 的「末尾文件级块」（`# 更新日志` H1 + 阅读契约 + Unreleased +
    # 编号规则行）会**沉在段区中间**（实测 H1 在行 522，其下仍挂 W1248/W1247/W1246 三段·
    # 起点 96878/97683/98560 均 > tail_start 96869）⇒ 迁出块止于 tail_start
    # （split_tail_block）⇒ 实际迁出段 = 落在 [cut, tail_start) 的段（实测 4 段）；
    # 而旧实现按 hits[keep:] 计 ⇒ **段表多算**（实测 7 vs 4）
    # ⇒ `assert len(moved_in_block) == len(moved_ws)` 在该边界必然触发
    # （分段迁 17 段成功、第二步 7 段仍失败 ⇒ 不是规模问题，是口径不一致）。
    # 修法：moved_ws 只计**实际落在迁出区间内**的段 ⇒ 与 moved_in_block 同源 ⇒ 恒等。
    _tail = _tail_block_start(src_text)
    if _tail is not None and _tail > cut:
        moved_ws = [w for w, s0 in hits[keep:] if s0 < _tail]
    return cut, moved_ws


def _to_nl(text, target_nl):
    """任意行尾归一到目标行尾（W960 实证：正本 CRLF 块直插 LF 归档容器会造出混行尾·fail-closed 自锁）。"""
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    if target_nl != "\n":
        t = t.replace("\n", target_nl)
    return t


def _rule_seg_index(hits, src_text):
    """返回含「（W001-W…）」编号规则串的段下标（找不到返回 None）——该段**不得被迁出**。
    W1119 实证：编号规则段上限是版本面字面量（version_surface.advance_changelog_rule 要改写它）
    ⇒ 若被腾窗迁进 archive，版本面推进器即 fail-closed「未找到锚点」⇒ 整条收官链停摆。
    """
    tail = _tail_block_start(src_text)
    for i, (_w, start) in enumerate(hits):
        end = hits[i + 1][1] if i + 1 < len(hits) else len(src_text)
        m = re.search(r"（W001-W\d+）", src_text[start:end])
        if not m:
            continue
        if tail is not None and (start + m.start()) >= tail:
            continue
        # W1309 修（过严约束治本）：真锚点只在**治理声明行**（以「>」开头的引用行）——
        # file-index 表格登记行里的「本批段 + 编号规则段推进（W001-W1258）」只是**登记描述**
        # ·不是锚点本体（真锚点在 CHANGELOG 的末尾文件级块内·不随段迁出）⇒ 原判据把
        # file-index 的最老段误判为「不可迁出段」⇒ max_k=0 ⇒ **体积窗永远无法腾窗**（死锁）。
        _ls = src_text.rfind("\n", start, start + m.start())
        _line_start = start if _ls == -1 else _ls + 1
        if not src_text[_line_start:start + m.start()].lstrip().startswith(">"):
            continue
        return i
    return None


def _tail_block_start(src_text):
    """返回正本末尾文件级块的起始下标；无末尾块返回 None。

    W1130 实证（两面下界对齐时触发）：归档迁出时的迁出块是 s[cut:]（一路到文件末尾）
    => 末尾文件级块（# 更新日志标题 + 阅读契约 + Unreleased + 编号规则行（含编号规则串）
    + 全站页数口径 + 维护契约）也被一起搬走 => 正本不再含编号规则串
    => 版本面推进器 fail-closed「编号规则段上限未找到锚点」=> 整条收官链停摆。
    正确行为：末尾块不属于任何批段 => 必须留在正本，不得随段迁出。
    """
    m = re.search(r"(?m)^# 更新日志\s*$", src_text)
    if m:
        return m.start()
    # W1233 增锚：级联滚动把现役段推顶后，尾部「## [Unreleased] 段」（编号规则行 +
    # 全站页数口径等文件级块·W1232 实证其被随段迁走 ⇒ 版本面推进器 fail-closed 复现）
    # 同属「非批段的末尾文件级块」——同规则留守正本。
    m2 = re.search(r"(?m)^## \[Unreleased\]\s*$", src_text)
    return m2.start() if m2 else None


def split_tail_block(src_text, cut, tail_start):
    """按「末尾文件级块」边界拆分迁出文本与留存文本。

    返回 (moved_text, kept_text)：迁出块不含末尾块（留存在正本）；
    tail_start 为 None 或 <= cut 时行为与原实现一致。
    """
    if tail_start is None or tail_start <= cut:
        return src_text[cut:], src_text[:cut]
    return src_text[cut:tail_start], src_text[:cut] + src_text[tail_start:]


def _split_decl_blocks(src_text):
    """抽出治理文档声明行（以「> **维护契约**」开头的引用行），返回 (remaining, decls)。

    W1130 实证：file-index.md 的「> **维护契约**：本索引按 W 追加登记……」声明行位于段区**中部**，
    体积模式迁出（迁出块 = s[cut:]）时随之被搬走 => 正本不再含「维护契约」
    => 治理文档维护契约门禁判红。声明行不属于任何批段 => 必须留在正本。
    """
    lines = src_text.splitlines(True)
    keep, decls = [], []
    for _line in lines:
        if _line.lstrip().startswith("> **维护契约**"):
            decls.append(_line)
        else:
            keep.append(_line)
    return "".join(keep), "".join(decls)


def plan_by_size(src_text, re_seg, max_bytes, chunk):
    """W1119 体积阈值规划：每批迁出 chunk 个 W 段（最后一批可不足），循环直到正本 <= max_bytes。
    段为降序（最新在前）⇒ 迁出块恒为尾部（最老）连续段 ⇒ 与 move() 的 A1/A4 断言兼容。"""
    hits = [(_wnum(m), m.start()) for m in re_seg.finditer(src_text)]
    assert hits, "正本未找到任何段（结构异常）"
    ws = [w for w, _ in hits]
    assert ws == sorted(ws, reverse=True), "正本段序非严格降序（先修复再归档）"
    assert len(set(ws)) == len(ws), "正本出现重复段号（先修复再归档）"
    n = len(hits)
    if len(src_text.encode('utf-8')) <= max_bytes:
        return None, []
    guard = _rule_seg_index(hits, src_text)   # 编号规则段不可迁出
    # W1308 根修：迁出量改由「体积刚好达标」决定。
    # 病根（实测）：原实现以 chunk（50）为**固定步长**迁出 ⇒ 迁出量由 chunk 决定而非由
    # 体积决定 ⇒ 在「正本段数 < chunk + 保留底线」时被迫迁到击穿铁律 22 底线
    # （实测 file-index 正本 50 段·体积 262964 B·仅超窗 820 B ⇒ 原实现迁出 44 段
    #  ⇒ 正本仅剩 6 段 ⇒ move() 的 `kept_segs >= 20` 断言 FAIL ⇒ 收官链 archive 步死锁）。
    # 上界**收紧**（判据只加严不放宽）：迁出块不得含编号规则段（原上界 limit-1 会把
    # 编号规则段一并迁走 ⇒ 版本面推进器 fail-closed「未找到锚点」⇒ 整条收官链停摆）。
    if guard is not None:
        max_k = n - guard - 1
        if max_k < 1:
            raise AssertionError(
                "体积超窗但编号规则段位于最老段（不可迁出）⇒ 无法靠归档腾窗达标——"
                "应压缩段行密度（batch_spec.fi_group_rows 立式）而非归档搬段")
    else:
        max_k = n - 1                          # 至少留 1 段
    # 二分：正本体积随 k 增大单调不增 ⇒ 求**最小达标** k（迁出更少 ⇒ 底线风险更低）
    lo, hi, best = 1, max_k, None
    while lo <= hi:
        mid = (lo + hi) // 2
        if len(src_text[:hits[n - mid][1]].encode('utf-8')) <= max_bytes:
            best = mid
            hi = mid - 1
        else:
            lo = mid + 1
    if best is None:
        best = max_k       # 迁到上限仍超窗 ⇒ 由 move() 的 20 段底线断言 fail-closed
    k = best
    cut = hits[n - k][1]
    moved_ws = [w for w, _ in hits[n - k:]]
    return cut, moved_ws


def plan_to_boundary(src_text, re_seg, boundary):
    """迁出所有 W 号 <= boundary 的段（两面按同一 W 号边界对齐用·W1119）。"""
    hits = [(_wnum(m), m.start()) for m in re_seg.finditer(src_text)]
    assert hits, "正本未找到任何段（结构异常）"
    ws = [w for w, _ in hits]
    assert ws == sorted(ws, reverse=True), "正本段序非严格降序（先修复再归档）"
    guard = _rule_seg_index(hits, src_text)   # 编号规则段不可迁出
    idx = [i for i, w in enumerate(ws) if w <= boundary]
    if not idx:
        return None, []
    k0 = idx[0]
    if guard is not None and k0 <= guard:
        raise AssertionError(
            "边界迁出块会含编号规则段（guard 下标 %d ≤ 迁出起点 %d）⇒ 不可迁——"
            "应压缩段行密度而非归档搬段" % (guard, k0))
    cut = hits[k0][1]
    moved_ws = [w for w, _ in hits[k0:]]
    return cut, moved_ws


def plan_align_below(src_text, re_seg, min_w):
    """对齐迁出规划（W1308）：迁出所有 W 号 **< min_w** 的段。

    用途：一面体积超窗而另一面未超窗时，未超窗面须迁到同一下界 ⇒ 两面正本最小 W 号
    一致（rebuild_section.boundary_check 是硬断言·不对齐即返红）。
    与 plan_to_boundary 的区别：后者迁出 W <= boundary；本函数迁出 W < min_w
    （min_w 本身留在正本 ⇒ 迁出后正本下界 = min_w）。
    """
    hits = [(_wnum(m), m.start()) for m in re_seg.finditer(src_text)]
    assert hits, "正本未找到任何段（结构异常）"
    ws = [w for w, _ in hits]
    assert ws == sorted(ws, reverse=True), "正本段序非严格降序（先修复再归档）"
    guard = _rule_seg_index(hits, src_text)   # 编号规则段不可迁出
    idx = [i for i, w in enumerate(ws) if w < min_w]
    if not idx:
        return None, []
    k0 = idx[0]
    if guard is not None and k0 <= guard:
        raise AssertionError(
            "对齐迁出块会含编号规则段（guard 下标 %d ≤ 迁出起点 %d）⇒ 不可迁——"
            "应压缩段行密度而非归档搬段" % (guard, k0))
    cut = hits[k0][1]
    moved_ws = [w for w, _ in hits[k0:]]
    return cut, moved_ws


def _face_ws(target):
    """某面正本的段号清单（新→旧）——纯读取。"""
    cfg = TARGETS[target]
    s, _nl = bc.load(cfg["src"])
    return [_wnum(m) for m in cfg["re_seg"].finditer(s)]


def _min_after(ws, moved):
    """迁出 moved 后正本的最小 W 号（moved 为空 ⇒ 原最小 W 号）。"""
    rem = [w for w in ws if w not in set(moved)]
    return min(rem) if rem else None


def _split_for_move(src_text, cut):
    """按「末尾文件级块」与「治理声明行」两种形态拆分迁出/留存文本。

    返回 (moved_text, kept_text, tail_start)：
    - 有末尾文件级块（CHANGELOG 形态）⇒ 迁出块止于末尾块起点，末尾块留在正本；
    - 无末尾块（file-index 形态）⇒ 治理声明行（维护契约行）抽出并留存正本末尾。
    """
    tail = _tail_block_start(src_text)
    moved, kept = split_tail_block(src_text, cut, tail)
    if tail is not None and tail > cut:
        return moved, kept, tail
    body, decls = _split_decl_blocks(moved)
    if decls:
        moved = body
        kept = kept + decls
    return moved, kept, tail


def _a3_ok(new_src, src_text, cut, tail):
    """A3 断言辅助：留存前缀逐字节不变 + 末尾文件级块逐字节留在正本。"""
    if not new_src.startswith(src_text[:cut]):
        return False
    if tail is not None and tail > cut:
        # W1192 根修：原写法 `not new_src.endswith(src_text[tail:])` 与本函数文档及
        #   split_tail_block 的行为**相互矛盾**——split_tail_block 在 tail > cut 时把末尾块
        #   留在正本末尾（kept = src[:cut] + src[tail:]）⇒ new_src 必以末尾块结尾；
        #   原断言却要求「不以末尾块结尾」⇒ 该分支恒假 ⇒ CHANGELOG 体积模式迁移必红
        #   （W1192 实测：CHANGELOG 264907 B 超 262144 B 上限 → 触发体积迁移 → A3 AssertionError）。
        #   判据意图「末尾块逐字节留在正本」应判为「以末尾块结尾」；留存前缀不变由上一行保证。
        return new_src.endswith(src_text[tail:])
    return True


def _plan_for_face(s, re_seg, keep, max_bytes, chunk, boundary, align_min):
    """单面迁出计划的**唯一分流点**（优先级：对齐 > 边界 > 体积 > 段数）。

    W1308：move() 原内联四路 if/elif ⇒ 分支数 17 > 16（ruff 结构档）⇒ 抽出本函数
    （分流单一事实源·move() 只负责落盘与守恒断言）。
    """
    if align_min is not None:
        return plan_align_below(s, re_seg, align_min)
    if boundary is not None:
        return plan_to_boundary(s, re_seg, boundary)
    if max_bytes is not None:
        return plan_by_size(s, re_seg, max_bytes, chunk)
    return plan(s, re_seg, keep)


def _write_all_or_rollback(writes):
    """跨面事务写（W1340·P1-1）：全部内容先在内存算定，再逐件写；任一写失败回滚已写件。

    病根：原实现每面 move() 内直接落盘 ⇒ 第一面写成功后第二面断言失败会留下**半迁移**
    （正本少了段、归档没多段，或两面下界不一致）⇒ 下次运行断言必红且无法自愈。
    """
    originals = {}
    done = []
    try:
        for path_, content in writes:
            if path_ not in originals:
                with open(path_, "rb") as f:
                    originals[path_] = f.read()
            with open(path_, "w", encoding="utf-8", newline="") as f:
                f.write(content)
            done.append(path_)
    except Exception:
        for path_ in done:
            try:
                with open(path_, "wb") as f:
                    f.write(originals[path_])
            except OSError:
                pass
        raise


def _append_archive_log(records, batch_tag):
    """迁移台账追加（W1340·P1-2）：每条记录一行 JSON（只追加·LF）。"""
    if not records:
        return
    log_path = os.path.join(ROOT, ARCHIVE_LOG)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    ts = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    with open(log_path, "a", encoding="utf-8", newline="\n") as f:
        for rec in records:
            line = {"ts": ts, "event": "migrate", "batch": batch_tag}
            line.update(rec)
            f.write(json.dumps(line, ensure_ascii=False) + "\n")


def move(target, keep, apply, batch_tag, max_bytes=None, chunk=50, boundary=None, align_min=None,
         defer=False):
    """执行单面迁移。返回 {moved_ws, writes, record}；defer=True 时不落盘（由调用方统一写）。"""
    cfg = TARGETS[target]
    src_rel, arc_rel, re_seg, arc_mode = cfg["src"], cfg["arc"], cfg["re_seg"], cfg["arc_mode"]
    src_path = os.path.join(ROOT, src_rel)
    arc_path = os.path.join(ROOT, arc_rel)

    s, nl = bc.load(src_rel)
    a, anl = bc.load(arc_rel)

    cut, moved_ws = _plan_for_face(s, re_seg, keep, max_bytes, chunk, boundary, align_min)
    if cut is None:
        # W1014：未超窗 → 无段可迁（正常状态·非失败）——原实现断言失败致级联回窗误报 FAIL
        n_seg = len(re_seg.findall(s))
        if keep is None:
            print("[SKIP] %s 段数 %d·体积未超阈值·无段可迁" % (src_rel, n_seg))
        else:
            print("[SKIP] %s 段数 %d ≤ keep %d——未超窗·无段可迁" % (src_rel, n_seg, keep))
        return {"moved_ws": [], "writes": [], "record": None}
    # W1130 根修：迁出块不得吞掉正本末尾文件级块（含编号规则串）=> 否则版本面推进器 fail-closed
    moved_text, kept_text, _tail = _split_for_move(s, cut)

    # W1142 立式（铁律 22 保留条款的机器化）：体积模式迁出后正本剩余段数不得 < 20——
    # W1139 实测 29 段曾被 chunk=50 全迁剩 1 段（合法工具调用 → 违规终态）；不足属
    # 「需压缩而非归档」场景，fail-closed 指引改用段行压缩（batch_spec.fi_group_rows 立式）。
    if max_bytes is not None or boundary is not None or align_min is not None:
        kept_segs = len(re_seg.findall(kept_text))
        assert kept_segs >= 20, (
            "迁移后正本仅剩 %d 段 < 保留底线 20（AGENTS 铁律 22）——此体量矛盾应压缩段行密度"
            "（batch_spec.fi_group_rows 立式）而非归档搬段" % kept_segs)

    # ---- A4 迁出块内部降序（块内段号）----
    moved_in_block = [_wnum(m) for m in re_seg.finditer(moved_text)]
    assert moved_in_block == sorted(moved_in_block, reverse=True), "迁出块内部段序非降序（尾部含异常内容）"
    assert len(moved_in_block) == len(moved_ws), "迁出块计数与段表不一致"

    # ---- A5 归档序（仅 top 模式）----
    arc_ws = [_wnum(m) for m in re_seg.finditer(a)]
    moved_arc = _to_nl(moved_text, anl)  # 迁出块按归档容器行尾转译（防混行尾·W960 实证）
    if arc_mode == "top":
        assert arc_ws and max(arc_ws) < min(moved_ws), \
            "归档既有最大段号 %s ≥ 迁出最小段号 %s——top 插入会破坏 newest-at-top 语义" % (
                max(arc_ws), min(moved_ws))
        first_seg = re_seg.search(a)
        assert first_seg, "归档文件无段锚（结构异常）"
        new_arc = a[:first_seg.start()] + moved_arc.rstrip() + anl + anl + a[first_seg.start():]
        insert_desc = "插在归档顶段 W%d 之前" % arc_ws[0]
    else:
        # append 模式：追加在末尾 + 头部「> 归档时间：」链追加注记
        new_arc = a
        if not new_arc.endswith(anl):
            new_arc += anl
        new_arc += moved_arc.rstrip() + anl
        mnote = re.search(r"(?m)^> 归档时间：.*$", new_arc)
        note = " + %s（%s 迁入 W%d-W%d）" % (datetime.date.today().isoformat(), batch_tag,
                                           min(moved_ws), max(moved_ws))
        if mnote:
            note_at = mnote.end()
            if new_arc[note_at - 1] == "\r":  # CRLF 文件上 $ 匹配含 \r（W960 实证：注记插进 \r 后成孤立 CR）
                note_at -= 1
            new_arc = new_arc[:note_at] + note + new_arc[note_at:]
        else:
            sys.exit("FAIL  归档文件缺「> 归档时间：」头注行（append 记账锚缺失·人工补后再跑）")
        insert_desc = "追加在归档末尾（其后 W%d-W%d）" % (min(moved_ws), max(moved_ws))

    new_src = kept_text
    # 留存前缀若以空段尾结束（原迁出段前有空行）保持原样——A3 要求逐字节不变，不做清理

    # ---- A1 段数守恒 ----
    src_before = len([_ for _ in re_seg.finditer(s)])
    src_after = len([_ for _ in re_seg.finditer(new_src)])
    arc_after_n = len([_ for _ in re_seg.finditer(new_arc)])
    assert src_before == src_after + len(moved_ws), "A1 段数守恒失败（正本）：%d != %d + %d" % (
        src_before, src_after, len(moved_ws))
    assert arc_after_n == len(arc_ws) + len(moved_ws), "A1 段数守恒失败（归档）"

    # ---- A2 内容守恒（行尾归一后逐字比对——迁出块已按归档行尾转译）----
    assert moved_arc.rstrip() and (moved_arc.rstrip() in new_arc), "A2 内容守恒失败（迁出块未出现在归档）"

    # ---- A3 锚点不动 ----
    assert _a3_ok(new_src, s, cut, _tail), "A3 留存前缀被改动或末尾文件级块未留在正本"
    rule = re.search(r"（W001-W\d+）", s)
    if rule:
        # W1119 批量迁移订正：原断言比**全文**计数 ⇒ 迁出块带走「（W001-W####）」字样时计数必减 ⇒ 批量模式恒假红。
        # 意图是「编号规则行未被改动」⇒ 留存前缀逐字节不变（A3 主断言）已覆盖 ⇒ 收紧为「留存前缀内计数相等」·判据强度不降。
        _rule_base = s[:cut].count(rule.group(0))
        if _tail is not None and _tail > cut:
            _rule_base += s[_tail:].count(rule.group(0))
        assert new_src.count(rule.group(0)) == _rule_base, "A3 编号规则行被改动"
    top_before = re_seg.search(s)
    top_after = re_seg.search(new_src)
    assert top_before and top_after and top_before.group(0) == top_after.group(0), "A3 顶段标题行被改动"
    # 留存段降序（A4 正本侧）
    kept_ws = [_wnum(m) for m in re_seg.finditer(new_src)]
    assert kept_ws == sorted(kept_ws, reverse=True), "A4 留存段序非降序"

    print("  %s：迁出 %d 段（W%d-W%d）·留存 %d 段·%s"
          % (src_rel, len(moved_ws), min(moved_ws), max(moved_ws), src_after, insert_desc))

    writes = [(src_path, new_src), (arc_path, new_arc)] if (apply and defer) else []
    if apply and not defer:
        _write_all_or_rollback([(src_path, new_src), (arc_path, new_arc)])
        print("  已落盘 %s + %s" % (src_rel, arc_rel))
    record = {
        "target": target,
        "src": src_rel.replace(os.sep, "/"),
        "archive": arc_rel.replace(os.sep, "/"),
        "moved_count": len(moved_ws),
        "w_min": min(moved_ws),
        "w_max": max(moved_ws),
        "src_segments_before": src_before,
        "src_segments_after": src_after,
        "src_bytes_before": len(s.encode("utf-8")),
        "src_bytes_after": len(new_src.encode("utf-8")),
    }
    return {"moved_ws": moved_ws, "writes": writes, "record": record}


def main() -> int:
    ap = argparse.ArgumentParser(description="治理文档版段滚动归档（W960·W1340 起默认体积档）")
    ap.add_argument("--target", choices=["changelog", "file-index", "both"], default="both")
    ap.add_argument("--keep", type=int, default=None,
                    help="段数档：正本保留段数（仅显式指定时生效；不给则默认体积档）")
    ap.add_argument("--max-bytes", type=int, default=None,
                    help="正本体积硬上限（字节）·默认 %d（utils/gate_common.MAX_DOC_BYTES）" % gc.MAX_DOC_BYTES)
    ap.add_argument("--headroom", type=int, default=8192,
                    help="体积水位（字节）：实际迁移目标 = max-bytes - headroom（默认 8192）")
    ap.add_argument("--chunk", type=int, default=50,
                    help="体积模式段数评估粒度（兼容参数·W1308 起迁出量由体积二分决定）")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--batch-tag", default="W960", help="归档注记的批次号")
    args = ap.parse_args()
    if not (args.apply or args.dry_run):
        ap.error("必须指定 --dry-run 或 --apply")
    # W1340（P0-1）：默认走**体积档**——原默认 --keep 109 是段数档，与真实约束（字节窗）错位。
    if args.keep is None and args.max_bytes is None:
        args.max_bytes = gc.MAX_DOC_BYTES
    budget = None
    if args.max_bytes is not None:
        if args.headroom < 0 or args.headroom >= args.max_bytes:
            ap.error("--headroom 必须 >=0 且 < --max-bytes")
        budget = args.max_bytes - args.headroom  # W1340（P0-2）：留水位，不迁到贴线

    faces = [t for t in ("changelog", "file-index") if args.target in (t, "both")]
    results = {}
    if budget is not None:
        ws_all = {t: _face_ws(t) for t in faces}
        vol_plans = {}
        for t in faces:
            s, _nl = bc.load(TARGETS[t]["src"])
            vol_plans[t] = plan_by_size(s, TARGETS[t]["re_seg"], budget, args.chunk)
        after = {}
        for t in faces:
            mv = vol_plans[t][1]
            after[t] = _min_after(ws_all[t], mv) if mv else min(ws_all[t])
        target = max(after.values())
        for t in faces:
            results[t] = move(t, None, args.apply, args.batch_tag, align_min=target, defer=True)
        final = {t: _min_after(ws_all[t], results[t]["moved_ws"]) for t in faces}
        assert len(set(final.values())) == 1, (
            "两面未迁到同一 W 号下界：%s" % " ".join("%s=W%s" % (t, final[t]) for t in faces))
        for t in faces:
            s, _nl = bc.load(TARGETS[t]["src"])
            cut, _mv = plan_align_below(s, TARGETS[t]["re_seg"], target)
            size = len(s[:cut].encode('utf-8')) if cut is not None else len(s.encode('utf-8'))
            assert size <= budget, (
                "%s 按 target=W%d 迁出后体积 %d 仍超水位 %d（硬上限 %d - 水位 %d）——"
                "须提高对齐下界或压缩登记面"
                % (t, target, size, budget, args.max_bytes, args.headroom))
        print("[ALIGN] 两面同下界 W%d（正本均保留 W 号 >= %d）" % (final[faces[0]], final[faces[0]]))
    else:
        for t in faces:
            results[t] = move(t, args.keep, args.apply, args.batch_tag, defer=True)

    moved_all = {t: results[t]["moved_ws"] for t in faces}
    if not args.apply:
        print("[DRY-RUN] 未落盘。加 --apply 写回。")
    else:
        # W1340（P1-1）：跨面事务写——全部断言通过后才落盘，任一写失败回滚已写件。
        writes = [w for t in faces for w in results[t]["writes"]]
        _write_all_or_rollback(writes)
        # W1340（P1-2）：迁移台账（每面一条·只追加）。
        _append_archive_log([results[t]["record"] for t in faces if results[t]["record"]], args.batch_tag)
        print("[APPLY] 归档完成：%s" % ", ".join("%s→%d 段" % (t, len(w)) for t, w in moved_all.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
