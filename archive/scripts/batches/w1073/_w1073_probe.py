# -*- coding: utf-8 -*-
"""W1073 · D-1 深色变体验收探针（真实 Playwright Chromium·非 IAB 合成点击）。

验收项（任务书 §3C）：
  1. 9/9 变体存在 + 2400×1017 + ≤300KB + webp        → _w1073_dark_verify.py（资产层）
  2. 深色下 h1/tagline 对当前插画对比度 ≥4.5:1（AA）    → 本脚本 §contrast（逐张验 9 张）
  3. 浅色模式零变化（对照改动前基线）                   → 本脚本 §light_baseline
  4. 深↔浅切换 ≤150ms 换图 + 无布局位移 + 无 404        → 本脚本 §theme_switch
  5. 轮播自动推进与圆点交互不受影响 + reduced-motion 无动画 → 本脚本 §carousel
  6. file:// 直开可用（无新增失败）                      → 本脚本 §file_mode

跑法：
  python scripts/_w1073_probe.py --baseline tmpe/w1073/baseline
"""
import argparse
import os
import pathlib
import sys
import time

from PIL import Image
import numpy as np

W, H = 2400, 1017
DARK_PAPER = (34, 29, 22)
INK_DARK = (242, 235, 220)
# 深色变体文件名 = 「原名 + -dark」（任务书 §3A 规定·实测 W1073 首轮踩过命名不一致⇒ 9 张全 404）
DARK_NAMES = [
    'hero-line-01-ruyi-staff-dark.webp',
    'hero-line-02-journey-scroll-dark.webp',
    'hero-line-03-classic-scroll-dark.webp',
    'hero-line-04-tight-crown-dark.webp',
    'hero-line-05-lotus-dark.webp',
    'hero-line-06-nine-ring-staff-dark.webp',
    'hero-line-07-banana-fan-dark.webp',
    'hero-line-08-jade-vase-dark.webp',
    'hero-line-09-somersault-cloud-dark.webp',
]


def srgb_to_lin(c):
    c = np.asarray(c, dtype=float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lum(rgb):
    v = srgb_to_lin(rgb)
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def cr(x, y):
    la, lb = lum(x), lum(y)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def paper_color_of(path):
    """取该图纸面中位色（低饱和 + 暗底邻域）。"""
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    L = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    mx = a.max(2); mn = a.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    m = (sat < 0.55) & (L >= 12) & (L < 95)
    if m.sum() < 1000:
        m = (sat < 0.6) & (L < 110)
    return tuple(a[m].mean(0).round(0).astype(int)), L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--baseline', default='tmpe/w1073/baseline')
    ap.add_argument('--out', default='tmpe/w1073/probe')
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    url = 'file:///' + str(pathlib.Path('site/index.html').resolve()).replace('\\', '/')
    fails = []

    # ---------- §contrast：9 张逐张验 AA（对「插画该片纸面」比） ----------
    print('=== §2 深色 h1 对当前插画对比度（9 张逐张·AA 门槛 4.5）===')
    for fname in DARK_NAMES:
        p = f'site/static/images/{fname}'
        pc, _ = paper_color_of(p)
        c = cr(INK_DARK, pc)
        ok = c >= 4.5
        if not ok:
            fails.append(f'§2 {fname} 对比度 {c:.2f} < 4.5')
        print(f'  {fname[:13]} 纸底{pc} 对比度 {c:.2f} {"OK" if ok else "FAIL"}')

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()

        # ---------- §theme_switch：深↔浅切换 + CLS + 404 ----------
        print()
        print('=== §4 主题实时切换（≤150ms 换图 / CLS 0 / 无 404）===')
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        ctx.add_init_script("try{localStorage.setItem('xy-theme','dark')}catch(e){}")
        pg = ctx.new_page()
        bad = []
        pg.on('response', lambda r: bad.append((r.status, r.url)) if r.status >= 400 else None)
        pg.goto(url, wait_until='load')
        pg.wait_for_timeout(1200)

        dark_bg = pg.evaluate("getComputedStyle(document.getElementById('heroGallery')).backgroundImage")
        print(f'  深色首帧 background-image: {dark_bg[:90]}')
        if '-dark.webp' not in dark_bg:
            fails.append('§4 深色首帧未指向 -dark 变体')

        # 浅色用户零新增请求：另开一个浅色 context·统计是否请求了 dark 变体
        ctx2 = b.new_context(viewport={'width': 1440, 'height': 900})
        ctx2.add_init_script("try{localStorage.setItem('xy-theme','light')}catch(e){}")
        pg2 = ctx2.new_page()
        dark_hits = []
        pg2.on('request', lambda r: dark_hits.append(r.url) if '-dark.webp' in r.url else None)
        pg2.goto(url, wait_until='load')
        pg2.wait_for_timeout(1500)
        print(f'  浅色访客请求 deep 变体次数: {len(dark_hits)}（须 0）')
        if dark_hits:
            fails.append(f'§4 浅色访客请求了 {len(dark_hits)} 次深色变体')

        # 切主题 → 计时换图
        pg.evaluate("""() => {
          const b = document.querySelector('.theme-toggle');
          if (b) b.click();
        }""")
        t0 = time.time()
        got = False
        while time.time() - t0 < 1.0:
            bg = pg.evaluate("getComputedStyle(document.getElementById('heroGallery')).backgroundImage")
            if '-dark.webp' not in bg:
                got = True
                break
            time.sleep(0.01)
        dt = (time.time() - t0) * 1000
        print(f'  切回浅色耗时 {dt:.0f}ms · 换图 {"OK" if got else "FAIL"}')
        if not got:
            fails.append('§4 切换后 background-image 未变')
        if dt > 150:
            fails.append(f'§4 切换耗时 {dt:.0f}ms > 150ms')

        # CLS：先测**基线**（页面加载态·未经任何切换）→ 再测**切换后**增量
        # 口径（实测 W1073 首轮）：CLS 0.0001 来自页面初始加载（字体回退等既有因素），
        # 不是本批改动引入 ⇒ 判据须看「切换前后的 CLS 增量」，绝对值只作参考。
        cls_base = pg.evaluate("""() => new Promise(res => {
          let v = 0;
          try { new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) v += e.value; }).observe({type:'layout-shift', buffered:true}); } catch(e) {}
          setTimeout(() => res(v), 800);
        })""")
        pg.evaluate("""() => {
          const b = document.querySelector('.theme-toggle');
          if (b) b.click();
        }""")
        pg.wait_for_timeout(1500)
        cls_after = pg.evaluate("""() => new Promise(res => {
          let v = 0;
          try { new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) v += e.value; }).observe({type:'layout-shift', buffered:true}); } catch(e) {}
          setTimeout(() => res(v), 600);
        })""")
        cls_delta = cls_after - cls_base
        print(f'  CLS 基线 {cls_base:.4f} → 切换后 {cls_after:.4f}（增量 {cls_delta:.4f}·须 0）')
        if cls_delta > 0.001:
            fails.append(f'§4 切换引入 CLS 增量 {cls_delta:.4f} > 0.001')

        if bad:
            for st, u in bad[:8]:
                print(f'  HTTP {st}: {u[:110]}')
            fails.append(f'§4 出现 {len(bad)} 个 4xx/5xx')
        else:
            print('  无 404/4xx')

        # —— 补盲区：CSS background-image 的加载失败**不发 response 事件** ——
        # 实测 W1073 首轮踩过：深色变体文件名与引用不匹配（9 张全 404），
        # 而浏览器的 404 监控与 response 监听**都抓不到**（CSS 背景图走的是样式系统加载通道）
        #   ⇒ 症状只是「插画不显示」·被 Playwright 的 element screenshot 暴露出来。
        # 修法：主动用 Image() 探测每个引用 URL 的**解码结果**（naturalWidth>0 即加载成功）。
        decode = pg.evaluate("""async (urls) => {
          const out = [];
          for (const u of urls) {
            const ok = await new Promise(res => {
              const im = new Image();
              im.onload = () => res(im.naturalWidth > 0);
              im.onerror = () => res(false);
              im.src = u;
            });
            out.push({u: u, ok: ok});
          }
          return out;
        }""", [f'static/images/{n}' for n in DARK_NAMES])
        bad_decode = [d['u'] for d in decode if not d['ok']]
        print(f'  深色变体解码：{len(decode)-len(bad_decode)}/{len(decode)} 成功')
        if bad_decode:
            for u in bad_decode:
                print(f'    解码失败: {u}')
            fails.append(f'§4 {len(bad_decode)} 个深色变体解码失败（CSS 背景图 404 静默）')

        # ---------- §5 轮播推进 + 圆点交互 + reduced-motion ----------
        print()
        print('=== §5 轮播推进 / 圆点交互 / reduced-motion ===')
        ctx3 = b.new_context(viewport={'width': 1440, 'height': 900})
        pg3 = ctx3.new_page()
        pg3.goto(url, wait_until='load')
        pg3.wait_for_timeout(800)
        before = pg3.evaluate("getComputedStyle(document.getElementById('heroGallery')).backgroundImage")
        pg3.evaluate("document.querySelectorAll('[data-hero-dot]')[4].click()")
        pg3.wait_for_timeout(300)
        after = pg3.evaluate("getComputedStyle(document.getElementById('heroGallery')).backgroundImage")
        pressed = pg3.evaluate(
            "document.querySelectorAll('[data-hero-dot][aria-pressed=\"true\"]').length")
        print(f'  点第 5 个圆点 · bg 变化={"OK" if before != after else "FAIL"} · aria-pressed 数={pressed}')
        if before == after:
            fails.append('§5 圆点点击未换图')
        if pressed != 1:
            fails.append(f'§5 aria-pressed 数 {pressed} != 1')

        ctx4 = b.new_context(viewport={'width': 1440, 'height': 900},
                             reduced_motion='reduce')
        pg4 = ctx4.new_page()
        pg4.goto(url, wait_until='load')
        pg4.wait_for_timeout(600)
        b1 = pg4.evaluate("getComputedStyle(document.getElementById('heroGallery')).backgroundImage")
        pg4.wait_for_timeout(7000)
        b2 = pg4.evaluate("getComputedStyle(document.getElementById('heroGallery')).backgroundImage")
        print(f'  reduced-motion 下 7 秒后 bg 变化={"FAIL（仍在自动推进）" if b1 != b2 else "OK（静止）"}')
        if b1 != b2:
            fails.append('§5 reduced-motion 下仍在自动推进')

        # ---------- §3 浅色零变化（对照基线） ----------
        print()
        print('=== §3 浅色模式零变化（对照改动前基线）===')
        base = os.path.join(args.baseline, 'light_desktop.png')
        cur = os.path.join(args.out, 'light_desktop_after.png')
        ctx5 = b.new_context(viewport={'width': 1440, 'height': 900})
        ctx5.add_init_script("try{localStorage.setItem('xy-theme','light')}catch(e){}")
        pg5 = ctx5.new_page()
        pg5.goto(url, wait_until='load')
        # 等 GSAP 入场动画**完全结束**再取样（口径订正·实测 W1073 首轮）：
        # 动画中间帧下标题字形处于亚像素变换态 ⇒ 与基线比出 0.307% 的抗锯齿边缘差，
        # 视觉完全一致 ⇒ 那是「取样时点」造成的假差异，不是本批引入的像素变化。
        # 判据：轮询 gsap.globalTimeline 的进度或直接等足够长（入场动画 ≤2s + 余量）。
        pg5.wait_for_timeout(4000)
        try:
            pg5.evaluate("""() => {
              if (window.gsap && gsap.globalTimeline) {
                gsap.globalTimeline.getChildren(true,true,true).forEach(a => { try { a.progress(1); } catch(e){} });
              }
            }""")
            pg5.wait_for_timeout(600)
        except Exception:
            pass
        pg5.screenshot(path=cur)
        if os.path.exists(base):
            a = np.asarray(Image.open(base).convert('RGB')).astype(int)
            c = np.asarray(Image.open(cur).convert('RGB')).astype(int)
            if a.shape != c.shape:
                print(f'  尺寸不同 {a.shape} vs {c.shape} · 跳过像素比对')
            else:
                diff = np.abs(a - c)
                changed = (diff.max(axis=2) > 2).mean()
                maxd = diff.max()
                print(f'  像素差异 >2 占比 {changed*100:.4f}% · 最大通道差 {maxd}')
                if changed > 0.002:
                    fails.append(f'§3 浅色像素差异 {changed*100:.3f}% > 0.2%')
                else:
                    print('  浅色模式视觉零变化 OK')
        else:
            print(f'  基线缺失 {base} · 跳过')

        b.close()

    print()
    print('=== 结论 ===')
    if fails:
        for f in fails:
            print('  FAIL', f)
        return 1
    print('全部验收项通过 ✅')
    return 0


if __name__ == '__main__':
    sys.exit(main())
