#!/usr/bin/env python3
"""check_css_var_selfref.py — CSS 变量**自引用**判据（W1110 新增·随第 54/55/56 槽同批建置）。

## 病根（W1108 批实证·本批施工⑤核档时抓出）

W1108 批把 chart-design 两页 INLINED 副本 `:root` 里的图表令牌定义改成
「`--chart-1: var(--chart-1);`」——**自引用**。浏览器对自引用变量的处理是：
该变量在当前元素上解析为**无效值**（invalid at computed-value time）⇒
`getComputedStyle(el).getPropertyValue('--chart-1')` 返回**空串**，
连带动使用它的 `--accent: var(--chart-1)` 一并失效 ⇒ 图表主题色回落为黑/继承色。

实测证据（Playwright 受控对照）：
- 改前：`--chart-1 = #C8463A` · `--accent = #C8463A` · 主题色 `rgb(200, 70, 58)` ✔
- 改后：`--chart-1 = ""` · `--accent = ""` · 主题色 `rgb(35, 32, 26)`（继承色）✘

**这类缺陷为何全绿**：CSP/结构/内联语法等门禁都不看 CSS 变量语义 ⇒ 页面照常渲染
（只是颜色不对）⇒ 全链无红灯。**机器判据缺位**是根因。

## 判据

扫描 `site/**/*.html` 的全部 `<style>` 块 + `site/tokens.css`：
任何 `--X: var(--X)` 形态（同名自引用）⇒ FAIL。

- **同名**才判红（`--a: var(--b)` 是正常引用）；
- 只看**定义位置**（属性值为 `var(...)` 且引用名 == 定义名）；
- `var(--X, fallback)` 带 fallback 的自引用**仍判红**（fallback 只在变量未定义时生效，
  而自引用场景下变量「已定义但无效」⇒ fallback 不生效 ⇒ 依然失效）。

## 用法

    py -3 scripts/check_css_var_selfref.py --gate     # 门禁态
    py -3 scripts/check_css_var_selfref.py --self-test  # 注入式负样本自测
    py -3 scripts/check_css_var_selfref.py --report     # 只报告不判红

退出码：0 通过 · 1 有 FAIL · 2 判据不可执行。
"""

from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

#: `<style>` 块提取（与 utils.gate_common.STYLE_BLOCK_RE 同口径）
STYLE_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
#: 自引用定义：`--name: var(--name)` / `var(--name, fallback)`
#: **W1110 收官笔修（盲审建议项 #3）**：原正则两处漏判 ——
#:   ① 嵌套自引用 `--a: var(--b, var(--a))` ⇒ 原式只匹配到外层 var( 的 `--b` ⇒ 不判；
#:   ② CSS 函数名**大小写不敏感** ⇒ `--a: VAR(--a)` 不判。
#: ⇒ 改用「先取定义值·再在值里找是否引用了同名变量」的判定（不看 var( 的嵌套层数·不看函数名大小写）。
RX_DECL = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]+)", re.S)
RX_VARREF = re.compile(r"var\s*\(\s*(--[A-Za-z0-9_-]+)", re.IGNORECASE)


def iter_site_files():
    """site 下所有 .html + **全部 .css**（排序·跨平台同序）。

    **W1110 收官笔修（盲审建议项 #2）**：原实现只收 `.html` + `tokens.css`
    ⇒ `site/system.css` 等**其他 .css 不在扫描域**（潜在盲区）。
    ⇒ 扩到「site 下全部 `.css`」。
    """
    out = []
    for root, dirs, files in os.walk(SITE):
        dirs.sort()
        for fn in sorted(files):
            if fn.endswith(".html") or fn.endswith(".css"):
                out.append(os.path.join(root, fn))
    return sorted(out)


def find_selfrefs(css_text):
    """返回 [(定义名, 引用名, 行号)]——同名自引用。行号为 css_text 内 1 基。

    判定口径（W1110 收官笔修）：**取每条声明的值**⇒ 若值里出现对**同名变量**的
    `var(` 引用 ⇒ 自引用（不看 var( 的嵌套层数·不看 var 函数名大小写）。
    ⇒ 覆盖 `--a: var(--a)` · `--a: var(--a, #fff)` · `--a: VAR(--a)` ·
    `--a: var(--b, var(--a))` 四形态。
    """
    out = []
    for m in RX_DECL.finditer(css_text):
        name = m.group(1)
        value = m.group(2)
        if not value.strip():
            continue
        for ref in RX_VARREF.findall(value):
            if ref == name:
                line = css_text[: m.start()].count("\n") + 1
                out.append((name, ref, line))
                break
    return out


def scan_text(text):
    """对一段 CSS 文本求自引用（逐 style 块 + 原文·行号相对整文件）。"""
    out = []
    # 逐 style 块（带文件内偏移 ⇒ 行号可回算到文件级）
    for sm in STYLE_RE.finditer(text):
        block = sm.group(1)
        base_line = text[: sm.start(1)].count("\n") + 1
        for name, ref, line in find_selfrefs(block):
            out.append((name, ref, base_line + line - 1))
    # 整文件再扫一遍（覆盖 .css 文件与 style 块外的裸 CSS）
    seen = set((n, ln) for n, _r, ln in out)
    for name, ref, line in find_selfrefs(text):
        if (name, line) not in seen:
            out.append((name, ref, line))
    return out


def evaluate(files_text):
    """纯函数判定 —— 返回 (issues, notes)。files_text: {rel_path: 文本}"""
    issues, notes = [], []
    for rel in sorted(files_text):
        text = files_text[rel]
        for name, ref, line in scan_text(text):
            issues.append(
                "%s:%d CSS 变量自引用 `--%s: var(--%s)` ⇒ 浏览器解析为无效值"
                "（computed-value time invalid）⇒ getComputedStyle 返回空串·连带引用它的变量一并失效"
                % (rel, line, name, ref))
    if not files_text:
        notes.append("扫描域为空（site/ 下无 .html 与 tokens.css）")
    return issues, notes


def run_check(report_only=False):
    files_text = {}
    for p in iter_site_files():
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                files_text[rel] = f.read()
        except OSError as exc:
            print("FAIL  读文件失败 %s：%s" % (rel, exc))
            return 2
    issues, notes = evaluate(files_text)
    for n in notes:
        print("NOTE  " + n)
    for it in issues:
        print("FAIL  " + it)
    n_fail = len(issues)
    if report_only:
        print("---- CSS 变量自引用（报告态）：%d 项 ----" % n_fail)
        return 0
    print("---- CSS 变量自引用：%d FAIL ----" % n_fail)
    return 1 if n_fail else 0


def _self_test():
    """注入式负样本自测：自引用必红 / 正常引用不红 / fallback 自引用仍红 / 干净态不误报。"""
    fails = []
    # T1 自引用必红
    i1, _ = evaluate({"p.html": ":root { --chart-1: var(--chart-1); }"})
    if not i1:
        fails.append("T1 自引用必红未命中")
    # T2 正常引用不红
    i2, _ = evaluate({"p.html": ":root { --accent: var(--chart-1); }"})
    if i2:
        fails.append("T2 正常引用误报：%s" % i2)
    # T3 带 fallback 的自引用仍红
    i3, _ = evaluate({"p.html": ":root { --x: var(--x, #fff); }"})
    if not i3:
        fails.append("T3 带 fallback 的自引用必须仍判红")
    # T4 干净态不误报
    i4, _ = evaluate({"p.html": ":root { --a: #fff; --b: var(--a); }"})
    if i4:
        fails.append("T4 干净态误报：%s" % i4)
    # T5 style 块内自引用必红（带行号定位）
    i5, _ = evaluate({"p.html": "<html><style>\n:root {\n  --y: var(--y);\n}\n</style></html>"})
    if not i5 or ":3" not in i5[0]:
        fails.append("T5 style 块内自引用必红且行号正确：%s" % i5)
    # T6 多文件同查
    i6, _ = evaluate({"a.html": "--z: var(--z);", "b.html": "--w: var(--w);"})
    if len(i6) != 2:
        fails.append("T6 多文件应各报 1 条：%s" % i6)

    for f in fails:
        print("FAIL  " + f)
    total = 6
    print("---- CSS 变量自引用 self-test：%d/%d 通过 ----" % (total - len(fails), total))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description="CSS 变量自引用判据（W1110）")
    ap.add_argument("--gate", action="store_true", help="门禁态（默认行为）")
    ap.add_argument("--report", action="store_true", help="只报告不判红")
    ap.add_argument("--self-test", action="store_true", help="注入式负样本自测")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    return run_check(report_only=args.report)


if __name__ == "__main__":
    sys.exit(main())
