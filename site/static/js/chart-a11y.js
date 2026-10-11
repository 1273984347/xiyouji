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
 *   4) MutationObserver 兜晚渲染图表（d3 fetch/EMBEDDED 异步建图），20s 后停观。
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

  function docTitle() {
    var t = (document.title || '').split(/[·|—]/)[0].trim();
    return t || '数据图表';
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
    var parts = [label + '（交互式图表）。'];
    var kpis = kpiDigest();
    if (kpis.length) parts.push('关键统计：' + kpis.join('；') + '。');
    if (document.getElementById('dataSource')) {
      parts.push('数据来源与引用格式见页面下方「数据源」区块。');
    }
    parts.push('本区块已设为可聚焦，屏幕阅读器可直接朗读本段替代文本。');
    div.textContent = parts.join(' ');
    return div;
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
    }
    return true;
  }

  function start() {
    apply();
    var stopAt = Date.now() + OBSERVE_MS;
    var pending = null;
    var mo = new MutationObserver(function () {
      if (Date.now() > stopAt) { mo.disconnect(); return; }
      if (pending) clearTimeout(pending);
      pending = setTimeout(function () {
        if (!apply()) mo.disconnect();
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
