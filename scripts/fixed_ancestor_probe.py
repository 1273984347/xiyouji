"""fixed_ancestor_probe.py — 运行时包含块退化探针（position:fixed 元素 offsetParent ∈ {null, body} 断言）

    机检范式：backdrop-filter/transform/filter 等特性使祖先成为 fixed 后代包含块——一条运行时判定即够。
    固化来源：tmpe/w1146（W1146 举一反三扫描·报告=docs/11-方案报告/审查与评审/包含块退化族举一反三扫描报告-2026-11-06.md）
    """
import json
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

PAGES = [
    "index.html", "guide.html", "curated.html", "dashboard.html", "dukou-engine.html",
    "data/cross-time-danmaku.html", "data/four-heavenly-kings-artifacts.html",
    "data/chapter-stats.html", "data/graph-explorer.html", "data/text-search.html",
    "data/ai-dialogue.html", "data/cipher-bible.html",
    "reader/ch001.html", "en/index.html",
]
VIEWPORTS = [(375, 812), (745, 957), (1440, 900)]

CHECK = """(() => {
    const degraded = [];
    for (const el of document.querySelectorAll('*')) {
        const cs = getComputedStyle(el);
        if (cs.position === 'fixed') {
            const op = el.offsetParent;
            if (op !== null && op !== document.body)
                degraded.push({cls: (el.className||'').toString().slice(0,40),
                               tag: el.tagName, anchor: (op.className||op.tagName).toString().slice(0,40)});
        }
    }
    const overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
    return {degraded, overflow};
})()"""


def probe_page(b, out, pg_name, w, h=957):
    """单页单视口探针（W1147：自 main 循环抽出·嵌套深度归阈内）。"""
    pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    url = "http://127.0.0.1:8792/site/" + pg_name
    try:
        pg.goto(url, wait_until="load")
        pg.wait_for_timeout(900)
        r = pg.evaluate(CHECK)
        key = "%s@%d" % (pg_name, w)
        if r["degraded"] or r["overflow"] > 0:
            out[key] = r
    except Exception as e:  # noqa: BLE001 探针容错
        out["%s@%d" % (pg_name, w)] = {"error": repr(e)[:100]}
    finally:
        pg.close()


def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8792", "--bind", "127.0.0.1"],
                           cwd=".", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    out = {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            for w, _h in VIEWPORTS:
                for pg_name in PAGES:
                    probe_page(b, out, pg_name, w)
            b.close()
    finally:
        srv.terminate()
    print(json.dumps(out, ensure_ascii=False, indent=1))
    n_deg = sum(len(v.get("degraded", [])) for v in out.values())
    n_ovf = sum(1 for v in out.values() if v.get("overflow", 0) > 0)
    print("---- 退化元素 %d 个 · 溢出视口 %d 例 ----" % (n_deg, n_ovf))


if __name__ == "__main__":
    main()
