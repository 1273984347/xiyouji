# -*- coding: utf-8 -*-
"""把 tokens.css 与 system.css 原样内联进两页样板（双击即开，零外域）。"""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, ".."))
tokens = io.open(os.path.join(OUT, "tokens.css"), encoding="utf-8").read()
system = io.open(os.path.join(OUT, "system.css"), encoding="utf-8").read()
for name in ("landing", "dataviz"):
    tpl = io.open(os.path.join(HERE, "tpl_%s.html" % name), encoding="utf-8").read()
    html = tpl.replace("/*@TOKENS@*/", tokens).replace("/*@SYSTEM@*/", system)
    target = os.path.join(OUT, "sample-%s.html" % name)
    with io.open(target, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("sample-%s.html" % name, len(html), "chars")
