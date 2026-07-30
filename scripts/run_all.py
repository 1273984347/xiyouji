#!/usr/bin/env python3
"""run_all.py — 批量运行 A-AH 34 类分析脚本

用途：
    遍历 scripts/ 下 A_*/ ~ AH_*/ 各目录的主分析脚本，按目录顺序批量执行，
    统一输出到 output/data/<脚本名>.json。失败不中断，最后汇总报告。

使用方式：
    # 跑全部
    python scripts/run_all.py
    # 仅列出会跑哪些脚本（dry-run）
    python scripts/run_all.py --dry-run
    # 仅跑指定类别（逗号分隔）
    python scripts/run_all.py --only A,B,F
    # 跳过指定类别
    python scripts/run_all.py --skip B

设计要点：
    - 自动发现：扫描 A_*/ ~ AH_*/ 子目录，找其中的 .py 主脚本（同目录脚本名约定）
    - 失败汇总：单脚本失败不阻断整体，最后输出 PASS/FAIL 汇总表
    - 默认输入由各脚本的 analyzer_base.run_analyzer 控制（默认 source/原文/分回/）
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def discover_scripts() -> list[tuple[str, Path]]:
    """扫描 A_*/ ~ AH_*/ 目录，返回 [(类别名, 脚本路径)]。

    每个目录取其中第一个 .py 文件作为主脚本（按文件名排序）。
    """
    result = []
    for d in sorted(SCRIPTS.iterdir()):
        if not d.is_dir() or not d.name[0].isalpha():
            continue
        # 仅取单字母前缀 + 下划线开头的目录（A_*/ B_*/ ... AH_*/）
        if "_" not in d.name:
            continue
        py_files = sorted(d.glob("*.py"))
        if py_files:
            # 类别名 = 目录名下划线前部分
            category = d.name.split("_")[0]
            result.append((category, py_files[0]))
    return result


def run_one(script_path: Path) -> tuple[bool, str]:
    """运行单个脚本，返回 (成功?, 输出尾部)。"""
    try:
        r = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(SCRIPTS),
            capture_output=True,
            text=True,
            timeout=300,
        )
        ok = r.returncode == 0
        tail = (r.stdout + r.stderr).strip().split("\n")[-1] if (r.stdout or r.stderr) else ""
        return ok, tail
    except subprocess.TimeoutExpired:
        return False, "[TIMEOUT >300s]"
    except Exception as e:
        return False, f"[EXC] {e}"


def main():
    parser = argparse.ArgumentParser(description="批量运行 A-AH 34 类分析脚本")
    parser.add_argument("--dry-run", action="store_true", help="仅列出会跑的脚本")
    parser.add_argument("--only", default="", help="仅跑指定类别（逗号分隔，如 A,B,F）")
    parser.add_argument("--skip", default="", help="跳过指定类别（逗号分隔）")
    args = parser.parse_args()

    scripts = discover_scripts()
    if args.only:
        only_set = {s.strip().upper() for s in args.only.split(",")}
        scripts = [(c, p) for c, p in scripts if c.upper() in only_set]
    if args.skip:
        skip_set = {s.strip().upper() for s in args.skip.split(",")}
        scripts = [(c, p) for c, p in scripts if c.upper() not in skip_set]

    print(f"==> 发现 {len(scripts)} 个分析脚本")
    if args.dry_run:
        for c, p in scripts:
            print(f"  [{c}] {p.relative_to(ROOT)}")
        return

    pass_count = 0
    fail_count = 0
    failures = []
    for i, (cat, path) in enumerate(scripts, 1):
        rel = path.relative_to(ROOT)
        print(f"[{i:02d}/{len(scripts)}] [{cat}] {rel} ...", end=" ", flush=True)
        ok, tail = run_one(path)
        if ok:
            print("[OK]")
            pass_count += 1
        else:
            print(f"[FAIL] {tail}")
            fail_count += 1
            failures.append((cat, rel, tail))

    print("\n" + "=" * 60)
    print(f"汇总：{pass_count} PASS / {fail_count} FAIL / {len(scripts)} 总计")
    if failures:
        print("\n失败列表：")
        for cat, rel, tail in failures:
            print(f"  [{cat}] {rel}  ->  {tail}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
