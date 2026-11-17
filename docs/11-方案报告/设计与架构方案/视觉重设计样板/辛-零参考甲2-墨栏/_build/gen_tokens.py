# -*- coding: utf-8 -*-
"""生成 tokens.css：亮/暗两套独立取值 + 两个暗态映射块（系统偏好 / data-theme 手动）。"""
import io, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tokens.css")

LIGHT = {
 "bg":"#EDE7D9","paper":"#F6F1E6","paper-warm":"#F1E9D7","surface-canvas":"#FBF8F1",
 "surface-raised":"#FFFDF8","surface-sunken":"#E6DFCE","surface-inset":"#DCD4C0",
 "dark":"#211D18","dark-text":"#F3EEE1",
 "ink":"#201B15","ink-soft":"#464035","ink-faint":"#756D5E","ink-tint":"#A79D8B",
 "text-primary":"#241F19","text-secondary":"#4E4740","text-tertiary":"#6E6658",
 "text-hero":"#17130E","text-inverse":"#F6F1E6","text-step-0":"16px","text-step-3":"24px",
 "accent":"#B23A2B","accent-primary":"#A8321F","accent-deep":"#7A2013","accent-muted":"#C9867A",
 "accent-soft":"#E9C6BC","accent-text":"#FFF8F1","accent-tint":"#F5DED6","accent-wash":"#FBF1EC",
 "accent-2":"#3C7FA8","accent-3":"#B98A0E","accent-4":"#6B4585",
 "ok":"#2F7355","warn":"#8A5A0B","info":"#2E6C97","danger":"#B3261E",
 "status-neg":"#6B4585","rebel":"#3E4A5A",
 "chart-1":"#3C7FA8","chart-2":"#B5641F","chart-3":"#A83E77",
 "chart-4":"#235F44","chart-5":"#B98A0E","chart-6":"#6B4585",
 "series-1":"#3C7FA8","series-2":"#B5641F","series-3":"#A83E77","series-4":"#235F44",
 "series-5":"#B98A0E","series-6":"#6B4585","series-7":"#3E4A5A","series-8":"#7A4B2A",
 "line":"#D9D1BE","border-subtle":"#E4DCCB","border-strong":"#BFB5A0","border-hairline":"#EDE7D9",
 "border-accent":"#C9867A","axis-line":"#8E8577","grid-line":"#E6E0D0","edge-visible":"#837A6B",
 "shadow":"0 1px 2px rgba(32,27,21,.08)","shadow-lift":"0 8px 24px -10px rgba(32,27,21,.22)",
 "elev-0":"none","elev-1":"0 1px 2px rgba(32,27,21,.06)","elev-2":"0 2px 6px -2px rgba(32,27,21,.12)",
 "elev-3":"0 8px 20px -8px rgba(32,27,21,.18)","elev-4":"0 18px 40px -16px rgba(32,27,21,.26)",
 "dur-fast":"150ms","dur-base":"200ms","dur-slow":"400ms",
 "ease-out-quart":"cubic-bezier(0.25, 1, 0.5, 1)","ease-out-expo":"cubic-bezier(0.16, 1, 0.3, 1)",
 "ease-in-out-soft":"cubic-bezier(0.4, 0, 0.2, 1)",
 "font-serif":'"Songti SC","SimSun","Noto Serif CJK SC","Source Han Serif SC",serif',
 "font-sans":'-apple-system,"SF Pro Text","Segoe UI",system-ui,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif',
 "font-mono":'ui-monospace,"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace',
 "font-code":'ui-monospace,"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace',
 "font-display":'"Songti SC","SimSun","Noto Serif CJK SC","Source Han Serif SC",serif',
 "font-text":'-apple-system,"SF Pro Text","Segoe UI",system-ui,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif',
 "font-data":'"Avenir Next","Helvetica Neue",Arial,"PingFang SC","Microsoft YaHei",sans-serif',
 "size-body":"16px","size-hero":"44px","size-label":"12px","size-micro":"11px","size-section":"28px",
 "type-body":"16px","type-caption":"13px","type-display":"44px","type-eyebrow":"11px","type-label":"12px",
 "type-lead":"17px","type-number":"34px","type-subtitle":"20px","type-title":"28px",
 "leading-tight":"1.25","space-1":"4px","space-5":"20px","space-9":"36px",
 "gap-tight":"8px","gap-loose":"24px","gap-section":"56px",
 "container-read":"40rem","grid-columns":"12","indent-0":"0","radius-sm":"2px","radius-pill":"999px",
 "z-nav":"100","z-drawer":"200","z-mask":"300","z-tooltip":"400",
}

DARK = {
 "bg":"#14110D","paper":"#1B1813","paper-warm":"#211D16","surface-canvas":"#221E18",
 "surface-raised":"#28241D","surface-sunken":"#100E0B","surface-inset":"#0B0907",
 "dark":"#F1EADB","dark-text":"#1B1813",
 "ink":"#E7DFCE","ink-soft":"#B7AE9D","ink-faint":"#8E8577","ink-tint":"#6A6255",
 "text-primary":"#EDE6D6","text-secondary":"#B9B0A0","text-tertiary":"#9A9182",
 "text-hero":"#F4EDDD","text-inverse":"#241F19",
 "accent":"#E0705A","accent-primary":"#D05A42","accent-deep":"#E88A74","accent-muted":"#8A4A3C",
 "accent-soft":"#4A2A23","accent-text":"#17130E","accent-tint":"#3A211B","accent-wash":"#241714",
 "accent-2":"#9AC4E2","accent-3":"#D8B44E","accent-4":"#A585D0",
 "ok":"#5FB08C","warn":"#D8A340","info":"#74AED3","danger":"#E36A5E",
 "status-neg":"#B294DC","rebel":"#93A4B8",
 "chart-1":"#9AC4E2","chart-2":"#B87428","chart-3":"#D982AE",
 "chart-4":"#4C9878","chart-5":"#D8B44E","chart-6":"#A585D0",
 "series-1":"#9AC4E2","series-2":"#B87428","series-3":"#D982AE","series-4":"#4C9878",
 "series-5":"#D8B44E","series-6":"#A585D0","series-7":"#6A7A8E","series-8":"#9A6539",
 "line":"#35302A","border-subtle":"#2B2721","border-strong":"#4E473C","border-hairline":"#201C17",
 "border-accent":"#8A4A3C","axis-line":"#7E7666","grid-line":"#262119","edge-visible":"#7E7666",
 "shadow":"0 1px 2px rgba(0,0,0,.50)","shadow-lift":"0 10px 30px -12px rgba(0,0,0,.65)",
 "elev-0":"none","elev-1":"0 1px 2px rgba(0,0,0,.40)","elev-2":"0 2px 8px -2px rgba(0,0,0,.50)",
 "elev-3":"0 8px 22px -8px rgba(0,0,0,.60)","elev-4":"0 18px 44px -16px rgba(0,0,0,.70)",
}

assert set(DARK) <= set(LIGHT), set(DARK) - set(LIGHT)
DARK_ALL = dict(LIGHT)
DARK_ALL.update(DARK)

GROUPS = [
 ("表面", ["bg","paper","paper-warm","surface-canvas","surface-raised","surface-sunken","surface-inset","dark","dark-text"]),
 ("文本", ["ink","ink-soft","ink-faint","ink-tint","text-primary","text-secondary","text-tertiary","text-hero","text-inverse","text-step-0","text-step-3"]),
 ("强调", ["accent","accent-primary","accent-deep","accent-muted","accent-soft","accent-text","accent-tint","accent-wash","accent-2","accent-3","accent-4"]),
 ("语义", ["ok","warn","info","danger","status-neg","rebel"]),
 ("数据序列", ["chart-1","chart-2","chart-3","chart-4","chart-5","chart-6","series-1","series-2","series-3","series-4","series-5","series-6","series-7","series-8"]),
 ("线与边", ["line","border-subtle","border-strong","border-hairline","border-accent","axis-line","grid-line","edge-visible"]),
 ("阴影", ["shadow","shadow-lift","elev-0","elev-1","elev-2","elev-3","elev-4"]),
 ("动效", ["dur-fast","dur-base","dur-slow","ease-out-quart","ease-out-expo","ease-in-out-soft"]),
 ("字体", ["font-serif","font-sans","font-mono","font-code","font-display","font-text","font-data"]),
 ("字号/行高/间距", ["size-body","size-hero","size-label","size-micro","size-section","type-body","type-caption","type-display","type-eyebrow","type-label","type-lead","type-number","type-subtitle","type-title","leading-tight","space-1","space-5","space-9","gap-tight","gap-loose","gap-section"]),
 ("布局", ["container-read","grid-columns","indent-0","radius-sm","radius-pill","z-nav","z-drawer","z-mask","z-tooltip"]),
]
order = [n for _, names in GROUPS for n in names]
assert sorted(order) == sorted(LIGHT), "分组覆盖不完整"

def block(d, prefix=""):
    out = []
    for g, names in GROUPS:
        out.append("  /* %s */" % g)
        for n in names:
            out.append("  --%s%s: %s;" % (prefix, n, d[n]))
        out.append("")
    return "\n".join(out)

def map_block():
    out = []
    for g, names in GROUPS:
        out.append("    /* %s */" % g)
        for n in names:
            out.append("    --%s: var(--d-%s);" % (n, n))
        out.append("")
    return "\n".join(out)

HEAD = """/* ============================================================
   tokens.css — 「墨栏 / INK-RULE」设计系统 · 令牌全量定义
   ------------------------------------------------------------
   明暗两套取值完全独立撰写（非亮色反相）：
   · :root          → 亮态（日读：纸为底、墨为字）
   · --d-* 组       → 暗态取值（夜读：墨为底、纸为字）
   · 暗态映射 A     → 系统 prefers-color-scheme: dark
   · 暗态映射 B     → 手动切换 [data-theme="dark"]
   令牌名为冻结接口，一字不改；取值在本文件内整体替换。
   ============================================================ */

:root {
  color-scheme: light;

  /* ===== 亮态取值 ===== */
%s
  /* ===== 暗态取值（独立撰写） ===== */
%s}

/* 暗态映射 A：跟随系统偏好（手动指定 light 时不生效） */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
%s
  }
}

/* 暗态映射 B：手动切换按钮 */
:root[data-theme="dark"] {
  color-scheme: dark;
%s}
"""

out = HEAD % (block(LIGHT), block(DARK_ALL, "d-"), map_block(), map_block())
with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(out)
print("tokens.css written:", os.path.normpath(OUT), len(out), "chars", len(LIGHT), "tokens")
