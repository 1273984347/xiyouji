"""fix_svg_negative_widths.py 单元测试

覆盖四个核心函数：
- skip_width_arg：判断是否应跳过包裹
- wrap_width_arg：包裹参数为 Math.max(0, ...)
- process_attr_widths：解析 .attr("width", <value>) 调用
- process_radius：包裹 Math.min(W, H) / 2 - N
- process_clientwidth：为 clientWidth fallback 增加最小宽度保护
- margin_defined_before：检查变量是否在指定位置前定义

工具来源：scripts/fix_svg_negative_widths.py
"""
import pytest

from fix_svg_negative_widths import (
    skip_width_arg,
    wrap_width_arg,
    process_attr_widths,
    process_radius,
    process_clientwidth,
    margin_defined_before,
)


# ---------------- skip_width_arg ----------------

class TestSkipWidthArg:
    def test_empty_string_skipped(self):
        assert skip_width_arg("") is True
        assert skip_width_arg("   ") is True

    def test_string_literal_skipped(self):
        """单/双/反引号字符串字面量应被跳过。"""
        assert skip_width_arg("'100px'") is True
        assert skip_width_arg('"100px"') is True
        assert skip_width_arg("`100px`") is True

    def test_numeric_literal_skipped(self):
        """纯数字应被跳过。"""
        assert skip_width_arg("100") is True
        assert skip_width_arg("0") is True

    def test_negative_numeric_literal_skipped(self):
        """负数字面量应被跳过。"""
        assert skip_width_arg("-100") is True
        assert skip_width_arg("-50") is True

    def test_already_protected_skipped(self):
        """已包裹 Math.max(0, ...) 应被跳过。"""
        assert skip_width_arg("Math.max(0, width)") is True
        assert skip_width_arg("Math.max(0, w - 10)") is True

    def test_function_expression_skipped(self):
        """function 表达式应被跳过（无法安全整体包裹）。"""
        assert skip_width_arg("function(d) { return d.w; }") is True

    def test_variable_not_skipped(self):
        """变量名不应被跳过。"""
        assert skip_width_arg("width") is False
        assert skip_width_arg("w") is False

    def test_expression_not_skipped(self):
        """表达式不应被跳过。"""
        assert skip_width_arg("w - margin.left - margin.right") is False
        assert skip_width_arg("x + 10") is False

    def test_negative_with_non_digit_not_skipped(self):
        """负号后非数字应不被跳过（如 -x）。"""
        # -x 不是纯数字字面量
        assert skip_width_arg("-x") is False


# ---------------- wrap_width_arg ----------------

class TestWrapWidthArg:
    def test_variable_wrapped(self):
        """变量应被包裹为 Math.max(0, var)。"""
        assert wrap_width_arg("width") == "Math.max(0, width)"

    def test_expression_wrapped(self):
        """表达式应被包裹。"""
        assert wrap_width_arg("w - 10") == "Math.max(0, w - 10)"

    def test_string_literal_not_wrapped(self):
        """字符串字面量应原样返回。"""
        assert wrap_width_arg("'100px'") == "'100px'"
        assert wrap_width_arg('"100"') == '"100"'

    def test_numeric_not_wrapped(self):
        """数字应原样返回。"""
        assert wrap_width_arg("100") == "100"
        assert wrap_width_arg("-50") == "-50"

    def test_already_protected_not_wrapped(self):
        """已包裹的应原样返回。"""
        assert wrap_width_arg("Math.max(0, w)") == "Math.max(0, w)"

    def test_function_not_wrapped(self):
        """function 表达式应原样返回。"""
        s = "function(d) { return d.w; }"
        assert wrap_width_arg(s) == s

    def test_arrow_function_body_wrapped(self):
        """箭头函数：Math.max(0, ...) 应加在函数体上。"""
        result = wrap_width_arg("d => d.w")
        assert result.startswith("d => ")
        assert "Math.max(0, d.w)" in result

    def test_arrow_function_already_protected_not_wrapped(self):
        """已保护的箭头函数应原样返回。"""
        s = "d => Math.max(0, d.w)"
        assert wrap_width_arg(s) == s

    def test_whitespace_stripped_before_wrap(self):
        """参数前后空白应被 strip。"""
        assert wrap_width_arg("  width  ") == "Math.max(0, width)"

    def test_empty_arg_returns_empty_string(self):
        """空参数（含纯空白）经 strip 后应返回空字符串。"""
        # wrap_width_arg 内部会 arg.strip()，纯空白 → "" → skip_width_arg → 返回 ""
        assert wrap_width_arg("") == ""
        assert wrap_width_arg("   ") == ""


# ---------------- process_attr_widths ----------------

class TestProcessAttrWidths:
    def test_no_attr_width_returns_unchanged(self):
        """无 .attr("width", ...) 调用应原样返回。"""
        s = "var x = 1;\nconsole.log('hello');"
        assert process_attr_widths(s) == s

    def test_attr_width_with_variable_wrapped(self):
        """变量参数应被包裹（注意：参数原前导空白会被 strip 掉）。"""
        s = '.attr("width", w)'
        result = process_attr_widths(s)
        assert "Math.max(0, w)" in result
        # arg_content " w" 被 strip 成 "w" 后包裹，因此逗号后无空格
        assert result == '.attr("width",Math.max(0, w))'

    def test_attr_width_with_expression_wrapped(self):
        """表达式参数应被包裹。"""
        s = '.attr("width", w - 10)'
        result = process_attr_widths(s)
        assert "Math.max(0, w - 10)" in result

    def test_attr_width_with_numeric_not_wrapped(self):
        """数字参数不应被包裹（arg_content 经 strip 后原样返回）。"""
        s = '.attr("width", 100)'
        result = process_attr_widths(s)
        # arg_content " 100" strip 成 "100"，原样返回（skip_width_arg 命中数字字面量）
        assert result == '.attr("width",100)'

    def test_attr_width_with_string_not_wrapped(self):
        """字符串参数不应被包裹。"""
        s = '.attr("width", "100px")'
        result = process_attr_widths(s)
        assert result == '.attr("width","100px")'

    def test_attr_width_with_already_protected_not_double_wrapped(self):
        """已包裹的参数不应被二次包裹。"""
        s = '.attr("width", Math.max(0, w))'
        result = process_attr_widths(s)
        # arg_content " Math.max(0, w)" strip 后 skip_width_arg 命中（已保护）
        assert result == '.attr("width",Math.max(0, w))'
        # 确保没有 Math.max(0, Math.max(0, w))
        assert "Math.max(0, Math.max(0," not in result

    def test_attr_width_with_arrow_function_wrapped_body(self):
        """箭头函数：包裹应加在函数体上。"""
        s = '.attr("width", d => d.w)'
        result = process_attr_widths(s)
        assert "d => Math.max(0, d.w)" in result

    def test_attr_width_with_nested_parens(self):
        """含嵌套括号的表达式应正确解析闭合。"""
        s = '.attr("width", Math.min(w, 100))'
        result = process_attr_widths(s)
        assert "Math.max(0, Math.min(w, 100))" in result

    def test_multiple_attr_width_calls(self):
        """多个 .attr("width", ...) 调用都应被处理。"""
        s = '.attr("width", w1).attr("width", w2)'
        result = process_attr_widths(s)
        assert "Math.max(0, w1)" in result
        assert "Math.max(0, w2)" in result

    def test_attr_height_not_affected(self):
        """ .attr("height", ...) 不应被处理。"""
        s = '.attr("height", h)'
        result = process_attr_widths(s)
        assert result == s
        assert "Math.max(0," not in result

    def test_unclosed_attr_preserves_rest(self):
        """未闭合的 .attr("width", ... 应保留剩余内容。"""
        s = '.attr("width", w'
        result = process_attr_widths(s)
        # 应不丢失内容（即使语法不完整）
        assert "w" in result


# ---------------- process_radius ----------------

class TestProcessRadius:
    def test_radius_pattern_wrapped(self):
        """Math.min(W, H) / 2 - N 应被包裹。"""
        s = "var r = Math.min(width, height) / 2 - 10;"
        result = process_radius(s)
        assert "Math.max(0, Math.min(width, height) / 2 - 10)" in result

    def test_radius_with_spaces(self):
        """含空格的 radius 表达式也应被匹配。"""
        s = "Math.min( w , h ) / 2 - 5"
        result = process_radius(s)
        assert "Math.max(0," in result

    def test_radius_already_protected_not_double_wrapped(self):
        """已包裹的 radius 不应被二次包裹。"""
        s = "Math.max(0, Math.min(width, height) / 2 - 10)"
        result = process_radius(s)
        # 不应出现 Math.max(0, Math.max(0, ...
        assert "Math.max(0, Math.max(0," not in result

    def test_radius_no_match_returns_unchanged(self):
        """无 radius 模式应原样返回。"""
        s = "var x = 1;"
        assert process_radius(s) == s

    def test_radius_multiple_matches(self):
        """多个 radius 模式都应被处理。"""
        s = (
            "Math.min(w1, h1) / 2 - 5;\n"
            "Math.min(w2, h2) / 2 - 10;"
        )
        result = process_radius(s)
        # 应有 2 个 Math.max(0, Math.min(...))
        count = result.count("Math.max(0, Math.min(")
        assert count == 2


# ---------------- margin_defined_before ----------------

class TestMarginDefinedBefore:
    def test_const_margin_defined_before(self):
        """const MARGIN = {...} 在 pos 之前定义应返回 True。"""
        text = "const MARGIN = {top: 20, right: 20};\nvar x = 1;"
        # pos 在 var x 之后
        pos = text.index("var x")
        assert margin_defined_before(text, pos, "MARGIN") is True

    def test_let_margin_defined_before(self):
        """let MARGIN = {...} 也应被识别。"""
        text = "let MARGIN = {top: 20};\nvar y = 2;"
        pos = text.index("var y")
        assert margin_defined_before(text, pos, "MARGIN") is True

    def test_var_margin_defined_before(self):
        """var MARGIN = {...} 也应被识别。"""
        text = "var MARGIN = {top: 20};\nvar y = 2;"
        pos = text.index("var y")
        assert margin_defined_before(text, pos, "MARGIN") is True

    def test_margin_not_defined_returns_false(self):
        """MARGIN 未定义应返回 False。"""
        text = "var x = 1;"
        assert margin_defined_before(text, 5, "MARGIN") is False

    def test_margin_defined_after_pos_returns_false(self):
        """MARGIN 在 pos 之后定义应返回 False。"""
        text = "var x = 1;\nconst MARGIN = {top: 20};"
        pos = text.index("var x")
        assert margin_defined_before(text, pos, "MARGIN") is False

    def test_margin_assigned_without_const_not_recognized(self):
        """MARGIN = {...} 无 const/let/var 前缀不应被识别。"""
        text = "MARGIN = {top: 20};\nvar x = 1;"
        pos = text.index("var x")
        assert margin_defined_before(text, pos, "MARGIN") is False


# ---------------- process_clientwidth ----------------

class TestProcessClientWidth:
    def test_no_clientwidth_returns_unchanged(self):
        """无 clientWidth 模式应原样返回。"""
        s = "var x = 1;"
        new_text, patched = process_clientwidth(s)
        assert new_text == s
        assert patched == []

    def test_already_protected_not_patched(self):
        """已被 Math.max(var, ...) 保护的应跳过。"""
        s = (
            "const w = container.clientWidth || 800;\n"
            "const inner = Math.max(w, 200);"
        )
        new_text, patched = process_clientwidth(s)
        assert patched == []
        assert new_text == s

    def test_default_min_width_protection(self):
        """无 margin 模式时应使用默认 200px 最小宽度保护。"""
        s = "const w = container.clientWidth || 800;"
        new_text, patched = process_clientwidth(s)
        assert len(patched) == 1
        var, obj, kind = patched[0]
        assert var == "w"
        assert obj == "container"
        assert kind == "default"
        assert "Math.max(200, container.clientWidth || 800)" in new_text

    def test_let_keyword_supported(self):
        """let 关键字也应被支持。"""
        s = "let w = el.clientWidth || 600;"
        new_text, patched = process_clientwidth(s)
        assert len(patched) == 1
        assert patched[0][0] == "w"
        assert patched[0][1] == "el"
        assert patched[0][2] == "default"

    def test_margin_aware_protection_when_margin_defined_before(self):
        """当后续出现 VAR - MARGIN.left - MARGIN.right 且 MARGIN 已定义时应使用 margin-aware 模式。"""
        s = (
            "const MARGIN = {left: 30, right: 30};\n"
            "const w = container.clientWidth || 800;\n"
            "const inner = w - MARGIN.left - MARGIN.right;"
        )
        new_text, patched = process_clientwidth(s)
        assert len(patched) == 1
        var, obj, kind = patched[0]
        assert var == "w"
        assert kind == "margin-aware"
        assert "MARGIN.left + MARGIN.right + 40" in new_text

    def test_margin_not_defined_skips_margin_aware(self):
        """当 MARGIN 未在赋值前定义时应退回默认模式。"""
        s = (
            "const w = container.clientWidth || 800;\n"
            "const inner = w - MARGIN.left - MARGIN.right;"
        )
        new_text, patched = process_clientwidth(s)
        # MARGIN 在 pos 之前未定义 → 退回 default
        assert len(patched) == 1
        assert patched[0][2] == "default"

    def test_multiple_clientwidth_assignments(self):
        """多个 clientWidth 赋值都应被处理。"""
        s = (
            "const w1 = a.clientWidth || 100;\n"
            "const w2 = b.clientWidth || 200;"
        )
        new_text, patched = process_clientwidth(s)
        assert len(patched) == 2
        vars_patched = [p[0] for p in patched]
        assert "w1" in vars_patched
        assert "w2" in vars_patched

    def test_already_math_max_wrapped_not_patched(self):
        """已被 Math.max( 包裹的赋值不应被处理。"""
        s = "const w = Math.max(container.clientWidth || 800, 200);"
        new_text, patched = process_clientwidth(s)
        # lookbehind 跳过 Math.max( 前缀
        assert patched == []

    def test_already_math_min_wrapped_not_patched(self):
        """已被 Math.min( 包裹的赋值不应被处理。"""
        s = "const w = Math.min(container.clientWidth || 800, 1000);"
        new_text, patched = process_clientwidth(s)
        assert patched == []
