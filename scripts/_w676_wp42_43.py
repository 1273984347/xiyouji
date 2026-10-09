"""W676 WP-4.2②③/4.2④部分/4.3②③④⑤ 机械修复（ZH+EN 八面）。

- mbti-evolution：雷达/色标/图例三 scale domain[0,8]→[0,10] + 网格圆 [2,4,6,8,10]
  + 4 个 stage-btn 补 aria-controls（单共享面板语义，role=tabpanel 落在 radar-wrap）
- magic-system：预算图删 totalRevenue/totalExpense 折算两条 bar（0.9249 硬编码与明细量纲脱节）
  + kills 字段→combat_record（ZH 表头 战绩→战斗记录·EN 已是 Combat Record）
- monster-background：renderKPI 补前置清空 + 「差距 10.7 倍」→「之比约 10.7」
- narratology-13d：window.__clusterOrder 全局泄漏 → 局部 const（提到 forceSimulation 链前）
- poetry-rhythm：「词牌分布矩形树图」→「诗词类别分布矩形树图」（实含 7 类非词牌）

一次性脚本；每处替换带出现次数断言，任一失配即中止不落盘。
"""
import sys

FILES = {
    "mz": "site/data/mbti-evolution.html",
    "me": "site/en/mbti-evolution.html",
    "gz": "site/data/magic-system.html",
    "ge": "site/en/magic-system.html",
    "bz": "site/data/monster-background.html",
    "be": "site/en/monster-background.html",
    "nz": "site/data/narratology-13d-network.html",
    "ne": "site/en/narratology-13d-network.html",
    "pz": "site/data/poetry-rhythm-analysis.html",
    "pe": "site/en/poetry-rhythm-analysis.html",
}

EDITS = []


def add(f, old, new, n=1):
    EDITS.append((f, old, new, n))


# ---------- mbti ----------
for k in ("mz", "me"):
    add(k, "domain([0, 8])", "domain([0, 10])", 3)
    add(k, "[2, 4, 6, 8].forEach", "[2, 4, 6, 8, 10].forEach")
    add(k, 'role="tab" aria-selected="true"', 'role="tab" aria-controls="mbti-radar-panel" aria-selected="true"')
    add(k, 'role="tab" aria-selected="false"', 'role="tab" aria-controls="mbti-radar-panel" aria-selected="false"', 3)
add("mz", '<div class="radar-wrap">',
    '<div class="radar-wrap" id="mbti-radar-panel" role="tabpanel" aria-label="阶段人格雷达图">')
add("me", '<div class="radar-wrap">',
    '<div class="radar-wrap" id="mbti-radar-panel" role="tabpanel" aria-label="Stage personality radar">')

# ---------- magic-system ----------
add("gz", """        // 盈余率 92.49% → 推算总收支（蟠桃单位折算）
        const totalRevenue = Math.round(budget.surplus / 0.9249);
        const totalExpense = totalRevenue - budget.surplus;

        const bars = [
            {label: "年度收入", value: totalRevenue, color: "#c8463a", unit: "蟠桃单位"},
            {label: "年度支出", value: totalExpense, color: "#3a6b8c", unit: "蟠桃单位"},
            {label: "年度盈余", value: budget.surplus, color: "#6B8E5A", unit: "蟠桃单位"}
        ];""",
    """        const bars = [
            {label: "年度盈余", value: budget.surplus, color: "#6B8E5A", unit: "蟠桃单位"}
        ];""")
add("gz", ".domain([0, totalRevenue * 1.1])", ".domain([0, budget.surplus * 1.25])")
add("ge", """        // surplus rate 92.49% → derive total revenue/expense (converted to Peach Units)
        const totalRevenue = Math.round(budget.surplus / 0.9249);
        const totalExpense = totalRevenue - budget.surplus;

        const bars = [
            {label: "Annual Revenue", value: totalRevenue, color: "#c8463a", unit: "Peach Units"},
            {label: "Annual Expense", value: totalExpense, color: "#3a6b8c", unit: "Peach Units"},
            {label: "Annual Surplus", value: budget.surplus, color: "#6B8E5A", unit: "Peach Units"}
        ];""",
    """        const bars = [
            {label: "Annual Surplus", value: budget.surplus, color: "#6B8E5A", unit: "Peach Units"}
        ];""")
add("ge", ".domain([0, totalRevenue * 1.1])", ".domain([0, budget.surplus * 1.25])")
for k in ("gz", "ge"):
    add(k, '"kills":"', '"combat_record":"', 5)
    add(k, 'tr.append("td").text(f.kills);', 'tr.append("td").text(f.combat_record);')
add("gz", "<th>战绩</th>", "<th>战斗记录</th>")

# ---------- monster-background ----------
add("bz", "const row = d3.select('#kpi-row');",
    "const row = d3.select('#kpi-row');\n        row.selectAll('*').remove();")
add("be", "const row = d3.select('#kpi-row');",
    "const row = d3.select('#kpi-row');\n        row.selectAll('*').remove();")
add("bz", "存活率差距 10.7 倍", "存活率之比约 10.7")
add("be", "a 10.7× survival-rate gap", "a survival-rate ratio of about 10.7")

# ---------- narratology-13d clusterOrder 局部化 ----------
for k in ("nz", "ne"):
    add(k, "  const sim = d3.forceSimulation(nodes).alphaDecay(0.08).velocityDecay(0.5)",
        "  const clusterOrder = Array.from(new Set(nodes.map(n => (n.parent || n.id || n.category || n.type || '')).filter(Boolean)));\n"
        "  const sim = d3.forceSimulation(nodes).alphaDecay(0.08).velocityDecay(0.5)")
    add(k, """                const key = (d.parent || d.id || d.category || d.type || '');
                if (!window.__clusterOrder) {
                    window.__clusterOrder = Array.from(new Set(nodes.map(n => (n.parent || n.id || n.category || n.type || '')).filter(Boolean)));
                }
                const idx = window.__clusterOrder.indexOf(key);
                return (width / (window.__clusterOrder.length + 1)) * (idx + 1);""",
        """                const key = (d.parent || d.id || d.category || d.type || '');
                const idx = clusterOrder.indexOf(key);
                return (width / (clusterOrder.length + 1)) * (idx + 1);""")

# ---------- poetry-rhythm ----------
add("pz", "<!-- 板块 2：词牌分布饼图 -->", "<!-- 板块 2：诗词类别分布 -->")
add("pz", '<h2 id="sec-pie">① 词牌分布矩形树图</h2>', '<h2 id="sec-pie">① 诗词类别分布矩形树图</h2>')
add("pz", '<title id="pie-title">词牌分布矩形树图</title>', '<title id="pie-title">诗词类别分布矩形树图</title>')
add("pz", "// ============= 板块 2：词牌分布矩形树图（treemap）=============",
    "// ============= 板块 2：诗词类别分布矩形树图（treemap）=============")
add("pe", "<!-- 板块 2：词牌分布饼图 -->", "<!-- 板块 2：诗词类别分布 -->")
add("pe", '<h2 id="sec-pie">① Cipai Distribution Treemap</h2>', '<h2 id="sec-pie">① Poetry Category Distribution Treemap</h2>')
add("pe", '<title id="pie-title">Cipai Distribution Treemap</title>', '<title id="pie-title">Poetry Category Distribution Treemap</title>')


def main():
    dry = "--dry" in sys.argv
    fail = []
    caches = {}
    for key, path in FILES.items():
        with open(path, encoding="utf-8", newline="") as fh:
            caches[key] = fh.read()

    for fkey, old, new, n in EDITS:
        nl = "\r\n" if "\r\n" in caches[fkey] else "\n"
        old_n = old.replace("\n", nl)
        new_n = new.replace("\n", nl)
        c = caches[fkey].count(old_n)
        if c != n:
            fail.append("%s: %r 期望 %d 实得 %d" % (FILES[fkey], old[:60], n, c))
            continue
        caches[fkey] = caches[fkey].replace(old_n, new_n)

    if fail:
        for x in fail:
            print("FAIL " + x)
        sys.exit(1)

    if not dry:
        for key, path in FILES.items():
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(caches[key])

    checks = [
        ("mz", "domain([0, 8])"), ("me", "domain([0, 8])"),
        ("gz", "0.9249"), ("ge", "0.9249"),
        ("gz", '"kills"'), ("ge", '"kills"'),
        ("bz", "10.7 倍"), ("be", "10.7×"),
        ("nz", "__clusterOrder"), ("ne", "__clusterOrder"),
        ("pz", "词牌分布"), ("pe", "Cipai Distribution"),
    ]
    bad = 0
    for key, pat in checks:
        c = caches[key].count(pat)
        print("%s %r 残留=%d" % (FILES[key], pat, c))
        bad += c
    print("OK: 断言全过%s，残留总计=%d" % ("（dry 未落盘）" if dry else "，已落盘", bad))
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
