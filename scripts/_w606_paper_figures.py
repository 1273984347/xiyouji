"""_w606_paper_figures.py — W606 S4 论文配图重绘（一次性·可重复执行）

修复 W604 图 1/图 2 的排版硬伤（盒标题悬空被裁切、箭头穿过文字）：
- 图 1 文化母题转译流程：四盒横排，文字盒内居中，箭头走盒间空隙
- 图 2 令牌三层模型：三层纵叠，箭头只画在层间空隙，附侧注
- 图 6 已随 W612 用户研究删除移除（W618 起重跑不再生成，防止复活已删配图）

输出：docs/S4-学术投稿/装饰投稿/图表/图1/图2（覆盖原 PNG，200dpi·W616 目录迁移后新址）
配套：图1/图2-重绘底稿.svg 为作者手工重绘底稿（降图片 AI 检测特征·W618）
运行：python scripts/_w606_paper_figures.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.rcParams["font.family"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

INK = "#23201A"
PAPER = "#FAF7F0"
CINNABAR = "#C8463A"
INDIGO = "#3A6B8C"
OCHRE = "#C9A063"
RICEGREY = "#D8CFBC"
SOFT = "#6B6455"

OUT = r"D:\xiyouji\docs\S4-学术投稿\装饰投稿\图表"


def box(ax, x, y, w, h, face, edge=INK, lw=1.6):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.012",
        facecolor=face, edgecolor=edge, linewidth=lw, mutation_aspect=1))


def arrow_h(ax, x0, x1, y):
    ax.add_patch(FancyArrowPatch(
        (x0, y), (x1, y), arrowstyle="-|>", mutation_scale=22,
        color=CINNABAR, linewidth=2.2))


def arrow_v(ax, x, y0, y1):
    ax.add_patch(FancyArrowPatch(
        (x, y0), (x, y1), arrowstyle="-|>", mutation_scale=22,
        color=CINNABAR, linewidth=2.2))


# ---------------- 图 1 文化母题转译流程 ----------------
fig, ax = plt.subplots(figsize=(12.8, 4.8), dpi=200)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

w, h, y0, gap, x_start = 0.205, 0.62, 0.24, 0.055, 0.015
boxes = [
    (["《西游记》文本"], "母题三结构层", PAPER, INK),
    (["宣纸底（静）", "墨文（文）", "朱砂点醒（动）"], "文化语义提取", PAPER, INK),
    (["--bg  #FAF7F0", "--ink  #23201A", "--accent  #C8463A"], "设计变量转译", PAPER, INK),
    (["tokens.css 单一事实源", "全站 233 页同步"], "令牌体系化", PAPER, INK),
]
for i, (title_lines, label, face, tc) in enumerate(boxes):
    x = x_start + i * (w + gap)
    box(ax, x, y0, w, h, face)
    ax.text(x + w / 2, y0 + h * 0.58, "\n".join(title_lines),
            ha="center", va="center", fontsize=12, color=tc, linespacing=1.9)
    ax.text(x + w / 2, y0 + h * 0.14, label,
            ha="center", va="center", fontsize=11, color=CINNABAR)
    if i < 3:
        arrow_h(ax, x + w + 0.008, x + w + gap - 0.008, y0 + h / 2)

ax.text(0.5, 0.06, "把文化母题转译成可复用的设计变量——令牌取值本身承载文化语义",
        ha="center", va="center", fontsize=12.5, color=INK)
fig.savefig(OUT + r"\图1-文化母题转译流程.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("图 1 完成")

# ---------------- 图 2 令牌三层模型 ----------------
fig, ax = plt.subplots(figsize=(11, 7), dpi=200)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

bx, bw = 0.16, 0.68
# 自底向上：tokens → system → 页面内联；箭头只画在层间空隙
layers = [
    {"y": 0.075, "h": 0.23, "face": CINNABAR, "tc": "white",
     "title": "tokens.css（单一事实源）", "desc": "纸 / 墨 / 朱 三元令牌 · 缓动三系 · 暗色组"},
    {"y": 0.395, "h": 0.21, "face": OCHRE, "tc": INK,
     "title": "system.css（组件层）", "desc": "消费变量 · 不写死值 · 交互五态 · 动效契约"},
    {"y": 0.695, "h": 0.23, "face": RICEGREY, "tc": INK,
     "title": "页面内联 <style>（图表样式层）", "desc": "233 页图表特有样式 · 只覆盖图表"},
]
for L in layers:
    box(ax, bx, L["y"], bw, L["h"], L["face"])
    ax.text(bx + bw / 2, L["y"] + L["h"] * 0.62, L["title"],
            ha="center", va="center", fontsize=15, color=L["tc"], fontweight="bold")
    ax.text(bx + bw / 2, L["y"] + L["h"] * 0.22, L["desc"],
            ha="center", va="center", fontsize=11.5, color=L["tc"])

arrow_v(ax, 0.5, layers[0]["y"] + layers[0]["h"] + 0.006, layers[1]["y"] - 0.006)
ax.text(0.525, (layers[0]["y"] + layers[0]["h"] + layers[1]["y"]) / 2, "变量消费",
        ha="left", va="center", fontsize=10.5, color=SOFT)
arrow_v(ax, 0.5, layers[1]["y"] + layers[1]["h"] + 0.006, layers[2]["y"] - 0.006)
ax.text(0.525, (layers[1]["y"] + layers[1]["h"] + layers[2]["y"]) / 2, "内联分发",
        ha="left", va="center", fontsize=10.5, color=SOFT)

ax.text(0.5, 0.965, "改一处 · 全站同步 · 双主题（亮 / 暗）共用同一语义系统",
        ha="center", va="center", fontsize=12.5, color=CINNABAR)
fig.savefig(OUT + r"\图2-令牌三层模型.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("图 2 完成")

# ---------------- 图 6 已随 W612 用户研究删除移除（防止误重跑复活已删配图） ----------------
print("图 6 跳过（W612 已删除）")
