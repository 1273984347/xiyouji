#!/usr/bin/env python3
"""duipai.py — 门禁/检查器重构的受控对拍模板（W775 方法论 · W778 固化）。

用法（快照 → 落地 → 对拍）：

  # 1) 旧版状态采集（在旧版代码在位时执行）
  python duipai.py snapshot --tag old_selftest -- node scripts/check_x.js --self-test
  python duipai.py snapshot --tag old_gate3   -- node scripts/check_x.js --gate --pages a,b,c

  # 2) 落地新版代码后，同命令再采
  python duipai.py snapshot --tag new_selftest -- node scripts/check_x.js --self-test

  # 3) 对拍（默认 stdout 逐行；--sort 做多重集比较以容忍并发输出序）
  python duipai.py compare old_selftest new_selftest
  python duipai.py compare old_gate3 new_gate3 --sort

判定规则（与 docs/10-方法论沉淀/批次交付流水线.md §八 一致）：
  · 计时/像素/时间戳 = 固有抖动 → 归一化后放行
  · 文案/字段/退出码 = 契约 → 零容忍
  · 覆盖集合变化必须追根因（修复型变化显式记录，不得回滚）

快照落点：本目录 snapshots/<tag>/{stdout.txt,stderr.txt,exit.txt,meta.json}
退出码：compare 0=一致 / 1=有差异 / 2=参数或快照缺失。
仅依赖标准库。
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP_ROOT = os.path.join(HERE, "snapshots")

# 归一化规则（顺序敏感：先具体后一般）
NORMALIZERS = [
    (re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?"), "<TS>"),
    (re.compile(r"done in \d+s"), "done in <T>s"),
    (re.compile(r"in \d+(?:\.\d+)?s \(0:00:\d+\)"), "in <T>s (<clock>)"),
    (re.compile(r"· \d+(?:\.\d+)?s ·"), "· <T>s ·"),
    (re.compile(r"\bms=\d+\b"), "ms=<T>"),
    (re.compile(r"\b\d+(?:\.\d+)?s\b"), "<T>s"),
    (re.compile(r"\b\d+(?:\.\d+)? seconds\b"), "<T> seconds"),
]


def normalize(text: str) -> str:
    for rx, repl in NORMALIZERS:
        text = rx.sub(repl, text)
    return text


def cmd_snapshot(args) -> int:
    if not args.command:
        print("FAIL snapshot 需要命令：snapshot --tag NAME -- <command...>", file=sys.stderr)
        return 2
    tag = args.tag
    out_dir = os.path.join(SNAP_ROOT, tag)
    os.makedirs(out_dir, exist_ok=True)
    t0 = datetime.now()
    proc = subprocess.run(args.command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    elapsed = (datetime.now() - t0).total_seconds()
    with open(os.path.join(out_dir, "stdout.txt"), "w", encoding="utf-8") as f:
        f.write(normalize(proc.stdout))
    with open(os.path.join(out_dir, "stderr.txt"), "w", encoding="utf-8") as f:
        f.write(normalize(proc.stderr))
    with open(os.path.join(out_dir, "exit.txt"), "w", encoding="utf-8") as f:
        f.write(str(proc.returncode))
    meta = {
        "tag": tag,
        "command": args.command,
        "exit": proc.returncode,
        "elapsed_s": round(elapsed, 1),
        "captured_at": t0.isoformat(timespec="seconds"),
    }
    with open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print(f"[snapshot] {tag} · exit={proc.returncode} · {elapsed:.1f}s → {out_dir}")
    return 0


def _read(tag: str, name: str) -> str:
    p = os.path.join(SNAP_ROOT, tag, name)
    if not os.path.exists(p):
        raise FileNotFoundError(f"快照缺失：{p}")
    return open(p, encoding="utf-8").read()


def cmd_compare(args) -> int:
    try:
        old_out, new_out = _read(args.old, "stdout.txt"), _read(args.new, "stdout.txt")
        old_err, new_err = _read(args.old, "stderr.txt"), _read(args.new, "stderr.txt")
        old_exit, new_exit = _read(args.old, "exit.txt").strip(), _read(args.new, "exit.txt").strip()
    except FileNotFoundError as e:
        print(f"FAIL {e}", file=sys.stderr)
        return 2

    def lines_of(s: str, sort: bool):
        ls = [ln.rstrip() for ln in s.splitlines() if ln.strip()]
        return sorted(ls) if sort else ls

    diffs = []
    # ① 退出码 = 契约
    if old_exit != new_exit:
        diffs.append(f"[exit] {old_exit} → {new_exit}")
    # ② stdout
    o, n = lines_of(old_out, args.sort), lines_of(new_out, args.sort)
    only_old = [x for x in o if x not in n]
    only_new = [x for x in n if x not in o]
    if only_old or only_new:
        diffs.append(f"[stdout] 仅旧版 {len(only_old)} 行 / 仅新版 {len(only_new)} 行")
        for x in only_old[:8]:
            diffs.append("  - " + x[:200])
        for x in only_new[:8]:
            diffs.append("  + " + x[:200])
    # ③ stderr（信息面，差异提醒但不单独判死）
    if old_err != new_err:
        diffs.append("[stderr] 内容有差异（人工判定是否契约面）")

    if not diffs:
        mode = "多重集" if args.sort else "逐行"
        print(f"PASS 对拍一致（{mode}比较·计时已归一）: {args.old} == {args.new}")
        return 0
    print(f"FAIL 对拍差异: {args.old} vs {args.new}")
    for d in diffs:
        print(d)
    return 1


def cmd_show(args) -> int:
    try:
        print(_read(args.tag, "stdout.txt"), end="")
        print(f"[exit] {_read(args.tag, 'exit.txt').strip()}")
    except FileNotFoundError as e:
        print(f"FAIL {e}", file=sys.stderr)
        return 2
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="门禁重构受控对拍（快照 + 归一化 diff）")
    sub = ap.add_subparsers(dest="mode", required=True)

    sp = sub.add_parser("snapshot", help="运行命令并保存归一化快照")
    sp.add_argument("--tag", required=True)
    sp.add_argument("command", nargs=argparse.REMAINDER, help="-- <命令...>")
    sp.set_defaults(func=cmd_snapshot)

    cp = sub.add_parser("compare", help="对拍两个快照")
    cp.add_argument("old")
    cp.add_argument("new")
    cp.add_argument("--sort", action="store_true", help="按行多重集比较（容忍并发输出序）")
    cp.set_defaults(func=cmd_compare)

    sh = sub.add_parser("show", help="查看快照 stdout")
    sh.add_argument("tag")
    sh.set_defaults(func=cmd_show)

    args = ap.parse_args()
    if args.mode == "snapshot" and args.command and args.command[0] == "--":
        args.command = args.command[1:]
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
