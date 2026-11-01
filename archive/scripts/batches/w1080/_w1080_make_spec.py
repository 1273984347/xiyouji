#!/usr/bin/env python3
"""_w1080_make_spec.py — 生成/同步 W1080 批次 spec 的 file_index_rows（索引态全集覆盖）。"""
import json
import os
import subprocess
import sys


def _repo_root():
    cur = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("未找到仓库根（.git）")
        cur = parent


ROOT = _repo_root()
SPEC = os.path.join(ROOT, "scripts", "output", "_w1080_spec.json")
BATCH = "W1080"
CURATED = [
    "scripts/_w1080_style_tokenize.py", "scripts/_w1080_make_spec.py",
    "archive/scripts/batches/w1080/_w1080_style_tokenize.py",
    "archive/scripts/batches/w1080/_w1080_make_spec.py",
    "scripts/output/_w1080_spec.json",
    "scripts/output/_w1080_j2_before", "scripts/output/_w1080_j2_after",
    "scripts/output/_vermilion_solid_cache.json", "scripts/output/_vermilion_solid_report.json",
    "CHANGELOG.md", "HANDOVER.md", "README.md", "STRUCTURE.md", "AGENTS.md",
    "docs/00-导读/项目说明.md", "docs/00-导读/W批次编号对账表.md",
    "scripts/output/file-index.md", "scripts/output/stats.json",
    "scripts/output/index.md", "scripts/output/README.md", "scripts/output/tools-inventory.md",
]


def _git(*args):
    r = subprocess.run(["git", "-c", "core.quotepath=false"] + list(args),
                       cwd=ROOT, capture_output=True, text=True)
    return r.stdout.splitlines()


def main():
    spec = json.load(open(SPEC, encoding="utf-8"))
    files = set(CURATED)
    for ln in _git("diff", "--cached", "--name-only"):
        if ln and not ln.endswith("/"):
            files.add(ln)
    for ln in _git("status", "--porcelain"):
        ln = ln.strip()
        if not ln:
            continue
        p = ln[3:].strip()
        if " -> " in p:
            p = p.split(" -> ")[-1].strip()
        p = p.strip('"')
        if p and not p.endswith("/"):
            files.add(p)
    rows = []
    for p in sorted(files):
        cat = ("页面" if p.startswith("site/") else
               "本批工具/产物" if (p.startswith("scripts/") or p.startswith("archive/")) else
               "治理文档")
        rows.append("| %s | %s | %s |" % (p, BATCH, cat))
    spec["file_index_rows"] = rows
    with open(SPEC, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(spec, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("spec file_index_rows：%d 行 → %s" % (len(rows), SPEC))
    return 0


if __name__ == "__main__":
    sys.exit(main())
