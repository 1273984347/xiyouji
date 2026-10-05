/*!
 * cite-box.js — 可引用性组件交互模块（B-6 第二步 · W657）
 *
 * 职责：为页面静态 cite-block（由 _w657_cite_inject.py 注入）绑定「复制」按钮与样式。
 * 复制：navigator.clipboard 优先，file:// 降级 execCommand；成功后按钮文案 2s 内反馈。
 * 样式：全部 var(--token)（零裸色·token 覆盖率门禁合规）；样式节点由本模块注入 head
 *       （details 默认收起·视觉零扰动——W550 验收面不变）。
 * 挂载：<script defer src="../static/js/cite-box.js"></script>——DOMContentLoaded 委托绑定，
 *       无需配置（cite-block 存在即生效，不存在的页面零开销）。
 */
(function () {
  'use strict';

  var CSS = [
    '.cite-block{margin:10px 0 0;padding:10px 12px;border:1px solid var(--line);border-radius:var(--radius-md);background:var(--paper-warm);font-size:12px;color:var(--ink-soft);line-height:1.6;}',
    '.cite-block code{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius-sm);padding:1px 5px;font-family:var(--font-mono);font-size:11px;}',
    '.cite-block .cite-details{margin-top:6px;}',
    '.cite-block .cite-details summary{cursor:pointer;color:var(--accent-2);font-weight:500;user-select:none;}',
    '.cite-block .cite-item{display:flex;gap:8px;align-items:flex-start;margin-top:8px;}',
    '.cite-block .cite-item>span{flex:0 0 44px;font-weight:600;color:var(--ink);padding-top:6px;}',
    '.cite-block pre.cite-text{flex:1;margin:0;padding:6px 8px;background:var(--paper);border:1px solid var(--line);border-radius:var(--radius-sm);font-family:var(--font-mono);font-size:11px;white-space:pre-wrap;word-break:break-all;color:var(--ink);}',
    '.cite-block .cite-copy{flex:0 0 auto;padding:4px 10px;border:1px solid var(--line);border-radius:var(--radius-sm);background:var(--paper);color:var(--accent-2);font-size:11px;cursor:pointer;transition:background var(--dur-fast) var(--ease-out-quart),color var(--dur-fast) var(--ease-out-quart);}',
    '.cite-block .cite-copy:hover{background:var(--accent-tint);color:var(--accent);}',
    '.cite-block .cite-copy.ok{color:var(--ok);border-color:var(--ok);}',
    '.cite-block a[href$=".json"]{display:inline-block;margin-top:6px;color:var(--accent-2);}'
  ].join('\n');

  function copyText(text, btn) {
    var done = function () {
      var old = btn.textContent;
      btn.textContent = '已复制';
      btn.classList.add('ok');
      setTimeout(function () { btn.textContent = old; btn.classList.remove('ok'); }, 2000);
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
    var style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);
    bind(box);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
