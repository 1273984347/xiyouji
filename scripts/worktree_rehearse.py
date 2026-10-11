#!/usr/bin/env python3
"""worktree_rehearse.py — worktree 预演法工具化（W701·S-26·用户圈选开工）。

E-14 三步手工的封装：在仅含 tracked 文件的临时 worktree 中复刻「提交后的 CI 环境」，
把工作区未提交改动（含新增非 gitignore 文件）定向拷入后跑校验——提交前本地证伪
「本地绿≠CI 绿」类问题（W700 CI 首跑 5 broken 的预防线：目标侧 untracked 件在
checkout 环境必断）。

用法：
  python scripts/worktree_rehearse.py                     # 默认 lint_links --dir docs
  python scripts/worktree_rehearse.py --tool lint --dir . # 全仓链接口径
  python scripts/worktree_rehearse.py --tool verify       # verify_delivery（快速档较慢）
  python scripts/worktree_rehearse.py --keep              # 调试：保留临时树不清理

步骤：git worktree add --detach（tmpe/_rehearsal）→ 收集「工作区 vs HEAD」改动集
（modified + 新增非 gitignore 文件·跳过 tmpe/）→ 逐文件拷入 → 在临时树内跑校验 →
always 清理。git 不可用/非仓库 → exit 2。
"""
import argparse
import os
import shutil
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, ".."))
WT = os.path.join(ROOT, "tmpe", "_rehearsal")


def git(args, **kw):
    return subprocess.run(["git", "-c", "core.quotePath=false"] + args,
                          cwd=ROOT, capture_output=True, text=True, **kw)


def changed_files():
    files = set()
    for args in (["diff", "--name-only", "HEAD"], ["ls-files", "--others", "--exclude-standard"]):
        r = git(args)
        if r.returncode != 0:
            return None
        files |= {ln.strip().replace("\\", "/") for ln in r.stdout.splitlines() if ln.strip()}
    return {f for f in files if not f.startswith("tmpe/")}


def main():
    ap = argparse.ArgumentParser(description="worktree 预演：仅 tracked 环境跑校验")
    ap.add_argument("--tool", choices=["lint", "verify"], default="lint")
    ap.add_argument("--dir", default="docs", help="lint_links 扫描目录（默认 docs）")
    ap.add_argument("--keep", action="store_true", help="保留临时树（调试）")
    args = ap.parse_args()

    r = git(["rev-parse", "--show-toplevel"])
    if r.returncode != 0:
        print("[rehearse] 非 git 仓库")
        return 2
    if git(["worktree", "list"]).stdout.find("_rehearsal") >= 0:
        git(["worktree", "remove", "--force", WT])

    add = git(["worktree", "add", "--detach", WT, "HEAD"])
    if add.returncode != 0:
        print("[rehearse] worktree add 失败：%s" % add.stderr.strip()[:200])
        return 2

    ok = True
    try:
        files = changed_files()
        if files is None:
            print("[rehearse] git 改动集读取失败")
            return 2
        copied = 0
        for f in sorted(files):
            src = os.path.join(ROOT, f)
            dst = os.path.join(WT, f)
            if not os.path.isfile(src):
                continue  # 工作区已删除的文件：预演树保持 HEAD 态即可（删除 diff 极少影响链接面）
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1
        print("[rehearse] 临时树 tmpe/_rehearsal 就绪（HEAD 态）+ 拷入工作区改动 %d 文件" % copied)

        if args.tool == "lint":
            cmd = [sys.executable, os.path.join(_HERE, "lint_links.py"), "--dir", args.dir]
        else:
            cmd = [sys.executable, os.path.join(_HERE, "verify_delivery.py")]
        run = subprocess.run(cmd, cwd=WT, capture_output=True, text=True)
        tail = [x for x in (run.stdout + run.stderr).splitlines()
                if "[BROKEN]" in x or "校验完成" in x or "FAIL" in x][-6:]
        print("[rehearse] %s（cwd=临时树·exit %d）" % (args.tool, run.returncode))
        for x in tail:
            print("  " + x)
        ok = run.returncode == 0
        print("[rehearse] 结论：%s" % ("预演通过（等价 CI 环境绿）" if ok else "预演失败——提交前先修"))
        return 0 if ok else 1
    finally:
        if args.keep:
            print("[rehearse] --keep：临时树保留于 %s" % WT)
        else:
            git(["worktree", "remove", "--force", WT])


if __name__ == "__main__":
    sys.exit(main())
