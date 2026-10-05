# -*- coding: utf-8 -*-
# _w673_fix_orphans.py — W673 WP-2.4：孤立选择器/裸标签残缺行删除（84 处扫描命中 + footer./.detail- 连带残缀）。
# 方案：docs/superpowers/plans/2026-10-05-site-quality-remediation-plans.md §四 WP-2.4
# 规则：
# - 扫描命中行（附录 A 扫描器 2 同款内核）默认整行删除；
# - text-search 的 footer. 三连残缀：沿命中行向上/下扩展删除全部同文连续行；
# - header 孤立行同样向上/下扩展同文连续行（当前清单均为单行，扩展为防御）；
# - timeline 的 .detail- 族按方案「考古无果（detail-icon 自 v2.2.42 未改）→ 删除孤立行」处置，
#   含 @media 内扫描器豁免的残缀行（手动清单，随本脚本一并删）。
# 落盘后重跑扫描，残留即 FAIL。
#
# 用法：--dry-run | --apply
import argparse
import glob
import re

SEL_RE = re.compile(r"^\s*([.#][^{};]*|[a-zA-Z][\w-]*\.?)\s*$", re.I)

# .detail- 族手动处置清单：文件 -> 需删除的（块内行文本 strip 后）行集合上下文锚
DETAIL_FILES = {"site/data/timeline.html", "site/en/timeline.html"}


def scan_block(block):
    hits = []
    lines = block.split("\n")
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s or not SEL_RE.match(ln) or s.endswith(","):
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and "{" in lines[j]:
            hits.append((i, s[:60]))
    return hits


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    files = sorted(glob.glob("site/data/*.html") + glob.glob("site/en/*.html"))
    total = 0
    fails = 0
    for f in files:
        with open(f, encoding="utf-8", newline="") as fh:
            src = fh.read()
        spans = [(m.start(1), m.end(1), m.group(1)) for m in re.finditer(r"<style[^>]*>(.*?)</style>", src, re.S | re.I)]
        # 收集待删行：{(span_idx, line_idx)}
        kills = set()
        extra = 0
        for si, (a, b, blk) in enumerate(spans):
            hits = scan_block(blk)
            if not hits:
                continue
            if f in DETAIL_FILES:
                # .detail- 族：删除全部 strip == '.detail-' 的行（含 @media 内豁免行）
                lines = blk.split("\n")
                for i, ln in enumerate(lines):
                    if ln.strip() == ".detail-":
                        kills.add((si, i))
                        extra += 1
                for (i, s) in hits:
                    kills.add((si, i))
                continue
            for (i, s) in hits:
                kills.add((si, i))
                # 同文连续残缀行扩展（footer./header 类裸标签连排）
                lines = blk.split("\n")
                core = s
                j = i - 1
                while j >= 0 and lines[j].strip() == core:
                    kills.add((si, j)); extra += 1; j -= 1
                j = i + 1
                while j < len(lines) and lines[j].strip() == core:
                    kills.add((si, j)); extra += 1; j += 1
        if not kills:
            continue
        total += len(kills)
        parts = []
        for si, (a, b, blk) in enumerate(spans):
            dead = sorted(i for (s2, i) in kills if s2 == si)
            if not dead:
                continue
            lines = blk.split("\n")
            base = src[:a].count("\n") + 1
            for i in dead:
                print("%s:%d DEL %s" % (f, base + i, lines[i].strip()[:60]))
            keep = [ln for i, ln in enumerate(lines) if i not in set(dead)]
            parts.append((a, b, "\n".join(keep)))
        out = []
        pos = 0
        for (a, b, newblk) in parts:
            out.append(src[pos:a])
            out.append(newblk)
            pos = b
        out.append(src[pos:])
        s2 = "".join(out)
        rest = sum(len(scan_block(x[2])) for x in
                   [(m.start(1), m.end(1), m.group(1)) for m in re.finditer(r"<style[^>]*>(.*?)</style>", s2, re.S | re.I)])
        if rest:
            fails += 1
            print("FAIL %s: 修复后残留 %d" % (f, rest))
            continue
        if extra:
            print("  +%d 连带残缀行（同文扩展）" % extra)
        if args.apply:
            with open(f, "w", encoding="utf-8", newline="") as fh:
                fh.write(s2)
    print("=== 删除行 %d（含连带） · 失败文件 %d ===" % (total, fails))
    if fails:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
