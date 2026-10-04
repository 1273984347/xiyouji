/*!
 * chart-audit.js — 图表渲染后标签防重叠与轴修复统一模块（B-9① · W656）
 *
 * 由 85 页重复注入的六族页面级补丁合并（原块 id → 家族键）：
 *   audit-axisfix      → axisfix    底轴刻度旋转 -38°（≥6 刻度·domain 守卫·translate 判底）
 *   audit-axisfix2/3   → axesvar    方差判轴向：水平旋转 -40°/垂直缩 9px+重叠隐藏
 *                                   （两块逐字节同逻辑仅 domain 守卫差·合并为无守卫版=原 axisfix3
 *                                    终态超集·同 800/2600/5000 时序一次执行）
 *   audit-labelavoid-all → avoidall 全 text 重叠隐藏较小者+补 <title>（排除轴/图例/标题类）
 *   audit-axisfix4     → numfix     数值/轴刻度优先重叠隐藏（行/列聚类判轴刻度·title 属性保留）
 *   audit-labelavoid   → netlabels  无类过滤全 text 重叠隐藏（暴露 window.__avoidOverlap 兼容 API）
 *   audit-contentavoid → content    热力列标签旋转 -42° + SKIP 类过滤重叠隐藏
 *
 * 等价性约定：各家族保留原 setTimeout 时序与 DOM 写入语义；svg[data-audit-skip] 豁免统一化
 * 仅应用于隐藏型四族（W553 决议：旋转型 axisfix/axesvar 不识别该属性·维持 W550 已验收外观）。
 *
 * 单一事实源：本文件。页面内联副本由 scripts/output/_w656_replace_audit.py 生成
 * （file:// 直开约束·同 vis-tools.js 先例）——改本文件后重跑该脚本再跑 generate_csp.py。
 */
(function () {
  'use strict';

  function variance(a) {
    var m = a.reduce(function (s, v) { return s + v; }, 0) / a.length;
    return a.reduce(function (s, v) { return s + (v - m) * (v - m); }, 0) / a.length;
  }

  function overlapRatio(a, b) {
    var ix = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
    var iy = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
    var inter = ix * iy;
    if (inter <= 0) return 0;
    var area = Math.min(a.width * a.height, b.width * b.height);
    return area > 0 ? inter / area : 0;
  }

  function skipped(svg) {
    return svg.hasAttribute && svg.hasAttribute('data-audit-skip');
  }

  /* ---- axisfix：底轴刻度旋转 -38° ---- */
  function fixAxes() {
    try {
      var svgs = document.querySelectorAll('svg');
      svgs.forEach(function (svg) {
        var groups = svg.querySelectorAll('g');
        groups.forEach(function (axisG) {
          if (!axisG.querySelector(':scope > .domain')) return;
          var ticks = axisG.querySelectorAll(':scope > g.tick');
          if (ticks.length < 6) return;
          var bottom = false;
          ticks.forEach(function (t) {
            var tr = t.getAttribute('transform') || '';
            var m = tr.match(/translate\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)/);
            if (m && Math.abs(parseFloat(m[2])) < 0.5) bottom = true;
          });
          if (!bottom) return;
          ticks.forEach(function (t) {
            var txt = t.querySelector('text');
            if (!txt) return;
            txt.style.transformBox = 'fill-box';
            txt.style.transformOrigin = 'top center';
            txt.style.transform = 'rotate(-38deg)';
            txt.style.fontSize = '10px';
            txt.style.fontWeight = '500';
          });
        });
      });
    } catch (e) { /* noop */ }
  }

  /* ---- axesvar：方差判轴向（axisfix2/3 合并·无 domain 守卫=原 axisfix3 终态超集） ---- */
  function fixAxesVariance() {
    try {
      document.querySelectorAll('svg').forEach(function (svg) {
        svg.querySelectorAll('g').forEach(function (g) {
          var ticks = [].slice.call(g.querySelectorAll(':scope > g.tick'));
          if (ticks.length < 5) return;
          var xs = [], ys = [];
          ticks.forEach(function (t) {
            var m = (t.getAttribute('transform') || '').match(/translate\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)/);
            if (m) { xs.push(parseFloat(m[1])); ys.push(parseFloat(m[2])); }
          });
          if (xs.length < 3) return;
          var vx = variance(xs), vy = variance(ys);
          if (vx > vy) {
            ticks.forEach(function (t) {
              var tx = t.querySelector('text'); if (!tx) return;
              tx.style.transformBox = 'fill-box';
              tx.style.transformOrigin = 'top center';
              tx.style.transform = 'rotate(-40deg)';
              tx.style.fontSize = '10px';
              tx.style.fontWeight = '500';
            });
          } else {
            var texts = ticks.map(function (t) { return t.querySelector('text'); }).filter(Boolean);
            texts.forEach(function (tx) { tx.style.fontSize = '9px'; });
            var R = texts.map(function (t) { return t.getBoundingClientRect(); });
            for (var i = 0; i < texts.length; i++) {
              for (var j = i + 1; j < texts.length; j++) {
                var a = R[i], b = R[j];
                if (!a.width || !b.width) continue;
                if (overlapRatio(a, b) > 0.5) {
                  var hide = (a.width * a.height <= (b.width * b.height)) ? texts[i] : texts[j];
                  if (hide.style.display !== 'none') hide.style.display = 'none';
                }
              }
            }
          }
        });
      });
    } catch (e) { /* noop */ }
  }

  /* ---- avoidall：全 text 重叠隐藏 + <title> 保留（排除轴/图例/标题类） ---- */
  function avoidAllLabels() {
    try {
      document.querySelectorAll('svg').forEach(function (svg) {
        if (skipped(svg)) return;
        var ts = [].slice.call(svg.querySelectorAll('text')).filter(function (t) {
          if (t.closest && t.closest('.tick, .legend, .axis, .domain, .title, .cell, .tooltip, .axis-label')) return false;
          var r = t.getBoundingClientRect(); return r.width > 0 && r.height > 0;
        });
        var R = ts.map(function (t) { return t.getBoundingClientRect(); });
        for (var i = 0; i < ts.length; i++) {
          for (var j = i + 1; j < ts.length; j++) {
            var a = R[i], b = R[j];
            if (!a.width || !b.width) continue;
            if (overlapRatio(a, b) > 0.5) {
              var hide = (a.width * a.height <= (b.width * b.height)) ? ts[i] : ts[j];
              if (hide.style.display !== 'none') {
                if (!hide.querySelector(':scope > title')) {
                  var ti = document.createElementNS('http://www.w3.org/2000/svg', 'title');
                  ti.textContent = hide.textContent;
                  hide.appendChild(ti);
                }
                hide.style.display = 'none';
              }
            }
          }
        }
      });
    } catch (e) { /* noop */ }
  }

  /* ---- numfix：数值/轴刻度优先重叠隐藏（axisfix4） ---- */
  function fixNumericOverlap() {
    try {
      var NUM = /^(第?\d+回?|\d+(\.\d+)?|\d+%?|W\d+)$/;
      document.querySelectorAll('svg').forEach(function (svg) {
        if (skipped(svg)) return;
        var all = [].slice.call(svg.querySelectorAll('text')).filter(function (t) { var r = t.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
        var nums = all.filter(function (t) { return NUM.test((t.textContent || '').trim()); });
        var axisNum = new Set();
        var rows = {}, cols = {};
        nums.forEach(function (t) { var r = t.getBoundingClientRect(); var y = Math.round(r.top / 8) * 8; rows[y] = rows[y] || []; rows[y].push(t); var x = Math.round(r.left / 8) * 8; cols[x] = cols[x] || []; cols[x].push(t); });
        Object.keys(rows).forEach(function (k) { if (rows[k].length >= 3) rows[k].forEach(function (t) { axisNum.add(t); }); });
        Object.keys(cols).forEach(function (k) { if (cols[k].length >= 3) cols[k].forEach(function (t) { axisNum.add(t); }); });
        axisNum.forEach(function (t) { t.style.fontSize = '9px'; t.style.fontWeight = '500'; });
        for (var i = 0; i < all.length; i++) {
          for (var j = i + 1; j < all.length; j++) {
            var a = all[i], b = all[j];
            var ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
            var inter = ra.width && rb.width ? overlapRatio(ra, rb) : 0;
            if (inter < 0.4) continue;
            var ta = (a.textContent || '').trim(), tb = (b.textContent || '').trim();
            var dup = ta && ta === tb;
            var aAxis = axisNum.has(a), bAxis = axisNum.has(b);
            var aNum = NUM.test(ta), bNum = NUM.test(tb);
            var act = false;
            if (dup) act = true; else if (aAxis || bAxis) act = true; else if (aNum && bNum) act = true;
            if (!act) continue;
            var hide, keep;
            if (dup) { hide = (ta.length <= tb.length) ? a : b; keep = (hide === a) ? b : a; }
            else { hide = (ra.width * ra.height <= rb.width * rb.height) ? a : b; keep = (hide === a) ? b : a; }
            if (hide.style.display !== 'none') {
              hide.setAttribute('data-axisfix4', '1');
              if (!hide.getAttribute('title')) hide.setAttribute('title', (hide.textContent || '').trim());
              hide.style.display = 'none';
            }
          }
        }
      });
    } catch (e) { /* noop */ }
  }

  /* ---- netlabels：无类过滤重叠隐藏（labelavoid·兼容 API） ---- */
  function avoidNetLabels() {
    document.querySelectorAll('svg').forEach(function (svg) {
      if (skipped(svg)) return;
      var ts = [].slice.call(svg.querySelectorAll('text')).filter(function (t) { var r = t.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
      var R = ts.map(function (t) { return t.getBoundingClientRect(); });
      for (var i = 0; i < ts.length; i++) for (var j = i + 1; j < ts.length; j++) {
        var a = R[i], b = R[j];
        if (overlapRatio(a, b) > 0.5) {
          var hide = (a.width * a.height <= (b.width * b.height)) ? ts[i] : ts[j];
          if (hide.style.display !== 'none') hide.style.display = 'none';
        }
      }
    });
  }

  /* ---- content：热力列标签旋转 + SKIP 类过滤重叠隐藏（contentavoid） ---- */
  function fixContentOverlap() {
    try {
      var SKIP = /(tick|legend|title|axis|domain|cell|tooltip|axisfix|dark-halo|subtitle|grid|background|heat-col-label|heat-row-label)/i;
      document.querySelectorAll('svg text.heat-col-label').forEach(function (t) {
        var x = +t.getAttribute('x') || 0, y = +t.getAttribute('y') || 0;
        t.setAttribute('transform', 'rotate(-42 ' + x + ' ' + y + ')');
        t.setAttribute('text-anchor', 'end');
      });
      document.querySelectorAll('svg').forEach(function (svg) {
        if (skipped(svg)) return;
        var texts = [].slice.call(svg.querySelectorAll('text')).filter(function (t) {
          var c = t.getAttribute('class') || '';
          if (SKIP.test(c)) return false;
          var b = t.getBoundingClientRect(); return b.width > 0 && b.height > 0;
        });
        for (var i = 0; i < texts.length; i++) {
          for (var j = i + 1; j < texts.length; j++) {
            var a = texts[i], b = texts[j];
            var ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
            if (overlapRatio(ra, rb) < 0.4) continue;
            var ta = (a.textContent || '').trim(), tb = (b.textContent || '').trim();
            var hide;
            if (ta === tb) { hide = a; }
            else { hide = (ra.width * ra.height <= rb.width * rb.height) ? a : b; }
            if (hide.style.display !== 'none') {
              hide.setAttribute('data-cavoid', '1');
              if (!hide.getAttribute('title')) hide.setAttribute('title', (hide.textContent || '').trim());
              hide.style.display = 'none';
            }
          }
        }
      });
    } catch (e) { /* noop */ }
  }

  var FAMILIES = {
    axisfix:   { fix: fixAxes,            times: [800, 2600] },
    axesvar:   { fix: fixAxesVariance,    times: [800, 2600, 5000] },
    avoidall:  { fix: avoidAllLabels,     times: [1200, 3000, 6000, 9000, 12000] },
    numfix:    { fix: fixNumericOverlap,  times: [800, 2600, 5000, 8000, 11000] },
    netlabels: { fix: function () { try { avoidNetLabels(); } catch (e) { } }, times: [3000, 6000, 9000, 12000] },
    content:   { fix: fixContentOverlap,  times: [800, 2600, 5000, 8000, 11000, 14000] }
  };

  function runFamilies(list) {
    (list || []).forEach(function (key) {
      var f = FAMILIES[key];
      if (!f) return;
      var schedule = function () { f.times.forEach(function (ms) { setTimeout(f.fix, ms); }); };
      if (document.readyState === 'complete') schedule();
      else window.addEventListener('load', schedule);
    });
  }

  window.ChartAudit = { run: runFamilies, families: FAMILIES };

  /* 页面接入：defer src 加载时 currentScript 指向自身——家族集由 data-families 供给
   * （如 data-families="axisfix,axesvar,avoidall,numfix"），无属性则不自动运行。 */
  try {
    if (document.currentScript && document.currentScript.getAttribute('data-families')) {
      runFamilies(document.currentScript.getAttribute('data-families').split(',').filter(Boolean));
    }
  } catch (e) { /* noop */ }

  /* netlabels 兼容 API（原 audit-labelavoid 暴露·现网 0 消费方·保留防外部脚本依赖） */
  window.__avoidOverlap = avoidNetLabels;
})();
