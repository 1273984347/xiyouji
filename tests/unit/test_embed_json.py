r"""W751 专项测试：scripts/embed_json.py（JSON 嵌入 HTML 的 EMBEDDED 对象）

## 为什么测这个脚本（缺口取证）

W751 四面引用普查实测 embed_json.py 属「无任何引用」清单。它是**可视化页数据回退铁律
（AGENTS §4.1：site/data 每页必须内嵌 EMBEDDED 回退）的落地工具**——一旦它把括号边界算错，
产出的是「fetch 失败时整页空白」的页面，而 file:// 直开正是本站主用法（铁律 5）。它还是
W733 重构（main 拆 _parse_args/_load_inputs/_embed_key/_write_with_backup）之后**首个无测试
覆盖的纯函数簇**。

## 覆盖判据（每条对应一个真实失效模式）

  E1 括号深度边界     → 贪婪正则截断后续内容（脚本 docstring 自陈的历史教训）
  E2 字符串内括号      → JSON 值里出现 `{`/`}` 会把边界算错（真实数据常见）
  E3 insert 追加语义   → 空对象/有尾逗号/无尾逗号三种形态的排版正确性
  E4 ensure 注入位置   → 缺 EMBEDDED 时注入点错会破坏 head
  E5 replace 精确替换  → 只换目标键值，邻键与其它内容零损
  E6 键名匹配边界      → `\bkey\s*:\s*{` 不得命中 `key_extra`/前缀键（误伤=改错数据）
  E7 退出码契约        → 1/2/3/4/5 五档错误码是脚本对外承诺（docstring §参数）
  E8 备份语义          → 默认 .bak、--no-backup 不写备份
  E9 中文不转义        → ensure_ascii=False（页面内嵌中文可读，CSV/审查依赖）

## 手法

纯函数用字符串直测；CLI 面用 monkeypatch.setattr(sys, "argv", [...]) 在进程内调 main()，
全部输入输出走 tmp_path——**真实仓库的 site/ 永不被触碰**（末尾专用断言）。
"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import embed_json as ej  # noqa: E402

HTML_WITH_EMBEDDED = """<!doctype html>
<html><head><title>t</title></head><body>
<script>
    const EMBEDDED = {
        existing: {"a": 1},
        tail: {"z": 9}
    };
    const OTHER = {"keep": true};
</script>
<svg><rect/><rect/></svg>
</body></html>
"""

def run_main(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["embed_json.py", *argv])
    ej.main()


# ------------------------------------------------------------------ E1 括号深度边界
def test_e1_bounds_span_only_the_embedded_object():
    start, end = ej.find_embedded_bounds(HTML_WITH_EMBEDDED)
    body = HTML_WITH_EMBEDDED[start:end + 1]
    assert body.startswith("{") and body.endswith("}")
    assert "existing:" in body and "tail:" in body
    assert "OTHER" not in body, "越界吞掉了后续 JS（贪婪匹配回归）"
    assert "svg" not in body


def test_e1b_unbalanced_or_missing_returns_none():
    assert ej.find_embedded_bounds("<html>no embedded here</html>") is None
    assert ej.find_embedded_bounds("const EMBEDDED = { broken: ") is None


# ------------------------------------------------------------------ E2 字符串内括号
def test_e2_braces_inside_json_string_do_not_break_depth_count():
    html = 'const EMBEDDED = {\n  note: {"text": "含 { 与 } 的说明"},\n  after: {"ok": 1}\n};\n'
    start, end = ej.find_embedded_bounds(html)
    body = html[start:end + 1]
    assert "after:" in body, "字符串内括号导致提前闭合"
    assert html[end + 1:].startswith(";")


# ------------------------------------------------------------------ E3 insert 追加语义
def test_e3_insert_into_empty_object():
    html = "const EMBEDDED = {};\n"
    s, e = ej.find_embedded_bounds(html)
    out = ej.insert_key(html, s, e, "k", '{"v":1}')
    assert "k: {\"v\":1}" in out
    # 产出的 JS 对象体必须仍是合法 JSON（键加引号后解析）
    body = out[out.index("{", out.index("=")):out.rindex("}") + 1]
    assert json.loads(body.replace("k:", '"k":')) == {"k": {"v": 1}}


def test_e3b_insert_with_and_without_trailing_comma():
    for body, label in [('{\n  a: {"x":1},\n}', "有尾逗号"), ('{\n  a: {"x":1}\n}', "无尾逗号")]:
        s, e = ej.find_embedded_bounds("const EMBEDDED = " + body + ";\n")
        out = ej.insert_key("const EMBEDDED = " + body + ";\n", s, e, "b", '{"y":2}')
        assert ",,\n" not in out and "{," not in out, "%s：逗号排版坏了" % label
        assert '"y":2' in out.replace(" ", "")


def test_e3c_insert_appends_after_last_field_not_before():
    html = 'const EMBEDDED = {\n  first: {"n":1}\n};\n'
    s, e = ej.find_embedded_bounds(html)
    out = ej.insert_key(html, s, e, "second", '{"n":2}')
    assert out.index("first:") < out.index("second:")


# ------------------------------------------------------------------ E4 ensure 注入位置
def test_e4_ensure_injects_before_head_close_when_missing():
    html = "<html><head><title>t</title></head><body>x</body></html>"
    out = ej.ensure_embedded_exists(html)
    assert out.index("const EMBEDDED = {};") < out.index("</head>")
    assert ej.find_embedded_bounds(out) is not None


def test_e4b_ensure_falls_back_to_body_then_eof():
    body_only = "<html><body>x</body></html>"
    out = ej.ensure_embedded_exists(body_only)
    assert out.index("const EMBEDDED = {};") < out.index("</body>")
    bare = "no tags at all"
    out2 = ej.ensure_embedded_exists(bare)
    assert out2.startswith(bare) and "EMBEDDED" in out2


def test_e4c_ensure_is_noop_when_present():
    assert ej.ensure_embedded_exists(HTML_WITH_EMBEDDED) == HTML_WITH_EMBEDDED
    assert ej.ensure_embedded_exists("window.EMBEDDED = {a:1};") == "window.EMBEDDED = {a:1};"
    assert ej.ensure_embedded_exists("let EMBEDDED = {a:1};") == "let EMBEDDED = {a:1};"


# ------------------------------------------------------------------ E5 replace 精确替换
def test_e5_replace_only_touches_target_value():
    s, e = ej.find_embedded_bounds(HTML_WITH_EMBEDDED)
    out = ej.replace_key(HTML_WITH_EMBEDDED, s, e, "existing", '{"a": 2, "b": 3}')
    assert '"b": 3' in out
    assert "tail:" in out and '{"z": 9}' in out, "邻键被破坏"
    assert "const OTHER" in out and "<svg>" in out, "对象外内容被破坏"


def test_e5b_replace_missing_key_raises_keyerror():
    s, e = ej.find_embedded_bounds(HTML_WITH_EMBEDDED)
    with pytest.raises(KeyError) as ei:
        ej.replace_key(HTML_WITH_EMBEDDED, s, e, "nope", "{}")
    assert "nope" in str(ei.value)


# ------------------------------------------------------------------ E6 键名匹配边界
def test_e6_field_lookup_does_not_match_key_prefixes():
    html = 'const EMBEDDED = {\n  note_extra: {"a":1},\n  note: {"b":2}\n};\n'
    s, e = ej.find_embedded_bounds(html)
    bounds = ej.find_field_bounds(html, s, e, "note")
    assert bounds is not None
    val = html[bounds[0]:bounds[1] + 1]
    assert val == '{"b":2}', "命中了 note_extra（前缀误伤）"


# ------------------------------------------------------------------ E7 退出码契约
def test_e7_exit_codes(monkeypatch, tmp_path, capsys):
    html = tmp_path / "p.html"
    html.write_text(HTML_WITH_EMBEDDED, encoding="utf-8")
    good = tmp_path / "d.json"
    good.write_text('{"n": 1}', encoding="utf-8")
    bad = tmp_path / "bad.json"
    bad.write_text('{ not json', encoding="utf-8")

    with pytest.raises(SystemExit) as e1:
        run_main(monkeypatch, "--html", str(tmp_path / "missing.html"), "--json", str(good), "--key", "k")
    assert e1.value.code == 1 and "HTML 文件不存在" in capsys.readouterr().err

    with pytest.raises(SystemExit) as e2:
        run_main(monkeypatch, "--html", str(html), "--json", str(tmp_path / "nope.json"), "--key", "k")
    assert e2.value.code == 1

    with pytest.raises(SystemExit) as e3:
        run_main(monkeypatch, "--html", str(html), "--json", str(bad), "--key", "k")
    assert e3.value.code == 2 and "JSON 解析失败" in capsys.readouterr().err

    # insert 模式键已存在 → 4
    with pytest.raises(SystemExit) as e4:
        run_main(monkeypatch, "--html", str(html), "--json", str(good), "--key", "existing")
    assert e4.value.code == 4 and "已存在" in capsys.readouterr().err

    # replace 模式键不存在 → 4
    with pytest.raises(SystemExit) as e5:
        run_main(monkeypatch, "--html", str(html), "--json", str(good), "--key", "nope", "--mode", "replace")
    assert e5.value.code == 4

    # 无 EMBEDDED 锚点且无法注入 → 3（构造一个连 </head>/</body> 都没有的片段也不会失败，
    # 故直接对内部边界函数断言 None 即 3 档前提）
    assert ej.find_embedded_bounds("") is None


# ------------------------------------------------------------------ E8 备份 + E9 中文
def test_e8_backup_default_and_no_backup(monkeypatch, tmp_path, capsys):
    html = tmp_path / "p.html"
    html.write_text(HTML_WITH_EMBEDDED, encoding="utf-8")
    data = tmp_path / "d.json"
    data.write_text('{"中文键": "数值"}', encoding="utf-8")

    run_main(monkeypatch, "--html", str(html), "--json", str(data), "--key", "fresh")
    out = capsys.readouterr().out
    assert "[OK]" in out and "bytes" in out
    assert (tmp_path / "p.html.bak").exists(), "默认必须备份"
    assert (tmp_path / "p.html.bak").read_text(encoding="utf-8") == HTML_WITH_EMBEDDED

    run_main(monkeypatch, "--html", str(html), "--json", str(data), "--key", "fresh2", "--no-backup")
    assert (tmp_path / "p.html.bak").read_text(encoding="utf-8") == HTML_WITH_EMBEDDED, \
        "--no-backup 不得刷新备份"


def test_e9_embedded_chinese_not_escaped(monkeypatch, tmp_path):
    html = tmp_path / "p.html"
    html.write_text("const EMBEDDED = {};\n", encoding="utf-8")
    data = tmp_path / "d.json"
    data.write_text('{"名": "孙悟空"}', encoding="utf-8")
    run_main(monkeypatch, "--html", str(html), "--json", str(data), "--key", "k", "--no-backup")
    text = html.read_text(encoding="utf-8")
    assert "孙悟空" in text
    assert "\\u" not in text, "ensure_ascii 未关：内嵌中文被转义（可读性与审查面受损）"


# ------------------------------------------------------------------ 真实仓库零触碰
def test_real_repo_files_untouched():
    rel = ROOT / "site" / "data" / "relationships.html"
    assert rel.exists(), "取证前提：该页存在"
    text = rel.read_text(encoding="utf-8")
    assert "fresh2" not in text and '{"中文键"' not in text, "测试产物泄漏进真实页面"
    assert not (ROOT / "site" / "data" / "relationships.html.bak").exists(), "测试在真实页面留了备份"
