#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w888_chapter_plate.py — W888 路 B：百回母版插画接回目页（ch007/014/015/023/027/030）。

**两处必改**（仓规「改了产物就要改生成器」·反之亦然）：
① 生成器 `scripts/build_reader.py`（源）：
   - `STYLE` 常量末尾追加 `.chapter-plate` 规则；
   - 新增 `CHAPTER_PLATES` 映射常量（母版图 → 回目页文件名的对应表）；
   - `_render_one_page()` 内**条件化**插入 `<figure class="chapter-plate">`（插在回目 H1 之后）。
   ⇒ 下次全量重生成时规则与插画都在，不会被抹掉。
② 产物 6 个 reader 回目页：精准注入（**不跑全量重生成**）。理由有两条实测依据：
   - 单跑 `build_reader.py` 会把已内联的 CSS 与 CSP meta 全剥掉，制造 **12 万行假 diff**
     （CHANGELOG:431 实证）；
   - 同步内联须跑 `inline_css.py --force`，而它的处理范围含 `site/en/` 138 页
     —— **与在途 W887 批的写面直接冲突**。
   注入内容与生成器输出逐字一致 ⇒ 将来全量重生成零漂移。

母版图语义：chap-07/14/15/23/27/30 是「百回体系化封面」的同一母版（旅人背影立中轴偏下、
层叠远山、通宽淡天、淡墨坡地贯通左右），按「可参数化铺一百回」设计；本批只落有图的六回，
其余 94 回无母版图（母版是「该回的配图」，不是全站装饰）。

暗色模式：浅底宣纸图贴 `--bg:#221D16` 会成亮斑 ⇒ 暗色模式隐藏。

行尾原样保留（读写均 newline=""）；已接过的页跳过（幂等）。
用法：python scripts/_w888_chapter_plate.py [--dry-run]
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILDER = os.path.join(ROOT, "scripts", "build_reader.py")

PLATES = {
    "ch007.html": "chap-07.webp",
    "ch014.html": "chap-14.webp",
    "ch015.html": "chap-15.webp",
    "ch023.html": "chap-23.webp",
    "ch027.html": "chap-27.webp",
    "ch030.html": "chap-30.webp",
}

# 生成器内的 STYLE 常量追加段（缩进 2 空格·与 STYLE 既有规则一致）
STYLE_ANCHOR = '  .reader-feedback a:hover { border-color: var(--accent); color: var(--accent-text); }\n"""'
STYLE_ADD = (
    '  .reader-feedback a:hover { border-color: var(--accent); color: var(--accent-text); }\n'
    '  /* W888：百回母版插画（浅底宣纸版·暗色模式下隐藏——浅底图贴深底会成亮斑） */\n'
    '  .chapter-plate { margin: 28px auto 36px; max-width: 420px; }\n'
    '  .chapter-plate img { width: 100%; height: auto; display: block; opacity: .92; }\n'
    '  html[data-theme="dark"] .chapter-plate { display: none; }\n'
    '"""'
)

CONST_ANCHOR = 'FOLD_SECTIONS = ("剧情梗概", "深度解读", "原文全文")'
CONST_ADD = CONST_ANCHOR + (
    '\n# W888：百回母版插画（chap-07/14/15/23/27/30 六张 1:1 母版·同一母版按「可参数化铺一百回」设计·'
    '\n# 本批只落有图的六回·其余 94 回无母版图——母版是「该回的配图」而非全站装饰）。'
    '\nCHAPTER_PLATES = {\n'
    + "".join('    "%s": "%s",\n' % (k, v) for k, v in sorted(PLATES.items()))
    + '}'
)

RENDER_ANCHOR = '    body_html, _n_folded = fold_sections(body_html)  # W847 AC-22'
# 注入到生成器里的代码：字符串内的换行须写成字面 \n（两字符），否则生成的 Python 源码
# 会出现「未闭合字符串字面量」——本批第一轮即栽在此处（py_compile 拦下·未落到任何页面）。
RENDER_ADD = RENDER_ANCHOR + (
    '\n    # W888：百回母版插画（仅六回有母版图·插在回目 H1 之后）'
    '\n    plate = CHAPTER_PLATES.get(out_rel.rsplit("/", 1)[-1])'
    '\n    if plate:'
    '\n        plate_html = ('
    '\n            "\\n<figure class=\\"chapter-plate\\" aria-hidden=\\"true\\">"'
    '\n            "\\n<img src=\\"%s../static/images/%s\\" alt=\\"\\" loading=\\"lazy\\" decoding=\\"async\\">"'
    '\n            "\\n</figure>" % (up, plate)'
    '\n        )'
    '\n        m_h1 = re.search(r"</h1>", body_html)'
    '\n        if m_h1:'
    '\n            body_html = body_html[:m_h1.end()] + plate_html + body_html[m_h1.end():]'
)

# 产物页内联副本追加段（build_reader 的 STYLE 块内·缩进 2 空格·与生成器 STYLE 同形态）
# 注释文字须与生成器 STYLE 常量里的**逐字一致**——否则「工作树 vs 生成器输出」的逐字节
# 对拍会在注释行上出差异（本批第一轮即栽在此处·由零漂移探针抓出）。
INLINE_RULE = (
    '  /* W888：百回母版插画（浅底宣纸版·暗色模式下隐藏——浅底图贴深底会成亮斑） */\n'
    '  .chapter-plate { margin: 28px auto 36px; max-width: 420px; }\n'
    '  .chapter-plate img { width: 100%; height: auto; display: block; opacity: .92; }\n'
    '  html[data-theme="dark"] .chapter-plate { display: none; }\n'
)


def read(p: str) -> str:
    with io.open(os.path.normpath(p), encoding="utf-8", newline="") as f:
        return f.read()


def write(p: str, s: str) -> None:
    with io.open(os.path.normpath(p), "w", encoding="utf-8", newline="") as f:
        f.write(s)


def _nl_of(s: str) -> str:
    """文件主行尾（CRLF 文件用 \\r\\n · LF 文件用 \\n）——锚点与补丁须与目标文件同尾。"""
    return "\r\n" if "\r\n" in s else "\n"


def _adapt(text: str, nl: str) -> str:
    """把补丁文本里的真换行换成目标文件的行尾（字面 \\n 两字符不受影响）。"""
    return text.replace("\n", nl) if nl != "\n" else text


def patch_builder(dry: bool) -> int:
    s = read(BUILDER)
    nl = _nl_of(s)
    n = 0
    if "CHAPTER_PLATES" not in s:
        anchor = _adapt(CONST_ANCHOR, nl)
        add = _adapt(CONST_ADD, nl)
        assert anchor in s, 'CONST_ANCHOR 未命中'
        s = s.replace(anchor, add, 1)
        n += 1
    if ".chapter-plate" not in s:
        anchor = _adapt(STYLE_ANCHOR, nl)
        add = _adapt(STYLE_ADD, nl)
        assert anchor in s, 'STYLE_ANCHOR 未命中'
        s = s.replace(anchor, add, 1)
        n += 1
    if "plate = CHAPTER_PLATES.get" not in s:
        anchor = _adapt(RENDER_ANCHOR, nl)
        add = _adapt(RENDER_ADD, nl)
        assert anchor in s, 'RENDER_ANCHOR 未命中'
        s = s.replace(anchor, add, 1)
        n += 1
    if n and not dry:
        write(BUILDER, s)
    print("  生成器 build_reader.py：%d 处改动（行尾 %s）%s"
          % (n, "CRLF" if nl == "\r\n" else "LF", "（dry-run 未写盘）" if dry else ""))
    return n


def inject_page(path: str, img: str, dry: bool) -> str:
    s = read(path)
    if "chapter-plate" in s:
        return "已接·跳过"
    m = re.search(r"</h1>", s)
    if not m:
        return "跳过·无 </h1>"
    fig = ('\n<figure class="chapter-plate" aria-hidden="true">'
           '\n<img src="../static/images/%s" alt="" loading="lazy" decoding="async">'
           '\n</figure>' % img)
    s2 = s[:m.end()] + fig + s[m.end():]
    # 内联副本：补进含 .reader-wrap 的 style 块（= build_reader.py 的 STYLE 块）
    done = False
    for mm in re.finditer(r"(<style[^>]*>)(.*?)(</style>)", s2, re.S):
        if ".reader-wrap" not in mm.group(2):
            continue
        s2 = s2[:mm.start(2)] + mm.group(2).rstrip("\n") + "\n" + INLINE_RULE + s2[mm.end(2):]
        done = True
        break
    if not done:
        return "跳过·未找到 .reader-wrap 样式块"
    if not dry:
        write(path, s2)
    return "接入"


def wire_pages(dry: bool) -> int:
    n = 0
    for name, img in sorted(PLATES.items()):
        p = os.path.join(ROOT, "site", "reader", name)
        if not os.path.exists(p):
            print("  %s：不存在·跳过" % name)
            continue
        r = inject_page(p, img, dry)
        print("  %s：%s" % (name, r))
        if r == "接入":
            n += 1
    print("  回目页母版：%d 页接入" % n)
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    print("[%s] W888 路 B：百回母版插画接回目页" % ("DRY-RUN" if args.dry_run else "APPLY"))
    patch_builder(args.dry_run)
    wire_pages(args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
