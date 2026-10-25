#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w931_file_index_seg.py — 在 scripts/output/file-index.md 补 W931 段登记

背景：W932 批收官时本批的 CHANGELOG 段与对账表认领行随其提交入库，但 file-index 段未含 W931
  ⇒ 第「索引健康」门禁报「file-index 缺 1 个 CHANGELOG 版段登记：['W931']」。
  按 W932 批书面告知「file-index 缺 W931 段请直接按段格式补入」执行。

纪律：
  · 段序降序（插在 W932 段之后）；只插入，不改既有段字符；
  · 幂等：W931 段已存在则直接退出；
  · 结构断言：插入后各 W 段号序列保持非递增。

用法：py -3 scripts/_w931_file_index_seg.py [--dry-run]
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FI = REPO / "scripts" / "output" / "file-index.md"

BATCH_NO = "W931"

ROWS = [
    ("assets/promo/hero-set/hero-line-01-ruyi-staff.png", "成品母版 2400×1017·如意金箍棒（黑铁杆 + 赭金云纹端头）·左侧 46% 留白"),
    ("assets/promo/hero-set/hero-line-02-journey-scroll.png", "成品母版 2400×1017·行程图卷轴（山路 / 路线 / 河曲）"),
    ("assets/promo/hero-set/hero-line-03-classic-scroll.png", "成品母版 2400×1017·经卷 + 篆香（竖行纹理非可读文字）"),
    ("assets/promo/hero-set/hero-line-04-sinan-compass.png", "成品母版 2400×1017·司南（铜盘回纹刻度 + 匙柄）"),
    ("assets/promo/hero-set/hero-line-05-lotus.png", "成品母版 2400×1017·莲花（层瓣线描 + 赭金叶脉）"),
    ("assets/promo/hero-set/hero-line-06-nine-ring-staff.png", "成品母版 2400×1017·九环锡杖（赭金环 + 白杆）"),
    ("assets/promo/hero-set/hero-line-07-banana-fan.png", "成品母版 2400×1017·芭蕉扇（线描叶脉 + 纸色透出·第二版·首版黑色实心块已废弃）"),
    ("assets/promo/hero-set/hero-line-08-jade-vase.png", "成品母版 2400×1017·玉净瓶（白瓷瓶 + 柳枝）"),
    ("assets/promo/hero-set/hero-line-01-ruyi-staff.webp", "站点用 WebP q90（8 张全套同规格）"),
    ("assets/promo/hero-set/hero-line-02-journey-scroll.webp", "站点用 WebP q90"),
    ("assets/promo/hero-set/hero-line-03-classic-scroll.webp", "站点用 WebP q90"),
    ("assets/promo/hero-set/hero-line-04-sinan-compass.webp", "站点用 WebP q90"),
    ("assets/promo/hero-set/hero-line-05-lotus.webp", "站点用 WebP q90"),
    ("assets/promo/hero-set/hero-line-06-nine-ring-staff.webp", "站点用 WebP q90"),
    ("assets/promo/hero-set/hero-line-07-banana-fan.webp", "站点用 WebP q90"),
    ("assets/promo/hero-set/hero-line-08-jade-vase.webp", "站点用 WebP q90"),
    ("assets/promo/hero-set/preview-contact-sheet.png", "成套一览拼图 2×4（8 张缩略·一眼验一致性）"),
    ("assets/promo/hero-set/preview-contact-sheet.webp", "成套一览拼图 WebP"),
    ("assets/promo/hero-set/raw/hero-01-ruyi-staff.jpg", "出图原件 3168×1344（重出基准·模型不可复现）"),
    ("assets/promo/hero-set/raw/hero-02-journey-scroll.jpg", "出图原件 3168×1344"),
    ("assets/promo/hero-set/raw/hero-03-classic-scroll.jpg", "出图原件 3168×1344"),
    ("assets/promo/hero-set/raw/hero-04-sinan-compass.jpg", "出图原件 3168×1344"),
    ("assets/promo/hero-set/raw/hero-05-lotus.jpg", "出图原件 3168×1344"),
    ("assets/promo/hero-set/raw/hero-06-nine-ring-staff.jpg", "出图原件 3168×1344"),
    ("assets/promo/hero-set/raw/hero-07-banana-fan.jpg", "出图原件 3168×1344（第二版）"),
    ("assets/promo/hero-set/raw/hero-08-jade-vase.jpg", "出图原件 3168×1344"),
    ("assets/promo/hero-set/README.md", "目录导读（规格 / 接入方法 / 维护约定 / 已知取舍）"),
    ("assets/promo/hero-set/index.md", "目录文件索引（生成器产物）"),
    ("assets/promo/hero-set/raw/README.md", "出图原件目录导读（含废弃首版留证）"),
    ("assets/promo/hero-set/raw/index.md", "出图原件目录文件索引（生成器产物）"),
    ("assets/promo/index.md", "上级目录索引刷新（新增 hero-set 子目录登记）"),
    ("STRUCTURE.md", "promo 段登记行（promo/hero-set/ 目录用途）"),
    ("docs/00-导读/W批次编号对账表.md", "W931 认领行（取号依据 + touches 声明）"),
    ("CHANGELOG.md", "W931 版段（四件套·来源 / 文件 / 验证 / 状态）"),
    ("scripts/_w931_hero_verify.py", "成套判据脚本（7 条 J1–J7 + 负样本可证伪自检）"),
    ("scripts/_w931_claim_row.py", "对账表认领行登记脚本（幂等·绝不覆盖他人认领）"),
    ("scripts/_w931_changelog_seg.py", "CHANGELOG 段插入脚本（段序结构断言 + 让号后重定位）"),
]

SEG = (
    "## W931 首页 Hero 横幅素材图成套批·线描版 8 张（2026-10-25）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    + "".join("| " + f + " | W931 | " + d + " |\n" for f, d in ROWS)
    + "\n"
)

RE_SEG = re.compile(r"^## (W\d+) ", re.M)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    raw = io.open(FI, "rb").read().decode("utf-8")
    nl = "\r\n" if b"\r\n" in raw.encode("utf-8") else "\n"
    text = raw.replace("\r\n", "\n")

    if re.search(r"^## " + BATCH_NO + r" ", text, re.M):
        print(BATCH_NO + " file-index 段已存在，幂等退出")
        return 0

    target = int(BATCH_NO[1:])
    pos = None
    for m in RE_SEG.finditer(text):
        n = int(m.group(1)[1:])
        if n < target:
            pos = m.start()
            break
    if pos is None:
        print("FATAL: 未找到可插入锚点（file-index 段序异常）")
        return 2

    new_text = text[:pos] + SEG + text[pos:]
    nums = [int(m.group(1)[1:]) for m in RE_SEG.finditer(new_text)]
    bad = [(nums[i], nums[i + 1]) for i in range(len(nums) - 1) if nums[i] < nums[i + 1]]
    if bad:
        print("FATAL: 插入后段序非降序（" + str(bad[:3]) + "）· 回滚不落盘")
        return 2
    if nums.count(target) != 1:
        print("FATAL: 目标段号出现次数异常 · 回滚不落盘")
        return 2

    if args.dry_run:
        print("DRY: 将插入 W931 段于偏移 " + str(pos) + "·段序前 6 = " + str(nums[:6]))
        return 0

    io.open(FI, "w", encoding="utf-8", newline=nl).write(new_text)
    print(BATCH_NO + " file-index 段已插入（偏移 " + str(pos) + "·段序前 6 = " + str(nums[:6]) + "）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
