# -*- coding: utf-8 -*-
"""_s4b_334_sync.py — B 轨 334 口径回填（一次性·断言式）

背景：F1（234/225→334）2026-10-02 修订单体为投稿版；匿名稿（3 处）与完整稿（5 处）未同步，
2026-10-06 docx 重生成批次全量差异核查发现。修正后两处文档与投稿版口径一致。
注意：完整稿 L237「225 个 data/EN 深链页面」为另一口径（data+EN 页数），不在本批范围、保留不动。

备份：tmpe/dxbak_20261006/md_bak/
"""
from __future__ import annotations

import shutil
from pathlib import Path

D = Path(r"d:\xiyouji\docs\S4-学术投稿\05-投稿\装饰投稿")
ANON = D / "设计方向-匿名稿.md"
FULL = D / "设计方向-新中式数字雅集.md"
BAK = Path(r"d:\xiyouji\tmpe\dxbak_20261006\md_bak")

EDITS = {
    "匿名稿": [
        ("经三层架构分发至全部 234 个页面", "经三层架构分发至全部 334 个页面"),
        ("distributed across 234 pages through a three-tier architecture", "distributed across 334 pages through a three-tier architecture"),
        ("225 个页面各自内联覆盖图表样式", "334 个页面各自内联覆盖图表样式"),
    ],
    "完整稿": [
        ("→ 225 页内联分发）", "→ 334 页内联分发）"),
        ("inline distribution across 225 pages", "inline distribution across 334 pages"),
        ("从单一事实源到 225 页内联分发", "从单一事实源到 334 页内联分发"),
        ("└─→ 225 个页面内联 <style>（图表特有样式）", "└─→ 334 个页面内联 <style>（图表特有样式）"),
        ("全站 234 页同步。", "全站 334 页同步。"),
    ],
}

def main() -> int:
    BAK.mkdir(parents=True, exist_ok=True)
    problems: list[str] = []
    out: dict[str, str] = {}
    for label, path in (("匿名稿", ANON), ("完整稿", FULL)):
        shutil.copy2(path, BAK / path.name)
        text = path.read_text(encoding="utf-8")
        for old, new in EDITS[label]:
            n = text.count(old)
            if n != 1:
                problems.append(f"[{label}] count={n}: {old[:50]}…")
                continue
            text = text.replace(old, new)
        out[label] = text
    if problems:
        print("== 断言失败，未写回 ==")
        for p in problems:
            print(" -", p)
        return 1
    ANON.write_text(out["匿名稿"], encoding="utf-8")
    FULL.write_text(out["完整稿"], encoding="utf-8")
    print("== 已写回：匿名稿 3 处 / 完整稿 5 处（备份 tmpe/dxbak_20261006/md_bak/）==")
    for label, path in (("匿名稿", ANON), ("完整稿", FULL)):
        t = path.read_text(encoding="utf-8")
        print(f"[{label}] 残留 234/225 检查: 234={t.count('234')} 225={t.count('225')} 334={t.count('334')}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())