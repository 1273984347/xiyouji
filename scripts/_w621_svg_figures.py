"""_w621_svg_figures.py — W621 装饰投稿包五图 SVG 重绘（数据忠实·一次性·可重复执行）

用户裁决：装饰投稿包内全部图表以 SVG 重绘。口径：
- 图 1/2：自绘示意图终版（此前 W618 底稿升级为成品）
- 图 3 人物语义网络：忠实重绘页面实际渲染的「神佛体系」子图——12 节点三层着色
  （顶层主权 #c8463a / 中层执行 #3a6b8c / 底层差遣 #8b7355）+ divine_edges 过滤后 7 边（与截图一致）
- 图 4 八十一难难度热力图：EMBEDDED_DATA 81 条真实记录，9×9 按回目序，
  色阶复刻页面 d3.scaleLinear domain [1,3,6,8,10] 五级线性插值
- 图 5 取经路线图：EMBEDDED_MOCK 5 地 4 域（页面实际数据源·journey_route.json 为空——不虚构完整路线）
- 图注口径改「据项目数据重绘」、AI 声明同步（由调用方/后续编辑完成，本脚本只产图）
输出：图表/*.svg + tmpe/w621_jobs.json（供 _w621_render_png.js 渲染 PNG 2x）
"""
import json
import math
import os
import re

ROOT = r"D:\xiyouji"
FIG = os.path.join(ROOT, "docs", "S4-学术投稿", "装饰投稿", "图表")
TMPE = os.path.join(ROOT, "tmpe")

INK = "#23201A"
PAPER = "#FAF7F0"
CINNABAR = "#C8463A"
INDIGO = "#3A6B8C"
OCHRE = "#C9A063"
MOSS = "#6B8E5A"
BROWN = "#8B7355"
LINEC = "#E5DFD0"
SOFT = "#6B6455"

FONT = "SimHei, Microsoft YaHei, sans-serif"
FONT_SONG = "SimSun, NSimSun, serif"


def w(name, svg):
    p = os.path.join(FIG, name)
    open(p, "w", encoding="utf-8", newline="").write(svg)
    print("SVG", name, len(svg), "B")


# ---------- 图 1 ----------
def fig1():
    boxes = [
        (["《西游记》文本"], "母题三结构层"),
        (["宣纸底（静）", "墨文（文）", "朱砂点醒（动）"], "文化语义提取"),
        (["--bg  #FAF7F0", "--ink  #23201A", "--accent  #C8463A"], "设计变量转译"),
        (["tokens.css 单一事实源", "全站 233 页同步"], "令牌体系化"),
    ]
    W, H = 1280, 470
    bw, bh, y0, gap, x0 = 280, 270, 70, 40, 20
    p = []
    for i, (lines, label) in enumerate(boxes):
        x = x0 + i * (bw + gap)
        p.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>')
        ty = y0 + (bh - 46 * len(lines)) / 2 + 10
        for ln in lines:
            p.append(f'<text x="{x + bw / 2}" y="{ty}" text-anchor="middle" font-size="23" fill="{INK}" font-family="{FONT}">{ln}</text>')
            ty += 46
        p.append(f'<text x="{x + bw / 2}" y="{y0 + bh - 28}" text-anchor="middle" font-size="20" fill="{CINNABAR}" font-family="{FONT}">{label}</text>')
        if i < 3:
            ax = x + bw
            p.append(f'<line x1="{ax + 6}" y1="{y0 + bh / 2}" x2="{ax + gap - 20}" y2="{y0 + bh / 2}" stroke="{CINNABAR}" stroke-width="5"/>')
            p.append(f'<polygon points="{ax + gap - 16},{y0 + bh / 2 - 11} {ax + gap + 4},{y0 + bh / 2} {ax + gap - 16},{y0 + bh / 2 + 11}" fill="{CINNABAR}"/>')
    p.append(f'<text x="{W / 2}" y="432" text-anchor="middle" font-size="23" fill="{INK}" font-family="{FONT_SONG}">把文化母题转译成可复用的设计变量——令牌取值本身承载文化语义</text>')
    w("图1-文化母题转译流程.svg",
      f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(p) + "</svg>")


# ---------- 图 2 ----------
def fig2():
    W, H = 1100, 700
    layers = [
        (500, 130, CINNABAR, "#FFFFFF", "tokens.css（单一事实源）", "纸 / 墨 / 朱 三元令牌 · 缓动三系 · 暗色组"),
        (290, 120, OCHRE, INK, "system.css（组件层）", "消费变量 · 不写死值 · 交互五态 · 动效契约"),
        (80, 130, "#D8CFBC", INK, "页面内联 <style>（图表样式层）", "233 页图表特有样式 · 只覆盖图表"),
    ]
    p = []
    for y, h, face, tc, title, desc in layers:
        p.append(f'<rect x="170" y="{y}" width="760" height="{h}" rx="12" fill="{face}" stroke="{INK}" stroke-width="2.5"/>')
        p.append(f'<text x="550" y="{y + h * 0.42}" text-anchor="middle" font-size="27" font-weight="bold" fill="{tc}" font-family="{FONT}">{title.replace("<", "&lt;").replace(">", "&gt;")}</text>')
        p.append(f'<text x="550" y="{y + h * 0.42 + 44}" text-anchor="middle" font-size="20" fill="{tc}" font-family="{FONT}">{desc}</text>')
    for y0, y1, lab in ((494, 424, "变量消费"), (284, 224, "内联分发")):
        p.append(f'<line x1="550" y1="{y0}" x2="550" y2="{y1 + 16}" stroke="{CINNABAR}" stroke-width="4"/>')
        p.append(f'<polygon points="542,{y1 + 16} 550,{y1} 558,{y1 + 16}" fill="{CINNABAR}"/>')
        p.append(f'<text x="575" y="{(y0 + y1) / 2 + 6}" font-size="19" fill="{SOFT}" font-family="{FONT}">{lab}</text>')
    p.append(f'<text x="550" y="40" text-anchor="middle" font-size="23" fill="{CINNABAR}" font-family="{FONT}">改一处 · 全站同步 · 双主题（亮 / 暗）共用同一语义系统</text>')
    w("图2-令牌三层模型.svg",
      f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(p) + "</svg>")


# ---------- 图 3 数据 ----------
def extract_divine():
    t = open(os.path.join(ROOT, "site", "data", "character-semantic-network.html"), encoding="utf-8").read()
    seg = t[t.index("subnetworks"):t.index("divine_edges")]
    m = re.search(r"divine:\s*\{\s*name:\s*'[^']+',\s*color:\s*'[^']+',\s*nodes:\s*\[([^\]]+)\]", seg)
    nodes = re.findall(r"'([^']+)'", m.group(1))
    hi = t[t.index("divine_hierarchy"):]
    top = re.findall(r"'([^']+)'", re.search(r"top:\s*\{ nodes: \[([^\]]+)\]", hi).group(1))
    mid = re.findall(r"'([^']+)'", re.search(r"middle:\s*\{ nodes: \[([^\]]+)\]", hi).group(1))
    ee = t[t.index("divine_edges"):]
    ee = ee[:ee.index("]")]
    edges = [(a, b, int(wv)) for a, b, wv in
             re.findall(r"source:\s*'([^']+)',\s*target:\s*'([^']+)',\s*weight:\s*(\d+)", ee)]
    ns = set(nodes)
    edges = [e for e in edges if e[0] in ns and e[1] in ns]
    tier = {n: ("top" if n in top else "middle" if n in mid else "bottom") for n in nodes}
    assert len(nodes) == 12 and len(edges) >= 6, (len(nodes), len(edges))
    return nodes, tier, edges


def spring(nodes, edges, W, H, iters=420, seed=7):
    pos = {}
    for i, n in enumerate(nodes):
        a = 2 * math.pi * i / len(nodes)
        pos[n] = [W / 2 + 190 * math.cos(a), H / 2 + 150 * math.sin(a)]
    k = 128.0
    t0 = 80.0
    deg = {n: 0 for n in nodes}
    for a, b, _ in edges:
        deg[a] += 1
        deg[b] += 1
    for it in range(iters):
        disp = {n: [0.0, 0.0] for n in nodes}
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                a, b = nodes[i], nodes[j]
                dx = pos[a][0] - pos[b][0]
                dy = pos[a][1] - pos[b][1]
                d = math.hypot(dx, dy) or 0.01
                f = k * k / d / (2.2 if d < 60 else 1.0)
                disp[a][0] += dx / d * f
                disp[a][1] += dy / d * f
                disp[b][0] -= dx / d * f
                disp[b][1] -= dy / d * f
        for a, b, wv in edges:
            dx = pos[a][0] - pos[b][0]
            dy = pos[a][1] - pos[b][1]
            d = math.hypot(dx, dy) or 0.01
            f = (d - k) * 0.055 * (0.5 + wv * 0.1)
            disp[a][0] -= dx / d * f
            disp[a][1] -= dy / d * f
            disp[b][0] += dx / d * f
            disp[b][1] += dy / d * f
        t = t0 * (1 - it / iters) + 1.5
        for n in nodes:
            dx, dy = disp[n]
            dl = math.hypot(dx, dy) or 0.01
            step = min(dl, t)
            pos[n][0] += dx / dl * step
            pos[n][1] += dy / dl * step
            # 向心力：防点云贴边离散
            pos[n][0] += (W / 2 - pos[n][0]) * 0.02
            pos[n][1] += (H / 2 - pos[n][1]) * 0.02
            pos[n][0] = min(W - 130, max(130, pos[n][0]))
            pos[n][1] = min(H - 150, max(150, pos[n][1]))
    # 点云居中：消除单侧大空白
    xs = [p2[0] for p2 in pos.values()]
    ys = [p2[1] for p2 in pos.values()]
    ox = W / 2 - (min(xs) + max(xs)) / 2
    oy = H / 2 - (min(ys) + max(ys)) / 2
    for n in nodes:
        pos[n][0] += ox
        pos[n][1] += oy
    return pos, deg


def fig3():
    nodes, tier, edges = extract_divine()
    W, H = 1200, 860
    pos, deg = spring(nodes, edges, W, H)
    colors = {"top": CINNABAR, "middle": INDIGO, "bottom": BROWN}
    p = []
    for a, b, wv in edges:
        p.append(f'<line x1="{pos[a][0]:.1f}" y1="{pos[a][1]:.1f}" x2="{pos[b][0]:.1f}" y2="{pos[b][1]:.1f}" stroke="{LINEC}" stroke-width="{1.5 + wv * 0.5:.1f}"/>')
    for n in nodes:
        x, y = pos[n]
        r = 16 + deg[n] * 4
        c = colors[tier[n]]
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="{PAPER}" stroke-width="2.5"/>')
        ly = y + r + 24
        p.append(f'<text x="{x:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="21" fill="{INK}" font-family="{FONT}">{n}</text>')
    lx, ly = 40, 46
    for lab, c in (("顶层主权", CINNABAR), ("中层执行", INDIGO), ("底层差遣", BROWN)):
        p.append(f'<circle cx="{lx}" cy="{ly}" r="10" fill="{c}"/>')
        p.append(f'<text x="{lx + 20}" y="{ly + 7}" font-size="19" fill="{INK}" font-family="{FONT}">{lab}</text>')
        lx += 30 + len(lab) * 19 + 46
    p.append(f'<text x="40" y="{H - 24}" font-size="16" fill="{SOFT}" font-family="{FONT}">连线粗细=共现强度 · 据项目「神佛体系」子图数据重绘</text>')
    w("图3-人物语义网络-浅.svg",
      f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">' + "".join(p) + "</svg>")


# ---------- 图 4 数据 ----------
def extract_hardships():
    t = open(os.path.join(ROOT, "site", "data", "hardship-heatmap.html"), encoding="utf-8").read()
    seg = t[t.index("const EMBEDDED_DATA"):]
    seg = seg[:seg.index("\n    ];") if "\n    ];" in seg else seg.index("];")]
    recs = [{"n": int(a), "name": b, "score": int(c), "stage": d, "cause": e}
            for a, b, e, c, d in re.findall(
                r'\{n:(\d+), name:"([^"]+)", chapter:"[^"]*", chNum:-?\d+, cause:"(\w+)", ending:"\w+", difficulty:"\w+", score:(\d+), stage:"(\w+)"\}', seg)]
    assert len(recs) == 81, len(recs)
    return recs


def scale_color(s):
    dom = [1, 3, 6, 8, 10]
    rng = [(245, 233, 212), (233, 184, 133), (217, 128, 96), (200, 70, 58), (140, 42, 42)]
    s = max(1, min(10, s))
    for i in range(4):
        if s <= dom[i + 1]:
            t = (s - dom[i]) / (dom[i + 1] - dom[i])
            return "#%02x%02x%02x" % tuple(round(a + (b - a) * t) for a, b in zip(rng[i], rng[i + 1], strict=True))
    return "#%02x%02x%02x" % rng[-1]


STAGE_CN = {"pre": "前传", "early": "前期", "mid": "中期", "late": "后期", "end": "末段"}
CAUSE_CN = {"arranged": "谋", "wild": "野", "mount": "山", "mind": "心"}


def fig4():
    recs = extract_hardships()
    cols = 9
    cw, ch, gap = 126, 74, 7
    mx, my = 46, 64
    W = mx * 2 + cols * cw + (cols - 1) * gap + 190
    rows = math.ceil(len(recs) / cols)
    H = my * 2 + rows * ch + (rows - 1) * gap + 56
    p = []
    for r in recs:
        i = r["n"] - 1
        cx = mx + (i % cols) * (cw + gap)
        cy = my + (i // cols) * (ch + gap)
        c = scale_color(r["score"])
        tc = "#FFFFFF" if r["score"] >= 6 else INK
        p.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="7" fill="{c}" stroke="#FFFFFF" stroke-width="1.2"/>')
        p.append(f'<text x="{cx + 9}" y="{cy + 21}" font-size="14" fill="{tc}" opacity="0.78" font-family="{FONT}">{r["n"]:02d}</text>')
        p.append(f'<text x="{cx + cw / 2}" y="{cy + 46}" text-anchor="middle" font-size="18" fill="{tc}" font-family="{FONT}">{r["name"]}</text>')
        p.append(f'<text x="{cx + cw - 9}" y="{cy + ch - 10}" text-anchor="end" font-size="13" fill="{tc}" opacity="0.85" font-family="{FONT}">{CAUSE_CN.get(r["cause"], "")}·{STAGE_CN.get(r["stage"], "")}</text>')
    # 右侧色标（线性五锚点）
    lx = W - 158
    ly = my + 8
    p.append(f'<text x="{lx}" y="{ly - 14}" font-size="18" fill="{INK}" font-family="{FONT}">难度色阶（1-10）</text>')
    for i in range(5):
        yy = ly + i * 46
        c = scale_color(dom_a[i]) if False else None
    # 连续渐变条
    steps = 60
    for i in range(steps):
        s = 1 + 9 * i / (steps - 1)
        p.append(f'<rect x="{lx}" y="{ly + 8 + i * 3}" width="34" height="3.2" fill="{scale_color(s)}"/>')
    for v in (1, 3, 6, 8, 10):
        yy = ly + 8 + (v - 1) / 9 * (steps * 3 - 3)
        p.append(f'<text x="{lx + 42}" y="{yy + 5}" font-size="15" fill="{SOFT}" font-family="{FONT}">{v}</text>')
    p.append(f'<text x="{lx - 4}" y="{ly + 224}" font-size="15" fill="{SOFT}" font-family="{FONT}">格内角标：</text>')
    p.append(f'<text x="{lx - 4}" y="{ly + 248}" font-size="15" fill="{SOFT}" font-family="{FONT}">起因·阶段</text>')
    p.append(f'<text x="{mx}" y="{H - 22}" font-size="16" fill="{SOFT}" font-family="{FONT}">81 难按回目序排布（9×9）· 色深=难度高 · 角标=起因（谋/野/山/心）与阶段 · 据项目实测数据重绘</text>')
    w("图4-八十一难难度热力图-浅.svg",
      f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(p) + "</svg>")


dom_a = None


# ---------- 图 5 数据 ----------
def extract_route():
    t = open(os.path.join(ROOT, "site", "data", "journey-route.html"), encoding="utf-8").read()
    seg = t[t.index("EMBEDDED_MOCK"):]
    seg = seg[:seg.index("]\n") + 2] if "]\n" in seg else seg
    places = [{"id": int(a), "chapter": int(b), "name": c, "region": d, "type": e, "event": f}
              for a, b, c, d, e, f in re.findall(
                  r'\{ id: (\d+), chapter: (\d+), name: "([^"]+)", region: "([^"]+)", type: "([^"]+)", event: "([^"]+)" \}', t)]
    assert len(places) == 5, len(places)
    return places


def fig5():
    places = extract_route()
    regions = []
    for pl in places:
        if pl["region"] not in regions:
            regions.append(pl["region"])
    rc = {r: c for r, c in zip(regions, (CINNABAR, INDIGO, OCHRE, MOSS), strict=True)}
    W, H = 1300, 460
    x0, x1, y = 150, W - 150, 250
    xs = {pl["id"]: x0 + i * (x1 - x0) / (len(places) - 1) for i, pl in enumerate(places)}
    p = []
    for r in regions:
        members = [x for x in places if x["region"] == r]
        xa = min(xs[m["id"]] for m in members)
        xb = max(xs[m["id"]] for m in members)
        pad = 46
        p.append(f'<rect x="{xa - pad}" y="{y - 64}" width="{xb - xa + pad * 2}" height="128" rx="14" fill="{rc[r]}" opacity="0.10"/>')
    p.append(f'<line x1="{x0 - 60}" y1="{y}" x2="{x1 + 60}" y2="{y}" stroke="{INK}" stroke-width="2"/>')
    p.append(f'<polygon points="{x1 + 60},{y - 8} {x1 + 76},{y} {x1 + 60},{y + 8}" fill="{INK}"/>')
    for i, pl in enumerate(places):
        xx = xs[pl["id"]]
        up = i % 2 == 0
        c = rc[pl["region"]]
        p.append(f'<line x1="{xx:.1f}" y1="{y}" x2="{xx:.1f}" y2="{y + (-58 if up else 58)}" stroke="{c}" stroke-width="1.6"/>')
        p.append(f'<circle cx="{xx:.1f}" cy="{y}" r="11" fill="{c}" stroke="#FFFFFF" stroke-width="2.5"/>')
        p.append(f'<text x="{xx:.1f}" y="{y + 32}" text-anchor="middle" font-size="15" fill="{SOFT}" font-family="{FONT}">第{pl["chapter"]}回</text>')
        ty = y + (-84 if up else 108)
        p.append(f'<text x="{xx:.1f}" y="{ty}" text-anchor="middle" font-size="21" font-weight="bold" fill="{INK}" font-family="{FONT}">{pl["name"]}</text>')
        p.append(f'<text x="{xx:.1f}" y="{ty + 28}" text-anchor="middle" font-size="17" fill="{SOFT}" font-family="{FONT}">{pl["event"]}（{pl["type"]}）</text>')
    lx = 90
    for r in regions:
        p.append(f'<rect x="{lx}" y="34" width="20" height="20" rx="5" fill="{rc[r]}" opacity="0.55"/>')
        p.append(f'<text x="{lx + 28}" y="50" font-size="18" fill="{INK}" font-family="{FONT}">{r}</text>')
        lx += 28 + len(r) * 18 + 40
    p.append(f'<text x="{W - 90}" y="{H - 20}" text-anchor="end" font-size="16" fill="{SOFT}" font-family="{FONT}">以回目为时间轴 · 地点为节点 · 据项目路线数据重绘（页面当前数据源：5 地 4 域）</text>')
    w("图5-取经路线图-浅.svg",
      f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(p) + "</svg>")


def main():
    global dom_a
    dom_a = [1, 3, 6, 8, 10]
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    # 清理 W618 底稿（已被成品取代）
    for f in ("图1-重绘底稿.svg", "图2-重绘底稿.svg"):
        fp = os.path.join(FIG, f)
        if os.path.exists(fp):
            os.remove(fp)
            print("RM", f)
    # 渲染任务清单
    jobs = []
    for f, out in (
        ("图1-文化母题转译流程", "图1-文化母题转译流程.png"),
        ("图2-令牌三层模型", "图2-令牌三层模型.png"),
        ("图3-人物语义网络-浅", "图3-人物语义网络-浅.png"),
        ("图4-八十一难难度热力图-浅", "图4-八十一难难度热力图-浅.png"),
        ("图5-取经路线图-浅", "图5-取经路线图-浅.png"),
    ):
        svg = open(os.path.join(FIG, f + ".svg"), encoding="utf-8").read()
        m = re.search(r'width="(\d+)" height="(\d+)"', svg)
        jobs.append({"svg": os.path.join(FIG, f + ".svg"), "png": os.path.join(FIG, out),
                     "w": int(m.group(1)), "h": int(m.group(2))})
    open(os.path.join(TMPE, "w621_jobs.json"), "w", encoding="utf-8").write(json.dumps(jobs))
    print("jobs:", len(jobs))


if __name__ == "__main__":
    main()
