"""api_diff.py — 对比 HEAD 与工作区的公开 API 变化（签名/默认值/返回注解/raise 异常）。

用途：回答自检第 3 条「这次 diff 有没有动签名、默认值、返回注解、异常语义」。
只看公开符号（模块级函数与类的公开方法，名字不以 `_` 开头）。

用法：
    python scripts/guardrails/api_diff.py                # 自动取 git 改动里的 .py
    python scripts/guardrails/api_diff.py a.py b.py
    python scripts/guardrails/api_diff.py --base HEAD~1
    python scripts/guardrails/api_diff.py --strict       # 有破坏性变化即退出 1

输出标记：
    + 新增公开函数（非破坏）
    - 删除公开函数（破坏）
    ~ 签名/默认值/返回注解/raise 集合变化（破坏）
退出码：默认 0（只报告）；--strict 且有破坏性变化 → 1；git/IO 异常 → 2。

已知局限（README 同步登记）：
    - 只比较 AST 可表达的信息，注解/默认值是文本级比较（引号、空白差异可能误报）；
    - 不追踪跨模块 re-export、`*args` 展开、动态赋值（`f.__defaults__`）等运行时形态；
    - 私有符号（`_` 开头）不纳入，符合「内部实现自由改」的约定。
"""

from __future__ import annotations

import argparse
import ast
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Signature:
    params: tuple[tuple[str, str, str], ...]  # (名字, 注解, 默认值文本)
    returns: str
    raises: frozenset[str]


def repo_root() -> Path:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, encoding="utf-8"
        )
        if out.returncode == 0 and out.stdout.strip():
            return Path(out.stdout.strip())
    except OSError:
        pass
    return Path(__file__).resolve().parents[2]


def git(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(cwd),
    )


def changed_py_files(root: Path, base: str) -> list[str]:
    diff = git("diff", "--name-only", base, "--", "*.py", cwd=root)
    untracked = git("ls-files", "--others", "--exclude-standard", "--", "*.py", cwd=root)
    names: list[str] = []
    for proc in (diff, untracked):
        if proc.returncode != 0:
            continue
        names.extend(line.strip() for line in proc.stdout.splitlines() if line.strip())
    return sorted(set(names))


def base_source(root: Path, base: str, rel: str) -> str | None:
    proc = git("show", f"{base}:{rel}", cwd=root)
    return proc.stdout if proc.returncode == 0 else None


def collect(tree: ast.AST) -> dict[str, Signature]:
    out: dict[str, Signature] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
            out[node.name] = signature_of(node)
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) and not sub.name.startswith("_"):
                    out[f"{node.name}.{sub.name}"] = signature_of(sub)
    return out


def signature_of(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> Signature:
    a = fn.args
    params: list[tuple[str, str, str]] = []
    pos = a.posonlyargs + a.args
    defaults = [None] * (len(pos) - len(a.defaults)) + [ast.unparse(d) for d in a.defaults]
    for arg, default in zip(pos, defaults, strict=True):
        params.append((arg.arg, ast.unparse(arg.annotation) if arg.annotation else "", default or ""))
    if a.vararg:
        params.append(("*" + a.vararg.arg, _ann(a.vararg.annotation), ""))
    for arg, default in zip(a.kwonlyargs, a.kw_defaults, strict=True):
        params.append((arg.arg, _ann(arg.annotation), ast.unparse(default) if default else ""))
    if a.kwarg:
        params.append(("**" + a.kwarg.arg, _ann(a.kwarg.annotation), ""))
    return Signature(
        params=tuple(params),
        returns=ast.unparse(fn.returns) if fn.returns else "",
        raises=frozenset(_raised(fn)),
    )


def _ann(node: ast.expr | None) -> str:
    return ast.unparse(node) if node is not None else ""


def _raised(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """收集函数体内 raise 的异常类型名；不进入嵌套函数（它们对外不可见）。"""

    found: list[str] = []

    def walk(node: ast.AST) -> None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)) and node is not fn:
            return
        if isinstance(node, ast.Raise):
            exc = node.exc
            if isinstance(exc, ast.Call):
                exc = exc.func
            if isinstance(exc, ast.Name):
                found.append(exc.id)
            elif isinstance(exc, ast.Attribute):
                found.append(ast.unparse(exc))
        for child in ast.iter_child_nodes(node):
            walk(child)

    walk(fn)
    return found


def diff_one(rel: str, base: dict[str, Signature], cur: dict[str, Signature]) -> tuple[list[str], list[str]]:
    lines: list[str] = []
    breaking: list[str] = []
    for name in sorted(cur.keys() - base.keys()):
        lines.append(f"+ 新增公开函数 {name}({', '.join(p[0] for p in cur[name].params)})")
    for name in sorted(base.keys() - cur.keys()):
        lines.append(f"- 删除公开函数 {name}")
        breaking.append(name)
    for name in sorted(base.keys() & cur.keys()):
        old, new = base[name], cur[name]
        if old.params != new.params:
            lines.append(f"~ {name}: 参数变化 {_fmt_params(old)} → {_fmt_params(new)}")
            # W1144 根修（铁律 15·判据缺陷修正）：尾部追加**带默认值**的参数 = 向后兼容
            # （旧调用 f(旧参) 仍合法·W1143 实证 self_test 加 edge=None 被误判破坏阻断
            # pre-commit）→ 不判破坏；删除/改名/必填新增/既有默认值变更仍判破坏。
            tail_added = (
                len(new.params) > len(old.params)
                and new.params[: len(old.params)] == old.params
                and all(p[2] for p in new.params[len(old.params):])
            )
            if not tail_added:
                breaking.append(name)
        if old.returns != new.returns:
            lines.append(f"~ {name}: 返回注解变化 -> {old.returns or 'None'} → -> {new.returns or 'None'}")
            breaking.append(name)
        added, removed = new.raises - old.raises, old.raises - new.raises
        if added:
            lines.append(f"~ {name}: 新增 raise {', '.join(sorted(added))}")
            breaking.append(name)
        if removed:
            lines.append(f"~ {name}: 移除 raise {', '.join(sorted(removed))}")
            breaking.append(name)
    return lines, breaking


def _fmt_params(sig: Signature) -> str:
    parts = [f"{n}{': ' + a if a else ''}{'=' + d if d else ''}" for n, a, d in sig.params]
    return "(" + ", ".join(parts) + ")"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="公开 API 变化对比")
    ap.add_argument("paths", nargs="*", help="仓内相对路径的 .py（默认取 git 改动）")
    ap.add_argument("--base", default="HEAD", help="对比基线（默认 HEAD）")
    ap.add_argument("--strict", action="store_true", help="有破坏性变化时退出 1")
    args = ap.parse_args(argv)

    root = repo_root()
    paths = args.paths or changed_py_files(root, args.base)
    if not paths:
        print("api_diff: 没有改动中的 .py 文件，跳过。")
        return 0

    breaking_any = False
    count = 0
    for rel in paths:
        cur_path = root / rel
        if not cur_path.is_file():
            print(f"{rel}: 工作区不存在（已删除？），跳过")
            continue
        base_src = base_source(root, args.base, rel)
        if base_src is None:
            print(f"{rel}: {args.base} 中不存在（新增文件），无 API 变化可对比")
            continue
        try:
            old_tree: ast.AST | None = ast.parse(base_src)
            new_tree: ast.AST | None = ast.parse(cur_path.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            print(f"{rel}: 解析失败（HEAD 或工作区存在语法错误），跳过")
            continue
        lines, breaking = diff_one(rel, collect(old_tree), collect(new_tree))
        for line in lines:
            print(f"{rel}: {line}")
            count += 1
        if breaking:
            breaking_any = True

    print(f"-- 对比 {len(paths)} 个文件（base={args.base}），变化 {count} 处，破坏性 {'有' if breaking_any else '无'}")
    if args.strict and breaking_any:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
