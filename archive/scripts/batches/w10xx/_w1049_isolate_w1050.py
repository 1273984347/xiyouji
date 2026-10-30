# -*- coding: utf-8 -*-
"""_w1049_isolate_w1050.py — 摘出 W1050 批的 6 个在途件（用户 2026-10-31 令）

用户令：「工作树里有另一批（W1050 判据批）的 6 个在途件，收官提交时请摘出勿卷入：
scripts/verify_delivery.py、scripts/check_doc_sync.py、docs/agent/gates.md、
scripts/output/_w1050_spec.json、scripts/output/_cascade_files_W1050.txt、台账末尾的 W1050 行。
你收官完成后告知用户，W1050 批会自动重放。」

处置口径（**不丢失他方工作**）：
  ① 3 个脚本/文档件：从暂存区**撤出**（`git restore --staged`）⇒ 保持工作树内容不变·
     不进我的提交 ⇒ W1050 批重放时仍可原样取用；
  ② 2 个 spec/清单件：若为未跟踪文件则移出到 `tmpe/`（gitignore 区）·内容不丢；
  ③ 台账 W1050 行：从我的提交中排除（精确暂存时用 HEAD 版台账 + 仅替换我方 W1049 行）。

**不做**：不删除任何他方文件·不改他方文件内容·不 commit 他的改动。
用法：py -3 archive/scripts/batches/w10xx/_w1049_isolate_w1050.py [--dry-run]
"""
import io
import os
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))

# 用户点名的 6 件
SCRIPT_FILES = [
    "scripts/verify_delivery.py",
    "scripts/check_doc_sync.py",
    "docs/agent/gates.md",
]
OUTPUT_FILES = [
    "scripts/output/_w1050_spec.json",
    "scripts/output/_cascade_files_W1050.txt",
]
LEDGER = "docs/00-导读/W批次编号对账表.md"


def git(*a):
    return subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO] + list(a),
                          capture_output=True).stdout.decode("utf-8", "replace")


def main() -> int:
    dry = "--dry-run" in sys.argv
    print("== ① 撤出暂存（W1050 三个脚本/文档件·工作树内容保留）==")
    for f in SCRIPT_FILES:
        abs_p = os.path.join(REPO, f.replace("/", os.sep))
        if not os.path.exists(abs_p):
            print("  SKIP  %s 磁盘不存在" % f)
            continue
        # 是否在暂存区
        staged = git("diff", "--cached", "--name-only")
        in_staged = f in staged.splitlines()
        if not in_staged:
            print("  SKIP  %s 未在暂存区（工作树改动保留）" % f)
            continue
        if dry:
            print("  DRY  将撤出暂存：%s" % f)
            continue
        subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO,
                        "restore", "--staged", "--", f], check=True)
        print("  OK    已撤出暂存（工作树内容保留）：%s" % f)

    print("\n== ② W1050 输出件：撤出暂存（若已暂存）· 未跟踪者移入 tmpe/ ==")
    tmpe = os.path.join(REPO, "tmpe")
    os.makedirs(tmpe, exist_ok=True)
    staged_now = git("diff", "--cached", "--name-only").splitlines()
    for f in OUTPUT_FILES:
        abs_p = os.path.join(REPO, f.replace("/", os.sep))
        if not os.path.exists(abs_p):
            print("  SKIP  %s 磁盘不存在" % f)
            continue
        if f in staged_now:
            if dry:
                print("  DRY  将撤出暂存：%s" % f)
                continue
            subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO,
                            "restore", "--staged", "--", f], check=True)
            print("  OK    已撤出暂存：%s" % f)
            # 撤出后若成为「未跟踪」⇒ 移入 tmpe/（内容不丢）
            untracked = git("ls-files", "--others", "--exclude-standard").splitlines()
            if f in untracked:
                dest = os.path.join(tmpe, os.path.basename(f))
                if os.path.exists(dest):
                    dest = os.path.join(tmpe, "w1050-" + os.path.basename(f))
                shutil.move(abs_p, dest)
                print("        已移入 %s（内容保留·gitignore 区）"
                      % os.path.relpath(dest, REPO).replace("\\", "/"))
            continue
        tracked = f in git("ls-files").splitlines()
        if tracked:
            print("  SKIP  %s 已跟踪且未暂存（提交时不 add 即可排除）" % f)
            continue
        if dry:
            print("  DRY  将移动：%s -> tmpe/" % f)
            continue
        dest = os.path.join(tmpe, os.path.basename(f))
        if os.path.exists(dest):
            dest = os.path.join(tmpe, "w1050-" + os.path.basename(f))
        shutil.move(abs_p, dest)
        print("  OK    已移动：%s -> %s（内容保留）"
              % (f, os.path.relpath(dest, REPO).replace("\\", "/")))

    print("\n== ③ 台账 W1050 行排除 ==")
    print("  台账为共享面 ⇒ 收官提交时用「HEAD 版台账 + 仅替换我方 W1049 行」精确暂存")
    print("  （W1050 行不进入我的提交·W1050 批重放时由其自行取用）")

    print("\n== 复核：暂存区与工作树现状 ==")
    print("  staged=%d 项" % len(git("diff", "--cached", "--name-only").splitlines()))
    for f in SCRIPT_FILES:
        st = git("diff", "--cached", "--name-only")
        print("   %-34s 在暂存区=%s · 工作树存在=%s"
              % (f, f in st.splitlines(),
                 os.path.exists(os.path.join(REPO, f.replace("/", os.sep)))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
