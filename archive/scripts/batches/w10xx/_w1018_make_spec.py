# -*- coding: utf-8 -*-
"""_w1018_make_spec.py — W1018 级联 spec 生成（结构照 w10xx/_w1013_make_spec.py·文案换本批）

文件行按 **git 现状全量**列出（不手抄）；desc/head_sentence 禁分隔符「· ; —」；
agents_note 以「阿拉伯日期（W###）」开头且 ≤120 字（W964 定形契约）。

输出：scripts/output/_w1018_spec.json
用法：py -3 scripts/_w1018_make_spec.py
"""
from __future__ import annotations

import io
import json
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
SPEC = os.path.join(OUT, "_w1018_spec.json")

BATCH = "W1018"
DATE = "2026-10-29"
TITLE = "W1018 回次 og:image 全覆盖批·第三轮（12 张线描立像/场面）"
DESC = "回次 og:image 全覆盖第三轮：十二张线描立像与场面接入对应回目页并换专属 og:image"
HEAD_ENTRY = "2026-10-29（W1018 回次 og:image 全覆盖第三轮 12 张）"
HEAD_SENTENCE = "回次 og:image 全覆盖第三轮：十二张线描立像与场面接入对应回目页并换专属 og:image"
AGENTS_NOTE = ("2026-10-29（W1018）给回目页补 og:image，第三轮 12 张。先扫缺口 68 回角色谱，"
               "按已出 100 主体 slug 全表避重；母版段只改三处派生场面变体。3 张重出：桌案器物、"
               "主体过小、四周黑边——判据只抓到两张。")
MILESTONE = ("- **W1018 回次 og:image 全覆盖批·第三轮**（12 张线描立像/场面）：\n"
             "  - 缺口实读 68 回 · 已出 100 主体 slug 全表避重 · 回目覆盖 32 → 44 回（余 56 回）\n"
             "  - 母版段两变体：立像段逐字 249 字符（6 张）+ 场面段仅改 3 处（6 张）\n"
             "  - 12 个主体全部未出（虎先锋/清风童子/老鼋/杏仙/寇员外/金顶大仙 + 巴山虎倚海龙/"
             "鼍龙摩昂/羊力大仙/青牛精/青狮白象/辟尘大王）· 3 张重出（器物/主体过小/黑边）\n"
             "  - 本笔连带登记 W1015 工具链补强（跨行改写扫描器 + 第 48 门禁读盘路径覆盖）")

BODY = (
    "\n\n\n\n> **来源**：用户 2026-10-29 令「同族扫描 + 第 48 门禁补覆盖 做完再继续剩余 68 回扩量」"
    "⇒ 沿用 W1001/W1013 批已过目的口径（线描立像族·母版段两变体·按题材定主体·12 张一批）。\n"
    ">\n"
    "> **连带登记**：本笔同时落 **W1015 工具链稳健性补强①** 的登记面——"
    "① 跨行改写扫描器（`scripts/check_cross_line_rewrite.py`：改写面正则「`[^X]*` 无尾锚点 ⇒ "
    "匹配段可跨行 ⇒ `re.sub` 整段替换 = 静默删行」；全仓 scripts/ 全树实扫 **高危 0 处**，"
    "另 43 处可疑 + 184 处只读面；判据自带 4 例负样本自证；接线 `ci_sim.py` 第 8 项）"
    "② 第 48 门禁补覆盖（`judge_file()` 的**读盘路径**此前零覆盖 ⇒ W1005 批 `R.io` 类 "
    "AttributeError 潜伏到首个新增件才引爆；现补 self_test 第⑧例 + 4 例 pytest）。"
    "W1015 提交 = `7771c9d3`（让号·台账行精确暂存·未代提并行批在途件）。\n"
    ">\n"
)


def _git(*args):
    """git 调用统一加 `-c core.quotepath=false`。

    病根（本批实证）：git show/status 的默认输出把中文路径转成 octal 转义字面量
    （`W\\346\\211\\271...`）⇒ 直接拼进段文件行 ⇒ CHANGELOG 与 file-index 里
    中文路径显示为乱码串（C4-f 判「未入提交树」也是同一根因的连带症状）。
    """
    out = subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO] + list(args),
                         capture_output=True).stdout
    return out.decode("utf-8", "replace")


def _collect_files():
    """本批文件全集（段「文件」行与 file_index_rows 的唯一来源）。

    口径 = ① 已提交的资产面（b0c0d072）∪ ② 索引态（登记面）∪ ③ 工作树未暂存
    ∪ ④ 未跟踪，**再剔除磁盘上已不存在的路径**（一次性出图中间件已被清理 ⇒
    列进清单会让第 31 门禁 C4-f 判「未入提交树」）。
    """
    files = []

    def add(p):
        p = p.strip().strip('"')
        if p and not p.startswith("tmpe/") and p not in files:
            files.append(p)

    for ln in _git("show", "--name-only", "--format=", "b0c0d072").splitlines():
        add(ln)
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
    """本批 rename 映射 {旧名: 新名}（第 51 门禁判据用 diff.renames=false ⇒ rename 计为删+增，
    两侧都须在 spec 内，否则旧名判「spec 之外·代提风险」）。"""
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
        if f.startswith("site/reader/ch"):
            return "回目页接入题图 + 换专属 1200×630 og:image"
        if f.startswith("site/static/images/og-"):
            return "专属 og:image（1200×630·由母版裁切）"
        if f.startswith("site/static/images/plate-line-"):
            return "站点版（母版裁切·只裁上部留白）"
        if f.startswith("assets/promo/plate-set/raw/") and f.endswith(".md"):
            return "出图原件目录清单（索引/说明）"
        if f.startswith("assets/promo/plate-set/raw/"):
            return "出图原件（12 张·含 3 张重出）"
        if f.startswith("assets/promo/plate-set/plate-line-"):
            return "新增母版（1200×1600）"
        if f.startswith("assets/promo/plate-set/preview-"):
            return "拼图预览（含本批 12 张）"
        if f.startswith("scripts/"):
            return "本批工具/产物"
        if f.startswith("docs/"):
            return "登记面（报告/坑表/计数链/台账）"
        return "本批新增/修改"

    rows = ["| %s | W1018 | %s |" % (f, note_of(f)) for f in files]
    # 删除面（rename 旧名）：只进 file_index_rows，不进 CHANGELOG 段「文件」行——
    # 后者受第 31 门禁 C4-f 约束（清单路径须在提交树内 ⇒ 已删旧名会判红）；
    # 前者受第 51 门禁约束（索引态路径集 ⊆ spec ⇒ rename 两侧都须在）。
    for old in deleted:
        rows.append("| %s | W1018 | 本批改名·旧名（已由 %s 取代） |" % (old, renames[old]))

    body = BODY + "> - **文件**：" + "、".join(files) + "。\n\n"
    body += ("**本批要点**：① **缺口全量角色谱扫描**——缺口 68 回逐回统计角色出现次数并打上下文片段；"
             "② **已出主体全表避重**——plate-set 实为 **88→100 个母版 / 100 个唯一 slug**"
             "（编号 1–12 被四个批次族复用 ⇒ 编号 max≠主体数）⇒ 12 个主体与已出全表**零冲突**；"
             "③ **母版段两变体**——立像段**逐字复用 249 字符**（6 张），场面段**仅改 3 处**（6 张）；"
             "④ **3 张重出**——① 画面出现桌案器物（违反母版段「不画器物细节」）② 主体过小过淡"
             "（下部墨 0.0217 < 0.03）③ 左右大面积黑边 + 主体触顶触底（3×3 窗口暗占比 0.761 / 判据值 200.08）；"
             "⑤ **落位 12 页** ⇒ 回目覆盖 **32 → 44 回**、缺口 **68 → 56 回**；"
             "⑥ **未覆盖页零回归**——缺口 56 页中 54 页仍为通用 og-cover-ink-zh.jpg、2 页保留既有 card-* 专属图。\n\n")
    body += ("**验证**：母版判据 J1–J10 **112 张 · FAIL 0**（重出后）· 裁切验算 **112 张 · FAIL 0**（重出后）· "
             "落位验收 **0 FAIL**（12 页题图 + og + alt + 暗色隐藏 + 未覆盖页零回归）· "
             "跨行改写扫描器 **高危 0 处** · 第 48 门禁自测 **9/9** · 全量门禁见收官提交。\n\n")
    body += ("> - **状态**：已收官（12 张落地·母版族 100 → 112 张·既有 100 张母版与站点版零改动·"
             "其余 56 个无配图回目页的 og:image 未误改·坑表 +2 条·待用户目视）\n")

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
