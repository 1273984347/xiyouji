#!/usr/bin/env python3
"""gen_rss.py — 生成 site/rss.xml（B-1·W644）。

数据源：CHANGELOG.md 现役版段（### vX.Y.Z（日期）：WNNN 标题）取最近 20 条。
幂等：全量重写 site/rss.xml；链接指向仓库 CHANGELOG（GitHub 锚点含中文不稳定·统一指向文件）。

用法：python scripts/gen_rss.py
"""
import datetime
import email.utils
import os
import re
import sys
import xml.sax.saxutils as sx

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://1273984347.github.io/xiyouji/"
CHANGELOG_URL = "https://github.com/1273984347/xiyouji/blob/main/CHANGELOG.md"
N_ITEMS = 20


def main():
    s = open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8").read()
    items = re.findall(r"^### (v[\d.]+)（(\d{4}-\d{2}-\d{2})）：(W\d+[^\n]*)$", s, re.M)[:N_ITEMS]
    assert items, "CHANGELOG 现役版段解析为空"

    rows = []
    for ver, date, title in items:
        # RFC 822 pubDate（日期零点·UTC 标注不影响日粒度订阅语义）
        pd = email.utils.format_datetime(datetime.datetime.fromisoformat(date + "T00:00:00+00:00"))
        rows.append(
            "    <item>\n"
            f"      <title>{sx.escape(ver + ' ' + title.strip())}</title>\n"
            f"      <link>{CHANGELOG_URL}</link>\n"
            f"      <guid isPermaLink=\"false\">xiyouji-{ver}</guid>\n"
            f"      <pubDate>{pd}</pubDate>\n"
            f"      <description>{sx.escape('详见 CHANGELOG 对应版段（四件套：来源/文件/验证/状态）。')}</description>\n"
            "    </item>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0">\n'
        "  <channel>\n"
        "    <title>详解西游记 · 更新动态</title>\n"
        f"    <link>{BASE}</link>\n"
        "    <description>一源多形 · 数字人文可视化解读《西游记》100 回——版本发布批次动态（W### 编号·详见 CHANGELOG）。</description>\n"
        "    <language>zh-CN</language>\n"
        + "\n".join(rows)
        + "\n  </channel>\n</rss>\n"
    )
    dst = os.path.join(ROOT, "site", "rss.xml")
    open(dst, "w", encoding="utf-8", newline="\n").write(xml)
    print(f"[OK] site/rss.xml 写入 {len(items)} 条（{items[0][0]} → {items[-1][0]}）")


if __name__ == "__main__":
    main()
