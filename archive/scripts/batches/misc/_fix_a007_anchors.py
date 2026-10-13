#!/usr/bin/env python3
"""建议项 A-007 处置（2026-09-27）：表 1 两条压缩锚点逐字化。

  74 回：`八百里狮驼岭三魔头`（跨词压缩）→ `八百里狮驼岭 · 三个魔头`（两段逐字，· 分隔）
  98-100 回：`将通关文牒取上来缴纳`（跨词压缩）→ `将通关文牒取上来，对主公缴纳`（逐字连续）
两稿同步；锚点审计脚本 CLAIMS 同步更新（74 回拆两条）；审查报告加已修复标记与执行记录。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "docs" / "S4-学术投稿" / "01-论文" / "明清小说方向-投稿版.md"
A = ROOT / "docs" / "S4-学术投稿" / "01-论文" / "明清小说方向-匿名稿.md"
AUDIT = ROOT / "scripts" / "_s4_audit_a_track_anchors.py"
R = ROOT / "docs" / "S4-学术投稿" / "审查报告-明清小说方向-2026-09-26.md"

ROW74_OLD = "| 第 74 回 | 狮驼国 | 未验 | unv | line 19 八百里狮驼岭三魔头 |"
ROW74_NEW = "| 第 74 回 | 狮驼国 | 未验 | unv | line 19 八百里狮驼岭 · 三个魔头 |"
ROW98_OLD = "| 第 98-100 回 | 灵山 | 传经不验 | sutra | line 43 无字真经 / 100 回 line 19 将通关文牒取上来缴纳 |"
ROW98_NEW = "| 第 98-100 回 | 灵山 | 传经不验 | sutra | line 43 无字真经 / 100 回 line 19 将通关文牒取上来，对主公缴纳 |"

MD_PAIRS = [(ROW74_OLD, ROW74_NEW), (ROW98_OLD, ROW98_NEW)]

AUDIT_PAIRS = [
    ('    ("表1-74回-狮驼国", 74, 19, "八百里狮驼岭三魔头"),',
     '    ("表1-74回-狮驼国a", 74, 19, "八百里狮驼岭"),\n    ("表1-74回-狮驼国b", 74, 19, "三个魔头"),'),
    ('    ("表1-100回-灵山b", 100, 19, "将通关文牒取上来缴纳"),',
     '    ("表1-100回-灵山b", 100, 19, "将通关文牒取上来，对主公缴纳"),'),
]

R_PAIRS = [
    ("### 批注 A-007：两条锚点片段为压缩表述，非逐字原文",
     "### 批注 A-007：两条锚点片段为压缩表述，非逐字原文（2026-09-27 已修复）"),
    ("- **修复过程中新发现并处置两项**：",
     "- **A-007（建议项·提前处置）**：表 1 两条压缩锚点逐字化——74 回改为"
     "\u201c八百里狮驼岭 · 三个魔头\u201d（两段逐字，底本实测均在第 74 回 line 19）、"
     "98-100 回末段改为\u201c将通关文牒取上来，对主公缴纳\u201d（逐字连续，第 100 回 line 19）；"
     "两稿同步，锚点审计脚本复跑通过。\n"
     "- **修复过程中新发现并处置两项**："),
    ("**仍待**：`line_check.py` 与 `check_citations.py` 加固随批次提交入库；A-007 / A-009 / A-010 建议项。",
     "**仍待**：`line_check.py` 与 `check_citations.py` 加固随批次提交入库；A-009 / A-010 建议项"
     "（A-007 已于 2026-09-27 提前处置）。"),
]


def apply(path: Path, pairs) -> None:
    t = path.read_text(encoding="utf-8")
    for old, new in pairs:
        n = t.count(old)
        assert n == 1, "%s: count=%d: %s" % (path.name, n, old[:50])
        t = t.replace(old, new)
    path.write_text(t, encoding="utf-8")
    print("ok:", path.name)


def main() -> int:
    apply(S, MD_PAIRS)
    apply(A, MD_PAIRS)
    apply(AUDIT, AUDIT_PAIRS)
    apply(R, R_PAIRS)
    return 0


if __name__ == "__main__":
    sys.exit(main())