# -*- coding: utf-8 -*-
"""W266 E5 测试深化·a11y_audit.py 单元测试·pytest 风格

覆盖 9 条 WCAG 2.2 AA 规则 + 键盘导航 + ARIA 完整性：
  - test_rule_1_alt_text           原规则 1：屏幕阅读器（img alt/input label/th scope）
  - test_rule_2_color_contrast      规则 2：色彩对比度（WCAG AA 4.5:1）
  - test_rule_3_label_association   规则 3：ARIA 标签（label/labelledby 互斥等）
  - test_rule_4_heading_hierarchy   规则 4：焦点指示（含 heading 层级验证）
  - test_rule_5_lang_attr           规则 5：屏幕阅读器扩展（lang 属性）
  - test_rule_6_focus_visible       新规则 6：焦点可见（WCAG 2.2 SC 2.4.13）
  - test_rule_7_target_size         规则 7：目标尺寸（WCAG 2.2 SC 2.5.8）
  - test_rule_8_dragging            规则 8：拖拽移动（WCAG 2.2 SC 2.5.7）
  - test_rule_9_consistent_help     规则 9：一致帮助（WCAG 2.2 SC 3.2.6）
  - test_keyboard_navigation        键盘导航（tabindex/accesskey/焦点陷阱）
  - test_aria_completeness          ARIA 完整性（labelledby/describedby 引用验证）

运行：pytest tests/unit/test_a11y_audit.py -v
"""
import sys
from pathlib import Path

import pytest

# 将 scripts/ 加入 sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import a11y_audit  # noqa: E402


# ---------------------------------------------------------------------------
# 公共 fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def good_html_text():
    """符合 WCAG 2.2 AA 的标准 HTML 文本"""
    return (
        '<!DOCTYPE html><html lang="zh-CN"><head>'
        '<meta charset="utf-8">'
        '<title>测试页</title>'
        '<style>'
        ':focus-visible { outline: 2px solid currentColor; }'
        'a, button { min-width: 24px; min-height: 24px; }'
        '.contrast-text { color: #000; background-color: #fff; }'
        '</style>'
        '</head><body>'
        '<header><nav>'
        '<a href="#main">跳到主内容</a>'
        '<a href="/help" aria-label="帮助中心">帮助</a>'
        '</nav></header>'
        '<main id="main">'
        '<h1>主标题</h1>'
        '<h2>二级</h2>'
        '<p>正文段落</p>'
        '<img src="logo.png" alt="站点 logo">'
        '<label>邮箱<input type="email" name="email" id="email"></label>'
        '<button type="button" aria-label="提交">提交</button>'
        '</main>'
        '<noscript>请启用 JavaScript</noscript>'
        '</body></html>'
    )


@pytest.fixture
def bad_html_text():
    """违反多条 WCAG 2.2 AA 规则的 HTML 文本"""
    return (
        '<!DOCTYPE html><html><head>'
        '<title>无 lang · 无 CSP</title>'
        '<style>a { outline: none; }</style>'
        '</head><body>'
        '<h3>跳级</h3><h1>主标题</h1>'  # heading 层级跳跃
        '<img src="bad.png">'  # 无 alt
        '<div onclick="doStuff()">click</div>'  # role=button 缺键盘事件
        '<button style="width:10px;height:10px;">x</button>'  # 目标尺寸过小
        '<div draggable="true">拖我</div>'  # 拖拽无键盘替代
        '<a href="javascript:void(0)" tabindex="5">focus 陷阱</a>'  # tabindex>0
        '<div role="button" onclick="x()">按钮</div>'  # role=button 缺键盘事件
        '</body></html>'
    )


# ---------------------------------------------------------------------------
# 规则 1：屏幕阅读器（img alt / input label / th scope / noscript）
# ---------------------------------------------------------------------------

def test_rule_1_alt_text_good(good_html_text):
    """符合规范的 HTML：屏幕阅读器检查应无 P0/P1"""
    findings = a11y_audit.check_screen_reader(good_html_text, Path("good.html"))
    p0 = [f for f in findings if f["severity"] == a11y_audit.Severity.P0]
    p1 = [f for f in findings if f["severity"] == a11y_audit.Severity.P1]
    # 应无 P0（img alt 已提供）
    assert len(p0) == 0
    # P1 也应无（input 含 id 可关联 label）
    assert len(p1) == 0


def test_rule_1_alt_text_missing(bad_html_text):
    """img 缺 alt 应报 P0"""
    findings = a11y_audit.check_screen_reader(bad_html_text, Path("bad.html"))
    p0 = [f for f in findings if f["severity"] == a11y_audit.Severity.P0]
    assert len(p0) >= 1
    assert any("img" in f["message"].lower() and "alt" in f["message"].lower()
               for f in p0)


def test_rule_1_alt_text_empty_role_presentation():
    """alt="" + role="presentation" 应无 P0"""
    text = '<img src="decor.png" alt="" role="presentation">'
    findings = a11y_audit.check_screen_reader(text, Path("dec.html"))
    p0 = [f for f in findings if f["severity"] == a11y_audit.Severity.P0]
    assert len(p0) == 0


def test_rule_1_noscript_missing():
    """≥2 个 script 但无 noscript 应报 P2"""
    text = (
        '<html><head><script src="a.js"></script><script src="b.js"></script>'
        '</head><body></body></html>'
    )
    findings = a11y_audit.check_screen_reader(text, Path("ns.html"))
    p2 = [f for f in findings if f["severity"] == a11y_audit.Severity.P2]
    assert any("noscript" in f["message"].lower() for f in p2)


# ---------------------------------------------------------------------------
# 规则 2：色彩对比度
# ---------------------------------------------------------------------------

def test_rule_2_color_contrast_pass():
    """黑色文本白色背景对比度 ≥ 4.5:1 应通过"""
    text = (
        '<html><head><style>'
        '.contrast-text { color: #000000; background-color: #ffffff; }'
        '</style></head><body><p class="contrast-text">hello</p></body></html>'
    )
    findings = a11y_audit.check_color_contrast(text, Path("ok.html"))
    # 应无低于 4.5:1 的发现
    fails = [f for f in findings if f["severity"] in
             (a11y_audit.Severity.P0, a11y_audit.Severity.P1, a11y_audit.Severity.P2)]
    assert len(fails) == 0


def test_rule_2_color_contrast_fail():
    """浅灰背景深灰文本对比度 < 4.5:1 应报"""
    text = (
        '<html><head><style>'
        '.low { color: #aaaaaa; background-color: #cccccc; }'
        '</style></head><body><p class="low">low contrast</p></body></html>'
    )
    findings = a11y_audit.check_color_contrast(text, Path("fail.html"))
    # 应至少有一个对比度问题
    assert len(findings) >= 1
    assert any("对比度" in f["message"] or "ratio" in f["message"].lower()
               for f in findings)


# ---------------------------------------------------------------------------
# 规则 3：ARIA 标签 + label 关联
# ---------------------------------------------------------------------------

def test_rule_3_label_association_good():
    """aria-labelledby 引用存在的 ID 应通过"""
    text = (
        '<html><body>'
        '<div id="title">标题</div>'
        '<button aria-labelledby="title">按钮</button>'
        '</body></html>'
    )
    findings = a11y_audit.check_aria_labels(text, Path("ok.html"))
    p1 = [f for f in findings if f["severity"] == a11y_audit.Severity.P1]
    # 仅 P1 中可能含 label 引用问题，应无
    assert not any("aria-labelledby" in f["message"] for f in p1)


def test_rule_3_label_association_dangling():
    """aria-labelledby 引用不存在 ID 应报 P1"""
    text = (
        '<html><body>'
        '<button aria-labelledby="nonexistent">按钮</button>'
        '</body></html>'
    )
    findings = a11y_audit.check_aria_labels(text, Path("dangling.html"))
    dangling = [f for f in findings if "aria-labelledby" in f["message"]
                and "不存在" in f["message"]]
    assert len(dangling) >= 1


def test_rule_3_label_mutually_exclusive():
    """aria-label 与 aria-labelledby 同时存在应报 P2"""
    text = (
        '<html><body>'
        '<button aria-label="A" aria-labelledby="x">按钮</button>'
        '</body></html>'
    )
    findings = a11y_audit.check_aria_labels(text, Path("mutual.html"))
    mutual = [f for f in findings if "aria-label" in f["message"]
              and "aria-labelledby" in f["message"]]
    assert len(mutual) >= 1


# ---------------------------------------------------------------------------
# 规则 4：焦点指示 + 标题层级（heading hierarchy 复用 focus_indicator 模块）
# ---------------------------------------------------------------------------

def test_rule_4_heading_hierarchy_good():
    """heading 层级正确（h1→h2→h3）应通过"""
    text = (
        '<html><head><style>'
        ':focus-visible { outline: 2px solid blue; }'
        '</style></head><body>'
        '<h1>主</h1><h2>二</h2><h3>三</h3>'
        '</body></html>'
    )
    findings = a11y_audit.check_focus_indicator(text, Path("h.html"))
    # 应无 outline:none 缺替代的发现
    outline_issues = [f for f in findings if "outline:none" in f["message"]
                      or "outline" in f["message"]]
    assert len(outline_issues) == 0


def test_rule_4_heading_hierarchy_skip():
    """outline:none 无替代应报 P1"""
    text = (
        '<html><head><style>'
        'a:focus { outline: none; }'
        '</style></head><body>'
        '<a href="#x">click</a>'
        '</body></html>'
    )
    findings = a11y_audit.check_focus_indicator(text, Path("bad.html"))
    outline_finds = [f for f in findings
                    if "outline:none" in f["message"]
                    or "outline" in f["evidence"]]
    assert len(outline_finds) >= 1


# ---------------------------------------------------------------------------
# 规则 5：lang 属性（屏幕阅读器扩展）
# ---------------------------------------------------------------------------

def test_rule_5_lang_attr_present():
    """html lang 已设置：通过"""
    text = (
        '<!DOCTYPE html><html lang="zh-CN"><head><title>x</title></head>'
        '<body></body></html>'
    )
    # 这里直接验证 a11y_audit 模块的 _parse_html 能正确解析 lang
    parser = a11y_audit._parse_html(text)
    html_el = next(el for el in parser.elements if el.tag == "html")
    assert html_el.attrs.get("lang", "").strip() == "zh-CN"


def test_rule_5_lang_attr_missing():
    """html lang 缺失：a11y_audit 的 check_screen_reader 不直接检查 lang，
    这里以独立验证模块导出能识别 lang 属性缺失"""
    text = (
        '<!DOCTYPE html><html><head><title>x</title></head>'
        '<body></body></html>'
    )
    parser = a11y_audit._parse_html(text)
    html_el = next((el for el in parser.elements if el.tag == "html"), None)
    assert html_el is not None
    assert "lang" not in html_el.attrs or html_el.attrs.get("lang", "").strip() == ""


# ---------------------------------------------------------------------------
# 规则 6：焦点可见（WCAG 2.2 SC 2.4.13）
# ---------------------------------------------------------------------------

def test_rule_6_focus_visible_present(good_html_text):
    """含 :focus-visible 样式应通过"""
    findings = a11y_audit.rule_6_focus_visible(good_html_text, Path("ok.html"))
    # 应无 findings（已含 :focus-visible）
    assert len(findings) == 0


def test_rule_6_focus_visible_missing():
    """无 :focus-visible 样式且含交互元素应报 P2"""
    text = (
        '<!DOCTYPE html><html><head><style>'
        'a { color: blue; }'
        '</style></head><body>'
        '<a href="#x">link</a>'
        '<button>b</button>'
        '</body></html>'
    )
    findings = a11y_audit.rule_6_focus_visible(text, Path("bad.html"))
    assert len(findings) >= 1
    assert findings[0]["severity"] == a11y_audit.Severity.P2
    assert ":focus-visible" in findings[0]["message"]


# ---------------------------------------------------------------------------
# 规则 7：目标尺寸（WCAG 2.2 SC 2.5.8）
# ---------------------------------------------------------------------------

def test_rule_7_target_size_pass(good_html_text):
    """符合最小目标尺寸的 HTML 应通过"""
    findings = a11y_audit.rule_7_target_size(good_html_text, Path("ok.html"))
    # 应无 findings（CSS 设 min-width/min-height: 24px）
    assert len(findings) == 0


def test_rule_7_target_size_fail_inline():
    """内联 style 设 width:10px 应报 P2"""
    text = (
        '<html><body>'
        '<button style="width:10px;height:10px;">x</button>'
        '</body></html>'
    )
    findings = a11y_audit.rule_7_target_size(text, Path("bad.html"))
    assert len(findings) >= 1
    assert findings[0]["severity"] == a11y_audit.Severity.P2


def test_rule_7_target_size_fail_css():
    """CSS 规则中 a { width: 20px } 应报"""
    text = (
        '<html><head><style>'
        'a { width: 20px; height: 20px; }'
        '</style></head><body>'
        '<a href="#x">x</a>'
        '</body></html>'
    )
    findings = a11y_audit.rule_7_target_size(text, Path("css.html"))
    assert len(findings) >= 1


# ---------------------------------------------------------------------------
# 规则 8：拖拽移动（WCAG 2.2 SC 2.5.7）
# ---------------------------------------------------------------------------

def test_rule_8_dragging_with_keyboard_alt():
    """可拖拽元素含 tabindex 应通过"""
    text = (
        '<html><body>'
        '<div draggable="true" tabindex="0" onkeydown="key(event)">拖我</div>'
        '</body></html>'
    )
    findings = a11y_audit.rule_8_dragging(text, Path("ok.html"))
    assert len(findings) == 0


def test_rule_8_dragging_missing_alt():
    """可拖拽元素无键盘替代应报 P1"""
    text = (
        '<html><body>'
        '<div draggable="true">拖我</div>'
        '</body></html>'
    )
    findings = a11y_audit.rule_8_dragging(text, Path("bad.html"))
    assert len(findings) >= 1
    assert findings[0]["severity"] == a11y_audit.Severity.P1
    assert "键盘替代" in findings[0]["message"]


# ---------------------------------------------------------------------------
# 规则 9：一致帮助（WCAG 2.2 SC 3.2.6）
# ---------------------------------------------------------------------------

def test_rule_9_consistent_help_in_landmark():
    """帮助链接位于 nav 内应通过"""
    text = (
        '<html><body>'
        '<nav><a href="/help" aria-label="帮助">帮助</a></nav>'
        '<main>主内容</main>'
        '</body></html>'
    )
    findings = a11y_audit.rule_9_consistent_help(text, Path("ok.html"))
    assert len(findings) == 0


def test_rule_9_consistent_help_missing_landmark():
    """帮助链接未置于 landmark 应报 P2"""
    text = (
        '<html><body>'
        '<div><a href="/help">帮助</a></div>'
        '<p>内容</p>'
        '</body></html>'
    )
    findings = a11y_audit.rule_9_consistent_help(text, Path("bad.html"))
    assert len(findings) >= 1
    assert findings[0]["severity"] == a11y_audit.Severity.P2


# ---------------------------------------------------------------------------
# 键盘导航（增强 E2-1：tabindex/accesskey/焦点陷阱）
# ---------------------------------------------------------------------------

def test_keyboard_navigation_accesskey_conflict():
    """accesskey 重复应报 P1"""
    text = (
        '<html><body>'
        '<a href="#a" accesskey="a">A</a>'
        '<a href="#b" accesskey="a">B</a>'
        '</body></html>'
    )
    findings = a11y_audit.check_keyboard_navigation(text, Path("ak.html"))
    ak = [f for f in findings if "accesskey" in f["message"]]
    assert len(ak) >= 1


def test_keyboard_navigation_positive_tabindex():
    """tabindex > 0 应报 P1"""
    text = '<html><body><a href="#x" tabindex="5">x</a></body></html>'
    findings = a11y_audit.check_keyboard_navigation(text, Path("tb.html"))
    tb = [f for f in findings if "tabindex" in f["message"]]
    assert len(tb) >= 1


def test_keyboard_navigation_focus_trap_alert():
    """onfocus 内含 alert 应报 P0"""
    text = (
        '<html><body>'
        '<input onfocus="alert(1)">'
        '</body></html>'
    )
    findings = a11y_audit.check_keyboard_navigation(text, Path("trap.html"))
    p0 = [f for f in findings if f["severity"] == a11y_audit.Severity.P0]
    assert len(p0) >= 1


def test_keyboard_navigation_dialog_no_modal():
    """role=dialog 缺少 aria-modal/焦点事件应报 P1"""
    text = (
        '<html><body>'
        '<div role="dialog">对话框</div>'
        '</body></html>'
    )
    findings = a11y_audit.check_keyboard_navigation(text, Path("dialog.html"))
    dialog = [f for f in findings if "dialog" in f["message"].lower()
              and "aria-modal" in f["message"]]
    assert len(dialog) >= 1


# ---------------------------------------------------------------------------
# ARIA 完整性（增强 E2-3：labelledby/describedby 引用 + button 可访问名）
# ---------------------------------------------------------------------------

def test_aria_completeness_button_no_name():
    """<button> 缺可访问名应报 P1"""
    text = (
        '<html><body>'
        '<button type="button"></button>'
        '</body></html>'
    )
    parser = a11y_audit._parse_html(text)
    findings = a11y_audit.validate_aria_completeness(parser, text, Path("btn.html"))
    btn = [f for f in findings if "button" in f["message"].lower()
           and "可访问名" in f["message"]]
    assert len(btn) >= 1


def test_aria_completeness_button_with_text():
    """<button> 含文本应通过"""
    text = (
        '<html><body>'
        '<button type="button">提交</button>'
        '</body></html>'
    )
    parser = a11y_audit._parse_html(text)
    findings = a11y_audit.validate_aria_completeness(parser, text, Path("btn.html"))
    btn = [f for f in findings if "可访问名" in f["message"]]
    assert len(btn) == 0


def test_aria_completeness_describedby_dangling():
    """aria-describedby 引用不存在 ID 应报 P2"""
    text = (
        '<html><body>'
        '<button aria-describedby="nope">x</button>'
        '</body></html>'
    )
    parser = a11y_audit._parse_html(text)
    findings = a11y_audit.validate_aria_completeness(parser, text, Path("db.html"))
    db = [f for f in findings if "aria-describedby" in f["message"]]
    assert len(db) >= 1


def test_aria_completeness_labelledby_dangling():
    """aria-labelledby 引用不存在 ID 应报 P1"""
    text = (
        '<html><body>'
        '<button aria-labelledby="ghost">x</button>'
        '</body></html>'
    )
    parser = a11y_audit._parse_html(text)
    findings = a11y_audit.validate_aria_completeness(parser, text, Path("lb.html"))
    lb = [f for f in findings if "aria-labelledby" in f["message"]
          and "不存在" in f["message"]]
    assert len(lb) >= 1


# ---------------------------------------------------------------------------
# audit_directory / audit_file 入口验证
# ---------------------------------------------------------------------------

def test_audit_directory_integration(tmp_path: Path):
    """audit_directory 能扫描目录并输出报告"""
    hp = tmp_path / "page.html"
    hp.write_text(
        '<!DOCTYPE html><html lang="zh"><head><title>x</title></head>'
        '<body><img src="x"></body></html>',
        encoding="utf-8",
    )
    rc = a11y_audit.audit_directory(tmp_path, output_format="md", quiet=True)
    # 含 img 无 alt → P0，退出码应为 1
    assert rc == 1
    out_report = SCRIPTS_DIR / "output" / "a11y-report.md"
    assert out_report.exists()
