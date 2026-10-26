#!/usr/bin/env python3
"""_w978_review_evidence.py — 第 44 篇工作复盘取证脚本（W978）。

口径与 _w954_review_evidence.py 同族：本报告全部统计数字的唯一源头，无手写估计值。
区间 = 上篇复盘（CHANGELOG 现役+归档两面标题含「工作复盘」的最高段·即第 43 篇 W954·
2026-10-26）当日起 → 现在。复算命令见报告附录 A。

产物：scripts/output/_w978_review_evidence.json
"""
from __future__ import annotations

import collections
import datetime
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOW = datetime.datetime.now()
THRESHOLDS = {"days": 3, "batches": 30, "commits": 80}
RE_SEG = re.compile(r"^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（(20\d{2}-\d{2}-\d{2})）：)([^\n]*)", re.M)
RE_ROW = re.compile(r"^\|\s*W(\d{3,4})\s*\|")
NON_BATCH_MARKS = ("让号留痕", "已停止")
RE_TYPE = re.compile(r"^(\w+)(?:\([^)]*\))?:")
GROUPS = [
    ("治理/登记面机器化", ("登记", "台账", "回填", "状态", "号位", "迁移")),
    ("体积窗口与归档体系", ("体积", "归档", "窗口", "退役")),
    ("工具链体检与修复", ("体检", "修复", "断言", "自撞", "修路")),
    ("门禁与审计加固", ("门禁", "CodeQL", "审计", "探针")),
    ("素材图与题图", ("题图", "素材", "出图", "hero", "plate")),
    ("文档治理与沉淀", ("清理", "沉淀", "坑表", "方法论", "HANDOVER", "指针")),
]


def run(*cmd):
    return subprocess.run(list(cmd), capture_output=True, text=True, encoding="utf-8",
                          errors="replace", cwd=ROOT)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8", newline="") as fh:
        return fh.read()


def main():
    # 上篇复盘（现役+归档合看·降序取最高含「工作复盘」段）
    combined = read("CHANGELOG.md") + read(os.path.join("archive", "docs", "CHANGELOG-ARCHIVE.md"))
    last = None
    for m in RE_SEG.finditer(combined):
        if "工作复盘" in m.group(4):
            last = {"w": int(m.group(1) or m.group(2)), "date": m.group(3), "title": m.group(4).strip()}
            break
    assert last, "未找到上篇复盘段"
    since = last["date"] + " 00:00:00"

    # 提交面
    log = run("git", "log", "--since=" + since, "--format=%h|%ad|%s",
              "--date=format:%Y-%m-%d").stdout.strip().splitlines()
    commits = []
    for ln in log:
        if not ln.strip():
            continue
        h, d, subject = ln.split("|", 2)
        ws = [int(x) for x in re.findall(r"[Ww](\d{3,4})", subject)]
        commits.append({"hash": h, "date": d, "subject": subject, "w": ws[0] if ws else None})
    by_day = collections.Counter(c["date"] for c in commits)
    by_type = collections.Counter((RE_TYPE.match(c["subject"]) or [None, "other"])[1]
                                  if RE_TYPE.match(c["subject"]) else "other" for c in commits)
    per_batch = collections.Counter(c["w"] for c in commits if c["w"])

    # 批次面：CHANGELOG 段（两面合看）+ 台账行
    segs = {}
    for m in RE_SEG.finditer(combined):
        w = int(m.group(1) or m.group(2))
        if w > last["w"]:
            segs[w] = {"date": m.group(3) or "", "title": m.group(4).strip()}
    ledger_rows = []
    for ln in read(os.path.join("docs", "00-导读", "W批次编号对账表.md")).splitlines():
        m = RE_ROW.match(ln)
        if m and int(m.group(1)) > last["w"]:
            tail = " | ".join(ln.split(" | ")[-5:-1])
            if not any(k in tail for k in NON_BATCH_MARKS):
                ledger_rows.append(int(m.group(1)))

    # 主题分组（标题关键词机分·命中即止）
    def group_of(title):
        low = title.lower()
        for name, kws in GROUPS:
            if any(k.lower() in low for k in kws):
                return name
        return "其他"

    groups = collections.Counter(group_of(s["title"]) for s in segs.values())

    # 触发器面板值
    days = round((NOW - datetime.datetime.fromisoformat(last["date"] + "T00:00:00")).total_seconds() / 3600 / 24, 2)
    hours = round((NOW - datetime.datetime.fromisoformat(last["date"] + "T00:00:00")).total_seconds() / 3600, 1)
    trig = {"days": days, "batches": len(ledger_rows), "commits": len(commits)}
    fired = [k for k, v in trig.items() if v >= THRESHOLDS[k]]

    out = {
        "generated_at": NOW.isoformat(timespec="seconds"),
        "last_review": last,
        "period": {"since": since, "until": NOW.isoformat(timespec="seconds"),
                   "hours": hours, "days": round(hours / 24, 2)},
        "commits": {"total": len(commits), "by_day": dict(sorted(by_day.items())),
                    "by_type": dict(by_type.most_common()),
                    "per_batch_top": dict(per_batch.most_common(8))},
        "batches": {"changelog_segments": len(segs), "ledger_rows": len(ledger_rows),
                    "w_range": [min(segs) if segs else None, max(segs) if segs else None],
                    "zero_commit": sorted(set(range(min(segs), max(segs) + 1)) - set(segs)) if segs else [],
                    "groups": dict(groups.most_common()),
                    "titles": {str(w): segs[w]["title"][:60] for w in sorted(segs)}},
        "trigger": {"thresholds": THRESHOLDS, "values": trig, "fired": fired},
    }
    dst = os.path.join(ROOT, "scripts", "output", "_w978_review_evidence.json")
    with open(dst, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("提交 %d · 段 %d · 台账行 %d · 触发 %s -> %s"
          % (len(commits), len(segs), len(ledger_rows), fired or "无", dst))
    print("分组:", dict(groups.most_common()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
