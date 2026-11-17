# -*- coding: utf-8 -*-
import importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pc", os.path.join(HERE, "..", "_palette_check.py"))
pc = importlib.util.module_from_spec(spec); spec.loader.exec_module(pc)
L, D = pc.parse_tokens(os.path.join(HERE, "..", "tokens.css"))
def row(fg, bg):
    return (fg, bg, pc.contrast(L[fg], L[bg]), pc.contrast(D[fg], D[bg]))
items = [
 ("text-primary","bg"),("text-primary","paper"),("text-primary","surface-raised"),
 ("text-secondary","bg"),("text-secondary","paper"),("text-tertiary","bg"),("text-tertiary","paper"),
 ("accent","bg"),("accent","paper"),("accent-text","accent-primary"),("text-inverse","dark"),
 ("chart-1","surface-raised"),("chart-2","surface-raised"),("chart-3","surface-raised"),
 ("chart-4","surface-raised"),("chart-5","surface-raised"),("chart-6","surface-raised"),
 ("axis-line","surface-raised"),("edge-visible","surface-raised"),("ok","bg"),("warn","bg"),
 ("info","bg"),("danger","bg"),
]
print("| 前景 | 背景 | 亮态 | 暗态 |")
print("| --- | --- | --- | --- |")
for fg, bg in items:
    _, _, cl, cd = row(fg, bg)
    print("| --%s | --%s | %.2f:1 | %.2f:1 |" % (fg, bg, cl, cd))
print()
print("亮态色值：")
for k in ["bg","paper","surface-canvas","surface-raised","surface-sunken","dark","ink","ink-soft","ink-faint","ink-tint",
          "text-primary","text-secondary","text-tertiary","accent","accent-primary","accent-deep","accent-muted",
          "accent-soft","accent-text","accent-tint","accent-wash","accent-2","accent-3","accent-4",
          "ok","warn","info","danger","status-neg","rebel",
          "chart-1","chart-2","chart-3","chart-4","chart-5","chart-6","series-7","series-8",
          "line","border-subtle","border-strong","border-hairline","border-accent","axis-line","grid-line","edge-visible"]:
    print("  --%s  %s / %s" % (k, L[k], D[k]))
