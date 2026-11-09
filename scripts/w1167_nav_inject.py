"""W1167① 主导航单组件分发生成器（正本=本文件内 CANONICAL，改导航只改这里）。

用法：
  python scripts/w1167_nav_inject.py --dry-run    # 只出计划报告，不写盘
  python scripts/w1167_nav_inject.py --apply      # 执行替换/插入（幂等：已规范页跳过）
  python scripts/w1167_nav_inject.py --check      # 门禁模式：不一致即退出非 0（第 65 槽调用）

规则来源：spark-output/context/sitemap.json（6 项主导航）+ W1167 普查规格
_w1167_nav_survey.json；页内子导航（reader catalog-jump 等）保留不动。
"""
import io
import json
import re
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
# 根路径按 __file__ 派生：硬编码盘符在 CI（Linux runner）上指向不存在目录，
# 会让消费方门禁「扫到 0 页」而假绿——本地绿≠CI 绿（W700 教训形态）。
ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

# —— 导航正本（唯一可编辑处）——
# 三元组 (标签, 目标, 埋点事件名)。事件名**显式声明不派生**：它是 metric.json nav_click 的
# 契约面，而目标路径派生不出唯一名字（index.html 在中/英/回根三处含义不同，
# "../index.html" 更会派生成空 slug）——派生＝把契约交给猜测，改路径会静默改事件名。
# 中英两区事件名分属两套，跨区不合并（同一 slug 在两区各自计数会混流）。
ZH_ITEMS = [
    ("导读", "guide.html", "nav-guide"),
    ("阅读", "reader/index.html", "nav-reader"),
    ("看板", "dashboard.html", "nav-dashboard"),
    ("检索", "data/text-search.html", "nav-search"),
    ("关于", "about.html", "nav-about"),
    ("EN", "en/index.html", "nav-switch-en"),
]
EN_ITEMS = [
    ("Home", "index.html", "nav-home"),
    ("Guide", "guide.html", "nav-en-guide"),
    ("Dashboard", "dashboard.html", "nav-en-dashboard"),
    ("Search", "text-search.html", "nav-en-search"),
    ("Visualizations", "visualizations.html", "nav-en-visualizations"),
    ("中文", "../index.html", "nav-switch-zh"),
]
BRAND_ZH = ("西游详解", "index.html")
BRAND_EN = ("JTTW Notes", "index.html")
NAV_CLASS = "site-mainnav"
MARK = "<!-- NAV-CANONICAL v1 w1167 -->"

HDR = re.compile(r"<header\b[^>]*>.*?</header>", re.S)
BODY = re.compile(r"(<body[^>]*>)", re.S)

def relpath(target, from_file):
    """file:// 相对路径。ZH 目标相对 site/ 根；EN 目标相对 en/ 根（同目录直链）。"""
    depth = len(Path(from_file).parts) - 1
    if from_file.startswith("en/"):
        if target.startswith("../"):
            return "../" * depth + target[3:]  # 中文切换 → site 根
        return "../" * (depth - 1) + target if depth >= 2 else target
    return ("../" * depth) + target

def active_for(rel):
    if rel == "index.html" or rel == "404.html" or rel == "_template.html":
        return None
    if rel.startswith("en/"):
        return None
    if rel in ("guide.html", "curated.html"):
        return "导读"
    if rel.startswith("reader/"):
        return "阅读"
    if rel == "dashboard.html":
        return "看板"
    if rel == "data/text-search.html":
        return "检索"
    if rel.startswith("data/"):
        return "看板"
    if rel == "about.html":
        return "关于"
    return None

def build_nav(rel, zone):
    items = EN_ITEMS if zone == "en" else ZH_ITEMS
    brand = BRAND_EN if zone == "en" else BRAND_ZH
    act = active_for(rel)
    links = []
    for label, target, event in items:
        href = relpath(target, rel)
        cur = ' aria-current="page"' if label == act else ""
        cls = ' class="nav-item is-active"' if label == act else ' class="nav-item"'
        links.append(f'<a href="{href}"{cls}{cur} data-goatcounter-click="{event}">{label}</a>')
    bhref = relpath(brand[1], rel)
    inner = f'<a class="nav-brand" href="{bhref}">{brand[0]}</a>' + "".join(links)
    return (
        f'{MARK}\n<nav class="{NAV_CLASS}" aria-label="主导航">{inner}</nav>'
    )

def process(rel, txt):
    zone = "en" if rel.startswith("en/") else ("reader" if rel.startswith("reader/") else ("data" if rel.startswith("data/") else "root"))
    nav = build_nav(rel, zone)
    if MARK in txt:
        # 已规范：替换正文（幂等更新）
        new = re.sub(re.escape(MARK) + r".*?</nav>", nav.replace("\\", "\\\\") + "\n</nav>", txt, count=1, flags=re.S) if "</nav>" in txt else txt
        m = re.search(re.escape(MARK) + r"\s*<nav\b.*?</nav>", txt, re.S)
        if m:
            new = txt[:m.start()] + nav + txt[m.end():]
            return new, "update"
        return txt, "mark-broken"
    m = HDR.search(txt)
    if m:
        seg = m.group(0)
        # header 内保留非导航内容（如搜索框、主题按钮），仅替换 nav 区
        new_header = seg
        nm = re.search(r'<nav\b[^>]*>.*?</nav>', seg, re.S)
        if nm:
            new_header = seg[:nm.start()] + nav + seg[nm.end():]
        else:
            new_header = seg[:seg.rindex("</header>")] + nav + "\n</header>"
        return txt[:m.start()] + new_header + txt[m.end():], "replace-header-nav"
    mb = BODY.search(txt)
    if mb:
        i = mb.end()
        return txt[:i] + f'\n<header class="site-header">{nav}</header>\n' + txt[i:], "insert-header"
    return txt, "no-anchor"

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--dry-run"
    skip = {"_template.html"}  # 模板源不注入
    stats = {}
    changed = []
    for f in sorted(SITE.rglob("*.html")):
        rel = f.relative_to(SITE).as_posix()
        if rel in skip:
            continue
        txt = f.read_text(encoding="utf-8", errors="replace")
        new, action = process(rel, txt)
        stats[action] = stats.get(action, 0) + 1
        if new != txt:
            changed.append(rel)
            if mode == "--apply":
                f.write_text(new, encoding="utf-8")
    print(f"mode={mode}  stats={stats}  实际改动={len(changed)}")
    bad = {k: v for k, v in stats.items() if k in ("no-anchor", "mark-broken")}
    if bad:
        print("WARN 异常页:", bad)
    if mode == "--check":
        inconsistent = stats.get("replace-header-nav", 0) + stats.get("insert-header", 0) + stats.get("no-anchor", 0) + stats.get("mark-broken", 0)
        print(f"CHECK {'FAIL' if inconsistent else 'PASS'} 未规范化页数={inconsistent}")
        sys.exit(1 if inconsistent else 0)
    (ROOT / "scripts/output/_w1167_nav_plan.json").write_text(
        json.dumps({"mode": mode, "stats": stats, "changed_sample": changed[:20], "changed_total": len(changed)}, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
