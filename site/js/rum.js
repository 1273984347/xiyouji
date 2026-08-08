/*!
 * W267 v2.2.47 · E6 性能监控深化 · RUM 真实用户监控采集脚本
 *
 * 采集浏览器端 5 项 Core Web Vitals 指标并上报至 /api/rum：
 *   - LCP  Largest Contentful Paint  （≤2.5s 优良）
 *   - CLS  Cumulative Layout Shift   （≤0.1 优良）
 *   - INP  Interaction to Next Paint （≤200ms 优良）
 *   - TBT  Total Blocking Time       （≤200ms 优良，由 long-task 估算）
 *   - FCP  First Contentful Paint    （≤1.8s 优良）
 *
 * 数据格式（POST /api/rum，application/json）：
 *   {
 *     "page": "index.html",
 *     "ts": 1719000000000,
 *     "metrics": {"lcp": 1.2, "cls": 0.05, "inp": 0.15, "tbt": 0.2, "fcp": 0.8},
 *     "nav": "navigate",
 *     "ua": "Mozilla/5.0 ..."
 *   }
 *
 * 特性：
 *   - 使用 PerformanceObserver API（降级兼容老版本浏览器）
 *   - 采样率控制（RUM_SAMPLE_RATE，默认 1.0 = 100%）
 *   - 页面隐藏时（visibilitychange）统一上报，避免 unload 不可靠
 *   - 全程 try/catch 错误处理，永不抛出影响业务
 *   - 单例模式，防止重复初始化
 *
 * 用法：在 HTML <head> 末尾引入（路径相对站点根，子路径部署也安全）：
 *       <script defer src="js/rum.js"></script>            （站点根页）
 *       <script defer src="../js/rum.js"></script>         （data/ en/ 等子目录页）
 *       可通过 window.__RUM_CONFIG__ 覆盖默认配置。
 * 注意：GitHub Pages 无后端，/api/rum 会 404；开启 storeLocal 后数据
 *       落 localStorage（rum_queue），可用于本地验证，未来接后端改 endpoint 即回流。
 */
(function (window, document) {
  'use strict';

  if (window.__RUM_INITIALIZED__) {
    return; // 单例：防止重复初始化
  }
  window.__RUM_INITIALIZED__ = true;

  // ---------------------------------------------------------------------------
  // 配置（允许 window.__RUM_CONFIG__ 覆盖）
  // ---------------------------------------------------------------------------
  var DEFAULT_CONFIG = {
    endpoint: '/api/rum',          // 上报地址（GitHub Pages 无后端，会 404）
    sampleRate: 1.0,               // 采样率 0~1（默认 100%）
    enableTBT: true,               // 是否采集 TBT（long-task）
    sendOnHidden: true,            // 页面隐藏时上报
    sendTimeoutMs: 4000,           // 最长等待上报窗口
    storeLocal: true,              // 本地备援：写入 localStorage 环形队列（rum_queue）
    localMax: 50,                  // 本地队列最大条数
    debug: false                   // 调试模式：输出 console 日志
  };
  var config = mergeConfig(DEFAULT_CONFIG, window.__RUM_CONFIG__ || {});

  // ---------------------------------------------------------------------------
  // 采样判定：未命中采样直接退出
  // ---------------------------------------------------------------------------
  if (Math.random() > config.sampleRate) {
    if (config.debug) {
      console.warn('[RUM] 未命中采样，跳过采集');
    }
    return;
  }

  // ---------------------------------------------------------------------------
  // 指标缓存
  // ---------------------------------------------------------------------------
  var metrics = {
    lcp: null,
    cls: 0,          // CLS 累计值
    inp: null,       // 最大 INP
    tbt: 0,          // TBT 累计值（ms）
    fcp: null
  };
  var clsSession = { value: 0, hadInput: false };
  var inpEntries = [];
  var observers = [];
  var reported = false;

  // ---------------------------------------------------------------------------
  // 工具：合并配置
  // ---------------------------------------------------------------------------
  function mergeConfig(base, override) {
    var result = {};
    for (var k in base) {
      if (Object.prototype.hasOwnProperty.call(base, k)) {
        result[k] = base[k];
      }
    }
    for (var j in override) {
      if (Object.prototype.hasOwnProperty.call(override, j)) {
        result[j] = override[j];
      }
    }
    return result;
  }

  // ---------------------------------------------------------------------------
  // 工具：安全 PerformanceObserver 注册
  // ---------------------------------------------------------------------------
  function safeObserve(type, callback, opts) {
    if (!window.PerformanceObserver) {
      return false;
    }
    try {
      var entryTypes = opts && opts.buffered !== false;
      var observer = new PerformanceObserver(function (list) {
        try {
          callback(list);
        } catch (e) {
          if (config.debug) {
            console.warn('[RUM] observer callback error:', e);
          }
        }
      });
      observer.observe({ type: type, buffered: entryTypes });
      observers.push(observer);
      return true;
    } catch (e) {
      // 某些 entryType 老浏览器不支持，降级跳过
      if (config.debug) {
        console.warn('[RUM] observe failed for', type, e);
      }
      return false;
    }
  }

  // ---------------------------------------------------------------------------
  // 1. LCP - Largest Contentful Paint
  // ---------------------------------------------------------------------------
  safeObserve('largest-contentful-paint', function (list) {
    var entries = list.getEntries();
    for (var i = 0; i < entries.length; i++) {
      // 取最后一个 LCP 候选（最终的 LCP）
      metrics.lcp = entries[i].startTime;
    }
  });

  // ---------------------------------------------------------------------------
  // 2. CLS - Cumulative Layout Shift（会话窗口法，5.0 实现）
  // ---------------------------------------------------------------------------
  safeObserve('layout-shift', function (list) {
    var entries = list.getEntries();
    for (var i = 0; i < entries.length; i++) {
      var entry = entries[i];
      // 用户输入后不再累计 CLS（标准做法）
      if (!entry.hadRecentInput) {
        clsSession.value += entry.value;
        metrics.cls = clsSession.value;
      }
    }
  });

  // ---------------------------------------------------------------------------
  // 3. INP - Interaction to Next Paint（取所有交互的最大 duration）
  // ---------------------------------------------------------------------------
  safeObserve('event', function (list) {
    var entries = list.getEntries();
    for (var i = 0; i < entries.length; i++) {
      var entry = entries[i];
      if (entry.interactionId && entry.duration) {
        inpEntries.push(entry.duration);
        if (metrics.inp === null || entry.duration > metrics.inp) {
          metrics.inp = entry.duration;
        }
      }
    }
  });

  // ---------------------------------------------------------------------------
  // 4. TBT - Total Blocking Time（由 long-task 估算：sum(duration > 50ms 的部分)）
  // ---------------------------------------------------------------------------
  if (config.enableTBT) {
    safeObserve('longtask', function (list) {
      var entries = list.getEntries();
      for (var i = 0; i < entries.length; i++) {
        var entry = entries[i];
        if (entry.duration > 50) {
          // long-task duration 已是 ms；blocking time = duration - 50
          metrics.tbt += (entry.duration - 50);
        }
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 5. FCP - First Contentful Paint（从 paint entries 提取）
  // ---------------------------------------------------------------------------
  safeObserve('paint', function (list) {
    var entries = list.getEntries();
    for (var i = 0; i < entries.length; i++) {
      if (entries[i].name === 'first-contentful-paint') {
        metrics.fcp = entries[i].startTime;
      }
    }
  });

  // 降级：若 PerformanceObserver 不支持 paint，尝试 performance.timing
  if (metrics.fcp === null && window.performance && performance.timing) {
    try {
      var t = performance.timing;
      // navigationStart 已废弃但仍可用作降级
      var navStart = t.navigationStart || 0;
      // msFirstPaint 是 IE/Edge 私有，Chrome 不支持
      if (t.msFirstPaint) {
        metrics.fcp = t.msFirstPaint - navStart;
      }
    } catch (e) {
      // ignore
    }
  }

  // ---------------------------------------------------------------------------
  // 上报逻辑
  // ---------------------------------------------------------------------------
  function buildPayload() {
    var navEntry = (performance && performance.getEntriesByType)
      ? performance.getEntriesByType('navigation')[0]
      : null;
    var navType = navEntry ? navEntry.type : 'navigate';
    return {
      page: getPageName(),
      ts: Date.now(),
      metrics: {
        lcp: round(metrics.lcp !== null ? metrics.lcp / 1000 : null, 4),
        cls: round(metrics.cls, 5),
        inp: round(metrics.inp !== null ? metrics.inp / 1000 : null, 4),
        tbt: round(metrics.tbt / 1000, 4),
        fcp: round(metrics.fcp !== null ? metrics.fcp / 1000 : null, 4)
      },
      nav: navType,
      ua: navigator.userAgent || ''
    };
  }

  function getPageName() {
    try {
      var path = location.pathname || '/';
      // 取最后一段作为页面名，根目录用 index.html
      var parts = path.split('/').filter(Boolean);
      if (parts.length === 0) {
        return 'index.html';
      }
      var last = parts[parts.length - 1];
      return last.indexOf('.') > 0 ? last : last + '.html';
    } catch (e) {
      return 'unknown';
    }
  }

  function round(v, digits) {
    if (v === null || v === undefined || isNaN(v)) {
      return null;
    }
    var p = Math.pow(10, digits);
    return Math.round(v * p) / p;
  }

  // ---------------------------------------------------------------------------
  // 本地备援：GitHub Pages 无后端，/api/rum 会 404，先把数据落 localStorage
  // 环形队列（rum_queue），未来接真实后端改 endpoint 即可回流，不丢数据。
  // ---------------------------------------------------------------------------
  function storeLocal(payload) {
    if (!config.storeLocal || !window.localStorage) {
      return;
    }
    try {
      var key = 'rum_queue';
      var queue;
      try {
        queue = JSON.parse(window.localStorage.getItem(key)) || [];
      } catch (e) {
        queue = [];
      }
      if (!Array.isArray(queue)) {
        queue = [];
      }
      queue.push({ ts: Date.now(), payload: payload });
      // 超出上限则丢弃最旧记录（环形）
      if (queue.length > config.localMax) {
        queue = queue.slice(queue.length - config.localMax);
      }
      window.localStorage.setItem(key, JSON.stringify(queue));
      if (config.debug) {
        console.log('[RUM] stored locally, queue size =', queue.length);
      }
    } catch (e) {
      // 隐私模式 / 配额超限：静默降级，不影响业务
    }
  }

  function sendPayload(payload) {
    if (reported) {
      return;
    }
    reported = true;

    // 1) 本地备援优先（即使上报失败也不丢数据）
    storeLocal(payload);

    if (config.debug) {
      console.log('[RUM] send payload:', payload);
    }

    var body = JSON.stringify(payload);
    // 优先 navigator.sendBeacon（页面卸载时更可靠）
    if (navigator.sendBeacon && config.endpoint) {
      try {
        var blob = new Blob([body], { type: 'application/json' });
        if (navigator.sendBeacon(config.endpoint, blob)) {
          return;
        }
      } catch (e) {
        // sendBeacon 失败则降级 fetch
      }
    }
    // 降级 fetch（keepalive）
    if (window.fetch) {
      try {
        fetch(config.endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: body,
          keepalive: true,
          credentials: 'same-origin'
        }).catch(function () { /* 静默失败 */ });
      } catch (e) {
        // ignore
      }
    } else if (window.XMLHttpRequest) {
      // 最终降级 XHR
      try {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', config.endpoint, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(body);
      } catch (e) {
        // ignore
      }
    }
  }

  function flush() {
    try {
      sendPayload(buildPayload());
    } catch (e) {
      if (config.debug) {
        console.warn('[RUM] flush error:', e);
      }
    }
  }

  // ---------------------------------------------------------------------------
  // 触发上报：页面隐藏 或 超时窗口
  // ---------------------------------------------------------------------------
  if (config.sendOnHidden && document.addEventListener) {
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'hidden') {
        flush();
      }
    });
  }

  // 兜底超时上报（避免长时间不 hidden 导致数据丢失）
  setTimeout(flush, config.sendTimeoutMs);

  // 暴露调试接口（只读 + 本地队列查看/清空）
  window.__RUM__ = {
    config: config,
    getMetrics: function () {
      return JSON.parse(JSON.stringify(metrics));
    },
    flush: flush,
    getLocalQueue: function () {
      try {
        return JSON.parse(window.localStorage.getItem('rum_queue')) || [];
      } catch (e) {
        return [];
      }
    },
    clearLocalQueue: function () {
      try {
        window.localStorage.removeItem('rum_queue');
      } catch (e) {
        // ignore
      }
    }
  };

})(window, document);
