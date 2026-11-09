/*
 * stats.js — 全站统计事件桥（W1168·GoatCounter 单轨唯一写入口）
 *
 * 为什么要有这一层（而不是各页各脚本直接调 goatcounter.count）：
 *   ① 加载时序：goatcounter.js 是 async，早期事件（首屏曝光、启动错误）若直接调用会在
 *      库未就绪时静默丢失 ⇒ 桥负责「未就绪先入队，load 时冲刷」；
 *   ② 离线静默：goatcounter 自身在 file:// 与 localhost 下会 console.warn「not counting」，
 *      859 页 × 每页若干事件 = 持续噪声，而 H3 健康监控盯的正是 console ⇒ 桥直接短路，
 *      既不发也不 warn；
 *   ③ 单写入口：事件名只从这一层与分发正本出去，第 67 槽 check_stat_events.py 才能对
 *      「清单 ↔ 落点」做穷举对拍（散落直调会让清单永远缺项而无人知）。
 *
 * 契约：
 *   window.XYstats.count(name, value)   上报一个事件（name 必须登记于
 *                                       scripts/output/_w1168_stat_events.json）
 *   window.XYstats.observeViews()       对 [data-goatcounter-view] 做一次性曝光上报
 *   window error / unhandledrejection   自动上报 debug_error（全站覆盖，不必改各消费脚本）
 *
 * 失败面：本文件是**增强**，任何异常都不得冒泡影响页面功能（file:// 铁律与页面渲染零依赖
 * 统计的承诺）⇒ 全程 try/catch 静默，不 throw、不外抛。
 */
(function (w) {
  'use strict';
  if (w.XYstats) { return; }

  var queue = [];
  var LOCAL_RE = /^(localhost$|^127\.|^10\.|^172\.(1[6-9]|2[0-9]|3[01])\.|^192\.168\.|^0\.0\.0\.0$)/;

  function silenced() {
    try {
      var loc = w.location || {};
      if (loc.protocol === 'file:') { return true; }
      return LOCAL_RE.test(loc.hostname || '');
    } catch (e) { return true; }
  }

  function emit(name, value) {
    var gc = w.goatcounter;
    if (!gc || typeof gc.count !== 'function') {
      if (queue.length < 50) { queue.push([name, value]); }
      return;
    }
    gc.count({ event: true, path: name, title: (value === undefined || value === null) ? '' : String(value) });
  }

  function flush() {
    var pending = queue;
    queue = [];
    for (var i = 0; i < pending.length; i++) {
      try { emit(pending[i][0], pending[i][1]); } catch (e) { /* 增强面：静默 */ }
    }
  }

  var api = {
    count: function (name, value) {
      try {
        if (!name || silenced()) { return; }
        emit(String(name), value);
      } catch (e) { /* 增强面：静默 */ }
    },
    observeViews: function () {
      try {
        if (!w.IntersectionObserver || !w.document || !w.document.querySelectorAll) { return; }
        var els = w.document.querySelectorAll('[data-goatcounter-view]');
        var io = new w.IntersectionObserver(function (entries, obs) {
          for (var i = 0; i < entries.length; i++) {
            var el = entries[i].target;
            if (!entries[i].isIntersecting) { continue; }
            if (el.dataset && el.dataset.goatcounterBoundView) { continue; }
            if (el.dataset) { el.dataset.goatcounterBoundView = '1'; }
            // 名字取自 dataset——与 goatcounter.js 自身的 elem.dataset.goatcounterClick 同约定，
            // 也避免同一属性在 getAttribute / dataset 两种读法间分叉
            api.count((el.dataset && el.dataset.goatcounterView) || '', '');
            obs.unobserve(el);
          }
        });
        for (var j = 0; j < els.length; j++) { io.observe(els[j]); }
      } catch (e) { /* 增强面：静默 */ }
    }
  };

  w.XYstats = api;
  w.addEventListener('load', function () {
    flush();
    // 曝光观察器自动挂载：徽标等声明式元素无需各页自己调用（分发正本只加属性即可）
    try { api.observeViews(); } catch (e) { /* 增强面：静默 */ }
  });
  w.addEventListener('error', function (ev) {
    api.count('debug_error', (ev && (ev.message || ev.type)) || 'error');
  });
  w.addEventListener('unhandledrejection', function () { api.count('debug_error', 'rejection'); });
})(window);
