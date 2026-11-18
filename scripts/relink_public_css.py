#!/usr/bin/env python3
# relink_public_css.py — 自包含页「公共层内联副本 → 外部 link」外链化工具（W1274 立·批三 A 方案）
#
# 背景（W1273/W1274 实测）：全站 875 页中 867 页把 site/tokens.css 与 site/system.css 的
# 合并副本内联在页面第一个 style 块里（每页约 68.9 KB）=> 公共层改一次不能全站生效
#（公共层实际只被 7 页外链引用）。本工具把这类页里的**公共层规则**剥离出来、换成两个
# link（tokens 在前、system 在后·与原内联顺序一致），相对路径按页所在目录计算。
#
# 剥离粒度 = 规则级（不是整块！）：块0 实为「公共层 + 该页私有层」合并体（实测 667 个
# 选择器里 157 个是页私有）=> 整块替换会删掉私有层样式。判定某条规则可剥离的条件：
#   ① 选择器集合在公共层索引中；② 声明与公共层**逐字相同**（⇒ 私有层覆写版本保留不动，
#   例如 .data-status-badge 的 var(--radius-pill) 覆盖版）；③ 仅处理顶层规则（@media 内
#   规则保守保留·先证等价再逐步瘦身）。
#
# 前提（已实测）：CSP 的 style-src 含 self 故放行同源外链；file:// 与 http:// 双协议外链
# 均生效；@font-face 走 tokens.css 原件的 site/ 相对路径故天然正确。
#
# 用法：
#   py -3 scripts/relink_public_css.py --dry-run
#   py -3 scripts/relink_public_css.py --apply
#   py -3 scripts/relink_public_css.py --apply <file> ...
#   py -3 scripts/relink_public_css.py --self-test
#
# 退出码：0 = 成功（无改动亦 0）· 1 = 有失败页 · 2 = 判据自身异常。
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
RE_STYLE = re.compile(r"(<style[^>]*>)(.*?)(</style>)", re.S | re.I)
RE_COMMENT = re.compile(r"/\*.*?\*/", re.S)
PUBLIC_FILES = ("tokens.css", "system.css")
MIN_STRIP_RULES = 150


def _norm(css: str) -> str:
    return re.sub(r"\s+", " ", css).strip()


def _match_block(css: str, i: int) -> int:
    # 从第 i 个字符（"{"）起找配对 "}" 的结束位置（不含）
    depth = 1
    j = i + 1
    n = len(css)
    while j < n and depth:
        if css[j] == "{":
            depth += 1
        elif css[j] == "}":
            depth -= 1
        j += 1
    return j


def _top_rules(css: str):
    # 顶层规则（不进 @media 嵌套）：[(selset, body, start, end)]
    out = []
    i = 0
    n = len(css)
    depth = 0
    buf_start = 0
    while i < n:
        ch = css[i]
        if ch == "{" and depth == 0:
            end = _match_block(css, i)
            head = css[buf_start:i]
            body = css[i + 1:end - 1]
            sels = frozenset(s.strip() for s in head.split(",") if s.strip())
            out.append((sels, _norm(body), buf_start, end))
            i = end
            buf_start = end
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth = max(0, depth - 1)
        i += 1
    return out


def public_rule_index() -> dict:
    # {选择器集合: {声明集合}}
    idx = {}
    for name in PUBLIC_FILES:
        p = os.path.join(SITE, name)
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as f:
            css = f.read()
        for sels, body, _s, _e in _top_rules(css):
            idx.setdefault(sels, set()).add(body)
    return idx


def rel_href(page_path: str, name: str) -> str:
    # 页所在目录 → 公共层文件的相对路径（posix 风格）
    page_dir = os.path.dirname(os.path.abspath(page_path))
    target = os.path.join(SITE, name)
    return os.path.relpath(target, page_dir).replace(os.sep, "/")


def build_links(page_path: str) -> str:
    parts = []
    for name in PUBLIC_FILES:
        parts.append("<link rel=\"stylesheet\" href=\"%s\">" % rel_href(page_path, name))
    return "\n".join(parts)


def strip_public_rules(css: str, pub_idx: dict):
    # 返回 (新 css, 剥离条数, 保留条数)
    rules = _top_rules(css)
    cuts = []
    keep = []
    for sels, body, st, en in rules:
        if sels in pub_idx and body in pub_idx[sels]:
            cuts.append((st, en))
        else:
            keep.append((sels, body))
    if not cuts:
        return css, 0, len(keep)
    out = css
    for st, en in reversed(cuts):
        out = out[:st] + out[en:]
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip(), len(cuts), len(keep)


def relink_page(path: str, pub_idx: dict, apply: bool = False):
    # 返回 (状态, 前字节, 后字节, 备注)；状态 ∈ changed / already / skip / error
    try:
        with open(path, encoding="utf-8", newline="") as f:
            html = f.read()
    except OSError as exc:
        return ("error", 0, 0, str(exc)[:120])
    before = len(html.encode("utf-8"))
    done = True
    for n in PUBLIC_FILES:
        if rel_href(path, n) not in html:
            done = False
            break
    if done:
        return ("already", before, before, "")
    m = RE_STYLE.search(html)
    if not m:
        return ("skip", before, before, "无内联 style 块")
    stripped, ncut, nkeep = strip_public_rules(m.group(2), pub_idx)
    if ncut < MIN_STRIP_RULES:
        return ("skip", before, before, "可剥离规则 %d 条 < 阈值 %d（非公共层副本·不误伤）" % (ncut, MIN_STRIP_RULES))
    # W1274 修正：替换区间覆盖了整个 style 块（含开闭标签）⇒ 必须**重建 <style> 包裹**，
    # 否则 CSS 源码会被当正文渲染（E-244 目视亲验抓出·探针与门禁当时全绿）。
    if stripped:
        replacement = (build_links(path) + "\n" + m.group(1) + "\n"
                       "/* W1274：公共层规则已外链（tokens.css + system.css）·本页私有层保留 */\n"
                       + stripped + "\n" + m.group(3))
    else:
        replacement = build_links(path) + "\n<!-- W1274：公共层已外链（tokens.css + system.css） -->"
    new_html = html[:m.start()] + replacement + html[m.end():]
    after = len(new_html.encode("utf-8"))
    if apply and after != before:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_html)
    return ("changed", before, after, "剥离 %d 条·保留 %d 条" % (ncut, nkeep))


def iter_pages():
    for dirpath, _dirs, files in os.walk(SITE):
        for fn in files:
            if fn.endswith(".html") and not fn.startswith("_"):
                yield os.path.join(dirpath, fn)


def _self_test() -> int:
    fails = []
    idx = {frozenset([".a"]): {"color: red"}}
    out, ncut, nkeep = strip_public_rules(".a{color: red}\n.b{color: blue}", idx)
    if ncut != 1 or nkeep != 1:
        fails.append("正例1 应剥离 1 条公共层规则·保留 1 条私有")
    if ".b{color: blue}" not in out:
        fails.append("正例2 私有层规则必须保留")
    out2, ncut2, _ = strip_public_rules(".a{color: green}", idx)
    if ncut2 != 0:
        fails.append("负例 声明不同（覆写）时不得剥离")
    if rel_href(os.path.join(SITE, "data", "x.html"), "tokens.css") != "../tokens.css":
        fails.append("正例3 相对路径计算错误")
    if rel_href(os.path.join(SITE, "reader", "themes", "x.html"), "system.css") != "../../system.css":
        fails.append("正例4 深目录相对路径错误")
    print("自测：4 条正例 + 1 条负例%s" % ("·全部通过 ✓" if not fails else "·失败 ✗"))
    for f in fails:
        print("   " + f)
    return 1 if fails else 0


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--self-test" in argv:
        return _self_test()
    apply = "--apply" in argv
    targets = [a for a in argv if not a.startswith("-")]
    if not targets:
        targets = list(iter_pages())
    pub_idx = public_rule_index()
    changed = already = skipped = 0
    saved = 0
    for p in targets:
        full = p if os.path.isabs(p) else os.path.join(ROOT, p)
        st, before, after, note = relink_page(full, pub_idx, apply)
        if st == "changed":
            changed += 1
            saved += before - after
        elif st == "already":
            already += 1
        else:
            skipped += 1
            if st == "error":
                print("FAIL %s：%s" % (p, note))
                return 1
    print("目标 %d 页：改造 %d · 已外链 %d · 跳过 %d · 私有层净减 %d B"
          % (len(targets), changed, already, skipped, saved))
    return 0


if __name__ == "__main__":
    sys.exit(main())
