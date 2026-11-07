"""check_nav_parity.py — 第 65 门禁 · 导航一致性（W1167 · MVP 迁移批③）

背景：audit-1 唯一 major=跨页主导航不一致（普查 20 个签名族实证，5 类页 5 套导航）。
本批以 scripts/w1167_nav_inject.py 为唯一正本做全站分发（859 页），本槽把「一致率 100%」
判据化——brief.design_criteria.quantitative[0] 的机器形态：漏页/乱序/双高亮/结构破损即红。

判据（同源引用正本，不复制清单——W1120 双阈值同族纪律）：
  N1 每页含 NAV-CANONICAL MARK 恰一次（_template.html 模板源豁免）
  N2 .nav-item 文本序 == 正本 ZH/EN 六项（按分区）
  N3 aria-current="page" ≤1 且取值 ∈ 正本项
  N4 有 MARK 无 nav[aria-label=主导航] 结构 → 破损红（防手工剥壳）
退出码：0 通过 / 1 判红 / 2 基础设施缺失（fail-closed）。恒跑（_SCOPE_CORE·毫秒级静态扫描）。
用法：py scripts/check_nav_parity.py [--report] [--self-test]
"""
import importlib.util
import io
import re
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MARK = "<!-- NAV-CANONICAL v1 w1167 -->"
MARKER = "---- 第 65 门禁 导航一致性："
SKIP = {"_template.html"}


def _load_truth():
    spec = importlib.util.spec_from_file_location("navtruth", Path(__file__).with_name("w1167_nav_inject.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # it[0] 而非解包——正本元组后续加字段（W1167 加了埋点事件名）不应让门禁炸「too many values」
    return [it[0] for it in mod.ZH_ITEMS], [it[0] for it in mod.EN_ITEMS]


NAV = re.compile(r"<nav\b[^>]*aria-label=\"主导航\"[^>]*>(.*?)</nav>", re.S)
ITEM = re.compile(r"<a\b[^>]*class=\"nav-item[^\"]*\"[^>]*>([^<]+)</a>")
CUR = re.compile(r"<a\b[^>]*aria-current=\"page\"[^>]*>")


def check_page(rel: str, txt: str, zh_items, en_items):
    errs = []
    n_mark = txt.count(MARK)
    if n_mark != 1:
        errs.append(f"MARK 出现 {n_mark} 次（应恰 1）")
        if n_mark == 0:
            return errs
    m = NAV.search(txt)
    if not m:
        return errs + ["有 MARK 无主导航结构（破损）"]
    items = ITEM.findall(m.group(1))
    want = en_items if rel.startswith("en/") else zh_items
    if items != want:
        errs.append(f"nav-item 序不符：{items} ≠ {want}")
    curs = m.group(1).count('aria-current="page"')
    if curs > 1:
        errs.append(f"aria-current 出现 {curs} 次（≤1）")
    return errs


def run_all(files, zh_items, en_items):
    viol = []
    for rel, txt in files:
        e = check_page(rel, txt, zh_items, en_items)
        if e:
            viol.append((rel, e))
    return viol


def self_test(zh, en):
    zh, en = _load_truth()
    good = '<nav aria-label="主导航">' + "".join(f'<a class="nav-item" href="#">{t}</a>' for t in zh) + "</nav>"
    cases = [
        ("正样本-缺MARK", "x.html", "<p>无导航</p>", 1),
        ("正样本-规范页", "index.html", MARK + good, 0),
        ("负样本-乱序", "a.html", MARK + '<nav aria-label="主导航"><a class="nav-item">阅读</a><a class="nav-item">导读</a>' + "".join(f'<a class="nav-item">{t}</a>' for t in zh[2:]) + "</nav>", 1),
        ("负样本-双高亮", "b.html", MARK + '<nav aria-label="主导航">' + f'<a class="nav-item" aria-current="page">{zh[0]}</a>' + f'<a class="nav-item" aria-current="page">{zh[1]}</a>' + "".join(f'<a class="nav-item">{t}</a>' for t in zh[2:]) + "</nav>", 1),
        ("负样本-结构剥壳", "c.html", MARK + "<div>导航被手工替换</div>", 1),
    ]
    fails = 0
    for name, rel, txt, expect in cases:
        errs = check_page(rel, txt, zh, en)
        got = 1 if errs else 0
        tag = "OK" if got == expect else "WRONG"
        if got != expect:
            fails += 1
        print(f"  [{tag}] {name}: errs={len(errs)} 期望违规标志={expect}")
    print(f"自测 {'PASS' if fails == 0 else 'FAIL'}（{len(cases)} 例）")
    return 0 if fails == 0 else 1


def main():
    try:
        zh, en = _load_truth()
    except Exception as e:  # fail-closed：正本不可读=判据不可执行
        print(f"{MARKER}基础设施缺失（正本模块不可读）: {e}")
        sys.exit(2)
    files = []
    for f in sorted(SITE.rglob("*.html")):
        rel = f.relative_to(SITE).as_posix()
        if rel in SKIP:
            continue
        files.append((rel, f.read_text(encoding="utf-8", errors="replace")))
    viol = run_all(files, zh, en)
    verdict = "OK" if not viol else "FAIL"
    print(f"{MARKER}页面 {len(files)} · 违规 {len(viol)} · {verdict}")
    for rel, errs in viol[:15]:
        for e in errs:
            print(f"  ✗ {rel}: {e}")
    if "--report" in sys.argv:
        sys.exit(0)
    sys.exit(1 if viol else 0)


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test(*_load_truth()))
    main()
