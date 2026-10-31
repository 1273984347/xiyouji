#!/usr/bin/env python3
"""check_inlined_css.py — W495 转正门禁：data/EN 页 INLINED CSS 块完整性防回归。

背景（W495 热修复）：W493 一次性脚本曾把 224 个 data+EN 页的 INLINED 块
（tokens.css + system.css 内联副本，约 30KB）清空为空 <style>，全站渲染裸文本，
而既有 14 道门禁（结构平衡/CSP/pageerror/溢出等）全部 trivially 通过、无一拦截。
本门禁直接断言 INLINED 块内容体积 ≥ 阈值，堵住"文本门禁全绿、渲染全裸"盲区。

规则：
- 扫描 site/data/*.html + site/en/*.html（排除 _shell.html / _template.html）；
- 每页必须含 INLINED CSS 标记，且标记块内容（<style> 与 </style> 之间）≥ 20000 字节；
- 当前实测 30659B，阈值 20KB 留足瘦身余量又能抓住清空/半清空事故。

退出码：0 全过 / 1 有违规。
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN_BYTES = 20000
MARKER_RE = re.compile(r"INLINED CSS.*?-->\s*<style>(.*?)</style>", re.S)

# W1053 G-02（W1046 方案）：内容特征断言——体积阈值之外的「真 INLINED」判定。
# 词表 2026-10-31 实测提取（tokens.css 72 变量取稳定核心 12；system.css 顶级选择器族取 8），
# 实测真实 INLINED 块 tokens 12/12·system 8/8 全命中；阈值 ≥8/≥3 留瘦身余量。
TOKEN_FEATURES = ("--ink", "--accent", "--paper", "--danger", "--dur-base", "--ease-out-quart",
                  "--font-mono", "--border-hairline", "--accent-soft", "--dark-text",
                  "--container-read", "--accent-wash")
SYS_FEATURES = (".topnav", ".hero", ".chart-block", ".site-footer", ".kpi-card",
                ".filter-tab", ".section-head", ".dark-band")
TOKEN_MIN = 8
SYS_MIN = 3

EXCLUDE = ("_shell.html", "_template.html")


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "site", "data", "*.html"))
                   + glob.glob(os.path.join(ROOT, "site", "en", "*.html")))
    files = [f for f in files if os.path.basename(f) not in EXCLUDE]
    bad = []
    sizes = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            t = fh.read()
        m = MARKER_RE.search(t)
        n = len(m.group(1).strip()) if m else 0
        if not m or n < MIN_BYTES:
            bad.append((os.path.relpath(f, ROOT), "体积 %dB < %dB 或块缺失" % (n, MIN_BYTES)))
            continue
        body = m.group(1)
        tok_hit = sum(1 for x in TOKEN_FEATURES if x in body)
        sys_hit = sum(1 for x in SYS_FEATURES if x in body)
        if tok_hit < TOKEN_MIN or sys_hit < SYS_MIN:
            bad.append((os.path.relpath(f, ROOT),
                        "内容特征不足（tokens %d/%d·system %d/%d）——疑似塞无关 CSS 冒充"
                        % (tok_hit, len(TOKEN_FEATURES), sys_hit, len(SYS_FEATURES))))
            continue
        sizes.append(n)

    if bad:
        print("INLINED CSS 门禁 FAIL：%d/%d 页体积不足或特征缺失" % (len(bad), len(files)))
        for p, why in bad[:10]:
            print("  %s  (%s)" % (p, why))
        if len(bad) > 10:
            print("  ... 共 %d 个" % len(bad))
        return 1
    print("INLINED CSS 门禁通过：%d 页块完整（min %dB ≥ %dB·特征 tokens ≥%d/system ≥%d 全过）"
          % (len(files), min(sizes), MIN_BYTES, TOKEN_MIN, SYS_MIN))
    return 0


def _self_test():
    """G-02 负例/正例：20KB 垃圾 CSS 必红（特征不足）·真 tokens/system 片段必过。"""
    import tempfile
    filler = "/* junk */\n" + ".junk-x{color:#123}\n" * 1400  # ~20KB 无特征 CSS
    real = ("/* INLINED */\n" + "\n".join("%s: x;" % v for v in TOKEN_FEATURES)
            + "\n" + "\n".join("%s{color:#000}" % c for c in SYS_FEATURES)
            + "\n" + "body{margin:0}\n" + "/* real padding */\n" + "/* fill line */\n" * 1400)
    cases = [
        ("垃圾 20KB 无特征必红", "INLINED CSS test-->\n<style>%s</style>" % filler, False),
        ("真 tokens/system 片段必过", "INLINED CSS test-->\n<style>%s</style>" % real, True),
    ]
    fails = 0
    for name, page, expect_pass in cases:
        d = tempfile.mkdtemp(prefix="g02_")
        data = os.path.join(d, "site", "data")
        os.makedirs(data)
        with open(os.path.join(data, "t.html"), "w", encoding="utf-8") as fh:
            fh.write(page)
        # 借 glob：把临时目录伪装成 ROOT——直接调核心判定而非常规 main
        m = MARKER_RE.search(page)
        body = m.group(1) if m else ""
        n = len(body.strip())
        tok = sum(1 for x in TOKEN_FEATURES if x in body)
        sysc = sum(1 for x in SYS_FEATURES if x in body)
        ok_vol = n >= MIN_BYTES
        ok_feat = tok >= TOKEN_MIN and sysc >= SYS_MIN
        passed = ok_vol and ok_feat
        ok = (passed == expect_pass)
        print("%s  %s（tokens %d/%d·system %d/%d·%dB）"
              % ("PASS" if ok else "FAIL", name, tok, len(TOKEN_FEATURES), sysc, len(SYS_FEATURES), n))
        if not ok:
            fails += 1
    print("---- inlined-css self-test：%d/%d 通过 ----" % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(_self_test())
    sys.exit(main())
