#!/usr/bin/env python3
"""check_page_admission.py — 新建页准入门禁（W916 建置·C-W818-01 清偿·静态版）。

背景（W818 档 0）：「新建页准入检查」长期只有取证探针（file_protocol_probe.py·
一次性诊断件）而无常驻防线——file:// 双击直开两铁律（禁 type=module·零外域 script src）
靠纪律维持，全站现状为零违例但回归无门禁锁定。

判据（静态·无浏览器·秒级）：
  P1 全站 HTML 零 `<script type="module">`（file:// 下被 CORS 拦·W818 探针判据 A 实证）
  P2 全站 HTML 零外域 script src（http(s):// 开头且非本仓白名单——零外域铁律·
     与 generate_csp EXTERNAL_SCRIPT_HOSTS=[] 同源口径；本地 ./ 与 / 引用放行）
  fail-closed：扫描异常按 FAIL。

用法：
    python scripts/check_page_admission.py --gate
    python scripts/check_page_admission.py --self-test
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE_RE = re.compile(r"<script[^>]*\btype=[\"']module[\"']", re.I)
EXT_SRC_RE = re.compile(r"<script[^>]*\bsrc=[\"'](https?://[^\"']+)[\"']", re.I)
SCAN_DIRS = ("site",)


def scan(verbose: bool = True) -> int:
    fails: list[str] = []
    total = 0
    for d in SCAN_DIRS:
        for p in (ROOT / d).rglob("*.html"):
            total += 1
            try:
                t = p.read_text(encoding="utf-8", errors="ignore")
            except OSError as e:
                fails.append("P1: %s 读取失败（fail-closed）：%s" % (p, e))
                continue
            if MODULE_RE.search(t):
                fails.append("P1: %s 含 <script type=module>（file:// 被 CORS 拦·准入禁用）" % p.relative_to(ROOT))
            for m in EXT_SRC_RE.finditer(t):
                fails.append("P2: %s 外域脚本 %s（零外域铁律）" % (p.relative_to(ROOT), m.group(1)))
    if verbose:
        for f in fails:
            print("FAIL ", f)
        print("---- 新建页准入：%d FAIL / %d 页 ----" % (len(fails), total))
    return 1 if fails else 0


def self_test() -> int:
    import tempfile
    cases = []
    with tempfile.TemporaryDirectory() as td:
        global ROOT
        old = ROOT
        try:
            ROOT = Path(td)
            (ROOT / "site").mkdir()
            (ROOT / "site" / "a.html").write_text("<script src='./ok.js'></script>", encoding="utf-8")
            cases.append(("T1 本地引用放行", scan(verbose=False) == 0))
            (ROOT / "site" / "b.html").write_text('<script type="module" src="./m.js"></script>', encoding="utf-8")
            cases.append(("T2 type=module 必红", scan(verbose=False) == 1))
            (ROOT / "site" / "b.html").write_text('<script src="https://cdn.example.com/x.js"></script>', encoding="utf-8")
            cases.append(("T3 外域脚本必红", scan(verbose=False) == 1))
        finally:
            ROOT = old
    bad = [n for n, ok in cases if not ok]
    for n, ok in cases:
        print("%s  %s" % ("PASS" if ok else "FAIL", n))
    print("---- 新建页准入 self-test：%d/%d ----" % (len(cases) - len(bad), len(cases)))
    return 1 if bad else 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    return scan()


if __name__ == "__main__":
    sys.exit(main())
