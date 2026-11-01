# -*- coding: utf-8 -*-
"""W1073 基线补拍：桌面浅色首页基线（W1070 shots/ 缺此件——只有 dark_home 与移动端 t11_m_home）。

用途：D-1 验收项 3「浅色模式零变化——浅色截图与改动前像素一致」需要**改动前**的桌面浅色首页截图做对照。
W1070 存档目录里只有 dark_home.png（深色桌面）与 t11_m_home.png（375×812 移动端），
桌面浅色首页基线缺失 ⇒ 本脚本在改动前补拍。

跑法：先起本地服务（或 file:// 直开），再：
  python scripts/_w1073_baseline_shot.py --out tmpe/w1073/baseline
"""
import argparse
import os
import pathlib

VIEWPORTS = [('desktop', 1440, 900), ('mobile', 375, 812)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='tmpe/w1073/baseline')
    ap.add_argument('--url', default='file:///' + str(pathlib.Path('site/index.html').resolve()).replace('\\', '/'))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    from playwright.sync_api import sync_playwright
    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, w, h in VIEWPORTS:
            ctx = b.new_context(viewport={'width': w, 'height': h})
            ctx.add_init_script("try{localStorage.setItem('xy-theme','light')}catch(e){}")
            pg = ctx.new_page()
            pg.on('console', lambda m: errors.append(f'{m.type}: {m.text}')
                  if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
            pg.goto(args.url, wait_until='load')
            # 等 GSAP 入场动画结束再取样（与 _w1073_probe.py 同口径·否则比出抗锯齿假差异）
            pg.wait_for_timeout(4000)
            try:
                pg.evaluate("""() => {
                  if (window.gsap && gsap.globalTimeline) {
                    gsap.globalTimeline.getChildren(true,true,true).forEach(a => { try { a.progress(1); } catch(e){} });
                  }
                }""")
                pg.wait_for_timeout(600)
            except Exception:
                pass
            out = os.path.join(args.out, f'light_{name}.png')
            pg.screenshot(path=out)
            print('SHOT', out, os.path.getsize(out), 'bytes')
            ctx.close()
        b.close()

    if errors:
        print('CONSOLE ERRORS:')
        for e in errors[:20]:
            print('  ', e)
    else:
        print('CONSOLE 0 error')


if __name__ == '__main__':
    main()
