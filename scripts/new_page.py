#!/usr/bin/env python3
"""new_page.py — 可视化页面脚手架

用途：
    基于 site/_template.html 生成新页面骨架，自动替换占位符（标题/描述/分类/文件名），
    并在 site/index.html 导航中追加链接条目（可选）。

使用方式：
    # 创建新页面
    python scripts/new_page.py --name power-resources --title "三界权力资源" --category "J_权力与资源" --desc "三界权力结构 + 长生资源链"
    # 仅创建页面，不修改 index.html
    python scripts/new_page.py --name foo --title "Foo" --category "Z_图表设计" --desc "..." --no-index

设计要点：
    - 模板源：site/_template.html（含 tokens.css + d3.v7.min.js + EMBEDDED_DATA fallback 框架）
    - 输出路径：site/data/<name>.html
    - 占位符替换：【占位】页面标题 / 【占位】分类 / 【占位】子分类 / 【占位】页面标题一句话描述 / 【占位】一句话描述本页面内容
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "site" / "_template.html"
OUTPUT_DIR = ROOT / "site" / "data"
INDEX = ROOT / "site" / "index.html"


def render_template(name: str, title: str, category: str, desc: str) -> str:
    """读取模板并替换占位符。

    模板 _template.html 的占位符约定：
      - <title>页面标题 · 详解西游记</title>            -> <title>{title} · 详解西游记</title>
      - <h1>页面主标题</h1>                            -> <h1>{title}</h1>
      - <div class="subtitle">副标题 / SECTION NAME</div> -> <div class="subtitle">{category}</div>
      - <div class="tagline">一句话点题，斜体浅色</div>  -> <div class="tagline">{desc}</div>
      - 面包屑 <span class="current">当前页面</span>    -> <span class="current">{title}</span>
    """
    if not TEMPLATE.exists():
        sys.exit(f"[ERROR] 模板文件不存在: {TEMPLATE}")
    text = TEMPLATE.read_text(encoding="utf-8")

    # <title>
    text = text.replace("页面标题 · 详解西游记", f"{title} · 详解西游记")
    # hero h1
    text = text.replace("<h1>页面主标题</h1>", f"<h1>{title}</h1>")
    # subtitle（副标题改为分类名）
    text = text.replace("副标题 / SECTION NAME", category)
    # tagline
    text = text.replace("一句话点题，斜体浅色", desc)
    # breadcrumb current
    text = text.replace('<span class="current">当前页面</span>', f'<span class="current">{title}</span>')
    return text


def append_to_index(name: str, title: str, category: str) -> list[str]:
    """在 site/index.html 中追加新页面链接条目。

    策略：寻找 `<!-- A-AH 数据可视化 -->` 注释下方最近的 <ul> 块，
    按 category 分组在末尾追加 <li> 条目。
    若找不到锚点，则附加到 index.html 末尾并打印警告。
    返回追加的行（用于回滚或 dry-run 展示）。
    """
    if not INDEX.exists():
        print(f"[WARN] site/index.html 不存在，跳过索引追加")
        return []
    text = INDEX.read_text(encoding="utf-8")

    # 简单策略：在 <!-- A-AH 数据可视化 --> 注释后找第一个 </ul>，在 </ul> 前插入
    anchor = "<!-- A-AH 数据可视化"
    idx = text.find(anchor)
    if idx < 0:
        print(f"[WARN] index.html 中未找到锚点 '{anchor}'，跳过索引追加")
        return []

    end_ul = text.find("</ul>", idx)
    if end_ul < 0:
        print(f"[WARN] index.html 中未找到 </ul>，跳过索引追加")
        return []

    new_line = f'  <li><a href="data/{name}.html">{title}（{category}）</a></li>\n'
    new_text = text[:end_ul] + new_line + text[end_ul:]
    INDEX.write_text(new_text, encoding="utf-8")
    return [new_line.strip()]


def main():
    parser = argparse.ArgumentParser(description="可视化页面脚手架")
    parser.add_argument("--name", required=True, help="页面文件名（不含 .html，如 power-resources）")
    parser.add_argument("--title", required=True, help="页面标题（如 三界权力资源）")
    parser.add_argument("--category", required=True, help="所属分类（如 J_权力与资源）")
    parser.add_argument("--desc", default="", help="一句话描述本页面内容")
    parser.add_argument("--no-index", action="store_true", help="不修改 site/index.html 导航")
    parser.add_argument("--dry-run", action="store_true", help="仅打印将生成的文件内容，不写入")
    args = parser.parse_args()

    # 校验 name 仅含 a-z 0-9 -
    if not re.fullmatch(r"[a-z0-9-]+", args.name):
        sys.exit(f"[ERROR] --name 只能包含小写字母/数字/连字符：{args.name}")

    desc = args.desc or args.title
    content = render_template(args.name, args.title, args.category, desc)
    out_path = OUTPUT_DIR / f"{args.name}.html"

    if args.dry_run:
        print(f"==> [DRY-RUN] 将写入：{out_path}")
        print("--- 内容预览（前 30 行）---")
        for line in content.splitlines()[:30]:
            print(line)
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"[OK] 页面已创建：{out_path}")

    if not args.no_index:
        added = append_to_index(args.name, args.title, args.category)
        for line in added:
            print(f"[OK] 已追加到 index.html: {line}")


if __name__ == "__main__":
    main()
