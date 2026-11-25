"""W1327 页脚同类关联链接生成器（正本=本文件内规则，改推荐口径只改这里）。

来源：site/dashboard.html 专题卡片（href=data/xxx.html + data-category）——
每张卡片即一条「页面 ↔ 类别」事实，类别名取自同页 filter-tab 的 data-label。
规则：同类别内按看板顺序循环取后 3 页（自页排除），每个目标页恰得一组 3 条链接；
     类别成员 < 4 时取 n-1 条（如 Q+ 仅 2 页则互链 1 条）。
注入：目标页 <footer class="site-footer"> 内、现有页脚导航之后，带 MARK 便于幂等重放。

用法：
  python scripts/w1327_related_links.py --dry-run    # 打印计划，不写盘
  python scripts/w1327_related_links.py --apply      # 注入/更新（幂等：重放零漂移）
  python scripts/w1327_related_links.py --check      # 门禁：覆盖/条数/自页排除/可达性/分类一致

判定口径说明：
  - 「关联」= 同 data-category（看板既有分类，不新增人工标签）；
  - 链接只用 file:// 相对路径（与目标页同目录，site/data/ 内直链）；
  - 不新增 CSS：复用 .site-footer nav 与 .footer-meta 既有样式（零外域、零内联脚本）。
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

CARD = re.compile(r'<a class="kpi-card"[^>]*?href="data/([^"]+\.html)"[^>]*?data-category="([^"]+)"[^>]*>(.*?)</a>', re.S)
LABEL = re.compile(r'<div class="label">(.*?)</div>', re.S)
IDX = re.compile(r'^[A-Z]{1,2}\+{0,3}\s*·\s*')
FOOTER = re.compile(r'(<footer class="site-footer">)(.*?)(</footer>)', re.S)


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


def related_for(cat, page):
    items = [p for p, _ in parse_cache[cat]]
    n = len(items)
    i = items.index(page)
    take = min(MAX_LINKS, n - 1)
    out = []
    for k in range(1, take + 1):
        out.append(items[(i + k) % n])
    return out


def build_block(cat, page):
    links = related_for(cat, page)
    titles = dict(parse_cache[cat])
    lines = [
        f"        {MARK}",
        f'        <nav class="footer-related" aria-label="{NAV_LABEL}">',
        f'            <span class="footer-meta">同类 · {CAT_NAMES[cat]}</span>',
    ]
    for t in links:
        lines.append(f'            <a href="{t}">{titles[t]}</a>')
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
        fail.append(f"缺页 {page}（看板卡片指向不存在文件）")
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
            out.append(f"{page}: {h} 分类不一致（{page_cat.get(h)} ≠ {cat}）")
    return out


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
    hrefs = re.findall(r'<a href="([^"]+)">', blk)
    fail = []
    if len(hrefs) != expect:
        fail.append(f"{page}: 链接 {len(hrefs)} 条（应 {expect}）")
    if page in hrefs:
        fail.append(f"{page}: 含自页链接")
    fail.extend(_check_hrefs(page, cat, hrefs, page_cat))
    if f"同类 · {CAT_NAMES[cat]}" not in blk:
        fail.append(f"{page}: 类别标签缺失")
    return fail


def _check_coverage(page_cat):
    fail = []
    for cat, items in parse_cache.items():
        expect = min(MAX_LINKS, len(items) - 1)
        for page, _ in items:
            if page in NO_FOOTER:
                continue  # 主扫描已反向锁死（无 footer 且无 MARK）
            fail.extend(_check_one(page, cat, expect, page_cat))
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


def _check_stray(page_cat):
    fail = []
    for f in sorted(DATA.glob("*.html")):
        if f.name == "_shell.html" or f.name in page_cat:
            continue
        if MARK in f.read_text(encoding="utf-8"):
            fail.append(f"{f.name}: 非看板页出现 MARK（杂散注入）")
    return fail


def _run_check(page_cat, stats):
    fail = _check_coverage(page_cat)
    fail.extend(_check_grid())
    fail.extend(_check_stray(page_cat))
    bad = {k: v for k, v in stats.items() if k in ("no-footer", "mark-broken")}
    if bad:
        fail.append(f"异常动作 {bad}")
    print(f"CHECK {'FAIL' if fail else 'PASS'}  问题 {len(fail)} 条")
    for x in fail[:40]:
        print("  -", x)
    sys.exit(1 if fail else 0)


def _print_plan(mode, page_cat, stats, changed):
    print(f"mode={mode}  类别={len(parse_cache)}  目标页={len(page_cat)}  stats={stats}  实际改动={len(changed)}")
    for cat, items in parse_cache.items():
        print(f"  {CAT_NAMES[cat]:<18} {len(items):>2} 页")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--dry-run"
    global parse_cache
    parse_cache = parse_cards()
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
