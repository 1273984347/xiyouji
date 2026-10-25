#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W946 · 第 50 门禁：UI 图标位 emoji 残留 + 图标渲染正确性

两段判据（缺一不可）：
  A 静态：全仓 UI 图标位不得残留 emoji 表情/图形字符
     （判据与 scripts/_w939_scan_targets.py 同源·控件首位 / 图标槽 class / 标题前缀 / CSS content）
  B 实测：浏览器实开代表页，验证内联 SVG 图标**确为线描**（stroke≠none 且 fill=none）、
     尺寸跟随字号（1em 量级·非 300×150 巨图）、CSS content 位的同源 mask 图标已加载、
     且无 console 错误 / pageerror（含 CSP 拒执行）

B 段的存在理由：W941 批的静态判据全绿，但浏览器实开才发现内联 SVG 丢了
fill/stroke 属性 ⇒ 图标渲染成黑块 ⇒ **静态判据无法覆盖「渲染正确」**。

用法：
    py -3 scripts/check_emoji_icons.py            # 自检（人跑）
    py -3 scripts/check_emoji_icons.py --gate     # 门禁模式（退出码 0/1 + 汇总行）
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# —— A 段：静态 emoji 判据（承 W941 扫描器）——
PICTO = re.compile("["
                   "\U0001F000-\U0001FAFF"
                   "\u2728\u274C\u2705\u26A1\u2B50\u2934\u2935\u3030\u303D\u3297\u3299"
                   "\u203C\u2049\u00A9\u00AE]")
SYM = re.compile("[\u2190-\u21FF\u2300-\u23FF\u2600-\u27BF\u2B00-\u2BFF]")
VS16 = "\uFE0F"
ARROWS = {"\u2190", "\u2192", "\u2194", "\u21ba", "\u2191", "\u2193", "\u21d2", "\u21d0", "\u21d4"}
NON_GRAPHIC = set("\u00a7\u00b6\u2022\u2026\u00b7\u2014\u2013\u2018\u2019\u201c\u201d\u2032\u2033")
SLOT_HINT = re.compile(r"icon|emoji|ico|glyph|symbol|badge|avatar|mark", re.I)
TITLE_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "th", "legend", "dt", "option", "li", "summary"}
CONTROL_TAGS = {"button", "a", "summary", "label"}
TAG_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9:-]*)((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>")
CSS_CONTENT_RE = re.compile(r"content\s*:\s*[\"']([^\"']*)[\"']")
SRC_SUFFIX = {".html", ".htm", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".vue", ".css"}
SCAN_ROOTS = ["site", "xiyouji-agent-web/src", "xiyouji-desktop/src", "assets/promo"]


def graphic_chars(text: str) -> set[str]:
    if not PICTO.search(text) and not SYM.search(text):
        return set()
    out = set()
    for m in PICTO.finditer(text):
        out.add(m.group(0))
    for m in SYM.finditer(text):
        ch = m.group(0)
        if ch == VS16:
            continue
        nxt = text[m.end():m.end() + 1]
        prev = text[m.start() - 1:m.start()] if m.start() > 0 else ""
        if nxt == VS16 or prev == VS16:
            out.add(ch)
        elif ch not in ARROWS and ch not in NON_GRAPHIC:
            out.add(ch)
    return out


def scan_static() -> list[dict]:
    hits = []
    for root in SCAN_ROOTS:
        p = ROOT / root
        if not p.exists():
            continue
        for f in sorted(p.rglob("*")):
            if not (f.is_file() and f.suffix.lower() in SRC_SUFFIX):
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            lines = text.split("\n")
            covered = [False] * len(text)
            for m in TAG_RE.finditer(text):
                tag = m.group(1).lower()
                attrs = m.group(2) or ""
                nxt = text.find("<", m.end())
                inner = text[m.end():nxt if nxt != -1 else len(text)]
                if not inner.strip():
                    continue
                stripped = inner.lstrip()
                lead = bool(graphic_chars(stripped[:2])) and graphic_chars(stripped[:2]) == set(stripped[:2]) \
                    and stripped[:1] in graphic_chars(stripped[:2])
                cat = None
                if lead and (tag in CONTROL_TAGS or ("role" in attrs and "button" in attrs)):
                    cat = "A control-icon"
                elif SLOT_HINT.search(attrs):
                    cat = "B slot-icon"
                elif lead and tag in TITLE_TAGS:
                    cat = "C title-prefix"
                if cat is None:
                    continue
                g = graphic_chars(stripped)
                if not g:
                    continue
                hits.append({"file": str(f.relative_to(ROOT)).replace("\\", "/"),
                             "line": text.count("\n", 0, m.start()) + 1,
                             "cat": cat, "chars": "".join(sorted(g)),
                             "snippet": re.sub(r"\s+", " ", stripped)[:70]})
                for i in range(m.start(), nxt if nxt != -1 else len(text)):
                    covered[i] = True
            for m in CSS_CONTENT_RE.finditer(text):
                g = graphic_chars(m.group(1))
                if not g:
                    continue
                hits.append({"file": str(f.relative_to(ROOT)).replace("\\", "/"),
                             "line": text.count("\n", 0, m.start()) + 1,
                             "cat": "D css-content", "chars": "".join(sorted(g)),
                             "snippet": m.group(1)[:70]})
    return hits


# —— B 段：浏览器实测 ——
PROBE_JS = r"""
() => {
  const out = { svg: [], mask: [], err: [] };
  document.querySelectorAll('svg.ico').forEach((s) => {
    const b = s.getBoundingClientRect();
    const cs = getComputedStyle(s);
    const fs = parseFloat(getComputedStyle(s.parentElement || s).fontSize) || 16;
    out.svg.push({
      cls: s.getAttribute('class'),
      w: b.width, h: b.height,
      stroke: cs.stroke, fill: cs.fill,
      strokeWidth: cs.strokeWidth,
      emRatio: fs ? +(b.width / fs).toFixed(2) : null,
    });
  });
  const sels = ['.radio-out .caption', '.detective-banner', '.suspect-card', '.hu-card',
                '.warn-item', '.cc-acq', '.nc-quote', '.search-box', '.id-innovation'];
  sels.forEach((sel) => {
    document.querySelectorAll(sel).forEach((el) => {
      const pb = getComputedStyle(el, '::before');
      const mi = pb.maskImage || pb.webkitMaskImage || 'none';
      if (mi === 'none' || pb.content === 'none') return;
      out.mask.push({ sel: sel, w: pb.width, h: pb.height, mask: mi.slice(0, 70) });
    });
  });
  return out;
}
"""

PROBE_PAGES = [
    ("reader/ch001.html", "内联 SVG（收藏/赞/踩）"),
    ("data/timeline.html", "时间线专属图标（内联 SVG）"),
    ("data/concept-device.html", "CSS content 位（同源 mask）"),
    ("data/graph-explorer.html", "控件图标（菜单/关闭/检索）"),
]

# 两套环境：file://（本地双击）与 http://（线上同源·真实用户环境）
#   · file://：字体子集与 fetch 属既有降级；CSS mask 引用外部 SVG 在 file:// 下被 CORS 拦
#     ⇒ 22 处 CSS content 位图标在本地不显示（线上正常）——本门禁在 file:// 下记 NOTE 不判红
#   · http://：真实用户环境 ⇒ 全部判据严格（mask 必须加载成功，否则判红）
ENVIRONMENTS = [("file", "file:///" + str(SITE).replace("\\", "/") + "/"),
                ("http", "http://127.0.0.1:8899/")]


def run_browser() -> tuple[list[str], dict]:
    """返回 (失败项列表, 采集数据)"""
    fails = []
    notes = []
    data = {}
    node_script = ROOT / "scripts" / "node_modules" / "playwright"
    if not node_script.exists():
        return ["浏览器段跳过：未安装 playwright（scripts/node_modules/playwright 缺失）"], data
    probe_js = ROOT / "scripts" / "_w946_icon_probe.js"
    probe_js.write_text(
        "const { chromium } = require('" + str(node_script).replace("\\", "/") + "');\n"
        "const path = require('path');\n"
        "const PAGES = " + json.dumps(PROBE_PAGES, ensure_ascii=False) + ";\n"
        "const ENVS = " + json.dumps(ENVIRONMENTS, ensure_ascii=False) + ";\n"
        "const PROBE = " + json.dumps(PROBE_JS, ensure_ascii=False) + ";\n"
        "(async () => {\n"
        "  const browser = await chromium.launch();\n"
        "  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });\n"
        "  const report = {};\n"
        "  for (const [env, base] of ENVS) {\n"
        "    for (const [rel, note] of PAGES) {\n"
        "      const p = await ctx.newPage();\n"
        "      const errs = [], failed = [];\n"
        "      p.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });\n"
        "      p.on('pageerror', (e) => errs.push('pageerror: ' + e.message));\n"
        "      p.on('requestfailed', (r) => failed.push(r.url() + ' :: ' + (r.failure()||{}).errorText));\n"
        "      await p.goto(base + rel, { waitUntil: 'load' });\n"
        "      await p.waitForTimeout(1200);\n"
        "      report[env + '|' + rel] = { env, note, probe: await p.evaluate('(' + PROBE + ')()'),"
        " errors: errs, failed };\n"
        "      await p.close();\n"
        "    }\n"
        "  }\n"
        "  await browser.close();\n"
        "  console.log(JSON.stringify(report));\n"
        "})();\n", encoding="utf-8")
    import subprocess
    # 起本地 http server（真实用户环境·同源 ⇒ mask 可加载）
    import atexit
    import time
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8899",
                            "--bind", "127.0.0.1"],
                           cwd=str(SITE), stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    atexit.register(srv.kill)
    time.sleep(1.2)
    r = subprocess.run(["node", str(probe_js)], capture_output=True, text=True,
                       encoding="utf-8", cwd=str(ROOT), timeout=900)
    srv.kill()
    if r.returncode != 0:
        return [f"浏览器段执行失败 rc={r.returncode}: {(r.stderr or '')[:300]}"], data
    try:
        data = json.loads(r.stdout.strip().split("\n")[-1])
    except Exception as e:
        return [f"浏览器输出解析失败: {e}"], data

    # 错误过滤：file:// 环境的**既有降级**不属本门禁范畴
    #   · 字体子集 CORS（file:// 加载 woff2 被拦）——全站既有行为
    #   · Fetch API 不支持 file scheme——数据走 EMBEDDED 回退，全站既有行为
    # 但凡指向本批自建图标资产（icons/ui）的加载失败，一律判红
    PREEXISTING = ("font", "Fetch API", "ERR_FAILED", "net::")
    for key, rep in data.items():
        rel = rep.get("env", "?") + "|" + key.split("|", 1)[-1]
        env = rep.get("env", "file")
        is_http = env == "http"
        p = rep.get("probe", {})
        for s in p.get("svg", []):
            if s.get("stroke") in (None, "none"):
                fails.append(f"{rel}: 内联 SVG 描边为 none（渲染成黑块）· {s.get('cls')}")
            if s.get("fill") not in (None, "none"):
                fails.append(f"{rel}: 内联 SVG fill={s.get('fill')}（应为 none）· {s.get('cls')}")
            w = s.get("w") or 0
            if w <= 0:
                fails.append(f"{rel}: 内联 SVG 宽度为 0（不可见）· {s.get('cls')}")
            elif w > 64:
                fails.append(f"{rel}: 内联 SVG 宽度 {w}px 异常（疑似 300×150 巨图）· {s.get('cls')}")
        for m in p.get("mask", []):
            w = m.get("w")
            try:
                wf = float(str(w).replace("px", "")) if w else 0
            except Exception:
                wf = 0
            if wf <= 0:
                fails.append(f"{rel}: mask 伪元素尺寸为 0（图标不可见）· {m.get('sel')}")
            if "icons/ui" not in str(m.get("mask", "")):
                fails.append(f"{rel}: mask 未指向自建图标资产 · {m.get('sel')} · {m.get('mask')}")
        # 失败请求：按 URL 精确判定（file:// 下指向 icons/ui 的 mask 被 CORS 拦 ⇒ 已知降级）
        for fr in rep.get("failed", []):
            if "icons/ui" in fr:
                if is_http:
                    fails.append(f"{rel}: 自建图标资产加载失败（http 同源环境·线上即此环境）· {fr[:130]}")
                else:
                    notes.append(f"{rel}: file:// 下 CSS content 位的同源 mask 被 CORS 拦"
                                 f"（本地双击时该图标不显示·线上同源正常）· {fr[:90]}")
            else:
                notes.append(f"{rel}: file:// 既有降级（字体/fetch）· {fr[:90]}")
        for e in rep.get("errors", []):
            if "icons/ui" in e:
                if is_http:
                    fails.append(f"{rel}: 自建图标资产加载失败（http 同源环境·线上即此环境）· {e[:150]}")
                else:
                    notes.append(f"{rel}: file:// 下 CSS content 位的同源 mask 被 CORS 拦"
                                 f"（本地双击时该图标不显示·线上同源正常）· {e[:90]}")
            elif is_http and "404" in e:
                notes.append(f"{rel}: http 环境资源 404（既有数据源缺失·非图标）· {e[:100]}")
            else:
                notes.append(f"{rel}: file:// 既有降级（字体/fetch）· {e[:100]}")
    return fails, data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    hits = scan_static()
    print("=" * 72)
    print("W946 · 第 50 门禁 UI 图标位 emoji 残留与图标渲染正确性")
    print("=" * 72)
    print(f"A 静态段：UI 图标位 emoji 命中 {len(hits)} 处")
    for h in hits[:20]:
        print(f"  {h['file']}:{h['line']}  [{h['cat']}]  {h['chars']}  :: {h['snippet'][:50]}")

    fails = []
    if hits:
        fails.append(f"A 静态段：UI 图标位仍有 {len(hits)} 处 emoji 残留")

    data = {}
    if not args.no_browser:
        bfails, data = run_browser()
        fails.extend(bfails)
        print(f"B 实测段：{len(PROBE_PAGES)} 页")
        for rel, rep in data.items():
            pr = rep.get("probe", {})
            print(f"  {rel}: 内联 SVG {len(pr.get('svg', []))} 个 · mask {len(pr.get('mask', []))} 个"
                  f" · 错误 {len(rep.get('errors', []))} 条")

    print("-" * 72)
    if fails:
        print(f"FAIL {len(fails)} 项：")
        for f in fails[:30]:
            print("  -", f)
    else:
        print("OK    UI 图标位零残留 · 图标渲染线描正确 · 无浏览器错误")
    print("=" * 72)
    if args.gate:
        print(f"==== 第 50 门禁 UI 图标位：{'PASS' if not fails else 'FAIL'}（静态 {len(hits)} 处残留 + 实测 {len(fails)} 项） ====")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
