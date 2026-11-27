"""W1327/W1328 页脚同类关联链接生成器（正本=本文件内规则，改推荐口径只改这里）。

来源（两段式，W1328 扩）：
  ① 看板专题卡：site/dashboard.html 的 href=data/xxx.html + data-category（45 页）；
  ② 文件名族：不在看板卡上的 site/data 内容页按族归组（关系网络 / 人物与文风 /
     地理与行程 / 叙事与文本 / 专题图谱 / 交互工具与导航）。
规则：组内按页面顺序循环取后 3 页（自页排除）；组成员 < 4 时取 n-1 条。
注入：目标页 <footer class="site-footer"> 内、现有页脚导航之后，带 MARK 便于幂等重放；
     看板类别的标签是指向 dashboard.html#cat=<类别> 的深链（W1328 交互），族标签为纯文本。

用法：
  python scripts/w1327_related_links.py --dry-run    # 打印计划，不写盘
  python scripts/w1327_related_links.py --apply      # 注入/更新（幂等：重放零漂移）
  python scripts/w1327_related_links.py --check      # 门禁：覆盖/条数/自页排除/可达性/分类一致

判定口径说明：
  - 「关联」= 同看板类别或同文件名族（不新增人工标签表；族规则显式声明在本文件）；
  - 链接只用 file:// 相对路径（与目标页同目录，site/data/ 内直链）；
  - 不新增 CSS：复用 .site-footer nav / .footer-meta 既有样式（零外域、零内联脚本）。
"""
import io
import re
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DATA = SITE / "data"
DASH = SITE / "dashboard.html"
MARK = "<!-- RELATED-LINKS v1 w1327 -->"
MAX_LINKS = 3
NAV_LABEL = "同类可视化推荐"
DASH_LINK = "../dashboard.html#cat="

# 数据中枢 5 个工具页：整页无 site-footer（独立工具布局，非内容页），不注入；
# check 模式反向锁死：这 5 页必须仍无 footer 且无 MARK——若某页后续长出 footer，
# 判据立即转红，强制重评而不是静默漏配。
NO_FOOTER = {
    "81-hardships-view.html",
    "character-relationship-3d-view.html",
    "data-explorer.html",
    "graph-explorer.html",
    "search.html",
}

# 看板 filter-tab 的 data-label（正本=dashboard.html 筛选条；此处显式声明，
# 避免从 HTML 反解析 data-label 时因按钮文案（含计数）漂移而静默错配）。
CAT_NAMES = {
    "a-l": "A-L 基础",
    "m-u": "M-U 扩展",
    "v-ah": "V-AH 跨学科",
    "q-plus": "Q+ 批评史",
    "q-plusplus": "Q++ 弹幕博物馆",
    "q-plusplusplus": "Q+++ v2.0 新功能",
    "data": "数据中枢",
}
# 只有筛选条上真实存在的类别才能深链；data 中枢卡不在 #topic-grid 内、无对应 tab。
FILTER_CATS = frozenset(CAT_NAMES) - {"data"}

# W1328：非看板页的文件名族（每页必须恰好命中 1 族·parse 期断言）。
FAMILIES = {
    "关系网络": lambda n: "network" in n or n in {
        "character-relationship-3d.html",
        "character-relationship-3d-view.html",
        "graph-explorer.html",
    },
    "人物与文风": lambda n: n in {
        "character-presence-timeline.html",
        "character-sentiment-arc.html",
        "dialogue-sentiment.html",
        "language-style-radar.html",
        "wukong-tangseng-benchmark.html",
        "pilgrim-team-psychology-arc.html",
    },
    "地理与行程": lambda n: n.startswith("journey-") or n == "customs-pass-route.html",
    "叙事与文本": lambda n: n in {
        "chapter-structure-graph.html",
        "narrative-rhythm-curve.html",
        "story-timeline.html",
        "poetry-density.html",
        "poetry-rhythm-analysis.html",
    },
    "专题图谱": lambda n: n in {
        "four-heavenly-kings-artifacts.html",
        "ming-political-thought-comparison.html",
        "glossary.html",
        "hardship-difficulty-heatmap.html",
        "monster-capability-radar.html",
    },
    "交互工具与导航": lambda n: n in {
        "tag-cloud.html",
        "perf-canvas-rendering.html",
        "81-hardships-view.html",
        "data-explorer.html",
        "search.html",
    },
}

CARD = re.compile(r'<a class="kpi-card"[^>]*?href="data/([^"]+\.html)"[^>]*?data-category="([^"]+)"[^>]*>(.*?)</a>', re.S)
LABEL = re.compile(r'<div class="label">(.*?)</div>', re.S)
IDX = re.compile(r'^[A-Z]{1,2}\+{0,3}\s*·\s*')
FOOTER = re.compile(r'(<footer class="site-footer">)(.*?)(</footer>)', re.S)


def _page_title(page):
    """导航标签：优先取 <title> 的专题名（W1347 标题结论化后 h1 已换成结论句，不再适合做链接名）。

    <title> 现役两种形态：「专题名：结论 · 详解西游记」与旧的「专题名 · 详解西游记」，
    统一剥掉「 · 详解西游记」后缀与「：结论」段；解析失败才退化到 h1 首段。
    """
    txt = (DATA / page).read_text(encoding="utf-8")
    tm = re.search(r"<title>(.*?)</title>", txt, re.S)
    if tm:
        t = re.sub(r"\s*[·|]\s*详解西游记\s*$", "", tm.group(1).strip()).strip()
        t = t.split("：", 1)[0].strip()
        if t and "<" not in t:
            return t
    m = re.search(r"<h1[^>]*>(.*?)</h1>", txt, re.S)
    raw = m.group(1) if m else ""
    title = re.split(r"<", raw, maxsplit=1)[0].strip()
    return title or page


def parse_cards():
    """dashboard → 有序 [类别 → [(页面, 标题)]]，顺序即看板呈现顺序。"""
    txt = DASH.read_text(encoding="utf-8")
    cats = {}
    seen = set()
    for m in CARD.finditer(txt):
        page, cat, body = m.group(1), m.group(2), m.group(3)
        if cat not in CAT_NAMES:
            raise SystemExit(f"FAIL 未知类别 {cat}（页 {page}）：请先补 CAT_NAMES")
        lm = LABEL.search(body)
        if not lm:
            raise SystemExit(f"FAIL 卡片缺 .label：{page}")
        # 标签文本在徽章 <span> 之前（如「A · 章节统计<span class=…>A-L</span>」）⇒ 截断取前缀；
        # 不再用整行标签剥标签正则（跨行改写门禁会判高危候选·且此处本就无其它内联标签）。
        title = re.split(r"<span\b", lm.group(1), maxsplit=1)[0].strip()
        title = IDX.sub("", title).strip()
        if not title or "<" in title:
            raise SystemExit(f"FAIL 卡片标题解析异常：{page} → {title!r}")
        if page in seen:
            continue
        seen.add(page)
        cats.setdefault(cat, []).append((page, title))
    return cats


def parse_groups():
    """看板类别 ∪ 文件名族 → 全量分组；非看板页必须恰好命中 1 族。"""
    dash = parse_cards()
    dash_pages = {p for items in dash.values() for p, _ in items}
    fams = {}
    for f in sorted(DATA.glob("*.html")):
        page = f.name
        if page == "_shell.html" or page in dash_pages:
            continue
        hits = [name for name, rule in FAMILIES.items() if rule(page)]
        if len(hits) != 1:
            raise SystemExit(f"FAIL 文件名族归属异常：{page} 命中 {hits}（应恰 1 族）")
        fams.setdefault(hits[0], []).append((page, _page_title(page)))
    groups = dict(dash)
    groups.update(fams)
    return groups


def related_for(cat, page):
    items = [p for p, _ in parse_cache[cat]]
    n = len(items)
    i = items.index(page)
    take = min(MAX_LINKS, n - 1)
    out = []
    for k in range(1, take + 1):
        out.append(items[(i + k) % n])
    return out


def _label(cat):
    name = CAT_NAMES.get(cat, cat)
    if cat in FILTER_CATS:
        return f'<a class="footer-meta" href="{DASH_LINK}{cat}">同类 · {name}</a>'
    return f'<span class="footer-meta">同类 · {name}</span>'


def build_block(cat, page):
    links = related_for(cat, page)
    titles = dict(parse_cache[cat])
    lines = [
        f"        {MARK}",
        f'        <nav class="footer-related" aria-label="{NAV_LABEL}">',
        f"            {_label(cat)}",
    ]
    for t in links:
        lines.append(f'            <a class="footer-related-link" href="{t}">{titles[t]}</a>')
    lines.append("        </nav>")
    return "\n".join(lines)


def process(txt, block):
    action = "insert"
    if MARK in txt:
        # 旧块整体扣出（含行首缩进与紧贴的 </footer> 前空白），统一交由下方重插，
        # 保证人工改过缩进/换行后重放仍归一到同一形态。
        txt, n = re.subn(
            r"[ \t]*" + re.escape(MARK) + r".*?</nav>\s*(?=</footer>)",
            "", txt, count=1, flags=re.S,
        )
        if not n:
            return txt, "mark-broken"
        action = "update"
    fm = FOOTER.search(txt)
    if not fm:
        return txt, "no-footer"
    im = re.search(r"\n([ \t]*)<footer class=\"site-footer\">", txt)
    indent = im.group(1) if im else ""
    end = fm.start(3)
    pre = txt[:end].rstrip()
    new = pre + "\n" + block + "\n" + indent + txt[end:]
    return new, action


def _check_no_footer(page, txt, stats, fail):
    if FOOTER.search(txt):
        fail.append(f"{page}: 已长出 site-footer，NO_FOOTER 豁免需重评")
    if MARK in txt:
        fail.append(f"{page}: 无 footer 页出现 MARK")
    stats["skip-no-footer"] = stats.get("skip-no-footer", 0) + 1


def _drift_reason(page, action, had_crlf):
    if had_crlf:
        return f"{page}: 行尾为 CRLF（.gitattributes 契约为 LF）"
    if action == "insert":
        return f"{page}: 缺注入块（跑 --apply 生成）"
    return f"{page}: 注入块与生成器派生值不一致（人工改动或生成器漂移）"


def _process_page(mode, cat, page, stats, changed, fail):
    f = DATA / page
    if not f.is_file():
        fail.append(f"缺页 {page}（分类指向不存在文件）")
        return
    txt = f.read_text(encoding="utf-8")
    had_crlf = b"\r\n" in f.read_bytes()
    if page in NO_FOOTER:
        _check_no_footer(page, txt, stats, fail)
        return
    new, action = process(txt, build_block(cat, page))
    stats[action] = stats.get(action, 0) + 1
    if action == "mark-broken":
        fail.append(f"{page}: MARK 存在但其后无 </nav>（块结构损坏·人工修复后再跑）")
        return
    # .gitattributes 契约为 eol=lf（全仓 blob 与工作树皆 LF）⇒ 内容未变但行尾为
    # CRLF 时同样回写归一，防「纯追加 diff 却整文件翻行尾」污染与门禁误判。
    if new != txt or had_crlf:
        changed.append(page)
        if mode == "--apply":
            f.write_text(new, encoding="utf-8", newline="\n")
        elif mode == "--check":
            fail.append(_drift_reason(page, action, had_crlf))


def _scan_pages(mode, page_cat):
    stats, changed, fail = {}, [], []
    for cat, items in parse_cache.items():
        for page, _ in items:
            _process_page(mode, cat, page, stats, changed, fail)
    return stats, changed, fail


def _check_hrefs(page, cat, hrefs, page_cat):
    out = []
    for h in hrefs:
        if not (DATA / h).is_file():
            out.append(f"{page}: 死链 {h}")
        if page_cat.get(h) != cat:
            out.append(f"{page}: {h} 分组不一致（{page_cat.get(h)} ≠ {cat}）")
    return out


def _check_label(page, cat, blk):
    name = CAT_NAMES.get(cat, cat)
    if f"同类 · {name}" not in blk:
        return [f"{page}: 类别标签缺失"]
    if cat in FILTER_CATS and f'href="{DASH_LINK}{cat}"' not in blk:
        return [f"{page}: 看板深链缺失（{DASH_LINK}{cat}）"]
    if cat not in FILTER_CATS and '<span class="footer-meta">' not in blk:
        return [f"{page}: 族标签应为纯文本 span"]
    return []


def _check_one(page, cat, expect, page_cat):
    f = DATA / page
    if not f.is_file():
        return []
    txt = f.read_text(encoding="utf-8")
    cnt = txt.count(MARK)
    if cnt != 1:
        return [f"{page}: MARK 出现 {cnt} 次（应 1）"]
    m = re.search(re.escape(MARK) + r".*?</nav>", txt, re.S)
    if not m:
        return [f"{page}: MARK 后无 </nav>（块结构损坏）"]
    blk = m.group(0)
    hrefs = re.findall(r'<a class="footer-related-link" href="([^"]+)">', blk)
    fail = []
    if len(hrefs) != expect:
        fail.append(f"{page}: 链接 {len(hrefs)} 条（应 {expect}）")
    if page in hrefs:
        fail.append(f"{page}: 含自页链接")
    fail.extend(_check_hrefs(page, cat, hrefs, page_cat))
    fail.extend(_check_label(page, cat, blk))
    return fail


def _check_coverage(page_cat):
    fail = []
    for cat, items in parse_cache.items():
        expect = min(MAX_LINKS, len(items) - 1)
        for page, _ in items:
            if page in NO_FOOTER:
                continue  # 主扫描已反向锁死（无 footer 且无 MARK）
            fail.extend(_check_one(page, cat, expect, page_cat))
    # 全量守恒：磁盘 90 页（减模板壳）必须 = 已分组页 ∪ NO_FOOTER，且无重复分组。
    disk = {f.name for f in DATA.glob("*.html")} - {"_shell.html"}
    grouped = list(page_cat)
    if len(grouped) != len(set(grouped)):
        fail.append("分组重复：同一页出现在多个类别/族")
    missing = sorted(disk - set(grouped) - NO_FOOTER)
    extra = sorted(set(grouped) - disk)
    if missing:
        fail.append(f"未覆盖页 {missing}（既不在看板卡也不在文件名族）")
    if extra:
        fail.append(f"分组含不存在的页 {extra}")
    return fail


def _check_grid():
    """看板解析完备性：专题网格内每张卡都必须带 data-category。

    新增卡若漏写该属性，CARD 正则会把整卡静默跳过（少一张卡＝少一组推荐且无人察觉）。
    """
    dash_txt = DASH.read_text(encoding="utf-8")
    gi = dash_txt.find('id="topic-grid"')
    grid = dash_txt[gi:] if gi != -1 else ""
    if "</section>" in grid:
        grid = grid[: grid.find("</section>")]
    total = len(re.findall(r'<a class="kpi-card"', grid))
    withcat = len(re.findall(r'<a class="kpi-card"[^>]*data-category="', grid))
    if total == withcat:
        return []
    return [
        f"看板专题卡缺分类：网格 {total} 张 vs 带 data-category {withcat} 张"
        "（缺属性的卡会被静默跳过·补 data-category 后重跑）"
    ]


def _check_tab_counts():
    """筛选标签静态计数 ≡ 网格实卡数（W1328：51/12 两处长期漂移的机器防线）。"""
    dash = DASH.read_text(encoding="utf-8")
    gi = dash.find('id="topic-grid"')
    grid = dash[gi:] if gi != -1 else ""
    if "</section>" in grid:
        grid = grid[: grid.find("</section>")]
    counts = {}
    for m in re.finditer(r'data-category="([^"]+)"', grid):
        counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    total = len(re.findall(r'<a class="kpi-card"', grid))
    fail = []
    for m in re.finditer(
        r'<button[^>]*class="filter-tab[^"]*"[^>]*data-category="([^"]+)"[^>]*>([^<]*)</button>', dash
    ):
        cat, text = m.group(1), m.group(2).strip()
        mm = re.search(r"(\d+)\s*$", text)
        if not mm:
            continue
        got = int(mm.group(1))
        expect = total if cat == "all" else counts.get(cat, 0)
        if got != expect:
            fail.append(f"看板筛选标签计数漂移：{cat} 标 {got} vs 网格实卡 {expect}")
    return fail


def _check_dash_deeplink():
    """看板深链契约：footer 生成的 #cat=<类别> 必须有对应解析代码。"""
    txt = DASH.read_text(encoding="utf-8")
    if "URLSearchParams" not in txt or "readHashState" not in txt:
        return ["看板缺少 #cat= 深链解析（readHashState/URLSearchParams）"]
    return []


def _check_stray(page_cat):
    fail = []
    for f in sorted(DATA.glob("*.html")):
        if f.name == "_shell.html" or f.name in page_cat:
            continue
        if MARK in f.read_text(encoding="utf-8"):
            fail.append(f"{f.name}: 非目标页出现 MARK（杂散注入）")
    return fail


def _run_check(page_cat, stats):
    fail = _check_coverage(page_cat)
    fail.extend(_check_grid())
    fail.extend(_check_tab_counts())
    fail.extend(_check_dash_deeplink())
    fail.extend(_check_stray(page_cat))
    bad = {k: v for k, v in stats.items() if k in ("no-footer", "mark-broken")}
    if bad:
        fail.append(f"异常动作 {bad}")
    print(f"CHECK {'FAIL' if fail else 'PASS'}  问题 {len(fail)} 条")
    for x in fail[:40]:
        print("  -", x)
    sys.exit(1 if fail else 0)


def _print_plan(mode, page_cat, stats, changed):
    print(f"mode={mode}  分组={len(parse_cache)}  目标页={len(page_cat)}  stats={stats}  实际改动={len(changed)}")
    for cat, items in parse_cache.items():
        print(f"  {CAT_NAMES.get(cat, cat):<18} {len(items):>2} 页")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--dry-run"
    global parse_cache
    parse_cache = parse_groups()
    page_cat = {p: c for c, items in parse_cache.items() for p, _ in items}
    stats, changed, fail = _scan_pages(mode, page_cat)
    _print_plan(mode, page_cat, stats, changed)
    if mode == "--check":
        _run_check(page_cat, stats)
    if fail:
        for x in fail:
            print("  -", x)
        sys.exit(1)


if __name__ == "__main__":
    main()
