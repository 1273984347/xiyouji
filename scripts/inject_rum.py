#!/usr/bin/env python3
"""
W390 · P0 埋点注入脚本

遍历 site/ 下所有 *.html，按文件相对站点根目录的深度，
幂等地注入一行 <script defer src=".../js/rum.js"></script> 到 </head> 前。

路径计算使用 os.path.relpath，天然适配：
  - 站点根页 (site/index.html)        -> js/rum.js
  - 一级子目录 (site/data/x.html)     -> ../js/rum.js
  - 更深目录 (site/chapters/a/b.html) -> ../../js/rum.js

幂等：若已包含 "rum.js" 字样则跳过，可重复运行不重复注入。

用法:
  python scripts/inject_rum.py            # 注入
  python scripts/inject_rum.py --check     # 仅报告哪些文件缺 rum.js，不写入
"""

import os
import sys

SITE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
RUM_RELPATH_FROM_SITE = os.path.join("js", "rum.js")
MARKER = "rum.js"


def compute_rel_src(html_path):
    """返回从 html 所在目录到 js/rum.js 的相对路径（POSIX 分隔符）。"""
    rum_abs = os.path.join(SITE_DIR, RUM_RELPATH_FROM_SITE)
    rel = os.path.relpath(rum_abs, os.path.dirname(html_path))
    return rel.replace(os.sep, "/")


def inject(html_path, check_only=False):
    with open(html_path, encoding="utf-8") as f:
        content = f.read()

    if MARKER in content:
        return "skip"  # 已注入，幂等跳过

    rel_src = compute_rel_src(html_path)
    tag = '  <script defer src="%s"></script>\n' % rel_src

    # 优先注入到 </head> 前；无 head 则退到 </body> 前；都没有则跳过
    if "</head>" in content or "</HEAD>" in content:
        anchor = "</head>" if "</head>" in content else "</HEAD>"
        new_content = content.replace(anchor, tag + anchor, 1)
    elif "</body>" in content or "</BODY>" in content:
        anchor = "</body>" if "</body>" in content else "</BODY>"
        new_content = content.replace(anchor, tag + anchor, 1)
    else:
        return "no-anchor"

    if check_only:
        return "would-inject"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return "injected"


def main():
    check_only = "--check" in sys.argv
    html_files = []
    for root, _dirs, files in os.walk(SITE_DIR):
        for fn in files:
            if fn.endswith(".html"):
                html_files.append(os.path.join(root, fn))
    html_files.sort()

    stats = {"injected": 0, "skip": 0, "no-anchor": 0, "would-inject": 0}
    for hp in html_files:
        rel = os.path.relpath(hp, SITE_DIR)
        result = inject(hp, check_only=check_only)
        stats[result] = stats.get(result, 0) + 1
        if result in ("injected", "would-inject", "no-anchor"):
            print("[%s] %s" % (result, rel))

    print("\n=== 统计 ===")
    print("  扫描文件数: %d" % len(html_files))
    print("  注入/待注入: %d" % (stats["injected"] + stats["would-inject"]))
    print("  已跳过(幂等): %d" % stats["skip"])
    print("  无锚点(跳过): %d" % stats["no-anchor"])
    if check_only:
        print("(check-only 模式，未写入任何文件)")


if __name__ == "__main__":
    main()
