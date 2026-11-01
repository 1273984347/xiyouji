#!/usr/bin/env python3
"""逐段渲染探针：定位图表色改动下 DOM 塌缩的真实成因（W1084）。

背景：W1080（var() 直喂）与 W1082（求值实际色值）两轮试点都出现同一症状——
`en/global-pattern.html` 暗色下 J2 可见元素数由 532/533 塌缩到 108/109；
W1083 自审发现「改动点（renderTimeline 行 1894/1903）与塌缩点（更早的卡片区）
不同源」，故此前「改动致因」的结论降级为未证实。本工具的职责就是取证，不是修复。

四个取证设计（对应「先取证据再下结论」纪律）：

1. **A/B 在 HTTP 层做文本替换**：本地 http.server + Playwright route 拦截，
   `site/` 工作树零改动 ⇒ 两态的唯一差异就是那两行颜色写法，无他因。
2. **错误捕获**：捕获 window.onerror / unhandledrejection，并**拦截 window.d3 赋值**
   包装 d3 顶层 API ⇒ 能定位「哪个 d3 调用抛错 + 栈」。
3. **塌缩形态二分**：每 100ms 采样，区分
   - 元素**不存在**（DOM 里没有）⇒ 渲染中断
   - 元素**零尺寸**（存在但 rect 宽高全零）⇒ 可见性变化
   两者的探针读数完全不同，不能混为一谈。
4. **时间序列**：输出逐样本序列 + 三态首个分叉点，可复核「分叉发生在哪一次
   渲染/修复波次」。

用法：
    py -3 scripts/chart_render_probe.py --page en/global-pattern.html \
        --variants base,var,token --out scripts/output/_w1084_probe.json
    py -3 scripts/chart_render_probe.py --self-test
"""

from __future__ import annotations

import argparse
import functools
import json
import os
import sys
import threading
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "site")

# 三态的替换规则：锚点是行 1894 / 1903 的 .style() 调用（唯一命中，
# 常量表行 1734 的 "#c8463a" 无 ".style(" 前缀故不会被误替换）。
# 变体名带 _csp 后缀者 = 改写后**同步重算 CSP 哈希**（对照「改内联脚本必须
# 重跑 generate_csp.py」这条铁律：不同步则整脚本被 CSP 拒执行 ⇒ 元素数塌缩
# 到「只剩静态 HTML」的水平，那是假塌缩而非页面真实行为）。
VARIANTS = {
    "base": [],
    "var": [
        ('.style("stroke", "#c8463a")', '.style("stroke", "var(--chart-1)")'),
        ('.style("fill", "#c8463a")', '.style("fill", "var(--chart-1)")'),
    ],
    "token": [
        ('.style("stroke", "#c8463a")',
         '.style("stroke", "window.__chartTokens.get(\'chart-1\')")'),
        ('.style("fill", "#c8463a")',
         '.style("fill", "window.__chartTokens.get(\'chart-1\')")'),
    ],
    # 同上两组 + 同步 CSP 哈希（对照组：塌缩是否随 CSP 同步而消失）
    "var_csp": [
        ('.style("stroke", "#c8463a")', '.style("stroke", "var(--chart-1)")'),
        ('.style("fill", "#c8463a")', '.style("fill", "var(--chart-1)")'),
    ],
    "token_csp": [
        ('.style("stroke", "#c8463a")',
         '.style("stroke", "window.__chartTokens.get(\'chart-1\')")'),
        ('.style("fill", "#c8463a")',
         '.style("fill", "window.__chartTokens.get(\'chart-1\')")'),
    ],
}
# 需要同步 CSP 的变体后缀
CSP_SYNC_SUFFIX = "_csp"

# 探针注入代码（页面任何脚本之前执行）。
PROBE_JS = r"""
(() => {
  const P = { errors: [], d3errors: [], samples: [], mutLog: [], mutations: 0,
              console: [], t0: Date.now() };
  window.__probe = P;
  window.__chartTokens = {
    get(name) {
      try {
        const v = getComputedStyle(document.documentElement)
          .getPropertyValue('--' + name).trim();
        return v || '#c8463a';
      } catch (e) { return '#c8463a'; }
    }
  };
  window.addEventListener('error', (e) => {
    P.errors.push({ t: Date.now() - P.t0, type: 'error',
      msg: String((e.message) || (e.error && e.error.message) || ''),
      src: String(e.filename || ''), line: e.lineno || 0 });
  });
  window.addEventListener('unhandledrejection', (e) => {
    const r = e.reason;
    P.errors.push({ t: Date.now() - P.t0, type: 'rejection',
      msg: String((r && r.message) || r || '') });
  });
  // 拦截 window.d3 赋值：包装顶层 API，捕获「哪个调用抛错 + 栈」。
  let _d3;
  Object.defineProperty(window, 'd3', {
    configurable: true,
    get() { return _d3; },
    set(v) {
      _d3 = v;
      try {
        for (const k of Object.keys(v)) {
          const orig = v[k];
          if (typeof orig !== 'function' || orig.__wrapped) continue;
          const w = function (...args) {
            try { return orig.apply(this, args); }
            catch (e) {
              P.d3errors.push({ t: Date.now() - P.t0, fn: k,
                msg: String((e && e.message) || e),
                stack: String((e && e.stack) || '').split('\n').slice(0, 4).join(' | ') });
              throw e;
            }
          };
          w.__wrapped = true;
          try { v[k] = w; } catch (_) { /* 只读属性则跳过 */ }
        }
      } catch (e) {
        P.errors.push({ t: Date.now() - P.t0, type: 'd3wrap', msg: String(e) });
      }
    }
  });
  const vis = (el) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return !(r.width === 0 && r.height === 0);
  };
  const snap = () => {
    const all = document.querySelectorAll('*');
    let visible = 0;
    for (const el of all) if (vis(el)) visible++;
    const grid = document.getElementById('pilgrim-grid');
    const cards = document.querySelectorAll('#pilgrim-grid .pilgrim-card');
    let cardsVis = 0;
    for (const c of cards) if (vis(c)) cardsVis++;
    const c0 = cards[0];
    const gr = grid ? grid.getBoundingClientRect() : null;
    const cr = c0 ? c0.getBoundingClientRect() : null;
    const tl = document.getElementById('timeline');
    // 注入有效性断言：枚举 #timeline 内所有内联色值 ⇒ 证明替换真的生效
    // （防「替换未生效却据此下结论」的自我确认）。
    const tlStyles = (function () {
      const vals = [];
      document.querySelectorAll('#timeline line, #timeline text').forEach((n) => {
        const v = n.style.stroke || n.style.fill || '';
        if (v) vals.push(v);
      });
      return Array.from(new Set(vals)).join(' | ');
    })();
    // 计算样式读数（J2 属性集**不含** SVG stroke/fill ⇒ 「零差异」测不出令牌跟随）
    const computed = (sel, prop) => {
      const vals = [];
      document.querySelectorAll(sel).forEach((n) => {
        const v = getComputedStyle(n).getPropertyValue(prop);
        if (v) vals.push(v.trim());
      });
      return Array.from(new Set(vals)).sort().join(' | ');
    };
    const strokeComputed = computed('#timeline line', 'stroke');
    const fillComputed = computed('#timeline text', 'fill');
    return {
      t: Date.now() - P.t0,
      total: all.length,
      visible: visible,
      cards: cards.length,
      cardsVis: cardsVis,
      gridW: gr ? Math.round(gr.width * 10) / 10 : null,
      gridH: gr ? Math.round(gr.height * 10) / 10 : null,
      card0W: cr ? Math.round(cr.width * 10) / 10 : null,
      card0H: cr ? Math.round(cr.height * 10) / 10 : null,
      tlChildren: tl ? tl.children.length : null,
      journeyRows: document.querySelectorAll('#journey-table tbody tr').length,
      treemapPaths: document.querySelectorAll('#chart-country path').length,
      bodyH: Math.round(document.body.getBoundingClientRect().height),
      tlStyles: tlStyles,
      strokeComputed: strokeComputed,
      fillComputed: fillComputed
    };
  };
  const tick = () => {
    try { P.samples.push(snap()); }
    catch (e) { P.errors.push({ t: Date.now() - P.t0, type: 'sample', msg: String(e) }); }
  };
  // console 捕获：页面把「使用内嵌数据」等关键信息打在 console 上。
  for (const lvl of ['warn', 'error', 'info', 'log']) {
    const orig = console[lvl];
    console[lvl] = function (...a) {
      try {
        P.console.push({ t: Date.now() - P.t0, level: lvl,
                         msg: a.map((x) => String(x)).join(' ') });
      } catch (_) { /* 不阻断页面 */ }
      return orig.apply(console, a);
    };
  }
  const startObs = () => {
    try {
      new MutationObserver((recs) => {
        P.mutations += recs.length;
        if (P.mutLog.length >= 400) return;
        for (const r of recs) {
          if (r.type !== 'childList') continue;
          const tg = r.target;
          const id = tg.id ? '#' + tg.id
            : (typeof tg.className === 'string' && tg.className
                ? '.' + tg.className.trim().split(/\s+/).slice(0, 2).join('.')
                : tg.tagName);
          P.mutLog.push({ t: Date.now() - P.t0, target: String(id),
            added: r.addedNodes.length, removed: r.removedNodes.length });
        }
      }).observe(document.documentElement,
        { subtree: true, childList: true, attributes: true, characterData: true });
    } catch (_) { /* 观察失败不阻断采样 */ }
  };
  document.addEventListener('DOMContentLoaded', startObs);
  setInterval(tick, 100);
  tick();
})();
"""

# 终态对拍关注的字段。
COMPARE_FIELDS = (
    "total", "visible", "cards", "cardsVis", "gridW", "gridH",
    "card0W", "card0H", "tlChildren", "journeyRows", "treemapPaths", "bodyH",
    "tlStyles",
)


def _serve_site():
    """起本地 http.server（root = site/）并返回 (server, base_url)。"""
    handler = functools.partial(SimpleHTTPRequestHandler, directory=SITE)
    handler.log_message = lambda *a, **k: None  # 静音
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd, "http://127.0.0.1:%d" % httpd.server_address[1]


def _capture_variant(browser, page_url, rel_path, variant, theme, floor_ms):
    """采集单态：HTTP 层替换 → 注入探针 → 采样 → 取回探针数据。"""
    from playwright.sync_api import sync_playwright  # noqa: F401  (仅做可用性提示)

    scheme = "dark" if theme == "dark" else "light"
    out = {"variant": variant, "theme": theme, "page": rel_path,
           "samples": [], "errors": [], "d3errors": [], "mutLog": [],
           "mutations": 0, "anchor_hits": 0, "console": [], "selfcheck": []}
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        try:
            ctx = b.new_context(reduced_motion="reduce", color_scheme=scheme)
            page = ctx.new_page()
            hits = {"n": 0}
            selfcheck = []
            # 浏览器层 console（页面内包装器抓不到「浏览器自己发出」的消息——
            # 典型如 CSP 违规：Executing inline script violates …）
            browser_msgs = []
            page.on("console", lambda m: browser_msgs.append(
                {"level": m.type, "msg": m.text, "src": "browser"}))

            def handler(route):
                resp = route.fetch()
                body = resp.text()
                for old, new in VARIANTS[variant]:
                    if old not in body:
                        raise SystemExit("替换锚点缺失（%s）：%r" % (variant, old))
                    body = body.replace(old, new)
                    hits["n"] += 1
                if variant.endswith(CSP_SYNC_SUFFIX):
                    # 同步重算 CSP 哈希（复用 generate_csp.py 同一套实现·避免口径漂移）
                    sys.path.insert(0, HERE)
                    from generate_csp import build_policy, inject  # noqa: WPS433
                    body = inject(body, build_policy(body, False))
                # 【判据自纠·W1084】改写 body 后必须去掉原 Content-Length：
                # 沿用旧长度会被浏览器按声明长度截断响应 ⇒ 页面 <script> 块解析
                # 失败 ⇒ 元素数塌缩 —— 那是探针自造的假象，不是页面真实行为。
                headers = {k: v for k, v in resp.headers.items()
                           if k.lower() != "content-length"}
                route.fulfill(status=resp.status, headers=headers, body=body)
                selfcheck.append({"bytes": len(body.encode("utf-8")),
                                  "declared_len": resp.headers.get("content-length")})

            page.route("**" + rel_path, handler)
            page.add_init_script(PROBE_JS)
            page.goto(page_url + "/" + rel_path, wait_until="networkidle",
                      timeout=60000)
            page.wait_for_timeout(floor_ms)
            data = page.evaluate("() => window.__probe")
            out.update({
                "samples": data.get("samples") or [],
                "errors": data.get("errors") or [],
                "d3errors": data.get("d3errors") or [],
                "mutLog": data.get("mutLog") or [],
                "mutations": data.get("mutations") or 0,
                "anchor_hits": hits["n"],
                "console": data.get("console") or [],
                "browser_console": browser_msgs,
                "selfcheck": selfcheck,
                # 一等读数：CSP 违规条数（改内联脚本未同步哈希 ⇒ 整脚本被拒执行
                # ⇒ 页面塌到只剩静态 HTML。取证第一步就是查这个数）
                "csp_violations": sum(
                    1 for m in (list(data.get("console") or []) + browser_msgs)
                    if "Content Security Policy" in str(m.get("msg", ""))),
            })
            ctx.close()
        finally:
            b.close()
    return out


def _final(sample_rows):
    return sample_rows[-1] if sample_rows else {}


def compare(base, other):
    """两态终态逐字段对拍（区分「不存在」与「零尺寸」）。"""
    fb, fo = _final(base["samples"]), _final(other["samples"])
    fields = []
    for f in COMPARE_FIELDS:
        vb, vo = fb.get(f), fo.get(f)
        fields.append({
            "field": f,
            "base": vb,
            "other": vo,
            "same": vb == vo,
        })
    diff = [f for f in fields if not f["same"]]
    # 分叉时刻：base 与 other 各自「该字段最终值首次出现」的样本时间
    divergence = None
    for f in diff:
        fb_v, fo_v = f["base"], f["other"]
        tb = next((s["t"] for s in base["samples"] if s.get(f["field"]) == fb_v), None)
        to = next((s["t"] for s in other["samples"] if s.get(f["field"]) == fo_v), None)
        divergence = {"field": f["field"], "base_t": tb, "other_t": to,
                      "delta_ms": (to - tb) if (tb is not None and to is not None) else None}
        break
    return {"fields": fields, "diff_fields": [f["field"] for f in diff],
            "first_divergence": divergence}


def _self_test():
    """自测：探针必须能区分「元素不存在」与「元素零尺寸」两种塌缩形态。

    构造两页：
      - vanish：把卡片 display:none ⇒ 元素仍在 DOM，但 J2 判据不可见
      - remove：把卡片从 DOM 移除 ⇒ 元素不存在
    两页的 visible 读数都下降，但 cards/cardsVis 读数不同 ⇒ 探针可二分。
    """
    import tempfile
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        print("SKIP: playwright 不可用 —— %s" % e)
        return 0
    tmp = tempfile.mkdtemp(prefix="w1084_selftest_")
    page_html = """<!doctype html><meta charset="utf-8">
<style>#box{width:100px;height:40px;background:#333}</style>
<div id="box">x</div><div id="pilgrim-grid"></div>
<script>
const mode = new URLSearchParams(location.search).get('m');
const g = document.getElementById('pilgrim-grid');
const c = document.createElement('div'); c.className='pilgrim-card';
c.textContent='c'; g.appendChild(c);
if (mode === 'vanish') { c.style.display='none'; }
if (mode === 'remove') { c.remove(); }
</script>"""
    with open(os.path.join(tmp, "t.html"), "w", encoding="utf-8") as f:
        f.write(page_html)
    results = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        try:
            for mode in ("keep", "vanish", "remove"):
                ctx = b.new_context(reduced_motion="reduce", color_scheme="light")
                page = ctx.new_page()
                page.add_init_script(PROBE_JS)
                page.goto("file:///" + os.path.join(tmp, "t.html").replace("\\", "/")
                          + "?m=" + mode, wait_until="networkidle")
                page.wait_for_timeout(600)
                d = page.evaluate("() => window.__probe")
                s = _final(d.get("samples") or [])
                results[mode] = {"visible": s.get("visible"), "cards": s.get("cards"),
                                 "cardsVis": s.get("cardsVis")}
                ctx.close()
        finally:
            b.close()
    ok = True
    k, v, r = results["keep"], results["vanish"], results["remove"]
    print("keep   =", k)
    print("vanish =", v)
    print("remove =", r)
    if not (k["visible"] > v["visible"] and k["visible"] > r["visible"]):
        print("FAIL: 两种塌缩形态的 visible 均应低于基线")
        ok = False
    if not (v["cards"] == 1 and v["cardsVis"] == 0):
        print("FAIL: vanish 态应 cards=1 且 cardsVis=0（元素在·不可见）")
        ok = False
    if not (r["cards"] == 0):
        print("FAIL: remove 态应 cards=0（元素不在）")
        ok = False
    print("SELF-TEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="逐段渲染探针（W1084）")
    ap.add_argument("--page", default="en/global-pattern.html",
                    help="site/ 下的相对路径")
    ap.add_argument("--variants", default="base,var,token",
                    help="逗号分隔：base,var,token")
    ap.add_argument("--theme", default="both", choices=("light", "dark", "both"))
    ap.add_argument("--out", default="", help="输出 JSON 路径")
    ap.add_argument("--floor-ms", type=int, default=16000,
                    help="采集前地板等待（覆盖 setTimeout 修复波次）")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return _self_test()

    rel = args.page.replace("\\", "/").lstrip("/")
    if not os.path.isfile(os.path.join(SITE, rel.replace("/", os.sep))):
        print("FAIL: 目标页不存在 site/%s" % rel)
        return 1
    variants = [v.strip() for v in args.variants.split(",") if v.strip()]
    for v in variants:
        if v not in VARIANTS:
            print("FAIL: 未知变体 %r" % v)
            return 1
    themes = ("light", "dark") if args.theme == "both" else (args.theme,)

    httpd, base_url = _serve_site()
    result = {"schema": "w1084-chart-render-probe/1",
              "captured_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
              "page": rel, "floor_ms": args.floor_ms,
              "variants": {}, "compare": {}}
    try:
        for theme in themes:
            for v in variants:
                print("[probe] %s / %s ..." % (theme, v), flush=True)
                data = _capture_variant(None, base_url, rel, v, theme, args.floor_ms)
                key = "%s::%s" % (theme, v)
                result["variants"][key] = data
                fb = _final(data["samples"])
                print("   total=%s visible=%s cards=%s cardsVis=%s errors=%d d3errors=%d"
                      " | bytes=%s"
                      % (fb.get("total"), fb.get("visible"), fb.get("cards"),
                         fb.get("cardsVis"), len(data["errors"]), len(data["d3errors"]),
                         (data["selfcheck"] or [{}])[0].get("bytes")),
                      flush=True)
                print("   tlStyles=%r" % (fb.get("tlStyles"),), flush=True)
                print("   cspViolations=%d" % (data.get("csp_violations") or 0),
                      flush=True)
                for e in (data["errors"] or [])[:4]:
                    print("   ERR %r" % (e,), flush=True)
                for e in (data["d3errors"] or [])[:4]:
                    print("   D3ERR %r" % (e,), flush=True)
                for e in (data["console"] or [])[:6]:
                    print("   CONSOLE[%s] %s" % (e.get("level"), e.get("msg")), flush=True)
            for v in variants:
                if v == "base":
                    continue
                key = "%s::%s" % (theme, v)
                bkey = "%s::base" % theme
                if bkey in result["variants"] and key in result["variants"]:
                    result["compare"][key] = compare(result["variants"][bkey],
                                                     result["variants"][key])
    finally:
        httpd.shutdown()

    if args.out:
        outp = args.out if os.path.isabs(args.out) else os.path.join(ROOT, args.out)
        os.makedirs(os.path.dirname(outp), exist_ok=True)
        with open(outp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(result, f, ensure_ascii=False, indent=1)
        print("OUT: %s" % outp)

    for key, cmp_ in result["compare"].items():
        print("[compare] %s → diff=%s" % (key, cmp_["diff_fields"] or "无差异"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
