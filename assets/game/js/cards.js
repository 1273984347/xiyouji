/* 取经三试 · 第三试「卡牌斗法」· 回合制 DOM 战斗 */
(function () {
    'use strict';

    var XG = window.XG;
    var BEST_KEY = 'xy_trials_cards_best';
    var OPPONENTS = ['白骨精', '红孩儿', '六耳猕猴', '牛魔王', '二郎神杨戬'];
    var MULT = [0.82, 0.92, 1.0, 1.03, 1.05];
    var ELEM_BEAT = { '金': '木', '木': '土', '土': '水', '水': '火', '火': '金' };

    var els = {};
    var B = null;
    var cards = [];
    var best = 0;

    function setText(el, text) {
        if (el && el.textContent !== String(text)) el.textContent = String(text);
    }

    function normalize(card, mult) {
        var m = mult || 1;
        var maxHp = Math.round((90 + card.hp / 10000 * 80) * m);
        return {
            name: card.character,
            title: card.title,
            rarity: card.rarity,
            element: card.element,
            power: card.power,
            maxHp: maxHp,
            hp: maxHp,
            atk: Math.round((11 + card.atk / 10000 * 15) * m),
            def: Math.round((4 + card.def / 10000 * 7) * m),
            spd: Math.round(card.spd / 1000),
            skills: (card.skills || []).slice(0, 4).map(function (s) {
                return {
                    name: s.name,
                    cost: XG.clamp(Math.ceil((s.cost || 1) / 3), 1, 3),
                    effect: s.effect,
                    type: s.type
                };
            }),
            passive: card.passive || '',
            lore: card.lore || '',
            guard: false,
            dodgeTurns: 0,
            atkBuffTurns: 0,
            atkBuff: 1,
            firstShield: card.character === '孙悟空',
            firstShieldUsed: false,
            reviveUsed: false,
            enraged: false
        };
    }

    function buildOrder() {
        var first = XG.shuffle(OPPONENTS.slice(0, OPPONENTS.length - 1));
        first.push(OPPONENTS[OPPONENTS.length - 1]);
        return first;
    }

    function gradeOf(card) {
        if (card.power >= 9000) return '难度：易';
        if (card.power >= 7000) return '难度：中';
        if (card.power >= 3000) return '难度：难';
        return '难度：极难';
    }

    function renderSelect() {
        if (!els.grid) return;
        els.grid.innerHTML = '';
        cards.forEach(function (card) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'cf-char';
            var top = document.createElement('div');
            top.className = 'top';
            var name = document.createElement('span');
            name.className = 'name';
            name.textContent = card.character;
            var rarity = document.createElement('span');
            rarity.className = 'rarity';
            rarity.textContent = card.rarity;
            top.appendChild(name);
            top.appendChild(rarity);
            var title = document.createElement('div');
            title.className = 'title';
            title.textContent = card.title + ' · ' + card.element;
            var stats = document.createElement('div');
            stats.className = 'stats';
            stats.textContent = '战力 ' + XG.fmt(card.power) + ' · HP ' + card.hp + ' · ATK ' + card.atk + ' · DEF ' + card.def;
            var grade = document.createElement('div');
            grade.className = 'grade';
            grade.textContent = gradeOf(card);
            btn.appendChild(top);
            btn.appendChild(title);
            btn.appendChild(stats);
            btn.appendChild(grade);
            if (card.skills && card.skills.length) {
                btn.title = card.skills.map(function (s) {
                    return s.name + '：' + s.effect;
                }).join('\n');
            }
            btn.addEventListener('click', function () {
                startGauntlet(card);
            });
            els.grid.appendChild(btn);
        });
    }

    function startGauntlet(card) {
        XG.audio.play('click');
        var player = normalize(card, 1);
        if (player.name === '牛魔王') player.maxHp = Math.round(player.maxHp * 1.15);
        player.hp = player.maxHp;
        if (els.select) els.select.hidden = true;
        if (els.battle) els.battle.hidden = false;
        if (els.restart) els.restart.hidden = false;
        if (els.end) els.end.hidden = true;
        B = {
            player: player,
            enemy: null,
            stage: 0,
            order: buildOrder(),
            energy: 3,
            round: 1,
            log: [],
            busy: false,
            over: false,
            turn: 'player',
            enemySkip: false,
            token: (B && B.token ? B.token : 0) + 1
        };
        if (player.name === '白龙马') B.energy = 5;
        addLog('斗法开始：' + player.name + ' 对上白骨精。', true);
        spawnEnemy(0);
    }

    function spawnEnemy(stage) {
        var card = null;
        var targetName = B.order[stage];
        for (var i = 0; i < cards.length; i += 1) {
            if (cards[i].character === targetName) {
                card = cards[i];
                break;
            }
        }
        if (!card) card = cards[cards.length - 1];
        var e = normalize(card, MULT[stage]);
        B.enemy = e;
        B.stage = stage;
        B.energy = Math.max(B.energy, 3);
        B.round = 1;
        B.turn = 'player';
        B.busy = false;
        B.enemySkip = false;
        B.player.guard = false;
        B.player.atkBuffTurns = 0;
        B.player.atkBuff = 1;
        B.player.dodgeTurns = 0;
        addLog('第 ' + (stage + 1) + ' 阵：' + e.name + '（' + e.title + '）拦住去路。', true);
        renderBattle();
    }

    function addLog(text, hl) {
        if (!B) return;
        B.log.push({ text: text, hl: !!hl });
        if (B.log.length > 30) B.log.shift();
        renderLog();
    }

    function renderLog() {
        if (!els.log || !B) return;
        els.log.innerHTML = '';
        B.log.slice(-8).forEach(function (line) {
            var div = document.createElement('div');
            if (line.hl) div.className = 'hl';
            div.style.color = line.hl ? 'var(--accent-primary)' : '';
            div.textContent = line.text;
            els.log.appendChild(div);
        });
        els.log.scrollTop = els.log.scrollHeight;
    }

    function renderFighter(box, f, isEnemy) {
        if (!box || !f) return;
        var who = box.querySelector('.who strong');
        var sub = box.querySelector('.who span');
        var bar = box.querySelector('.cf-hp i');
        var nums = box.querySelectorAll('.cf-num span');
        setText(who, f.name);
        setText(sub, f.title + ' · ' + f.element);
        if (bar) bar.style.width = (XG.clamp(f.hp / f.maxHp, 0, 1) * 100).toFixed(1) + '%';
        if (nums && nums.length >= 2) {
            setText(nums[0], 'HP');
            setText(nums[1], Math.max(0, Math.ceil(f.hp)) + ' / ' + f.maxHp);
        }
    }

    function elementMult(atkElem, defElem) {
        if (ELEM_BEAT[atkElem] === defElem) return 1.25;
        if (ELEM_BEAT[defElem] === atkElem) return 0.85;
        return 1;
    }

    function damageOf(src, tgt, mult) {
        var base = src.atk * mult * elementMult(src.element, tgt.element);
        return Math.max(1, Math.round(base - tgt.def * 0.5));
    }

    function playerDamageMult() {
        var m = 1;
        if (B.player.name === '如来佛祖' || B.player.name === '红孩儿') m *= 1.1;
        if (B.player.name === '二郎神') m *= 1.2;
        if (B.player.atkBuffTurns > 0) m *= B.player.atkBuff;
        return m;
    }

    function takePlayerDamage(amount) {
        var p = B.player;
        if (p.name === '孙悟空' && !p.firstShieldUsed) {
            p.firstShieldUsed = true;
            addLog('大闹天宫被动：首次受击免疫。');
            return 0;
        }
        if (p.name === '白骨精' && Math.random() < 0.15) {
            addLog('解尸法：白骨精闪过这一击。');
            return 0;
        }
        if (p.guard) {
            amount = Math.round(amount * 0.5);
            p.guard = false;
        }
        if (p.name === '猪八戒') amount = Math.round(amount * 0.85);
        return Math.max(1, amount);
    }

    function parseMult(text) {
        var m = String(text).match(/×\s*(\d+(?:\.\d+)?)/);
        if (!m) return 1.2;
        var v = parseFloat(m[1]);
        if (v >= 3) return 2.1;
        if (v >= 2.5) return 1.8;
        if (v >= 1.8) return 1.4;
        return 1.25;
    }

    function parseHeal(text) {
        var m = String(text).match(/(\d+)\s*%/);
        return m ? Math.min(0.6, parseInt(m[1], 10) / 100) : 0.2;
    }

    function renderEnergy() {
        if (!els.actions || !B) return;
        var wrap = document.createElement('div');
        wrap.className = 'cf-energy';
        var label = document.createElement('span');
        label.textContent = '能量 ' + B.energy + '/6';
        wrap.appendChild(label);
        for (var i = 0; i < 6; i += 1) {
            var dot = document.createElement('i');
            if (i < B.energy) dot.className = 'on';
            wrap.appendChild(dot);
        }
        els.actions.appendChild(wrap);
    }

    function actionButton(label, note, disabled, fn) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'tr-btn';
        btn.disabled = disabled;
        btn.textContent = label + (note ? ' · ' + note : '');
        btn.addEventListener('click', fn);
        return btn;
    }

    function renderSkillList() {
        if (!els.skillList || !B) return;
        els.skillList.innerHTML = '';
        B.player.skills.forEach(function (skill) {
            var line = document.createElement('div');
            var name = document.createElement('b');
            name.textContent = skill.name;
            line.appendChild(name);
            line.appendChild(document.createTextNode(' · ' + skill.effect));
            els.skillList.appendChild(line);
        });
    }

    function renderActions() {
        if (!els.actions || !B) return;
        els.actions.innerHTML = '';
        renderSkillList();
        renderEnergy();
        if (B.over || B.turn !== 'player' || B.busy) return;

        els.actions.appendChild(actionButton('普攻', '回能 +1', false, function () { playerAct('attack'); }));
        B.player.skills.forEach(function (skill, idx) {
            var disabled = B.energy < skill.cost;
            els.actions.appendChild(actionButton(skill.name, '耗能 ' + skill.cost, disabled, function () { playerAct('skill', idx); }));
        });
        els.actions.appendChild(actionButton('防御', '减伤 50%', false, function () { playerAct('guard'); }));
        els.actions.appendChild(actionButton('调息', '回血 8%', false, function () { playerAct('rest'); }));
    }

    function renderBattle() {
        if (!B) return;
        renderFighter(els.playerBox, B.player, false);
        renderFighter(els.enemyBox, B.enemy, true);
        renderActions();
    }

    function playerAct(kind, idx) {
        if (!B || B.over || B.busy || B.turn !== 'player') return;
        B.busy = true;
        var p = B.player;
        var e = B.enemy;

        if (kind === 'attack') {
            XG.audio.play('swing');
            var dmg = Math.round(damageOf(p, e, 1 * playerDamageMult()));
            e.hp -= dmg;
            B.energy = Math.min(6, B.energy + 1);
            addLog('你挥棒普攻，造成 ' + dmg + ' 点伤害。');
        } else if (kind === 'guard') {
            p.guard = true;
            B.energy = Math.min(6, B.energy + 1);
            addLog('你收棒护身，本回合受伤减半。');
        } else if (kind === 'rest') {
            var heal = Math.max(1, Math.round(p.maxHp * 0.15));
            p.hp = Math.min(p.maxHp, p.hp + heal);
            B.energy = Math.min(6, B.energy + 1);
            addLog('你调息运气，回复 ' + heal + ' 点体力。');
        } else if (kind === 'skill') {
            var skill = p.skills[idx];
            if (!skill || B.energy < skill.cost || !e) {
                B.busy = false;
                return;
            }
            B.energy -= skill.cost;
            useSkill(skill);
        }

        renderBattle();
        if (!e || e.hp <= 0) {
            e.hp = Math.max(0, e.hp);
            renderBattle();
            addLog(e.name + ' 倒下了。', true);
            var token = B.token;
            setTimeout(function () {
                if (!B || B.token !== token) return;
                advanceStage();
            }, 650);
            return;
        }
        var token2 = B.token;
        setTimeout(function () {
            if (!B || B.token !== token2) return;
            enemyTurn();
        }, 560);
    }

    function useSkill(skill) {
        var p = B.player;
        var e = B.enemy;
        var text = skill.effect || '';
        addLog('你施展「' + skill.name + '」。');

        if (skill.type === 'attack') {
            var dmg = Math.round(damageOf(p, e, parseMult(text) * playerDamageMult()));
            e.hp -= dmg;
            addLog('「' + skill.name + '」命中，造成 ' + dmg + ' 点伤害。');
            if (text.indexOf('破防') >= 0) {
                e.def = Math.max(1, Math.round(e.def * 0.85));
                addLog(e.name + ' 的防御被削弱。');
            }
        } else if (skill.type === 'heal') {
            var pct = parseHeal(text);
            var heal = Math.max(1, Math.round(p.maxHp * pct));
            p.hp = Math.min(p.maxHp, p.hp + heal);
            addLog('回复 ' + heal + ' 点体力。');
            if (text.indexOf('解除') >= 0 || text.indexOf('净化') >= 0) {
                p.atkBuffTurns = 0;
                addLog('负面状态被净化。');
            }
        } else if (skill.type === 'buff') {
            if (text.indexOf('回避') >= 0 || text.indexOf('变形') >= 0) {
                p.dodgeTurns = 3;
                addLog('身形变化，三回合内有闪避机会。');
            } else {
                p.atkBuff = 1.25;
                p.atkBuffTurns = 3;
                addLog('气势上扬，三回合内攻击 +25%。');
            }
        } else if (skill.type === 'control') {
            B.enemySkip = true;
            addLog(e.name + ' 被定住，下一回合无法行动。');
        } else if (skill.type === 'move') {
            B.energy = Math.min(6, B.energy + 1);
            var mdmg = Math.round(damageOf(p, e, 0.8 * playerDamageMult()));
            e.hp -= mdmg;
            addLog('先手抢攻，造成 ' + mdmg + ' 点伤害，回能 +1。');
        } else {
            if (text.indexOf('识破') >= 0 || text.indexOf('看穿') >= 0) {
                e.def = Math.max(1, Math.round(e.def * 0.8));
                addLog('你看破虚实，' + e.name + ' 防御下降。');
            } else {
                B.energy = Math.min(6, B.energy + 1);
                addLog('你稳住阵脚，回能 +1。');
            }
        }
    }

    function enemyTurn() {
        if (!B || B.over) return;
        B.turn = 'enemy';
        B.busy = true;
        var p = B.player;
        var e = B.enemy;
        if (!e || !p) return;

        // 被动回复
        if (p.name === '观音菩萨') {
            p.hp = Math.min(p.maxHp, p.hp + Math.round(p.maxHp * 0.05));
        } else if (p.name === '沙悟净') {
            p.hp = Math.min(p.maxHp, p.hp + Math.round(p.maxHp * 0.03));
        }

        if (B.enemySkip) {
            B.enemySkip = false;
            addLog(e.name + ' 动弹不得，这一回合被跳过。');
            endEnemyTurn();
            return;
        }

        if (!e.enraged && e.hp / e.maxHp < 0.3) {
            e.enraged = true;
            e.atk = Math.round(e.atk * 1.25);
            addLog(e.name + ' 困兽犹斗，攻击提升。', true);
        }

        var special = B.round % 3 === 0;
        var specialMult = special ? 1.5 : 1;
        if (special && e.name === '二郎神杨戬') {
            specialMult = 1.6;
            p.atkBuffTurns = 0;
            p.atkBuff = 1;
            addLog('二郎神 开天眼，破除你的增益。');
        }
        var dmg = Math.round(damageOf(e, p, specialMult));
        if (p.name === '白骨精' && p.dodgeTurns > 0) {
            p.dodgeTurns -= 1;
            addLog('你借着变化身法避开了攻击。');
            endEnemyTurn();
            return;
        }
        dmg = takePlayerDamage(dmg);
        if (dmg === 0) {
            endEnemyTurn();
            return;
        }
        XG.audio.play('hurt');
        p.hp -= dmg;
        addLog(e.name + (special ? ' 使出杀招' : ' 出手') + '，你受到 ' + dmg + ' 点伤害。');

        if (p.hp <= 0) {
            if (p.name === '唐三藏' && !p.reviveUsed) {
                p.reviveUsed = true;
                p.hp = 1;
                addLog('金蝉子护体：你以 1 点体力撑住。', true);
            } else {
                p.hp = 0;
                finish(false);
                return;
            }
        }
        endEnemyTurn();
    }

    function endEnemyTurn() {
        if (!B || B.over) return;
        var p = B.player;
        if (p.name === '六耳猕猴') p.atk = Math.round(p.atk * 1.04);
        if (p.atkBuffTurns > 0) p.atkBuffTurns -= 1;
        if (p.guard) p.guard = false;
        B.round += 1;
        B.energy = Math.min(6, B.energy + 1);
        B.turn = 'player';
        B.busy = false;
        renderBattle();
    }

    function advanceStage() {
        if (!B || B.over) return;
        if (B.stage >= OPPONENTS.length - 1) {
            finish(true);
            return;
        }
        var heal = B.player.maxHp - B.player.hp;
        B.player.hp = B.player.maxHp;
        addLog('阵间调息，体力回满（+' + heal + '）。');
        var next = B.stage + 1;
        var token = B.token;
        setTimeout(function () {
            if (!B || B.token !== token) return;
            spawnEnemy(next);
        }, 450);
    }

    function finish(won) {
        if (!B || B.over) return;
        XG.audio.play(won ? 'win' : 'lose');
        B.over = true;
        B.busy = false;
        B.turn = 'none';
        var cleared = won ? OPPONENTS.length : B.stage;
        if (cleared > best) {
            best = cleared;
            XG.storage.set(BEST_KEY, best);
        }
        if (els.end) {
            els.end.hidden = false;
            els.end.innerHTML = '';
            var h = document.createElement('h4');
            h.textContent = won ? '五阵皆胜' : '斗法止步';
            var p = document.createElement('p');
            p.textContent = (won ? '五张妖王卡都被你打过，取经路再通一段。' : '你倒在第 ' + (B.stage + 1) + ' 阵。') +
                ' 已过 ' + cleared + ' / ' + OPPONENTS.length + ' 阵 · 最高 ' + best + ' 阵';
            els.end.appendChild(h);
            els.end.appendChild(p);
        }
        addLog(won ? '五阵皆胜。' : '斗法止步。', true);
        renderActions();
    }

    function onKeyDown(e) {
        var panel = document.getElementById('panel-cards');
        if (!panel || panel.hidden || !B || B.over || B.busy || B.turn !== 'player') return;
        if (e.key === 'r' || e.key === 'R') {
            if (els.restart) els.restart.click();
            return;
        }
        var n = Number(e.key);
        if (!n || n < 1 || n > 6) return;
        var buttons = els.actions ? els.actions.querySelectorAll('button') : [];
        var target = buttons[n - 1];
        if (target && !target.disabled) {
            e.preventDefault();
            target.click();
        }
    }

    function resetToSelect() {
        B = null;
        if (els.select) els.select.hidden = false;
        if (els.battle) els.battle.hidden = true;
        if (els.end) els.end.hidden = true;
        if (els.restart) els.restart.hidden = true;
    }

    function init() {
        els = {
            grid: document.getElementById('cf-grid'),
            select: document.getElementById('cf-select'),
            battle: document.getElementById('cf-battle'),
            playerBox: document.getElementById('cf-player'),
            enemyBox: document.getElementById('cf-enemy'),
            actions: document.getElementById('cf-actions'),
            skillList: document.getElementById('cf-skill-list'),
            log: document.getElementById('cf-log'),
            end: document.getElementById('cf-end'),
            restart: document.getElementById('cf-restart')
        };
        cards = XG.loadData().cards;
        best = XG.storage.get(BEST_KEY, 0);
        if (!cards.length) {
            if (els.grid) els.grid.textContent = '角色卡数据未载入。';
            return;
        }
        renderSelect();
        if (els.restart) {
            els.restart.addEventListener('click', resetToSelect);
        }
        document.addEventListener('keydown', onKeyDown);
    }

    XG.registerMode('cards', {
        init: init,
        pause: function () {}
    });
})();
