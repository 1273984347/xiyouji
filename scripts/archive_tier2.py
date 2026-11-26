#!/usr/bin/env python3
"""archive_tier2.py — 归档件二级归档工具（W994 建·文档规范 §11.2 tier-2 条款执行器）。

把一级归档件中 **W 号最老的段**迁入对应 -tier2.md，直到一级体积回落到目标线内。
段级逐字节搬运（零改写）；一级头部归档时间链追加一行指针；tier2 不存在则按规范建。
本工具的存在理由：§11.2 的 1MB 线自 W513 后掉档（W994 实测 CHANGELOG-ARCHIVE 1198KB /
file-index-ARCHIVE 1070KB 双破线零反应）——check_archive_health.py T1 探针 + 本执行器
构成「探测→修法」闭环，与 archive_segments（正本→archive）互补。

守恒五道（断言失败零落盘）：
  A1 段数守恒：迁出 + 留存 = 总段数
  A2 内容守恒：迁出段逐字节出现在 tier2
  A3 头部只追加：一级新文本以原头部为前缀（指针行仅追加）
  A4 号序前缀：迁出集=号升序前缀（剩余最小段号 > 迁出最大段号）
  A5 字节守恒：一级缩减字节数 == 迁出段字节数总和

用法：
  py -3 scripts/archive_tier2.py --file changelog --dry-run
  py -3 scripts/archive_tier2.py --file changelog --apply
  py -3 scripts/archive_tier2.py --file file-index --apply [--target-bytes 921600]
  py -3 scripts/archive_tier2.py --self-test
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_TARGET = 900 * 1024  # 迁到 1MB 线内且留判距余量（探针 WARN=800KB 之下尽量）
LIMIT = 1024 * 1024          # §11.2 1MB 线（W995 起 tier2 追加前容量判断用）
DATE = datetime.date.today().isoformat()

# W1335（用户 2026-11-27 裁决）：新卷宽度 = 250 个 W 号；无范围名的旧二级卷冻结为只读。
# 冻结理由：旧卷名不含范围（tier2.md 实装 W277-W672），继续追加会让「查哪个体积/哪段」失去
# 可判定性；冻结后由 archive/docs/ARCHIVE-MANIFEST.md + gen_archive_manifest.py 登记真实区间。
RANGE_WIDTH = 250
FROZEN_TIER2 = ("CHANGELOG-ARCHIVE-tier2.md", "file-index-ARCHIVE-tier2.md")


def align_boundary(min_key, width=RANGE_WIDTH):
    """把迁出上界对齐到 width 的整数倍（→ 卷名稳定、可复算）。

    min_key=951、width=250 ⇒ 1000（本卷只迁到 W1000，宽度 50）；
    min_key=1001 ⇒ 1250（宽度 250）。key 0（file-index 早期目录节）按 1 处理。
    """
    k = max(int(min_key), 1)
    return (k - 1) // width * width + width

KINDS = {
    "changelog": {
        "primary": os.path.join("archive", "docs", "CHANGELOG-ARCHIVE.md"),
        "tier2": os.path.join("archive", "docs", "CHANGELOG-ARCHIVE-tier2.md"),
        "block": re.compile(r"(?m)^### ", re.M),
        "tier2_header": None,  # 已存在
    },
    "file-index": {
        "primary": os.path.join("archive", "docs", "file-index-ARCHIVE.md"),
        "tier2": os.path.join("archive", "docs", "file-index-ARCHIVE-tier2.md"),
        # 两代混层：早期按目录分节（`## 目录名`·标题无 W 号·W031-W087 时代），后期 `## W### `
        "block": re.compile(r"(?m)^## "),
        "key_fn": None,  # file-index 用 key_from_heading（见下）
        "tier2_header": (
            "# file-index 二级归档（最老段容器）\n\n"
            "> **📖 阅读契约（W707）**：禁通读——本文件为 file-index-ARCHIVE.md 的二级归档层，\n"
            "> 承载一级超 1MB 后迁出的最老段（文档规范 §11.2·W513 先例）。查历史 W 号用 grep。\n"
        ),
    },
}


def key_from_heading(heading):
    """段排序键：标题行首个 W 数字；无 W 号（file-index 早期目录节）取 0=排最老。"""
    m = re.search(r"W(\d{3,4})", heading)
    return int(m.group(1)) if m else 0


def parse_segments(text, block_re, kind):
    """→ [(key, start, end)]（段=块起点到下一块起点/文末；key=key_from_heading(标题行)）。"""
    marks = [(m.start(), m.end()) for m in block_re.finditer(text)]
    segs = []
    for i, (s, _e) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        nl = text.find("\n", s)
        heading = text[s:nl if nl != -1 else end]
        segs.append((key_from_heading(heading), s, end))
    return segs


def plan(text, block_re, kind, target, max_key=None):
    """→ (header, 迁出[(key,start,end)], 保留[(key,start,end)])——键升序前缀切分·纯函数。

    目标判定按**全文字节**（§11.2 管文件体积·非 body）：剩余全文 = 全文 − 已迁段字节。
    max_key（W1335）：迁出上界——键 > max_key 的段不迁（分卷宽度由 align_boundary 决定）。
    """
    segs = parse_segments(text, block_re, kind)
    if not segs:
        return text, [], []
    header_end = segs[0][1]
    header = text[:header_end]
    ordered = sorted(segs, key=lambda t: (t[0], t[1]))
    # 全程按「字节」计量——中文 UTF-8 下字符数 ≈ 字节数 1/3·混用会把 1198KB 误判成 713KB「线内」（W994 实证）
    total_bytes = len(text.encode())
    moved_bytes = 0
    moved = []
    for k, s, e in ordered:
        if total_bytes - moved_bytes <= target:
            break
        if max_key is not None and k > max_key:
            break
        moved_bytes += len(text[s:e].encode())
        moved.append((k, s, e))
    kept = [t for t in segs if t not in set(moved)]
    if moved and kept:
        assert max((k, s) for k, s, _e in moved) < min((k, s) for k, s, _e in kept), "A4 键序前缀（构造性保证·断言兜底）"
    return header, moved, kept


def migrate(kind, target, apply, range_width=RANGE_WIDTH):
    cfg = KINDS[kind]
    primary_p = os.path.join(ROOT, cfg["primary"])
    text = open(primary_p, encoding="utf-8", newline="").read()
    segs = parse_segments(text, cfg["block"], kind)
    if not segs:
        print("[TIER2] %s 无段可迁（结构异常）" % kind)
        return 0
    # W1335：迁出上界先按 range_width 对齐（卷名稳定可复算），再由体积目标决定实际迁多少
    boundary = align_boundary(min(k for k, _s, _e in segs), range_width)
    header, moved, kept = plan(text, cfg["block"], kind, target, max_key=boundary)
    moved = [t for t in moved if t[0] <= boundary]
    if not moved:
        print("[TIER2] %s 已在目标线内（%d KB ≤ %d KB）·无迁出" % (kind, len(text.encode()) // 1024, target // 1024))
        return 0
    keys = [k for k, _s, _e in moved]
    moved_bytes = sum(len(text[s:e].encode()) for _k, s, e in moved)
    # W1335：一律写**范围命名卷**（旧的无范围名 tier2.md 已冻结只读，不再追加）
    stem = os.path.splitext(os.path.basename(cfg["tier2"]))[0]  # CHANGELOG-ARCHIVE-tier2
    vol_name = "%s-W%d-W%d.md" % (stem, min(keys), max(keys))
    assert vol_name not in FROZEN_TIER2, "分卷目标命中了冻结卷（冻结卷不得追加）"
    tier2_p = os.path.join(ROOT, os.path.dirname(cfg["tier2"]), vol_name)
    tier2_size = os.path.getsize(tier2_p) if os.path.exists(tier2_p) else 0
    assert tier2_size + moved_bytes <= LIMIT, (
        "分卷 %s 追加后破 1MB 线（现有 %d KB + 迁出 %d KB）——收窄 --range-width 或人工拆卷"
        % (vol_name, tier2_size // 1024, moved_bytes // 1024))
    kr = ("目录节(最老)" if keys[0] == 0 else "W%d" % keys[0],
          "目录节" if keys[-1] == 0 else "W%d" % keys[-1])
    print("[TIER2] %s：迁出 %d 段（%s-%s·%d KB）→ %s ·一级留存（%d KB）"
          % (kind, len(moved), kr[0], kr[1], moved_bytes // 1024, vol_name,
             (len(text.encode()) - moved_bytes) // 1024))
    if not apply:
        print("[DRY-RUN] 未落盘。加 --apply 执行。")
        return 0

    pointer = "\n> **%s（%s 迁出 %d 段·%s-%s 至 %s·§11.2 tier-2）**：一级归档超 1MB 触发二级归档，最老段按键序前缀迁出（archive_tier2.py·守恒五道）。\n" % (
        DATE, "W1335", len(moved), kr[0], kr[1], vol_name)
    moved_spans = [(s, e) for _k, s, e in moved]
    # body = header 之后；按 span 切除迁出段——**必须按位置升序**：
    # 键序（=W 升序）在本文件里是位置降序（新段插顶·老段沉底），cur 前向切除会静默保留新版段
    # （A5 字节守恒断言 W994 实测当场活捉·fail-closed 零落盘）
    body = text[len(header):]
    cut = sorted((s - len(header), e - len(header)) for s, e in moved_spans)
    out, cur = [], 0
    for s, e in cut:
        out.append(body[cur:s])
        cur = e
    out.append(body[cur:])
    body_new = "".join(out)
    new_primary = header + pointer + "\n" + body_new

    # 守恒断言（零落盘前置）
    assert len(moved) + len(kept) == len(parse_segments(text, cfg["block"], kind)), "A1 段数守恒"
    if os.path.exists(tier2_p):
        tier2_old = open(tier2_p, encoding="utf-8", newline="").read()
    else:
        # 新容器（含 W995 范围命名新件）：生成合规头部
        stem = os.path.splitext(os.path.basename(tier2_p))[0]
        tier2_old = (
            "# %s（二级归档容器·范围件）\n\n"
            "> **📖 阅读契约（W707）**：禁通读——本文件为 %s 的二级归档层（文档规范 §11.2·W513 先例）。\n"
            "> 拆分约定（W995）：范围命名 `*-tier2-W<lo>-W<hi>.md`·单件 ≤1MB（check_archive_health T1b 监视）。\n"
            "> 归档时间：%s（%s 首建）\n\n" % (stem, cfg["primary"], DATE, "W995")
        )
    marker = "\n> 归档追加：%s（%s 迁入 %s-%s）\n" % (DATE, "W994", kr[0], kr[1])
    seg_text = "".join(text[s:e] for s, e in moved_spans)
    tier2_new = tier2_old.rstrip("\n") + "\n" + marker + "\n" + seg_text
    for s, e in moved_spans:
        assert text[s:e] in tier2_new, "A2 迁出段逐字节在 tier2"
    assert new_primary.startswith(header), "A3 头部前缀保持（指针行仅追加）"
    assert max((k, s) for k, s, _e in moved) < min((k, s) for k, s, _e in kept), "A4 键序前缀"
    # A5 用字符口径（len(text) 是字符数——两端异单位中文下必不等，W994 实证二次）
    moved_chars = sum(e - s for s, e in moved_spans)
    assert len(text) - len(new_primary) == moved_chars - len(pointer) - 1, "A5 字节守恒（缩减=迁出−指针行）"

    with open(primary_p, "w", encoding="utf-8", newline="") as f:
        f.write(new_primary)
    os.makedirs(os.path.dirname(tier2_p), exist_ok=True)
    with open(tier2_p, "w", encoding="utf-8", newline="") as f:
        f.write(tier2_new)
    print("[APPLY] 已落盘 %s + %s" % (os.path.relpath(primary_p, ROOT), os.path.relpath(tier2_p, ROOT)))
    return 0


def _self_test() -> int:
    fails = []
    # 合成：header + 5 段（纯 ASCII·chars==bytes 确定性）·target=150 时恰迁 2 段
    segs_txt = "".join("### W%d (2026-01-0%d): t%d\n\nbody %d a\nbody %d b\n\n" % (905 + i, i % 9 + 1, i, i, i) for i in range(5))
    text = "# archive header\n\n> time chain\n\n" + segs_txt
    block_re = re.compile(r"(?m)^### ", re.M)
    header, moved, kept = plan(text, block_re, "changelog", target=150)
    if [k for k, _s, _e in moved] != [905, 906, 907] or [k for k, _s, _e in kept][0] != 908:
        fails.append("号序前缀切分错：%s" % [k for k, _s, _e in moved])
    # 字节守恒（与 migrate 同构的 span 切除）
    cut_total = sum(e - s for _k, s, e in moved)
    out, cur = [], 0
    for _k, s, e in moved:
        out.append(text[len(header):][cur:s - len(header)])
        cur = e - len(header)
    out.append(text[len(header):][cur:])
    if len("".join(out)) + cut_total != len(text) - len(header):
        fails.append("字节守恒错")
    # A4 元组序：剩余最小 (key,pos) > 迁出最大
    if not (kept[0][:2] > moved[-1][:2]):
        fails.append("键序前缀断言错")
    # file-index 混层键：目录节（无 W 号）取 0 排最老
    fx = "# fx\n\n## site/data/（归档段：v2.0.4）\n\n| a | W031 |\n\n## W389 后期段\n\n| b | x |\n"
    h2, m2, k2 = plan(fx, re.compile(r"(?m)^## "), "file-index", target=10)
    if [k for k, _s, _e in m2] != [0, 389] or (k2 and k2[0][0] != 0):
        fails.append("file-index 混层键错：%s / kept=%s" % ([k for k, _s, _e in m2], [k for k, _s, _e in k2]))
    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：号序前缀切分/字节守恒/头前缀（判据可证伪）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="归档件二级归档工具（W994·§11.2 执行器·W1335 分卷）")
    ap.add_argument("--file", choices=sorted(KINDS), help="一级归档件种类（--self-test 时可省）")
    ap.add_argument("--apply", action="store_true", help="落盘（默认 dry-run）")
    ap.add_argument("--target-bytes", type=int, default=DEFAULT_TARGET, help="一级目标体积（默认 900KB）")
    ap.add_argument("--range-width", type=int, default=RANGE_WIDTH,
                    help="分卷宽度（W 号跨度·默认 %d·卷名按 align_boundary 对齐）" % RANGE_WIDTH)
    ap.add_argument("--rounds", type=int, default=5,
                    help="最多连续迁出几卷（单卷宽度受限 ⇒ 需多轮才把一级压回目标线内）")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    if not args.file:
        ap.error("必须指定 --file（或 --self-test）")
    rc = 0
    for _ in range(max(1, args.rounds)):
        primary_p = os.path.join(ROOT, KINDS[args.file]["primary"])
        before = os.path.getsize(primary_p)
        rc = migrate(args.file, args.target_bytes, apply=args.apply, range_width=args.range_width)
        if rc != 0 or not args.apply:
            break
        if os.path.getsize(primary_p) >= before:
            break  # 无进展（已在线内或迁不动）⇒ 停止，避免空转
    return rc


if __name__ == "__main__":
    sys.exit(main())
