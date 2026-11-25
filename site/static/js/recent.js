/* recent.js — W1330 最近浏览记录（仅 site/data 内容页加载）
 *
 * 职责：把当前页写入 localStorage 的 xy-recent-pages（最多 5 条·去重置顶）。
 * 看板 dashboard.html 读取该键渲染「最近浏览」条；数据全程留在本浏览器，不上传。
 * 失败语义：隐私模式 / 配额满 / 非 data 页 ⇒ 静默跳过（不影响页面其余功能）。
 */
(function () {
  var KEY = 'xy-recent-pages';
  var MAX = 5;
  try {
    var path = (window.location.pathname || '');
    var name = path.split('/').pop() || '';
    if (!/^[A-Za-z0-9_-]+\.html$/.test(name)) return;
    var parts = (document.title || '').split(' · ');
    var title = (parts[0] || '').trim();
    if (parts.length > 1 && (title === '详解西游记' || title === 'JTTW Notes')) {
      title = (parts[1] || '').trim();
    }
    if (!title) return;
    var item = { href: 'data/' + name, title: title };
    var list = [];
    try { list = JSON.parse(window.localStorage.getItem(KEY) || '[]'); } catch (_) { list = []; }
    if (!Array.isArray(list)) list = [];
    list = list.filter(function (x) { return x && x.href && x.href !== item.href; });
    list.unshift(item);
    window.localStorage.setItem(KEY, JSON.stringify(list.slice(0, MAX)));
  } catch (_) { /* 静默：记录失败不影响阅读 */ }
})();
