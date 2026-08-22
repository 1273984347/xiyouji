// 夜读模式（W489）：全站 theme 初始化——先读 localStorage，无则跟随系统；body 渲染前挂 html[data-theme] 防 FOUC。
// 同步加载（head 内非 defer）；禁 JS 或异常时保持浅色（fail-open）。
(function () {
  var t = null;
  try { t = localStorage.getItem('xy-theme'); } catch (_) {}
  if (t !== 'light' && t !== 'dark') {
    try { t = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'; } catch (_) { t = 'light'; }
  }
  if (t === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
})();
