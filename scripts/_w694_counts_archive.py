"""_w694_counts_archive.py — W694 一次性文档批处理（不入库门禁）。

1) STRUCTURE.md 两段批次速记迁移至 docs/archive/STRUCTURE-ARCHIVE.md（维护契约：禁速记段）
2) 86→87 可视化页计数级联（README×2 / STRUCTURE / 项目说明 / 交接文档 / AGENTS×2）
全部替换带命中数断言，零命中即中止不落盘（单文件粒度）。
"""
import sys

ROOT = r"D:\xiyouji"

STRUCT = ROOT + r"\STRUCTURE.md"
ARCHIVE = ROOT + r"\docs\archive\STRUCTURE-ARCHIVE.md"

L79_PREFIX = "按主题立文件"
L88_PREFIX = "现代视角解读、职场映射"

NEW_79 = "按主题立文件（七段式模板），现 209 篇；建置沿革见 docs/archive/STRUCTURE-ARCHIVE.md 与 CHANGELOG。"
NEW_88 = "现代视角解读、职场映射、时代变迁中的西游。独立随笔以六段式（古今对位 + 加粗金句）建设，现 44 篇；建置沿革见 docs/archive/STRUCTURE-ARCHIVE.md 与 CHANGELOG。"

COUNT_EDITS = [
    (r"\README.md",
     "📊 **数据可视化**：86 个 D3.js 可视化/交互页",
     "📊 **数据可视化**：87 个 D3.js 可视化/交互页"),
    (r"\README.md",
     "`site/data/` 86 个可视化页（含 V3 标签云全站导航 W313）",
     "`site/data/` 87 个可视化页（含 V3 标签云全站导航 W313）"),
    (r"\STRUCTURE.md",
     "现 86 个可视化页——口径与明细随批次演进",
     "现 87 个可视化页——口径与明细随批次演进"),
    (r"\docs\00-导读\项目说明.md",
     "- 86 个 D3.js/Three.js 可视化页面（含 W313",
     "- 87 个 D3.js/Three.js 可视化页面（含 W313"),
    (r"\交接文档.md",
     "- 86 个可视化/交互页（含 graph-explorer",
     "- 87 个可视化/交互页（含 graph-explorer"),
    (r"\AGENTS.md",
     "**数据可视化**：86 个 D3.js / Three.js 可视化页（site/data/ 共 87 个 HTML，「86」不含模板壳 _shell.html）",
     "**数据可视化**：87 个 D3.js / Three.js 可视化页（site/data/ 共 88 个 HTML，「87」不含模板壳 _shell.html）"),
    (r"\AGENTS.md",
     "│   ├── data/              # 可视化页（87 个 HTML，D3/Three；「86 可视化页」口径不含模板壳 _shell.html）",
     "│   ├── data/              # 可视化页（88 个 HTML，D3/Three；「87 可视化页」口径不含模板壳 _shell.html）"),
]


def read(p):
    return open(p, encoding="utf-8", newline="").read()


def main():
    s = read(STRUCT)
    lines = s.split("\n")
    idx79 = idx88 = None
    for i, ln in enumerate(lines):
        if ln.startswith(L79_PREFIX) and len(ln) > 800:
            idx79 = i
        if ln.startswith(L88_PREFIX) and len(ln) > 5000:
            idx88 = i
    assert idx79 is not None and idx88 is not None, "speed-run lines not found"
    old79, old88 = lines[idx79], lines[idx88]
    assert "W286" in old79 and "W285" in old79, "line79 shape unexpected"
    assert "W069" in old88 or "W068" in old88 or "W072" in old88, "line88 shape unexpected"

    arc = read(ARCHIVE)
    header = "\n## W694 迁出：建置沿革速记段（2026-10-10 自 STRUCTURE.md 迁入·维护契约禁速记段）\n\n"
    assert "W694 迁出" not in arc, "archive section already present"
    arc_new = arc.rstrip("\n") + "\n" + header + old79 + "\n\n" + old88 + "\n"
    open(ARCHIVE, "w", encoding="utf-8", newline="").write(arc_new)

    lines[idx79] = NEW_79
    lines[idx88] = NEW_88
    open(STRUCT, "w", encoding="utf-8", newline="").write("\n".join(lines))
    print("OK-1 archive+prune: line%d(%d ch) + line%d(%d ch) moved" % (idx79 + 1, len(old79), idx88 + 1, len(old88)))

    for rel, old, new in COUNT_EDITS:
        p = ROOT + rel
        t = read(p)
        n = t.count(old)
        assert n == 1, "expect 1 hit for %s in %s, got %d" % (old[:30], rel, n)
        open(p, "w", encoding="utf-8", newline="").write(t.replace(old, new, 1))
        print("OK-2 %s: %s -> 87" % (rel, old[:24]))
    print("ALL-DONE")


if __name__ == "__main__":
    sys.exit(main())
