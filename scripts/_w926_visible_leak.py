#!/usr/bin/env python3
"""W926 可见文本面审计：剥离 script/style/注释后，统计**访客真正看得见**的内部术语外泄。

判据（先质疑判据再质疑结论）：
  · 只看 <body> 内可见文本 —— script/style/HTML 注释/meta 一律剥离
  · 命中两类内部术语：① 批次号 W\\d{3}  ② 门禁/工程黑话词
用法：py -3 scripts/_w926_visible_leak.py [--out <path>]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "scripts" / "output" / "_w926_visible_leak.json"

BODY_RE = re.compile(r"<body[^>]*>(.*)</body>", re.S | re.I)
DROP_RE = re.compile(r"<(script|style|template|noscript)\b.*?</\1>", re.S | re.I)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"[ \t\u00a0]+")

BATCH_RE = re.compile(r"\bW\d{3}\b")
JARGON_RE = re.compile(
    r"(门禁|判红|假绿|假收敛|在途|级联|台账|批次号|自测|复算|口径|实跑|"
    r"取证|快照|漂移|根修|批次|议题|抽象|收敛|谱系化|实体标记|首屏归并|"
    r"存量脚本|全绿|判据|立项|复核批|裁决落地|内联|回退|归并|洗牌)"
)


def visible_text(html: str) -> str:
    m = BODY_RE.search(html)
    seg = m.group(1) if m else html
    seg = DROP_RE.sub(" ", seg)
    seg = COMMENT_RE.sub(" ", seg)
    seg = TAG_RE.sub(" ", seg)
    return WS_RE.sub(" ", seg)


def main() -> int:
    ap = argparse.ArgumentParser(description="W926 可见文本面审计（访客可见文本中的内部术语外泄）")
    ap.add_argument("--out", default=str(OUT), help="改写落点（默认 scripts/output/_w926_visible_leak.json）")
    args = ap.parse_args()
    out_path = Path(args.out)
    rows = []
    total_batch = 0
    total_jargon = 0
    pages_batch = 0
    for f in sorted(SITE.rglob("*.html")):
        rel = f.relative_to(SITE).as_posix()
        txt = visible_text(f.read_text(encoding="utf-8", errors="replace"))
        b = BATCH_RE.findall(txt)
        j = JARGON_RE.findall(txt)
        if b or j:
            total_batch += len(b)
            total_jargon += len(j)
            pages_batch += 1
            snippets = []
            for m in re.finditer(r"[^。！？\n]{0,60}(?:W\d{3}|门禁|判红|假绿|假收敛|在途|级联|台账|判据|全绿|根修|存量脚本|实体标记)[^。！？\n]{0,60}", txt):
                s = m.group(0).strip()
                if s and s not in snippets:
                    snippets.append(s)
                if len(snippets) >= 3:
                    break
            rows.append({"page": rel, "batch_n": len(b), "jargon_n": len(j),
                         "batch_terms": sorted(set(b))[:8], "snippets": snippets})
    rows.sort(key=lambda r: -(r["batch_n"] + r["jargon_n"]))
    out = {"pages_total": len(list(SITE.rglob("*.html"))),
           "pages_with_leak": pages_batch,
           "visible_batch_terms": total_batch,
           "visible_jargon_terms": total_jargon,
           "rows": rows}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[可见文本泄漏扫描] {out_path}")
    print(f"  含内部术语的页：{pages_batch}/{out['pages_total']}· 可见批次号 {total_batch} 处· 门禁黑话 {total_jargon} 处")
    print("  —— 泄漏最重的前 12 页 ——")
    for r in rows[:12]:
        print(f"    {r['page']}  W号×{r['batch_n']} 黑话×{r['jargon_n']}  {r['batch_terms'][:4]}")
        for s in r["snippets"][:1]:
            print(f"       「{s[:120]}」")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
