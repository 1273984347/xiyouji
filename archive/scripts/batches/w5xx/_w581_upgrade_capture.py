"""W581 注入升级：三处形态（W574/W575/W581）的 touch 委托统一加 capture:true。

根因：d3.drag 的 touchstarted 会 stopImmediatePropagation，document 冒泡层注入收不到
可拖拽节点的 touchstart（EN heaven/monster/six-senses 实证）——捕获阶段先于目标阶段，
天然免疫下游拦截。仅处理带注入标记的页面，多行锚点精确替换（防误伤自有监听）。
"""
import glob

HEAD = "}, { passive: true });\n    document.addEventListener('touchmove', function () {"
TAIL = "}, { passive: true });\n})();"
HEAD_NEW = "}, { passive: true, capture: true });\n    document.addEventListener('touchmove', function () {"
TAIL_NEW = "}, { passive: true, capture: true });\n})();"

MARKERS = ("W574 H", "W575 touch tooltip", "W581 touch tooltip")

targets = []
for p in sorted(glob.glob("site/data/*.html") + glob.glob("site/en/*.html")):
    s = open(p, encoding="utf-8", errors="ignore").read()
    if any(m in s for m in MARKERS):
        targets.append(p)

print("upgrade targets:", len(targets))
bad = []
for p in targets:
    s = open(p, encoding="utf-8", newline="").read()
    h, t = s.count(HEAD), s.count(TAIL)
    if h != 1 or t != 1:
        bad.append((p, h, t))
        continue
    s = s.replace(HEAD, HEAD_NEW, 1).replace(TAIL, TAIL_NEW, 1)
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)

if bad:
    for p, h, t in bad:
        print("ANCHOR-MISS", p, "head:", h, "tail:", t)
    raise SystemExit(1)
print("all upgraded to capture phase")
