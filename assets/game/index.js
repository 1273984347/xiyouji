/* 西游小游戏 · 十八款合集（零依赖 · file:// 可用） */
(function () {
    'use strict';

    var CATS = [
        { id: 'all', label: '全部', color: 'var(--accent-primary)' },
        { id: 'action', label: '动作', color: 'var(--series-1)' },
        { id: 'strategy', label: '策略', color: 'var(--series-2)' },
        { id: 'cards', label: '卡牌', color: 'var(--series-6)' },
        { id: 'puzzle', label: '解谜', color: 'var(--series-3)' },
        { id: 'casual', label: '休闲', color: 'var(--series-4)' }
    ];

    var GAMES = [
        {
            file: 'journey-trials.html#action',
            title: '护师西行',
            type: '横版动作 · 护送',
            cat: 'action',
            isNew: true,
            bestKey: 'xy_trials_action_best',
            bestKind: 'score',
            tags: ['护送', '三 Boss', 'Canvas'],
            desc: '唐僧自动西行，你操控悟空清怪。白虎岭、火云洞、火焰山三试，心灯不灭才能走到灵山；另有修罗挑战与无尽循环。'
        },
        {
            file: 'journey-trials.html#rogue',
            title: '八十一难',
            type: '轻 Roguelike',
            cat: 'strategy',
            isNew: true,
            bestKey: 'xy_trials_rogue_best',
            bestKind: 'score',
            tags: ['81 难', '资源', '抉择'],
            desc: '先选悟空、八戒或沙僧，再从八十一难中抽十二难或十八难，靠体力、心性、救兵走到灵山。每四难还有一次途中事件。'
        },
        {
            file: 'journey-trials.html#cards',
            title: '卡牌斗法',
            type: '回合制卡牌',
            cat: 'cards',
            isNew: true,
            bestKey: 'xy_trials_cards_best',
            bestKind: 'stage',
            tags: ['12 角色卡', '能量', '五行'],
            desc: '从十二张角色卡里选一位，连打五阵；前四阵顺序每局随机，二郎神压轴。能量、技能与五行相克都要算。'
        },
        {
            file: 'xiyou-huoyanshan.html',
            title: '火焰山 · 大圣弹幕',
            type: '弹幕射击',
            cat: 'action',
            diff: 94,
            rating: 8.8,
            tags: ['弹幕', '三阶段 Boss', '高难'],
            desc: '弹幕密度与三阶段 Boss 的双重压顶，十五款既有作品里难度最高的一款。'
        },
        {
            file: 'xiyou-baiguling.html',
            title: '白虎岭 · 三打白骨精',
            type: '横版动作',
            cat: 'action',
            diff: 90,
            rating: 9.1,
            tags: ['近战', '三变', '动作'],
            desc: '近战贴身与白骨夫人三变，最完整的动作骨架，也是既有作品里评测最高的一款。'
        },
        {
            file: 'xiyou-yaochi.html',
            title: '夜探瑶池',
            type: '潜行',
            cat: 'action',
            diff: 86,
            rating: 8.6,
            tags: ['潜行', '视野', '紧张'],
            desc: '被看见就掉护体，十五款既有作品里最紧张的一款。'
        },
        {
            file: 'xiyou-huangfengling.html',
            title: '黄风岭 · 守关塔防',
            type: '塔防',
            cat: 'strategy',
            diff: 81,
            rating: 8.4,
            tags: ['塔防', '经济', '十波'],
            desc: '十波妖潮与经济账，最需要规划的一款。'
        },
        {
            file: 'xiyou-qujingpai.html',
            title: '取经牌途',
            type: '卡牌构筑',
            cat: 'cards',
            diff: 78,
            rating: 8.6,
            tags: ['构筑', '抽牌', '费用'],
            desc: '五场牌局，抽牌与费用之间的取舍。'
        },
        {
            file: 'xiyou-zhenhuoshi.html',
            title: '镇火石',
            type: '推箱子',
            cat: 'strategy',
            diff: 75,
            rating: 8.3,
            tags: ['推箱', '空间', '四石'],
            desc: '四石归台的最后一关，最费脑的一款。'
        },
        {
            file: 'xiyou-pingdingshan.html',
            title: '平顶山 · 蟠桃三消',
            type: '三消',
            cat: 'puzzle',
            diff: 71,
            rating: 8.0,
            tags: ['三消', '倒计时', '随机'],
            desc: '随机盘面与妖王倒计时，运气占一半。'
        },
        {
            file: 'xiyou-wuxingzhen.html',
            title: '五行阵',
            type: '路线解谜',
            cat: 'puzzle',
            diff: 67,
            rating: 8.1,
            tags: ['相生', '门锁', '路线'],
            desc: '相生顺序与门锁，走错就要绕路。'
        },
        {
            file: 'xiyou-fabaolianxiao.html',
            title: '法宝连消',
            type: '连连看',
            cat: 'puzzle',
            diff: 63,
            rating: 7.7,
            tags: ['连连看', '限时', '寻路'],
            desc: '限时清盘，两折寻路考验眼力。'
        },
        {
            file: 'xiyou-jingjuan.html',
            title: '经卷归位',
            type: '滑块拼图',
            cat: 'puzzle',
            diff: 60,
            rating: 7.4,
            tags: ['滑块', '5×5', '推理'],
            desc: '5×5 滑块的耐力与空间推理。'
        },
        {
            file: 'xiyou-pantaoyuan.html',
            title: '蟠桃园',
            type: '经营模拟',
            cat: 'strategy',
            diff: 56,
            rating: 8.1,
            tags: ['经营', '取舍', '十二天'],
            desc: '十二天凑三十枚，取舍比手速重要。'
        },
        {
            file: 'xiyou-jindouyun.html',
            title: '筋斗云',
            type: '无尽跑酷',
            cat: 'action',
            diff: 53,
            rating: 7.7,
            tags: ['跑酷', '无尽', '反应'],
            desc: '速度递增与三命，纯反应型。'
        },
        {
            file: 'xiyou-qiandeng.html',
            title: '千灯阵',
            type: '点灯解谜',
            cat: 'puzzle',
            diff: 47,
            rating: 7.5,
            tags: ['点灯', '十字翻转', '低压力'],
            desc: '十字翻转，规则优雅、压力很低。'
        },
        {
            file: 'xiyou-ganluyin.html',
            title: '甘露引',
            type: '接水管',
            cat: 'puzzle',
            diff: 43,
            rating: 7.2,
            tags: ['接水管', '转管', '试错'],
            desc: '转管接通，试错成本最低。'
        },
        {
            file: 'xiyou-tongtianhe.html',
            title: '通天河钓月',
            type: '钓鱼',
            cat: 'casual',
            diff: 36,
            rating: 7.8,
            tags: ['钓鱼', '放松', '无失败'],
            desc: '没有失败条件，只有收放与收获。'
        }
    ];

    var state = { cat: 'all', q: '', sort: 'default' };

    var els = {};

    function catOf(id) {
        for (var i = 0; i < CATS.length; i += 1) {
            if (CATS[i].id === id) return CATS[i];
        }
        return CATS[0];
    }

    function countOf(id) {
        if (id === 'all') return GAMES.length;
        return GAMES.filter(function (g) { return g.cat === id; }).length;
    }

    var LAST_KEY = 'xy_trials_last';

    function readBest(g) {
        if (!g.bestKey) return '';
        var v = 0;
        try {
            v = Number(window.localStorage.getItem(g.bestKey) || 0);
        } catch (e) {
            v = 0;
        }
        if (!v) return '最佳 · 未开局';
        if (g.bestKind === 'stage') return '最佳 · 已过 ' + v + ' 阵';
        return '最佳 · ' + v.toLocaleString('zh-CN') + ' 分';
    }

    function remember(g) {
        try {
            window.localStorage.setItem(LAST_KEY, JSON.stringify({
                file: g.file,
                title: g.title,
                ts: Date.now()
            }));
        } catch (e) {
            /* 忽略 */
        }
    }

    function renderRecent() {
        if (!els.recent || !els.recentLink) return;
        var raw = null;
        try {
            raw = window.localStorage.getItem(LAST_KEY);
        } catch (e) {
            raw = null;
        }
        if (!raw) {
            els.recent.hidden = true;
            return;
        }
        var data = null;
        try {
            data = JSON.parse(raw);
        } catch (e) {
            data = null;
        }
        if (!data || !data.file || !data.title) {
            els.recent.hidden = true;
            return;
        }
        els.recent.hidden = false;
        els.recentLink.href = data.file;
        els.recentLink.textContent = '继续「' + data.title + '」 →';
    }

    function buildFilters() {
        els.filters.innerHTML = '';
        CATS.forEach(function (cat) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'hub-filter';
            btn.setAttribute('data-cat', cat.id);
            btn.setAttribute('aria-pressed', state.cat === cat.id ? 'true' : 'false');
            btn.textContent = cat.label;
            var n = document.createElement('span');
            n.className = 'n';
            n.textContent = String(countOf(cat.id));
            btn.appendChild(n);
            btn.addEventListener('click', function () {
                state.cat = cat.id;
                buildFilters();
                render();
            });
            els.filters.appendChild(btn);
        });
    }

    function filtered() {
        var q = state.q.trim().toLowerCase();
        var list = GAMES.filter(function (g) {
            if (state.cat !== 'all' && g.cat !== state.cat) return false;
            if (!q) return true;
            var hay = (g.title + ' ' + g.type + ' ' + g.tags.join(' ') + ' ' + g.desc).toLowerCase();
            return hay.indexOf(q) >= 0;
        });
        list.sort(function (a, b) {
            if (state.sort === 'diff') {
                return (b.diff == null ? -1 : b.diff) - (a.diff == null ? -1 : a.diff);
            }
            if (state.sort === 'rating') {
                return (b.rating == null ? -1 : b.rating) - (a.rating == null ? -1 : a.rating);
            }
            if (state.sort === 'name') {
                return a.title.localeCompare(b.title, 'zh-Hans-CN');
            }
            var na = a.isNew ? 1 : 0;
            var nb = b.isNew ? 1 : 0;
            if (na !== nb) return nb - na;
            return (b.diff || 0) - (a.diff || 0);
        });
        return list;
    }

    function buildCard(g) {
        var cat = catOf(g.cat);
        var card = document.createElement('a');
        card.className = 'game-card';
        card.href = g.file;
        card.setAttribute('data-cat', g.cat);
        card.style.setProperty('--cat-color', cat.color);

        if (g.isNew) {
            var badge = document.createElement('span');
            badge.className = 'game-new';
            badge.textContent = '新作';
            card.appendChild(badge);
        }

        var catChip = document.createElement('span');
        catChip.className = 'game-cat cat-' + g.cat;
        catChip.textContent = cat.label;
        card.appendChild(catChip);

        var title = document.createElement('h2');
        title.textContent = g.title;
        card.appendChild(title);

        var type = document.createElement('p');
        type.className = 'game-type';
        type.textContent = g.type;
        card.appendChild(type);

        var desc = document.createElement('p');
        desc.className = 'game-desc';
        desc.textContent = g.desc;
        card.appendChild(desc);

        var meta = document.createElement('div');
        meta.className = 'game-meta';
        if (g.diff == null) {
            var newLabel = document.createElement('span');
            newLabel.className = 'game-diff is-new';
            newLabel.textContent = '新作 · 未评级';
            meta.appendChild(newLabel);
        } else {
            var diff = document.createElement('span');
            diff.className = 'game-diff';
            var bar = document.createElement('i');
            bar.style.setProperty('--v', String(g.diff));
            diff.appendChild(bar);
            var txt = document.createElement('b');
            txt.textContent = '难度 ' + g.diff;
            diff.appendChild(txt);
            meta.appendChild(diff);
            var rating = document.createElement('span');
            rating.className = 'game-rating';
            rating.textContent = '评测 ' + g.rating.toFixed(1);
            meta.appendChild(rating);
        }
        card.appendChild(meta);

        var tags = document.createElement('div');
        tags.className = 'game-tags';
        g.tags.forEach(function (t) {
            var tag = document.createElement('span');
            tag.textContent = '#' + t;
            tags.appendChild(tag);
        });
        card.appendChild(tags);

        if (g.bestKey) {
            var record = document.createElement('div');
            record.className = 'game-record';
            record.textContent = readBest(g);
            card.appendChild(record);
        }

        var go = document.createElement('span');
        go.className = 'game-go';
        go.textContent = '进入 →';
        card.appendChild(go);

        card.addEventListener('click', function () {
            remember(g);
        });

        return card;
    }

    function render() {
        var list = filtered();
        els.grid.innerHTML = '';
        list.forEach(function (g) {
            els.grid.appendChild(buildCard(g));
        });
        els.count.textContent = '显示 ' + list.length + ' / ' + GAMES.length + ' 款';
        els.empty.hidden = list.length > 0;
    }

    function init() {
        els.filters = document.getElementById('hub-filters');
        els.grid = document.getElementById('hub-grid');
        els.count = document.getElementById('hub-count');
        els.empty = document.getElementById('hub-empty');
        els.recent = document.getElementById('hub-recent');
        els.recentLink = document.getElementById('hub-recent-link');
        els.search = document.getElementById('hub-search');
        els.sort = document.getElementById('hub-sort');
        els.random = document.getElementById('hub-random');

        buildFilters();
        render();
        renderRecent();

        els.search.addEventListener('input', function () {
            state.q = els.search.value;
            render();
        });
        els.sort.addEventListener('change', function () {
            state.sort = els.sort.value;
            render();
        });
        els.random.addEventListener('click', function () {
            var list = filtered();
            if (!list.length) return;
            var pick = list[Math.floor(Math.random() * list.length)];
            window.location.href = pick.file;
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === '/' && document.activeElement !== els.search) {
                e.preventDefault();
                els.search.focus();
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
