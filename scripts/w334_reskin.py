#!/usr/bin/env python3
"""w334_reskin.py — W334 新中式·数字雅集 全站批量换肤

对 site/data/*.html + site/en/*.html + site/mobile-index.html + site/dukou-engine.html
执行三项机械改造（幂等，重复运行自动跳过）：

1. tokens.css 链接归位：确保 <link rel="stylesheet" href="...tokens.css"> 位于
   最后一个 </style> 之后、</head> 之前，使 tokens.css 的变量与覆写层
   （字体分层/hero 玄墨化）在级联中胜出。已存在的旧位置链接会被移动。
2. D3/JS 硬编码色值映射到新雅集色板：
     #7a5230 → #C9A063（赭褐 → 赭金）
     #5a7a3a → #6B8E5A（苔绿旧 → 苔绿新）
     #2c2418 → #23201A（墨褐 → 墨）
     #6b5e4d → #6B6455（浅墨褐 → 浅墨）
   （#c8463a / #3a6b8c / #e9b885 保持不变）
3. 写入 W334-RESKIN 标记注释，保证幂等。

不改动：页面结构、EMBEDDED_DATA、图表逻辑、a11y 属性。
site/index.html / dashboard.html / _template.html 已手工重写，不在本脚本范围。

用法：
    python scripts/w334_reskin.py --dry-run   # 预览
    python scripts/w334_reskin.py             # 执行
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "<!-- W334-RESKIN -->"

HEX_MAP = [
    (re.compile(r"#7a5230", re.IGNORECASE), "#C9A063"),
    (re.compile(r"#5a7a3a", re.IGNORECASE), "#6B8E5A"),
    (re.compile(r"#2c2418", re.IGNORECASE), "#23201A"),
    (re.compile(r"#6b5e4d", re.IGNORECASE), "#6B6455"),
]

LINK_RE = re.compile(r'<link\s+rel="stylesheet"\s+href="[^"]*tokens\.css"\s*/?>', re.IGNORECASE)


def target_files() -> list[Path]:
    files = sorted((ROOT / "site" / "data").glob("*.html"))
    en_dir = ROOT / "site" / "en"
    if en_dir.exists():
        files += sorted(en_dir.glob("*.html"))
    for extra in ["mobile-index.html", "dukou-engine.html"]:
        p = ROOT / "site" / extra
        if p.exists():
            files.append(p)
    return files


def tokens_href(path: Path) -> str:
    """data/ 与 en/ 子目录页面用 ../tokens.css，site/ 根页面用 tokens.css。"""
    return "tokens.css" if path.parent == ROOT / "site" else "../tokens.css"


def reskin(path: Path, dry_run: bool) -> tuple[str, int, bool]:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return ("skip(marked)", 0, False)

    # 1) tokens.css 链接归位：移除旧链接（如有），在 </head> 前重新插入
    had_link = bool(LINK_RE.search(text))
    text = LINK_RE.sub("", text)
    link_tag = f'<link rel="stylesheet" href="{tokens_href(path)}">\n{MARKER}\n</head>'
    if "</head>" not in text:
        return ("skip(no </head>)", 0, False)
    text = text.replace("</head>", link_tag, 1)

    # 2) JS/CSS 硬编码色值映射
    swaps = 0
    for pattern, repl in HEX_MAP:
        text, n = pattern.subn(repl, text)
        swaps += n

    if not dry_run:
        path.write_text(text, encoding="utf-8")
    action = "reskin" + ("(link-moved)" if had_link else "(link-added)")
    return (action, swaps, True)


def main() -> None:
    parser = argparse.ArgumentParser(description="W334 全站批量换肤")
    parser.add_argument("--dry-run", action="store_true", help="只打印不写入")
    args = parser.parse_args()

    files = target_files()
    print(f"[INFO] 目标文件 {len(files)} 个")
    done = skipped = 0
    for f in files:
        action, swaps, changed = reskin(f, args.dry_run)
        if changed:
            done += 1
            print(f"  [OK] {f.relative_to(ROOT)}  {action}  hex×{swaps}")
        else:
            skipped += 1
            print(f"  [--] {f.relative_to(ROOT)}  {action}")
    print(f"[DONE] 处理 {done} / 跳过 {skipped} / 共 {len(files)}" + ("（dry-run 未写入）" if args.dry_run else ""))


if __name__ == "__main__":
    main()
