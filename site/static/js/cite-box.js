/*!
 * cite-box.js — 可引用性组件交互模块（B-6 第二步 · W657）
 *
 * 职责：为页面静态 cite-block（由 _w657_cite_inject.py 注入）绑定「复制」按钮。
 * 复制：navigator.clipboard 优先，file:// 降级 execCommand；成功后按钮显示对勾并在 2.5s 后还原。
 *
 * 样式归属（W1165 变更）：本模块原以字符串数组声明全部 .cite-* 样式并在 init() 里建 <style> 注入 head。
 *   该设计把表现层寄生于脚本——未引用本脚本但含 cite 结构的页面（如 wukong-tangseng-benchmark）
 *   结构在而样式缺，复制按钮回落浏览器默认 31×21。W1165 已将样式整体迁至 site/system.css
 *   「可引用性组件（cite）」段，本模块只保留交互职责。
 *
 * 挂载：<script defer src="../static/js/cite-box.js"></script>——DOMContentLoaded 委托绑定，
 *       无需配置（.cite-block 存在即生效，不存在的页面零开销）。
 */
(function () {
  'use strict';

  function copyText(text, btn) {
    var done = function () {
      var old = btn.textContent;
      // W1134: 文案改为对勾（✓）·2.5s 后由 CSS 动画淡出并在此刻还原文案
      btn.textContent = '✓';
      btn.classList.remove('ok');
      // 强制重排以便连续复制时重新触发淡出动画
      void btn.offsetWidth;
      btn.classList.add('ok');
      setTimeout(function () { btn.textContent = old; btn.classList.remove('ok'); }, 2500);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { legacy(); });
    } else {
      legacy();
    }
    function legacy() {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); done(); } catch (e) { /* noop */ }
      document.body.removeChild(ta);
    }
  }

  function bind(root) {
    root.addEventListener('click', function (ev) {
      var btn = ev.target.closest ? ev.target.closest('.cite-copy') : null;
      if (!btn || !root.contains(btn)) return;
      var item = btn.closest('.cite-item');
      var pre = item ? item.querySelector('pre.cite-text') : null;
      if (pre) copyText(pre.textContent, btn);
    });
  }

  function init() {
    var box = document.querySelector('.cite-block');
    if (!box) return; /* 无组件页零开销 */
    bind(box);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
