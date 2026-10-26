# -*- coding: utf-8 -*-
"""W722 一次性脚本：A4 计数叙述面标记化（用户裁决 6A·三处同改之二）——五处唯一锚点替换。
用后即弃。"""
import io

EDITS = [
    ("README.md", "A4 209 篇已含", "A4 209<!--stats:a4_docs--> 篇已含"),
    ("STRUCTURE.md", "现 209 篇；", "现 209<!--stats:a4_docs--> 篇；"),
    ("AGENTS.md", "A4 主题专题（209 篇）", "A4 主题专题（209<!--stats:a4_docs--> 篇）"),
    ("交接文档.md", "已有 209 篇。", "已有 209<!--stats:a4_docs--> 篇。"),
    ("docs/00-导读/项目说明.md", "A4 主题专题 209 篇·", "A4 主题专题 209<!--stats:a4_docs--> 篇·"),
]
for p, old, new in EDITS:
    s = io.open(p, encoding="utf-8", newline="").read()
    n = s.count(old)
    assert n == 1, "%s 命中 %d: %s" % (p, n, old)
    io.open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new, 1))
    print("OK", p)
