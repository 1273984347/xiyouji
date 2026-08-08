// visit-log.js — 本地访问记录（W403 · 零注册零依赖基线）
//
// 在页面加载时把一次访问（时间戳/路径/来源/UA 摘要）写入 localStorage：
//   localStorage["visit_log"] = [{t, p, r, u}, ...]  （上限 500 条，FIFO）
//
// 限制（诚实声明）：localStorage 仅本浏览器可见——只能统计"你本地打开过哪些页面"，
// 无法统计真实读者。外部统计（GoatCounter/Umami Cloud）接入后此文件可弃用，
// 升级路径见 scripts/inject_goatcounter.py。
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
