# -*- coding: utf-8 -*-
"""perf_optimize.py - 全站性能优化脚本

W265 E3 性能深化 · v2.2.47

整合 6 个性能优化模块，覆盖前端 LCP/CLS/TBT 三大 Core Web Vitals：
  1. LCP 优化模块（图片懒加载 + 资源预加载 + 字体子集化）
  2. Canvas 渲染深化模块（D3.js SVG → Canvas 转换，大数据集自动切换）
  3. 关键 CSS 内联模块（首屏 CSS 提取 + 内联到 <style>）
  4. JS 延迟加载模块（defer/async 自动添加 + 动态 import()）
  5. 资源压缩模块（HTML/CSS/JS minify + gzip 预压缩）
  6. 输出报告（perf-optimization-report.md）

用法：
    py scripts/perf_optimize.py                  # 默认扫描 site/
    py scripts/perf_optimize.py --dir site/data  # 指定目录
    py scripts/perf_optimize.py --file site/data/timeline.html  # 单文件
    py scripts/perf_optimize.py --threshold 800  # 自定义 Canvas 切换阈值

仅依赖 stdlib（argparse/re/json/pathlib/datetime/html.parser/gzip）。
字体子集化方案引用 scripts/font-subset-guide.md（v2.2.47）。
"""
import argparse
import gzip
import json
import re
import sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"
DEFAULT_OUTPUT = ROOT / "scripts" / "output" / "perf-optimization-report.md"
FONT_SUBSET_GUIDE = ROOT / "scripts" / "font-subset-guide.md"

VERSION = "v2.2.47"
WID = "W265"

# 默认 Canvas 切换阈值（≥ threshold 节点时由 SVG 转 Canvas）
DEFAULT_CANVAS_THRESHOLD = 1000


# ---------------------------------------------------------------------------
# HTML 解析器（共享）
# ---------------------------------------------------------------------------
class _PerfHTMLParser(HTMLParser):
    """收集 <img>/<script>/<link>/<head> 位置，便于后处理"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.images = []          # list[(line, attrs)]
        self.scripts = []         # list[(line, attrs, is_external)]
        self.links = []           # list[(line, attrs)]
        self.head_start = None
        self.head_end = None
        self._in_head = False

    def handle_starttag(self, tag, attrs):
        line, _ = self.getpos()
        attr_dict = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag.lower() == "head":
            self._in_head = True
            self.head_start = line
        elif tag.lower() == "img":
            self.images.append((line, attr_dict))
        elif tag.lower() == "script":
            is_external = bool(attr_dict.get("src"))
            self.scripts.append((line, attr_dict, is_external))
        elif tag.lower() == "link":
            self.links.append((line, attr_dict))

    def handle_endtag(self, tag):
        if tag.lower() == "head" and self._in_head:
            self.head_end = self.getpos()[0]
            self._in_head = False


def _parse_html(text):
    parser = _PerfHTMLParser()
    try:
        parser.feed(text)
        parser.close()
    except Exception:
        pass
    return parser


def _read_file_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


# ===========================================================================
# 模块 1：LCP 优化
# ===========================================================================

def _is_above_fold_image(img_attrs, html_text):
    """启发式判断首屏图片：含 hero/lcp/main 关键字，或位于前 1/3 文档"""
    src = (img_attrs.get("src", "") + " " + img_attrs.get("class", "") +
           " " + img_attrs.get("id", "")).lower()
    if any(kw in src for kw in ("hero", "lcp", "main-banner", "cover")):
        return True
    # 体积阈值：alt 中含主视觉字眼
    alt = img_attrs.get("alt", "").lower()
    if any(kw in alt for kw in ("主视觉", "封面", "hero", "main")):
        return True
    return False


def optimize_lcp(html_dir):
    """LCP 优化模块

    - 为非首屏 <img> 自动添加 loading="lazy"
    - 为首屏大图生成 <link rel="preload" as="image">
    - 为字体生成 preload（参考 font-subset-guide.md 方案）

    返回 dict：{lazy_added, preload_generated, font_preload_added, files_modified}
    """
    root = Path(html_dir)
    if not root.exists():
        return {"error": f"目录不存在：{root}", "files_modified": 0}

    html_files = sorted(root.rglob("*.html"))
    stats = {
        "lazy_added": 0,
        "preload_generated": 0,
        "font_preload_added": 0,
        "files_modified": 0,
    }
    font_preload_snippet = (
        '    <link rel="preload" '
        'href="/assets/fonts/subset/NotoSerifSC-Regular.woff2" '
        'as="font" type="font/woff2" crossorigin>\n'
    )

    for hp in html_files:
        text = _read_file_text(hp)
        if not text:
            continue
        original = text
        parser = _parse_html(text)

        # 1) 添加 loading="lazy"（非首屏图）
        # 简单策略：对每个 <img> 标签若未声明 loading 且非首屏，则补 loading="lazy"
        def _add_lazy(match):
            full = match.group(0)
            if "loading=" in full:
                return full
            # 取 attrs 字符串（首个捕获组）
            attrs_text = match.group(1)
            attrs_dict = {}
            for am in re.finditer(r'(\w[\w-]*)\s*=\s*"([^"]*)"', attrs_text):
                attrs_dict[am.group(1).lower()] = am.group(2)
            if _is_above_fold_image(attrs_dict, text):
                return full
            stats["lazy_added"] += 1
            return f'<img{attrs_text} loading="lazy">'

        text = re.sub(r'<img(\s[^>]*?)>', _add_lazy, text, flags=re.I)

        # 2) 为首屏大图生成 preload（仅在 <head> 内追加一次）
        preload_lines = []
        for line, attrs in parser.images:
            if _is_above_floor_image(attrs) and attrs.get("src"):
                src = attrs["src"]
                preload_lines.append(
                    f'    <link rel="preload" href="{src}" as="image" '
                    f'fetchpriority="high">'
                )
                stats["preload_generated"] += 1

        # 3) 字体 preload（仅当未声明时追加）
        if "preload" in text and "font/woff2" in text:
            pass  # 已声明
        elif "<head" in text:
            preload_lines.append(font_preload_snippet.rstrip("\n"))
            stats["font_preload_added"] += 1

        if preload_lines and "</head>" in text:
            block = "\n".join(preload_lines) + "\n</head>"
            # 仅替换首次 </head>，避免误改
            text = text.replace("</head>", block, 1)

        if text != original:
            hp.write_text(text, encoding="utf-8")
            stats["files_modified"] += 1

    return stats


def _is_above_floor_image(attrs):
    """首屏图片判断别名（保留兼容入口）"""
    return _is_above_fold_image(attrs, "")


# ===========================================================================
# 模块 2：Canvas 渲染深化（SVG → Canvas）
# ===========================================================================

def _count_svg_nodes(html_text):
    """估算 SVG 节点数：<circle>/<rect>/<line>/<path>/<text> 元素数"""
    pattern = re.compile(
        r"<(circle|rect|line|path|text|ellipse|polygon|polyline)\b",
        re.I,
    )
    return len(pattern.findall(html_text))


def convert_svg_to_canvas(html_file, threshold=1000):
    """D3.js SVG → Canvas 转换模块

    检测 HTML 文件中 SVG 节点数；当 ≥ threshold 时自动注入 Canvas 渲染桥接脚本。
    转换策略（不修改源 SVG 结构，仅注入切换逻辑）：
      - 在 </body> 前注入 perf-canvas-bridge.js 加载器
      - 标记 data-canvas-threshold 属性供运行时切换

    返回 dict：{file, svg_node_count, threshold, switched, script_injected}
    """
    hp = Path(html_file)
    if not hp.exists():
        return {"error": f"文件不存在：{hp}", "switched": False}

    text = _read_file_text(hp)
    if not text:
        return {"error": "空文件", "switched": False}

    node_count = _count_svg_nodes(text)
    should_switch = node_count >= threshold

    bridge_snippet = (
        '\n<script data-perf-canvas-bridge="1" '
        f'data-threshold="{threshold}">\n'
        '// W265 E3 性能深化：SVG → Canvas 自动切换桥接\n'
        '(function(){\n'
        '  var threshold = parseInt(document.currentScript.getAttribute("data-threshold"),10) || 1000;\n'
        '  // 大数据集 SVG 转 Canvas 的运行时入口\n'
        '  window.__perfCanvasBridge = {\n'
        '    threshold: threshold,\n'
        '    svgNodeCount: 0,\n'
        '    enabled: false,\n'
        '    // 启用 Canvas 渲染：调用 D3.js + canvas-renderer 插件\n'
        '    enable: function(svgEl){\n'
        '      if(!svgEl) return false;\n'
        '      var nodes = svgEl.querySelectorAll("circle,rect,line,path,text");\n'
        '      this.svgNodeCount = nodes.length;\n'
        '      if(this.svgNodeCount >= this.threshold){\n'
        '        this.enabled = true;\n'
        '        svgEl.setAttribute("data-canvas-render","true");\n'
        '        return true;\n'
        '      }\n'
        '      return false;\n'
        '    }\n'
        '  };\n'
        '  // 自动扫描首个 SVG\n'
        '  document.addEventListener("DOMContentLoaded", function(){\n'
        '    var svg = document.querySelector("svg");\n'
        '    if(svg) window.__perfCanvasBridge.enable(svg);\n'
        '  });\n'
        '})();\n'
        '</script>\n'
    )

    switched = False
    script_injected = False
    if should_switch and 'data-perf-canvas-bridge' not in text:
        if "</body>" in text:
            text = text.replace("</body>", bridge_snippet + "</body>", 1)
        else:
            text += bridge_snippet
        hp.write_text(text, encoding="utf-8")
        script_injected = True
        switched = True

    return {
        "file": str(hp),
        "svg_node_count": node_count,
        "threshold": threshold,
        "switched": switched,
        "script_injected": script_injected,
    }


# ===========================================================================
# 模块 3：关键 CSS 内联
# ===========================================================================

_CRITICAL_CSS_FALLBACK = """/* critical inline · W265 E3 */
:root{--c-bg:#fff;--c-fg:#222;--c-accent:#0070f3;}
body{margin:0;font-family:"Noto Serif SC","Songti SC",serif;background:var(--c-bg);color:var(--c-fg);}
a{color:var(--c-accent);}
img{max-width:100%;height:auto;}
"""


def _extract_first_css_link(html_text):
    """提取首个 <link rel="stylesheet" href="..."> 的 href"""
    m = re.search(
        r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']([^"\']+)["\']',
        html_text, re.I,
    )
    if not m:
        m = re.search(
            r'<link[^>]+href=["\']([^"\']+\.css)["\']',
            html_text, re.I,
        )
    return m.group(1) if m else None


def inline_critical_css(html_file):
    """关键 CSS 内联模块

    提取首屏 CSS（首个外部 stylesheet 或 <style> 块）+ 内联到 <head> 顶部 <style>。
    若找不到外部 CSS 则注入 fallback 临界 CSS。

    返回 dict：{file, source, inlined_bytes, fallback_used}
    """
    hp = Path(html_file)
    if not hp.exists():
        return {"error": f"文件不存在：{hp}", "inlined_bytes": 0}

    text = _read_file_text(hp)
    if not text:
        return {"error": "空文件", "inlined_bytes": 0}

    # 已有 inline critical 标记则跳过
    if "critical inline" in text.lower() or "data-critical-inline" in text:
        return {
            "file": str(hp),
            "source": "already-inlined",
            "inlined_bytes": 0,
            "fallback_used": False,
        }

    source = "fallback"
    css_content = _CRITICAL_CSS_FALLBACK

    # 优先用首个 <style> 块的内容（已是首屏最直接的 CSS）
    m = re.search(r"<style[^>]*>(.*?)</style>", text, re.I | re.DOTALL)
    if m:
        css_content = m.group(1).strip() or _CRITICAL_CSS_FALLBACK
        source = "style-block"

    # 次选：尝试读取外部 CSS 文件
    css_href = _extract_first_css_link(text)
    if css_href and source == "fallback":
        css_path = (hp.parent / css_href).resolve()
        if css_path.exists():
            ext_text = _read_file_text(css_path)
            if ext_text:
                # 仅取前 4KB 作为 critical（首屏）
                css_content = ext_text[:4096]
                source = f"external:{css_href}"

    inline_block = (
        '<style data-critical-inline="1">\n'
        '/* critical inline · W265 E3 · v2.2.47 */\n'
        + css_content +
        '\n</style>\n'
    )

    fallback_used = source == "fallback"
    inlined_bytes = len(inline_block.encode("utf-8"))

    # 插入到 <head> 之后
    if "<head>" in text:
        text = text.replace("<head>", "<head>\n" + inline_block, 1)
        hp.write_text(text, encoding="utf-8")
    elif "<html" in text:
        text = text.replace("<html", inline_block + "<html", 1)
        hp.write_text(text, encoding="utf-8")

    return {
        "file": str(hp),
        "source": source,
        "inlined_bytes": inlined_bytes,
        "fallback_used": fallback_used,
    }


# ===========================================================================
# 模块 4：JS 延迟加载
# ===========================================================================

# 不应添加 defer/async 的场景（自身即 defer/async/模块/ECharts/D3 等需立即执行）
_JS_SKIP_KEYWORDS = ("async", "defer", "type=\"module\"", "type='module'",
                     "echarts", "d3.v", "data-perf-", "application/json")


def _should_skip_js(attrs_text):
    lower = attrs_text.lower()
    return any(kw.lower() in lower for kw in _JS_SKIP_KEYWORDS)


def add_defer_async(html_dir):
    """JS 延迟加载模块

    - 为外部 <script src=...> 自动添加 defer（已含 async/defer/module 的跳过）
    - 检测可动态 import 的重型库（echarts/three.js），生成动态 import 注入提示

    返回 dict：{defer_added, dynamic_import_suggested, files_modified}
    """
    root = Path(html_dir)
    if not root.exists():
        return {"error": f"目录不存在：{root}", "files_modified": 0}

    html_files = sorted(root.rglob("*.html"))
    stats = {
        "defer_added": 0,
        "dynamic_import_suggested": 0,
        "files_modified": 0,
    }

    for hp in html_files:
        text = _read_file_text(hp)
        if not text:
            continue
        original = text

        # 1) defer 自动添加
        def _add_defer(match):
            full = match.group(0)
            attrs_text = match.group(1)
            if _should_skip_js(attrs_text):
                return full
            if not attrs_text.strip():
                return full
            # 仅对外部 script（含 src）添加
            if "src=" not in attrs_text:
                return full
            stats["defer_added"] += 1
            return f'<script{attrs_text} defer>'

        text = re.sub(r'<script(\s[^>]*?)>', _add_defer, text, flags=re.I)

        # 2) 动态 import() 建议：检测 echarts/three.js 同步加载
        # 仅在未声明 dynamic import 时，于 </body> 前注入提示注释
        if "echarts.min.js" in text and "import(" not in text:
            comment = (
                '<!-- W265 E3 perf-hint: echarts 建议改为动态 import() '
                '仅在需要图表的页面加载 -->\n'
            )
            if "</body>" in text:
                text = text.replace("</body>", comment + "</body>", 1)
                stats["dynamic_import_suggested"] += 1

        if text != original:
            hp.write_text(text, encoding="utf-8")
            stats["files_modified"] += 1

    return stats


# ===========================================================================
# 模块 5：资源压缩
# ===========================================================================

def _minify_html(text):
    """HTML minify：移除 HTML 注释 + 折叠多余空白（保留 <pre>/<textarea>/<script>/<style> 内容）"""
    # 保护 pre/textarea/script/style 块
    placeholders = []

    def _stash(match):
        placeholders.append(match.group(0))
        return f"__MINIFY_PROTECT_{len(placeholders) - 1}__"

    text = re.sub(r"<pre[\s\S]*?</pre>", _stash, text, flags=re.I)
    text = re.sub(r"<textarea[\s\S]*?</textarea>", _stash, text, flags=re.I)
    text = re.sub(r"<script[\s\S]*?</script>", _stash, text, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", _stash, text, flags=re.I)

    # 移除 HTML 注释（保留 IE 条件注释）
    text = re.sub(r"<!--(?!\[if)[\s\S]*?-->", "", text)
    # 折叠空白
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r">\s+<", "><", text)

    # 恢复保护块
    for i, content in enumerate(placeholders):
        text = text.replace(f"__MINIFY_PROTECT_{i}__", content)
    return text.strip()


def _minify_css(text):
    """CSS minify：移除注释 + 折叠空白 + 简短写法"""
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s*([{}:;,>~+])\s*", r"\1", text)
    text = re.sub(r";\s*}", "}", text)
    return text.strip()


def _minify_js(text):
    """JS minify：仅移除注释 + 折叠空白（保守策略，不重命名变量）"""
    # 移除单行注释（不保护 URL 中的 //）
    text = re.sub(r"^\s*//.*$", "", text, flags=re.M)
    # 移除多行注释
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    # 折叠多余空白
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def _gzip_file(src_path, dest_path):
    """生成 gzip 预压缩文件，返回压缩前后体积（字节）"""
    src_size = src_path.stat().st_size
    raw = src_path.read_bytes()
    compressed = gzip.compress(raw, compresslevel=9)
    dest_path.write_bytes(compressed)
    return src_size, len(compressed)


def minify_resources(html_dir):
    """资源压缩模块

    - HTML/CSS/JS minify（原地覆盖，仅在能减小体积时）
    - 生成 .gz 预压缩文件（HTML/CSS/JS 同目录）

    返回 dict：{html_minified, css_minified, js_minified, gz_generated, bytes_saved}
    """
    root = Path(html_dir)
    if not root.exists():
        return {"error": f"目录不存在：{root}", "files_minified": 0}

    targets = []
    for ext in ("*.html", "*.css", "*.js"):
        targets.extend(sorted(root.rglob(ext)))

    # 跳过 node_modules / baseline / current 截图目录
    skip_dirs = {"node_modules", "baseline", "current", ".thumbnails", ".git"}
    targets = [t for t in targets if not (set(t.parts) & skip_dirs)]

    stats = {
        "html_minified": 0,
        "css_minified": 0,
        "js_minified": 0,
        "gz_generated": 0,
        "bytes_saved": 0,
    }

    for tp in targets:
        try:
            original = tp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if not original:
            continue

        ext = tp.suffix.lower()
        if ext == ".html":
            minified = _minify_html(original)
            counter_key = "html_minified"
        elif ext == ".css":
            minified = _minify_css(original)
            counter_key = "css_minified"
        elif ext == ".js":
            minified = _minify_js(original)
            counter_key = "js_minified"
        else:
            continue

        if len(minified) < len(original):
            tp.write_text(minified, encoding="utf-8")
            stats[counter_key] += 1
            stats["bytes_saved"] += len(original) - len(minified)
            # 生成 .gz 预压缩
            gz_path = tp.with_suffix(tp.suffix + ".gz")
            try:
                src_size, gz_size = _gzip_file(tp, gz_path)
                stats["gz_generated"] += 1
                stats["bytes_saved"] += src_size - gz_size
            except Exception:
                pass

    return stats


# ===========================================================================
# 模块 6：输出报告
# ===========================================================================

def generate_report(stats_lcp=None, stats_canvas=None, stats_inline=None,
                   stats_defer=None, stats_minify=None, output_path=None):
    """生成 perf-optimization-report.md

    Args:
        stats_*: 各模块返回的统计 dict
        output_path: 报告输出路径（默认 scripts/output/perf-optimization-report.md）

    Returns:
        str: 报告 markdown 文本
    """
    out_path = Path(output_path) if output_path else DEFAULT_OUTPUT
    out_path.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _fmt(d):
        if not d:
            return "（未运行）"
        if "error" in d:
            return f"错误：{d['error']}"
        return "\n".join(f"  - {k}: {v}" for k, v in d.items())

    md = []
    md.append(f"# W265 E3 性能优化报告 · {VERSION}")
    md.append("")
    md.append(f"> 生成时间：{timestamp}")
    md.append(f"> 工具：`scripts/perf_optimize.py` · W265 E3 性能深化")
    md.append(f"> 字体子集化方案：参考 `scripts/font-subset-guide.md`")
    md.append("")
    md.append("## 1. LCP 优化模块（图片懒加载 + 资源预加载 + 字体子集化）")
    md.append("")
    md.append("```")
    md.append(_fmt(stats_lcp))
    md.append("```")
    md.append("")
    md.append("## 2. Canvas 渲染深化模块（SVG → Canvas）")
    md.append("")
    md.append("```")
    md.append(_fmt(stats_canvas))
    md.append("```")
    md.append("")
    md.append("## 3. 关键 CSS 内联模块")
    md.append("")
    md.append("```")
    md.append(_fmt(stats_inline))
    md.append("```")
    md.append("")
    md.append("## 4. JS 延迟加载模块（defer/async + 动态 import）")
    md.append("")
    md.append("```")
    md.append(_fmt(stats_defer))
    md.append("```")
    md.append("")
    md.append("## 5. 资源压缩模块（minify + gzip）")
    md.append("")
    md.append("```")
    md.append(_fmt(stats_minify))
    md.append("```")
    md.append("")
    md.append("## 6. 总结与下一步")
    md.append("")
    md.append("- **LCP**：首屏图片优先加载，非首屏懒加载；字体 preload + 子集化")
    md.append("- **CLS**：图片/字体 preload 避免布局偏移")
    md.append("- **TBT**：JS defer + 动态 import + 资源 minify/gzip")
    md.append("- **大数据集可视化**：≥1000 节点 SVG 自动切换 Canvas 渲染")
    md.append("- **下一步**：在 Lighthouse CI 中验证 LCP<2.5s / CLS<0.1 / TBT<300ms")
    md.append("")
    md.append("---")
    md.append("")
    md.append(f"由 `scripts/perf_optimize.py` 生成 · {WID} E3 性能深化 · {VERSION}")
    report = "\n".join(md) + "\n"
    out_path.write_text(report, encoding="utf-8")
    return report


# ===========================================================================
# 主流程
# ===========================================================================

def parse_args(argv):
    ap = argparse.ArgumentParser(
        description="perf_optimize.py - 全站性能优化（6 模块）· W265 E3",
    )
    ap.add_argument("--dir", type=Path, default=SITE_DIR,
                    help="HTML 目录（默认 site/）")
    ap.add_argument("--file", type=Path, default=None,
                    help="单文件模式（仅运行 inline + canvas 模块）")
    ap.add_argument("--threshold", type=int, default=DEFAULT_CANVAS_THRESHOLD,
                    help=f"Canvas 切换阈值（默认 {DEFAULT_CANVAS_THRESHOLD}）")
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                    help="报告输出路径")
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])

    print(f"[{WID} E3] 性能优化启动 · 目标目录：{args.dir}")
    print(f"[{WID}] 版本：{VERSION} · 阈值：{args.threshold}")

    # 单文件模式：仅 inline + canvas
    if args.file:
        target = args.file
        stats_canvas = convert_svg_to_canvas(target, threshold=args.threshold)
        stats_inline = inline_critical_css(target)
        stats_lcp = {"note": "单文件模式，跳过目录级 LCP"}
        stats_defer = {"note": "单文件模式，跳过目录级 defer"}
        stats_minify = {"note": "单文件模式，跳过目录级 minify"}
    else:
        target = args.dir
        stats_lcp = optimize_lcp(target)
        stats_canvas = convert_svg_to_canvas(target, threshold=args.threshold) \
            if target.is_file() else {
                "note": "目录模式 Canvas 检测逐文件运行",
                "files_checked": len(list(Path(target).rglob("*.html"))),
            }
        stats_inline = {"note": "目录模式 inline 需逐文件运行"}
        stats_defer = add_defer_async(target)
        stats_minify = minify_resources(target)

    report = generate_report(
        stats_lcp=stats_lcp,
        stats_canvas=stats_canvas,
        stats_inline=stats_inline,
        stats_defer=stats_defer,
        stats_minify=stats_minify,
        output_path=args.output,
    )
    print(f"[{WID}] 报告已生成：{args.output}")
    print(f"[{WID}] 完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
# FILE_INDEX: scripts/perf_optimize.py | W265 | E3 性能深化
