#!/usr/bin/env python3
"""check_untracked.py — 交付物 untracked 文件检测

用途：
    检测 docs/、site/data/、scripts/ 目录中是否有 git untracked 文件。
    E1 铁律 31 次复现中 23 次是"Created 未 git add"，本工具工程化防护。

    设计为 pre-commit hook：检测到 untracked 交付物文件时警告（不阻断 commit），
    因为可能有合理未跟踪文件（如临时脚本）。

使用方式：
    python scripts/check_untracked.py
    # 退出码：0（即使有 untracked 也返回 0，仅警告）/ 1（参数错误）

    # 作为 pre-commit hook：
    #   entry: python scripts/check_untracked.py
    #   pass_filenames: false
    #   always_run: true
"""
import subprocess
import sys

# 需要检测 untracked 的交付物目录（相对项目根）
DELIVERABLE_DIRS = [
    "docs",
    "site/data",
    "scripts",
]

# 排除的模式（这些文件 untracked 是合理的）
EXCLUDE_PATTERNS = [
    "__pycache__",
    ".pyc",
    "_temp_",
    "tmp_",
    ".tmp",
]


def get_untracked_files() -> list[str]:
    """获取 git untracked 文件列表。"""
    result = subprocess.run(
        ["git", "status", "--porcelain", "-u"],
        capture_output=True,
        text=True,
        check=True,
    )
    untracked = []
    for line in result.stdout.splitlines():
        if line.startswith("?? "):
            filepath = line[3:].strip()
            # 排除模式
            if any(p in filepath for p in EXCLUDE_PATTERNS):
                continue
            untracked.append(filepath)
    return untracked


def filter_deliverables(untracked: list[str]) -> dict[str, list[str]]:
    """按交付物目录分类 untracked 文件。"""
    result: dict[str, list[str]] = {d: [] for d in DELIVERABLE_DIRS}
    for filepath in untracked:
        for d in DELIVERABLE_DIRS:
            if filepath.startswith(d + "/") or filepath.startswith(d + "\\"):
                result[d].append(filepath)
                break
    return result


def main() -> int:
    untracked = get_untracked_files()
    if not untracked:
        return 0

    deliverables = filter_deliverables(untracked)
    total = sum(len(v) for v in deliverables.values())

    if total == 0:
        return 0

    print(f"\n⚠️  检测到 {total} 个 untracked 交付物文件（E1 铁律防护）：")
    for d, files in deliverables.items():
        if files:
            print(f"\n  [{d}/]")
            for f in files:
                print(f"    {f}")

    print("\n  这些文件可能是新建但未 git add 的交付物。")
    print("  如确认需要提交：git add <file>")
    print("  如确认不需要提交：忽略此警告或添加到 .gitignore")
    print("  （此警告不阻断 commit）\n")

    return 0  # 警告不阻断


if __name__ == "__main__":
    sys.exit(main())
