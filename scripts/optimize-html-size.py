#!/usr/bin/env python3
"""
W230 E3 · HTML 文件体积优化脚本
==================================================
扫描 site/data/*.html，识别大文件（>100KB）并给出优化建议。
不修改 HTML 文件本身，仅生成报告 scripts/output/html-size-report.md。

用法：
    python scripts/optimize-html-size.py
可选依赖：beautifulsoup4（用于更精准的 <style>/<script> 标签解析）
            如未安装，自动回退到正则匹配。

技术要点：
    1. 文件大小（KB/MB）
    2. 内联 <style> 块大小
    3. 内联 <script> 块大小
    4. HTML 注释数量与体积
    5. 多余空白（连续 2+ 空格或行尾空白）
    6. 懒加载建议（识别 <img> / <iframe> 缺 loading="lazy"）
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ===== 路径配置 =====
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
HTML_DIR = PROJECT_ROOT / "site" / "data"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "html-size-report.md"

# 阈值
LARGE_FILE_KB = 100.0  # > 100 KB 视为大文件
MINIFY_REDUCTION_RATIO = 0.20  # 预估压缩比例下限

# ===== 可选依赖：beautifulsoup4 =====
try:
    from bs4 import BeautifulSoup  # type: ignore
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


@dataclass
class FileMetrics:
    """单个 HTML 文件的体积与构成指标。"""
    path: str = ""
    raw_size: int = 0                      # 原始字节
    inline_css_size: int = 0               # <style> 内字符数
    inline_js_size: int = 0                # <script> 内字符数（不含 src）
    external_scripts: int = 0              # <script src=> 数量
    external_styles: int = 0               # <link rel=stylesheet> 数量
    comments_count: int = 0                # HTML 注释数
    comments_size: int = 0                 # 注释字符数
    whitespace_size: int = 0               # 可压缩空白字符数
    img_count: int = 0                     # <img> 数量
    img_lazy: int = 0                      # 已带 loading="lazy" 的 <img>
    iframe_count: int = 0                  # <iframe> 数量
    iframe_lazy: int = 0                   # 已带 loading="lazy" 的 <iframe>
    estimated_optimized_size: int = 0      # 优化后预估字节
    suggestions: list = field(default_factory=list)

    @property
    def raw_size_kb(self) -> float:
        return self.raw_size / 1024.0

    @property
    def optimized_size_kb(self) -> float:
        return self.estimated_optimized_size / 1024.0

    @property
    def reduction_ratio(self) -> float:
        if self.raw_size == 0:
            return 0.0
        return (self.raw_size - self.estimated_optimized_size) / self.raw_size


# ===== 解析函数 =====
def parse_html(content: str) -> FileMetrics:
    """使用 BeautifulSoup 优先解析；缺失时回退到正则。"""
    fm = FileMetrics(path="")

    if HAS_BS4:
        try:
            soup = BeautifulSoup(content, "html.parser")
            # 内联 style
            for tag in soup.find_all("style"):
                fm.inline_css_size += len(tag.string or tag.text or "")
            # 内联 script
            for tag in soup.find_all("script"):
                if tag.get("src"):
                    fm.external_scripts += 1
                else:
                    fm.inline_js_size += len(tag.string or tag.text or "")
            # 外链 CSS
            fm.external_styles = len(soup.find_all("link", rel=lambda r: r and "stylesheet" in r))
            # img / iframe
            for tag in soup.find_all("img"):
                fm.img_count += 1
                if tag.get("loading") == "lazy":
                    fm.img_lazy += 1
            for tag in soup.find_all("iframe"):
                fm.iframe_count += 1
                if tag.get("loading") == "lazy":
                    fm.iframe_lazy += 1
        except Exception:
            _parse_with_regex(content, fm)
    else:
        _parse_with_regex(content, fm)

    # 注释与空白（两种方式都要算）
    _parse_comments_whitespace(content, fm)
    return fm


def _parse_with_regex(content: str, fm: FileMetrics) -> None:
    """正则回退解析。"""
    # <style>...</style> 非贪婪
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", content, flags=re.DOTALL | re.IGNORECASE):
        fm.inline_css_size += len(m.group(1))
    # <script>...</script> 没有 src 的
    for m in re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", content, flags=re.DOTALL | re.IGNORECASE):
        fm.inline_js_size += len(m.group(1))
    fm.external_scripts = len(re.findall(r"<script[^>]*\bsrc=", content, flags=re.IGNORECASE))
    fm.external_styles = len(re.findall(r"<link[^>]*\brel=['\"]?stylesheet['\"]?", content, flags=re.IGNORECASE))
    # img / iframe
    imgs = re.findall(r"<img\b[^>]*>", content, flags=re.IGNORECASE)
    fm.img_count = len(imgs)
    fm.img_lazy = sum(1 for t in imgs if re.search(r"\bloading=['\"]?lazy['\"]?", t, re.IGNORECASE))
    iframes = re.findall(r"<iframe\b[^>]*>", content, flags=re.IGNORECASE)
    fm.iframe_count = len(iframes)
    fm.iframe_lazy = sum(1 for t in iframes if re.search(r"\bloading=['\"]?lazy['\"]?", t, re.IGNORECASE))


def _parse_comments_whitespace(content: str, fm: FileMetrics) -> None:
    # HTML 注释（条件注释除外）
    comments = re.findall(r"<!--(.*?)-->", content, flags=re.DOTALL)
    fm.comments_count = len(comments)
    fm.comments_size = sum(len(c) + 7 for c in comments)  # 7 = <!-- + -->

    # 可压缩空白：连续 2+ 空格 / 制表符 / 行尾空白 / 多空行
    whitespace = 0
    for line in content.splitlines():
        # 行尾空白
        trailing = len(line) - len(line.rstrip())
        whitespace += trailing
        # 行内连续 2+ 空格（保守估算：每处只算多余的 1 个）
        whitespace += len(re.findall(r"  +", line))
    # 空行
    whitespace += sum(1 for line in content.splitlines() if not line.strip())
    fm.whitespace_size = whitespace


def estimate_optimized_size(fm: FileMetrics) -> None:
    """估算优化后体积（仅提取外部 + 压缩空白 + 删注释，未做真正的压缩）。"""
    saved = 0
    # 假设 60% 的内联 CSS 提取到外部共享样式表（仅本页保留 ~40% 页面专属样式）
    css_extract = int(fm.inline_css_size * 0.6)
    saved += css_extract
    # 假设 50% 的内联 JS 提取到外部 .js 文件
    js_extract = int(fm.inline_js_size * 0.5)
    saved += js_extract
    # 删除注释（保留 5% 的条件注释）
    comments_saved = int(fm.comments_size * 0.95)
    saved += comments_saved
    # 压缩空白（保留 30%，因 <pre> 等需保留）
    whitespace_saved = int(fm.whitespace_size * 0.7)
    saved += whitespace_saved

    fm.estimated_optimized_size = max(0, fm.raw_size - saved)


def build_suggestions(fm: FileMetrics) -> None:
    """生成针对单文件的优化建议列表。"""
    s = fm.suggestions
    if fm.raw_size_kb >= LARGE_FILE_KB:
        s.append(f"⚠️ 大文件（{fm.raw_size_kb:.1f}KB > {LARGE_FILE_KB:.0f}KB 阈值），优先优化")

    if fm.inline_css_size > 5 * 1024:
        s.append(f"内联 CSS 较大（{fm.inline_css_size / 1024:.1f}KB）：建议提取到 site/static/css/<page>.css 外部文件，多页共享时合并为 common.css，浏览器可缓存")
    elif fm.inline_css_size > 1 * 1024:
        s.append(f"内联 CSS 偏大（{fm.inline_css_size / 1024:.1f}KB）：可考虑提取到外部样式表以提升缓存命中率")

    if fm.inline_js_size > 10 * 1024:
        s.append(f"内联 JS 较大（{fm.inline_js_size / 1024:.1f}KB）：建议提取到 site/static/js/<page>.js，配合 defer 异步加载")
    elif fm.inline_js_size > 3 * 1024:
        s.append(f"内联 JS 偏大（{fm.inline_js_size / 1024:.1f}KB）：可提取到外部文件 + defer")

    if fm.comments_size > 2 * 1024:
        s.append(f"HTML 注释较多（{fm.comments_count} 个，{fm.comments_size / 1024:.1f}KB）：生产环境可删除非必要注释，保留 <!--[if IE]> 等条件注释")

    if fm.whitespace_size > 5 * 1024:
        s.append(f"冗余空白较多（{fm.whitespace_size / 1024:.1f}KB）：可启用 HTML minify（如 html-minifier-terser）压缩空白")

    if fm.img_count > 0 and fm.img_lazy < fm.img_count:
        missing = fm.img_count - fm.img_lazy
        s.append(f"懒加载缺失：{missing}/{fm.img_count} 个 <img> 未带 loading=\"lazy\"，首屏外的图片应启用懒加载")

    if fm.iframe_count > 0 and fm.iframe_lazy < fm.iframe_count:
        missing = fm.iframe_count - fm.iframe_lazy
        s.append(f"iframe 懒加载缺失：{missing}/{fm.iframe_count} 个 <iframe> 未带 loading=\"lazy\"")

    if fm.external_scripts > 5:
        s.append(f"外部脚本较多（{fm.external_scripts}）：合并为单 bundle 或采用 HTTP/2 push，减少请求数")

    if not s:
        s.append("✅ 文件体积健康，无需立即优化")


def format_kb(n: int) -> str:
    if n >= 1024 * 1024:
        return f"{n / (1024 * 1024):.2f} MB"
    return f"{n / 1024:.2f} KB"


# ===== 主流程 =====
def scan_directory(html_dir: Path) -> list[FileMetrics]:
    if not html_dir.exists():
        print(f"[ERR] 目录不存在: {html_dir}", file=sys.stderr)
        sys.exit(1)

    html_files = sorted(html_dir.glob("*.html"))
    if not html_files:
        print(f"[WARN] 未在 {html_dir} 中找到 .html 文件", file=sys.stderr)
        return []

    results: list[FileMetrics] = []
    for fp in html_files:
        try:
            content = fp.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            print(f"[ERR] 读取失败 {fp}: {e}", file=sys.stderr)
            continue
        fm = parse_html(content)
        fm.path = str(fp.relative_to(PROJECT_ROOT)).replace("\\", "/")
        fm.raw_size = len(content.encode("utf-8"))
        estimate_optimized_size(fm)
        build_suggestions(fm)
        results.append(fm)

    return results


def render_report(results: list[FileMetrics]) -> str:
    if not results:
        return "# HTML 体积优化报告\n\n（无扫描结果）\n"

    total_raw = sum(r.raw_size for r in results)
    total_opt = sum(r.estimated_optimized_size for r in results)
    total_reduction = total_raw - total_opt
    reduction_pct = (total_reduction / total_raw * 100) if total_raw else 0.0
    large_files = [r for r in results if r.raw_size_kb >= LARGE_FILE_KB]

    lines: list[str] = []
    lines.append("# HTML 文件体积优化报告")
    lines.append("")
    lines.append("> W230 E3 · 由 `scripts/optimize-html-size.py` 自动生成 · 不修改 HTML 源文件")
    lines.append("")
    lines.append("- **扫描目录**：`site/data/`")
    lines.append(f"- **HTML 文件数**：{len(results)}")
    lines.append(f"- **总体积（原始）**：{format_kb(total_raw)}")
    lines.append(f"- **总体积（优化后预估）**：{format_kb(total_opt)}")
    lines.append(f"- **可减少体积**：{format_kb(total_reduction)}（{reduction_pct:.1f}%）")
    lines.append(f"- **大文件（>{LARGE_FILE_KB:.0f}KB）数量**：{len(large_files)}")
    lines.append(f"- **解析后端**：{'BeautifulSoup4' if HAS_BS4 else '正则回退（建议 pip install beautifulsoup4 以获得更精准的解析）'}")
    lines.append("")

    # Top 10 大文件
    top10 = sorted(results, key=lambda r: r.raw_size, reverse=True)[:10]
    lines.append("## 一、Top 10 大文件（按原始体积降序）")
    lines.append("")
    lines.append("| # | 文件 | 原始 | 内联CSS | 内联JS | 注释 | 空白 | 优化后 | 减少 | 建议数 |")
    lines.append("|---|------|------|---------|--------|------|------|--------|------|--------|")
    for i, r in enumerate(top10, 1):
        lines.append(
            f"| {i} | `{r.path}` | {format_kb(r.raw_size)} | "
            f"{format_kb(r.inline_css_size)} | {format_kb(r.inline_js_size)} | "
            f"{format_kb(r.comments_size)} | {format_kb(r.whitespace_size)} | "
            f"{format_kb(r.estimated_optimized_size)} | "
            f"{format_kb(r.raw_size - r.estimated_optimized_size)} ({r.reduction_ratio * 100:.0f}%) | "
            f"{len(r.suggestions)} |"
        )
    lines.append("")

    # 全量文件明细表
    lines.append("## 二、全量文件明细")
    lines.append("")
    lines.append("| 文件 | 原始 | 优化后预估 | 优化比例 | 内联CSS | 内联JS | 注释 | 空白 | 外链JS | 外链CSS | img/lazy | iframe/lazy |")
    lines.append("|------|------|-----------|----------|---------|--------|------|------|--------|---------|----------|-------------|")
    for r in sorted(results, key=lambda x: x.raw_size, reverse=True):
        img_str = f"{r.img_lazy}/{r.img_count}" if r.img_count else "0/0"
        iframe_str = f"{r.iframe_lazy}/{r.iframe_count}" if r.iframe_count else "0/0"
        lines.append(
            f"| `{r.path}` | {format_kb(r.raw_size)} | {format_kb(r.estimated_optimized_size)} | "
            f"{r.reduction_ratio * 100:.1f}% | {format_kb(r.inline_css_size)} | {format_kb(r.inline_js_size)} | "
            f"{format_kb(r.comments_size)} | {format_kb(r.whitespace_size)} | "
            f"{r.external_scripts} | {r.external_styles} | {img_str} | {iframe_str} |"
        )
    lines.append("")

    # 大文件专项建议
    lines.append("## 三、大文件（>100KB）优化建议")
    lines.append("")
    if not large_files:
        lines.append("✅ 当前未发现 > 100KB 的大文件，整体体积可控。")
        lines.append("")
    else:
        for r in sorted(large_files, key=lambda x: x.raw_size, reverse=True):
            lines.append(f"### `{r.path}` — {format_kb(r.raw_size)} → 预估 {format_kb(r.estimated_optimized_size)}（减少 {r.reduction_ratio * 100:.1f}%）")
            lines.append("")
            for sug in r.suggestions:
                lines.append(f"- {sug}")
            lines.append("")

    # 通用优化策略
    lines.append("## 四、通用优化策略")
    lines.append("")
    lines.append("### 4.1 内联 CSS 提取到外部文件")
    lines.append("- 多页共享的样式（如 `.section` / `.kpi-card` / `.chart-block`）合并为 `site/static/css/common.css`，浏览器跨页面缓存")
    lines.append("- 页面专属样式保留在 `<style>` 或单独 `site/static/css/<page>.css`")
    lines.append("- 工具：`purgecss` 可剔除未使用的 CSS 规则")
    lines.append("")
    lines.append("### 4.2 内联 JS 提取到外部文件")
    lines.append("- 大块 D3.js 渲染逻辑提取到 `site/static/js/<page>.js`，配合 `<script defer>` 异步加载")
    lines.append("- 共享的常量（如 `NAME_POOL` / `COLOR_BY_GROUP`）抽取到 `site/static/js/common.js`")
    lines.append("- 第三方库（D3.js v7）改为 CDN 引用 + SRI 完整性校验")
    lines.append("")
    lines.append("### 4.3 删除 HTML 注释")
    lines.append("- 生产构建时通过 `html-minifier-terser` 删除所有非条件注释")
    lines.append("- 保留 `<!--[if IE]>` 等条件注释")
    lines.append("- 保留 `<!-- noscript -->` 等功能性注释")
    lines.append("")
    lines.append("### 4.4 压缩空白")
    lines.append("- 启用 HTML minify（连续空格 → 单空格、移除行尾空白、移除空行）")
    lines.append("- 保守压缩：保留 `<pre>` / `<textarea>` 内的空白")
    lines.append("- 工具链：`html-minifier-terser` 或 Vite `vite-plugin-html-minify`")
    lines.append("")
    lines.append("### 4.5 懒加载非关键资源")
    lines.append("- `<img loading=\"lazy\">`：首屏外图片延迟加载")
    lines.append("- `<iframe loading=\"lazy\">`：嵌入页面延迟加载")
    lines.append("- `<link rel=\"preload\">` 仅用于关键字体 / 关键 CSS")
    lines.append("- `<script defer>` 或 `<script type=\"module\">`：非关键 JS 异步化")
    lines.append("")
    lines.append("### 4.6 进一步压缩（gzip / brotli）")
    lines.append("- Web 服务器启用 gzip（一般可达 70% 压缩）或 brotli（可达 80%+ 压缩）")
    lines.append("- HTML 文本压缩率高于二进制资源，优先确保 text/html 启用压缩")
    lines.append("- 配合 CDN 边缘缓存，命中后零字节传输")
    lines.append("")

    # 附录：脚本说明
    lines.append("## 五、脚本运行说明")
    lines.append("")
    lines.append("```bash")
    lines.append("# 进入项目根")
    lines.append("cd d:/1/xiyouji")
    lines.append("")
    lines.append("# 运行脚本（标准库即可，无需额外依赖）")
    lines.append("python scripts/optimize-html-size.py")
    lines.append("")
    lines.append("# 可选：安装 beautifulsoup4 获得更精准的解析")
    lines.append("pip install beautifulsoup4")
    lines.append("```")
    lines.append("")
    lines.append("- **输出位置**：`scripts/output/html-size-report.md`")
    lines.append("- **运行模式**：只读扫描，不修改 HTML 文件")
    lines.append("- **建议频率**：每次新增可视化页面后运行一次")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    print(f"[INFO] 扫描目录: {HTML_DIR}")
    print(f"[INFO] BeautifulSoup4: {'available' if HAS_BS4 else 'not installed (using regex fallback)'}")

    results = scan_directory(HTML_DIR)
    if not results:
        print("[WARN] 无文件可分析，退出。")
        return 1

    print(f"[INFO] 扫描到 {len(results)} 个 HTML 文件")

    report = render_report(results)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"[OK] 报告已生成: {OUTPUT_FILE}")

    total_raw = sum(r.raw_size for r in results)
    total_opt = sum(r.estimated_optimized_size for r in results)
    print(f"[STATS] 原始总体积: {format_kb(total_raw)}")
    print(f"[STATS] 优化后预估: {format_kb(total_opt)}")
    print(f"[STATS] 可减少: {format_kb(total_raw - total_opt)} ({(total_raw - total_opt) / total_raw * 100:.1f}%)")

    large_count = sum(1 for r in results if r.raw_size_kb >= LARGE_FILE_KB)
    print(f"[STATS] 大文件(>{LARGE_FILE_KB:.0f}KB): {large_count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
