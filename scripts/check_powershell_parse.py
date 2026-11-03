#!/usr/bin/env python3
"""check_powershell_parse.py — PowerShell 脚本可解析性判据（W1110 新增第 55 槽）。

## 为什么需要它（病根）

仓内 `.ps1` 文件此前**零机器判据**：

- **语法面**：PowerShell 脚本写坏（括号不配、字符串未闭合、`param` 块位置错）时，
  `pwsh -File` 只在**运行时**报错 ⇒ 该脚本是 pre-commit 守门链的一环（`scripts/guardrails/`），
  写坏 ⇒ 守卫**静默失效**（人只在提交那一刻才发现「这次没拦住」）。
- **编码面（E-68 实证的静默死亡）**：`.ps1` 含非 ASCII 时**必须** UTF-8 with BOM ——
  Windows PowerShell 5.1 的 `-File` 加载器对**无 BOM** 文件回退 ANSI 代码页，
  在 CJK 系统上**解析器静默死亡**（中文变乱码 → 关键字不匹配 → 行为漂移或直接崩）。
  而 `pwsh`（PS 7）默认按 UTF-8 读 ⇒ **本机 pwsh 跑得通 ≠ 5.1 跑得通**，
  这条差异**没有任何门禁在管**。

## 判据（两条）

**C1 语法可解析性**：用 PowerShell 官方 AST 解析器（`System.Management.Automation.Language.Parser`
的 `ParseFile`）逐文件解析 ⇒ 语法错误即 FAIL。解析器缺失（无 `pwsh`/`powershell`）⇒
**fail-closed 退出码 2**（判据不可执行不得静默放过——与第 31/45 槽同族纪律）。

**C2 编码面**：含非 ASCII 字符的 `.ps1` 必须带 UTF-8 BOM（E-68 口径）⇒ 缺 BOM 即 FAIL。
纯 ASCII 的 `.ps1` 无 BOM 是**安全**的（ANSI 与 UTF-8 同解）⇒ 不判红。

## 豁免与边界

- 扫描域 = **tracked 的 `.ps1`**（`git ls-files`）——只管入库件，不管本地临时件。
- `archive/` 下的历史批脚本**豁免**（归档件只追加不改写，且历史 `.ps1` 不参与本仓守门链）。
- `tmpe/`（gitignored 本地临时区）天然不在 tracked 面内。

## 用法

    py -3 scripts/check_powershell_parse.py --gate     # 门禁态（供 verify_delivery 调用）
    py -3 scripts/check_powershell_parse.py --self-test  # 注入式负样本自测
    py -3 scripts/check_powershell_parse.py --report     # 只报告不判红

退出码：0 通过 · 1 有 FAIL · 2 判据不可执行（无 PowerShell 解析器）。
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- 扫描域口径 ----------------------------------------------------------
# 归档件豁免：归档目录下的历史批脚本不参与本仓守门链，且归档只追加不改写。
ARCHIVE_PREFIXES = ("archive/",)

# 语法解析用的一次性 PowerShell 片段（单行，避免 here-string 引号地狱）。
# - 用 `ParseFile` 官方 AST 解析器（不是 `Get-Command` 试运行——试运行会**执行**脚本，
#   对含副作用的脚本是危险动作；AST 解析只读不执行）。
# - 输出 JSON：`{errors: [{message, line, column}], count: n}`。
_PARSE_SNIPPET = (
    "$ErrorActionPreference='Stop';"
    "$out=@();"
    "$files=($env:PS_FILES -split ';') | Where-Object { $_ };"
    "foreach($f in $files){"
    "  $e=$null;$t=$null;"
    "  [void][System.Management.Automation.Language.Parser]::ParseFile($f,[ref]$t,[ref]$e);"
    "  foreach($x in $e){"
    "    $out+=[pscustomobject]@{file=$f;message=$x.Message;"
    "      line=$x.Extent.StartLineNumber;column=$x.Extent.StartColumnNumber}"
    "  }"
    "};"
    "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8;"
    # 空数组时 ConvertTo-Json 输出**空串**（非 "[]"）⇒ 手工拼数组字面量保证恒可解析
    "if($out.Count -eq 0){'[]'}else{'[' + (($out | ForEach-Object { $_ | ConvertTo-Json -Compress -Depth 4 }) -join ',') + ']'}"
)


def _git(*args):
    r = subprocess.run(
        ["git", "-c", "core.quotePath=false", "-C", ROOT] + list(args),
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
    )
    return r.stdout if r.returncode == 0 else ""


def tracked_ps1():
    """返回 tracked 的 .ps1 相对路径列表（排除 archive/ 豁免面）。"""
    out = []
    for line in _git("ls-files").splitlines():
        p = line.strip()
        if not p or not p.endswith(".ps1"):
            continue
        if p.startswith(ARCHIVE_PREFIXES):
            continue
        out.append(p.replace("\\", "/"))
    return sorted(out)


def read_bytes(rel):
    with open(os.path.join(ROOT, rel), "rb") as f:
        return f.read()


def has_utf8_bom(data):
    return data[:3] == b"\xef\xbb\xbf"


def contains_nonascii(data):
    """字节流是否含非 ASCII（≥0x80）——用于判「需要 BOM」的文件集合。"""
    return any(b > 0x7F for b in data)


def find_ps_parser():
    """定位可用的 PowerShell 解析宿主（pwsh 优先，powershell 回退）。"""
    for exe in ("pwsh", "powershell"):
        try:
            r = subprocess.run(
                [exe, "-NoProfile", "-NonInteractive", "-Command",
                 "$PSVersionTable.PSVersion.Major"],
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if r.returncode == 0 and r.stdout.strip().isdigit():
            return exe
    return None


def parse_ps1(files, exe):
    """用 PowerShell AST 解析器逐文件解析 ⇒ 返回 (错误列表, 不可执行原因)。

    错误列表元素：{"file", "message", "line", "column"}。
    """
    if not files:
        return [], None
    env = dict(os.environ)
    env["PS_FILES"] = ";".join(os.path.abspath(os.path.join(ROOT, f)) for f in files)
    try:
        r = subprocess.run(
            [exe, "-NoProfile", "-NonInteractive", "-Command", _PARSE_SNIPPET],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=300, env=env,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return [], "调用 %s 失败：%s" % (exe, exc)
    if r.returncode != 0:
        return [], "%s 解析宿主返回 rc=%d：%s" % (exe, r.returncode, (r.stderr or "").strip()[:200])
    raw = (r.stdout or "").strip()
    if not raw:
        return [], "%s 未输出解析结果（判据不可执行）" % exe
    try:
        data = json.loads(raw)
    except ValueError as exc:
        return [], "%s 输出不可解析为 JSON（%s）：%r" % (exe, exc, raw[:200])
    if isinstance(data, dict) and "items" in data:
        data = data["items"]
    if isinstance(data, dict):
        data = [data]
    if data is None:
        data = []
    errs = []
    for item in data or []:
        if not isinstance(item, dict):
            continue
        if not item.get("message"):
            continue
        errs.append({
            "file": os.path.relpath(str(item.get("file", "")), ROOT).replace("\\", "/"),
            "message": str(item.get("message", "")).strip(),
            "line": item.get("line"),
            "column": item.get("column"),
        })
    return errs, None


def evaluate(files, parse_errs, parse_unavailable=None):
    """纯函数判定 —— 返回 (issues, notes)。

    issues 元素为 FAIL 级；notes 为提示级（不判红）。
    """
    issues, notes = [], []
    # C1 语法
    if parse_unavailable:
        issues.append("C1: 判据不可执行——%s（无 PowerShell AST 解析器可调用）" % parse_unavailable)
    else:
        for e in parse_errs:
            issues.append("C1: %s:%s 列 %s 语法错误——%s"
                          % (e["file"], e.get("line"), e.get("column"), e["message"]))
    # C2 编码面（E-68）
    for rel in files:
        data = read_bytes(rel)
        if contains_nonascii(data) and not has_utf8_bom(data):
            issues.append(
                "C2: %s 含非 ASCII 但无 UTF-8 BOM——Windows PowerShell 5.1 的 -File 加载器"
                "会回退 ANSI 代码页⇒CJK 关键字解析静默死亡（E-68）·加 BOM 或改纯 ASCII" % rel)
    if not files:
        notes.append("扫描域内无 .ps1 文件（tracked 口径）")
    return issues, notes


def run_check(report_only=False):
    files = tracked_ps1()
    exe = find_ps_parser()
    parse_errs, unavailable = [], None
    if exe is None:
        unavailable = "未找到 pwsh / powershell"
    else:
        parse_errs, unavailable = parse_ps1(files, exe)
    issues, notes = evaluate(files, parse_errs, unavailable)
    for f in files:
        print("SCAN  %s（%s）" % (f, "含非 ASCII" if contains_nonascii(read_bytes(f)) else "纯 ASCII"))
    for n in notes:
        print("NOTE  " + n)
    for it in issues:
        print("FAIL  " + it)
    n_fail = len(issues)
    if report_only:
        print("---- PowerShell 解析（报告态）：%d 项 ----" % n_fail)
        return 0
    if unavailable and not parse_errs:
        # 判据不可执行 ⇒ fail-closed（退出码 2）
        print("---- PowerShell 解析：不可执行（fail-closed）----")
        return 2
    print("---- 第 55 门禁 PowerShell 解析：%d FAIL ----" % n_fail)
    return 1 if n_fail else 0


def _self_test():
    """注入式负样本自测：语法错误必红 + 缺 BOM 必红 + 干净态不误报。"""
    import tempfile
    fails = []
    tmp = tempfile.mkdtemp(prefix="w1110_ps_")
    good = os.path.join(tmp, "good.ps1")
    with open(good, "wb") as f:
        f.write(b"param([string]$Name)\nWrite-Output $Name\n")
    bad = os.path.join(tmp, "bad.ps1")
    with open(bad, "wb") as f:
        f.write(b"function Broken {\n  Write-Output 'x'\n")  # 缺右花括号
    cjk_nobom = os.path.join(tmp, "cjk_nobom.ps1")
    with open(cjk_nobom, "wb") as f:
        f.write("Write-Output '中文'\n".encode())  # 非 ASCII · 无 BOM
    cjk_bom = os.path.join(tmp, "cjk_bom.ps1")
    with open(cjk_bom, "wb") as f:
        f.write(b"\xef\xbb\xbf" + "Write-Output '中文'\n".encode())

    # evaluate 读盘 ⇒ 用真实临时文件替换（ROOT 临时指向 tmp）
    def _eval_with(rel_list, errs, unavail=None):
        global ROOT
        old = ROOT
        try:
            ROOT = tmp
            return evaluate(rel_list, errs, unavail)
        finally:
            ROOT = old

    i1, _ = _eval_with(["good.ps1"], [])
    if i1:
        fails.append("T1 干净态误报：%s" % i1)
    # T2 语法错误 ⇒ 必红
    i2, _ = _eval_with([], [{"file": "bad.ps1", "message": "缺少右花括号", "line": 3, "column": 1}])
    if not any("C1" in x for x in i2):
        fails.append("T2 语法错误必红未命中")
    # T3 非 ASCII 无 BOM ⇒ 必红
    i3, _ = _eval_with(["cjk_nobom.ps1"], [])
    if not any("C2" in x for x in i3):
        fails.append("T3 非 ASCII 缺 BOM 必红未命中")
    # T4 非 ASCII 有 BOM ⇒ 不红
    i4, _ = _eval_with(["cjk_bom.ps1"], [])
    if i4:
        fails.append("T4 有 BOM 不应误报：%s" % i4)
    # T5 纯 ASCII 无 BOM ⇒ 不红（ANSI 同解）
    i5, _ = _eval_with(["good.ps1"], [])
    if i5:
        fails.append("T5 纯 ASCII 无 BOM 不应误报：%s" % i5)
    # T6 解析器缺失 ⇒ fail-closed（issues 非空）
    i6, _ = _eval_with([], [], "未找到 pwsh / powershell")
    if not any("不可执行" in x for x in i6):
        fails.append("T6 解析器缺失须 fail-closed")
    # T7 真实 AST 解析：坏文件必被解析器抓到（依赖 pwsh 可用）
    exe = find_ps_parser()
    if exe:
        errs, unavail = parse_ps1(["bad.ps1"], exe)
        if unavail:
            fails.append("T7 解析宿主不可用：%s" % unavail)
        elif not errs:
            fails.append("T7 真实 AST 解析未抓到语法错误")
    else:
        print("SKIP  T7 真实 AST 解析（环境无 pwsh/powershell）")

    for f in fails:
        print("FAIL  " + f)
    total = 7
    print("---- 第 55 门禁 PowerShell 解析 self-test：%d/%d 通过 ----" % (total - len(fails), total))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description="PowerShell 脚本可解析性判据（第 55 槽）")
    ap.add_argument("--gate", action="store_true", help="门禁态（默认行为·保留显式 flag 兼容）")
    ap.add_argument("--report", action="store_true", help="只报告不判红")
    ap.add_argument("--self-test", action="store_true", help="注入式负样本自测")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    return run_check(report_only=args.report)


if __name__ == "__main__":
    sys.exit(main())
