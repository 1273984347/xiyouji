#!/usr/bin/env python3
"""mobile_viewport_probe.py — 移动视口渲染探针（W1165 · V4 375px 回归）。

只诊断不判红：逐页在窄视口下量四类真实渲染事实，产出 JSON 报告供修复与门禁化取数。

四类判据（每页）：
  A 水平溢出   documentElement.scrollWidth - innerWidth（> 1 ⇒ 内容横向溢出，可横向拖动）
  B 越界元凶   rect.right > innerWidth 的**最外层**元素（父元素不越界者）——定位到具体节点
  C 触摸目标   可见可交互元素尺寸 < 44 与 < 24（WCAG 2.5.8 AA 线 = 24；44 为 HIG 建议）
  D 正文字号   可见文本节点最小 font-size（< 12 ⇒ 可读性风险）

设计取舍：
  - 一律走 file:// 加载（项目铁律「file:// 双击可开」即本仓交付形态，同时验证 EMBEDDED 回退路径）
  - 内联链接豁免触摸判据（正文流内 a 不受 44px 规则约束，WCAG 2.5.8 亦豁免行内文本）
  - SVG 内部节点不判越界（图表坐标系允许超框，容器裁剪另计）

用法：
  py -3 scripts/mobile_viewport_probe.py                      # 全量（site/*.html + site/data/*.html）
  py -3 scripts/mobile_viewport_probe.py --width 414
  py -3 scripts/mobile_viewport_probe.py --pages index.html data/dashboard.html
  py -3 scripts/mobile_viewport_probe.py --limit 5 --verbose
  py -3 scripts/mobile_viewport_probe.py --self-test
退出码：0 全过 / 1 有 FAIL / 2 基础设施异常
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join("scripts", "output", "mobile_viewport_report.json")

# 页内探针：返回四类事实。只用一次 evaluate，避免多次往返。
PROBE_JS = r"""
(cfg) => {
  const VW = window.innerWidth;
  const doc = document.documentElement;
  const vis = (el) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    if (cs.opacity !== '' && parseFloat(cs.opacity) === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 1 && r.height > 1;
  };
  const desc = (el) => ({
    tag: el.tagName.toLowerCase(),
    cls: (el.className || '').toString().trim().slice(0, 64),
    id: (el.id || '').slice(0, 40),
    txt: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 24),
    right: Math.round(el.getBoundingClientRect().right),
    w: Math.round(el.getBoundingClientRect().width)
  });

  // B 越界元凶：最外层（父不在越界集合内）
  const over = [];
  for (const el of document.querySelectorAll('body *')) {
    if (el.ownerSVGElement) continue;
    if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') continue;
    if (!vis(el)) continue;
    if (el.getBoundingClientRect().right <= VW + 1) continue;
    over.push(el);
  }
  const overSet = new Set(over);
  // 越界到底是「容器可横向滚动（正常）」还是「被 overflow:hidden 裁掉（内容不可达）」——
  // 前者是移动端表格/图表的既定形态，后者是真实缺陷。判据按最近可滚动祖先区分。
  const scrollAncestor = (el) => {
    let p = el.parentElement;
    while (p && p !== document.body && p !== document.documentElement) {
      const cs = getComputedStyle(p);
      if (/(auto|scroll)/.test(cs.overflowX)) return (p.className || p.tagName).toString().slice(0, 40);
      p = p.parentElement;
    }
    return null;
  };
  const offenders = [];
  const clipped = [];
  // 装饰性越界豁免：弹幕/飘落类动画元素按设计从视口外飞入，越界是动效本体而非内容不可达。
  // （实测来源：data/cross-time-danmaku.html 的 .danmaku-fly 397px 越界）
  const DECORATIVE = /danmaku-fly|falling-|petal|snowflake/i;
  for (const el of over) {
    if (el.parentElement && overSet.has(el.parentElement)) continue;
    if (DECORATIVE.test((el.className || '').toString())) continue;
    const sc = scrollAncestor(el);
    const item = Object.assign(desc(el), {scroll: sc});
    (sc ? offenders : clipped).push(item);
  }
  const offendersTop = offenders.slice(0, 8);
  const clippedTop = clipped.slice(0, 8);

  // C 触摸目标
  // 口径修正（W1165 实测）：① input[type=range] 的 rect 是**轨道**不是触摸区（实测 129x6），
  // 浏览器把命中区扩展到 thumb 周边 ⇒ 按 rect 判会系统性误报，剔除；② SVG 内部节点尺寸由数据
  // 与坐标系决定（D3 网络图/热力图），移动端替代方案是缩放与点选，不适用 44px 规则 ⇒ 单列 svgSmall
  // 只作信息项，不进分级。
  const tapSel = 'a[href], button, [role="button"], summary, input:not([type=hidden]), select, label[for]';
  const small44 = [];
  const small24 = [];
  const svgSmall = [];
  let tapTotal = 0;
  for (const el of document.querySelectorAll(tapSel)) {
    if (!vis(el)) continue;
    const cs = getComputedStyle(el);
    if (cs.pointerEvents === 'none') continue;
    if (el.tagName === 'INPUT' && (el.type === 'range' || el.type === 'checkbox' || el.type === 'radio')) continue;
    // 行内文本链接豁免（WCAG 2.5.8 例外条款）
    if (el.tagName === 'A' && /^inline/.test(cs.display)) continue;
    if (el.ownerSVGElement) {
      if (svgSmall.length < 12) {
        const rr = el.getBoundingClientRect();
        svgSmall.push(Object.assign(desc(el), {w: Math.round(rr.width), h: Math.round(rr.height)}));
      }
      continue;
    }
    tapTotal++;
    const r = el.getBoundingClientRect();
    const w = Math.round(r.width), h = Math.round(r.height);
    if (w < 44 || h < 44) {
      const item = Object.assign(desc(el), {w, h});
      if (small44.length < 10) small44.push(item);
      if (w < 24 || h < 24) { if (small24.length < 10) small24.push(item); }
    }
  }

  // D 字号：遍历可见文本元素取最小
  let minFont = 99;
  const fontSamples = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    const t = (n.textContent || '').trim();
    if (t.length < 4) continue;
    const p = n.parentElement;
    if (!p || !vis(p)) continue;
    if (p.tagName === 'SCRIPT' || p.tagName === 'STYLE') continue;
    const fs = parseFloat(getComputedStyle(p).fontSize);
    if (!isFinite(fs)) continue;
    if (fs < minFont) minFont = fs;
    if (fs < cfg.minFont && fontSamples.length < 8) {
      fontSamples.push({fs, txt: t.slice(0, 24), tag: p.tagName.toLowerCase(),
                        cls: (p.className || '').toString().trim().slice(0, 40)});
    }
  }

  return {
    vw: VW,
    scrollWidth: doc.scrollWidth,
    overflow: Math.max(0, doc.scrollWidth - VW),
    offenders: offendersTop,
    clipped: clippedTop,
    tapTotal: tapTotal,
    small44: small44,
    small24: small24,
    svgSmall: svgSmall,
    minFont: minFont === 99 ? null : minFont,
    fontSamples: fontSamples
  };
}
"""


def list_pages(site_root: str, only: list[str] | None, scope: str = "data", reader_sample: int = 0) -> list[str]:
    """返回相对 site/ 的页面路径列表。

    scope（W1173 扩面）：
      data    根页 + site/data（默认·W1165 起的覆盖面）
      en      根页 + site/en
      reader  根页 + site/reader（623 页·可用 reader_sample 抽样：每 N 页取一）
      all     根页 + data + en + reader

    W1173 起因：原实现只覆盖 data，而 en(138)/reader(623) 从未被移动端检查过——
    实测 reader 正文裸 <table> 在 375px 下就溢出 274px，却在 99 页的口径里「全部通过」。
    """
    if only:
        return only
    roots = sorted(os.path.basename(p) for p in glob.glob(os.path.join(site_root, "*.html")))
    pages = list(roots)
    want = {"data", "en", "reader"} if scope == "all" else ({scope} if scope in ("data", "en", "reader") else {"data"})
    for sub in ("data", "en", "reader"):
        if sub not in want:
            continue
        # 递归：reader 有 people/themes/essays/culture 四个子目录（623 页），只取直接子文件会漏掉八成
        items = sorted(
            os.path.relpath(p, site_root).replace("\\", "/")
            for p in glob.glob(os.path.join(site_root, sub, "**", "*.html"), recursive=True)
        )
        items = [x for x in items if not os.path.basename(x).startswith("_")]
        if sub == "reader" and reader_sample > 1:
            items = items[::reader_sample]
        pages += items
    return pages


def grade(rec: dict, min_font: float) -> tuple[str, list[str]]:
    """按四类判据给单页分级，返回 (等级, 理由列表)。"""
    reasons = []
    if rec["overflow"] > 1:
        reasons.append(f"水平溢出 {rec['overflow']}px")
    if rec["small24"]:
        reasons.append(f"触摸目标 <24px ×{len(rec['small24'])}")
    fatal = rec["overflow"] > 1

    warns = []
    # 越界分两类：落在可横向滚动容器内＝移动端表格/图表的既定形态（不计）；
    # 无可滚动祖先＝被 overflow:hidden 裁掉，内容用户不可达（计 WARN）。
    if rec.get("clipped") and not fatal:
        warns.append(f"内容被裁剪不可达 ×{len(rec['clipped'])}")
    if rec["small44"] and not rec["small24"]:
        warns.append(f"触摸目标 <44px ×{len(rec['small44'])}")
    if rec["minFont"] is not None and rec["minFont"] < min_font:
        warns.append(f"最小字号 {rec['minFont']}px")

    if fatal or rec["small24"]:
        return "FAIL", reasons
    if warns:
        return "WARN", warns
    return "OK", []


def run(pages: list[str], args) -> dict:
    from playwright.sync_api import sync_playwright

    site_root = args.site_root
    out = {"viewport": {"width": args.width, "height": args.height}, "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "pages": [], "summary": {}}
    t0 = time.time()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
        )
        for rel in pages:
            path = os.path.join(ROOT, site_root, rel.replace("/", os.sep))
            rec = {"page": rel}
            if not os.path.exists(path):
                rec["grade"] = "ERROR"
                rec["reasons"] = ["文件不存在"]
                out["pages"].append(rec)
                continue
            pg = ctx.new_page()
            try:
                pg.goto("file:///" + path.replace("\\", "/"), wait_until="load", timeout=25000)
                pg.wait_for_timeout(args.settle)
                facts = pg.evaluate(PROBE_JS, {"minFont": args.min_font})
                rec.update(facts)
                g, why = grade(facts, args.min_font)
                rec["grade"] = g
                rec["reasons"] = why
            except Exception as exc:  # noqa: BLE001 单页失败不中断全量普查
                rec["grade"] = "ERROR"
                rec["reasons"] = [f"{type(exc).__name__}: {str(exc)[:120]}"]
            finally:
                pg.close()
            out["pages"].append(rec)
            if args.verbose:
                mark = {"OK": ".", "WARN": "w", "FAIL": "F", "ERROR": "E"}[rec["grade"]]
                sys.stdout.write(mark)
                sys.stdout.flush()
        browser.close()

    agg = {"OK": 0, "WARN": 0, "FAIL": 0, "ERROR": 0}
    for rec in out["pages"]:
        agg[rec["grade"]] = agg.get(rec["grade"], 0) + 1
    out["summary"] = {
        "total": len(out["pages"]),
        "counts": agg,
        "overflowPages": sum(1 for r in out["pages"] if r.get("overflow", 0) > 1),
        "elapsedSec": round(time.time() - t0, 1),
    }
    return out


SELF_TEST_CASES = [
    # (facts, min_font, 期望等级)
    ({"overflow": 0, "offenders": [], "clipped": [], "small44": [], "small24": [], "minFont": 14}, 12, "OK"),
    ({"overflow": 24, "offenders": [], "clipped": [], "small44": [], "small24": [], "minFont": 14}, 12, "FAIL"),
    ({"overflow": 0, "offenders": [{"tag": "div"}], "clipped": [], "small44": [], "small24": [], "minFont": 14}, 12, "OK"),
    ({"overflow": 0, "offenders": [], "clipped": [{"tag": "div"}], "small44": [], "small24": [], "minFont": 14}, 12, "WARN"),
    ({"overflow": 0, "offenders": [], "clipped": [], "small44": [{"w": 30}], "small24": [], "minFont": 14}, 12, "WARN"),
    ({"overflow": 0, "offenders": [], "clipped": [], "small44": [{"w": 30}], "small24": [{"w": 18}], "minFont": 14}, 12, "FAIL"),
    ({"overflow": 0, "offenders": [], "clipped": [], "small44": [], "small24": [], "minFont": 11}, 12, "WARN"),
    ({"overflow": 0, "offenders": [], "clipped": [], "small44": [], "small24": [], "minFont": 12}, 12, "OK"),
    ({"overflow": 1, "offenders": [], "clipped": [], "small44": [], "small24": [], "minFont": 14}, 12, "OK"),
]


def self_test() -> int:
    bad = 0
    for i, (facts, mf, want) in enumerate(SELF_TEST_CASES, 1):
        got, why = grade(facts, mf)
        ok = got == want
        print(f"{'OK  ' if ok else 'FAIL'} 例{i}: 期望 {want} 实得 {got} · {why}")
        bad += 0 if ok else 1
    print(f"自测 {len(SELF_TEST_CASES) - bad}/{len(SELF_TEST_CASES)} 通过")
    return 0 if bad == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-root", default="site")
    ap.add_argument("--width", type=int, default=375)
    ap.add_argument("--height", type=int, default=667)
    ap.add_argument("--pages", nargs="*", default=None, help="只测指定页（相对 site/）")
    ap.add_argument("--scope", default="data", choices=["data", "en", "reader", "all"],
                    help="覆盖面（W1173 扩面）：data=根页+data / en / reader / all=三目录")
    ap.add_argument("--reader-sample", type=int, default=0, help="reader 抽样步长（0/1=全量）")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--settle", type=int, default=400, help="加载后等待 ms（动效/图表落位）")
    ap.add_argument("--min-font", type=float, default=12.0)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    pages = list_pages(args.site_root, args.pages, args.scope, args.reader_sample)
    if args.limit:
        pages = pages[: args.limit]
    print(f"探针视口 {args.width}x{args.height} · 页数 {len(pages)}")
    report = run(pages, args)
    out_path = os.path.join(ROOT, args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)

    c = report["summary"]["counts"]
    print(f"\n汇总：OK {c['OK']} · WARN {c['WARN']} · FAIL {c['FAIL']} · ERROR {c['ERROR']} "
          f"· 溢出页 {report['summary']['overflowPages']} · 耗时 {report['summary']['elapsedSec']}s")
    for rec in report["pages"]:
        if rec["grade"] in ("FAIL", "ERROR"):
            print(f"  [{rec['grade']}] {rec['page']}: {'; '.join(rec['reasons'])}")
    print(f"报告：{args.out}")
    return 1 if (c["FAIL"] or c["ERROR"]) else 0


if __name__ == "__main__":
    sys.exit(main())
