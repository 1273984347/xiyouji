#!/usr/bin/env python3
"""_w851_visual_regression_probe.py — J2 视觉回归探针（W851 建·设计迁移阶段 1 验收件）

## 为什么需要它

W826 细化规格 §7 的 J2 要求：「现役页面 computed style 快照零差异」作为
「令牌纯加法不破坏视觉」的**机器证明**。规格书预留名 `_w827_visual_regression_probe.py`
（撰写时预判的落地批号），实际落地批为 W851，按实际批号命名（预留号从未占用，
W827 是另一批·P0-01 阅读入口打通）。

本探针不止服务 W851：设计迁移 B1-B11 每一批都声称「只迁该迁的」，前后各采一次
快照、diff 为零即证明、非零即定位到元素与属性——它是整个迁移计划的验收仪器。

## 口径（与 W826 §7 J2 对齐）

- **采样面**：21 页 = 首页 1 + 根页 4 + data 8 + reader 4 + en 4（J2 要求 ≥20）；
- **双主题**：浅色 + 暗色各采一遍（theme-init 跟随 prefers-color-scheme·
  context 级 `color_scheme` 强制·fresh context 无 localStorage 污染）；
- **元素口径**：全部可见元素（display 非 none · visibility 非 hidden · 盒非零），
  记 `[tag, class]` + 计算后的 color / background-color / font-size / font-family /
  line-height / padding 四向 / margin 四向 / border 四向（宽/样式/色）/ border-radius；
- **动画中间态**：context `reduced_motion=reduce` + networkidle 后 **固定地板等待
  （默认 15s）+ DOM 静默收敛**（MutationObserver：连续静默窗无 mutation 才采·总帽
  15s）。W851 实证坑——① 首版把 settle 等在了采集**之后**（`wait_for_timeout` 跟在
  evaluate 后面），被采页面从未获得 settle；② `site/static/js/chart-audit.js` 六族
  标签修复按 setTimeout 波次执行（最远 14s·axisfix/axesvar/avoidall/numfix/netlabels/
  content·见该文件 FAMILIES 表·波间空隙最大 3000ms）——任何静默窗都会在波间空隙
  提前到期，同态两采出现元素数 124↔125、font-size 9px↔10px 跳变，故加 15s 地板；
  ③ diff 侧同批修：元素数不齐时不再短路，公共前缀仍逐属性对拍（计数差异曾把
  属性比拍整个掩盖）。
- **SVG 子元素同口径**（图表数据色在计算样式里·改令牌必然现形）；
- **零依赖**：stdlib + playwright；playwright 缺失 = 明确报错退出 1，**不静默跳过**
  （与 obs_sample 拒收启发式估算同族纪律——没有证据不许说「通过」）。

## 用法

    py -3 scripts/_w851_visual_regression_probe.py capture --out before.json
    py -3 scripts/_w851_visual_regression_probe.py capture --out after.json --theme dark
    py -3 scripts/_w851_visual_regression_probe.py diff before.json after.json
    py -3 scripts/_w851_visual_regression_probe.py --self-test

退出码：capture 0（异常 1）· diff 0=零差异 / 1=有差异或对拍面不齐 · self-test 全过 0。
"""

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

SCHEMA = 3

# J2 采样面（21 页·缺一即 FAIL——采样面萎缩等于证明面萎缩）
PROBE_PAGES = (
    # 首页 1
    "index.html",
    # 根页 4
    "guide.html", "dashboard.html", "curated.html", "404.html",
    # data 8（含两张重 DOM 图表页·SVG 子元素在口径内）
    "data/character-relationship-3d.html", "data/relationships.html",
    "data/timeline.html", "data/text-search.html", "data/chapter-stats.html",
    "data/tag-cloud.html", "data/cross-time-danmaku.html", "data/hardship-heatmap.html",
    # reader 4（跨卷 spread）
    "reader/ch001.html", "reader/ch030.html", "reader/ch060.html", "reader/ch081.html",
    # en 4（与中文页同构·双主题在英文面同样证明）
    "en/relationships.html", "en/timeline.html", "en/text-search.html",
    "en/character-relationship-3d.html",
)

# 计算样式采集属性（固定序·diff 按索引对拍）
PROPS = (
    "color", "background-color", "font-size", "font-family", "line-height",
    "padding-top", "padding-right", "padding-bottom", "padding-left",
    "margin-top", "margin-right", "margin-bottom", "margin-left",
    "border-top-width", "border-top-style", "border-top-color",
    "border-right-width", "border-right-style", "border-right-color",
    "border-bottom-width", "border-bottom-style", "border-bottom-color",
    "border-left-width", "border-left-style", "border-left-color",
    "border-top-left-radius", "border-top-right-radius",
    "border-bottom-left-radius", "border-bottom-right-radius",
)

_CAPTURE_JS = """
() => {
  const props = %s;
  const out = [];
  const els = document.querySelectorAll('*');
  for (const el of els) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const rec = [el.tagName.toLowerCase(), el.getAttribute('class') || ''];
    for (const p of props) rec.push(cs.getPropertyValue(p));
    out.push(rec);
  }
  return out;
}
""" % json.dumps(list(PROPS))


# DOM 静默收敛：networkidle 后等到连续 quiet_ms 无 DOM mutation 才 resolve；
# 总帽 QUIESCE_CAP_MS 防永动页（持续注入类）把采集挂死。
_QUIESCE_CAP_MS = 15000

_QUIESCE_JS = """
(quietMs) => new Promise((resolve) => {
  const finish = () => { obs.disconnect(); resolve(); };
  let timer = setTimeout(finish, quietMs);
  const obs = new MutationObserver(() => {
    clearTimeout(timer);
    timer = setTimeout(finish, quietMs);
  });
  obs.observe(document.documentElement,
              {subtree: true, childList: true, attributes: true, characterData: true});
  setTimeout(finish, %d);  // 总帽：永动页不至于把采集挂死
})
""" % _QUIESCE_CAP_MS


def _file_url(path):
    return "file:///" + os.path.abspath(path).replace("\\", "/")


def _capture_one(page, path, floor_ms=0, quiet_ms=400):
    """单页单主题采集：网络空闲 → 地板等待 → DOM 静默收敛 → 采集。

    floor_ms 覆盖 chart-audit.js 六族修复的 setTimeout 波次（最远 14s·默认 15s）；
    W851 实证：无地板等待时静默窗在波间空隙提前到期，同态两采出现 124↔125 元素
    跳变。自测页面无晚期波，floor 传 0 保持快速。
    """
    page.goto(_file_url(path), wait_until="networkidle", timeout=30000)
    if floor_ms > 0:
        page.wait_for_timeout(floor_ms)
    page.evaluate(_QUIESCE_JS, quiet_ms)
    return page.evaluate(_CAPTURE_JS)


def capture(paths, themes=("light", "dark"), floor_ms=15000, quiet_ms=400):
    """采集快照。paths: [(rel, abspath)]。返回快照 dict。

    缺页/浏览器不可用即抛（调用方转 SystemExit）——宁缺勿假。
    """
    try:
        from playwright.sync_api import sync_playwright  # noqa: WPS433
    except ImportError as e:
        raise SystemExit(
            "playwright 不可用（%s）——J2 探针拒绝在无浏览器环境下出具「通过」结论" % e
        ) from None
    snap = {
        "schema": SCHEMA,
        "captured_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "props": list(PROPS),
        "themes": list(themes),
        "pages": {},
        "meta": {"page_count": len(paths), "floor_ms": floor_ms,
                 "quiet_ms": quiet_ms, "quiesce_cap_ms": _QUIESCE_CAP_MS},
    }
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        try:
            for theme in themes:
                scheme = "dark" if theme == "dark" else "light"
                ctx = browser.new_context(reduced_motion="reduce", color_scheme=scheme)
                page = ctx.new_page()
                for rel, abspath in paths:
                    els = _capture_one(page, abspath, floor_ms=floor_ms,
                                       quiet_ms=quiet_ms)
                    snap["pages"].setdefault(rel, {})[theme] = els
                ctx.close()
        finally:
            browser.close()
    return snap


def _resolve_pages(rel_list):
    """rel → (rel, abspath)；缺页即 SystemExit（采样面不齐 = 证明面不齐）。"""
    out = []
    missing = []
    for rel in rel_list:
        p = os.path.join(SITE, rel.replace("/", os.sep))
        if os.path.isfile(p):
            out.append((rel, p))
        else:
            missing.append(rel)
    if missing:
        raise SystemExit("J2 采样面缺页（补页再采·不许缩面）：%s" % "、".join(missing))
    return out


def _diff_snapshots(before, after, max_report=20):
    """对拍两个快照。返回 (diffs, notes)。diffs 非空即 J2 不过。"""
    diffs = []
    notes = []
    bp, ap = before.get("pages", {}), after.get("pages", {})
    if set(bp) != set(ap):
        only_b = sorted(set(bp) - set(ap))
        only_a = sorted(set(ap) - set(bp))
        notes.append("采样面不齐：仅 before 有 %s·仅 after 有 %s" % (only_b, only_a))
    for rel in sorted(set(bp) & set(ap)):
        for theme in sorted(set(bp[rel]) & set(ap[rel])):
            eb, ea = bp[rel][theme], ap[rel][theme]
            if len(eb) != len(ea):
                diffs.append({"page": rel, "theme": theme, "kind": "元素数",
                              "before": len(eb), "after": len(ea)})
                # 不短路：计数差异曾把属性对拍整个掩盖（W851 实证）——
                # 公共前缀仍按索引逐属性比，多退少补都显形
            for i, (rb, ra) in enumerate(zip(eb, ea, strict=False)):
                if rb == ra:
                    continue
                if rb[:2] != ra[:2]:
                    diffs.append({"page": rel, "theme": theme, "index": i,
                                  "kind": "元素身份", "before": rb[:2], "after": ra[:2]})
                else:
                    for pi in range(2, len(PROPS) + 2):
                        if rb[pi] != ra[pi]:
                            diffs.append({"page": rel, "theme": theme, "index": i,
                                          "kind": "属性",
                                          "element": rb[:2], "prop": PROPS[pi - 2],
                                          "before": rb[pi], "after": ra[pi]})
                if len(diffs) >= max_report:
                    notes.append("差异已达 %d 条上限·截断（修完再复跑）" % max_report)
                    return diffs, notes
    return diffs, notes


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# T4 用：600ms 后追加一个可见元素（模拟晚期 DOM fixer）
_LATE_MUTATION_SCRIPT = (
    "<script>setTimeout(function(){var d=document.createElement('div');"
    "d.className='late';d.style.cssText='width:10px;height:10px';"
    "document.body.appendChild(d);},600);</script>")


def _self_test():
    """4 例：① 零变化再采 → 零差异（正样本·防「永远报差异」的假红）；
    ② 注入 var() 重定义 → 差异定位到属性（负样本·防「永远报零差异」的假绿）；
    ③ 采样面缺页 → 拒采（口径塌陷 fail-closed）；
    ④ 晚期 mutation（600ms 追加可见元素）两采一致且落入采样——锁「静默
    收敛等在采集之前」（W851 实证坑：首版等在了采集之后·从未作用于被采页）。"""
    cases = []
    tmp = tempfile.mkdtemp(prefix="w851probe_")
    base = os.path.join(tmp, "probe_page.html")

    def write_html(token_value, late_script=""):
        with open(base, "w", encoding="utf-8") as f:
            f.write(
                "<!DOCTYPE html><html><head><meta charset='utf-8'><style>"
                ":root{--probe-token:%s;}"
                ".box{color:var(--probe-token);background-color:#ffffff;padding:8px;}"
                "</style></head><body><div class='box'>探针</div>%s</body></html>"
                % (token_value, late_script))

    try:
        from playwright.sync_api import sync_playwright  # noqa: WPS433
    except ImportError:
        print("FAIL T0 playwright 不可用——自测拒绝出具任何结论")
        return 1

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(reduced_motion="reduce", color_scheme="light")
        page = ctx.new_page()

        def cap():
            return _capture_one(page, base)

        write_html("#112233")
        s1 = cap()
        s2 = cap()
        cases.append(("T1 零变化再采 → 零差异（防假红）", s1 == s2 and len(s1) >= 2))

        write_html("#445566")
        s3 = cap()
        d, _n = _diff_snapshots(
            {"pages": {"p": {"light": s1}}}, {"pages": {"p": {"light": s3}}})
        hit = any(x.get("prop") == "color" and x.get("before") == "rgb(17, 34, 51)"
                  and x.get("after") == "rgb(68, 85, 102)" for x in d)
        cases.append(("T2 注入令牌重定义 → 定位到 color 差异（防假绿）", hit))

        # T4：晚期 mutation（600ms 后追加可见元素）——静默收敛必须等在采集之前
        write_html("#112233", _LATE_MUTATION_SCRIPT)
        s4a, s4b = cap(), cap()
        has_late = any(r[0] == "div" and "late" in r[1] for r in s4a)
        cases.append(("T4 晚期 mutation 两采一致且落入采样（收敛前置）",
                      s4a == s4b and has_late and len(s4a) == len(s1) + 1))

        ctx.close()
        browser.close()

    # T3：采样面缺页即拒（纯逻辑·不触浏览器）
    missing_rel = "data/__no_such_page__.html"
    try:
        _resolve_pages([missing_rel])
        cases.append(("T3 采样面缺页 → 拒采", False))
    except SystemExit:
        cases.append(("T3 采样面缺页 → 拒采", True))

    ok = sum(1 for _, p in cases if p)
    for name, passed in cases:
        print("%s %s" % ("PASS" if passed else "FAIL", name))
    print("---- J2 视觉回归探针自测：%d/%d ----" % (ok, len(cases)))
    return 0 if ok == len(cases) else 1


def main(argv):
    args = argv[1:]
    if "--self-test" in args:
        return _self_test()
    ap = argparse.ArgumentParser(description="J2 视觉回归探针（W851）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("capture", help="采集快照")
    c.add_argument("--out", required=True)
    c.add_argument("--theme", default="both", choices=["light", "dark", "both"])
    c.add_argument("--pages", default="", help="逗号分隔子集（默认 J2 全量 21 页）")
    c.add_argument("--wait", type=int, default=400,
                   help="DOM 静默窗 ms（默认 400·总帽 15s）")
    c.add_argument("--floor", type=int, default=15000,
                   help="采集前固定地板等待 ms（覆盖 chart-audit 修复波·最远 14s·默认 15000）")

    d = sub.add_parser("diff", help="对拍前后快照")
    d.add_argument("before")
    d.add_argument("after")

    ns = ap.parse_args(args)
    if ns.cmd == "capture":
        rels = [r.strip() for r in ns.pages.split(",") if r.strip()] or list(PROBE_PAGES)
        themes = ("light", "dark") if ns.theme == "both" else (ns.theme,)
        snap = capture(_resolve_pages(rels), themes=themes, floor_ms=ns.floor,
                       quiet_ms=ns.wait)
        os.makedirs(os.path.dirname(os.path.abspath(ns.out)), exist_ok=True)
        with open(ns.out, "w", encoding="utf-8", newline="\n") as f:
            json.dump(snap, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
        n = sum(len(v[t]) for v in snap["pages"].values() for t in v)
        print("已采集 %d 页 × %d 主题 · %d 元素 → %s"
              % (len(snap["pages"]), len(themes), n, ns.out))
        return 0

    # diff
    before, after = _load(ns.before), _load(ns.after)
    diffs, notes = _diff_snapshots(before, after)
    for nt in notes:
        print("NOTE %s" % nt)
    if diffs:
        print("---- J2 视觉回归：%d 处差异（前 %d 条）----" % (len(diffs), len(diffs)))
        for x in diffs:
            print("  %s" % json.dumps(x, ensure_ascii=False))
        print("J2 FAIL：现役页面计算样式非零差异——「视觉零变化」不成立")
        return 1
    total = sum(len(v[t]) for v in before.get("pages", {}).values() for t in v)
    print("---- J2 视觉回归：零差异（%d 页 × %s 主题 · %d 元素逐属性对拍）----"
          % (len(before.get("pages", {})), "+".join(before.get("themes", [])), total))
    print("J2 PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
