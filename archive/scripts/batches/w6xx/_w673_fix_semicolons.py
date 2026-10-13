# -*- coding: utf-8 -*-
# _w673_fix_semicolons.py — W673 WP-2.3：CSS 缺分号机械修复（442 处 = 换行形态 + 同行形态）。
# 方案：docs/superpowers/plans/2026-10-05-site-quality-remediation-plans.md §四 WP-2.3
# 判定内核与方案附录 A 扫描器 1 同款（同行双通道 + 换行形态，规则末条豁免）；
# 修复：换行形态在声明行尾补 ;；同行形态在被吞属性名前插 ;。CRLF 逐行保持原行尾。
# 落盘后逐文件重跑判定，残留即 FAIL。
#
# 用法：--dry-run 输出逐处前后片段；--apply 落盘。
import argparse
import glob
import re

PROP_RE = re.compile(r"^\s*(--[-\w]|[-\w]+\s*):.*\S")
DECL_RE = re.compile(r"([-\w]+)\s*:\s*")


def find_style_spans(src):
    return [(m.start(1), m.end(1), m.group(1)) for m in re.finditer(r"<style[^>]*>(.*?)</style>", src, re.S | re.I)]


def scan_block(block):
    """返回 [(行内索引 line_idx, kind)]。判定在「剥离 CSS 注释（保换行）」后的文本上进行——
    与方案附录 A 扫描器 1 同款；行号与原始块对齐（keep_nl 保换行），修复作用于原始行。"""
    def keep_nl(mm):
        return re.sub(r"[^\n]", " ", mm.group(0))
    stripped_block = re.sub(r"/\*.*?\*/", keep_nl, block, flags=re.S)
    hits = []
    lines = stripped_block.split("\n")
    hit_lines = set()
    depth = 0
    for i, ln in enumerate(lines):
        if depth > 0:
            if has_same_line_defect(ln):
                hits.append((i, "same-line"))
                hit_lines.add(i)
        if "{" in ln:
            if has_same_line_defect(ln[ln.rfind("{") + 1:]):
                if i not in hit_lines:
                    hits.append((i, "same-line"))
                    hit_lines.add(i)
        depth += ln.count("{") - ln.count("}")
    for i, ln in enumerate(lines):
        if i in hit_lines:
            continue
        s = ln.rstrip()
        if not PROP_RE.match(s) or s.endswith((";", "{", "}", ",", "(", ":")):
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j >= len(lines):
            continue
        nxt = lines[j].strip()
        if nxt.startswith("}"):
            continue
        if PROP_RE.match(nxt) and not nxt.startswith(("@", "<")):
            hits.append((i, "newline"))
    return hits


def has_same_line_defect(text):
    cs = [(x.start(), x.group(1)) for x in DECL_RE.finditer(text)]
    for (p1, n1), (p2, n2) in zip(cs, cs[1:]):
        seg = text[p1:p2]
        if ";" not in seg and "{" not in seg and "}" not in seg:
            return True
    return False


def fix_line(ln, kind):
    """返回修复后的行（保留原行尾）。"""
    eol = ""
    body = ln
    while body.endswith("\r") or body.endswith("\n"):
        eol = body[-1] + eol
        body = body[:-1]
    if kind == "newline":
        return body.rstrip() + ";" + eol
    # same-line：从右向左在每个缺陷对第二属性名前插 "; "
    cs = [(x.start(), x.group(1)) for x in DECL_RE.finditer(body)]
    inserts = []
    for (p1, n1), (p2, n2) in zip(cs, cs[1:]):
        seg = body[p1:p2]
        if ";" not in seg and "{" not in seg and "}" not in seg:
            inserts.append(p2)
    for p in sorted(set(inserts), reverse=True):
        body = body[:p] + "; " + body[p:]
    return body + eol


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    files = sorted(glob.glob("site/data/*.html") + glob.glob("site/*.html") + glob.glob("site/en/*.html"))
    total = 0
    fails = 0
    for f in files:
        with open(f, encoding="utf-8", newline="") as fh:
            src = fh.read()
        spans = find_style_spans(src)
        file_hits = []
        for (a, b, blk) in spans:
            file_hits.extend((a, b, h) for h in scan_block(blk))
        if not file_hits:
            continue
        total += len(file_hits)
        # 按 span 分组，逐 span 一次性应用全部行修复（避免多命中互相覆盖）
        span_fixes = {}
        for (a, b, (line_idx, kind)) in file_hits:
            span_fixes.setdefault((a, b), []).append((line_idx, kind))
        parts = []
        for (a, b), fixes in span_fixes.items():
            lines = src[a:b].split("\n")
            base_line = src[:a].count("\n") + 1
            for (line_idx, kind) in fixes:
                old = lines[line_idx]
                new = fix_line(old, kind)
                print("%s:%d [%s] %s -> %s" % (f, base_line + line_idx, kind,
                                               old.strip()[:64], new.strip()[:64]))
                lines[line_idx] = new
            parts.append((a, b, "\n".join(lines)))
        # 重组（spans 从前到后，逐段替换）
        out = []
        pos = 0
        for (a, b, newblk) in parts:
            out.append(src[pos:a])
            out.append(newblk)
            pos = b
        out.append(src[pos:])
        s2 = "".join(out)
        # 自断言：重跑判定必须为 0
        rest = sum(len(scan_block(x[2])) for x in find_style_spans(s2))
        if rest:
            fails += 1
            print("FAIL %s: 修复后残留 %d" % (f, rest))
            continue
        if args.apply:
            with open(f, "w", encoding="utf-8", newline="") as fh:
                fh.write(s2)
    print("=== 总命中 %d · 失败文件 %d ===" % (total, fails))
    if fails:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
