#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w953_cascade.py — W953 四面登记 + 当前态指针（themes 库专题题图批·12 张）

**文件清单由 PLATES 列表自动生成具体路径**（不再手写通配符）——W952 曾因手写 `scripts/_w952_*.py`
被门禁 C4-f 判红（门禁按「字面路径 token ∈ 提交树」核对）。

并发纪律：共享面**不整份 add**，改为**按内容粒度精确暂存**（HEAD 基底 + 本批段·update-index --cacheinfo）。

用法：python scripts/_w953_cascade.py [--dry-run]
"""
import argparse
import io
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = "W953"
LEDGER_REL = "docs/00-导读/W批次编号对账表.md"
CHANGELOG_REL = "CHANGELOG.md"
FILE_INDEX_REL = "scripts/output/file-index.md"
README_REL = "README.md"
HANDOVER_REL = "HANDOVER.md"

# (stem, 专题名, 主题页相对路径)
PLATES = [
    ("01-zhenjia-meihouwang", "真假美猴王专题", "site/reader/themes/真假美猴王专题.html"),
    ("02-pantao-yuan", "蟠桃园-体制内的秘密", "site/reader/themes/蟠桃园-体制内的秘密.html"),
    ("03-danaotian-gong", "大闹天宫-英雄还是悲剧", "site/reader/themes/大闹天宫-英雄还是悲剧.html"),
    ("04-shuilandong", "水帘洞专题", "site/reader/themes/水帘洞专题.html"),
    ("05-hunshi-sihou", "混世四猴专题", "site/reader/themes/混世四猴专题.html"),
    ("06-bingqi-xiuyang", "兵器的自我修养专题", "site/reader/themes/兵器的自我修养专题.html"),
    ("07-ershiba-xingsu", "二十八星宿专题", "site/reader/themes/二十八星宿专题.html"),
    ("08-sizhi-gongcao", "四值功曹专题", "site/reader/themes/四值功曹专题.html"),
    ("09-wufang-jiedi", "五方揭谛专题", "site/reader/themes/五方揭谛专题.html"),
    ("10-liuding-liujia", "六丁六甲专题", "site/reader/themes/六丁六甲专题.html"),
    ("11-jingubang-zhongliang", "金箍棒的重量专题", "site/reader/themes/金箍棒的重量-一万三千五百斤的秘密.html"),
    ("12-qiwu-zhuanji", "器物传记学专题", "site/reader/themes/器物传记学专题.html"),
]

SCRIPTS = [
    "scripts/_w953_make_prompts.py", "scripts/_w953_make_insert.py", "scripts/_w953_insert_plates.py",
    "scripts/_w953_cascade.py", "scripts/_w953_prep_raws.py", "scripts/_w953_prep_raws2.py",
    "scripts/_w953_prep_raws3.py", "scripts/_w953_update_readme.py", "scripts/_w945_prepare.py",
    "scripts/_w945_plates_verify.py",
    "scripts/_w951_check_crop.py", "scripts/_w951_site_sheet.py",
]
BATCH_JSONS = ["scripts/output/_w953_batch%d.json" % i for i in (1, 2, 3, 4, 5)]
EXTRA = ["scripts/output/_cascade_files_W953.txt", "scripts/output/file-index.md",
         "assets/promo/plate-set/README.md", "assets/promo/plate-set/preview-contact-sheet.png",
         "assets/promo/plate-set/preview-site-sheet.png", "assets/promo/plate-set/index.md",
         "CHANGELOG.md", "README.md", "HANDOVER.md", LEDGER_REL]

SITE_FILES = ["site/static/images/plate-line-%s.webp" % s for s, _, _ in PLATES]
PAGE_FILES = [p for _, _, p in PLATES]
FILE_LIST = SITE_FILES + PAGE_FILES + SCRIPTS + BATCH_JSONS + EXTRA

FILE_LINE = "> - **文件**：" + "、".join(FILE_LIST)


def claim_row():
    return (
        "| W953 | themes 库专题题图批（用户 2026-10-26 令「再继续帮我做几张素材图」·开工前三问已答："
        "**用途=内页专题题图续批 3:4 竖版** / **张数=12 张** / **风格=沿用站内线描墨稿风** / **题材=themes 库专题题图**）："
        "① **缺口**——reader 622 页中仅 39 页有题图；**themes 库 209 页只有 9 页有题图**、"
        "essays/culture/poetry 三库 91 页零题图 ⇒ 本批专攻 themes 库的空白专题；"
        "② **选题原则**——只选**有具象标志物**的专题（抽象概念题无法做人眼形制核·且难画成器物静物）；"
        "③ **题材**——真假美猴王（两个一模一样的猴王 + 照妖镜）/ 蟠桃园（守园仙童 + 三枚蟠桃）/ "
        "大闹天宫（金箍棒 + 反旗 + 蟠桃枝）/ 水帘洞（石猴拨帘 + 飞瀑）/ 混世四猴（石猴·马猴·猿猴·六耳猕猴并列）/ "
        "兵器专题（金箍棒·钉耙·月牙铲·火尖枪悬浮排开）/ 二十八星宿（星宿神将 + 星盘）/ 四值功曹（玉板·铜镜·日轮·漏刻）/ "
        "五方揭谛（金刚杵·铃·念珠·锡杖·如意）/ 六丁六甲（六甲神将结圈）/ 金箍棒的重量（金箍棒 + 大秤）/ "
        "器物传记（牛首持混铁棍 + 龙君托玉净瓶 + 紫金红葫芦）；"
        "④ **母版一字未改**——直接读上批 `_w952_batch1.json` 取母版（249 字符）拼本批 SUBJECT 段"
        "⇒ 跨批同族由**构造**保证（脚本断言「批内 12 条母版逐字一致」+「与 W952 母版逐字相同」）；"
        "⑤ **重出 6 张**——首轮机器判据抓出 06（兵器挤在左上角·顶满画面）与 10（六将画得过密），人眼另抓出 04（石帘被涂成黑色实心条）与 08（四值功曹被画成四张猴脸·题材误读）；二次重出时 06 画得过稀（墨量 0.0137 低于下限）、10 画成黑框密图 ⇒ 再调（兵器放大 + 六将改一字横排）后收敛；"
        "⑥ **防画中画**——并列型题材（混世四猴/兵器/四值功曹/五方揭谛/六丁六甲/器物传记）统一带"
        "「四周不得有任何边框、格子、展板或深色底板」措辞（W952 的 11-法宝系统正是栽在「展柜」上）；"
        "⑦ **接入**——按 `chapter-plate` 范式插入 12 个 themes 专题页（幂等脚本 `_w953_insert_plates.py`）；"
        "⑧ **前置**——preflight 取号 W953（max=W952+1·撞号检测无同号多行） | "
        "—（待回填） | —（待回填） | 在途（认领·未收官） | 并行 Agent 会话 2026-10-26（themes 库专题题图批） | "
        + " · ".join("`%s`" % f for f in FILE_LIST) + " |"
    )


CHANGELOG_SEG = """### W953（2026-10-26）：themes 库专题题图批（12 张·专题 + 器物静物·站内线描题图累计 40 张）

> **来源**：用户 2026-10-26 令「再继续帮我做几张素材图」，并要求开工前先问三件事。
>
> **三问答复**：① 用途与画幅 = **内页专题题图续批 · 3:4 竖版** ② 张数 = **12 张** ③ 参考风格 = **沿用站内线描墨稿风**（附加题材范围 = **themes 库专题题图**）。
>
%s

**缺口**：reader 622 页中仅 39 页有题图；**themes 库 209 页只有 9 页有题图**，essays / culture / poetry 三库 91 页仍零题图 ⇒ 本批专攻 themes 库空白专题。

**选题原则**：只选**有具象标志物**的专题（抽象概念题既难画成器物静物、也做不了人眼形制核）。

**母版一字未改**：直接读上批 `_w952_batch1.json` 取母版（249 字符）拼本批 SUBJECT 段 ⇒ 跨批同族由**构造**保证（脚本断言：批内 12 条母版逐字一致 + 与 W952 母版逐字相同）。

**防画中画**：并列型题材（混世四猴 / 兵器 / 四值功曹 / 五方揭谛 / 六丁六甲 / 器物传记）统一带「四周不得有任何边框、格子、展板或深色底板」措辞——W952 的 11-法宝系统正是栽在「展柜」上，重出后有效的措辞。

**接入**：沿用站内 `chapter-plate` 范式（420px 居中 + 描述性 alt + 浅底图暗色模式隐藏）。

**并发纪律**：共享面按内容粒度**精确暂存**（`git update-index --cacheinfo`·HEAD 为基底叠加本批段）⇒ 不把对方在途内容带进本批提交。

> - **验证**：（见本批脚本输出与对账表回填）
> - **状态**：在途（认领登记 W953·待提交入库）

""" % FILE_LINE

FILE_INDEX_SEG = (
    "## W953 themes 库专题题图批（12 张）（2026-10-26）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    + "".join("| site/static/images/plate-line-%s.webp | W953 | 新增·%s |\n" % (s, n) for s, n, _ in PLATES)
    + "".join("| %s | W953 | 接入题图（%s） |\n" % (p, n) for _, n, p in PLATES)
    + "| assets/promo/plate-set/ | W953 | 母版 + 站点版 + 拼图 + README（累计 40 张） |\n"
    "| scripts/_w953_make_prompts.py | W953 | 母版复用生成器（读上批 JSON 取母版·断言逐字一致） |\n"
    "| scripts/_w953_insert_plates.py | W953 | 12 页 chapter-plate 接入（幂等） |\n"
    "| scripts/_w953_cascade.py | W953 | 四面登记 + 当前态指针（共享面精确暂存·文件行自动生成） |\n"
    "| scripts/output/_w953_batch1~3.json | W953 | 出图参数 12 条 |\n"
    "| scripts/output/_cascade_files_W953.txt | W953 | 当批级联清单 |\n"
    "| CHANGELOG.md | W953 | W953 版段 |\n"
    "| docs/00-导读/W批次编号对账表.md | W953 | W953 认领行 |\n"
    "\n"
)

README_LINE = "> **当前批次 W953（2026-10-26）**：themes 库专题题图批（十二张线描专题题图，站内累计 40 张）"

HANDOVER_LINE = (
    "> 最后更新：2026-10-26（W953 themes 库专题题图批）·2026-10-25（W952 内页人物题图续批第二组）·"
    "2026-10-25（W951 题图版式批）·2026-10-25（W948 内页专题题图续批）·2026-10-25（W945 内页专题题图成套批）·"
    "2026-10-25（W944 章回插画新组批）·2026-10-25（W943 全站图片审查批）·2026-10-25（W942 Hero 素材全量复审批）·"
    "2026-10-25（W941 UI 图标位 emoji 治理批 + 东方线描图标集自绘）·2026-10-25（W940 Hero 素材题材辨识度修正批）·"
    "（W449-W549 及更早批次详见 CHANGELOG.md）"
)

HANDOVER_PROGRESS = (
    "## 一、当前进度（W953 themes 库专题题图批；更早批次详见 CHANGELOG.md）\n"
    "- **W953 themes 库专题题图批**：再出 12 张线描专题题图（真假美猴王/蟠桃园/大闹天宫/水帘洞/混世四猴/"
    "兵器/二十八星宿/四值功曹/五方揭谛/六丁六甲/金箍棒的重量/器物传记），接入 12 个 themes 专题页 ⇒ "
    "站内线描题图累计 40 张、reader 有题图页 51/622（themes 库 9→21 页）；母版 249 字符从上批 JSON 逐字复用。\n"
)


def t_ledger(t):
    if re.search(r"^\| " + BATCH + r" \|", t, re.M):
        return t
    lines = t.split("\n")
    anchor = None
    for i, ln in enumerate(lines):
        if re.match(r"^\| W952 \|", ln):
            anchor = i
            break
    if anchor is None:
        for i, ln in enumerate(lines):
            if re.match(r"^\| W\d+ \|", ln):
                anchor = i
                break
    if anchor is None:
        raise SystemExit("FATAL 台账未找到锚点行")
    lines.insert(anchor + 1, claim_row())
    return "\n".join(lines)


def t_changelog(t):
    if re.search(r"^### " + BATCH + r"（", t, re.M):
        return t
    m = re.search(r"^### W\d+", t, re.M)
    pos = m.start() if m else len(t)
    t = t[:pos] + CHANGELOG_SEG + t[pos:]
    t = re.sub(r"（W001-W\d+）", "（W001-W953）", t, count=1)
    return t


def t_file_index(t):
    if re.search(r"^## " + BATCH + r" ", t, re.M):
        return t
    m = re.search(r"^## W\d+", t, re.M)
    pos = m.start() if m else len(t)
    return t[:pos] + FILE_INDEX_SEG + t[pos:]


def t_readme(t):
    return re.sub(r"> \*\*当前批次 W\d+（2026-10-2[56]）\*\*：[^\n]*", README_LINE, t, count=1)


def t_handover(t):
    t = re.sub(r"> 最后更新：2026-10-2[56][^\n]*", HANDOVER_LINE, t, count=1)
    t = re.sub(r"- \*\*W953 themes 库专题题图批\*\*：[^\n]*\n", "", t)
    t = re.sub(r"## 一、当前进度（W\d+[^\n]*\n", HANDOVER_PROGRESS, t, count=1)
    t = re.sub(r"每次完成新 W### 后更新。最后更新：2026-10-2[56][^\n]*",
               "每次完成新 W### 后更新。最后更新：2026-10-26（W953 themes 库专题题图批）", t, count=1)
    return t


TARGETS = [
    (LEDGER_REL, t_ledger),
    (CHANGELOG_REL, t_changelog),
    (FILE_INDEX_REL, t_file_index),
    (README_REL, t_readme),
    (HANDOVER_REL, t_handover),
]


def read(p):
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def write(p, t, nl):
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))


def git_show(rel):
    p = subprocess.run(["git", "show", "HEAD:" + rel], cwd=REPO, capture_output=True)
    return None if p.returncode != 0 else p.stdout.decode("utf-8")


def stage_exact(rel, text):
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO,
                          input=text.encode("utf-8"), capture_output=True)
    if blob.returncode != 0:
        raise SystemExit("FATAL hash-object 失败")
    b = blob.stdout.decode().strip()
    p = subprocess.run(["git", "update-index", "--cacheinfo", "100644," + b + "," + rel],
                       cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("FATAL update-index 失败: " + p.stderr.decode("utf-8", "replace")[:200])
    return b


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-stage", action="store_true")
    args = ap.parse_args()

    for rel, fn in TARGETS:
        path = os.path.join(REPO, rel.replace("/", os.sep))
        t, nl = read(path)
        new = fn(t)
        if new != t:
            if not args.dry_run:
                write(path, new, nl)
            print("工作树已更新  %s" % rel)
        else:
            print("工作树无变化  %s" % rel)
        if args.dry_run or args.no_stage:
            continue
        head = git_show(rel)
        if head is None:
            print("  跳过（HEAD 无此文件）：%s" % rel)
            continue
        head_new = fn(head)
        if head_new == head:
            print("  HEAD 基底下无新增 → 跳过暂存：%s" % rel)
            continue
        blob = stage_exact(rel, head_new)
        print("  精确暂存 %s（blob %s·只含本批改动）" % (rel, blob[:8]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
