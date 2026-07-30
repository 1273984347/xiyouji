#!/usr/bin/env python3
"""a11y_audit.py - 全站可访问性审查脚本
W234-E2 a11y 深化·5 条 WCAG 2.1 AA 规则

扫描 site/ 下所有 HTML 文件，按 5 条规则审查可访问性问题：
  E2-1 键盘导航规则（tabindex/focus 陷阱/accesskey 冲突）
  E2-2 色彩对比度规则（WCAG 2.1 AA：正常文本 4.5:1，大文本 3:1）
  E2-3 ARIA 标签规则（role 完整性/aria 互斥/aria-hidden 冲突）
  E2-4 焦点指示规则（outline:none 无替代/交互元素无 :focus）
  E2-5 屏幕阅读器规则（img alt/input label/th scope/noscript）

用法：
    py scripts/a11y_audit.py --dir site --quiet
    py scripts/a11y_audit.py --dir site/data --format json
    py scripts/a11y_audit.py --dir site            # 默认输出 markdown 报告

退出码：0 if P0=0, 1 if P0>0
默认 markdown 报告写入 scripts/output/a11y-report.md
仅依赖 stdlib：argparse/re/json/pathlib/html.parser/datetime
"""
import argparse
import re
import json
import sys
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime


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

RULE_NAMES = {
    R_KEYBOARD: "键盘导航规则",
    R_CONTRAST: "色彩对比度规则",
    R_ARIA: "ARIA 标签规则",
    R_FOCUS: "焦点指示规则",
    R_SCREEN_READER: "屏幕阅读器规则",
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
    """收集元素、<style> 块、button 内文本"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.style_blocks = []  # list[(start_line, css_text)]
        self._in_style = False
        self._style_buf = []
        self._style_start = 0
        self._button_stack = []

    def handle_starttag(self, tag, attrs):
        line, _ = self.getpos()
        self.elements.append(A11yElement(tag, attrs, line))
        if tag.lower() == "style":
            self._in_style = True
            self._style_buf = []
            self._style_start = line
        if tag.lower() == "button":
            self._button_stack.append(len(self.elements) - 1)

    def handle_startendtag(self, tag, attrs):
        # 自闭合标签（如 <img/>）
        line, _ = self.getpos()
        self.elements.append(A11yElement(tag, attrs, line))

    def handle_endtag(self, tag):
        if tag.lower() == "style" and self._in_style:
            self.style_blocks.append((self._style_start, "".join(self._style_buf)))
            self._in_style = False
            self._style_buf = []
        if tag.lower() == "button" and self._button_stack:
            self._button_stack.pop()

    def handle_data(self, data):
        if self._in_style:
            self._style_buf.append(data)
        if self._button_stack:
            self.elements[self._button_stack[-1]].text += data.strip()


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


# ---------- 规则 1：键盘导航 ----------
def check_keyboard_navigation(html_content, file_path):
    """E2-1：tabindex>0、focus 陷阱、accesskey 冲突"""
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
    """E2-3：role 完整性、aria 互斥、aria-hidden 冲突、role=img/button 检查"""
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


# ---------- 主流程 ----------
ALL_CHECKS = [
    (R_KEYBOARD, check_keyboard_navigation),
    (R_CONTRAST, check_color_contrast),
    (R_ARIA, check_aria_labels),
    (R_FOCUS, check_focus_indicator),
    (R_SCREEN_READER, check_screen_reader),
]


def audit_file(file_path):
    """对单个 HTML 文件运行 5 检查，返回 findings 列表"""
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
    """扫描目录下所有 HTML，运行 5 检查，输出报告"""
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
    R_KEYBOARD: "检测 tabindex>0、onfocus/onblur 内 alert 陷阱、accesskey 冲突",
    R_CONTRAST: "WCAG 2.1 AA 对比度（正常文本 4.5:1，大文本 3:1），解析内联+style 块",
    R_ARIA: "role 完整性、aria-label/labelledby 互斥、aria-hidden 与 focusable 冲突",
    R_FOCUS: "outline:none 无 :focus-visible 替代、交互元素无 :focus 样式",
    R_SCREEN_READER: "img alt、input label、th scope、noscript 完整性",
}


def _render_md(root, html_files, counts, all_findings):
    """渲染 markdown 报告"""
    lines = []
    lines.append("# 西游记项目 a11y 审查报告")
    lines.append("")
    lines.append("> 本报告由 `scripts/a11y_audit.py` 自动生成，按 5 条 WCAG 2.1 AA 规则扫描全站 HTML。")
    lines.append("> 严重度分级：P0 阻断 / P1 严重 / P2 一般 / P3 提示。退出码 0 表示无 P0 问题。")
    lines.append("")
    lines.append("## 元信息")
    lines.append("")
    lines.append(f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- 扫描目录：`{root}`")
    lines.append(f"- 扫描文件数：{len(html_files)} 个 HTML")
    lines.append(f"- 规则数：{len(ALL_CHECKS)} 条 WCAG 2.1 AA")
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
    lines.append("2. **P1 严重**：本轮迭代内修复（role=button 缺键盘事件、对比度 < 3:1、tabindex>0）")
    lines.append("3. **P2 一般**：下个版本修复（对比度 3–4.5:1、`<noscript>` 缺失、aria 互斥）")
    lines.append("4. **P3 提示**：作为优化项跟踪（`<th>` 缺 scope、`alt=\"\"` 配 `role=\"presentation\"`）")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("由 `scripts/a11y_audit.py` 生成 · W234-E2 a11y 深化 · 5 条 WCAG 2.1 AA 规则")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(
        description="a11y_audit.py - 全站可访问性审查（5 条 WCAG 2.1 AA 规则）",
    )
    ap.add_argument("--dir", type=Path, default=Path("site"), help="扫描目录（默认 site）")
    ap.add_argument("--format", choices=["md", "json"], default="md", help="输出格式（默认 md）")
    ap.add_argument("--quiet", action="store_true", help="静默模式（仅退出码，不打印报告）")
    args = ap.parse_args()

    return audit_directory(args.dir, output_format=args.format, quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
