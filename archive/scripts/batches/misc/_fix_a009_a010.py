#!/usr/bin/env python3
"""A-009 + A-010 处置（2026-09-27）。

A-009：页面 15 条关文节点 cite 中 11 条与论文表 1 不一致 → 全部统一为表 1 锚点；
       论文 §3.3 两处表述校准（"30 处排布"→"15 处关文节点排布；表 2 为文本数据集"、
       图号-文件名-数据源显式化）——两稿同步。
A-010：图号与文件名对应写入正文；未入正文的"明代驿递制度对照"图重命名消歧（另步执行）。
报告：批注 A-009/A-010 加"已修复"标记 + 执行记录 + 核验状态行更新。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "docs" / "S4-学术投稿" / "01-论文" / "明清小说方向-投稿版.md"
A = ROOT / "docs" / "S4-学术投稿" / "01-论文" / "明清小说方向-匿名稿.md"
PAGE = ROOT / "site" / "data" / "customs-pass-route.html"
R = ROOT / "docs" / "S4-学术投稿" / "审查报告-明清小说方向-2026-09-26.md"
Q = chr(34)

SEC_OLD = ("上述数据集已实现为交互式可视化（通关文牒·取经驿路图）：30 处驿传交通节点按时间顺序排布于取经路线"
           "（15 处关文节点以" + Q + "发牒/验讫/未验/波折/传经不验" + Q + "四态着色，15 处馆驿与流程节点为补充层），"
           "并附明代驿递制度对照表。可视化使" + Q + "关文叙事" + Q + "的时空结构直观可感，也是量化结论的可视化佐证。"
           "本文从该页面导出两幅印刷态图（驿路时间线全景与涉关文地点地理类型分布，见图 A-1、图 A-2），"
           "并作灰度处理以适应印刷。两图的数据源与表 1、表 2 完全同源（同一次检索、同一份锚点清单），"
           "读者可以逐点对照核验。")
SEC_NEW = ("上述数据集已实现为交互式可视化（通关文牒·取经驿路图）：15 处关文节点以"
           + Q + "发牒/验讫/未验/波折/传经不验" + Q + "四态着色、按回目顺序排布于取经路线，"
           "并附明代驿递制度对照表；表 2 补充集（15 处馆驿与流程节点）为文本数据集，本章以表格形式呈现。"
           "本文从该页面导出两幅印刷态图并作灰度处理以适应印刷：图 A-1 为驿路时间线全景"
           "（文件 A-图1-驿路时间线-灰度.png），图 A-2 为涉关文地点地理类型分布"
           "（文件 A-图2-涉关文地点地理类型分布-灰度.png）。两图的数据源均为表 1 的 15 处关文节点"
           "（同一次检索、同一份锚点清单），读者可以逐点对照核验。")

PAGE_PAIRS = [
    ('cite:"第29回 line 3"', 'cite:"第29回 line 19"'),
    ('cite:"第37回 line 11"', 'cite:"第39回 line 31"'),
    ('cite:"第44回 line 15·45回 line 43"', 'cite:"第45回 line 69"'),
    ('cite:"第54回 line 13"', 'cite:"第54回 line 17"'),
    ('cite:"第68回 line 3"', 'cite:"第68回 line 21"'),
    ('cite:"第74回 line 41"', 'cite:"第74回 line 19"'),
    ('cite:"第84回 line 3·line 17"', 'cite:"第84回 line 3·line 63"'),
    ('cite:"第88回 line 9"', 'cite:"第88回 line 15"'),
    ('cite:"第93回 line 3"', 'cite:"第93回 line 41"'),
    ('cite:"第96回 line 5·97回 line 31/67"', 'cite:"第96回 line 5·97回 line 31/75"'),
    ('cite:"第98回 line 1/43·100回 line 7/45"', 'cite:"第98回 line 43·100回 line 19"'),
]

R_EXEC = ("- **A-009（建议项·提前处置）**：范围核实后扩大——页面 15 条关文节点 cite 中 **11 条**与论文表 1 不一致"
          "（不止宝象国一处：含乌鸡国回目 37→39、车迟国/女儿国/朱紫国/狮驼国/玉华县/天竺国行号、"
          "灭法国/铜台府/灵山复合锚点等），已全部统一为表 1 锚点（表 1 侧 43/43 已实测）；"
          "页面改后重跑 CSP 注入与交付门禁。附带修正：论文 §3.3「30 处节点排布于页面」表述与页面实际"
          "（15 关文节点 + 制度对照表）不符，已校准为「15 处关文节点四态着色排布；表 2 为文本数据集」（两稿）。\n"
          "- **A-010（建议项·提前处置）**：图号-文件名-数据源对应显式化于 §3.3（图 A-1 ↔ A-图1-驿路时间线-灰度.png；"
          "图 A-2 ↔ A-图2-涉关文地点地理类型分布-灰度.png；两图数据源 = 表 1 十五节点）；未入正文的"
          "「A-图2-明代驿递制度对照-灰度.png」重命名为「A-附-明代驿递制度对照-灰度.png」以消除「图 2」指代冲突。\n")


def apply(path: Path, pairs) -> None:
    t = path.read_text(encoding="utf-8")
    for old, new in pairs:
        n = t.count(old)
        assert n == 1, "%s: count=%d: %s" % (path.name, n, old[:60])
        t = t.replace(old, new)
    path.write_text(t, encoding="utf-8")
    print("ok:", path.name)


def mark_section(text: str, prefix: str) -> str:
    lines = text.splitlines(keepends=True)
    for i, l in enumerate(lines):
        if l.startswith(prefix) and "已修复" not in l:
            lines[i] = l.rstrip("\n") + "（2026-09-27 已修复）\n"
            return "".join(lines)
    raise AssertionError("section not found: " + prefix)


def main() -> int:
    apply(S, [(SEC_OLD, SEC_NEW)])
    apply(A, [(SEC_OLD, SEC_NEW)])
    apply(PAGE, PAGE_PAIRS)
    # 报告
    t = R.read_text(encoding="utf-8")
    t = mark_section(t, "### 批注 A-009")
    t = mark_section(t, "### 批注 A-010")
    assert t.count("- **A-007（建议项·提前处置）**：") == 1
    t = t.replace("- **A-007（建议项·提前处置）**：", R_EXEC + "- **A-007（建议项·提前处置）**：")
    t = t.replace("**仍待**：`line_check.py` 与 `check_citations.py` 加固随批次提交入库；A-009 / A-010 建议项"
                  "（A-007 已于 2026-09-27 提前处置）。",
                  "**仍待**：`line_check.py` 与 `check_citations.py` 加固随批次提交入库"
                  "（A-007 / A-009 / A-010 建议项均已于 2026-09-27 处置）。")
    R.write_text(t, encoding="utf-8")
    print("ok:", R.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())