"""W676 WP-4.1/4.2 机械修复：female/victims 参数化 + ecology 深拷贝与 d3.sankey 重写 + 13d fetch 反转（ZH+EN 六文件）。

一次性脚本（_ 前缀不入门禁）。每处替换带出现次数断言，任一失配即中止不落盘。
用法：python scripts/_w676_wp41.py          # 应用并自检
      python scripts/_w676_wp41.py --dry    # 只校验断言不写盘
"""
import sys

FILES = {
    "fz": "site/data/monster-female-network.html",
    "fe": "site/en/monster-female-network.html",
    "vz": "site/data/monster-victims-network.html",
    "ve": "site/en/monster-victims-network.html",
    "ez": "site/data/monster-ecology-network.html",
    "ee": "site/en/monster-ecology-network.html",
    "nz": "site/data/narratology-13d-network.html",
    "ne": "site/en/narratology-13d-network.html",
}

# (file, old, new, expected_count)
EDITS = []


def add(f, old, new, n=1):
    EDITS.append((f, old, new, n))


# ---------- female：render 函数接收 nodes 参数，函数内 0 处 EMBEDDED 直引 ----------
for k in ("fz", "fe"):
    add(k, "function buildSankeyGraph(linkData) {",
        "function buildSankeyGraph(linkData, monsterNodes) {")
    add(k, "const monsterNames = EMBEDDED_DATA.monsterFemale.nodes",
        "const monsterNames = monsterNodes")
    add(k, "const graphData = buildSankeyGraph(sankeyLinkData);",
        "const graphData = buildSankeyGraph(sankeyLinkData, monsterNodes);")
    add(k, "function renderSankey(sankeyLinkData) {",
        "function renderSankey(sankeyLinkData, monsterNodes) {")
    add(k, "EMBEDDED_DATA.monsterFemale.nodes.forEach(n => { monsterColors[n.name] = n.color; });",
        "monsterNodes.forEach(n => { monsterColors[n.name] = n.color; });")
    add(k, "function renderRadar(radarData) {",
        "function renderRadar(radarData, monsterNodes) {")
    add(k, "EMBEDDED_DATA.monsterFemale.nodes.forEach(n => { roleColors[n.name] = n.color; });",
        "monsterNodes.forEach(n => { roleColors[n.name] = n.color; });")
    # loadData 合并层死回退摘除（fetchJson 失败已整体回退 EMBEDDED，节点键必然在位）
    add(k, "nodes: data.nodes || EMBEDDED_DATA.monsterFemale.nodes,\n"
           "    network: { nodes: data.nodes || EMBEDDED_DATA.monsterFemale.nodes, links: data.links || EMBEDDED_DATA.monsterFemale.links },",
        "nodes: data.nodes,\n"
           "    network: { nodes: data.nodes, links: data.links },")
    add(k, "renderSankey(data.sankey);", "renderSankey(data.sankey, data.nodes);", 2)
    add(k, "renderRadar(data.radar);", "renderRadar(data.radar, data.nodes);", 2)

# ---------- victims：render 函数接收 victims 参数 ----------
for k in ("vz", "ve"):
    add(k, "victims: Array.isArray(victims) ? victims : (victims.victims || EMBEDDED_DATA.victims),",
        "victims: Array.isArray(victims) ? victims : victims.victims,")
    add(k, "function renderForce(networkData) {", "function renderForce(networkData, victims) {")
    add(k, "function renderSankey(sankeyData) {", "function renderSankey(sankeyData, victims) {")
    add(k, "function renderRadar(radarData) {", "function renderRadar(radarData, victims) {")
    add(k, "function renderTimeline(timelineData) {", "function renderTimeline(timelineData, victims) {")
    add(k, "EMBEDDED_DATA.victims.forEach(v => { victimColors[v.name] = v.color; });",
        "victims.forEach(v => { victimColors[v.name] = v.color; });", 4)
    add(k, "const victimNames = EMBEDDED_DATA.victims.map(v => v.name);",
        "const victimNames = victims.map(v => v.name);")
    add(k, "renderForce(data.network);", "renderForce(data.network, data.victims);", 2)
    add(k, "renderSankey(data.sankey);", "renderSankey(data.sankey, data.victims);", 2)
    add(k, "renderRadar(data.radar);", "renderRadar(data.radar, data.victims);", 2)
    add(k, "renderTimeline(data.timeline);", "renderTimeline(data.timeline, data.victims);", 2)

# ---------- ecology：links 深拷贝（防 forceLink 原地污染 EMBEDDED_DATA） ----------
for k in ("ez", "ee"):
    add(k, "let links = EMBEDDED_DATA.network.links;",
        "let links = EMBEDDED_DATA.network.links.map(d => ({...d}));")

# ---------- 13d：fetchJson 协议分支删除（对齐 12d 形态，http 恢复实时装载路径） ----------
for k in ("nz", "ne"):
    add(k, "async function fetchJson(path, fallbackKey) {\n"
           "  // file:// 协议下尝试 fetch 外部 JSON；http(s):// 协议下直接用嵌入数据（避免跨路径 404）\n"
           "  if (location.protocol !== 'file:') {\n"
           "    return EMBEDDED_DATA[fallbackKey];\n"
           "  }\n"
           "  try {",
        "async function fetchJson(path, fallbackKey) {\n"
           "  try {")


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
            fail.append("%s: %r 期望 %d 次实得 %d 次" % (FILES[fkey], old[:60], n, c))
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

    # 自检：EMBEDDED 直引清零（ecology 例外——其网络数据本身为 EMBEDDED 单源页）
    for key in ("fz", "fe", "vz", "ve", "nz", "ne"):
        pat = ("EMBEDDED_DATA.monsterFemale.nodes" if key in ("fz", "fe")
               else "EMBEDDED_DATA.victims" if key in ("vz", "ve")
               else "location.protocol")
        c = caches[key].count(pat)
        print("%s %s 残留=%d" % (FILES[key], pat, c))
        if c:
            sys.exit(1)
    for key in ("ez", "ee"):
        c = caches[key].count("yPositions")
        print("%s yPositions 残留=%d links 深拷贝=%d" % (
            FILES[key], c, "links.map(d => ({...d}))" in caches[key]))
    print("OK: 全部断言通过%s" % ("（dry-run 未落盘）" if dry else "，已落盘"))


if __name__ == "__main__":
    main()
