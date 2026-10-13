"""W676 WP-4.2① monster-ecology-network 手搓桑基 → d3.sankey()（ZH+EN）。

旧实现 yPositions[i]/3 公式错乱致相邻节点重叠；新实现走 d3-sankey 插件
（site/static/js/d3-sankey.min.js，本批同步补 script 引用）。
锚点截取：start = "(function renderSankey() {"，end = 头注文本 append 行（保留）。
"""

NEW_BLOCK = """
        const svg = d3.select("#sankey-svg");
        const width = svg.node().clientWidth;
        const height = 420;
        const data = EMBEDDED_DATA.sankey;
        const colors = ["#6B8E5A", "#C9A063", "#c8463a", "#3a6b8c", "#23201A"];

        const nodes = data.nodes.map((n, i) => Object.assign({}, n, { __i: i, __color: colors[i % colors.length] }));
        const links = data.links.map(l => Object.assign({}, l));

        const sankeyGen = d3.sankey()
            .nodeId(d => d.__i)
            .nodeWidth(24)
            .nodePadding(24)
            .extent([[40, 50], [width - 40, height - 30]]);
        const graph = sankeyGen({ nodes: nodes, links: links });

        svg.append("g").selectAll("path")
            .data(graph.links)
            .join("path")
            .attr("d", d3.sankeyLinkHorizontal())
            .attr("fill", "none")
            .attr("stroke", l => l.source.__color)
            .attr("stroke-width", l => Math.max(1, l.width))
            .attr("opacity", 0.55)
            .append("title").text(l => (l.source.name || "") + " -> " + (l.target.name || "") + ": " + l.value + "%");

        svg.append("g").selectAll("text")
            .data(graph.links)
            .join("text")
            .attr("x", l => (l.source.x1 + l.target.x0) / 2)
            .attr("y", l => (l.y0 + l.y1) / 2 - 6)
            .attr("text-anchor", "middle").attr("font-size", "10px").style("fill", "var(--ink-soft)")
            .text(l => l.value + "%");

        svg.append("g").selectAll("rect")
            .data(graph.nodes)
            .join("rect")
            .attr("x", d => d.x0).attr("y", d => d.y0)
            .attr("width", d => d.x1 - d.x0).attr("height", d => d.y1 - d.y0)
            .attr("fill", d => d.__color).attr("opacity", 0.85).attr("rx", 4)
            .append("title").text(d => d.name + "(" + d.value + ")");

        svg.append("g").selectAll("text")
            .data(graph.nodes)
            .join("text")
            .attr("x", d => (d.x0 + d.x1) / 2)
            .attr("y", d => d.y0 + (d.y1 - d.y0) / 2 + 4)
            .attr("text-anchor", "middle")
            .attr("fill", d => d.__color === "#C9A063" ? "#23201A" : "#fff").attr("font-size", "11px")
            .text(d => d.name);

"""

START = "(function renderSankey() {"
END = 'svg.append("text").attr("x", width/2).attr("y", 30)'
SCRIPT_TAG = '<script src="../static/js/d3.v7.min.js"></script>'


def main():
    for path in ("site/data/monster-ecology-network.html",
                 "site/en/monster-ecology-network.html"):
        with open(path, encoding="utf-8", newline="") as fh:
            text = fh.read()
        nl = "\r\n" if "\r\n" in text else "\n"
        i = text.find(START)
        j = text.find(END, i if i >= 0 else 0)
        assert i >= 0 and j > i, "锚点失配: %s (i=%d j=%d)" % (path, i, j)
        # 行首缩进对齐 END 行
        line_start = text.rfind("\n", 0, j) + 1
        indent = text[line_start:j]
        block = NEW_BLOCK.replace("\n", nl)
        new_text = text[:i + len(START)] + block + indent + text[j:]
        # d3-sankey 插件引用（紧随 d3.v7 之后）
        assert new_text.count(SCRIPT_TAG) == 1, path + " d3.v7 引用数异常"
        new_text = new_text.replace(
            SCRIPT_TAG,
            SCRIPT_TAG + nl + '<script src="../static/js/d3-sankey.min.js"></script>')
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(new_text)
        print(path, "OK yPositions 残留=%d d3.sankey=%d" % (
            new_text.count("yPositions"), new_text.count("d3.sankey()")))
    print("OK")


if __name__ == "__main__":
    main()
