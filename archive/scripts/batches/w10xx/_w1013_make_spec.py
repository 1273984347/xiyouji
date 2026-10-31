# -*- coding: utf-8 -*-
"""_w1013_make_spec.py — W1013 级联 spec 生成（文件行按 git 现状全量列出）

沿用 W1001 批 `_w1001_stage.py` 的口径：
  · 文件行按**当前 git 状态**（暂存区 + 未跟踪）全量列出，不手抄；
  · file_index_rows 每文件 1 行（W 号 + 归类说明）；
  · desc / head_sentence 禁分隔符「· ; —」（batch_cascade precheck fail-closed）；
  · agents_note 以「阿拉伯日期（W###）」开头且 ≤120 字（W964 定形契约）。

输出：scripts/output/_w1013_spec.json
用法：py -3 scripts/_w1013_make_spec.py
"""
from __future__ import annotations

import io
import json
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
SPEC = os.path.join(OUT, "_w1013_spec.json")

BATCH = "W1013"
DATE = "2026-10-29"
TITLE = "W1013 回次 og:image 全覆盖批·第二轮（12 张线描立像/场面）"
DESC = "回次 og:image 全覆盖第二批：十二张线描立像与场面接入对应回目页并换专属 og:image"
HEAD_ENTRY = "2026-10-29（W1013 回次 og:image 全覆盖第二轮 12 张）"
HEAD_SENTENCE = "回次 og:image 全覆盖第二批：十二张线描立像与场面接入对应回目页并换专属 og:image"

AGENTS_NOTE = (
    "2026-10-29（W1013）给回目页补 og:image，出了第二轮 12 张。按 slug 全表避开已出的 88 个主体；"
    "母版段只改三处派生场面段。5 张重出：朱砂成大块、钢鞭多钩、主体底被切、杖脱手——"
    "判据全 PASS，得靠人眼。"
)

MILESTONE = (
    "- **W1013 回次 og:image 全覆盖批·第二轮**（12 张线描立像/场面）：\n"
    "  - 缺口实读 80 回 · 回目覆盖 20 → 32 回（余 68 回）\n"
    "  - 母版段两变体：立像段逐字 249 字符 + 场面段仅改 3 处\n"
    "  - 12 张主体全部避开已出的 88 个 plate-line 主体（slug 全表核对）· 5 张重出（两轮）\n"
    "  - 坑表 +2 条（冒号路径落盘 0 字节 / 编号 max 不等于主体数）"
)

BODY_TAIL = (
    "\n\n**本批要点**：① **缺口实读 80 回**（100 回中已有配图 20 回）· ② **已出主体全表核对**——"
    "plate-set 实为 **88 个母版 / 88 个唯一 slug**（编号 1–12 被四个批次族复用 ⇒ 编号 max 60 不等于主体数）"
    "⇒ 12 个候选主体与全表**零冲突**；③ **母版段两变体**——立像段**逐字复用 249 字符**（7 张），"
    "场面段**仅改 3 处**（5 张）；④ **5 张重出**（两轮）——朱砂被画成大块火焰 / 竖椭圆、钢鞭末端多出弯钩、"
    "主体底被画布切掉、杖头金龙悬空脱手（其中 4 张**机器判据全 PASS**·只靠人眼硬关）；"
    "⑤ **12 页接入**（题图位 + 专属 1200×630 og:image）⇒ 回目页覆盖 **20 → 32 回**、缺口 **80 → 68 回**；"
    "⑥ **未覆盖页零回归**——缺口 68 页中 66 页仍为通用 og-cover-ink-zh.jpg、2 页保留既有 card-* 专属图。\n\n"
    "**验证**：母版判据 J1–J10 **100/100 FAIL 0** · 裁切验算 **100/100 FAIL 0** · 负样本自证命中（J1 尺寸）· "
    "落位验收 **0 FAIL**（含「未覆盖页 68 个零回归」）· 幂等复跑 **24/24 SKIP** · "
    "浏览器实跑 **0 FAIL**（题图 HTTP 200 + naturalWidth > 0 + 位置在 h1 之后 + 暗色隐藏生效）· "
    "第 48 门禁 **0 FAIL**（新增文件·全项符合）· 全量门禁 **55 段全绿**。\n\n"
    "> - **状态**：已收官（12 张落地·母版族 88 → 100 张·既有 88 张母版与站点版零改动·"
    "其余 68 个无配图回目页的 og:image 未误改·坑表 +2 条）\n"
)


def main() -> int:
    st = subprocess.run(["git", "status", "--porcelain", "-z"], capture_output=True, cwd=REPO).stdout
    files = []
    for rec in st.split(b"\x00"):
        if not rec:
            continue
        s = rec.decode("utf-8")
        p = s[3:]
        if p not in files:
            files.append(p)
    files = sorted(f for f in files if f and not f.startswith("tmpe/"))

    rows = []
    for f in files:
        note = "本批新增/修改"
        if f.startswith("site/reader/ch"):
            note = "回目页接入题图 + 换专属 1200×630 og:image"
        elif f.startswith("site/static/images/og-"):
            note = "专属 og:image（1200×630·由母版裁切）"
        elif f.startswith("site/static/images/plate-line-"):
            note = "站点版（母版裁切·只裁上部留白）"
        elif f.startswith("assets/promo/plate-set/raw/"):
            note = "出图原件（12 张·含 5 张重出）"
        elif f.startswith("assets/promo/plate-set/plate-line-"):
            note = "新增母版（1200×1600）"
        elif f.startswith("assets/promo/plate-set/preview-"):
            note = "拼图预览（含本批 12 张）"
        elif f.startswith("scripts/"):
            note = "本批工具/产物"
        elif f.startswith("docs/"):
            note = "登记面（报告/坑表/计数链/台账）"
        rows.append("| %s | W1013 | %s |" % (f, note))

    body = (
        "\n\n\n\n> **来源**：用户 2026-10-29 目视确认 W1005 两张 hero 图「合格」后令「继续扩」"
        "⇒ 沿用 W1001 批已过目的口径（线描立像族·母版段两变体·按题材定主体·战斗回场面其余立像·12 张一批）。\n"
        ">\n"
        "> - **文件**：" + "、".join(files) + "。\n"
        + BODY_TAIL
    )

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
    print("spec 写出 · %s · 文件清单 %d 项 · file_index %d 行"
          % (os.path.basename(SPEC), len(files), len(rows)))
    print("agents_note %d 字（上限 120）" % len(AGENTS_NOTE))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
