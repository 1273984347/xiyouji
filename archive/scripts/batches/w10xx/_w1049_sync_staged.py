# -*- coding: utf-8 -*-
"""_w1049_sync_staged.py — 让暂存区 ⊇ 当批级联清单（第 45/31 门禁 C4-e 要求）

做法：读 `scripts/output/_cascade_files_W1049.txt` ⇒ 逐项 `git add`（**仅清单内文件**）
⇒ 清单外文件不动（他方在途件保持不暂存）。
用法：py -3 archive/scripts/batches/w10xx/_w1049_sync_staged.py [--dry-run]
"""
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
MANIFEST = os.path.join(REPO, "scripts", "output", "_cascade_files_W1049.txt")


def main() -> int:
    dry = "--dry-run" in sys.argv
    paths = [p.strip() for p in io.open(MANIFEST, encoding="utf-8").read().splitlines()
             if p.strip()]
    missing = []
    for p in paths:
        if not os.path.exists(os.path.join(REPO, p.replace("/", os.sep))):
            print("GONE  %s（磁盘不存在·跳过）" % p)
            continue
        # 已暂存？⇒ 查 git 索引
        r = subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO,
                            "ls-files", "--error-unmatch", "--", p],
                           capture_output=True)
        if r.returncode == 0:
            continue
        missing.append(p)
    print("清单 %d 项 · 未暂存 %d 项" % (len(paths), len(missing)))
    if not missing:
        print("OK    暂存区已覆盖当批级联清单")
        return 0
    if dry:
        for p in missing[:20]:
            print("  DRY  git add %s" % p)
        return 0
    for p in missing:
        subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO,
                        "add", "--", p], check=True)
    print("OK    已暂存 %d 项" % len(missing))
    for p in missing[:20]:
        print("  + %s" % p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
