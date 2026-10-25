"""W949 · 第 50 门禁扩展：字段图标位判据（avatar / icon / flag / stage）

背景：前三轮治理靠「HTML 形态」分类判据（控件首位 / 图标槽 class / CSS content），
      漏掉了「数据字段值里用图形字符充当图标」的形态（avatar / icon / flag / STAGE_EMOJI），
      实测漏掉 5 个页面 + 1 个数据源 ⇒ 现作为**扩展判据**纳入机检。

判据与白名单（scripts/output/_w949_icon_field_allowlist.json）逐条比对：
  · 白名单外的命中 ⇒ 判红（新漏网）
  · 白名单条目已消失 ⇒ 判红（白名单腐化，需同步核销）
  · 两者一致 ⇒ 通过（白名单清空后该判据自然转绿，不设恒红豁免）
"""
from __future__ import annotations

import json
import pathlib
import re
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALLOW_FILE = ROOT / "scripts" / "output" / "_w949_icon_field_allowlist.json"

GRAPHICS = re.compile("[\U0001F000-\U0001FAFF"
                      "\u2728\u274C\u2705\u26A1\u2B50\u2934\u2935\u3030\u303D\u3297\u3299"
                      "\u2600-\u27BF\u2B00-\u2BFF]")

# 字段型：avatar: "…" / 'icon': '…' / "flag": "…"（JSON 键带引号也要匹配）
FIELD_PATTERNS = [
    ("avatar", re.compile(r"[\"']?\bavatar\b[\"']?\s*[:=]\s*[\"']([^\"']*)[\"']")),
    ("icon", re.compile(r"[\"']?\bicon\b[\"']?\s*[:=]\s*[\"']([^\"']*)[\"']")),
    ("flag", re.compile(r"[\"']?\bflag\b[\"']?\s*[:=]\s*[\"']([^\"']*)[\"']")),
]
# 数组常量型：STAGE_EMOJI = ["⛰️", "💀", …]
ARRAY_PATTERN = re.compile(r"\b([A-Z_]*EMOJI[A-Z_]*)\s*=\s*\[([^\]]*)\]")


def scan_field_icons() -> list[dict]:
    hits: list[dict] = []
    roots = ["site", "dataset", "xiyouji-agent-web/src", "xiyouji-desktop/src", "assets/promo"]
    exts = {".html", ".htm", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".vue", ".json"}
    for root in roots:
        p = ROOT / root
        if not p.exists():
            continue
        for f in sorted(p.rglob("*")):
            if not (f.is_file() and f.suffix.lower() in exts):
                continue
            rel = f.relative_to(ROOT).as_posix()
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            for field, rx in FIELD_PATTERNS:
                for m in rx.finditer(text):
                    val = m.group(1)
                    if not GRAPHICS.search(val):
                        continue
                    # 保留**原始值**（不逐码位拆解·不排序）：ZWJ 序列与 VS16 必须整体匹配
                    hits.append({"file": rel, "line": text.count("\n", 0, m.start()) + 1,
                                 "field": field, "chars": val})
            for m in ARRAY_PATTERN.finditer(text):
                for item in re.findall(r"[\"']([^\"']*)[\"']", m.group(2)):
                    if not GRAPHICS.search(item):
                        continue
                    hits.append({"file": rel, "line": text.count("\n", 0, m.start()) + 1,
                                 "field": "stage", "chars": item})
    # 去重（同 file+field+chars 多次出现只记一次，与白名单口径一致）
    seen = set()
    uniq = []
    for h in hits:
        key = (h["file"], h["field"], h["chars"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(h)
    return uniq


def compare(hits: list[dict]) -> tuple[list[dict], list[dict]]:
    """返回 (白名单外的新命中, 白名单中已消失的条目)"""
    allow = json.loads(ALLOW_FILE.read_text(encoding="utf-8"))
    allow_keys = {(a["file"], a["field"], a["chars"]) for a in allow}
    hit_keys = {(h["file"], h["field"], h["chars"]) for h in hits}
    new_hits = [h for h in hits if (h["file"], h["field"], h["chars"]) not in allow_keys]
    stale = []
    for a in allow:
        if (a["file"], a["field"], a["chars"]) not in hit_keys:
            stale.append(a)
    return new_hits, stale


def main() -> int:
    hits = scan_field_icons()
    new_hits, stale = compare(hits)
    print("=" * 72)
    print("字段图标位判据（avatar / icon / flag / stage）")
    print("=" * 72)
    print(f"命中 {len(hits)} 条（去重后）· 字段分布 {dict(Counter(h['field'] for h in hits))}")
    print(f"白名单外的新命中: {len(new_hits)}")
    for h in new_hits[:20]:
        print(f"  {h['file']}:{h['line']}  [{h['field']}]  {h['chars']}")
    print(f"白名单中已消失（需核销）: {len(stale)}")
    for a in stale[:20]:
        print(f"  {a['file']}  [{a['field']}]  {a['chars']}")
    ok = not new_hits and not stale
    print("-" * 72)
    print("OK    字段图标位与白名单一致" if ok else "FAIL  字段图标位与白名单不一致")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
