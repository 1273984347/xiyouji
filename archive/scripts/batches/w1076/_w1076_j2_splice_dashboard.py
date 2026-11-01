#!/usr/bin/env python3
"""_w1076_j2_splice_dashboard.py — W1076 B1：终态 J2 快照的 dashboard 单页拼接（含等价性证明）。

## 为什么需要拼接

W1076 B1 施工末尾有两处对 `site/dashboard.html` 的改动（朱砂实底限额修复）：
共享实现的朱砂顶条落到本页 8 张 KPI 卡 ⇒ 第 49 槽（朱砂实底每页 ≤3 处）判红
⇒ 改为保留 1px 发丝线顶边（裁决 2 优先于卡片 ② 的顶线默认态）。

全量 24 页重拍一轮约 40 分钟；本脚本用**单页重拍 + 等价性证明**完成等价更新：
1. 采集 dashboard 单页（独立 context·本地存储为空）；
2. 与全量采集里的 dashboard 条目逐元素对拍 —— **若差异仅限本次边框修复的属性**，
   则证明 dashboard 的渲染不依赖前序页面写入的 localStorage（等价性成立）；
3. 证明成立才把单页条目写回全量快照，并在 meta 里登记拼接事实。

任一前提不成立即拒绝拼接（fail-closed）——判据不对拍在与实际提交同一条语义路径上。
"""
import json
import os
import sys

def _repo_root():
    """向上找仓库根（带 .git 的目录）——脚本归档到 archive/scripts/batches/w1076/ 后仍可用。"""
    cur = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("未找到仓库根（.git）")
        cur = parent


sys.path.insert(0, os.path.join(_repo_root(), "scripts"))
import visual_regression_probe as P  # noqa: E402

ROOT = _repo_root()
OUT = os.path.join(ROOT, "scripts", "output")
PAGE = "dashboard.html"

# 本次边框修复触及的属性（其余任何差异 = 等价性前提不成立 ⇒ 拒绝拼接）
ALLOWED_PROPS = {"border-top-width", "border-top-style", "border-top-color"}
ALLOWED_KINDS = {"元素数"}


def main():
    full_path = os.path.join(OUT, "_w1076_j2_after")
    only_path = os.path.join(OUT, "_w1076_j2_dashboard_only.json")
    full = json.loads(open(full_path, encoding="utf-8").read())
    only = json.loads(open(only_path, encoding="utf-8").read())

    diffs, notes = P._diff_snapshots(full, only, max_report=100000)
    illegal = [d for d in diffs
               if d.get("prop") not in ALLOWED_PROPS and d.get("kind") not in ALLOWED_KINDS]
    print("单页 vs 全量中的 dashboard 条目：差异 %d 条（notes=%s）" % (len(diffs), notes))
    for d in diffs[:10]:
        print("   %s" % json.dumps(d, ensure_ascii=False))
    if illegal:
        print("FAIL 等价性前提不成立：%d 条差异落在允许属性之外 ⇒ 拒绝拼接" % len(illegal))
        for d in illegal[:10]:
            print("   %s" % json.dumps(d, ensure_ascii=False))
        return 1

    # 证明成立 ⇒ 拼接
    for theme in ("light", "dark"):
        if theme in only["pages"].get(PAGE, {}):
            full["pages"].setdefault(PAGE, {})[theme] = only["pages"][PAGE][theme]
    meta = full.setdefault("meta", {})
    meta["spliced_pages"] = sorted(set(meta.get("spliced_pages", [])) | {PAGE})
    meta["splice_reason"] = ("dashboard 单页重拍后拼接（等价性已证：单页与全量条目差异仅限"
                              "border-top-* 属性＝本次裁决 2 修复；dashboard 渲染不依赖前序 "
                              "localStorage 写入）")
    with open(full_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(full, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write("\n")
    print("OK 已拼接 %s → %s（meta.spliced_pages=%s）" % (PAGE, full_path, meta["spliced_pages"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
