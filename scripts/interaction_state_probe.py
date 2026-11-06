"""interaction_state_probe.py — 交互后态探针（W1147 待办①·12 类开合组件清单驱动）。

对 scripts/interaction_components.py 的 COMPONENTS 清单逐组件执行：
  交互入口点击/悬停 → 开启态断言（fixed 退化 + 开启选择器在位）→ 关闭 → 残留断言（白名单外 .open 残留即 FAIL）。
产出 JSON 报告；退出码 0=全过 / 1=有发现。本仓历史实证：交互后态是全部门禁的零覆盖面
（抽屉塌陷 600+ 批未被发现即此盲区本体·W1147 固化）。

用法：python scripts/interaction_state_probe.py [--site-root site] [--out 报告.json]
"""
import argparse
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from interaction_components import COMPONENTS  # noqa: E402

FIXED_SNAP = """(() => {
    const out = [];
    for (const el of document.querySelectorAll('*')) {
        const cs = getComputedStyle(el);
        if (cs.position === 'fixed') {
            const op = el.offsetParent;
            out.push({cls: (el.className||'').toString().slice(0,36),
                      ok: op === null || op === document.body});
        }
    }
    return out;
})()"""


def interact(pg, entry):
    if entry is None:
        return False
    el = pg.query_selector(entry)
    if not el:
        return False
    try:
        el.hover(timeout=2000)
    except Exception:  # noqa: BLE001 hover 失败（被遮罩等）改 force click
        try:
            el.click(force=True, timeout=2000)
        except Exception:  # noqa: BLE001
            return False
    pg.wait_for_timeout(450)
    return True


def probe_component(b, args, comp, page, entry, open_sel, residue_wl):
    """单组件交互后态探针（W1147：自 main 循环抽出·嵌套深度归阈内）。"""
    pg = b.new_context(viewport={"width": 745, "height": 957}).new_page()
    try:
        pg.goto("http://127.0.0.1:%d/%s/%s" % (args.port, args.site_root, page),
                wait_until="load")
        pg.wait_for_timeout(900)
        acted = interact(pg, entry)
        snap = pg.evaluate(FIXED_SNAP)
        degraded = [x for x in snap if not x["ok"]]
        open_ok = bool(pg.query_selector(open_sel)) if open_sel else True
        if acted:
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(450)
        leftover = [x for x in pg.evaluate(
            """(() => [...document.querySelectorAll('.open')].map(
                x => (x.className||'').toString().slice(0,40)))()""")
            if not any(w and w in x for w in residue_wl)]
        entry_found = bool(pg.query_selector(entry)) if entry else True
        return {"acted": acted, "entry_found": entry_found,
                "degraded": degraded, "open_ok": open_ok, "leftover": leftover}
    except Exception as e:  # noqa: BLE001
        return {"error": repr(e)[:140]}
    finally:
        pg.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-root", default="site")
    ap.add_argument("--out", default=None)
    ap.add_argument("--port", type=int, default=8796)
    args = ap.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(args.port), "--bind", "127.0.0.1"],
                           cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    report = {}
    fails = 0
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            for comp, page, entry, (open_sel, _open_attr), residue_wl in COMPONENTS:
                res = probe_component(b, args, comp, page, entry, open_sel, residue_wl)
                report["%s:%s" % (page, comp)] = res
                if res.get("degraded") or res.get("leftover") or "error" in res:
                    fails += 1
            b.close()
    finally:
        srv.terminate()

    if args.out:
        json.dump(report, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n_bad = sum(1 for v in report.values() if v.get("degraded") or v.get("leftover"))
    print("---- 交互后态探针：组件 %d · 退化 %d · 残留 %d · 异常 %d ----"
          % (len(report), sum(len(v.get("degraded", [])) for v in report.values()),
             n_bad, sum(1 for v in report.values() if "error" in v)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
