# -*- coding: utf-8 -*-
"""构建：把 tokens.css + system.css 内联注入三页模板，产出自包含样板页。

样板页为最终交付物，必须双击即开、零外域；本脚本只做注入，不改动设计内容。
用法：py -3 _build.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
PAGES = {"landing": "sample-landing.html", "dataviz": "sample-dataviz.html", "reader": "sample-reader.html"}


def main() -> int:
    tokens = (ROOT / "tokens.css").read_text(encoding="utf-8")
    system = (ROOT / "system.css").read_text(encoding="utf-8")
    for key, out_name in PAGES.items():
        tpl_path = ROOT / "_tpl" / (key + ".html")
        tpl = tpl_path.read_text(encoding="utf-8")
        if "/*__TOKENS__*/" not in tpl or "/*__SYSTEM__*/" not in tpl:
            print("[FAIL] 模板缺少注入标记: %s" % tpl_path.name)
            return 1
        out = tpl.replace("/*__TOKENS__*/", tokens).replace("/*__SYSTEM__*/", system)
        (ROOT / out_name).write_text(out, encoding="utf-8")
        print("[PASS] 构建 %-22s %6d bytes" % (out_name, len(out.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
