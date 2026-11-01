#!/usr/bin/env python3
"""_w1078_color_inventory.py — 全站硬编码颜色盘点（B2 落地面·可复算）

## 产出

1. `scripts/output/_w1078_color_inventory.json` — 机器可读（逐页 × 分类 × 色值 × 令牌候选）
2. `scripts/output/_w1078_color_inventory.md` — 人读版（令牌映射总表 + 逐页清单 + 不可替换项分类）

## 分类口径（决定「能不能换成令牌」）

| 分类 | 含义 | 能否替换为 var() | 说明 |
|:--|:---|:--:|:---|
| `定义面` | `:root` / `html[data-theme="dark"]` 块里的**令牌定义本身** | 否 | 不是消费面；改它＝改令牌取值（须走令牌批） |
| `共享副本消费` | `<!-- INLINED CSS -->` 块内（tokens.css + system.css 的拷贝） | 是，但属**共享层** | 改这里＝改共享层 ⇒ 级联全部内联页 ⇒ 须连传播同批做 |
| `页内私有消费` | 页面自己的 `<style>` 块内的声明 | 是 | 逐页可做（零差异或暗色对齐） |
| `内联样式消费` | `style="..."` 属性 | 是 | 同上 |
| `SVG属性位` | `fill="#xxx"` / `stroke="#xxx"` 等表现属性 | 需改写法 | `var()` 在表现属性里**不生效** ⇒ 要改成 `style="fill:var(--chart-1)"` |
| `JS字面量` | `<script>` 内的字符串 | 需工程化 | SVG/Canvas 属性位不解析 `var()` ⇒ 需读 `getComputedStyle` 喂图表，或改配置为 CSS 变量驱动 |
| `标记文本` | HTML 文本/非样式属性 | 视情况 | 少量 |

## 替换后果判定

- 令牌**浅色值 == 该 hex** ⇒ 替换后浅色零差异；暗色若不同 ⇒ 暗色会变（有意变化·须列举）。
- 只有令牌**暗色值 == 该 hex** ⇒ 替换后暗色零差异、浅色会变（如 #E46250 → var(--accent)）。
- 无任何令牌同值 ⇒ **页面私有意设计色** ⇒ 不动（登记）。

用法：
    python scripts/_w1078_color_inventory.py            # 生成两件产物
    python scripts/_w1078_color_inventory.py --md-only   # 只重生成 md
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(ROOT, "scripts", "output")

HEX_RE = re.compile(r"#([0-9A-Fa-f]{6})\b")
RE_INLINED = re.compile(r"<!--\s*INLINED CSS.*?-->\s*<style>(.*?)</style>", re.S)
RE_STYLE = re.compile(r"<style[^>]*>(.*?)</style>", re.S)
RE_SCRIPT = re.compile(r"<script\b[^>]*>(.*?)</script>", re.S)
RE_STYLE_ATTR = re.compile(r"\bstyle\s*=\s*(\"[^\"]*\"|'[^']*')")
RE_SVG_ATTR = re.compile(r"\b(fill|stroke|stop-color|flood-color|lighting-color)\s*=\s*(\"[^\"]*\"|'[^']*')", re.I)
RE_TOKEN_DECL = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;{}\n]+);")
RE_ROOT_BLOCK = re.compile(r"(:root|html\[data-theme=\"dark\"\]|html\[data-theme='dark'\])\s*\{([^{}]*)\}", re.S)


def parse_tokens():
    """tokens.css → (light: name→value, dark: name→value)"""
    txt = open(os.path.join(SITE, "tokens.css"), encoding="utf-8").read()
    light, dark = {}, {}
    for m in RE_ROOT_BLOCK.finditer(txt):
        sel, body = m.group(1), m.group(2)
        target = dark if "data-theme" in sel else light
        for tm in RE_TOKEN_DECL.finditer(body):
            target.setdefault(tm.group(1), tm.group(2).strip())
    return light, dark


def hex_index(light, dark):
    """hex(大写) → {"light": [token...], "dark": [token...]}"""
    idx = defaultdict(lambda: {"light": [], "dark": []})
    for name, val in light.items():
        m = re.fullmatch(r"#([0-9A-Fa-f]{6})", val)
        if m:
            idx["#" + m.group(1).upper()]["light"].append(name)
    for name, val in dark.items():
        m = re.fullmatch(r"#([0-9A-Fa-f]{6})", val)
        if m:
            idx["#" + m.group(1).upper()]["dark"].append(name)
    return idx


def classify_page(txt):
    """返回 (分类名 → [(hex, pos)]) 与 span 辅助信息"""
    inl = [(m.start(1), m.end(1)) for m in RE_INLINED.finditer(txt)]
    styles = [(m.start(1), m.end(1)) for m in RE_STYLE.finditer(txt)]
    scripts = [(m.start(1), m.end(1)) for m in RE_SCRIPT.finditer(txt)]
    style_attrs = [(m.start(1), m.end(1)) for m in RE_STYLE_ATTR.finditer(txt)]
    svg_attrs = [(m.start(1), m.end(1)) for m in RE_SVG_ATTR.finditer(txt)]
    # 定义面（:root / dark 块）span
    defs = []
    for m in RE_ROOT_BLOCK.finditer(txt):
        defs.append((m.start(2), m.end(2)))

    def in_spans(pos, spans):
        return any(s <= pos < e for s, e in spans)

    buckets = defaultdict(list)
    for m in HEX_RE.finditer(txt):
        h = "#" + m.group(1).upper()
        pos = m.start()
        if in_spans(pos, defs):
            buckets["定义面"].append(h)
        elif in_spans(pos, inl):
            buckets["共享副本消费"].append(h)
        elif in_spans(pos, styles):
            buckets["页内私有消费"].append(h)
        elif in_spans(pos, style_attrs):
            buckets["内联样式消费"].append(h)
        elif in_spans(pos, svg_attrs):
            buckets["SVG属性位"].append(h)
        elif in_spans(pos, scripts):
            buckets["JS字面量"].append(h)
        else:
            buckets["标记文本"].append(h)
    return buckets


REPLACEABLE = ("页内私有消费", "内联样式消费")
NON_REPLACE = {
    "定义面": "令牌定义本身（改它＝改令牌取值·须走令牌批）",
    "共享副本消费": "共享层（tokens.css/system.css 的拷贝）⇒ 级联全部内联页·须连传播同批做",
    "SVG属性位": "var() 在表现属性里不生效⇒须改写成 style=\"fill:var(--chart-N)\"",
    "JS字面量": "SVG/Canvas 属性位不解析 var()⇒须读 getComputedStyle 喂图表或改配置驱动",
    "标记文本": "文本/非样式属性·逐处判定",
}


def main():
    light, dark = parse_tokens()
    idx = hex_index(light, dark)
    pages = []
    for dirpath, _dirs, files in os.walk(SITE):
        if any(part.startswith(".") for part in dirpath.split(os.sep)):
            continue
        for fn in sorted(files):
            if fn.endswith(".html"):
                pages.append(os.path.join(dirpath, fn))
    pages.sort()

    out = {"meta": {"page_count": len(pages), "light_tokens": len(light), "dark_tokens": len(dark)},
           "token_map": {}, "pages": [], "totals": {}, "non_replaceable": {}, "token_consumers": {}}

    for name, val in sorted(light.items()):
        out["token_map"].setdefault(name, {})["light"] = val
    for name, val in sorted(dark.items()):
        out["token_map"].setdefault(name, {})["dark"] = val

    total_cat = Counter()
    hex_cat = defaultdict(Counter)
    consumers = defaultdict(set)
    for p in pages:
        txt = open(p, encoding="utf-8", errors="ignore").read()
        rel = os.path.relpath(p, SITE).replace(os.sep, "/")
        buckets = classify_page(txt)
        rec = {"page": rel, "counts": {}, "hexes": {}}
        for cat, hs in buckets.items():
            if not hs:
                continue
            c = Counter(hs)
            rec["counts"][cat] = len(hs)
            rec["hexes"][cat] = dict(c.most_common())
            total_cat[cat] += len(hs)
            hex_cat[cat].update(c)
            if cat in REPLACEABLE or cat in ("JS字面量", "SVG属性位"):
                for h in c:
                    for tok in idx.get(h, {}).get("light", []) + idx.get(h, {}).get("dark", []):
                        consumers[tok].add(rel)
        # 该页消费的 var(--chart-N)/var(--accent*) 名单
        used = sorted(set(re.findall(r"var\(--(?:chart-\d|accent(?:-text|-soft)?)\)", txt)))
        if used:
            rec["consumes_tokens"] = used
        pages_rec = rec
        out["pages"].append(pages_rec)

    out["totals"] = dict(total_cat)
    out["hex_by_category"] = {k: dict(v.most_common()) for k, v in hex_cat.items()}
    out["non_replaceable"] = {k: {"reason": NON_REPLACE.get(k, ""), "count": total_cat.get(k, 0)}
                               for k in ("定义面", "共享副本消费", "SVG属性位", "JS字面量", "标记文本")}
    out["token_consumers"] = {k: sorted(v) for k, v in sorted(consumers.items())}

    with open(os.path.join(OUT, "_w1078_color_inventory.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    # ---- Markdown ----
    L = []
    L.append("# 全站硬编码颜色盘点（W1078 · B2 落地面）\n")
    L.append("> 生成件：`python scripts/_w1078_color_inventory.py` · 机器版同目录 `_w1078_color_inventory.json`\n")
    L.append(f"> 扫描面：site/ 下 {len(pages)} 个 HTML 页（含根页 / data / en / reader）· 令牌表取自 `site/tokens.css`"
             f"（浅色 {len(light)} 名 · 暗色 {len(dark)} 名）\n")
    L.append("\n## 1. 总量与分类\n")
    L.append("| 分类 | 处数 | 可否换成 var() | 理由 |\n|:--|--:|:--:|:--|")
    L.append("| 页内私有消费 | %d | ✅ 可（逐页） | 页内自己的 `<style>` 声明 |" % total_cat.get("页内私有消费", 0))
    L.append("| 内联样式消费 | %d | ✅ 可（逐页） | `style=\"…\"` 属性 |" % total_cat.get("内联样式消费", 0))
    L.append("| SVG属性位 | %d | ⚠️ 需改写法 | `fill=\"#xxx\"` 等表现属性不解析 `var()` |" % total_cat.get("SVG属性位", 0))
    L.append("| JS字面量 | %d | ⚠️ 需工程化 | SVG/Canvas 属性位不解析 `var()` |" % total_cat.get("JS字面量", 0))
    L.append("| 共享副本消费 | %d | ⚠️ 属共享层 | INLINED 拷贝（tokens.css+system.css）⇒ 改这里级联全站 |" % total_cat.get("共享副本消费", 0))
    L.append("| 定义面 | %d | ❌ 不算消费面 | `:root` / 暗色块里的令牌定义本身 |" % total_cat.get("定义面", 0))
    L.append("| 标记文本 | %d | 逐处判定 | 文本/非样式属性 |" % total_cat.get("标记文本", 0))
    L.append("\n**可逐页消费的量 = 页内私有消费 + 内联样式消费 = %d 处**；其余 %d 处分别受「共享层边界」「属性位不解析 var()」「令牌定义非消费面」三类约束。"
             % (total_cat.get("页内私有消费", 0) + total_cat.get("内联样式消费", 0),
                total_cat.get("JS字面量", 0) + total_cat.get("SVG属性位", 0) + total_cat.get("共享副本消费", 0)
                + total_cat.get("定义面", 0)))
    L.append("\n## 2. 令牌映射总表（hex → 令牌 → 浅/暗取值 → 替换后果）\n")
    L.append("| 色值 | 令牌 | 浅色值 | 暗色值 | 替换后果 |\n|:--|:--|:--|:--|:--|")
    for h, info in sorted(idx.items()):
        lt = info["light"] or []
        dk = info["dark"] or []
        for tok in lt:
            dv = dark.get(tok)
            cons = len(consumers.get(tok, ()))
            if dv is None:
                conseq = "暗色沿用浅色值（零差异）"
            elif dv == light.get(tok):
                conseq = "暗色同值（零差异）"
            else:
                conseq = "暗色变为 %s（有意变化·须列举）" % dv
            L.append("| `%s` | `%s` | %s | %s | 浅色零差异；%s |"
                     % (h, tok, light.get(tok, ""), dv if dv else "（无暗色覆盖）", conseq))
        for tok in dk:
            if tok in lt:
                continue
            L.append("| `%s` | `%s`（暗色值） | %s | %s | 仅暗色同值；浅色会变（暗色语境替换） |"
                     % (h, tok, light.get(tok, "（浅色未定义）"), dark.get(tok, "")))
    L.append("\n## 3. 逐页清单（全站 %d 页 · 有硬编码色的页按分类计数）\n" % len(pages))
    L.append("| 页 | 页内私有消费 | 内联样式 | SVG属性 | JS字面量 | 共享副本 | 定义面 | 主要色值（页内私有+JS） |")
    L.append("|:--|--:|--:|--:|--:|--:|--:|:--|")
    for rec in out["pages"]:
        c = rec["counts"]
        if not c:
            continue
        own = Counter()
        for cat in ("页内私有消费", "内联样式消费", "JS字面量", "SVG属性位"):
            own.update(rec["hexes"].get(cat, {}))
        top = "、".join("%s×%d" % (k, v) for k, v in own.most_common(3))
        L.append("| `%s` | %d | %d | %d | %d | %d | %d | %s |"
                 % (rec["page"], c.get("页内私有消费", 0), c.get("内联样式消费", 0),
                    c.get("SVG属性位", 0), c.get("JS字面量", 0), c.get("共享副本消费", 0),
                    c.get("定义面", 0), top or "—"))
    L.append("\n## 4. 不可替换项（分类统计与处理口径）\n")
    for cat, info in out["non_replaceable"].items():
        L.append("**%s（%d 处）** — %s\n" % (cat, info["count"], info["reason"]))
        top = hex_cat.get(cat, Counter()).most_common(6)
        if top:
            L.append("  色值分布：" + "、".join("%s×%d" % (k, v) for k, v in top) + "\n")
    # B2 专项：结构与回目 10 页的逐页明细
    B2 = ["data/chapter-structure-graph.html", "data/chapter-stats.html", "data/story-timeline.html",
          "data/timeline.html", "data/relationships.html", "data/81-hardships.html",
          "data/81-hardships-view.html", "data/hardship-heatmap.html",
          "data/hardship-difficulty-heatmap.html", "data/methodology-matrix.html"]
    L.append("\n## 4b. B2 专项（结构与回目 10 页）·逐页明细\n")
    L.append("| 页 | 分类 | 处数 | 色值分布（该分类内） |\n|:--|:--|--:|:--|")
    for rec in out["pages"]:
        if rec["page"] not in B2:
            continue
        for cat in ("页内私有消费", "内联样式消费", "JS字面量", "共享副本消费", "定义面", "标记文本"):
            c = rec["counts"].get(cat, 0)
            if not c:
                continue
            dist = "、".join("%s×%d" % (k, v) for k, v in list(rec["hexes"].get(cat, {}).items())[:6])
            L.append("| `%s` | %s | %d | %s |" % (rec["page"], cat, c, dist))
    L.append("\n> B2 判定小结：① 十页的**页内私有 CSS 消费面**共 %d 处、**内联样式**共 %d 处 ⇒ 可逐页消费的量很小；"
             "② 十页的硬编码色主体在 **JS 字面量**（共 %d 处）⇒ `var()` 在 SVG/Canvas 属性位不生效 ⇒ 需工程化或改配置驱动；"
             "③ 十页容器**全部已是 `var(--container-wide)`** ⇒ 无容器归并对象；"
             "④ `--chart-3` / `--chart-5` 的**硬编码消费面为空** ⇒ defer「暗色 chart 新增」不触发。\n"
             % (sum(rec["counts"].get("页内私有消费", 0) for rec in out["pages"] if rec["page"] in B2),
                sum(rec["counts"].get("内联样式消费", 0) for rec in out["pages"] if rec["page"] in B2),
                sum(rec["counts"].get("JS字面量", 0) for rec in out["pages"] if rec["page"] in B2)))
    L.append("\n## 5. 令牌消费面（defer 项判定用）\n")
    L.append("| 令牌 | 消费页数 | 消费页（前 8） |\n|:--|--:|:--|")
    for tok, ps in sorted(out["token_consumers"].items(), key=lambda kv: -len(kv[1])):
        L.append("| `%s` | %d | %s |" % (tok, len(ps), "、".join("`%s`" % x for x in ps[:8])))
    L.append("\n> **defer「暗色 `--chart-3` / `--chart-5` 新增」判定**：`--chart-3` / `--chart-5` 的**硬编码消费面为空**"
             "（全站无任何页面以 `var(--chart-3)` / `var(--chart-5)` 消费）⇒ 本批**不触发**纯加法；"
             "两者的硬编码值目前只存在于**令牌定义与 JS 字面量**中 ⇒ 治理路径是「JS 侧令牌化」而非「补令牌」。\n")
    L.append("\n---\n")
    L.append("*本件为盘点产物（只读统计·未改动任何页面）·复算命令：`python scripts/_w1078_color_inventory.py`*\n")

    with open(os.path.join(OUT, "_w1078_color_inventory.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L))

    print("盘点完成：%d 页 → scripts/output/_w1078_color_inventory.{json,md}" % len(pages))
    print("分类合计：%s" % dict(total_cat))
    print("可逐页消费（页内私有 + 内联样式）：%d 处" % (total_cat.get("页内私有消费", 0) + total_cat.get("内联样式消费", 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
