#!/usr/bin/env python3
"""inject_chart_a11y.py — 可视化页 a11y 模块加载器注入器（W701·BL-20）。

对 site/data/*.html（排除 _shell.html）在 </body> 前注入一行外部脚本加载器：
    <script defer src="../static/js/chart-a11y.js"></script>
模块本体 chart-a11y.js 在运行时为 svg/canvas 图表注入 aria 摘要层与 tabable 焦点
（详见模块头注）。外部本地脚本形态与 cite-box.js/chart-audit.js 同款——无内联
哈希需求（CSP script-src 'self' 放行），零页面 CSS/DOM 静态改动。

幂等：已含 chart-a11y.js 引用的页面跳过。--check 只验不写（缺注入器行则 exit 1，
供后续挂门禁候选）。深度感知：site/data → ../static。

用法：
  python scripts/inject_chart_a11y.py            # 注入（幂等）
  python scripts/inject_chart_a11y.py --check    # 只验不写
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, ".."))
DATA_DIR = os.path.join(ROOT, "site", "data")
SKIP = {"_shell.html"}
LOADER = '<script defer src="{rel}static/js/chart-a11y.js"></script>'
REL = "../"


def target_pages():
    return sorted(
        fn for fn in os.listdir(DATA_DIR)
        if fn.endswith(".html") and fn not in SKIP
    )


def main():
    check_only = "--check" in sys.argv
    pages = target_pages()
    injected, already, missing = 0, 0, []
    for fn in pages:
        p = os.path.join(DATA_DIR, fn)
        with open(p, encoding="utf-8", newline="") as f:
            t = f.read()
        if "chart-a11y.js" in t:
            already += 1
            continue
        if "</body>" not in t:
            missing.append(fn + "（无 </body>）")
            continue
        if check_only:
            missing.append(fn)
            continue
        t2 = t.replace("</body>", LOADER.format(rel=REL) + "\n</body>", 1)
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(t2)
        injected += 1

    print("扫描 %d 页：已注入 %d · 本次注入 %d · 异常 %d"
          % (len(pages), already, injected, len(missing)))
    if missing:
        if check_only:
            print("缺注入器行 %d 页（--check）：%s" % (len(missing), ", ".join(missing[:8])))
        else:
            print("无 </body> 异常页：%s" % ", ".join(missing[:8]))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
