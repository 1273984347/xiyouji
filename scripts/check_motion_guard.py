#!/usr/bin/env python3
"""check_motion_guard.py — d3 动效守卫覆盖率判据（W1135·遗留① 根治 + 防复发）

背景：站内 reduced-motion 契约（DESIGN.md §5.3）要求用户开启「减少动态效果」时，
d3 图表的 .duration()/.delay() 必须归零。W1105 批把「裸数字实参」清零（BARE=0），
但**表达式实参**（如 .delay(1500 + i * 200)、.delay((d,i) => 200 + i*120)）未套守卫
⇒ reduced-motion 用户仍会经历动效与延迟。W1135 批根治并把口径固化为机器判据。

调用点三档：
  GUARDED 实参含守卫变量（MOYUN_RM / REDUCE_MOTION 任一）⇒ 合规
  BARE    实参是纯数字 ⇒ 未套守卫 ⇒ FAIL
  EXPR    实参含运算符/箭头函数/调用 ⇒ 未套守卫 ⇒ FAIL
  EMPTY   实参为空（异常形态）⇒ FAIL
页级：含调用点的页（d3 页）必须声明守卫变量。

两条既有纪律的落实：
  E-97 覆盖率类判据必须枚举**全部**合法守卫命名（站内并存 MOYUN_RM 与
        REDUCE_MOTION 两种，只认一种会漏判真实缺陷）。
  E-101 按实参形态分类的统计必须用**括号平衡扫描**而非 [^()]* 形态正则
        （窄口径正则会漏掉含嵌套括号的实参）。

用法：py -3 scripts/check_motion_guard.py [--report] [--list] [--json]
退出码：0 = 通过；1 = 有 FAIL；2 = 基础设施缺失（fail-closed）
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

# 标签名/属性名大小写不敏感（HTML 语义）⇒ 过滤型正则必须大小写不敏感：
# 原写法 `<script` 只匹配小写 ⇒ 大写 `<SCRIPT>` 的内联块被整块漏扫（动效守卫漏判）；
# 同理 `src=` 只匹配小写 ⇒ 大写 `SRC=` 的外链脚本会被误当内联块。
# 字符类写法（而非 re.IGNORECASE）⇒ 静态分析（CodeQL bad-html-filtering-regexp）可判定为已大小写不敏感。
SCRIPT_RE = re.compile(
    r"<[sS][cC][rR][iI][pP][tT](?![^>]*\b[sS][rR][cC]=)[^>]*>"
    r"(.*?)</[sS][cC][rR][iI][pP][tT]>",
    re.DOTALL,
)
CALL_RE = re.compile(r"\.(duration|delay)\s*\(")
GUARD_RE = re.compile(r"\b(MOYUN_RM|REDUCE_MOTION)\b")
DECL_RE = re.compile(r"\b(?:var|let|const)\s+(MOYUN_RM|REDUCE_MOTION)\b")
BARE_RE = re.compile(r"^\d+(?:\.\d+)?$")


def iter_html(base):
    for dirpath, _dirs, files in os.walk(base):
        for name in sorted(files):
            if name.endswith(".html"):
                full = os.path.join(dirpath, name)
                yield os.path.relpath(full, base).replace(os.sep, "/"), full


def extract_arg(text, open_idx):
    """open_idx 指向 '(' → (实参文本, 是否闭合)。括号平衡 + 跳过字符串与注释。"""
    depth = 0
    i = open_idx
    n = len(text)
    quote = None
    while i < n:
        ch = text[i]
        if quote is not None:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "\"'":
            quote = ch
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[open_idx + 1:i], True
        i += 1
    return text[open_idx + 1:], False


def classify(arg):
    a = arg.strip()
    if not a:
        return "EMPTY"
    if GUARD_RE.search(a):
        return "GUARDED"
    if BARE_RE.match(a):
        return "BARE"
    return "EXPR"


def scan_file(path, rel):
    html = open(path, encoding="utf-8", errors="replace").read()
    calls = []
    has_guard = False
    for m in SCRIPT_RE.finditer(html):
        body = m.group(1)
        line_off = html.count("\n", 0, m.start(1)) + 1
        if DECL_RE.search(body):
            has_guard = True
        for cm in CALL_RE.finditer(body):
            arg, closed = extract_arg(body, cm.end() - 1)
            if not closed:
                continue
            calls.append({
                "file": rel,
                "line": line_off + body.count("\n", 0, cm.start()),
                "fn": cm.group(1),
                "arg": arg.strip(),
                "kind": classify(arg),
            })
    return {"file": rel, "calls": calls, "has_guard": has_guard}


def summarize(pages):
    d3_pages = [p for p in pages if p["calls"]]
    calls = [c for p in pages for c in p["calls"]]
    kinds = {"GUARDED": 0, "EXPR": 0, "BARE": 0, "EMPTY": 0}
    for c in calls:
        kinds[c["kind"]] += 1
    bad_calls = [c for c in calls if c["kind"] != "GUARDED"]
    return {
        "html_pages": len(pages),
        "d3_pages": len(d3_pages),
        "guard_decl_pages": sum(1 for p in d3_pages if p["has_guard"]),
        "no_guard_pages": [p["file"] for p in d3_pages if not p["has_guard"]],
        "calls_total": len(calls),
        "kinds": kinds,
        "bad_calls": bad_calls,
        "bad_expr_pages": sorted({c["file"] for c in bad_calls}),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="d3 动效守卫覆盖率判据（W1135）")
    ap.add_argument("--report", action="store_true", help="只报不判红")
    ap.add_argument("--list", action="store_true", help="列出未合规调用点明细")
    ap.add_argument("--json", action="store_true", help="输出 JSON 汇总")
    args = ap.parse_args()

    if not os.path.isdir(SITE):
        print("FAIL 基础设施缺失：site/ 目录不存在（fail-closed）")
        return 2

    pages = [scan_file(full, rel) for rel, full in iter_html(SITE)]
    s = summarize(pages)

    if args.json:
        print(json.dumps(s, ensure_ascii=False, indent=2))
        return 0

    print("---- 第 58 门禁 动效守卫覆盖：d3 页 %d（声明守卫 %d / 未声明 %d）· 调用点 %d（GUARDED %d / EXPR %d / BARE %d / EMPTY %d）· 违规调用点页 %d ----"
          % (s["d3_pages"], s["guard_decl_pages"], len(s["no_guard_pages"]),
             s["calls_total"], s["kinds"]["GUARDED"], s["kinds"]["EXPR"],
             s["kinds"]["BARE"], s["kinds"]["EMPTY"], len(s["bad_expr_pages"])))

    if args.list:
        for c in s["bad_calls"]:
            print("  %-7s %s:%d .%s(%s)" % (c["kind"], c["file"], c["line"], c["fn"], c["arg"]))

    problems = []
    for f in s["no_guard_pages"]:
        problems.append("d3 页无守卫声明：%s" % f)
    for c in s["bad_calls"]:
        problems.append("未套守卫的 %s：%s:%d .%s(%s)" % (c["kind"], c["file"], c["line"], c["fn"], c["arg"]))
    if problems and not args.report:
        for p in problems[:40]:
            print("FAIL  " + p)
        if len(problems) > 40:
            print("FAIL  …… 另有 %d 项（用 --list 看全量）" % (len(problems) - 40))
        print("---- 第 58 门禁 动效守卫覆盖：%d FAIL ----" % len(problems))
        return 1
    print("---- 第 58 门禁 动效守卫覆盖：0 FAIL ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
