# -*- coding: utf-8 -*-
"""_w1043_make_spec.py — W1043 级联 spec 生成（资产批·12 张扩量第四轮）

与 W1042 工具面批不同，本批 spec 文案全变 ⇒ 新写（派生纪律的适用面是「内容不变只改常量」）；
但**沿用 W1018/W1042 已修的三处口径**（不得重犯）：
  ① git 调用统一 `-c core.quotepath=false` ⇒ 含中文的路径以**真中文**写入段文件行；
  ② 文件全集 = 索引态 ∪ 工作树 ∪ 未跟踪，再**剔除磁盘已不存在的路径**；
  ③ 段「文件」行只列**现存路径**；`file_index_rows` 另含 rename 删除面旧名。

输出：scripts/output/_w1043_spec.json
用法：py -3 archive/scripts/batches/w10xx/_w1043_make_spec.py
"""
from __future__ import annotations

import io
import json
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
OUT = os.path.join(REPO, "scripts", "output")
SPEC = os.path.join(OUT, "_w1043_spec.json")

BATCH = "W1043"
DATE = "2026-10-31"
TITLE = "W1043 回次 og:image 全覆盖批·第四轮（12 张线描立像/场面）"
DESC = "回次 og:image 全覆盖第四轮：十二张线描立像与场面接入缺口回目页并换专属 og:image"
HEAD_ENTRY = "2026-10-31（W1043 回次 og:image 全覆盖第四轮 12 张）"
HEAD_SENTENCE = "回次 og:image 全覆盖第四轮：十二张线描立像与场面接入缺口回目页并换专属 og:image"
AGENTS_NOTE = ("2026-10-31（W1043）回目页补 og:image，第四轮 12 张。缺口实读 54 回通用 og，"
               "已出 111 slug 全表避重；本批新增 11 回题图、1 回只换 og（该回已有旧题图）。")
MILESTONE = ("- **W1043 回次 og:image 全覆盖批·第四轮**（12 张线描立像/场面）：\n"
             "  - 缺口实读 54 回通用 og · 已出母版 112 张 / 唯一 slug 111 个 · 全表避重\n"
             "  - 母版段两变体：立像段逐字 249 字符（6 张）+ 场面段仅改 3 处（6 张）\n"
             "  - 12 个主体全部未出（如意真仙/吹口仙/太阴星君/多目怪/紫阳真人/乙救苦天尊 +\n"
             "    九灵元圣与十八罗汉/辟寒与辟暑二王/玉面狐狸/奔波儿灞与灞波儿奔/地涌夫人/犀牛怪）\n"
             "  - 落位 11 回题图 + 1 回只换 og ⇒ 配图覆盖 44 → 55 回 · 通用 og 缺口 54 → 43 回")

BODY = (
    "\n\n\n\n> **来源**：用户 2026-10-30 五项连发指令之第 5 项「剩余 56 回继续扩量（每批 12 张·约 5 批）」"
    "⇒ 本批为第四轮（W1043）。\n"
    ">\n"
    "> **基线实读**（非引用旧批报告）：已落位专属 og-image **44 回** + 保留既有 card-* 专属 **2 回**"
    "（ch019/ch031）+ 通用 og 缺口 **54 回**；已出母版 **112 张 / 唯一 slug 111 个**"
    "（早期命名 `NN-slug` 与新批命名 `NN-chNNN-slug` 两种形态全扫）。\n"
    ">\n"
    "> - **文件**："
)


def _git(*args):
    out = subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO] + list(args),
                         capture_output=True).stdout
    return out.decode("utf-8", "replace")


def _collect_files():
    files = []

    def add(p):
        p = p.strip().strip('"')
        if p and not p.startswith("tmpe/") and p not in files:
            files.append(p)

    for ln in _git("diff", "--cached", "--name-only").splitlines():
        add(ln)
    for ln in _git("diff", "--name-only").splitlines():
        add(ln)
    for ln in _git("status", "--porcelain").splitlines():
        if ln.startswith("?? "):
            add(ln[3:])
    alive = [p for p in files
             if os.path.exists(os.path.join(REPO, p.replace("/", os.sep)))]
    dropped = [p for p in files if p not in alive]
    if dropped:
        print("[DEBUG] 剔除磁盘已不存在路径 %d 项：%s" % (len(dropped), dropped))
    return sorted(alive)


def _rename_map():
    m = {}
    for ln in _git("status", "--porcelain").splitlines():
        if ln.startswith("R  ") and " -> " in ln:
            old, new = ln[3:].split(" -> ", 1)
            m[old.strip()] = new.strip()
    return m


def main() -> int:
    files = _collect_files()
    renames = _rename_map()
    deleted = sorted(p for p in renames if p not in files)
    print("[DEBUG] files=%d · rename=%d · 删除面=%d" % (len(files), len(renames), len(deleted)))

    def note_of(f):
        if f.startswith("archive/scripts/batches/w10xx/_w1043"):
            return "本批工具脚本（归档批次区）"
        if f.startswith("scripts/output/_w1043"):
            return "本批出图批次与结果件"
        if f.startswith("assets/promo/plate-set/raw/round17"):
            return "出图原件（12 份·含 1 张重出）"
        if f.startswith("assets/promo/plate-set/plate-line-"):
            return "新增母版（1200×1600）"
        if f.startswith("assets/promo/plate-set/preview-"):
            return "拼图预览（含本批 12 张）"
        if f.startswith("site/static/images/og-plate-line"):
            return "专属 og:image（1200×630）"
        if f.startswith("site/static/images/plate-line"):
            return "站点版（母版裁切·只裁上部留白）"
        if f.startswith("site/reader/"):
            return "缺口回目页接入题图 + 换专属 og:image"
        if f.startswith("docs/11-方案报告/计划方案/"):
            return "方案报告（执行前计划件）"
        if f.startswith("docs/11-方案报告/"):
            return "方案报告（索引/架构方案）"
        if f == "docs/agent/pitfalls.md":
            return "坑表（+1 条·判据脆性）"
        if f.startswith("docs/00-"):
            return "台账（认领行与收官回填）"
        if f.startswith("scripts/output/"):
            return "登记面产物（索引/统计/工具清单）"
        return "本批新增/修改"

    rows = ["| %s | W1043 | %s |" % (f, note_of(f)) for f in files]
    for old in deleted:
        rows.append("| %s | W1043 | 本批改名·旧名（已由 %s 取代） |" % (old, renames[old]))

    body = BODY + "、".join(files) + "。\n\n"
    body += ("**本批要点**：① **缺口与 slug 全表实读**——通用 og 缺口 54 回、已出母版 112 张 / "
             "唯一 slug 111 个（早期命名无 ch 段 ⇒ 只按新形态扫会漏 100 个）；"
             "② **母版段两变体**——立像段逐字复用 249 字符（6 张）、场面段仅改 3 处（6 张）；"
             "③ **12 个主体全部未出**（如意真仙/吹口仙/太阴星君/多目怪/紫阳真人/乙救苦天尊 + "
             "九灵元圣与十八罗汉/辟寒与辟暑二王/玉面狐狸/奔波儿灞与灞波儿奔/地涌夫人/犀牛怪）；"
             "④ **1 张重出**——93 号原选 ch033 与 86 号吹口仙**同回** ⇒ 同页两题图不被落位脚本支持 "
             "⇒ 改 ch095 玉面狐狸并重出（重出件须同时清旧结果文件条目，否则下载器幂等会复活旧件）；"
             "⑤ **1 回只换 og**——ch086 已有 W1001 批题图（毗蓝大菩萨）⇒ 题图不覆盖、只换专属 og；"
             "⑥ **坑表 +1 条**（E-46·判据脆性：暗色隐藏规则用整串字面量匹配 ⇒ 页面 CSS 多行排版时"
             "误判「缺规则」⇒ 改为容忍空白的正则）。"
             "⑦ **订正前批口径**——W1042 段所写「坑表 +4 条（124 → 128 条）」实为 **+8 条"
             "（124 → 132 条）**（该批一次落 E-38…E-45 八条；本批再加 E-46 ⇒ 现 133 条）；"
             "历史段不改写，故在此订正。\n\n")
    body += ("**验证**：母版判据 **124 张 · FAIL 0** · 裁切验算 **124 张 · FAIL 0** · "
             "落位验收 **0 FAIL**（11 回题图 + 1 回只换 og + 未覆盖页零回归）· "
             "配图覆盖 **44 → 55 回** · 通用 og 缺口 **54 → 43 回** · 全量门禁见收官提交。\n\n")
    body += ("> - **状态**：已收官（12 张落地·新增题图 11 回·母版族 112 → 124 张·"
             "既有 112 张母版与站点版零改动·待用户目视）\n")

    spec = {
        "batch": BATCH,
        "date": DATE,
        "title": TITLE,
        "desc": DESC,
        "head_entry": HEAD_ENTRY,
        "head_sentence": HEAD_SENTENCE,
        "changelog_body": body,
        "milestone_block": MILESTONE,
        "agents_note": AGENTS_NOTE,
        "file_index_rows": rows,
    }
    io.open(SPEC, "w", encoding="utf-8", newline="\n").write(json.dumps(spec, ensure_ascii=False, indent=1))
    print("spec 写出 · %s · 文件清单 %d 项 · file_index %d 行 · agents_note %d 字"
          % (os.path.basename(SPEC), len(files), len(rows), len(AGENTS_NOTE)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
