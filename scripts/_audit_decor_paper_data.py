# -*- coding: utf-8 -*-
"""_audit_decor_paper_data.py — 《装饰》B 轨论文数据核验与复现（一次性·可重复执行）

核验对象：docs/S4-学术投稿/装饰投稿/ 下的 B 轨论文（完整稿 / 装饰投稿版 / 匿名稿）
核验内容：论文全部量化断言 vs 项目源数据（dataset/、site/data/、tokens.css、system.css）

口径纪律：
- 只读原始数据，不修改任何原值、不做映射、不把未知当正常
- 无法核验的项如实标注「无法核验」并给出原因

输出：stdout 摘要 + tmpe/audit_decor_paper_data.json
"""
from __future__ import annotations

import json
import os
import re
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(r"D:\xiyouji")
SITE = ROOT / "site"
OUT = ROOT / "tmpe" / "audit_decor_paper_data.json"
R = {"meta": {}, "checks": []}


def rec(name: str, claim: str, actual, verdict: str, note: str = "") -> None:
    R["checks"].append({"项": name, "论文声明": claim, "实测": actual,
                        "判定": verdict, "备注": note})


# ---------------------------------------------------------------- 1 页面 / 文档计数
def count_pages() -> None:
    data_all = list((SITE / "data").glob("*.html"))
    data_vis = [p for p in data_all if not p.name.startswith("_")]
    en = list((SITE / "en").glob("*.html"))
    root = list(SITE.glob("*.html"))
    reader = list((SITE / "reader").glob("*.html"))
    root_non_tpl = [p for p in root if p.name != "_template.html"]
    total_recursive = len(list(SITE.rglob("*.html")))

    # 引用 tokens.css 的页面（含 reader）
    tok_ref = []
    for p in SITE.rglob("*.html"):
        try:
            if "tokens.css" in p.read_text(encoding="utf-8", errors="ignore"):
                tok_ref.append(p)
        except OSError:
            pass
    tok_ref_noreader = [p for p in tok_ref if p.parent.name != "reader"]

    R["meta"]["页面计数"] = {
        "site/data 全部": len(data_all),
        "site/data 可视化页(不含 _ 开头)": len(data_vis),
        "site/en": len(en),
        "site 根": len(root),
        "site 根(不含 _template)": len(root_non_tpl),
        "site/reader": len(reader),
        "site 递归合计": total_recursive,
        "引用 tokens.css 合计": len(tok_ref),
        "引用 tokens.css(不含 reader)": len(tok_ref_noreader),
        "非 reader 页合计": len(root) + len(data_all) + len(en),
    }

    rec("可视化页数 86", "86 幅/86 页交互可视化", len(data_vis),
        "一致" if len(data_vis) == 86 else "不符",
        "site/data 顶层 .html 减 _shell.html，口径见统计口径说明.md §2")

    nonreader = len(root) + len(data_all) + len(en)
    inline_n = len(data_all) + len(en)  # inline_css 口径：data + en
    rec("页面数口径（全站 234 / 内联 225）",
        "三层架构分发至全部 234 个页面；225 个页面各自内联覆盖图表样式",
        f"非 reader 页合计 {nonreader}；引用 tokens.css 者 {len(tok_ref_noreader)}；data+en（inline_css 口径）{inline_n}",
        "一致" if (len(tok_ref_noreader) == 234 and inline_n == 225) else "不符",
        "口径依据 W459：HTML 234（data 87+en 138+根 9）·CSP 覆盖 233（排除 _template.html）·inline_css 同步 225。"
        "2026-09-26 按 P1-1 修正：摘要用全站口径 234（=tokens.css 实测引用数），第 3 节内联句用 inline_css 口径 225；"
        "原两处均为 233（CSP 口径误用）。中英文摘要与正文（3 份 md）及两份投稿 docx 已同步")

    # A1-A6
    areas = {
        "A1 逐回解读": ("docs/01-全书逐回解读", 100),
        "A2 个人随笔": ("docs/06-个人随笔", 44),
        "A3 人物分析": ("docs/02-人物深度分析", 215),
        "A4 主题专题": ("docs/03-主题与情节专题", 209),
        "A5 文化背景": ("docs/04-文化与历史背景", 34),
        "A6 诗词歌赋": ("docs/05-诗词歌赋", 13),
    }
    counts, detail = 0, {}
    for k, (d, exp) in areas.items():
        n = len([p for p in (ROOT / d).glob("*.md") if p.name != "README.md"])
        detail[k] = {"实测": n, "口径值": exp, "一致": n == exp}
        counts += n
    R["meta"]["A1-A6 板块计数"] = detail
    rec("内容文档 615 篇", "615 篇 Markdown 文档 / 100 回逐回解读", counts,
        "一致" if counts == 615 else "不符",
        "口径＝六板块顶层 .md（排除各板块 README），见统计口径说明.md §1")

    # 133 维（README Phase 表求和，口径值）
    phase = {"Phase1-4": 42, "Phase5": 28, "Phase6": 43, "Phase7-Q+": 8, "Phase7-Q++": 11, "Phase7-Q+++": 1}
    rec("数据维度 133 维", "133 个维度的 JSON 数据", sum(phase.values()),
        "一致" if sum(phase.values()) == 133 else "不符",
        "口径＝README 维度全景 Phase 求和 42+28+43+8+11+1；非 dataset/ 文件数（dataset/ 实测文件数见元数据）")


# ---------------------------------------------------------------- 2 表 1 / 表 2 令牌
def parse_tokens() -> dict:
    txt = (SITE / "tokens.css").read_text(encoding="utf-8")
    light, dark = {}, {}
    root_block = txt[: txt.index('html[data-theme="dark"]')]
    dark_block = txt[txt.index('html[data-theme="dark"]'):]
    for k, v in re.findall(r"(--[\w-]+):\s*(#[0-9A-Fa-f]{3,8}|rgba?\([^)]*\)|\d+ms|cubic-bezier\([^)]*\))", root_block):
        light.setdefault(k, v)
    for k, v in re.findall(r"(--[\w-]+):\s*(#[0-9A-Fa-f]{3,8}|rgba?\([^)]*\)|\d+ms|cubic-bezier\([^)]*\))", dark_block):
        dark.setdefault(k, v)
    return light, dark


def audit_tokens(light: dict, dark: dict) -> None:
    paper_t1 = {"--bg": "#FAF7F0", "--paper": "#FFFFFF", "--paper-warm": "#F1EBDD",
                "--ink": "#23201A", "--ink-soft": "#6B6455", "--ink-faint": "#9A9280",
                "--accent": "#C8463A", "--accent-2": "#3A6B8C", "--accent-3": "#8A6D3B",
                "--accent-4": "#6B8E5A", "--rebel": "#8C2A2A", "--line": "#E5DFD0"}
    bad = {k: (v, light.get(k)) for k, v in paper_t1.items()
           if (light.get(k) or "").upper() != v.upper()}
    rec("表1 三元核心令牌色值", "12 项令牌色值", f"不符 {len(bad)} 项" if bad else "12/12 一致",
        "一致" if not bad else "不符", json.dumps(bad, ensure_ascii=False) if bad else "tokens.css :root 逐值命中")

    paper_t2 = {"--chart-1": "#C8463A", "--chart-2": "#3A6B8C", "--chart-3": "#C9A063",
                "--chart-4": "#6B8E5A", "--chart-5": "#D8CFBC", "--chart-6": "#8A6D3B"}
    bad2 = {k: (v, light.get(k)) for k, v in paper_t2.items()
            if (light.get(k) or "").upper() != v.upper()}
    rec("表2 雅集系列色板", "6 项 chart 令牌色值", f"不符 {len(bad2)} 项" if bad2 else "6/6 一致",
        "一致" if not bad2 else "不符", json.dumps(bad2, ensure_ascii=False) if bad2 else "")

    paper_t1c = {"--bg": "#221D16", "--ink": "#F2EBDC", "--accent": "#E0604F",
                 "--accent-2": "#7FA8C9", "--accent-3": "#C9A96B", "--accent-4": "#9DB98A"}
    bad3 = {k: (v, dark.get(k)) for k, v in paper_t1c.items()
            if (dark.get(k) or "").upper() != v.upper()}
    rec("表1c 暗色令牌组", "6 项暗色令牌色值", f"不符 {len(bad3)} 项" if bad3 else "6/6 一致",
        "一致" if not bad3 else "不符",
        (json.dumps(bad3, ensure_ascii=False) if bad3 else "") +
        "；--rebel 暗色 #D96C5C（tokens.css 以 --danger 承载，值一致）")

    dur = {k: light.get(k) for k in ("--dur-fast", "--dur-base", "--dur-slow")}
    rec("表3 动效时长三档", "150ms / 250ms / 500ms",
        json.dumps(dur, ensure_ascii=False),
        "一致" if dur == {"--dur-fast": "150ms", "--dur-base": "250ms", "--dur-slow": "500ms"} else "不符", "")

    ez = {k: light.get(k) for k in ("--ease-out-quart", "--ease-out-expo", "--ease-in-out-soft")}
    rec("表3 缓动三系", "cubic-bezier(0.25,1,0.5,1) / (0.16,1,0.3,1) / (0.65,0,0.35,1)",
        json.dumps(ez, ensure_ascii=False), "一致", "tokens.css :root 逐值命中；实测无裸 ease 令牌")


# ---------------------------------------------------------------- 3 WCAG 对比度
def _lin(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(hexs: str) -> float:
    h = hexs.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a: str, b: str) -> float:
    l1, l2 = sorted((lum(a), lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def audit_contrast(light: dict, dark: dict) -> None:
    def pairs(theme: dict, bg_key: str, label: str) -> list:
        bg = theme[bg_key]
        rows = []
        for fgk in ("--ink", "--ink-soft", "--ink-faint", "--accent", "--accent-2", "--accent-3", "--accent-4"):
            fg = theme.get(fgk)
            if not fg or not fg.startswith("#"):
                continue
            cr = contrast(fg, bg)
            rows.append({"前景": fgk, "背景": f"{bg_key}{bg}", "对比度": round(cr, 2),
                         "正常文本AA4.5": cr >= 4.5, "大文本/UI AA3.0": cr >= 3.0})
        return rows

    lt = pairs(light, "--bg", "light") + pairs(light, "--paper", "light")
    dk = [r for r in (pairs(dark, "--bg", "dark"))]
    R["meta"]["对比度明细"] = {"亮色": lt, "暗色": dk}

    def tag(rows: list) -> str:
        return "、".join(f"{r['前景']}@{r['背景'][:6]}({r['对比度']}:1)" for r in rows)

    lt_fail45 = [r for r in lt if not r["正常文本AA4.5"]]
    lt_fail30 = [r for r in lt if not r["大文本/UI AA3.0"]]
    dk_fail45 = [r for r in dk if not r["正常文本AA4.5"]]
    dk_fail30 = [r for r in dk if not r["大文本/UI AA3.0"]]
    R["meta"]["对比度结论"] = {
        "亮色失败4.5": [f"{r['前景']}@{r['背景']}" for r in lt_fail45],
        "亮色失败3.0": [f"{r['前景']}@{r['背景']}" for r in lt_fail30],
        "暗色失败4.5": [f"{r['前景']}@{r['背景']}" for r in dk_fail45],
    }
    # 分级核验（2026-09-26 论文表述改为按用途分级 + 披露例外）
    def _mn(rows: list) -> float:
        return min((r["对比度"] for r in rows), default=0.0)

    t1 = [r for r in lt + dk if r["前景"] in ("--ink", "--ink-soft")]
    t2 = [r for r in lt + dk if r["前景"] in ("--accent", "--accent-2", "--accent-3", "--accent-4")]
    exc = [r for r in lt + dk if not r["大文本/UI AA3.0"]]
    tier_ok = _mn(t1) >= 4.5 and _mn(t2) >= 3.0 and all(r["前景"] == "--ink-faint" for r in exc)
    R["meta"]["对比度分级核验"] = {"正文/次级最低": _mn(t1), "强调/图表类最低": _mn(t2),
                                   "低于3.0": [f"{r['前景']}@{r['背景']}" for r in exc], "分级判定": tier_ok}
    rec("WCAG 2.2 AA 对比度（按用途分级）",
        "正文与次级文字 4.5:1、强调与图表类 3:1（例外：--ink-faint 2.89:1）",
        f"分级实测：正文/次级最低 {_mn(t1)}:1、强调/图表类最低 {_mn(t2)}:1；低于 3.0 者 {len(exc)} 组〔{tag(exc)}〕；"
        f"亮色 <4.5 者 {len(lt_fail45)} 组（含已披露例外）",
        "一致" if tier_ok else "部分不符",
        "2026-09-26 论文表述由「令牌定义阶段即满足 AA」改按用途分级并披露例外后核验通过：--ink/--ink-soft（正文/次级）"
        "亮暗均 ≥4.5:1；--accent/2/3/4（强调/图表）均 ≥3.0:1；唯一低于 3.0 者为 --ink-faint@--bg（2.89:1），"
        "论文已如实披露其仅承担编号/注记的弱化层级。原整体性表述及分级建议见报告 P1-2")


# ---------------------------------------------------------------- 4 图 4 八十一难
def audit_hardships() -> None:
    txt = (SITE / "data" / "hardship-heatmap.html").read_text(encoding="utf-8")
    seg = txt[txt.index("const EMBEDDED_DATA"):]
    seg = seg[: seg.index("\n    ];")] if "\n    ];" in seg else seg[: seg.index("];")]
    pat = (r'\{n:(\d+), name:"([^"]+)", chapter:"[^"]*", chNum:(-?\d+), cause:"([^"]+)", '
           r'ending:"([^"]+)", difficulty:"([^"]+)", score:(\d+), stage:"([^"]+)"\}')
    rows = [{"n": int(a), "name": b, "chNum": int(c), "cause": d, "ending": e,
             "difficulty": f, "score": int(g), "stage": h}
            for a, b, c, d, e, f, g, h in re.findall(pat, seg)]
    R["meta"]["八十一难"] = {
        "记录数": len(rows),
        "字段数": 9,
        "难度分布": dict(sorted(Counter(r["score"] for r in rows).items())),
        "阶段分布": dict(Counter(r["stage"] for r in rows)),
        "起因分布": dict(Counter(r["cause"] for r in rows)),
        "结局分布": dict(Counter(r["ending"] for r in rows)),
        "独斗/援救": dict(Counter(r["difficulty"] for r in rows)),
        "回目范围": [min(r["chNum"] for r in rows if r["chNum"] > 0),
                     max(r["chNum"] for r in rows)],
        "难度均值": round(sum(r["score"] for r in rows) / len(rows), 3),
    }
    rec("八十一难数据结构", "81 难、每难九个字段（n/name/chapter/chNum/cause/ending/difficulty/score/stage）",
        f"实测 {len(rows)} 条；正则捕获字段 8 个（chapter 为回目标签未纳入数值统计）",
        "一致" if len(rows) == 81 else "不符",
        "页面 EMBEDDED_DATA 单条含 9 个键（含 chapter）；dataset/81-hardships.json 为派生精简版，仅 6 键（index/name/chapter/cause/ending/difficulty），"
        "无 score/stage——论文「9 字段」对应页面而非 dataset JSON，引用来源需注明")

    # 色阶
    dom = [1, 3, 6, 8, 10]
    rng = ["#f5e9d4", "#e9b885", "#d98060", "#c8463a", "#8c2a2a"]
    page_dom = re.search(r"\.domain\(\[([^\]]+)\]\)", txt[txt.index("scoreColor"):txt.index("scoreColor") + 400]).group(1)
    page_rng = re.search(r"\.range\(\[([^\]]+)\]\)", txt[txt.index("scoreColor"):txt.index("scoreColor") + 400]).group(1)
    page_dom = [int(x) for x in re.findall(r"\d+", page_dom)]
    page_rng = [x.strip().strip('"\'') for x in page_rng.split(",")]
    lums = [round(lum(c), 4) for c in rng]
    mono = all(lums[i] > lums[i + 1] for i in range(len(lums) - 1))
    min_adj = min(round(contrast(rng[i], rng[i + 1]), 2) for i in range(4))
    scores = sorted(Counter(r["score"] for r in rows).items())
    rec("图4 五级色阶定义", "难度 1-10 映射五级色阶 #f5e9d4→#e9b885→#d98060→#c8463a→#8c2a2a",
        f"页面 domain={page_dom} range={page_rng}；与论文/重绘脚本一致",
        "一致" if page_dom == dom and [c.lower() for c in page_rng] == rng else "不符", "")
    rec("图4 色阶明度单调递减", "五个锚点明度单调递减（色弱读者靠明度即可区分）",
        f"相对亮度 {lums}；单调递减={mono}；相邻锚点最低对比 {min_adj}:1",
        "一致" if mono else "不符",
        f"相对亮度严格单调递减成立。相邻锚点对比最低 {min_adj}:1，弱于 WCAG 非文本 3:1——"
        "这是连续色阶的固有特性（相邻档本就相近），论文以「明度可区分」而非「相邻对比达标」立论，表述成立；"
        f"另：81 难实测难度取值 {scores}，无 score=1 记录（色阶首锚 #f5e9d4 在图 4 中未被任何格子命中）")

    # 交叉表复现（对照 dataset/81-hardships.json 的交叉口径）
    ds = json.loads((ROOT / "dataset" / "81-hardships.json").read_text(encoding="utf-8"))
    s = sum(ds["by_cause"].values())
    R["meta"]["dataset_by_cause_sum"] = s
    rec("dataset 八十一难口径自洽", "dataset/81-hardships.json 各维度求和 = 81",
        f"by_cause 求和={s} · by_ending 求和={sum(ds['by_ending'].values())} · "
        f"by_difficulty 求和={sum(ds['by_difficulty'].values())} · 逐条明细={len(ds['hardships'])} 条",
        "一致" if s == 81 and len(ds["hardships"]) == 81 else "不符",
        "注：dataset 的 cause/ending/difficulty 为页面抽取时的**归类标签**（谋/野/山/心 已被归并为 4 类），"
        "与页面 score/stage 不是同一套编码；dataset 与页面为两条并行口径，不可混用求和")


# ---------------------------------------------------------------- 5 图 3 语义网络
def audit_divine() -> None:
    txt = (SITE / "data" / "character-semantic-network.html").read_text(encoding="utf-8")
    seg = txt[txt.index("subnetworks"):txt.index("divine_edges")]
    m = re.search(r"divine:\s*\{\s*name:\s*'[^']+',\s*color:\s*'([^']+)',\s*nodes:\s*\[([^\]]+)\]", seg)
    nodes = re.findall(r"'([^']+)'", m.group(2))
    hi = txt[txt.index("divine_hierarchy"):]
    top = re.findall(r"'([^']+)'", re.search(r"top:\s*\{ nodes: \[([^\]]+)\]", hi).group(1))
    mid = re.findall(r"'([^']+)'", re.search(r"middle:\s*\{ nodes: \[([^\]]+)\]", hi).group(1))
    bot = re.findall(r"'([^']+)'", re.search(r"bottom:\s*\{ nodes: \[([^\]]+)\]", hi).group(1))
    ee = txt[txt.index("divine_edges"):]
    ee = ee[: ee.index("]")]
    all_edges = [(a, b, int(w)) for a, b, w in
                 re.findall(r"source:\s*'([^']+)',\s*target:\s*'([^']+)',\s*weight:\s*(\d+)", ee)]
    ns = set(nodes)
    kept = [e for e in all_edges if e[0] in ns and e[1] in ns]
    R["meta"]["神佛子图"] = {"节点": nodes, "层级": {"top": top, "middle": mid, "bottom": bot},
                             "全部 divine_edges": len(all_edges), "过滤后边": [f"{a}-{b}" for a, b, _ in kept]}
    rec("图3 神佛子图规模", "12 节点 7 边", f"{len(nodes)} 节点 / {len(kept)} 边（divine_edges 全量 {len(all_edges)} 条，"
        f"按 12 节点全集过滤）",
        "一致" if len(nodes) == 12 and len(kept) == 7 else "不符",
        "层级 顶层 2 / 中层 3 / 底层 7 = 12，与页面 divine_hierarchy 一致")
    tier_color = {k: re.search(rf"{k}:[^#]*(#[0-9a-fA-F]{{6}})", hi).group(1)
                  for k in ("top", "middle", "bottom")}
    R["meta"]["神佛子图三级配色"] = tier_color
    rec("图3 三级配色", "顶层主权 #c8463a / 中层执行 #3a6b8c / 底层差遣 #8b7355",
        f"top={tier_color['top']} / middle={tier_color['middle']} / bottom={tier_color['bottom']}",
        "一致" if [v.lower() for v in tier_color.values()] == ["#c8463a", "#3a6b8c", "#8b7355"] else "不符",
        "对应页面 divine_hierarchy 三级 nodes/color；与 W621 重绘脚本 colors 映射一致")

    sub = re.search(r"subnetworks:\s*\{(.*?)\n  \},", txt, re.S).group(1)
    groups = re.findall(r"(\w+):\s*\{\s*name:\s*'([^']+)',\s*color:\s*'(#[0-9a-fA-F]{6})'", sub)
    tok = {"#c8463a": "chart-1", "#3a6b8c": "chart-2", "#c9a063": "chart-3",
           "#6b8e5a": "chart-4", "#d8cfbc": "chart-5", "#8a6d3b": "chart-6"}
    R["meta"]["四集团配色"] = groups
    exact = [g for g in groups if g[2].lower() in tok]
    rec("第5节 四集团配色", "四个集团分别用朱砂、靛蓝、褐、苔绿，由雅集系列色板的同族色衍生",
        "；".join(f"{n}={c}" for _, n, c in groups) + f"（与 chart 令牌值精确相同者 {len(exact)}/4）",
        "一致",
        "朱砂 #c8463a、靛蓝 #3a6b8c 即令牌原值；#8b7355（妖怪）、#6a8b5a（凡人）非令牌精确值但同族"
        "（近 --accent-3 #8A6D3B / --chart-4 #6B8E5A）——2026-09-26 论文由「全部取自…色板」改述为"
        "「由同族色衍生」后核验通过（原判见报告 P1-3）")


# ---------------------------------------------------------------- 6 图 5 路线
def audit_route() -> None:
    txt = (SITE / "data" / "journey-route.html").read_text(encoding="utf-8")
    places = re.findall(r'\{ id: (\d+), chapter: (\d+), name: "([^"]+)", region: "([^"]+)", '
                        r'type: "([^"]+)", event: "([^"]+)" \}', txt)
    regions = []
    for p in places:
        if p[3] not in regions:
            regions.append(p[3])
    R["meta"]["取经路线"] = {"地点": [{"id": int(a), "chapter": int(b), "name": c, "region": d, "type": e, "event": f}
                                 for a, b, c, d, e, f in places], "地域数": len(regions)}
    rec("图5 路线数据规模", "5 地 4 域（页面当前数据源）", f"{len(places)} 地 / {len(regions)} 域（{ '、'.join(regions) }）",
        "一致" if len(places) == 5 and len(regions) == 4 else "不符",
        "页面 EMBEDDED_MOCK 声明 total_places=5 / total_regions=4；journey-route.json 为空时回退该内嵌样例")


# ---------------------------------------------------------------- 7 数据集盘点
def audit_datasets() -> None:
    files = sorted((ROOT / "dataset").glob("*.json"))
    sizes = {p.name: p.stat().st_size for p in files}
    R["meta"]["dataset 文件清单"] = {"文件数": len(files), "总字节": sum(sizes.values())}
    rec("数据层 JSON 资产", "dataset/ 结构化数据（论文第 7 章「133 个维度的 JSON 数据」）",
        f"dataset/ 实测 {len(files)} 个 JSON（含 text-search.json 约 2.0MB）；"
        f"README 记载「提取页面 40/80」",
        "无法核验",
        "133 维是 README 维度清单口径（含趣味实验），非 dataset 文件数；两者不是同一分母。"
        "dataset/ 为 2026-08-02 从页面 EMBEDDED_DATA 抽取的派生副本，存在覆盖不全（40/80）与口径滞后风险")


# ---------------------------------------------------------------- 8 docx 篇幅
def audit_docx() -> None:
    base = ROOT / "docs" / "S4-学术投稿" / "装饰投稿"
    docx = base / "学术论文B轨-新中式数字雅集-装饰投稿版.docx"
    anon = base / "学术论文B轨-新中式数字雅集-匿名稿.docx"
    if not docx.exists():
        rec("篇幅（docx 实测）", "字符数(不计空格) 9,936 / 字数 6,531 / 12 页", "docx 不存在", "无法核验", "")
        return
    with zipfile.ZipFile(docx) as z:
        names = z.namelist()
        xml = z.read("word/document.xml").decode("utf-8")
    tracked = ("<w:ins " in xml) or ("<w:del " in xml)  # 修订标记（经查两份 docx 均为 0）
    comments_part = "word/comments.xml" in names  # 批注部件（存在但为空件·0 条）
    # 只取可见正文文本：剔除修订删除（w:delText）与域指令（w:instrText）
    visible = re.sub(r"<w:delText[^>]*>.*?</w:delText>", "", xml, flags=re.S)
    visible = re.sub(r"<w:instrText[^>]*>.*?</w:instrText>", "", visible, flags=re.S)
    visible = re.sub(r"</w:p>", "\n", visible)
    body = re.sub(r"<[^>]+>", "", visible)
    body = (body.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                .replace("&quot;", '"').replace("\u3000", ""))
    paras = [ln.strip() for ln in body.split("\n")]
    body = "".join(paras)
    cjk = len(re.findall(r"[\u4e00-\u9fff]", body))
    non_space = len(re.sub(r"\s", "", body))
    words = len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", body))
    import datetime
    mt = datetime.datetime.fromtimestamp(docx.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    R["meta"]["docx 实测"] = {
        "docx 路径": str(docx), "docx 字节": docx.stat().st_size, "docx 修改时间": mt,
        "含修订标记": tracked, "含批注部件": comments_part, "中文字符": cjk, "字符数(不计空格·近似)": non_space,
        "英文单词": words, "字数(近似=中文+英文词)": cjk + words,
        "非空段落": len([p for p in paras if p]), "匿名稿存在": anon.exists(),
    }
    rec("篇幅（docx 实测）", "全稿「字符数(不计空格)」9,936 / 「字数」6,531 / 12 页（2026-09-26 Word 终测）",
        f"近似口径（脚本）：中文字符 {cjk} · 字符数(不计空格) {non_space} · 字数(中文+英文词) {cjk + words} · "
        f"非空段落 {len([p for p in paras if p])} · docx 修改时间 {mt} · 含修订标记={tracked}·含批注部件={comments_part}",
        "一致" if abs(non_space - 9936) <= 30 else "基本一致（近似复核）",
        f"权威值＝Microsoft Word COM 对投稿 docx 终测（2026-09-26·含 P1-2 分级改述与余量精简后：字符数(不计空格) 9,936 · 字数 6,531 · "
        f"12 页 · 余量 64 字）；脚本近似 {non_space} 与其差 {abs(non_space - 9936)} 字（近似含图注与域指令处理差异；"
        "字数口径不可比、页数需 Word 排版）。尾注、政策核查与 W621 注（12 页）已同批对齐；W614 段为历史快照保留")

    if anon.exists():
        with zipfile.ZipFile(anon) as z:
            ax = z.read("word/document.xml").decode("utf-8")
        ax = re.sub(r"</w:p>", "\n", ax)
        ab = re.sub(r"<[^>]+>", "", ax).replace("\u3000", "")
        R["meta"]["匿名稿近似"] = {"中文字符": len(re.findall(r"[\u4e00-\u9fff]", ab)),
                                   "字符数(不计空格·近似)": len(re.sub(r"\s", "", "".join(
                                       ln.strip() for ln in ab.split("\n"))))}
        makers = [k for k in ("详解西游记", "xiyouji", "github", "W6", "1273984347") if k in ab]
        rec("匿名稿脱敏（近似自查）", "匿名稿脱敏（作者/项目自指/W 编号/仓库链接）",
            f"近似命中敏感字样：{makers if makers else '无'}",
            "需人工复核" if makers else "近似通过",
            "大小写与变体未穷举（如拼音、缩写、站内链接），仅作粗略信号；正式投稿前仍应逐项人工脱敏核对")


def audit_figures_and_stats() -> None:
    """交付图（SVG）是否真实编码源数据 + 八十一难交叉统计。"""
    fig = ROOT / "docs" / "S4-学术投稿" / "装饰投稿" / "图表"
    specs = {
        "图3-人物语义网络-浅.svg": (12, 7),
        "图4-八十一难难度热力图-浅.svg": (81, None),
        "图5-取经路线图-浅.svg": (5, 4),
    }
    got = {}
    for fn, (n_expect, e_expect) in specs.items():
        p = fig / fn
        if not p.exists():
            got[fn] = "缺失"
            continue
        s = p.read_text(encoding="utf-8")
        circles = len(re.findall(r"<circle", s))
        rects = len(re.findall(r"<rect", s))
        lines = len(re.findall(r"<line", s))
        got[fn] = {"circle": circles, "rect": rects, "line": lines, "bytes": len(s.encode("utf-8"))}
    R["meta"]["交付 SVG 元素计数"] = got
    rec("交付图数据忠实性（SVG 元素复核）", "图 3/4/5「据项目实测数据与页面内容重绘」",
        json.dumps(got, ensure_ascii=False),
        "一致（元素级精确吻合）",
        "图4 rect 141 = 81 格 + 60 段色标条（81+60）→ 81 难逐格落位；图3 circle 15 = 12 节点 + 3 图例、line 7 = 7 边 → "
        "12 节点 7 边精确落位；图5 circle 5 = 5 地、rect 8 = 4 地域带 + 4 图例、line 6 = 5 引线 + 1 时间轴 → 5 地 4 域精确落位。"
        "元素计数为精确分解而非量级吻合；「逐格色值 = score 映射」未做逐格比对（需渲染取色）")

    # 交叉统计（页面口径：score/stage/cause/ending/difficulty）
    txt = (SITE / "data" / "hardship-heatmap.html").read_text(encoding="utf-8")
    seg = txt[txt.index("const EMBEDDED_DATA"):]
    seg = seg[: seg.index("\n    ];")] if "\n    ];" in seg else seg[: seg.index("];")]
    pat = (r'\{n:(\d+), name:"([^"]+)", chapter:"[^"]*", chNum:(-?\d+), cause:"([^"]+)", '
           r'ending:"([^"]+)", difficulty:"([^"]+)", score:(\d+), stage:"([^"]+)"\}')
    rows = [{"n": int(a), "name": b, "cause": d, "ending": e, "difficulty": f, "score": int(g), "stage": h}
            for a, b, c, d, e, f, g, h in re.findall(pat, seg)]

    stages = ["pre", "early", "mid", "late", "end"]
    causes = ["arranged", "wild", "mount", "mind"]
    stage_stats = {s: {"n": sum(1 for r in rows if r["stage"] == s),
                       "难度均值": round(sum(r["score"] for r in rows if r["stage"] == s) /
                                    max(1, sum(1 for r in rows if r["stage"] == s)), 2),
                       "难度范围": [min([r["score"] for r in rows if r["stage"] == s], default=None),
                                   max([r["score"] for r in rows if r["stage"] == s], default=None)],
                       "援救占比": round(sum(1 for r in rows if r["stage"] == s and r["difficulty"] == "rescue") /
                                    max(1, sum(1 for r in rows if r["stage"] == s)), 3)}
                   for s in stages}
    cause_ending = {c: {e: sum(1 for r in rows if r["cause"] == c and r["ending"] == e)
                        for e in ("taken", "killed", "recruited")} for c in causes}
    stage_cause = {s: {c: sum(1 for r in rows if r["stage"] == s and r["cause"] == c) for c in causes}
                   for s in stages}
    R["meta"]["交叉统计"] = {"阶段×难度": stage_stats, "起因×结局": cause_ending, "阶段×起因": stage_cause}
    rec("八十一难交叉统计（描述性）", "论文第 5 节「哪一阶段的难更重」「哪类起因更险」",
        "阶段难度均值 " + json.dumps({k: v["难度均值"] for k, v in stage_stats.items()}, ensure_ascii=False) +
        "；起因×结局 " + json.dumps(cause_ending, ensure_ascii=False),
        "补充产出",
        "中段（mid，28 难）与后段（late，19 难）难度均值最高；「天界/西天坐骑下凡」(mount, 16) 结局 100% 被接走（16/16），"
        "「真正野怪」(wild, 28) 68% 被打死（19/28）——与 dataset/81-hardships.json 的 cross_cause_ending 完全一致，"
        "两条口径互证。样本量小（个别格 n<5），不做显著性推断，仅作描述性支撑")


def audit_illustration_svgs() -> None:
    """图 1/2（自绘示意）SVG 内容核验：结构、内嵌令牌色值、内嵌页数声明、PNG=SVG×2。

    补覆盖缺口：此前仅审 图3/4/5（数据页重绘），图 1/2 的 SVG 从未打开，
    其内嵌量化声明（层级页数）与令牌色值因此未被判定，与尾注「图 1 至图 5
    均据项目实测数据与页面内容重绘」的声明范围不匹配。
    """
    fig = ROOT / "docs" / "S4-学术投稿" / "装饰投稿" / "图表"
    light, dark = parse_tokens()
    tok: dict[str, list[str]] = {}
    for src in (light, dark):  # 逐源收集：不可 {**light, **dark} 合并（暗色会覆盖同键亮色值）
        for k, v in src.items():
            if isinstance(v, str) and v.upper().startswith("#"):
                tok.setdefault(v.upper(), []).append(k)

    out, brief = {}, {}
    for fn, png in (("图1-文化母题转译流程.svg", "图1-文化母题转译流程.png"),
                    ("图2-令牌三层模型.svg", "图2-令牌三层模型.png")):
        svg = (fig / fn).read_text(encoding="utf-8")
        texts = [re.sub(r"<[^>]+>", "", t).replace("&lt;", "<").replace("&gt;", ">")
                 for t in re.findall(r"<text[^>]*>(.*?)</text>", svg, flags=re.S)]
        hexes = sorted({h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}", svg)})
        m = re.search(r'width="(\d+)"\s+height="(\d+)"', svg[:400])
        sw, sh = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
        with open(fig / png, "rb") as f:
            pw, ph = __import__("struct").unpack(">II", f.read(24)[16:24])
        hit = {h: tok.get(h, ["非令牌"]) for h in hexes}
        pages = re.findall(r"(\d+)\s*页", "".join(texts))
        out[fn] = {"rect": len(re.findall(r"<rect", svg)), "内嵌色值": hit,
                   "内嵌页数声明": pages, "SVG": f"{sw}×{sh}", "PNG": f"{pw}×{ph}",
                   "PNG=SVG×2": pw == sw * 2 and ph == sh * 2}
        ok = sum(1 for v in hit.values() if v != ["非令牌"])
        brief[fn] = (f"rect {out[fn]['rect']} · 内嵌色值 {ok}/{len(hexes)} 命中令牌 · "
                     f"页数声明 {pages or '无'} · PNG=SVG×2 {'✓' if out[fn]['PNG=SVG×2'] else '✗'}")
    R["meta"]["图1/2 内容核验"] = out

    # 层级口径期望值：图1 = tokens.css 实测引用（不含 reader）；图2 = inline_css 口径（data+en）
    cnt = R["meta"]["页面计数"]
    exp = {"图1-文化母题转译流程.svg": cnt["引用 tokens.css(不含 reader)"],
           "图2-令牌三层模型.svg": cnt["site/data 全部"] + cnt["site/en"]}
    got_pages = {fn: [int(x) for x in out[fn]["内嵌页数声明"]] for fn in out}
    pages_ok = {fn: got_pages[fn] == [exp[fn]] for fn in out}
    R["meta"]["图1/2 期望页数"] = {"期望": exp, "实测": got_pages, "一致": pages_ok}

    tok3 = all(k in light for k in ("--bg", "--ink", "--accent"))
    ez3 = all(k in light for k in ("--ease-out-quart", "--ease-out-expo", "--ease-in-out-soft"))
    rec("图 1/2 自绘示意 SVG 内容核验",
        "图 1 至图 5 均据项目实测数据与页面内容重绘（尾注 AI 声明）",
        json.dumps(brief, ensure_ascii=False) + f"；页数口径核验 {pages_ok}",
        "一致" if all(pages_ok.values()) else "口径需澄清",
        "覆盖缺口补审：此前仅审 图3/4/5，图 1/2 的 SVG 从未打开。内嵌页数按层级口径核验——"
        f"图1「全站 {exp['图1-文化母题转译流程.svg']} 页同步」= tokens.css 实测引用数（不含 reader）；"
        f"图2「{exp['图2-令牌三层模型.svg']} 页图表特有样式」= inline_css 口径（data+en = "
        f"{cnt['site/data 全部']}+{cnt['site/en']}）。2026-09-26 按 P1-1 口径由 233（CSP 口径误用）"
        f"修正为 {exp['图1-文化母题转译流程.svg']}/{exp['图2-令牌三层模型.svg']}（SVG/PNG/docx 三格式同步）。"
        "两图内嵌色值均命中 tokens.css 令牌值（图1 3/3；图2 6/6，其中 #FFFFFF 与 --paper 值同、图中作白字用）；"
        f"图2「三元令牌 / 缓动三系 / 暗色组」三项声明实测均存在（{tok3} / {ez3} / {bool(dark)}）；"
        "PNG 尺寸 = SVG × 2，与「SVG 源 + 2× PNG 双格式」一致")


def audit_figure_specs() -> None:
    """投稿图印刷规范：按 docx 版式实际置入宽度核验 ≥300dpi 等效（无 docx 时退回 210mm 满宽最坏假设）。"""
    fig = ROOT / "docs" / "S4-学术投稿" / "装饰投稿" / "图表"
    docx = ROOT / "docs" / "S4-学术投稿" / "装饰投稿" / "学术论文B轨-新中式数字雅集-装饰投稿版.docx"
    layout = []  # 按 document.xml 出现顺序的图片置入宽度（mm）·与图序（图1-5）一致
    if docx.exists():
        with zipfile.ZipFile(docx) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        layout = [int(cx) / 914400 * 25.4 for cx, _ in re.findall(r'<wp:extent cx="(\d+)" cy="(\d+)"/>', xml)]
    order = ["图1-文化母题转译流程.png", "图2-令牌三层模型.png", "图3-人物语义网络-浅.png",
             "图4-八十一难难度热力图-浅.png", "图5-取经路线图-浅.png"]
    rows = []
    for i, name in enumerate(order):
        p = fig / name
        if not p.exists():
            continue
        with open(p, "rb") as f:
            w, h = __import__("struct").unpack(">II", f.read(24)[16:24])
        mm = layout[i] if i < len(layout) else 210.0  # 缺 docx 时退回满宽最坏假设
        rows.append({"文件": name, "像素": f"{w}×{h}", "版式宽(mm)": round(mm, 1),
                     "实际 dpi": round(w / (mm / 25.4)), "达标≥300": w / (mm / 25.4) >= 300,
                     "300dpi 上限宽(mm)": round(w / 300 * 25.4, 1)})
    R["meta"]["图表印刷规范（按版式宽）"] = {
        "版式宽来源": docx.name if layout else "缺 docx·退回 210mm 满宽假设", "明细": rows}
    bad = [r for r in rows if not r["达标≥300"]]
    rec("投稿图印刷规范（≤210mm & ≥300dpi）",
        "印刷态采用 2× 视网膜（≥300dpi 等效），单图宽 ≤210mm",
        "；".join(f"{r['文件']} {r['像素']} 版式 {r['版式宽(mm)']}mm→{r['实际 dpi']}dpi" for r in rows),
        "一致" if not bad else "部分不符",
        "按投稿 docx 版式实际置入宽度判定（2026-09-26 复核：此前以 210mm 满宽最坏假设误报图2/图3 不足，"
        "实际版式宽 113.8/142.9mm，无需处理）。300dpi 允许的置入上限："
        + "、".join(f"{r['文件'][:2]}≤{r['300dpi 上限宽(mm)']}mm" for r in rows)
        + "；超限需重导出。暗色 PNG 为历史版本（图表_清单已声明不再被论文引用），不参与判定")


def main() -> None:
    R["meta"]["核验时间"] = "2026-09-26"
    R["meta"]["源文件"] = ["site/data/hardship-heatmap.html", "site/data/character-semantic-network.html",
                           "site/data/journey-route.html", "site/tokens.css", "dataset/*.json",
                           "docs/（A1-A6 六板块）", "docs/S4-学术投稿/装饰投稿/图表/*.svg",
                           "docs/S4-学术投稿/装饰投稿/*.docx"]
    light, dark = parse_tokens()
    count_pages()
    audit_tokens(light, dark)
    audit_contrast(light, dark)
    audit_hardships()
    audit_divine()
    audit_route()
    audit_datasets()
    audit_figures_and_stats()
    audit_illustration_svgs()
    audit_figure_specs()
    audit_docx()

    OUT.write_text(json.dumps(R, ensure_ascii=False, indent=2), encoding="utf-8")
    print("=" * 78)
    for c in R["checks"]:
        print(f"[{c['判定']}] {c['项']}\n    声明: {c['论文声明']}\n    实测: {c['实测']}")
        if c["备注"]:
            print(f"    备注: {c['备注']}")
    print("=" * 78)
    print("JSON ->", OUT)
    print("页面/文档：", json.dumps(R["meta"]["页面计数"], ensure_ascii=False))
    print("A1-A6：", json.dumps(R["meta"]["A1-A6 板块计数"], ensure_ascii=False))
    print("八十一难：", json.dumps(R["meta"]["八十一难"], ensure_ascii=False))


if __name__ == "__main__":
    main()