#!/usr/bin/env python3
"""
批量修复 SVG 负宽度/负半径 class-level pattern。
仅修改内联脚本中的以下三类表达式：
1. radius = Math.min(W, H) / 2 - N  →  Math.max(0, Math.min(W, H) / 2 - N)
2. .attr("width", <expr>)  →  .attr("width", Math.max(0, <expr>))（避开数字/字符串字面量、已保护表达式和 function 表达式）
3. const/let VAR = X.clientWidth || N  →  加最小宽度保护，避免移动视口下内部绘图区宽度为负

Usage:
    # from scripts/ directory, patch all site/data HTML + dashboard.html
    python fix_svg_negative_widths.py
    # with extra HTML files (relative to project root)
    python fix_svg_negative_widths.py --extra site/index.html
    # preview only, do not write
    python fix_svg_negative_widths.py --dry-run
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TARGETS = list((ROOT / "site" / "data").glob("*.html")) + [ROOT / "site" / "dashboard.html"]

RADIUS_RE = re.compile(
    r"(?<!Math\.max\(0,\s)"          # 避免重复包裹
    r"Math\.min\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*,\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)\s*/\s*2\s*-\s*(\d+)",
    re.MULTILINE,
)

ATTR_PREFIX = '.attr("width",'

# 匹配 const/let VAR = X.clientWidth || N;
# 通过 negative lookbehind 跳过已被 Math.max/Math.min 保护的表达式
CLIENTWIDTH_ASSIGN_RE = re.compile(
    r"(?<!Math\.max\()"
    r"(?<!Math\.min\()"
    r"\b(const|let)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"
    r"([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*(?:\(\))?)*)\.clientWidth\s*\|\|\s*(\d+)\s*;"
)

# 后续文本中是否已用 Math.max(VAR, ...) 或 Math.min(VAR, ...) 保护
ALREADY_PROTECTED_RE_TMPL = r"Math\.(?:max|min)\s*\([^)]*\b{}\b"

# 后续文本中是否出现 VAR - MARGIN.left - MARGIN.right
MARGIN_SUB_RE_TMPL = r"\b{}\s*-\s*([A-Za-z_][A-Za-z0-9_]*)\.left\s*-\s*\1\.right"


def skip_width_arg(arg: str) -> bool:
    arg = arg.strip()
    if not arg:
        return True
    # 数字/字符串字面量
    if arg[0] in "'\"`" or arg.isdigit() or (arg[0] == "-" and arg[1:].isdigit()):
        return True
    # 已保护
    if arg.startswith("Math.max(0,"):
        return True
    # function 表达式无法安全整体包裹
    if arg.startswith("function"):
        return True
    return False


def wrap_width_arg(arg: str) -> str:
    arg = arg.strip()
    if skip_width_arg(arg):
        return arg
    # 箭头函数：把 Math.max(0, ...) 加在函数体表达式上
    arrow_match = re.match(r"^((?:\([^)]*\)|[A-Za-z_][A-Za-z0-9_]*)\s*=>\s*)(.+)$", arg, re.DOTALL)
    if arrow_match:
        header, body = arrow_match.group(1), arrow_match.group(2).strip()
        if body.startswith("Math.max(0,"):
            return arg
        return f"{header}Math.max(0, {body})"
    return f"Math.max(0, {arg})"


def process_attr_widths(text: str) -> str:
    """解析 .attr("width", <value>) 调用并包裹 Math.max(0, ...)。"""
    out = []
    i = 0
    while True:
        idx = text.find(ATTR_PREFIX, i)
        if idx == -1:
            out.append(text[i:])
            break
        out.append(text[i:idx + len(ATTR_PREFIX)])
        # 此时已经处于 .attr( 的括号内部（depth=1），解析直到闭合该调用
        pos = idx + len(ATTR_PREFIX)
        depth = 1
        val_start = pos
        for j in range(pos, len(text)):
            ch = text[j]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    arg_content = text[val_start:j]
                    new_arg = wrap_width_arg(arg_content)
                    out.append(new_arg)
                    out.append(")")
                    i = j + 1
                    break
        else:
            # 未闭合，直接保留剩余
            out.append(text[pos:])
            break
    return "".join(out)


def process_radius(text: str) -> str:
    def repl(m):
        return f"Math.max(0, {m.group(0)})"
    return RADIUS_RE.sub(repl, text)


def margin_defined_before(text: str, pos: int, margin_var: str) -> bool:
    """检查 margin_var 是否在 pos 之前已定义。"""
    prefix = text[:pos]
    regex = re.compile(rf"\b(const|let|var)\s+{re.escape(margin_var)}\s*=\s*{{[^}}]*}}")
    return regex.search(prefix) is not None


def process_clientwidth(text: str) -> tuple[str, list[tuple[str, str, str]]]:
    """
    为 clientWidth fallback 赋值增加最小宽度保护。
    返回 (new_text, patched_locations)。
    """
    patched = []

    def repl(m):
        decl, var, obj, fallback = m.group(1), m.group(2), m.group(3), m.group(4)
        end = m.end()
        following = text[end:end + 800]

        # 若后续已用 Math.max(VAR, ...) / Math.min(VAR, ...) 保护，跳过
        if re.search(ALREADY_PROTECTED_RE_TMPL.format(re.escape(var)), following):
            return m.group(0)

        # 若后续出现 VAR - MARGIN.left - MARGIN.right，按 margin 总和保护
        margin_sub_match = re.search(MARGIN_SUB_RE_TMPL.format(re.escape(var)), following)
        if margin_sub_match:
            margin_var = margin_sub_match.group(1)
            # margin 必须先于当前赋值定义，否则引用未定义变量
            if margin_defined_before(text, m.start(), margin_var):
                new_expr = (
                    f"{decl} {var} = Math.max({obj}.clientWidth || {fallback}, "
                    f"{margin_var}.left + {margin_var}.right + 40);"
                )
                patched.append((var, obj, "margin-aware"))
                return new_expr

        # 默认最小宽度保护 200px，避免 viewBox / 半径计算拿到极小值
        new_expr = f"{decl} {var} = Math.max(200, {obj}.clientWidth || {fallback});"
        patched.append((var, obj, "default"))
        return new_expr

    new_text = CLIENTWIDTH_ASSIGN_RE.sub(repl, text)
    return new_text, patched


def main():
    parser = argparse.ArgumentParser(description="批量修复 SVG 负宽度/负半径 class-level pattern。")
    parser.add_argument("--extra", nargs="*", help="Additional HTML files to patch (relative to project root)")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, do not write changes")
    args = parser.parse_args()

    targets = list(DEFAULT_TARGETS)
    for rel in (args.extra or []):
        extra_path = ROOT / rel
        if extra_path.exists():
            targets.append(extra_path)
        else:
            print(f"Warning: extra file not found: {extra_path}")

    changed = 0
    for f in sorted(targets):
        text = f.read_text(encoding="utf-8")
        new_text = process_attr_widths(process_radius(text))
        new_text, patched = process_clientwidth(new_text)
        if new_text != text:
            changed += 1
            kinds = ", ".join(f"{v} ({kind})" for v, obj, kind in patched)
            print(f"patched {f.name}: {kinds}")
            if not args.dry_run:
                f.write_text(new_text, encoding="utf-8")
    if args.dry_run:
        print(f"\n[dry-run] Would change {changed} files (no writes performed).")
        sys.exit(1 if changed > 0 else 0)
    else:
        print(f"\nTotal files changed: {changed}")


if __name__ == "__main__":
    main()
