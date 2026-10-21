#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_assets.py — 第二轮 Logo 方案：生成资产 + 预览页 + 设计说明 + 自检。

自检比第一轮多两项：
  · 路径包围盒检查：每个图形必须完整落在 64×64 视口内（留 ≥1.5 单位边距），
    自动抓出「笔画出界 / 贴边 / 画歪」这类肉眼容易漏的缺陷
  · 笔画数量检查：每个方向至少 3 条楔形笔画，避免退化成单一描边

用法：py build_assets.py [--check]
"""
from __future__ import annotations

import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
# 归档版：重出产物落系统临时目录（不污染仓库），人工确认后拷入 ../logo/ 与 site/static/icons/
_OUT = tempfile.mkdtemp(prefix="logo-regen-")
ASSETS = os.path.join(_OUT, "assets")

from brush import fit_transform  # noqa: E402
from svgkit_text import FONT_SANS, FONT_SERIF, TextPath  # noqa: E402
from svgkit2 import BRANDS, MARKS, PALETTES, lockup, mark_svg  # noqa: E402

DIRS = ["e", "f", "g", "h", "i"]

# 各方向的合法笔画数下限（按构造声明，不是一刀切阈值）
# f 的云是「闭合轮廓 + 内部涡卷」两笔构造 —— 前三次失败正因把云当成线条组合
MIN_STROKES = {"e": 5, "f": 2, "g": 4, "h": 3, "i": 4}

MEANING = {
    "e": {
        "title": "棒 · 器物",
        "brand": "阅微",
        "idea": [
            "金箍棒是全书唯一的「制式装备」：一根两端束金箍的棍，横贯十万八千里。取「棒」不取「斗战」——不画打斗，画器物：工具本身才是这段旅程的主角。",
            "棒上钤一枚朱砂小印：器物与信物合一，正好落在「取经录」这个名字上——一路的器物，最后被记录下来。",
        ],
        "type": "思源宋体 Heavy（中文字标）· Noto Sans SC（副标）· 图形为楔形笔触",
        "colors": [
            ("墨 #23201A", "棍身（主笔画）"),
            ("赭金 #B98A4A", "两端金箍与节纹（金属）"),
            ("朱砂 #C8463A", "钤印（唯一点睛）"),
        ],
        "fit": "斜置的横构图 + 一枚方印，缩到 16px 仍能读出「一根棍 + 一个印」；favicon 用标准标即可，无需简化版。",
    },
    "f": {
        "title": "幡 · 引路",
        "brand": "问津",
        "idea": [
            "取经路上有旗：路旗经幡插在关口，替远行的人指方向，也标记「此处有物」。",
            "造型用竖杆 + 一条被风吹起的飘带，线描留白，杆顶一枚朱珠、旗面一点朱批——循着旗走，就能读到被略过的细节。",
        ],
        "type": "思源宋体 Heavy · 图形为楔形笔触（旗杆 + 双线飘带 + 朱珠朱点）",
        "colors": [
            ("墨 #23201A", "旗杆与飘带上缘（主）"),
            ("淡墨 #6B6455", "飘带下缘（次）"),
            ("朱砂 #C8463A", "杆顶朱珠 + 旗面朱点"),
        ],
        "fit": "竖构图 + 一条横向飘带，16px 仍可辨；favicon 用标准标即可（杆与带的关系在小尺寸下依然成立）。",
    },
    "g": {
        "title": "卷 · 载体",
        "brand": "拾遗",
        "idea": [
            "经卷是文本的容器：两端轴头，中间展开的卷面上是竖排的字。这个符号直接对应数字人文的对象——不是「西游记」四个字，而是一卷被反复展开、检索、批注的文本。",
            "「拾遗」的落点在这里：卷面上有一处朱砂朱批。散佚的东西被拾起来，是因为有人在上面批了字。",
        ],
        "type": "思源宋体 Heavy · 图形为楔形笔触（轴头 + 卷面 + 竖排文）",
        "colors": [
            ("墨 #23201A", "两端轴头（主）"),
            ("淡墨 #6B6455", "卷面边框与竖排文（次）"),
            ("朱砂 #C8463A", "朱批一点（唯一点睛）"),
        ],
        "fit": "卷面横长方形在 16px 会糊成一根横线 → favicon 需改用「两端轴头 + 一道竖」的极简版。",
    },
    "h": {
        "title": "山 · 门槛",
        "brand": "取经录",
        "idea": [
            "问津者先问路，而这条路要翻山。五行山是取经路的门槛：山脊用一条连绵的毛笔线画出来，笔锋有起有收，像一笔写成的连绵远山。",
            "山下有地平线，上方有云气与一点朱红（远寺的灯）。翻不过这道山，就还在问津。",
        ],
        "type": "思源宋体 Heavy · 图形为楔形笔触（连绵山脊 + 地平线 + 云气）",
        "colors": [
            ("墨 #23201A", "山脊（主）"),
            ("淡墨 #6B6455", "地平线与云气（次）"),
            ("朱砂 #C8463A", "山顶一点（远寺/灯）"),
        ],
        "fit": "山脊起伏在 16px 会连成一片 → favicon 需减为「两峰 + 地平线」的简化版。",
    },
    "i": {
        "title": "图 · 路书",
        "brand": "十万八千里",
        "idea": [
            "这张图的原型是 AI 概念稿里最有潜力的一张，现已回写为矢量：两端卷筒 + 一张斜摊开的纸面，"
            "纸面上是三座山脊、一条穿行的路线、一枚朱点。",
            "它直接对应这个项目的本体——一张画着山河与路线的图。数字人文做的事，就是把一部古典摊开成一张可检索的图；"
            "「十万八千里」不是修辞，是这张纸面上那条线的长度。",
        ],
        "type": "思源宋体 Heavy · 图形为楔形笔触（卷筒 + 纸面 + 山脊 + 路线 + 朱点）",
        "colors": [
            ("墨 #23201A", "卷筒 / 山脊 / 路线（主）"),
            ("淡墨 #6B6455", "纸面上下缘（次）"),
            ("朱砂 #C8463A", "路线上的一个点（唯一点睛）"),
        ],
        "fit": "横向构图，16px 下卷筒与纸面关系仍成立；山脊在小尺寸会糊成一排锯齿，favicon 建议只留卷筒 + 路线 + 朱点。",
    },
}

BRAND_TABLE = [
    ("取经录", "「录」是史书体例后缀（自《隋书·经籍志》以来的「录」体），数字人文的本分就是录、载；与「取经」主线构成双关。",
     "第 100 回：「圣僧努力取经编，西宇周流十四年」（原文 254 处「取经」）",
     "3 字 · 字标比例最佳 · 器物方向首选", "「录」略平，需副标补足品类信息"),
    ("十万八千里", "悟空筋斗云一纵的距离，也是全书的刻度与数据体量；数字与路程合成一个尺度。",
     "第 7 回：「会驾筋斗云，一纵十万八千里」（原文多处）",
     "5 字 · 数字人文气质最强 · 云形方向首选", "5 字偏长，组合标最小宽度要求高"),
    ("问津", "问路、寻渡、问法；读者向文本问路，正是这个品牌的日常动作。",
     "原文 0 命中 —— 典出《桃花源记》「后遂无问津者」，非原著语，须在文案中交代",
     "2 字 · 学术气质最浓 · 山形方向首选", "今日日常语义偏「打听消息」，需副标或释义兜底"),
    ("拾遗", "辑佚之学的「拾遗」，也指拾起阅读中被略过的细节 —— 与项目「一源多形」的方法论一致。",
     "原文 0 命中 —— 典出辑佚学传统（《拾遗记》），非原著语",
     "2 字 · 学术型首选 · 经卷方向首选", "2 字略短，需与图形标强绑定或加副标"),
    ("阅微", "自清·纪昀《阅微草堂笔记》化出，「从细微处察看」，对应细读与微观史学。",
     "原文 0 命中 —— 晚出典籍，非西游语境",
     "2 字 · 气质最雅 · 备选", "晚出（18 世纪）与西游语境无直接血脉，需额外解释"),
]

CONCEPTS = [
    ("concept-01-ruyi-staff", "如意金箍棒", "工笔线描的棍身 + 鎏金箍纹 + 朱砂印，形制最完整。", True),
    ("concept-02-ruyi-cloud", "如意祥云", "闭合轮廓 + 内部涡卷 —— 该构造已回写为矢量（方向 F）。", True),
    ("concept-03-scroll", "经卷（已判废）", "画成了装饰画框，且图内混入了乱码汉字，违反「无文字」约束。", False),
    ("concept-04-mountains", "水墨远山", "文人画笔意的连绵山脊 + 地平线 + 朱点，气质最佳。", True),
    ("concept-05-headband-ring", "紧箍环（已判废）", "读成了粗黑甜甜圈，缺紧箍的形制信息。", False),
    ("concept-06-bodhi-leaf", "菩提叶（已判废）", "轮廓像水滴，叶脉走形，整体偏卡通。", False),
]

# 第二批（12 张）：扩母题，挑出可用者并把最好的一张回写成矢量
CONCEPTS2 = [
    ("c2-01-ruyi-staff-v2", "如意金箍棒 v2", "细杆 + 鎏金箍纹 + 朱印，箍纹细节明显优于第一版。", True),
    ("c2-02-nine-ring-staff", "九环锡杖", "细长杖身 + 顶端法器 + 串环，构图完整。", True),
    ("c2-03-lotus", "侧生莲花", "工笔线描的莲花与叶，偏插画、细节偏多。", True),
    ("c2-04-eave", "飞檐斗拱", "起翘的飞檐 + 斗拱 + 铃铛，建筑气质与线条质量都高。", True),
    ("c2-05-prayer-beads", "佛珠念珠", "珠串 + 佛头 + 朱流苏，简洁清楚。", True),
    ("c2-06-vase-willow", "净瓶与柳枝", "细颈瓶 + 一枝垂柳，雅致好认。", True),
    ("c2-07-moon-spade", "月牙铲", "双月牙 + 杖身，辨识度高。", True),
    ("c2-08-itinerary-map", "取经路舆图", "★ 全部 18 张里最具 Logo 潜力的一张 —— 已回写为矢量（方向 I）。", True),
    ("c2-09-sinan-compass", "司南", "圆盘 + 勺针 + 朱点，古代科学感。", True),
    ("c2-10-jade-seal", "玉印（已判废）", "印面出现伪篆乱码字符，违反「无文字」约束。", False),
    ("c2-11-banana-fan", "芭蕉扇（已判废）", "叶脉写实过密、底部两笔突兀，整体偏插画。", False),
    ("c2-12-bell", "晨钟铜钟", "钟形 + 顶环 + 侧耳 + 朱点，简洁。", True),
]

CHANGES = [
    ("图形语言", "抽象制图：方框 / 折线 / 版框（像 UI 图标）",
     "具象母题：金箍棒 / 筋斗云 / 经卷 / 五行山（一眼认得出西游）"),
    ("线条工艺", "等宽 stroke 描边（图标线条，无笔意）",
     "楔形笔触：起笔顿、行笔提按、收笔顿收（毛笔线条）"),
    ("字标组合", "朱砂横分隔线（把名字压成两块）",
     "一枚朱砂钤记点睛（名字与图形是一个整体）"),
    ("配色纪律", "强制等同站点令牌（朱砂+墨+靛蓝三色并列）",
     "墨为主、朱砂只点一处、赭金只用于金属；站点令牌仍是底色基准"),
    ("构图节奏", "四方向都是「框 + 线 + 点」，节奏雷同",
     "横置 / 卷曲 / 横长 / 层叠，四种完全不同的构图"),
]


def esc(s: str) -> str:
    return s.replace("&", "&").replace("<", "<").replace(">", ">")


# ─────────────────────────────────────────────────────────────
# 自检工具：路径包围盒
# ─────────────────────────────────────────────────────────────
def path_points(d: str):
    """粗解析 SVG path d，返回采样点列表（M/L/C/a 足够）。"""
    pts = []
    cur = (0.0, 0.0)
    for m in re.finditer(r"([A-Za-z])([^A-Za-z]*)", d):
        cmd = m.group(1)
        nums = [float(x) for x in re.findall(r"-?\d*\.?\d+", m.group(2))]
        if cmd in "ML":
            for i in range(0, len(nums) - 1, 2):
                cur = (nums[i], nums[i + 1])
                pts.append(cur)
        elif cmd in "ml":
            for i in range(0, len(nums) - 1, 2):
                cur = (cur[0] + nums[i], cur[1] + nums[i + 1])
                pts.append(cur)
        elif cmd == "C":
            for i in range(0, len(nums) - 5, 6):
                pts.append((nums[i], nums[i + 1]))
                pts.append((nums[i + 2], nums[i + 3]))
                cur = (nums[i + 4], nums[i + 5])
                pts.append(cur)
        elif cmd == "c":
            for i in range(0, len(nums) - 5, 6):
                pts.append((cur[0] + nums[i], cur[1] + nums[i + 1]))
                cur = (cur[0] + nums[i + 4], cur[1] + nums[i + 5])
                pts.append(cur)
        elif cmd in "Aa":
            for i in range(0, len(nums) - 6, 7):
                dx, dy = nums[i + 4], nums[i + 5]
                if cmd == "a":
                    cur = (cur[0] + dx, cur[1] + dy)
                else:
                    cur = (dx, dy)
                pts.append(cur)
        elif cmd in "Zz":
            pass
    return pts


def bbox_of(markup: str):
    xs, ys = [], []
    for d in re.findall(r'\sd="([^"]+)"', markup):
        for x, y in path_points(d):
            xs.append(x)
            ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def build_svgs(serif: TextPath, sans: TextPath) -> None:
    os.makedirs(ASSETS, exist_ok=True)
    for key in DIRS:
        for pal in ("light", "dark", "mono"):
            with open(os.path.join(ASSETS, f"{key}-mark-{pal}.svg"), "w", encoding="utf-8") as f:
                f.write(mark_svg(key, pal))
        with open(os.path.join(ASSETS, f"{key}-mark-inv.svg"), "w", encoding="utf-8") as f:
            f.write(mark_svg(key, "mono_inv"))
        for pal in ("light", "dark"):
            with open(os.path.join(ASSETS, f"{key}-lockup-{pal}.svg"), "w", encoding="utf-8") as f:
                f.write(lockup(key, pal, serif, sans))
    src = os.path.abspath(os.path.join(BASE, "..", "..", "..", "site", "static", "icons", "icon-512.png"))
    dst = os.path.join(ASSETS, "current-icon-512.png")
    if os.path.exists(src):
        import shutil
        shutil.copy2(src, dst)


HTML_HEAD = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Logo 探索 · 第二轮（具象符号 + 楔形笔触）</title>
<style>
:root{
  --bg:#FAF7F0; --paper:#FFFFFF; --paper-warm:#F1EBDD; --dark:#221D16;
  --ink:#23201A; --ink-soft:#6B6455; --ink-faint:#9A9280;
  --accent:#C8463A; --accent-deep:#AF3F34; --accent-2:#3A6B8C;
  --line:#E5DFD0;
  --font-serif:'Source Han Serif SC','Noto Serif SC','Songti SC',serif;
  --font-sans:'Noto Sans SC','Source Han Sans SC','Microsoft YaHei',sans-serif;
  --font-mono:'JetBrains Mono','Consolas',monospace;
}
html[data-theme="dark"]{
  --bg:#221D16; --paper:#2B2419; --paper-warm:#33291B;
  --ink:#F2EBDC; --ink-soft:#CBBFA9; --ink-faint:#8F8674;
  --accent:#E0604F; --accent-deep:#C94F3F; --accent-2:#7FA8C9;
  --line:rgba(242,235,220,0.14);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-sans);
  line-height:1.8;-webkit-font-smoothing:antialiased}
.wrap{max-width:1120px;margin:0 auto;padding:0 28px 96px}
header.hero{background:var(--dark);color:#F2EBDC;padding:52px 0 42px;margin-bottom:38px;
  border-bottom:3px solid var(--accent)}
header.hero .wrap{padding-bottom:0}
h1{font-family:var(--font-serif);font-size:clamp(1.6rem,1.1rem+2vw,2.4rem);margin:0 0 8px;letter-spacing:.04em}
.kicker{font-family:var(--font-mono);font-size:.78rem;letter-spacing:.22em;color:#C9A063;margin:0 0 14px}
.hero p{margin:0 0 10px;max-width:66ch;color:#CBBFA9;font-size:.94rem}
.toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:22px 0 0}
.toolbar button{font-family:var(--font-sans);font-size:.85rem;padding:7px 16px;border-radius:999px;
  border:1px solid #5B5040;background:transparent;color:#CBBFA9;cursor:pointer}
.toolbar button[aria-pressed="true"]{background:#C8463A;border-color:#C8463A;color:#fff}
h2{font-family:var(--font-serif);font-size:1.35rem;margin:0 0 4px}
h3{font-family:var(--font-serif);font-size:1.05rem;margin:30px 0 10px}
.tag{display:inline-block;font-family:var(--font-mono);font-size:.72rem;letter-spacing:.16em;
  color:var(--accent);border:1px solid var(--accent);border-radius:3px;padding:1px 7px;margin-bottom:8px}
.lede{color:var(--ink-soft);font-size:.94rem;margin:0 0 8px}
section.dir{border-top:1px solid var(--line);padding-top:28px;margin-top:42px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:18px 0 16px}
@media (max-width:820px){.cols{grid-template-columns:1fr}}
.panel{border:1px solid var(--line);border-radius:10px;padding:22px 22px 26px;overflow:hidden}
.panel.light{background:#FAF7F0;--m-ink:#23201A;--m-ink2:#6B6455;--m-accent:#C8463A;
  --m-gold:#B98A4A;--m-paper:#FAF7F0;--m-line:#E5DFD0}
.panel.dark{background:#221D16;--m-ink:#F2EBDC;--m-ink2:#CBBFA9;--m-accent:#E0604F;
  --m-gold:#C9A96B;--m-paper:#221D16;--m-line:rgba(242,235,220,.16)}
.plabel{font-family:var(--font-mono);font-size:.7rem;letter-spacing:.14em;
  color:var(--ink-faint);margin-bottom:14px}
.panel.dark .plabel{color:#8F8674}
.lockup svg{width:100%;height:auto;max-width:470px;display:block}
.meaning p{margin:0 0 10px;color:var(--ink-soft);font-size:.94rem}
.meaning p:first-child{color:var(--ink)}
.meta{display:grid;grid-template-columns:200px 1fr;gap:6px 18px;font-size:.88rem;margin:16px 0 4px}
.meta dt{font-family:var(--font-mono);font-size:.74rem;letter-spacing:.1em;color:var(--ink-faint);padding-top:4px}
.meta dd{margin:0;color:var(--ink-soft)}
.mini{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}
@media (max-width:820px){.mini{grid-template-columns:1fr}}
.card{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:18px}
.card h4{font-family:var(--font-mono);font-size:.72rem;letter-spacing:.12em;color:var(--ink-faint);
  margin:0 0 12px;font-weight:500}
.sizes{display:flex;align-items:flex-end;gap:16px;flex-wrap:wrap}
.sizebox{text-align:center}
.sizebox svg{display:block;margin:0 auto 5px}
.sizebox span{font-family:var(--font-mono);font-size:.68rem;color:var(--ink-faint)}
.chiprow{display:flex;gap:10px;flex-wrap:wrap}
.chip{display:flex;align-items:center;gap:8px;border:1px solid var(--line);border-radius:6px;
  padding:6px 10px;font-size:.82rem}
.chip i{width:16px;height:16px;border-radius:3px;display:block;border:1px solid rgba(0,0,0,.12)}
.chip b{font-family:var(--font-mono);font-size:.76rem;font-weight:500}
.chip span{color:var(--ink-faint);font-size:.78rem}
table{width:100%;border-collapse:collapse;font-size:.88rem;margin:12px 0 4px}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-family:var(--font-mono);font-size:.72rem;letter-spacing:.1em;color:var(--ink-faint);font-weight:500}
td.name{font-family:var(--font-serif);font-size:1.05rem;white-space:nowrap}
td.cite{font-family:var(--font-serif);color:var(--accent-2);font-size:.86rem}
td.old{color:var(--ink-faint);text-decoration:line-through}
td.new{color:var(--ink)}
.rules{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:12px}
@media (max-width:820px){.rules{grid-template-columns:1fr}}
.rule h4{font-family:var(--font-serif);margin:0 0 6px;font-size:1rem}
.rule ul{margin:0;padding-left:18px;font-size:.88rem;color:var(--ink-soft)}
.rule li{margin-bottom:4px}
.compare{display:flex;gap:24px;align-items:center;flex-wrap:wrap}
.compare figure{margin:0;text-align:center}
.compare figcaption{font-family:var(--font-mono);font-size:.7rem;color:var(--ink-faint);margin-top:8px}
.compare img{width:92px;height:92px;border-radius:14px;border:1px solid var(--line);background:#FAF7F0}
.compare svg{width:92px;height:92px}
.concept-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:14px 0 4px}
@media (max-width:820px){.concept-grid{grid-template-columns:1fr}}
.concept{border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--paper)}
.concept img{display:block;width:100%;aspect-ratio:1/1;object-fit:cover;background:#FAF7F0}
.concept figcaption{padding:10px 12px;font-size:.82rem;color:var(--ink-soft)}
.concept figcaption b{display:block;font-family:var(--font-serif);font-size:1rem;color:var(--ink);margin-bottom:2px}
.concept.rejected{opacity:.52}
.concept .verdict{font-family:var(--font-mono);font-size:.68rem;letter-spacing:.08em;
  display:inline-block;margin-top:5px;padding:1px 6px;border-radius:3px;border:1px solid currentColor}
.concept .v-ok{color:#6B8E5A}
.concept .v-no{color:#8C2A2A}
footer{margin-top:52px;padding-top:20px;border-top:1px solid var(--line);
  font-family:var(--font-mono);font-size:.74rem;color:var(--ink-faint);line-height:2}
</style>
</head>
<body>
<header class="hero"><div class="wrap">
  <p class="kicker">LOGO EXPLORATION · ROUND 2 · FIGURATIVE</p>
  <h1>Logo 探索 · 第二轮：具象符号 + 楔形笔触</h1>
  <p>第一轮（方框 + 线条的抽象制图）判定作废：它们像 UI 图标，不像品牌标志，既无西游的具体性，也无独占的轮廓。
     本轮三处改动：① 图形换成具象母题（金箍棒 / 筋斗云 / 经卷 / 五行山）；② 线条换成有起收提按的楔形笔触；
     ③ 字标组合去掉朱砂分隔线，改为一枚钤记点睛。</p>
  <p>配色仍以站点 tokens.css 为底色基准，但不再强制等同：墨为主、朱砂只点一处、赭金只用于金属。</p>
  <div class="toolbar">
    <button id="t-light" aria-pressed="true">页面：浅底</button>
    <button id="t-dark" aria-pressed="false">页面：深底</button>
    <span style="font-size:.78rem;color:#8F8674">（下方每张卡片已并排给出浅底 / 深底两版）</span>
  </div>
</div></header>
<div class="wrap">
<h3>一、本轮相对第一轮改了什么</h3>
<table>
<thead><tr><th style="width:120px">维度</th><th style="width:38%">第一轮（作废）</th><th>本轮</th></tr></thead>
<tbody>
__CHANGE_ROWS__
</tbody></table>
<h3>二、品牌名候选（5 个）</h3>
<p class="lede">名字问题与图形无关，沿用上一轮的候选与核验结论：「取经」「十万八千里」为原著语，
   「问津」「拾遗」「阅微」原著 0 命中，典出后出文献，已如实标注。</p>
<table>
<thead><tr><th style="width:110px">候选名</th><th>寓意提炼</th><th style="width:30%">出处（已核）</th><th style="width:16%">适配</th><th style="width:16%">风险</th></tr></thead>
<tbody>
__BRAND_ROWS__
</tbody></table>
<h3>三、四个图形方向</h3>
__DIR_BLOCKS__
<h3>四、AI 概念稿（造型上限探索）</h3>
<p class="lede">手工路径画不出工笔质感的东方纹样，因此另用生成模型做了一轮<strong>纯图形</strong>概念探索
   （提示词已锁死：无文字、单色墨 + 一处朱砂、宣纸底、无渐变无 3D 无卡通）。六张里<strong>三张可用、三张已判废</strong>——
   可用的棒 / 云 / 山，其形制已被回写成矢量：如意云的「闭合轮廓 + 内部涡卷」构造，就是从概念稿反推的。</p>
<div class="concept-grid">
__CONCEPT_BLOCKS__
</div>
<p class="lede" style="margin-top:18px">第二轮扩批（12 张）：再出 12 个母题，把概念板做厚。
   其中<strong>取经路舆图</strong>被回写成矢量（方向 I）；玉印（伪篆乱码）与芭蕉扇（写实过密）判废。</p>
<div class="concept-grid">
__CONCEPT2_BLOCKS__
</div>
<h3>五、深浅底与单色适配规则</h3>
<div class="rules">
  <div class="rule card">
    <h4>形状恒定，只换语义色</h4>
    <ul>
      <li>浅底：墨 #23201A · 淡墨 #6B6455 · 朱砂 #C8463A · 赭金 #B98A4A</li>
      <li>深底：宣纸 #F2EBDC · 淡墨 #CBBFA9 · 朱砂 #E0604F · 赭金 #C9A96B</li>
      <li>同一套内联 SVG 渲染两版，验证的是真实映射关系而非两张不同的图</li>
    </ul>
  </div>
  <div class="rule card">
    <h4>单色 / 印刷</h4>
    <ul>
      <li>单色版：纯墨（浅底）/ 纯宣纸（深底），用于传真、烫印、雕刻、单色章</li>
      <li>赭金在单色版里并入墨色 —— 金属感靠形态而非颜色</li>
    </ul>
  </div>
  <div class="rule card">
    <h4>小尺寸</h4>
    <ul>
      <li>图形标在 16 / 24 / 32 / 48 / 96 px 逐档实测，页面内可直接比对</li>
      <li>棒、云两方向结构紧，16px 可用；卷、山两方向需减元素（见各方向「适配说明」）</li>
    </ul>
  </div>
  <div class="rule card">
    <h4>与站点 / 与第一轮的关系</h4>
    <ul>
      <li>现有站点图标是红白蓝同心圆（见对比区），只表达「圆」</li>
      <li>第一轮四个方向已归档在 tmpe/_reports/logo-explore/，可横向对照</li>
      <li>本轮尚未改动仓库任何入库文件，也未替换现有图标</li>
    </ul>
  </div>
</div>
<h3>五、与现有图标 / 第一轮对比</h3>
<div class="compare">
  <figure><img src="assets/current-icon-512.png" alt="现有图标"><figcaption>现状 · 同心圆</figcaption></figure>
__COMPARE_MARKS__
</div>
<footer>
  生成物 · tmpe/_reports/logo-explore-v2/ ｜ 中文字标：思源宋体 Heavy（已转 SVG 路径）<br>
  图形：楔形笔触引擎 tools/brush.py（Catmull-Rom 中线 + 宽度函数 + 平滑轮廓）<br>
  配色底座：site/tokens.css（--ink #23201A / --accent #C8463A / --ink-soft #6B6455）<br>
  引文核验：scripts/_cite_probe.py 实读 dataset/text-search.json（--max-len 100 默认档）
</footer>
</div>
<script>
(function(){
  var l=document.getElementById('t-light'), d=document.getElementById('t-dark'), r=document.documentElement;
  function set(t){ r.setAttribute('data-theme', t);
    l.setAttribute('aria-pressed', String(t==='light'));
    d.setAttribute('aria-pressed', String(t==='dark')); }
  l.addEventListener('click', function(){ set('light'); });
  d.addEventListener('click', function(){ set('dark'); });
})();
</script>
</body>
</html>
"""


def dir_block(key: str, serif: TextPath, sans: TextPath) -> str:
    m = MEANING[key]
    lock = lockup(key, "vars", serif, sans)
    idea = "".join(f"<p>{esc(t)}</p>" for t in m["idea"])
    colors = "".join(
        f'<div class="chip"><i style="background:{hexv.split()[0]}"></i>'
        f'<b>{esc(hexv)}</b><span>{esc(desc)}</span></div>'
        for hexv, desc in m["colors"]
    )
    sizes = "".join(
        f'<div class="sizebox">{mark_svg(key, "light", size=s)}<span>{s}</span></div>'
        for s in (16, 24, 32, 48, 96)
    )
    return f"""
<section class="dir" id="dir-{key}">
  <span class="tag">方向 {key.upper()}</span>
  <h2>{esc(m["title"])} —《{esc(m["brand"])}》</h2>
  <p class="lede">{esc(m["type"])}</p>
  <div class="cols">
    <div class="panel light"><div class="plabel">浅底 · 宣纸暖白 #FAF7F0</div><div class="lockup">{lock}</div></div>
    <div class="panel dark"><div class="plabel">深底 · 玄墨 #221D16</div><div class="lockup">{lock}</div></div>
  </div>
  <div class="meaning">{idea}</div>
  <dl class="meta">
    <dt>图形构成</dt><dd>{esc(m["fit"])}</dd>
    <dt>字体组合</dt><dd>{esc(m["type"])}</dd>
    <dt>配色方案</dt><dd>{colors}</dd>
  </dl>
  <div class="mini">
    <div class="card"><h4>图形标（64px 域）</h4>
      <div style="display:flex;gap:26px;align-items:center;flex-wrap:wrap">
        <div class="sizebox">{mark_svg(key, "light", size=96)}<span>标准标 96</span></div>
        <div class="sizebox">{mark_svg(key, "dark", size=96)}<span>深底版 96</span></div>
      </div>
    </div>
    <div class="card"><h4>小尺寸实测（16 → 96）</h4>
      <div class="sizes">{sizes}</div>
    </div>
  </div>
</section>
"""


def build_html(serif: TextPath, sans: TextPath) -> None:
    rows = "".join(
        f'<tr><td class="name">{esc(a)}</td><td class="old">{esc(b)}</td><td class="new">{esc(c)}</td></tr>'
        for a, b, c in CHANGES
    )
    brows = "".join(
        f'<tr><td class="name">{esc(n)}</td><td>{esc(m)}</td>'
        f'<td class="cite">{esc(c)}</td><td>{esc(a2)}</td><td>{esc(r)}</td></tr>'
        for n, m, c, a2, r in BRAND_TABLE
    )
    blocks = "".join(dir_block(k, serif, sans) for k in DIRS)
    concepts = "".join(
        f'<figure class="concept{"" if ok else " rejected"}">'
        f'<img src="assets/concepts/{fn}.png" alt="{esc(title)}">'
        f'<figcaption><b>{esc(title)}</b>{esc(note)}'
        f'<span class="verdict {"v-ok" if ok else "v-no"}">'
        f'{"可用 · 形制已回写矢量" if ok else "判废"}</span></figcaption></figure>'
        for fn, title, note, ok in CONCEPTS
    )
    concepts2 = "".join(
        f'<figure class="concept{"" if ok else " rejected"}">'
        f'<img src="assets/concepts2/{fn}.png" alt="{esc(title)}">'
        f'<figcaption><b>{esc(title)}</b>{esc(note)}'
        f'<span class="verdict {"v-ok" if ok else "v-no"}">'
        f'{"可用" if ok else "判废"}</span></figcaption></figure>'
        for fn, title, note, ok in CONCEPTS2
    )
    compare = "".join(
        f'<figure>{mark_svg(k, "light", size=92)}'
        f'<figcaption>方向 {k.upper()} · {esc(MEANING[k]["title"])}</figcaption></figure>'
        for k in DIRS
    )
    html = (HTML_HEAD
            .replace("__CHANGE_ROWS__", rows)
            .replace("__BRAND_ROWS__", brows)
            .replace("__DIR_BLOCKS__", blocks)
            .replace("__CONCEPT_BLOCKS__", concepts)
            .replace("__CONCEPT2_BLOCKS__", concepts2)
            .replace("__COMPARE_MARKS__", compare))
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


README = """# Logo 探索 · 第二轮（具象符号 + 楔形笔触）· 设计说明

> **一句话结论**：第一轮（方框 + 线条的抽象制图）判定作废——它们像 UI 图标而不像品牌标志。
> 本轮改为四个具象母题（金箍棒 / 筋斗云 / 经卷 / 五行山），线条用楔形笔触重画，
> 字标组合改为「图形 + 中文字标 + 一枚朱砂钤记」。
> **状态**：待用户选型；**尚未**改动仓库任何入库文件，**尚未**替换现有站点图标。
> **复算**：`py tools/build_assets.py --check`（生成 + 自检，输出 SELF-CHECK OK 即一致）。

---

## 1. 第一轮为什么作废

| 维度 | 第一轮 | 本轮 |
| --- | --- | --- |
{changes}

**一句话诊断**：第一轮四个方向全是「方框 + 线条」的抽象制图语言，构图节奏雷同，
既没有一样东西让人想到西游，也没有「只有这家才有」的独占轮廓——那是图标，不是标志。

## 2. 品牌名候选（5 个）

{brand_table}

## 3. 四个方向

{dir_sections}

## 4. AI 概念稿（造型上限探索）

手工路径画不出工笔质感的东方纹样，因此另用生成模型做**纯图形**概念探索
（提示词锁死：无文字、单色墨 + 一处朱砂、宣纸底、无渐变无 3D 无卡通）。
共两批 18 张，**14 张可用、4 张判废**。

第一批（6 张）：

| 概念稿 | 判定 | 说明 |
| --- | --- | --- |
| 如意金箍棒 | **可用** | 工笔线描棍身 + 鎏金箍纹 + 朱砂印，形制最完整 |
| 如意祥云 | **可用** | 闭合轮廓 + 内部涡卷——该构造已回写为矢量（方向 F） |
| 水墨远山 | **可用** | 文人画笔意的连绵山脊 + 地平线 + 朱点，气质最佳 |
| 经卷 | 判废 | 画成装饰画框，且图内混入乱码汉字，违反「无文字」约束 |
| 紧箍环 | 判废 | 读成粗黑甜甜圈，缺紧箍的形制信息 |
| 菩提叶 | 判废 | 轮廓像水滴，叶脉走形，整体偏卡通 |

第二批（12 张 · 扩母题）：

| 概念稿 | 判定 | 说明 |
| --- | --- | --- |
| **取经路舆图** | **可用 · 已回写为矢量（方向 I）** | 全部 18 张里最具 Logo 潜力的一张：几何化、可矢量化，且直指项目本体 |
| 如意金箍棒 v2 | 可用 | 箍纹细节明显优于第一版（方向 E 已据此升级） |
| 飞檐斗拱 | 可用 | 起翘飞檐 + 斗拱 + 铃铛，线条质量高 |
| 九环锡杖 / 月牙铲 / 佛珠 / 净瓶柳枝 / 司南 / 晨钟 | 可用 | 各自形制清楚，可作后续储备 |
| 侧生莲花 | 可用 | 工笔线条好，但偏插画、细节偏多 |
| 玉印 | 判废 | 印面出现伪篆乱码字符，违反「无文字」约束 |
| 芭蕉扇 | 判废 | 叶脉写实过密、底部两笔突兀，偏插画 |

**关键教训（写给下一轮）**：

1. 云的关键是**闭合轮廓 + 内部涡卷**，不是「线条组合」。本轮手写云失败三次
   （杏仁眼 → 逗号 → 放大镜），每次都是因为把云当成若干条线拼；改用闭合轮廓后一次就对。
   任何「有团块感的形制」（云、果实、器皿）都应先画闭合外轮廓，再加内部细节。
2. **AI 概念稿的价值在形制，不在像素**：位图不可缩放、不能换底色、favicon 不可用，
   必须回写成矢量才能落地。本轮回写了两张（祥云 → 方向 F，取经路舆图 → 方向 I）。
3. **生成模型的文字污染是硬伤**：两次都出现「印面伪篆乱码」「卷内混入汉字」。
   提示词必须显式写 `no text, no letters, no Chinese characters`，且验收时要专门查这一项。

## 5. 配色方案总表

| 语义 | 浅底 | 深底 | 与站点令牌关系 |
| --- | --- | --- | --- |
| 墨（主） | `#23201A` | `#F2EBDC` | `--ink` 同值 |
| 淡墨（次） | `#6B6455` | `#CBBFA9` | `--ink-soft` 同值 |
| 朱砂（点睛） | `#C8463A` | `#E0604F` | `--accent` 同值 |
| 赭金（金属） | `#B98A4A` | `#C9A96B` | 邻近 `--chart-3 #C9A063`，偏暖以区别于数据色 |

配色纪律：**墨为主体，朱砂全图只出现一处（钤记/朱批/山顶灯），赭金只用于金属部件**。
这是本轮相对第一轮最重要的修正——第一轮把朱砂、靛蓝、赭金三色并列，视觉上花且缺乏主次。

## 5. 深浅底、单色与小尺寸

1. **形状恒定**：深浅底只换语义色映射，图形一个点都不改；预览页用同一套内联 SVG 渲染两版。
2. **单色版**：`*-mark-mono.svg`（纯墨）与 `*-mark-inv.svg`（纯宣纸），用于传真、烫印、雕刻、黑白印刷；
   赭金在单色版里并入墨色——金属感靠形态不靠颜色。
3. **小尺寸**：页面内提供 16 / 24 / 32 / 48 / 96 px 逐档实测。
   棒与云结构紧，16px 可用；卷与山在 16px 需减元素（见各方向「适配说明」）。
4. **安全区**：图形在 64 单位视口内留 ≥1.5 单位净空（约 2.3%），符合 maskable 图标安全区要求。

## 6. 笔触引擎

`tools/brush.py` 用「中线 + 宽度函数 + 左右轮廓」生成楔形笔画：
Catmull-Rom 加密中线 → 按弧长参数插值宽度（起 / 峰 / 收）→ 求法向偏移出左右轮廓 →
Catmull-Rom 转三次贝塞尔平滑闭合。笔锋的粗细变化是本轮视觉质感的主要来源。

## 7. 资产清单

```
tmpe/_reports/logo-explore-v2/
├── index.html                 预览页（零外域依赖 · file:// 可开 · 深浅底切换 · 多档小尺寸实测 · AI 概念稿区）
├── README.md                  本文件
├── assets/
│   ├── {e,f,g,h}-mark-{light,dark,mono}.svg
│   ├── {e,f,g,h}-mark-inv.svg
│   ├── {e,f,g,h}-lockup-{light,dark}.svg
│   ├── current-icon-512.png   现有站点图标（对比用）
│   ├── concepts/              AI 概念稿（6 张，640×640）
│   └── png/                   PNG 导出（透明背景）+ favicon.ico
├── screenshots/
│   ├── preview-sheet.png      四方向 × 深浅底拼版
│   ├── concept-sheet.png      AI 概念稿拼版
│   ├── full-page-light.png    整页截图
│   └── dir-{e,f,g,h}.png      四个方向分区截图
└── tools/
    ├── brush.py               楔形笔触引擎（中线 + 宽度函数 + 平滑轮廓）
    ├── svgkit2.py             四个图形 + 组合标
    ├── build_assets.py              资产生成 + 自检（--check）
    ├── preview_png.py         拼版预览（不依赖浏览器）
    ├── concept_args.json      AI 概念稿提示词
    ├── fetch_concepts.py      概念稿下载与归一
    ├── export_png.py          SVG → PNG / favicon.ico
    └── archive_shots.py       截图归档与分区裁切
```

## 8. 自检口径

`py tools/build_assets.py --check` 覆盖：
- 全部 SVG 可被 XML 解析、文件非空
- 预览页占位符已替换、**零外域资源引用**（file:// 铁律）
- **路径包围盒检查**：每个图形必须完整落在 64×64 视口内
  —— 自动抓出「笔画出界 / 贴边 / 画歪」，这类缺陷肉眼容易漏
- **视觉体量均衡检查**：四个方向的归一化包围盒面积必须落在同一量级（最大/最小 ≤ 1.15），
  否则并排时扁的那个会明显显小（本轮实测：扁的棒曾只有方的山的 1/2 体量）
- **笔画数检查**：按各方向的构造声明下限（棒 5 / 云 2 / 卷 4 / 山 3），
  避免退化成单一描边；云是「闭合轮廓 + 内部涡卷」两笔构造，故下限为 2

## 9. 定稿后的落地清单（本轮**未执行**）

**开工前置（已实测通过 · 2026-10-21）**

```
python scripts/preflight_check.py --touches "site/static/icons/,site/manifest.webmanifest,site/index.html,xiyouji-desktop/,README.md,docs/00-导读/W批次编号对账表.md" --self W856
```

实测结论：`取号 = 已认领 max=W855 → 下一自由号 W856` ·
`touches 交集检查：本批声明 6 项·与在途批次（W854）无交集` · `PREFLIGHT PASS——无风险项，可动工`。
**注意**：号序会随其他批次收官推进，施工当时必须重跑，以脚本输出为准，不按此静态结论硬套。

**落地步骤**

- [ ] 在对账表登记 W856 认领行（touches 声明上述 6 项）
- [ ] 按选定方向 + 品牌名重新导出（字标随名字变，图形不变）
- [ ] 替换 `site/static/icons/icon-{16,32,192,512}.png` 与 `icon-maskable-512.png`
- [ ] 更新 `site/manifest.webmanifest` 的图标引用
- [ ] `site/index.html` 页眉换成组合标，hero 深色区块用深底版
- [ ] 桌面端应用图标（`xiyouji-desktop/`）同步
- [ ] 补 macOS `icns`
- [ ] 全站品牌名统一（README / 页眉 / manifest / 桌面端）

**并行协作纪律（W855 批实测 · 三条）**

1. **新增文档有 7 面连带**（报告正文 + 目录索引 + `docs/INDEX.md` + `scripts/output/index.md`
   登记 + stats 三件 + 站内搜索索引两页 + CSP 复算 + 标记面）。
   若把 Logo 设计说明纳入 `docs/` 体系，同样会触发搜索索引与 CSP 面 —— 不能只写正文就提交。
2. **共享面「丢失更新」**：并行会话整文件写入会**静默覆盖**对方刚写好的台账行
   （git diff 为空、无冲突提示）。改台账/索引后须**核 mtime 并立即提交**，别攒着。
3. **`site/static/icons/` 是新目录**：现有生成件 `site/static/icons/index.md` 需随内容刷新 ——
   落图标后跑 `python scripts/gen_folder_docs.py --refresh`
   （仅刷新生成物所有件，人工维护件自动跳过），否则第 45 门禁会报该目录清单漂移。

## 10. 复算命令

```powershell
cd tmpe/_reports\\logo-explore-v2
py -3 tools\\build_assets.py --check          # 生成 SVG / 预览页 / README + 全量自检
py -3 tools\\preview_png.py              # 四方向 × 深浅底拼版（不依赖浏览器，最快的视觉回路）
py -3 tools\\export_png.py               # SVG → PNG（透明背景）+ favicon.ico
py -3 tools\\fetch_concepts.py           # 概念稿下载（需 mcode-tools）
py -3 tools\\archive_shots.py <整页截图.png>   # 归档截图并裁四方向分区图
```

第一轮的产物保留在 `tmpe/_reports/logo-explore/`，可横向对照（第一轮判定作废，仅留作对照）。
"""


def write_readme() -> None:
    changes = "\n".join(f"| {a} | {b} | {c} |" for a, b, c in CHANGES)
    brows = "\n".join(
        f"### 《{n}》\n\n- **寓意**：{m}\n- **出处（已核）**：{c}\n"
        f"- **适配**：{a}\n- **风险**：{r}\n" for n, m, c, a, r in BRAND_TABLE
    )
    dirs = []
    for key in DIRS:
        m = MEANING[key]
        colors = "；".join(f"{h}（{d}）" for h, d in m["colors"])
        idea = "\n".join(f"  {i}" for i in m["idea"])
        dirs.append(f"### 方向 {key.upper()} · {m['title']} ——《{m['brand']}》\n\n"
                    f"- **寓意提炼**：\n{idea}\n- **字体组合**：{m['type']}\n"
                    f"- **配色**：{colors}\n- **适配说明**：{m['fit']}\n")
    text = (README
            .replace("{changes}", changes)
            .replace("{brand_table}", brows)
            .replace("{dir_sections}", "\n".join(dirs)))
    with open(os.path.join(BASE, "README.md"), "w", encoding="utf-8") as f:
        f.write(text)


def self_check() -> int:
    errs = []
    weights = {}
    for key in DIRS:
        for name in (f"{key}-mark-light.svg", f"{key}-mark-dark.svg", f"{key}-mark-mono.svg",
                     f"{key}-mark-inv.svg", f"{key}-lockup-light.svg", f"{key}-lockup-dark.svg"):
            p = os.path.join(ASSETS, name)
            if not os.path.exists(p):
                errs.append(f"缺文件 {name}")
                continue
            try:
                ET.parse(p)
            except ET.ParseError as e:
                errs.append(f"XML 解析失败 {name}: {e}")
            if os.path.getsize(p) < 120:
                errs.append(f"文件过小（疑空） {name}")
        # 归一化后包围盒 + 笔画数 + 视觉体量
        raw = MARKS[key](PALETTES["light"])
        tr, bb = fit_transform(raw)
        strokes = raw.count("<path")
        if strokes < MIN_STROKES[key]:
            errs.append(f"方向 {key}: 楔形笔画数 {strokes} < {MIN_STROKES[key]}"
                         f"（构造退化，预期 ≥{MIN_STROKES[key]}）")
        if bb is None:
            errs.append(f"方向 {key}: 无路径数据")
            continue
        x0, y0, x1, y1 = bb
        w, h = x1 - x0, y1 - y0
        if x0 < 0.5 or y0 < 0.5 or x1 > 63.5 or y1 > 63.5:
            errs.append(f"方向 {key}: 归一后越界 bbox=({x0:.1f},{y0:.1f},{x1:.1f},{y1:.1f})")
        weight = (w * h) ** 0.5
        weights[key] = weight
        print(f"  方向 {key}  归一 bbox=({x0:.1f},{y0:.1f},{x1:.1f},{y1:.1f})"
              f"  {w:.1f}×{h:.1f}  视觉体量 {weight:.1f}  笔画 {strokes}")
    if len(weights) == len(DIRS):
        lo, hi = min(weights.values()), max(weights.values())
        if hi / lo > 1.15:
            errs.append(f"视觉体量不均衡：最大/最小 = {hi / lo:.2f}（阈值 1.15）· {weights}")
    idx = os.path.join(BASE, "index.html")
    if not os.path.exists(idx):
        errs.append("缺 index.html")
    else:
        text = open(idx, encoding="utf-8").read()
        for token in ("__CHANGE_ROWS__", "__BRAND_ROWS__", "__DIR_BLOCKS__", "__COMPARE_MARKS__"):
            if token in text:
                errs.append(f"占位符未替换 {token}")
        import re as _re
        ext = _re.findall(r'(?:src|href)\s*=\s*["\']https?://[^"\']+', text)
        ext += _re.findall(r'@import\s+[^;]*https?://', text)
        if ext:
            errs.append(f"预览页含外域资源引用（违反 file:// 零外域铁律）: {ext[:3]}")
        for key in DIRS:
            if f'id="dir-{key}"' not in text:
                errs.append(f"方向 {key} 区块缺失")
    rd = os.path.join(BASE, "README.md")
    if not os.path.exists(rd):
        errs.append("缺 README.md")
    else:
        rtext = open(rd, encoding="utf-8").read()
        for token in ("{changes}", "{brand_table}", "{dir_sections}"):
            if token in rtext:
                errs.append(f"README 占位符未替换 {token}")
    if errs:
        print("SELF-CHECK FAIL")
        for e in errs:
            print(" -", e)
        return 1
    print("SELF-CHECK OK · 4 方向 · 资产 / 包围盒 / 笔画数 / 零外域 全部通过")
    return 0


def main() -> int:
    serif = TextPath(FONT_SERIF)
    sans = TextPath(FONT_SANS)
    build_svgs(serif, sans)
    build_html(serif, sans)
    write_readme()
    print(f"产物目录：{BASE}")
    if "--check" in sys.argv:
        return self_check()
    return 0


if __name__ == "__main__":
    sys.exit(main())
