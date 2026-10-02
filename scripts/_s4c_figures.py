"""_s4c_figures.py — S4 C 轨系统配图 4 幅（实测输出忠实重绘·SVG 源）

图 C-1 三层体系（自绘示意）
图 C-2 锚点查询实测（line_check 真实输出转录）
图 C-3 校验输出实测（check_citations 全量通过 + 单字改写阻断·真实输出转录）
图 C-4 门禁运行实测（verify_delivery 输出节选·逐行取自 tmpe/_s4c_verify_final.txt）
输出：docs/S4-学术投稿/图表/C-图*.svg + tmpe/s4c_jobs.json（供 _w621_render_png.js 2x 渲染）
"""
import io
import json
import os
import sys

ROOT = r"D:\xiyouji"
FIG = os.path.join(ROOT, "docs", "S4-学术投稿", "图表")
VERIFY_TXT = os.path.join(ROOT, "tmpe", "_s4c_verify_final.txt")

INK = "#23201A"
PAPER = "#FAF7F0"
WHITE = "#FFFFFF"
CINNABAR = "#C8463A"
DARKRED = "#8C2A2A"
INDIGO = "#3A6B8C"
OCHRE = "#C9A063"
BROWN = "#8B7355"
LINEC = "#E5DFD0"
SOFT = "#6B6455"
FONT = "SimHei, Microsoft YaHei, sans-serif"
MONO = "Consolas, 'Microsoft YaHei', monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, s, size=22, fill=INK, font=FONT, anchor="start", weight="normal", spacing=None):
    a = ' text-anchor="%s"' % anchor if anchor != "start" else ""
    wgt = ' font-weight="%s"' % weight if weight != "normal" else ""
    sp = ' letter-spacing="%s"' % spacing if spacing else ""
    return ('<text x="%s" y="%s" font-size="%s" fill="%s" font-family="%s"%s%s%s>%s</text>'
            % (x, y, size, fill, font, a, wgt, sp, esc(s)))


def rect(x, y, w, h, fill=WHITE, stroke=INK, sw=2.5, rx=12):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
            % (x, y, w, h, rx, fill, stroke, sw))


def arrow(x1, y1, x2, y2, color=CINNABAR, sw=4):
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"/>'
            % (x1, y1, x2, y2, color, sw))


def head(px, py, dx, dy, color=CINNABAR, s=11):
    a = []
    for sx, sy in ((px - dy * s / 2, py + dx * s / 2), (px + dy * s / 2, py - dx * s / 2)):
        a.append("%s,%s" % (round(px + dx * 2.2 * s), round(py + dy * 2.2 * s)))
        a.append("%s,%s" % (round(sx), round(sy)))
    return '<polygon points="%s" fill="%s"/>' % (" ".join(a), color)


def write(name, svg):
    p = os.path.join(FIG, name)
    io.open(p, "w", encoding="utf-8", newline="").write(svg)
    print("SVG", name, len(svg), "B")
    return p


# ---------------------------------------------------------------- 图 C-1 体系图
def fig1():
    W, H = 1240, 700
    p = []
    # 左：内容生产
    p.append(rect(40, 40, 256, 190, PAPER))
    p.append(T(168, 80, "内容文档 615 篇", 24, INK, FONT, "middle", "bold"))
    p.append(T(168, 116, "（人机协作产出）", 19, SOFT, FONT, "middle"))
    p.append(T(168, 158, "每条原著引文行：", 19, INK, FONT, "middle"))
    p.append(T(168, 192, "> 原文引文（第N回）：“…”", 17, INDIGO, MONO, "middle"))
    p.append(arrow(300, 135, 344, 135))
    p.append(head(344, 135, 1, 0))
    # 中：三层
    layers = [
        (76, "锚点层｜引文在哪里", ["第 N 回 line X · 只读定位脚本 · 锚定公开底本"]),
        (222, "校验层｜引文对不对", ["去空白归一 + 精确子串命中（最小归一）", "任一未命中即失败 · 禁止省略号节引"]),
        (368, "门禁层｜核验何时发生", ["挂在交付路径 · 提交即执行 · 24 道门禁含引文硬验证"]),
    ]
    for y, t, descs in layers:
        p.append(rect(348, y, 560, 118, WHITE))
        p.append(T(378, y + 44, t, 25, INK, FONT, "start", "bold"))
        dy = y + 78
        for d in descs:
            p.append(T(378, dy, d, 19, SOFT))
            dy += 26
    for y0, y1 in ((194, 222), (340, 368)):
        p.append(arrow(628, y0, 628, y1 - 4))
        p.append(head(628, y1, 0, 1))
    # 右：交付出口
    p.append(rect(952, 176, 248, 210, PAPER))
    p.append(T(1076, 216, "交 付", 25, INK, FONT, "middle", "bold"))
    p.append(T(1076, 264, "命中 → 放行", 20, "#3F6E4C", FONT, "middle"))
    p.append(T(1076, 306, "未命中 → 阻断", 20, DARKRED, FONT, "middle"))
    p.append(T(1076, 348, "（退出码非零）", 18, SOFT, FONT, "middle"))
    p.append(arrow(908, 427, 992, 388, INK, 3.5))
    p.append(head(992, 388, 0.86, -0.5))
    # 基座：公开底本
    p.append(rect(348, 556, 560, 92, PAPER, INK, 2))
    p.append(T(628, 596, "公开底本：百回本《西游记》电子文本（100 回 · 708,441 字）", 21, INK, FONT, "middle"))
    p.append(T(628, 630, "锚定与命中判定的唯一判定材料", 18, SOFT, FONT, "middle"))
    p.append(arrow(470, 556, 470, 492, CINNABAR, 3.5))
    p.append(head(470, 492, 0, -1))
    p.append(T(486, 528, "锚定", 18, CINNABAR))
    p.append(arrow(790, 556, 790, 492, CINNABAR, 3.5))
    p.append(head(790, 492, 0, -1))
    p.append(T(806, 528, "比对", 18, CINNABAR))
    # 底部小结
    p.append(T(620, 676, "锚点层定坐标 · 校验层判真伪 · 门禁层保执行——核验从“能力”变成“路径”", 22, INK, FONT, "middle"))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
           % (W, H, W, H)) + "".join(p) + "</svg>"
    return write("C-图1-三层体系.svg", svg), W, H


# ---------------------------------------------------------------- 图 C-2 锚点查询
def fig2():
    W, H = 1180, 430
    p = []
    p.append(rect(40, 30, 1100, 330, WHITE, INK, 2.5, 14))
    x = 76
    p.append(T(x, 96, "$ python scripts/audit/line_check.py 2 \"此山叫做灵台方寸山，山中有座斜月三星洞。\"", 20, INK, MONO))
    p.append(T(x, 136, "9", 21, INK, MONO))
    p.append(T(x + 60, 136, "→  第 2 回 line 9（引文首字符所在行）", 20, CINNABAR, FONT))
    p.append(T(x, 216, "$ python scripts/audit/line_check.py 7 \"皇帝轮流做，明年到我家。\"", 20, INK, MONO))
    p.append(T(x, 256, "45", 21, INK, MONO))
    p.append(T(x + 60, 256, "→  第 7 回 line 45", 20, CINNABAR, FONT))
    p.append(T(x, 322, "两条命令均只读；输出行号即「第 N 回 line X」中的 X，任何第三方可在公开语料上重跑复现", 19, SOFT))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
           % (W, H, W, H)) + "".join(p) + "</svg>"
    return write("C-图2-锚点查询实测.svg", svg), W, H


# ---------------------------------------------------------------- 图 C-3 校验输出
def fig3():
    W, H = 1180, 560
    p = []
    # A 通过
    p.append(rect(40, 30, 1100, 200, WHITE, INK, 2.5, 14))
    p.append(T(76, 70, "A　全量校验：通过", 22, "#3F6E4C", FONT, "start", "bold"))
    p.append(T(76, 118, "$ python scripts/check_citations.py --dir docs", 20, INK, MONO))
    p.append(T(76, 158, "引文核验通过：共 437 条引文行 · 命中率 100%（842 个文件扫描）", 20, INK, MONO))
    p.append(T(76, 200, "→  退出码 0 · 全库放行", 20, CINNABAR, FONT))
    # B 阻断
    p.append(rect(40, 260, 1100, 240, WHITE, INK, 2.5, 14))
    p.append(T(76, 300, "B　单字改写：未命中即阻断（示例：把“魔生”改写成“魔灭”）", 22, DARKRED, FONT, "start", "bold"))
    p.append(T(76, 348, "$ python scripts/check_citations.py --file tmpe/引文改写示例.md", 20, INK, MONO))
    p.append(T(76, 388, "FAIL tmpe/引文改写示例.md:1 第13回未命中（非原文精确子串）", 20, DARKRED, MONO))
    p.append(T(76, 424, "引文核验：共 1 条引文行 · 1 个文件存在未命中/格式错误", 20, INK, MONO))
    p.append(T(76, 466, "→  退出码 1 · 本次交付被阻断", 20, CINNABAR, FONT))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
           % (W, H, W, H)) + "".join(p) + "</svg>"
    return write("C-图3-校验输出实测.svg", svg), W, H


# ---------------------------------------------------------------- 图 C-4 门禁运行
def fig4():
    raw = io.open(VERIFY_TXT, encoding="utf-8").read().replace("\r\n", "\n").split("\n")
    keep_kw = [
        "A1-A6 真实文件计数",
        "docs/01 链接校验通过",
        "CSP 校验通过",
        "数据漂移检查通过",
        "INLINED CSS 门禁通过",
        "元信息块 v2 门禁通过",
        "术语一致性门禁通过",
        "原著引文核验通过",
        "图表静态自洽门禁通过",
        "数据内容一致性门禁通过",
    ]
    lines = []
    for kw in keep_kw:
        hit = [l for l in raw if l.startswith("OK") and kw in l]
        assert len(hit) == 1, "门禁输出行定位异常: %s -> %d" % (kw, len(hit))
        lines.append(hit[0])
    assert "核心全部通过" in "\n".join(raw), "汇总行缺失"

    W = 1280
    H = 80 + 44 * (len(lines) + 4) + 40
    p = []
    p.append(rect(40, 30, W - 80, H - 90, WHITE, INK, 2.5, 14))
    y = 78
    p.append(T(76, y, "$ python scripts/verify_delivery.py", 21, INK, MONO))
    y += 48
    for l in lines:
        p.append(T(76, y, l, 19, INK, MONO))
        y += 40
    y += 6
    p.append('<line x1="76" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (y - 12, W - 76, y - 12, LINEC))
    y += 24
    p.append(T(76, y, "==== 交付校验汇总 ====", 21, INK, MONO))
    y += 44
    p.append(T(76, y, "核心全部通过 ✅", 23, "#3F6E4C", FONT, "start", "bold"))
    y += 46
    p.append(T(76, y, "（输出节选：本次交付核心检查全部通过，任一 FAIL 即以非零退出码阻断提交）", 19, SOFT))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
           % (W, H, W, H)) + "".join(p) + "</svg>"
    return write("C-图4-门禁运行实测.svg", svg), W, H


def main():
    jobs = []
    for fn in (fig1, fig2, fig3, fig4):
        path, w, h = fn()
        jobs.append({"svg": path.replace("\\", "/"),
                     "png": path.replace("\\", "/").replace(".svg", ".png"),
                     "w": w, "h": h})
    io.open(os.path.join(ROOT, "tmpe", "s4c_jobs.json"), "w", encoding="utf-8").write(
        json.dumps(jobs, ensure_ascii=False, indent=1))
    print("jobs:", len(jobs))
    return 0


if __name__ == "__main__":
    sys.exit(main())