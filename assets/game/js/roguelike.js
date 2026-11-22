/* 取经三试 · 第二试「八十一难」· DOM 轻 Roguelike */
(function () {
    'use strict';

    var XG = window.XG;
    var BEST_KEY = 'xy_trials_rogue_best';
    var DEFAULT_TOTAL = 12;
    var LONG_TOTAL = 18;

    var ITEMS = [
        { id: 'dingfeng', name: '定风丹', desc: '硬闯体力消耗 -3' },
        { id: 'zhaoyao', name: '照妖镜', desc: '智取心性消耗 -3' },
        { id: 'jialan', name: '锦襕袈裟', desc: '心性上限 +20，立即回 20' },
        { id: 'xizhang', name: '九环锡杖', desc: '硬闯得分 +40' },
        { id: 'hulu', name: '紫金葫芦', desc: '立即 +1 救兵' },
        { id: 'haomao', name: '救命毫毛', desc: '每难开始回复 2 体力与 2 心性' }
    ];

    var EVENTS = [
        {
            id: 'alms',
            title: '化缘',
            desc: '路边一户人家见你们风尘仆仆，愿意施舍。',
            options: [
                { label: '求一顿斋饭', cost: '体力 +12', log: '体力 +12', apply: function () { run.hp = Math.min(run.maxHp, run.hp + 12); } },
                { label: '求一卷经书', cost: '心性 +12', log: '心性 +12', apply: function () { run.mind = Math.min(run.maxMind, run.mind + 12); } },
                { label: '求一位向导', cost: '救兵 +1', log: '救兵 +1', apply: function () { run.rescue += 1; } }
            ]
        },
        {
            id: 'temple',
            title: '古庙避雨',
            desc: '山雨忽至，前方一座破庙可供暂歇。',
            options: [
                { label: '歇脚', cost: '体力 +8 · 心性 +4', log: '体力 +8，心性 +4', apply: function () { run.hp = Math.min(run.maxHp, run.hp + 8); run.mind = Math.min(run.maxMind, run.mind + 4); } },
                { label: '抄经', cost: '心性 +12', log: '心性 +12', apply: function () { run.mind = Math.min(run.maxMind, run.mind + 12); } },
                { label: '冒雨赶路', cost: '得分 +80', log: '得分 +80', apply: function () { run.score += 80; } }
            ]
        },
        {
            id: 'mountain',
            title: '山神指路',
            desc: '山神现身，愿指一条近路，但也要你拿主意。',
            options: [
                { label: '问近路', cost: '得分 +100', log: '得分 +100', apply: function () { run.score += 100; } },
                { label: '求护符', cost: '救兵 +1', log: '救兵 +1', apply: function () { run.rescue += 1; } },
                { label: '就地休整', cost: '体力 +10', log: '体力 +10', apply: function () { run.hp = Math.min(run.maxHp, run.hp + 10); } }
            ]
        },
        {
            id: 'wind',
            title: '妖风突袭',
            desc: '一阵妖风卷过，避无可避。',
            options: [
                { label: '硬扛', cost: '体力 -8 · 得分 +150', log: '体力 -8，得分 +150', apply: function () { run.hp = Math.max(1, run.hp - 8); run.score += 150; } },
                { label: '破法', cost: '心性 -8 · 得分 +120', log: '心性 -8，得分 +120', apply: function () { run.mind = Math.max(1, run.mind - 8); run.score += 120; } },
                { label: '绕行', cost: '得分 +30', log: '得分 +30', apply: function () { run.score += 30; } }
            ]
        },
        {
            id: 'immortal',
            title: '仙翁赠药',
            desc: '一位采药仙翁拦住去路，说与取经人有缘。',
            options: [
                { label: '求药', cost: '体力 +20', log: '体力 +20', apply: function () { run.hp = Math.min(run.maxHp, run.hp + 20); } },
                { label: '求静心法', cost: '心性 +20', log: '心性 +20', apply: function () { run.mind = Math.min(run.maxMind, run.mind + 20); } },
                { label: '求一件法宝', cost: '随机法宝', log: '获得一件法宝', apply: function () { grantItem(); } }
            ]
        },
        {
            id: 'ferry',
            title: '渡口',
            desc: '大河横在眼前，船家开价，潮水也在涨。',
            options: [
                { label: '雇船', cost: '救兵 +1', log: '救兵 +1', apply: function () { run.rescue += 1; } },
                { label: '涉水', cost: '体力 -6 · 得分 +120', log: '体力 -6，得分 +120', apply: function () { run.hp = Math.max(1, run.hp - 6); run.score += 120; } },
                { label: '等潮', cost: '心性 -6 · 得分 +100', log: '心性 -6，得分 +100', apply: function () { run.mind = Math.max(1, run.mind - 6); run.score += 100; } }
            ]
        }
    ];

    var HEROES = [
        {
            id: 'wukong',
            name: '悟空',
            desc: '硬闯体力消耗 -2',
            apply: function () { run.forceBonus += 2; }
        },
        {
            id: 'bajie',
            name: '八戒',
            desc: '体力上限 +20',
            apply: function () { run.maxHp += 20; run.hp += 20; }
        },
        {
            id: 'wujing',
            name: '沙僧',
            desc: '心性上限 +20',
            apply: function () { run.maxMind += 20; run.mind += 20; }
        }
    ];

    var els = {};
    var run = null;
    var best = 0;
    var selectedHero = 'wukong';

    function setText(el, text) {
        if (el && el.textContent !== String(text)) el.textContent = String(text);
    }

    function panelVisible() {
        var panel = document.getElementById('panel-rogue');
        return panel && !panel.hidden;
    }

    function chapterRank(h) {
        var n = Number(h.chapter);
        return isNaN(n) ? 0 : n;
    }

    function chapterLabel(h) {
        var n = Number(h.chapter);
        return isNaN(n) ? '前传' : '第 ' + n + ' 回';
    }

    function pickRun(total) {
        var data = XG.loadData();
        var list = data.hardships.slice().sort(function (a, b) {
            return chapterRank(a) - chapterRank(b);
        });
        if (!list.length) return [];
        var picks = [];
        for (var i = 0; i < total; i += 1) {
            var lo = Math.floor(i * list.length / total);
            var hi = Math.max(lo + 1, Math.floor((i + 1) * list.length / total));
            picks.push(list[XG.randInt(lo, hi - 1)]);
        }
        return picks;
    }

    function hasItem(id) {
        return run.items.some(function (it) { return it.id === id; });
    }

    function addLog(text, hl) {
        run.log.push({ text: text, hl: !!hl });
        if (run.log.length > 40) run.log.shift();
        renderLog();
    }

    function renderLog() {
        if (!els.log) return;
        els.log.innerHTML = '';
        run.log.slice(-10).forEach(function (line) {
            var div = document.createElement('div');
            if (line.hl) div.className = 'hl';
            div.textContent = line.text;
            els.log.appendChild(div);
        });
        els.log.scrollTop = els.log.scrollHeight;
    }

    function startRun(total) {
        XG.audio.play('click');
        var count = total === LONG_TOTAL ? LONG_TOTAL : DEFAULT_TOTAL;
        run = {
            total: count,
            steps: pickRun(count),
            idx: 0,
            hp: 100,
            maxHp: 100,
            mind: 100,
            maxMind: 100,
            rescue: 3,
            score: 0,
            items: [],
            forceBonus: 0,
            witBonus: 0,
            forceScore: 0,
            regen: 0,
            log: [],
            over: false,
            won: false,
            pending: false,
            event: null,
            eventIds: []
        };
        if (!run.steps.length) {
            addLog('八十一难数据未载入，无法开局。', true);
            return;
        }
        var hero = HEROES.filter(function (h) { return h.id === selectedHero; })[0] || HEROES[0];
        hero.apply();
        run.hero = hero.name;
        if (els.start) els.start.textContent = count === LONG_TOTAL ? '重新长途' : '重新西行';
        if (els.end) els.end.hidden = true;
        addLog('行者：' + hero.name + '（' + hero.desc + '）。', true);
        addLog('自长安出发。' + run.total + ' 难在前，体力、心性、救兵各有限。', true);
        renderRun();
    }

    function optionsFor(h) {
        var hpCost = h.difficulty === '需要搬救兵' ? 16 : 9;
        var mindCost = h.cause === '人心自生的魔障' ? 5 : 12;
        hpCost = Math.max(3, hpCost - (hasItem('dingfeng') ? 3 : 0) - run.forceBonus);
        mindCost = Math.max(3, mindCost - (hasItem('zhaoyao') ? 3 : 0) - run.witBonus);

        return [
            {
                key: 'force',
                label: '硬闯',
                cost: '体力 -' + hpCost,
                desc: h.difficulty === '需要搬救兵'
                    ? '这一难原需搬救兵，硬闯代价更高，但拿分最多。'
                    : '悟空独立可解之难，硬闯是正路。',
                ok: run.hp > hpCost,
                apply: function () {
                    run.hp -= hpCost;
                    var gain = 120 + (h.ending === '被打死（无背景）' ? 40 : (h.ending === '被收编' ? 30 : 10)) + (hasItem('xizhang') ? 40 : 0);
                    run.score += gain;
                    addLog('硬闯「' + h.name + '」：体力 -' + hpCost + '，得分 +' + gain + '。');
                }
            },
            {
                key: 'wit',
                label: '智取',
                cost: '心性 -' + mindCost,
                desc: h.cause === '人心自生的魔障'
                    ? '此难本是心魔，智取最省，另有额外得分。'
                    : '绕开正面冲突，看破因果，但耗心性。',
                ok: run.mind > mindCost,
                apply: function () {
                    run.mind -= mindCost;
                    var gain = 90 + (h.cause === '人心自生的魔障' ? 50 : 0) + (h.ending === '被接走（有背景）' ? 10 : 0);
                    run.score += gain;
                    addLog('智取「' + h.name + '」：心性 -' + mindCost + '，得分 +' + gain + '。');
                }
            },
            {
                key: 'rescue',
                label: '请救兵',
                cost: '救兵 -1',
                desc: h.difficulty === '需要搬救兵'
                    ? '原典正是搬救兵之难，请人出手最稳，另有额外得分。'
                    : '请观音或天庭出手，必过，但救兵只有三次。',
                ok: run.rescue > 0,
                apply: function () {
                    run.rescue -= 1;
                    var gain = 50 + (h.difficulty === '需要搬救兵' ? 40 : 0);
                    run.score += gain;
                    addLog('请救兵过「' + h.name + '」：救兵 -1，得分 +' + gain + '。');
                }
            }
        ];
    }

    function renderRun() {
        if (!run) return;
        var h = run.steps[run.idx];
        setText(els.hpNum, Math.max(0, Math.round(run.hp)));
        setText(els.mindNum, Math.max(0, Math.round(run.mind)));
        setText(els.rescueNum, run.rescue);
        setText(els.score, XG.fmt(run.score));
        XG.bar(els.hp, run.hp / run.maxHp);
        XG.bar(els.mind, run.mind / run.maxMind);
        XG.bar(els.rescue, run.rescue / 3);
        XG.bar(els.scoreBar, run.score / 2000);

        if (run.event) {
            renderEvent();
            return;
        }
        if (!h || run.over) return;
        setText(els.chapter, '第 ' + (run.idx + 1) + ' / ' + run.total + ' 难 · ' + chapterLabel(h));
        setText(els.title, h.name);
        setText(els.desc, '出处：' + chapterLabel(h) + '。成因：' + h.cause + '；结局：' + h.ending + '；难度：' + h.difficulty + '。');

        els.tags.innerHTML = '';
        [h.cause, h.ending, h.difficulty].forEach(function (t) {
            var span = document.createElement('span');
            span.className = 'rg-tag';
            span.textContent = t;
            els.tags.appendChild(span);
        });

        renderProgress();
        renderOptions(h);
        renderItems();
    }

    function renderProgress() {
        if (!els.progress) return;
        els.progress.innerHTML = '';
        for (var i = 0; i < run.total; i += 1) {
            var dot = document.createElement('i');
            if (i < run.idx) dot.className = 'done';
            else if (i === run.idx && !run.over) dot.className = 'now';
            els.progress.appendChild(dot);
        }
    }

    function renderOptions(h) {
        if (!els.options) return;
        els.options.innerHTML = '';
        var opts = optionsFor(h);
        var anyOk = opts.some(function (opt) { return opt.ok; });
        if (!anyOk && !run.over) {
            finish(false);
            return;
        }
        opts.forEach(function (opt, i) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'rg-opt';
            btn.disabled = !opt.ok || run.pending;
            var row = document.createElement('div');
            row.className = 'row';
            var strong = document.createElement('strong');
            strong.textContent = (i + 1) + '. ' + opt.label;
            var cost = document.createElement('span');
            cost.className = 'cost';
            cost.textContent = opt.cost;
            row.appendChild(strong);
            row.appendChild(cost);
            var small = document.createElement('small');
            small.textContent = opt.ok ? opt.desc : '资源不足，无法选择。';
            btn.appendChild(row);
            btn.appendChild(small);
            btn.addEventListener('click', function () {
                choose(opt);
            });
            els.options.appendChild(btn);
        });
    }

    function renderItems() {
        if (!els.items) return;
        els.items.innerHTML = '';
        if (!run.items.length) {
            var none = document.createElement('span');
            none.className = 'rg-item';
            none.textContent = '尚无法宝 · 每过三难可得一件';
            els.items.appendChild(none);
            return;
        }
        run.items.forEach(function (it) {
            var span = document.createElement('span');
            span.className = 'rg-item';
            span.textContent = it.name + ' · ' + it.desc;
            els.items.appendChild(span);
        });
    }

    function pickEvent() {
        var pool = EVENTS.filter(function (ev) {
            return run.eventIds.indexOf(ev.id) < 0;
        });
        if (!pool.length) return null;
        var chosen = XG.pick(pool);
        run.eventIds.push(chosen.id);
        return chosen;
    }

    function renderEventOptions(ev) {
        if (!els.options) return;
        els.options.innerHTML = '';
        ev.options.forEach(function (opt, i) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'rg-opt';
            btn.disabled = run.pending;
            var row = document.createElement('div');
            row.className = 'row';
            var strong = document.createElement('strong');
            strong.textContent = (i + 1) + '. ' + opt.label;
            var cost = document.createElement('span');
            cost.className = 'cost';
            cost.textContent = opt.cost;
            row.appendChild(strong);
            row.appendChild(cost);
            btn.appendChild(row);
            btn.addEventListener('click', function () {
                chooseEvent(opt);
            });
            els.options.appendChild(btn);
        });
    }

    function renderEvent() {
        var ev = run.event;
        if (!ev) return;
        setText(els.chapter, '途中事件 · 已完成 ' + run.idx + ' 难');
        setText(els.title, ev.title);
        setText(els.desc, ev.desc);
        els.tags.innerHTML = '';
        ['机缘', '可选择'].forEach(function (t) {
            var span = document.createElement('span');
            span.className = 'rg-tag';
            span.textContent = t;
            els.tags.appendChild(span);
        });
        renderProgress();
        renderEventOptions(ev);
        renderItems();
    }

    function chooseEvent(opt) {
        if (!run || !run.event || run.over || run.pending) return;
        run.pending = true;
        XG.audio.play('click');
        var title = run.event.title;
        opt.apply();
        addLog('途中事件「' + title + '」：' + opt.log + '。', true);
        run.event = null;
        if (run.hp <= 0 || run.mind <= 0) {
            run.hp = Math.max(0, run.hp);
            run.mind = Math.max(0, run.mind);
            finish(false);
            return;
        }
        if (run.idx >= run.total) {
            run.score += run.total * 25;
            finish(true);
            return;
        }
        run.pending = false;
        renderRun();
    }

    function grantItem() {
        var pool = ITEMS.filter(function (it) { return !hasItem(it.id); });
        if (!pool.length) return;
        var item = XG.pick(pool);
        XG.audio.play('item');
        run.items.push(item);
        if (item.id === 'jialan') {
            run.maxMind += 20;
            run.mind += 20;
        } else if (item.id === 'hulu') {
            run.rescue += 1;
        } else if (item.id === 'haomao') {
            run.regen += 2;
        } else if (item.id === 'dingfeng') {
            run.forceBonus += 3;
        } else if (item.id === 'zhaoyao') {
            run.witBonus += 3;
        } else if (item.id === 'xizhang') {
            run.forceScore += 40;
        }
        addLog('得法宝「' + item.name + '」：' + item.desc + '。', true);
    }

    function choose(opt) {
        if (!run || run.over || run.pending || !opt.ok) return;
        run.pending = true;
        XG.audio.play('click');
        opt.apply();

        if (run.hp <= 0 || run.mind <= 0) {
            run.hp = Math.max(0, run.hp);
            run.mind = Math.max(0, run.mind);
            finish(false);
            return;
        }

        run.idx += 1;

        if (run.idx % 3 === 0 && run.idx < run.total) {
            grantItem();
        }
        if (run.regen > 0 && run.idx < run.total) {
            run.hp = Math.min(run.maxHp, run.hp + run.regen);
            run.mind = Math.min(run.maxMind, run.mind + run.regen);
        }

        if (run.idx >= run.total) {
            run.score += run.total * 25;
            finish(true);
            return;
        }
        if (run.idx > 0 && run.idx % 4 === 0) {
            var ev = pickEvent();
            if (ev) {
                run.event = ev;
                run.pending = false;
                renderRun();
                return;
            }
        }
        run.pending = false;
        renderRun();
    }

    function finish(won) {
        XG.audio.play(won ? 'win' : 'lose');
        run.over = true;
        run.event = null;
        run.won = won;
        run.pending = false;
        if (won) run.score += Math.round(run.hp * 2 + run.mind * 2 + run.rescue * 30);
        if (run.score > best) {
            best = run.score;
            XG.storage.set(BEST_KEY, best);
        }
        renderRun();
        renderProgress();
        if (els.options) els.options.innerHTML = '';
        if (els.end) {
            els.end.hidden = false;
            els.end.innerHTML = '';
            var h = document.createElement('h4');
            h.textContent = won ? '西行圆满' : '止步第 ' + (run.idx + 1) + ' 难';
            var p = document.createElement('p');
            p.textContent = (won ? run.total + ' 难已过，灵山在望。' : '体力或心性耗尽，取经路断在这里。') +
                ' 得分 ' + XG.fmt(run.score) + ' · 最高 ' + XG.fmt(best);
            els.end.appendChild(h);
            els.end.appendChild(p);
        }
        addLog(won ? run.total + ' 难已过，得分 ' + XG.fmt(run.score) + '。' : '西行止步，得分 ' + XG.fmt(run.score) + '。', true);
    }

    function onKeyDown(e) {
        if (!panelVisible() || !run || run.over || run.pending) return;
        if (e.key === '1' || e.key === '2' || e.key === '3') {
            e.preventDefault();
            var n = Number(e.key) - 1;
            if (run.event) {
                var eventOpt = run.event.options[n];
                if (eventOpt) chooseEvent(eventOpt);
                return;
            }
            var h = run.steps[run.idx];
            if (!h) return;
            var opts = optionsFor(h);
            var opt = opts[n];
            if (opt) choose(opt);
        }
    }

    function renderHeroes() {
        if (!els.heroes) return;
        els.heroes.innerHTML = '';
        HEROES.forEach(function (hero) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'rg-hero' + (selectedHero === hero.id ? ' is-active' : '');
            btn.setAttribute('aria-pressed', selectedHero === hero.id ? 'true' : 'false');
            var name = document.createElement('b');
            name.textContent = hero.name;
            var desc = document.createElement('small');
            desc.textContent = hero.desc;
            btn.appendChild(name);
            btn.appendChild(desc);
            btn.addEventListener('click', function () {
                selectedHero = hero.id;
                renderHeroes();
            });
            els.heroes.appendChild(btn);
        });
    }

    function init() {
        els = {
            heroes: document.getElementById('rg-heroes'),
            hp: document.getElementById('rg-hp'),
            hpNum: document.getElementById('rg-hp-num'),
            mind: document.getElementById('rg-mind'),
            mindNum: document.getElementById('rg-mind-num'),
            rescue: document.getElementById('rg-rescue'),
            rescueNum: document.getElementById('rg-rescue-num'),
            score: document.getElementById('rg-score'),
            scoreBar: document.getElementById('rg-score-bar'),
            chapter: document.getElementById('rg-chapter'),
            title: document.getElementById('rg-title'),
            desc: document.getElementById('rg-desc'),
            tags: document.getElementById('rg-tags'),
            progress: document.getElementById('rg-progress'),
            options: document.getElementById('rg-options'),
            items: document.getElementById('rg-items'),
            log: document.getElementById('rg-log'),
            end: document.getElementById('rg-end'),
            start: document.getElementById('rg-start')
        };
        best = XG.storage.get(BEST_KEY, 0);
        renderHeroes();
        if (els.start) {
            els.start.addEventListener('click', function () {
                startRun();
            });
        }
        var restart = document.getElementById('rg-restart');
        if (restart) restart.addEventListener('click', function () { startRun(); });
        var longBtn = document.getElementById('rg-start-long');
        if (longBtn) {
            longBtn.addEventListener('click', function () { startRun(LONG_TOTAL); });
        }
        document.addEventListener('keydown', onKeyDown);
    }

    XG.registerMode('rogue', {
        init: init,
        pause: function () {}
    });
})();
