#!/usr/bin/env python3
"""_w929_ledger_spec.py — W929→W931 让号改号（W895 缺口机制·让号先例族 W907/W908/W910/W911）。

背景：施工期间并行「界面布局复核批」先落地并立 W930 段 ⇒ 本会话早先认领的 W929 成为
在途缺口（台账有行、CHANGELOG 无段）⇒ 按「先落地者保留」让号，本批最终取 W931。
让号行在 CHANGELOG 不落段（与 W907/W908/W910/W911 同族）。

用法：py -3 scripts/_w929_ledger_spec.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md")
SPEC_OLD = os.path.join(ROOT, "scripts", "output", "_w929_spec.json")
SPEC_NEW = os.path.join(ROOT, "scripts", "output", "_w932_spec.json")

GIVEUP_LINE = (
    "| W929 | **让号登记行**（编号空间字典：W 号单调永不复用·跳号须登记）——本号先由本会话认领"
    "（站点 Hero 素材图成套批·用户 2026-10-25 令「帮我做几张素材图」·开工前三问=用途与画幅 / "
    "数量 / 参考风格），施工期间并行「界面布局复核批」先落地并立 W930 段、并行「Hero 横幅素材图"
    "成套批·线描版」认领 W931 ⇒ 按「先落地者保留」两次让号，本批最终取 W932；W929 永久无 "
    "CHANGELOG 段（与 W907/W908/W910/W911 同族让号先例） "
    "| —（让号留痕） | —（无段·跳号） | **已收官**（让号留痕·本批最终取 W932） | 主会话 2026-10-25 | — |"
)

CLAIM_LINE = (
    "| W932 | 站点 Hero 素材图成套批（用户 2026-10-25 令「帮我做几张素材图」·开工前三问=用途与画幅 / "
    "数量 / 参考风格；问卷答复 = 站点 Hero 横幅 16:9 · 6 张 · 沿用 assets/promo/hero-main-visual.png "
    "主视觉（宣纸底浓墨剪影 + 朱砂钤记）· 四类主题全覆盖）：① **锚点**：复用 W852→W893 成熟 "
    "art direction 段（宣纸 #FAF7F0 / 玄墨 #221D16 / 淡墨 #6B6455 / 单一朱砂 #C8463A / 赭金 #E9B885 "
    "五色锁死 + 松散枯笔湿染笔触句 + 禁项清单逐字复用）·本批仅按「浓墨剪影」改写笔触强度段 + "
    "改写钤印条款（用户点名的参考风格含朱砂钤记）·其余逐字不动；② **六张**：hero-10 至 hero-15 "
    "接续既有 hero-01 至 hero-09 编号·人物叙事 2（冥府判官队列 / 持瓶菩萨立像）+ 法器符号 1"
    "（紧箍与金刚杵静物）+ 世界观场景 2（五行山两界山 / 东海龙宫水殿）+ 学术概念 1（六道轮回轮"
    "抽象水墨）·题材全部避开既有 9 张 hero 与 27 张 card 撞车；③ **构图硬边界**：主体止于上三分之二·"
    "下三分之一完全空白宣纸（叠字区）；④ **三轮返工**：v1 量化全绿但目视抳出钤印形态漂移（竖长条 / "
    "椭圆 / 四方）→ v2 写死方形后印面成清晰篆字形 → v3 印面限定纯朱砂块 + 另四张走交付端印面归一"
    "（只重绘印面·主体零改动）⇒ 六张印面统一且零可读文字；⑤ **验收**：2560×1440 精确 16:9 · "
    "净空带 282–557 px · 主体墨量 11.92%–77.82% · 严格朱砂 0.11%–1.52% · 底色 5 值同族 · "
    "规则线 0 命中 | —（认领登记·施工中） | —（本批级联立段） | **在途**（认领登记·2026-10-25·"
    "本会话） | 主会话 2026-10-25 | site/static/images/hero-10~15-*.webp · site/static/images/index.md · "
    "scripts/_w929_*.py · scripts/output/_w932_spec.json · CHANGELOG.md |"
)


def patch_ledger():
    with io.open(LEDGER, "r", encoding="utf-8", newline="") as f:
        lines = f.readlines()
    hit = -1
    for i, line in enumerate(lines):
        if line.startswith("| W929 |"):
            hit = i
            break
    if hit < 0:
        raise SystemExit("台账未找到 W929 行")
    if any(l.startswith("| W932 |") for l in lines):
        raise SystemExit("台账已有 W932 行（避免重复插入）")
    eol = "\r\n" if lines[hit].endswith("\r\n") else "\n"
    lines[hit] = GIVEUP_LINE + eol
    lines.insert(hit + 1, CLAIM_LINE + eol)
    with io.open(LEDGER, "w", encoding="utf-8", newline="") as f:
        f.writelines(lines)
    print("台账：W929 → 让号留痕行 · 新增 W931 认领行")


def patch_spec():
    with io.open(SPEC_OLD, "r", encoding="utf-8") as f:
        s = f.read()
    s = s.replace("_w929_spec.json", "_w932_spec.json")
    s = s.replace("_cascade_files_W929.txt", "_cascade_files_W932.txt")
    s = re.sub(r"W929", "W932", s)
    with io.open(SPEC_NEW, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    os.remove(SPEC_OLD)
    print("spec：_w929_spec.json → _w931_spec.json（批次号 W929 → W931）")


if __name__ == "__main__":
    patch_ledger()
    patch_spec()
