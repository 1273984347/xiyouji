"""containment_block_scan.py — 包含块退化族静态扫描（CSS 特性 × fixed/sticky 规则交叉面）

    用法：python scripts/containment_block_scan.py（只读报告）
    固化来源：tmpe/w1146（W1146 举一反三扫描·报告=docs/11-方案报告/审查与评审/包含块退化族举一反三扫描报告-2026-11-06.md）
    """
import glob
import re

BLOCKING = re.compile(
    r"(?:^|;)\s*(?:backdrop-filter|-webkit-backdrop-filter|filter|transform|perspective|will-change|contain)\s*:\s*([^;]+)", re.I)
NONNONE = re.compile(r"none", re.I)
FIXEDPOS = re.compile(r"position:\s*(fixed|sticky)", re.I)

css_files = ["site/system.css", "site/tokens.css"] + sorted(
    glob.glob("site/*.html") + glob.glob("site/data/*.html") + glob.glob("site/en/*.html"))

block_rules = {}   # (file, selector) -> 特性
fixed_rules = {}   # (file, selector) -> position
for f in css_files:
    s = open(f, encoding="utf-8", errors="ignore").read()
    # 去掉注释与 @media 前缀噪声（保留选择器体）
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    for m in re.finditer(r"([^{}]+)\{([^}]*)\}", s):
        sel = re.sub(r"\s+", " ", m.group(1)).strip()[-90:]
        body = m.group(2)
        for bm in BLOCKING.finditer(body):
            val = bm.group(1).strip()
            if NONNONE.fullmatch(val) or val == "":
                continue
            # will-change 只关心变换类值
            if bm.group(0).lower().startswith("will-change") and not re.search(
                    r"transform|perspective|filter|top|left|right|bottom", val, re.I):
                continue
            key = (f, sel[:80])
            block_rules.setdefault(key, set()).add(bm.group(0).split(":")[0].strip())
        for fm in FIXEDPOS.finditer(body):
            key = (f, sel[:80])
            fixed_rules[key] = fm.group(1)

print("== 创建包含块的规则数（去重选择器）==")
sels = {}
for (_f, sel), feats in block_rules.items():
    sels.setdefault(sel, set()).update(feats)
for sel, feats in sorted(sels.items()):
    print("  [%s] %s" % (",".join(sorted(feats)), sel))
print("\n== fixed/sticky 规则（去重）==")
fsels = {}
for (_f, sel), pos in fixed_rules.items():
    fsels.setdefault(sel, pos)
for sel, pos in sorted(fsels.items()):
    print("  [%s] %s" % (pos, sel))
print("\n统计：包含块规则选择器 %d 个 · fixed/sticky 规则选择器 %d 个" % (len(sels), len(fsels)))
