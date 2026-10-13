# -*- coding: utf-8 -*-
"""_w694_tagcloud_fix.py — 第六轮外审 P0/P2 修复（一次性）。

tag-cloud.html：16d 条目 13维→16维、V 方向注释 29→30、stat-* 三处死代码移除、
countTags 空转函数移除、四组死样式移除、dataSource 块移至页脚前+skip-link 移至 body 首、
数据源措辞与快照日期据实更新。全部替换带命中断言。
"""
import sys

PATH = r"D:\xiyouji\site\data\tag-cloud.html"

REPLACES = [
    # 1) 16d 条目（title/tags/desc 三处 13维→16维）
    ('{file:"narratology-16d-network.html", title:"13维叙事学网络", category:"v-new", tags:["叙事学","13维","网络","多维"], size:9, desc:"13维叙事学网络"},',
     '{file:"narratology-16d-network.html", title:"16维叙事学网络", category:"v-new", tags:["叙事学","16维","网络","多维"], size:9, desc:"16维叙事学网络"},',
     1),
    # 2) V 方向注释计数
    ("V 方向新增 (29)", "V 方向新增 (30)", 1),
    # 3) stat 死代码两行 + 注释
    ('        // 更新统计\n        d3.select("#stat-shown").text(data.length);\n        d3.select("#stat-total").text(EMBEDDED_DATA.length);\n', "", 1),
    # 4) countTags 空转函数整体
    ('    function countTags() {\n        const tagSet = new Set();\n        EMBEDDED_DATA.forEach(d => d.tags.forEach(t => tagSet.add(t)));\n        d3.select("#stat-tags").text(tagSet.size);\n    }\n\n', "", 1),
    # 5) countTags 调用
    ("        countTags();\n", "", 1),
    # 6-8) 死样式三块
    ("        footer p {\n            margin-bottom: 6px;\n        }\n", "", 1),
    ("        .footer-index {\n            margin-top: 14px;\n            padding-top: 14px;\n            border-top: 1px solid #3a2820;\n            font-size: 0.78rem;\n            color: var(--accent-3);\n        }\n", "", 1),
    ("        .footer-cross {\n            margin-top: 6px;\n            font-size: 0.78rem;\n            color: var(--accent-3);\n        }\n        .footer-cross a {\n            color: #c8a878;\n        }\n", "", 1),
    # 9) 375px 媒体查询里的 tab-row 死行
    ("            .tab-row { overflow-x: auto; -webkit-overflow-scrolling: touch; flex-wrap: nowrap; padding-bottom: 4px; }\n", "", 1),
]


def main():
    raw = open(PATH, "rb").read()
    eol = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8")
    # 统一按 \n 处理再还原（本文件此前被 inline_css 以 LF 写过，探测仅防御）
    if eol == "\r\n":
        work = text.replace("\r\n", "\n")
    else:
        work = text

    for old, new, expect in REPLACES:
        n = work.count(old)
        assert n == expect, "expect %d hit for %r..., got %d" % (expect, old[:50], n)
        work = work.replace(old, new, expect)

    # dataSource 块搬迁（行级操作）
    lines = work.split("\n")
    i_start = next(i for i, l in enumerate(lines) if '<div id="dataSource"' in l)
    i_end = next(i for i in range(i_start, len(lines)) if "</div></div>" in lines[i])
    block = lines[i_start:i_end + 1]
    joined = "\n".join(block)
    assert joined.count("citeBox") == 1 and joined.count("cite-details") == 1
    i_skip = next(i for i, l in enumerate(lines) if 'class="skip-link"' in l)
    i_body = next(i for i, l in enumerate(lines) if l.strip() == "<body>")
    assert i_body < i_start < i_skip
    del lines[i_start:i_end + 1]
    i_skip = next(i for i, l in enumerate(lines) if 'class="skip-link"' in l)
    del lines[i_skip]
    i_footer = next(i for i, l in enumerate(lines) if "site-footer" in l and ("<footer" in l or "<div" in l or "<section" in l))
    # 据实更新措辞与日期后再插入
    block = [l.replace(
        "数据源：页面内嵌 EMBEDDED 数据（run_all 批量生成 JSON 快照于构建时嵌入·快照 2026-10-04）",
        "数据源：页面内嵌 EMBEDDED 数据（页目元数据手工维护·快照 2026-10-10）",
    ).replace("2026-10-04", "2026-10-10") for l in block]
    lines[i_footer:i_footer] = block + [""]
    lines.insert(i_body + 1, '    <a class="skip-link" href="#main">跳到主要内容</a>')

    out = "\n".join(lines)
    if eol == "\r\n":
        out = out.replace("\n", "\r\n")
    open(PATH, "wb").write(out.encode("utf-8"))
    print("OK tag-cloud: %d replaces + dataSource moved + skip-link first" % len(REPLACES))


if __name__ == "__main__":
    sys.exit(main())
