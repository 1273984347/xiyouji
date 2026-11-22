/* 取经三试 · 模式切换入口 */
(function () {
    'use strict';

    var XG = window.XG;
    XG.loadData();

    var tabs = Array.prototype.slice.call(document.querySelectorAll('.tr-tab'));
    var panels = {
        action: document.getElementById('panel-action'),
        rogue: document.getElementById('panel-rogue'),
        cards: document.getElementById('panel-cards')
    };
    var current = null;
    var started = {};

    var MODES = { action: 1, rogue: 1, cards: 1 };

    function modeFromHash() {
        var h = String(window.location.hash || '').replace('#', '');
        return MODES[h] ? h : 'action';
    }

    function setHash(mode) {
        if (history.replaceState) {
            history.replaceState(null, '', '#' + mode);
        } else {
            window.location.hash = mode;
        }
    }

    function activate(mode) {
        if (mode === current) return;
        Object.keys(panels).forEach(function (key) {
            var panel = panels[key];
            if (!panel) return;
            if (key === mode) {
                panel.hidden = false;
            } else {
                panel.hidden = true;
                var api = XG.modes[key];
                if (started[key] && api && api.pause) api.pause();
            }
        });
        tabs.forEach(function (tab) {
            var on = tab.getAttribute('data-mode') === mode;
            tab.setAttribute('aria-selected', on ? 'true' : 'false');
            tab.tabIndex = on ? 0 : -1;
        });
        current = mode;
        if (!started[mode]) {
            started[mode] = true;
            var modeApi = XG.modes[mode];
            if (modeApi && modeApi.init) modeApi.init(panels[mode]);
        } else {
            var resumeApi = XG.modes[mode];
            if (resumeApi && resumeApi.resume) resumeApi.resume();
        }
    }

    tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
            var mode = tab.getAttribute('data-mode');
            setHash(mode);
            activate(mode);
        });
        tab.addEventListener('keydown', function (e) {
            if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
            e.preventDefault();
            var idx = tabs.indexOf(tab);
            var next = tabs[(idx + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
            next.focus();
            activate(next.getAttribute('data-mode'));
        });
    });

    window.addEventListener('hashchange', function () {
        activate(modeFromHash());
    });

    activate(modeFromHash());

    var soundBtn = document.getElementById('jt-sound');
    if (soundBtn && XG.audio) {
        var syncSound = function () {
            var off = XG.audio.muted();
            soundBtn.textContent = off ? '音效 关' : '音效 开';
            soundBtn.setAttribute('aria-pressed', off ? 'false' : 'true');
        };
        syncSound();
        soundBtn.addEventListener('click', function () {
            XG.audio.toggle();
            syncSound();
            if (!XG.audio.muted()) XG.audio.play('click');
        });
    }

    // 引用块复制（独立页不加载站点 cite-box.js）
    document.addEventListener('click', function (e) {
        var btn = e.target && e.target.closest ? e.target.closest('.cite-copy') : null;
        if (!btn) return;
        var item = btn.parentElement;
        var pre = item ? item.querySelector('.cite-text') : null;
        if (!pre || !navigator.clipboard) return;
        navigator.clipboard.writeText(pre.textContent).then(function () {
            btn.textContent = '已复制';
            setTimeout(function () { btn.textContent = '复制'; }, 1200);
        }).catch(function () {});
    });
})();
