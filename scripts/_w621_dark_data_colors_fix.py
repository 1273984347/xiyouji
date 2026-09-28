#!/usr/bin/env python3
"""W621 暗色阶段三：数据驱动角色色暗色可读性修复（48/7 登记批清零）。

四族根因（均为 fetch(部署) 与 EMBEDDED(file://) 双路径失配家族，W565 同族）：
  A. character-appearance zh+en：W565 timeline 派生短路了 color 兜底分支——部署 fetch
     数据无 color 字段 → .attr("fill", undefined) → SVG 默认黑（条形 15/timeline 圆点）。
  B. methodology-matrix zh+en：部署 JSON villain_positions.quadrant 为中文象限名，
     页面 QUADRANT_COLORS 键为英文 id → 查表 undefined → 散点黑 ×15。
  C. en methodology-matrix：部署 JSON rescue_phase 为中文阶段名，PHASE_COLORS 键为
     英文 → ROI 趋势色带/圆点/表徽章黑；且部署 JSON phase_analysis 为字典（EMBEDDED
     为数组）→ forEach 抛错被 safe() 静默吞掉，阶段对比卡整节缺失（zh/en 同病）。
  D. en chart-design：部署 JSON monster_clock 怪物名为中文，MONSTER_COLORS 键为英文
     → 散点黑 ×6。en narrative-experiment：部署数据组色 #7a5230 过暗 → tokens 暗色
     映射补一行。journey-spacetime：轴 hover 标记为 CSS 类上色（fill 属性映射打不中）
     → JS 补 fill 属性让既有 #3a6b8c 映射接管（暗色提亮为 #7d99a9，浅色零变化）。

EMBEDDED 路径安全性：别名键对英文 id / 数组 / 已有 color 全部透传（passthrough）。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(path: Path, old: str, new: str, count: int = 1) -> None:
    text = path.read_text(encoding="utf-8")
    n = text.count(old)
    if n != count:
        print(f"FAIL {path.name}: 匹配 {n} 处（期望 {count}）——模式：{old[:60]!r}...")
        sys.exit(1)
    path.write_text(text.replace(old, new), encoding="utf-8", newline="")
    print(f"OK   {path.name}: 替换 {count} 处")


# ---------- A. character-appearance zh+en：color 兜底与 timeline 解耦 ----------
MERGE_ZH = """        // 容错：若 server 返回数据缺少 timeline 字段，按算法补齐
        if (data.characters && data.characters[0] && !data.characters[0].timeline) {
            data.characters = data.characters.map(c => ({
                ...c,
                timeline: makeTimeline(c.first_chapter || 1, c.appearances || 0, c.mentions || 0),
                color: c.color || "#c8463a"
            }));
        }
"""
MERGE_NEW_ZH = """        // 容错：若 server 返回数据缺少 timeline 字段，按算法补齐
        if (data.characters && data.characters[0] && !data.characters[0].timeline) {
            data.characters = data.characters.map(c => ({
                ...c,
                timeline: makeTimeline(c.first_chapter || 1, c.appearances || 0, c.mentions || 0)
            }));
        }
        // W621：颜色兜底与 timeline 派生解耦——部署 fetch 数据无 color 字段，此前兜底
        // 分支被「timeline 已派生」短路，fill 落回 SVG 默认黑（暗色下不可见）；
        // 按角色名对齐 MOCK 配色，其余角色按 MOCK 调色板轮转
        if (data.characters && data.characters[0]) {
            const nameColors = Object.fromEntries(MOCK_CHARACTERS.map(c => [c.name, c.color]));
            data.characters = data.characters.map((c, i) => ({
                ...c,
                color: c.color || nameColors[c.name] || MOCK_CHARACTERS[i % MOCK_CHARACTERS.length].color
            }));
        }
"""

# ---------- B/C. methodology-matrix：象限/阶段别名 + phase_analysis 形状归一 ----------
QUAD_DEF_ZH = """    const QUADRANT_COLORS = {
        "left_top": "#7a3a8c",      // 强背景+形而上 · 紫
        "right_top": "#3a6b8c",     // 强背景+求生 · 蓝
        "left_bottom": "#c8463a",   // 弱背景+求生 · 红
        "right_bottom": "#C9A063"   // 弱背景+形而上 · 棕
    };
"""
QUAD_DEF_EN = """    const QUADRANT_COLORS = {
        "left_top": "#7a3a8c",      // strong backing + metaphysical · purple
        "right_top": "#3a6b8c",     // strong backing + survival · blue
        "left_bottom": "#c8463a",   // weak backing + survival · red
        "right_bottom": "#C9A063"   // weak backing + metaphysical · brown
    };
"""
QUAD_KEY_LINE = """    // W621：象限字段双形态兼容——部署 JSON 用中文象限名，EMBEDDED/代码键为英文 id
    const QUADRANT_KEY = q => ({ "左上": "left_top", "右上": "right_top", "左下": "left_bottom", "右下": "right_bottom" }[q] || q);
"""
PHASE_DEF_EN_ANCHOR = """    const PHASE_COLORS = {
        "Early · instinctive": "#c8463a",
        "Middle · learning": "#d97706",
        "Late · actuary": "#6B8E5A"
    };
"""
PHASE_DEF_EN_NEW = PHASE_DEF_EN_ANCHOR + """    // W621：阶段字段双形态兼容——部署 JSON 用中文阶段名，EMBEDDED/代码键为英文
    const PHASE_KEY = p => ({ "早期·本能型": "Early · instinctive", "中期·学习型": "Middle · learning", "后期·精算师型": "Late · actuary" }[p] || p);
"""
MAIN_ANCHOR = """    async function main() {
        const data = await loadAll();
        window.__data = data;
"""
MAIN_ANCHOR_NEW = MAIN_ANCHOR + """
        // W621：部署 JSON 的 phase_analysis 为字典（键=阶段名），EMBEDDED 为数组——
        // 归一为数组，否则 forEach 抛错被 safe() 静默吞掉，部署态阶段对比卡整节缺失
        const pa621 = data.rescue_roi && data.rescue_roi.phase_analysis;
        if (pa621 && !Array.isArray(pa621)) {
            data.rescue_roi.phase_analysis = Object.entries(pa621).map(([phase, v]) => ({ phase, ...v }));
        }
"""

# ---------- D. en chart-design：怪物名别名 ----------
MONSTER_DEF_EN = """    const MONSTER_COLORS = {
        "White Bone Spirit": "#c8463a",
        "Green Ox Spirit": "#6B8E5A",
        "Yellow-Robed Monster": "#d97706",
        "Red Boy": "#e9b885",
        "Six-Eared Macaque": "#8A6D3B",
        "Great Peng Golden-Winged Eagle": "#3a6b8c"
    };
"""
MONSTER_DEF_EN_NEW = MONSTER_DEF_EN + """    // W621：怪物名双形态兼容——部署 JSON 为中文名，页面色表键为英文名
    const MONSTER_KEY = d => ({ "白骨精": "White Bone Spirit", "青牛精": "Green Ox Spirit", "黄袍怪": "Yellow-Robed Monster", "红孩儿": "Red Boy", "六耳猕猴": "Six-Eared Macaque", "大鹏金翅雕": "Great Peng Golden-Winged Eagle" }[d.monster] || d.monster);
"""

# ---------- journey-spacetime：标记改挂 fill 属性（让既有暗色映射接管） ----------
MARKER_OLD = """        const axisHoverMarker = g.append("rect")
            .attr("class", "axis-hover-marker")
            .attr("y", innerH + 2).attr("width", 8).attr("height", 11).attr("rx", 1)
            .attr("x", -4);
"""
MARKER_NEW = """        const axisHoverMarker = g.append("rect")
            .attr("class", "axis-hover-marker")
            .attr("y", innerH + 2).attr("width", 8).attr("height", 11).attr("rx", 1)
            .attr("x", -4)
            // W621：补 fill 属性——标记原为 CSS 类上色，暗色映射（属性精确匹配）打不中；
            // 挂属性后暗色由 tokens #3a6b8c→#7d99a9 映射接管，浅色仍由类规则着色零变化
            .attr("fill", "#3A6B8C");
"""

# ---------- tokens.css：#7a5230 暗色映射补行 ----------
TOKENS_ANCHOR = '  html[data-theme="dark"] svg [fill="#23201A" i] { fill: #9a9489; }  /* ×2 L<0.16 */\n'
TOKENS_NEW = TOKENS_ANCHOR + '  html[data-theme="dark"] svg [fill="#7a5230" i] { fill: #bb9070; }  /* narrative-experiment 部署数据组色·暗色提亮 */\n'


# ---------- en character-appearance：时间线过滤归一（visual-judge 实拍补刀） ----------
TIMELINE_ANCHOR = '    const MAIN_CHARACTERS = ["Sun Wukong", "Tang Sanzang", "Zhu Bajie", "Sha Wujing", "Guanyin", "Tathāgata"];\n'
TIMELINE_NEW = TIMELINE_ANCHOR + """    // W621：部署 fetch 数据角色名为中文（EMBEDDED 为英文）——时间线过滤/显示前归一，
    // 否则英文页部署态过滤得 0 行、整图空渲染（visual-judge 实拍实证）
    const ZH2EN_NAME = { "孙悟空": "Sun Wukong", "唐僧": "Tang Sanzang", "猪八戒": "Zhu Bajie", "沙僧": "Sha Wujing", "观音": "Guanyin", "如来": "Tathāgata" };
"""
MAIN_FILTER_OLD = "        const main = data.characters.filter(c => MAIN_CHARACTERS.includes(c.name));\n"
MAIN_FILTER_NEW = """        const main = data.characters
            .map(c => ({ ...c, name: ZH2EN_NAME[c.name] || c.name }))
            .filter(c => MAIN_CHARACTERS.includes(c.name));
"""


def main() -> int:
    ok = True

    # A2：en character-appearance 时间线（幂等：带 marker 跳过）
    p = ROOT / "site/en/character-appearance.html"
    t = p.read_text(encoding="utf-8")
    if "ZH2EN_NAME" in t:
        print("SKIP en character-appearance：时间线归一已存在")
    else:
        try:
            patch(p, TIMELINE_ANCHOR, TIMELINE_NEW)
            patch(p, MAIN_FILTER_OLD, MAIN_FILTER_NEW)
        except SystemExit:
            ok = False

    # A：character-appearance zh+en
    for rel in ("site/data/character-appearance.html", "site/en/character-appearance.html"):
        try:
            patch(ROOT / rel, MERGE_ZH, MERGE_NEW_ZH)
        except SystemExit:
            ok = False

    # B：methodology-matrix zh+en 象限别名 + 查表点
    quad_defs = (("site/data/methodology-matrix.html", QUAD_DEF_ZH), ("site/en/methodology-matrix.html", QUAD_DEF_EN))
    for rel, qdef in quad_defs:
        p = ROOT / rel
        try:
            patch(p, qdef, qdef + QUAD_KEY_LINE)
            patch(p, 'QUADRANT_COLORS[d.quadrant]', 'QUADRANT_COLORS[QUADRANT_KEY(d.quadrant)]', 2)
            patch(p, 'QUADRANT_COLORS[v.quadrant]', 'QUADRANT_COLORS[QUADRANT_KEY(v.quadrant)]', 1)
        except SystemExit:
            ok = False

    # C：en methodology-matrix 阶段别名 + 双语 phase_analysis 形状归一
    try:
        patch(ROOT / "site/en/methodology-matrix.html", PHASE_DEF_EN_ANCHOR, PHASE_DEF_EN_NEW)
        patch(ROOT / "site/en/methodology-matrix.html", 'PHASE_COLORS[c.rescue_phase]', 'PHASE_COLORS[PHASE_KEY(c.rescue_phase)]', 1)
        patch(ROOT / "site/en/methodology-matrix.html", 'PHASE_COLORS[phase]', 'PHASE_COLORS[PHASE_KEY(phase)]', 1)
        patch(ROOT / "site/en/methodology-matrix.html", 'PHASE_COLORS[d.rescue_phase]', 'PHASE_COLORS[PHASE_KEY(d.rescue_phase)]', 1)
        patch(ROOT / "site/en/methodology-matrix.html", 'PHASE_COLORS[p.phase]', 'PHASE_COLORS[PHASE_KEY(p.phase)]', 1)
    except SystemExit:
        ok = False
    for rel in ("site/data/methodology-matrix.html", "site/en/methodology-matrix.html"):
        try:
            patch(ROOT / rel, MAIN_ANCHOR, MAIN_ANCHOR_NEW)
        except SystemExit:
            ok = False

    # D：en chart-design 怪物名别名
    try:
        patch(ROOT / "site/en/chart-design.html", MONSTER_DEF_EN, MONSTER_DEF_EN_NEW)
        patch(ROOT / "site/en/chart-design.html", 'MONSTER_COLORS[d.monster]', 'MONSTER_COLORS[MONSTER_KEY(d)]', 3)
    except SystemExit:
        ok = False

    # journey-spacetime 标记 fill 属性
    try:
        patch(ROOT / "site/data/journey-spacetime.html", MARKER_OLD, MARKER_NEW)
    except SystemExit:
        ok = False

    # tokens.css #7a5230 映射
    tp = ROOT / "site/tokens.css"
    t = tp.read_text(encoding="utf-8")
    if '[fill="#7a5230" i]' in t:
        print("SKIP tokens.css：#7a5230 映射已存在")
    elif TOKENS_ANCHOR not in t:
        print("FAIL tokens.css：锚点缺失")
        ok = False
    else:
        tp.write_text(t.replace(TOKENS_ANCHOR, TOKENS_NEW), encoding="utf-8", newline="")
        print("OK   tokens.css：#7a5230 映射 +1")

    print("RESULT:", "ALL OK" if ok else "HAS FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
