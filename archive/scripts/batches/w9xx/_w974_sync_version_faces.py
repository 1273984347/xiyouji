# -*- coding: utf-8 -*-
"""_w974_sync_version_faces.py — 同步版本面（`.github/workflows/README.md` 两处 W 号）

站点面门禁报两项：
  ① `.github/workflows/README.md 头部版本 W973 != 现役 W974`
  ② `.github/workflows/README.md 里程碑行上限 W973 != 现役 W974`
⇒ 两处「范围标记」需推进到 W974；**历史条目里的 W973 一律不动**（那是历史记录）。

共享面 ⇒ 以 `HEAD:<file>` 为基底做两处精确替换 → `git update-index --cacheinfo` 精确暂存，
工作树同步为同一内容。

用法：py -3 scripts/_w974_sync_version_faces.py [--dry-run]
"""
import io
import os
import subprocess
import sys

REPO = r"D:\xiyouji"
REL = ".github/workflows/README.md"

REPL = [
    ("→ W450-W973** — 西游记解读项目（`D:\\xiyouji`，W973）的",
     "→ W450-W974** — 西游记解读项目（`D:\\xiyouji`，W974）的"),
    ("> **W450-W973**：verify 门禁体系扩展",
     "> **W450-W974**：verify 门禁体系扩展"),
]


def main() -> int:
    dry = "--dry-run" in sys.argv
    p = subprocess.run(["git", "show", "HEAD:" + REL], cwd=REPO, capture_output=True)
    if p.returncode != 0:
        print("FATAL 无法读取 HEAD:%s" % REL)
        return 2
    head = p.stdout.decode("utf-8").replace("\r\n", "\n")
    new = head
    for old, rep in REPL:
        if new.count(old) != 1:
            print("ABORT 锚点命中 %d 次（期望 1）：%s" % (new.count(old), old[:50]))
            return 2
        new = new.replace(old, rep, 1)
    if dry:
        print("DRY-RUN：2 处替换可命中")
        return 0
    # 工作树同步（原子）
    ap = os.path.join(REPO, REL.replace("/", os.sep))
    raw = io.open(ap, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    tmp = ap + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(new.replace("\n", nl).encode("utf-8"))
    os.replace(tmp, ap)
    # 精确暂存
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO,
                          input=new.encode("utf-8"), capture_output=True)
    if blob.returncode != 0:
        print("FATAL hash-object 失败")
        return 2
    b = blob.stdout.decode().strip()
    q = subprocess.run(["git", "update-index", "--cacheinfo", "100644," + b + "," + REL],
                       cwd=REPO, capture_output=True)
    if q.returncode != 0:
        print("FATAL update-index 失败: " + q.stderr.decode("utf-8", "replace")[:200])
        return 2
    print("OK  %s：2 处版本标记 W973 → W974（精确暂存 blob %s·工作树已同步）" % (REL, b[:8]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
