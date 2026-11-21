#!/usr/bin/env python3
"""check_chart_content_completeness.py — 第 82 门禁 · 图表内容完备度（W1266 线 A1 · 建尺子）

背景：现役 875 页中 171 页含图表、716 个图表。既有门禁覆盖的是**渲染层与数据层**
（第 29/30/77/78/80 槽：色相可分辨 · 窄屏降级声明 · 视觉身份 · EN 数据源语言隔离 ·
SVG 文字对比度），**没有任何一道门禁问过「这张图有没有说清楚它要说什么」**——
即数据来源标注、结论段、tooltip、图例这四项**内容层**要素。
本槽（第 82 槽）只判**内容完备度**（读者能否读懂这张图），
**不判视觉质量**（对比度/裁切/色彩可辨另有其槽）。

扫描范围：site/ 根 + site/data + site/en 的 .html（与第 30 槽同口径：_shell/_template 跳过）。
  含图页口径：页内存在任一图表载体 —— <svg> / <canvas> 元素 · 图表容器 class
  （chart|graph|plot|viz|visualization 前缀族）· 图表库调用（d3 选图 / Chart / echarts）。
  非含图页不参与四项判据。

判据（每项写明：方向 / 阈值 / 下限 / 触发时机 / 豁免条件）：

  C1 数据来源标注（方向：页内必须有**人眼可读**的来源/口径说明文本）
     候选块：①自身有直接文本的叶子块（普通段落里的来源说明）②来源语义容器
       （class 或 id 命中 source/cite/provenance 词表，含 id="dataSource" / class="source-note"）
       —— 取其**完整可见文本**（路径常被 <code> 包住，只看直接文本会丢锚点；超过 600 字符
       的容器退回直接文本，避免整页文本被当成一条来源说明）。
     阈值：候选文本块须**同时**命中
         · 来源语义词表（数据来源|数据源|来源|出处|口径|Source:|Sources:|based on|
           derived from|drawn from|grounded in …）
         · 真值源锚点词表（.json/.csv 路径 · site/data/json · dataset/ · scripts/ ·
           《…》书名 · 西游记|吴承恩|Wu Cheng'en|原文|本项目|数据集 …）
       ⇒ 两表交集 = 「口径说明能定位到真值源」。
     下限：归一化后文本长度 ≥ 8 字符（短于此不足以承载来源与锚点）。
     触发时机：每页每判据各判一次（页面级·非图元级）。
     豁免：**无**（任何含图页都必须能说清数据从哪来）。
     反例（明确不算数）：仅出现 HTML 属性名（data-source=""）或 CSS 类名（.source-note）
       而无可提取的文本内容 —— 属性名与类名不是读者看得见的说明。

  C2 结论/洞察段（方向：页内必须有**处于可识别结论区块**的结论性文本段）
     结论区块识别（任一即成）：
       a) 元素 class 命中结论语义词表（insight|conclusion|takeaway|finding|synthesis|
          summary|interpretation|reading-note …）⇒ 区块语义由 class 承担；
       b) <figcaption> 图注 ⇒ 但其文本须**自身**命中结论语义词表（纯图题不算结论）；
       c) 容器元素内标题（h1-h6）命中结论语义词表（结论|洞察|解读|小结|要点|启示|
          Key Insights|Conclusion|Takeaways|Findings|Synthesis|Interpretation …）。
     下限：区块内容（**去掉标题后的**可见文本——标题本身不算结论内容）归一化长度 ≥ 8 字符；
       **或**该区块内元素 id 在 <script> 中被写入内容
       （d3 渲染的结论列表：静态 HTML 为空壳，浏览器里有内容 —— 空壳不算有结论）。
     触发时机：页面级；页内存在 ≥1 个「有内容的结论区块」即 PASS。
     豁免：无（本判据不因页面类型豁免）。
     反伪命中：正文里恰好出现「结论」二字而所在 section 标题/区块 class 均不命中结论语义
       ⇒ **不计数**（结论语义必须落在结论区块上）。

  C3 tooltip（方向：图元可查细节）
     三条通路任一即 PASS：
       A. <title> 子元素挂在 **<svg> 内的图形元素**（g|rect|circle|ellipse|path|polyline|
          polygon|line|text|use|image）上且文本非空 ——
          <head><title> 是**页面标题**不是图元提示，不算；
       B. <svg> 内的图形元素带非空 title 属性（浏览器原生悬停提示）；
       C. <script> 内存在**绑定到图元**的 tooltip 语句：在命中处**前后各 400 字符**的窗口内
          同时命中「tooltip 写入/事件模式」（.append('title') · .title( · on('mouseover'|
          'mousemove'|'mouseenter')·**pointer 族同义**（pointerover|pointermove|
          pointerenter|pointerleave））与「图元选择器」（svg|rect|circle|ellipse|path|polyline|
          polygon|bar|arc|node|point|series|slice|wedge|dot）。
     下限：通路 A/B 的文本/属性值长度 ≥ 1（空 title 不算可查细节）。
     触发时机：页面级。
     豁免：无。
     **「有 tooltip 代码但没绑定到图元」如何处理**：不算 PASS ——
       仅写 .chart-tooltip{…} CSS 规则、仅出现 "tooltip" 字样（注释/类名字符串）、
       或事件只挂在非图元元素（按钮/链接）上而窗口内无图元选择器 ⇒ 判 C3 违例。

  C4 图例（方向：多系列图必有图例）
     系列数 series_count（页面级·可静态观测的上限）：
       S1 图例静态项数（class 命中 legend-item|legend-cell|legend-label|legend-swatch|
          legend-key|legend-entry 的元素数）；
       S2 <script> 内多系列证据：series|datasets|groups 数组字面量 ≥2 项，
          或 .range([...]) / .domain([...]) 数组字面量 ≥2 项；
       S3 静态 SVG 内不同 fill/stroke 色值数 ≥2（排除图例容器内元素）。
       series_count = max(S1, S2, S3)。
     阈值：series_count ≥ 2 ⇒ 多系列 ⇒ **必须**有图例，否则 C4 违例。
     图例存在判定：存在 class 命中 legend 词表的元素 L，且
       · L 内图例项数 ≥1（静态）或
       · L 的可见文本长度 ≥2（纯文本图例）或
       · L 内元素 id 在 <script> 中被写入内容（JS 渲染图例）。
     下限：图例项 ≥1 项（单色块无标签不算图例）。
     触发时机：页面级。
     豁免：**单系列图显式豁免**，豁免清单入库在
       scripts/output/chart-legend-exemptions.txt（每行 <页面>|<声明>|<依据>）。
       声明四类（静态口径 + 渲染级口径，二者互为交叉校验）：
         series=1  静态实测明确单系列（须与静态实测一致）；
         series=0  静态不可判定（图元 JS 渲染·静态证据为零）；
         render=nochart         渲染级复核：无图表容器（本无图·仅图标/插画）⇒ 图例判据不适用；
         render=unknown         渲染级复核：静态有图表容器/图表库调用但渲染后无图表 svg
                                （file:// 下数据未加载 ⇒ 渲染失败）⇒ 渲染级不可判定；
         render=legend          渲染级复核：多系列且可见图例齐备（≥2 项）；
         render=single          渲染级复核：单系列；
         render=multi-nolegend  渲染级复核：多系列且**无**可见图例 ⇒ **不豁免**·判 C4。
       render=* 声明须与**渲染复核档案** scripts/output/chart-legend-render-audit.json
       的 verdict 完全一致 ⇒ 改清单或改页面都骗不过（双向校验：声明↔档案 verdict、
       档案↔页面内容哈希 sha）。
       渲染级分类口径见 RENDER_RULEBOOK（按渲染后图元实证分类·非 id/class 关键词单判）：
       页面级三分类 has_chart（真有图）/ env_blocked（环境性未加载·不计入真无图）/
       no_chart（真无图）——「真无图」与「环境性未加载」必须分开记，不得混算。
       豁免条目缺依据字段 / 声明与实测或档案不符 ⇒ 豁免无效（记 C5）。

  C5 单系列图未登记豁免（方向：单系列图须显式豁免登记，不靠默认放过）
     触发时机：页面级·series_count ≤ 1 且页内无图例时。
     豁免：仅 scripts/output/chart-legend-exemptions.txt 内登记且复核通过者。

输出（自上而下·末行格式恒定）：
  扫描行   扫描页数 · 含图页数 · 违例条数 · 存量基线条数 · 基线外新增条数
  四项缺口行 无来源 / 无结论 / 无 tooltip / 无图例（多系列无图例 + 单系列未登记豁免）页数
  末行     ---- 第 82 门禁 图表内容完备度：N FAIL ----（N = 基线外新增数·0 亦照此格式）

模式：门禁默认「基线冻结」（基线内记「存量基线」不计 FAIL；基线外新增 = FAIL）；
      零容忍 --strict（基线不参与判定）；--report 只报数·退出码 0；
      --generate-baseline 生成基线；--generate-exemptions 生成豁免清单初版。
      **fail-closed**：扫描页数 = 0 或含图页数 = 0 ⇒ 判红（探针没跑到任何页不许静默通过）；
      基线文件缺失 / 豁免清单缺失 / 渲染复核档案缺失 ⇒ 判红（拒绝通过）。

用法：
  py -3 scripts/check_chart_content_completeness.py                # 门禁（基线冻结）
  py -3 scripts/check_chart_content_completeness.py --strict       # 零容忍
  py -3 scripts/check_chart_content_completeness.py --report       # 只报数·退出码 0
  py -3 scripts/check_chart_content_completeness.py --generate-baseline
  py -3 scripts/check_chart_content_completeness.py --generate-exemptions
  py -3 scripts/output/_w1266_render_legend.py    # 渲染级复核（Playwright file://·只读渲染·不改页面）
  py -3 scripts/check_chart_content_completeness.py --self-test
退出码：0 通过 / 1 违例或基础设施缺失（fail-closed）/ 2 自测失败
末行恒为：---- 第 82 门禁 图表内容完备度：N FAIL ----
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from lib import freeze_gate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MARKER = "---- 第 82 门禁 图表内容完备度："
BASELINE = ROOT / "scripts" / "output" / "chart-content-baseline.txt"
EXEMPTIONS = ROOT / "scripts" / "output" / "chart-legend-exemptions.txt"
RENDER_AUDIT = ROOT / "scripts" / "output" / "chart-legend-render-audit.json"
RENDER_VERDICTS = {
    "render=nochart": "nochart",
    "render=unknown": "unknown",
    "render=legend": "multi_legend",
    "render=single": "single",
    "render=multi-nolegend": "multi_nolegend",
}
SKIP_STEMS = ("_shell", "_template")

_VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}
_SKIP_TEXT_TAGS = {"script", "style", "noscript", "template"}
_AXIS_HINT_RE = re.compile(r"axis|grid|tick|domain|frame|rule", re.I)  # W1277 P3-3
_MIN_TEXT = 8
_JS_WINDOW = 400


# ---------------------------------------------------------------- 极简 DOM
class _Node:
    """极简 DOM 节点（只保留判据需要的 tag / attrs / 直接文本 / 子节点）。"""

    __slots__ = ("tag", "attrs", "children", "text", "parent")

    def __init__(self, tag, attrs, parent):
        self.tag = tag
        self.attrs = attrs
        self.children = []
        self.text = ""
        self.parent = parent


class _DomParser(HTMLParser):
    """容错 HTML 解析器：只取结构与文本，不做 CSS 计算。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = _Node("#root", {}, None)
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = _Node(tag, dict(attrs), self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in _VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(_Node(tag, dict(attrs), self.stack[-1]))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].text += data


def parse_html(html: str) -> _Node:
    """解析 HTML → 根节点。"""
    dom = _DomParser()
    dom.feed(html)
    dom.close()
    return dom.root


def iter_nodes(node: _Node):
    """深度优先遍历（含节点自身）。"""
    yield node
    for child in node.children:
        yield from iter_nodes(child)


def norm(text: str) -> str:
    """归一化空白。"""
    return re.sub(r"\s+", " ", text or "").strip()


def own_text(node: _Node) -> str:
    """元素的**直接**文本（不含子元素文本）——文本块判定的基本单位。"""
    if node.tag in _SKIP_TEXT_TAGS:
        return ""
    return norm(node.text)


def visible_text(node: _Node) -> str:
    """元素的可见文本（递归·跳过 script/style/noscript/template）。"""
    out: list[str] = []

    def rec(n: _Node) -> None:
        if n.tag in _SKIP_TEXT_TAGS:
            return
        if n.text:
            out.append(n.text)
        for child in n.children:
            rec(child)

    rec(node)
    return norm(" ".join(out))


def class_tokens(node: _Node) -> list[str]:
    return (node.attrs.get("class") or "").split()


def node_id(node: _Node) -> str:
    return node.attrs.get("id") or ""


def script_text(nodes) -> str:
    """所有 <script> 的原始文本拼接（供脚本侧证据判定）。"""
    return "\n".join(n.text for n in nodes if n.tag == "script")


# ---------------------------------------------------------------- 词表
CHART_CLASS_RE = re.compile(r"^(chart|graph|plot|viz|visualization|data-viz|echarts|d3)([-_].*)?$", re.I)
CHART_LIB_RE = re.compile(
    r"d3\.(select|selectAll)\(\s*['\"][^'\"]*(chart|graph|plot|svg|#)|new\s+Chart\(|echarts\.\w+\(|Chart\(",
    re.I,
)
SOURCE_CLASS_RE = re.compile(r"(^|[-_ ])(source|sources|provenance|citation|cite|credits?)([-_ ]|$)", re.I)
SOURCE_ID_RE = re.compile(r"^(data-?source|source-?note|source-?line|data-?provenance|cite-?(box|block|note)?|provenance)$", re.I)
SOURCE_TEXT_RE = re.compile(
    r"(数据来源|数据源|资料来源|来源\s*[:：]|来源|出处\s*[:：]|出处|数据出处|来源说明|数据口径|统计口径|"
    r"口径\s*[:：]|数据依据|data\s*source|data-source|source\s*[:：]|sources?\s*[:：]|based\s+on|derived\s+from|"
    r"drawn\s+from|grounded\s+in|provenance)",
    re.I,
)
TRUTHY_RE = re.compile(
    r"(\.json\b|\.csv\b|\.tsv\b|site/data/json|data/json|/json/|dataset/|scripts/|github\.com|"
    r"《[^》]{1,24}》|西游记|吴承恩|Wu Cheng'en|原文|本项目|项目统计|本仓库|数据集|公开数据|文献)",
    re.I,
)
CONCLUSION_CLASS_RE = re.compile(
    r"(^|[-_ ])(insight|insights|conclusion|conclusions|takeaway|takeaways|key-?insight|key-?takeaway|"
    r"finding|findings|synthesis|synthesis-note|summary|summaries|interpretation|reading-note)([-_ ]|$)",
    re.I,
)
CONCLUSION_TEXT_RE = re.compile(
    r"(结论|洞察|解读|小结|要点|启示|要义|综述|key\s*insights?|insights?|conclusions?|"
    r"takeaways?|findings?|synthesis|interpretation)",
    re.I,
)
LEGEND_CLASS_RE = re.compile(r"(^|[-_ ])(legend|legends)([-_ ]|$)", re.I)
LEGEND_ITEM_CLASS_RE = re.compile(
    r"(^|[-_ ])(legend-item|legend-cell|legend-label|legend-swatch|legend-key|legend-entry)([-_ ]|$)", re.I,
)
TOOLTIP_WRITE_RE = re.compile(
    r"\.append\(\s*['\"]title['\"]\s*\)|\.title\(\s*['\"\`]|"
    r"(?:on|addEventListener)\(\s*['\"](?:mouse|pointer)(?:over|move|enter|leave)['\"]",
    re.I,
)
CHART_SELECTOR_RE = re.compile(
    r"\b(svg|rect|circle|ellipse|path|polyline|polygon|bar|arc|node|point|series|slice|wedge|dot)\b", re.I,
)
JS_WRITE_RE = re.compile(
    r"\.(?:text|html|append|appendChild|prepend|insertAdjacentHTML)\s*\(|\.innerHTML\s*=", re.I,
)
MULTI_SERIES_JS_RE = re.compile(
    r"(?:series|datasets|groups|seriesKeys)\s*[:=]\s*\[([^\]]*)\]|"
    r"\.(?:range|domain)\(\s*\[([^\]]*)\]",
    re.I,
)
_GRAPHIC_TAGS = {"svg", "rect", "circle", "ellipse", "path", "polyline", "polygon", "line", "g", "text", "use"}
_TITLE_HOST_TAGS = {"g", "rect", "circle", "ellipse", "path", "polyline", "polygon", "line", "text", "use", "image"}


# ---------------------------------------------------------------- 工具
def _count_items(text: str) -> int:
    """数组字面量文本 → 元素数（空数组 0；单元素无逗号 1）。"""
    t = text.strip()
    if not t:
        return 0
    return len([x for x in t.split(",") if x.strip()])


def js_bound_content(script: str, ident: str) -> bool:
    """id 是否在 <script> 中被写入内容（400 字符窗口命中写入模式）。

    用于「d3 渲染的结论列表 / 图例：静态 HTML 是空壳，浏览器里才有内容」。
    """
    if not ident or len(ident) < 2:
        return False
    pat = re.compile(r"#\s*" + re.escape(ident) + r"\b|['\"]" + re.escape(ident) + r"['\"]")
    for m in pat.finditer(script):
        window = script[m.end(): m.end() + _JS_WINDOW]
        if JS_WRITE_RE.search(window):
            return True
    return False


def _in_svg(node: _Node) -> bool:
    """节点是否位于 <svg> 之内（<head><title> 页面标题因此被排除）。"""
    cur = node.parent
    while cur is not None:
        if cur.tag == "svg":
            return True
        cur = cur.parent
    return False


def _in_legend(node: _Node) -> bool:
    """节点是否位于图例容器内（图例 swatch 的颜色不计入系列色计数）。"""
    cur = node.parent
    while cur is not None:
        if LEGEND_CLASS_RE.search(" ".join(class_tokens(cur))):
            return True
        cur = cur.parent
    return False


# ---------------------------------------------------------------- 判据
def chart_evidence(nodes, html: str) -> tuple[bool, bool, bool]:
    """静态图表证据 → (有任意 svg/canvas, 有图表语义 class, 有图表库调用)。

    供渲染级复核区分两种「渲染后无图」：本无图（只有图标 svg）vs
    渲染失败（静态有图表容器/图表库调用·但渲染后无图表 svg ⇒ 数据未加载）。
    """
    has_svg = any(n.tag in ("svg", "canvas") for n in nodes)
    has_cls = any(CHART_CLASS_RE.search(" ".join(class_tokens(n))) for n in nodes)
    has_lib = bool(CHART_LIB_RE.search(html))
    return has_svg, has_cls, has_lib


def is_chart_page(nodes, html: str) -> bool:
    """含图页判定：svg / canvas / 图表容器 class / 图表库调用。"""
    has_svg, has_cls, has_lib = chart_evidence(nodes, html)
    return has_svg or has_cls or has_lib


# ---------------------------------------------------------------- 渲染级分类口径
CHART_MIN_W = 120
CHART_MIN_H = 80
CHART_WORD_RE = re.compile(r"chart|graph|plot|viz|visual|sankey|network|heatmap|matrix|timeline|radar|pie|donut", re.I)
RENDER_RULEBOOK = (
    "渲染级分类口径 v2（修正 v1「按 id/class 关键词单判」的错误——JS 动态创建的图表 svg 无 chart 类名）："
    "· 尺寸门槛：w ≥ 120 且 h ≥ 80 = 可承载图表的画布；小于此 = 图标尺度；"
    "· chart（图表）：画布达标 且（可见文本标签 ≥1 或 数据图元 ≥3 或 id/class 命中图表词表）；"
    "· illustration（装饰插画）：画布达标 但（无文本 且 图元 ≤2 且未命中图表词表）⇒ 不计图表；"
    "· small_graph（迷你图）：画布不达标 但（文本 ≥1 或图元 ≥3）；"
    "· icon（图标）：画布不达标 且（图元 ≤2 且无文本）；"
    "· 页面级三分类：has_chart（有图表 svg）/ env_blocked（静态有图表语义但渲染后无图表 svg ⇒"
    "环境性未加载·file:// fetch 失败等 ⇒ 不计入真无图）/ no_chart（只有图标或插画且静态无图表语义 ⇒ 真无图）"
)


def classify_svg(svg: dict) -> tuple[str, str]:
    """渲染级 svg 分类 → (类别, 依据)。类别: chart / small_graph / illustration / icon。"""
    w = svg.get("w", 0)
    h = svg.get("h", 0)
    marks = svg.get("marks", 0)
    texts = svg.get("texts", 0)
    word = bool(CHART_WORD_RE.search("%s %s" % (svg.get("cls", ""), svg.get("id", ""))))
    if w >= CHART_MIN_W and h >= CHART_MIN_H:
        if texts >= 1 or marks >= 3 or word:
            extra = "·命中图表词表" if word else ""
            return ("chart", "%dx%d·图元 %d·文本 %d%s" % (w, h, marks, texts, extra))
        return ("illustration", "%dx%d·图元 %d·无文本且未命中图表词表 ⇒ 装饰插画" % (w, h, marks))
    if texts >= 1:
        return ("small_graph", "%dx%d·图元 %d·文本 %d（小尺寸图表）" % (w, h, marks, texts))
    return ("icon", "%dx%d·图元 %d·无文本（小尺寸·无文本 ⇒ 图标）" % (w, h, marks))


def page_chart_verdict(svgs: list, static_cls: bool, static_lib: bool) -> tuple[str, str, list]:
    """页面级渲染结论 → (结论, 依据, 逐 svg 分类明细)。

    结论: has_chart（真有图）/ env_blocked（环境性未加载）/ no_chart（真无图）。
    """
    kinds = []
    charts = []
    for s in svgs:
        kind, basis = classify_svg(s)
        kinds.append({"cls": s.get("cls", "")[:40], "id": s.get("id", "")[:40],
                      "w": s.get("w", 0), "h": s.get("h", 0), "marks": s.get("marks", 0),
                      "texts": s.get("texts", 0), "kind": kind, "basis": basis})
        if kind in ("chart", "small_graph"):
            charts.append(kinds[-1])
    if charts:
        return ("has_chart", "渲染后有图表 svg %d 个（最大者：%s）" % (len(charts), charts[0]["basis"]), kinds)
    if static_cls or static_lib:
        return (
            "env_blocked",
            "渲染后无图表 svg·但静态有图表语义容器/图表库调用 ⇒ 环境性未加载（file:// fetch 失败等）⇒ 不计入真无图",
            kinds,
        )
    return ("no_chart", "渲染后无图表 svg·全部 svg 为图标/插画且静态无图表语义 ⇒ 真无图", kinds)


def render_series_evidence(svgs: list) -> tuple[int, str]:
    """渲染级系列数证据 → (证据值, 说明)：取图表 svg 的 填充色组/描边色组/堆叠段 最大值。"""
    best = 0
    parts = []
    for s in svgs:
        kind, _ = classify_svg(s)
        if kind not in ("chart", "small_graph"):
            continue
        f = len(s.get("fills", []))
        st = len(s.get("strokes", []))
        sk = s.get("stackMax", 0)
        v = max(f, st, sk)
        if v > best:
            best = v
            parts = ["填充色组 %d·描边色组 %d·同 x 堆叠段 %d" % (f, st, sk)]
    return (best, "；".join(parts))


def source_evidence(nodes) -> tuple[bool, str]:
    """C1 数据来源标注 → (是否有可见来源说明且能定位真值源, 证据文本)。

    候选块 = ①自身有直接文本的叶子块（普通段落里的来源说明）②来源语义容器
    （class 或 id 命中 source/cite/provenance 词表）—— 取其**完整可见文本**
    （路径常被 <code> 包住，只看直接文本会丢锚点）。
    """
    for n in nodes:
        if n.tag in _SKIP_TEXT_TAGS:
            continue
        own = own_text(n)
        is_src_block = bool(
            SOURCE_CLASS_RE.search(" ".join(class_tokens(n))) or SOURCE_ID_RE.search(node_id(n))
        )
        if not own and not is_src_block:
            continue
        text = visible_text(n)
        if len(text) > 600:
            text = own
        if len(text) < _MIN_TEXT:
            continue
        if SOURCE_TEXT_RE.search(text) and TRUTHY_RE.search(text):
            return True, text[:80]
    return False, ""


_HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")
_CONTAINER_TAGS = ("section", "article", "div", "main", "aside", "header", "details")


def _is_conclusion_heading(node: _Node) -> bool:
    """标题元素本身是否命中结论语义词表（正文里的「结论」二字不算）。"""
    if node.tag not in _HEADING_TAGS:
        return False
    title = visible_text(node)
    return bool(title) and bool(CONCLUSION_TEXT_RE.search(title))


def _container_has_conclusion_heading(node: _Node) -> bool:
    """容器内（任意深度）是否有命中结论语义的标题。"""
    return any(_is_conclusion_heading(d) for d in iter_nodes(node))


def _conclusion_blocks(nodes) -> list[tuple[_Node, bool]]:
    """结论区块 → [(节点, 是否需自身命中结论语义词)]。"""
    out: list[tuple[_Node, bool]] = []
    for n in nodes:
        if n.tag == "figcaption":
            out.append((n, True))
            continue
        if CONCLUSION_CLASS_RE.search(" ".join(class_tokens(n))):
            out.append((n, False))
            continue
        if n.tag in _CONTAINER_TAGS and _container_has_conclusion_heading(n):
            out.append((n, False))
    return out


def visible_text_without_headings(node: _Node) -> str:
    """可见文本·排除标题（h1-h6）——结论区块的**内容**不得是区块自己的标题。"""
    out: list[str] = []

    def rec(n: _Node) -> None:
        if n.tag in _SKIP_TEXT_TAGS or n.tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            return
        if n.text:
            out.append(n.text)
        for child in n.children:
            rec(child)

    rec(node)
    return norm(" ".join(out))


def conclusion_evidence(nodes, script: str) -> tuple[bool, str]:
    """C2 结论/洞察段 → (是否有处于结论区块的结论性文本段, 证据)。"""
    for node, need_text_sem in _conclusion_blocks(nodes):
        text = visible_text(node)
        if need_text_sem:
            # 图注：自身须命中结论语义词，且内容非空
            if not CONCLUSION_TEXT_RE.search(text):
                continue
            if len(text) >= _MIN_TEXT:
                return True, text[:80]
            continue
        # class/标题命中的区块：内容 = 去掉标题后的可见文本
        body = visible_text_without_headings(node)
        if len(body) >= _MIN_TEXT:
            return True, body[:80]
        for d in iter_nodes(node):
            ident = node_id(d)
            if ident and js_bound_content(script, ident):
                return True, "js:%s" % ident
    return False, ""


def tooltip_evidence(nodes, script: str) -> tuple[bool, str]:
    """C3 tooltip → (图元是否可查细节, 证据)。"""
    for n in nodes:
        if n.tag != "title" or not norm(n.text):
            continue
        host = n.parent
        if host is not None and host.tag in _TITLE_HOST_TAGS and _in_svg(n):
            return True, "svg-title:%s" % norm(n.text)[:40]
    for n in nodes:
        if n.tag not in _TITLE_HOST_TAGS or not _in_svg(n):
            continue
        title = (n.attrs.get("title") or "").strip()
        if title:
            return True, "title-attr:%s" % title[:40]
    for m in TOOLTIP_WRITE_RE.finditer(script):
        window = script[max(0, m.start() - _JS_WINDOW): m.end() + _JS_WINDOW]
        if CHART_SELECTOR_RE.search(window):
            return True, "js-bind:%s" % norm(window)[:60]
    return False, ""


def legend_evidence(nodes, script: str) -> tuple[int, bool, bool, str]:
    """C4/C5 图例 → (series_count, 是否多系列, 是否已有图例, 证据)。

    series_count = max(S1 图例项数, S2 脚本多系列证据, S3 静态 SVG 色数)。
    """
    legend_nodes = [n for n in nodes if LEGEND_CLASS_RE.search(" ".join(class_tokens(n)))]
    item_count = 0
    has_legend = False
    for lg in legend_nodes:
        items = [
            d for d in iter_nodes(lg)
            if LEGEND_ITEM_CLASS_RE.search(" ".join(class_tokens(d)))
        ]
        item_count = max(item_count, len(items))
        if items:
            has_legend = True
        elif len(visible_text(lg)) >= 2:
            has_legend = True
        else:
            for d in iter_nodes(lg):
                ident = node_id(d)
                if ident and js_bound_content(script, ident):
                    has_legend = True
                    break
            if has_legend:
                break
    s2 = 0
    for m in MULTI_SERIES_JS_RE.finditer(script):
        s2 = max(s2, _count_items(m.group(1) or m.group(2) or ""))
    s3 = 0
    colors = set()
    for n in nodes:
        if n.tag in _SKIP_TEXT_TAGS or _in_legend(n):
            continue
        # W1277 对抗审查 P3-3 修：轴/网格/标尺形态（line 元素·axis/grid/tick 命名）不计入
        # 系列色——轴色计入曾使 series_count 虚高进基线
        _ident = " ".join(filter(None, [node_id(n), n.attrs.get("class"), n.attrs.get("id")]))
        if n.tag == "line" or _AXIS_HINT_RE.search(_ident or ""):
            continue
        for attr in ("fill", "stroke"):
            val = (n.attrs.get(attr) or "").strip().lower()
            if val and val not in ("none", "currentcolor", "transparent", "inherit"):
                colors.add((attr, val))
    s3 = len(colors)
    series_count = max(item_count, s2, s3)
    evidence = "legend_items=%d js_multi=%d svg_colors=%d" % (item_count, s2, s3)
    return series_count, series_count >= 2, has_legend, evidence


# ---------------------------------------------------------------- 扫描
def scan_pages(scope: str = "all") -> list[Path]:
    """枚举待扫页面（scope: all / en / zh）。"""
    out: list[Path] = []
    if scope in ("zh", "all"):
        for d in (ROOT / "site" / "data", ROOT / "site"):
            if d.is_dir():
                out.extend(p for p in sorted(d.glob("*.html")) if p.stem not in SKIP_STEMS)
    if scope in ("en", "all"):
        d = ROOT / "site" / "en"
        if d.is_dir():
            out.extend(p for p in sorted(d.glob("*.html")) if p.stem not in SKIP_STEMS)
    seen: set[str] = set()
    uniq: list[Path] = []
    for p in out:
        rel = p.relative_to(ROOT).as_posix()
        if rel in seen:
            continue
        seen.add(rel)
        uniq.append(p)
    return uniq


def analyze_html(html: str) -> dict:
    """分析一页 HTML → 四项判据读数（纯函数·可注入·不改真实文件）。"""
    root = parse_html(html)
    nodes = list(iter_nodes(root))
    script = script_text(nodes)
    src_ok, src_ev = source_evidence(nodes)
    con_ok, con_ev = conclusion_evidence(nodes, script)
    tip_ok, tip_ev = tooltip_evidence(nodes, script)
    series, multi, has_legend, leg_ev = legend_evidence(nodes, script)
    return {
        "is_chart_page": is_chart_page(nodes, html),
        "source": (src_ok, src_ev),
        "conclusion": (con_ok, con_ev),
        "tooltip": (tip_ok, tip_ev),
        # 判据码别名（单测与自测按 C1/C2/C3 取值）
        "C1": (src_ok, src_ev),
        "C2": (con_ok, con_ev),
        "C3": (tip_ok, tip_ev),
        "legend": (series, multi, has_legend, leg_ev),
        "script": script,
    }


def read_exemptions(path: Path) -> tuple[dict[str, str], list[str]]:
    """读豁免清单 → ({页面相对路径: 依据}, 问题列表)。"""
    if not path.exists():
        return {}, ["豁免清单缺失: %s（fail-closed·拒绝通过）" % path]
    mapping: dict[str, str] = {}
    problems: list[str] = []
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        return {}, ["豁免清单不可读: %s（%s）" % (path, exc)]
    for lineno, line in enumerate(raw.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split("|")
        if len(parts) < 3:
            problems.append("豁免条目格式非法（第 %d 行·须 <页面>|<系列数声明>|<依据>）: %s" % (lineno, s[:60]))
            continue
        rel, series_spec, reason = parts[0].strip(), parts[1].strip(), parts[2].strip()
        if not reason:
            problems.append("豁免条目缺依据（第 %d 行）: %s" % (lineno, rel))
            continue
        mapping[rel] = "%s|%s" % (series_spec, reason)
    return mapping, problems


def read_render_audit(path: Path) -> tuple[dict, list[str]]:
    """读渲染级复核档案 → ({页面: {verdict, basis}}, 问题列表)。缺失 → fail-closed。"""
    if not path.exists():
        return {}, ["渲染复核档案缺失: %s（fail-closed·拒绝通过）" % path]
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {}, ["渲染复核档案不可读: %s（%s）" % (path, exc)]
    out = {}
    rows = raw.get("rows") if isinstance(raw, dict) else raw
    for row in rows or []:
        rel = row.get("page")
        if rel:
            out[rel] = {
                "verdict": row.get("verdict"),
                "basis": row.get("basis", ""),
                "sha": row.get("sha", ""),
            }
    return out, []


def _page_sha(path: Path) -> str:
    """页面内容哈希前 12 位（渲染档案的防漂移锚点）。

    W1286：**按仓内规范（LF）归一后计算**——`.gitattributes` 声明 `* text=auto eol=lf`
    ⇒ 仓内 blob 恒为 LF，而 Windows 工作树因 `core.autocrlf=true` 检出为 CRLF
    ⇒ 直接 `read_bytes()` 会让「本地算的 sha」与「CI 上 blob 的 sha」永不相等
    ⇒ 渲染档案在 CI 上恒被判「过期」（实证 about.html：本地 309d118255fa / CI f917041c34ea）。
    ⇒ 归一后两侧同口径 ⇒ 跨平台可复现。
    """
    raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(raw).hexdigest()[:12]


def _resolve_legend_exemption(rel: str, spec: str, series: int, audit: dict, page_sha: str = "") -> tuple[str, str]:
    """豁免声明 → (状态, 细节)。状态: exempt / c4 / invalid。

    防绕过三道闸：
      ① render=* 声明须与**渲染复核档案**的 verdict 完全一致；
      ② 档案记录的页面内容哈希须与当前页面一致（页面一改·豁免自动失效·
         强制重跑渲染复核）⇒ 改页面骗不过；
      ③ 改清单本身：声明与档案不符即失效 ⇒ 改清单也骗不过。"""
    if spec in RENDER_VERDICTS:
        row = audit.get(rel) or {}
        actual = row.get("verdict")
        recorded_sha = row.get("sha") or ""
        if page_sha and (not recorded_sha or recorded_sha != page_sha):
            # W1277 对抗审查 P3-2 修：缺 sha 的档案行原样放行豁免（fail-open 弱点）⇒
            # 一律判 invalid（档案不可信·须重跑渲染复核补 sha）
            return ("invalid", "渲染档案过期或缺 sha（页 %s≠%s）·须重跑渲染复核" % (recorded_sha or "无", page_sha))
        if actual == RENDER_VERDICTS[spec]:
            if spec == "render=multi-nolegend":
                return ("c4", "渲染级复核：多系列且无可见图例")
            return ("exempt", "渲染级复核 verdict=%s" % actual)
        return ("invalid", "声明 %s·渲染级复核为 %s" % (spec, actual or "缺档"))
    if spec.startswith("series="):
        if _exemption_valid(spec, series):
            # W1271 对抗审查 P1-2 修：series=* 分支同样接渲染档案——档案新鲜（sha 一致）
            # 且 verdict=multi_nolegend ⇒ 渲染级实证多系列无图例，声明 series=N 不构成豁免
            # （docstring「改清单也骗不过」对本分支成立）。
            row = audit.get(rel) or {}
            rsha = row.get("sha") or ""
            verdict = row.get("verdict") or ""
            if rsha and page_sha and rsha == page_sha and verdict == "multi_nolegend":
                return ("c4", "渲染级复核：多系列且无可见图例（series=* 声明与档案 verdict 冲突）")
            return ("exempt", "静态实测 series=%d" % series)
        return ("invalid", "声明 %s·静态实测 series=%d" % (spec, series))
    return ("invalid", "声明不可解析：%s" % spec)


def scan(scope: str = "all", exem_path: Path | None = None) -> dict:
    """扫描 → 结果字典（含违例键、统计、fail-closed 标记）。"""
    pages = scan_pages(scope)
    exemptions, exem_problems = read_exemptions(exem_path or EXEMPTIONS)
    audit, audit_problems = read_render_audit(RENDER_AUDIT)
    viol: list[str] = []
    chart_pages = 0
    stats = {"C1": 0, "C2": 0, "C3": 0, "C4": 0, "C5": 0}
    exempt_used: set[str] = set()
    triggered: set[str] = set()
    stale_exemptions: list[str] = []
    for p in pages:
        rel = p.relative_to(ROOT).as_posix()
        html = p.read_text(encoding="utf-8", errors="ignore")
        res = analyze_html(html)
        if not res["is_chart_page"]:
            continue
        chart_pages += 1
        src_ok = res["source"][0]
        con_ok = res["conclusion"][0]
        tip_ok = res["tooltip"][0]
        series, multi, has_legend, _ = res["legend"]
        if not src_ok:
            viol.append("%s|C1|缺可读数据来源标注" % rel)
            stats["C1"] += 1
        if not con_ok:
            viol.append("%s|C2|缺结论/洞察段" % rel)
            stats["C2"] += 1
        if not tip_ok:
            viol.append("%s|C3|图表元素无 tooltip 可查细节" % rel)
            stats["C3"] += 1
        if multi and not has_legend:
            viol.append("%s|C4|多系列图（series=%d）无图例" % (rel, series))
            stats["C4"] += 1
        elif not multi and not has_legend:
            entry = exemptions.get(rel)
            spec = entry.split("|", 1)[0].strip() if entry else ""
            status, detail = _resolve_legend_exemption(rel, spec, series, audit, _page_sha(p))
            if status == "exempt":
                exempt_used.add(rel)
                triggered.add(rel)
            elif status == "c4":
                viol.append("%s|C4|多系列图无图例（%s）" % (rel, detail))
                stats["C4"] += 1
                triggered.add(rel)
            elif status == "invalid":
                stale_exemptions.append("%s（%s）" % (rel, detail))
                viol.append("%s|C5|图例豁免无效（%s）" % (rel, detail))
                stats["C5"] += 1
            else:
                viol.append("%s|C5|单系列图未登记图例豁免（series=%d）" % (rel, series))
                stats["C5"] += 1
    for rel in exemptions:
        if rel not in triggered and rel not in stale_exemptions:
            stale_exemptions.append("%s（登记项未被触发）" % rel)
    return {
        "viol": viol,
        "pages": len(pages),
        "chart_pages": chart_pages,
        "stats": stats,
        "fail_closed": (len(pages) == 0) or (chart_pages == 0),
        "exem_problems": exem_problems + audit_problems,
        "stale_exemptions": stale_exemptions,
        "exempt_used": sorted(exempt_used),
    }


# ---------------------------------------------------------------- 自测
_SELF_TEST_CASES: list[tuple[str, str, str, bool]] = [
    (
        "C1-正样本-可见来源文本含真值源",
        '<div class="source-note">数据来源：site/data/json/character-relationship-3d.json</div>',
        "C1",
        True,
    ),
    (
        "C1-负样本-只有属性名无可见文本",
        '<div class="chart" data-source="site/data/json/x.json"><span>图</span></div>',
        "C1",
        False,
    ),
    (
        "C1-负样本-只有 CSS 类名无文本",
        '<style>.source-note{color:red}</style><div class="source-note"></div>',
        "C1",
        False,
    ),
    (
        "C1-负样本-有来源语义但无真值源锚点",
        "<p>数据来源：见相关说明</p>",
        "C1",
        False,
    ),
    (
        "C2-正样本-标题命中结论语义且有正文",
        "<section><h2>Key Insights</h2><p>三个趋势显示……</p></section>",
        "C2",
        True,
    ),
    (
        "C2-负样本-正文提到结论二字（伪命中）",
        "<section><h2>数据概览</h2><p>本章结论将在后文给出。</p></section>",
        "C2",
        False,
    ),
    (
        "C2-负样本-结论区块存在但无内容",
        '<section><h2>Key Insights</h2><div class="insight-box"></div></section>',
        "C2",
        False,
    ),
    (
        "C2-正样本-JS 渲染的结论列表",
        '<div class="insight-box"><ul id="insights"></ul></div>'
        "<script>d3.select('#insights').selectAll('li').data(rows).enter().append('li').text(d => d);</script>",
        "C2",
        True,
    ),
    (
        "C3-正样本-SVG title 子元素",
        "<svg><g><title>唐僧 81 难</title></g></svg>",
        "C3",
        True,
    ),
    (
        "C3-正样本-title 属性",
        '<svg><rect x="1" y="1" width="4" height="4" title="灵山势力 42"></rect></svg>',
        "C3",
        True,
    ),
    (
        "C3-负样本-只有 tooltip CSS 无绑定",
        "<style>.chart-tooltip{position:absolute}</style><svg><rect/></svg>",
        "C3",
        False,
    ),
    (
        "C3-负样本-tooltip 绑定在非图元上",
        "<script>document.querySelector('.btn').on('mouseover', function(){ show('tooltip'); });</script>",
        "C3",
        False,
    ),
]


def self_test() -> int:
    """内存负样本自证：违例必红·正样本必绿·基线语义正确·零命中 fail-closed。"""
    bad = 0
    total = 0
    for name, html, key, expect_ok in _SELF_TEST_CASES:
        total += 1
        res = analyze_html(html)
        got = res[key][0]
        ok = got == expect_ok
        print("%s %s：期望 %s·实得 %s" % ("OK  " if ok else "FAIL", name, expect_ok, got))
        bad += 0 if ok else 1

    # 图例判据（多系列无图例 ⇒ FAIL；多系列有图例 ⇒ PASS）
    multi_html = "<script>d3.scaleOrdinal().range(['#a','#b']);</script><div class='chart'></div>"
    total += 1
    res = analyze_html(multi_html)
    series, multi, has_legend, _ = res["legend"]
    ok = multi and not has_legend
    print("%s C4-负样本-多系列无图例（series=%d·multi=%s·legend=%s）" % ("OK  " if ok else "FAIL", series, multi, has_legend))
    bad += 0 if ok else 1
    total += 1
    legend_html = (
        "<script>d3.scaleOrdinal().range(['#a','#b']);</script>"
        '<div class="chart"><div class="legend"><span class="legend-item">天庭</span>'
        '<span class="legend-item">灵山</span></div></div>'
    )
    res = analyze_html(legend_html)
    series, multi, has_legend, _ = res["legend"]
    ok = multi and has_legend
    print("%s C4-正样本-多系列有图例（series=%d·multi=%s·legend=%s）" % ("OK  " if ok else "FAIL", series, multi, has_legend))
    bad += 0 if ok else 1

    # 豁免语义：登记 series=1 且实测 1 ⇒ 豁免有效；实测 ≥2 ⇒ 豁免失效
    total += 1
    ok = _exemption_valid("series=1", 1)
    print("%s 豁免-实测单系列 ⇒ 豁免有效" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    total += 1
    ok = not _exemption_valid("series=1", 2)
    print("%s 豁免-实测多系列 ⇒ 豁免失效（防绕过）" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    total += 1
    ok = not _exemption_valid("series=2", 1)
    print("%s 豁免-声明与实测不符 ⇒ 豁免失效" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    total += 1
    ok = _exemption_valid("series=0", 0)
    print("%s 豁免-静态不可判定（series=0）⇒ 豁免有效" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1

    # 基线语义（共用 freeze_gate）
    viol = ["site/data/x.html|C1|缺可读数据来源标注"]
    total += 1
    res = freeze_gate.evaluate(viol, set(viol), strict=False)
    ok = not res["new_fail"]
    print("%s 基线内违例不计 FAIL" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    total += 1
    res = freeze_gate.evaluate(viol, set(), strict=False)
    ok = len(res["new_fail"]) == 1
    print("%s 基线外新增违例计 FAIL" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    total += 1
    res = freeze_gate.evaluate(viol, set(viol), strict=True)
    ok = len(res["new_fail"]) == 1
    print("%s 零容忍模式存量全红" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1

    # fail-closed：扫描面为空 ⇒ 判红
    total += 1
    empty = scan(scope="none")
    ok = empty["fail_closed"] and empty["pages"] == 0
    print("%s 零命中 fail-closed（扫描页 0 ⇒ 判红）" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1

    print("自测 %d/%d 通过" % (total - bad, total))
    return 0 if bad == 0 else 2


def _exemption_valid(series_spec: str, measured_series: int) -> bool:
    """豁免是否有效：**声明须与实测完全一致**且实测 ≤1（单系列/静态不可判定）。

    series=1 = 明确单系列；series=0 = 静态不可判定（图元 JS 渲染·静态证据为零）。
    声明与实测不符 ⇒ 豁免失效（页面改多系列后自动失效 ⇒ 改页面骗不过判据）。
    """
    return series_spec.strip() == "series=%d" % measured_series and measured_series <= 1


# ---------------------------------------------------------------- CLI
def _parse_args(argv: list[str]) -> tuple[str, bool, bool, Path]:
    scope = "all"
    if "--scope" in argv:
        i = argv.index("--scope")
        if i + 1 < len(argv) and argv[i + 1] in ("zh", "en", "all"):
            scope = argv[i + 1]
    exem_path = EXEMPTIONS
    if "--exemptions" in argv:
        i = argv.index("--exemptions")
        if i + 1 < len(argv):
            exem_path = Path(argv[i + 1])
            if not exem_path.is_absolute():
                exem_path = ROOT / exem_path
    return scope, ("--strict" in argv), ("--report" in argv), exem_path


def _write_baseline(res) -> int:
    """--generate-baseline：把当前存量违例冻结成基线文件（口径注释随文件走·换人可复算）。"""
    n = freeze_gate.write_baseline_ratcheted(
        BASELINE,
        res["viol"],
        [
            "# 第 82 门禁 · 图表内容完备度基线（W1266 建立·存量违例冻结）",
            "# 生成命令：py -3 scripts/check_chart_content_completeness.py --generate-baseline",
            "# 豁免清单：scripts/output/chart-legend-exemptions.txt（单系列图图例豁免·入库文件）",
            "# 格式：<页面>|<判据码>|<细节>；C1=缺来源标注 C2=缺结论段 C3=缺 tooltip C4=多系列无图例 C5=单系列未登记豁免",
            "# 语义：基线内违例记「存量基线」不计 FAIL；基线外新增 = FAIL；零容忍：--strict",
        ],
        allow_grow=True,  # W1277 P3-1：CLI 显式动作即人工复核放行
    )
    print("基线已写入 %s（%d 条）" % (BASELINE, n))
    return 0


def _read_baseline_or_fail(report_only: bool):
    """读基线文件；缺失/不可用 ⇒ fail-closed（默认档判红·report 档仅提示并按空基线继续）。"""
    baseline, problems = freeze_gate.read_baseline(BASELINE)
    for p in problems:
        print(("NOTE " if report_only else "FAIL ") + p)
    if problems and not report_only:
        print("%s 0 FAIL（基线缺失·fail-closed）----" % MARKER)
        return None
    return set() if problems else baseline


def _exemptions_ok(res, report_only: bool) -> bool:
    """豁免清单可用性检查：清单缺失/不可用 ⇒ fail-closed（不静默放过）。"""
    for p in res["exem_problems"]:
        print(("NOTE " if report_only else "FAIL ") + p)
    if res["exem_problems"] and not report_only:
        print("%s 0 FAIL（豁免清单不可用·fail-closed）----" % MARKER)
        return False
    return True


def main() -> int:
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return self_test()
    scope, strict, report_only, exem_path = _parse_args(argv)

    if "--generate-exemptions" in argv:
        return generate_exemptions(scope, exem_path)

    res = scan(scope, exem_path)
    if res["fail_closed"]:
        print(
            "FAIL 扫描面为空：扫描 %d 页·含图页 %d 页（fail-closed·拒绝通过）" % (res["pages"], res["chart_pages"])
        )
        print("%s 0 FAIL（零命中·fail-closed）----" % MARKER)
        return 1

    if "--generate-baseline" in argv:
        return _write_baseline(res)

    baseline = _read_baseline_or_fail(report_only)
    if baseline is None:
        return 1
    if not _exemptions_ok(res, report_only):
        return 1

    ev = freeze_gate.evaluate(res["viol"], baseline, strict=strict)
    print(
        "扫描 %d 页（scope=%s）· 含图页 %d 页 · 违例 %d 条 · %s %d 条 · 基线外新增 %d 条 · %s"
        % (
            res["pages"], scope, res["chart_pages"], ev["total"],
            freeze_gate.FROZEN_LABEL, len(ev["frozen"]), len(ev["new_fail"]),
            "FAIL" if ev["new_fail"] else "OK",
        )
    )
    print(
        "四项缺口：无来源 %d 页 · 无结论 %d 页 · 无 tooltip %d 页 · 无图例 %d 页（多系列无图例 %d + 单系列未登记 %d）"
        % (res["stats"]["C1"], res["stats"]["C2"], res["stats"]["C3"],
           res["stats"]["C4"] + res["stats"]["C5"], res["stats"]["C4"], res["stats"]["C5"])
    )
    if res["stale_exemptions"]:
        print("NOTE 豁免清单复核未通过 %d 条：%s" % (len(res["stale_exemptions"]), " / ".join(res["stale_exemptions"][:6])))
    # 明细行**不以**「---- 第 82 门禁」开头：verify_delivery 的汇总行解析按 marker 前缀抓行，
    # 同前缀出现两行会被重复计数（门禁段自洽锁「实跑段数 == 声明段数」会不符）。
    print(
        "· 第 82 槽明细：违例 %d 条 · %s %d 条 · 基线外新增 %d 条 · %s"
        % (
            ev["total"],
            freeze_gate.FROZEN_LABEL,
            len(ev["frozen"]),
            len(ev["new_fail"]),
            "FAIL" if ev["new_fail"] else "OK",
        )
    )
    for k in ev["new_fail"][:12]:
        print("  ✗ 新增/未登记违例 " + k)
    if len(ev["new_fail"]) > 12:
        print("  …其余 %d 条略" % (len(ev["new_fail"]) - 12))
    if ev["frozen"]:
        print("  · %s（%d 条）：%s" % (freeze_gate.FROZEN_LABEL, len(ev["frozen"]), " / ".join(ev["frozen"][:4])))
    if ev["fixed"]:
        print(
            "  · 可收紧（基线内违例已消失 %d 条·建议删行）：%s"
            % (len(ev["fixed"]), " / ".join(ev["fixed"][:4]))
        )
    if strict:
        print("  · 零容忍模式（--strict）：基线不参与判定·全部违例计 FAIL")
    print("%s%d FAIL ----" % (MARKER, len(ev["new_fail"])))
    if report_only:
        return 0
    return 1 if ev["new_fail"] else 0


def generate_exemptions(scope: str, exem_path: Path) -> int:
    """生成豁免清单初版：单系列（series_count ≤1）且页内无图例的页面。

    每行 <页面>|<系列数声明>|<依据>；依据写明实测证据（可复核）。
    """
    pages = scan_pages(scope)
    audit, _ = read_render_audit(RENDER_AUDIT)
    lines: list[str] = []
    for p in pages:
        rel = p.relative_to(ROOT).as_posix()
        html = p.read_text(encoding="utf-8", errors="ignore")
        res = analyze_html(html)
        if not res["is_chart_page"]:
            continue
        series, multi, has_legend, evidence = res["legend"]
        if multi or has_legend:
            continue
        verdict = (audit.get(rel) or {}).get("verdict")
        if verdict:
            spec = {
                "nochart": "render=nochart",
                "unknown": "render=unknown",
                "multi_legend": "render=legend",
                "single": "render=single",
                "multi_nolegend": "render=multi-nolegend",
            }[verdict]
            basis = "渲染级复核（Playwright file://·只读渲染）：%s" % (audit[rel]["basis"])
            if verdict == "multi_nolegend":
                basis += " ⇒ 撤豁免·判 C4（渲染级复核确认）"
        else:
            spec = "series=%d" % series
            basis = "静态实测 series=%d（%s）·%s" % (
                series, evidence, "单系列图" if series == 1 else "静态不可判定（图元 JS 渲染）")
        lines.append("%s|%s|依据：%s" % (rel, spec, basis))
    exem_path.parent.mkdir(parents=True, exist_ok=True)
    header = [
        "# 第 82 门禁 · 单系列图图例豁免清单（W1266 建立·入库文件）",
        "# 生成命令：py -3 scripts/check_chart_content_completeness.py --generate-exemptions",
        "# 格式：<页面相对路径>|<声明>|<依据>",
        "# 声明四类：series=1（静态明确单系列）· series=0（静态不可判定）·",
        "#         render=nochart|legend|single|multi-nolegend（渲染级复核结论·须与档案一致）；",
        "# 渲染档案：scripts/output/chart-legend-render-audit.json（render=* 声明的一致性依据）",
        "# 语义：声明与实测/档案**完全一致**才豁免；render=multi-nolegend 不豁免·判 C4；",
        "#       页面改多系列或改清单都骗不过（双向校验）",
    ]
    exem_path.write_text("\n".join(header + lines) + "\n", encoding="utf-8")
    print("豁免清单已写入 %s（%d 条）" % (exem_path, len(lines)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
