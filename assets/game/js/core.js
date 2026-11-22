/* 取经三试 · 共享核心（零依赖 · file:// 可用） */
(function () {
    'use strict';

    var XG = window.XG = window.XG || {};
    XG.modes = XG.modes || {};

    XG.registerMode = function (name, api) {
        XG.modes[name] = api;
    };

    XG.qs = function (sel, root) {
        return (root || document).querySelector(sel);
    };

    XG.clamp = function (v, min, max) {
        return v < min ? min : (v > max ? max : v);
    };

    XG.rand = function (min, max) {
        return min + Math.random() * (max - min);
    };

    XG.randInt = function (min, max) {
        return Math.floor(min + Math.random() * (max - min + 1));
    };

    XG.pick = function (arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    };

    XG.shuffle = function (arr) {
        var a = arr.slice();
        for (var i = a.length - 1; i > 0; i -= 1) {
            var j = Math.floor(Math.random() * (i + 1));
            var t = a[i];
            a[i] = a[j];
            a[j] = t;
        }
        return a;
    };

    XG.fmt = function (n) {
        return Number(n || 0).toLocaleString('zh-CN');
    };

    XG.storage = {
        get: function (key, fallback) {
            try {
                var raw = window.localStorage.getItem(key);
                return raw === null ? fallback : Number(raw);
            } catch (e) {
                return fallback;
            }
        },
        set: function (key, value) {
            try {
                window.localStorage.setItem(key, String(value));
            } catch (e) {
                /* 隐私模式下静默降级 */
            }
        }
    };

    XG.reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

    XG.data = null;
    XG.loadData = function () {
        if (XG.data) return XG.data;
        var node = document.getElementById('EMBEDDED_DATA');
        var parsed = null;
        if (node) {
            try {
                parsed = JSON.parse(node.textContent || '{}');
            } catch (e) {
                console.warn('[INFO] 游戏内嵌数据解析失败，使用空集', e);
            }
        }
        XG.data = {
            hardships: (parsed && parsed.hardships) || [],
            cards: (parsed && parsed.cards) || []
        };
        return XG.data;
    };

    XG.bar = function (el, ratio) {
        if (!el) return;
        el.style.width = (XG.clamp(ratio, 0, 1) * 100).toFixed(1) + '%';
    };

    // 合成音效（零素材 · 首次用户操作后才创建 AudioContext）
    XG.audio = (function () {
        var ctx = null;
        var muted = false;
        try {
            muted = window.localStorage.getItem('xy_trials_muted') === '1';
        } catch (e) {
            muted = false;
        }

        function ensure() {
            if (muted) return null;
            var AC = window.AudioContext || window.webkitAudioContext;
            if (!AC) return null;
            if (!ctx) ctx = new AC();
            if (ctx.state === 'suspended') {
                try { ctx.resume(); } catch (e) { /* 忽略 */ }
            }
            return ctx;
        }

        function tone(freq, dur, type, gain, slideTo) {
            var c = ensure();
            if (!c) return;
            var osc = c.createOscillator();
            var vol = c.createGain();
            osc.type = type || 'sine';
            osc.frequency.setValueAtTime(freq, c.currentTime);
            if (slideTo) {
                osc.frequency.exponentialRampToValueAtTime(Math.max(30, slideTo), c.currentTime + dur);
            }
            vol.gain.setValueAtTime(gain || 0.035, c.currentTime);
            vol.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + dur);
            osc.connect(vol);
            vol.connect(c.destination);
            osc.start();
            osc.stop(c.currentTime + dur);
        }

        var SFX = {
            click: function () { tone(520, 0.05, 'sine', 0.025); },
            jump: function () { tone(360, 0.12, 'sine', 0.035, 620); },
            swing: function () { tone(260, 0.08, 'triangle', 0.03, 520); },
            hit: function () { tone(180, 0.08, 'square', 0.035, 90); },
            dash: function () { tone(420, 0.1, 'sawtooth', 0.025, 760); },
            hurt: function () { tone(140, 0.2, 'sawtooth', 0.04, 60); },
            boss: function () { tone(90, 0.4, 'sine', 0.05, 55); },
            item: function () {
                tone(660, 0.08, 'sine', 0.03);
                window.setTimeout(function () { tone(880, 0.12, 'sine', 0.03); }, 90);
            },
            win: function () {
                [523, 659, 784].forEach(function (f, i) {
                    window.setTimeout(function () { tone(f, 0.18, 'sine', 0.035); }, i * 130);
                });
            },
            lose: function () { tone(240, 0.35, 'sine', 0.04, 110); }
        };

        return {
            play: function (name) {
                if (muted) return;
                (SFX[name] || SFX.click)();
            },
            toggle: function () {
                muted = !muted;
                try {
                    window.localStorage.setItem('xy_trials_muted', muted ? '1' : '0');
                } catch (e) { /* 忽略 */ }
                return muted;
            },
            muted: function () { return muted; }
        };
    })();
})();
