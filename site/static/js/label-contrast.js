/*
 * label-contrast.js — 图表标签前景色自适应（公共工具·W1283）
 * ------------------------------------------------------------------
 * 用途：当 SVG 文字压在色块上时，按**渲染后实际底色**自适应前景色，
 *       使前景/底色对比度达到 WCAG AA 正文线（≥ 4.5:1）。
 *
 * 背景（第 80 门禁 graphic 口径实测）：全站 89 页 / 544 条唯一违例
 *   （四态累计 1236 条），成因是各页 JS 各自写死 fill（#fff / var(--ink-soft)
 *   / 继承公共层 --text-tertiary），与所压色块的颜色方向不匹配。
 *   典型：白字压浅底（CR 1.8）、深墨字压深底（CR 1.77）。
 *
 * 设计要点（与第 80 门禁 graphic 口径**同源规则**·E-285）：
 *   ① 底色 = **几何上真正覆盖该文字的 SVG 图形**的 computed fill；
 *      - rect 等实心盒：中心点落在 bbox 内 且 交集/文字面积 ≥ 0.6
 *      - circle/ellipse：中心点落在**真实椭圆**内 且 交集比 ≥ 0.6
 *      - path/polygon：**仅当 bbox 完全包含文字 bbox** 才算覆盖（保守·宁可漏检）
 *   ② 坐标系归一化：getBBox() + getCTM() 变换到同一 <svg> 的 viewBox 用户空间
 *      （禁用 getBoundingClientRect——视口像素在缩放/变换后会与图形层错位）。
 *   ③ 暗色态：公共层会给图形加 brightness() 提亮（实测 #8E7D62 → rgb(193,190,139)），
 *      computed fill 仍是原色 ⇒ 必须把 brightness 系数乘进去才是**视觉实际底色**。
 *   ④ 描边同步：前景变深色时，原白色描边会变成"深字压深描边" ⇒ 描边一并切换。
 *
 * 用法：页面引入本脚本即自动生效（无需调用方写任何代码）。
 *   <script src="../static/js/label-contrast.js"></script>
 *   （EN 站与 data 站路径相同，均为 site/static/js/）
 *
 * 幂等：重复执行不叠加（每次都按当前实际底色重算）。
 * 保守：找不到覆盖图形 ⇒ 不改；找不到更高对比色 ⇒ 不改（保持原样）。
 */
(function (root, factory) {
    var api = factory();
    if (typeof module === "object" && module.exports) {
        module.exports = api;
    }
    if (root) {
        root.XJLabelContrast = api;
        api.auto();
    }
})(typeof window !== "undefined" ? window : null, function () {
    "use strict";

    // 与第 80 门禁 graphic 口径**同源**（E-285）：判红线 3.0（WCAG 图形对象最低可读线），
    // 且「有描边且描边与真实底色的分离度 ≥ 3.0」即视为光晕已提供分离 ⇒ 豁免。
    // 目标线 4.5（WCAG AA 正文线）仅作**改动时的择优方向**，不作是否改动的判据。
    var TARGET_CR = 3.0;              // 判红线（与门禁一致）
    var PREFERRED_CR = 4.5;           // 择优方向
    var HALO_MIN_SEPARATION = 3.0;    // 描边与真实底色的最小分离度（光晕豁免门槛）
    var MIN_COVER = 0.6;              // 文字面积落入图形的最小比例
    var DARK_INK = [35, 32, 26]; // 深墨（与仓内 treemap 既有口径一致：#23201A）
    var LIGHT_INK = [255, 255, 255];

    function parseColor(str) {
        if (!str) return null;
        str = String(str).trim();
        var m = str.match(/rgba?\(([^)]+)\)/);
        if (m) {
            var p = m[1].split(",").map(function (x) { return parseFloat(x); });
            if (p.length < 3 || isNaN(p[0])) return null;
            return [p[0], p[1], p[2], p.length > 3 && !isNaN(p[3]) ? p[3] : 1];
        }
        m = str.match(/^#([0-9a-f]{3,8})$/i);
        if (m) {
            var h = m[1];
            if (h.length === 3) h = h.split("").map(function (c) { return c + c; }).join("");
            if (h.length === 6) h += "ff";
            if (h.length !== 8) return null;
            return [
                parseInt(h.slice(0, 2), 16),
                parseInt(h.slice(2, 4), 16),
                parseInt(h.slice(4, 6), 16),
                parseInt(h.slice(6, 8), 16) / 255,
            ];
        }
        return null;
    }

    function luminance(c) {
        var f = function (v) {
            v = v / 255;
            return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
        };
        return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]);
    }

    function contrast(a, b) {
        var la = luminance(a), lb = luminance(b);
        var hi = Math.max(la, lb), lo = Math.min(la, lb);
        return (hi + 0.05) / (lo + 0.05);
    }

    /** 视觉实际底色：computed fill × filter 的 brightness 系数（暗色态公共层会提亮图形）。 */
    function effectiveBg(el) {
        var cs = getComputedStyle(el);
        var c = parseColor(cs.fill);
        if (!c || c[3] < 0.3) return null;
        var k = 1;
        var fm = String(cs.filter || "").match(/brightness\(([\d.]+)\)/);
        if (fm) k = parseFloat(fm[1]);
        if (!isNaN(k) && k > 0) {
            c = [
                Math.min(255, c[0] * k),
                Math.min(255, c[1] * k),
                Math.min(255, c[2] * k),
                c[3],
            ];
        }
        return c;
    }

    /** 把带 alpha 的前景色合成到底色上（与门禁 over() 同源·光晕实际覆盖处的颜色）。 */
    function over(fg, bg) {
        var a = fg[3] === undefined ? 1 : fg[3];
        return [
            fg[0] * a + bg[0] * (1 - a),
            fg[1] * a + bg[1] * (1 - a),
            fg[2] * a + bg[2] * (1 - a),
            1,
        ];
    }

    /** 元素 bbox 归一化到所属 <svg> 的 viewBox 用户空间（getBBox + getCTM）。 */
    function normBox(el) {
        var b;
        try { b = el.getBBox(); } catch (e) { return null; }
        if (!b || b.width <= 0 || b.height <= 0) return null;
        var m = el.getCTM();
        if (!m) return { x: b.x, y: b.y, w: b.width, h: b.height };
        var xs = [], ys = [];
        var pts = [[b.x, b.y], [b.x + b.width, b.y], [b.x, b.y + b.height], [b.x + b.width, b.y + b.height]];
        for (var i = 0; i < pts.length; i++) {
            var px = pts[i][0], py = pts[i][1];
            xs.push(m.a * px + m.c * py + m.e);
            ys.push(m.b * px + m.d * py + m.f);
        }
        var minX = Math.min.apply(null, xs), maxX = Math.max.apply(null, xs);
        var minY = Math.min.apply(null, ys), maxY = Math.max.apply(null, ys);
        return { x: minX, y: minY, w: maxX - minX, h: maxY - minY };
    }

    function intersectArea(a, b) {
        var ox = Math.max(0, Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x));
        var oy = Math.max(0, Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y));
        return ox * oy;
    }

    /** 最近的非透明 CSS 背景色（自元素向上找·含 body）——文字直接落在纸底/卡片底时的底色。 */
    function nearestCssBg(el) {
        var node = el;
        while (node && node.nodeType === 1) {
            var cs = null;
            try { cs = getComputedStyle(node); } catch (e) { cs = null; }
            if (cs) {
                var c = parseColor(cs.backgroundColor);
                if (c && c[3] >= 0.3) return c;
            }
            node = node.parentElement;
        }
        try {
            var bc = parseColor(getComputedStyle(document.body).backgroundColor);
            if (bc && bc[3] >= 0.3) return bc;
        } catch (e) {}
        return null;
    }

    /** 找覆盖该文字的图形（面积最小者＝最贴近文字那层）。null = 未覆盖。 */
    function coveringShape(svg, textEl, textBox) {
        var shapes = svg.querySelectorAll("rect,circle,ellipse,polygon,path");
        var area = textBox.w * textBox.h;
        var best = null, bestCov = 0, bestArea = Infinity;
        for (var i = 0; i < shapes.length; i++) {
            var sh = shapes[i];
            if (sh.closest("text")) continue;
            var sb = normBox(sh);
            if (!sb) continue;
            var inter = intersectArea(textBox, sb);
            if (inter <= 0) continue;
            if (sh.tagName.toLowerCase() === "path" || sh.tagName.toLowerCase() === "polygon") {
                // path/polygon：仅当 bbox 完全包含文字 bbox 才算覆盖（保守）
                var contains = sb.x <= textBox.x + 0.5 && sb.y <= textBox.y + 0.5
                    && sb.x + sb.w >= textBox.x + textBox.w - 0.5
                    && sb.y + sb.h >= textBox.y + textBox.h - 0.5;
                if (!contains) continue;
            } else if (sh.tagName.toLowerCase() === "circle" || sh.tagName.toLowerCase() === "ellipse") {
                // 椭圆档：中心点须落在**真实椭圆**内（bbox 是外接矩形·直接用 bbox 会误判角落）
                var cx = sb.x + sb.w / 2, cy = sb.y + sb.h / 2;
                var rx = sb.w / 2, ry = sb.h / 2;
                var tx = (textBox.x + textBox.w / 2 - cx) / (rx || 1);
                var ty = (textBox.y + textBox.h / 2 - cy) / (ry || 1);
                if (tx * tx + ty * ty > 1) continue;
                if (inter / area < MIN_COVER) continue;
            } else {
                // 矩形档：中心点须落在图形 bbox 内 **且** 文字大部分落入
                // （与第 80 门禁 coversText 完全一致——只判交集比例会把「文字偏在图形边缘」误算成覆盖）
                var mx = textBox.x + textBox.w / 2, my = textBox.y + textBox.h / 2;
                if (mx < sb.x || mx > sb.x + sb.w || my < sb.y || my > sb.y + sb.h) continue;
                if (inter / area < MIN_COVER) continue;
            }
            var shArea = sb.w * sb.h;
            var cov = inter / area;
            if (cov > bestCov + 0.01 || (Math.abs(cov - bestCov) <= 0.01 && shArea < bestArea)) {
                bestCov = cov; bestArea = shArea; best = sh;
            }
        }
        return best;
    }

    /** 处理单个 text：返回是否改动。 */
    function fixText(textEl) {
        var svg = textEl.ownerSVGElement || textEl.closest("svg");
        if (!svg) return false;
        var cs = getComputedStyle(textEl);
        if (!cs || cs.fill === "none" || cs.visibility === "hidden" || cs.display === "none") return false;
        if (parseFloat(cs.opacity || "1") === 0) return false;
        var fg = parseColor(cs.fill);
        if (!fg || fg[3] < 0.3) return false;
        var tb = normBox(textEl);
        if (!tb) return false;
        var shape = coveringShape(svg, textEl, tb);
        var bg = null;
        if (shape) {
            bg = effectiveBg(shape);
        } else {
            // 无覆盖图形 ⇒ 底色取「最近的非透明 CSS 背景」（含 body）
            // ——与第 80 门禁 graphic 口径的 body 回退同族：浅色文字直接放在纸底上时，
            //   若不处理会整段不可读（实测 visual-art 明态 CR 1.58·暗态同字正常）。
            bg = nearestCssBg(textEl);
        }
        if (!bg) return false;

        var cur = contrast(fg, bg);

        // 描边（光晕）是否已提供足够分离？——**与门禁完全同源**：
        // 光晕色按 alpha **合成到底色**后与底色的对比度 ≥ 3.0 ⇒ 豁免。
        // （注：用纯描边色而非合成色算会偏乐观——实测白描边 0.88 覆金黄底：
        //   纯白口径 3.18（豁免）· 合成口径 2.79（不豁免）⇒ 差 0.4 就判红不同）
        var stroke = cs.stroke;
        var hasHalo = !!(stroke && stroke !== "none" && parseFloat(cs.strokeWidth) >= 1);
        var haloSep = 0;
        if (hasHalo) {
            var sc = parseColor(stroke);
            if (sc) haloSep = contrast(over(sc, bg), bg);
        }
        if (cur >= TARGET_CR) return false;                              // 已达判红线 ⇒ 不动
        if (hasHalo && haloSep >= HALO_MIN_SEPARATION) return false;      // 光晕已提供分离 ⇒ 不动

        // 需改：先试「换前景色」——选对比更高的一方（择优向 PREFERRED_CR）
        var crDark = contrast(DARK_INK, bg);
        var crLight = contrast(LIGHT_INK, bg);
        var pickDark = crDark >= crLight;
        var pick = pickDark ? DARK_INK : LIGHT_INK;
        var newCr = pickDark ? crDark : crLight;

        if (newCr < TARGET_CR) {
            // 中等亮度底色：白与深墨**都**达不到判红线 ⇒ 换 fill 无解
            // ⇒ 唯一解是**不透明描边**（光晕与底色的分离度 ≥ 门槛 ⇒ 门禁豁免 + 视觉可读）。
            if (!hasHalo) return false;
            var haloWant = pickDark ? "rgb(255,255,255)" : "rgb(20,20,30)";
            var hc = parseColor(haloWant);
            if (!hc || contrast(over(hc, bg), bg) < HALO_MIN_SEPARATION) return false;
            if (haloSep < HALO_MIN_SEPARATION) {
                textEl.style.setProperty("stroke", haloWant, "important");
                textEl.style.setProperty("stroke-width", "3px", "important");
            }
            return true;
        }

        if (newCr <= cur) return false;        // 没有更好方案 ⇒ 不动（保守）

        var newFill = pickDark ? "#23201A" : "#ffffff";
        if (cs.fill !== newFill) textEl.style.setProperty("fill", newFill, "important");

        // 描边同步：前景变深色时原白色描边会变成「深字压深描边」⇒ 描边切到相反方向；
        // 且必须用**不透明**色（否则 alpha 合成后分离度可能仍 < 门槛 ⇒ 改完仍被门禁判红）。
        if (hasHalo) {
            var wantStroke = pickDark ? "rgb(255,255,255)" : "rgb(20,20,30)";
            var scWant = parseColor(wantStroke);
            if (scWant && contrast(over(scWant, bg), bg) >= HALO_MIN_SEPARATION) {
                textEl.style.setProperty("stroke", wantStroke, "important");
            }
        }
        return true;
    }

    /** 对一棵 DOM 下的所有 svg text 执行一次。返回改动条数。 */
    function apply(root) {
        var scope = root && root.querySelectorAll ? root : document;
        var texts = scope.querySelectorAll("svg text");
        var n = 0;
        for (var i = 0; i < texts.length; i++) {
            try {
                if (fixText(texts[i])) n++;
            } catch (e) { /* 单个失败不影响其余 */ }
        }
        return n;
    }

    // **节流**（非去抖）——关键：页面 DOM 持续变化（count-up 动画 / 图表重绘）时，
    // 去抖写法（clearTimeout + 200ms）会被无限推迟 ⇒ apply 永远不执行 ⇒ 修复静默失效。
    // 节流保证每 200ms 至少执行一次。
    var timer = null;
    var lastRun = 0;
    function runNow() {
        lastRun = Date.now();
        try { apply(document); } catch (e) {}
    }
    function schedule() {
        var wait = Math.max(0, 200 - (Date.now() - lastRun));
        if (timer) {
            if (wait === 0) { clearTimeout(timer); timer = null; runNow(); }
            return;
        }
        timer = setTimeout(function () { timer = null; runNow(); }, wait);
    }

    function auto() {
        if (typeof document === "undefined") return;
        var run = function () { try { apply(document); } catch (e) {} };
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", run);
        } else {
            run();
        }
        // 图表多在 fetch 之后渲染 ⇒ 补跑几轮（配合节流，覆盖渲染完成时机）
        [400, 1200, 2500].forEach(function (ms) {
            setTimeout(run, ms);
        });
        // 图表多由 fetch 后渲染 ⇒ 监听 DOM 变化（节流）
        try {
            var mo = new MutationObserver(schedule);
            mo.observe(document.documentElement, { childList: true, subtree: true });
        } catch (e) {}
        // 主题切换（暗态公共层会提亮图形 ⇒ 须重算）
        try {
            var mo2 = new MutationObserver(schedule);
            mo2.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
        } catch (e) {}
        // 系统配色切换（prefers-color-scheme）——**必须监听**：
        // 第 80 门禁探针以 colorScheme 模拟明暗四态，若工具只听 data-theme，
        // 则 CSS 已随 colorScheme 变化而工具算出的内联色未变 ⇒ 改后仍被判红。
        try {
            if (window.matchMedia) {
                var mq = window.matchMedia("(prefers-color-scheme: dark)");
                var onScheme = function () { schedule(); };
                if (mq.addEventListener) mq.addEventListener("change", onScheme);
                else if (mq.addListener) mq.addListener(onScheme);
            }
        } catch (e) {}
    }

    return {
        apply: apply,
        auto: auto,
        fixText: fixText,
        contrast: contrast,
        luminance: luminance,
        parseColor: parseColor,
        normBox: normBox,
        over: over,
        nearestCssBg: nearestCssBg,
        coveringShape: coveringShape,
        TARGET_CR: TARGET_CR,
        PREFERRED_CR: PREFERRED_CR,
        HALO_MIN_SEPARATION: HALO_MIN_SEPARATION,
    };
});
