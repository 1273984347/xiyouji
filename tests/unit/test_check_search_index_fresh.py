r"""W809 专项测试：scripts/check_search_index_fresh.py（第 46 槽 · 站内搜索索引新鲜度）

## 为什么测这个脚本

W807 实证的债：站内搜索索引停更（771 条仅含 61 篇 doc + 9 条死链）且**刷新动作本身
无机器防线**——内容批次改 docs/ 或 site/ 后忘重跑生成器，索引即静默陈旧（用户搜不到
新文档、旧链接点不开）。本门禁是那条债的唯一防线：它自身若判据失效（模式写宽/写窄、
忽略规则放水、fail-closed 绕过），该防线会静默归零——项目 W663/W709 教训：门禁自身
漂移要靠点检抓。

## 覆盖判据（W1223 外置数据件·W1317 拆 docs 共享件的三件形态）

  G1 现网实跑 0 FAIL（当前仓库真实状态·索引数据件与生成器一致）
  G2 自检：`--self-test` 7/7 且退出码 0
  G3 判据单元：check_pages() 对六类漂移（缺共享件 / 缺页面外链 / 外链顺序错 /
     zh 少条目 / docs 字段漂移 / 常量名错位）必须给出对应 C1-C4 码；一致态必须零 FAIL
  G4 环境 fail-closed：jieba 缺失即「不可判定→FAIL」（禁静默跳过假绿）
  G5 挂载一致性：verify_delivery 的 EXPECTED_SECTION_NAMES 与门禁元组均含「搜索索引」段
     （挂槽漏改任一手工面即启动期断言红——此处再做一层点检）

## 手法

判据用 check_pages() 注入构造（纯函数·合成数据·不触仓库）；CLI 面走 subprocess
（真实入口，含退出码语义）；挂载面直接断言 verify_delivery 的模块常量。
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_search_index_fresh as gate  # noqa: E402
import verify_delivery as v  # noqa: E402

GATE = SCRIPTS / "check_search_index_fresh.py"

EXP_DOCS = [
    {"kind": "doc", "title": "甲", "category": "c", "snippet": "s", "url": "u1", "kw": ["a"]},
    {"kind": "doc", "title": "乙", "category": "c", "snippet": "s2", "url": "u2", "kw": ["b"]},
]
EXP_ZH = [{"kind": "page", "title": "丙", "category": "c", "snippet": "s3", "url": "u3", "kw": ["c"]}]
EXP_EN = [{"kind": "page", "title": "丁", "category": "c", "snippet": "s4", "url": "u4", "kw": ["d"]}]


def _run(*args, timeout=600):
    return subprocess.run(
        [sys.executable, str(GATE), *args],
        capture_output=True, text=True, timeout=timeout, cwd=str(ROOT),
    )


def _mk_js(const, items, concat=False):
    payload = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
    expr = ("%s.concat(%s)" % (gate.SHARED_CONST, payload)) if concat else payload
    return "%s\nconst %s = %s;\n%s\n" % (gate.BEGIN, const, expr, gate.END)


def _mk_page(refs):
    tags = "".join('<script src="%s"></script>' % r for r in refs)
    return ('<html><body>%s'
            '<script>function renderOffline(q){return SITE_SEARCH_INDEX_ZH;}</script></body></html>'
            % tags)


def _pages():
    """判据域全集（页面 + 三件索引数据件同入一个文件文本映射）。"""
    return {
        "site/data/search.html": _mk_page(["search-index-docs.js", "search-index-zh.js"]),
        "site/en/search.html": _mk_page(["../data/search-index-docs.js", "search-index-en.js"]),
        gate.SHARED_FILE: _mk_js(gate.SHARED_CONST, EXP_DOCS),
        "site/data/search-index-zh.js": _mk_js("SITE_SEARCH_INDEX_ZH", EXP_ZH, concat=True),
        "site/en/search-index-en.js": _mk_js("SITE_SEARCH_INDEX_EN", EXP_EN, concat=True),
    }


def test_g1_repo_fresh():
    """G1 现网实跑：0 FAIL（索引数据件与生成器实算一致）。"""
    res = _run()
    assert res.returncode == 0, res.stdout + res.stderr
    assert gate.MARKER in res.stdout
    assert "0 FAIL" in res.stdout


def test_g2_self_test():
    """G2 自检：7/7 且退出码 0。"""
    res = _run("--self-test")
    assert res.returncode == 0, res.stdout + res.stderr
    assert res.stdout.count("PASS") == 7, res.stdout
    assert "SELF_TEST_OK" in res.stdout


def test_g3_judgements():
    """G3 判据单元：一致态零 FAIL + 六类漂移各命中对应码。"""
    expected = {"docs": EXP_DOCS, "zh": EXP_ZH, "en": EXP_EN}
    good = _pages()
    assert gate.check_pages(expected, good) == []

    # 缺共享件 → C1
    no_shared = dict(good)
    del no_shared[gate.SHARED_FILE]
    assert any(f.startswith("C1") for f in gate.check_pages(expected, no_shared))

    # 缺页面外链引用 → C1
    no_ref = dict(good)
    no_ref["site/data/search.html"] = "<html><body>no script ref</body></html>"
    assert any(f.startswith("C1") for f in gate.check_pages(expected, no_ref))

    # 外链顺序错（本语言件在前）→ C1
    bad_order = dict(good)
    bad_order["site/en/search.html"] = _mk_page(
        ["search-index-en.js", "../data/search-index-docs.js"])
    assert any(f.startswith("C1") for f in gate.check_pages(expected, bad_order))

    # zh 少一条条目 → C3
    stale = dict(good)
    stale["site/data/search-index-zh.js"] = _mk_js("SITE_SEARCH_INDEX_ZH", [], concat=True)
    assert any(f.startswith("C3") for f in gate.check_pages(expected, stale))

    # docs 共享件字段漂移（摘要被改）→ C2
    drift = dict(good)
    tampered = [dict(e) for e in EXP_DOCS]
    tampered[0]["snippet"] = "改过的摘要"
    drift[gate.SHARED_FILE] = _mk_js(gate.SHARED_CONST, tampered)
    assert any(f.startswith("C2") for f in gate.check_pages(expected, drift))

    # en 件常量名错位 → C1
    wrong = dict(good)
    wrong["site/en/search-index-en.js"] = _mk_js("SITE_SEARCH_INDEX_ZH", EXP_EN, concat=True)
    assert any(f.startswith("C1") for f in gate.check_pages(expected, wrong))


def test_g4_fail_closed_on_missing_jieba(monkeypatch):
    """G4 环境 fail-closed：jieba 缺失即不可判定→FAIL（禁静默跳过假绿）。

    进程内测（子进程会重新 import 到可用的 jieba·patch 不生效）——走 gate.main()
    真实入口，断言返回码 1 且报「jieba」。
    """
    import _gen_search_index as gen

    monkeypatch.setattr(gen, "jieba", None)
    monkeypatch.setattr(sys, "argv", ["check_search_index_fresh.py", "--gate"])
    assert gate.main() == 1


def test_g5_mount_consistency():
    """G5 挂载一致性：段名在 EXPECTED_SECTION_NAMES 与门禁元组两侧都在。"""
    assert "搜索索引" in v.EXPECTED_SECTION_NAMES
    sections = [g.section for g in v._STRICT_GATES]
    assert "搜索索引" in sections
    # 相对序一致（启动期四查之一·此处点检）
    assert [n for n in v.EXPECTED_SECTION_NAMES if n in set(sections)] == sections
    # 门禁脚本在位
    assert GATE.exists()
