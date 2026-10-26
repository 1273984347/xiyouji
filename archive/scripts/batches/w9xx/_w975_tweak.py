# -*- coding: utf-8 -*-
"""_w975_tweak.py — 通用「字面替换 + 精确暂存」工具（W975 收尾微调用）

用法：py -3 scripts/_w975_tweak.py <相对路径> <旧串> <新串> [--dry-run]
  · 旧串必须**逐字**复制（禁凭印象重写）·命中数必须 = 1，否则中止不写盘
  · 以 HEAD 为基底做替换 → 原子写工作树 → `git update-index --cacheinfo` 精确暂存
    （共享面不整份 add；并发会话在途内容既不入本批提交也不被抹掉）
"""
import io
import os
import subprocess
import sys

REPO = r"D:\xiyouji"


def main() -> int:
    argv = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry = "--dry-run" in sys.argv
    if len(argv) != 3:
        print("用法: py -3 scripts/_w975_tweak.py <相对路径> <旧串> <新串> [--dry-run]")
        return 2
    rel, old, new = argv
    # 基底 = **索引版**（同批内前几次修改在索引里·HEAD 版还没有 ⇒ 用 HEAD 会命中 0 次）
    # 索引版是本批自己精确暂存的内容（含本批段）⇒ 替换不引入他人在途内容
    p = subprocess.run(["git", "show", ":" + rel], cwd=REPO, capture_output=True)
    src_ref = ":"
    if p.returncode != 0 or not p.stdout:
        p = subprocess.run(["git", "show", "HEAD:" + rel], cwd=REPO, capture_output=True)
        src_ref = "HEAD:"
    if p.returncode != 0:
        print("FATAL 无法读取 %s%s" % (src_ref, rel))
        return 2
    head = p.stdout.decode("utf-8").replace("\r\n", "\n")
    n = head.count(old)
    if n != 1:
        print("FATAL 旧串命中 %d 次（期望 1）：%s" % (n, old[:60]))
        return 2
    out = head.replace(old, new, 1)
    if dry:
        print("DRY  %s：%d → %d 字符" % (rel, len(head), len(out)))
        return 0
    ap = os.path.join(REPO, rel.replace("/", os.sep))
    raw = io.open(ap, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    tmp = ap + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(out.replace("\n", nl).encode("utf-8"))
    os.replace(tmp, ap)
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO,
                          input=out.encode("utf-8"), capture_output=True)
    if blob.returncode != 0:
        print("FATAL hash-object 失败")
        return 2
    b = blob.stdout.decode().strip()
    q = subprocess.run(["git", "update-index", "--cacheinfo", "100644," + b + "," + rel],
                       cwd=REPO, capture_output=True)
    if q.returncode != 0:
        print("FATAL update-index 失败: " + q.stderr.decode("utf-8", "replace")[:200])
        return 2
    print("OK  %s：已替换并精确暂存（blob %s）" % (rel, b[:8]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
