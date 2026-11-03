"""W1110 四槽判据的 pytest 单测（盲审建议项 #6·此前仅有脚本内建 --self-test）。

覆盖要点：
- 第 54 槽：**同批号撞号必须判红**（盲审指出的漏判形态·本槽立项原场景）+ 基点默认取开叉点；
- 第 55 槽：BOM 口径（纯 ASCII 无 BOM 不判红）+ tracked 域排除 archive/；
- 第 56 槽：哈希口径与 generate_csp 逐字一致 + 交集判红（存量漂移不归本批）；
- 第 57 槽：四种自引用形态全覆盖 + 正常引用不误报 + 覆盖域含 site 下全部 .css。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import check_csp_drift as cspd  # noqa: E402
import check_css_var_selfref as selfref  # noqa: E402
import check_pitfall_id_unique as pitfall  # noqa: E402
import check_powershell_parse as psp  # noqa: E402
import generate_csp as gencsp  # noqa: E402

# ---- 第 54 槽：坑表编号唯一 ----

def test_pitfall_same_batch_duplicate_must_fail():
    """**同批号**撞号必须判红（盲审漏判形态·本槽立项原场景：两批各占同一号且批号字面相同）。"""
    lines = [
        "- **甲**（W1000 实证·E-500）：甲",
        "- **乙**（W1000 实证·E-500）：乙",
    ]
    dups, _stock, _added = pitfall.audit("HEAD", lines, added=["- **丙**（W1000 实证·E-500）：丙"])
    assert dups, "同批号撞号必须判红"
    assert dups[0][0] == "E-500"


def test_pitfall_new_entry_same_batch_num_as_existing_must_fail():
    """新条目批号与既有条目批号字面相同 ⇒ 也必须判红（不得按批号豁免）。"""
    lines = ["- **甲**（W1000 实证·E-500）：甲"]
    dups, _stock, _added = pitfall.audit("HEAD", lines, added=["- **乙**（W1000 实证·E-500）：乙"])
    assert dups, "批号字面相同的撞号必须判红"


def test_pitfall_cross_batch_duplicate_still_fails():
    """跨批撞号（回归锁）仍判红。"""
    lines = ["- **甲**（W1000 实证·E-500）：甲"]
    dups, _s, _a = pitfall.audit("HEAD", lines, added=["- **乙**（W1001 实证·E-500）：乙"])
    assert dups and dups[0][0] == "E-500"


def test_pitfall_no_false_positive_on_distinct_ids():
    lines = [
        "- **甲**（W1000 实证·E-500）：甲",
        "- **乙**（W1001 实证·E-501）：乙",
    ]
    dups, _s, _a = pitfall.audit("HEAD", lines, added=["- **丙**（W1002 实证·E-502）：丙"])
    assert not dups


def test_pitfall_base_resolves_to_fork_point():
    """默认基点必须是**本批开叉点**（merge-base）而非 HEAD（HEAD ⇒ CI 上恒绿）。"""
    base, desc = pitfall.resolve_base()
    assert base, "基点必须可解析"
    assert len(base) >= 7, "基点应为 commit hash"
    assert desc


# ---- 第 55 槽：PowerShell 解析 ----

def test_ps_bom_required_only_for_nonascii():
    """含非 ASCII 必须带 BOM；纯 ASCII 无 BOM 是安全的 ⇒ 不判红。"""
    ascii_only = b"Write-Output 'x'\n"
    assert not psp.contains_nonascii(ascii_only)
    cjk = "Write-Output '中文'\n".encode()
    assert psp.contains_nonascii(cjk)
    assert not psp.has_utf8_bom(cjk)
    assert psp.has_utf8_bom(b"\xef\xbb\xbf" + cjk)


def test_ps_tracked_domain_excludes_archive():
    """tracked 域排除 archive/（归档件只追加不改写）。"""
    files = psp.tracked_ps1()
    assert files == sorted(files)
    assert not any(f.startswith("archive/") for f in files)


# ---- 第 56 槽：CSP 增量漂移 ----

def test_csp_hash_matches_generate_csp口径():
    """哈希口径必须与 generate_csp 逐字一致（归一后）——否则恒不匹配/恒匹配。"""
    html = ("<html><head><meta http-equiv=\"Content-Security-Policy\" content=\"x\">"
            "</head><body><script>var a = 1;</script></body></html>")
    gen = gencsp.inline_script_hashes(html)
    mine = [cspd.block_hash(b) for b in cspd.inline_blocks(html)]
    assert len(gen) == len(mine) == 1
    assert gen[0].strip("'\"") == mine[0], "两侧哈希归一后必须逐字相等"


def test_csp_meta_hashes_normalised():
    """meta 内带单引号的哈希须去引号（否则永不相等 ⇒ 假红）。"""
    h = cspd.block_hash("var a = 1;")
    html = ('<html><head><meta http-equiv="Content-Security-Policy" '
            'content="default-src \'self\'; script-src \'self\' \'%s\'"></head></html>' % h)
    assert cspd.meta_hashes(html) == [h]


def test_csp_intersection_excludes_stock_drift():
    """交集判红：存量漂移页不在本批改动页集合 ⇒ 不判红。"""
    html = '<html><head><meta http-equiv="Content-Security-Policy" content="x"></head>'
    issues, _notes = cspd.evaluate([], {}, {"other.html": html})
    assert not issues, "存量漂移不得归本批"


# ---- 第 57 槽：CSS 变量自引用 ----

def test_selfref_covers_all_four_forms():
    """四种自引用形态全覆盖（基本 / 带 fallback / 函数名大写 / 嵌套）。"""
    for css in (
        "--a: var(--a);",
        "--a: var(--a, #fff);",
        "--a: VAR(--a);",
        "--a: var(--b, var(--a));",
    ):
        hits = selfref.find_selfrefs(css)
        assert hits, "未识别自引用：%s" % css
        assert hits[0][0] == "--a"


def test_selfref_normal_reference_not_flagged():
    """正常引用与字面值不得误报。"""
    for css in ("--a: var(--b);", "--a: #fff;", "--a: var(--b, #ccc);"):
        assert not selfref.find_selfrefs(css), "误报：%s" % css


def test_selfref_domain_includes_all_site_css():
    """覆盖域含 site 下全部 .css（不止 tokens.css·盲审建议项 #2）。"""
    names = [os.path.basename(p) for p in selfref.iter_site_files()]
    assert "tokens.css" in names
    assert "system.css" in names, "system.css 必须在扫描域内"
