# _w672_move_datasource.py — W672 WP-1.1：把 <head> 内误注入的 <div id="dataSource">（W657 落点缺陷）
# 整块移到 <body> 开标签之后（作为 body 第一个子节点），与浏览器 foster parenting 的
# 实际渲染位置一致，预期渲染零变化。方案：docs/superpowers/plans/2026-10-05-site-quality-remediation-plans.md §三 WP-1.1
#
# 用法：
#   python scripts/_w672_move_datasource.py --dry-run   # 逐页输出计划行，不改盘
#   python scripts/_w672_move_datasource.py --apply     # 落盘（保持原行尾，utf-8）
import argparse
import glob
import re

HEAD_RE = re.compile(r"<head[^>]*>(.*?)</head>", re.S | re.I)
BODY_OPEN = re.compile(r"<body[^>]*>", re.I)
DIV_TOK = re.compile(r"<div\b|</div>", re.I)
DS_IN_HEAD = re.compile(r"<div\s+[^>]*id=\"dataSource\"", re.I)


def find_pages():
    pages = []
    for f in sorted(glob.glob("site/data/*.html") + glob.glob("site/*.html") + glob.glob("site/en/*.html")):
        src = open(f, encoding="utf-8", newline="").read()
        m = HEAD_RE.search(src)
        if m and DS_IN_HEAD.search(m.group(1)):
            pages.append(f)
    return pages


def plan_one(src, fname):
    """返回 (计划行, ls, removal_end, block)。定位/平衡失败抛 ValueError。"""
    if src.count('id="dataSource"') != 1:
        raise ValueError("%s: id=\"dataSource\" 出现 %d 次（须为 1）" % (fname, src.count('id="dataSource"')))
    head = HEAD_RE.search(src)
    mdiv = DS_IN_HEAD.search(head.group(1))
    i = head.start(1) + mdiv.start()
    # 块起始 = 该行行首（含缩进）
    ls = src.rfind("\n", 0, i) + 1
    if src[ls:i].strip():
        raise ValueError("%s: dataSource div 前同行有其他内容" % fname)
    # div 嵌套平衡，找配对闭合
    depth = 0
    e = None
    for m in DIV_TOK.finditer(src, i):
        if m.group(0)[1] != "/":
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                e = m.end()
                break
    if e is None:
        raise ValueError("%s: div 嵌套不平衡" % fname)
    # 块后同行若只剩空白则连同行尾换行一起移除
    nl = src.find("\n", e)
    if nl == -1:
        removal_end = e
        block = src[ls:e]
    elif src[e:nl].strip() == "":
        removal_end = nl + 1
        block = src[ls:nl]
    else:
        removal_end = e
        block = src[ls:e]
    line_no = src[:ls].count("\n") + 1
    return "%s: 头内行 %d → body 首子节点（块 %d 字符）" % (fname, line_no, len(block)), ls, removal_end, block


def transform(src, ls, removal_end, block):
    s1 = src[:ls] + src[removal_end:]
    m = BODY_OPEN.search(s1)
    if not m:
        raise ValueError("body 开标签未找到")
    s2 = s1[:m.end()] + "\n" + block + s1[m.end():]
    if s2.count('id="dataSource"') != 1:
        raise ValueError("变换后 id=\"dataSource\" 计数异常")
    if DS_IN_HEAD.search(HEAD_RE.search(s2).group(1)):
        raise ValueError("变换后 head 内仍有 dataSource div")
    return s2


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    pages = find_pages()
    print("对象页数:", len(pages))
    fails = 0
    for f in pages:
        src = open(f, encoding="utf-8", newline="").read()
        try:
            line, ls, removal_end, block = plan_one(src, f)
        except ValueError as exc:
            fails += 1
            print("FAIL", exc)
            continue
        print(line)
        if args.apply:
            open(f, "w", encoding="utf-8", newline="").write(transform(src, ls, removal_end, block))
    if args.apply:
        print("已落盘 %d 页（失败 %d）" % (len(pages) - fails, fails))
    if fails:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
