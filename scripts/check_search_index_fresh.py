#!/usr/bin/env python3
"""check_search_index_fresh.py — 站内搜索索引新鲜度门禁（W809 建立·verify_delivery 第 46 槽）。

背景（W807 实证）：站内搜索索引自 2026-09-16 前后停更——全站 771 条索引仅含 61 篇
doc 条目，且 9 条链接仍指向已改名的 `docs/11-报告复盘/`（GitHub 侧 404）。W807 刷新了
索引（doc 61→111·失效目录引用 9→0）并把生成器恢复常驻，但**刷新动作本身无机器防线**：
任何内容批次改了 `docs/` 或 `site/` 后忘记重跑生成器，索引即静默陈旧（用户搜不到新文档
·老链接点不开）——本槽把该面关进笼子。

判据（全过 exit 0，任一 FAIL exit 1）：
C1 两页内嵌索引块存在：SEARCH_INDEX:BEGIN/END 标记对齐全（缺标记即 FAIL——索引被手删
   或页面被重写，站内搜索退化为「无命中」而无人察觉）
C2 zh 页内嵌载荷 == 生成器实算载荷（逐条对拍：kind/标题/分类/摘要/URL/关键词）
C3 en 页内嵌载荷 == 生成器实算载荷（同上）

口径与纪律：
- 期望载荷由 `scripts/_gen_search_index.py` 的 `build_indexes()` **纯计算**得出（W809
  函数化：import 不落盘）；本门禁**只读不写**——刷新动作为
  `python scripts/_gen_search_index.py`（写盘在生成器侧，门禁侧只对拍）。
- 判据按 JSON 条目**逐项**比对，禁字节串比对（JSON 序列化细节变化会致假红）。
- fail-closed：jieba 缺失（索引关键词依赖，缺则 kw 退化为逐字）时本槽**不可判定** →
  报「环境缺 jieba」并 FAIL，禁「静默跳过」假绿（与第 31/45 门禁同族纪律）。
- 跨平台断言纪律（pitfalls「latent 三问 + 双平台断言禁例」）：比对基于 JSON 值与路径
  字符串，零 os.name/盘符/大小写语义断言；负样本用系统临时目录注入（合成树两平台同构·
  不触仓库），真实执行位=CI（Linux）与本地（Windows）同断言。

用法：
    python scripts/check_search_index_fresh.py             # 门禁模式（= --gate）
    python scripts/check_search_index_fresh.py --gate      # 同上（verify_delivery 调用形态）
    python scripts/check_search_index_fresh.py --self-test # 注入式自测（1 正 4 负·不触仓库）

退出码：0 全过；1 有 FAIL；2 参数/环境错误。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

MARKER = "---- 第 46 门禁 搜索索引新鲜度："

BEGIN = "/* SEARCH_INDEX:BEGIN */"
END = "/* SEARCH_INDEX:END */"

# 页面 → 索引常量名（zh 页收 zh 站点页，en 页收 en 站点页·生成器口径）
PAGES = {
    "site/data/search.html": "SITE_SEARCH_INDEX_ZH",
    "site/en/search.html": "SITE_SEARCH_INDEX_EN",
}

_CONST_RE = re.compile(r"const\s+(SITE_SEARCH_INDEX_[A-Z]+)\s*=\s*(\[.*?\]);", re.S)


def extract_embedded(html: str):
    """抽取页面内嵌索引载荷。返回 (常量名, 条目列表) 或 (None, None)（块缺失/不可解析）。"""
    if BEGIN not in html or END not in html:
        return None, None
    block = html[html.find(BEGIN):html.find(END) + len(END)]
    m = _CONST_RE.search(block)
    if not m:
        return None, None
    try:
        return m.group(1), json.loads(m.group(2))
    except ValueError:
        return m.group(1), None


def diff_entries(expected, actual, limit=3):
    """逐条对拍两个条目列表，返回差异描述列表（空 = 一致）。"""
    diffs = []
    if actual is None:
        return ["内嵌载荷不可解析（非合法 JSON）"]
    exp_by_key = {}
    for e in expected:
        exp_by_key[(e.get("kind"), e.get("title"), e.get("url"))] = e
    act_by_key = {}
    for e in actual:
        act_by_key[(e.get("kind"), e.get("title"), e.get("url"))] = e
    missing = sorted(set(exp_by_key) - set(act_by_key))
    extra = sorted(set(act_by_key) - set(exp_by_key))
    for k in missing[:limit]:
        diffs.append("缺条目：%s | %s" % (k[0], k[1]))
    for k in extra[:limit]:
        diffs.append("多余条目：%s | %s" % (k[0], k[1]))
    # 同键但字段漂移（标题/分类/摘要/关键词任一不同）
    drift = 0
    for k in sorted(set(exp_by_key) & set(act_by_key)):
        e, a = exp_by_key[k], act_by_key[k]
        if (e.get("category"), e.get("snippet"), e.get("kw")) != \
           (a.get("category"), a.get("snippet"), a.get("kw")):
            drift += 1
            if drift <= limit:
                diffs.append("字段漂移：%s | %s" % (k[0], k[1]))
    if drift > limit:
        diffs.append("字段漂移其余 %d 条略" % (drift - limit))
    return diffs


def check_pages(expected: dict, pages: dict) -> list[str]:
    """核心判据（纯函数形态：--self-test 复用同一判据）。

    expected: {'zh': 条目列表, 'en': 条目列表}
    pages:    {'site/data/search.html': 页面文本, 'site/en/search.html': 页面文本}
    返回 FAIL 明细列表（空 = 全过）。
    """
    fails = []
    for path, const_name in PAGES.items():
        html = pages.get(path)
        if html is None:
            fails.append("C1 页面缺失：%s" % path)
            continue
        name, actual = extract_embedded(html)
        if name is None:
            fails.append("C1 索引块缺失或不可解析（%s/%s 标记对不齐）：%s" % (BEGIN, END, path))
            continue
        if name != const_name:
            fails.append("C1 索引常量名不符（期望 %s·实得 %s）：%s" % (const_name, name, path))
            continue
        lang = "zh" if "SITE_SEARCH_INDEX_ZH" == const_name else "en"
        diffs = diff_entries(expected.get(lang) or [], actual)
        if diffs:
            fails.append("C%d 内嵌索引陈旧（应重跑 python scripts/_gen_search_index.py）：%s"
                         % (2 if lang == "zh" else 3, path))
            for d in diffs:
                fails.append("    · %s" % d)
            fails.append("    · 条目数 期望 %d·实得 %d"
                         % (len(expected.get(lang) or []), len(actual)))
    return fails


def _self_test() -> int:
    """注入式自测：1 正 4 负，合成树用系统临时目录，不触仓库。"""
    import shutil
    import tempfile

    tmp = tempfile.mkdtemp(prefix="search_index_fresh_")
    ok = True
    try:
        exp_zh = [{"kind": "doc", "title": "甲", "category": "c", "snippet": "s", "url": "u1", "kw": ["a"]},
                  {"kind": "page", "title": "乙", "category": "c", "snippet": "s2", "url": "u2", "kw": ["b"]}]
        exp_en = list(exp_zh)

        def mk_html(const, items):
            payload = json.dumps(items, ensure_ascii=False, separators=(',', ':'))
            return ("<html><body>x</body></html>\n%s\nconst %s = %s;\n%s\n"
                    % (BEGIN, const, payload, END))

        def case(label, expect_codes, pages, expected=None):
            nonlocal ok
            got = check_pages(expected or {"zh": exp_zh, "en": exp_en}, pages)
            hit = [g for g in got if any(g.startswith(c) for c in expect_codes)] if expect_codes else []
            passed = (not got) if not expect_codes else bool(hit)
            print("  %s %s" % ("PASS" if passed else "FAIL", label))
            if not passed:
                ok = False
                print("    期望命中 %r·实得 %r" % (expect_codes, got))

        good = {
            "site/data/search.html": mk_html("SITE_SEARCH_INDEX_ZH", exp_zh),
            "site/en/search.html": mk_html("SITE_SEARCH_INDEX_EN", exp_en),
        }
        # 正样本：完全一致 → 无 FAIL
        case("fresh-must-pass", [], good)
        # 负样本 1：缺索引块（标记被删）
        broken = dict(good)
        broken["site/data/search.html"] = "<html><body>no index</body></html>"
        case("missing-block-must-fail-C1", ["C1"], broken)
        # 负样本 2：少一条条目（索引陈旧）
        stale = dict(good)
        stale["site/data/search.html"] = mk_html("SITE_SEARCH_INDEX_ZH", exp_zh[:1])
        case("stale-entry-must-fail-C2", ["C2"], stale)
        # 负样本 3：字段漂移（摘要被改）
        drift = dict(good)
        tampered = [dict(e) for e in exp_zh]
        tampered[0]["snippet"] = "改过的摘要"
        drift["site/data/search.html"] = mk_html("SITE_SEARCH_INDEX_ZH", tampered)
        case("field-drift-must-fail-C2", ["C2"], drift)
        # 负样本 4：en 页常量名错位（zh 常量写进 en 页）
        wrong = dict(good)
        wrong["site/en/search.html"] = mk_html("SITE_SEARCH_INDEX_ZH", exp_en)
        case("wrong-const-must-fail-C1", ["C1"], wrong)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if ok:
        print("SELF_TEST_OK")
        return 0
    print("SELF_TEST_FAIL")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description="站内搜索索引新鲜度门禁（W809·第 46 槽）")
    ap.add_argument("--gate", action="store_true", help="门禁模式（默认）")
    ap.add_argument("--self-test", action="store_true", help="注入式自测（不触仓库）")
    args = ap.parse_args()

    if args.self_test:
        return _self_test()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scripts_dir = os.path.join(root, "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    try:
        import _gen_search_index as gen  # noqa: E402  纯计算模块（W809 函数化·import 不落盘）
    except Exception as exc:
        print(MARKER + "1 FAIL")
        print("  FAIL 无法导入生成器模块 scripts/_gen_search_index.py：%s" % exc)
        return 1

    # fail-closed：jieba 缺失 → 关键词退化为逐字 → 期望载荷不可信 → 不可判定即红
    if getattr(gen, "jieba", None) is None:
        print(MARKER + "1 FAIL")
        print("  FAIL 环境缺 jieba（索引关键词依赖·缺则 kw 退化为逐字）——本槽不可判定，"
              "禁静默跳过（装依赖：pip install -r scripts/requirements.txt）")
        return 1

    try:
        built = gen.build_indexes()
    except Exception as exc:
        print(MARKER + "1 FAIL")
        print("  FAIL 生成器实算失败：%s" % exc)
        return 1

    expected = {"zh": json.loads(built["zh"][1]), "en": json.loads(built["en"][1])}
    pages = {}
    for rel in PAGES:
        p = os.path.join(root, rel)
        try:
            with open(p, encoding="utf-8") as f:
                pages[rel] = f.read()
        except OSError as exc:
            print(MARKER + "1 FAIL")
            print("  FAIL 页面读取失败：%s（%s）" % (rel, exc))
            return 1

    fails = check_pages(expected, pages)
    if fails:
        print(MARKER + "%d FAIL" % len(fails))
        for msg in fails[:20]:
            print("  FAIL", msg)
        if len(fails) > 20:
            print("  ...（其余 %d 条略）" % (len(fails) - 20))
        return 1
    print(MARKER + "0 FAIL（zh %d 条 · en %d 条 与生成器实算一致）"
          % (len(expected["zh"]), len(expected["en"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
