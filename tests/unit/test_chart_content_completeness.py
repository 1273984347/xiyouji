"""check_chart_content_completeness 的专项单测（第 82 门禁「图表内容完备度」）。

测的是**纯逻辑 + 真实页面读数**（不启浏览器 ⇒ CI 可跑、快、可复算）：
  1. 脚本自带 self-test 全绿（内存负样本：违例必红 · 正样本必绿）
  2. 真仓负样本：以**真实页面**为底本注入违例 ⇒ 判红；撤销注入 ⇒ 读数复原
     （注入只发生在内存字符串里·**绝不改真实文件**）
  3. 属性名 / CSS 类名不算「可见来源标注」（防「有属性无文本」误判）
  4. 结论伪命中：正文提到「结论」二字而无结论区块 ⇒ 判红
  5. tooltip 三通路：svg <title> / title 属性 / 脚本绑定；未绑定到图元 ⇒ 判红
  6. 图例：多系列无图例判红；单系列豁免登记 ⇒ 绿；页面改多系列 ⇒ 豁免失效 ⇒ 红
  7. 基线语义：基线内不计 FAIL · 基线外新增计 FAIL（共用 freeze_gate）
  8. 零命中 fail-closed（探针没跑到任何页 ⇒ 判红）
  9. 输出末行格式恒为「---- 第 82 门禁 图表内容完备度：N FAIL ----」
"""

import os
import re
import sys
from pathlib import Path

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import check_chart_content_completeness as cc  # noqa: E402
from check_chart_content_completeness import analyze_html  # noqa: E402,F401  （第 42 槽测试面引用形态）

TARGET = os.path.join(ROOT, "site", "data", "business-model.html")


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


# ------------------------------------------------------------ 1. 自测自证
def test_script_self_test_passes():
    """脚本自带 --self-test 必须全绿（违例必红 · 正样本必绿）。"""
    assert cc.self_test() == 0


# ------------------------------------------------------------ 2. 真仓负样本
def test_real_page_injected_violation_is_red():
    """真仓页面注入违例 ⇒ 判红（注入只在内存·不改真实文件）。

    注入手法：把页内**全部来源语义词**替换成中性词 ⇒ 必然不再命中来源语义。
    """
    html = _read(TARGET)
    broken = re.sub(cc.SOURCE_TEXT_RE.pattern, "资料说明", html)
    assert broken != html, "注入失败：目标页不含来源语义词（页面线可能已修）"
    assert cc.analyze_html(broken)["C1"][0] is False


def test_real_page_restored_after_injection():
    """撤销注入 ⇒ 读数复原（与注入前一致）。"""
    html = _read(TARGET)
    before = cc.analyze_html(html)
    broken = re.sub(cc.SOURCE_TEXT_RE.pattern, "资料说明", html)
    assert cc.analyze_html(broken)["C1"][0] is False
    assert cc.analyze_html(html)["C1"][0] == before["C1"][0]


def test_real_page_tooltip_injection_is_red():
    """真仓页面抽掉 tooltip 通路 ⇒ 判红（脚本绑定 + svg <title> 两条都抽掉）。"""
    html = _read(TARGET)
    broken = re.sub(cc.TOOLTIP_WRITE_RE.pattern, "noop", html)
    broken = re.sub(r"<title\b[^>]*>.*?</title>", "", broken, flags=re.S)
    assert cc.analyze_html(broken)["C3"][0] is False
    assert cc.analyze_html(html)["C3"][0] == cc.analyze_html(html)["C3"][0]


# ------------------------------------------------------------ 3. 属性名不算数
def test_attribute_name_only_is_not_source_annotation():
    """只有 HTML 属性名（data-source=）没有可见文本 ⇒ 判红。"""
    html = '<div class="chart" data-source="site/data/json/x.json"><span>图</span></div>'
    assert cc.analyze_html(html)["C1"][0] is False


def test_css_class_name_only_is_not_source_annotation():
    """只有 CSS 类名（.source-note）没有可见文本 ⇒ 判红。"""
    html = "<style>.source-note{color:red}</style><div class='source-note'></div>"
    assert cc.analyze_html(html)["C1"][0] is False


def test_script_text_is_not_visible_text():
    """<script>/<style> 里的来源文本不算读者可见 ⇒ 判红。"""
    html = "<style>.a{content:'数据来源：site/data/json/x.json'}</style><script>var s='数据来源：x.json';</script>"
    assert cc.analyze_html(html)["C1"][0] is False


# ------------------------------------------------------------ 4. 结论伪命中
def test_conclusion_word_in_body_is_pseudo_hit():
    """正文里恰好提到「结论」二字而所在区块无结论语义 ⇒ 判红。"""
    html = "<section><h2>数据概览</h2><p>本章结论将在后文给出。</p></section>"
    assert cc.analyze_html(html)["C2"][0] is False


def test_conclusion_block_heading_counts():
    """标题命中结论语义 + 有正文 ⇒ 绿。"""
    html = "<section><h2>关键洞察</h2><p>三个趋势显示……</p></section>"
    assert cc.analyze_html(html)["C2"][0] is True


def test_conclusion_block_heading_without_body_is_red():
    """结论区块只有标题没有正文 ⇒ 判红（标题不算结论内容）。"""
    html = "<section><h2>Key Insights</h2><div class='insight-box'></div></section>"
    assert cc.analyze_html(html)["C2"][0] is False


# ------------------------------------------------------------ 5. tooltip 三通路
def test_tooltip_svg_title_child():
    assert cc.analyze_html("<svg><g><title>唐僧 81 难</title></g></svg>")["C3"][0] is True


def test_tooltip_title_attribute():
    html = '<svg><rect x="1" y="1" width="4" height="4" title="灵山势力 42"></rect></svg>'
    assert cc.analyze_html(html)["C3"][0] is True


def test_tooltip_page_head_title_is_not_chart_tooltip():
    """<head><title> 是页面标题·不是图元提示 ⇒ 判红。"""
    html = "<html><head><title>详解西游记</title></head><body><svg><rect/></svg></body></html>"
    assert cc.analyze_html(html)["C3"][0] is False


def test_tooltip_css_without_binding_is_red():
    """只有 .chart-tooltip CSS 无绑定语句 ⇒ 判红。"""
    html = "<style>.chart-tooltip{position:absolute}</style><svg><rect/></svg>"
    assert cc.analyze_html(html)["C3"][0] is False


def test_tooltip_bound_to_non_chart_element_is_red():
    """tooltip 绑定在非图元元素上 ⇒ 判红（没绑定到图元不算数）。"""
    html = "<script>document.querySelector('.btn').on('mouseover', function(){ show('tooltip'); });</script>"
    assert cc.analyze_html(html)["C3"][0] is False


# ------------------------------------------------------------ 6. 图例与豁免
def test_multi_series_without_legend_is_red():
    html = "<script>d3.scaleOrdinal().range(['#a','#b']);</script><div class='chart'></div>"
    series, multi, has_legend, _ = cc.analyze_html(html)["legend"]
    assert multi and not has_legend


def test_multi_series_with_legend_is_green():
    html = (
        "<script>d3.scaleOrdinal().range(['#a','#b']);</script>"
        "<div class='chart'><div class='legend'><span class='legend-item'>天庭</span>"
        "<span class='legend-item'>灵山</span></div></div>"
    )
    series, multi, has_legend, _ = cc.analyze_html(html)["legend"]
    assert multi and has_legend


def test_exemption_invalid_when_page_becomes_multi_series():
    """豁免登记 series=1，页面改多系列 ⇒ 豁免失效（改页面骗不过判据）。"""
    assert cc._exemption_valid("series=1", 1) is True
    assert cc._exemption_valid("series=1", 2) is False
    assert cc._exemption_valid("series=2", 1) is False
    assert cc._exemption_valid("series=0", 0) is True
    assert cc._exemption_valid("series=1", 0) is False  # 声明与实测不符 ⇒ 失效


def test_exemptions_file_entries_are_wellformed():
    """豁免清单每行须 <页面>|<声明>|<依据>，声明属四类词表且依据非空。"""
    mapping, problems = cc.read_exemptions(cc.EXEMPTIONS)
    assert not problems, "豁免清单格式问题：%s" % problems
    for rel, entry in mapping.items():
        assert rel.startswith("site/"), "豁免条目路径异常：%s" % rel
        spec = entry.split("|", 1)[0]
        assert spec.startswith("series=") or spec in cc.RENDER_VERDICTS, "豁免声明不在词表：%s" % spec
        parts = entry.split("|", 1)
        assert len(parts) == 2 and parts[1].strip(), "豁免依据为空或格式异常：%s" % rel


def test_render_exemption_requires_audit_match():
    """render=* 声明须与渲染复核档案一致：一致才豁免·multi-nolegend 判 C4·不一致即失效。"""
    audit_ok = {"site/data/x.html": {"verdict": "multi_legend"}}
    assert cc._resolve_legend_exemption("site/data/x.html", "render=legend", 0, audit_ok)[0] == "exempt"
    assert cc._resolve_legend_exemption("site/data/x.html", "render=multi-nolegend", 0, audit_ok)[0] == "invalid"
    audit_bad = {"site/data/x.html": {"verdict": "multi_nolegend"}}
    assert cc._resolve_legend_exemption("site/data/x.html", "render=multi-nolegend", 0, audit_bad)[0] == "c4"
    assert cc._resolve_legend_exemption("site/data/x.html", "render=legend", 0, audit_bad)[0] == "invalid"
    assert cc._resolve_legend_exemption("site/data/x.html", "render=nochart", 0, {})[0] == "invalid"


def test_render_audit_stale_page_invalidates_exemption():
    """页面内容改了而渲染档案未刷新 ⇒ 豁免自动失效（改页面骗不过判据）。"""
    audit = {"site/data/x.html": {"verdict": "multi_legend", "sha": "aaaa"}}
    status, detail = cc._resolve_legend_exemption("site/data/x.html", "render=legend", 0, audit, "bbbb")
    assert status == "invalid"
    assert "过期" in detail
    status2, _ = cc._resolve_legend_exemption("site/data/x.html", "render=legend", 0, audit, "aaaa")
    assert status2 == "exempt"


def test_render_audit_sha_matches_current_pages():
    """档案记录的页面哈希须与当前页面一致（否则豁免失效 ⇒ 强制重跑渲染复核）。"""
    audit, problems = cc.read_render_audit(cc.RENDER_AUDIT)
    assert not problems
    mapping, _ = cc.read_exemptions(cc.EXEMPTIONS)
    for rel, entry in mapping.items():
        spec = entry.split("|", 1)[0]
        if spec not in cc.RENDER_VERDICTS:
            continue
        row = audit.get(rel) or {}
        assert row.get("sha") == cc._page_sha(Path(ROOT) / rel), "渲染档案过期（页面已改）：%s" % rel


def test_render_audit_matches_exemptions_file():
    """清单里的 render=* 声明须与渲染档案 verdict 一致（改清单骗不过判据）。"""
    audit, problems = cc.read_render_audit(cc.RENDER_AUDIT)
    assert not problems, "渲染复核档案问题：%s" % problems
    mapping, _ = cc.read_exemptions(cc.EXEMPTIONS)
    checked = 0
    for rel, entry in mapping.items():
        spec = entry.split("|", 1)[0]
        if spec not in cc.RENDER_VERDICTS:
            continue
        checked += 1
        assert audit.get(rel, {}).get("verdict") == cc.RENDER_VERDICTS[spec], (
            "豁免声明与渲染档案不符：%s（声明 %s·档案 %s）"
            % (rel, spec, audit.get(rel, {}).get("verdict"))
        )
    assert checked > 0, "清单里没有 render=* 声明·渲染级复核未生效"


def test_missing_render_audit_is_reported(monkeypatch, tmp_path):
    """渲染复核档案缺失 ⇒ 报缺（fail-closed 的前置信号·不得静默通过）。"""
    monkeypatch.setattr(cc, "RENDER_AUDIT", tmp_path / "no_such_audit.json")
    res = cc.scan("all")
    assert any("渲染复核档案缺失" in p for p in res["exem_problems"])


# ------------------------------------------------------------ 7. 基线语义
def test_baseline_inside_not_counted_and_outside_counted():
    viol = ["site/data/x.html|C1|缺可读数据来源标注"]
    res = cc.freeze_gate.evaluate(viol, set(viol), strict=False)
    assert res["new_fail"] == []
    res = cc.freeze_gate.evaluate(viol, set(), strict=False)
    assert len(res["new_fail"]) == 1


def test_baseline_file_exists_and_documents_command():
    """基线文件存在，且首部写明生成命令与语义（可复算）。"""
    assert os.path.exists(cc.BASELINE), "基线文件缺失：%s" % cc.BASELINE
    head = _read(cc.BASELINE).splitlines()[:6]
    joined = "\n".join(head)
    assert "--generate-baseline" in joined, "基线首部未写生成命令"
    assert "语义" in joined, "基线首部未写语义说明"




def test_missing_baseline_is_fail_closed(monkeypatch, capsys):
    """基线文件缺失 ⇒ fail-closed 判红（拒绝通过）。"""
    fake = {
        "viol": [],
        "pages": 1,
        "chart_pages": 1,
        "stats": {"C1": 0, "C2": 0, "C3": 0, "C4": 0, "C5": 0},
        "fail_closed": False,
        "exem_problems": [],
        "stale_exemptions": [],
        "exempt_used": [],
    }
    monkeypatch.setattr(cc, "scan", lambda scope="all", exem_path=None: fake)
    monkeypatch.setattr(cc.freeze_gate, "read_baseline", lambda path: (set(), ["基线文件缺失"]))
    monkeypatch.setattr(sys, "argv", ["check_chart_content_completeness.py"])
    assert cc.main() == 1
    out = capsys.readouterr().out
    assert "fail-closed" in out


def test_missing_exemptions_file_is_fail_closed(monkeypatch, capsys):
    """豁免清单缺失 ⇒ fail-closed 判红（判据输入缺一不可）。"""
    fake = {
        "viol": [],
        "pages": 1,
        "chart_pages": 1,
        "stats": {"C1": 0, "C2": 0, "C3": 0, "C4": 0, "C5": 0},
        "fail_closed": False,
        "exem_problems": ["豁免清单缺失: x（fail-closed·拒绝通过）"],
        "stale_exemptions": [],
        "exempt_used": [],
    }
    monkeypatch.setattr(cc, "scan", lambda scope="all", exem_path=None: fake)
    monkeypatch.setattr(cc.freeze_gate, "read_baseline", lambda path: (set(), []))
    monkeypatch.setattr(sys, "argv", ["check_chart_content_completeness.py"])
    assert cc.main() == 1
    out = capsys.readouterr().out
    assert "fail-closed" in out


def test_real_scan_shape():
    """真实扫描：页数 > 0 · 含图页数 > 0 · 违例键格式正确（读数面健康）。"""
    res = cc.scan("all")
    assert res["pages"] > 0
    assert res["chart_pages"] > 0
    assert res["fail_closed"] is False
    for key in res["viol"]:
        assert re.match(r"^site/.+\|C[1-5]\|.+$", key), "违例键格式异常：%s" % key


# ------------------------------------------------------------ 8. 零命中 fail-closed
def test_zero_hit_is_fail_closed():
    """扫描面为空 ⇒ fail-closed 判红（不许静默通过）。"""
    res = cc.scan(scope="none")
    assert res["pages"] == 0
    assert res["fail_closed"] is True


# ------------------------------------------------------------ 9. 末行格式
def test_final_line_format_is_fixed(monkeypatch, capsys):
    """输出末行恒为「---- 第 82 门禁 图表内容完备度：N FAIL ----」。"""
    fake = {
        "viol": ["site/data/x.html|C1|缺可读数据来源标注"],
        "pages": 1,
        "chart_pages": 1,
        "stats": {"C1": 1, "C2": 0, "C3": 0, "C4": 0, "C5": 0},
        "fail_closed": False,
        "exem_problems": [],
        "stale_exemptions": [],
        "exempt_used": [],
    }
    monkeypatch.setattr(cc, "scan", lambda scope="all", exem_path=None: fake)
    monkeypatch.setattr(cc.freeze_gate, "read_baseline", lambda path: (set(), []))
    monkeypatch.setattr(sys, "argv", ["check_chart_content_completeness.py", "--report"])
    assert cc.main() == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert out[-1] == "---- 第 82 门禁 图表内容完备度：1 FAIL ----", "末行格式漂移：%s" % out[-1]
    assert re.match(r"^---- 第 82 门禁 图表内容完备度：\d+ FAIL ----$", out[-1])
    marker_lines = [ln for ln in out if ln.startswith("---- 第 82 门禁")]
    assert len(marker_lines) == 1, "marker 前缀行数应恒为 1（verify_delivery 汇总行解析按前缀抓行）：%s" % marker_lines


def test_final_line_reports_fail_count(monkeypatch, capsys):
    """基线外新增 N 条 ⇒ 末行报 N FAIL。"""
    fake = {
        "viol": ["site/data/x.html|C1|缺可读数据来源标注"],
        "pages": 1,
        "chart_pages": 1,
        "stats": {"C1": 1, "C2": 0, "C3": 0, "C4": 0, "C5": 0},
        "fail_closed": False,
        "exem_problems": [],
        "stale_exemptions": [],
        "exempt_used": [],
    }
    monkeypatch.setattr(cc, "scan", lambda scope="all", exem_path=None: fake)
    monkeypatch.setattr(cc.freeze_gate, "read_baseline", lambda path: (set(), []))
    monkeypatch.setattr(sys, "argv", ["check_chart_content_completeness.py"])
    assert cc.main() == 1
    out = capsys.readouterr().out.strip().splitlines()
    assert out[-1] == "---- 第 82 门禁 图表内容完备度：1 FAIL ----", "末行格式漂移：%s" % out[-1]


def test_baseline_frozen_violation_reports_zero_fail(monkeypatch, capsys):
    """违例全在基线内 ⇒ 末行报 0 FAIL（存量冻结）。"""
    fake = {
        "viol": ["site/data/x.html|C1|缺可读数据来源标注"],
        "pages": 1,
        "chart_pages": 1,
        "stats": {"C1": 1, "C2": 0, "C3": 0, "C4": 0, "C5": 0},
        "fail_closed": False,
        "exem_problems": [],
        "stale_exemptions": [],
        "exempt_used": [],
    }
    monkeypatch.setattr(cc, "scan", lambda scope="all", exem_path=None: fake)
    monkeypatch.setattr(
        cc.freeze_gate, "read_baseline", lambda path: ({"site/data/x.html|C1|缺可读数据来源标注"}, [])
    )
    monkeypatch.setattr(sys, "argv", ["check_chart_content_completeness.py"])
    assert cc.main() == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert out[-1] == "---- 第 82 门禁 图表内容完备度：0 FAIL ----", "末行格式漂移：%s" % out[-1]
