// 阅读页增强（W847）：阅读进度记忆 · 书签 · 字号调节 · 顶部进度条。
// 纯 localStorage 三键（reader.progress / reader.bookmark / reader.fontsize），零外域请求，
// file:// 双击直开可用；localStorage 不可用（隐私模式/沙箱）时全部降级为无状态，不抛错（fail-open）。
// 页面标识取生成器写入的 data-page（形如 reader/ch008.html），不用 location.pathname——
// 后者在 file:// 与 http:// 下形态不同，会让同一页的进度在两种打开方式间互不认。
(function () {
  'use strict';

  var KEY_PROGRESS = 'reader.progress';
  var KEY_BOOKMARK = 'reader.bookmark';
  var KEY_FONT = 'reader.fontsize';
  var FONT_MIN = 15;
  var FONT_MAX = 21;
  var FONT_DEFAULT = 17;

  var tools = document.querySelector('[data-reader-tools]');
  var bar = document.querySelector('[data-reader-progress]');
  var article = document.querySelector('.reader-body');
  var page = tools ? (tools.getAttribute('data-page') || '') : '';
  var statusEl = tools ? tools.querySelector('[data-role="status"]') : null;
  var markBtn = tools ? tools.querySelector('[data-act="bookmark"]') : null;
  var minusBtn = tools ? tools.querySelector('[data-act="font-minus"]') : null;
  var plusBtn = tools ? tools.querySelector('[data-act="font-plus"]') : null;

  var ls = null;
  try { ls = window.localStorage; } catch (e) { ls = null; }

  function getJSON(key, dflt) {
    if (!ls) return dflt;
    try {
      var raw = ls.getItem(key);
      if (!raw) return dflt;
      var v = JSON.parse(raw);
      return (v === null || typeof v === 'undefined') ? dflt : v;
    } catch (e) { return dflt; }
  }

  function setJSON(key, val) {
    if (!ls) return;
    try { ls.setItem(key, JSON.stringify(val)); } catch (e) {}
  }

  function getInt(key, dflt) {
    if (!ls) return dflt;
    try {
      var v = parseInt(ls.getItem(key), 10);
      return isFinite(v) ? v : dflt;
    } catch (e) { return dflt; }
  }

  function flash(msg) {
    if (!statusEl) return;
    statusEl.textContent = msg;
    window.setTimeout(function () {
      if (statusEl.textContent === msg) statusEl.textContent = '';
    }, 1800);
  }

  // —— 字号：写 inline style（CSP 已许可 style-src 'unsafe-inline'） ——
  var font = getInt(KEY_FONT, FONT_DEFAULT);
  if (font < FONT_MIN || font > FONT_MAX) font = FONT_DEFAULT;

  function applyFont(px, persist) {
    font = Math.min(FONT_MAX, Math.max(FONT_MIN, px));
    if (article) article.style.fontSize = font + 'px';
    if (persist && ls) { try { ls.setItem(KEY_FONT, String(font)); } catch (e) {} }
  }

  applyFont(font, false);

  if (minusBtn) {
    minusBtn.addEventListener('click', function () {
      applyFont(font - 1, true);
      flash('字号 ' + font + 'px');
    });
  }
  if (plusBtn) {
    plusBtn.addEventListener('click', function () {
      applyFont(font + 1, true);
      flash('字号 ' + font + 'px');
    });
  }

  // —— 全部折叠段展开/收起（速览 ↔ 深读一键切换） ——
  var allBtn = tools ? tools.querySelector('[data-act="toggle-all"]') : null;
  var folds = document.querySelectorAll('details.reader-fold');

  function anyClosed() {
    for (var i = 0; i < folds.length; i++) {
      if (!folds[i].open) return true;
    }
    return false;
  }

  function renderAllBtn() {
    if (!allBtn) return;
    allBtn.textContent = anyClosed() ? '展开全部' : '收起全部';
  }

  if (allBtn && folds.length) {
    allBtn.addEventListener('click', function () {
      var open = anyClosed();
      for (var i = 0; i < folds.length; i++) folds[i].open = open;
      renderAllBtn();
      paint();
    });
    for (var k = 0; k < folds.length; k++) {
      folds[k].addEventListener('toggle', renderAllBtn);
    }
    renderAllBtn();
  }

  // —— 书签 ——
  var marks = getJSON(KEY_BOOKMARK, []);
  if (!(marks instanceof Array)) marks = [];

  function isMarked() {
    for (var i = 0; i < marks.length; i++) {
      if (marks[i] === page) return true;
    }
    return false;
  }

  function renderMark() {
    if (!markBtn) return;
    var on = isMarked();
    markBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
    markBtn.textContent = on ? '★ 已收藏' : '☆ 收藏本页';
  }

  renderMark();

  if (markBtn) {
    markBtn.addEventListener('click', function () {
      var idx = -1;
      for (var i = 0; i < marks.length; i++) {
        if (marks[i] === page) { idx = i; break; }
      }
      if (idx >= 0) {
        marks.splice(idx, 1);
        flash('已取消收藏');
      } else {
        marks.push(page);
        flash('已收藏');
      }
      setJSON(KEY_BOOKMARK, marks);
      renderMark();
    });
  }

  // —— 进度：滚动百分比存 map，跨页/跨会话保持 ——
  var progress = getJSON(KEY_PROGRESS, {});
  if (!progress || typeof progress !== 'object' || progress instanceof Array) progress = {};

  function scrollSpan() {
    var doc = document.documentElement;
    var h = Math.max(doc.scrollHeight, document.body ? document.body.scrollHeight : 0);
    var vh = window.innerHeight || doc.clientHeight || 0;
    return h - vh;
  }

  function ratio() {
    var span = scrollSpan();
    if (span <= 0) return 0;
    var y = window.pageYOffset || document.documentElement.scrollTop || 0;
    return Math.min(1, Math.max(0, y / span));
  }

  function paint() {
    if (bar) bar.style.width = (ratio() * 100).toFixed(2) + '%';
  }

  var timer = null;

  function saveSoon() {
    if (timer) window.clearTimeout(timer);
    timer = window.setTimeout(function () {
      if (!page) return;
      progress[page] = Math.round(ratio() * 1000) / 1000;
      setJSON(KEY_PROGRESS, progress);
    }, 400);
  }

  try {
    window.addEventListener('scroll', function () { paint(); saveSoon(); }, { passive: true });
  } catch (e) {
    window.addEventListener('scroll', function () { paint(); saveSoon(); });
  }

  function restore() {
    if (!page || location.hash) return;
    var r = progress[page];
    if (typeof r !== 'number' || r < 0.02 || r > 0.98) return;
    var span = scrollSpan();
    if (span <= 0) return;
    window.scrollTo(0, Math.round(span * r));
  }

  if (document.readyState === 'complete') {
    restore();
    paint();
  } else {
    window.addEventListener('load', function () { restore(); paint(); });
  }
})();
