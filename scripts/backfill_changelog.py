#!/usr/bin/env python3
"""CHANGELOG / file-index 递延段补写器（W842）。

**要解决的问题**：`batch_cascade.py` 的 `assert batch == W{顶段+1}` 保证「只能顺序立段」——
这条断言本身是对的（段序不能乱），但它有个副作用：**只要有任何一个号没立段（被让出、被占用、
或那批没走级联），整条链就停在那里**。W828 让给一个始终未施工的批次之后，W830–W841 十二批
全部卡住：内容批早已落库、spec 早已入库、对账表早已翻「已收官」，只有段立不上。

**做什么**：把那批「已收官但未立段」的 spec 按号序补回正确位置。段标题按 W 号降序排列，
新段插在「第一个号小于自己的段」之前——不是插在顶部（插顶部会让段序变成非单调）。

**与 batch_cascade 的分工（关键，别混）**：
  - `batch_cascade.py` = 正常批的十面级联（CHANGELOG + 版本行 + 交接 + AGENTS + 页脚 + CITATION …）
  - 本工具 = 只补**两个面**：CHANGELOG 段 + file-index 段
  - **不碰「当前态」文档**：README / STRUCTURE / 项目说明的版本行、交接里程碑、AGENTS、
    CITATION、三简单页脚，表达的都是「现在是什么」，该指向**最高号**；被一批历史段拉回去是错的。
    这是本工具与 batch_cascade 最根本的差别，也是补段不能直接复用级联的原因。

**不改历史段**：只插入，不清洗、不重排、不改写既有段的任何字符。

用法：
  py -3 scripts/backfill_changelog.py --dry-run    # 打印将补哪些段、插在哪
  py -3 scripts/backfill_changelog.py --apply      # 落盘
退出码：0 成功；1 断言失败（不落盘）。
"""

import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
RE_SEG = re.compile(r"^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（[^）]*）：)", re.M)
RE_FI_SEG = re.compile(r"^## (W\d+) ", re.M)
RE_RULE = re.compile(r"（W001-W(\d+)）")

# W956/E-27：归档面与现役面必须合看——CHANGELOG 自 W921 瘦身起把百段级老段移入归档文件，
# 本工具原先只读现役面 ⇒ 已归档段被误判「未立段」（实测待补 74 段假清单·W728-W802 全是
# 归档段假阳性）。立段判定自此两面合扫；**插入目标仍只有现役面**（归档文件禁写）。
ARCHIVE_CHANGELOG = os.path.join("archive", "docs", "CHANGELOG-ARCHIVE.md")

SPEC_KEYS = ("batch", "date", "title", "desc", "head_entry", "head_sentence",
             "changelog_body", "milestone_block", "agents_note", "file_index_rows")


def load(path):
    """读文件并统一为 \\n 内存形态；返回 (text, 原换行符)。"""
    with open(os.path.join(ROOT, path), "rb") as f:
        raw = f.read().decode("utf-8")
    nl = "\r\n" if b"\r\n" in raw.encode("utf-8") else "\n"
    return raw.replace("\r\n", "\n"), nl


def segments(text):
    """CHANGELOG 已立段：[(W 号, 段标题起点)]，按文中顺序（即 W 号降序）。"""
    return [(int(m.group(1) or m.group(2)), m.start()) for m in RE_SEG.finditer(text)]


def insert_before_smaller(text, w, block):
    """把 block 插到「第一个号小于 w 的段」之前。返回 (新文本, 锚点段号)。"""
    for sw, st in segments(text):
        if sw < w:
            return text[:st] + block + text[st:], sw
    raise AssertionError(
        "W%d 找不到更小的已立段可作锚点——本批号高于所有已立段，"
        "这种情况应走 batch_cascade 正常级联，不该用补段工具" % w)


def changelog_block(spec):
    """单段 CHANGELOG 块（与 batch_cascade._face_changelog 同形态）。"""
    title_body = re.sub(r"^W\d+\s+", "", spec["title"]).strip()
    return "### %s（%s）：%s" % (spec["batch"], spec["date"], title_body) + \
           spec["changelog_body"] + "\n"


def file_index_block(spec):
    """单段 file-index 块（与 batch_cascade._face_file_index 同形态）。"""
    tb = re.sub(r"^W\d+\s+", "", spec["title"].split(" — ")[0].split("（")[0]).strip()
    rows = ["## %s %s（%s）" % (spec["batch"], tb, spec["date"]),
            "", "| 文件 | W | 说明 |", "|---|---|---|"] + list(spec["file_index_rows"]) + ["", ""]
    return "\n".join(rows)


def insert_fi(text, w, block):
    """file-index 段按数值序插入（W676/W677 先例：认领号小于现役 max 时插数值位）。"""
    hits = [(int(m.group(1)[1:]), m.start()) for m in RE_FI_SEG.finditer(text)]
    for sw, st in hits:
        if sw < w:
            return text[:st] + block + "\n" + text[st:]
    raise AssertionError("file-index 找不到更小的段可作锚点（W%d）" % w)


def collect_pending():
    """扫 spec，筛出「未立段」的（现役+归档两面合看·已立段的不重复补）。"""
    cl, _ = load("CHANGELOG.md")
    established = {w for w, _ in segments(cl)}
    arc_p = os.path.join(ROOT, ARCHIVE_CHANGELOG)
    if os.path.exists(arc_p):
        arc, _ = load(ARCHIVE_CHANGELOG)
        established |= {w for w, _ in segments(arc)}
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "scripts", "output", "_w*_spec.json"))):
        spec = json.load(open(p, encoding="utf-8"))
        missing = [k for k in SPEC_KEYS if k not in spec]
        if missing:
            raise AssertionError("%s 缺字段 %s（补段前先补 spec）" % (os.path.basename(p), missing))
        w = int(spec["batch"][1:])
        if w in established:
            continue
        out.append((w, spec))
    out.sort(key=lambda t: t[0])
    return out, established


def refresh_current(apply):
    """把「当前态」六面统一推进到最高已立段。

    补段只补历史，不动版本行等「现在是什么」的面；但一旦补完，顶段号变了，
    这些面就必须跟着走，否则 C1（README 抬头 ≡ 顶段）当场红。
    这里直接复用 batch_cascade 的面函数——它们是纯函数，只吃 ctx，
    不碰「插段」逻辑，所以补段场景下可以安全调用。
    """
    import importlib.util
    cl, _ = load("CHANGELOG.md")
    segs = segments(cl)
    top_w = max(w for w, _ in segs)
    spec_path = os.path.join(ROOT, "scripts", "output", "_w%03d_spec.json" % top_w)
    if not os.path.exists(spec_path):
        raise AssertionError(
            "顶段 W%d 没有对应 spec（%s）——当前态同步需要该批的 desc/标题；"
            "若顶段是手工立的，请先补 spec" % (top_w, spec_path))
    spec = json.load(open(spec_path, encoding="utf-8"))
    print("[SYNC] 顶段 W%d · 用 %s 同步当前态六面" % (top_w, os.path.basename(spec_path)))

    sp = importlib.util.spec_from_file_location(
        "batch_cascade", os.path.join(ROOT, "scripts", "batch_cascade.py"))
    bc = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(bc)

    ctx = bc._Ctx(spec)
    ctx.new_w = top_w
    ctx.new_rule = "（W001-W%d）" % top_w
    ctx.cl_src = cl  # 交接文档面断言需要 CHANGELOG 原文
    for face in (bc._face_three_docs, bc._face_handover, bc._face_workflows,
                 bc._face_agents, bc._face_citation, bc._face_footers):
        before = len(ctx.pend)
        face(ctx)
        assert len(ctx.pend) > before, "%s 未产生落盘项" % face.__name__
        print("  OK  %s（+%d 面）" % (face.__name__, len(ctx.pend) - before))

    assert ctx.pend, "当前态同步未产生任何落盘项"
    if not apply:
        print("[DRY-RUN] 将改 %d 个文件：%s" % (len(ctx.pend), [p for p, _, _ in ctx.pend]))
        return 0
    bc._apply_pend(ctx.pend, "W%d" % top_w)
    print("[SYNC] 落盘完成：%d 面" % len(ctx.pend))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--refresh-current", action="store_true",
                    help="把 README/STRUCTURE/项目说明/交接/AGENTS/CITATION/页脚推进到最高已立段")
    ap.add_argument("--only", default="",
                    help="只补指定 W 号（逗号分隔·W956 新增）——其余「未立段」spec 属让号遗留"
                         "（工作已改号落库·如 W908/W910→W912·W939→W941）不立段，留档不动")
    args = ap.parse_args()
    if not (args.apply or args.dry_run):
        ap.error("必须指定 --dry-run 或 --apply")

    if args.refresh_current:
        return refresh_current(apply=args.apply)

    pending, established = collect_pending()
    if args.only:
        only = {int(x.strip().lstrip("Ww")) for x in args.only.split(",") if x.strip()}
        known = {w for w, _ in pending}
        unknown = sorted(only - known)
        assert not unknown, "--only 指定号 %s 不在待补清单（或 spec 缺失/已立段）" % unknown
        pending = [(w, s) for w, s in pending if w in only]
    if not pending:
        print("[BACKFILL] 无待补段（所有 spec 均已在 CHANGELOG 有对应段）")
        return 0
    print("[BACKFILL] 已立段 %d 个（max W%d）· 待补 %d 段：%s"
          % (len(established), max(established), len(pending),
             " ".join("W%d" % w for w, _ in pending)))

    cl, cl_nl = load("CHANGELOG.md")
    fi, fi_nl = load("scripts/output/file-index.md")
    seg_before = len(segments(cl))
    fi_before = len(RE_FI_SEG.findall(fi))
    max_w = max(max(established), max(w for w, _ in pending))

    for w, spec in pending:
        # W956/P-43-05：与 batch_cascade 同款段状态断言（两个段状态写入点共用判据·E-28 防线）
        import batch_cascade as _bc
        _bc._assert_status_wnum(spec, spec["batch"])
        cl, anchor = insert_before_smaller(cl, w, changelog_block(spec))
        fi = insert_fi(fi, w, file_index_block(spec))
        print("  + W%-3d 插在 W%d 段之前" % (w, anchor))

    # ---------- 编号规则推进（只升不降） ----------
    m = RE_RULE.search(cl)
    assert m, "编号规则「（W001-W###）」锚点缺失"
    old_max = int(m.group(1))
    if max_w > old_max:
        cl = cl.replace("（W001-W%d）" % old_max, "（W001-W%d）" % max_w, 1)
        print("  规则：W001-W%d -> W001-W%d" % (old_max, max_w))
    else:
        print("  规则：不变（已是 W001-W%d）" % old_max)

    # ---------- 落盘前全量断言 ----------
    segs = segments(cl)
    ws = [w for w, _ in segs]
    assert len(ws) == seg_before + len(pending), \
        "段数不符：%d + %d != %d" % (seg_before, len(pending), len(ws))
    assert ws == sorted(ws, reverse=True), "段序未保持严格降序：%s" % ws[:20]
    assert len(set(ws)) == len(ws), "出现重复段号"
    for w, spec in pending:
        title_body = re.sub(r"^W\d+\s+", "", spec["title"]).strip()
        head = "### %s（%s）：%s" % (spec["batch"], spec["date"], title_body)
        assert cl.count(head) == 1, "W%d 段标题命中 %d 次（应为 1）" % (w, cl.count(head))
    assert len(RE_FI_SEG.findall(fi)) == fi_before + len(pending), "file-index 段数不符"
    fi_ws = [int(x[1:]) for x in RE_FI_SEG.findall(fi)]
    assert fi_ws == sorted(fi_ws, reverse=True), "file-index 段序未保持降序"

    print("[BACKFILL] 断言全过：CHANGELOG %d->%d 段（降序完好）· file-index %d->%d 段"
          % (seg_before, len(ws), fi_before, len(fi_ws)))

    if not args.apply:
        print("[DRY-RUN] 未落盘。加 --apply 写回。")
        return 0

    for path, text, nl in (("CHANGELOG.md", cl, cl_nl),
                           ("scripts/output/file-index.md", fi, fi_nl)):
        with open(os.path.join(ROOT, path), "w", encoding="utf-8", newline="") as f:
            f.write(text.replace("\n", nl))
        print("  写入 %s（%s）" % (path, "CRLF" if nl == "\r\n" else "LF"))
    print("[APPLY] 补段完成：%d 段" % len(pending))
    return 0


if __name__ == "__main__":
    sys.exit(main())
