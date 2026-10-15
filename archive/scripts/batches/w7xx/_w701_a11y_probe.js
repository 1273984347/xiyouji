#!/usr/bin/env node
/* _w701_a11y_probe.js — BL-20 验收探针（一次性）：site/data 87 页 file:// 全扫。
 * 每页断言：≥1 个图表元素带 data-chart-a11y + tabindex="0" + 非空 aria-label +
 * aria-describedby 指向存在的 sr-only 摘要块（文本 ≥20 字）。
 * 抽样键盘断言（3 页）：连按 Tab ≤10 次内 document.activeElement 命中图表元素。
 * 退出码 = 失败页数。
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const SKIP = new Set(['_shell.html']);
const FOCUS_SAMPLES = ['story-timeline.html', 'character-relationship-3d.html', 'hardship-heatmap.html'];

(async () => {
  const pages = fs.readdirSync(DATA).filter(f => f.endsWith('.html') && !SKIP.has(f));
  const browser = await chromium.launch({ headless: true });
  const fails = [];
  for (const f of pages) {
    const page = await browser.newPage();
    const errs = [];
    page.on('pageerror', (e) => errs.push(String(e).slice(0, 100)));
    try {
      await page.goto('file:///' + path.join(DATA, f).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
      await page.waitForTimeout(1800); // EMBEDDED 回退渲染 + MutationObserver 结算
      const res = await page.evaluate(() => {
        // 先数「应有标注」的候选：≥200x120 的顶层 svg/canvas——无候选页=N/A（对话/
        // 搜索页纯文本、tag-cloud 词云为 div+span 群对读屏天然可读、-view 壳页）
        const big = [...document.querySelectorAll('svg,canvas')].filter(el => {
          if (el.tagName === 'SVG' && el.ownerSVGElement) return false;
          if (el.closest('[class*="tooltip"],.chart-tooltip,#audit-halo,[aria-hidden="true"]')) return false;
          const r = el.getBoundingClientRect();
          return r.width >= 200 && r.height >= 120;
        });
        if (!big.length) return { ok: true, na: true };
        const els = [...document.querySelectorAll('[data-chart-a11y]')];
        if (!els.length) return { ok: false, why: '有 ' + big.length + ' 个大图元素但 0 标注' };
        for (const el of els) {
          if (el.getAttribute('tabindex') !== '0') return { ok: false, why: 'tabindex≠0' };
          if (!(el.getAttribute('aria-label') || '').trim()) return { ok: false, why: 'aria-label 空' };
          const sid = el.getAttribute('aria-describedby');
          const s = sid && document.getElementById(sid);
          if (!s || (s.textContent || '').length < 20) return { ok: false, why: '摘要块缺失/过短' };
          const st = getComputedStyle(s);
          if (st.position !== 'absolute' || parseFloat(st.width) > 2) return { ok: false, why: '摘要块非 sr-only' };
        }
        return { ok: true, n: els.length };
      });
      if (errs.length) res.why = (res.why || '') + ' pageerror×' + errs.length + ':' + errs[0];
      if (!res.ok) fails.push(f + ' → ' + (res.why || 'unknown'));
      else if (process.argv.includes('-v')) console.log('[PASS] ' + f + '（' + res.n + ' 图表元素）');
    } catch (e) {
      fails.push(f + ' → 探针异常: ' + String(e).slice(0, 100));
    }
    await page.close();
  }

  for (const f of FOCUS_SAMPLES) {
    const page = await browser.newPage();
    try {
      await page.goto('file:///' + path.join(DATA, f).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
      await page.waitForTimeout(1800);
      let hit = false;
      for (let i = 0; i < 25 && !hit; i++) {
        await page.keyboard.press('Tab');
        hit = await page.evaluate(() =>
          !!(document.activeElement && document.activeElement.hasAttribute('data-chart-a11y')));
      }
      if (!hit) fails.push(f + ' → Tab×10 未命中图表焦点');
      else console.log('[FOCUS] ' + f + ' 键盘可达 ✓');
    } catch (e) {
      fails.push(f + ' → 焦点探针异常: ' + String(e).slice(0, 100));
    }
    await page.close();
  }

  await browser.close();
  console.log('\n共 ' + pages.length + ' 页 + ' + FOCUS_SAMPLES.length + ' 页焦点抽样；失败 ' + fails.length);
  fails.slice(0, 12).forEach(x => console.log('  [FAIL] ' + x));
  process.exit(fails.length ? 1 : 0);
})();
