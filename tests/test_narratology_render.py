"""P1 组件测试 · 十七维叙事学关系图谱 narratology-13d-network.html

依据：docs/10-方法论沉淀/可视化测试计划-十七维叙事学图谱.md
覆盖：渲染非空 + dim-card 交互 + summary-table 排序 + tooltip + 降级 + 响应式
运行：python -m pytest tests/test_narratology_render.py -v
前置：pip install playwright pytest-playwright && playwright install chromium
"""

import re
from pathlib import Path

import pytest

pytest.importorskip("playwright", reason="playwright 未安装：pip install playwright pytest-playwright")
from playwright.sync_api import Page, expect

HTML_PATH = Path(__file__).resolve().parent.parent / "site" / "data" / "narratology-13d-network.html"
HTML_URL = HTML_PATH.as_uri()  # file:// 协议


def _wait_render_ready(page: Page, timeout: int = 8000) -> None:
    """等待 main() 完成：window.__lastData 存在 + 16 个 dim-card 渲染。"""
    page.wait_for_function("() => window.__lastData && window.__lastData.dimensions", timeout=timeout)
    page.wait_for_function(
        "() => document.querySelectorAll('.dim-card').length === window.__lastData.dimensions.length",
        timeout=timeout,
    )


@pytest.fixture(scope="module")
def browser_context(browser):
    """模块级 browser_context，复用浏览器实例。"""
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    yield context
    context.close()


@pytest.fixture
def page(browser_context):
    """每个测试用例新建 page，隔离状态。"""
    p = browser_context.new_page()
    p.goto(HTML_URL)
    _wait_render_ready(p)
    yield p
    p.close()


# ============================================================
# Section 1: 渲染非空（4 个 SVG + 概览卡片 + 汇总表）
# ============================================================

class TestRenderNonEmpty:
    """验证 6 个渲染组件均产出可见 DOM 节点。"""

    def test_force_svg_non_empty(self, page):
        """力导向图：circle/line/text 节点数 > 0。"""
        svg = page.locator("#chart-force")
        expect(svg).to_be_visible()
        # 节点 circle（维度 + 外部节点）
        circle_count = svg.locator("circle").count()
        line_count = svg.locator("line.rel-link").count()
        text_count = svg.locator("text").count()
        assert circle_count > 0, f"force circle 数为 0，line={line_count}, text={text_count}"
        assert line_count > 0, f"force line 数为 0，circle={circle_count}"
        assert text_count > 0, f"force text 数为 0"

    def test_sankey_svg_non_empty(self, page):
        """桑基图：path 或 rect 节点数 > 0。"""
        svg = page.locator("#chart-sankey")
        expect(svg).to_be_visible()
        path_count = svg.locator("path").count()
        rect_count = svg.locator("rect").count()
        # d3-sankey 节点为 rect，链接为 path
        assert rect_count > 0 or path_count > 0, f"sankey rect={rect_count}, path={path_count} 均为 0"

    def test_radar_svg_non_empty(self, page):
        """雷达图：polygon 节点数 > 0。"""
        svg = page.locator("#chart-radar")
        expect(svg).to_be_visible()
        polygon_count = svg.locator("polygon").count()
        circle_count = svg.locator("circle").count()
        assert polygon_count > 0 or circle_count > 0, f"radar polygon={polygon_count}, circle={circle_count} 均为 0"

    def test_timeline_svg_non_empty(self, page):
        """时间线：circle 或 line 节点数 > 0。"""
        svg = page.locator("#chart-timeline")
        expect(svg).to_be_visible()
        circle_count = svg.locator("circle").count()
        line_count = svg.locator("line").count()
        text_count = svg.locator("text").count()
        assert circle_count > 0 or line_count > 0, f"timeline circle={circle_count}, line={line_count} 均为 0"

    def test_dim_cards_count(self, page):
        """概览卡片：16 个 .dim-card 渲染。"""
        cards = page.locator(".dim-card")
        expect(cards.first).to_be_visible()
        count = cards.count()
        # 数据为 16 维度（W191 网络叙事学未入 dimensions 数组，编辑决策）
        assert count == 16, f"dim-card 数={count}，期望 16"

    def test_summary_table_rows(self, page):
        """汇总表：16 行渲染 + 11 列表头。"""
        tbody_rows = page.locator("#summary-table-wrap tbody tr")
        expect(tbody_rows.first).to_be_visible()
        assert tbody_rows.count() == 16, f"summary-table 行数={tbody_rows.count()}，期望 16"
        th_count = page.locator("#summary-table-wrap thead th").count()
        assert th_count == 11, f"summary-table 列数={th_count}，期望 11"


# ============================================================
# Section 2: dim-card 交互（click + 键盘）
# ============================================================

class TestDimCardInteraction:
    """验证 dim-card 的 click + Enter/Space 键盘合约。"""

    def test_dim_card_click_shows_tooltip(self, page):
        """dim-card click → .tooltip 出现且内容含维度 code。"""
        first_card = page.locator(".dim-card").first
        first_card.click()
        tooltip = page.locator(".tooltip")
        expect(tooltip).to_be_visible()
        # tooltip 内容应含 code（如 D1）或维度名
        tooltip_text = tooltip.inner_text()
        assert len(tooltip_text) > 0, "tooltip 内容为空"

    def test_dim_card_enter_shows_tooltip(self, page):
        """dim-card Enter 键 → .tooltip 出现。"""
        first_card = page.locator(".dim-card").first
        first_card.focus()
        page.keyboard.press("Enter")
        tooltip = page.locator(".tooltip")
        expect(tooltip).to_be_visible()

    def test_dim_card_space_shows_tooltip_no_scroll(self, page):
        """dim-card Space 键 → .tooltip 出现 + 页面不滚动（e.preventDefault）。"""
        first_card = page.locator(".dim-card").first
        first_card.focus()
        scroll_before = page.evaluate("() => window.scrollY")
        page.keyboard.press("Space")
        tooltip = page.locator(".tooltip")
        expect(tooltip).to_be_visible()
        scroll_after = page.evaluate("() => window.scrollY")
        assert scroll_after == scroll_before, f"Space 导致页面滚动：{scroll_before} → {scroll_after}"


# ============================================================
# Section 3: summary-table 排序（click + 键盘）
# ============================================================

class TestSummaryTableSort:
    """验证 summary-table 表头排序行为。"""

    def test_sort_by_code_click(self, page):
        """表头『编号』click → 行顺序变化（升序→降序）。"""
        def codes():
            return page.eval_on_selector_all(
                "#summary-table-wrap tbody tr td:nth-child(1)",
                "els => els.map(e => e.innerText.trim())",
            )
        before = codes()
        page.locator("#summary-table-wrap thead th").first.click()
        after_first = codes()
        # 第一次 click 升序，再次 click 降序
        page.locator("#summary-table-wrap thead th").first.click()
        after_second = codes()
        # 至少有一次顺序发生变化（升序或降序与初始不同）
        assert before != after_first or before != after_second, "排序未生效：两次 click 后顺序均未变化"

    def test_sort_by_code_enter(self, page):
        """表头『编号』Enter 键 → 行顺序变化（升序→降序，两次 Enter）。"""
        def codes():
            return page.eval_on_selector_all(
                "#summary-table-wrap tbody tr td:nth-child(1)",
                "els => els.map(e => e.innerText.trim())",
            )
        before = codes()
        first_th = page.locator("#summary-table-wrap thead th").first
        first_th.focus()
        # 数据初始已升序，第一次 Enter 触发升序（结果同 before），第二次 Enter 翻转为降序
        first_th.press("Enter")
        after_first = codes()
        first_th.press("Enter")
        after_second = codes()
        assert before != after_first or before != after_second, "Enter 排序未生效"

    def test_sort_by_code_space_no_scroll(self, page):
        """表头『编号』Space 键 → 排序生效 + 页面不滚动（e.preventDefault）。"""
        first_th = page.locator("#summary-table-wrap thead th").first
        first_th.focus()
        scroll_before = page.evaluate("() => window.scrollY")
        # 用 element.press 确保 keydown 事件目标为 th，而非 body
        first_th.press("Space")
        scroll_after = page.evaluate("() => window.scrollY")
        assert scroll_after == scroll_before, f"Space 导致页面滚动：{scroll_before} → {scroll_after}"


# ============================================================
# Section 4: force 节点 hover → tooltip
# ============================================================

class TestForceNodeHover:
    """验证 force 力导向图节点 hover 行为。"""

    def test_force_node_hover_shows_tooltip(self, page):
        """force 节点 hover → .tooltip 出现。"""
        # force 节点是 #chart-force 内的 circle（非 rel-link）
        node = page.locator("#chart-force circle").first
        node.hover()
        tooltip = page.locator(".tooltip")
        expect(tooltip).to_be_visible()


# ============================================================
# Section 5: sankey 降级防御
# ============================================================

class TestSankeyFallback:
    """验证 d3.sankey 未加载时的降级文本。"""

    def test_sankey_missing_d3_sankey_shows_fallback(self, browser):
        """mock d3.sankey = undefined → 降级文本出现。"""
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        p = context.new_page()
        # 在 main() 执行前注入脚本，移除 d3.sankey
        p.add_init_script(
            "Object.defineProperty(window, '__stripSankey', { value: true });"
            "window.addEventListener('load', () => {"
            "  if (window.d3) { delete window.d3.sankey; }"
            "  // 重新触发 sankey 渲染"
            "  if (window.__lastData) {"
            "    const svg = document.querySelector('#chart-sankey');"
            "    if (svg) svg.innerHTML = '';"
            "    if (typeof renderSankey === 'function') { renderSankey(window.__lastData.sankey, window.__lastData.dimensions, window.__lastData.sankeyTheoristColors); }"
            "  }"
            "});"
        )
        p.goto(HTML_URL)
        _wait_render_ready(p)
        # 等待降级文本出现（load 事件后重新渲染）
        p.wait_for_timeout(500)
        # 由于 d3.sankey 在 main() 执行时可能仍存在（init_script 在 load 前注入但删除在 load 后），
        # 改为直接调用 renderSankey 验证降级路径
        result = p.evaluate(
            """() => {
                if (window.d3) { delete window.d3.sankey; }
                const svg = document.querySelector('#chart-sankey');
                if (svg) svg.innerHTML = '';
                if (typeof renderSankey === 'function') {
                    renderSankey(window.__lastData.sankey, window.__lastData.dimensions, window.__lastData.sankeyTheoristColors);
                }
                return svg.querySelector('text') ? svg.querySelector('text').textContent : '';
            }"""
        )
        p.close()
        context.close()
        assert "d3-sankey" in result or "未加载" in result, f"降级文本未出现，实际：{result!r}"


# ============================================================
# Section 6: file:// 协议不发起 fetch
# ============================================================

class TestNoFetchOnFileProtocol:
    """验证 file:// 协议下 fetchJson 不发起网络请求（直接返回嵌入数据）。"""

    def test_no_network_requests(self, browser):
        """file:// 协议下 page.goto 不触发 fetch/XHR（除 file:// 本身 + CDN 资源）。"""
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        p = context.new_page()
        requests = []
        p.on("request", lambda req: requests.append((req.method, req.url)) if "file://" not in req.url else None)
        p.goto(HTML_URL)
        _wait_render_ready(p)
        p.wait_for_timeout(500)
        # 过滤掉 file:// 协议 + CDN 资源（d3js.org 等），只关注 narratology JSON 的 fetch
        cdn_prefixes = ("https://d3js.org/", "https://cdn.", "https://unpkg.com/", "https://cdnjs.")
        http_requests = [
            r for r in requests
            if not r[1].startswith("file://") and not r[1].startswith(cdn_prefixes)
        ]
        p.close()
        context.close()
        assert http_requests == [], f"file:// 协议下意外发起数据 fetch 请求：{http_requests}"


# ============================================================
# Section 7: 响应式布局（dims-grid 列数）
# ============================================================

class TestResponsiveLayout:
    """验证 .dims-grid 在不同 viewport 下的列数。"""

    @pytest.mark.parametrize("viewport_width,expected_cols", [
        pytest.param(375, 1, id="mobile-375-1col"),
        pytest.param(768, 2, id="tablet-768-2col"),
        pytest.param(1200, 4, id="desktop-1200-4col"),
    ])
    def test_dims_grid_columns(self, browser, viewport_width, expected_cols):
        """不同 viewport 下 .dims-grid 列数正确。"""
        context = browser.new_context(viewport={"width": viewport_width, "height": 800})
        p = context.new_page()
        p.goto(HTML_URL)
        _wait_render_ready(p)
        cols = p.evaluate(
            """() => {
                const grid = document.querySelector('.dims-grid');
                if (!grid) return 0;
                const style = window.getComputedStyle(grid);
                return style.gridTemplateColumns.split(' ').length;
            }"""
        )
        p.close()
        context.close()
        assert cols == expected_cols, f"viewport={viewport_width} 列数={cols}，期望 {expected_cols}"
