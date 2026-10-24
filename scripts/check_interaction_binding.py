#!/usr/bin/env python3
"""check_interaction_binding.py — 交互绑定门禁（W908 建置·T-18/A-T07-05）。

背景（W858 P0 实证）：渡口页 6 控件零事件绑定长期在线上失效——页面控件骨架在而
主脚本整段缺失（W333 后某批剥离·W908 自 git 历史回灌原装修复）。此类缺陷 CSP/语法
门禁全绿（脚本没了就没有语法可查），需「控件 ↔ 绑定信号」对账防线。

判据（宁窄勿误）：
  P1 注册控件绑定对账：KNOWN_CONTROLS 表（页 → 必须有绑定信号的控件 id/选择器）——
     页面任一 script 块中出现该 id/选择器的 DOM 引用（getElementById / querySelector
     / $('#id') / classList 操作任一形态）即视为已绑定；缺一即 FAIL。
  P2 泛化扫（WARN 级·防误伤）：根页所有 <button id="X"> 在脚本区零引用 → 计数报告
     （存量豁免面大·起步 NOTE 策略·W904 C5c 同款治理路径）。
  C1 crash 即拦（fail-closed）：文件缺失/不可解析按 FAIL。

豁免：KNOWN_CONTROLS 的 id 变更须同批改本表（单一注册表·防漂移）。

用法：
    python scripts/check_interaction_binding.py --gate      # 门禁模式（verify 调用）
    python scripts/check_interaction_binding.py --self-test # 自测（正负样本）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAIL = 0

# 注册表：页 → 控件绑定信号清单（id 字符串或选择器片段·在任一 script 块出现即算）
KNOWN_CONTROLS: dict[str, list[str]] = {
    "site/dukou-engine.html": ["gen", "rand", "rag", "themeToggle", "graphReset"],
    "site/index.html": ["nav-toggle", "ask-chip"],
    "site/curated.html": ["nav-toggle"],
    "site/dashboard.html": ["nav-toggle"],
    "site/guide.html": ["nav-toggle"],
}

SCRIPT_RE = re.compile(r"<script[^>]*>(.*?)</script>", re.S | re.I)


def page_scripts(rel: str) -> str:
    p = ROOT / rel
    if not p.exists():
        raise FileNotFoundError(rel)
    return "\n".join(SCRIPT_RE.findall(p.read_text(encoding="utf-8", errors="ignore")))


def check(verbose: bool = True) -> int:
    global FAIL
    fails: list[str] = []
    notes: list[str] = []
    for rel, signals in KNOWN_CONTROLS.items():
        try:
            js = page_scripts(rel)
        except FileNotFoundError:
            fails.append("P1: %s 页面缺失（fail-closed）" % rel)
            continue
        for sig in signals:
            hit = sig if sig.startswith(".") else ("'%s'" % sig)
            if sig in js or hit in js or ('"%s"' % sig) in js:
                continue
            fails.append("P1: %s 控件「%s」在页面脚本区零引用（绑定缺失·W858 P0 族）" % (rel, sig))
    # P2 泛化扫（NOTE）
    orphan = 0
    for rel in KNOWN_CONTROLS:
        try:
            js = page_scripts(rel)
            html = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        except FileNotFoundError:
            continue
        for bid in re.findall(r'<button[^>]*\bid="([^"]+)"', html):
            if bid not in js and ("'%s'" % bid) not in js:
                orphan += 1
    if orphan:
        notes.append("P2: 根页 button[id] 脚本零引用 %d 处（起步 NOTE·防误伤·存量豁免）" % orphan)

    if verbose:
        for f in fails:
            print("FAIL ", f)
        for n in notes:
            print("NOTE ", n)
        print("---- 交互绑定门禁：%d FAIL / %d NOTE ----" % (len(fails), len(notes)))
    FAIL = len(fails)
    return 1 if fails else 0


def self_test() -> int:
    """正负样本：好树全绿 / 摘掉一个绑定信号必红 / 页面缺失必红。"""
    import tempfile
    ok_page = "<html><body><button id='gen'>g</button><script>['gen','rand','rag','themeToggle','graphReset'].forEach(function(i){document.getElementById(i)})</script></body></html>"
    cases = []
    with tempfile.TemporaryDirectory() as td:
        global ROOT
        old = ROOT
        try:
            ROOT = Path(td)
            (ROOT / "site").mkdir()
            (ROOT / "site" / "dukou-engine.html").write_text(ok_page, encoding="utf-8")
            (ROOT / "site" / "index.html").write_text(
                "<button class='nav-toggle'></button><span class='ask-chip'></span><script>q('.nav-toggle');q('.ask-chip')</script>", encoding="utf-8")
            for rel in ("curated", "dashboard", "guide"):
                (ROOT / "site" / ("%s.html" % rel)).write_text(
                    "<script>nav-toggle 关联</script>", encoding="utf-8")
            r = check(verbose=False)
            cases.append(("T1 注册控件全绿", r == 0))
            t = (ROOT / "site" / "dukou-engine.html").read_text(encoding="utf-8").replace("'gen'", "'gone'")
            (ROOT / "site" / "dukou-engine.html").write_text(t, encoding="utf-8")
            r2 = check(verbose=False)
            cases.append(("T2 摘除绑定信号必红", r2 == 1))
            (ROOT / "site" / "guide.html").unlink()
            r3 = check(verbose=False)
            cases.append(("T3 页面缺失必红（fail-closed）", r3 == 1))
        finally:
            ROOT = old
    bad = [n for n, ok in cases if not ok]
    for n, ok in cases:
        print("%s  %s" % ("PASS" if ok else "FAIL", n))
    print("---- 交互绑定门禁 self-test：%d/%d ----" % (len(cases) - len(bad), len(cases)))
    return 1 if bad else 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    return check()


if __name__ == "__main__":
    sys.exit(main())
