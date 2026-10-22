#!/usr/bin/env python3
"""_w851_j2_evidence.py — W851 J2 证据摘要一次性生成器。

把 before/after 两个全量快照的判词（probe._diff_snapshots）、元素计数与
sha256 打成一个可提交的小证据文件；原始大快照（~8MB/份）按仓内 scripts/output
小件惯例不提交（探针确定性已实证·可复现），本文件 + 冻结页两份小快照构成证据链。
"""

import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import _w851_visual_regression_probe as probe  # noqa: E402

OUT = os.path.join(ROOT, "scripts", "output", "_w851_j2_evidence.json")
BEFORE = os.path.join(ROOT, "scripts", "output",
                      "_w851_visual_snapshot_before.json")
AFTER = os.path.join(ROOT, "scripts", "output",
                     "_w851_visual_snapshot_after.json")


def _load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _counts(snap):
    return {rel: {t: len(els) for t, els in themes.items()}
            for rel, themes in snap["pages"].items()}


def main():
    before, after = _load(BEFORE), _load(AFTER)
    diffs, notes = probe._diff_snapshots(before, after)
    ev = {
        "schema": 1,
        "batch": "W851",
        "criterion": "J2",
        "verdict": "PASS" if not diffs else "FAIL",
        "method": "probe._diff_snapshots（29 属性固定序·元素身份 + 逐属性对拍）",
        "diff_count": len(diffs),
        "diffs_head": diffs[:20],
        "notes": notes,
        "before": {"captured_at": before["captured_at"],
                   "meta": before["meta"],
                   "sha256": _sha(BEFORE),
                   "element_counts": _counts(before)},
        "after": {"captured_at": after["captured_at"],
                  "meta": after["meta"],
                  "sha256": _sha(AFTER),
                  "element_counts": _counts(after)},
        "raw_snapshots": "随批入库（file-index C4-f 要求·判词的原始证据）·"
                         "本文件 sha256 字段为判词的防篡改锚",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ev, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("J2 证据：%s（差异 %d 条）→ %s"
          % (ev["verdict"], len(diffs), os.path.relpath(OUT, ROOT)))
    return 0 if not diffs else 1


if __name__ == "__main__":
    sys.exit(main())
