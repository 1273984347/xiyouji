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

# 单脚本执行超时（秒）；W536 起沿用 300，改此值即全局生效
SCRIPT_TIMEOUT_SECONDS = 300


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
            timeout=SCRIPT_TIMEOUT_SECONDS,
        )
        ok = r.returncode == 0
        tail = (r.stdout + r.stderr).strip().split("\n")[-1] if (r.stdout or r.stderr) else ""
        return ok, tail
    except subprocess.TimeoutExpired:
        return False, f"[TIMEOUT >{SCRIPT_TIMEOUT_SECONDS}s]"
    except Exception as e:
        return False, f"[EXC] {e}"


def _parse_category_filter(raw: str) -> set[str]:
    """把 `--only`/`--skip` 的逗号分隔字符串解析为归一化类别集合。

    大小写归一化为大写；空串与空白片段忽略。原实现未过滤空串，
    但空串不会命中任何类别，结果等价。
    """
    return {s.strip().upper() for s in raw.split(",") if s.strip()}


def _filter_scripts(
    scripts: list[tuple[str, Path]],
    only: str,
    skip: str,
) -> list[tuple[str, Path]]:
    """按 --only / --skip 过滤脚本列表。"""
    if only:
        only_set = _parse_category_filter(only)
        scripts = [(c, p) for c, p in scripts if c.upper() in only_set]
    if skip:
        skip_set = _parse_category_filter(skip)
        scripts = [(c, p) for c, p in scripts if c.upper() not in skip_set]
    return scripts


def _print_dry_run(scripts: list[tuple[str, Path]]) -> None:
    """dry-run 分支：仅打印将执行的脚本清单。"""
    for c, p in scripts:
        print(f"  [{c}] {p.relative_to(ROOT)}")


def _execute_scripts(
    scripts: list[tuple[str, Path]],
) -> tuple[int, list[tuple[str, Path, str]]]:
    """顺序执行全部脚本。

    返回：
        (PASS 数, 失败列表)，失败列表元素为 (类别名, 相对路径, 输出尾部)。
    """
    total = len(scripts)
    pass_count = 0
    failures: list[tuple[str, Path, str]] = []

    for i, (cat, path) in enumerate(scripts, 1):
        rel = path.relative_to(ROOT)
        print(f"[{i:02d}/{total}] [{cat}] {rel} ...", end=" ", flush=True)
        ok, tail = run_one(path)
        if ok:
            print("[OK]")
            pass_count += 1
        else:
            print(f"[FAIL] {tail}")
            failures.append((cat, rel, tail))

    return pass_count, failures


def _print_summary(
    pass_count: int,
    failures: list[tuple[str, Path, str]],
    total: int,
) -> None:
    """打印 PASS/FAIL 汇总行与失败明细。"""
    print("\n" + "=" * 60)
    print(f"汇总：{pass_count} PASS / {len(failures)} FAIL / {total} 总计")
    if failures:
        print("\n失败列表：")
        for cat, rel, tail in failures:
            print(f"  [{cat}] {rel}  ->  {tail}")


def main() -> int:
    parser = argparse.ArgumentParser(description="批量运行 A-AH 34 类分析脚本")
    parser.add_argument("--dry-run", action="store_true", help="仅列出会跑的脚本")
    parser.add_argument("--only", default="", help="仅跑指定类别（逗号分隔，如 A,B,F）")
    parser.add_argument("--skip", default="", help="跳过指定类别（逗号分隔）")
    args = parser.parse_args()

    scripts = _filter_scripts(discover_scripts(), args.only, args.skip)

    print(f"==> 发现 {len(scripts)} 个分析脚本")
    if args.dry_run:
        _print_dry_run(scripts)
        return 0

    pass_count, failures = _execute_scripts(scripts)
    _print_summary(pass_count, failures, len(scripts))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
