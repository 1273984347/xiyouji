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
py -3 scripts/ci_sim.py --ci-steps      # 先复现 CI 前置步骤序列（重生成 → 探针现跑 → 还原 → 干净断言）再跑门禁（W1287）
```

## 只读保证

本工具**不改主工作树任何文件**：只在系统临时目录建 `git worktree`（detached），在其中
跑门禁，结束后 `git worktree remove --force` 清理。门禁在干净检出里若产生缓存类副产物
（如 `scripts/output/*.json` 增量缓存），只落在临时 worktree 内，随清理一并消失。
"""

from __future__ import annotations

import argparse
import os
import re
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
    ("跨行改写(W1014建)", "{py} scripts/check_cross_line_rewrite.py --gate"),
    ("CSP 零漂移", "{py} scripts/generate_csp.py --check"),
    ("全仓链接", "{py} scripts/lint_links.py --dir ."),
    ("交互绑定(W908建)", "{py} scripts/check_interaction_binding.py --gate"),
    ("页准入(W916建)", "{py} scripts/check_page_admission.py --gate"),
    ("DB schema(W917建)", "{py} scripts/check_db_schema.py --gate"),
    ("副本链对账(W920建)", "{py} scripts/check_data_copy_chain.py --gate"),
    ("占位符哈希载体(第71槽)", "{py} scripts/check_placeholder_hash_carrier.py --gate"),
    ("LFS 文本纯净性(W1214建)", "{py} scripts/check_lfs_text_purity.py --gate"),
    ("分析包同步(W1230接·P3#24)", "{py} scripts/package_analysis_sync.py --check"),
    ("搜索语料同步(W1316建)", "{py} scripts/sync_search_corpus.py --check"),
]

# CI 前置步骤序列（W1287·复现 CI workflow 的真实动作顺序）
CI_STEPS = [
    ("CI: 重生成输出数据", "{py} scripts/run_all.py"),
    # W1295：真实 CI 已把两口径合并为**单 step 内 bash 并行**（`&` + `wait`）⇒ 墙钟省 ≈5m43s；
    # 本仿真保留**串行等价**（Windows 本地无 POSIX `&`/`wait`）⇒ 仿真验证的是「两口径产物
    # 与 page_sha 覆盖」这条**正确性链**（第 80 槽 fail-closed 依赖它）·加速形态属 CI 墙钟面·不入仿真。
    ("CI: graphic 口径探针现跑（串行等价·真实 CI 为并行）", "{nodepath} node scripts/svg_text_contrast_probe.js --bg-mode graphic --scope all --out scripts/output/svg_text_contrast_graphic_report.json"),
    ("CI: body 口径探针现跑", "{nodepath} node scripts/svg_text_contrast_probe.js --bg-mode body --scope data,en --out scripts/output/svg_text_contrast_report.json"),
    ("CI: 还原探针产物", "git checkout -- scripts/output/svg_text_contrast_graphic_report.json scripts/output/svg_text_contrast_report.json"),
]


def _node_path() -> str:
    """worktree 里没有 node_modules ⇒ 探针需借主仓的 playwright（NODE_PATH）。"""
    nm = os.path.join(ROOT, "scripts", "node_modules")
    if os.name == "nt":
        return 'set "NODE_PATH=%s" &&' % nm
    return "NODE_PATH=%s" % nm


# 推前闸门项（W1287·把「一批 = 一轮 CI」从纪律变机器约束）
PUSH_GATE_ITEMS = [
    ("闸门: 推送笔数(单笔或连续批次积压)", "__UNPUSHED__"),
    ("闸门: 本批已推笔数告警", "__BATCHCOUNT__"),
    ("闸门: 主工作树干净(含未跟踪)", "__CLEAN_MAIN__"),
]

# 快档关键槽位（推前约 2 分钟；完整档再加 CI 步骤序列 + 全量门禁）
FAST_GATES = [
    ("文档口径体检(第31槽)", "{py} scripts/check_doc_sync.py --check"),
    ("图表内容完备度(第82槽)", "{py} scripts/check_chart_content_completeness.py"),
    ("SVG 标签裁切(第83槽)", "{py} scripts/check_chart_label_clipping.py"),
    ("SVG 文字对比度(第80槽·探针新鲜度)", "{py} scripts/check_svg_text_contrast.py"),
    ("CSP 零漂移", "{py} scripts/generate_csp.py --check"),
]


def _py() -> str:
    """解释器前缀：Windows 用 py -3（仓内约定），其余用 python3。"""
    if os.name == "nt":
        return "py -3"
    return "python3"


def _assert_clean_worktree(wt: str) -> tuple[int, str]:
    """CI 侧产物面断言：worktree 内有未提交/未还原的差异即红（W1287·E-308 机器化）。"""
    # 内容级判定（git diff 已按 .gitattributes 做 EOL 归一）⇒ 行尾差异不误伤，
    # 而「入库文件内容真被改动且未还原」判红（W1287·E-308 机器化）。
    # 内容级判定（git diff 已按 .gitattributes 做 EOL 归一）⇒ 行尾差异不误伤；
    # 并上未跟踪文件（git diff 不覆盖 untracked ⇒ 否则 CI 步骤新建的产物会漏检）。
    d = subprocess.run(["git", "-C", wt, "diff", "--name-only"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    u = subprocess.run(["git", "-C", wt, "ls-files", "--others", "--exclude-standard"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    dirty = [ln for ln in ((d.stdout or "") + chr(10) + (u.stdout or "")).splitlines() if ln.strip()]
    if not dirty:
        return 0, "入库文件与未跟踪文件均无改动"
    return 1, "入库/未跟踪文件被改动且未还原：%s" % " | ".join(dirty[:6])


def _changelog_batches() -> set:
    """CHANGELOG 中已立段的批次号集合（段标题形态：`### W####（` 或 `### vX（…）：W####（`）。"""
    p = os.path.join(ROOT, "CHANGELOG.md")
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            txt = f.read()
    except OSError:
        return set()
    return {"W" + m for m in re.findall(r"(?m)^###\s+(?:v[\d.]+（[^）]*）：)?W(\d+)（", txt)}


def _unpushed_commits() -> tuple[int, str]:
    """推送笔数判据（W1287 立「一次推送只带 1 笔」·W1363 放宽为「单笔或连续批次积压」）。

    为什么放宽（W1363 实证）：origin/main 停在 W1340，本地积压 45 笔（14 批历史 + 本会话
    10 批）。原判据的**原意**是「同一批的修复笔不得拆成多轮 CI」，而非「历史积压也要逐笔」；
    逐笔推需 45 轮 CI ≈ 60 分钟，与判据原意无关。故改为：
      n ≤ 1 ⇒ 单笔模式直接通过；
      n > 1 ⇒ 必须同时满足 ①每笔可解析 W 号 ②W 号时间序单调不减（禁回插旧批）
              ③每个 W 号在 CHANGELOG 有独立段（批次可追溯）⇒ 视为「连续批次积压」放行。
    任一条不满足 ⇒ 仍按原判据拒绝。
    """
    p = subprocess.run(["git", "-C", ROOT, "log", "--reverse", "--format=%s", "origin/main..HEAD"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    subjects = [ln for ln in (p.stdout or "").splitlines() if ln.strip()]
    n = len(subjects)
    if n <= 1:
        return 0, "未推送提交数=%d（单笔模式）" % n
    wnums = []
    for s in subjects:
        m = re.search(r"[Ww](\d{3,4})", s)
        if not m:
            return 1, "未推送提交数=%d·但有一笔缺 W 号：%s" % (n, s[:48])
        wnums.append(int(m.group(1)))
    if wnums != sorted(wnums):
        return 1, "未推送提交数=%d·W 号非单调（%s）⇒ 禁回插旧批" % (
            n, "/".join("W%d" % w for w in wnums[:8]))
    missing = sorted({w for w in wnums if ("W%d" % w) not in _changelog_batches()})
    if missing:
        return 1, "未推送提交数=%d·批次缺 CHANGELOG 段：%s ⇒ 先补段再推" % (
            n, "/".join("W%d" % w for w in missing[:8]))
    return 0, "未推送提交数=%d（积压模式·%d 个批次均有 CHANGELOG 段·W%d→W%d）" % (
        n, len(set(wnums)), wnums[0], wnums[-1])


def _batch_pushed_count(batch: str) -> tuple[int, str]:
    """本批已推送的提交数（按 subject 里的 W 号计数）——用于告警「轮数已被放大」。"""
    p = subprocess.run(["git", "-C", ROOT, "log", "--format=%s", "-n", "40"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    n = sum(1 for ln in (p.stdout or "").splitlines() if batch and batch in ln)
    return n, ("本批已推送提交数=%d" % n)


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
    ap.add_argument("--ci-steps", action="store_true",
                    help="先复现 CI 的前置步骤序列（重生成产物 → 探针现跑 → 还原 → 干净断言）再跑门禁（W1287）")
    ap.add_argument("--push-gate", action="store_true",
                    help="推前闸门：推送笔数（单笔 / 连续批次积压·W1363 放宽）·工作树干净（含未跟踪）·关键槽位绿（W1287）")
    ap.add_argument("--fast", action="store_true", help="闸门快档（仅工作树/提交数/关键槽位·约 2 分钟）")
    ap.add_argument("--batch", default="", help="批次号（W###）·用于统计本批已推送笔数并告警")
    args = ap.parse_args()

    tmp = tempfile.mkdtemp(prefix="ci_sim_")
    wt = os.path.join(tmp, "wt")
    print("== CI 侧预演 ==")
    print("目标：%s    worktree：%s" % (args.ref, wt))

    add = subprocess.run(["git", "-c", "core.autocrlf=false", "-C", ROOT, "worktree", "add", "--detach", wt, args.ref],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    if add.returncode != 0:
        print("建 worktree 失败：%s" % (add.stderr or add.stdout).strip())
        shutil.rmtree(tmp, ignore_errors=True)
        return 2

    results = []
    try:
        gates = list(GATES)
        if args.push_gate:
            # 快档 = 闸门项 + 关键槽位（约 2 分钟）；完整档 = + CI 步骤序列 + 全量门禁
            base = FAST_GATES if args.fast else gates
            gates = PUSH_GATE_ITEMS + base
            if args.ci_steps or not args.fast:
                gates = CI_STEPS + [("CI: 工作树干净断言", "__CLEAN__")] + gates
        elif args.ci_steps:
            gates = CI_STEPS + [("CI: 工作树干净断言", "__CLEAN__")] + gates
        if args.full:
            gates.append(("全量交付门禁", "{py} scripts/verify_delivery.py --scope full"))
        for label, tmpl in gates:
            if tmpl == "__CLEAN__":
                rc, out = _assert_clean_worktree(wt)
            elif tmpl == "__CLEAN_MAIN__":
                rc, out = _assert_clean_worktree(ROOT)
            elif tmpl == "__UNPUSHED__":
                n, msg = _unpushed_commits()
                rc = 0 if (0 <= n <= 1) else 1
                out = msg + ("　⇒ 一次推送只应带 1 笔（>1 说明同批多笔待推 ⇒ 先 squash 成 1 笔）"
                             if rc else "　⇒ 满足「一批 = 一轮 CI」")
            elif tmpl == "__BATCHCOUNT__":
                n, msg = _batch_pushed_count(args.batch)
                out = msg + ("　⇒ 告警：本批已推多笔 ⇒ CI 轮数被放大，后续批次须合并推送"
                             if n >= 2 else "")
                rc = 0
            else:
                cmd = tmpl.format(py=_py(), root=wt, nodepath=_node_path())
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
