"""once_call.py — 报告「只被调用一次」的自定义函数/方法。

用途：自检「这个新增辅助函数是不是只为一个调用点服务」。纯 AST 静态统计，
按名字匹配调用点（`foo()` 与 `obj.foo()` 都算），调用统计范围恒为整个仓库，
定义范围由命令行参数指定。

用法：
    python scripts/guardrails/once_call.py            # 默认扫 scripts/ tests/ mcp-server/
    python scripts/guardrails/once_call.py a.py b.py   # 只看这些文件里的定义
    python scripts/guardrails/once_call.py --max-calls 1
    python scripts/guardrails/once_call.py --json

输出：文件:行号 函数名 调用次数

退出码：默认恒 0（这是启发式报告，不当作门禁）；加 --fail-on-findings 时有发现即 1。

已知局限（README「已知限制」同步登记）：
  - 按名字匹配，不做作用域/类型解析：同名函数、动态派发（getattr/回调/装饰器注册）会低估；
  - 带装饰器的定义默认跳过（注解注入框架代调，静态统计必然失真）；
  - 递归调用不算「被别处调用」，但同一函数名在别处再定义时仍会计入；
  - 测试文件里的调用会算数，别把「只在测试里调一次」当生产信号。
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
import warnings
from dataclasses import dataclass, field
from pathlib import Path

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
# 静态统计必然失真的装饰器：由框架/注解机制代调，不按普通函数计。
SKIP_DECORATORS = {"property", "cached_property", "fixture", "route", "get", "post", "put", "delete", "patch", "task"}


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


def default_targets(root: Path) -> list[str]:
    return [str(root / d) for d in ("scripts", "tests", "mcp-server") if (root / d).is_dir()]


@dataclass
class Definition:
    path: Path
    line: int
    name: str
    qualified: str


@dataclass
class CallIndex:
    sites: dict[str, list[tuple[Path, int, str]]] = field(default_factory=dict)

    def add(self, name: str, path: Path, line: int, enclosing: str) -> None:
        self.sites.setdefault(name, []).append((path, line, enclosing))


class Collector(ast.NodeVisitor):
    def __init__(
        self, path: Path, index: CallIndex, defs: list[Definition] | None, collect_calls: bool = True
    ) -> None:
        self.path = path
        self.index = index
        self.defs = defs
        self.collect_calls = collect_calls
        self.scope: list[str] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def _record_def(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        if self.defs is None:
            return
        decorated = {_decorator_name(d) for d in node.decorator_list}
        if decorated & SKIP_DECORATORS:
            return
        if node.name.startswith("__") and node.name.endswith("__"):
            return
        if node.name.startswith("visit_"):
            # ast.NodeVisitor 协议方法由框架反射调用，静态统计必然为 0。
            return
        qualified = ".".join([*self.scope, node.name])
        self.defs.append(Definition(self.path, node.lineno, node.name, qualified))

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._record_def(node)
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._record_def(node)
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_Call(self, node: ast.Call) -> None:
        name = _call_name(node.func)
        if name and self.collect_calls:
            enclosing = self.scope[-1] if self.scope else ""
            self.index.add(name, self.path, node.lineno, enclosing)
        self.generic_visit(node)


def _decorator_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Call):
        return _decorator_name(node.func)
    return ""


def _call_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def parse_file(path: Path) -> ast.AST | None:
    try:
        with warnings.catch_warnings():
            # 仓库里存在历史脚本的无效转义序列，解析告警与本工具无关，一律静音。
            warnings.simplefilter("ignore")
            return ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError):
        return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="报告只被调用一次的函数/方法")
    ap.add_argument("paths", nargs="*", help="要统计定义的文件/目录（调用统计仍覆盖全仓）")
    ap.add_argument("--max-calls", type=int, default=1, help="调用点 <= N 视为可疑（默认 1）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--fail-on-findings", action="store_true", help="有发现时退出 1")
    args = ap.parse_args(argv)

    root = repo_root()
    if not args.paths:
        args.paths = default_targets(root)

    scan_files = iter_py_files(args.paths)
    if not scan_files:
        print("once_call: 没有可扫描的 .py 文件，跳过。")
        return 0

    # 调用索引恒扫全仓，否则「只在别处被调用一次」的判定必然失真。
    index = CallIndex()
    for f in iter_py_files([str(root)]):
        tree = parse_file(f)
        if tree is not None:
            Collector(f, index, None).visit(tree)

    defs: list[Definition] = []
    for f in scan_files:
        tree = parse_file(f)
        if tree is not None:
            # 第二遍只收定义，不再重复累计调用点（否则调用次数会被翻倍）。
            Collector(f, index, defs, collect_calls=False).visit(tree)

    rows = []
    for d in defs:
        calls = [c for c in index.sites.get(d.name, []) if not (c[0] == d.path and c[2] == d.name)]
        if len(calls) <= args.max_calls:
            rows.append((d, len(calls)))

    if args.json:
        print(
            json.dumps(
                [
                    {"file": _rel(d.path, root), "line": d.line, "function": d.qualified, "calls": n}
                    for d, n in sorted(rows, key=lambda r: (str(r[0].path), r[0].line))
                ],
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for d, n in sorted(rows, key=lambda r: (str(r[0].path), r[0].line)):
            print(f"{_rel(d.path, root)}:{d.line}  {d.qualified}  调用次数={n}")
        print(f"-- 扫描定义 {len(defs)} 个（{len(scan_files)} 个文件），其中调用点 <= {args.max_calls} 的 {len(rows)} 个")

    return 1 if (rows and args.fail_on_findings) else 0


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    sys.exit(main())
