#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w974_cascade.py — W974 四面登记 + 当前态指针（内页题图成套批·第三组·12 张）

并发纪律：共享面**不整份 add**，改为**按内容粒度精确暂存**（HEAD 基底 + 本批段·
`git update-index --cacheinfo`）⇒ 对方在途内容既不入我的提交、也不被我抹掉。

文件清单由**目录实扫 + 常量表**程序化生成（不手写通配符）——手写路径 token 若不在提交树会被门禁判红。

用法：python scripts/_w974_cascade.py [--dry-run]
"""
import argparse
import io
import os
import re
import subprocess
import sys

REPO = r"D:\xiyouji"
BATCH = "W974"
LEDGER_REL = "docs/00-导读/W批次编号对账表.md"
CHANGELOG_REL = "CHANGELOG.md"
FILE_INDEX_REL = "scripts/output/file-index.md"
README_REL = "README.md"
HANDOVER_REL = "HANDOVER.md"
CITATION_REL = "CITATION.cff"

# (stem, 主体, 落位页相对路径, 类别)
PLATES = [
    ("13-jinjiaodawang", "金角大王", "site/reader/people/金角银角深化专题.html", "人物"),
    ("14-yinjiaodawang", "银角大王", "site/reader/people/银角大王.html", "人物"),
    ("15-huangmeidawang", "黄眉大王", "site/reader/people/黄眉老佛外传.html", "人物"),
    ("16-heixiongjing", "黑熊精", "site/reader/people/黑熊精.html", "人物"),
    ("17-tuota-lijing", "托塔李靖", "site/reader/people/托塔李天王外传.html", "人物"),
    ("18-yutujing", "玉兔精", "site/reader/people/玉兔精.html", "人物"),
    ("19-nvziguo-topic", "女儿国主题", "site/reader/people/女儿国国王.html", "主题"),
    ("20-chelingguo-topic", "车迟国斗法主题", "site/reader/people/车迟国三国师外传.html", "主题"),
    ("21-shituoling-topic", "狮驼岭主题", "site/reader/people/狮驼岭三魔-方向二深化.html", "主题"),
    ("22-tonghehe-topic", "通天河主题", "site/reader/people/老鼋外传.html", "主题"),
    ("23-pansidong-topic", "盘丝洞主题", "site/reader/people/蜘蛛精.html", "主题"),
    ("24-wudidong-topic", "无底洞主题", "site/reader/people/老鼠精.html", "主题"),
]

SCRIPTS = [
    "scripts/_w974_claim_row.py", "scripts/_w974_make_prompts.py", "scripts/_w974_make_retry.py",
    "scripts/_w974_merge_retry.py", "scripts/_w974_download.py", "scripts/_w974_prepare.py",
    "scripts/_w974_zoom.py", "scripts/_w974_sheet_full.py", "scripts/_w974_insert_plates.py",
    "scripts/_w974_stats.py", "scripts/_w974_update_readme.py", "scripts/_w974_probe_top.py",
    "scripts/_w974_probe_top2.py", "scripts/_w974_probe_clusters.py", "scripts/_w974_probe_subjtop.py",
    "scripts/_w974_negative_sample.py", "scripts/_w974_cascade.py", "scripts/_w974_backfill_stage.py",
    "scripts/_w974_final_check.py", "scripts/_w974_register_report.py",
    "scripts/_w974_sync_stats_marks.py", "scripts/_w974_sync_version_faces.py",
]
BATCH_OUTPUTS = ["scripts/output/_w974_batch1.json", "scripts/output/_w974_batch2.json",
                 "scripts/output/_w974_batch3.json", "scripts/output/_w974_batch34.json",
                 "scripts/output/_w974_retry15.json", "scripts/output/_w974_stats.json",
                 "scripts/output/_w974_negative_sample.png", "scripts/output/_w974_probe_top_zoom.png",
                 "scripts/output/_w974_urls_a.json", "scripts/output/_w974_urls_b.json",
                 "scripts/output/_w974_urls_c.json"]
DOCS = [
    "docs/11-方案报告/计划方案/执行前计划-T29-内页题图成套批第三组.md",
    "docs/11-方案报告/计划方案/T29-任务计划执行与经验沉淀报告-2026-10-27.md",
]
EXTRA = [
    "assets/promo/plate-set/README.md", "assets/promo/plate-set/index.md",
    "assets/promo/plate-set/preview-contact-sheet.png",
    "assets/promo/plate-set/preview-contact-sheet.webp",
    "scripts/output/_cascade_files_W974.txt", "scripts/output/file-index.md",
    "CHANGELOG.md", "README.md", "HANDOVER.md", LEDGER_REL,
    "docs/11-方案报告/README.md",
]

# 目录条目（级联面）——**展开为具体文件路径**：
# 第 31 门禁 C4-e 判据 = 「HEAD 树 ∪ staged ⊇ 当批 _cascade_files 清单」，逐行做**确切路径**比对
# ⇒ 清单里写目录路径（带尾斜杠）永远不在文件集合里 ⇒ 必然判红（本批实证）。
EXPAND_DIRS = [
    "assets/promo/plate-set/zoom-w974",
    "assets/promo/plate-set/raw/round11",
]

SITE_FILES = ["site/static/images/plate-line-%s.webp" % s for s, _n, _p, _c in PLATES]
MASTER_FILES = ([os.path.join("assets", "promo", "plate-set", "plate-line-%s.png" % s).replace("\\", "/") for s, _n, _p, _c in PLATES]
                + [os.path.join("assets", "promo", "plate-set", "plate-line-%s.webp" % s).replace("\\", "/") for s, _n, _p, _c in PLATES])
PAGE_FILES = [p for _s, _n, p, _c in PLATES]
FILE_LIST = SITE_FILES + MASTER_FILES + PAGE_FILES + SCRIPTS + BATCH_OUTPUTS + DOCS + EXTRA

# 展开目录条目为具体文件（门禁 C4-e 要求清单每行都是确切路径）
_expanded = []
for _d in EXPAND_DIRS:
    _abs = os.path.join(REPO, _d.replace("/", os.sep))
    if not os.path.isdir(_abs):
        raise SystemExit("FATAL 目录不存在：%s" % _d)
    for _root, _dirs, _files in os.walk(_abs):
        for _f in sorted(_files):
            _p = os.path.join(_root, _f)
            _expanded.append(os.path.relpath(_p, REPO).replace("\\", "/"))
_expanded.sort()
FILE_LIST += _expanded

FILE_LINE = "> - **文件**：" + "、".join(FILE_LIST)

CHANGELOG_SEG = """### W974（2026-10-27）：内页题图成套批·第三组（12 张·人物 6 + 主题 6·站内线描题图累计 52 张）

> **来源**：用户 2026-10-27 令「帮我做几张素材图：用途与画幅、风格与配色统一、主体清晰、留好放文字的空间都考虑到，成套出图保证风格一致」，并明文要求「开始前先问我：素材用在哪里、需要几张、有没有参考风格」。
>
> **四问答复**：① 用途与画幅 = **内页题图 · 3:4 竖版 1200×1600（沿用 plate-set 母版）** ② 张数 = **12 张** ③ 参考风格 = **沿用站内线描墨稿风（母版逐字复用）** ④ 题材范围 = **人物 + 主题混合（各占一半）**。

%s

**母版逐字复用**：直接读 W953 的 `_w953_batch1.json` 取母版（**249 字符**）拼本批 SUBJECT 段 ⇒ 跨三批（W952 / W953 / W974）风格同族由**构造**保证；脚本断言「批内 12 条母版逐字一致」+「与 W953 母版逐字相同」+「stem 与既有母版零冲突（含负样本自证）」。

**出图与返工**：首轮 batch1 **3/4 成功**（04 黑熊精 err_code 451「The result is unavailable」⇒ 补出）；**选题调整 1 处**——原定「虎力大仙」在 people 库无独立页面（只有「车迟国三国师」页）⇒ 改为**玉兔精**（有独立页且无题图），原图弃用；**重出 1 张**——人眼放大复核抓出 **15 黄眉大王的金铙被画成圆环**（读作手镯）⇒ 改措辞为「倒扣的金钵 · 半圆盘 · 钵面一圈回纹 · 绝不是圆环或手镯」后达标。

**站点版「主体顶」抗噪口径修正（本批实质工程贡献）**：现行 `ink_top()` 取**整图墨迹 bbox 顶**，会被**孤立噪点**污染——实测 `plate-line-24-wudidong-topic` 顶部第 18 行仅 **3 个像素**（差值 41），放大取证显示 0–260 px 为纯宣纸底、零主体笔触 ⇒ 裁切线失真（站点版 1588 px ≈ 母版高）。⇒ 改为「**主体顶 = 面积 ≥ 200 px² 的墨迹连通簇的最小顶**」（滤孤立噪点、保留真实稀疏顶部如冠尖）。全目录 52 张复算：两种口径**仅 4 张不同**（本批 24 号 +419 px；既有 03 大闹天宫 +188 / 05 混世四猴 +113 / 11 金箍棒重量 +4 px）⇒ 既有 3 张属**存量欠账**（需人眼判定后再处置），本批**不重写既有资产**。

**判据可证伪性**：合成多维负样本（1200×1600·下部纯黑块 + 四边 6 px 贯穿暗框 + 左侧 300 px 纯白竖带）⇒ 同一判据**同时抓出 J2 / J3 / J6 / J8** 四条；J10 另经独立探针实测 9.333 > 阈值 5.0 ⇒ 可证伪。

**接入**：沿用站内 `chapter-plate` 范式（420 px 居中 + 描述性 alt + 浅底图暗色模式隐藏），幂等脚本 `_w974_insert_plates.py`；**浏览器实跑 2 页**（黑熊精 / 车迟国三国师）确认标题紧贴主体、无冗余留白、宣纸底与页面底色无色边、console 0 错误。

**并发纪律**：共享面按内容粒度**精确暂存**（`git update-index --cacheinfo`·HEAD 为基底叠加本批段）⇒ 不把对方在途内容带进本批提交。

> - **验证**：（见本批脚本输出与对账表回填）
> - **状态**：在途（认领登记 W974·待提交入库）

""" % FILE_LINE

FILE_INDEX_SEG = (
    "## W974 内页题图成套批·第三组（12 张）（2026-10-27）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    + "".join("| site/static/images/plate-line-%s.webp | W974 | 新增·%s（%s） |\n" % (s, n, c) for s, n, _p, c in PLATES)
    + "".join("| %s | W974 | 接入题图（%s） |\n" % (p, n) for _s, n, p, _c in PLATES)
    + "| assets/promo/plate-set/plate-line-13~24-*.png/.webp | W974 | 新增 12 张母版（1200×1600·线描墨稿） |\n"
    "| assets/promo/plate-set/raw/round11/ | W974 | 出图原件 12 份（含 15 号两次重出的生效件） |\n"
    "| assets/promo/plate-set/zoom-w974/ | W974 | 人眼放大复核图（12 张主体区全图 + 12 张局部放大 + 分组拼图） |\n"
    "| assets/promo/plate-set/README.md | W974 | 口径更新（40→52 张·第五组清单·抗噪口径·已知取舍） |\n"
    "| scripts/_w974_prepare.py | W974 | 本批专用成品处理（**主体顶抗噪口径**·只处理 raw/round11·不重写既有 40 张） |\n"
    "| scripts/_w974_make_prompts.py | W974 | 母版复用生成器（读 W953 JSON·三条断言 + 冲突检查负样本自证） |\n"
    "| scripts/_w974_insert_plates.py | W974 | 12 页 chapter-plate 接入（幂等） |\n"
    "| scripts/_w974_probe_subjtop.py | W974 | bbox 顶 vs 主体顶 全目录 52 张口径对比探针 |\n"
    "| scripts/_w974_negative_sample.py | W974 | 多维负样本合成器（J2/J3/J6/J8 四条可证伪） |\n"
    "| scripts/_w974_stats.py | W974 | 实测汇总（数字唯一源头·README 数字程序化回填） |\n"
    "| scripts/output/_w974_stats.json | W974 | 实测统计产物 |\n"
    "| scripts/output/_cascade_files_W974.txt | W974 | 当批级联清单 |\n"
    "| CHANGELOG.md | W974 | W974 版段 |\n"
    "| docs/00-导读/W批次编号对账表.md | W974 | W974 认领行 |\n"
    "\n"
)

README_LINE = ("> **当前批次 W974（2026-10-27）**：内页题图成套批第三组（十二张线描题图、人物 6 + 主题 6、"
               "站内累计 52 张、reader 有题图页 51→63）·A1-A6<!--doc-sync:exempt-->")

HANDOVER_LINE = (
    "> 最后更新：2026-10-27（W974 内页题图成套批·第三组）·2026-10-26（W973 HANDOVER 五区清理批）·"
    "2026-10-26（W972 CodeQL 三高危修复批）·（W449-W549 及更早批次详见 CHANGELOG.md）"
)

HANDOVER_PROGRESS = (
    "## 一、当前进度（W974 内页题图成套批·第三组；更早批次详见 CHANGELOG.md）\n"
    "- **W974 内页题图成套批·第三组**：再出 12 张线描题图（人物 6：金角大王/银角大王/黄眉大王/黑熊精/"
    "托塔李靖/玉兔精 + 主题 6：女儿国/车迟国斗法/狮驼岭/通天河/盘丝洞/无底洞），接入 12 个 people 库页 ⇒ "
    "站内线描题图累计 52 张、reader 有题图页 63/622；母版 249 字符从 W953 JSON 逐字复用；"
    "同批修正站点版「主体顶」抗噪口径（bbox 顶会被孤立噪点污染）。\n"
)


def t_ledger(t):
    if re.search(r"^\| " + BATCH + r" \|", t, re.M):
        return t
    return t  # 认领行由 scripts/_w974_claim_row.py 负责（字节级追加）


def t_changelog(t):
    if re.search(r"^### " + BATCH + r"（", t, re.M):
        # 已有段 ⇒ 刷新该段的「> - **文件**：」行（清单与提交树保持一致·门禁 C4-f 按清单核对提交树）
        lines = t.split("\n")
        in_seg = False
        for i, ln in enumerate(lines):
            if ln.startswith("### " + BATCH + "（"):
                in_seg = True
                continue
            if in_seg and ln.startswith("> - **文件**："):
                lines[i] = FILE_LINE
                break
            if in_seg and ln.startswith("### "):
                break
        return "\n".join(lines)
    m = re.search(r"^### W\d+", t, re.M)
    pos = m.start() if m else len(t)
    t = t[:pos] + CHANGELOG_SEG + t[pos:]
    t = re.sub(r"（W001-W\d+）", "（W001-W974）", t, count=1)
    return t


def t_file_index(t):
    if re.search(r"^## " + BATCH + r" ", t, re.M):
        return t
    m = re.search(r"^## W\d+", t, re.M)
    pos = m.start() if m else len(t)
    return t[:pos] + FILE_INDEX_SEG + t[pos:]


def t_readme(t):
    return re.sub(r"> \*\*当前批次 W\d+（\d{4}-\d{2}-\d{2}）\*\*：[^\n]*", README_LINE, t, count=1)


def t_handover(t):
    """幂等改写（⚠️ W974 修正：初版非幂等——`re.sub("## 一、当前进度（W\\d+...")` 会匹配**自己刚插入的标题行**
    ⇒ 每跑一次 cascade 就多插一份本批条目（实测插了 3 份）。
    ⇒ 改为逐行处理：① 丢弃已有的本批条目行 ② 用本批段落替换「一、当前进度」标题行。"""
    lines = t.split("\n")
    out = []
    for ln in lines:
        if ln.startswith("- **W974 "):
            continue                      # 幂等：移除本批旧条目行
        if ln.startswith("## 一、当前进度（W"):
            out.extend(HANDOVER_PROGRESS.rstrip("\n").split("\n"))
            continue                      # 替换标题行（连带插入本批条目）
        out.append(ln)
    t = "\n".join(out)
    t = re.sub(r"> 最后更新：\d{4}-\d{2}-\d{2}[^\n]*", HANDOVER_LINE, t, count=1)
    # 「当前 HEAD = W###（…）」治理契约字段（W711 形态·须与 CHANGELOG 最新段一致）
    t = re.sub(r"当前 HEAD = (?:v[\d.]+\s+)?W\d+（[^）]*）",
               "当前 HEAD = W974（内页题图成套批·第三组）", t, count=1)
    t = re.sub(r"每次完成新 W### 后更新。最后更新：[^\n]*",
               "每次完成新 W### 后更新。最后更新：2026-10-27（W974 内页题图成套批·第三组）", t, count=1)
    return t


def t_citation(t):
    """CITATION.cff 的批次号形态 version（W711 方案 D·非 SemVer）——只改第一个 version 字段"""
    return re.sub(r'(?m)^version: "W\d+"', 'version: "W974"', t, count=1)


TARGETS = [
    (LEDGER_REL, t_ledger),
    (CHANGELOG_REL, t_changelog),
    (FILE_INDEX_REL, t_file_index),
    (README_REL, t_readme),
    (HANDOVER_REL, t_handover),
    (CITATION_REL, t_citation),
]


def read(p):
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def write_atomic(p, t, nl):
    data = t.replace("\n", nl).encode("utf-8")
    tmp = p + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, p)


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

    # 级联清单落盘（供门禁核对）
    os.makedirs(os.path.join(REPO, "scripts", "output"), exist_ok=True)
    cl = os.path.join(REPO, "scripts", "output", "_cascade_files_W974.txt")
    with io.open(cl, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(FILE_LIST) + "\n")
    print("级联清单：scripts/output/_cascade_files_W974.txt（%d 项）" % len(FILE_LIST))

    for rel, fn in TARGETS:
        path = os.path.join(REPO, rel.replace("/", os.sep))
        t, nl = read(path)
        new = fn(t)
        if new != t:
            if not args.dry_run:
                write_atomic(path, new, nl)
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
