# -*- coding: utf-8 -*-
"""_w1049_cascade_manifest.py — 生成级联清单 scripts/output/_cascade_files_W1049.txt

清单内容 = 本批实际改动面（git 工作树三态实测·排除 tmpe/）。
用法：py -3 archive/scripts/batches/w10xx/_w1049_cascade_manifest.py
"""
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
OUT = os.path.join(REPO, "scripts", "output")

files = []
out = subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO, "status", "--porcelain"],
                     capture_output=True).stdout.decode("utf-8", "replace")
# W1050 批的六件在途件 + 其级联面 ⇒ 不进本批清单（用户令「摘出勿卷入」）
W1050_EXCLUDE = {
    "scripts/verify_delivery.py",
    "scripts/check_doc_sync.py",
    "docs/agent/gates.md",
    "scripts/output/_w1050_spec.json",
    "scripts/output/_cascade_files_W1050.txt",
    # W1050 批的级联面（版本行指向 W1050 ⇒ 属 W1050 批重放范围·本批不暂存）
    ".github/workflows/README.md", "README.md", "STRUCTURE.md", "CITATION.cff",
    "docs/00-导读/项目说明.md", "archive/docs/AGENTS-ARCHIVE.md",
    "archive/docs/CHANGELOG-ARCHIVE.md", "archive/docs/W批次编号对账表-ARCHIVE.md",
    "archive/docs/file-index-ARCHIVE.md", "scripts/output/README.md",
    "scripts/output/index.md", "scripts/output/tools-inventory.md",
    "site/index.html", "site/data/cross-time-danmaku.html",
    "site/data/tag-cloud.html", "site/dukou-engine.html",
    "scripts/output/stats-changelog.json", "scripts/output/stats-index.md",
}
for ln in out.splitlines():
    p = ln[3:].strip().strip('"')
    if " -> " in p:
        p = p.split(" -> ")[1]
    if p and not p.startswith("tmpe/") and p not in W1050_EXCLUDE:
        files.append(p)
alive = sorted(p for p in files if os.path.exists(os.path.join(REPO, p.replace("/", os.sep))))
path = os.path.join(OUT, "_cascade_files_W1049.txt")
io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(alive) + "\n")
print("级联清单 %d 项 -> scripts/output/_cascade_files_W1049.txt" % len(alive))
