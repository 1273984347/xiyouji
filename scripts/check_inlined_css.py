#!/usr/bin/env python3
"""check_inlined_css.py — 页面样式来源完整性门禁（W495 转正 · W1274 口径修订）。

背景（W495 热修复）：W493 一次性脚本曾把 224 个 data+EN 页的 INLINED 块
（tokens.css + system.css 内联副本，约 30KB）清空为空 <style>，全站渲染裸文本，
而既有 14 道门禁（结构平衡/CSP/pageerror/溢出等）全部 trivially 通过、无一拦截。
本门禁直接断言 INLINED 块内容体积 ≥ 阈值，堵住"文本门禁全绿、渲染全裸"盲区。

W1274 口径修订（随批三 A 方案「先转外部共享 CSS」）：公共层开始以外链加载后，
"INLINED 块 ≥ 20KB"这一形态判据会在外链化后对全部页面误判 ⇒ 改为**二选一**：
  · 形态 A（内联）：保留原判据（INLINED 块 ≥ 20KB + tokens/system 内容特征）；
  · 形态 B（外链·W1274 起）：页面含指向 tokens.css 与 system.css 的两个 <link>，
    且**两个目标文件按页目录解析后真实存在** ⇒ 相对路径写错（外链指向不存在的文件 ⇒
    样式整体失效·渲染裸文本）必判红 ⇒ 与原判据等强度地堵住盲区。

退出码：0 全过 / 1 有违规。
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN_BYTES = 20000
MARKER_RE = re.compile(r"INLINED CSS.*?-->\s*<style>(.*?)</style>", re.S)
RE_LINK_HREF = re.compile(r"<link[^>]+href=[\"']([^\"']+)[\"']", re.I)
PUBLIC_NAMES = ("tokens.css", "system.css")

TOKEN_FEATURES = ("--ink", "--accent", "--paper", "--danger", "--dur-base", "--ease-out-quart",
                  "--font-mono", "--border-hairline", "--accent-soft", "--dark-text",
                  "--container-read", "--accent-wash")
SYS_FEATURES = (".topnav", ".hero", ".chart-block", ".site-footer", ".kpi-card",
                ".filter-tab", ".section-head", ".dark-band")
TOKEN_MIN = 8
SYS_MIN = 3

EXCLUDE = ("_shell.html", "_template.html")
REDIRECT_RE = re.compile(r"<meta[^>]+http-equiv=[\"']refresh[\"']", re.I)


def public_links(text):
    # 页内指向公共层（tokens.css / system.css）的 link href 列表
    out = []
    for m in RE_LINK_HREF.finditer(text):
        href = m.group(1)
        if os.path.basename(href) in PUBLIC_NAMES:
            out.append(href)
    return out


def judge_page(text, page_path):
    """判定单页样式来源是否完好 → (ok, why, kind)；kind ∈ inline / external。"""
    _links = public_links(text)
    if _links:
        _names = {os.path.basename(x) for x in _links}
        if _names != set(PUBLIC_NAMES):
            return (False, "公共层外链不完整（%s）" % sorted(_names), "external")
        _missing = []
        for href in _links:
            tgt = os.path.join(os.path.dirname(os.path.abspath(page_path)), href)
            if not os.path.exists(tgt):
                _missing.append(href)
        if _missing:
            return (False, "公共层外链目标不存在（%s）" % ",".join(sorted(_missing)), "external")
        return (True, "", "external")
    m = MARKER_RE.search(text)
    n = len(m.group(1).strip()) if m else 0
    if not m or n < MIN_BYTES:
        return (False, "体积 %dB < %dB 或块缺失" % (n, MIN_BYTES), "inline")
    body = m.group(1)
    tok_hit = sum(1 for x in TOKEN_FEATURES if x in body)
    sys_hit = sum(1 for x in SYS_FEATURES if x in body)
    if tok_hit < TOKEN_MIN or sys_hit < SYS_MIN:
        return (False, "内容特征不足（tokens %d/%d·system %d/%d）——疑似塞无关 CSS 冒充"
                % (tok_hit, len(TOKEN_FEATURES), sys_hit, len(SYS_FEATURES)), "inline")
    return (True, "", "inline")


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "site", "data", "*.html"))
                   + glob.glob(os.path.join(ROOT, "site", "en", "*.html"))
                   + glob.glob(os.path.join(ROOT, "site", "reader", "**", "*.html"), recursive=True))
    files = [f for f in files if os.path.basename(f) not in EXCLUDE]
    bad = []
    sizes = []
    n_inline = 0
    n_external = 0
    for f in files:
        with open(f, encoding="utf-8") as fh:
            t = fh.read()
        if not public_links(t) and REDIRECT_RE.search(t) and "tokens.css" not in t:
            continue  # reader 跳转桩无 CSS 链接（themes/index.html）
        ok, why, kind = judge_page(t, f)
        if not ok:
            bad.append((os.path.relpath(f, ROOT), why))
            continue
        if kind == "external":
            n_external += 1
        else:
            n_inline += 1
            m = MARKER_RE.search(t)
            sizes.append(len(m.group(1).strip()))

    if bad:
        print("页面样式来源门禁 FAIL：%d/%d 页不完好（内联 %d·外链 %d）"
              % (len(bad), len(files), n_inline, n_external))
        for p, why in bad[:10]:
            print("  %s  (%s)" % (p, why))
        if len(bad) > 10:
            print("  ... 共 %d 个" % len(bad))
        return 1
    _mn = ("min %dB ≥ %dB" % (min(sizes), MIN_BYTES)) if sizes else "无内联形态页"
    print("页面样式来源门禁通过：%d 页（内联形态 %d·外链形态 %d·%s·特征 tokens ≥%d/system ≥%d 全过）"
          % (len(files), n_inline, n_external, _mn, TOKEN_MIN, SYS_MIN))
    return 0


def _self_test():
    """自测：垃圾 20KB 无特征必红 ·真片段必过 ·外链形态必过 ·外链目标缺失必红。"""
    import tempfile
    filler = "/* junk */\n" + ".junk-x{color:#123}\n" * 1400
    real = ("/* INLINED */\n" + "\n".join("%s: x;" % v for v in TOKEN_FEATURES)
            + "\n" + "\n".join("%s{color:#000}" % c for c in SYS_FEATURES)
            + "\n" + "body{margin:0}\n" + "/* real padding */\n" + "/* fill line */\n" * 1400)
    ext_ok = '<link rel="stylesheet" href="../../tokens.css">\n<link rel="stylesheet" href="../../system.css">\n<style>.x{}</style>'
    ext_bad = '<link rel="stylesheet" href="../../nope.css">\n<style>.x{}</style>'
    cases = [
        ("垃圾 20KB 无特征必红", "INLINED CSS test-->\n<style>%s</style>" % filler, False),
        ("真 tokens/system 片段必过", "INLINED CSS test-->\n<style>%s</style>" % real, True),
        ("外链形态必过（目标存在）", ext_ok, True),
        ("外链目标缺失必红", ext_bad, False),
    ]
    fails = 0
    for name, page, expect_pass in cases:
        d = tempfile.mkdtemp(prefix="g02_")
        data = os.path.join(d, "site", "data")
        os.makedirs(data)
        page_path = os.path.join(data, "t.html")
        with open(page_path, "w", encoding="utf-8") as fh:
            fh.write(page)
        # 外链用例的 href 是 ../../tokens.css（页在 <d>/site/data/ ⇒ 解析到 <d>/）
        if "tokens.css" in page:
            with open(os.path.join(d, "tokens.css"), "w", encoding="utf-8") as fh:
                fh.write("x")
            with open(os.path.join(d, "system.css"), "w", encoding="utf-8") as fh:
                fh.write("x")
        ok, why, kind = judge_page(page, page_path)
        good = (ok == expect_pass)
        print("%s  %s（%s%s）"
              % ("PASS" if good else "FAIL", name, kind, ("·" + why) if why else ""))
        if not good:
            fails += 1
    print("---- inlined-css self-test：%d/%d 通过 ----" % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(_self_test())
    sys.exit(main())
