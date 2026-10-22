#!/usr/bin/env python3
"""_w876_value_check.py — W876 值切换与 C 渠换色的计算样式锚点校验（一次性件·W876 重建版）。

**重建原因**：原版三个锚点里两个选择器错位（philosophy h2 采到 ink-1 墨色标题·
暗色锚点采到 ink-1 元素）——探针假设「首个匹配元素就是目标」不成立。本版改
**搜索式断言**：不猜选择器，直接在页面里找「持期望计算色的元素」，找到即过；
同时补 dukou-engine 令牌锚点（根级 INLINED 页·inline_css 跳过·手工靶向修复的验证）。

四组锚点（全部读计算样式·不靠目测）：
1. C 渠换色（浅色）：aesthetics / chapter-structure-graph / workplace 三页各找
   ≥1 个 color = rgb(199,70,58)（--accent-text #C7463A）的文本元素；
2. --chart-3：heaven-power-network 的 .role-card.r-judge border-top-color
   = rgb(179,143,88)（#B38F58·3.01:1）+ dukou-engine 的 --chart-3 自定义属性值；
3. 暗色 --accent：index.html 暗色下找 ≥1 个 color = rgb(228,98,80)（#E46250）的元素；
4. 反向证据（残余如实记账）：monster-sociology（复评清单页）仍存在
   color = rgb(200,70,58)（--accent 未换）的文本元素——253 处残余的在役证明。

退出码：0 = 全部锚点通过 · 1 = 有锚点失败。
"""

import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

ACCENT_TEXT = "rgb(199, 70, 58)"   # --accent-text 浅
ACCENT_OLD = "rgb(200, 70, 58)"    # --accent 浅（换色后 C 渠目标元素不应再是它）
CHART3_NEW = "rgb(179, 143, 88)"   # --chart-3 新值
ACCENT_DARK_NEW = "rgb(228, 98, 80)"  # 暗色 --accent 新值


def probe(page, rel, js, scheme="light", arg=None):
    page.emulate_media(color_scheme=scheme)
    page.goto("file:///" + os.path.join(SITE, rel).replace("\\", "/"),
              wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(1500)
    return page.evaluate(js, arg) if arg is not None else page.evaluate(js)


# 找持指定颜色的文本元素（返回前 3 个的 tag.class 描述·找不到返回空数组）
_FIND_JS = """
(color) => {
  const out = [];
  for (const el of document.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    let hasText = false;
    for (const n of el.childNodes) {
      if (n.nodeType === 3 && n.textContent.trim()) { hasText = true; break; }
    }
    if (hasText && cs.color === color) {
      out.push(el.tagName.toLowerCase() + '.' + (el.getAttribute('class') || '(无类)'));
      if (out.length >= 3) break;
    }
  }
  return out;
}
"""


def main():
    fails = 0
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        ctx = b.new_context(reduced_motion="reduce")
        page = ctx.new_page()

        # 1) C 渠换色锚点（三页·换色规则命中页·均为默认态可见文本：
        #    chapter-structure-graph 的两条规则是 :hover 态·默认态无 accent-text 文本·不作锚点）
        for rel in ("data/aesthetics.html", "data/business-model.html",
                    "data/workplace.html"):
            hits = probe(page, rel, _FIND_JS, arg=ACCENT_TEXT)
            print("C 渠 %-38s --accent-text 文本元素: %s" % (rel, hits or "（无）"))
            if not hits:
                print("  ✗ 未找到 color=%s 的文本元素" % ACCENT_TEXT)
                fails += 1

        # 2) chart-3 锚点（非 SVG 消费点 + 根级 INLINED 页令牌）
        c3 = probe(page, "data/heaven-power-network.html",
                   "() => { const e = document.querySelector('.role-card.r-judge');"
                   " return e ? getComputedStyle(e).borderTopColor : 'none'; }")
        print("r-judge border-top (light):", c3)
        if c3 != CHART3_NEW:
            print("  ✗ 期望 %s" % CHART3_NEW)
            fails += 1
        c3b = probe(page, "dukou-engine.html",
                    "() => getComputedStyle(document.documentElement)"
                    ".getPropertyValue('--chart-3').trim();")
        print("dukou-engine --chart-3 令牌值:", c3b)
        if c3b != "#B38F58":
            print("  ✗ 期望 #B38F58（根级页手工靶向修复验证）")
            fails += 1

        # 3) 暗色 --accent 锚点（搜索式）
        dark = probe(page, "index.html", _FIND_JS, scheme="dark",
                     arg=ACCENT_DARK_NEW)
        print("index 暗色 --accent 新值元素:", dark or "（无）")
        if not dark:
            print("  ✗ 暗色未找到 color=%s 的元素" % ACCENT_DARK_NEW)
            fails += 1

        # 4) 反向证据：复评清单页仍有未换元素（253 处残余的在役证明）
        resid = probe(page, "data/monster-sociology.html", _FIND_JS,
                      arg=ACCENT_OLD)
        print("monster-sociology 残余 --accent 元素:", resid or "（无）")
        if not resid:
            print("  ✗ 复评清单页应仍有未换元素（反向证据缺失·疑换色过度）")
            fails += 1

        b.close()
    print("FAIL · 锚点失败 %d" % fails if fails else "PASS · 锚点全部通过")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
