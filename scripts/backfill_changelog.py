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
# W1122：file-index 面的归档件（立段判定须与 CHANGELOG 面同口径合看现役+归档两面）
ARCHIVE_FILE_INDEX = os.path.join("archive", "docs", "file-index-ARCHIVE.md")

SPEC_KEYS = ("batch", "date", "title", "desc", "head_entry", "head_sentence",
             "changelog_body", "milestone_block", "agents_note", "file_index_rows")

# W1122：字段需求按「写入去向」拆分——CHANGELOG 面与 file-index 面所需字段不同。
# 完整性检查改为按**待补的那一面**校验：该面缺字段 ⇒ 阻断（判据强度不降）；
# 无关面的历史缺字段不再误伤待补面（原单面判定会让「只缺一面字段」的件整批阻断）。
CL_FACE_KEYS = ("batch", "date", "title", "changelog_body")
FI_FACE_KEYS = ("batch", "date", "title", "file_index_rows")


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
    """单段 CHANGELOG 块（与 batch_cascade._face_changelog 同形态）。

    W1157 根修（粘行事故）：段头与 body 是**直接字符串拼接**，依赖 body 以空行（\\n\\n）
    开场才不粘行——batch_cascade 的 PRECHECK 有此判据而本共享渲染点没有 ⇒ 无判据入口
    （rebuild_section）会产出「…错位归位）**本批要点**…」粘行段（本批实证）。判据上移到
    单一事实源：body 非空行开场即 fail-closed（与 cascade PRECHECK 同语义），指引自改 spec。
    """
    body = spec["changelog_body"]
    # W1157 根修（粘行事故）：段头与 body 是**直接字符串拼接**，body 不以空行开场即产出
    # 「…错位归位）**本批要点**…」粘行段（batch_cascade PRECHECK 有判据而本共享渲染点
    # 没有的同族缺口·本批实证）。渲染点做**规范化兜底**（缺空行自动补·不 raise·api_diff
    # 零破坏）：任何入口（含未来新入口）经此渲染永不粘行。
    if not body.startswith("\n\n"):
        body = "\n\n" + body.lstrip("\n")
    title_body = re.sub(r"^W\d+\s+", "", spec["title"]).strip()
    return "### %s（%s）：%s" % (spec["batch"], spec["date"], title_body) + body + "\n"


def file_index_block(spec):
    """单段 file-index 块（与 batch_cascade._face_file_index 同形态）。

    W1142 立式：行数超阈值时自动转目录分组行（职责分工——spec 恒全量·登记面压缩，
    每文件路径集由 spec 权威承载·covers group-aware 判定兼容）。
    """
    import batch_spec as _bs
    tb = re.sub(r"^W\d+\s+", "", spec["title"].split(" — ")[0].split("（")[0]).strip()
    grouped = _bs.fi_group_rows(spec["file_index_rows"], spec.get("batch", ""))
    rows = ["## %s %s（%s）" % (spec["batch"], tb, spec["date"]),
            "", "| 文件 | W | 说明 |", "|---|---|---|"] + grouped + ["", ""]
    return "\n".join(rows)


def insert_fi(text, w, block):
    """file-index 段按数值序插入（W676/W677 先例：认领号小于现役 max 时插数值位）。"""
    hits = [(int(m.group(1)[1:]), m.start()) for m in RE_FI_SEG.finditer(text)]
    for sw, st in hits:
        if sw < w:
            return text[:st] + block + "\n" + text[st:]
    raise AssertionError("file-index 找不到更小的段可作锚点（W%d）" % w)


def fi_segments(text):
    """file-index 已立段号集合（W1122 新增·与 segments 同形态）。"""
    return {int(m.group(1)[1:]) for m in RE_FI_SEG.finditer(text)}


def collect_pending_faces():
    """扫 spec，判定每个 spec 在 **CHANGELOG 面**与 **file-index 面**各自的立段状态。

    W1122 根修（遗留 A）：原 collect_pending 的「已立段」判定**只看 CHANGELOG 一面**
    ⇒ 某批若 CHANGELOG 已立段而 file-index 未立段 ⇒ 被判「已立段」⇒ 跳过
    ⇒ **file-index 段永远补不上**（单面判定 ⇒ 双面独立判定）。

    返回 ([(W 号, spec, need_changelog, need_file_index)], established, fi_established)；
    两面皆已立段 ⇒ 不在结果内。
    """
    cl, _ = load("CHANGELOG.md")
    established = {w for w, _ in segments(cl)}
    arc_p = os.path.join(ROOT, ARCHIVE_CHANGELOG)
    if os.path.exists(arc_p):
        arc, _ = load(ARCHIVE_CHANGELOG)
        established |= {w for w, _ in segments(arc)}
    fi, _ = load("scripts/output/file-index.md")
    fi_established = fi_segments(fi)
    fi_arc_p = os.path.join(ROOT, ARCHIVE_FILE_INDEX)
    if os.path.exists(fi_arc_p):
        fi_arc, _ = load(ARCHIVE_FILE_INDEX)
        fi_established |= fi_segments(fi_arc)
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "scripts", "output", "_w*_spec.json"))):
        try:
            spec = json.load(open(p, encoding="utf-8"))
        except Exception:
            # W1117 根修：历史 spec 可能含裸控制字符而不可解析 ⇒ 不阻断整个补段流程。
            # W1122：跳过条件由「CHANGELOG 已立段」收紧为「**两面皆已立段**」
            # ⇒ 一面已立一面未立的坏件仍阻断（该件确实需要补段 ⇒ fail-closed）。
            m = re.search(r"_w(\d+)_spec\.json$", os.path.basename(p))
            if m and int(m.group(1)) in established and int(m.group(1)) in fi_established:
                continue
            raise
        batch = spec.get("batch")
        if not batch:
            continue
        w = int(batch[1:])
        need_cl = w not in established
        need_fi = w not in fi_established
        if not need_cl and not need_fi:
            continue
        missing = []
        if need_cl:
            missing += [k for k in CL_FACE_KEYS if k not in spec]
        if need_fi:
            missing += [k for k in FI_FACE_KEYS if k not in spec]
        if missing:
            raise AssertionError("%s 缺字段 %s（补段前先补 spec）" % (os.path.basename(p), missing))
        out.append((w, spec, need_cl, need_fi))
    out.sort(key=lambda t: t[0])
    return out, established, fi_established


def collect_pending():
    """扫 spec，筛出「未立段」的（现役+归档两面合看·已立段的不重复补）。

    W1122：返回形状与语义**均保持不变**（按 CHANGELOG 面判定）⇒ 既有调用方不受影响；
    双面独立判定的新能力见 collect_pending_faces。
    """
    faces, established, _fi_established = collect_pending_faces()
    return [(w, spec) for w, spec, need_cl, _need_fi in faces if need_cl], established


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

    # W1122：改用**双面独立判定**（CHANGELOG 面与 file-index 面分判）——
    # 原判定只看 CHANGELOG 一面 ⇒ 一面已立一面未立的批次被永久跳过 ⇒ file-index 段补不上。
    pending_faces, established, fi_established = collect_pending_faces()
    if args.only:
        only = {int(x.strip().lstrip("Ww")) for x in args.only.split(",") if x.strip()}
        known = {w for w, _s, _c, _f in pending_faces}
        unknown = sorted(only - known)
        assert not unknown, "--only 指定号 %s 不在待补清单（或 spec 缺失/两面皆已立段）" % unknown
        pending_faces = [t for t in pending_faces if t[0] in only]
    # W1122：**历史缺口**（待补 W 号低于已立段 max）默认**不自动补**——补它会把 2026-10 的
    # 老段插进现役降序位（改现役面 + 撞体积窗）⇒ 须显式 --only 指定才补（fail-closed·先看清单）。
    if not args.only and established:
        _hist = [t[0] for t in pending_faces if t[0] < max(established)]
        if _hist:
            print("[BACKFILL] 提示：以下为**历史缺口**（W 号低于已立段 max W%d）·默认不自动补"
                  "（会改现役面）⇒ 须显式 --only %s 确认后补：%s"
                  % (max(established), ",".join("W%d" % x for x in _hist),
                     " ".join("W%d" % x for x in _hist)))
            pending_faces = [t for t in pending_faces if t[0] >= max(established)]
    if not pending_faces:
        print("[BACKFILL] 无待补段（所有 spec 均已在 CHANGELOG 与 file-index 两面有对应段）")
        return 0
    n_cl = sum(1 for _w, _s, c, _f in pending_faces if c)
    n_fi = sum(1 for _w, _s, _c, f in pending_faces if f)
    print("[BACKFILL] 已立段 CHANGELOG %d 个（max W%d）· file-index %d 个（max W%d）"
          "· 待补 %d 段（CHANGELOG 面 %d · file-index 面 %d）：%s"
          % (len(established), max(established), len(fi_established),
             max(fi_established) if fi_established else 0,
             len(pending_faces), n_cl, n_fi,
             " ".join("W%d" % t[0] for t in pending_faces)))

    cl, cl_nl = load("CHANGELOG.md")
    fi, fi_nl = load("scripts/output/file-index.md")
    seg_before = len(segments(cl))
    fi_before = len(RE_FI_SEG.findall(fi))
    max_w = max(max(established), max(fi_established) if fi_established else 0,
                max(t[0] for t in pending_faces))

    for w, spec, need_cl, need_fi in pending_faces:
        if need_cl:
            # W956/P-43-05：与 batch_cascade 同款段状态断言（两个段状态写入点共用判据·E-28 防线）
            import batch_cascade as _bc
            _bc._assert_status_wnum(spec, spec["batch"])
            cl, anchor = insert_before_smaller(cl, w, changelog_block(spec))
            print("  + W%-3d CHANGELOG 段插在 W%d 段之前" % (w, anchor))
        if need_fi:
            fi = insert_fi(fi, w, file_index_block(spec))
            print("  + W%-3d file-index 段插入" % w)

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
    assert len(ws) == seg_before + n_cl, \
        "段数不符：%d + %d != %d" % (seg_before, n_cl, len(ws))
    assert ws == sorted(ws, reverse=True), "段序未保持严格降序：%s" % ws[:20]
    assert len(set(ws)) == len(ws), "出现重复段号"
    for w, spec, need_cl, _need_fi in pending_faces:
        if not need_cl:
            continue
        title_body = re.sub(r"^W\d+\s+", "", spec["title"]).strip()
        head = "### %s（%s）：%s" % (spec["batch"], spec["date"], title_body)
        assert cl.count(head) == 1, "W%d 段标题命中 %d 次（应为 1）" % (w, cl.count(head))
    assert len(RE_FI_SEG.findall(fi)) == fi_before + n_fi, "file-index 段数不符"
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
    print("[APPLY] 补段完成：%d 段" % len(pending_faces))
    return 0


if __name__ == "__main__":
    sys.exit(main())
