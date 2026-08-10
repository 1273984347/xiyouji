#!/usr/bin/env python3
"""a11y_audit.py - 全站可访问性审查脚本
W264-E2 a11y 深化·9 条 WCAG 2.2 AA 规则（v2.2.47）
W271-E2 a11y 深化·7 项深化规则（v2.2.48）
W275-E2 a11y 深化·5 项深化规则（v2.2.49）
W279-E2 a11y 深化·5 项表单与状态消息规则（v2.2.50）
W283-E2 a11y 深化·4 项持续可用与解析规则（v2.2.51）
W316-E2 a11y 深化·10 项 WCAG 2.2 完整规范扩展规则（v2.2.68）
W263-E1 CI/CD 深化配套：9 矩阵 × 3 OS 跨平台验证

扫描 site/ 下所有 HTML 文件，按 40 条规则审查可访问性问题：
  E2-1 键盘导航规则（tabindex/focus 陷阱/accesskey 冲突 + Tab 顺序 + 焦点陷阱）
  E2-2 色彩对比度规则（WCAG 2.2 AA：正常文本 4.5:1，大文本 3:1）
  E2-3 ARIA 标签规则（role 完整性/aria 互斥/aria-hidden 冲突 + ARIA 引用完整性）
  E2-4 焦点指示规则（outline:none 无替代/交互元素无 :focus）
  E2-5 屏幕阅读器规则（img alt/input label/th scope/noscript）
  E2-6 焦点可见规则（:focus-visible 样式存在性，WCAG 2.2 SC 2.4.13）
  E2-7 目标尺寸规则（按钮/链接最小 24×24px，WCAG 2.2 SC 2.5.8）
  E2-8 拖拽移动规则（可拖拽元素需有键盘替代，WCAG 2.2 SC 2.5.7）
  E2-9 一致帮助规则（帮助机制位置一致，WCAG 2.2 SC 3.2.6）
  E2-10 ARIA live regions 验证规则（W271 深化）
  E2-11 tabindex 顺序规则（W271 深化）
  E2-12 焦点陷阱规则（W271 深化）
  E2-13 屏幕阅读器专用文本规则（W271 深化）
  E2-14 跳过链接规则（W271 深化）
  E2-15 标题层级规则（W271 深化）
  E2-16 landmark 完整性规则（W271 深化）
  E2-17 键盘焦点 DOM 顺序规则（W275 深化·原生元素冗余 tabindex=0）
  E2-18 滚动陷阱检测规则（W275 深化·onscroll 重置 + overflow:hidden）
  E2-19 颜色单一信息载体规则（W275 深化·状态类名需配文本/icon）
  E2-20 文字间距可调规则（W275 深化·!important 锁死 + nowrap 阻止重排）
  E2-21 内容重排焦点保持规则（W275 深化·viewport 禁用缩放 + 固定宽度）
  E2-22 表单错误识别规则（W279 深化·错误提示需文本呈现，WCAG 3.3.1）
  E2-23 表单标签或指令规则（W279 深化·表单控件需关联 label，WCAG 3.3.2）
  E2-24 表单错误建议规则（W279 深化·错误提示需提供修正建议，WCAG 3.3.3）
  E2-25 状态消息角色规则（W279 深化·动态消息需 role=status/alert，WCAG 4.1.3）
  E2-26 目标尺寸最小增强规则（W279 深化·紧凑元素需 min-size 兜底，WCAG 2.5.8 增强版）
  E2-27 持续可用规则（W283 深化·自动播放/滚动/动画需可暂停，Pause, Stop, Hide，WCAG 2.2.2）
  E2-28 无闪烁规则（W283 深化·页面不含超过 3 次/秒闪烁，Three Flashes or Below Threshold，WCAG 2.3.1）
  E2-29 可编程确定规则（W283 深化·HTML 无严重解析错误，Parsing，WCAG 4.1.1）
  E2-30 不变功能规则（W283 深化·一致导航元素在多页面中保持相同顺序，Consistent Navigation，WCAG 3.2.3）
  E2-31 页面语言规则（W316 深化·<html lang> 存在且有效，Language of Page，WCAG 3.1.1）
  E2-32 链接目的规则（W316 深化·链接文本非模糊，Link Purpose，WCAG 2.4.4/2.4.9）
  E2-33 多种导航方式规则（W316 深化·至少 2 种导航方式，Multiple Ways，WCAG 2.4.5）
  E2-34 非文本对比度规则（W316 深化·UI 组件边框/图标对比度 ≥ 3:1，Non-text Contrast，WCAG 1.4.11）
  E2-35 悬停或聚焦内容规则（W316 深化·tooltip 可关闭/可悬停/持续，Content on Hover or Focus，WCAG 1.4.13）
  E2-36 字符快捷键规则（W316 深化·单字符快捷键可关闭/重映射/仅聚焦，Character Key Shortcuts，WCAG 2.1.4）
  E2-37 指针手势规则（W316 深化·多点/路径手势有单点替代，Pointer Gestures，WCAG 2.5.1）
  E2-38 指针取消规则（W316 深化·onmousedown 即时触发需有 onmouseup 替代，Pointer Cancellation，WCAG 2.5.2）
  E2-39 名称中的标签规则（W316 深化·可见标签文本包含在可访问名中，Label in Name，WCAG 2.5.3）
  E2-40 交互动画规则（W316 深化·非必要动画支持 prefers-reduced-motion，Animation from Interactions，WCAG 2.3.3）

用法：
    py scripts/a11y_audit.py --dir site --quiet
    py scripts/a11y_audit.py --dir site/data --format json
    py scripts/a11y_audit.py --dir site            # 默认输出 markdown 报告

退出码：0 if P0=0, 1 if P0>0
默认 markdown 报告写入 scripts/output/a11y-report.md
仅依赖 stdlib：argparse/re/json/pathlib/html.parser/datetime
"""
import argparse
import json
import re
import sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path


# ---------- 严重度等级 ----------
class Severity:
    P0 = "P0"  # 阻断级：完全无法访问
    P1 = "P1"  # 严重：部分访问障碍
    P2 = "P2"  # 一般：建议修复
    P3 = "P3"  # 提示：优化项


# ---------- 规则 ID ----------
R_KEYBOARD = "E2-1"
R_CONTRAST = "E2-2"
R_ARIA = "E2-3"
R_FOCUS = "E2-4"
R_SCREEN_READER = "E2-5"
R_FOCUS_VISIBLE = "E2-6"
R_TARGET_SIZE = "E2-7"
R_DRAGGING = "E2-8"
R_CONSISTENT_HELP = "E2-9"
# W271 E 方向深化：7 项 a11y 深化规则（ARIA live + tabindex + 焦点陷阱 + sr-only + 跳过链接 + 标题层级 + landmark）
R_ARIA_LIVE = "E2-10"
R_TABINDEX = "E2-11"
R_FOCUS_TRAP = "E2-12"
R_SR_ONLY = "E2-13"
R_SKIP_LINK = "E2-14"
R_HEADING_HIERARCHY = "E2-15"
R_LANDMARK = "E2-16"
# W275 E 方向深化：5 项 a11y 深化规则（DOM 顺序 + 滚动陷阱 + 颜色单一载体 + 文字间距 + 内容重排）
R_KEYBOARD_FOCUS_ORDER = "E2-17"
R_SCROLL_TRAP = "E2-18"
R_COLOR_ONLY_INFO = "E2-19"
R_TEXT_SPACING = "E2-20"
R_REFLOW_FOCUS = "E2-21"
# W279 E 方向深化：5 项表单与状态消息 a11y 规则（错误识别 + 标签指令 + 错误建议 + 状态消息 + 目标尺寸增强）
R_ERROR_IDENTIFICATION = "E2-22"
R_LABELS_OR_INSTRUCTIONS = "E2-23"
R_ERROR_SUGGESTION = "E2-24"
R_STATUS_MESSAGES = "E2-25"
R_TARGET_SIZE_ENHANCED = "E2-26"
# W283 E 方向深化：4 项持续可用与解析规则（暂停/停止/隐藏 + 无闪烁 + 解析 + 一致导航）
R_PAUSE_STOP_HIDE = "E2-27"
R_NO_THREE_FLASHES = "E2-28"
R_PARSING = "E2-29"
R_CONSISTENT_NAVIGATION = "E2-30"
# W316 E 方向深化：10 项 WCAG 2.2 完整规范扩展规则（页面语言/链接目的/多种导航/非文本对比/悬停聚焦/字符快捷键/指针手势/指针取消/名称标签/交互动画）
R_LANGUAGE_OF_PAGE = "E2-31"
R_LINK_PURPOSE = "E2-32"
R_MULTIPLE_WAYS = "E2-33"
R_NON_TEXT_CONTRAST = "E2-34"
R_HOVER_FOCUS_CONTENT = "E2-35"
R_CHAR_KEY_SHORTCUTS = "E2-36"
R_POINTER_GESTURES = "E2-37"
R_POINTER_CANCELLATION = "E2-38"
R_LABEL_IN_NAME = "E2-39"
R_ANIMATION_INTERACTIONS = "E2-40"

RULE_NAMES = {
    R_KEYBOARD: "键盘导航规则",
    R_CONTRAST: "色彩对比度规则",
    R_ARIA: "ARIA 标签规则",
    R_FOCUS: "焦点指示规则",
    R_SCREEN_READER: "屏幕阅读器规则",
    R_FOCUS_VISIBLE: "焦点可见规则",
    R_TARGET_SIZE: "目标尺寸规则",
    R_DRAGGING: "拖拽移动规则",
    R_CONSISTENT_HELP: "一致帮助规则",
    R_ARIA_LIVE: "ARIA live regions 验证规则",
    R_TABINDEX: "tabindex 顺序规则",
    R_FOCUS_TRAP: "焦点陷阱规则",
    R_SR_ONLY: "屏幕阅读器专用文本规则",
    R_SKIP_LINK: "跳过链接规则",
    R_HEADING_HIERARCHY: "标题层级规则",
    R_LANDMARK: "landmark 完整性规则",
    R_KEYBOARD_FOCUS_ORDER: "键盘焦点 DOM 顺序规则",
    R_SCROLL_TRAP: "滚动陷阱检测规则",
    R_COLOR_ONLY_INFO: "颜色单一信息载体规则",
    R_TEXT_SPACING: "文字间距可调规则",
    R_REFLOW_FOCUS: "内容重排焦点保持规则",
    R_ERROR_IDENTIFICATION: "表单错误识别规则",
    R_LABELS_OR_INSTRUCTIONS: "表单标签或指令规则",
    R_ERROR_SUGGESTION: "表单错误建议规则",
    R_STATUS_MESSAGES: "状态消息角色规则",
    R_TARGET_SIZE_ENHANCED: "目标尺寸最小增强规则",
    R_PAUSE_STOP_HIDE: "持续可用规则",
    R_NO_THREE_FLASHES: "无闪烁规则",
    R_PARSING: "可编程确定规则",
    R_CONSISTENT_NAVIGATION: "不变功能规则",
    R_LANGUAGE_OF_PAGE: "页面语言规则",
    R_LINK_PURPOSE: "链接目的规则",
    R_MULTIPLE_WAYS: "多种导航方式规则",
    R_NON_TEXT_CONTRAST: "非文本对比度规则",
    R_HOVER_FOCUS_CONTENT: "悬停或聚焦内容规则",
    R_CHAR_KEY_SHORTCUTS: "字符快捷键规则",
    R_POINTER_GESTURES: "指针手势规则",
    R_POINTER_CANCELLATION: "指针取消规则",
    R_LABEL_IN_NAME: "名称中的标签规则",
    R_ANIMATION_INTERACTIONS: "交互动画规则",
}


# ---------- HTML 解析器 ----------
class A11yElement:
    """单个 HTML 元素记录"""

    def __init__(self, tag, attrs, line):
        self.tag = tag.lower()
        self.attrs = {k.lower(): (v if v is not None else "") for k, v in attrs}
        self.line = line
        self.text = ""


class A11yHTMLParser(HTMLParser):
    """收集元素、<style> 块、button/a 内文本"""

    # 需要收集可见文本的标签（用于规则 E2-32 链接目的 / E2-39 名称中的标签等）
    _TEXT_COLLECT_TAGS = ("button", "a")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.style_blocks = []  # list[(start_line, css_text)]
        self._in_style = False
        self._style_buf = []
        self._style_start = 0
        self._text_stack = []  # 收集 button/a 文本的元素索引栈

    def handle_starttag(self, tag, attrs):
        line, _ = self.getpos()
        self.elements.append(A11yElement(tag, attrs, line))
        if tag.lower() == "style":
            self._in_style = True
            self._style_buf = []
            self._style_start = line
        if tag.lower() in self._TEXT_COLLECT_TAGS:
            self._text_stack.append(len(self.elements) - 1)

    def handle_startendtag(self, tag, attrs):
        # 自闭合标签（如 <img/>）
        line, _ = self.getpos()
        self.elements.append(A11yElement(tag, attrs, line))

    def handle_endtag(self, tag):
        if tag.lower() == "style" and self._in_style:
            self.style_blocks.append((self._style_start, "".join(self._style_buf)))
            self._in_style = False
            self._style_buf = []
        if tag.lower() in self._TEXT_COLLECT_TAGS and self._text_stack:
            self._text_stack.pop()

    def handle_data(self, data):
        if self._in_style:
            self._style_buf.append(data)
        if self._text_stack:
            self.elements[self._text_stack[-1]].text += data.strip()


def _parse_html(html_text):
    parser = A11yHTMLParser()
    try:
        parser.feed(html_text)
        parser.close()
    except Exception:
        pass
    return parser


def _snippet(html_text, line_num):
    if line_num <= 0:
        return ""
    lines = html_text.split("\n")
    if 0 < line_num <= len(lines):
        return lines[line_num - 1].strip()[:140]
    return ""


def _finding(file_path, line, rule_id, severity, message, evidence):
    return {
        "file": str(file_path),
        "line": int(line),
        "rule_id": rule_id,
        "rule_name": RULE_NAMES.get(rule_id, ""),
        "severity": severity,
        "message": message,
        "evidence": evidence,
    }


# ---------- CSS 工具 ----------
def _extract_css_rules(css_text):
    """从 CSS 文本提取 [(selector, decls)]，跳过 @-规则与注释"""
    css = re.sub(r"/\*.*?\*/", "", css_text, flags=re.DOTALL)
    rules = []
    pos = 0
    while True:
        bo = css.find("{", pos)
        if bo == -1:
            break
        bc = css.find("}", bo)
        if bc == -1:
            break
        selector = css[pos:bo].strip()
        decls = css[bo + 1:bc]
        if selector and "@" not in selector:
            rules.append((selector, decls))
        pos = bc + 1
    return rules


def _extract_css_size(style_text, prop):
    """从 CSS 文本提取指定属性的像素值，返回 int 或 None。
    使用负向后顾避免 width 匹配 min-width/max-width。"""
    pattern = rf"(?<![\w-]){re.escape(prop)}\s*:\s*(\d+(?:\.\d+)?)\s*px"
    m = re.search(pattern, style_text, re.I)
    if m:
        return int(float(m.group(1)))
    return None


_HEX_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
_RGB_RE = re.compile(r"^rgba?\(\s*([0-9.]+)[,\s]+([0-9.]+)[,\s]+([0-9.]+)")


def _parse_color(text):
    """解析 #hex 或 rgb()，返回 (r,g,b) 或 None"""
    if not text:
        return None
    t = text.strip().lower()
    m = _HEX_RE.match(t)
    if m:
        h = m.group(1)
        if len(h) == 3:
            return tuple(int(c * 2, 16) for c in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = _RGB_RE.match(t)
    if m:
        return tuple(float(m.group(i)) for i in (1, 2, 3))
    return None


def _relative_luminance(rgb):
    """WCAG 相对亮度：sRGB → linear → 0.2126 R + 0.7152 G + 0.0722 B"""

    def chan(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def _contrast_ratio(rgb1, rgb2):
    L1, L2 = _relative_luminance(rgb1), _relative_luminance(rgb2)
    if L1 < L2:
        L1, L2 = L2, L1
    return (L1 + 0.05) / (L2 + 0.05)


# ---------- 增强审计函数 ----------
def audit_keyboard_navigation(parser, html_content, file_path):
    """键盘导航审计：Tab 顺序 + 焦点陷阱检测（增强 E2-1）"""
    findings = []

    # 焦点陷阱：role=dialog/alertdialog 缺少焦点管理
    for el in parser.elements:
        role = el.attrs.get("role", "").strip().lower()
        if role in ("dialog", "alertdialog"):
            has_aria_modal = "aria-modal" in el.attrs
            has_focus_handler = any(
                h in el.attrs for h in ("onfocus", "onblur", "onkeydown")
            )
            if not has_aria_modal and not has_focus_handler:
                findings.append(_finding(
                    file_path, el.line, R_KEYBOARD, Severity.P1,
                    f'role="{role}" 对话框缺少 aria-modal 或焦点管理事件，可能形成焦点陷阱',
                    _snippet(html_content, el.line),
                ))

    # Tab 顺序：多个正 tabindex 破坏 DOM 顺序
    positive_tabindex = []
    for el in parser.elements:
        tb = el.attrs.get("tabindex", "").strip()
        if tb.lstrip("-").isdigit() and int(tb) > 0:
            positive_tabindex.append((el.line, int(tb)))

    if len(positive_tabindex) > 1:
        lines_str = ", ".join(str(t[0]) for t in positive_tabindex)
        findings.append(_finding(
            file_path, positive_tabindex[0][0], R_KEYBOARD, Severity.P2,
            f"页面含 {len(positive_tabindex)} 个正 tabindex（行 {lines_str}），"
            f"Tab 顺序由数值决定而非 DOM 顺序，可能造成导航混乱",
            _snippet(html_content, positive_tabindex[0][0]),
        ))

    return findings


def validate_aria_completeness(parser, html_content, file_path):
    """ARIA 标签验证：aria-label/aria-labelledby/aria-describedby 完整性（增强 E2-3）"""
    findings = []

    # 收集所有元素 ID 用于引用验证
    all_ids = set()
    for el in parser.elements:
        eid = el.attrs.get("id", "").strip()
        if eid:
            all_ids.add(eid)

    for el in parser.elements:
        attrs = el.attrs
        tag = el.tag

        # aria-labelledby 引用验证
        if "aria-labelledby" in attrs:
            ref_ids = attrs["aria-labelledby"].split()
            if not ref_ids or (len(ref_ids) == 1 and not ref_ids[0]):
                findings.append(_finding(
                    file_path, el.line, R_ARIA, Severity.P1,
                    "aria-labelledby 值为空，未引用任何元素 ID",
                    _snippet(html_content, el.line),
                ))
            else:
                missing = [rid for rid in ref_ids if rid not in all_ids]
                if missing:
                    findings.append(_finding(
                        file_path, el.line, R_ARIA, Severity.P1,
                        f"aria-labelledby 引用的 ID {missing} 在页面中不存在",
                        _snippet(html_content, el.line),
                    ))

        # aria-describedby 引用验证
        if "aria-describedby" in attrs:
            ref_ids = attrs["aria-describedby"].split()
            if ref_ids and not (len(ref_ids) == 1 and not ref_ids[0]):
                missing = [rid for rid in ref_ids if rid not in all_ids]
                if missing:
                    findings.append(_finding(
                        file_path, el.line, R_ARIA, Severity.P2,
                        f"aria-describedby 引用的 ID {missing} 在页面中不存在",
                        _snippet(html_content, el.line),
                    ))

        # <button> 缺少可访问名（文本/aria-label/aria-labelledby/title）
        if tag == "button":
            has_label = any(k in attrs for k in ("aria-label", "aria-labelledby"))
            has_text = bool(el.text and el.text.strip())
            has_title = bool(attrs.get("title", "").strip())
            if not (has_label or has_text or has_title):
                findings.append(_finding(
                    file_path, el.line, R_ARIA, Severity.P1,
                    "<button> 缺少可访问名（aria-label/aria-labelledby/文本内容/title）",
                    _snippet(html_content, el.line),
                ))

    return findings


# ---------- 规则 1：键盘导航 ----------
def check_keyboard_navigation(html_content, file_path):
    """E2-1：tabindex>0、focus 陷阱、accesskey 冲突 + Tab 顺序 + 焦点陷阱"""
    findings = []
    parser = _parse_html(html_content)

    # accesskey 冲突
    accesskey_map = {}
    for el in parser.elements:
        ak = el.attrs.get("accesskey", "").strip().lower()
        if ak:
            accesskey_map.setdefault(ak, []).append(el.line)
    for ak, lines in accesskey_map.items():
        if len(lines) > 1:
            findings.append(_finding(
                file_path, lines[0], R_KEYBOARD, Severity.P1,
                f"accesskey={ak!r} 出现在多行 {lines}，可能造成快捷键冲突",
                _snippet(html_content, lines[0]),
            ))

    for el in parser.elements:
        attrs = el.attrs
        # tabindex > 0
        tb = attrs.get("tabindex", "").strip()
        if tb:
            try:
                tbv = int(tb)
                if tbv > 0:
                    findings.append(_finding(
                        file_path, el.line, R_KEYBOARD, Severity.P1,
                        f"tabindex={tbv} > 0 破坏 DOM 顺序，应改用 0 或 -1",
                        _snippet(html_content, el.line),
                    ))
            except ValueError:
                pass

        # 焦点陷阱：onfocus/onblur 内含 alert/confirm/prompt
        for handler in ("onfocus", "onblur"):
            if handler in attrs:
                code = attrs[handler]
                if re.search(r"\b(alert|confirm|prompt)\s*\(", code):
                    findings.append(_finding(
                        file_path, el.line, R_KEYBOARD, Severity.P0,
                        f"{handler} 内含 alert/confirm/prompt，可能形成焦点陷阱",
                        _snippet(html_content, el.line),
                    ))

    # 增强审计：Tab 顺序 + 焦点陷阱检测
    findings.extend(audit_keyboard_navigation(parser, html_content, file_path))

    return findings


# ---------- 规则 2：色彩对比度 ----------
def check_color_contrast(html_content, file_path):
    """E2-2：解析 CSS color/background-color 计算对比度"""
    findings = []
    parser = _parse_html(html_content)

    # 收集 CSS：style 块 + 内联 style
    css_blocks = [css for _, css in parser.style_blocks]
    for el in parser.elements:
        if "style" in el.attrs and el.attrs["style"]:
            css_blocks.append(el.attrs["style"])

    for css in css_blocks:
        for selector, decls in _extract_css_rules(css):
            color_val = None
            bg_val = None
            for decl in decls.split(";"):
                if ":" not in decl:
                    continue
                k, _, v = decl.partition(":")
                k = k.strip().lower()
                v = v.strip()
                if k == "color":
                    color_val = v
                elif k in ("background", "background-color"):
                    bg_val = v
            # 仅当 color 与 bg 都是直接颜色值（非 var/gradient）才检测
            if not color_val or not bg_val:
                continue
            if "var(" in color_val or "var(" in bg_val:
                continue
            if "gradient" in bg_val or "gradient" in color_val:
                continue
            color_rgb = _parse_color(color_val)
            bg_rgb = _parse_color(bg_val)
            if not color_rgb or not bg_rgb:
                continue
            ratio = _contrast_ratio(color_rgb, bg_rgb)
            # 启发式判断大文本：选择器含 h1/h2/h3/hero/title/headline
            is_large = bool(re.search(r"\b(h1|h2|h3|hero|title|headline)\b", selector, re.I))
            threshold = 3.0 if is_large else 4.5
            if ratio < threshold:
                sev = Severity.P1 if ratio < 3.0 else Severity.P2
                findings.append(_finding(
                    file_path, 0, R_CONTRAST, sev,
                    f"选择器 {selector!r} 的 color={color_val} vs background={bg_val} "
                    f"对比度 {ratio:.2f}:1 低于 WCAG AA 阈值 {threshold}:1"
                    f"（{'大文本' if is_large else '正常文本'}）",
                    f"color:{color_val}; background:{bg_val}; ratio={ratio:.2f}",
                ))

    return findings


# ---------- 规则 3：ARIA 标签 ----------
def check_aria_labels(html_content, file_path):
    """E2-3：role 完整性、aria 互斥、aria-hidden 冲突、role=img/button 检查 + ARIA 引用完整性"""
    findings = []
    parser = _parse_html(html_content)

    for el in parser.elements:
        attrs = el.attrs
        tag = el.tag
        role = attrs.get("role", "").strip().lower()

        # aria-label 与 aria-labelledby 互斥
        if "aria-label" in attrs and "aria-labelledby" in attrs:
            findings.append(_finding(
                file_path, el.line, R_ARIA, Severity.P2,
                "aria-label 与 aria-labelledby 同时存在，屏幕阅读器可能歧义（应二选一）",
                _snippet(html_content, el.line),
            ))

        # aria-hidden=true 与 focusable 冲突
        if attrs.get("aria-hidden") == "true":
            tb = attrs.get("tabindex", "").strip()
            tb_focusable = False
            if tb.lstrip("-").isdigit():
                tb_focusable = int(tb) >= 0
            if tb_focusable:
                findings.append(_finding(
                    file_path, el.line, R_ARIA, Severity.P0,
                    'aria-hidden="true" 与 tabindex>=0 共存：对 SR 隐藏但仍可键盘聚焦',
                    _snippet(html_content, el.line),
                ))
            if tag == "a" and "href" in attrs:
                findings.append(_finding(
                    file_path, el.line, R_ARIA, Severity.P0,
                    '<a href> 含 aria-hidden="true"：键盘可聚焦但被 SR 忽略',
                    _snippet(html_content, el.line),
                ))

        # role="img" 缺少可访问名
        if role == "img":
            if not any(k in attrs for k in ("alt", "aria-label", "aria-labelledby", "title")):
                findings.append(_finding(
                    file_path, el.line, R_ARIA, Severity.P1,
                    'role="img" 元素缺少 alt/aria-label/aria-labelledby/title',
                    _snippet(html_content, el.line),
                ))

        # role="button" 在 a/div/span 上缺少键盘事件
        if role == "button" and tag in ("a", "div", "span"):
            has_click = "onclick" in attrs
            has_key = any(k in attrs for k in ("onkeydown", "onkeyup", "onkeypress"))
            if has_click and not has_key:
                findings.append(_finding(
                    file_path, el.line, R_ARIA, Severity.P1,
                    f'<{tag} role="button"> 含 onclick 但缺 onkeydown 等键盘事件处理',
                    _snippet(html_content, el.line),
                ))

    # 增强审计：ARIA 标签引用完整性验证
    findings.extend(validate_aria_completeness(parser, html_content, file_path))

    return findings


# ---------- 规则 4：焦点指示 ----------
def check_focus_indicator(html_content, file_path):
    """E2-4：outline:none 无替代、交互元素无 :focus 样式"""
    findings = []
    parser = _parse_html(html_content)

    css_text = "\n".join(css for _, css in parser.style_blocks)
    if not css_text.strip():
        return findings

    has_any_focus_visible = bool(re.search(r":\s*focus-visible", css_text))
    has_any_focus = bool(re.search(r":\s*focus(?:-visible)?\s*[{,]", css_text))

    # outline:none in :focus context without replacement
    for selector, decls in _extract_css_rules(css_text):
        if "outline" not in decls:
            continue
        is_focus_ctx = bool(re.search(r":\s*focus", selector))
        if not is_focus_ctx:
            continue
        outline_none = bool(re.search(r"outline\s*:\s*(none|0(\s|;|$))", decls, re.I))
        if not outline_none:
            continue
        # 同块内是否有替代指示器
        has_box_shadow = "box-shadow" in decls
        has_border_change = "border-color" in decls or bool(
            re.search(r"border\s*:\s*(?!none|0\b)", decls)
        )
        has_bg_change = "background" in decls
        if has_box_shadow or has_border_change or has_bg_change:
            continue
        # 若页面其他位置存在 :focus-visible 规则，假设提供替代
        if has_any_focus_visible:
            continue
        findings.append(_finding(
            file_path, 0, R_FOCUS, Severity.P1,
            f"选择器 {selector!r} 设 outline:none 但未见 :focus-visible 替代样式",
            f"{selector} {{ outline: none; ... }}",
        ))

    # 全局无任何 :focus/:focus-visible 样式时，提示首个交互元素
    if not has_any_focus and not has_any_focus_visible:
        for el in parser.elements:
            if el.tag in ("a", "button", "input", "select", "textarea"):
                findings.append(_finding(
                    file_path, el.line, R_FOCUS, Severity.P2,
                    f"页面 CSS 未发现 :focus/:focus-visible 全局样式，<{el.tag}> 可能无焦点指示",
                    _snippet(html_content, el.line),
                ))
                break

    return findings


# ---------- 规则 5：屏幕阅读器 ----------
def check_screen_reader(html_content, file_path):
    """E2-5：img alt、input label、th scope、noscript 完整性"""
    findings = []
    parser = _parse_html(html_content)

    script_count = sum(1 for el in parser.elements if el.tag == "script")
    has_noscript = any(el.tag == "noscript" for el in parser.elements)

    for el in parser.elements:
        attrs = el.attrs
        tag = el.tag

        # <img> 缺少 alt
        if tag == "img":
            if "alt" not in attrs:
                src = attrs.get("src", "?")
                findings.append(_finding(
                    file_path, el.line, R_SCREEN_READER, Severity.P0,
                    f"<img src={src!r}> 缺少 alt 属性，屏幕阅读器无法识别",
                    _snippet(html_content, el.line),
                ))
            elif attrs["alt"].strip() == "":
                if attrs.get("role") != "presentation":
                    findings.append(_finding(
                        file_path, el.line, R_SCREEN_READER, Severity.P3,
                        '<img alt=""> 空白 alt 建议显式 role="presentation" 标记装饰性',
                        _snippet(html_content, el.line),
                    ))
            elif attrs.get("role") == "presentation" and attrs.get("alt", "") != "":
                findings.append(_finding(
                    file_path, el.line, R_SCREEN_READER, Severity.P3,
                    '<img role="presentation"> 应配 alt="" 显式空 alt',
                    _snippet(html_content, el.line),
                ))

        # <input> 缺少 label/aria-label/id
        if tag == "input":
            input_type = attrs.get("type", "text").lower()
            if input_type in ("hidden", "submit", "button", "image", "reset"):
                pass
            elif not any(k in attrs for k in ("aria-label", "aria-labelledby", "id")):
                findings.append(_finding(
                    file_path, el.line, R_SCREEN_READER, Severity.P1,
                    f"<input type={input_type!r}> 缺少 aria-label/aria-labelledby/id 无法关联 label",
                    _snippet(html_content, el.line),
                ))

        # <th> 缺少 scope（role="button" 的可排序表头除外）
        if tag == "th" and attrs.get("role") != "button":
            if "scope" not in attrs:
                findings.append(_finding(
                    file_path, el.line, R_SCREEN_READER, Severity.P3,
                    '<th> 缺少 scope 属性（建议 scope="col" 或 scope="row"）',
                    _snippet(html_content, el.line),
                ))

    # noscript 完整性：≥2 个 <script> 但无 <noscript>
    if script_count >= 2 and not has_noscript:
        findings.append(_finding(
            file_path, 0, R_SCREEN_READER, Severity.P2,
            f"页面含 {script_count} 个 <script> 但无 <noscript>，禁用 JS 时无降级提示",
            "",
        ))

    return findings


# ---------- 规则 6：焦点可见（WCAG 2.2 SC 2.4.13） ----------
def rule_6_focus_visible(html_content, file_path):
    """E2-6：验证 HTML/CSS 中 :focus-visible 样式存在"""
    findings = []
    parser = _parse_html(html_content)

    css_text = "\n".join(css for _, css in parser.style_blocks)
    has_focus_visible = bool(re.search(r":focus-visible", css_text))

    if not has_focus_visible:
        interactive_tags = ("a", "button", "input", "select", "textarea", "summary")
        has_interactive = any(el.tag in interactive_tags for el in parser.elements)
        if has_interactive:
            findings.append(_finding(
                file_path, 0, R_FOCUS_VISIBLE, Severity.P2,
                "页面 CSS 未发现 :focus-visible 样式，键盘用户可能无法识别当前焦点元素"
                "（WCAG 2.2 SC 2.4.13）",
                "建议添加 :focus-visible { outline: 2px solid currentColor; } 全局样式",
            ))

    return findings


# ---------- 规则 7：目标尺寸（WCAG 2.2 SC 2.5.8） ----------
def rule_7_target_size(html_content, file_path):
    """E2-7：验证按钮/链接最小 24×24px"""
    findings = []
    parser = _parse_html(html_content)
    MIN_SIZE = 24
    target_tags = ("a", "button", "input", "select", "textarea", "summary")
    target_selector_re = re.compile(
        r"\b(a|button|input|select|textarea|summary|\.btn|\.button|\.link)\b", re.I
    )
    css_text = "\n".join(css for _, css in parser.style_blocks)

    # 检查内联样式
    for el in parser.elements:
        if el.tag not in target_tags:
            continue
        style = el.attrs.get("style", "")
        if not style:
            continue
        for prop in ("width", "height", "min-width", "min-height"):
            size = _extract_css_size(style, prop)
            if size is not None and size < MIN_SIZE:
                findings.append(_finding(
                    file_path, el.line, R_TARGET_SIZE, Severity.P2,
                    f"<{el.tag}> 内联样式 {prop}={size}px 小于 WCAG 2.2 SC 2.5.8 "
                    f"最小目标尺寸 {MIN_SIZE}px",
                    _snippet(html_content, el.line),
                ))

    # 检查 CSS 规则中针对交互元素的选择器
    for selector, decls in _extract_css_rules(css_text):
        if not target_selector_re.search(selector):
            continue
        for prop in ("width", "height", "min-width", "min-height"):
            size = _extract_css_size(decls, prop)
            if size is not None and size < MIN_SIZE:
                findings.append(_finding(
                    file_path, 0, R_TARGET_SIZE, Severity.P2,
                    f"选择器 {selector!r} 设 {prop}={size}px 小于 WCAG 2.2 SC 2.5.8 "
                    f"最小目标尺寸 {MIN_SIZE}px",
                    f"{selector} {{ {prop}: {size}px; }}",
                ))

    return findings


# ---------- 规则 8：拖拽移动（WCAG 2.2 SC 2.5.7） ----------
def rule_8_dragging(html_content, file_path):
    """E2-8：验证可拖拽元素有替代方案"""
    findings = []
    parser = _parse_html(html_content)

    drag_handlers = (
        "ondragstart", "ondrag", "ondragend",
        "ondrop", "ondragover", "ondragenter", "ondragleave",
    )

    for el in parser.elements:
        is_draggable = el.attrs.get("draggable", "").lower() == "true"
        has_drag_handler = any(h in el.attrs for h in drag_handlers)

        if not (is_draggable or has_drag_handler):
            continue

        # 检查是否有键盘替代方案
        has_keyboard_alt = any(
            k in el.attrs for k in ("onkeydown", "onkeyup", "onkeypress")
        )
        has_tabindex = "tabindex" in el.attrs
        has_role = el.attrs.get("role", "").strip().lower() in (
            "button", "slider", "spinbutton", "listbox",
        )
        if not (has_keyboard_alt or has_tabindex or has_role):
            findings.append(_finding(
                file_path, el.line, R_DRAGGING, Severity.P1,
                f"<{el.tag}> 含拖拽操作（draggable/ondrag*）但未提供键盘替代方案"
                f"（WCAG 2.2 SC 2.5.7）",
                _snippet(html_content, el.line),
            ))

    return findings


# ---------- 规则 9：一致帮助（WCAG 2.2 SC 3.2.6） ----------
def rule_9_consistent_help(html_content, file_path):
    """E2-9：验证帮助机制位置一致"""
    findings = []
    parser = _parse_html(html_content)

    help_patterns = re.compile(r"(help|faq|contact|support|帮助|联系|客服|常见问题)", re.I)
    landmark_tags = ("nav", "header", "footer", "main", "aside")

    help_links = []
    for el in parser.elements:
        if el.tag != "a":
            continue
        href = el.attrs.get("href", "")
        aria_label = el.attrs.get("aria-label", "")
        if help_patterns.search(href) or help_patterns.search(aria_label):
            help_links.append(el)

    if help_links:
        has_landmarks = any(el.tag in landmark_tags for el in parser.elements)
        if not has_landmarks:
            for el in help_links:
                findings.append(_finding(
                    file_path, el.line, R_CONSISTENT_HELP, Severity.P2,
                    "帮助链接未置于 landmark 元素（nav/header/footer/main/aside）内，"
                    "可能导致跨页面位置不一致（WCAG 2.2 SC 3.2.6）",
                    _snippet(html_content, el.line),
                ))

    return findings


# ---------- 规则 10：ARIA live regions 验证（W271 E 方向深化） ----------
def rule_10_aria_live(html_content, file_path):
    """验证动态更新内容（带 aria-live 属性）的设置是否正确"""
    findings = []

    # 检测动态更新内容：[aria-live], role="status", role="alert", role="log"
    live_patterns = [
        r'aria-live\s*=\s*["\']?(?:polite|assertive|off)["\']?',
        r'role\s*=\s*["\']?(?:status|alert|log|timer|marquee)["\']?',
    ]
    has_live = any(re.search(p, html_content) for p in live_patterns)

    # 检测动态内容指示：aria-live="polite" 或 role="status" 用于 node-card / phase-detail 类
    has_dynamic_text = bool(re.search(
        r'(?:class\s*=\s*["\'][^"\']*(?:node-card|phase-detail|kpi-|tip|notice|alert|toast|status)[^"\']*["\'])',
        html_content
    ))

    if has_dynamic_text and not has_live:
        findings.append(_finding(
            file_path, 1, R_ARIA_LIVE, Severity.P2,
            "检测到动态更新内容（node-card/phase-detail/tip/notice 类），"
            "但未设置 aria-live 属性或 role=status/alert。"
            "屏幕阅读器用户无法感知动态更新（W271 E2-10 深化）",
            "",
        ))

    # 验证 aria-live="assertive" 是否过度使用（应仅用于紧急通知）
    assertive_count = len(re.findall(r'aria-live\s*=\s*["\']assertive["\']', html_content))
    if assertive_count > 2:
        findings.append(_finding(
            file_path, 1, R_ARIA_LIVE, Severity.P3,
            f"aria-live=assertive 出现 {assertive_count} 次，过度使用会打断屏幕阅读器用户。"
            "建议仅用于紧急通知（W271 E2-10 深化）",
            "",
        ))

    return findings


# ---------- 规则 11：tabindex 顺序规则（W271 E 方向深化） ----------
def rule_11_tabindex(html_content, file_path):
    """验证 tabindex > 0 不被使用（避免破坏自然 tab 顺序）"""
    findings = []

    # 查找所有 tabindex 属性
    tabindex_pattern = re.compile(r'tabindex\s*=\s*["\'](\d+)["\']')
    for match in tabindex_pattern.finditer(html_content):
        value = int(match.group(1))
        if value > 0:
            # 找到行号
            line_num = html_content[:match.start()].count("\n") + 1
            findings.append(_finding(
                file_path, line_num, R_TABINDEX, Severity.P2,
                f"tabindex={value} 大于 0，会破坏自然 tab 顺序。"
                "应使用 tabindex=0（可聚焦）或 tabindex=-1（仅程序聚焦）"
                "（W271 E2-11 深化）",
                _snippet(html_content, line_num),
            ))

    return findings


# ---------- 规则 12：焦点陷阱规则（W271 E 方向深化） ----------
def rule_12_focus_trap(html_content, file_path):
    """验证模态/对话框是否有焦点陷阱机制"""
    findings = []

    # 检测模态/对话框元素
    modal_patterns = [
        r'class\s*=\s*["\'][^"\']*(?:modal|dialog|popup|overlay)[^"\']*["\']',
        r'role\s*=\s*["\']?(?:dialog|alertdialog)["\']?',
        r'aria-modal\s*=\s*["\']?true["\']?',
    ]
    has_modal = any(re.search(p, html_content) for p in modal_patterns)

    if has_modal:
        # 检测焦点陷阱机制：JS 中需有 keydown 监听 Tab/Shift+Tab
        has_trap_js = bool(re.search(
            r'(?:keydown|keyup|keypress).*?(?:Tab|shiftKey)|focusTrap|trapFocus',
            html_content, re.DOTALL
        ))
        if not has_trap_js:
            findings.append(_finding(
                file_path, 1, R_FOCUS_TRAP, Severity.P1,
                "检测到模态/对话框元素，但未找到焦点陷阱机制（keydown Tab/Shift+Tab 监听或 trapFocus 函数）。"
                "键盘用户可能被困或逃出模态（W271 E2-12 深化）",
                "",
            ))

    return findings


# ---------- 规则 13：屏幕阅读器专用文本规则（W271 E 方向深化） ----------
def rule_13_sr_only(html_content, file_path):
    """验证 sr-only / visually-hidden 类用于隐藏屏幕阅读器专用文本"""
    findings = []

    # 检测图标按钮（无文本的按钮/链接）
    icon_button_pattern = re.compile(
        r'<(?:button|a)[^>]*>\s*(?:<i[^>]*>|<svg[^>]*>|<span[^>]*class\s*=\s*["\'][^"\']*(?:icon|fa|material)[^"\']*["\'][^>]*>.*?</span>)\s*</(?:button|a)>',
        re.DOTALL
    )
    for match in icon_button_pattern.finditer(html_content):
        line_num = html_content[:match.start()].count("\n") + 1
        # 检测是否有 aria-label 或 sr-only 文本
        btn_content = match.group(0)
        has_aria_label = bool(re.search(r'aria-label\s*=\s*["\'][^"\']+["\']', btn_content))
        has_sr_only = bool(re.search(r'class\s*=\s*["\'][^"\']*(?:sr-only|visually-hidden|screen-reader-text)[^"\']*["\']', btn_content))
        if not has_aria_label and not has_sr_only:
            findings.append(_finding(
                file_path, line_num, R_SR_ONLY, Severity.P1,
                "图标按钮/链接缺少 aria-label 或 sr-only 文本，"
                "屏幕阅读器用户无法识别用途（W271 E2-13 深化）",
                _snippet(html_content, line_num),
            ))

    return findings


# ---------- 规则 14：跳过链接规则（W271 E 方向深化） ----------
def rule_14_skip_link(html_content, file_path):
    """验证页面是否有跳过链接（skip link）以便键盘用户快速跳到主内容"""
    findings = []

    # 检测 skip link：href="#main" 或 class="skip-link" 或 "跳到主内容"
    skip_patterns = [
        r'<a[^>]*href\s*=\s*["\']#main[^"\']*["\'][^>]*>',
        r'class\s*=\s*["\'][^"\']*skip-link[^"\']*["\']',
        r'>\s*跳到主',
    ]
    has_skip_link = any(re.search(p, html_content) for p in skip_patterns)

    if not has_skip_link:
        findings.append(_finding(
            file_path, 1, R_SKIP_LINK, Severity.P2,
            "页面缺少 skip link（跳过链接），键盘用户需按多次 Tab 才能到达主内容。"
            "建议在 body 起始添加 <a href='#main' class='skip-link'>跳到主内容</a>"
            "（W271 E2-14 深化）",
            "",
        ))
    else:
        # 验证 skip link 指向的 main 元素存在
        has_main = bool(re.search(r'<main\b', html_content))
        if not has_main:
            findings.append(_finding(
                file_path, 1, R_SKIP_LINK, Severity.P1,
                "skip link 存在但 <main> 元素缺失，跳过链接将无法聚焦"
                "（W271 E2-14 深化）",
                "",
            ))

    return findings


# ---------- 规则 15：标题层级规则（W271 E 方向深化） ----------
def rule_15_heading_hierarchy(html_content, file_path):
    """验证标题层级不跳级（h1 → h2 → h3，不应出现 h1 → h3）"""
    findings = []

    # 提取所有标题（h1-h6）按出现顺序
    headings = []
    heading_pattern = re.compile(r'<(h[1-6])\b', re.IGNORECASE)
    for match in heading_pattern.finditer(html_content):
        line_num = html_content[:match.start()].count("\n") + 1
        level = int(match.group(1).lower()[1])
        headings.append((level, line_num))

    if not headings:
        return findings

    # 验证第一个标题是 h1
    if headings[0][0] != 1:
        findings.append(_finding(
            file_path, headings[0][1], R_HEADING_HIERARCHY, Severity.P2,
            f"第一个标题是 h{headings[0][0]} 而非 h1。"
            "页面应只有一个 h1 作为主标题（W271 E2-15 深化）",
            _snippet(html_content, headings[0][1]),
        ))

    # 验证不跳级（h1 → h3 是跳级，h1 → h2 → h3 不是）
    for i in range(1, len(headings)):
        prev_level, _ = headings[i - 1]
        curr_level, curr_line = headings[i]
        if curr_level > prev_level + 1:
            findings.append(_finding(
                file_path, curr_line, R_HEADING_HIERARCHY, Severity.P2,
                f"标题跳级：h{prev_level} → h{curr_level}（应 h{prev_level} → h{prev_level + 1}）。"
                "屏幕阅读器用户依赖标题层级导航（W271 E2-15 深化）",
                _snippet(html_content, curr_line),
            ))

    # 验证 h1 唯一
    h1_count = sum(1 for level, _ in headings if level == 1)
    if h1_count > 1:
        findings.append(_finding(
            file_path, 1, R_HEADING_HIERARCHY, Severity.P3,
            f"页面有 {h1_count} 个 h1，建议每页仅一个 h1 作为主标题"
            "（W271 E2-15 深化）",
            "",
        ))

    return findings


# ---------- 规则 16：landmark 完整性规则（W271 E 方向深化） ----------
def rule_16_landmark(html_content, file_path):
    """验证页面 landmark 完整性（header/main/nav/footer）"""
    findings = []

    landmark_required = {
        "header": "页眉 landmark（<header> 或 role=banner）",
        "main": "主内容 landmark（<main> 或 role=main）",
        "nav": "导航 landmark（<nav> 或 role=navigation）",
        "footer": "页脚 landmark（<footer> 或 role=contentinfo）",
    }

    for tag, desc in landmark_required.items():
        # 检测 HTML5 元素或 ARIA role
        tag_pattern = rf'<{tag}\b'
        role_map = {
            "header": "banner",
            "main": "main",
            "nav": "navigation",
            "footer": "contentinfo",
        }
        role_pattern = rf'role\s*=\s*["\']?{role_map[tag]}["\']?'
        has_landmark = bool(re.search(tag_pattern, html_content, re.IGNORECASE)) or \
                       bool(re.search(role_pattern, html_content, re.IGNORECASE))
        if not has_landmark:
            findings.append(_finding(
                file_path, 1, R_LANDMARK, Severity.P2,
                f"页面缺少 {desc}。landmark 帮助屏幕阅读器用户快速定位页面结构"
                "（W271 E2-16 深化）",
                "",
            ))

    return findings


# ---------- 规则 17：键盘焦点 DOM 顺序规则（W275 E 方向深化） ----------
def rule_17_keyboard_focus_order(html_content, file_path):
    """E2-17：检测交互元素上冗余 tabindex=0，可能误导 DOM 顺序与焦点顺序一致性的预期。
    原生交互元素（a[href]/button/input/select/textarea/summary）天然可聚焦，
    显式 tabindex=0 是冗余且暗示开发者可能误用了 tabindex 机制。"""
    findings = []
    parser = _parse_html(html_content)

    native_focusable = ("a", "button", "input", "select", "textarea", "summary")
    redundant_count = 0
    first_redundant_line = 0
    for el in parser.elements:
        if el.tag not in native_focusable:
            continue
        tb = el.attrs.get("tabindex", "").strip()
        if tb == "0":
            # <a> 需有 href 才天然可聚焦
            if el.tag == "a" and "href" not in el.attrs:
                continue
            redundant_count += 1
            if first_redundant_line == 0:
                first_redundant_line = el.line

    if redundant_count >= 3:
        findings.append(_finding(
            file_path, first_redundant_line, R_KEYBOARD_FOCUS_ORDER, Severity.P3,
            f"页面含 {redundant_count} 个原生交互元素显式设 tabindex=0（冗余）。"
            "原生 a/button/input 等天然可聚焦，显式 tabindex=0 暗示可能误用 tabindex 机制。"
            "应移除冗余 tabindex，依赖 DOM 顺序保证焦点自然（W275 E2-17 深化）",
            _snippet(html_content, first_redundant_line),
        ))

    return findings


# ---------- 规则 18：滚动陷阱检测规则（W275 E 方向深化） ----------
def rule_18_scroll_trap(html_content, file_path):
    """E2-18：检测滚动陷阱：CSS overflow:hidden 锁死内容区 + JS 强制 scrollTop/scrollTo。
    典型模式：modal/overlay 内 overflow:hidden 但无关闭按钮，或 onscroll 事件重置滚动位置。"""
    findings = []
    parser = _parse_html(html_content)

    # 1. 检测 onscroll 事件中强制重置滚动位置（scroll trap JS）
    scroll_reset_patterns = re.compile(
        r'(?:onscroll|addEventListener\s*\(\s*["\']scroll).*?'
        r'(?:scrollTop\s*=\s*0|scrollTo\s*\(\s*0|window\.scrollTo\s*\(\s*0|'
        r'e\.preventDefault\s*\(\s*\)|event\.preventDefault)',
        re.DOTALL
    )
    if scroll_reset_patterns.search(html_content):
        line_num = html_content[:scroll_reset_patterns.search(html_content).start()].count("\n") + 1
        findings.append(_finding(
            file_path, line_num, R_SCROLL_TRAP, Severity.P1,
            "检测到 onscroll/addEventListener('scroll') 中含 scrollTop=0/scrollTo(0)/preventDefault，"
            "可能形成滚动陷阱：用户无法自然滚出该区域（W275 E2-18 深化）",
            _snippet(html_content, line_num),
        ))

    # 2. 检测 body/html overflow:hidden 但无 skip/close 机制（锁死整页滚动）
    css_text = "\n".join(css for _, css in parser.style_blocks)
    body_overflow_locked = False
    for selector, decls in _extract_css_rules(css_text):
        if re.search(r"\b(body|html)\b", selector, re.I):
            if re.search(r"overflow\s*:\s*hidden", decls, re.I):
                body_overflow_locked = True
                break
    if body_overflow_locked:
        # 检测是否有关闭/跳过机制（close 按钮、skip link、Esc 处理）
        has_close_mechanism = bool(re.search(
            r'(?:class\s*=\s*["\'][^"\']*close[^"\']*["\'])|'
            r'(?:aria-label\s*=\s*["\'][^"\']*(?:关闭|close)[^"\']*["\'])|'
            r'(?:onkeydown.*?Escape|key\s*===?\s*["\']Escape["\'])',
            html_content, re.DOTALL | re.IGNORECASE
        ))
        if not has_close_mechanism:
            findings.append(_finding(
                file_path, 1, R_SCROLL_TRAP, Severity.P2,
                "body/html 设 overflow:hidden 锁死整页滚动，但未检测到关闭/跳过机制"
                "（close 按钮、Esc 键处理）。键盘/触屏用户可能无法逃离该状态"
                "（W275 E2-18 深化）",
                "",
            ))

    return findings


# ---------- 规则 19：颜色单一信息载体规则（W275 E 方向深化） ----------
def rule_19_color_only_info(html_content, file_path):
    """E2-19：检测仅用颜色（无文本/icon/aria-label）传达信息的模式。
    WCAG 1.4.1 Use of Color：颜色不应作为唯一的信息载体。
    典型违规：class="error" 但无文本说明、仅靠红色边框提示错误。"""
    findings = []

    # 状态类名通常意味着用颜色区分状态
    state_class_re = re.compile(
        r'class\s*=\s*["\'][^"\']*\b(error|warning|success|danger|invalid|'
        r'required|disabled|active|selected)\b[^"\']*["\']',
        re.IGNORECASE
    )
    state_class_hits = []
    for match in state_class_re.finditer(html_content):
        line_num = html_content[:match.start()].count("\n") + 1
        state_class_hits.append((line_num, match.group(0)))

    # 对每个含状态类名的元素，检查是否有文本/aria-label/icon 辅助
    for line_num, _raw in state_class_hits:
        # 提取该 class 所在标签的整段（粗略：取该行 + 后 2 行）
        lines = html_content.split("\n")
        context = "\n".join(lines[max(0, line_num - 1):min(len(lines), line_num + 2)])
        # 检测是否有辅助信息：aria-label、aria-describedby、title、可见文本（非空 tag 内容）
        has_aria = bool(re.search(r'aria-(?:label|describedby)\s*=\s*["\'][^"\']+["\']', context))
        has_title = bool(re.search(r'\btitle\s*=\s*["\'][^"\']+["\']', context))
        # 检测可见文本（标签后跟非空内容）
        has_text = bool(re.search(r'>\s*[^<\s][^<]*<', context))
        # 检测 icon 元素（<i>/<svg> 含 class icon）
        has_icon = bool(re.search(r'<(?:i|svg)\b[^>]*class\s*=\s*["\'][^"\']*icon[^"\']*', context, re.IGNORECASE))
        if not (has_aria or has_title or has_text or has_icon):
            findings.append(_finding(
                file_path, line_num, R_COLOR_ONLY_INFO, Severity.P2,
                "元素含状态类名（error/warning/success/danger 等）但未检测到"
                "aria-label/title/可见文本/icon 辅助。颜色可能作为唯一信息载体"
                "（WCAG 1.4.1，W275 E2-19 深化）",
                _snippet(html_content, line_num),
            ))

    return findings


# ---------- 规则 20：文字间距可调规则（W275 E 方向深化） ----------
def rule_20_text_spacing(html_content, file_path):
    """E2-20：WCAG 2.1 SC 1.4.12 Text Spacing。
    检测 CSS 是否用 !important 锁死 line-height/letter-spacing/word-spacing/word-spacing，
    或用 white-space:nowrap 阻止文字重排导致溢出。"""
    findings = []
    parser = _parse_html(html_content)
    css_text = "\n".join(css for _, css in parser.style_blocks)

    if not css_text.strip():
        return findings

    # 1. !important 锁死文本间距属性
    spacing_props = ("line-height", "letter-spacing", "word-spacing", "text-indent")
    for selector, decls in _extract_css_rules(css_text):
        for prop in spacing_props:
            pattern = rf"{re.escape(prop)}\s*:\s*[^;]+!\s*important"
            if re.search(pattern, decls, re.IGNORECASE):
                findings.append(_finding(
                    file_path, 0, R_TEXT_SPACING, Severity.P3,
                    f"选择器 {selector!r} 用 !important 锁死 {prop}，"
                    "用户样式表/辅助技术无法覆盖调整文字间距"
                    "（WCAG 2.1 SC 1.4.12，W275 E2-20 深化）",
                    f"{selector} {{ {prop}: ... !important; }}",
                ))
                break  # 每个选择器仅报一次

    # 2. white-space:nowrap 阻止重排（仅在大范围容器上报告）
    nowrap_selectors = []
    for selector, decls in _extract_css_rules(css_text):
        if re.search(r"white-space\s*:\s*nowrap", decls, re.IGNORECASE):
            # 排除按钮/链接等小元素（nav/btn/button/a/td/th）
            if not re.search(r"\b(a|button|nav|td|th|btn|label|chip|tag)\b", selector, re.I):
                nowrap_selectors.append(selector)
    if len(nowrap_selectors) >= 2:
        findings.append(_finding(
            file_path, 0, R_TEXT_SPACING, Severity.P3,
            f"页面含 {len(nowrap_selectors)} 处 white-space:nowrap（非按钮/单元格），"
            "可能阻止用户调整文字间距后的重排。建议仅在必要内联场景使用"
            "（WCAG 2.1 SC 1.4.12，W275 E2-20 深化）",
            "; ".join(nowrap_selectors[:3]),
        ))

    return findings


# ---------- 规则 21：内容重排焦点保持规则（W275 E 方向深化） ----------
def rule_21_reflow_focus(html_content, file_path):
    """E2-21：WCAG 2.1 SC 1.4.10 Reflow + SC 2.1.2 No Keyboard Trap。
    检测 viewport meta 禁用缩放（user-scalable=no / maximum-scale=1），
    以及 CSS 固定宽度（width: XXXpx 无 max-width 响应式）导致 320px 重排失败。"""
    findings = []
    parser = _parse_html(html_content)

    # 1. viewport 禁用缩放
    for el in parser.elements:
        if el.tag != "meta":
            continue
        name = el.attrs.get("name", "").strip().lower()
        if name != "viewport":
            continue
        content = el.attrs.get("content", "")
        # user-scalable=no 或 maximum-scale=1（含 1.0）
        if re.search(r"user-scalable\s*=\s*no", content, re.I):
            findings.append(_finding(
                file_path, el.line, R_REFLOW_FOCUS, Severity.P1,
                "viewport meta 设 user-scalable=no 禁用用户缩放，"
                "低视力用户无法放大页面（WCAG 2.1 SC 1.4.4 / 1.4.10，W275 E2-21 深化）",
                _snippet(html_content, el.line),
            ))
        max_scale_match = re.search(r"maximum-scale\s*=\s*([0-9.]+)", content, re.I)
        if max_scale_match:
            try:
                ms = float(max_scale_match.group(1))
                if ms <= 1.0:
                    findings.append(_finding(
                        file_path, el.line, R_REFLOW_FOCUS, Severity.P1,
                        f"viewport meta 设 maximum-scale={ms} 限制缩放上限，"
                        "低视力用户无法放大页面（WCAG 2.1 SC 1.4.4，W275 E2-21 深化）",
                        _snippet(html_content, el.line),
                    ))
            except ValueError:
                pass

    # 2. 固定宽度容器无响应式（width: XXXpx 且无 max-width/min-width 兜底）
    css_text = "\n".join(css for _, css in parser.style_blocks)
    fixed_width_count = 0
    for selector, decls in _extract_css_rules(css_text):
        # 跳过媒体查询内的规则（已在响应式处理）
        if "@media" in selector:
            continue
        width_match = re.search(r"(?<![\w-])width\s*:\s*(\d{3,})px", decls)
        if not width_match:
            continue
        width_val = int(width_match.group(1))
        if width_val < 320:
            continue
        # 检查同块是否有 max-width/min-width 兜底
        has_responsive = bool(re.search(r"(?:max|min)-width\s*:", decls))
        if has_responsive:
            continue
        fixed_width_count += 1
    if fixed_width_count >= 3:
        findings.append(_finding(
            file_path, 0, R_REFLOW_FOCUS, Severity.P2,
            f"页面含 {fixed_width_count} 处固定宽度（≥320px）CSS 规则且无 max-width/min-width 兜底，"
            "320px 重排时可能溢出或丢失焦点（WCAG 2.1 SC 1.4.10，W275 E2-21 深化）",
            "建议为大宽度容器添加 max-width: 100% 或响应式断点",
        ))

    return findings


# ---------- W279 E 方向深化：5 项表单与状态消息规则（E2-22 至 E2-26）----------


def rule_22_error_identification(html_content, file_path):
    """E2-22：WCAG 3.3.1 Error Identification。
    检测表单错误提示是否以文本形式呈现（非仅依赖颜色或图标）。
    触发条件：含 input/select/textarea 的页面若无错误提示文本节点（class 含 error/invalid/warning），
    或错误提示仅用颜色区分（class 含 error 但无文本内容），视为错误识别缺失。"""
    findings = []
    parser = _parse_html(html_content)

    form_controls = [el for el in parser.elements if el.tag in ("input", "select", "textarea")]
    if not form_controls:
        return findings

    # 检测是否存在错误提示节点
    error_keywords = ("error", "invalid", "warning", "错误", "警告", "无效")
    has_error_text_node = False
    for el in parser.elements:
        cls = el.attrs.get("class", "").lower()
        if any(kw in cls for kw in error_keywords):
            # 检测是否有文本内容（aria-label 或内联文本）
            aria_label = el.attrs.get("aria-label", "").strip()
            if aria_label:
                has_error_text_node = True
                break

    if not has_error_text_node:
        # 检测是否存在仅用颜色区分的错误提示（class 含 error 但无文本）
        color_only_errors = 0
        for el in parser.elements:
            cls = el.attrs.get("class", "").lower()
            if "error" in cls and not el.attrs.get("aria-label"):
                color_only_errors += 1
        if color_only_errors >= 2:
            findings.append(_finding(
                file_path, 0, R_ERROR_IDENTIFICATION, Severity.P2,
                f"页面含 {len(form_controls)} 个表单控件 + {color_only_errors} 处仅用 class=error 标记的错误提示，"
                "错误提示需以文本形式呈现给用户（WCAG 3.3.1，W279 E2-22 深化）",
                "建议为错误提示节点添加 aria-label 或内联文本描述具体错误",
            ))

    return findings


def rule_23_labels_or_instructions(html_content, file_path):
    """E2-23：WCAG 3.3.2 Labels or Instructions。
    检测表单控件是否有关联的 label（<label for> 或 aria-label 或 aria-labelledby）。
    触发条件：input/select/textarea 无关联 label 且无 aria-label/aria-labelledby。"""
    findings = []
    parser = _parse_html(html_content)

    # 收集所有 <label for> 的目标 id
    label_for_ids = set()
    for el in parser.elements:
        if el.tag == "label":
            for_id = el.attrs.get("for", "").strip()
            if for_id:
                label_for_ids.add(for_id)

    # 检查需要 label 的控件（排除 hidden/submit/button/image）
    skip_types = {"hidden", "submit", "button", "image", "reset"}
    missing_count = 0
    first_missing_line = 0
    for el in parser.elements:
        if el.tag not in ("input", "select", "textarea"):
            continue
        input_type = el.attrs.get("type", "").lower()
        if input_type in skip_types:
            continue
        ctrl_id = el.attrs.get("id", "").strip()
        aria_label = el.attrs.get("aria-label", "").strip()
        aria_labelledby = el.attrs.get("aria-labelledby", "").strip()
        title = el.attrs.get("title", "").strip()
        # 有 label for 关联 / aria-label / aria-labelledby / title 任一即可
        if (ctrl_id and ctrl_id in label_for_ids) or aria_label or aria_labelledby or title:
            continue
        missing_count += 1
        if first_missing_line == 0:
            first_missing_line = el.line

    if missing_count >= 1:
        severity = Severity.P1 if missing_count >= 3 else Severity.P2
        findings.append(_finding(
            file_path, first_missing_line, R_LABELS_OR_INSTRUCTIONS, severity,
            f"页面含 {missing_count} 个表单控件缺少关联 label（<label for> 或 aria-label 或 aria-labelledby 或 title）。"
            "表单控件必须有关联的可访问名称（WCAG 3.3.2，W279 E2-23 深化）",
            _snippet(html_content, first_missing_line),
        ))

    return findings


def rule_24_error_suggestion(html_content, file_path):
    """E2-24：WCAG 3.3.3 Error Suggestion。
    检测表单错误提示是否提供修正建议（如格式示例或修正方向）。
    触发条件：错误提示节点（class 含 error/invalid）的文本长度过短（<10 字符）或无格式提示。"""
    findings = []
    parser = _parse_html(html_content)

    error_keywords = ("error", "invalid")
    short_error_count = 0
    first_short_line = 0
    for el in parser.elements:
        cls = el.attrs.get("class", "").lower()
        if not any(kw in cls for kw in error_keywords):
            continue
        # 检测 aria-label 或 aria-describedby 的文本长度
        text = el.attrs.get("aria-label", "").strip()
        if not text:
            # 检测 aria-describedby 引用的节点
            describedby = el.attrs.get("aria-describedby", "").strip()
            if describedby:
                # 简化处理：仅检测 aria-label，实际生产环境需解析 describedby 引用
                continue
            continue
        if len(text) < 10:
            short_error_count += 1
            if first_short_line == 0:
                first_short_line = el.line

    if short_error_count >= 2:
        findings.append(_finding(
            file_path, first_short_line, R_ERROR_SUGGESTION, Severity.P3,
            f"页面含 {short_error_count} 处错误提示文本长度过短（<10 字符），"
            "错误提示应提供具体修正建议（如格式示例 'email@example.com'，WCAG 3.3.3，W279 E2-24 深化）",
            _snippet(html_content, first_short_line),
        ))

    return findings


def rule_25_status_messages(html_content, file_path):
    """E2-25：WCAG 4.1.3 Status Messages。
    检测动态状态消息是否使用 role=status/alert 或 aria-live 通告屏幕阅读器。
    触发条件：含 class 含 status/message/notice/toast/success 的节点未设 role=status/alert 或 aria-live。"""
    findings = []
    parser = _parse_html(html_content)

    status_keywords = ("status", "message", "notice", "toast", "success", "info", "状态", "消息", "提示")
    missing_count = 0
    first_missing_line = 0
    for el in parser.elements:
        if el.tag in ("script", "style"):
            continue
        cls = el.attrs.get("class", "").lower()
        if not any(kw in cls for kw in status_keywords):
            continue
        role = el.attrs.get("role", "").lower().strip()
        aria_live = el.attrs.get("aria-live", "").lower().strip()
        if role in ("status", "alert") or aria_live in ("polite", "assertive"):
            continue
        missing_count += 1
        if first_missing_line == 0:
            first_missing_line = el.line

    if missing_count >= 2:
        findings.append(_finding(
            file_path, first_missing_line, R_STATUS_MESSAGES, Severity.P2,
            f"页面含 {missing_count} 处状态消息节点（class 含 status/message/notice/toast/success）"
            "未设 role=status/alert 或 aria-live，屏幕阅读器无法感知动态更新"
            "（WCAG 4.1.3，W279 E2-25 深化）",
            _snippet(html_content, first_missing_line),
        ))

    return findings


def rule_26_target_size_enhanced(html_content, file_path):
    """E2-26：WCAG 2.5.8 Target Size Minimum（增强版）。
    在 E2-7 基础上增加间距检测：相邻交互元素间距过小（<4px）会降低可点击性。
    触发条件：相邻 a/button 的 class 含 inline/compact/mini 但无 min-width/min-height 兜底。"""
    findings = []
    parser = _parse_html(html_content)

    compact_keywords = ("inline", "compact", "mini", "small", "tiny", "xs")
    compact_count = 0
    first_compact_line = 0
    for el in parser.elements:
        if el.tag not in ("a", "button"):
            continue
        cls = el.attrs.get("class", "").lower()
        if not any(kw in cls for kw in compact_keywords):
            continue
        style = el.attrs.get("style", "").lower()
        # 检测是否有 min-width/min-height 兜底
        has_min_size = bool(re.search(r"min-(?:width|height)\s*:\s*\d+", style))
        if has_min_size:
            continue
        compact_count += 1
        if first_compact_line == 0:
            first_compact_line = el.line

    if compact_count >= 3:
        findings.append(_finding(
            file_path, first_compact_line, R_TARGET_SIZE_ENHANCED, Severity.P3,
            f"页面含 {compact_count} 个紧凑型交互元素（class 含 inline/compact/mini/small）"
            "且无 min-width/min-height 兜底，相邻元素间距可能不足 4px，"
            "降低可点击性与触摸友好性（WCAG 2.5.8 增强版，W279 E2-26 深化）",
            _snippet(html_content, first_compact_line),
        ))

    return findings


# ---------- W283 E 方向深化：4 项持续可用与解析规则（E2-27 至 E2-30）----------


def check_pause_stop_hide(html_content, file_path):
    """E2-27：WCAG 2.2.2 Pause, Stop, Hide。
    检测自动播放/滚动/动画是否提供暂停/停止/隐藏机制。
    触发条件：<video autoplay>/<audio autoplay> 无 controls、<marquee>/<blink> 元素、
    CSS animation infinite 无限循环但页面缺少 pause/stop/play 控制按钮。"""
    findings = []
    parser = _parse_html(html_content)

    # 1. <video autoplay> / <audio autoplay> 无 controls
    for el in parser.elements:
        if el.tag not in ("video", "audio"):
            continue
        if "autoplay" not in el.attrs:
            continue
        if "controls" not in el.attrs:
            findings.append(_finding(
                file_path, el.line, R_PAUSE_STOP_HIDE, Severity.P1,
                f"<{el.tag} autoplay> 未设 controls，用户无法暂停/停止自动播放"
                "（WCAG 2.2.2，W283 E2-27 深化）",
                _snippet(html_content, el.line),
            ))

    # 2. <marquee> 与 <blink>（已废弃但仍可能存在，自动滚动/闪烁且无法暂停）
    for match in re.finditer(r"<(marquee|blink)\b", html_content, re.IGNORECASE):
        line_num = html_content[:match.start()].count("\n") + 1
        tag = match.group(1).lower()
        findings.append(_finding(
            file_path, line_num, R_PAUSE_STOP_HIDE, Severity.P1,
            f"<{tag}> 元素自动滚动/闪烁且无法暂停，应改用 CSS animation 配合 pause 按钮"
            "（WCAG 2.2.2，W283 E2-27 深化）",
            _snippet(html_content, line_num),
        ))

    # 3. CSS animation infinite 无限循环但页面无 pause/stop/play 控件
    css_text = "\n".join(css for _, css in parser.style_blocks)
    infinite_anim_count = 0
    first_anim_line = 0
    for _selector, decls in _extract_css_rules(css_text):
        if not re.search(r"animation\s*:", decls, re.I):
            continue
        if re.search(r"\binfinite\b", decls, re.I):
            infinite_anim_count += 1
            # 尝试定位 style 块起始行
            for start_line, css in parser.style_blocks:
                if decls in css and start_line > first_anim_line:
                    first_anim_line = start_line
                    break

    if infinite_anim_count >= 1:
        # 检测是否提供 pause/stop/play 控件（按钮/类名/aria-label 关键词）
        pause_patterns = re.compile(
            r'<button[^>]*(?:pause|stop|play|暂停|停止|播放)[^>]*>|'
            r'class\s*=\s*["\'][^"\']*(?:pause|stop|play|暂停|停止|播放)[^"\']*["\']|'
            r'aria-label\s*=\s*["\'][^"\']*(?:pause|stop|play|暂停|停止|播放)[^"\']*["\']',
            re.IGNORECASE,
        )
        if not pause_patterns.search(html_content):
            findings.append(_finding(
                file_path, first_anim_line, R_PAUSE_STOP_HIDE, Severity.P2,
                f"页面含 {infinite_anim_count} 处 CSS animation infinite 无限循环动画，"
                "但未检测到 pause/stop/play 控件。建议提供动画暂停机制（如 .pause 按钮）"
                "（WCAG 2.2.2，W283 E2-27 深化）",
                "animation: ... infinite; 应配合 .pause 控件",
            ))

    return findings


def check_no_three_flashes(html_content, file_path):
    """E2-28：WCAG 2.3.1 Three Flashes or Below Threshold。
    检测页面是否含超过 3 次/秒闪烁的元素（光敏性癫痫安全阈值）。
    触发条件：<blink> 元素自动闪烁、CSS animation duration < 333ms 且 infinite 且关键帧含闪烁语义
    （动画名含 flash/blink/flicker 或关键帧内 opacity 在 0/1 之间切换）。"""
    findings = []
    parser = _parse_html(html_content)

    # 1. <blink> 元素（自动闪烁，频率不可控）
    for match in re.finditer(r"<blink\b", html_content, re.IGNORECASE):
        line_num = html_content[:match.start()].count("\n") + 1
        findings.append(_finding(
            file_path, line_num, R_NO_THREE_FLASHES, Severity.P1,
            "<blink> 元素自动闪烁可能超过 3 次/秒阈值，存在光敏性癫痫风险。"
            "应移除 <blink>，改用静态高亮或其他非闪烁形式（WCAG 2.3.1，W283 E2-28 深化）",
            _snippet(html_content, line_num),
        ))

    # 2. CSS animation duration < 333ms 且 infinite（频率 > 3Hz）
    css_text = "\n".join(css for _, css in parser.style_blocks)
    flash_keywords = ("flash", "blink", "flicker", "闪烁")
    for selector, decls in _extract_css_rules(css_text):
        if not re.search(r"animation\s*:", decls, re.I):
            continue
        # 提取 animation-duration（支持简写 animation: name dur ... 或 animation-duration: ...）
        duration_match = re.search(
            r"animation(?:-duration)?\s*:\s*[^;]*?([0-9]+(?:\.[0-9]+)?)\s*(ms|s)",
            decls, re.I,
        )
        if not duration_match:
            continue
        try:
            val = float(duration_match.group(1))
            unit = duration_match.group(2).lower()
            duration_ms = val if unit == "ms" else val * 1000
        except ValueError:
            continue
        if duration_ms >= 333:
            continue
        if not re.search(r"\binfinite\b", decls, re.I):
            continue
        # 进一步判定是否为"闪烁"动画：动画名含 flash/blink/flicker 或关键帧含 opacity 0 切换
        anim_name_match = re.search(
            r"animation(?:-name)?\s*:\s*([a-zA-Z_-][\w-]*)", decls, re.I,
        )
        anim_name = anim_name_match.group(1).lower() if anim_name_match else ""
        is_flash_anim = any(kw in anim_name for kw in flash_keywords)
        if not is_flash_anim and anim_name:
            # 关键帧定义内含 opacity: 0 ↔ opacity: 1 切换
            keyframe_block = re.search(
                rf"@keyframes\s+{re.escape(anim_name)}\b[^{{]*\{{[^@]*?(?:opacity\s*:\s*0\b[^@]*?opacity\s*:\s*1\b|opacity\s*:\s*1\b[^@]*?opacity\s*:\s*0\b)",
                css_text, re.I | re.DOTALL,
            )
            if keyframe_block:
                is_flash_anim = True
        if is_flash_anim:
            findings.append(_finding(
                file_path, 0, R_NO_THREE_FLASHES, Severity.P1,
                f"CSS animation {selector!r} 持续时间 {duration_ms:g}ms < 333ms 且 infinite，"
                f"闪烁频率超过 3 次/秒阈值，存在光敏性癫痫风险"
                f"（WCAG 2.3.1，W283 E2-28 深化）",
                f"{selector} {{ animation: ... {duration_match.group(0)} ... infinite; }}",
            ))

    return findings


def check_parsing(html_content, file_path):
    """E2-29：WCAG 4.1.1 Parsing。
    检测 HTML 是否有严重解析错误（重复 ID、未闭合标签、stray end tag）。
    严重解析错误会导致辅助技术 DOM 解析异常，影响可访问性。"""
    findings = []
    parser = _parse_html(html_content)

    # 1. 重复 ID
    id_count = {}
    for el in parser.elements:
        eid = el.attrs.get("id", "").strip()
        if eid:
            id_count.setdefault(eid, []).append(el.line)
    for eid, lines in id_count.items():
        if len(lines) > 1:
            findings.append(_finding(
                file_path, lines[0], R_PARSING, Severity.P1,
                f"重复 ID {eid!r} 出现在 {len(lines)} 处（行 {lines}），"
                "ID 必须唯一，否则辅助技术定位元素异常（WCAG 4.1.1，W283 E2-29 深化）",
                _snippet(html_content, lines[0]),
            ))

    # 2. 未闭合的非空元素（起始标签 > 结束标签）
    void_tags = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }
    optional_close = {
        "html", "head", "body", "p", "li", "dt", "dd", "option",
        "tr", "td", "th", "thead", "tbody", "tfoot", "colgroup",
    }
    open_count = {}
    close_count = {}
    open_lines = {}
    for el in parser.elements:
        tag = el.tag
        if tag in void_tags or tag in optional_close:
            continue
        open_count[tag] = open_count.get(tag, 0) + 1
        if tag not in open_lines:
            open_lines[tag] = el.line

    endtag_pattern = re.compile(r"</\s*([a-zA-Z][\w-]*)\s*>", re.IGNORECASE)
    for match in endtag_pattern.finditer(html_content):
        tag = match.group(1).lower()
        if tag in void_tags or tag in optional_close:
            continue
        close_count[tag] = close_count.get(tag, 0) + 1

    for tag, oc in open_count.items():
        cc = close_count.get(tag, 0)
        if oc > cc:
            findings.append(_finding(
                file_path, open_lines[tag], R_PARSING, Severity.P2,
                f"<{tag}> 起始标签 {oc} 个但结束标签仅 {cc} 个，可能存在未闭合标签。"
                "未闭合标签会破坏辅助技术的 DOM 解析（WCAG 4.1.1，W283 E2-29 深化）",
                _snippet(html_content, open_lines[tag]),
            ))

    # 3. Stray end tag（结束标签无对应起始标签）
    for tag, cc in close_count.items():
        oc = open_count.get(tag, 0)
        if cc > oc:
            for match in re.finditer(rf"</\s*{re.escape(tag)}\s*>", html_content, re.IGNORECASE):
                line_num = html_content[:match.start()].count("\n") + 1
                findings.append(_finding(
                    file_path, line_num, R_PARSING, Severity.P2,
                    f"</{tag}> 结束标签无对应起始标签（stray end tag）。"
                    "冗余结束标签会被解析器丢弃或破坏 DOM 树（WCAG 4.1.1，W283 E2-29 深化）",
                    _snippet(html_content, line_num),
                ))
                break

    return findings


def check_consistent_navigation(html_content, file_path):
    """E2-30：WCAG 3.2.3 Consistent Navigation。
    检测导航元素（<nav> / role=navigation）是否有稳定识别属性（id 或 aria-label），
    保证在多页面中保持相同顺序与定位。
    触发条件：页面含多个 <nav>/role=navigation 但其中有节点缺少 id/aria-label/aria-labelledby 稳定标识。"""
    findings = []
    parser = _parse_html(html_content)

    nav_elements = []
    for el in parser.elements:
        if el.tag == "nav":
            nav_elements.append(el)
            continue
        role = el.attrs.get("role", "").strip().lower()
        if role == "navigation":
            nav_elements.append(el)

    if len(nav_elements) <= 1:
        return findings

    missing_id_count = 0
    first_missing_line = 0
    for el in nav_elements:
        has_id = bool(el.attrs.get("id", "").strip())
        has_aria_label = bool(el.attrs.get("aria-label", "").strip())
        has_aria_labelledby = bool(el.attrs.get("aria-labelledby", "").strip())
        if not (has_id or has_aria_label or has_aria_labelledby):
            missing_id_count += 1
            if first_missing_line == 0:
                first_missing_line = el.line

    if missing_id_count >= 1:
        findings.append(_finding(
            file_path, first_missing_line, R_CONSISTENT_NAVIGATION, Severity.P3,
            f"页面含 {len(nav_elements)} 个 <nav>/role=navigation，"
            f"其中 {missing_id_count} 个缺少稳定标识（id/aria-label/aria-labelledby）。"
            "多导航区域必须有可区分的稳定标识，才能在多页面中保持相同顺序"
            "（WCAG 3.2.3，W283 E2-30 深化）",
            _snippet(html_content, first_missing_line),
        ))

    return findings


# ---------- W316 E 方向深化：10 项 WCAG 2.2 完整规范扩展规则（E2-31 至 E2-40）----------


def check_language_of_page(html_content, file_path):
    """E2-31：WCAG 3.1.1 Language of Page。
    检测 <html> 元素是否有 lang 属性且值有效（BCP 47 语言标签，如 zh/zh-CN/en/en-US）。
    无 lang 属性 → 屏幕阅读器无法正确发音。"""
    findings = []
    parser = _parse_html(html_content)

    html_el = None
    for el in parser.elements:
        if el.tag == "html":
            html_el = el
            break

    if html_el is None:
        # 可能是片段 HTML（如 data 子页面 include），不报
        return findings

    lang = html_el.attrs.get("lang", "").strip()
    if not lang:
        findings.append(_finding(
            file_path, html_el.line, R_LANGUAGE_OF_PAGE, Severity.P1,
            "<html> 元素缺少 lang 属性，屏幕阅读器无法确定页面语言"
            "（WCAG 3.1.1，W316 E2-31 深化）",
            _snippet(html_content, html_el.line),
        ))
    else:
        # 简单验证：lang 应至少 2 字符且含字母
        if len(lang) < 2 or not re.search(r"[a-zA-Z]", lang):
            findings.append(_finding(
                file_path, html_el.line, R_LANGUAGE_OF_PAGE, Severity.P2,
                f"<html lang={lang!r}> 值不符合 BCP 47 语言标签格式（如 zh/zh-CN/en）"
                "（WCAG 3.1.1，W316 E2-31 深化）",
                _snippet(html_content, html_el.line),
            ))

    return findings


def check_link_purpose(html_content, file_path):
    """E2-32：WCAG 2.4.4 Link Purpose (In Context) + 2.4.9 Link Purpose (Link Only)。
    检测 <a> 链接文本是否模糊（仅"点击这里"/"更多"/"链接"/here/more/click 等），
    用户脱离上下文时无法判断链接目的。"""
    findings = []
    parser = _parse_html(html_content)

    # 模糊链接文本（中英文）
    vague_patterns = re.compile(
        r"^(点击这里|点击|查看|更多|详见|链接|这里|此处|查看更多|了解更多|阅读更多|"
        r"click\s*here|here|more|read\s*more|click|link|this|details?|continue)$",
        re.IGNORECASE,
    )

    vague_count = 0
    first_vague_line = 0
    for el in parser.elements:
        if el.tag != "a":
            continue
        # 收集链接文本（直接文本 + 子元素文本）
        link_text = el.text.strip() if el.text else ""
        # 如果有 aria-label，以 aria-label 为准（已有可访问名，不报模糊）
        aria_label = el.attrs.get("aria-label", "").strip()
        if aria_label:
            continue
        # 如果链接含 <img alt>，认为有替代文本
        # （简化检测：如果链接文本为空但有 aria-label 已跳过，此处只检测有文本但模糊的）
        if not link_text:
            continue
        # 清理文本：去除首尾空白和常见标点
        clean_text = re.sub(r"^[\s\d•·\-–—]+|[\s·]+$", "", link_text).strip()
        if vague_patterns.match(clean_text):
            vague_count += 1
            if first_vague_line == 0:
                first_vague_line = el.line

    if vague_count >= 1:
        findings.append(_finding(
            file_path, first_vague_line, R_LINK_PURPOSE, Severity.P2,
            f"页面含 {vague_count} 个链接使用模糊文本（如「点击这里」/「更多」/「here」），"
            "脱离上下文时用户无法判断链接目的。应使用描述性链接文本"
            "（WCAG 2.4.4/2.4.9，W316 E2-32 深化）",
            _snippet(html_content, first_vague_line),
        ))

    return findings


def check_multiple_ways(html_content, file_path):
    """E2-33：WCAG 2.4.5 Multiple Ways。
    检测页面是否提供至少 2 种导航方式（导航栏 + 搜索框/站点地图/面包屑等），
    帮助用户以不同方式发现内容。"""
    findings = []
    parser = _parse_html(html_content)

    ways = 0
    way_names = []

    # 方式 1：<nav> 导航栏
    has_nav = any(el.tag == "nav" for el in parser.elements)
    if has_nav:
        ways += 1
        way_names.append("导航栏<nav>")

    # 方式 2：搜索框（<input type=search> / role=search / 搜索类名）
    has_search = bool(
        re.search(r'<input[^>]*type\s*=\s*["\']?search["\']?', html_content, re.I)
        or re.search(r'role\s*=\s*["\']?search["\']?', html_content, re.I)
        or re.search(r'class\s*=\s*["\'][^"\']*search[^"\']*["\']', html_content, re.I)
        or re.search(r'id\s*=\s*["\'][^"\']*search[^"\']*["\']', html_content, re.I)
    )
    if has_search:
        ways += 1
        way_names.append("搜索框")

    # 方式 3：面包屑导航（breadcrumb 类名或 aria-label）
    has_breadcrumb = bool(
        re.search(r'class\s*=\s*["\'][^"\']*breadcrumb[^"\']*["\']', html_content, re.I)
        or re.search(r'aria-label\s*=\s*["\'][^"\']*面包屑[^"\']*["\']', html_content, re.I)
        or re.search(r'class\s*=\s*["\'][^"\']*面包屑[^"\']*["\']', html_content, re.I)
    )
    if has_breadcrumb:
        ways += 1
        way_names.append("面包屑")

    # 方式 4：站点地图链接（href 含 sitemap / 站点地图）
    has_sitemap = bool(re.search(r'href\s*=\s*["\'][^"\']*(?:sitemap|site-map|站点地图)["\']', html_content, re.I))
    if has_sitemap:
        ways += 1
        way_names.append("站点地图")

    # 方式 5：skip link（跳过链接也算一种导航辅助）
    has_skip = bool(re.search(r'class\s*=\s*["\'][^"\']*skip-link[^"\']*["\']', html_content, re.I))
    if has_skip:
        ways += 1
        way_names.append("跳过链接")

    if ways < 2:
        findings.append(_finding(
            file_path, 1, R_MULTIPLE_WAYS, Severity.P2,
            f"页面仅提供 {ways} 种导航方式（{', '.join(way_names) or '无'}），"
            "应至少提供 2 种（如导航栏 + 搜索框/面包屑/站点地图），"
            "帮助用户以不同方式发现内容"
            "（WCAG 2.4.5，W316 E2-33 深化）",
            "",
        ))

    return findings


def check_non_text_contrast(html_content, file_path):
    """E2-34：WCAG 1.4.11 Non-text Contrast。
    检测 UI 组件（button/input/select/textarea 的 border-color）与背景的对比度 ≥ 3:1。
    非文本元素（边框/图标）对比度不足会影响识别。"""
    findings = []
    parser = _parse_html(html_content)

    css_text = "\n".join(css for _, css in parser.style_blocks)
    if not css_text.strip():
        return findings

    # 检测交互元素的 border-color vs background-color 对比度
    ui_selector_re = re.compile(
        r"\b(button|input|select|textarea|\.btn|\.button|\.link|\.tab|\.stage-btn)\b",
        re.I,
    )
    THRESHOLD = 3.0

    for selector, decls in _extract_css_rules(css_text):
        if not ui_selector_re.search(selector):
            continue
        # 提取 border-color
        border_color_val = None
        bg_val = None
        for decl in decls.split(";"):
            if ":" not in decl:
                continue
            k, _, v = decl.partition(":")
            k = k.strip().lower()
            v = v.strip()
            if k == "border-color":
                border_color_val = v
            elif k in ("background", "background-color"):
                bg_val = v
        if not border_color_val or not bg_val:
            continue
        if "var(" in border_color_val or "var(" in bg_val:
            continue
        if "gradient" in bg_val or "gradient" in border_color_val:
            continue
        border_rgb = _parse_color(border_color_val)
        bg_rgb = _parse_color(bg_val)
        if not border_rgb or not bg_rgb:
            continue
        ratio = _contrast_ratio(border_rgb, bg_rgb)
        if ratio < THRESHOLD:
            findings.append(_finding(
                file_path, 0, R_NON_TEXT_CONTRAST, Severity.P2,
                f"选择器 {selector!r} 的 border-color={border_color_val} vs "
                f"background={bg_val} 对比度 {ratio:.2f}:1 低于 WCAG 1.4.11 "
                f"非文本对比度阈值 {THRESHOLD}:1",
                f"border-color:{border_color_val}; background:{bg_val}; ratio={ratio:.2f}",
            ))

    return findings


def check_hover_focus_content(html_content, file_path):
    """E2-35：WCAG 1.4.13 Content on Hover or Focus。
    检测悬停/聚焦触发的附加内容（tooltip/popover）是否满足三条件：
    1. 可关闭（Esc 键关闭）
    2. 可悬停（鼠标移入附加内容不立即消失）
    3. 持续显示（直到用户移除触发器或关闭）
    静态检测：title 属性（原生 tooltip 不满足条件）+ tooltip 类名但无 Esc 处理。"""
    findings = []

    # 1. title 属性作为 tooltip（原生 tooltip 不可关闭、不可悬停、不持续）
    # 仅检测交互元素上的 title（a/button/input/img 等）
    parser = _parse_html(html_content)
    interactive_tags = ("a", "button", "input", "select", "textarea", "summary", "img")
    title_count = 0
    first_title_line = 0
    for el in parser.elements:
        if el.tag not in interactive_tags:
            continue
        title = el.attrs.get("title", "").strip()
        if not title:
            continue
        # title 长度 > 5 才报（短 title 可能只是标签补充）
        if len(title) > 5:
            title_count += 1
            if first_title_line == 0:
                first_title_line = el.line

    if title_count >= 2:
        findings.append(_finding(
            file_path, first_title_line, R_HOVER_FOCUS_CONTENT, Severity.P3,
            f"页面含 {title_count} 个交互元素使用 title 属性作为 tooltip，"
            "原生 title tooltip 不可关闭（无 Esc 键）、不可悬停（鼠标移入即消失）、"
            "不持续显示。建议改用自定义 tooltip 组件并实现三条件"
            "（WCAG 1.4.13，W316 E2-35 深化）",
            _snippet(html_content, first_title_line),
        ))

    # 2. CSS tooltip 类名但无 Esc 处理（检测 .tooltip:hover 但无 JS Esc 监听）
    has_tooltip_css = bool(re.search(r"\.tooltip\s*[,{:~+>]|\.popover", html_content, re.I))
    if has_tooltip_css:
        has_esc_handler = bool(re.search(
            r"(?:Escape|Esc|key\s*===?\s*['\"]Escape['\"]|keyCode\s*===?\s*27)",
            html_content, re.I,
        ))
        if not has_esc_handler:
            findings.append(_finding(
                file_path, 1, R_HOVER_FOCUS_CONTENT, Severity.P2,
                "页面检测到 tooltip/popover CSS 但未找到 Esc 键关闭处理。"
                "悬停/聚焦触发的附加内容必须可关闭（Esc 键）"
                "（WCAG 1.4.13，W316 E2-35 深化）",
                "",
            ))

    return findings


def check_char_key_shortcuts(html_content, file_path):
    """E2-36：WCAG 2.1.4 Character Key Shortcuts。
    检测单字符快捷键（accesskey 或 JS keydown 单字符监听）是否满足：
    可关闭 / 可重映射 / 仅在聚焦时生效。
    单字符快捷键可能误触发（如语音输入用户）。"""
    findings = []
    parser = _parse_html(html_content)

    # 1. accesskey 属性（单字符快捷键）
    accesskey_count = 0
    first_accesskey_line = 0
    for el in parser.elements:
        ak = el.attrs.get("accesskey", "").strip()
        if ak:
            accesskey_count += 1
            if first_accesskey_line == 0:
                first_accesskey_line = el.line

    # accesskey 本身是浏览器原生快捷键，WCAG 2.1.4 主要关注 JS 实现的单字符快捷键
    # 但 accesskey 无关闭机制也值得提示
    if accesskey_count >= 2:
        findings.append(_finding(
            file_path, first_accesskey_line, R_CHAR_KEY_SHORTCUTS, Severity.P3,
            f"页面含 {accesskey_count} 个 accesskey 属性，单字符快捷键可能误触发"
            "（语音输入/键盘用户）。建议提供关闭或重映射机制"
            "（WCAG 2.1.4，W316 E2-36 深化）",
            _snippet(html_content, first_accesskey_line),
        ))

    # 2. JS 单字符快捷键（addEventListener keydown 检测单字符 e.key === 'x'）
    # 检测模式：e.key === 'x' 或 e.key == 'x' 或 event.key == 'x'
    # 排除修饰键组合（Ctrl+ / Meta+ / Alt+）
    single_char_keydown = re.findall(
        r"(?:e|event)\.key\s*===?\s*['\"]([a-zA-Z])['\"]",
        html_content,
    )
    # 排除常见非快捷键用途（如 Enter/Escape/Tab 等不是单字符）
    # single_char_keydown 已经过滤为单字母
    if len(single_char_keydown) >= 1:
        # 检测是否仅在聚焦时生效（检测元素级 addEventListener 而非 document/window 级）
        # 简化：如果检测到 document.addEventListener 或 window.addEventListener keydown
        # 且匹配单字符，则视为全局单字符快捷键
        has_global_listener = bool(re.search(
            r"(?:document|window)\.addEventListener\s*\(\s*['\"]keydown",
            html_content, re.I,
        ))
        if has_global_listener:
            findings.append(_finding(
                file_path, 1, R_CHAR_KEY_SHORTCUTS, Severity.P2,
                f"页面检测到 {len(single_char_keydown)} 个全局单字符快捷键"
                f"（{', '.join(single_char_keydown[:5])}），"
                "全局单字符快捷键可能误触发（语音输入用户说字母即触发）。"
                "应提供关闭、重映射、或仅在特定元素聚焦时生效"
                "（WCAG 2.1.4，W316 E2-36 深化）",
                "",
            ))

    return findings


def check_pointer_gestures(html_content, file_path):
    """E2-37：WCAG 2.5.1 Pointer Gestures。
    检测多点触控或路径手势是否有单点替代方案。
    触发条件：JS 中 touchstart 检测 touches.length > 1（多指）或
    touchmove 检测路径手势（swipe/pinch）但无 click 替代。"""
    findings = []

    # 检测多指手势（touches.length > 1 / touches.length === 2）
    multi_touch = bool(re.search(
        r"touches\.length\s*[><=]+\s*[2-9]|touches\.length\s*===?\s*[2-9]",
        html_content,
    ))
    # 检测路径手势（swipe/pinch/drag 方向检测）
    path_gesture = bool(re.search(
        r"(?:swipe|pinch|gesture|gesturestart|gesturechange)",
        html_content, re.I,
    ))

    if multi_touch or path_gesture:
        # 检测是否有单点替代（click/tap 或 click 事件处理）
        has_click_alt = bool(re.search(
            r"(?:onclick|addEventListener\s*\(\s*['\"]click|\.on\s*\(\s*['\"]click)",
            html_content, re.I,
        ))
        if not has_click_alt:
            gesture_type = "多指触控" if multi_touch else "路径手势"
            findings.append(_finding(
                file_path, 1, R_POINTER_GESTURES, Severity.P2,
                f"页面检测到 {gesture_type} 但未找到 click 替代方案。"
                "多点/路径手势必须有单点（click/tap）替代方案"
                "（WCAG 2.5.1，W316 E2-37 深化）",
                "",
            ))

    return findings


def check_pointer_cancellation(html_content, file_path):
    """E2-38：WCAG 2.5.2 Pointer Cancellation。
    检测 onmousedown/ontouchstart 即时触发操作是否提供 onmouseup/onclick 替代。
    应使用 up 事件触发操作，允许用户通过移开指针取消。"""
    findings = []
    parser = _parse_html(html_content)

    # 检测 onmousedown 但无 onmouseup/onclick 的元素
    down_only_count = 0
    first_down_line = 0
    for el in parser.elements:
        has_mousedown = "onmousedown" in el.attrs or "ontouchstart" in el.attrs
        has_mouseup = "onmouseup" in el.attrs or "ontouchend" in el.attrs
        has_click = "onclick" in el.attrs
        if has_mousedown and not has_mouseup and not has_click:
            down_only_count += 1
            if first_down_line == 0:
                first_down_line = el.line

    if down_only_count >= 1:
        findings.append(_finding(
            file_path, first_down_line, R_POINTER_CANCELLATION, Severity.P2,
            f"页面含 {down_only_count} 个元素使用 onmousedown/ontouchstart 即时触发操作"
            "但无 onmouseup/onclick 替代。用户无法通过移开指针取消操作。"
            "应使用 onmouseup/onclick 触发，down 事件仅做视觉反馈"
            "（WCAG 2.5.2，W316 E2-38 深化）",
            _snippet(html_content, first_down_line),
        ))

    return findings


def check_label_in_name(html_content, file_path):
    """E2-39：WCAG 2.5.3 Label in Name。
    检测可见标签文本是否包含在可访问名（aria-label）中。
    语音控制用户说出可见标签文本应能激活对应元素。
    触发条件：button/a/input 的 aria-label 不包含其可见文本。"""
    findings = []
    parser = _parse_html(html_content)

    for el in parser.elements:
        if el.tag not in ("button", "a", "input"):
            continue
        aria_label = el.attrs.get("aria-label", "").strip()
        if not aria_label:
            continue
        # 获取可见文本
        visible_text = el.text.strip() if el.text else ""
        if not visible_text:
            continue
        # 检查可见文本是否是 aria-label 的一部分（或反之）
        # 简化：如果 aria-label 完全不包含可见文本（忽略大小写），报告
        if (visible_text.lower() not in aria_label.lower() and
                aria_label.lower() not in visible_text.lower()):
            findings.append(_finding(
                file_path, el.line, R_LABEL_IN_NAME, Severity.P3,
                f"<{el.tag}> 可见文本 {visible_text!r} 未包含在 aria-label {aria_label!r} 中。"
                "语音控制用户说出可见标签文本时无法激活元素。"
                "aria-label 应包含或等于可见文本"
                "（WCAG 2.5.3，W316 E2-39 深化）",
                _snippet(html_content, el.line),
            ))

    return findings


def check_animation_interactions(html_content, file_path):
    """E2-40：WCAG 2.3.3 Animation from Interactions（新增 WCAG 2.2）。
    检测非必要动画是否支持 prefers-reduced-motion。
    触发条件：页面含 transition/animation 但无 @media (prefers-reduced-motion: reduce) 覆盖。
    前庭 disorder 用户需要关闭非必要动画。"""
    findings = []
    parser = _parse_html(html_content)
    css_text = "\n".join(css for _, css in parser.style_blocks)
    if not css_text.strip():
        return findings

    # 检测是否含 transition 或 animation
    has_transition = bool(re.search(r"transition\s*:", css_text, re.I))
    has_animation = bool(re.search(r"animation\s*:", css_text, re.I))

    if not (has_transition or has_animation):
        return findings

    # 检测是否有 prefers-reduced-motion 覆盖
    has_reduced_motion = bool(re.search(
        r"@media\s*\(?\s*prefers-reduced-motion\s*:\s*reduce",
        css_text, re.I,
    ))

    if not has_reduced_motion:
        findings.append(_finding(
            file_path, 1, R_ANIMATION_INTERACTIONS, Severity.P2,
            "页面含 transition/animation 但无 @media (prefers-reduced-motion: reduce) 覆盖。"
            "非必要动画应支持用户通过系统设置关闭，前庭 disorder 用户可能因动画不适"
            "（WCAG 2.3.3，W316 E2-40 深化）",
            "建议添加：@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }",
        ))

    return findings


# ---------- 主流程 ----------
ALL_CHECKS = [
    (R_KEYBOARD, check_keyboard_navigation),
    (R_CONTRAST, check_color_contrast),
    (R_ARIA, check_aria_labels),
    (R_FOCUS, check_focus_indicator),
    (R_SCREEN_READER, check_screen_reader),
    (R_FOCUS_VISIBLE, rule_6_focus_visible),
    (R_TARGET_SIZE, rule_7_target_size),
    (R_DRAGGING, rule_8_dragging),
    (R_CONSISTENT_HELP, rule_9_consistent_help),
    # W271 E 方向深化：7 项 a11y 深化规则
    (R_ARIA_LIVE, rule_10_aria_live),
    (R_TABINDEX, rule_11_tabindex),
    (R_FOCUS_TRAP, rule_12_focus_trap),
    (R_SR_ONLY, rule_13_sr_only),
    (R_SKIP_LINK, rule_14_skip_link),
    (R_HEADING_HIERARCHY, rule_15_heading_hierarchy),
    (R_LANDMARK, rule_16_landmark),
    # W275 E 方向深化：5 项 a11y 深化规则（DOM 顺序 + 滚动陷阱 + 颜色单一载体 + 文字间距 + 内容重排）
    (R_KEYBOARD_FOCUS_ORDER, rule_17_keyboard_focus_order),
    (R_SCROLL_TRAP, rule_18_scroll_trap),
    (R_COLOR_ONLY_INFO, rule_19_color_only_info),
    (R_TEXT_SPACING, rule_20_text_spacing),
    (R_REFLOW_FOCUS, rule_21_reflow_focus),
    # W279 E 方向深化：5 项表单与状态消息 a11y 规则
    (R_ERROR_IDENTIFICATION, rule_22_error_identification),
    (R_LABELS_OR_INSTRUCTIONS, rule_23_labels_or_instructions),
    (R_ERROR_SUGGESTION, rule_24_error_suggestion),
    (R_STATUS_MESSAGES, rule_25_status_messages),
    (R_TARGET_SIZE_ENHANCED, rule_26_target_size_enhanced),
    # W283 E 方向深化：4 项持续可用与解析规则（暂停/停止/隐藏 + 无闪烁 + 解析 + 一致导航）
    (R_PAUSE_STOP_HIDE, check_pause_stop_hide),
    (R_NO_THREE_FLASHES, check_no_three_flashes),
    (R_PARSING, check_parsing),
    (R_CONSISTENT_NAVIGATION, check_consistent_navigation),
    # W316 E 方向深化：10 项 WCAG 2.2 完整规范扩展规则（页面语言/链接目的/多种导航/非文本对比/悬停聚焦/字符快捷键/指针手势/指针取消/名称标签/交互动画）
    (R_LANGUAGE_OF_PAGE, check_language_of_page),
    (R_LINK_PURPOSE, check_link_purpose),
    (R_MULTIPLE_WAYS, check_multiple_ways),
    (R_NON_TEXT_CONTRAST, check_non_text_contrast),
    (R_HOVER_FOCUS_CONTENT, check_hover_focus_content),
    (R_CHAR_KEY_SHORTCUTS, check_char_key_shortcuts),
    (R_POINTER_GESTURES, check_pointer_gestures),
    (R_POINTER_CANCELLATION, check_pointer_cancellation),
    (R_LABEL_IN_NAME, check_label_in_name),
    (R_ANIMATION_INTERACTIONS, check_animation_interactions),
]


def audit_file(file_path):
    """对单个 HTML 文件运行 40 项检查，返回 findings 列表"""
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [_finding(file_path, 0, R_KEYBOARD, Severity.P0, f"读取失败: {e}", "")]
    findings = []
    for rule_id, fn in ALL_CHECKS:
        try:
            findings.extend(fn(text, file_path))
        except Exception as e:
            findings.append(_finding(
                file_path, 0, rule_id, Severity.P2,
                f"规则 {rule_id} 执行异常: {e}", "",
            ))
    return findings


def audit_directory(root_dir, output_format="md", quiet=False):
    """扫描目录下所有 HTML，运行 40 项检查，输出报告"""
    root = Path(root_dir)
    if not root.exists():
        print(f"错误：目录不存在 {root}", file=sys.stderr)
        return 2

    html_files = sorted(root.rglob("*.html"))
    all_findings = []
    for f in html_files:
        all_findings.extend(audit_file(f))

    # 计数表
    counts = {r: {"P0": 0, "P1": 0, "P2": 0, "P3": 0} for r, _ in ALL_CHECKS}
    for fd in all_findings:
        if fd["rule_id"] in counts and fd["severity"] in counts[fd["rule_id"]]:
            counts[fd["rule_id"]][fd["severity"]] += 1
    p0_total = sum(c["P0"] for c in counts.values())

    if output_format == "json":
        out = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "scanned_dir": str(root),
            "file_count": len(html_files),
            "rule_count": len(ALL_CHECKS),
            "summary": counts,
            "findings": all_findings,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        report = _render_md(root, html_files, counts, all_findings)
        if not quiet:
            print(report)
        out_path = Path(__file__).parent / "output" / "a11y-report.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")

    return 1 if p0_total > 0 else 0


RULE_DESCRIPTIONS = {
    R_KEYBOARD: "检测 tabindex>0、onfocus/onblur alert 陷阱、accesskey 冲突、对话框焦点管理、Tab 顺序",
    R_CONTRAST: "WCAG 2.2 AA 对比度（正常文本 4.5:1，大文本 3:1），解析内联+style 块",
    R_ARIA: "role 完整性、aria-label/labelledby 互斥、aria-hidden 与 focusable 冲突、aria 引用完整性",
    R_FOCUS: "outline:none 无 :focus-visible 替代、交互元素无 :focus 样式",
    R_SCREEN_READER: "img alt、input label、th scope、noscript 完整性",
    R_FOCUS_VISIBLE: ":focus-visible 样式存在性（WCAG 2.2 SC 2.4.13）",
    R_TARGET_SIZE: "按钮/链接最小 24×24px 目标尺寸（WCAG 2.2 SC 2.5.8）",
    R_DRAGGING: "可拖拽元素需提供键盘替代方案（WCAG 2.2 SC 2.5.7）",
    R_CONSISTENT_HELP: "帮助机制置于 landmark 内保证跨页位置一致（WCAG 2.2 SC 3.2.6）",
    R_ARIA_LIVE: "动态更新内容需设 aria-live 或 role=status/alert（W271 E2-10 深化）",
    R_TABINDEX: "tabindex>0 会破坏自然 tab 顺序（W271 E2-11 深化）",
    R_FOCUS_TRAP: "模态/对话框需有焦点陷阱机制（W271 E2-12 深化）",
    R_SR_ONLY: "图标按钮需 aria-label 或 sr-only 文本（W271 E2-13 深化）",
    R_SKIP_LINK: "页面需 skip link 跳过链接且指向 <main>（W271 E2-14 深化）",
    R_HEADING_HIERARCHY: "标题层级不跳级，首个标题为 h1 且唯一（W271 E2-15 深化）",
    R_LANDMARK: "页面 landmark 完整性 header/main/nav/footer（W271 E2-16 深化）",
    R_KEYBOARD_FOCUS_ORDER: "原生交互元素冗余 tabindex=0 检测（W275 E2-17 深化）",
    R_SCROLL_TRAP: "onscroll 重置滚动 + overflow:hidden 无关闭机制（W275 E2-18 深化）",
    R_COLOR_ONLY_INFO: "状态类名需配文本/aria-label/icon，颜色非唯一载体（W275 E2-19 深化）",
    R_TEXT_SPACING: "!important 锁死间距属性 + white-space:nowrap 阻止重排（W275 E2-20 深化）",
    R_REFLOW_FOCUS: "viewport 禁用缩放 + 固定宽度无响应式兜底（W275 E2-21 深化）",
    R_ERROR_IDENTIFICATION: "表单错误提示需文本呈现，非仅颜色/图标（WCAG 3.3.1，W279 E2-22 深化）",
    R_LABELS_OR_INSTRUCTIONS: "表单控件需关联 label/aria-label/aria-labelledby/title（WCAG 3.3.2，W279 E2-23 深化）",
    R_ERROR_SUGGESTION: "错误提示需提供具体修正建议（WCAG 3.3.3，W279 E2-24 深化）",
    R_STATUS_MESSAGES: "动态状态消息需 role=status/alert 或 aria-live（WCAG 4.1.3，W279 E2-25 深化）",
    R_TARGET_SIZE_ENHANCED: "紧凑型交互元素需 min-width/min-height 兜底（WCAG 2.5.8 增强版，W279 E2-26 深化）",
    R_PAUSE_STOP_HIDE: "自动播放/滚动/动画需提供暂停/停止/隐藏机制（WCAG 2.2.2，W283 E2-27 深化）",
    R_NO_THREE_FLASHES: "页面不含超过 3 次/秒闪烁元素，避免光敏性癫痫风险（WCAG 2.3.1，W283 E2-28 深化）",
    R_PARSING: "HTML 无严重解析错误：重复 ID、未闭合标签、stray end tag（WCAG 4.1.1，W283 E2-29 深化）",
    R_CONSISTENT_NAVIGATION: "多导航元素需稳定标识保证多页面顺序一致（WCAG 3.2.3，W283 E2-30 深化）",
    R_LANGUAGE_OF_PAGE: "<html lang> 存在且有效 BCP 47 语言标签（WCAG 3.1.1，W316 E2-31 深化）",
    R_LINK_PURPOSE: "链接文本非模糊，描述性文本代替「点击这里」（WCAG 2.4.4/2.4.9，W316 E2-32 深化）",
    R_MULTIPLE_WAYS: "至少 2 种导航方式：导航栏 + 搜索/面包屑/站点地图（WCAG 2.4.5，W316 E2-33 深化）",
    R_NON_TEXT_CONTRAST: "UI 组件 border-color 与背景对比度 ≥ 3:1（WCAG 1.4.11，W316 E2-34 深化）",
    R_HOVER_FOCUS_CONTENT: "tooltip/popover 可关闭/可悬停/持续显示（WCAG 1.4.13，W316 E2-35 深化）",
    R_CHAR_KEY_SHORTCUTS: "单字符快捷键可关闭/重映射/仅聚焦时（WCAG 2.1.4，W316 E2-36 深化）",
    R_POINTER_GESTURES: "多点/路径手势有单点 click 替代（WCAG 2.5.1，W316 E2-37 深化）",
    R_POINTER_CANCELLATION: "onmousedown 即时触发需有 onmouseup/onclick 替代（WCAG 2.5.2，W316 E2-38 深化）",
    R_LABEL_IN_NAME: "可见标签文本包含在 aria-label 中，支持语音控制（WCAG 2.5.3，W316 E2-39 深化）",
    R_ANIMATION_INTERACTIONS: "非必要动画支持 prefers-reduced-motion 关闭（WCAG 2.3.3，W316 E2-40 深化）",
}


def _render_md(root, html_files, counts, all_findings):
    """渲染 markdown 报告"""
    lines = []
    lines.append("# 西游记项目 a11y 审查报告")
    lines.append("")
    lines.append("> 本报告由 `scripts/a11y_audit.py` 自动生成，按 40 条 WCAG 2.2 完整规范规则扫描全站 HTML。")
    lines.append("> 严重度分级：P0 阻断 / P1 严重 / P2 一般 / P3 提示。退出码 0 表示无 P0 问题。")
    lines.append("")
    lines.append("## 元信息")
    lines.append("")
    lines.append(f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- 扫描目录：`{root}`")
    lines.append(f"- 扫描文件数：{len(html_files)} 个 HTML")
    lines.append(f"- 规则数：{len(ALL_CHECKS)} 条 WCAG 2.2 AA")
    lines.append(f"- findings 总数：{len(all_findings)}")
    lines.append("")
    lines.append("## 规则说明")
    lines.append("")
    for rule_id, _ in ALL_CHECKS:
        lines.append(f"- **{rule_id} {RULE_NAMES[rule_id]}**：{RULE_DESCRIPTIONS[rule_id]}")
    lines.append("")
    lines.append("## 规则计数表（P0 / P1 / P2 / P3）")
    lines.append("")
    lines.append("| 规则 ID | 规则名称 | P0 | P1 | P2 | P3 | 合计 |")
    lines.append("|---------|----------|----|----|----|----|------|")
    for rule_id, _ in ALL_CHECKS:
        c = counts[rule_id]
        total = c["P0"] + c["P1"] + c["P2"] + c["P3"]
        lines.append(
            f"| {rule_id} | {RULE_NAMES[rule_id]} | {c['P0']} | {c['P1']} | {c['P2']} | {c['P3']} | {total} |"
        )
    totals = {s: sum(counts[r][s] for r, _ in ALL_CHECKS) for s in ("P0", "P1", "P2", "P3")}
    lines.append(
        f"| **合计** | - | **{totals['P0']}** | **{totals['P1']}** | "
        f"**{totals['P2']}** | **{totals['P3']}** | **{sum(totals.values())}** |"
    )
    lines.append("")
    # Top 5 文件问题数
    file_counts = {}
    for fd in all_findings:
        try:
            rel = str(Path(fd["file"]).relative_to(root))
        except Exception:
            rel = fd["file"]
        file_counts[rel] = file_counts.get(rel, 0) + 1
    top_files = sorted(file_counts.items(), key=lambda x: -x[1])[:5]
    if top_files:
        lines.append("## Top 5 文件问题数")
        lines.append("")
        lines.append("| 文件 | findings 数 |")
        lines.append("|------|------------|")
        for rel, n in top_files:
            lines.append(f"| `{rel}` | {n} |")
        lines.append("")
    lines.append("## Top 10 findings 详情")
    lines.append("")
    sev_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    sorted_f = sorted(all_findings, key=lambda x: (sev_order.get(x["severity"], 9), x["rule_id"]))
    for i, fd in enumerate(sorted_f[:10], 1):
        rel = fd["file"]
        try:
            rel = str(Path(rel).relative_to(root))
        except Exception:
            pass
        lines.append(f"### {i}. [{fd['severity']}] {fd['rule_id']} {fd['rule_name']}")
        lines.append(f"- 文件：`{rel}`")
        lines.append(f"- 行号：{fd['line']}")
        lines.append(f"- 描述：{fd['message']}")
        if fd["evidence"]:
            lines.append(f"- 证据：`{fd['evidence']}`")
        lines.append("")
    lines.append("## 建议修复优先级")
    lines.append("")
    lines.append("1. **P0 阻断级**：立即修复（aria-hidden 与可聚焦冲突、`<img>` 完全无 alt）")
    lines.append("2. **P1 严重**：本轮迭代内修复（role=button 缺键盘事件、对比度 < 3:1、tabindex>0、拖拽缺键盘替代、对话框焦点陷阱、按钮缺可访问名）")
    lines.append("3. **P2 一般**：下个版本修复（对比度 3–4.5:1、`<noscript>` 缺失、aria 互斥、目标尺寸 < 24px、缺 :focus-visible、帮助链接未入 landmark）")
    lines.append("4. **P3 提示**：作为优化项跟踪（`<th>` 缺 scope、`alt=\"\"` 配 `role=\"presentation\"`）")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("由 `scripts/a11y_audit.py` 生成 · W264-E2 + W271-E2 + W275-E2 + W279-E2 + W283-E2 + W316-E2 a11y 深化 · 40 条 WCAG 2.2 完整规范规则 · v2.2.68")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(
        description="a11y_audit.py - 全站可访问性审查（19 项检查覆盖 20 条 WCAG 2.2 SC）",
    )
    ap.add_argument("--dir", type=Path, default=Path("site"), help="扫描目录（默认 site）")
    ap.add_argument("--format", choices=["md", "json"], default="md", help="输出格式（默认 md）")
    ap.add_argument("--quiet", action="store_true", help="静默模式（仅退出码，不打印报告）")
    args = ap.parse_args()

    return audit_directory(args.dir, output_format=args.format, quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
