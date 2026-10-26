# -*- coding: utf-8 -*-
"""_w974_sync_stats_marks.py — 同步 3 处 `<!--stats:report_docs-->` 标记数字（75 → 77）

背景：第 31 门禁 C5b「标记数字 ≠ stats.json report_docs」——
本批新增 2 个报告件（执行前计划 T29 + T29 报告）⇒ report_docs 由 75 变为 77（磁盘实算与
「提交后 HEAD 实况」一致·75 + 2 = 77·无并行会话污染）。

三处均为**共享面** ⇒ 以 `HEAD:<file>` 为基底做单行替换 → `git update-index --cacheinfo`
精确暂存（工作树同步为同一内容）⇒ 并行会话在途内容既不入本批提交、也不被我抹掉。

判定：只替换 `数字<!--stats:report_docs-->` 这一种标记；其余 `<!--stats:*-->` 标记不动。

用法：py -3 scripts/_w974_sync_stats_marks.py [--dry-run]
"""
import io
import os
import re
import subprocess
import sys

REPO = r"D:\xiyouji"
TARGETS = [
    "STRUCTURE.md",
    "docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md",
    "docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md",
]
PAT = re.compile(r"(\d+)(<!--stats:report_docs-->)")


def git_show(rel):
    p = subprocess.run(["git", "show", "HEAD:" + rel], cwd=REPO, capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout.decode("utf-8")


def write_atomic(rel, text):
    p = os.path.join(REPO, rel.replace("/", os.sep))
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    data = text.replace("\n", nl).encode("utf-8")
    tmp = p + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, p)


def stage_exact(rel, text):
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO,
                          input=text.encode("utf-8"), capture_output=True)
    if blob.returncode != 0:
        raise SystemExit("FATAL hash-object 失败")
    b = blob.stdout.decode().strip()
    p = subprocess.run(["git", "update-index", "--cacheinfo", "100644," + b + "," + rel],
                       cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("FATAL update-index 失败: " + p.stderr.decode("utf-8", "replace")[:200])
    print("  精确暂存 %s（blob %s）" % (rel, b[:8]))


def main() -> int:
    dry = "--dry-run" in sys.argv
    st = io.open(os.path.join(REPO, "scripts", "output", "stats.json"), encoding="utf-8")
    import json
    raw = json.load(st)["report_docs"]
    # stats.json 里该键是 {domain, generator, value, ...} 结构·取 value
    target = raw["value"] if isinstance(raw, dict) else raw
    print("stats.json report_docs = %d（键形态：%s）" % (target, "dict" if isinstance(raw, dict) else "scalar"))
    for rel in TARGETS:
        head = git_show(rel)
        if head is None:
            print("SKIP（HEAD 无此文件）：%s" % rel)
            continue
        m = PAT.search(head)
        if not m:
            print("SKIP（无 report_docs 标记）：%s" % rel)
            continue
        old = m.group(1)
        if old == str(target):
            print("OK   已是 %s（无需改）：%s" % (target, rel))
            continue
        new_text = PAT.sub(lambda mm: "%d%s" % (target, mm.group(2)), head, count=1)
        if dry:
            print("DRY  %s：%s → %d" % (rel, old, target))
            continue
        write_atomic(rel, new_text.replace("\r\n", "\n"))
        stage_exact(rel, new_text.replace("\r\n", "\n"))
        print("  %s：%s → %d（工作树已同步）" % (rel, old, target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
