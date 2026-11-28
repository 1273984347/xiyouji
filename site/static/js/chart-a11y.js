/* chart-a11y.js — 可视化页读屏替代文本与 tabable 焦点层（W701·BL-20·经用户圈选动工）
 *
 * 解决：D3/Three 图表为 svg/canvas 静默元素——屏幕阅读器读不到图名，键盘用户
 * 无法把焦点移到图表本体（对比度/色盲/窄屏/触屏/reduced-motion/skip-link 均已有
 * 门禁或批次闭环，本模块补 a11y 唯一未覆盖面）。
 *
 * 机制（零页面静态 DOM/CSS 改动·file:// 直开可用·外部本地脚本无内联哈希需求）：
 *   1) 扫描文档内顶层 svg/canvas，按渲染尺寸过滤（≥200x120，排除图例/icon/tooltip），
 *      每页至多标注 24 个（小多联网格整组覆盖）；
 *   2) 对每个图表元素注入 tabindex="0" + role="img" + aria-label（取最近前驱标题，
 *      缺省退页面标题）+ aria-describedby 指向注入的 sr-only 摘要块；
 *   3) 摘要块内容 = 图名 + KPI 摘要（.kpi-card 等可见统计文本·至多 6 条）+
 *      「数据源」区块指引（#dataSource 在场时）；
 *   4) MutationObserver 兜晚渲染图表（d3 fetch/EMBEDDED 异步建图），20s 后停观；
 *   5) i18n（W773）：摘要文本按 document.documentElement.lang 选 zh/en
 *      （缺省 zh·中文页行为逐字节不变）——EN 镜像页（site/en·W773 起注入）
 *      不再产出中文读屏文本。
 *
 * 幂等：window.__chartA11y 全局闸 + 元素级 data-chart-a11y 标记。无动画（不动效契约面）。
 */
(function () {
  'use strict';
  if (window.__chartA11y) return;
  window.__chartA11y = true;

  var SR_STYLE = 'position:absolute;width:1px;height:1px;padding:0;margin:-1px;' +
    'overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;';
  var MIN_W = 200;
  var MIN_H = 120;
  var MAX_CHARTS = 24;
  var OBSERVE_MS = 20000;
  var appliedCount = 0;

  // W773 最小 i18n：zh 串与原实现逐字节一致（中文页零行为变化）；en 供 site/en 镜像页
  var LANG = (document.documentElement.lang || 'zh').toLowerCase().indexOf('en') === 0 ? 'en' : 'zh';
  var I18N = {
    zh: {
      chart: '（交互式图表）。',
      kpi: '关键统计：',
      kpiSep: '；',
      kpiEnd: '。',
      source: '数据来源与引用格式见页面下方「数据源」区块。',
      focus: '本区块已设为可聚焦，屏幕阅读器可直接朗读本段替代文本。',
      fallbackTitle: '数据图表',
      tableTitle: '本页数据表',
      tableFrom: '数据路径：',
      tableRows: '（仅列前 %d 行，共 %d 行）',
      tableHint: '聚焦图表后按 Enter 可打开本表，Esc 关闭。'
    },
    en: {
      chart: ' (interactive chart).',
      kpi: 'Key statistics: ',
      kpiSep: '; ',
      kpiEnd: '.',
      source: 'See the "Data Source" section below for data provenance and citation format.',
      focus: 'This region is focusable; screen readers can read this alternative text directly.',
      fallbackTitle: 'Chart',
      tableTitle: 'Data table (this page)',
      tableFrom: 'Data path: ',
      tableRows: ' (first %d of %d rows)',
      tableHint: 'Press Enter on a focused chart to open this table; Esc closes it.'
    }
  };
  var T = I18N[LANG];

  function docTitle() {
    // W1348：标题现役形态「专题名：结论 · 详解西游记」⇒ 读屏标签只取专题名
    var t = (document.title || '').split(/[：·|—]/)[0].trim();
    return t || T.fallbackTitle;
  }

  function isTopLevelGraphic(el) {
    // 排除嵌套 svg（图例/坐标标尺常为父 svg 的子元素）
    if (el.tagName === 'SVG' && el.ownerSVGElement) return false;
    if (el.tagName === 'CANVAS' && el.parentElement && el.parentElement.tagName === 'SVG') return false;
    if (el.closest('[class*="tooltip"],.chart-tooltip,#audit-halo,[aria-hidden="true"]')) return false;
    var r = el.getBoundingClientRect();
    return r.width >= MIN_W && r.height >= MIN_H;
  }

  function nearestHeading(el) {
    var node = el;
    for (var depth = 0; depth < 6 && node; depth++) {
      var scope = node.previousElementSibling;
      while (scope) {
        var h = scope.matches && scope.matches('h1,h2,h3,h4')
          ? scope
          : (scope.querySelector ? scope.querySelector(':scope > h1,:scope > h2,:scope > h3,:scope > h4') : null);
        if (h && h.textContent.trim()) return h.textContent.trim();
        scope = scope.previousElementSibling;
      }
      node = node.parentElement;
    }
    return '';
  }

  function chartLabel(el) {
    return nearestHeading(el) || docTitle();
  }

  function kpiDigest() {
    var nodes = document.querySelectorAll('.kpi-card,.stat-card,[class*="kpi"]');
    var out = [];
    for (var i = 0; i < nodes.length && out.length < 6; i++) {
      var txt = (nodes[i].textContent || '').replace(/\s+/g, ' ').trim();
      if (txt && txt.length <= 60 && out.indexOf(txt) === -1) out.push(txt);
    }
    return out;
  }

  function buildSummary(label, idx) {
    var div = document.createElement('div');
    div.id = 'chart-a11y-summary-' + idx;
    div.className = 'sr-only';
    div.style.cssText = SR_STYLE;
    div.setAttribute('role', 'note');
    var parts = [label + T.chart];
    var kpis = kpiDigest();
    if (kpis.length) parts.push(T.kpi + kpis.join(T.kpiSep) + T.kpiEnd);
    if (document.getElementById('dataSource')) {
      parts.push(T.source);
    }
    parts.push(T.focus);
    div.textContent = parts.join(' ');
    return div;
  }

  // ---- W1356（批 B）：键盘可达路径 + 数据表 fallback（零页面静态改动·全部运行时注入） ----
  var TABLE_MAX_ROWS = 50;
  var TABLE_MAX_COLS = 6;

  function injectStyle() {
    if (document.getElementById('chart-a11y-style')) return;
    var st = document.createElement('style');
    st.id = 'chart-a11y-style';
    st.textContent =
      '[data-chart-a11y]:focus-visible{outline:2px solid var(--accent-primary,#C0392B);outline-offset:2px}' +
      '.chart-a11y-data{margin:18px 0;padding:14px 16px;border:1px solid var(--border-subtle,#DCD3BF);' +
      'border-radius:6px;background:var(--surface-raised,#FCFAF4);font-size:.86rem}' +
      '.chart-a11y-data summary{cursor:pointer;font-weight:600;color:var(--text-primary,#1C1A17)}' +
      '.chart-a11y-data figcaption{margin:6px 0 8px;color:var(--text-tertiary,#6B665C);font-size:.78rem}' +
      '.chart-a11y-data .wrap{max-height:320px;overflow:auto}' +
      '.chart-a11y-data table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}' +
      '.chart-a11y-data th,.chart-a11y-data td{border:1px solid var(--border-subtle,#DCD3BF);padding:4px 8px;text-align:left}' +
      '.chart-a11y-data th{background:var(--surface-sunken,#EDE7D6)}';
    document.head.appendChild(st);
  }

  function isObjArray(a) {
    return Array.isArray(a) && a.length >= 2 && a[0] && typeof a[0] === 'object' && !Array.isArray(a[0]);
  }

  function findArray(node, path, depth) {
    if (!node || typeof node !== 'object' || depth > 3) return null;
    var keys = Object.keys(node);
    for (var i = 0; i < keys.length; i++) {
      if (isObjArray(node[keys[i]])) return { path: path + '.' + keys[i], arr: node[keys[i]] };
    }
    for (var j = 0; j < keys.length; j++) {
      var w = node[keys[j]];
      if (w && typeof w === 'object' && !Array.isArray(w)) {
        var sub = findArray(w, path + '.' + keys[j], depth + 1);
        if (sub) return sub;
      }
    }
    return null;
  }

  function dataSource() {
    // 注意：页面多以 `const EMBEDDED_DATA = {...}` 在经典脚本顶层声明 —— 那是**全局词法环境**
    // 的绑定，不是 window 属性（window.EMBEDDED_DATA 恒 undefined）。故须以裸标识符取值，
    // 并对未声明标识符用 typeof 守卫（typeof 对未声明名不抛）。
    var roots = [];
    try { if (typeof __lastData !== 'undefined' && __lastData) roots.push(['window.__lastData', __lastData]); } catch (e1) { /* fail-open */ }
    try { if (window.__lastData) roots.push(['window.__lastData', window.__lastData]); } catch (e2) { /* fail-open */ }
    try { if (typeof EMBEDDED_DATA !== 'undefined' && EMBEDDED_DATA) roots.push(['EMBEDDED_DATA', EMBEDDED_DATA]); } catch (e3) { /* fail-open */ }
    try { if (window.EMBEDDED_DATA) roots.push(['window.EMBEDDED_DATA', window.EMBEDDED_DATA]); } catch (e4) { /* fail-open */ }
    for (var i = 0; i < roots.length; i++) {
      if (roots[i][1] && typeof roots[i][1] === 'object') {
        var hit = findArray(roots[i][1], roots[i][0], 0);
        if (hit) return hit;
      }
    }
    return null;
  }

  function buildDataTable() {
    if (document.getElementById('chart-a11y-data')) return;
    var src = dataSource();
    if (!src) return;
    var arr = src.arr;
    var cols = Object.keys(arr[0] || {}).filter(function (k) {
      var v = arr[0][k];
      return v === null || typeof v !== 'object';
    }).slice(0, TABLE_MAX_COLS);
    if (!cols.length) return;

    var d = document.createElement('details');
    d.id = 'chart-a11y-data';
    d.className = 'chart-a11y-data';
    var s = document.createElement('summary');
    s.textContent = T.tableTitle;
    d.appendChild(s);

    var cap = document.createElement('figcaption');
    cap.textContent = T.tableFrom + src.path + (arr.length > TABLE_MAX_ROWS
      ? T.tableRows.replace('%d', TABLE_MAX_ROWS).replace('%d', arr.length) : '') + ' ' + T.tableHint;
    d.appendChild(cap);

    var wrap = document.createElement('div');
    wrap.className = 'wrap';
    var tb = document.createElement('table');
    var thead = document.createElement('thead');
    var trh = document.createElement('tr');
    for (var c = 0; c < cols.length; c++) {
      var th = document.createElement('th');
      th.scope = 'col';
      th.textContent = cols[c];
      trh.appendChild(th);
    }
    thead.appendChild(trh);
    tb.appendChild(thead);
    var tbody = document.createElement('tbody');
    for (var r = 0; r < Math.min(arr.length, TABLE_MAX_ROWS); r++) {
      var tr = document.createElement('tr');
      for (var c2 = 0; c2 < cols.length; c2++) {
        var td = document.createElement('td');
        var v = arr[r][cols[c2]];
        td.textContent = v === undefined || v === null ? '' : String(v);
        tr.appendChild(td);
      }
      tbody.appendChild(tr);
    }
    tb.appendChild(tbody);
    wrap.appendChild(tb);
    d.appendChild(wrap);

    var host = document.getElementById('dataSource');
    if (host && host.parentNode) host.parentNode.insertBefore(d, host);
    else document.body.appendChild(d);
  }

  function chartList() {
    return Array.prototype.slice.call(document.querySelectorAll('[data-chart-a11y]'));
  }

  function bindKeyboard(el) {
    if (el.__a11yKeys) return;
    el.__a11yKeys = true;
    el.addEventListener('keydown', function (e) {
      var list = chartList();
      var i = list.indexOf(el);
      var d = document.getElementById('chart-a11y-data');
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        if (!list.length) return;
        e.preventDefault();
        list[(i + 1) % list.length].focus();
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        if (!list.length) return;
        e.preventDefault();
        list[(i - 1 + list.length) % list.length].focus();
      } else if (e.key === 'Enter' || e.key === ' ') {
        if (!d) return;
        e.preventDefault();
        d.open = true;
        var sum = d.querySelector('summary');
        if (sum) sum.focus();
      } else if (e.key === 'Escape') {
        if (d && d.open) {
          d.open = false;
          el.focus();
        }
      }
    });
  }

  function apply() {
    var cands = [];
    var all = document.querySelectorAll('svg,canvas');
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      if (el.hasAttribute('data-chart-a11y')) continue;
      if (!isTopLevelGraphic(el)) continue;
      var r = el.getBoundingClientRect();
      cands.push({ el: el, area: r.width * r.height });
    }
    if (!cands.length) return false;
    cands.sort(function (a, b) { return b.area - a.area; });
    var pick = cands.slice(0, MAX_CHARTS);
    for (var j = 0; j < pick.length; j++) {
      var el2 = pick[j].el;
      var idx = ++appliedCount;
      var label = chartLabel(el2).slice(0, 80);
      var summary = buildSummary(label, idx);
      document.body.appendChild(summary);
      el2.setAttribute('data-chart-a11y', String(idx));
      el2.setAttribute('tabindex', '0');
      el2.setAttribute('role', 'img');
      el2.setAttribute('aria-label', label);
      el2.setAttribute('aria-describedby', summary.id);
      bindKeyboard(el2);
    }
    return true;
  }

  function start() {
    injectStyle();
    apply();
    buildDataTable();
    var stopAt = Date.now() + OBSERVE_MS;
    var pending = null;
    var mo = new MutationObserver(function () {
      if (Date.now() > stopAt) { mo.disconnect(); return; }
      if (pending) clearTimeout(pending);
      pending = setTimeout(function () {
        var added = apply();
        buildDataTable();
        if (!added) mo.disconnect();
      }, 300);
    });
    mo.observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
