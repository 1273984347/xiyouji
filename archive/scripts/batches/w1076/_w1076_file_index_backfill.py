# -*- coding: utf-8 -*-
"""W1076：file-index 的 W1076 段回填（级联时 spec.file_index_rows 尚为空 ⇒ 写成空壳）。

段内定向订正（级联不可重跑）：按当前 spec 的 file_index_rows 重写该段的表格体。
"""
import json, os, pathlib, re, sys

def _repo_root():
    """向上找仓库根（带 .git 的目录）——脚本归档到 archive/scripts/batches/w1076/ 后仍可用。"""
    cur = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("未找到仓库根（.git）")
        cur = parent


ROOT = pathlib.Path(_repo_root())
SPEC = ROOT / "scripts" / "output" / "_w1076_spec.json"
IDX = ROOT / "scripts" / "output" / "file-index.md"

spec = json.loads(SPEC.read_text(encoding="utf-8"))
rows = spec.get("file_index_rows") or []
if not rows:
    raise SystemExit("spec.file_index_rows 仍为空——先跑 make_spec 再回填")

text = IDX.read_text(encoding="utf-8")
pat = re.compile(r"(^## W1076[^\n]*\n\n\| 文件 \| W \| 说明 \|\n\|---\|---\|---\|\n)(.*?)(?=\n## |\Z)", re.M | re.S)
m = pat.search(text)
if not m:
    raise SystemExit("未定位到 file-index 的 W1076 段——拒绝盲改")

body = m.group(2).rstrip("\n")
new_body = ("\n" + "\n".join(rows) + "\n") if body.strip() == "" else body
new = text[:m.start(2)] + new_body + text[m.end(2):]
if "--apply" in sys.argv:
    IDX.write_text(new, encoding="utf-8", newline="")
    print("file-index W1076 段已回填 %d 行登记（原体为空壳·已写盘）" % len(rows))
else:
    print("file-index W1076 段将回填 %d 行登记（dry-run·须 --apply 才写盘）" % len(rows))
