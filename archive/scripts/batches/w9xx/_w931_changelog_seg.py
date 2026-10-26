#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w931_changelog_seg.py — 在 CHANGELOG.md 插入 W931 版段

纪律（CHANGELOG 维护契约 ②「新版本段插入/重排只用脚本 + 结构断言（锚点唯一性 + 版段 order 校验）」）：
  · 插入位置 = 「第一个段号小于 W931 的段」之前 —— 无论 W929/W930 段是否已立，段序都保持降序；
  · 只插入，不改任何既有段字符（历史段禁改）；
  · 结构断言：插入后全文件段号序列必须严格非递增，否则回滚不落盘；
  · 幂等：W931 段已存在则直接退出。

用法：py -3 scripts/_w931_changelog_seg.py [--dry-run]
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHANGELOG = REPO / "CHANGELOG.md"

BATCH_NO = "W931"

SEG = """### W931（2026-10-25）：首页 Hero 横幅素材图成套批（线描版 8 张 · 2400×1017 · 左半留白供叠字）

> **来源**：用户 2026-10-25 令「帮我做几张素材图：用途与画幅、风格与配色统一、主体清晰、留好放文字的空间都考虑到，成套出图保证风格一致」+ 明文要求「开始前先问我：素材用在哪里、需要几张、有没有参考风格」；问卷答复 = 首页 Hero 横幅 **2400×1017** · **8 张** · 沿用 `assets/design/ai-concepts/` 的 c2 线描概念图 + 现有色板。

> - **文件**：assets/promo/hero-set/hero-line-01~08.{png,webp}、assets/promo/hero-set/preview-contact-sheet.{png,webp}、assets/promo/hero-set/raw/hero-0X-*.jpg、assets/promo/hero-set/README.md、assets/promo/hero-set/index.md、assets/promo/hero-set/raw/README.md、assets/promo/hero-set/raw/index.md、assets/promo/index.md、STRUCTURE.md

**规格与机器判据**：8 张共用同一条逐字风格母版（宣纸 `#FAF7F0` · 墨 `#23201A` · 赭金 `#8A6D3B` · 单点朱砂 `#C8463A` + 纯墨线无实心填充 + 禁文字禁印章禁水印 + 左侧 46% 纯留白）⇒ 成套一致性由「同母版」保证。画幅 `2400×1017`（`21:9` 出图后按 `2400/1017` 精确裁切·不拉伸）；**左侧 46% 文字安全区墨量实测 0.0000–0.0014（8/8 达标）**·主体墨量落右半区（整图 2.11%–8.11%）。

**一处返工留证**：07 芭蕉扇首版扇面被画成**黑色实心块**（主体墨量 26.2%·与其余 7 张 3%~8% 断层）⇒ 判破套并重出，复测 7.72% 回到套内；**AI 伪文字人工放大 2× 复核**（04 司南盘面字符状符号验明为回纹刻纹非乱码·06 九环锡杖同验）——机器判据抓不到伪文字，只能放大看。

**落位与接入**：新目录 `assets/promo/hero-set/`（8×PNG 母版 + 8×WebP 站点版 + 成套一览拼图 + 8 张出图原件 `raw/` + README/index ×2）·站点 Pages 只发布 `site/`，接入前须复制到 `site/static/images/`，方法写在该目录 README（背景图 + `background-position: right center` 保住「主体在右·文字在左」版面约定）·**未改 `site/index.html`**。与并行 **W932** 素材批（渲染型浓墨剪影 `hero-10~15` · 2560×1440 · 落 `site/static/images/`）路径零重叠，两套视觉语言并存、接入由用户决定。

> - **验证**：8/8 出图成功（批量 `generate_image` 零失败）·2400×1017 尺寸 8/8 实测一致 ·左侧留白区墨量 0.0000–0.0014（8/8 达标）·AI 伪文字人工放大复核 2 张（04/06）·成套一览拼图逐张目视复核全过
> - **状态**：在途（素材已落盘并暂存·认领登记 W931·站点接入待用户决定）

"""

RE_SEG = re.compile(r"^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（[^）]*）：)", re.M)


def seg_nums(text: str) -> list[int]:
    return [int(m.group(1) or m.group(2)) for m in RE_SEG.finditer(text)]


def remove_existing(text: str) -> tuple[str, bool]:
    """移除已存在的 W931 段（含段正文到下一个 '### ' 段标题之前）——用于段序重定位。"""
    m = re.search(r"^### " + BATCH_NO + r"（[^\n]*\n", text, re.M)
    if not m:
        return text, False
    nxt = re.search(r"^### ", text[m.end():], re.M)
    end = m.end() + nxt.start() if nxt else len(text)
    return text[:m.start()] + text[end:], True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--reposition", action="store_true",
                    help="移除已插入的 W931 段并按当前段序重新插入（用于让号后段序纠偏）")
    args = ap.parse_args()

    raw = io.open(CHANGELOG, "rb").read().decode("utf-8")
    nl = "\r\n" if b"\r\n" in raw.encode("utf-8") else "\n"
    text = raw.replace("\r\n", "\n")

    if re.search(r"^### " + BATCH_NO + r"（", text, re.M):
        if not args.reposition:
            print(BATCH_NO + " 版段已存在，幂等退出（需重定位请加 --reposition）")
            return 0
        text, removed = remove_existing(text)
        print(BATCH_NO + " 已存在段已移除（重定位模式）·removed=" + str(removed))

    nums = seg_nums(text)
    if not nums:
        print("FATAL: 未识别到任何版段，拒绝插入")
        return 2

    # 插入点 = 第一个「段号 < BATCH_NO」的段之前；无则插到最后一个段之后
    target = int(BATCH_NO[1:])
    pos = None
    for m in RE_SEG.finditer(text):
        n = int(m.group(1) or m.group(2))
        if n < target:
            pos = m.start()
            break
    if pos is None:
        # 插到最后一个段之后
        last = list(RE_SEG.finditer(text))[-1]
        pos = last.end()
        seg_text = "\n" + SEG
    else:
        seg_text = SEG

    new_text = text[:pos] + seg_text + text[pos:]

    # 结构断言：段号序列必须严格非递增（降序）
    new_nums = seg_nums(new_text)
    bad = [(new_nums[i], new_nums[i + 1]) for i in range(len(new_nums) - 1) if new_nums[i] < new_nums[i + 1]]
    if bad:
        print("FATAL: 插入后段序非降序（" + str(bad[:3]) + "）· 回滚不落盘")
        return 2
    if new_nums.count(target) != 1:
        print("FATAL: 目标段号出现次数异常 · 回滚不落盘")
        return 2

    if args.dry_run:
        print("DRY: 将插入 " + BATCH_NO + " 段于偏移 " + str(pos) + "·插入后段序前 6 = " + str(new_nums[:6]))
        return 0

    io.open(CHANGELOG, "w", encoding="utf-8", newline=nl).write(new_text)
    print(BATCH_NO + " 版段已插入（偏移 " + str(pos) + "·段序前 6 = " + str(new_nums[:6]) + "）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
