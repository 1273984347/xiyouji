"""P6 编码复核：site/data 可视化页的视觉编码通道逐页清点（_ 工具不入库、不过门禁）。

用途：为 P6 论文（《艺术设计研究》投稿）第 3.3 节方法 / 第 4 节结果 / 第 5 节讨论提供可复算数据。

方法：
  1. 读取 site/data/*.html，排除模板壳 _shell.html
  2. 剥离 HTML 注释与 JS 注释（// 仅在前置非 : 且非 / 时剥离）后再匹配，消除裸子串误报
  3. 分三级签名：
     - 强签名 = 某类图表的确定性 API
     - 实现路径签名 = 渲染路径（Canvas2D）与命名型图表（雷达图，依赖变量命名，属弱证据）
     - 弱签名 = 辅助判读，不计入类型计数
  4. **区分「定义」与「使用」**：tokens.css / system.css 被内联进每一页，
     故在全页文本上匹配 --chart-N 或 .chart-tooltip 会得到 86/86 的假象——
     本脚本把色板使用与 tooltip 使用限定在**内联 <script> 区域**内统计（数据驱动用色与运行时调用），
     「页面内定义命中」单列一栏仅作对照，不进入结论。
  5. **令牌落地断裂检测**：统计 JS 内 `.attr("fill","#......")` 硬编码色值（去重并列色值），
     与 --chart-N 的 JS 使用量对照——用于识别设计令牌在渲染层的治理盲区。
  6. **SQ4 降级阶梯**（本次新增）：把非静态承载拆成两档并计量：
     - 交互承载 = tooltip / 标题属性中引用的、且属于本页数据字段的字段数（去重）
     - 控件承载 = 页面筛选控件数量（select / range / button）
     另记录 tooltip 文本字符总量，作为「交互层信息量」的量级代理。
     **字段识别为代理指标**：以本页 KEY_RE 抽出的键集合为候选，与 tooltip 模板内的标识符取交集，
     故会同时受两方面误差影响（键集合含配置键；模板内字段名可能与键名不同形）。
  7. 记录每类编码命中次数与首个偏移，保证可回溯

局限（须写入论文方法节）：
  - 正则基于 API 调用与命名，封装后或动态生成的编码会漏检；无签名不等于无编码
  - 雷达图签名依赖变量命名，属弱证据；强/弱分级为人工判定，判定表须随论文附出
  - EMBEDDED 键名去重数是「数据维度」的代理指标，与项目口径的 133 个数据维度不等价
  - SQ4 的字段数为交集代理，不等于真实承载维度；结论须用相对比较（页间/层间）而非绝对值

用法：
  py -3 scripts/_p6_encoding_audit.py [--json <out>] [--list-unclassified] [--sq4]
"""
import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "site" / "data"

HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
JS_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
JS_LINE_COMMENT = re.compile(r"(?<![:/])//[^\n]*")
INLINE_SCRIPT = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE)
THREE_SRC_RE = re.compile(r"three[\w.\-]*\.js", re.IGNORECASE)
KEY_RE = re.compile(r"[\"']([A-Za-z_][\w\-]*)[\"']\s*:")
FILL_HEX_RE = re.compile(r"""\.attr\(\s*["']fill["']\s*,\s*["'](#[0-9a-fA-F]{3,8})["']""")
# tooltip 承载：.html()/.text() 的字符串或模板实参（容忍箭头函数/函数表达式包裹）
TIP_CALL_RE = re.compile(
    r"""\.(?:html|text)\(\s*(?:function\s*\([^)]*\)\s*\{|\(?[A-Za-z_$][\w$]*\)?\s*=>)?\s*(`[^`]*`|"[^"]*"|'[^']*')""",
    re.DOTALL,
)
TIP_ATTR_RE = re.compile(r"""\.attr\(\s*["'](?:title|aria-label|data-tip)["']\s*,\s*(`[^`]*`|"[^"]*"|'[^']*')""")
# 广义承载：全页模板字面量与字符串中的字段引用（含经 helper 函数间接触发的 tooltip）
TEMPLATE_RE = re.compile(r"`[^`]*`", re.DOTALL)
QUOTED_RE = re.compile(r"""["'][^"'\n]{2,}["']""")
IDENT_RE = re.compile(r"[A-Za-z_$][\w$]*")
CONTROL_RE = re.compile(r"<select|<input[^>]*type=[\"']range[\"']|<button", re.IGNORECASE)

STRONG = {
    "力导向网络": r"forceSimulation\s*\(|forceLink\s*\(|forceManyBody\s*\(",
    "桑基流向": r"\.sankey\s*\(|d3\.sankey\s*\(",
    "矩形树图": r"\.treemap\s*\(",
    "层次树": r"d3\.hierarchy\s*\(|\.hierarchy\s*\(",
    "弦图": r"\.chord\s*\(",
    "饼/环形": r"d3\.pie\s*\(|d3\.arc\s*\(",
    "折线": r"d3\.line\s*\(",
    "面积": r"d3\.area\s*\(",
    "堆叠": r"d3\.stack\s*\(",
    "连续色阶/热力": r"scaleSequential\s*\(|scaleQuantize\s*\(",
    "地理投影": r"d3\.geo\w*|geoPath\s*\(|geoMercator|geoAlbers",
    "3D(Three)": r"new\s+THREE\.|THREE\.Scene|WebGLRenderer",
    "打包/分区": r"d3\.pack\s*\(|d3\.partition\s*\(",
    "词云": r"wordcloud|layout\.cloud",
}
# 实现路径签名：反映渲染路径而非图表类型（雷达图依赖变量命名，属弱证据，单独标注）
PATH_SIG = {
    "雷达图(命名)": r"\bradar[A-Za-z]*\b",
    "Canvas2D": r"getContext\(\s*[\"']2d[\"']",
}
# 弱签名：辅助判读，不计入图表类型计数（避免把通用工具误判为图表类型）
WEAK = {
    "比例尺Band/Ordinal": r"scaleBand\s*\(|scaleOrdinal\s*\(",
    "时间比例尺": r"scaleTime\s*\(|timeParse\s*\(|d3\.timeFormat",
    "线性比例尺": r"scaleLinear\s*\(",
    "矩形元素": r'\.append\(\s*["\']rect["\']',
    "圆元素": r'\.append\(\s*["\']circle["\']',
}
TOKENS = {f"chart-{i}": rf"--chart-{i}\b" for i in range(1, 7)}
# 运行时通道：tooltip / hover 绑定在内联脚本内统计（避免内联 CSS 定义造成的假象）
JS_USAGE = {
    "tooltip运行时": r"chart-tooltip|classed\(\s*['\"]visible",
    "hover绑定": r"mouseover|mouseenter|mousemove",
}
# 结构通道：控件与可达性属性落在 HTML，须全页统计（在 <script> 内搜会严重低估）
HTML_USAGE = {
    "筛选控件": r"<select|<input[^>]*type=[\"']range[\"']|<button",
    "可达性属性": r"tabindex|aria-",
    "键盘绑定": r"keydown|keyup",
}


def strip_comments(text: str) -> str:
    text = HTML_COMMENT.sub(" ", text)
    text = JS_BLOCK_COMMENT.sub(" ", text)
    return JS_LINE_COMMENT.sub(" ", text)


def scan(patterns: dict, code: str) -> dict:
    out = {}
    for name, pat in patterns.items():
        hits = [m.start() for m in re.finditer(pat, code)]
        if hits:
            out[name] = {"count": len(hits), "first_offset": hits[0]}
    return out


def sq4_probe(code: str, data_keys: set) -> dict:
    """降级阶梯：交互承载（tooltip/标题属性）与控件承载（筛选控件）。

    narrow = 仅 .html()/.text()/.attr(title) 直调中的字段引用（下限）
    broad  = 全页模板字面量与字符串中的字段引用（含经 helper 间接触发的 tooltip，更接近真实承载）
    """
    blocks = [m.group(1) for m in TIP_CALL_RE.finditer(code)]
    blocks += [m.group(1) for m in TIP_ATTR_RE.finditer(code)]
    refs: set = set()
    for b in blocks:
        body = b[1:-1] if len(b) >= 2 else b
        refs |= {i for i in IDENT_RE.findall(body) if i in data_keys}
    broad_blocks = TEMPLATE_RE.findall(code) + QUOTED_RE.findall(code)
    broad: set = set()
    for b in broad_blocks:
        body = b[1:-1] if len(b) >= 2 else b
        broad |= {i for i in IDENT_RE.findall(body) if i in data_keys}
    return {
        "tip_blocks": len(blocks),
        "tip_text_chars": sum(len(b) - 2 for b in blocks if len(b) >= 2),
        "interactive_field_refs": sorted(refs),
        "interactive_field_count": len(refs),
        "broad_field_refs": sorted(broad),
        "broad_field_count": len(broad),
        "control_count": len(CONTROL_RE.findall(code)),
    }


def audit_page(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    code = strip_comments(raw)
    inline_js = strip_comments("\n".join(INLINE_SCRIPT.findall(raw)))
    strong = scan(STRONG, code)
    fills = FILL_HEX_RE.findall(code)
    data_keys = {m.group(1) for m in KEY_RE.finditer(code)}
    sq4 = sq4_probe(code, data_keys)
    return {
        "page": path.name,
        "encodings": sorted(strong),
        "path_signatures": sorted(scan(PATH_SIG, code)),
        "n_encoding_types": len(strong),
        "encoding_hits": {k: v["count"] for k, v in strong.items()},
        "weak_signatures": sorted(scan(WEAK, code)),
        "token_used_in_js": sorted(scan(TOKENS, inline_js)),
        "token_defined_in_page": sorted(scan(TOKENS, code)),
        "js_channels": sorted(scan(JS_USAGE, inline_js)),
        "html_channels": sorted(scan(HTML_USAGE, code)),
        "hardcoded_fill_hex_count": len(fills),
        "hardcoded_fill_hex_values": sorted({v.upper() for v in fills}),
        "data_keys_proxy": len(data_keys),
        **sq4,
        "loads_three_lib": bool(THREE_SRC_RE.search(raw)),
        "naive_three_hit": "three" in raw.lower(),
    }


def bucket(n: int) -> str:
    return "0" if n == 0 else ("4+" if n >= 4 else str(n))


def median(xs: list) -> float:
    if not xs:
        return 0.0
    ys = sorted(xs)
    mid = len(ys) // 2
    return float(ys[mid]) if len(ys) % 2 else round((ys[mid - 1] + ys[mid]) / 2, 1)


def main() -> int:
    ap = argparse.ArgumentParser(description="P6 编码复核（_ 工具）")
    ap.add_argument("--json", default=str(ROOT / "scripts" / "output" / "_p6_encoding_audit.json"))
    ap.add_argument("--list-unclassified", action="store_true")
    ap.add_argument("--sq4", action="store_true", help="输出降级阶梯明细")
    ap.add_argument("--ladder-detail", action="store_true", help="按分层点名列出页面")
    args = ap.parse_args()

    pages = sorted(p for p in DATA_DIR.glob("*.html") if p.name != "_shell.html")
    rows = [audit_page(p) for p in pages]
    n = len(rows)

    dist: dict[str, int] = {}
    for r in rows:
        for e in r["encodings"]:
            dist[e] = dist.get(e, 0) + 1

    per_page = [r["n_encoding_types"] for r in rows]
    buckets: dict[str, int] = {}
    for c in per_page:
        b = bucket(c)
        buckets[b] = buckets.get(b, 0) + 1
    buckets = {k: buckets[k] for k in sorted(buckets, key=lambda x: (x != "0", x))}

    def col(field: str) -> dict:
        out: dict[str, int] = {}
        for r in rows:
            for v in r[field]:
                out[v] = out.get(v, 0) + 1
        return dict(sorted(out.items(), key=lambda kv: -kv[1]))

    unclassified = [r["page"] for r in rows if r["n_encoding_types"] == 0]
    hex_pages = [r for r in rows if r["hardcoded_fill_hex_count"]]
    all_hex: dict[str, int] = {}
    for r in hex_pages:
        for v in r["hardcoded_fill_hex_values"]:
            all_hex[v] = all_hex.get(v, 0) + 1

    # SQ4 降级阶梯：六层互斥分层（静态编码 → 交互承载 → 控件承载 → 无承载）
    LADDER_KEYS = (
        "静态编码+交互承载",
        "静态编码+仅控件承载",
        "静态编码·无任何承载",
        "仅交互承载·无静态签名",
        "仅控件承载·无静态签名",
        "静态签名未覆盖·且无承载标记",
    )
    ladder = dict.fromkeys(LADDER_KEYS, 0)
    ladder_broad = dict.fromkeys(LADDER_KEYS, 0)
    by_bucket: dict[str, list] = {k: [] for k in LADDER_KEYS}

    def tier_of(row: dict, field: str) -> str:
        has_enc = row["n_encoding_types"] > 0
        has_int = row[field] > 0
        has_ctl = row["control_count"] > 0
        if has_enc and has_int:
            return "静态编码+交互承载"
        if has_enc and has_ctl:
            return "静态编码+仅控件承载"
        if has_enc:
            return "静态编码·无任何承载"
        if has_int:
            return "仅交互承载·无静态签名"
        if has_ctl:
            return "仅控件承载·无静态签名"
        return "静态签名未覆盖·且无承载标记"

    for r in rows:
        key = tier_of(r, "interactive_field_count")
        ladder[key] += 1
        by_bucket[key].append(r["page"])
        ladder_broad[tier_of(r, "broad_field_count")] += 1
    assert sum(ladder.values()) == n and sum(ladder_broad.values()) == n, "降级阶梯分层须覆盖全部页面"
    enc_only = ladder["静态编码·无任何承载"]
    enc_only_broad = ladder_broad["静态编码·无任何承载"]
    enc_total = sum(1 for r in rows if r["n_encoding_types"] > 0)
    hover_no_payload = sum(1 for r in rows if "hover绑定" in r["js_channels"] and r["broad_field_count"] == 0)

    tip_counts = [r["interactive_field_count"] for r in rows if r["interactive_field_count"]]
    broad_counts = [r["broad_field_count"] for r in rows if r["broad_field_count"]]
    summary = {
        "generated_at": datetime.now(UTC).astimezone().isoformat(timespec="seconds"),
        "pages_scanned": n,
        "pages_with_strong_signature": n - len(unclassified),
        "pages_without_strong_signature": len(unclassified),
        "encoding_type_distribution": dict(sorted(dist.items(), key=lambda kv: -kv[1])),
        "path_signature_distribution": col("path_signatures"),
        "encoding_types_per_page_buckets": buckets,
        "avg_distinct_encoding_types_per_page": round(sum(per_page) / n, 2) if n else 0,
        "max_encoding_types_on_one_page": max(per_page) if per_page else 0,
        "token_used_in_js_pages": col("token_used_in_js"),
        "token_defined_in_page_pages": col("token_defined_in_page"),
        "js_channel_pages": col("js_channels"),
        "html_channel_pages": col("html_channels"),
        "hardcoded_fill_pages": len(hex_pages),
        "hardcoded_fill_occurrences": sum(r["hardcoded_fill_hex_count"] for r in rows),
        "hardcoded_fill_distinct_values": len(all_hex),
        "hardcoded_fill_top_values": dict(sorted(all_hex.items(), key=lambda kv: -kv[1])[:15]),
        "data_keys_proxy_total": sum(r["data_keys_proxy"] for r in rows),
        "naive_three_false_positive": sum(
            1 for r in rows if r["naive_three_hit"] and "3D(Three)" not in r["encodings"]
        ),
        # ---- SQ4 ----
        "sq4_ladder": ladder,
        "sq4_ladder_broad": ladder_broad,
        "sq4_ladder_pages": by_bucket,
        "sq4_encoding_pages": enc_total,
        "sq4_static_only_pages": enc_only,
        "sq4_static_only_pages_broad": enc_only_broad,
        "sq4_encoding_pages_without_payload_ratio": round(enc_only / enc_total, 3) if enc_total else 0,
        "sq4_encoding_pages_without_payload_ratio_broad": round(enc_only_broad / enc_total, 3) if enc_total else 0,
        "sq4_pages_with_interactive_payload": len(tip_counts),
        "sq4_pages_with_interactive_payload_broad": len(broad_counts),
        "sq4_interactive_field_median": median(tip_counts),
        "sq4_interactive_field_median_broad": median(broad_counts),
        "sq4_interactive_field_max": max(tip_counts) if tip_counts else 0,
        "sq4_hover_but_no_payload": hover_no_payload,
        "sq4_tip_block_total": sum(r["tip_blocks"] for r in rows),
        "sq4_tip_text_chars_total": sum(r["tip_text_chars"] for r in rows),
        "sq4_control_pages": sum(1 for r in rows if r["control_count"]),
    }

    Path(args.json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json).write_text(
        json.dumps({"summary": summary, "pages": rows}, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"扫描 {n} 页（排除模板壳 _shell.html）")
    print(f"有强编码签名：{summary['pages_with_strong_signature']} · 无签名待复核：{len(unclassified)}")
    print("图表类型分布（按覆盖页数）：")
    for k, v in summary["encoding_type_distribution"].items():
        print(f"  {k:<14} {v:>3} 页")
    print(f"实现路径签名：{summary['path_signature_distribution']}")
    print(f"单页编码类型数分布：{buckets} · 平均 {summary['avg_distinct_encoding_types_per_page']} 种/页")
    print(f"色板令牌【JS 内使用】：{summary['token_used_in_js_pages']}")
    print(f"色板令牌【页面内定义·对照不结论】：{summary['token_defined_in_page_pages']}")
    print(f"运行时通道【JS】：{summary['js_channel_pages']}")
    print(f"结构通道【全页】：{summary['html_channel_pages']}")
    print(
        f"JS 硬编码填充色：{summary['hardcoded_fill_pages']} 页 · "
        f"{summary['hardcoded_fill_occurrences']} 处 · 去重 {summary['hardcoded_fill_distinct_values']} 色"
    )
    print(f"  高频色值：{summary['hardcoded_fill_top_values']}")
    print("---- SQ4 降级阶梯 ----")
    print(f"狭义分层（tooltip 直调）：{summary['sq4_ladder']}")
    print(f"广义分层（全模板/字符串）：{summary['sq4_ladder_broad']}")
    print(
        f"有静态编码 {enc_total} 页 → 无任何非静态承载：狭义 {enc_only} 页"
        f"（{summary['sq4_encoding_pages_without_payload_ratio'] * 100:.0f}%）· "
        f"广义 {enc_only_broad} 页（{summary['sq4_encoding_pages_without_payload_ratio_broad'] * 100:.0f}%）"
    )
    print(
        f"交互承载页数：狭义 {summary['sq4_pages_with_interactive_payload']} · "
        f"广义 {summary['sq4_pages_with_interactive_payload_broad']} · "
        f"字段中位 狭义 {summary['sq4_interactive_field_median']} / 广义 {summary['sq4_interactive_field_median_broad']}"
        f" · 最大 {summary['sq4_interactive_field_max']}"
    )
    print(f"绑定 hover 但广义仍未检出字段承载：{hover_no_payload} 页（测量边界提示）")
    print(
        f"tooltip 块 {summary['sq4_tip_block_total']} 个 · 文本合计 {summary['sq4_tip_text_chars_total']} 字符 · "
        f"带筛选控件 {summary['sq4_control_pages']} 页"
    )
    print(f"数据键名去重合计（代理指标）：{summary['data_keys_proxy_total']}")
    print(f"grep 误报对照：裸子串 three 命中但未渲染 3D = {summary['naive_three_false_positive']} 页")
    if args.list_unclassified:
        print("无强签名页面：")
        for p in unclassified:
            print("  " + p)
    if args.sq4:
        print("降级阶梯明细（交互承载字段数降序）：")
        for r in sorted(rows, key=lambda x: -x["interactive_field_count"])[:20]:
            print(
                f"  {r['page']:<44} 静态类型={r['n_encoding_types']} "
                f"交互字段={r['interactive_field_count']:>2} 控件={r['control_count']:>2} "
                f"数据键={r['data_keys_proxy']:>3}"
            )
    if args.ladder_detail:
        print("分层点名：")
        for k in LADDER_KEYS:
            pages_ = by_bucket[k]
            print(f"  [{k}] {len(pages_)} 页")
            for p in pages_:
                print("      " + p)
    print(f"明细已写入 {Path(args.json).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
