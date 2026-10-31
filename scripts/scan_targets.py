#!/usr/bin/env python3
"""W941 · UI 图标位 emoji 基准扫描器（机检判据·独立于替换逻辑）

产出 scripts/output/_w939_targets.json：
  reader_main : {files: [...], total_hits: N}   ← 615 个阅读页的三处主形态（收藏/赞/踩）
  scattered   : [ {file, line, cat, chars, snippet}, ... ]  ← 零散图标位逐条明细
  inline      : 全部 UI 图标位命中总数（复验用：治理后须为 0）

判据（承 W941 勘察脚本 tmpe/_scan_emoji_icon.py·已独立实现）：
  A control-icon  交互控件（button/a/role=button/div[role=button]）文本首位是具象字符
  B slot-icon     class/name 含 icon|emoji|ico|glyph|symbol|badge|avatar|mark 的元素内含具象字符
  C title-prefix  标题类（h1-h6/th/legend/dt/option/li）文本首位是具象字符
  D css-content   CSS content 属性里含具象字符
  E body-text     其余（正文装饰·不在治理范围）

「具象字符」定义：emoji 表情码位 + 几何/dingbat 图形（★☆✓✗⚠❝▶⏸☰✕）
★ 排除箭头 ←→↔↺↑↓⇒ 与 VS16（箭头承担正文流程语义·非图标）
用法：py -3 scripts/scan_targets.py [--json <out>]
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re

# ---- 表情码位（真 emoji）----
PICTO = re.compile(
    "["
    "\U0001F000-\U0001FAFF"
    "\u2728\u274C\u2705\u26A1\u2B50\u2934\u2935\u3030\u303D\u3297\u3299"
    "\u203C\u2049\u00A9\u00AE"
    "]"
)
# ---- 符号码位（几何 / dingbat）----
SYM = re.compile(
    "["
    "\u2190-\u21FF"
    "\u2300-\u23FF"
    "\u2600-\u27BF"
    "\u2B00-\u2BFF"
    "]"
)
VS16 = "\uFE0F"
ARROWS = {"\u2190", "\u2192", "\u2194", "\u21ba", "\u2191", "\u2193", "\u21d2", "\u21d0", "\u21d4"}
# 纯符号（非图形）—— 排除
NON_GRAPHIC = set("\u00a7\u00b6\u2022\u2026\u00b7\u2014\u2013\u2018\u2019\u201c\u201d\u2032\u2033")

SRC_SUFFIX = {".html", ".htm", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".vue", ".css"}
SCAN_ROOTS = ["site", "xiyouji-agent-web/src", "xiyouji-desktop/src", "assets/promo"]

CONTROL_TAGS = {"button", "a", "summary", "label"}
TITLE_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "th", "legend", "dt", "option", "li", "summary"}
SLOT_HINT = re.compile(r"icon|emoji|ico|glyph|symbol|badge|avatar|mark", re.I)

TAG_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9:-]*)((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>")
CSS_CONTENT_RE = re.compile(r"content\s*:\s*[\"']([^\"']*)[\"']")

# 阅读页三处主形态（615 页完全统一·由勘察实证）
READER_MAIN = [
    re.compile(r'data-act="bookmark"[^>]*>\s*\u2606\s*收藏本页'),
    re.compile(r'>\s*\U0001F44d\s*有帮助\s*</a>'),
    re.compile(r'>\s*\U0001F44e\s*待改进\s*</a>'),
]


def split_picto_sym(text: str) -> tuple[set[str], set[str]]:
    """返回 (表情集合, 符号集合)。带 VS16 的 dingbat 按表情计。"""
    pico, syms = set(), set()
    for m in PICTO.finditer(text):
        pico.add(m.group(0))
    for m in SYM.finditer(text):
        ch = m.group(0)
        if ch == VS16:
            continue
        nxt = text[m.end():m.end() + 1]
        prev = text[m.start() - 1:m.start()] if m.start() > 0 else ""
        if nxt == VS16 or prev == VS16:
            pico.add(ch)
        else:
            syms.add(ch)
    return pico, syms


def graphic_chars(text: str) -> set[str]:
    """具象图形字符集（表情 + 几何符号），排除箭头 / 纯符号 / VS16。"""
    if not CAND_RE.search(text):
        return set()
    pico, syms = split_picto_sym(text)
    out = set()
    for c in pico | syms:
        if c in ARROWS or c in NON_GRAPHIC or c == VS16:
            continue
        out.add(c)
    return out


def classify_file(text: str):
    cats = collections.Counter()
    hits = []
    covered = [False] * len(text)

    for m in TAG_RE.finditer(text):
        tag = m.group(1).lower()
        attrs = m.group(2) or ""
        start = m.end()
        nxt = text.find("<", start)
        inner = text[start:nxt if nxt != -1 else len(text)]
        if not inner.strip():
            continue
        stripped = inner.lstrip()
        mfirst = EMOJI_LEAD.search(stripped[:4])
        is_lead = bool(mfirst) and mfirst.start() == 0
        if not (is_lead or SLOT_HINT.search(attrs)):
            continue
        cat = None
        if is_lead and (tag in CONTROL_TAGS or "role" in attrs and "button" in attrs):
            cat = "A control-icon"
        elif SLOT_HINT.search(attrs):
            cat = "B slot-icon"
        elif is_lead and tag in TITLE_TAGS:
            cat = "C title-prefix"
        if cat is None:
            continue
        gchars = graphic_chars(stripped)
        if not gchars:
            continue
        cats[cat] += 1
        line = text.count("\n", 0, m.start()) + 1
        hits.append({
            "line": line,
            "cat": cat,
            "tag": tag,
            "chars": "".join(sorted(graphic_chars(stripped))),
            "snippet": re.sub(r"\s+", " ", stripped)[:80],
        })
        for i in range(m.start(), nxt if nxt != -1 else len(text)):
            covered[i] = True

    for m in CSS_CONTENT_RE.finditer(text):
        if graphic_chars(m.group(1)):
            cats["D css-content"] += 1
            hits.append({
                "line": text.count("\n", 0, m.start()) + 1,
                "cat": "D css-content",
                "tag": "css",
                "chars": "".join(sorted(graphic_chars(m.group(1)))),
                "snippet": m.group(1)[:80],
            })
            for i in range(m.start(), m.end()):
                covered[i] = True

    for lineno, line in enumerate(text.split("\n"), 1):
        if not CAND_RE.search(line):
            continue
        gc = graphic_chars(line)
        if not gc:
            continue
        idxs = [i for i, ch in enumerate(line) if ch in gc]
        if idxs and all(covered[i] for i in idxs):
            continue
        cats["E body-text"] += 1
        hits.append({
            "line": lineno,
            "cat": "E body-text",
            "tag": "-",
            "chars": "".join(sorted(graphic_chars(line))),
            "snippet": re.sub(r"\s+", " ", line.strip())[:80],
        })
    return cats, hits


EMOJI_LEAD = re.compile("[" + PICTO.pattern[1:-1] + SYM.pattern[1:-1] + "]")
# 快速预筛：任一候选码位出现即需精算
CAND_RE = re.compile("[" + PICTO.pattern[1:-1] + SYM.pattern[1:-1] + VS16 + "]")


def scan(roots: list[str]):
    reader_files: set[str] = set()
    reader_hits = 0
    scattered = []
    inline_total = 0
    body_total = 0
    per_cat = collections.Counter()

    for root in roots:
        p = pathlib.Path(root)
        if not p.exists():
            continue
        for f in sorted(p.rglob("*")):
            if not (f.is_file() and f.suffix.lower() in SRC_SUFFIX):
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            lines = text.split("\n")
            cats, hits = classify_file(text)
            fp = str(f).replace("\\", "/")
            for h in hits:
                if h["cat"] == "E body-text":
                    body_total += 1
                    continue
                inline_total += 1
                per_cat[h["cat"]] += 1
                ln = h["line"]
                ctx = "\n".join(lines[max(0, ln - 3):ln + 2])
                if any(rx.search(ctx) for rx in READER_MAIN):
                    reader_files.add(fp)
                    reader_hits += 1
                    continue
                h["file"] = fp
                scattered.append(h)
    return {
        "reader_main": {"files": sorted(reader_files), "total_hits": reader_hits},
        "scattered": scattered,
        "inline_total": inline_total,
        "body_total": body_total,
        "per_cat": dict(per_cat),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="scripts/output/_w939_targets.json")
    ap.add_argument("--roots", nargs="*", default=SCAN_ROOTS)
    args = ap.parse_args()

    res = scan(args.roots)
    out = pathlib.Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

    print("=" * 70)
    print(f"reader_main : {len(res['reader_main']['files'])} 文件 / {res['reader_main']['total_hits']} 命中")
    print(f"scattered   : {len(res['scattered'])} 条")
    print(f"UI 图标位合计: {res['inline_total']}   正文(body-text): {res['body_total']}")
    print(f"分类: {res['per_cat']}")
    print(f"→ {out}")
    print("=" * 70)
    for h in res["scattered"]:
        print(f"  {h['file']}:{h['line']}  [{h['cat']}]  {h['chars']}  :: {h['snippet'][:72]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
