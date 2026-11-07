// visit-log.js — 本地访问记录（W403 · 零注册零依赖基线）
//
// 在页面加载时把一次访问（时间戳/路径/来源/UA 摘要）写入 localStorage：
//   localStorage["visit_log"] = [{t, p, r, u}, ...]  （上限 500 条，FIFO）
//
// 限制（诚实声明）：localStorage 仅本浏览器可见——只能统计"你本地打开过哪些页面"，
// 无法统计真实读者，故它只是**本地自查面**，不是跨访客统计。
// 跨访客统计沿革：W806 因 GoatCounter 账号失效退役、一度归零；W1167 复验该账号仍在活
// （端点 HTTP 400=缺参，非 404=死号）后按「双轨具名例外」恢复——GoatCounter 自托管脚本
// 作大陆可达面、GA4 gtag 作海外面（Measurement ID 未填前该轨不注入）。
// 注入面见 scripts/w1167_analytics_inject.py，CSP 例外域见 scripts/generate_csp.py
// 的 ANALYTICS_CONNECT_HOSTS；性能与错误类另见 rum.js（window.__RUM_CONFIG__.endpoint）。
//
// 查看：打开 site/visit-viewer.html（读取本 localStorage 展示 + 导出 JSON）。
//
// 用法（注入脚本自动处理，勿手改）：
//   <script defer src="js/visit-log.js"></script>

(function () {
  'use strict';
  var KEY = 'visit_log';
  var MAX = 500;
  try {
    var log = JSON.parse(localStorage.getItem(KEY) || '[]');
    if (!Array.isArray(log)) log = [];
    log.push({
      t: Date.now(),
      p: location.pathname,
      r: document.referrer || '',
      u: (navigator.userAgent || '').slice(0, 80)
    });
    if (log.length > MAX) log = log.slice(-MAX);
    localStorage.setItem(KEY, JSON.stringify(log));
  } catch (e) {
    // 隐私模式或配额满：静默失败，不影响页面
  }
})();
