"""check_nested_comprehension.py — 报告「推导式里再套推导式」的写法。

为什么自建：ruff 0.16.9 没有对应规则（`ruff rule --all` 实测，comprehension 相关只有
C4xx 的「多余推导 / 用生成器」类，无嵌套深度项）；pylint 不装（见 scripts/guardrails/ruff-structure.toml 头注）。

用法：
    python scripts/guardrails/check_nested_comprehension.py <文件或目录>...
    python ... --max-depth 1        # 允许嵌套一层（默认 0：完全不允许）

判定：depth = 该推导式外面还套了几层推导式；depth > max-depth 即报告。
输出：文件:行号  嵌套深度=<depth>  <种类>
退出码：有违规 1；无违规 0；没有可扫描文件 0（提示跳过）。
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

COMP_TYPES = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
SKIP_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    "archive",
    "tmpe",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    "dist",
}
KIND = {ast.ListComp: "list", ast.SetComp: "set", ast.DictComp: "dict", ast.GeneratorExp: "generator"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def iter_py_files(targets: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in targets:
        p = Path(raw)
        if p.is_file() and p.suffix == ".py":
            files.append(p.resolve())
        elif p.is_dir():
            for f in p.rglob("*.py"):
                if not any(part in SKIP_DIRS for part in f.parts):
                    files.append(f.resolve())
    return sorted(set(files))


def scan(tree: ast.AST) -> list[tuple[int, int, str]]:
    hits: list[tuple[int, int, str]] = []

    def walk(node: ast.AST, depth: int) -> None:
        if isinstance(node, COMP_TYPES):
            if depth > 0:
                hits.append((node.lineno, depth, KIND[type(node)]))
            for child in ast.iter_child_nodes(node):
                walk(child, depth + 1)
            return
        for child in ast.iter_child_nodes(node):
            walk(child, depth)

    walk(tree, 0)
    return hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="嵌套推导式检查")
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--max-depth", type=int, default=0, help="允许的嵌套层数（默认 0）")
    args = ap.parse_args(argv)

    root = repo_root()
    targets = args.paths or [str(root / "scripts")]
    files = iter_py_files(targets)
    if not files:
        print("check_nested_comprehension: 没有可扫描的 .py 文件，跳过。")
        return 0

    total = 0
    failed = False
    for f in files:
        try:
            tree = ast.parse(f.read_text(encoding="utf-8", errors="replace"), filename=str(f))
        except SyntaxError as exc:
            print(f"{_rel(f, root)}:{exc.lineno}  语法错误，无法解析：{exc.msg}")
            failed = True
            continue
        for line, depth, kind in sorted(scan(tree)):
            if depth <= args.max_depth:
                continue
            print(f"{_rel(f, root)}:{line}  嵌套深度={depth}  {kind}-comprehension")
            total += 1
            failed = True

    print(f"-- 扫描 {len(files)} 个文件，嵌套深度 > {args.max_depth} 的 {total} 处")
    return 1 if failed else 0


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    sys.exit(main())
