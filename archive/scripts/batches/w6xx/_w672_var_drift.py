# _w672_var_drift.py — W672 WP-1.2 变量漂移映射替换（616 处/62 种/62 文件）+ WP-1.6 自引用删除（24 处/8 文件）。
# 方案：docs/superpowers/plans/2026-10-05-site-quality-remediation-plans.md §三 WP-1.2 / WP-1.6
#
# 口径：
# - 未定义判定与方案附录 A 扫描器 3 完全同口径（known = 页内 style 块 ∪ 内联 style 属性 ∪ JS 文本定义 ∪ tokens.css）；
#   只改「该文件内确实未定义」的变量引用，页内私有定义（如 en/dukou-engine 的 --cinnabar）天然豁免。
# - A 组直映射（方案 §三 WP-1.2 表）+ C 组语义映射（同表）+ D 组直映射（四路子代理取证裁决，2026-10-06）。
# - B 组 --shadow-hover 语境二分：选择器含 :hover/:focus/:active → --elev-2，否则 → --shadow（附录 B）。
# - D 组回退式改写（无把握/无对应 token）：var(--x) → var(--x, var(--tok))；--space-* 无间距 token → 像素回退。
# - --gold 按文件三分 + visual-art 按选择器二分（子代理 D3 取证）。
# - WP-1.6：删除 style 块内「--x: …var(--x)…」自引用声明行，令 INLINED tokens 定义获胜。
#
# 用法：python scripts/_w672_var_drift.py --dry-run | --apply
import collections
import glob
import re

TOK = open("site/tokens.css", encoding="utf-8").read()
TOK_DEFS = set(re.findall(r"(--[\w-]+)\s*:", TOK))
VAR_RE = re.compile(r"var\((--[\w-]+)\)")
DEF_RE = re.compile(r"(--[\w-]+)\s*:")

# A 组直映射 + --shadow-md（就近 --shadow-lift）
MAP_DIRECT = {
    "--border": "--line", "--muted": "--ink-soft", "--card": "--paper", "--fg": "--ink",
    "--text-muted": "--ink-soft", "--text-secondary": "--ink-soft", "--text-primary": "--ink",
    "--accent-primary": "--accent", "--accent-secondary": "--accent-2",
    "--accent-tertiary": "--accent-3", "--accent-quaternary": "--accent-4",
    "--accent2": "--accent-2", "--accent-1": "--accent-2",
    "--line-soft": "--line", "--bg-primary": "--bg", "--bg-secondary": "--paper-warm",
    "--table-header": "--paper-warm", "--table-stripe": "--paper",
    "--paper-card": "--paper-warm", "--paper-deep": "--paper-warm",
    "--hero-meta": "--ink-faint", "--tooltip-bg": "--dark", "--shadow-md": "--shadow-lift",
    # C 组语义近似
    "--pos": "--accent-4", "--neu": "--accent-3", "--neg": "--accent",
    "--accent-5": "--accent-4", "--accent-6": "--accent-4",
    # D 组直映射（子代理 D1-D4 取证：阵营/场景/金属/稀有度/渲染色）
    "--r-warrior": "--chart-4", "--r-king": "--chart-1", "--r-judge": "--chart-3",
    "--r-marginal": "--chart-6", "--r-buddha": "--accent-3", "--r-taoist": "--chart-2",
    "--r-bodhi": "--chart-2", "--r-mortal": "--chart-4",
    "--t-lone": "--rebel", "--t-family": "--chart-3", "--t-alliance": "--chart-4",
    "--water": "--chart-2", "--fire": "--chart-1", "--mountain": "--chart-3", "--sky": "--chart-4",
    "--cinnabar": "--accent", "--indigo": "--accent-2", "--jade": "--accent-4",
    "--shadow-deep": "--elev-3",
    "--rarity-ur": "--chart-3", "--rarity-ssr": "--accent-3", "--rarity-sr": "--accent-2",
    "--rarity-r": "--accent-4", "--rarity-n": "--ink-soft",
    "--svg-color": "--chart-1", "--canvas-color": "--chart-2",
}
# D 组回退式改写（现役调色板无对应：紫坐骑/紫灰官僚）
MAP_FALLBACK = {"--r-mount": "--chart-6", "--t-bureau": "--chart-2"}
# 间距 token 不存在（tokens.css 无 --spc-*），按 4px 尺度像素回退
SPACE_PX = {"--space-2": "8px", "--space-3": "12px", "--space-4": "16px", "--space-6": "24px"}
# --gold 按文件语义三分（子代理 D3 取证：数据叙事金→chart-3；成套 accent-3 场景→accent-3）
GOLD_FILE = {
    "four-dimensional-research-network": "--chart-3",
    "music-structure": "--chart-3",
    "narrative-experiment": "--chart-3",
    "ethics-consumption": "--accent-3",
    "magic-system": "--accent-3",
}
# visual-art 按选择器二分：浅底成套（kpi-card.gold/.spec-item）→accent-3；深底装饰 →chart-3（默认）
GOLD_SPLIT = [(re.compile(r"\.kpi-card\.gold|\.spec-item"), "--accent-3")]
GOLD_DEFAULT = "--chart-3"
# WP-1.6 自引用删除：外科手术式移除「--x: …var(--x)…」声明（含尾分号），同块其他合法声明保留
SELFREF_SUB = re.compile(r"(--[\w-]+)\s*:\s*[^;{}]*?var\(\1[),][^;{}]*?;?")


def known_defs(src):
    style_blocks = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S | re.I))
    inline_attr = " ".join(re.findall(r'style="([^"]*)"', src))
    js_text = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", src, re.S | re.I))
    defs = set(re.findall(DEF_RE, style_blocks)) | set(re.findall(DEF_RE, inline_attr))
    defs |= set(re.findall(r"['\"]?(--[\w-]+)\s*[:=]", js_text))
    defs |= set(re.findall(r"\.style\(\s*[\"'](--[\w-]+)", js_text))
    defs |= set(re.findall(r"setProperty\(\s*[\"'](--[\w-]+)", js_text))
    return defs | TOK_DEFS


def gold_for(sel, fname):
    for rx, tok in GOLD_SPLIT:
        if rx.search(sel):
            return tok
    for key, tok in GOLD_FILE.items():
        if key in fname:
            return tok
    return GOLD_DEFAULT


def contextual_pass(blk, fname, counts, undef):
    """style 块内 --shadow-hover 语境二分 + --gold 文件/选择器规则（仅未定义变量）。"""
    lines = blk.split("\n")
    out = []
    depth = 0
    cur_sel = ""
    for ln in lines:
        if depth == 0 and "{" in ln:
            head = ln[: ln.index("{")].strip()
            if head:
                cur_sel = head
        elif depth == 0 and ln.strip() and "{" not in ln and "}" not in ln:
            cur_sel = ln.strip()  # 多行选择器的续行
        if "var(--shadow-hover)" in ln and "--shadow-hover" in undef:
            tok = "--elev-2" if re.search(r":(hover|focus|active)", cur_sel) else "--shadow"
            n = ln.count("var(--shadow-hover)")
            ln = ln.replace("var(--shadow-hover)", "var(%s)" % tok)
            counts[("shadow-hover→" + tok)] += n
        if "var(--gold)" in ln and "--gold" in undef:
            tok = gold_for(cur_sel, fname)
            n = ln.count("var(--gold)")
            ln = ln.replace("var(--gold)", "var(%s)" % tok)
            counts[("gold→" + tok)] += n
        depth += ln.count("{") - ln.count("}")
        out.append(ln)
    return "\n".join(out)


def filewide_pass(src, undef, counts):
    """全文件直映射/回退式/间距像素 + style 块外 shadow-hover/gold 残留。"""
    def repl(m):
        v = m.group(1)
        if v == "--shadow-hover":
            counts["shadow-hover→--shadow(块外)"] += 1
            return "var(--shadow)"
        if v == "--gold":
            counts["gold→%s(块外)" % GOLD_DEFAULT] += 1
            return "var(%s)" % GOLD_DEFAULT
        if v in MAP_DIRECT:
            counts[v + "→" + MAP_DIRECT[v]] += 1
            return "var(%s)" % MAP_DIRECT[v]
        if v in MAP_FALLBACK:
            counts[v + "→回退(var(%s))" % MAP_FALLBACK[v]] += 1
            return "var(%s, var(%s))" % (v, MAP_FALLBACK[v])
        if v in SPACE_PX:
            counts[v + "→像素回退%s" % SPACE_PX[v]] += 1
            return "var(%s, %s)" % (v, SPACE_PX[v])
        return m.group(0)

    def sub_undef(m):
        return repl(m) if m.group(1) in undef else m.group(0)

    return VAR_RE.sub(sub_undef, src)


def main():
    import argparse

    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    all_files = sorted(glob.glob("site/data/*.html") + glob.glob("site/*.html") + glob.glob("site/en/*.html"))
    counts = collections.Counter()
    touched = 0
    fails = []
    for f in all_files:
        src = open(f, encoding="utf-8", newline="").read()
        known = known_defs(src)
        spans = list(re.finditer(r"<style[^>]*>(.*?)</style>", src, re.S | re.I))
        block_css = "\n".join(m.group(1) for m in spans)
        allrefs = VAR_RE.findall(block_css)
        undef = {v for v in allrefs if v not in known}
        before_undef = sum(1 for v in allrefs if v in undef)
        # ① style 块语境/选择器规则
        parts = []
        last = 0
        for m in spans:
            parts.append(src[last:m.start(1)])
            parts.append(contextual_pass(m.group(1), f, counts, undef))
            last = m.end(1)
        parts.append(src[last:])
        s2 = "".join(parts)
        # ② 自引用声明删除（WP-1.6，与未定义无关，全文件适用）
        n_self = len(SELFREF_SUB.findall(s2))
        s2 = SELFREF_SUB.sub("", s2)
        if not undef and not n_self:
            continue
        # ③ 全文件直映射/回退/像素
        s3 = filewide_pass(s2, undef, counts)
        # ④ 自断言：重算未定义与自引用必须为 0
        known3 = known_defs(s3)
        spans3 = list(re.finditer(r"<style[^>]*>(.*?)</style>", s3, re.S | re.I))
        rest = [m.group(1) for m in VAR_RE.finditer("\n".join(x.group(1) for x in spans3)) if m.group(1) not in known3]
        rest_self = len(re.findall(r"(--[\w-]+)\s*:\s*[^;{}]*var\(\1", "\n".join(x.group(1) for x in spans3)))
        if rest or rest_self:
            fails.append("%s: 残留未定义 %s / 自引用 %d" % (f, sorted(set(rest)), rest_self))
            continue
        if n_self:
            counts["<自引用删除>"] += n_self
        if s3 != src:
            touched += 1
            print("%s: 引用 %d 处 + 自引用 %d 行" % (f, before_undef, n_self))
            if args.apply:
                open(f, "w", encoding="utf-8", newline="").write(s3)
    print("=== 汇总 ===")
    print("改动文件数:", touched)
    for k, n in sorted(counts.items()):
        print("  %-38s %d" % (k, n))
    if fails:
        print("FAIL:")
        for x in fails:
            print(" ", x)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
