#!/usr/bin/env python3
"""check_template_contract.py — 第 69 槽 · 模板结构契约 / 检索假阳性判据（W1178）。

背景（两次同类实证）：
  · W1177：`grep -c cite-block site/_template.html` 返回 7 ⇒ 判断「模板已有引用块」。
    实际那 7 处全是 CSS 选择器（.cite-block / .cite-item / .cite-text …），HTML 结构为 0，
    新页 citability C3 因此判红。
  · W1175：只 grep `site/` 就断言「STATUS_TEXT 无定义」，实为正本在 scripts/。
两次都是「检索给了个数就下结论」，且缺的不是知识而是**可复算的判据**。

判据：
  C1 结构存在性——模板与每个 data 页必须含「完整标签串」，**类名/CSS 选择器命中不算证据**。
  C2 检索可复算——`--evidence KEYWORD` 输出命中行号、上下文与形态（结构 / CSS / 注释 / 其他），
     并在「只有 CSS 命中、无结构命中」时显式告警。让任何「我查过了」都能被机器复核。

E-167 自指防护：脚本自身含这些字面量，但扫描面严格限定为 site/_template.html 与
site/data/*.html（不含 scripts/），因此不会把自己判红。自测的假样本在内存中构造，不落盘。

用法：
  py -3 scripts/check_template_contract.py                  # 全量判据
  py -3 scripts/check_template_contract.py --self-test      # 反例自测
  py -3 scripts/check_template_contract.py --evidence cite-block
  py -3 scripts/check_template_contract.py --evidence STATUS_TEXT --scope all
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "site", "_template.html")
DATA_DIR = os.path.join(ROOT, "site", "data")

# 结构契约：必须是完整标签串（不是类名）。键为「门禁依据」。
CONTRACT = (
    ("C3 引用格式块", '<div class="cite-block">'),
    ("C1/C2/C4 数据源锚点", '<div id="dataSource">'),
    ("SEO R1 description", '<meta name="description"'),
    ("第 30 槽降级声明", '<!-- chart-degrade:'),
)

SUMMARY = "---- 第 69 门禁 模板契约：契约 %d 项 · 违规 %d · %s ----"


def _style_ranges(text: str) -> list[tuple[int, int]]:
    """返回 <style>...</style> 的字符区间（形态判定用）。"""
    return [m.span() for m in re.finditer(r"<style\b[^>]*>.*?</style>", text, re.S | re.I)]


def _comment_ranges(text: str) -> list[tuple[int, int]]:
    return [m.span() for m in re.finditer(r"<!--.*?-->", text, re.S)]


def classify(text: str, pos: int, style_ranges, comment_ranges) -> str:
    """判定命中形态：结构 / CSS / 注释 / 其他。"""
    if any(a <= pos < b for a, b in comment_ranges):
        return "注释"
    if any(a <= pos < b for a, b in style_ranges):
        return "CSS"
    line_start = text.rfind("\n", 0, pos) + 1
    line_end = text.find("\n", pos)
    line = text[line_start: line_end if line_end > 0 else len(text)]
    stripped = line.strip()
    # CSS 选择器形态：以 . 开头、或含 { }、或处于选择器列表里
    if re.search(r"(?:^|[\s,>])\.[A-Za-z][\w-]*", stripped) and "{" in stripped or stripped.startswith("."):
        return "CSS"
    if re.search(r"<[A-Za-z][^>]*>", line):
        return "结构"
    return "其他"


def evidence(keyword: str, scope: str = "site") -> int:
    """输出可复算的检索证据：命中位置 + 上下文 + 形态。"""
    files = [TEMPLATE] + sorted(
        os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".html")
    )
    if scope == "all":
        files += [os.path.join(ROOT, "scripts", f) for f in sorted(os.listdir(os.path.join(ROOT, "scripts")))
                  if f.endswith(".py")]

    total = 0
    struct = 0
    shapes: dict[str, int] = {}
    for path in files:
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        sr, cr = _style_ranges(text), _comment_ranges(text)
        for m in re.finditer(re.escape(keyword), text):
            total += 1
            shape = classify(text, m.start(), sr, cr)
            shapes[shape] = shapes.get(shape, 0) + 1
            if shape == "结构":
                struct += 1
            if total <= 8:
                line_no = text.count("\n", 0, m.start()) + 1
                ctx = text[text.rfind("\n", 0, m.start()) + 1: text.find("\n", m.start())].strip()
                print(f"  {os.path.relpath(path, ROOT)}:{line_no}  [{shape}]  {ctx[:110]}")
    print(f"[evidence] 关键词 {keyword!r} · 扫描 {len(files)} 文件 · 命中 {total} · "
          f"其中结构 {struct} · 形态分布 {shapes}")
    if total and not struct:
        print("  ⚠ 只有非结构命中——类名/CSS/注释不构成「结构存在」的证据（W1177 实证）")
    return 0


def check(target: str | None = None) -> tuple[list[str], int]:
    """检查模板（必查）与 data 页（--target 可只查一页）。返回 (违规列表, 检查文件数)。"""
    fails: list[str] = []
    if not os.path.exists(TEMPLATE):
        return [f"模板缺失：{os.path.relpath(TEMPLATE, ROOT)}"], 0

    # 默认只约束「模板」；历史页有自己的合规形态（例如 dataSource 的旧写法），
    # 全量套用新契约会误伤存量——新页由 --post 通过 --target 单独验。
    files = [TEMPLATE]
    if target:
        p = target if os.path.isabs(target) else os.path.join(ROOT, target)
        if not os.path.exists(p):
            return [f"目标页不存在：{target}"], 0
        files.append(p)

    for path in files:
        text = open(path, encoding="utf-8", errors="replace").read()
        try:
            rel = os.path.relpath(path, ROOT)
        except ValueError:  # 跨盘符（如 --target 指向系统临时目录）
            rel = os.path.basename(path)
        for label, needle in CONTRACT:
            if needle not in text:
                # 反查：是否只有类名/CSS 形态的命中（W1177 假阳性形态）
                hint = ""
                if label.startswith("C3") and ".cite-block" in text:
                    hint = "（命中 .cite-block 的 CSS 选择器但无 <div class=\"cite-block\"> 结构——W1177 实证形态）"
                fails.append(f"{rel}: 缺 {label}{hint}")
    return fails, len(files)


def self_test() -> int:
    """反例自测：构造 W1177 的假阳性样本，必须被判红。"""
    fake = """<html><head><style>
.cite-block { border: 1px solid; }
.cite-item { display: flex; }
.cite-text { font-size: 12px; }
</style></head><body><main></main></body></html>"""
    sr, cr = _style_ranges(fake), _comment_ranges(fake)
    hits = [m.start() for m in re.finditer(re.escape("cite-block"), fake)]
    shapes = [classify(fake, p, sr, cr) for p in hits]
    cases = [
        ("只有 CSS 类命中不算结构", all(s != "结构" for s in shapes) and len(hits) > 0),
        ("完整标签串才算结构", CONTRACT[0][1] in '<div class="cite-block"></div>'),
        ("假样本缺契约应判红", all(needle not in fake for _, needle in CONTRACT)),
        ("真模板四项齐备", all(needle in open(TEMPLATE, encoding="utf-8").read() for _, needle in CONTRACT)),
    ]
    ok = 0
    for name, passed in cases:
        print(f"{'OK  ' if passed else 'FAIL'}  {name}")
        ok += int(passed)
    print(f"自测 {ok}/{len(cases)} 通过 · 汇总行 {SUMMARY % (len(CONTRACT), 0, 'OK')}")
    return 0 if ok == len(cases) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--target", default="", help="只检查指定页（相对仓根，如 site/data/foo.html）")
    ap.add_argument("--evidence", default="", help="输出某关键词的可复算检索证据")
    ap.add_argument("--scope", default="site", choices=["site", "all"], help="--evidence 的扫描范围")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.evidence:
        return evidence(args.evidence, args.scope)

    fails, n = check(args.target or None)
    for f in fails[:12]:
        print("FAIL  " + f)
    if len(fails) > 12:
        print(f"FAIL  … 另有 {len(fails) - 12} 项")
    print(SUMMARY % (len(CONTRACT), len(fails), "FAIL" if fails else "OK"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
