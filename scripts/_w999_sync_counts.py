# -*- coding: utf-8 -*-
"""_w999_sync_counts.py — 坑表计数链**按实算**同步（稳健版·不依赖固定文本）

背景：W999 批期间并行会话也在改坑表 ⇒ 固定文本替换（依赖旧数值）会失配。
本脚本改为**实算驱动**：数每节的 `- **` 条目数 → 改写节标题的 (N 条) →
再把 AGENTS.md / HANDOVER.md 里的总条数与六主题计数按实算回填（正则定位模式·数字位替换）。

幂等：重复跑结果一致。
用法：py -3 scripts/_w999_sync_counts.py [--dry-run]
"""
from __future__ import annotations

import io
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIT = os.path.join(REPO, "docs", "agent", "pitfalls.md")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def section_counts(text):
    """按节切分，数每节的 '- **' 条目数（顺序即节序）。"""
    heads = list(re.finditer(r"^### (.+?)（\d+ 条）$", text, re.M))
    out = []
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        seg = text[h.end():end]
        n = len(re.findall(r"^- \*\*", seg, re.M))
        out.append((h.group(1), n, h.span()))
    return out


def main() -> int:
    dry = "--dry-run" in "--dry-run" in os.sys.argv
    t, n = read(PIT)
    counts = section_counts(t)
    total = sum(c[1] for c in counts)
    print("实算各节：", [(c[0], c[1]) for c in counts], "· 合计", total)

    # ① 改写节标题的 (N 条)
    changed = 0
    for name, cnt, (s, e) in reversed(counts):
        m = re.match(r"^(### .+?（)\d+( 条）)$", t[s:e])
        if not m:
            continue
        new = "%s%d%s" % (m.group(1), cnt, m.group(2))
        if t[s:e] != new:
            t = t[:s] + new + t[e:]
            changed += 1
    print("节标题修正：%d 处" % changed)

    # ② AGENTS.md / HANDOVER.md 回填
    theme_line = "·".join("%s（%d）" % (name, cnt) for name, cnt, _ in counts)
    for rel in ("AGENTS.md", "HANDOVER.md"):
        p = os.path.join(REPO, rel)
        t2, n2 = read(p)
        o2 = t2
        # 总条数：形如「91 条坑位」「（91 条·六主题）」
        t2 = re.sub(r"(\d+) 条坑位", "%d 条坑位" % total, t2)
        t2 = re.sub(r"（(\d+) 条·六主题", "（%d 条·六主题" % total, t2)
        # 六主题计数串：整行替换（保留行首前缀）
        lines = t2.split("\n")
        for i, ln in enumerate(lines):
            if "CSS/视觉渲染（" in ln and "JS/CSP/运行时（" in ln:
                pre = ln.split("CSS/视觉渲染（")[0]
                lines[i] = pre + theme_line
                break
        t2 = "\n".join(lines)
        if t2 != o2:
            if dry:
                print("DRY  %s 计数链回填：%d → %d 条" % (rel, total, total))
            else:
                write(p, t2, n2)
                print("OK   %s 计数链已回填（总 %d 条 · 六主题逐节实算）" % (rel, total))

    if not dry:
        write(PIT, t, n)
        print("OK   坑表节标题已按实算修正")

    # ③ 复核
    t3, _ = read(PIT)
    cs = section_counts(t3)
    print("复核：声明合计 %d · 实算条目 %d"
          % (sum(int(re.search(r"（(\d+) 条）", t3[s:e]).group(1)) for _, _, (s, e) in cs),
             len(re.findall(r"^- \*\*", t3, re.M))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
