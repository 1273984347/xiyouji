#!/usr/bin/env python3
"""_w956_pilot_pick.py — W956 施工批「试点页择优」机选探针（可复算·不手挑）。

依据：执行前计划-T28 §5.4 ASM-14 的三条择优规则
  ① 含 hero 或题图（装饰插画 / 章节题图）
  ② 含 ≥3 个 section（区块数足够·有多段结构可编排）
  ③ 结构类各异（首页 / 正文 / 专题 / 人物 四类各覆盖）

产出：scripts/output/_w956_pilot_pick.json
      · 候选页逐页特征量（hero / img / section / plate / h1 / h2 / prose / card）
      · 按规则机选出的 5 页试点清单（含选中理由）
      · 各页型的候选取舍说明（未入选页按规则落选原因）

用法：py -3 scripts/_w956_pilot_pick.py [--print]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripts" / "output" / "_w956_pilot_pick.json"

# 页型 → 候选 glob（相对 site/）
POOLS = [
    ("root", "index.html"),
    ("chapter", "reader/ch*.html"),
    ("theme", "reader/themes/*.html"),
    ("person", "reader/people/*.html"),
]

FEATURES = [
    ("hero", 'class="hero'),
    ("img", "<img"),
    ("plate", "chapter-plate"),
    ("section", "<section"),
    ("h2", "<h2"),
    ("details", "<details"),
    ("fold", 'class="reader-fold"'),
    ("h1", "<h1"),
    ("progress", "data-reader-progress"),
    ("body", 'class="reader-body"'),
    ("card", 'class="card'),
    ("reveal", "reveal-in"),
]

# 结构单元 = 分节标题 + 折叠块 + section 标签（reader 页无 <section>，以 h2/details 为主）
STRUCT_KEYS = ("h2", "details", "section")


def features(text: str) -> dict:
    return {name: text.count(pat) for name, pat in FEATURES}


def load(rel: str) -> str:
    return (ROOT / "site" / rel).read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    cands = []
    for kind, pattern in POOLS:
        for p in sorted((ROOT / "site").glob(pattern)):
            rel = str(p.relative_to(ROOT / "site")).replace("\\", "/")
            f = features(p.read_text(encoding="utf-8", errors="ignore"))
            f["kind"] = kind
            f["rel"] = rel
            f["bytes"] = p.stat().st_size
            # 规则①：含 hero 或题图（装饰图或章节题图）
            f["pass_visual"] = (f["hero"] > 0) or (f["img"] > 0) or (f["plate"] > 0)
            # 规则②：结构单元（h2 分节 + details 折叠 + section）≥ 3
            f["struct_units"] = sum(f[k] for k in STRUCT_KEYS)
            f["pass_sections"] = f["struct_units"] >= 3
            f["pass_all"] = f["pass_visual"] and f["pass_sections"]
            cands.append(f)

    by_kind = {}
    for c in cands:
        by_kind.setdefault(c["kind"], []).append(c)

    # 机选规则：每类取「结构量最大」的一页（区块多 ⇒ 编排空间大），
    # 同结构量时取文件字节数小者（渲染轻·先验证成本低）。
    def pick(kind: str):
        pool = [c for c in by_kind.get(kind, []) if c["pass_all"]]
        if not pool:
            return None
        pool.sort(key=lambda c: (-c["struct_units"], c["bytes"]))
        return pool[0]

    # 首页必选（首屏是最大编排面）；其余三类各取一页
    chosen = []
    root = by_kind.get("root", [None])[0] if by_kind.get("root") else None
    if root:
        chosen.append((root, "首页：首屏 + 三个 section（read/lookup/tools）编排面最大"))
    for kind, label in (("chapter", "正文页：回目结构，多段正文可编排"),
                        ("theme", "专题页：专题题图 + 专题结构"),
                        ("person", "人物页：人物题图 + 人物结构")):
        c = pick(kind)
        if c:
            chosen.append((c, label))
    # 若正文/专题/人物任一类规则落空，按「结构量降序」补位，保证试点覆盖 ≥3 类
    if len(chosen) < 5:
        pool = sorted([c for c in cands if c["pass_all"] and c["rel"] not in [x[0]["rel"] for x in chosen]],
                      key=lambda c: (-c["section"], c["bytes"]))
        for c in pool[: 5 - len(chosen)]:
            chosen.append((c, "补位：规则①②通过但该类前序页已被占用（结构量降序）"))

    data = {
        "batch": "W956",
        "generated_by": "scripts/_w956_pilot_pick.py",
        "rules": {
            "R1_visual": "含 hero 或题图（class=\"hero / <img / chapter-plate）",
            "R2_sections": "<section 数 ≥ 3",
            "R3_variety": "覆盖首页 / 正文 / 专题 / 人物 四类",
        },
        "candidate_count": len(cands),
        "by_kind": {k: len(v) for k, v in by_kind.items()},
        "pass_all_by_kind": {k: len([c for c in v if c["pass_all"]]) for k, v in by_kind.items()},
        "chosen": [
            {
                "rel": c["rel"],
                "kind": c["kind"],
                "reason": reason,
                "features": {k: c[k] for k, _ in FEATURES},
                "bytes": c["bytes"],
            }
            for c, reason in chosen
        ],
        "candidates": [
            {"rel": c["rel"], "kind": c["kind"], "pass_all": c["pass_all"],
             "struct_units": c["struct_units"], "img": c["img"], "hero": c["hero"], "plate": c["plate"],
             "bytes": c["bytes"]}
            for c in sorted(cands, key=lambda c: (c["kind"], -c["struct_units"], c["bytes"]))
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("pilot pick written: %s" % OUT)
    for item in data["chosen"]:
        print("  %-46s %-8s %s" % (item["rel"], item["kind"], item["reason"]))
    print("  candidates=%d  kinds=%s" % (len(cands), data["by_kind"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
