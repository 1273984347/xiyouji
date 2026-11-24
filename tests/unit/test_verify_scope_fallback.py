"""verify_delivery 判据单测：scope 分级 + 内嵌回退（W1312）。

为什么补这三条（都是「判据决定门禁跑不跑」的开关，错了不报错只静默少跑）：
  1. _parse_scope：CLI 取值形态（空/空格式/等号式）决定本轮 scope 档位；
     取错 ⇒ 本该跑的段被跳过，而汇总行仍可能全绿。
  2. _classify_scope：auto 档按变更路径白名单分类；分类错 ⇒ docs 档漏跑站点段
     （或反之）；任何越界文件必须保守回退 full（W698 scope 分级的 fail-safe 根）。
  3. _has_embedded_fallback：file:// 铁律的自动验证判据（第 22 槽）；公共层内联
     副本标记里的 FALLBACK 字样是注释副本，不得冒充页面自身的回退数据。

口径：只钉现有契约，不钉实现细节；每例只断言一个行为。
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

import verify_delivery as v  # noqa: E402

# ---------- _parse_scope：缺省与两种合法形态 ----------

def test_parse_scope_defaults_to_full():
    assert v._parse_scope([]) == "full"


def test_parse_scope_reads_space_form():
    assert v._parse_scope(["--scope", "docs"]) == "docs"


def test_parse_scope_reads_equals_form():
    assert v._parse_scope(["--scope=site"]) == "site"


def test_parse_scope_ignores_unrelated_flags():
    assert v._parse_scope(["--health", "--profile"]) == "full"


def test_parse_scope_missing_value_stays_full():
    """--scope 在末位没有取值 ⇒ 不得把空当档位，仍回退 full。"""
    assert v._parse_scope(["--scope"]) == "full"


# ---------- _classify_scope：白名单三态 + 越界保守回退 ----------

def test_classify_docs_only():
    assert v._classify_scope({"docs/01-逐回解读/a.md", "CHANGELOG.md"}) == "docs"


def test_classify_site_only():
    assert v._classify_scope({"site/data/x.html"}) == "site"


def test_classify_docs_plus_site_is_site():
    """文档 + 站点混合批 ⇒ site（站点段与级联文档段都要跑）。"""
    assert v._classify_scope({"docs/a.md", "site/data/x.html"}) == "site"


@pytest.mark.parametrize("out_of_scope", [
    "scripts/verify_delivery.py",      # 门禁脚本本体
    "tests/unit/test_x.py",            # 测试面
    ".github/workflows/ci.yml",        # CI 配置
    "scripts/output/chart-values-baseline.txt",  # 基线
])
def test_classify_any_out_of_whitelist_is_full(out_of_scope):
    """任何越界文件 ⇒ full（保守缺省·跳过任一门禁族都不安全）。"""
    assert v._classify_scope({"docs/a.md", out_of_scope}) == "full"


def test_classify_normalizes_backslash():
    """Windows 反斜杠路径先归一化再分类（否则 docs 批会误判 full）。"""
    assert v._classify_scope({"docs\\01-逐回解读\\a.md"}) == "docs"


# ---------- _has_embedded_fallback：file:// 铁律判据 ----------

def test_embedded_fallback_detects_embedded_data(tmp_path):
    p = tmp_path / "page.html"
    p.write_text("<script>const EMBEDDED_DATA = {a: 1};</script>", encoding="utf-8")
    assert v._has_embedded_fallback(str(p)) is True


def test_embedded_fallback_detects_const_data(tmp_path):
    p = tmp_path / "page.html"
    p.write_text("<script>const data = [{x: 1}];</script>", encoding="utf-8")
    assert v._has_embedded_fallback(str(p)) is True


def test_embedded_fallback_false_for_static_page(tmp_path):
    p = tmp_path / "page.html"
    p.write_text("<p>纯静态页，无数据回退</p>", encoding="utf-8")
    assert v._has_embedded_fallback(str(p)) is False


def test_embedded_fallback_ignores_inlined_css_marker(tmp_path):
    """公共层内联副本标记内的 FALLBACK 字样是注释副本，不得冒充页面回退。

    W1281：_INLINED_MARKER_RE 先剔除该标记再判，本测试钉住剔除顺序。
    """
    p = tmp_path / "page.html"
    p.write_text(
        "<!-- INLINED CSS shared layer\n.fallback-grid { display: grid; } FALLBACK\n-->\n"
        "<p>页面自身无回退数据</p>",
        encoding="utf-8",
    )
    assert v._has_embedded_fallback(str(p)) is False


def test_embedded_fallback_missing_file_is_false():
    """文件不存在 ⇒ _read 返回空串 ⇒ 判 False（由调用方按失败处理，此处只钉返回值）。"""
    assert v._has_embedded_fallback("tmpe/__not_exists__.html") is False
