// 夜读模式（W489/W496）：全站 theme 初始化——先读 localStorage，无则跟随系统；body 渲染前挂 html[data-theme] 防 FOUC。
// 同步加载（head 内非 defer）；禁 JS 或异常时保持浅色（fail-open）。
// W496：无 .theme-toggle 的页面（data/EN 225 页）注入浮动切换钮——深链用户也能切换夜读；
// 根页自有切换器（.theme-toggle）时跳过注入；按钮样式走运行时 <style>（style-src 'unsafe-inline' 已许可）。
(function () {
  var t = null;
  try { t = localStorage.getItem('xy-theme'); } catch (_) {}
  if (t !== 'light' && t !== 'dark') {
    try { t = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'; } catch (_) { t = 'light'; }
  }
  function apply(v) {
    if (v === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
    else document.documentElement.removeAttribute('data-theme');
  }
  apply(t);

  function injectToggle() {
    if (document.querySelector('.theme-toggle') || document.querySelector('.xy-fab-theme')) return;
    var st = document.createElement('style');
    st.textContent =
      '.xy-fab-theme{position:fixed;right:14px;bottom:14px;z-index:40;width:40px;height:40px;' +
      'border-radius:50%;border:1px solid var(--line,rgba(35,32,26,.18));background:var(--paper,#fff);' +
      'color:var(--ink,#23201A);display:flex;align-items:center;justify-content:center;cursor:pointer;' +
      'box-shadow:var(--shadow-2,0 2px 8px rgba(35,32,26,.12));padding:0;}' +
      '.xy-fab-theme svg{width:18px;height:18px;}' +
      '.xy-fab-theme .ic-sun{display:none;}' +
      'html[data-theme="dark"] .xy-fab-theme .ic-sun{display:block;}' +
      'html[data-theme="dark"] .xy-fab-theme .ic-moon{display:none;}';
    document.head.appendChild(st);
    var b = document.createElement('button');
    b.className = 'xy-fab-theme';
    b.type = 'button';
    b.setAttribute('aria-label', '切换夜读模式 / Toggle night mode');
    b.title = '夜读模式';
    b.innerHTML =
      '<svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">' +
      '<path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/></svg>' +
      '<svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">' +
      '<circle cx="12" cy="12" r="4"/>' +
      '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
    b.addEventListener('click', function () {
      var dark = document.documentElement.getAttribute('data-theme') === 'dark';
      var next = dark ? 'light' : 'dark';
      apply(next);
      try { localStorage.setItem('xy-theme', next); } catch (_) {}
    });
    document.body.appendChild(b);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', injectToggle);
  else injectToggle();
})();
