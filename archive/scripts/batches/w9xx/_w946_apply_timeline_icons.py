#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W946 · timeline 专属图标接入（数据字段 emoji → 图标名 + 渲染改内联 SVG）

按**事件语义**逐条映射（emoji 一符多义：📖 同时表示佛经西行与连环画、🎭 三义），
故不可按字符替换，须以「事件标题 + emoji」为键精确替换。
用法：py -3 scripts/_w946_apply_timeline_icons.py [--dry]
"""
from __future__ import annotations

import argparse
import pathlib
import re

# (事件标题, 原 emoji) → 专属图标名
MAP = [
    ("玄奘西行", "📖", "tl-pilgrim"),
    ("大唐西域记", "📜", "tl-scroll"),
    ("取经诗话", "✨", "tl-star-spark"),
    ("杂剧西游记", "🎭", "tl-mask"),
    ("世德堂本定稿", "📕", "tl-codex"),
    ("西游证道书", "☯️", "tl-taiji"),
    ("现代整理本", "📚", "tl-critical-edition"),
    ("世德堂百回本", "📕", "tl-codex"),
    ("证道书本", "☯️", "tl-taiji"),
    ("西游真诠", "✒️", "tl-brush-comment"),
    ("亚东排印本", "📰", "tl-punctuation"),
    ("人文社整理本", "📚", "tl-critical-edition"),
    ("新校注本", "✏️", "tl-pencil"),
    ("数字化版本", "💾", "tl-database"),
    ("明代戏曲改编", "🎭", "tl-mask"),
    ("清代年画", "🖼️", "tl-newyear-print"),
    ("连环画普及", "📖", "tl-comic"),
    ("铁扇公主动画", "🎬", "tl-film"),
    ("央视西游记", "📺", "tl-tv"),
    ("大话西游", "🎭", "tl-mask"),
    ("西游降魔篇", "🎬", "tl-film"),
    ("游戏与网文", "🎮", "tl-gamepad"),
]
# 英文站事件标题 → 同一映射（按 emoji + 出现顺序对齐，避免逐条维护英文标题）
EN_MAP = [
    ("Xuanzang’s Westward Journey", "📖", "tl-pilgrim"),
    ("Great Tang Records on the Western Regions", "📜", "tl-scroll"),
    ("Early Poetic Narrative", "✨", "tl-star-spark"),
    ("Ming-Era Opera Adaptations", "🎭", "tl-mask"),
    ("Final Form of the Hundred-Chapter Novel", "📕", "tl-codex"),
    ("Alchemical Commentary", "☯️", "tl-taiji"),
    ("Modern Collated Edition", "📚", "tl-critical-edition"),
    ("Alchemical Commentary (Shidao)", "☯️", "tl-taiji"),
    ("True Interpretation", "✒️", "tl-brush-comment"),
    ("Modern Punctuation Edition", "📰", "tl-punctuation"),
    ("People’s Literature Collated Edition", "📚", "tl-critical-edition"),
    ("New Annotated Edition", "✏️", "tl-pencil"),
    ("Digital Edition", "💾", "tl-database"),
    ("Qing New Year Prints", "🖼️", "tl-newyear-print"),
    ("Popularization of Lianhuanhua Comics", "📖", "tl-comic"),
    ("Princess Iron Fan (Animation)", "🎬", "tl-film"),
    ("A Dream of Red Mansions", "📺", "tl-tv"),
]

FILES = [
    ("site/data/timeline.html", "zh"),
    ("site/en/timeline.html", "en"),
]

# 事件 → 专属图标的**顺序表**（两页数据同序·按序对应·不依赖标题文本）
ORDER = [
    "tl-pilgrim",        # 玄奘西行 / Xuanzang's Westward Journey（📖 佛经义）
    "tl-scroll",         # 大唐西域记（📜）
    "tl-star-spark",     # 取经诗话（✨）
    "tl-mask",           # 杂剧西游记（🎭）
    "tl-codex",          # 世德堂本定稿（📕）
    "tl-taiji",          # 西游证道书（☯️）
    "tl-critical-edition",  # 现代整理本（📚）
    "tl-codex",          # 世德堂百回本（📕）
    "tl-taiji",          # 证道书本（☯️）
    "tl-brush-comment",  # 西游真诠（✒️）
    "tl-punctuation",    # 亚东排印本（📰）
    "tl-critical-edition",  # 人文社整理本（📚）
    "tl-pencil",         # 新校注本（✏️）
    "tl-database",       # 数字化版本（💾）
    "tl-mask",           # 明代戏曲改编（🎭）
    "tl-newyear-print",  # 清代年画（🖼️）
    "tl-comic",          # 连环画普及（📖 连环画义）
    "tl-film",           # 铁扇公主动画（🎬）
    "tl-tv",             # 央视西游记（📺）
    "tl-mask",           # 大话西游（🎭）
    "tl-film",           # 西游降魔篇（🎬）
    "tl-gamepad",        # 游戏与网文（🎮）
]

ICO_JS = pathlib.Path("scripts/output/_w946_timeline_icons.js")
ICON_RE = re.compile(r"icon: '([^']*)'")


def apply(path: str, dry: bool) -> tuple[int, list[str]]:
    p = pathlib.Path(path)
    t = p.read_text(encoding="utf-8")
    orig = t
    seq = [m.group(1) for m in ICON_RE.finditer(t)]
    if len(seq) != len(ORDER):
        print(f"  [ABORT] {path}: 数据行 {len(seq)} ≠ 顺序表 {len(ORDER)}")
        return 0, seq
    it = iter(ORDER)
    t = ICON_RE.sub(lambda m: f"icon: '{next(it)}'", t)
    # 渲染：.text(d => d.icon) → .html(d => TL_ICO[d.icon] || '')
    # ⚠️ 必须保留 D3 回调箭头：写成 .html(TL_ICO[d.icon] || '') 会让 d 落到外层作用域 ⇒ pageerror
    t = t.replace("head.append('div').attr('class', 'ec-icon').text(d => d.icon);",
                  "head.append('div').attr('class', 'ec-icon').html(d => TL_ICO[d.icon] || '');")
    t = t.replace("body.append('div').attr('class', 'detail-icon').text(d.icon);",
                  "body.append('div').attr('class', 'detail-icon').html(TL_ICO[d.icon] || '');")
    # 插入 TL_ICO 映射：必须放在**使用它的那段脚本内、且在使用点之前**
    # （W946 实测：插到页面最后一个 </script> 前会落到使用点之后 ⇒ TL_ICO is not defined）
    if "var TL_ICO" not in t:
        ico = ICO_JS.read_text(encoding="utf-8")
        use = t.find(".html(TL_ICO[d.icon]")
        if use == -1:
            print(f"  [ABORT] {path}: 未找到 TL_ICO 使用点")
            return 0, seq
        # 回溯到该使用点所在 <script> 的开头，在其后插入
        s_open = t.rfind("<script", 0, use)
        s_open_end = t.find(">", s_open) + 1
        t = t[:s_open_end] + "\n" + ico + t[s_open_end:]
    if not dry and t != orig:
        p.write_text(t, encoding="utf-8")
    return len(seq), seq


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    seqs = {}
    for path, _lang in FILES:
        n, seq = apply(path, args.dry)
        seqs[path] = seq
        print(f"{path}: 替换 {n} 条数据行")
    a, b = (seqs.get(FILES[0][0], []), seqs.get(FILES[1][0], []))
    same = a == b
    print(f"\n两页 emoji 序列一致: {same}")
    if not same:
        print("  zh:", a)
        print("  en:", b)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
