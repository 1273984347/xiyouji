# -*- coding: utf-8 -*-
"""_w1043_derive_verify.py — 由归档的 _w1018_verify.py **程序化派生** W1043 落位验收

派生纪律（坑表 E-37）：程序化派生 + 残留断言；期望值**按当批实算**（坑表 E-36）：
  · 有配图 44 → 56 回（44 + 本批 12）
  · 缺口   56 → 44 回（其中通用 og 54 → 42 + 既有 card-* 专属 2）
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
SRC = os.path.join(REPO, "archive", "scripts", "batches", "w10xx", "_w1018_verify.py")
DST = os.path.join(REPO, "archive", "scripts", "batches", "w10xx", "_w1043_verify.py")

REPO_EXPR = ("REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(\n"
             "    os.path.dirname(os.path.abspath(__file__))))))")

JOBS = '''JOBS = [
    ("ch053", "plate-line-85-ch053-ruyizhenxian.webp"), ("ch033", "plate-line-86-ch033-chuikouxian.webp"),
    ("ch094", "plate-line-87-ch094-taiyinxingjun.webp"), ("ch073", "plate-line-88-ch073-duomuguai.webp"),
    ("ch069", "plate-line-89-ch069-ziyangzhenren.webp"), ("ch090", "plate-line-90-ch090-yijiukutianzun.webp"),
    ("ch071", "plate-line-91-ch071-jiuling-shiba.webp"), ("ch086", "plate-line-92-ch086-bihan-bishu.webp"),
    ("ch095", "plate-line-93-ch095-yumian.webp"), ("ch029", "plate-line-94-ch029-bengpo-baboren.webp"),
    ("ch085", "plate-line-95-ch085-diyongfuren.webp"), ("ch097", "plate-line-96-ch097-xiniu.webp"),
]'''

text = io.open(SRC, encoding="utf-8").read()
text = text.replace(
    'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))', REPO_EXPR)
text = text.replace("_w1018_verify.py", "_w1043_verify.py")
text = text.replace("W1018 落位验收", "W1043 落位验收")
text = text.replace("④ 缺口复算：100 回中已有配图 20→32 回、缺口 80→68 回",
                    "④ 缺口复算：100 回中已有配图 44→56 回、缺口 56→44 回")
text = text.replace("⑤ **未覆盖页未回归**：其余 68 页",
                    "⑤ **未覆盖页未回归**：其余 44 页")
text = text.replace("其余 68 页的 og:image 仍为落位前的取值（66 通用图 + 2 张既有 card-* 专属）",
                    "其余 44 页的 og:image 仍为落位前的取值（42 通用图 + 2 张既有 card-* 专属）")

m = re.search(r"JOBS = \[.*?\n\]", text, re.S)
if not m:
    print("FAIL  源脚本未找到 JOBS 块")
    raise SystemExit(1)
text = text[:m.start()] + JOBS + text[m.end():]

# 期望值按当批实算替换（当批实况：**11** 回新增题图 + ch086 已有旧题图 ⇒ 只换 og）
#   有配图 44 → 55 · 缺口 56 → 45（通用 og 54 → 43 + 既有 card-* 专属 2）
text = text.replace("if len(covered) != 44:", "if len(covered) != 55:")
text = text.replace('fails.append("有配图回数 %d ≠ 32（期望 32+12）" % len(covered))',
                    'fails.append("有配图回数 %d ≠ 55（期望 44+11·ch086 已有旧题图只换 og）" % len(covered))')
text = text.replace("if len(gap) != 56:", "if len(gap) != 45:")
text = text.replace('fails.append("缺口 %d ≠ 68" % len(gap))',
                    'fails.append("缺口 %d ≠ 45" % len(gap))')
text = text.replace("if len(generic) != 54:", "if len(generic) != 43:")
text = text.replace('fails.append("缺口中通用 og 页 %d ≠ 66" % len(generic))',
                    'fails.append("缺口中通用 og 页 %d ≠ 43" % len(generic))')
text = text.replace("④ 缺口复算：100 回中已有配图 44→56 回、缺口 56→44 回",
                    "④ 缺口复算：100 回中已有配图 44→55 回、缺口 56→45 回")
text = text.replace("⑤ **未覆盖页未回归**：其余 44 页", "⑤ **未覆盖页未回归**：其余 45 页")
text = text.replace("其余 44 页的 og:image 仍为落位前的取值（42 通用图 + 2 张既有 card-* 专属）",
                    "其余 45 页的 og:image 仍为落位前的取值（43 通用图 + 2 张既有 card-* 专属）")

# --- 暗色规则判据**脆性**修（W1043 实测：页面 CSS 为多行 ⇒ 字面量整串不匹配 ⇒ 误判缺规则）---
text = text.replace(
    "DARK_RULE = 'html[data-theme=\"dark\"] .chapter-plate { display: none; }'",
    "DARK_RULE = 'html[data-theme=\"dark\"] .chapter-plate { display: none; }'\n"
    "# W1043：原判据用**整串字面量**匹配 ⇒ 页面 CSS 为多行排版时误判「缺暗色隐藏规则」\n"
    "# （实测 ch090 等 8 页明明含该规则却被判红）⇒ 改为容忍空白的正则（坑表 puti-shouye 第 5 条：\n"
    "#   判据禁止依赖脆弱特征）\n"
    "RE_DARK_RULE = re.compile(r'html\\[data-theme=\"dark\"\\]\\s*\\.chapter-plate\\s*\\{[^}]*display:\\s*none')")
text = text.replace(
    '        if mp.group(1).split("/")[-1] != site_name:\n'
    '            fails.append("%s 题图 src=%s ≠ %s" % (ch, mp.group(1), site_name))',
    '        if ch not in PREEXISTING and mp.group(1).split("/")[-1] != site_name:\n'
    '            fails.append("%s 题图 src=%s ≠ %s" % (ch, mp.group(1), site_name))\n'
    '        if ch in PREEXISTING:\n'
    '            notes.append("      %s 已有旧题图（%s）⇒ 本批只换 og:image·题图不覆盖"\n'
    '                         % (ch, mp.group(1).split("/")[-1]))')
text = text.replace(
    '        if DARK_RULE not in s.replace("  ", " "):\n'
    '            if \'html[data-theme="dark"] .chapter-plate { display: none; }\' not in s:\n'
    '                fails.append("%s 缺暗色隐藏规则" % ch)',
    '        if not RE_DARK_RULE.search(s):\n'
    '            fails.append("%s 缺暗色隐藏规则" % ch)')

# --- ① 题图断言：ch086 已有旧题图 ⇒ 只断言 og 已换（不判题图 src 指向本批站点版）---
text = text.replace(
    'JOBS = [',
    '# W1043：ch086 已有 W1001 批旧题图（plate-line-70-...-bichandawang）⇒ 本批**只换 og**·\n'
    '# 题图不覆盖（该回已有一张·同页两题图不被落位脚本支持）⇒ 断言对该回放宽。\n'
    'PREEXISTING = {"ch086"}\n\nJOBS = [', 1)

for bad in ("_w1018", "huxianfeng"):
    if bad in text:
        print("FAIL  派生产物残留源常量：%s" % bad)
        raise SystemExit(1)

ch_list = re.findall(r'\("(ch\d{3})",', text)
if len(ch_list) != 12 or len(set(ch_list)) != 12:
    print("FAIL  JOBS 回号异常：%d 条·唯一 %d" % (len(ch_list), len(set(ch_list))))
    raise SystemExit(1)

io.open(DST, "w", encoding="utf-8", newline="\n").write(text)
print("OK    派生 %s（%d 字符·JOBS 12 条·期望值 56/44/42）"
      % (os.path.relpath(DST, REPO).replace("\\", "/"), len(text)))
