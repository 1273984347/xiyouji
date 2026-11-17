#!/usr/bin/env python3
"""
check_screenshot_theme_delta.py — 明暗两态截图必须真的不同（W1264 立·E-245 机器化）

背景（坑位 E-245）：
  视觉改动的截图「看起来不一样」不等于「真的不一样」——暗色态可能整版复制了亮色图，
  而探针（0 console error / 0 横滚 / scrollWidth==clientWidth）全绿。
  实证：某次重渲染用 localStorage 置主题，而样板只认 prefers-color-scheme 媒体查询
  ⇒ 落地页「暗色图」与「亮色图」字节数完全相同（290,772 = 290,772），
  即暗色截图其实是亮色图重复写了一遍。**探针全绿 ≠ 产物正确**。

本判据（双通道·缺一不可）：
  ① 底色读数：body 的 computed background-color 在两态必须不同（且暗态确实变暗）
  ② 字节数交叉校验：两态 PNG 的文件大小必须不同（相同 ⇒ 极可能是同一张图）

用法：
  py -3 scripts/check_screenshot_theme_delta.py                 # 默认抽样页
  py -3 scripts/check_screenshot_theme_delta.py --pages a.html b.html
  py -3 scripts/check_screenshot_theme_delta.py --out <dir>

退出码：0 = 通过；1 = 有 FAIL；2 = 执行异常（fail-closed）
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT_DEFAULT = os.path.join(ROOT, "scripts", "output", "theme-delta-shots")

DEFAULT_PAGES = [
    ("index", "site/index.html"),
    ("data", "site/data/chapter-stats.html"),
    ("reader", "site/reader/ch001.html"),
    ("en", "site/en/index.html"),
]


def _playwright_root():
    """定位 playwright：优先仓内 scripts/node_modules，其次全局 npm。"""
    cand = os.path.join(ROOT, "scripts", "node_modules", "playwright")
    if os.path.isdir(cand):
        return cand
    try:
        out = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True, timeout=60).stdout.strip()
        if out and os.path.isdir(os.path.join(out, "playwright")):
            return os.path.join(out, "playwright")
    except Exception:
        pass
    return None


PROBE = r"""
const { chromium } = require(process.argv[2]);
const fs = require('fs');
const OUT = process.argv[3];
const PAGES = JSON.parse(process.argv[4]);
fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch();
  const rows = [];
  for (const [k, rel] of PAGES) {
    for (const theme of ['light', 'dark']) {
      const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: theme });
      const pg = await ctx.newPage();
      try {
        await pg.goto('file:///' + rel, { waitUntil: 'load', timeout: 45000 });
        await pg.waitForTimeout(1800);
        // 双通道：媒体查询 + data-theme 属性（两条通路都要设·E-245）
        if (theme === 'dark') {
          await pg.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
          await pg.waitForTimeout(400);
        }
        const st = await pg.evaluate(() => ({
          bg: getComputedStyle(document.body).backgroundColor,
          attr: document.documentElement.getAttribute('data-theme') || '(none)'
        }));
        const f = OUT + '/' + k + '-' + theme + '.png';
        await pg.screenshot({ path: f, fullPage: false });
        rows.push({ key: k, theme, bg: st.bg, attr: st.attr, bytes: fs.statSync(f).size, file: f });
      } catch (e) {
        rows.push({ key: k, theme, error: String(e).slice(0, 160) });
      }
      await ctx.close();
    }
  }
  await b.close();
  console.log(JSON.stringify(rows));
})();
"""


def _parse_rgb(s):
    import re
    m = re.match(r"rgba?\(([^)]+)\)", s or "")
    if not m:
        return None
    parts = [p for p in re.split(r"[,\s/]+", m.group(1)) if p]
    try:
        return tuple(float(p) for p in parts[:3])
    except ValueError:
        return None


def _luma(rgb):
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def _run_probe(pw, out, pages):
    """跑 Playwright 探针并回读 JSON 行（fail-closed：异常或空输出即判红）。"""
    probe_js = os.path.join(out, '_probe_theme_delta.js')
    with open(probe_js, 'w', encoding='utf-8') as fh:
        fh.write(PROBE)
    try:
        res = subprocess.run(
            ['node', probe_js, pw, out, json.dumps(pages)],
            capture_output=True, text=True, timeout=600,
        )
    except Exception as e:
        return None, '探针执行异常：%s' % str(e)[:200]
    if res.returncode != 0 or not res.stdout.strip():
        return None, '探针无有效输出（returncode=%s）⇒ fail-closed：%s' % (
            res.returncode, res.stderr.strip()[:200])
    try:
        return json.loads(res.stdout.strip().splitlines()[-1]), ''
    except Exception as e:
        return None, '探针输出不可解析：%s' % str(e)[:160]


def _judge(rows):
    """双校验判据：① 底色读数必须不同且暗态更暗 ② 两态 PNG 字节数必须不同。"""
    fails = []
    by_key = {}
    for r in rows:
        if r.get('error'):
            fails.append('%s/%s 渲染失败：%s' % (r['key'], r['theme'], r['error']))
            continue
        by_key.setdefault(r['key'], {})[r['theme']] = r
    for key, pair in sorted(by_key.items()):
        L, D = pair.get('light'), pair.get('dark')
        if not L or not D:
            fails.append('%s 缺明/暗一态' % key)
            continue
        lr, dr = _parse_rgb(L['bg']), _parse_rgb(D['bg'])
        if not lr or not dr:
            fails.append('%s 底色读数不可解析（light=%s dark=%s）' % (key, L['bg'], D['bg']))
        elif lr == dr:
            fails.append('%s 两态底色相同（%s）⇒ 暗色态未生效' % (key, L['bg']))
        elif _luma(dr) >= _luma(lr):
            fails.append('%s 暗态底色不比亮态暗（light=%s dark=%s）' % (key, L['bg'], D['bg']))
        if L['bytes'] == D['bytes']:
            fails.append('%s 两态截图字节数相同（%d）⇒ 暗色图疑似亮色图重复' % (key, L['bytes']))
        print('  %-8s light bg=%-22s %d B | dark bg=%-22s %d B' % (
            key, L['bg'], L['bytes'], D['bg'], D['bytes']))
    return fails


def _resolve_pages(args):
    """解析待测页面：默认抽样页 或 --pages 显式给定。"""
    if args.pages:
        return [(os.path.splitext(os.path.basename(x))[0], x.replace(chr(92), '/'))
                for x in args.pages]
    return [(k, os.path.join(ROOT, rel).replace(chr(92), '/')) for k, rel in DEFAULT_PAGES]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pages', nargs='*', default=None, help='相对 ROOT 的页面路径')
    ap.add_argument('--out', default=OUT_DEFAULT)
    args = ap.parse_args()

    pw = _playwright_root()
    if not pw:
        print('FAIL  playwright 不可用（仓内 scripts/node_modules 与全局 npm 均未找到）')
        return 2

    out = args.out
    os.makedirs(out, exist_ok=True)
    rows, err = _run_probe(pw, out, _resolve_pages(args))
    if rows is None:
        print('FAIL  ' + err)
        return 2

    fails = _judge(rows)
    if fails:
        print('---- 明暗两态截图差异判据：%d FAIL ----' % len(fails))
        for f in fails:
            print('FAIL  ' + f)
        return 1
    print('---- 明暗两态截图差异判据：0 FAIL（%d 页×2 态·底色读数 + 字节数双校验）----' % (len(rows) // 2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
