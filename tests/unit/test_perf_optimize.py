# -*- coding: utf-8 -*-
"""W265 E3 性能深化·perf_optimize.py 单元测试·pytest 风格

覆盖 6 个核心模块：
  - test_optimize_lcp            验证图片懒加载 + 资源预加载生成
  - test_convert_svg_to_canvas  验证阈值切换逻辑
  - test_inline_critical_css     验证关键 CSS 内联
  - test_add_defer_async         验证 defer/async 添加
  - test_minify_resources        验证资源压缩
  - test_generate_report         验证报告生成

运行：pytest tests/unit/test_perf_optimize.py -v
"""
import sys
from pathlib import Path

import pytest

# 将 scripts/ 加入 sys.path（与项目其他测试保持一致）
SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import perf_optimize  # noqa: E402


# ---------------------------------------------------------------------------
# 公共 fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_html_dir(tmp_path: Path):
    """生成包含若干 HTML 文件的临时目录"""
    html_a = tmp_path / "a.html"
    html_a.write_text(
        '<!DOCTYPE html><html><head><title>A</title></head>'
        '<body>'
        '<img src="hero.png" alt="主视觉" class="hero">'
        '<img src="b1.png" alt="b1">'
        '<img src="b2.png" alt="b2" loading="lazy">'
        '<script src="app.js"></script>'
        '<script src="echarts.min.js"></script>'
        '</body></html>',
        encoding="utf-8",
    )
    html_b = tmp_path / "b.html"
    html_b.write_text(
        '<!DOCTYPE html><html><head><title>B</title>'
        '<link rel="stylesheet" href="b.css"></head>'
        '<body><img src="cover.png" alt="封面">'
        '<script src="vendor.js" async></script>'
        '</body></html>',
        encoding="utf-8",
    )
    css_file = tmp_path / "b.css"
    css_file.write_text(
        "/* comment */\nbody { color: #222; }\n",
        encoding="utf-8",
    )
    return tmp_path


# ---------------------------------------------------------------------------
# test_optimize_lcp
# ---------------------------------------------------------------------------

def test_optimize_lcp(tmp_html_dir: Path):
    """验证懒加载自动添加 + 预加载生成 + 字体 preload"""
    stats = perf_optimize.optimize_lcp(tmp_html_dir)

    assert "error" not in stats
    assert stats["files_modified"] >= 1
    # 非首屏图应被加 loading="lazy"
    a_html = (tmp_html_dir / "a.html").read_text(encoding="utf-8")
    # b1.png 原本无 loading，应被添加
    assert 'src="b1.png"' in a_html and 'loading="lazy"' in a_html
    # 首屏 hero 不应被加 lazy
    assert 'src="hero.png" alt="主视觉" class="hero"' in a_html
    # 字体 preload 应至少在 1 个文件中注入
    assert stats["font_preload_added"] >= 1
    assert "preload" in a_html or "preload" in (tmp_html_dir / "b.html").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# test_convert_svg_to_canvas
# ---------------------------------------------------------------------------

def test_convert_svg_to_canvas_below_threshold(tmp_path: Path):
    """SVG 节点数低于阈值时不应切换"""
    hp = tmp_path / "small.html"
    hp.write_text(
        '<svg><circle r="5"/><rect width="10" height="10"/></svg>',
        encoding="utf-8",
    )
    result = perf_optimize.convert_svg_to_canvas(hp, threshold=1000)
    assert result["svg_node_count"] == 2
    assert result["switched"] is False
    assert result["script_injected"] is False


def test_convert_svg_to_canvas_above_threshold(tmp_path: Path):
    """SVG 节点数 ≥ 阈值时应注入 Canvas 桥接脚本"""
    hp = tmp_path / "large.html"
    # 生成 1200 个 circle 节点（>1000）
    nodes = "".join('<circle r="1"/>' for _ in range(1200))
    hp.write_text(f'<svg>{nodes}</svg>', encoding="utf-8")
    result = perf_optimize.convert_svg_to_canvas(hp, threshold=1000)
    assert result["svg_node_count"] == 1200
    assert result["threshold"] == 1000
    assert result["switched"] is True
    assert result["script_injected"] is True
    # 文件中应包含桥接脚本标记
    text = hp.read_text(encoding="utf-8")
    assert 'data-perf-canvas-bridge' in text


def test_convert_svg_to_canvas_custom_threshold(tmp_path: Path):
    """自定义阈值切换验证"""
    hp = tmp_path / "mid.html"
    hp.write_text('<svg><circle/><rect/></svg>', encoding="utf-8")
    result = perf_optimize.convert_svg_to_canvas(hp, threshold=2)
    assert result["svg_node_count"] == 2
    assert result["threshold"] == 2
    assert result["switched"] is True


def test_convert_svg_to_canvas_missing_file(tmp_path: Path):
    """文件不存在时返回 error"""
    result = perf_optimize.convert_svg_to_canvas(tmp_path / "nope.html")
    assert "error" in result
    assert result["switched"] is False


# ---------------------------------------------------------------------------
# test_inline_critical_css
# ---------------------------------------------------------------------------

def test_inline_critical_css_with_external(tmp_path: Path):
    """有外部 stylesheet 时从该文件提取首屏 CSS"""
    hp = tmp_path / "page.html"
    css = tmp_path / "style.css"
    css.write_text("body{margin:0;color:#222}a{color:#0070f3}", encoding="utf-8")
    hp.write_text(
        '<!DOCTYPE html><html><head>'
        '<link rel="stylesheet" href="style.css">'
        '</head><body><p>hi</p></body></html>',
        encoding="utf-8",
    )
    result = perf_optimize.inline_critical_css(hp)
    assert result["file"] == str(hp)
    assert result["inlined_bytes"] > 0
    text = hp.read_text(encoding="utf-8")
    assert "data-critical-inline" in text
    assert "color:#222" in text or "color: #222" in text


def test_inline_critical_css_fallback(tmp_path: Path):
    """无外部 CSS 时使用 fallback 临界 CSS"""
    hp = tmp_path / "bare.html"
    hp.write_text(
        '<!DOCTYPE html><html><head><title>T</title></head>'
        '<body><p>hi</p></body></html>',
        encoding="utf-8",
    )
    result = perf_optimize.inline_critical_css(hp)
    assert result["fallback_used"] is True
    text = hp.read_text(encoding="utf-8")
    assert "data-critical-inline" in text
    assert "--c-bg" in text  # fallback CSS 含 CSS 变量


def test_inline_critical_css_already_inlined(tmp_path: Path):
    """已含 critical-inline 标记的文件应跳过"""
    hp = tmp_path / "done.html"
    hp.write_text(
        '<head><style data-critical-inline="1">x{}</style></head>',
        encoding="utf-8",
    )
    result = perf_optimize.inline_critical_css(hp)
    assert result["inlined_bytes"] == 0


# ---------------------------------------------------------------------------
# test_add_defer_async
# ---------------------------------------------------------------------------

def test_add_defer_async(tmp_html_dir: Path):
    """验证 defer 自动添加 + echarts 动态 import 建议"""
    stats = perf_optimize.add_defer_async(tmp_html_dir)

    assert "error" not in stats
    assert stats["files_modified"] >= 1
    a_html = (tmp_html_dir / "a.html").read_text(encoding="utf-8")
    # app.js 原本无 defer，应被添加
    assert 'src="app.js" defer>' in a_html
    # echarts.min.js 命中跳过清单（含 echarts 关键字）→ 不加 defer
    assert 'src="echarts.min.js" defer>' not in a_html
    # echarts 应触发动态 import 建议
    assert stats["dynamic_import_suggested"] >= 1
    # b.html 中 vendor.js 已含 async，不应再加 defer
    b_html = (tmp_html_dir / "b.html").read_text(encoding="utf-8")
    assert 'src="vendor.js" async>' in b_html
    assert 'src="vendor.js" async defer>' not in b_html


def test_add_defer_async_missing_dir():
    """目录不存在时返回 error"""
    stats = perf_optimize.add_defer_async(Path("does/not/exist"))
    assert "error" in stats


# ---------------------------------------------------------------------------
# test_minify_resources
# ---------------------------------------------------------------------------

def test_minify_resources(tmp_path: Path):
    """验证 HTML/CSS/JS minify + .gz 生成"""
    hp = tmp_path / "p.html"
    hp.write_text(
        '<!-- comment -->\n<html>\n  <head>\n    <title>T</title>\n  </head>\n'
        '  <body>\n    <p>hi</p>\n  </body>\n</html>',
        encoding="utf-8",
    )
    css = tmp_path / "p.css"
    css.write_text("/* c */\nbody {\n  color: #222;\n}\n", encoding="utf-8")
    js = tmp_path / "p.js"
    js.write_text("// comment\nvar x = 1;\n\n\n\nvar y = 2;\n", encoding="utf-8")

    stats = perf_optimize.minify_resources(tmp_path)

    assert stats["html_minified"] >= 1
    assert stats["css_minified"] >= 1
    assert stats["js_minified"] >= 1
    assert stats["gz_generated"] >= 1
    assert stats["bytes_saved"] > 0

    # 验证 .gz 文件已生成
    assert (tmp_path / "p.html.gz").exists()
    assert (tmp_path / "p.css.gz").exists()
    assert (tmp_path / "p.js.gz").exists()

    # 验证 minify 后内容（HTML 注释被移除）
    html_text = hp.read_text(encoding="utf-8")
    assert "<!-- comment -->" not in html_text


def test_minify_resources_missing_dir():
    """目录不存在时返回 error"""
    stats = perf_optimize.minify_resources(Path("does/not/exist"))
    assert "error" in stats


# ---------------------------------------------------------------------------
# test_generate_report
# ---------------------------------------------------------------------------

def test_generate_report(tmp_path: Path):
    """验证报告生成 markdown + 落盘"""
    out = tmp_path / "report.md"
    report = perf_optimize.generate_report(
        stats_lcp={"lazy_added": 5, "preload_generated": 2,
                   "font_preload_added": 1, "files_modified": 3},
        stats_canvas={"switched": True, "svg_node_count": 1200,
                      "threshold": 1000, "script_injected": True},
        stats_inline={"inlined_bytes": 2048, "fallback_used": False},
        stats_defer={"defer_added": 4, "dynamic_import_suggested": 1,
                     "files_modified": 2},
        stats_minify={"html_minified": 3, "css_minified": 2,
                      "js_minified": 1, "gz_generated": 6,
                      "bytes_saved": 10240},
        output_path=out,
    )

    assert "W265" in report
    assert "v2.2.47" in report
    assert "LCP" in report
    assert "Canvas" in report
    assert "Critical CSS" in report or "关键 CSS" in report
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "lazy_added: 5" in text
    assert "svg_node_count: 1200" in text
    assert "bytes_saved: 10240" in text


def test_generate_report_default_path(tmp_path: Path, monkeypatch):
    """默认输出路径（scripts/output/perf-optimization-report.md）"""
    fake_out = tmp_path / "perf-optimization-report.md"
    monkeypatch.setattr(perf_optimize, "DEFAULT_OUTPUT", fake_out)
    report = perf_optimize.generate_report()
    assert fake_out.exists()
    assert "W265" in report
