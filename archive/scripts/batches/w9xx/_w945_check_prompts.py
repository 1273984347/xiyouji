# -*- coding: utf-8 -*-
"""_w945_check_prompts.py — 出图前母版一致性校验

判据：8 条 prompt 的「风格母版」（提示词中「主体：」之前的全部内容）必须**逐字相同**；
      aspect_ratio / resolution 必须全部一致；单条 prompt 内不得出现换行或控制字符。
不通过 ⇒ exit 2（禁止出图，防止成套风格脱节）。
"""
import io
import json
import os
import sys

REPO = r"D:\xiyouji"
FILES = [
    os.path.join(REPO, "scripts", "output", "_w945_batch1.json"),
    os.path.join(REPO, "scripts", "output", "_w945_batch2.json"),
    os.path.join(REPO, "scripts", "output", "_w945_batch3.json"),
    os.path.join(REPO, "scripts", "output", "_w948_batch1.json"),
    os.path.join(REPO, "scripts", "output", "_w948_batch2.json"),
    os.path.join(REPO, "scripts", "output", "_w948_batch3.json"),
]

errs = []
masters = []
rows = []
for f in FILES:
    if not os.path.exists(f):
        continue
    data = json.load(io.open(f, encoding="utf-8"))
    for i, r in enumerate(data["requests"]):
        p = r.get("prompt", "")
        if "主体：" not in p:
            errs.append("%s#%d prompt 缺少「主体：」标记" % (os.path.basename(f), i))
            continue
        m = p.split("主体：")[0]
        masters.append(m)
        rows.append((os.path.basename(f), i, r.get("output_file"), r.get("aspect_ratio"),
                     r.get("resolution"), len(p)))
        if r.get("aspect_ratio") != "3:4":
            errs.append("%s#%d aspect_ratio=%s（应为 3:4）" % (f, i, r.get("aspect_ratio")))
        if r.get("resolution") != "2K":
            errs.append("%s#%d resolution=%s（应为 2K）" % (f, i, r.get("resolution")))
        if "\n" in p or "\r" in p:
            errs.append("%s#%d prompt 含换行" % (f, i))

if len(masters) < 8:
    errs.append("prompt 条数 = %d（应 ≥ 8）" % len(masters))
else:
    base = masters[0]
    for i, m in enumerate(masters[1:], start=1):
        if m != base:
            errs.append("第 %d 条的风格母版与第 1 条不一致（母版长度 %d vs %d）" % (i + 1, len(m), len(base)))
            for a, b in zip(base.split("。"), m.split("。")):
                if a != b:
                    errs.append("  差异句：基准「%s」 vs 本条「%s」" % (a[:60], b[:60]))
                    break

print("== 母版一致性校验 ==")
for fn, i, of, ar, rs, ln in rows:
    print(" - %s#%d  %-28s %s %s  prompt=%d 字" % (fn, i, of, ar, rs, ln))
print("母版长度 = %d 字符（逐字相同）" % len(masters[0]) if masters else "无母版")
print("母版全文：\n%s" % (masters[0] if masters else ""))

if errs:
    print("\n== FAIL ==")
    for e in errs:
        print(" -", e)
    sys.exit(2)
print("\n== PASS：%d 条母版逐字一致·画幅/分辨率统一 ==" % len(masters))
