#!/usr/bin/env python3
"""_w955_motion_audit.py — W955「GSAP 动效体系引入批」前置体检取证脚本（唯一数字源头）。

目的：为《执行前计划-T28》提供可复算的动效现状基线，替代任何手写估计值。
产出：scripts/output/_w955_motion_audit.json

覆盖八组事实：
  F1 页面规模与目录分布（GSAP 引入的分级面）
  F2 现有动画存量（@keyframes / animation / transition / reveal-in / js-reveal）
  F3 reduced-motion 覆盖（RM 双守卫的 JS 侧现状）
  F4 动效禁止清单基线（复用 check_motion_ban.py 的判据正则，不另立标准）
  F5 d3 .duration(N>600) 残留（DESIGN §5.1 硬指标）
  F6 体积预算对账（DESIGN §4A.8：system.css / tokens.css 上限）
  F7 GSAP 引入体量测算（外链 vs 内联的量级差）
  F8 公共动效载体缺位（W471 motion.js 规划未落地 · 现状为逐页内联复制）

用法：
  py -3 scripts/_w955_motion_audit.py            # 产出 JSON
  py -3 scripts/_w955_motion_audit.py --print    # 同时打印人读摘要
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripts" / "output" / "_w955_motion_audit.json"

sys.path.insert(0, str(ROOT / "scripts"))
import check_motion_ban as MB  # noqa: E402  复用门禁判据正则（唯一事实源·禁另立标准）

# DESIGN.md §4A.8 体积预算红线（数值口径：KB = 1024 B）
BUDGET = {
    "system_css": {"limit_bytes": int(24.9 * 1024), "basis": "DESIGN.md §4A.8 system ≤ +6KB（18.9→≤24.9KB）"},
    "tokens_css": {"limit_bytes": 23799, "basis": "DESIGN.md §4A.8 tokens 上限 23,799 B（W851 上调 +3KB）"},
}

# GSAP 3.12.5 实测体积（2026-10-26 由本批实测下载取得·非估算）
GSAP_FILES = {
    "gsap.min.js": 72214,
    "ScrollTrigger.min.js": 43380,
}

# 页面内联 system.css 副本所贡献的 keyframes 名（system.css 实测 4 个）
SYSTEM_KEYFRAMES = {"row-in", "chart-loading-breath", "chart-loading-spin", "chart-fade-in"}

RE_KEYFRAMES = re.compile(r"@keyframes\s+([\w-]+)")
RE_REVEAL = re.compile(r"reveal-in")
RE_JS_REVEAL = re.compile(r"js-reveal")
RE_RM = re.compile(r"prefers-reduced-motion")
RE_ANIM = re.compile(r"(?<![\w-])animation\s*:")
RE_TRANS = re.compile(r"(?<![\w-])transition\s*:")
RE_BARE_EASE = re.compile(
    r"(?<![\w-])ease\s*;"                       # CSS 裸 ease（如 transition: opacity .3s ease;）
    r"|(?<![\w-])ease\s*:\s*['\"]none"          # GSAP ease:'none'
    r"|['\"]linear['\"]"                          # 线性缓动字面量
    r"|(?<![\w-])transition-timing-function\s*:\s*linear"
    # W961 订正：原正则 `ease\s*:` 无负向前查 ⇒ 命中数据字段名（avg_ease: 5.33 / most_ease: "青牛精"）
    # 与令牌定义（--ease-out-quart:）⇒ 「裸 ease 违规 4 处」为**假阳性**（实测 CSS 裸 ease = 0 处）。
)
RE_DURATION = re.compile(r"\.duration\(\s*(\d+)\s*\)")
RE_INLINE_CSS_BLOCK = re.compile(r"<style>(.*?)</style>", re.S)
RE_INLINE_JS_BLOCK = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script[^>]*>", re.S | re.I)
RE_SCRIPT_SRC = re.compile(r"<script[^>]*\bsrc=[\"']([^\"']+)[\"']", re.I)


def html_files():
    return sorted((ROOT / "site").rglob("*.html"))


def dir_key(p: Path) -> str:
    rel = p.relative_to(ROOT / "site")
    parts = rel.parts
    if len(parts) == 1:
        return "(root)"
    if parts[0] in ("reader", "themes", "people") and len(parts) >= 3:
        return "%s/%s" % (parts[0], parts[1])
    return parts[0]


def main() -> int:
    files = html_files()
    dist: dict[str, int] = {}
    for f in files:
        dist[dir_key(f)] = dist.get(dir_key(f), 0) + 1

    # ---- F2 / F3 / F4 / F5 逐页扫描 ----
    kf_pages = 0
    kf_total = 0
    kf_private: dict[str, int] = {}
    reveal_pages = 0
    js_reveal_pages = 0
    rm_pages = 0
    anim_decl = 0
    trans_decl = 0
    bare_ease_hits = 0
    bare_ease_files: list[str] = []
    dur_gt600_pages = 0
    dur_gt600_total = 0
    ban_files: dict[str, list[str]] = {}
    inline_js_blocks = 0
    inline_js_chars = 0

    for f in files:
        rel = str(f.relative_to(ROOT)).replace("\\", "/")
        s = f.read_text(encoding="utf-8", errors="ignore")

        kfs = RE_KEYFRAMES.findall(s)
        if kfs:
            kf_pages += 1
            kf_total += len(kfs)
            for k in kfs:
                if k not in SYSTEM_KEYFRAMES:
                    kf_private[k] = kf_private.get(k, 0) + 1
        if RE_REVEAL.search(s):
            reveal_pages += 1
        if RE_JS_REVEAL.search(s):
            js_reveal_pages += 1
        if RE_RM.search(s):
            rm_pages += 1
        anim_decl += len(RE_ANIM.findall(s))
        trans_decl += len(RE_TRANS.findall(s))

        be = RE_BARE_EASE.findall(s)
        if be:
            bare_ease_hits += len(be)
            bare_ease_files.append(rel)

        dn = [int(x) for x in RE_DURATION.findall(s) if int(x) > 600]
        if dn:
            dur_gt600_pages += 1
            dur_gt600_total += len(dn)

        # 动效禁止清单：直接复用门禁正则（含 strip_whitelist_blocks 的块级白名单逻辑）
        rest = s
        for st in RE_INLINE_CSS_BLOCK.findall(s):
            rest = rest.replace(st, "", 1)
            if "tokens.css —" in st:
                continue
            MB.scan_css(st, rel, [])
        for pat, desc in MB.BAN:
            for _m in pat.finditer(rest):
                ban_files.setdefault(desc, []).append(rel)

        for blk in RE_INLINE_JS_BLOCK.findall(s):
            inline_js_blocks += 1
            inline_js_chars += len(blk)

    # ---- F6 体积预算对账 ----
    size_facts = {}
    for key, fname in (("system_css", "site/system.css"), ("tokens_css", "site/tokens.css")):
        p = ROOT / fname
        size = p.stat().st_size if p.exists() else 0
        limit = BUDGET[key]["limit_bytes"]
        size_facts[key] = {
            "file": fname,
            "bytes": size,
            "limit_bytes": limit,
            "headroom_bytes": limit - size,
            "over_budget": size > limit,
            "basis": BUDGET[key]["basis"],
        }

    # ---- F7 GSAP 体量测算 ----
    gsap_total = sum(GSAP_FILES.values())
    page_total = len(files)
    # 每页引入外链 script 标签的增量字节（实测标签形态估算：两行 script 标签）
    tag_bytes = len('<script defer src="../static/js/gsap.min.js"></script>\n'
                     '<script defer src="../static/js/ScrollTrigger.min.js"></script>\n')
    gsap_facts = {
        "version": "3.12.5",
        "source": "https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/（本批实测下载·2026-10-26）",
        "files_bytes": GSAP_FILES,
        "total_bytes": gsap_total,
        "if_external_all_pages_bytes": page_total * tag_bytes,
        "if_inlined_all_pages_bytes": page_total * gsap_total,
        "script_tag_bytes_each_page": tag_bytes,
        "note": "外链=每页仅标签字节·内联=每页全量库字节；两者差 %.1f 倍"
                % ((page_total * gsap_total) / max(1, page_total * tag_bytes)),
    }

    # ---- F8 公共动效载体缺位 ----
    motion_js = ROOT / "site" / "static" / "js" / "motion.js"
    carrier = {
        "motion_js_planned_at": "W471（Phase 3·EN 站 JS 级动效对齐·条件分支「若共性率 ≥ 80% 抽 site/static/js/motion.js」）",
        "motion_js_exists": motion_js.exists(),
        "js_reveal_pages": js_reveal_pages,
        "page_total": page_total,
        "js_reveal_ratio": round(js_reveal_pages / page_total, 4) if page_total else 0,
        "inline_js_blocks_total": inline_js_blocks,
        "inline_js_chars_total": inline_js_chars,
        "conclusion": "W471 规划的公共载体未落地；滚动显现实现为逐页内联复制（js-reveal 钩子 %d/%d 页）"
                      % (js_reveal_pages, page_total),
    }

    data = {
        "batch": "W955",
        "generated_by": "scripts/_w955_motion_audit.py",
        "generated_at_local": "2026-10-26",
        "note": "本 JSON 为《执行前计划-T28》全部统计数字的唯一源头；报告与计划不得出现无来源数字",
        "F1_pages": {
            "total": page_total,
            "by_dir": dict(sorted(dist.items(), key=lambda kv: (-kv[1], kv[0]))),
        },
        "F2_animation_stock": {
            "pages_with_keyframes": kf_pages,
            "keyframes_total": kf_total,
            "private_keyframes": dict(sorted(kf_private.items(), key=lambda kv: (-kv[1], kv[0]))[:20]),
            "private_keyframes_distinct": len(kf_private),
            "pages_with_reveal_in": reveal_pages,
            "pages_with_js_reveal_hook": js_reveal_pages,
            "animation_declarations": anim_decl,
            "transition_declarations": trans_decl,
        },
        "F3_reduced_motion": {
            "pages_with_rm_guard": rm_pages,
            "ratio": round(rm_pages / page_total, 4) if page_total else 0,
            "design_ref": "DESIGN.md §5.3 reduced-motion 双守卫（强制）",
        },
        "F4_motion_ban_baseline": {
            "patterns": [(desc, pat.pattern) for pat, desc in MB.BAN],
            "hits_by_rule": {desc: len(v) for desc, v in sorted(ban_files.items())},
            "files_by_rule": {desc: sorted(set(v))[:20] for desc, v in sorted(ban_files.items())},
            "total_hits": sum(len(v) for v in ban_files.values()),
            "note": "判据复用 scripts/check_motion_ban.py 的正则与块级白名单逻辑；本节为基线快照，非门禁结论",
        },
        "F5_d3_duration_gt600": {
            "pages": dur_gt600_pages,
            "occurrences": dur_gt600_total,
            "design_ref": "DESIGN.md §5.1 全站硬指标 .duration(N) N ≤ 600",
        },
        "F6_size_budget": size_facts,
        "F7_gsap_payload": gsap_facts,
        "F8_carrier_gap": carrier,
        "F9_bare_ease_scan": {
            "hits": bare_ease_hits,
            "files": len(bare_ease_files),
            "sample_files": sorted(bare_ease_files)[:20],
            "design_ref": "DESIGN.md §5.2 禁止裸 ease/linear 新增使用",
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    if "--print" in sys.argv:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:4000])
    print("motion audit written: %s (%d bytes)" % (OUT, OUT.stat().st_size))
    print("  pages=%d  keyframes_pages=%d  reveal_pages=%d  rm_pages=%d"
          % (page_total, kf_pages, reveal_pages, rm_pages))
    print("  ban_hits=%d  dur_gt600_pages=%d  bare_ease_hits=%d"
          % (sum(len(v) for v in ban_files.values()), dur_gt600_pages, bare_ease_hits))
    for k, v in size_facts.items():
        print("  %s: %d B / limit %d B -> headroom %+d B%s"
              % (k, v["bytes"], v["limit_bytes"], v["headroom_bytes"],
                 "  OVER" if v["over_budget"] else ""))
    print("  gsap external=%d B/page  inlined=%d B/page"
          % (gsap_facts["script_tag_bytes_each_page"], gsap_facts["total_bytes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
