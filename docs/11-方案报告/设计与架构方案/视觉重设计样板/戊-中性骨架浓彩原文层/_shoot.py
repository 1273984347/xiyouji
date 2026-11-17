# -*- coding: utf-8 -*-
"""W1262 self-check shots: light/dark x 1280/375 for both pages + behavior probes."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
SHOTS = ROOT / 'shots'
SHOTS.mkdir(exist_ok=True)

PAGES = {
    'landing': 'sample-landing.html',
    'dataviz': 'sample-dataviz.html',
}

def shoot():
    with sync_playwright() as p:
        b = p.chromium.launch()
        errors = []
        for name, path in PAGES.items():
            for theme in ('light', 'dark'):
                for w, h, tag in ((1280, 900, '1280'), (375, 812, '375')):
                    pg = b.new_page(viewport={'width': w, 'height': h})
                    pg.on('console', lambda m, n=name: errors.append((n, m.text)) if m.type in ('error',) else None)
                    pg.on('pageerror', lambda e, n=name: errors.append((n, 'PAGEERROR ' + str(e))))
                    pg.emulate_media(color_scheme=theme)
                    pg.goto(f'file:///{ROOT / path}'.replace('\\', '/'))
                    pg.wait_for_timeout(800)
                    # scroll through the page so IntersectionObserver reveals fire
                    pg.evaluate("""async () => {
                        const H = document.documentElement.scrollHeight;
                        for (let y = 0; y <= H; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); }
                        window.scrollTo(0, 0);
                    }""")
                    pg.wait_for_timeout(900)
                    # horizontal scroll probe
                    hs = pg.evaluate(
                        "() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth})")
                    flag = 'HSCROLL!' if hs['sw'] > hs['cw'] else ''
                    pg.screenshot(path=str(SHOTS / f'{name}-{theme}-{tag}.png'), full_page=True)
                    print(f'{name} {theme} {tag}: scrollW={hs["sw"]} clientW={hs["cw"]} {flag}')
                    pg.close()
        # tooltip behavior probe on dataviz (light, 1280): hover a bar
        pg = b.new_page(viewport={'width': 1280, 'height': 900})
        pg.on('pageerror', lambda e: errors.append(('dataviz', 'PAGEERROR ' + str(e))))
        pg.emulate_media(color_scheme='light')
        pg.goto(f'file:///{ROOT / "sample-dataviz.html"}'.replace('\\', '/'))
        pg.wait_for_timeout(1500)
        hit = pg.locator('.bar-hit').nth(1)
        hit.hover(force=True)
        pg.wait_for_timeout(400)
        vis = pg.evaluate("() => document.getElementById('chartTip').classList.contains('visible')")
        box = pg.evaluate("""() => { const t = document.getElementById('chartTip');
            const r = t.getBoundingClientRect();
            return {l: r.left, t: r.top, r: r.right, b: r.bottom, vw: innerWidth, vh: innerHeight}; }""")
        inview = box['l'] >= 0 and box['t'] >= 0 and box['r'] <= box['vw'] and box['b'] <= box['vh']
        print(f'dataviz tooltip visible={vis} in-viewport={inview} rect={box}')
        pg.screenshot(path=str(SHOTS / 'dataviz-tooltip-light-1280.png'))
        # filter to demon + search miss -> empty state
        pg.click('button[data-group="demon"]')
        pg.fill('#searchInput', '孙悟空')
        pg.wait_for_timeout(500)
        empty_shown = pg.evaluate("() => document.getElementById('barEmpty').classList.contains('show')")
        print(f'dataviz empty-state shown after demon+miss filter: {empty_shown}')
        pg.screenshot(path=str(SHOTS / 'dataviz-empty-light-1280.png'))
        pg.close()
        # manual data-theme override check (attr path, not media query)
        pg = b.new_page(viewport={'width': 1280, 'height': 900})
        pg.emulate_media(color_scheme='light')
        pg.goto(f'file:///{ROOT / "sample-landing.html"}'.replace('\\', '/'))
        pg.wait_for_timeout(600)
        pg.evaluate("() => document.documentElement.setAttribute('data-theme','dark')")
        pg.wait_for_timeout(500)
        bg = pg.evaluate("() => getComputedStyle(document.body).backgroundColor")
        print(f'landing data-theme=dark body bg = {bg} (expect rgb(20, 19, 17))')
        pg.close()
        b.close()
        if errors:
            print('CONSOLE/PAGE ERRORS:')
            for n, e in errors:
                print(f'  [{n}] {e}')
        else:
            print('NO CONSOLE ERRORS')

if __name__ == '__main__':
    shoot()
