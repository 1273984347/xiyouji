/*!
 * site/static/js/motion-gsap.js
 * 《详解西游记》站点公共动效载体（GSAP 3.12.5）
 *
 * 契约来源：DESIGN.md §5（时长三档 / 缓动白名单 / reduced-motion 双守卫 /
 *           只动 transform 与 opacity / 禁止清单）与 §4A.7（微交互分工）
 *
 * 四条铁律：
 *   ① fail-open：无 GSAP / 无 ScrollTrigger / JS 异常 → 内容原样可见（绝不做初始态设置）
 *   ② 不与既有 `.reveal-in` 进场机制争抢同一元素的控制权（带该类的元素一律跳过）
 *   ③ 显式 opt-in：只处理带 `data-gsap` 标记的容器，不做全站扫描
 *   ④ 只动 transform 与 opacity（x / y / autoAlpha），不动布局属性
 *
 * 用法：容器上标 data-gsap="intro" | "sections" | "cards" | "fold"（空格分隔可多值）
 *   intro    —— 入场编排：容器直接子元素按序进场（Timeline + stagger）
 *   sections —— 滚动叙事：容器内 h2 分节标题进入视口时一次性进场（批量协调）
 *   cards    —— 卡片 / 分组网格进场：容器内匹配 data-gsap-target（缺省 .card）的元素按序进场
 *   fold     —— 微交互联动：折叠块展开时内容序列进场
 *
 * 同批待确认项（见《执行前计划-T28》Q-01）：是否把本文件的写法判据挂成常驻门禁槽；
 * 在获批前，判据以独立脚本 scripts/check_gsap_motion.py 形式存在（不改管控文件）。
 */
(function () {
  'use strict';

  var GSAP = window.gsap;
  if (!GSAP) { return; }                       /* 铁律①：无 GSAP 直接退出，内容原样可见 */

  var ST = window.ScrollTrigger;
  if (ST) { GSAP.registerPlugin(ST); }

  /* —— 时长三档（秒）· 对应 DESIGN §5.1：反馈 ≤150ms / 状态 ≤250ms / 入场 ≤600ms —— */
  var DUR = { feedback: 0.15, state: 0.25, enter: 0.5 };

  /* —— 缓动白名单（DESIGN §5.2：禁裸 ease / 禁线性 / 禁回弹类）—— */
  var EASE = {
    feedback: 'power1.out',
    state: 'power2.out',
    enter: 'power3.out',
    link: 'power2.inOut'
  };

  /* —— fail-open 兜底时限（毫秒）：编排未触发时把视口内单元直达终态 —— */
  var SAFE_MS = 1500;

  /* —— 编排单元筛选 —— */

  /* 带 reveal-in 的元素归既有进场机制所有，本载体不碰（铁律②） */
  function claimable(el) {
    return el && el.nodeType === 1 && !el.classList.contains('reveal-in');
  }

  function childrenOf(el) {
    var out = [];
    var kids = el.children || [];
    for (var i = 0; i < kids.length; i++) {
      if (claimable(kids[i])) { out.push(kids[i]); }
    }
    return out;
  }

  /* 分节单元：容器内的 h2 分节标题。
     W962 收窄：初版含 details（折叠块）⇒ 但折叠块默认折叠、进场时不可见 ⇒ 属**无效动效**，
     改为只取 h2；折叠块的展开编排由 fold 模式负责（职责分离）。 */
  function sectionsOf(el) {
    var out = [];
    var nodes = el.querySelectorAll('h2');
    for (var i = 0; i < nodes.length; i++) {
      if (claimable(nodes[i])) { out.push(nodes[i]); }
    }
    return out;
  }

  /* 卡片 / 分组网格单元：容器内匹配选择器的元素。
     选择器由容器上的 data-gsap-target 指定（缺省 .card）——入口层 hub 页的卡片类名各异
     （.reader-group / .reader-idx / .curated-card / .path-card）⇒ 须可配置。 */
  function cardsOf(el) {
    var sel = el.getAttribute('data-gsap-target') || '.card';
    var out = [];
    var nodes;
    try {
      nodes = el.querySelectorAll(sel);
    } catch (e) {
      return out;
    }
    for (var i = 0; i < nodes.length; i++) {
      if (claimable(nodes[i])) { out.push(nodes[i]); }
    }
    return out;
  }

  function foldsOf(el) {
    var out = [];
    var nodes = el.querySelectorAll('details');
    for (var i = 0; i < nodes.length; i++) {
      if (claimable(nodes[i])) { out.push(nodes[i]); }
    }
    return out;
  }

  /* 兜底：把视口内的单元直接推到终态（清除内联初始态，交还 CSS） */
  function settleInView(units) {
    var vh = window.innerHeight || 0;
    for (var i = 0; i < units.length; i++) {
      var r = units[i].getBoundingClientRect();
      if (r.top < vh && r.bottom > 0) {
        GSAP.set(units[i], { autoAlpha: 1, y: 0, clearProps: 'opacity,transform,visibility' });
      }
    }
  }

  function settleAll(units) {
    for (var i = 0; i < units.length; i++) {
      GSAP.set(units[i], { autoAlpha: 1, y: 0, clearProps: 'opacity,transform,visibility' });
    }
  }

  /* —— 模式 A：入场编排（首页首屏等）—— */
  function initIntro(scope) {
    var containers = scope.querySelectorAll('[data-gsap~="intro"]');
    for (var c = 0; c < containers.length; c++) {
      var box = containers[c];
      var units = childrenOf(box);
      if (!units.length) { continue; }

      var tl = GSAP.timeline({
        defaults: { duration: DUR.enter, ease: EASE.enter }
      });
      tl.from(units, {
        autoAlpha: 0,
        y: 10,
        stagger: 0.06,
        overwrite: true
      });
    }
  }

  /* —— 模式 B：滚动叙事（分节单元进入视口时一次性进场）—— */
  function initSections(scope) {
    if (!ST) { return; }                       /* 无 ScrollTrigger ⇒ 该模式整体降级，内容原样可见 */
    var containers = scope.querySelectorAll('[data-gsap~="sections"]');
    for (var c = 0; c < containers.length; c++) {
      var box = containers[c];
      var units = sectionsOf(box);
      if (!units.length) { continue; }

      /* 初始态由本载体设置（不复用 reveal-in 的 CSS 机制） */
      GSAP.set(units, { autoAlpha: 0, y: 8 });

      ST.batch(units, {
        start: 'top 92%',
        once: true,
        onEnter: function (batch) {
          GSAP.to(batch, {
            autoAlpha: 1,
            y: 0,
            duration: DUR.enter,
            ease: EASE.enter,
            stagger: 0.06,
            overwrite: true
          });
        }
      });

      /* 铁律①兜底：1.5s 后仍未进场的视口内单元直接可见 */
      window.setTimeout(function () { settleInView(units); }, SAFE_MS);

      /* 同体裁的折叠块一并接入微交互编排（reader 体裁的 sections 与 fold 同域） */
      var folds = foldsOf(box);
      for (var f = 0; f < folds.length; f++) { bindFold(folds[f]); }
    }
  }

  /* —— 模式 B2：卡片 / 分组网格进场（入口层 hub 页与卡片网格页）—— */
  function initCards(scope) {
    var containers = scope.querySelectorAll('[data-gsap~="cards"]');
    for (var c = 0; c < containers.length; c++) {
      var box = containers[c];
      var units = cardsOf(box);
      if (!units.length) { continue; }
      GSAP.set(units, { autoAlpha: 0, y: 8 });
      /* stagger 自适应：单条入场 0.5 s（§5.1 入场档）· 序列总时长封顶 ≈1.2 s
         （28 张卡片时 stagger 0.025 而非 0.04 ⇒ 避免整屏拖尾过长） */
      var st = Math.min(0.06, 0.7 / units.length);
      GSAP.to(units, {
        autoAlpha: 1,
        y: 0,
        duration: DUR.enter,
        ease: EASE.enter,
        stagger: st,
        overwrite: true
      });
    }
  }

  /* —— 模式 C：微交互联动（折叠块展开时内容序列进场）—— */
  function initFold(scope) {
    var containers = scope.querySelectorAll('[data-gsap~="fold"]');
    for (var c = 0; c < containers.length; c++) {
      var folds = foldsOf(containers[c]);
      for (var i = 0; i < folds.length; i++) {
        bindFold(folds[i]);
      }
    }
  }

  function bindFold(details) {
    if (details.__mgsapBound) { return; }        /* 幂等：同一 details 不重复绑定 */
    details.__mgsapBound = true;
    var summary = details.querySelector('summary');
    if (!summary) { return; }
    details.addEventListener('toggle', function () {
      if (!details.open) { return; }
      var body = details.querySelector('.reader-fold-body') || details;
      var kids = [];
      for (var i = 0; i < body.children.length; i++) {
        if (claimable(body.children[i])) { kids.push(body.children[i]); }
      }
      if (!kids.length) { return; }
      GSAP.fromTo(kids,
        { autoAlpha: 0, y: 6 },
        {
          autoAlpha: 1,
          y: 0,
          duration: DUR.state,
          ease: EASE.state,
          stagger: 0.04,
          overwrite: true
        }
      );
    });
  }

  /* —— 初始化总入口 —— */
  function init() {
    var scope = document.body || document.documentElement;
    if (!scope) { return; }
    try {
      initIntro(scope);
      initSections(scope);
      initCards(scope);
      initFold(scope);
      if (window.MotionGsap) { window.MotionGsap.stats.init += 1; }
    } catch (err) {
      /* 铁律①：任何异常都不得让内容隐身 */
      try {
        settleAll(childrenOf(document.querySelector('[data-gsap~="intro"]') || scope));
      } catch (e2) { /* 兜底失败则保持原状 */ }
      if (window.console && window.console.warn) {
        window.console.warn('[motion-gsap] 动效初始化异常，已降级为静态显示：', err);
      }
    }
  }

  /* 对外暴露最小 API（供后续批次做程序化编排）
     —— 必须定义在 matchMedia 之前：init() 可能同步执行（readyState 非 loading），
        此时若 MotionGsap 尚未定义，执行计数将无处自增 ⇒ 判据失效。 */
  window.MotionGsap = {
    version: '1.0.0',
    init: init,
    durations: DUR,
    eases: EASE,
    stats: { init: 0 }
  };

  /* —— reduced-motion 双守卫（DESIGN §5.3 强制）——
     动效属 JS 侧，不受 CSS 的 prefers-reduced-motion 全局覆写控制 ⇒ 必须 JS 侧短路。
     守卫命中「减弱动态效果」时：本载体完全不介入（不设任何初始态）⇒ 内容原样可见、
     执行的动画数为 0；且 GSAP 在条件不匹配时自动回滚已建实例。 */
  var mm = GSAP.matchMedia();
  mm.add({
    full: '(prefers-reduced-motion: no-preference)',
    calm: '(prefers-reduced-motion: reduce)'
  }, function (ctx) {
    if (!ctx.conditions.full) { return; }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init, { once: true });
    } else {
      init();
    }
  });
})();
