"""W575 池枚举与形态盘点（方案H全量推开前置取证）。

池定义沿用方案H/试点批口径：site/data/*.html 含 'mouseover' 且不含 'touchstart'。
每页盘点：tooltip 元素选择器 / visible 机制 / pointer 事件占用 / Three.js / d3.zoom / canvas。
输出 JSON 到 stdout（勿与其他输出混读）。
"""
import glob
import json
import re


def scan_page(path: str) -> dict:
    src = open(path, encoding="utf-8", errors="ignore").read()
    d = {"page": path.replace("\\", "/")}
    # tooltip 元素候选：id/class 声明
    ids = set(re.findall(r'id="([^"]*tooltip[^"]*)"', src, re.I))
    d["tooltip_ids"] = sorted(ids)
    d["chart_tooltip_class"] = ".chart-tooltip" in src
    d["visible_classed"] = bool(re.search(r'classed\(\s*["\']visible', src))
    d["visible_classlist"] = bool(re.search(r"classList\.(add|toggle|remove)\(\s*['\"]visible", src))
    d["mouseover"] = "mouseover" in src
    d["mouseenter"] = "mouseenter" in src
    d["touchstart"] = "touchstart" in src
    d["pointer_events"] = sorted(set(re.findall(r"pointer(?:over|enter|move|down|up)", src)))
    d["three_js"] = "three.r128" in src or "THREE." in src
    d["d3_zoom"] = bool(re.search(r"d3\.zoom\(", src))
    d["canvas_tag"] = "<canvas" in src
    d["tooltip_func"] = sorted(set(re.findall(r"function\s+(show\w*Tooltip|hide\w*Tooltip|move\w*Tooltip)\s*\(", src)))
    return d


def main() -> None:
    pool = []
    for p in sorted(glob.glob("site/data/*.html")):
        src = open(p, encoding="utf-8", errors="ignore").read()
        if "mouseover" in src and "touchstart" not in src:
            pool.append(p)
    out = {
        "pool_size": len(pool),
        "pages": [scan_page(p) for p in pool],
    }
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
