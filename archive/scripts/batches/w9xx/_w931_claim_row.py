#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w931_claim_row.py — 在 W 批次编号对账表主表登记 W931 认领行

纪律（沿用 W930 批先例 · scripts/_w930_claim_row.py）：
  · 追加行用表格行追加，禁改历史行；
  · 插入位置 = W930 行之后（号序相邻），避免打乱既有升序；
  · 文件读写一律 io.open(encoding='utf-8')，禁 PowerShell Set-Content（会写 UTF-8 BOM）；
  · 「关联 commit」「CHANGELOG 版段」两列施工后回填，先占位；
  · 幂等：若该号已有行则直接退出，**绝不覆盖他人已认领的号**；
  · 撞号防线：若 W931 已被他方认领（行存在但认领会话不是本批）则退出并报错，不覆盖。

用法：py -3 scripts/_w931_claim_row.py
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TABLE = REPO / "docs" / "00-导读" / "W批次编号对账表.md"

BATCH_NO = "W931"
PREV_NO = "W930"

ROW = (
    "| W931 | Hero 横幅素材图成套批·线描版（用户 2026-10-25 令「帮我做几张素材图：用途与画幅、风格与配色统一、"
    "主体清晰、留好放文字的空间都考虑到，成套出图保证风格一致」+ 明文要求「开始前先问我：素材用在哪里、需要几张、"
    "有没有参考风格」；问卷答复 = 首页 Hero 横幅 **2400×1017** · **8 张** · 沿用 assets/design/ai-concepts/ 的 "
    "c2 线描概念图 + 现有色板）：① **风格母版统一**——8 张共用同一条逐字风格母版（宣纸 #FAF7F0 / 墨 #23201A / "
    "赭金 #8A6D3B / 单点朱砂 #C8463A + 纯墨线无实心填充 + 禁文字禁印章禁水印 + 左侧 46% 纯留白），只换 SUBJECT 与 "
    "POSITION 段⇒成套一致性由「同 prompt 母版」保证而非事后拼凑；② **留白硬判据**——左侧 46% 文字安全区墨量实测 "
    "**0.0000–0.0014**（8/8 张达标）·主体墨量落在右半区（整图 2.11%–8.11%）；③ **一处返工留证**——07 芭蕉扇"
    "首版扇面被画成黑色实心块（主体墨量 26.2%·与其余 7 张 3%~8% 断层）⇒ 判定破套并**重出**，复测 7.72% 回到套内；"
    "④ **AI 伪文字人工放大复核**——04 司南盘面字符状符号放大 2× 验明为回纹刻纹非乱码·06 九环锡杖同验（机器判据"
    "抓不到伪文字·只能放大看）；⑤ **落位**——新目录 assets/promo/hero-set/（8×png + 8×webp + 成套一览拼图 + "
    "8 张出图原件 raw/ + README/index ×2）·站点接入需先复制到 site/static/images/（Pages 只发布 site/）·"
    "接入方法写在同目录 README（背景图 + background-position: right center 保住「主体在右·文字在左」版面约定）；"
    "⑥ **与并行 W932 素材批零重叠**——W932（渲染型浓墨剪影 hero-10~15 · 2560×1440 · 落 site/static/images/）"
    "与本批（线描 hero-line-01~08 · 2400×1017 · 落 assets/promo/hero-set/）路径不重叠·各自 README 写接入方法·"
    "站点接入统一交由用户决定·双方均不改 site/index.html | —（待回填） | —（待回填） | "
    "在途（认领·未收官） | 并行 Agent 会话 2026-10-25（素材图成套批 · 线描版） | "
    "`assets/promo/hero-set/**`（新增 32 件·含 raw/ 8 件）· `assets/promo/index.md`（目录生成器刷新）· "
    "`STRUCTURE.md`（promo 段登记行）· `CHANGELOG.md`（W931 版段）· `docs/00-导读/W批次编号对账表.md`（本行）· "
    "`scripts/_w931_claim_row.py` / `_w931_changelog_seg.py` / `_w931_hero_verify.py`（本批脚本） |"
)


def main() -> int:
    text = io.open(TABLE, encoding="utf-8").read()
    if re.search(r"^\| " + BATCH_NO + r" \|", text, re.M):
        print(BATCH_NO + " 认领行已存在，幂等退出（不重复插入、不覆盖他人认领）")
        return 0
    lines = text.split("\n")
    idx = None
    for i, ln in enumerate(lines):
        if ln.startswith("| " + PREV_NO + " |"):
            idx = i
            break
    if idx is None:
        print("FATAL: 未找到 " + PREV_NO + " 行，拒绝盲目插入")
        return 2
    lines.insert(idx + 1, ROW)
    io.open(TABLE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(BATCH_NO + " 认领行已插入（表内第 " + str(idx + 2) + " 行）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
