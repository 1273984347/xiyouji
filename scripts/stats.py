#!/usr/bin/env python3
"""聚合数字统计器 stats（W703）——从磁盘实算生成 scripts/output/stats.json（tracked）。

第 31 门禁 C5（check_doc_sync.py 聚合数字对账）的基准真值：治理文档现役叙述面中的
高危聚合句式（页数/篇数/门禁数/类数等）一律与本文件产物对账，不一致 = FAIL。
口径与 CHANGELOG 头部「全站页数口径」块一致；改口径的批次须同批重跑本脚本并
刷新受影响文档（与双源重灌同纪律）。

用法：python scripts/stats.py           # 生成/刷新 stats.json 并打印摘要
      python scripts/stats.py --check   # 与磁盘现存 stats.json 对比（应零差异·自证）
"""

import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "output", "stats.json")

CONTENT_DIRS = ["01-全书逐回解读", "02-人物深度分析", "03-主题与情节专题", "04-文化与历史背景", "05-诗词歌赋", "06-个人随笔"]
INLINED_MARK = "(tokens.css + system.css)"  # inline_css.py 注入的标记行特征


def build():
    site = os.path.join(ROOT, "site")
    htmls = glob.glob(os.path.join(site, "**", "*.html"), recursive=True)
    data_htmls = glob.glob(os.path.join(site, "data", "*.html"))
    template_n = sum(1 for p in htmls if os.path.basename(p) == "_template.html")
    shell_n = sum(1 for p in htmls if os.path.basename(p) == "_shell.html")

    inlined = 0
    for p in htmls:
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                if INLINED_MARK in f.read():
                    inlined += 1
        except OSError:
            continue

    with open(os.path.join(HERE, "verify_delivery.py"), encoding="utf-8") as f:
        gate_max = max(int(x) for x in re.findall(r"第\s*(\d+)\s*(?:槽|门禁)", f.read()))

    a1_a6 = sum(
        len([p for p in glob.glob(os.path.join(ROOT, "docs", d, "*.md")) if not os.path.basename(p).startswith("README")])
        for d in CONTENT_DIRS
    )  # 口径对齐 verify 第 3 门禁：板块顶层内容 .md（排除各板块 README.md·615=621-6）
    methodology = len(glob.glob(os.path.join(ROOT, "docs", "10-方法论沉淀", "*.md")))
    json_n = len(glob.glob(os.path.join(HERE, "output", "data", "*.json")))
    classes = sorted(
        d for d in os.listdir(HERE) if os.path.isdir(os.path.join(HERE, d)) and d[:1].isalpha() and d[:1].isupper()
    )

    return {
        "html_total": len(htmls),
        "site_data_html": len(data_htmls),
        "site_en_html": len(glob.glob(os.path.join(site, "en", "*.html"))),
        "site_root_html": len(glob.glob(os.path.join(site, "*.html"))),
        "site_reader_html": len(glob.glob(os.path.join(site, "reader", "**", "*.html"), recursive=True)),
        "visualization_pages": len(data_htmls) - shell_n,
        "csp_covered": len(htmls) - template_n,
        "scan_files": len(htmls) - template_n - shell_n,
        "seo_scanned": len(htmls) - template_n - shell_n,
        "inline_css_pages": inlined,
        "gate_count": gate_max,
        "a1_a6_docs": a1_a6,
        "methodology_docs": methodology,
        "json_count": json_n,
        "script_classes": len(classes),
    }


def main():
    stats = build()
    if "--check" in sys.argv:
        if not os.path.exists(OUT):
            print("FAIL  stats.json 不存在——先跑 python scripts/stats.py")
            return 1
        with open(OUT, encoding="utf-8") as f:
            old = json.load(f)
        diffs = {k: (old.get(k), v) for k, v in stats.items() if old.get(k) != v}
        if diffs:
            for k, (o, n) in sorted(diffs.items()):
                print("DRIFT %s: stats.json=%s 磁盘实算=%s" % (k, o, n))
            print("FAIL  %d 键漂移——重跑 python scripts/stats.py 刷新" % len(diffs))
            return 1
        print("OK    stats.json 与磁盘实算零差异（%d 键）" % len(stats))
        return 0
    stats["_generated"] = __import__("datetime").date.today().isoformat()
    stats["_generator"] = "scripts/stats.py（W703·第 31 门禁 C5 对账基准·改口径批次须同批刷新）"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    for k in sorted(k for k in stats if not k.startswith("_")):
        print("%s = %s" % (k, stats[k]))
    print("OK    -> %s" % os.path.relpath(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
