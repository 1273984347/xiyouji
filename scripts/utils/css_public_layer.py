"""公共层文本解析（同源共用·W1280 立）。

公共层（site/tokens.css + site/system.css）外链化后，页面内的静态契约声明
（第 53 槽的 chart-tooltip、第 64 槽 A8 的窄屏适配特征等）由**公共层提供**，
页内文本不再含这些声明 ⇒ 判据若只看页内文本，会把「加载形态变更」误判成「契约丢失」。

本模块提供统一入口 `public_layer_text(page_html, page_dir)`：该页若以 <link> 引用公共层，
则返回被引用公共层文件的文本（供判据把公共层并入判定面）；未引用则返回空串
（内联形态下判定面保持不变·口径不漂移）。

路径口径：<link href> 是**相对页所在目录**的（EN 页在 site/en/ ⇒ "../tokens.css"），
故按 page_dir 解析。

同源纪律：判据侧共用本模块，禁各自再抄一份（抄一次必漂移·E-280/E-281 教训）。
"""
from __future__ import annotations

import os
import re

PUBLIC_NAMES = ("tokens.css", "system.css")
_RE_LINK = re.compile(r"<link[^>]+href=[\"\']([^\"\']+)[\"\']", re.I)


def referenced_public_files(page_html: str, page_dir: str) -> list[str]:
    """该页引用的公共层文件绝对路径列表（按引用顺序·去重·仅存在的）。"""
    out: list[str] = []
    for href in _RE_LINK.findall(page_html or ""):
        name = os.path.basename(href)
        if name not in PUBLIC_NAMES:
            continue
        path = os.path.normpath(os.path.join(page_dir, href))
        if path not in out and os.path.exists(path):
            out.append(path)
    return out


def public_layer_text(page_html: str, page_dir: str) -> str:
    """该页引用的公共层文本（未引用公共层则返回空串）。"""
    parts = []
    for path in referenced_public_files(page_html, page_dir):
        with open(path, encoding="utf-8", errors="replace") as fh:
            parts.append(fh.read())
    return "\n".join(parts)
