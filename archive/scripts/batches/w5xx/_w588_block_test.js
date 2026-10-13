/* W588 dark lift v2（暗色阶段二·MutationObserver 无竞态·浅色零改动） */
(function () {
    try {
    if (!window.matchMedia || !window.matchMedia('(prefers-color-scheme: dark)').matches) return;
    var TH = 0.16, TARGET = 0.22, timer = null;
    function lum(r, g, b) {
        function f(c) { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
    }
    function liftOnce() {
        var els = document.querySelectorAll('svg rect, svg circle, svg path, svg polygon, svg ellipse');
        for (var i = 0; i < els.length; i++) {
            var el = els[i];
            var cf = getComputedStyle(el).fill;
            if (cf.indexOf('rgb') !== 0) continue;
            var m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(cf);
            if (!m) continue;
            var r = +m[1], g = +m[2], b = +m[3];
            if (lum(r, g, b) >= TH) continue;
            var rect = el.getBoundingClientRect();
            if (rect.width < 3 || rect.height < 3) continue;
            var rr = r, gg = g, bb = b;
            for (var k = 1; k <= 20; k++) {
                var a = k / 20;
                rr = Math.round(r + (242 - r) * a); gg = Math.round(g + (235 - g) * a); bb = Math.round(b + (220 - b) * a);
                if (lum(rr, gg, bb) >= TARGET) break;
            }
            el.style.fill = 'rgb(' + rr + ',' + gg + ',' + bb + ')';
        }
    }
    function schedule() { if (timer) return; timer = setTimeout(function () { timer = null; liftOnce(); }, 80); }
    [0, 500, 1500, 3000, 5000].forEach(function (d) { setTimeout(liftOnce, d); });
    if (window.MutationObserver) {
        var mo = new MutationObserver(schedule);
        mo.observe(document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ['fill', 'style'] });
    }
    window.__w588init = 1;
    } catch (e) { try { window.__w588err = String(e).slice(0, 120); } catch (_e) {} }
})();
