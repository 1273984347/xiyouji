"""containment_block_scan.py — 包含块退化族静态扫描（CSS 特性 × fixed/sticky 规则交叉面）

    用法：python scripts/containment_block_scan.py（只读报告）
    固化来源：tmpe/w1146（W1146 举一反三扫描·报告=docs/11-方案报告/审查与评审/包含块退化族举一反三扫描报告-2026-11-06.md）

    W1220 性能根修（pytest 最慢三项全由本脚本贡献·占全量 66%）：
      ① 扫描逻辑移入 main() + `if __name__ == "__main__"` 守卫——原实现在 **import 期**
         就跑全量扫描（86–93s/次），两个用例仅 import 即付两遍全站扫描成本；
      ② 只扫 `<style>` 块而不是整份 HTML——原实现把内联 `<script>`/SVG 里的 JS 对象
         字面量花括号也当 CSS 规则解析（假阳性），且扫描体量随页面内联脚本膨胀。
"""
import glob
import re
import sys

BLOCKING = re.compile(
    r"(?:^|;)\s*(?:backdrop-filter|-webkit-backdrop-filter|filter|transform|perspective|will-change|contain)\s*:\s*([^;]+)", re.I)
NONNONE = re.compile(r"none", re.I)
FIXEDPOS = re.compile(r"position:\s*(fixed|sticky)", re.I)
STYLE_BLOCK = re.compile(r"<style\b[^>]*>(.*?)</style>", re.I | re.S)

CSS_FILES = ["site/system.css", "site/tokens.css"]
HTML_FILES = sorted(
    glob.glob("site/*.html") + glob.glob("site/data/*.html") + glob.glob("site/en/*.html"))


def _css_sources():
    """产出 (文件, CSS 文本)：CSS 正本取全文；HTML 只取其中的 <style> 块正文。"""
    for f in CSS_FILES:
        yield f, open(f, encoding="utf-8", errors="ignore").read()
    for f in HTML_FILES:
        html = open(f, encoding="utf-8", errors="ignore").read()
        for m in STYLE_BLOCK.finditer(html):
            yield f, m.group(1)


def main():
    block_rules = {}   # (file, selector) -> 特性
    fixed_rules = {}   # (file, selector) -> position
    for f, s in _css_sources():
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
