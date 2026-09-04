import os
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2 试点：poetry-rhythm-analysis.html 的 7 类饼图 → 矩形树图(treemap)。
替换 renderPie 绘制逻辑（从 '板块 2' 注释到 '板块 3' 注释之前），保留 #pie-svg/#pie-legend/#pie-tip。
面积=占比，保留全部 7 类图例(含值+占比)与 hover 占比，小类不再因扇区过窄不可读。
幂等：已含 'tm-cell' 则跳过。
"""
import io

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

PATH = "site/data/poetry-rhythm-analysis.html"
START = "    // ============= 板块 2：词牌分布饼图 ============="
END = "    // ============= 板块 3"

NEW = '''    // ============= 板块 2：词牌分布矩形树图（treemap）=============
    // P2 试点：7 类饼图 → 矩形树图，面积=占比，保留图例与 hover 占比，避免小扇区不可读
    function renderPie() {
        const svg = d3.select("#pie-svg");
        svg.selectAll("*").remove();
        const wrap = document.getElementById("pie-svg");
        const width = Math.max(420, wrap.clientWidth || 760);
        const height = 420;
        svg.attr("viewBox", `0 0 ${width} ${height}`);

        const data = EMBEDDED_DATA.pie;
        const total = d3.sum(data, d => d.value);

        const root = d3.hierarchy({ name: "root", children: data })
            .sum(d => d.value)
            .sort((a, b) => b.value - a.value);
        d3.treemap().size([width, height]).paddingInner(3).round(true)(root);

        const tip = d3.select("#pie-tip");
        const wrapEl = wrap.parentElement;

        const cells = svg.selectAll("g.tm-cell")
            .data(root.leaves())
            .enter()
            .append("g")
            .attr("class", "tm-cell")
            .attr("transform", d => `translate(${d.x0},${d.y0})`);

        cells.append("rect")
            .attr("width", d => Math.max(0, d.x1 - d.x0))
            .attr("height", d => Math.max(0, d.y1 - d.y0))
            .attr("fill", (d) => PIE_COLORS[data.indexOf(d.data) % PIE_COLORS.length])
            .attr("stroke", "#fff")
            .attr("stroke-width", 2)
            .style("opacity", 0)
            .on("mouseover", function(event, d) {
                tip.style("opacity", 1)
                    .html(`<div class="tip-title">${d.data.name}</div>
                        <div class="tip-row">数量：<strong style="color:#e9b885">${d.data.value}</strong></div>
                        <div class="tip-row">占比：<strong style="color:#e9b885">${((d.data.value / total) * 100).toFixed(1)}%</strong></div>`);
            })
            .on("mousemove", function(event) {
                const rect = wrapEl.getBoundingClientRect();
                tip.style("left", (event.clientX - rect.left + 14) + "px")
                    .style("top", (event.clientY - rect.top + 14) + "px");
            })
            .on("mouseout", function() { tip.style("opacity", 0); })
            .transition().duration(DUR).style("opacity", 1);

        // 标签：仅当格子足够大，否则依赖图例 + hover
        const showLbl = d => ((d.x1 - d.x0) > 48 && (d.y1 - d.y0) > 28);
        cells.append("text")
            .attr("x", d => (d.x1 - d.x0) / 2).attr("y", d => (d.y1 - d.y0) / 2 - 4)
            .attr("text-anchor", "middle")
            .style("font-size", "0.82rem").style("font-weight", "600")
            .style("fill", "#fff").style("paint-order", "stroke")
            .style("stroke", "rgba(0,0,0,0.35)").style("stroke-width", "3px")
            .style("pointer-events", "none")
            .text(d => showLbl(d) ? d.data.name : "");
        cells.append("text")
            .attr("x", d => (d.x1 - d.x0) / 2).attr("y", d => (d.y1 - d.y0) / 2 + 13)
            .attr("text-anchor", "middle")
            .style("font-size", "0.72rem")
            .style("fill", "#fff").style("opacity", 0.92)
            .style("pointer-events", "none")
            .text(d => showLbl(d) ? `${d.data.value} · ${((d.data.value / total) * 100).toFixed(0)}%` : "");

        // 图例（保留全部 7 类 + 值 + 占比）
        const legend = d3.select("#pie-legend");
        legend.selectAll("*").remove();
        data.forEach((p, i) => {
            const item = legend.append("div").attr("class", "lg-item");
            item.append("span").attr("class", "lg-swatch round").style("background", PIE_COLORS[i % PIE_COLORS.length]);
            item.append("span").text(`${p.name}（${p.value}，${((p.value / total) * 100).toFixed(1)}%）`);
        });
    }
'''

def main():
    s = open(PATH, encoding="utf-8").read()
    if "tm-cell" in s:
        print("· 已是树图，跳过")
        return
    si = s.index(START)
    ei = s.index(END)
    new_s = s[:si] + NEW + "\n" + s[ei:]
    _w536_guard_open(PATH, "w", encoding="utf-8").write(new_s)
    print(f"✓ 替换完成：板块2 改为矩形树图（区间 {si}→{ei}）")

if __name__ == "__main__":
    main()
