#!/usr/bin/env python3
"""ci_sim.py — CI 侧预演工具（W894·用户批准根修的配套工具）

## 为什么存在

多 Agent 共享同一工作树时，**本地门禁红 ≠ CI 门禁红**：

- 本地工作树里可能有并行批的**未落库件**（未跟踪）⇒ 旧口径的门禁（实算扫物理工作树）
  会判红「盘上多 N 项」；
- 而 CI 是**干净检出**（无那些未落库件）⇒ CI 侧其实绿。

于是「本地红 / CI 绿」只能靠**在干净检出里实测**来判定——手工做要一串命令（建 worktree →
跑若干门禁 → 删 worktree），极易漏跑或忘删。本工具把这条链固化为**一条命令**。

## 用法

```bash
py -3 scripts/ci_sim.py                 # 对 HEAD 做关键门禁预演（默认）
py -3 scripts/ci_sim.py --ref <commit>  # 预演指定提交
py -3 scripts/ci_sim.py --full          # 追加全量 verify_delivery --scope full（慢）
py -3 scripts/ci_sim.py --keep          # 保留临时 worktree（调试用·需手动清理）
```

## 只读保证

本工具**不改主工作树任何文件**：只在系统临时目录建 `git worktree`（detached），在其中
跑门禁，结束后 `git worktree remove --force` 清理。门禁在干净检出里若产生缓存类副产物
（如 `scripts/output/*.json` 增量缓存），只落在临时 worktree 内，随清理一并消失。
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# (标签, 命令模板) —— {py} = 解释器前缀，{root} = worktree 根
GATES = [
    ("stats 对账", "{py} scripts/stats.py --check"),
    ("文档口径体检(第31槽)", "{py} scripts/check_doc_sync.py --check"),
    ("索引健康(第17槽)", "{py} scripts/check_index_health.py"),
    ("目录新鲜度(第45槽)", "{py} scripts/check_folder_docs.py --gate"),
    ("计划方案合规(第48槽)", "{py} scripts/check_plan_template.py --gate"),
    ("CSP 零漂移", "{py} scripts/generate_csp.py --check"),
    ("全仓链接", "{py} scripts/lint_links.py --dir ."),
    ("交互绑定(W908建)", "{py} scripts/check_interaction_binding.py --gate"),
    ("页准入(W916建)", "{py} scripts/check_page_admission.py --gate"),
]


def _py() -> str:
    """解释器前缀：Windows 用 py -3（仓内约定），其余用 python3。"""
    if os.name == "nt":
        return "py -3"
    return "python3"


def _run(cmd: str, cwd: str) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=1800)
        return p.returncode, ((p.stdout or "") + (p.stderr or ""))
    except subprocess.TimeoutExpired:
        return 99, "超时（1800s）"


def main() -> int:
    ap = argparse.ArgumentParser(description="CI 侧预演（worktree 干净检出跑关键门禁）")
    ap.add_argument("--ref", default="HEAD", help="预演目标（默认 HEAD）")
    ap.add_argument("--full", action="store_true", help="追加全量 verify_delivery --scope full")
    ap.add_argument("--keep", action="store_true", help="保留临时 worktree（调试用）")
    args = ap.parse_args()

    tmp = tempfile.mkdtemp(prefix="ci_sim_")
    wt = os.path.join(tmp, "wt")
    print("== CI 侧预演 ==")
    print("目标：%s    worktree：%s" % (args.ref, wt))

    add = subprocess.run(["git", "-C", ROOT, "worktree", "add", "--detach", wt, args.ref],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    if add.returncode != 0:
        print("建 worktree 失败：%s" % (add.stderr or add.stdout).strip())
        shutil.rmtree(tmp, ignore_errors=True)
        return 2

    results = []
    try:
        gates = list(GATES)
        if args.full:
            gates.append(("全量交付门禁", "{py} scripts/verify_delivery.py --scope full"))
        for label, tmpl in gates:
            cmd = tmpl.format(py=_py(), root=wt)
            rc, out = _run(cmd, wt)
            tail = ""
            for ln in reversed(out.strip().split("\n")):
                if ln.strip():
                    tail = ln.strip()
                    break
            results.append((label, rc, tail))
            print("%-28s %s  %s" % (label, "PASS" if rc == 0 else "FAIL(%d)" % rc, tail[:120]))
    finally:
        if args.keep:
            print("（--keep：保留 worktree 于 %s，手动清理：git worktree remove --force %s）" % (wt, wt))
        else:
            subprocess.run(["git", "-C", ROOT, "worktree", "remove", "--force", wt],
                           capture_output=True, text=True)
            shutil.rmtree(tmp, ignore_errors=True)

    failed = [r for r in results if r[1] != 0]
    print("---- CI 侧预演：%d 项，PASS %d，FAIL %d ----" % (len(results), len(results) - len(failed), len(failed)))
    if failed:
        print("失败项：%s" % "、".join(r[0] for r in failed))
        print("提示：本地红而此处绿 = 本地工作树含他方未落库件（本地红/CI 绿分歧族）；"
              "两处都红 = 真问题，须修到此处也绿。")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
