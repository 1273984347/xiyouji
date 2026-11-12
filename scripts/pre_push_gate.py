#!/usr/bin/env python3
"""pre_push_gate.py —— 推送前一命令真全量（W1215）。

## 病根（W1214 两轮 CI 浪费实证）

「本地全量门禁绿」的『全量』此前是**散文语义**——verify_delivery（71 槽）不含
pytest（体积窗 C7 / HANDOVER 概要块等判据只在 pytest 面）、不含 agent-guardrails
（复杂度/结构档只在 safe_commit 钩子里跑）⇒ **三绿不同源**：交接者各自只跑自己
那一面就宣布「全绿」，push 后 CI 两连红（guardrails 复杂度 18>15 + pytest C7 概要
块 7>6），每轮 ≈25 job × 15-25 分钟，而两个红灯**本地各 0.5 s 就能测出**。

## 本脚本把「真全量」变成可执行语义：四步一命令，任一步红即非 0 退出

  1. guardrails  pwsh scripts/guardrails/check_changed.ps1（ruff 风格/结构档 + api_diff）
  2. verify      python scripts/verify_delivery.py --scope full（71 槽交付门禁·CI Delivery Gate 同轨）
  3. pytest      python -m pytest tests -q（体积窗 C7 / HANDOVER 概要块等判据载体）
  4. ci_sim      python scripts/ci_sim.py（CI 侧预演·clean worktree 门禁；
                 **工作树有未提交改动时自动 SKIP**——预演目标 HEAD 不含未提交批，
                 跑了只会给旧提交的假安心 ⇒ 提交后、推送前这一步才有意义；
                 脏度在**四步开始前**快照——步骤本身会重写跟踪态生成物）

## 用法

    python scripts/pre_push_gate.py                 # 全四步（提交前/推送前判据）
    python scripts/pre_push_gate.py --skip-pytest   # 迭代期快跑（汇总行明确标注「非推送判据」）
    python scripts/pre_push_gate.py --steps         # 只打印步骤序

## 退出码

    0 = 所选步全绿（--skip-* 或 ci_sim 自跳过时汇总行标「非推送判据」）
    1 = 有步红
    2 = 基础设施缺失（fail-closed：判据脚本本体不在/不可执行 ⇒ 宁可中止不放行）
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STEP_ORDER = ("guardrails", "verify", "pytest", "ci_sim")
STEP_DESC = {
    "guardrails": "agent-guardrails（ruff 风格/结构档 + api_diff·铁律 20）",
    "verify": "verify_delivery --scope full（71 槽交付门禁·Delivery Gate 同轨）",
    "pytest": "pytest tests -q（体积窗 C7/HANDOVER 概要块等判据载体）",
    "ci_sim": "ci_sim（CI 侧预演·clean worktree·工作树未提交时 SKIP）",
}
REQUIRED_FILES = {
    "verify": os.path.join("scripts", "verify_delivery.py"),
    "pytest": None,  # 解释器模块形态·无仓内文件
    "ci_sim": os.path.join("scripts", "ci_sim.py"),
}
TAIL_PASS = 12   # PASS 时每步回显的输出尾行数
TAIL_FAIL = 60   # FAIL 时回显的尾行数（排障面）


def run(args):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def select_steps(skip):
    """按 --skip-* 过滤步骤·顺序恒为 STEP_ORDER（纯函数·供单测断言）。"""
    return [s for s in STEP_ORDER if not skip.get(s)]


def _ci_sim_should_run(tree_dirty):
    """ci_sim 步预检（纯函数）：工作树未提交 ⇒ SKIP（HEAD 不含未提交批·跑了是旧提交假安心）。"""
    if tree_dirty:
        return False, "工作树有未提交改动——预演目标 HEAD 不含本批，提交后重跑才有意义"
    return True, ""


def plan_run(skip, tree_dirty):
    """运行计划（纯函数·供单测）：返回 (steps, partial, ci_sim_skip_note)。

    判据降级口径：命令行 --skip-* **或 ci_sim 因工作树未提交自跳过** ⇒ 本次不是推送判据
    （自跳过与「本批无 .py 改动致 guardrails SKIP」不同：后者是无可检项，不降低覆盖）。
    tree_dirty 须由调用方在**任何步骤开始前**快照——步骤本身会重写跟踪态生成物
    （W1215 审查实证：全量 pytest 触发 w1167_nav_inject --dry-run 重写 _w1167_nav_plan.json）。
    """
    steps = select_steps(skip)
    partial = bool(skip.get("pytest") or skip.get("ci_sim"))
    note = ""
    if "ci_sim" in steps:
        ok, why = _ci_sim_should_run(tree_dirty)
        if not ok:
            partial = True
            note = why
    return steps, partial, note


def aggregate(results, partial):
    """汇总（纯函数·供单测）：results = [(name, status, seconds, note)]。

    status ∈ PASS / FAIL / SKIP。返回 (exit_code, 汇总行, 逐步行列表)。
    exit：任一 FAIL ⇒ 1；否则 0（SKIP 不算红·但 partial 模式汇总行标注「非推送判据」）。
    """
    lines = []
    fail = 0
    for name, status, secs, note in results:
        line = "%-6s %-10s %8.1fs" % (status, name, secs)
        if note:
            line += "  " + note
        lines.append(line)
        if status == "FAIL":
            fail += 1
    tag = " · ".join("%s %s" % (n, s) for n, s, _t, _n in results)
    total = sum(t for _n, _s, t, _n2 in results)
    verdict = "---- pre_push_gate：%d/%d 步绿·耗时 %.0fs%s----" % (
        sum(1 for _n, s, _t, _n2 in results if s == "PASS"), len(results), total,
        "（部分模式·非推送判据）" if partial else "（真全量·推送判据）")
    return (1 if fail else 0), "%s ｜ %s" % (verdict, tag), lines


def _changed_py():
    """本批 .py 改动清单（复用 batch_closeout 三态并集·引用不复制）。"""
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import batch_closeout  # 依赖缺失 ImportError 自然抛出（铁律 23·不吞不包）

    return batch_closeout._changed_py_files()


def run_guardrails(py_changed):
    """guardrails 步：有 .py 改动才跑；无则 SKIP（零成本语义·与铁律 20 对齐）。"""
    t0 = time.time()
    if not py_changed:
        return ("guardrails", "SKIP", time.time() - t0, "本批无 .py 改动")
    ps1 = os.path.join(ROOT, "scripts", "guardrails", "check_changed.ps1")
    if not os.path.isfile(ps1):
        return ("guardrails", "FAIL", time.time() - t0, "check_changed.ps1 缺失（fail-closed）")
    rc, out = run(["pwsh", "-File", ps1])
    tail = [ln for ln in out.splitlines() if ln.strip()][-TAIL_FAIL if rc else -TAIL_PASS:]
    print("[guardrails] " + "\n[guardrails] ".join(tail) if tail else "[guardrails] (无输出)")
    if rc != 0:
        return ("guardrails", "FAIL", time.time() - t0, "exit=%d" % rc)
    return ("guardrails", "PASS", time.time() - t0, "%d 件 .py" % len(py_changed))


def run_verify():
    t0 = time.time()
    rc, out = run([sys.executable, "scripts/verify_delivery.py", "--scope", "full"])
    tail = [ln for ln in out.splitlines() if ln.strip()][-TAIL_FAIL if rc else -TAIL_PASS:]
    print("[verify] " + "\n[verify] ".join(tail) if tail else "[verify] (无输出)")
    return ("verify", "PASS" if rc == 0 else "FAIL", time.time() - t0,
            "" if rc == 0 else "exit=%d" % rc)


def run_pytest():
    t0 = time.time()
    rc, out = run([sys.executable, "-m", "pytest", "tests", "-q"])
    tail = [ln for ln in out.splitlines() if ln.strip()][-TAIL_FAIL if rc else -TAIL_PASS:]
    print("[pytest] " + "\n[pytest] ".join(tail) if tail else "[pytest] (无输出)")
    return ("pytest", "PASS" if rc == 0 else "FAIL", time.time() - t0,
            "" if rc == 0 else "exit=%d" % rc)


def run_ci_sim():
    t0 = time.time()
    rc, out = run([sys.executable, "scripts/ci_sim.py"])
    tail = [ln for ln in out.splitlines() if ln.strip()][-TAIL_FAIL if rc else -TAIL_PASS:]
    print("[ci_sim] " + "\n[ci_sim] ".join(tail) if tail else "[ci_sim] (无输出)")
    return ("ci_sim", "PASS" if rc == 0 else "FAIL", time.time() - t0,
            "" if rc == 0 else "exit=%d" % rc)


def _infra_missing(steps, root=None):
    """基础设施反查（fail-closed）：判据脚本本体不在 ⇒ 宁可退出 2 也不假绿。root 可注入供单测。"""
    root = root or ROOT
    missing = []
    for s in steps:
        req = REQUIRED_FILES.get(s)
        if req and not os.path.isfile(os.path.join(root, req)):
            missing.append("%s（%s 不存在）" % (s, req))
    if "guardrails" in steps and not os.path.isfile(
            os.path.join(root, "scripts", "guardrails", "check_changed.ps1")):
        missing.append("guardrails（scripts/guardrails/check_changed.ps1 不存在）")
    return missing


def main(argv=None):
    ap = argparse.ArgumentParser(description="推送前一命令真全量（W1215）")
    ap.add_argument("--skip-pytest", action="store_true", help="跳过 pytest（迭代期·非推送判据）")
    ap.add_argument("--skip-ci-sim", action="store_true", help="跳过 ci_sim")
    ap.add_argument("--steps", action="store_true", help="只打印步骤序")
    a = ap.parse_args(argv)
    if a.steps:
        for s in STEP_ORDER:
            print("%-10s %s" % (s, STEP_DESC[s]))
        return 0
    skip = {"pytest": a.skip_pytest, "ci_sim": a.skip_ci_sim}
    # 脏度在四步开始前快照：pytest 会重写跟踪态生成物，步骤后再取会误判「提交后推送前」为脏
    tree_dirty = _tree_dirty() if not skip["ci_sim"] else False
    steps, partial, ci_sim_skip = plan_run(skip, tree_dirty)
    missing = _infra_missing(steps)
    if missing:
        print("FAIL  基础设施缺失（fail-closed）：%s" % "；".join(missing))
        return 2
    py_changed = _changed_py() if "guardrails" in steps else []
    results = []
    for s in steps:
        if s == "guardrails":
            results.append(run_guardrails(py_changed))
        elif s == "verify":
            results.append(run_verify())
        elif s == "pytest":
            results.append(run_pytest())
        elif s == "ci_sim":
            if ci_sim_skip:
                results.append(("ci_sim", "SKIP", 0.0, ci_sim_skip))
            else:
                results.append(run_ci_sim())
    code, verdict, lines = aggregate(results, partial)
    for ln in lines:
        print("  " + ln)
    print(verdict)
    return code


def _tree_dirty():
    rc, out = run(["git", "status", "--porcelain"])
    if rc != 0:
        # 查询失败按保守语义：视为 dirty（宁可 SKIP 也不假跑旧 HEAD）
        return True
    return bool(out.strip())


if __name__ == "__main__":
    sys.exit(main())
