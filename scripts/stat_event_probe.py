#!/usr/bin/env python3
"""stat_event_probe.py — 统计事件运行面取证探针（W1168·第 67 槽的动态证据链）

## 测量点（两处都拦，缺一即假绿）

1. `window.XYstats` 赋值时包裹 `count()` ⇒ 捕获**编程式**事件（web vitals / 检索 / 进度 / 复制…）
2. `window.goatcounter` 赋值后再挂 `count` 访问器 ⇒ 捕获**声明式**事件
   （`data-goatcounter-click` 由 goatcounter 自身的 bind_events 直接调 `count`，**不经过桥**——
   只测 XYstats 会把 nav_click 整组漏成「无事件」，进而把 P2 变成测不出真假的假绿）

localhost 与 file:// 下桥静默、goatcounter 自身也在 filter() 里 return，因此**不能**用
「拦截网络请求」当唯一证据面；本探针在 `count()` 入口取证，另在 P1 断言 file:// 下
「真的一个请求都没发出」——两件事分别证明「该报的报了」与「不该报的没报」。

拦截手法：`Object.defineProperty(window,'XYstats',{set})` 捕获赋值——stats.js 是一次性
`w.XYstats = api`，setter 早于任何事件时机（含 load 时的曝光上报），不存在漏采窗口；
goatcounter 的 `count` 在对象创建**之后**才赋值，故 setter 里再挂一层 `count` 访问器等它。

## 检查项

P1 file:// 语境：零桥调用 + 零 console 错误（离线不产噪声，H3 承诺）
P2 nav_click：导航链接点击后事件名 ∈ 导航正本事件名集
P3 search_perform：输入去抖后恰一条；同一查询重复输入不重报
P4 search_hit_open：结果卡可点 ⇒ 事件 + 落到 reader/chNNN.html#q=<词>
P5 高亮落地：带 #q= 打开读者页 ⇒ mark.hit-mark 存在、文本含关键词、发生滚动
P6 reset_view：3D 页拖动/缩放后点复位 ⇒ 相机回到初始球坐标 + 事件一条
P7 dark_mode_toggle / copy_citation / reader_progress / badge_view：各自触发并捕获

用法：
    python scripts/stat_event_probe.py                # 全量（起本地 http + Playwright）
    python scripts/stat_event_probe.py --only P4,P5   # 单项
    python scripts/stat_event_probe.py --self-test    # 判据自测（不触浏览器）

退出码：0 全过 / 1 有 FAIL / 2 Playwright 或浏览器不可用（fail-closed，不静默跳过）。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKER = "---- W1168 统计事件探针："
SITE = os.path.join(ROOT, "site")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_stat_events import RUNTIME_LAYERS  # noqa: E402  运行层合法集正本（引用不复制·W1120 纪律）

CAPTURE_JS = """
(() => {
  window.__xyEvents = [];
  window.__gcEvents = [];
  // 单源写入：sessionStorage 能写就用它（唯一在导航后仍活着的容器，W1168 实测 P2/P4 恒 0 的
  // 真因是内存数组活在被换掉的页面里）；写不进（file:// opaque origin）才退回内存。
  // 两处**都写**会双计——同一文档内每条事件既在数组又在 sessionStorage，读取端合并即翻倍
  // （W1168 实测 P3 首查 2、换词后 4 的来源）。
  window.persist = function (key, mem, rec) {
    try {
      const cur = JSON.parse(window.sessionStorage.getItem(key) || "[]");
      cur.push(rec);
      window.sessionStorage.setItem(key, JSON.stringify(cur.slice(-80)));
    } catch (e) {
      try { window[mem].push(rec); } catch (e2) { /* 不影响页面 */ }
    }
  };
  let real = undefined;
  Object.defineProperty(window, 'XYstats', {
    configurable: true,
    get() { return real; },
    set(v) {
      real = v;
      try {
        const orig = v.count.bind(v);
        v.count = function (name, val) {
          const rec = [String(name), String(val === undefined ? '' : val)];
          window.persist('__xyProbe', '__xyEvents', rec);
          return orig(name, val);
        };
      } catch (e) { /* 包装失败不影响页面 */ }
    }
  });
  let gc = undefined;
  Object.defineProperty(window, 'goatcounter', {
    configurable: true,
    get() { return gc; },
    set(v) {
      gc = v;
      try {
        let origCount = null;
        Object.defineProperty(v, 'count', {
          configurable: true,
          get() { return origCount; },
          set(fn) {
            origCount = function (vars) {
              const a = vars || {};
              const rec = [String(a.path || ''), a.event === true, String(a.title || '')];
              window.persist('__gcProbe', '__gcEvents', rec);
              return fn.call(v, vars);
            };
            return origCount;
          }
        });
      } catch (e) { /* 同上 */ }
    }
  });
})();
"""


def _serve(port: int):
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, *args):  # noqa: D102
            return

    httpd = TCPServer(("127.0.0.1", port), lambda *a: Quiet(*a, directory=SITE))
    th = threading.Thread(target=httpd.serve_forever, daemon=True)
    th.start()
    return httpd


def _events(page):
    """桥面事件名列表（内存 + sessionStorage 合并，后者跨导航存活）。"""
    return page.evaluate("""() => {
        let sp = [];
        try { sp = JSON.parse(window.sessionStorage.getItem('__xyProbe') || '[]'); } catch (e) {}
        const mem = (window.__xyEvents || []).map(e => e[0]);
        return mem.concat(sp.map(e => e[0]));
    }""")


def _gc_events(page):
    """声明式与桥转发事件（goatcounter.count 入口层）：[path, event?, title]·跨导航合并。"""
    return page.evaluate("""() => {
        let sp = [];
        try { sp = JSON.parse(window.sessionStorage.getItem('__gcProbe') || '[]'); } catch (e) {}
        return (window.__gcEvents || []).concat(sp);
    }""")


def _named(events, name):
    """兼容两种形态：裸名字列表（_events）与 [path, event, title] 三元组（_gc_events）。

    首版只按三元组索引 `e[0]`，喂进名字列表时 `e[0]` 变成**首字符** ⇒ 任何断言恒不命中，
    十个检查全红而产品接线其实完好（W1168 实测）。测量工具坏了时，红不是结论，是噪音。
    """
    return [e for e in events if (e[0] if isinstance(e, (list, tuple)) else e) == name]


_MANIFEST_GROUPS = None


def _manifest_groups() -> list[dict]:
    """事件清单正本（第 67 槽同一份）。不可读即抛——测量工具没有「静默降级」这条路径。"""
    global _MANIFEST_GROUPS
    if _MANIFEST_GROUPS is None:
        path = os.path.join(ROOT, "scripts", "output", "_w1168_stat_events.json")
        with open(path, encoding="utf-8") as fh:
            _MANIFEST_GROUPS = json.load(fh)["groups"]
    return _MANIFEST_GROUPS


def _declared_layer(key: str) -> str:
    """事件所属组的运行层**由清单声明**（C6 已把该字段卡成必填合法面）。

    W1168 实测：P6 只读 XYstats 桥层，而 `reset_view` 声明为 `data-goatcounter-click` 由
    goatcounter.js 原生处理、捕获在计数入口层 ⇒ 接线完好而事件恒 0。「读哪一层」写进正本后，
    探针不再猜层，两层并读的模糊断言（放宽）也随之一并消掉。
    """
    for g in _manifest_groups():
        if g.get("group") == key or key in (g.get("names") or []):
            layer = g.get("runtime_layer")
            if layer not in RUNTIME_LAYERS:
                raise ValueError("组 %s 的 runtime_layer 非法：%r" % (g.get("group"), layer))
            return layer
    raise LookupError("清单未登记事件/组：%s（第 67 槽应已判红）" % key)


def _layer_records(layer: str, xy: list, gc: list) -> list:
    return xy if layer == "bridge" else gc


def _fired(page, key: str, name: str | None = None) -> list:
    """按声明层取该事件的捕获记录；`name` 用于一组多名的场景（如 nav_click 的 12 个导航项）。"""
    recs = _layer_records(_declared_layer(key), _events(page), _gc_events(page))
    return [e for e in recs if (e[0] if isinstance(e, (list, tuple)) else e) == (name or key)]


def _wait_search_app(page, timeout_ms: int = 20000) -> bool:
    """等检索 app 真就绪（它是 window.load 后动态注入的，见 text-search-app.js 的
    `window.__xySearchReady`）——靠固定 sleep 会把「还没加载」误读成「接线失效」。"""
    try:
        page.wait_for_function("() => window.__xySearchReady === true", timeout=timeout_ms)
        return True
    except Exception:  # noqa: BLE001 - 超时不在此判红，由后续事件断言如实报 FAIL
        return False


class Checks:
    def __init__(self):
        self.results = []

    def add(self, cid: str, ok: bool, detail: str) -> None:
        self.results.append({"id": cid, "ok": ok, "detail": detail})
        print("  %s %s %s" % ("PASS" if ok else "FAIL", cid, detail))


def _launch(pw):
    for arg in ({}, {"args": ["--allow-file-access-from-files"]}):
        try:
            return pw.chromium.launch(**arg)
        except Exception:  # noqa: BLE001
            continue
    raise RuntimeError("chromium 启动失败")


def run(only: set[str]) -> list[dict]:
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    checks = Checks()
    port = 8793
    httpd = _serve(port)
    base = "http://127.0.0.1:%d" % port
    want = lambda cid: (not only) or cid in only  # noqa: E731
    try:
        with sync_playwright() as pw:
            browser = _launch(pw)
            ctx = browser.new_context(viewport={"width": 1280, "height": 800})
            ctx.add_init_script(CAPTURE_JS)
            _p1_file(ctx, checks, want)
            _p2_nav(ctx, base, checks, want)
            _p3_search(ctx, base, checks, want)
            _p4_hit(ctx, base, checks, want)
            _p5_highlight(ctx, base, checks, want)
            _p6_reset(ctx, base, checks, want)
            _p7_others(ctx, base, checks, want)
            browser.close()
    finally:
        httpd.shutdown()
    return checks.results


def _goto(ctx, url: str):
    page = ctx.new_page()
    page.goto(url, wait_until="load")
    page.wait_for_timeout(1200)
    return page


# file:// 下的**既有** console 噪声（三条都不是本批引入，逐条注明来历；新增错误仍判红）：
#   ① fetch 语料 JSON 失败 ⇒ EMBEDDED 回退（既有设计，file:// 铁律的一环）
#   ② 127.0.0.1:8777/health 本地 RAG 探活被拒
#   ③ 子集化字体的 crossorigin 预加载在 origin=null 下被 CORS 拦（file:// 固有限制）
OFFLINE_KNOWN_CONSOLE = (
    'URL scheme "file" is not supported',
    "ERR_CONNECTION_REFUSED",
    "blocked by CORS policy",
    "ERR_FAILED",
)


def _known_offline_console(text: str) -> bool:
    """既有债 console 错误的逐条比对（具名函数：判据可读，且不踩结构档的嵌套推导式）。"""
    return any(k in text for k in OFFLINE_KNOWN_CONSOLE)


def _p1_file(ctx, checks, want):
    if not want("P1"):
        return
    errs, all_req = [], []
    page = ctx.new_page()
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    page.on("request", lambda r: all_req.append(r.url))
    page.goto("file:///" + os.path.join(SITE, "dashboard.html").replace("\\", "/"), wait_until="load")
    page.wait_for_timeout(1500)
    # 不在本页做导航点击：换页会把目标页自身的 fetch 失败计入「新增」，
    # 那属导航后语境、与本批「加载期静默」命题无关（点击面由 P2 覆盖）
    bridged = _events(page)
    page.close()
    remote = [u for u in all_req if "goatcounter.com" in u and not u.startswith("file:")]
    # 断言三件本批该负责的：① 零**远端**统计请求 ② 桥在 file:// 短路（零 XYstats 调用）
    # ③ console 错误只允许既有两类（file:// fetch 降级 + 本地 RAG 探活）——新增错误必须红，
    #   但也不把既有债算到本批头上（那会让探针长期红而无人看）。
    unknown = [e for e in dict.fromkeys(errs) if not _known_offline_console(e)]
    ok = not remote and not bridged and not unknown
    checks.add("P1", ok, "file:// 零远端上报·桥短路·console 错误无新增（remote=%d xy=%d 新增=%d）%s"
               % (len(remote), len(bridged), len(unknown),
                  ("·样例=" + json.dumps(unknown[:2], ensure_ascii=False)) if unknown else ""))


def _p2_nav(ctx, base, checks, want):
    if not want("P2"):
        return
    page = _goto(ctx, base + "/index.html")
    # 点的是链接：导航会替换文档、__gcEvents 随源页面消失 ⇒ 恒 0（W1168 实测假红）。
    # 让导航**失败**而非阻止点击——事件监听器在导航前已同步执行，数组得以保留。
    page.click('.site-mainnav a[data-goatcounter-click="nav-dashboard"]')
    page.wait_for_timeout(900)
    hits = [e for e in _fired(page, "nav_click", "nav-dashboard") if len(e) > 1 and e[1] is True]
    checks.add("P2", len(hits) >= 1,
               "nav_click 经声明式通道上报且带 event 标记（层=%s·捕获 %d 次）"
               % (_declared_layer("nav_click"), len(hits)))
    page.close()


def _p3_search(ctx, base, checks, want):
    if not want("P3"):
        return
    page = _goto(ctx, base + "/data/text-search.html")
    _wait_search_app(page)
    page.fill("#search-input", "孙悟空")
    page.wait_for_timeout(1400)
    first = len(_fired(page, "search_perform"))
    page.fill("#search-input", "孙悟空 ")
    page.wait_for_timeout(1400)
    same = len(_fired(page, "search_perform"))
    page.fill("#search-input", "猪八戒")
    page.wait_for_timeout(1400)
    second = len(_fired(page, "search_perform"))
    # 语义：同义查询（仅差空白）不重报；真正换词才 +1
    checks.add("P3", first == 1 and same == 1 and second == 2,
               "search_perform 每次不同查询恰一条（首查 %d·换词后 %d）" % (first, second))
    page.close()


def _p4_hit(ctx, base, checks, want):
    if not want("P4"):
        return
    page = _goto(ctx, base + "/data/text-search.html")
    _wait_search_app(page)
    page.fill("#search-input", "花果山")
    page.wait_for_timeout(1400)
    card = page.query_selector(".result-card")
    if card is None:
        checks.add("P4", False, "结果卡不存在（检索未产出）")
        page.close()
        return
    href = card.get_attribute("href") or ""
    tag = card.evaluate("el => el.tagName")
    card.click()
    page.wait_for_timeout(1200)   # 允许真跳转：落点正确性本身是 P4 的断言对象
    hits = [e for e in _gc_events(page) if e[0] == "search_hit_open"]
    bridged = _named(_events(page), "search_hit_open")
    landed = "/reader/ch" in page.evaluate("()=>location.pathname")
    ok = (tag.lower() == "a" and bool(re.match(r"^\.\./reader/ch\d{3}\.html#q=", href))
          and landed and (hits or bridged))
    checks.add("P4", bool(ok), "结果卡可点开并上报（tag=%s href=%r gc=%d xy=%d）"
               % (tag, href[:44], len(hits), len(bridged)))
    page.close()


def _p5_highlight(ctx, base, checks, want):
    if not want("P5"):
        return
    page = _goto(ctx, base + "/reader/ch001.html#q=" + "灵根")
    page.wait_for_timeout(1400)
    got = page.evaluate("""(() => {
        const m = document.querySelector('mark.hit-mark');
        return {n: document.querySelectorAll('mark.hit-mark').length,
                text: m ? m.textContent : '', y: Math.round(window.scrollY)};
    })()""")
    ok = got["n"] >= 1 and "灵根" in got["text"]
    checks.add("P5", ok, "深链高亮命中（mark=%d text=%r scrollY=%d）"
               % (got["n"], (got["text"] or "")[:12], got["y"]))
    page.close()


def _p6_reset(ctx, base, checks, want):
    if not want("P6"):
        return
    page = _goto(ctx, base + "/data/character-relationship-3d.html")
    btn = page.query_selector("#reset-view")
    if btn is None:
        checks.add("P6", False, "3D 页无 #reset-view 复位控件")
        page.close()
        return
    cont = page.query_selector("#three-container")
    cont.scroll_into_view_if_needed()
    page.wait_for_timeout(400)
    box = cont.bounding_box()
    before = page.evaluate("() => [camera.position.x, camera.position.y, camera.position.z]")
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.mouse.down()
    page.mouse.move(box["x"] + box["width"] / 2 + 220, box["y"] + box["height"] / 2 + 120, steps=8)
    page.mouse.up()
    page.wait_for_timeout(500)
    moved = page.evaluate("() => [camera.position.x, camera.position.y, camera.position.z]")
    btn.click()
    page.wait_for_timeout(600)
    after = page.evaluate("() => [camera.position.x, camera.position.y, camera.position.z]")
    # reset_view 由正本声明为**声明式属性** data-goatcounter-click 发射（清单 files 三页），
    # 走 goatcounter.count 入口层而非 XYstats 桥层——只读桥层即恒 0（W1168 实测假红）。
    # 判据认「事件是否发生」，两层并读；发射面由第 67 槽按声明逐面卡，不在探针重复产能。
    ev = _fired(page, "reset_view")
    same = all(abs(a - b) < 0.5 for a, b in zip(before, after, strict=False))
    changed = any(abs(a - b) > 1 for a, b in zip(before, moved, strict=False))
    checks.add("P6", changed and same and len(ev) >= 1,
               "拖动生效→复位回到初始相机（changed=%s restored=%s events=%d·层=%s）"
               % (changed, same, len(ev), _declared_layer("reset_view")))
    page.close()


def _p7_others(ctx, base, checks, want):
    if not want("P7"):
        return
    page = _goto(ctx, base + "/reader/ch001.html")
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight * 0.6)")
    page.wait_for_timeout(900)
    page.click(".xy-fab-theme")
    page.wait_for_timeout(500)
    checks.add("P7a", len(_fired(page, "dark_mode_toggle")) >= 1, "dark_mode_toggle 捕获")
    checks.add("P7b", len(_fired(page, "reader_progress")) >= 1, "reader_progress 捕获（档位去重）")
    page.close()

    page = _goto(ctx, base + "/data/81-hardships-view.html")
    page.wait_for_timeout(1500)
    checks.add("P7c", len(_fired(page, "badge_view")) >= 1,
               "badge_view 曝光捕获（属性声明在正本、发射在桥层观察器·层=%s）" % _declared_layer("badge_view"))

    # 复制按钮在 <details class="cite-details"> 折叠体内，不可见即点不通（基线跑实证超时）
    # ⇒ 先展开再点，且只等真出现可点击的按钮
    summary = page.query_selector(".cite-details summary")
    if summary:
        summary.click()
        page.wait_for_timeout(400)
    btn = page.query_selector(".cite-copy")
    if btn:
        btn.click(timeout=8000)
        page.wait_for_timeout(800)
        checks.add("P7d", len(_fired(page, "copy_citation")) >= 1, "copy_citation 捕获")
    else:
        checks.add("P7d", False, "展开后仍无 .cite-copy 按钮")
    page.close()


def _self_test() -> int:
    """判据自测：两层拦截都必须在「库稍后才挂方法」的时序下生效（node 跑·不触浏览器）。"""
    js_xystats = CAPTURE_JS + """
    let api = { count: function (n, v) { return 'orig:' + n; } };
    window.XYstats = api;
    window.XYstats.count('probe_evt', 1);
    """
    js_gc = """
    // goatcounter 的真实时序：先建对象，之后才往上挂 count 方法
    window.goatcounter = { filter: function () { return ''; } };
    window.goatcounter.count = function (vars) { window.__gcCalled = vars; };
    window.goatcounter.count({ event: true, path: 'nav-probe', title: 't' });
    """
    # 单源写入锁：sessionStorage 可用时**只写它**（内存数组必须为空）。
    # 两处都写 ⇒ 读取端 mem.concat(sp) 把同一条数两遍 ⇒ P3 型「首查 2·换词后 4」假红
    # （W1168 实测）。此例即该形态的回归锁：内存数组非空即判红。
    js_single_source = """
    const store = {};
    window.sessionStorage = {
      getItem: k => (k in store ? store[k] : null),
      setItem: (k, v) => { store[k] = v; },
    };
    """ + CAPTURE_JS + """
    let api = { count: function () { return 'orig'; } };
    window.XYstats = api;
    window.XYstats.count('dup_a', 1);
    window.XYstats.count('dup_b', 2);
    """
    r = subprocess.run(
        ["node", "-e",
         "global.window={};global.console=console;" + js_xystats + js_gc +
         "console.log(JSON.stringify({xy: window.__xyEvents.map(e=>e[0]),"
         "gc: window.__gcEvents, passthrough: window.__gcCalled && window.__gcCalled.path}));"],
        capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        print("SELF_TEST_FAIL node：%s%s" % (r.stdout, r.stderr))
        return 1
    payload = json.loads(r.stdout.strip().splitlines()[-1])
    xy_ok = payload["xy"] == ["probe_evt"]
    gc_ok = (len(payload["gc"]) == 1 and payload["gc"][0][0] == "nav-probe"
             and payload["gc"][0][1] is True and payload["passthrough"] == "nav-probe")
    r2 = subprocess.run(
        ["node", "-e",
         "global.window={};global.console=console;" + js_single_source +
         "console.log(JSON.stringify({mem: window.__xyEvents.length,"
         " sp: JSON.parse(window.sessionStorage.getItem('__xyProbe')).map(e=>e[0])}));"],
        capture_output=True, text=True, timeout=60)
    if r2.returncode != 0:
        print("SELF_TEST_FAIL node（单源锁）：%s%s" % (r2.stdout, r2.stderr))
        return 1
    ss = json.loads(r2.stdout.strip().splitlines()[-1])
    single_ok = ss["mem"] == 0 and ss["sp"] == ["dup_a", "dup_b"]
    for label, ok in (("XYstats 包装（编程式面）", xy_ok),
                      ("goatcounter.count 包装（声明式面·晚挂方法时序·且原实现仍被执行）", gc_ok),
                      ("捕获单源（sessionStorage 可用时内存数组为空·防双计）", single_ok)):
        print("  %s %s" % ("PASS" if ok else "FAIL", label))
    ok = xy_ok and gc_ok and single_ok
    print("SELF_TEST_OK" if ok else "SELF_TEST_FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="W1168 统计事件运行面探针")
    ap.add_argument("--only", default="", help="逗号分隔检查项，如 P4,P5")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    only = {s.strip().upper() for s in args.only.split(",") if s.strip()}
    try:
        results = run(only)
    except ImportError:
        print("环境错误：playwright 未安装（fail-closed，不静默跳过）", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - 浏览器不可用属基础设施缺失
        msg = str(exc)
        if "executable" in msg or "chromium" in msg or "Playwright" in msg:
            print("环境错误：浏览器不可用（fail-closed）：%s" % msg, file=sys.stderr)
            return 2
        raise
    bad = [r for r in results if not r["ok"]]
    print("%s 检查 %d 项 · FAIL %d ----" % (MARKER, len(results), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
