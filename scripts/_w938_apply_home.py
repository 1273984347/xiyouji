# -*- coding: utf-8 -*-
"""W938 一次性重建：首屏版式 W938 改动全部落到 site/index.html（幂等·可复跑）

背景：① 并行批次的级联重写把本页回退到 W937 版（W938 结构与左侧重排丢失·第 9 张读屏标签
   仍停在「持瓶菩萨」）⇒ 本脚本以「幂等补丁」方式一次性重建，避免多次编辑被再次冲掉；
   ② 用户令「要适配各种比例大小啊·要不然每个人看到的都是不一样」⇒ 背景渲染由 cover 改 contain：
      cover 会按容器比例裁切（2.36:1 的图在 1006×645 容器里左右各裁 407 源像素·主体右端被切；
      16:9 的图在 1440×520 里垂直裁 290 px·只剩半身）⇒ contain 在任何比例下都完整显示，
      主体恒锚定容器右下角，容器富余处露 #FAF7F0 宣纸底（与图底色同色·无缝）。

用法：py -3 scripts/_w938_apply_home.py [--dry-run]
"""
from __future__ import annotations

import argparse
import io
import os
import sys

P = os.path.join(r"D:\xiyouji", "site", "index.html")

# ---------- CSS 补丁 ----------

CSS_OLD_BLOCK = """        .masthead-copy { max-width: 640px; }
        .masthead-copy .kicker { margin-bottom: var(--space-5); }
        /* W862 B1 裁决 1：kicker 落 --bg → --accent-text（落点审计 _w862_accent_text_audit.json） */
        .kicker { color: var(--accent-text); }
        .masthead-copy h1 { margin-bottom: 14px; }
        .masthead-copy .eng {
            font-size: 12px; color: var(--ink-faint);
            letter-spacing: 0.08em; margin-bottom: 16px;
        }
        .masthead-copy .tagline { font-size: 16px; color: var(--ink-soft); margin-bottom: 10px; }
        .masthead-copy .meta-line { font-size: 13px; color: var(--accent-3); }
        /* W937：「100 回」数据块由右侧巨型块移入左侧文字区·横排一行 —— 首屏右侧整块留给插画主体。
           原方案在右侧用纸色渐变底遮罩（实测九环锡杖竖杆直穿「100」）是补救不是设计；
           数据块移出插画区后不再需要任何遮罩：右侧画面完整、左侧文字区零干扰。 */
        .masthead-facts { display: flex; align-items: center; gap: 18px; margin: 18px 0 16px; }
        .mega-row { display: flex; align-items: baseline; gap: 12px; justify-content: flex-end; }
        .mega-num {
            font-family: var(--font-serif); font-weight: 900;
            font-size: clamp(96px, 14vw, 180px); line-height: 0.85;
            color: var(--ink); letter-spacing: -0.03em;
        }
        .mega-unit { font-family: var(--font-serif); font-weight: 500; font-size: clamp(28px, 4vw, 52px); }
        .mega-label { margin-top: 10px; font-size: 13px; color: var(--ink-soft); }
        .mega-sub { margin-top: var(--space-2); font-size: 11px; color: var(--ink-faint); letter-spacing: 0.06em; }
        /* W937 作用域覆盖：数据块移入左侧后尺寸降一档（避免与 h1 抢视觉重量） */
        .masthead-facts .mega-row { gap: 4px; flex-shrink: 0; justify-content: flex-start; }
        .masthead-facts .mega-num { font-size: clamp(44px, 6vw, 64px); line-height: 0.9; letter-spacing: -0.02em; }
        .masthead-facts .mega-unit { font-size: clamp(20px, 2.4vw, 26px); }
        .masthead-facts .mega-label { margin-top: 0; line-height: 1.6; }
        .masthead-facts .mega-sub { margin-top: 3px; }
"""

CSS_NEW_BLOCK = """        /* W938：首屏左侧文字重排 —— 原布局七层平铺、字号跳跃、层级无引导；
           改为「眉题 → 标题组（中文 + 英文紧贴）→ 主张句（放大提色）→ 细线 → 数据带 → 标签 → CTA → 插画切换器」结构。 */
        .masthead-copy { max-width: 620px; }
        .masthead-copy .kicker { font-size: 11px; letter-spacing: .16em; margin-bottom: 14px; }
        /* W862 B1 裁决 1：kicker 落 --bg → --accent-text（落点审计 _w862_accent_text_audit.json） */
        .kicker { color: var(--accent-text); }
        .masthead-copy h1 { font-size: clamp(54px, 5.6vw, 78px); line-height: 1.04; margin-bottom: 12px; }
        .masthead-copy .eng {
            font-size: 11px; color: var(--ink-faint);
            letter-spacing: .14em; margin-bottom: 30px;
        }
        .masthead-copy .tagline {
            font-size: 19px; color: var(--ink); line-height: 1.75;
            margin-bottom: 26px; max-width: 23em;
        }
        .masthead-copy .meta-line { font-size: 13px; color: var(--accent-3); }
        /* W938：「100 回」数据块并入左侧文字区做横排一行（右侧整块留给插画） */
        .masthead-facts {
            display: flex; align-items: flex-start; gap: 18px;
            border-top: 1px solid var(--line); padding-top: 20px; margin: 26px 0 22px;
        }
        .masthead-facts .mega-row { display: flex; align-items: baseline; gap: 4px; flex-shrink: 0; }
        .masthead-facts .mega-num {
            font-family: var(--font-serif); font-weight: 900;
            font-size: clamp(44px, 5.4vw, 60px); line-height: .92;
            color: var(--ink); letter-spacing: -.02em;
        }
        .masthead-facts .mega-unit { font-family: var(--font-serif); font-weight: 500; font-size: clamp(20px, 2.2vw, 24px); }
        .masthead-facts .mega-label { margin-top: 2px; font-size: 13px; color: var(--ink-soft); line-height: 1.6; }
        .masthead-facts .mega-sub { margin-top: 3px; font-size: 10px; color: var(--ink-faint); letter-spacing: .1em; }
        .masthead-cta { margin-top: 20px; }
        .masthead-cta > a { font-size: 15px; font-weight: 600; color: var(--accent-2); }
        .masthead-cta > a:hover { text-decoration: underline; }
        /* W938：插画切换器归位左侧文字列内（与 CTA 同排会撑破 620px 容器伸进插画区·被金箍棒压住） */
        .hero-dots-row { display: flex; align-items: center; gap: 12px; margin-top: 16px; }
        .hero-dots-label { font-size: 11px; color: var(--ink-faint); letter-spacing: .12em; }
"""

CSS_BG_OLD = """            /* W938：改按宽铺满（100% auto）——原 cover 在真实容器（1006×645·视口 1006 时）
               会把 2.36:1 的图放大 0.63 倍、左右各裁掉 407 源像素 ⇒ 主体右端被切（实测金箍棒右上端断头）。
               改按宽铺满后图不裁切，容器上部留宣纸空场给标题区（底色同为 #FAF7F0·无缝）。 */
            background-size: 100% auto;
            background-position: right bottom;"""

CSS_BG_NEW = """            /* W938：改 contain —— 用户要求「适配各种比例大小·每个人看到的都一样」。
               cover 会按容器比例裁切：2.36:1 的图在 1006×645 容器里被放大 0.63 倍、左右各裁 407 源像素
               （主体右端被切·实测金箍棒右上端断头）；16:9 的图在 1440×520 里垂直裁 290 px（只剩半身）。
               contain 在任何视口比例下都完整显示、主体恒锚定容器右下角；容器富余处露 #FAF7F0 宣纸底
               （与图底色同色·无缝），故各人看到的构图一致。 */
            background-size: contain;
            background-position: right bottom;"""

CSS_MEDIA_OLD = """            .mega-row { justify-content: flex-start; }
            /* W865 D1：移动端 mega 数字降为紧凑计量（首屏减法·@375 省约 50px·桌面保持品牌大字）
               W937：改为作用域形式·否则压不过 .masthead-facts .mega-num 的桌面尺寸 */
            .mega-num { font-size: clamp(40px, 12vw, 56px); line-height: 1; }
            .mega-unit { font-size: clamp(18px, 5vw, 24px); }
            .masthead-facts .mega-num { font-size: clamp(38px, 11vw, 52px); }
            .masthead-facts .mega-unit { font-size: clamp(18px, 5vw, 22px); }
            .mega-label { margin-top: 4px; }"""

CSS_MEDIA_NEW = """            /* W865 D1：移动端 mega 数字降为紧凑计量（首屏减法·@375 省约 50px）
               W938：全部改作用域形式（全局 .mega-* 规则已移除·孤立选择器门禁） */
            .masthead-facts .mega-num { font-size: clamp(38px, 11vw, 52px); line-height: 1; }
            .masthead-facts .mega-unit { font-size: clamp(18px, 5vw, 22px); }
            .masthead-facts .mega-label { margin-top: 2px; }
            .masthead-cta { flex-wrap: wrap; gap: 14px; }"""

# ---------- HTML 补丁 ----------

HTML_OLD = """                <p class="meta-line">双轨写作 · 大众普及 × 学术研究 · 数据可视化</p>
                <p class="meta-line" style="margin-top:18px;">
                    <a href="reader/ch001.html" style="font-weight:600;color:var(--accent-2);">开始阅读 · 第 1 回 灵根育孕源流出 →</a>
                </p>
                <div class="hero-dots" role="group" aria-label="首屏插画切换（共 9 张）" hidden>"""

HTML_NEW = """                <p class="meta-line">双轨写作 · 大众普及 × 学术研究 · 数据可视化</p>
                <div class="masthead-cta">
                    <a href="reader/ch001.html">开始阅读 · 第 1 回 灵根育孕源流出 →</a>
                </div>
                <div class="hero-dots-row">
                    <span class="hero-dots-label">首屏插画</span>
                    <div class="hero-dots" role="group" aria-label="首屏插画切换（共 9 张）" hidden>"""

HTML_DOTS_OLD = """                    <button type="button" data-hero-dot="8" aria-label="第 9 张插画：持瓶菩萨立像" aria-pressed="false"></button>
                </div>
            </div>
        </section>"""

HTML_DOTS_NEW = """                    <button type="button" data-hero-dot="8" aria-label="第 9 张插画：取经四众西行" aria-pressed="false"></button>
                    </div>
                </div>
            </div>
        </section>"""

PAIRS = [
    ("CSS 首页左侧重排", CSS_OLD_BLOCK, CSS_NEW_BLOCK),
    ("CSS 背景 contain", CSS_BG_OLD, CSS_BG_NEW),
    ("CSS 移动端作用域", CSS_MEDIA_OLD, CSS_MEDIA_NEW),
    ("HTML masthead 结构", HTML_OLD, HTML_NEW),
    ("HTML 第 9 张按钮 + 闭合", HTML_DOTS_OLD, HTML_DOTS_NEW),
    ("SLIDES 第 9 张",
     "    { src: 'static/images/hero-line-09-pilgrim-four.webp', label: '取经四众西行' }",
     "    { src: 'static/images/hero-line-09-somersault-cloud.webp', label: '筋斗云' }"),
    ("SLIDES 第 4 张",
     "    { src: 'static/images/hero-line-04-sinan-compass.webp', label: '司南' }",
     "    { src: 'static/images/hero-line-04-tight-crown.webp', label: '紧箍儿' }"),
    ("HTML 第 4 张按钮",
     'aria-label="第 4 张插画：司南"',
     'aria-label="第 4 张插画：紧箍儿"'),
    ("HTML 第 9 张按钮",
     'aria-label="第 9 张插画：取经四众西行"',
     'aria-label="第 9 张插画：筋斗云"'),
    ("CSS 注释·图集构成",
     "/* W935：首屏插画图集（9 张 = W931 线描 8 张 + W932 持瓶菩萨收尾重音）",
     "/* W938：首屏插画图集（9 张 = W931 线描 8 张 + W938 取经四众收尾重音·全部 2400×1017）"),
    ("JS 注释·图集构成",
     "// W935：首屏插画图集（9 张 = W931 线描 8 张 + W932 持瓶菩萨收尾重音）",
     "// W938：首屏插画图集（9 张 = W931 线描 8 张 + W938 取经四众收尾重音·全部 2400×1017）"),
    # —— 以下两条曾被并行会话的 site/index.html pathspec 提交覆盖（他们提交的是自己工作树版本）——
    ("CSS 切换器标签不折行",
     "        .hero-dots-label { font-size: 11px; color: var(--ink-faint); letter-spacing: .12em; }",
     "        .hero-dots-label { font-size: 11px; color: var(--ink-faint); letter-spacing: .12em; white-space: nowrap; flex-shrink: 0; }"),
    ("CSS 窄屏插画置顶",
     "            .masthead-cta { flex-wrap: wrap; gap: 14px; }",
     "            .masthead-cta { flex-wrap: wrap; gap: 14px; }\n"
     "            /* W938：窄屏 masthead 变 column 布局（文字在上）⇒ 插画移到容器顶部，首屏即可见\n"
     "               （contain 下按宽贴合·375px 视口图高约 159px·完整不裁切） */\n"
     "            .masthead { background-position: right top; }"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    raw = io.open(P, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    # 统一到 LF 做匹配，写回时再按原行尾还原（否则 CRLF 文件与 LF 补丁串匹配不上）
    t = raw.decode("utf-8").replace("\r\n", "\n")

    applied, skipped, failed = [], [], []
    for name, old, new in PAIRS:
        if new in t:
            skipped.append(name)
            continue
        if old not in t:
            failed.append(name)
            continue
        t = t.replace(old, new, 1)
        applied.append(name)

    if args.dry_run:
        print("DRY 将应用: %s" % applied)
        print("     已具备: %s" % skipped)
        print("     未匹配: %s" % failed)
        return 0

    io.open(P, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))
    print("已应用: %s" % applied)
    print("已具备: %s" % skipped)
    print("未匹配: %s" % failed)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
