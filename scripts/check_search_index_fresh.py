#!/usr/bin/env python3
"""check_search_index_fresh.py — 站内搜索索引新鲜度门禁（W809 建立·verify_delivery 第 46 槽）。

背景（W807 实证）：站内搜索索引自 2026-09-16 前后停更——全站 771 条索引仅含 61 篇
doc 条目，且 9 条链接仍指向已改名的 `docs/11-报告复盘/`（GitHub 侧 404）。W807 刷新了
索引（doc 61→111·失效目录引用 9→0）并把生成器恢复常驻，但**刷新动作本身无机器防线**：
任何内容批次改了 `docs/` 或 `site/` 后忘记重跑生成器，索引即静默陈旧（用户搜不到新文档
·老链接点不开）——本槽把该面关进笼子。

判据（全过 exit 0，任一 FAIL exit 1）：
C1 三件索引数据件与两页外链双侧在位（W1223 外置·W1317 拆共享件）：
   a) site/data/search-index-docs.js（docs/reader 共用·唯一副本）、
      site/data/search-index-zh.js、site/en/search-index-en.js 三件存在且
      SEARCH_INDEX: BEGIN/END 标记对齐全、常量名正确；zh/en 件必须以
      `SITE_SEARCH_INDEX_DOCS.concat([...])` 形态定义（缺件/形态错即 FAIL）；
   b) 两个搜索页各含两条外链 <script src="…">：共享件 + 本语言件，且共享件必须
      **先于**本语言件（后者定义时即求值共享常量——顺序错则 ReferenceError）。
C2 docs 共享件载荷 == 生成器实算载荷
C3 zh 数据件载荷（本语言页面条目）== 生成器实算载荷
C4 en 数据件载荷（本语言页面条目）== 生成器实算载荷

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
    python scripts/check_search_index_fresh.py --self-test # 注入式自测（1 正 6 负·不触仓库）

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

# 共享件常量（zh/en 件定义时引用·页面必须先加载共享件）
SHARED_CONST = "SITE_SEARCH_INDEX_DOCS"
SHARED_FILE = "site/data/search-index-docs.js"

# 索引数据件 → 索引常量名（W1223 外置·W1317 拆 docs 共享件）
INDEX_FILES = {
    SHARED_FILE: "SITE_SEARCH_INDEX_DOCS",
    "site/data/search-index-zh.js": "SITE_SEARCH_INDEX_ZH",
    "site/en/search-index-en.js": "SITE_SEARCH_INDEX_EN",
}

# 搜索页 → (共享件, 本语言件)；页面必须以外链 <script src> 引用两件且顺序在前者
PAGE_REFS = {
    "site/data/search.html": (SHARED_FILE, "site/data/search-index-zh.js"),
    "site/en/search.html": (SHARED_FILE, "site/en/search-index-en.js"),
}

_ARRAY_RE = re.compile(r"const\s+(SITE_SEARCH_INDEX_[A-Z]+)\s*=\s*(\[.*?\]);", re.S)
_CONCAT_RE = re.compile(
    r"const\s+(SITE_SEARCH_INDEX_[A-Z]+)\s*=\s*" + SHARED_CONST + r"\.concat\((\[.*?\])\);",
    re.S,
)


def extract_embedded(html: str):
    """抽取索引载荷（实参可承载任意含标记对文本）。

    返回 (常量名, 形态, 条目列表)；形态 ∈ {'plain','concat'}，块缺失/不可解析时
    常量名与形态为 None。concat 形态 = 本语言页面条目 + 共享 docs 件（唯一副本）。
    """
    if BEGIN not in html or END not in html:
        return None, None, None
    block = html[html.find(BEGIN):html.find(END) + len(END)]
    m = _CONCAT_RE.search(block)
    kind = "concat"
    if not m:
        m = _ARRAY_RE.search(block)
        kind = "plain"
    if not m:
        return None, None, None
    try:
        return m.group(1), kind, json.loads(m.group(2))
    except ValueError:
        return m.group(1), kind, None


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


# 数据件 → (期望载荷键, 判据码, 形态要求)
_FILE_SPEC = {
    SHARED_FILE: ("docs", "C2", "plain"),
    "site/data/search-index-zh.js": ("zh", "C3", "concat"),
    "site/en/search-index-en.js": ("en", "C4", "concat"),
}


def check_pages(expected: dict, pages: dict) -> list[str]:
    """核心判据（纯函数形态：--self-test 复用同一判据）。

    expected: {'docs': 条目列表, 'zh': 页面条目, 'en': 页面条目}
    pages:    判据域文件文本映射 {仓库相对路径: 文件文本}——键集由 INDEX_FILES
              与 PAGE_REFS 定义，调用方按全集传入。
    返回 FAIL 明细列表（空 = 全过）。
    """
    fails = []
    # C1-a/C2-C4：数据件在位（标记对 + 常量名 + 形态）并承载载荷对拍
    for path, const_name in INDEX_FILES.items():
        text = pages.get(path)
        if text is None:
            fails.append("C1 索引数据件缺失：%s" % path)
            continue
        name, kind, actual = extract_embedded(text)
        if name is None:
            fails.append("C1 索引块缺失或不可解析（%s/%s 标记对不齐）：%s" % (BEGIN, END, path))
            continue
        if name != const_name:
            fails.append("C1 索引常量名不符（期望 %s·实得 %s）：%s" % (const_name, name, path))
            continue
        key, code, want_kind = _FILE_SPEC[path]
        if kind != want_kind:
            hint = ("须以 %s.concat([...]) 定义（加载共享件后求值）" % SHARED_CONST
                    if want_kind == "concat" else "须为纯 JSON 数组定义")
            fails.append("C1 索引件定义形态不符（%s·实得 %s）：%s" % (hint, kind, path))
            continue
        diffs = diff_entries(expected.get(key) or [], actual)
        if diffs:
            fails.append("%s 索引数据件陈旧（应重跑 python scripts/_gen_search_index.py）：%s"
                         % (code, path))
            for d in diffs:
                fails.append("    · %s" % d)
            fails.append("    · 条目数 期望 %d·实得 %d"
                         % (len(expected.get(key) or []), len(actual)))
    # C1-b：页面外链引用在位且顺序正确（共享件先于本语言件）
    for page_rel, (shared_rel, own_rel) in PAGE_REFS.items():
        html = pages.get(page_rel)
        if html is None:
            fails.append("C1 搜索页缺失：%s" % page_rel)
            continue
        shared_pos = html.find(os.path.basename(shared_rel))
        own_pos = html.find(os.path.basename(own_rel))
        if shared_pos < 0 or own_pos < 0:
            fails.append('C1 页面外链引用缺失（应为 <script src="%s"> 与 "%s"）：%s'
                         % (os.path.basename(shared_rel), os.path.basename(own_rel), page_rel))
        elif shared_pos > own_pos:
            fails.append("C1 页面外链顺序错误（共享件须先于本语言件，否则定义求值即 ReferenceError）：%s"
                         % page_rel)
    return fails


def _self_test() -> int:
    """注入式自测：1 正 6 负，合成树用系统临时目录，不触仓库。"""
    import shutil
    import tempfile

    tmp = tempfile.mkdtemp(prefix="search_index_fresh_")
    ok = True
    try:
        exp_docs = [{"kind": "doc", "title": "甲", "category": "c", "snippet": "s", "url": "u1", "kw": ["a"]},
                    {"kind": "doc", "title": "乙", "category": "c", "snippet": "s2", "url": "u2", "kw": ["b"]}]
        exp_zh = [{"kind": "page", "title": "丙", "category": "c", "snippet": "s3", "url": "u3", "kw": ["c"]}]
        exp_en = [{"kind": "page", "title": "丁", "category": "c", "snippet": "s4", "url": "u4", "kw": ["d"]}]

        def mk_js(const, items, concat=False):
            payload = json.dumps(items, ensure_ascii=False, separators=(',', ':'))
            expr = ("%s.concat(%s)" % (SHARED_CONST, payload)) if concat else payload
            return ("%s\nconst %s = %s;\n%s\n" % (BEGIN, const, expr, END))

        def mk_page(refs):
            tags = "".join('<script src="%s"></script>' % r for r in refs)
            return ('<html><body>%s'
                    '<script>function renderOffline(q){return SITE_SEARCH_INDEX_ZH;}</script></body></html>\n'
                    % tags)

        def case(label, expect_codes, pages, expected=None):
            nonlocal ok
            got = check_pages(expected or {"docs": exp_docs, "zh": exp_zh, "en": exp_en}, pages)
            hit = []
            if expect_codes:
                for g in got:
                    if any(g.startswith(c) for c in expect_codes):
                        hit.append(g)
            passed = (not got) if not expect_codes else bool(hit)
            print("  %s %s" % ("PASS" if passed else "FAIL", label))
            if not passed:
                ok = False
                print("    期望命中 %r·实得 %r" % (expect_codes, got))

        good = {
            "site/data/search.html": mk_page(["search-index-docs.js", "search-index-zh.js"]),
            "site/en/search.html": mk_page(["../data/search-index-docs.js", "search-index-en.js"]),
            SHARED_FILE: mk_js(SHARED_CONST, exp_docs),
            "site/data/search-index-zh.js": mk_js("SITE_SEARCH_INDEX_ZH", exp_zh, concat=True),
            "site/en/search-index-en.js": mk_js("SITE_SEARCH_INDEX_EN", exp_en, concat=True),
        }
        # 正样本：完全一致 → 无 FAIL
        case("fresh-must-pass", [], good)
        # 负样本 1：共享件缺失（生成器未跑/被删）
        no_shared = dict(good)
        del no_shared[SHARED_FILE]
        case("missing-shared-file-must-fail-C1", ["C1"], no_shared)
        # 负样本 2：页面缺共享件外链（旧页面形态）
        no_ref = dict(good)
        no_ref["site/data/search.html"] = mk_page(["search-index-zh.js"])
        case("missing-shared-ref-must-fail-C1", ["C1"], no_ref)
        # 负样本 3：页面外链顺序错（本语言件在前 → 定义求值必 ReferenceError）
        bad_order = dict(good)
        bad_order["site/en/search.html"] = mk_page(["search-index-en.js", "../data/search-index-docs.js"])
        case("wrong-ref-order-must-fail-C1", ["C1"], bad_order)
        # 负样本 4：zh 件少一条（索引陈旧）
        stale = dict(good)
        stale["site/data/search-index-zh.js"] = mk_js("SITE_SEARCH_INDEX_ZH", [], concat=True)
        case("stale-entry-must-fail-C3", ["C3"], stale)
        # 负样本 5：docs 共享件字段漂移
        drift = dict(good)
        tampered = [dict(e) for e in exp_docs]
        tampered[0]["snippet"] = "改过的摘要"
        drift[SHARED_FILE] = mk_js(SHARED_CONST, tampered)
        case("shared-drift-must-fail-C2", ["C2"], drift)
        # 负样本 6：en 件常量名错位（zh 常量写进 en 件）
        wrong = dict(good)
        wrong["site/en/search-index-en.js"] = mk_js("SITE_SEARCH_INDEX_ZH", exp_en, concat=True)
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
              "禁静默跳过（装依赖：pip install --require-hashes -r scripts/requirements-hashed.txt）")
        return 1

    try:
        built = gen.build_indexes()
    except Exception as exc:
        print(MARKER + "1 FAIL")
        print("  FAIL 生成器实算失败：%s" % exc)
        return 1

    expected = {k: json.loads(built[k][1]) for k in ("docs", "zh", "en")}
    pages = {}
    for rel in list(INDEX_FILES) + list(PAGE_REFS):
        p = os.path.join(root, rel)
        try:
            with open(p, encoding="utf-8") as f:
                pages[rel] = f.read()
        except OSError as exc:
            print(MARKER + "1 FAIL")
            print("  FAIL 文件读取失败：%s（%s）" % (rel, exc))
            return 1

    fails = check_pages(expected, pages)
    if fails:
        print(MARKER + "%d FAIL" % len(fails))
        for msg in fails[:20]:
            print("  FAIL", msg)
        if len(fails) > 20:
            print("  ...（其余 %d 条略）" % (len(fails) - 20))
        return 1
    print(MARKER + "0 FAIL（docs %d 条 · zh %d 条 · en %d 条 与生成器实算一致）"
          % (len(expected["docs"]), len(expected["zh"]), len(expected["en"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
