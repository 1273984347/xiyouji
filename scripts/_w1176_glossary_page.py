#!/usr/bin/env python3
"""_w1176_glossary_page.py — 术语表页内容填充（W1176）。

把 new_page.py 生成的骨架改造成真正的术语速查页：
  main 内容区 → KPI + 分组筛选 + 关键词搜索 + 术语卡片网格 + 完整对照表
  EMBEDDED_DATA → dataset/glossary.json 全量（6 组 59 条，含含义与书中用法）
  render() → 原生 JS 渲染（无图表，不需要 D3 逻辑）
  cite 块 → 第 28 槽 C3 引用格式（APA / GB/T 7714 / MLA 三项）

设计约束：
  · 不新增共享 CSS（system.css 是全站单一事实源，改动半径 851 页），本页样式全走页内
  · 数据源徽标由 w1167_badge_inject.py 注入（已跑），本脚本不重复写
  · 文案与字体走令牌，禁硬编码色（token 覆盖率门禁）

用法：
  py -3 scripts/_w1176_glossary_page.py --dry-run
  py -3 scripts/_w1176_glossary_page.py --apply
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "site", "data", "glossary.html")
DATA = os.path.join(ROOT, "dataset", "glossary.json")

PAGE_CSS = """
        /* W1176：术语表页私有样式（不进 system.css——共享层改动半径 851 页，此处按页限定） */
        .glossary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: var(--space-4);
            margin-top: var(--space-5);
        }
        .glossary-card {
            background: var(--paper);
            border: 1px solid var(--line);
            border-left: 3px solid var(--chart-1);
            border-radius: var(--radius-md);
            padding: var(--space-4);
            transition: box-shadow var(--dur-fast) var(--ease-out-quart), transform var(--dur-fast) var(--ease-out-quart);
        }
        .glossary-card:hover {
            box-shadow: var(--elev-2);
            transform: translateY(-2px);
        }
        .glossary-card .g-term {
            font-family: var(--font-serif);
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--ink);
            margin-bottom: var(--space-2);
        }
        .glossary-card .g-term .g-arrow { color: var(--chart-2); margin: 0 6px; }
        .glossary-card .g-term .g-canon { color: var(--accent); }
        .glossary-card .g-meaning {
            font-size: 0.9rem;
            color: var(--ink-soft);
            line-height: 1.7;
            margin-bottom: var(--space-2);
        }
        .glossary-card .g-usage {
            font-size: 0.82rem;
            color: var(--ink-faint);
            line-height: 1.6;
            padding-top: var(--space-2);
            border-top: 1px solid var(--line);
        }
        .glossary-card .g-group {
            display: inline-block;
            font-size: 0.72rem;
            padding: 2px 8px;
            border-radius: var(--radius-pill);
            background: var(--accent-tint);
            color: var(--accent);
            margin-bottom: var(--space-2);
        }
        .glossary-toolbar {
            display: flex;
            flex-wrap: wrap;
            gap: var(--space-3);
            align-items: center;
            margin-top: var(--space-4);
        }
        .glossary-count {
            font-size: 0.85rem;
            color: var(--ink-faint);
            margin-left: auto;
        }
        @media (max-width: 640px) {
            .glossary-grid { grid-template-columns: 1fr; }
        }
"""


def build_main(g: dict) -> str:
    groups = g["groups"]
    total = sum(len(x["entries"]) for x in groups)
    variant_n = sum(len(x["entries"]) for x in groups if x["type"] == "variant")
    term_n = total - variant_n

    tabs = [f'<button class="filter-tab active" data-group="all" role="tab" aria-selected="true">全部 {total}</button>']
    for grp in groups:
        short = re.sub(r"^[一二三四五六七八九十]+、", "", grp["name"])
        tabs.append(
            f'<button class="filter-tab" data-group="{grp["name"]}" role="tab" aria-selected="false">'
            f'{short} {len(grp["entries"])}</button>'
        )

    return f"""    <main class="container">

        <nav class="breadcrumb">
            <a href="../index.html">首页</a>
            <span class="sep">/</span>
            <a href="../dashboard.html">数据看板</a>
            <span class="sep">/</span>
            <span class="current">术语表 · 名物典故速查</span>
        </nav>

        <section class="kpi-row">
            <div class="kpi-card">
                <div class="label">术语分组</div>
                <div class="value">{len(groups)}</div>
                <div class="desc">人物称谓 / 佛道术语 / 回目 / 地理 / 法宝</div>
            </div>
            <div class="kpi-card">
                <div class="label">条目总数</div>
                <div class="value">{total}</div>
                <div class="desc">逐条附源表原文的含义与书中用法</div>
            </div>
            <div class="kpi-card">
                <div class="label">异名映射</div>
                <div class="value">{variant_n}</div>
                <div class="desc">心猿 / 意马 / 金公 / 木母 等归一到正名</div>
            </div>
            <div class="kpi-card">
                <div class="label">术语词条</div>
                <div class="value">{term_n}</div>
                <div class="desc">佛道 / 地理 / 法宝 / 回目结构</div>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">术语速查</h2>
            <div class="section-sub">
                点选分组或输入关键词过滤。人物称谓组展示「异名 → 正名」的内丹配属关系；
                其余各组保留源表的含义与书中用法两列。
            </div>

            <div class="filter-tabs" role="tablist" aria-label="术语分组筛选">
                {"".join(tabs)}
            </div>

            <div class="glossary-toolbar">
                <div class="search-box" style="flex:1;min-width:220px">
                    <input type="search" id="glossary-q" placeholder="搜索术语、异名或释义…" aria-label="搜索术语">
                </div>
                <div class="glossary-count" id="glossary-count" aria-live="polite">共 {total} 条</div>
            </div>

            <div class="glossary-grid" id="glossary-grid"></div>
            <div class="empty-state hidden" id="glossary-empty">未找到匹配的术语，换个关键词试试。</div>
        </section>

        <section class="section">
            <h2 class="section-title">完整对照表</h2>
            <div class="section-sub">与源文档 <code>docs/00-导读/术语表.md</code> 逐条对拍（<code>check_glossary.py</code> C1 校验）。</div>
            <div class="table-wrap">
                <table class="data-table" id="glossary-table">
                    <thead>
                        <tr><th>分组</th><th>术语 / 异名</th><th>指代 / 含义</th><th>出处 / 书中用法</th></tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        </section>

        <!-- 数据源区：第 28 槽 C1/C2/C4 的扫描锚点（判据按 <div id="dataSource"> 取区域文本，
             内部不可有嵌套 div——非贪婪匹配会截断） -->
        <div class="notice" id="dataSource">
            数据源：<code>dataset/glossary.json</code>（由 <code>scripts/check_glossary.py --generate</code> 从
            <code>docs/00-导读/术语表.md</code> 解析生成，参数与口径见生成脚本源；快照 2026-11-08）。
            本页数据以页面内嵌 EMBEDDED 方式随发布生成，离线可读，勿手改 JSON。
        </div>
        <div class="cite-block">
            <details class="cite-details">
                <summary>引用格式</summary>
                <div class="cite-item"><span>APA</span><pre class="cite-text">《详解西游记》项目. (2026). 术语表 · 名物典故速查. 详解西游记可视化站点. https://1273984347.github.io/xiyouji/data/glossary.html（访问日期 2026-11-08）</pre><button type="button" class="cite-copy">复制</button></div>
                <div class="cite-item"><span>GB/T</span><pre class="cite-text">《详解西游记》项目. 术语表 · 名物典故速查[EB/OL]. (2026)[2026-11-08]. https://1273984347.github.io/xiyouji/data/glossary.html.</pre><button type="button" class="cite-copy">复制</button></div>
                <div class="cite-item"><span>MLA</span><pre class="cite-text">"术语表 · 名物典故速查." 详解西游记可视化站点, 2026, 1273984347.github.io/xiyouji/data/glossary.html. Accessed 8 Nov. 2026.</pre><button class="cite-copy">复制</button></div>
            </details>
        </div>

    </main>"""


def build_js(g: dict) -> str:
    payload = json.dumps(g, ensure_ascii=False, separators=(",", ":"))
    return f"""        // ===== 数据：与 dataset/glossary.json 逐字节同源（check_glossary.py C1 对拍） =====
        const GLOSSARY = {payload};

        let curGroup = 'all';
        let curQuery = '';

        function esc(s) {{
            return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {{
                return {{ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }}[c];
            }});
        }}

        // 扁平化：每条附带所属组名与组类型，便于筛选与展示
        const FLAT = [];
        GLOSSARY.groups.forEach(function (grp) {{
            grp.entries.forEach(function (e) {{
                FLAT.push(Object.assign({{ _group: grp.name, _type: grp.type }}, e));
            }});
        }});

        function rowOf(e) {{
            if (e._type === 'variant') {{
                return {{
                    term: e.variants.join(' / '),
                    isVariant: true,
                    canonical: e.canonical,
                    meaning: '指代 ' + e.canonical,
                    usage: e.note || ''
                }};
            }}
            return {{ term: e.term, isVariant: false, canonical: '', meaning: e.meaning || '', usage: e.usage || '' }};
        }}

        function match(e, q) {{
            if (!q) return true;
            var r = rowOf(e);
            return (r.term + r.canonical + r.meaning + r.usage + e._group).toLowerCase().indexOf(q) >= 0;
        }}

        function render() {{
            var q = curQuery.trim().toLowerCase();
            var list = FLAT.filter(function (e) {{
                if (curGroup !== 'all' && e._group !== curGroup) return false;
                return match(e, q);
            }});

            var grid = document.getElementById('glossary-grid');
            var empty = document.getElementById('glossary-empty');
            var cnt = document.getElementById('glossary-count');
            var tbody = document.querySelector('#glossary-table tbody');

            grid.innerHTML = list.map(function (e) {{
                var r = rowOf(e);
                var termHtml = r.isVariant
                    ? esc(r.term) + '<span class="g-arrow">→</span><span class="g-canon">' + esc(r.canonical) + '</span>'
                    : esc(r.term);
                var usageHtml = r.usage ? '<div class="g-usage">' + esc(r.usage) + '</div>' : '';
                return '<article class="glossary-card">' +
                    '<span class="g-group">' + esc(e._group) + '</span>' +
                    '<div class="g-term">' + termHtml + '</div>' +
                    '<div class="g-meaning">' + esc(r.meaning) + '</div>' +
                    usageHtml +
                    '</article>';
            }}).join('');

            empty.classList.toggle('hidden', list.length > 0);
            cnt.textContent = '共 ' + list.length + ' 条';

            tbody.innerHTML = list.map(function (e) {{
                var r = rowOf(e);
                var first = r.isVariant
                    ? esc(r.term) + ' → ' + esc(r.canonical)
                    : esc(r.term);
                var second = r.isVariant ? esc(r.canonical) : esc(r.meaning);
                var third = esc(r.usage);
                return '<tr><td>' + esc(e._group) + '</td><td>' + first + '</td><td>' + second + '</td><td>' + third + '</td></tr>';
            }}).join('');
        }}

        document.querySelectorAll('.filter-tab').forEach(function (tab) {{
            tab.addEventListener('click', function () {{
                document.querySelectorAll('.filter-tab').forEach(function (t) {{
                    t.classList.remove('active');
                    t.setAttribute('aria-selected', 'false');
                }});
                tab.classList.add('active');
                tab.setAttribute('aria-selected', 'true');
                curGroup = tab.dataset.group || 'all';
                render();
            }});
        }});

        var qEl = document.getElementById('glossary-q');
        var timer = null;
        qEl.addEventListener('input', function () {{
            clearTimeout(timer);
            timer = setTimeout(function () {{
                curQuery = qEl.value;
                render();
            }}, 120);
        }});

        render();"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dry = not args.apply

    if not os.path.exists(PAGE):
        print(f"FAIL 缺页面骨架：{PAGE}（先跑 new_page.py）")
        return 1
    g = json.load(open(DATA, encoding="utf-8"))

    s = open(PAGE, encoding="utf-8").read()

    # 1) 替换 main 内容
    m = re.search(r"    <main class=\"container\">.*?\n    </main>", s, re.S)
    if not m:
        print("FAIL 未找到 <main>...</main> 区间")
        return 1
    new_main = build_main(g)
    s = s[: m.start()] + new_main + s[m.end():]

    # 2) 替换 EMBEDDED_DATA 与渲染逻辑（从 EMBEDDED_DATA 到 render(EMBEDDED_DATA);）
    m2 = re.search(r"        const EMBEDDED_DATA = \[.*?render\(EMBEDDED_DATA\);", s, re.S)
    if not m2:
        print("FAIL 未找到 EMBEDDED_DATA / render 区间")
        return 1
    s = s[: m2.start()] + build_js(g) + s[m2.end():]

    # 3) 页内私有 CSS：插到最后一个 </style> 前
    if ".glossary-grid {" not in s:
        i = s.rfind("</style>")
        if i < 0:
            print("FAIL 未找到 </style>")
            return 1
        s = s[:i] + PAGE_CSS + s[i:]

    # 断言：行数与关键结构
    if s.count('<main class="container">') != 1 or s.count("</main>") != 1:
        print("FAIL main 结构异常")
        return 1
    if "const GLOSSARY =" not in s or "function render()" not in s:
        print("FAIL 脚本替换未生效")
        return 1

    if dry:
        print(f"[DRY] 页面将写入 {os.path.relpath(PAGE, ROOT)} · {len(s.splitlines())} 行 · "
              f"数据 {sum(len(x['entries']) for x in g['groups'])} 条")
        return 0

    with open(PAGE, "wb") as fh:  # 字节级写（避免 Windows CRLF 污染 · E-11 第三种形态）
        fh.write(s.encode("utf-8"))
    print(f"[OK] {os.path.relpath(PAGE, ROOT)} 已填充 · {len(s.splitlines())} 行 · "
          f"{sum(len(x['entries']) for x in g['groups'])} 条术语")
    return 0


if __name__ == "__main__":
    sys.exit(main())
