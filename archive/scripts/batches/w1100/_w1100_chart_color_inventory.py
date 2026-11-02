# -*- coding: utf-8 -*-
"""W1100 图表色工程盘点（只读批·零页面改动）。

产两件事：
A. **档 3 落层分类**（互斥归类·每处只归一层，避免 W1089 口径「各形态独立计数」
   导致同一处被多形态重复计数的口径漂移）：
   L1 D3 .attr/.style(fill|stroke)   —— 前两档（已归零，仅作对照）
   L2 echarts 配置色                 —— (color|colors|palette|itemStyle|backgroundColor|
                                        borderColor) : [ "HEX" ]（库自解析颜色串）
   L3 Canvas ctx.fillStyle/strokeStyle
   L4 通用 CSS 属性值                —— (fill|stroke|color|background|...)[:=]"HEX"
   L5 裸 hex 字面量（未被上四层捕获）—— 再分「调色板色」与「页面自有 hex」
B. **全站补偿规则形态盘点**（<style> 内）：
   C1 前缀型   svg path[fill^="#"]      —— 令牌化后失配（E-86/E-88 已证）
   C2 字面值型 svg [fill="#xxx" i]      —— 令牌化后失配（特异性可能压过类规则）
   C3 其它按属性匹配的补偿选择器
逐页统计 + 切批建议。ROOT 向上自动查找仓库根（归档后仍可跑）。
"""
import collections
import io
import json
import os
import pathlib
import re
import sys

HEX12 = ["C8463A", "E46250", "3A6B8C", "6B8E5A", "B38F58", "D8CFBC",
         "8A6D3B", "E9B885", "7FA8C9", "E0604F", "C9A96B", "9DB98A"]
PAL = set(h.lower() for h in HEX12)
ANY_HEX = r"#[0-9a-fA-F]{6}"

# 互斥优先级：从上到下，先命中者归类
LAYERS = [
    ("L1 D3 .attr/.style(fill|stroke)",
     re.compile(r"\.(?:attr|style)\(\s*['\"](fill|stroke)['\"]\s*,\s*['\"](" + ANY_HEX + r")", re.I)),
    ("L2 echarts 配置色",
     re.compile(r"(color|colors|palette|itemStyle|backgroundColor|borderColor)\s*:\s*\[?\s*['\"](" + ANY_HEX + r")", re.I)),
    ("L3 Canvas fillStyle/strokeStyle",
     re.compile(r"(fillStyle|strokeStyle)\s*=\s*['\"](" + ANY_HEX + r")", re.I)),
    ("L4 通用 CSS 属性值",
     re.compile(r"(color|background|backgroundColor|borderColor|fill|stroke)\s*[:=]\s*['\"](" + ANY_HEX + r")", re.I)),
    ("L5 裸 hex 字面量",
     re.compile(r"['\"](" + ANY_HEX + r")", re.I)),
]

# 补偿规则（按属性字面值匹配 ⇒ 令牌化后失配）
COMP = [
    ("C1 前缀型 [fill^=\"#\"]", re.compile(r"\[fill\^=", re.I)),
    ("C2 字面值型 [fill=\"#..\" i]", re.compile(r"\[fill\s*=\s*['\"]?#", re.I)),
    ("C3 其它按属性匹配的补偿选择器", re.compile(r"\[(fill|stroke)\b", re.I)),
]


def find_root(start):
    p = pathlib.Path(start).resolve()
    for cand in [p] + list(p.parents):
        if (cand / "site").is_dir() and (cand / "scripts").is_dir():
            return cand
    raise SystemExit("未找到仓库根")


def classify(js):
    """返回 [(层名, hex, 上下文)]（互斥·先命中者归类）。"""
    taken = []
    spans = []
    for name, rx in LAYERS:
        for m in rx.finditer(js):
            gi = m.re.groups          # 末组恒为 hex（L5 只有一个组）
            s, e = m.span(gi)
            if any(not (e <= a or s >= b) for a, b in spans):
                continue
            spans.append((s, e))
            taken.append((name, m.group(gi).lower(), " ".join(js[max(0, m.start() - 40):m.end() + 8].split())[:110]))
    taken.sort(key=lambda x: x[2].find(" "))
    return taken


def main():
    root = find_root(pathlib.Path(__file__).resolve().parent)
    site = root / "site"
    layer_pages = collections.defaultdict(collections.Counter)
    layer_totals = collections.Counter()
    layer_split = collections.Counter()      # (层, 类别) -> 处数
    pal_vs_own = collections.Counter()
    comp_pages = collections.Counter()
    comp_kind = collections.Counter()
    per_page_layers = collections.defaultdict(collections.Counter)
    per_page_split = collections.defaultdict(collections.Counter)
    comp_detail = {}

    for dirpath, _d, files in os.walk(site):
        if any(p.startswith(".") for p in dirpath.split(os.path.sep)):
            continue
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = pathlib.Path(dirpath) / fn
            rel = str(p.relative_to(site)).replace("\\", "/")
            txt = p.read_text(encoding="utf-8", errors="ignore")

            # A. 脚本内颜色字面量
            for m in re.finditer(r"<script\b[^>]*>(.*?)</script>", txt, re.S):
                for name, hexv, ctx in classify(m.group(1)):
                    cat = "调色板色" if hexv[1:] in PAL else "页面自有 hex"
                    layer_totals[name] += 1
                    layer_split[(name, cat)] += 1
                    layer_pages[name][rel] += 1
                    per_page_layers[rel][name] += 1
                    per_page_split[rel][cat] += 1
                    pal_vs_own[cat] += 1

            # B. 样式内补偿规则
            styles = "\n".join(m.group(1) for m in
                               re.finditer(r"<style\b[^>]*>(.*?)</style>", txt, re.S))
            if not styles.strip():
                continue
            hits = []
            for name, rx in COMP:
                n = len(rx.findall(styles))
                if n:
                    comp_kind[name] += n
                    comp_pages[rel] += n
                    hits.append((name, n))
            if hits:
                comp_detail[rel] = hits

    out = {
        "layers_total": dict(layer_totals),
        "layers_pages": {k: dict(v) for k, v in layer_pages.items()},
        "bare_hex_split": dict(pal_vs_own),
        "layer_split": {"%s|%s" % k: v for k, v in layer_split.items()},
        "per_page_split": {k: dict(v) for k, v in per_page_split.items()},
        "comp_total": dict(comp_kind),
        "comp_pages_top": dict(comp_pages.most_common(30)),
        "comp_page_count": len(comp_pages),
        "comp_detail": comp_detail,
        "per_page_layers": {k: dict(v) for k, v in per_page_layers.items()},
    }
    dst = root / "scripts" / "output" / "_w1100_inventory.json"
    with io.open(dst, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")

    print("=== A. 落层分类（互斥归类·全站·层内再分调色板色/自有 hex）===")
    for name, _rx in LAYERS:
        pages = layer_pages.get(name, {})
        pal = layer_split.get((name, "调色板色"), 0)
        own = layer_split.get((name, "页面自有 hex"), 0)
        print("%-32s 合计 %6d 处 / %4d 页  | 调色板色 %5d  自有 hex %5d"
              % (name, layer_totals.get(name, 0), len(pages), pal, own))
    print("合计：调色板色 %d · 页面自有 hex %d"
          % (pal_vs_own["调色板色"], pal_vs_own["页面自有 hex"]))
    print("校验：L1 调色板色应 = 0（档 1/档 2 已归零）⇒ 实测 %d"
          % layer_split.get(("L1 D3 .attr/.style(fill|stroke)", "调色板色"), 0))

    print("\n=== A2. 各层 top 页 ===")
    for name, _rx in LAYERS:
        pages = layer_pages.get(name, {})
        if not pages:
            continue
        print("--", name)
        for rel, n in pages.most_common(8):
            print("     %-46s %4d" % (rel, n))

    print("\n=== B. 补偿规则形态（全站）===")
    for name, _rx in COMP:
        print("%-34s %5d 条" % (name, comp_kind.get(name, 0)))
    print("含补偿规则的页数：%d" % len(comp_pages))
    print("含补偿规则页 top 12：")
    for rel, n in comp_pages.most_common(12):
        print("   %-46s %3d 条  %s" % (rel, n, comp_detail.get(rel)))

    print("\n=== C0. 档 3 口径（调色板色·L2+L3+L4+L5）逐页分布 ===")
    agg_pal = collections.Counter()
    for rel, c in per_page_split.items():
        pass
    for rel, c in per_page_layers.items():
        n = c.get("L2 echarts 配置色", 0) + c.get("L3 Canvas fillStyle/strokeStyle", 0) \
            + c.get("L4 通用 CSS 属性值", 0) + c.get("L5 裸 hex 字面量", 0)
        if n:
            agg_pal[rel] = n
    print("（注：此处置信『任意 hex』口径的档 3 施工面，与调色板色口径分开看）")
    print("=== C. 档 3 施工面页分布（按页合计 L2+L3+L4+L5）===")
    agg = collections.Counter()
    for rel, c in per_page_layers.items():
        n = sum(v for k, v in c.items() if k.startswith(("L2", "L3", "L4", "L5")))
        if n:
            agg[rel] = n
    print("涉及页数：%d · 合计处数：%d" % (len(agg), sum(agg.values())))
    for rel, n in agg.most_common(20):
        print("   %-46s %4d" % (rel, n))
    print("\n（清单已落盘：scripts/output/_w1100_inventory.json）")


if __name__ == "__main__":
    main()
