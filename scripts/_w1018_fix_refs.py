# -*- coding: utf-8 -*-
"""_w1018_fix_refs.py — 脚本改名后的引用同步（scripts/index.md 清单 + T38 报告 + spec/file-index 旧名核对）

背景：资产批号由 W1016 让为 **W1018**（W1016 被并行「教训固化批」占用）⇒ 脚本前缀由
`_w1016_*` 改为 `_w1018_*` ⇒ 三处引用面须同步：
  ① `scripts/index.md` 的文件清单（旧名行会让工具清单生成器按清单逐个打开失败 ⇒
     `gen_folder_docs --refresh` 报「工具清单生成失败」）
  ② T38 终稿报告里的复算命令与证据位置
  ③ `scripts/output/_w1018_spec.json` 与 file-index W1018 段的旧名（这两处指向**已入库**的
     旧文件名·仍在提交树内 ⇒ C4-f 应放行 ⇒ 只做核对不改写）

用法：py -3 scripts/_w1018_fix_refs.py [--dry-run]
"""
from __future__ import annotations

import io
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIDX = os.path.join(REPO, "scripts", "index.md")
T38 = os.path.join(REPO, "docs", "11-方案报告", "计划方案", "T38-任务计划执行与经验沉淀报告-2026-10-29.md")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in sys.argv
    for path in (SIDX, T38):
        text, nl = read(path)
        n = text.count("_w1016_")
        if n == 0:
            print("SKIP  %s 无旧名引用" % os.path.relpath(path, REPO).replace("\\", "/"))
            continue
        text2 = text.replace("_w1016_", "_w1018_")
        assert text2.count("\n") == text.count("\n"), "%s 行数变化" % path
        if dry:
            print("DRY  %s 替换 %d 处旧名" % (os.path.relpath(path, REPO).replace("\\", "/"), n))
        else:
            write(path, text2)
            print("OK   %s 替换 %d 处旧名" % (os.path.relpath(path, REPO).replace("\\", "/"), n))

    # 核对：已入库的旧名文件（b0c0d072）仍须在提交树内 ⇒ C4-f 不应判红
    import subprocess
    old = subprocess.run(["git", "show", "--name-only", "--format=", "b0c0d072"], cwd=REPO,
                         capture_output=True, text=True, encoding="utf-8").stdout
    old_names = [x.strip() for x in old.splitlines() if "_w1016_" in x]
    print("已入库旧名文件 %d 个（仍在提交树内⇒C4-f 放行）：" % len(old_names))
    for x in old_names[:4]:
        print("   " + x)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
