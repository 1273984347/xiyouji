#!/usr/bin/env python3
"""inject_chart_a11y.py — 可视化页 a11y 模块加载器注入器（W701·BL-20·W773 加 --dir）。

对目标目录的 *.html（排除 _shell.html）在 </body> 前注入一行外部脚本加载器：
    <script defer src="{rel}static/js/chart-a11y.js"></script>
模块本体 chart-a11y.js 在运行时为 svg/canvas 图表注入 aria 摘要层与 tabable 焦点
（详见模块头注；W773 起摘要文本按页面 lang 选 zh/en）。外部本地脚本形态与
cite-box.js/chart-audit.js 同款——无内联哈希需求（CSP script-src 'self' 放行），
零页面 CSS/DOM 静态改动。

幂等：已含 chart-a11y.js 引用的页面跳过。--check 只验不写（缺注入器行则 exit 1，
供后续挂门禁候选）。深度感知：相对前缀按目标目录相对 site/ 的深度计算
（site/data → ../·site/en → ../·site/data/json → ../../）。

用法：
  python scripts/inject_chart_a11y.py                  # 注入 site/data（默认·幂等）
  python scripts/inject_chart_a11y.py --dir site/en    # 注入英文站（W773·T-02 缺陷③）
  python scripts/inject_chart_a11y.py --check --dir site/en  # 只验不写
"""
import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, ".."))
SITE_DIR = os.path.join(ROOT, "site")
SKIP = {"_shell.html"}
LOADER = '<script defer src="{rel}static/js/chart-a11y.js"></script>'


def rel_prefix(data_dir: str) -> str:
    """目标目录相对 site/ 的深度 → static/ 的前缀。

    site/data → "../"·site/en → "../"·site/data/json → "../../"·site 本身 → ""。
    """
    rel = os.path.relpath(data_dir, SITE_DIR)
    depth = 0 if rel == "." else len(rel.replace("\\", "/").split("/"))
    return "../" * depth


def target_pages(data_dir: str) -> list:
    return sorted(
        fn for fn in os.listdir(data_dir)
        if fn.endswith(".html") and fn not in SKIP
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="可视化页 chart-a11y 加载器注入器")
    parser.add_argument("--dir", default="site/data",
                        help="目标目录（repo 相对或绝对·默认 site/data）")
    parser.add_argument("--check", action="store_true",
                        help="只验不写（缺注入器行 exit 1）")
    args = parser.parse_args()

    data_dir = args.dir if os.path.isabs(args.dir) else os.path.join(ROOT, args.dir)
    if not os.path.isdir(data_dir):
        print("[ERROR] 目标目录不存在: %s" % data_dir)
        return 2
    rel = rel_prefix(data_dir)

    pages = target_pages(data_dir)
    injected, already, missing = 0, 0, []
    for fn in pages:
        p = os.path.join(data_dir, fn)
        with open(p, encoding="utf-8", newline="") as f:
            t = f.read()
        if "chart-a11y.js" in t:
            already += 1
            continue
        if "</body>" not in t:
            missing.append(fn + "（无 </body>）")
            continue
        if args.check:
            missing.append(fn)
            continue
        t2 = t.replace("</body>", LOADER.format(rel=rel) + "\n</body>", 1)
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(t2)
        injected += 1

    print("扫描 %d 页：已注入 %d · 本次注入 %d · 异常 %d"
          % (len(pages), already, injected, len(missing)))
    if missing:
        if args.check:
            print("缺注入器行 %d 页（--check）：%s" % (len(missing), ", ".join(missing[:8])))
        else:
            print("无 </body> 异常页：%s" % ", ".join(missing[:8]))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
