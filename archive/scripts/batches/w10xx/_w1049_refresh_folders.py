# -*- coding: utf-8 -*-
"""_w1049_refresh_folders.py — 精准刷新本批涉及的目录文档（第 45 门禁 C2/C3）

背景（W1049 盲审 P0-2/P1-4）：本批新增件已入 Git 索引，但下列目录的 index.md /
README.md 未刷新 ⇒ 第 45 门禁报「索引有清单无」：
  · assets/promo/plate-set            （新增 12 张母版 PNG/WEBP）
  · assets/promo/plate-set/raw        （新增子目录 round18）
  · assets/promo/plate-set/raw/round18（新增 12 件原件）
  · site/static/images                （新增 12 站点版 + 12 og 版）
  · archive/scripts/batches/w10xx     （新增本批脚本）
  · scripts/output                    （新增本批 spec/清单/批次件；且含 W1050 幽灵预引）

**为何不用全量 `gen_folder_docs.py --refresh`**：它会重写全部 220 个在管目录
⇒ 远超本批改动面（其余目录属 W1050 批重放范围）⇒ 本脚本 **monkey-patch
`scan_dirs()`** 只返回本批 6 个目录，再调用**同一个 main()** ⇒ 产物与全量跑
逐字一致（同一渲染逻辑·同一所有权判定）。

用法：py -3 archive/scripts/batches/w10xx/_w1049_refresh_folders.py [--dry-run]
"""
import importlib.util
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
GEN = os.path.join(REPO, "scripts", "gen_folder_docs.py")

TARGETS = [
    "assets/promo/plate-set",
    "assets/promo/plate-set/raw",
    "assets/promo/plate-set/raw/round18",
    "site/static/images",
    "archive/scripts/batches/w10xx",
    "scripts/output",
]


def main() -> int:
    dry = "--dry-run" in sys.argv
    # 生成器 `import tracked_files as tf` ⇒ 需把 scripts/ 加入 sys.path
    sys.path.insert(0, os.path.join(REPO, "scripts"))
    spec = importlib.util.spec_from_file_location("gen_folder_docs", GEN)
    gfd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gfd)

    orig_scan = gfd.scan_dirs

    def patched_scan():
        ds = orig_scan()
        want = {os.path.join(REPO, t.replace("/", os.sep)) for t in TARGETS}
        return [d for d in ds if d in want]

    gfd.scan_dirs = patched_scan
    print("精准刷新目标 %d 个目录（其余 %d 个目录不动）" % (len(TARGETS), 0))
    sys.argv = [GEN, "--refresh"] + (["--dry-run"] if dry else [])
    rc = gfd.main()
    print("---- 生成器退出码 %d ----" % rc)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
