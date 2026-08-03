/* sw.js — 《详解西游记》移动端 PWA 离线缓存
 *
 * 策略：
 *   - install：预缓存应用外壳（app shell）——首页、移动端页、设计系统、
 *     字体、图标、核心 JS。让用户首次在线访问后即可离线打开骨架。
 *   - fetch：
 *       * 导航请求（HTML）→ 网络优先，失败回退到缓存的首页/移动端页（离线可用）
 *       * 静态资源（css/js/fonts/images）→ 缓存优先（稳定资产，秒开）
 *       * 数据/API（dataset/ 与 /query、/datasets、/search）→ 网络优先，
 *         失败时回退到缓存（若有）。RAG 与数据 API 本就需服务端，离线仅尽力而为。
 *   - activate：清理旧版本缓存。
 *
 * 注意：Service Worker 仅在 http(s) 或 localhost 生效；file:// 下不注册
 *（见 index.html / mobile-index.html 中的 http 协议守卫）。
 */
const CACHE = "xiyouji-shell-v1";
const SHELL = [
  "./",
  "./index.html",
  "./mobile-index.html",
  "./manifest.webmanifest",
  "./tokens.css",
  "./system.css",
  "./static/js/vis-tools.js",
  "./static/js/rag-chat.js",
  "./static/fonts/NotoSansSC-Regular.woff2",
  "./static/fonts/NotoSansSC-Medium.woff2",
  "./static/fonts/NotoSerifSC-VF.woff2",
  "./static/images/ink-mountains-hero.webp",
  "./static/icons/icon-192.png",
  "./static/icons/icon-512.png"
];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) { return c.addAll(SHELL); }).then(function () {
      return self.skipWaiting();
    })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; })
        .map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

function isNav(req) { return req.mode === "navigate"; }
function isStatic(req) {
  return /\.(css|js|woff2|woff|ttf|png|jpg|jpeg|webp|svg|json)$/.test(req.url);
}

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;
  var url = new URL(req.url);
  // 数据/API：网络优先，失败回退缓存
  if (url.pathname.indexOf("/dataset") === 0 || url.pathname.indexOf("/search") === 0 ||
      url.pathname.indexOf("/query") === 0 || url.pathname.indexOf("/datasets") === 0 ||
      url.pathname.indexOf("/health") === 0 || url.pathname.indexOf("/graph") === 0) {
    e.respondWith(
      fetch(req).catch(function () { return caches.match(req); })
    );
    return;
  }
  if (isNav(req)) {
    e.respondWith(
      fetch(req).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
        return res;
      }).catch(function () {
        return caches.match("./index.html").then(function (r) { return r || caches.match("./mobile-index.html"); });
      })
    );
    return;
  }
  if (isStatic(req)) {
    e.respondWith(
      caches.match(req).then(function (hit) {
        if (hit) return hit;
        return fetch(req).then(function (res) {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); });
          return res;
        });
      })
    );
    return;
  }
  // 其他：尽力网络
  e.respondWith(fetch(req).catch(function () { return caches.match(req); }));
});
