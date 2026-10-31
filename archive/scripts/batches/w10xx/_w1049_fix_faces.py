# -*- coding: utf-8 -*-
"""_w1049_fix_faces.py — 修收官门禁的 A 类项（CHANGELOG 编号规则 / workflows 里程碑上限）

A-1 CHANGELOG 编号规则段写「W001-W1050」但最新段是 W1049 ⇒ 门禁判「编号规则段上限
    W1050 != 最新 W 段 W1049」⇒ 改为 W001-W1049。
    （W1050 批重放时会按其号序再推进——本批只保证与本批最新段一致。）
A-2 `.github/workflows/README.md` 里程碑行上限写 W1050 而现役是 W1049 ⇒ 改为 W1049。

用法：py -3 archive/scripts/batches/w10xx/_w1049_fix_faces.py [--dry-run]
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))

JOBS = [
    ("CHANGELOG.md", "（W001-W1050）", "（W001-W1049）", "CHANGELOG 编号规则段上限"),
    (".github/workflows/README.md", "W450-W1050", "W450-W1049", "workflows 里程碑行上限"),
]


def main() -> int:
    dry = "--dry-run" in sys.argv
    for rel, old, new, label in JOBS:
        p = os.path.join(REPO, rel.replace("/", os.sep))
        if not os.path.exists(p):
            print("SKIP  %s 不存在" % rel)
            continue
        raw = io.open(p, "rb").read()
        text = raw.decode("utf-8")
        nl = "\r\n" if b"\r\n" in raw else "\n"
        if old not in text:
            print("SKIP  %s（锚点未命中：%s）" % (label, old))
            continue
        if dry:
            print("DRY  %s：%s → %s" % (label, old, new))
            continue
        text = text.replace(old, new, 1)
        tmp = p + ".tmp"
        with io.open(tmp, "wb") as fh:
            fh.write(text.replace("\n", nl).encode("utf-8"))
        os.replace(tmp, p)
        print("OK    %s：%s → %s" % (label, old, new))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
