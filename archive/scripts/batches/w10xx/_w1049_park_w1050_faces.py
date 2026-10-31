# -*- coding: utf-8 -*-
"""_w1049_park_w1050_faces.py — 停泊 W1050 批的当前态面（版本行/索引登记）

背景（W1049）：用户 2026-10-31 令「W1050 六件在途件·收官时摘出勿卷入」。
W1050 批除六件外还有 **19 个当前态面**（版本行指向 W1050 + 归档索引登记），
它们同样属 W1050 批重放范围 ⇒ 本批不提交、不改动其工作树内容。

处置：把这 19 个文件的**工作树版本**备份到 `tmpe/_w1050_park/faces/`
        然后从工作树**恢复到 HEAD 版**（内容零丢失·W1050 批重放时从备份取回）。
⇒ 工作树 == 本批提交内容 ⇒ 门禁读工作树时不再因 W1050 在途件报红。

**不改** W1050 的六件在途件本身（它们是 W1050 的实质工作·保持在工作树未暂存状态·
      由 `_w1049_isolate_w1050.py` 撤出暂存即可）。

用法：py -3 archive/scripts/batches/w10xx/_w1049_park_w1050_faces.py [--restore]
"""
import io
import os
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
PARK = os.path.join(REPO, "tmpe", "_w1050_park", "faces")

# W1050 批的当前态面（19 项）
FACES = [
    ".github/workflows/README.md",
    "CITATION.cff",
    "README.md",
    "STRUCTURE.md",
    "docs/00-导读/项目说明.md",
    "archive/docs/AGENTS-ARCHIVE.md",
    "archive/docs/CHANGELOG-ARCHIVE.md",
    "archive/docs/file-index-ARCHIVE.md",
    "archive/docs/W批次编号对账表-ARCHIVE.md",
    "scripts/output/README.md",
    "scripts/output/index.md",
    "scripts/output/stats.json",
    "scripts/output/stats-changelog.json",
    "scripts/output/stats-index.md",
    "scripts/output/tools-inventory.md",
    "site/data/cross-time-danmaku.html",
    "site/data/tag-cloud.html",
    "site/dukou-engine.html",
    "site/index.html",
]


def git(*a):
    return subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO] + list(a),
                          capture_output=True).stdout.decode("utf-8", "replace")


def restore():
    print("== 从 tmpe/_w1050_park/faces/ 还原 ==")
    for rel in FACES:
        src = os.path.join(PARK, rel.replace("/", "__"))
        if not os.path.exists(src):
            print("  SKIP  %s 无备份" % rel)
            continue
        dst = os.path.join(REPO, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        print("  OK    已还原 %s" % rel)
    return 0


def main() -> int:
    if "--restore" in sys.argv:
        return restore()

    os.makedirs(PARK, exist_ok=True)
    changed = []
    for rel in FACES:
        p = os.path.join(REPO, rel.replace("/", os.sep))
        if not os.path.exists(p):
            print("  SKIP  %s 磁盘不存在" % rel)
            continue
        diff = git("diff", "--", rel)
        if not diff.strip():
            print("  SKIP  %s 工作树与 HEAD 一致（无需停泊）" % rel)
            continue
        backup = os.path.join(PARK, rel.replace("/", "__"))
        shutil.copyfile(p, backup)
        changed.append(rel)
    print("备份 %d 个当前态面到 tmpe/_w1050_park/faces/" % len(changed))
    for rel in changed:
        print("  - %s" % rel)

    print("\n== 恢复到 HEAD 版（工作树内容回到本批提交前状态）==")
    if changed:
        r = subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO,
                            "checkout", "HEAD", "--"] + changed, capture_output=True)
        if r.returncode != 0:
            print("FAIL  恢复失败：%s" % r.stderr.decode("utf-8", "replace"))
            return 1
        print("OK    已恢复 %d 个文件到 HEAD 版" % len(changed))
    print("（W1050 批重放时：`python archive/scripts/batches/w10xx/_w1049_park_w1050_faces.py --restore`）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
