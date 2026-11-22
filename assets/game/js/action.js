/* 取经三试 · 第一试「护师西行」· Canvas 2D 横版动作（零依赖） */
(function () {
    'use strict';

    var XG = window.XG;
    var W = 960;
    var H = 540;
    var GY = 430;
    var BEST_KEY = 'xy_trials_action_best';
    var HARD = { hp: 1.4, dmg: 1.3, speed: 1.12, taken: 1.25, score: 1.5 };

    var STAGES = [
        {
            id: 'baihuling',
            name: '第一试 · 白虎岭',
            bossName: '白骨精',
            bossType: 'bone',
            len: 2100,
            speed: 48,
            bossAt: 1400,
            waves: [
                { x: 240, type: 'walker', n: 2 },
                { x: 560, type: 'flyer', n: 2 },
                { x: 880, type: 'walker', n: 3 },
                { x: 1160, type: 'archer', n: 1, extra: 'walker', extraN: 2 },
                { x: 1320, type: 'flyer', n: 2 }
            ]
        },
        {
            id: 'huoyundong',
            name: '第二试 · 火云洞',
            bossName: '红孩儿',
            bossType: 'fire',
            len: 2300,
            speed: 48,
            bossAt: 1560,
            waves: [
                { x: 240, type: 'walker', n: 2 },
                { x: 560, type: 'archer', n: 2 },
                { x: 900, type: 'flyer', n: 3 },
                { x: 1200, type: 'walker', n: 2, extra: 'archer', extraN: 1 },
                { x: 1450, type: 'flyer', n: 2, extra: 'walker', extraN: 1 }
            ]
        },
        {
            id: 'huoyanshan',
            name: '第三试 · 火焰山',
            bossName: '牛魔王',
            bossType: 'bull',
            len: 2500,
            speed: 48,
            bossAt: 1760,
            waves: [
                { x: 280, type: 'walker', n: 3 },
                { x: 640, type: 'archer', n: 2, extra: 'flyer', extraN: 1 },
                { x: 1000, type: 'walker', n: 4 },
                { x: 1360, type: 'flyer', n: 2, extra: 'archer', extraN: 2 },
                { x: 1660, type: 'walker', n: 3 }
            ]
        }
    ];

    var canvas = null;
    var ctx = null;
    var els = {};
    var keys = {};
    var lastTs = 0;
    var rafId = 0;

    var state = {
        active: false,
        mode: 'ready',
        stage: 0,
        cam: 0,
        monk: null,
        player: null,
        enemies: [],
        boss: null,
        shots: [],
        zones: [],
        parts: [],
        floats: [],
        waveIndex: 0,
        bossSpawned: false,
        combo: 0,
        comboT: 0,
        score: 0,
        stageStartScore: 0,
        shake: 0,
        hitStop: 0,
        best: 0,
        stageT: 0,
        hard: false,
        endless: false,
        loop: 0
    };

    function addScore(n) {
        var mult = (state.hard ? HARD.score : 1) * (state.endless ? 1 + (state.loop - 1) * 0.25 : 1);
        state.score += Math.round(n * mult);
    }

    function setText(el, txt) {
        if (el && el.textContent !== String(txt)) el.textContent = String(txt);
    }

    function panelVisible() {
        var panel = document.getElementById('panel-action');
        return panel && !panel.hidden;
    }

    function overlay(eyebrow, title, body, buttons) {
        var box = els.overlay;
        if (!box) return;
        box.classList.remove('is-hidden');
        box.innerHTML = '';
        var e = document.createElement('div');
        e.className = 'eyebrow';
        e.textContent = eyebrow;
        var h = document.createElement('h4');
        h.textContent = title;
        var p = document.createElement('p');
        p.textContent = body;
        var row = document.createElement('div');
        row.className = 'tr-btn-row';
        buttons.forEach(function (b) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'tr-btn' + (b.primary ? ' tr-btn-primary' : '');
            btn.textContent = b.label;
            btn.addEventListener('click', b.onClick);
            row.appendChild(btn);
        });
        box.appendChild(e);
        box.appendChild(h);
        box.appendChild(p);
        if (buttons.length) box.appendChild(row);
    }

    function hideOverlay() {
        if (els.overlay) els.overlay.classList.add('is-hidden');
    }

    function makePlayer(x) {
        return {
            x: x,
            y: GY - 64,
            vx: 0,
            vy: 0,
            w: 34,
            h: 64,
            hp: 100,
            maxHp: 100,
            onGround: true,
            jumps: 0,
            face: 1,
            atk: 0,
            atkCd: 0,
            dash: 0,
            dashCd: 0,
            inv: 0,
            hitT: 0,
            attackDone: false
        };
    }

    function makeEnemy(type, x) {
        var e;
        if (type === 'flyer') {
            e = { type: type, x: x, y: 220, w: 36, h: 30, hp: 48, maxHp: 48, speed: 122, dmg: 8, mdmg: 6, score: 140, fly: true, baseY: 220, t: XG.rand(0, 6), hitT: 0, atkCd: 0 };
        } else if (type === 'archer') {
            e = { type: type, x: x, y: GY - 48, w: 30, h: 48, hp: 52, maxHp: 52, speed: 46, dmg: 8, mdmg: 7, score: 160, ranged: true, shoot: XG.rand(0.8, 1.8), t: 0, hitT: 0, atkCd: 0 };
        } else {
            e = { type: 'walker', x: x, y: GY - 46, w: 34, h: 46, hp: 62, maxHp: 62, speed: 88, dmg: 10, mdmg: 8, score: 120, t: XG.rand(0, 6), hitT: 0, atkCd: 0 };
        }
        if (state.hard) {
            e.hp = Math.round(e.hp * HARD.hp);
            e.maxHp = e.hp;
            e.dmg = Math.round(e.dmg * HARD.dmg);
            e.mdmg = Math.round(e.mdmg * HARD.dmg);
            e.speed *= HARD.speed;
        }
        if (state.endless && state.loop > 1) {
            e.hp = Math.round(e.hp * (1 + (state.loop - 1) * 0.18));
            e.maxHp = e.hp;
            e.dmg = Math.round(e.dmg * (1 + (state.loop - 1) * 0.1));
            e.mdmg = Math.round(e.mdmg * (1 + (state.loop - 1) * 0.1));
            e.speed *= 1 + (state.loop - 1) * 0.05;
        }
        e.dead = false;
        return e;
    }

    function spawnBoss(type, x) {
        var cfg = {
            bone: { w: 54, h: 78, hp: 470, mdmg: 12 },
            fire: { w: 52, h: 70, hp: 560, mdmg: 10 },
            bull: { w: 88, h: 96, hp: 880, mdmg: 14 }
        }[type];
        if (state.hard) {
            cfg.hp = Math.round(cfg.hp * HARD.hp);
            cfg.mdmg = Math.round(cfg.mdmg * HARD.dmg);
        }
        if (state.endless && state.loop > 1) {
            cfg.hp = Math.round(cfg.hp * (1 + (state.loop - 1) * 0.2));
            cfg.mdmg = Math.round(cfg.mdmg * (1 + (state.loop - 1) * 0.1));
        }
        XG.audio.play('boss');
        state.boss = {
            type: type,
            x: x,
            y: GY - cfg.h,
            w: cfg.w,
            h: cfg.h,
            hp: cfg.hp,
            maxHp: cfg.hp,
            mdmg: cfg.mdmg,
            t: 0,
            cast: 1.4,
            summon: 4.5,
            phase: 1,
            state: 'idle',
            stateT: 0,
            dir: -1,
            vx: 0,
            hitT: 0,
            revealed: false,
            dead: false,
            baseY: GY - cfg.h
        };
        state.shake = 8;
        addFloat(x, 120, '妖王现身', '#C0392B');
    }

    function addPart(x, y, color, n, spread) {
        var count = XG.reduced ? Math.max(1, Math.floor(n / 2)) : n;
        for (var i = 0; i < count; i += 1) {
            state.parts.push({
                x: x,
                y: y,
                vx: XG.rand(-spread, spread),
                vy: XG.rand(-spread, spread * 0.4),
                life: XG.rand(0.3, 0.7),
                max: 0.7,
                r: XG.rand(1.2, 3.4),
                color: color
            });
        }
    }

    function addFloat(x, y, text, color) {
        state.floats.push({ x: x, y: y, text: text, color: color || '#1C1A17', life: 0.9, max: 0.9 });
    }

    function resetStage(idx, keepScore) {
        var cfg = STAGES[idx];
        state.stage = idx;
        state.mode = 'playing';
        state.cam = 0;
        state.stageT = 0;
        state.monk = { x: 120, hp: 100, maxHp: 100, w: 26, h: 58, t: 0, hurt: 0 };
        state.player = makePlayer(180);
        state.enemies = [];
        state.boss = null;
        state.shots = [];
        state.zones = [];
        state.parts = [];
        state.floats = [];
        state.waveIndex = 0;
        state.bossSpawned = false;
        state.combo = 0;
        state.comboT = 0;
        state.shake = 0;
        state.hitStop = 0;
        if (!keepScore) {
            state.score = 0;
            state.stageStartScore = 0;
        } else {
            state.stageStartScore = state.score;
        }
        hideOverlay();
        setText(els.stage, stageLabel(cfg));
        updateHud();
    }

    function stageLabel(cfg) {
        var label = cfg.name;
        if (state.endless) label += ' · 无尽第 ' + state.loop + ' 轮';
        if (state.hard) label += ' · 修罗';
        return label;
    }

    function saveBest() {
        if (state.score > state.best) {
            state.best = state.score;
            XG.storage.set(BEST_KEY, state.best);
        }
    }

    function startGame(hard) {
        state.hard = !!hard;
        state.endless = false;
        state.loop = 0;
        state.score = 0;
        resetStage(0, false);
    }

    function startEndless() {
        state.hard = false;
        state.endless = true;
        state.loop = 1;
        state.score = 0;
        resetStage(0, false);
    }

    function pauseGame() {
        if (state.mode !== 'playing') return;
        state.mode = 'paused';
        overlay('暂停', '歇一歇', '按 Esc 或点继续回到取经路。', [
            { label: '继续', primary: true, onClick: function () { state.mode = 'playing'; hideOverlay(); } },
            { label: '重开本试', onClick: function () { resetStage(state.stage, true); } }
        ]);
    }

    function resumeGame() {
        if (state.mode === 'paused') {
            state.mode = 'playing';
            hideOverlay();
        }
    }

    function lose(reason) {
        if (state.mode !== 'playing') return;
        state.mode = 'lost';
        XG.audio.play('lose');
        state.shake = 10;
        saveBest();
        if (state.endless) {
            overlay('无尽止步', reason + ' · 第 ' + state.loop + ' 轮', '得分 ' + XG.fmt(state.score) + ' · 最高 ' + XG.fmt(state.best), [
                { label: '再入无尽', primary: true, onClick: startEndless },
                { label: '常规模式', onClick: function () { startGame(false); } }
            ]);
            return;
        }
        overlay('本试失败', reason, '得分 ' + XG.fmt(state.score) + ' · 最高 ' + XG.fmt(state.best), [
            { label: '重试本试', primary: true, onClick: function () { state.score = state.stageStartScore; resetStage(state.stage, true); } }
        ]);
    }

    function clearStage() {
        if (state.mode !== 'playing') return;
        state.mode = 'clear';
        XG.audio.play('win');
        addScore(500);
        saveBest();
        if (state.endless) {
            addPart(state.monk.x + 30, 300, '#C0392B', 26, 260);
            updateHud();
            if (state.stage < STAGES.length - 1) {
                overlay('无尽 · 第 ' + state.loop + ' 轮', STAGES[state.stage].name + ' 已过', '当前得分 ' + XG.fmt(state.score), [
                    { label: '进入下一试', primary: true, onClick: function () { resetStage(state.stage + 1, true); } }
                ]);
            } else {
                var nextLoop = state.loop + 1;
                overlay('无尽 · 第 ' + state.loop + ' 轮已过', '下一轮更强', '当前得分 ' + XG.fmt(state.score) + '。妖怪会随轮次变强。', [
                    {
                        label: '进入第 ' + nextLoop + ' 轮',
                        primary: true,
                        onClick: function () {
                            state.loop = nextLoop;
                            resetStage(0, true);
                        }
                    }
                ]);
            }
            return;
        }
        if (state.stage >= STAGES.length - 1) {
            state.mode = 'won';
            overlay('三试皆过', '取经人到了', '总分 ' + XG.fmt(state.score) + ' · 最高 ' + XG.fmt(state.best), [
                { label: '再走一遍', primary: true, onClick: function () { startGame(state.hard); } }
            ]);
        } else {
            overlay('本试已过', STAGES[state.stage].name + ' 已过', '本试得分 ' + XG.fmt(state.score) + '（含过关 +500）', [
                { label: '进入下一试', primary: true, onClick: function () { resetStage(state.stage + 1, true); } }
            ]);
        }
        addPart(state.monk.x + 30, 300, '#C0392B', 26, 260);
        updateHud();
    }

    function damagePlayer(amount, fromX) {
        var p = state.player;
        if (!p || p.inv > 0 || p.dash > 0) return;
        if (state.hard) amount = Math.round(amount * HARD.taken);
        XG.audio.play('hurt');
        p.hp -= amount;
        p.inv = 1.0;
        p.hitT = 0.3;
        if (fromX !== undefined) {
            p.vx = (p.x < fromX ? -1 : 1) * 240;
            p.vy = -180;
        }
        state.shake = 6;
        state.combo = 0;
        addFloat(p.x, p.y - 20, '-' + amount, '#8C2A2A');
        if (p.hp <= 0) {
            p.hp = 0;
            lose('心猿散了');
        }
        updateHud();
    }

    function hurtMonk(amount, fromX) {
        var m = state.monk;
        if (!m) return;
        if (state.hard) amount = Math.round(amount * HARD.taken);
        XG.audio.play('hurt');
        m.hp -= amount;
        m.hurt = 0.35;
        state.shake = 7;
        addFloat(m.x, m.y - 40, '心灯 -' + amount, '#8C2A2A');
        addPart(m.x, GY - 40, '#8C2A2A', 10, 160);
        if (fromX !== undefined) m.x = XG.clamp(m.x - 6, 0, STAGES[state.stage].len - 40);
        if (m.hp <= 0) {
            m.hp = 0;
            lose('心灯灭了');
        }
        updateHud();
    }

    function hitEnemy(e, dmg, dir) {
        XG.audio.play('hit');
        e.hp -= dmg;
        e.hitT = 0.12;
        e.x += dir * 12;
        addPart(e.x, e.y + e.h / 2, '#1C1A17', 7, 120);
        addFloat(e.x, e.y - 10, String(dmg), '#C0392B');
        if (e.hp <= 0 && !e.dead) {
            e.dead = true;
            addScore(e.score);
            addPart(e.x, e.y + e.h / 2, '#8E7D62', 12, 180);
            addFloat(e.x, e.y - 18, '+' + e.score, '#40619E');
        }
    }

    function hitBoss(dmg, dir) {
        var b = state.boss;
        if (!b || b.dead) return;
        XG.audio.play('hit');
        b.hp -= dmg;
        b.hitT = 0.1;
        b.revealed = true;
        addPart(b.x, b.y + b.h * 0.5, '#C0392B', 9, 160);
        addFloat(b.x, b.y - 6, String(dmg), '#C0392B');
        if (b.hp <= 0) {
            b.dead = true;
            addScore(600);
            state.shake = 14;
            addPart(b.x, b.y + b.h * 0.5, '#1C1A17', 40, 300);
            addFloat(b.x, b.y - 20, '+' + 600, '#40619E');
            return;
        }
        var ratio = b.hp / b.maxHp;
        if (b.type === 'bone' && ratio < 0.66 && b.phase === 1) {
            b.phase = 2;
            b.x = XG.clamp(state.monk.x + 380, 120, STAGES[state.stage].len - 80);
            b.revealed = true;
            state.enemies.push(makeEnemy('walker', b.x - 60), makeEnemy('walker', b.x + 60));
            addFloat(b.x, b.y - 30, '一变', '#C0392B');
        } else if (b.type === 'bone' && ratio < 0.33 && b.phase === 2) {
            b.phase = 3;
            b.x = XG.clamp(state.monk.x + 330, 120, STAGES[state.stage].len - 80);
            state.enemies.push(makeEnemy('walker', b.x - 80), makeEnemy('walker', b.x + 80));
            addFloat(b.x, b.y - 30, '三变', '#C0392B');
        }
    }

    function nearestEnemyDist(x) {
        var best = 9999;
        state.enemies.forEach(function (e) {
            if (e.dead) return;
            var d = Math.abs(e.x - x);
            if (d < best) best = d;
        });
        if (state.boss && !state.boss.dead) {
            var d2 = Math.abs(state.boss.x - x);
            if (d2 < best) best = d2;
        }
        return best;
    }

    function updateMonk(dt) {
        var m = state.monk;
        if (!m) return;
        m.t += dt;
        if (m.hurt > 0) m.hurt -= dt;
        var threat = nearestEnemyDist(m.x);
        if (threat > 150) {
            m.x = Math.min(m.x + STAGES[state.stage].speed * dt, STAGES[state.stage].len - 50);
        }
        if (m.x >= STAGES[state.stage].len - 60) {
            var bossAlive = state.boss && !state.boss.dead;
            if (!bossAlive && state.bossSpawned) clearStage();
        }
    }

    function updatePlayer(dt) {
        var p = state.player;
        if (!p) return;
        if (p.atk > 0) p.atk -= dt;
        if (p.atkCd > 0) p.atkCd -= dt;
        if (p.dash > 0) p.dash -= dt;
        if (p.dashCd > 0) p.dashCd -= dt;
        if (p.inv > 0) p.inv -= dt;
        if (p.hitT > 0) p.hitT -= dt;

        var left = keys.left ? 1 : 0;
        var right = keys.right ? 1 : 0;

        if (p.dash > 0) {
            p.vx = p.face * 900;
        } else {
            p.vx = (right - left) * 280;
            if (right) p.face = 1;
            if (left) p.face = -1;
        }

        p.vy += 1900 * dt;
        p.x += p.vx * dt;
        p.y += p.vy * dt;

        var minX = 20;
        var maxX = STAGES[state.stage].len - 30;
        if (p.x < minX) p.x = minX;
        if (p.x > maxX) p.x = maxX;

        if (p.y >= GY - p.h) {
            p.y = GY - p.h;
            p.vy = 0;
            p.onGround = true;
            p.jumps = 0;
        } else {
            p.onGround = false;
        }

        if (p.atk > 0 && !p.attackDone) {
            var hx = p.face > 0 ? p.x + 22 : p.x - 100;
            var hit = { x: hx, y: p.y - 18, w: 78, h: 64 };
            var dmg = Math.round(36 * (1 + Math.min(state.combo, 20) * 0.03));
            var any = false;
            state.enemies.forEach(function (e) {
                if (e.dead) return;
                if (rectHit(hit, { x: e.x - e.w / 2, y: e.y, w: e.w, h: e.h })) {
                    hitEnemy(e, dmg, p.face);
                    any = true;
                }
            });
            if (state.boss && !state.boss.dead) {
                var b = state.boss;
                if (rectHit(hit, { x: b.x - b.w / 2, y: b.y, w: b.w, h: b.h })) {
                    hitBoss(dmg, p.face);
                    any = true;
                }
            }
            if (any) {
                p.attackDone = true;
                state.combo += 1;
                state.comboT = 1.4;
                addScore(Math.round(10 * (1 + Math.min(state.combo, 20) * 0.03)));
                state.shake = Math.min(4, state.shake + 2);
                updateHud();
            }
        }
    }

    function rectHit(a, b) {
        return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
    }

    function updateEnemies(dt) {
        var p = state.player;
        var m = state.monk;
        state.enemies.forEach(function (e) {
            if (e.dead) return;
            e.t += dt;
            if (e.hitT > 0) e.hitT -= dt;
            if (e.atkCd > 0) e.atkCd -= dt;

            if (e.fly) {
                var dir = m.x >= e.x ? 1 : -1;
                e.x += dir * e.speed * dt;
                e.y = e.baseY + Math.sin(e.t * 2.6) * 34;
            } else if (e.ranged) {
                var dist = m.x - e.x;
                if (Math.abs(dist) > 320) {
                    e.x += (dist > 0 ? 1 : -1) * e.speed * dt;
                }
                e.shoot -= dt;
                if (e.shoot <= 0) {
                    e.shoot = XG.rand(1.8, 2.6);
                    var target = p && p.x > e.x - 60 ? p : m;
                    var dx = target.x - e.x;
                    var dy = (target === p ? (p.y + 30) : (GY - 30)) - (GY - 34);
                    var len = Math.sqrt(dx * dx + dy * dy) || 1;
                    state.shots.push({ x: e.x, y: GY - 34, vx: dx / len * 330, vy: dy / len * 330, r: 5, dmg: 10, kind: 'arrow', life: 3, dead: false, hit: false });
                }
            } else {
                var dir2 = m.x >= e.x ? 1 : -1;
                e.x += dir2 * e.speed * dt;
                e.y = GY - e.h + Math.sin(e.t * 8) * 1.5;
            }

            if (p && e.atkCd <= 0 && rectHit({ x: e.x - e.w / 2, y: e.y, w: e.w, h: e.h }, { x: p.x - p.w / 2, y: p.y, w: p.w, h: p.h })) {
                damagePlayer(e.dmg, e.x);
                e.atkCd = 1.0;
            }

            if (Math.abs(e.x - m.x) < 34 && Math.abs(e.y + e.h - GY) < 80) {
                hurtMonk(e.mdmg, e.x);
                e.dead = true;
                addPart(e.x, e.y + e.h / 2, '#8C2A2A', 10, 140);
            }
        });
        state.enemies = state.enemies.filter(function (e) { return !e.dead; });
    }

    function updateBoss(dt) {
        var b = state.boss;
        if (!b || b.dead) return;
        var p = state.player;
        var m = state.monk;
        b.t += dt;
        if (b.hitT > 0) b.hitT -= dt;
        b.cast -= dt;
        b.stateT += dt;

        if (b.type === 'bone') {
            b.x += ((m.x + 400) - b.x) * Math.min(1, dt * 0.7);
            b.y = b.baseY;
            if (b.summon > 0) {
                b.summon -= dt;
                if (b.summon <= 0) {
                    b.summon = 7.5;
                    state.enemies.push(makeEnemy('walker', b.x - 70), makeEnemy('walker', b.x + 70));
                }
            }
            if (b.cast <= 0) {
                b.cast = 2.5;
                for (var i = -1; i <= 1; i += 1) {
                    var tx = p ? p.x : m.x;
                    var dx = tx - b.x;
                    var dy = (p ? p.y + 20 : GY - 40) - (b.y + 30);
                    var len = Math.sqrt(dx * dx + dy * dy) || 1;
                    state.shots.push({ x: b.x, y: b.y + 30, vx: dx / len * 300 + i * 55, vy: dy / len * 300 - 40, r: 7, dmg: 11, kind: 'bone', life: 4, dead: false, hit: false });
                }
            }
        } else if (b.type === 'fire') {
            b.x = XG.clamp(m.x + 330 + Math.sin(b.t * 0.9) * 70, 120, STAGES[state.stage].len - 80);
            b.y = 210 + Math.sin(b.t * 1.7) * 28;
            if (b.cast <= 0) {
                b.cast = 1.45;
                var px = p ? p.x : m.x;
                var py = p ? p.y + 20 : GY - 40;
                var ddx = px - b.x;
                var ddy = py - (b.y + 30);
                var dlen = Math.sqrt(ddx * ddx + ddy * ddy) || 1;
                state.shots.push({ x: b.x, y: b.y + 30, vx: ddx / dlen * 310, vy: ddy / dlen * 310, r: 9, dmg: 12, kind: 'fire', life: 4, dead: false, hit: false });
            }
            if (b.summon > 0) {
                b.summon -= dt;
                if (b.summon <= 0) {
                    b.summon = 5.4;
                    state.zones.push({ x: XG.clamp(m.x + XG.rand(-40, 240), 60, STAGES[state.stage].len - 60), w: 76, life: 4, tick: 0 });
                }
            }
        } else if (b.type === 'bull') {
            if (b.state === 'idle') {
                b.vx = 0;
                b.x += ((m.x + 360) - b.x) * Math.min(1, dt * 0.35);
                if (b.stateT > 1.9) {
                    b.state = 'telegraph';
                    b.stateT = 0;
                    b.dir = m.x >= b.x ? 1 : -1;
                    addFloat(b.x, b.y - 16, '冲', '#C0392B');
                }
            } else if (b.state === 'telegraph') {
                b.vx = 0;
                if (b.stateT > 0.85) {
                    b.state = 'charge';
                    b.stateT = 0;
                    b.vx = b.dir * 560;
                }
            } else if (b.state === 'charge') {
                b.x += b.vx * dt;
                var minX = state.cam + 60;
                var maxX = STAGES[state.stage].len - 60;
                if (b.x < minX || b.x > maxX || b.stateT > 1.25) {
                    b.x = XG.clamp(b.x, minX, maxX);
                    b.state = 'recover';
                    b.stateT = 0;
                    b.vx = 0;
                    state.shake = 6;
                }
            } else {
                if (b.stateT > 1.1) {
                    b.state = 'idle';
                    b.stateT = 0;
                }
            }
            if (b.summon > 0) {
                b.summon -= dt;
                if (b.summon <= 0) {
                    b.summon = 4.8;
                    state.shots.push({ x: b.x, y: GY - 10, vx: 0, vy: 0, r: 8, dmg: 15, kind: 'wave', life: 1.2, dead: false, hit: false });
                }
            }
            b.y = GY - b.h;
        }

        if (b.type !== 'bull') b.x = XG.clamp(b.x, state.cam + 70, STAGES[state.stage].len - 70);

        if (p && rectHit({ x: b.x - b.w / 2, y: b.y, w: b.w, h: b.h }, { x: p.x - p.w / 2, y: p.y, w: p.w, h: p.h })) {
            damagePlayer(10, b.x);
        }
        if (Math.abs(b.x - m.x) < 40 && Math.abs(b.y + b.h - GY) < 120) {
            hurtMonk(b.mdmg, b.x);
            b.x += (b.x > m.x ? 1 : -1) * 30;
        }
    }

    function updateShots(dt) {
        var p = state.player;
        state.shots.forEach(function (s) {
            if (s.dead) return;
            s.life -= dt;
            if (s.kind === 'wave') {
                s.r += 340 * dt;
                if (!s.hit && p && p.y + p.h > GY - 76 && Math.abs(p.x - s.x) < s.r) {
                    s.hit = true;
                    damagePlayer(s.dmg, s.x);
                }
            } else {
                s.x += s.vx * dt;
                s.y += s.vy * dt;
                if (s.kind === 'bone') s.vy += 380 * dt;
                if (!s.hit && p && rectHit({ x: s.x - s.r, y: s.y - s.r, w: s.r * 2, h: s.r * 2 }, { x: p.x - p.w / 2, y: p.y, w: p.w, h: p.h })) {
                    s.hit = true;
                    s.dead = true;
                    damagePlayer(s.dmg, s.x);
                }
            }
            if (s.life <= 0 || s.x < state.cam - 100 || s.x > state.cam + W + 100 || s.y > H + 40) s.dead = true;
        });
        state.shots = state.shots.filter(function (s) { return !s.dead; });
    }

    function updateZones(dt) {
        var p = state.player;
        state.zones.forEach(function (z) {
            z.life -= dt;
            z.tick -= dt;
            if (p && p.onGround && Math.abs(p.x - z.x) < z.w / 2 && z.tick <= 0) {
                z.tick = 0.55;
                damagePlayer(8, z.x);
            }
        });
        state.zones = state.zones.filter(function (z) { return z.life > 0; });
    }

    function updateParticles(dt) {
        state.parts.forEach(function (p) {
            p.life -= dt;
            p.x += p.vx * dt;
            p.y += p.vy * dt;
            p.vy += 260 * dt;
        });
        state.parts = state.parts.filter(function (p) { return p.life > 0; });
        state.floats.forEach(function (f) {
            f.life -= dt;
            f.y -= 34 * dt;
        });
        state.floats = state.floats.filter(function (f) { return f.life > 0; });
    }

    function update(dt) {
        if (state.hitStop > 0) {
            state.hitStop -= dt;
            return;
        }
        var stage = STAGES[state.stage];
        state.stageT += dt;

        updateMonk(dt);
        updatePlayer(dt);
        updateEnemies(dt);
        updateBoss(dt);
        updateShots(dt);
        updateZones(dt);
        updateParticles(dt);

        if (state.comboT > 0) {
            state.comboT -= dt;
            if (state.comboT <= 0) state.combo = 0;
        }
        if (state.shake > 0) state.shake = Math.max(0, state.shake - dt * 40);

        while (state.waveIndex < stage.waves.length && state.monk.x >= stage.waves[state.waveIndex].x) {
            var wave = stage.waves[state.waveIndex];
            var baseX = state.monk.x + 640;
            for (var i = 0; i < wave.n; i += 1) {
                state.enemies.push(makeEnemy(wave.type, baseX + i * 58));
            }
            if (wave.extra) {
                for (var j = 0; j < wave.extraN; j += 1) {
                    state.enemies.push(makeEnemy(wave.extra, baseX + 120 + j * 52));
                }
            }
            state.waveIndex += 1;
        }

        if (!state.bossSpawned && state.monk.x >= stage.bossAt) {
            state.bossSpawned = true;
            spawnBoss(stage.bossType, XG.clamp(state.monk.x + 560, 400, stage.len - 80));
        }

        if (state.boss && state.boss.dead && state.monk.x < stage.len - 60) {
            state.monk.x = Math.min(state.monk.x + stage.speed * dt, stage.len - 40);
        }

        var targetCam = state.player.x - W * 0.38;
        state.cam += (targetCam - state.cam) * Math.min(1, dt * 4.2);
        state.cam = XG.clamp(state.cam, 0, Math.max(0, stage.len - W));

        updateHud();
    }

    function updateHud() {
        if (!els.hp) return;
        XG.bar(els.hp, state.player ? state.player.hp / state.player.maxHp : 0);
        XG.bar(els.monk, state.monk ? state.monk.hp / state.monk.maxHp : 0);
        setText(els.hpNum, state.player ? Math.max(0, Math.ceil(state.player.hp)) : 0);
        setText(els.monkNum, state.monk ? Math.max(0, Math.ceil(state.monk.hp)) : 0);
        setText(els.combo, state.combo > 1 ? state.combo + ' 连' : '0');
        setText(els.score, XG.fmt(state.score));
        setText(els.best, XG.fmt(state.best));
        if (els.progress && state.monk) {
            var len = STAGES[state.stage].len;
            els.progress.style.width = (XG.clamp(state.monk.x / (len - 60), 0, 1) * 100).toFixed(1) + '%';
        }
    }

    /* ===== 渲染 ===== */
    function drawMountains(offset, alpha, baseY, height) {
        ctx.fillStyle = 'rgba(28, 26, 23, ' + alpha + ')';
        ctx.beginPath();
        ctx.moveTo(-40, baseY);
        for (var i = 0; i < 7; i += 1) {
            var x0 = i * 190 - (offset % 190) - 60;
            var peak = height * (0.55 + 0.35 * Math.abs(Math.sin(i * 1.7 + 0.4)));
            ctx.lineTo(x0 + 95, baseY - peak);
            ctx.lineTo(x0 + 190, baseY);
        }
        ctx.lineTo(W + 80, baseY);
        ctx.lineTo(W + 80, H);
        ctx.lineTo(-40, H);
        ctx.closePath();
        ctx.fill();
    }

    function drawGround() {
        ctx.strokeStyle = 'rgba(28, 26, 23, 0.55)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, GY);
        ctx.lineTo(W, GY);
        ctx.stroke();

        ctx.strokeStyle = 'rgba(28, 26, 23, 0.22)';
        ctx.lineWidth = 1;
        var start = Math.floor((state.cam - 60) / 42) * 42;
        for (var x = start; x < state.cam + W + 60; x += 42) {
            var sx = x - state.cam;
            var h = 4 + ((x * 7919) % 9);
            ctx.beginPath();
            ctx.moveTo(sx, GY);
            ctx.lineTo(sx + 3, GY - h);
            ctx.stroke();
        }
    }

    function drawMonk(x) {
        var m = state.monk;
        if (!m) return;
        var sx = x - state.cam;
        var bob = Math.sin(m.t * 6) * 1.5;
        var y = GY - m.h + bob;
        ctx.save();
        if (m.hurt > 0) {
            ctx.globalAlpha = 0.65 + Math.sin(m.t * 40) * 0.25;
        }
        // 袈裟
        ctx.fillStyle = '#FCFAF4';
        ctx.strokeStyle = '#1C1A17';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(sx - 13, y + 18);
        ctx.lineTo(sx + 13, y + 18);
        ctx.lineTo(sx + 18, y + 54);
        ctx.lineTo(sx - 18, y + 54);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        // 朱砂袈裟边
        ctx.fillStyle = '#C0392B';
        ctx.fillRect(sx - 13, y + 32, 26, 5);
        // 头
        ctx.fillStyle = '#E6DFCC';
        ctx.beginPath();
        ctx.arc(sx, y + 9, 9, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        // 毗卢帽
        ctx.fillStyle = '#C0392B';
        ctx.fillRect(sx - 8, y + 1, 16, 4);
        // 锡杖
        ctx.strokeStyle = '#8E7D62';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(sx + 20, y + 8);
        ctx.lineTo(sx + 20, y + 56);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(sx + 20, y + 7, 4, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
    }

    function drawWukong(x) {
        var p = state.player;
        if (!p) return;
        var sx = x - state.cam;
        var y = p.y;
        var face = p.face;
        ctx.save();
        ctx.translate(sx, y);
        ctx.scale(face, 1);
        if (p.inv > 0 && Math.floor(p.inv * 20) % 2 === 0) ctx.globalAlpha = 0.45;
        if (p.dash > 0) {
            ctx.strokeStyle = 'rgba(192, 57, 43, 0.35)';
            ctx.lineWidth = 3;
            for (var i = 1; i <= 3; i += 1) {
                ctx.beginPath();
                ctx.moveTo(-i * 22, 20 - i * 6);
                ctx.lineTo(-i * 22 - 18, 20 - i * 6);
                ctx.stroke();
            }
        }
        // 尾巴
        ctx.strokeStyle = '#1C1A17';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(-8, 44);
        ctx.quadraticCurveTo(-34, 30 + Math.sin((p.atk || 0) * 30) * 4, -26, 8);
        ctx.stroke();
        // 身体
        ctx.fillStyle = '#1C1A17';
        ctx.beginPath();
        ctx.ellipse(0, 40, 13, 20, 0, 0, Math.PI * 2);
        ctx.fill();
        // 虎皮裙
        ctx.fillStyle = '#C0392B';
        ctx.fillRect(-12, 46, 24, 6);
        // 头
        ctx.beginPath();
        ctx.arc(3, 14, 12, 0, Math.PI * 2);
        ctx.fill();
        // 耳朵
        ctx.beginPath();
        ctx.arc(-9, 10, 4, 0, Math.PI * 2);
        ctx.fill();
        // 眼
        ctx.fillStyle = '#F5E6A8';
        ctx.beginPath();
        ctx.arc(8, 12, 2.2, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#1C1A17';
        ctx.beginPath();
        ctx.arc(9, 12, 1, 0, Math.PI * 2);
        ctx.fill();
        // 金箍
        ctx.strokeStyle = '#B8860B';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(3, 14, 12, Math.PI * 0.95, Math.PI * 2.05);
        ctx.stroke();
        // 金箍棒
        ctx.save();
        var ang = -0.5;
        if (p.atk > 0) {
            ang = -1.35 + (1 - p.atk / 0.2) * 2.1;
        }
        ctx.translate(10, 34);
        ctx.rotate(ang);
        ctx.strokeStyle = '#8E7D62';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(-8, 0);
        ctx.lineTo(58, 0);
        ctx.stroke();
        ctx.fillStyle = '#C0392B';
        ctx.fillRect(54, -3, 8, 6);
        ctx.restore();
        ctx.restore();

        if (p.atk > 0) {
            var pct = 1 - p.atk / 0.22;
            ctx.strokeStyle = 'rgba(192, 57, 43, ' + (0.7 * (1 - pct)) + ')';
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.arc(sx + p.face * 26, y + 28, 62, -1.1, 1.1);
            ctx.stroke();
        }
    }

    function drawEnemy(e) {
        var sx = e.x - state.cam;
        var flash = e.hitT > 0;
        ctx.save();
        ctx.globalAlpha = flash ? 0.6 : 1;
        if (e.type === 'flyer') {
            var wing = Math.sin(e.t * 12) * 8;
            ctx.strokeStyle = '#1C1A17';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(sx - 6, e.y + 12);
            ctx.lineTo(sx - 26, e.y + 2 - wing);
            ctx.moveTo(sx + 6, e.y + 12);
            ctx.lineTo(sx + 26, e.y + 2 - wing);
            ctx.stroke();
            ctx.fillStyle = flash ? '#C0392B' : '#3A473A';
            ctx.beginPath();
            ctx.ellipse(sx, e.y + 16, 12, 13, 0, 0, Math.PI * 2);
            ctx.fill();
        } else if (e.type === 'archer') {
            ctx.fillStyle = flash ? '#C0392B' : '#4A463F';
            ctx.beginPath();
            ctx.ellipse(sx, e.y + 30, 12, 18, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#8E7D62';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(sx + 14, e.y + 26, 12, -1.2, 1.2);
            ctx.stroke();
        } else {
            ctx.fillStyle = flash ? '#C0392B' : '#3A473A';
            ctx.beginPath();
            ctx.ellipse(sx, e.y + 30, 14, 19, 0, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.fillStyle = '#C0392B';
        ctx.beginPath();
        ctx.arc(sx + (e.type === 'flyer' ? 0 : 2), e.y + (e.type === 'flyer' ? 12 : 14), 2.4, 0, Math.PI * 2);
        ctx.fill();
        // 血条
        if (e.hp < e.maxHp) {
            ctx.fillStyle = 'rgba(28,26,23,.18)';
            ctx.fillRect(sx - 16, e.y - 8, 32, 3);
            ctx.fillStyle = '#C0392B';
            ctx.fillRect(sx - 16, e.y - 8, 32 * (e.hp / e.maxHp), 3);
        }
        ctx.restore();
    }

    function drawBoss() {
        var b = state.boss;
        if (!b || b.dead) return;
        var sx = b.x - state.cam;
        var flash = b.hitT > 0;
        ctx.save();
        ctx.globalAlpha = flash ? 0.65 : 1;

        if (b.type === 'bone') {
            ctx.fillStyle = b.revealed ? '#4A463F' : '#FCFAF4';
            ctx.strokeStyle = '#1C1A17';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(sx - 18, b.y + 26);
            ctx.lineTo(sx + 18, b.y + 26);
            ctx.lineTo(sx + 26, b.y + b.h);
            ctx.lineTo(sx - 26, b.y + b.h);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = '#E6DFCC';
            ctx.beginPath();
            ctx.arc(sx, b.y + 16, 12, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = '#C0392B';
            ctx.beginPath();
            ctx.arc(sx - 4, b.y + 15, 1.6, 0, Math.PI * 2);
            ctx.arc(sx + 4, b.y + 15, 1.6, 0, Math.PI * 2);
            ctx.fill();
        } else if (b.type === 'fire') {
            ctx.fillStyle = 'rgba(192,57,43,.22)';
            ctx.beginPath();
            ctx.arc(sx, b.y + 34, 46 + Math.sin(b.t * 6) * 5, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#C0392B';
            ctx.beginPath();
            ctx.ellipse(sx, b.y + 38, 18, 24, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#E9B885';
            ctx.beginPath();
            ctx.arc(sx, b.y + 16, 12, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#8C2A2A';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(sx - 10, b.y + 4);
            ctx.lineTo(sx - 4, b.y - 12);
            ctx.moveTo(sx + 10, b.y + 4);
            ctx.lineTo(sx + 4, b.y - 12);
            ctx.stroke();
        } else {
            ctx.fillStyle = b.state === 'telegraph' ? '#C0392B' : '#2C2416';
            ctx.beginPath();
            ctx.ellipse(sx, b.y + 52, 34, 44, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#1C1A17';
            ctx.beginPath();
            ctx.arc(sx, b.y + 16, 20, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#E6DFCC';
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(sx - 16, b.y + 4);
            ctx.lineTo(sx - 30, b.y - 14);
            ctx.moveTo(sx + 16, b.y + 4);
            ctx.lineTo(sx + 30, b.y - 14);
            ctx.stroke();
            ctx.fillStyle = '#C0392B';
            ctx.beginPath();
            ctx.arc(sx - 7, b.y + 14, 2.6, 0, Math.PI * 2);
            ctx.arc(sx + 7, b.y + 14, 2.6, 0, Math.PI * 2);
            ctx.fill();
        }

        // 血条与名
        ctx.fillStyle = 'rgba(28,26,23,.2)';
        ctx.fillRect(sx - 46, b.y - 26, 92, 5);
        ctx.fillStyle = '#C0392B';
        ctx.fillRect(sx - 46, b.y - 26, 92 * (b.hp / b.maxHp), 5);
        ctx.fillStyle = '#1C1A17';
        ctx.font = '600 12px "Noto Sans SC", sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(STAGES[state.stage].bossName, sx, b.y - 34);
        ctx.textAlign = 'left';
        ctx.restore();
    }

    function drawShots() {
        state.shots.forEach(function (s) {
            var sx = s.x - state.cam;
            if (s.kind === 'wave') {
                ctx.strokeStyle = 'rgba(140, 42, 42, ' + Math.max(0, 1 - s.r / 420) + ')';
                ctx.lineWidth = 4;
                ctx.beginPath();
                ctx.arc(sx, GY - 6, s.r, Math.PI, Math.PI * 2);
                ctx.stroke();
            } else if (s.kind === 'fire') {
                ctx.fillStyle = 'rgba(192,57,43,.25)';
                ctx.beginPath();
                ctx.arc(sx, s.y, s.r + 5, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#C0392B';
                ctx.beginPath();
                ctx.arc(sx, s.y, s.r, 0, Math.PI * 2);
                ctx.fill();
            } else if (s.kind === 'bone') {
                ctx.strokeStyle = '#E6DFCC';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(sx - 6, s.y - 4);
                ctx.lineTo(sx + 6, s.y + 4);
                ctx.stroke();
            } else {
                ctx.strokeStyle = '#4A463F';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(sx - 10, s.y);
                ctx.lineTo(sx + 6, s.y);
                ctx.stroke();
            }
        });
    }

    function drawZones() {
        state.zones.forEach(function (z) {
            var sx = z.x - state.cam;
            var alpha = Math.min(0.55, z.life * 0.3);
            ctx.fillStyle = 'rgba(192, 57, 43, ' + alpha + ')';
            for (var i = -1; i <= 1; i += 1) {
                var fx = sx + i * 20;
                var fh = 26 + Math.sin(z.life * 9 + i) * 8;
                ctx.beginPath();
                ctx.moveTo(fx - 10, GY);
                ctx.quadraticCurveTo(fx, GY - fh, fx + 10, GY);
                ctx.fill();
            }
        });
    }

    function render() {
        if (!ctx) return;
        ctx.clearRect(0, 0, W, H);
        ctx.fillStyle = '#F5F0E4';
        ctx.fillRect(0, 0, W, H);

        var shakeX = 0;
        var shakeY = 0;
        if (state.shake > 0 && !XG.reduced) {
            shakeX = XG.rand(-state.shake, state.shake);
            shakeY = XG.rand(-state.shake, state.shake);
        }
        ctx.save();
        ctx.translate(shakeX, shakeY);

        // 远山（两层视差）
        drawMountains(state.cam * 0.18 + 40, 0.07, GY - 120, 150);
        drawMountains(state.cam * 0.34 + 160, 0.05, GY - 70, 110);

        // 朱砂日轮
        ctx.fillStyle = 'rgba(192, 57, 43, 0.10)';
        ctx.beginPath();
        ctx.arc(W - 140 - (state.cam * 0.05) % 80, 110, 46, 0, Math.PI * 2);
        ctx.fill();

        // 第二试火气、第三试火光
        if (STAGES[state.stage].id === 'huoyundong') {
            ctx.fillStyle = 'rgba(192, 57, 43, 0.05)';
            ctx.fillRect(0, 0, W, H);
        } else if (STAGES[state.stage].id === 'huoyanshan') {
            ctx.fillStyle = 'rgba(192, 57, 43, 0.08)';
            ctx.fillRect(0, GY - 40, W, 120);
        }

        drawGround();
        drawZones();
        drawMonk(state.monk ? state.monk.x : 0);
        state.enemies.forEach(drawEnemy);
        drawBoss();
        if (state.player) drawWukong(state.player.x);
        drawShots();

        state.parts.forEach(function (p) {
            ctx.globalAlpha = Math.max(0, p.life / p.max);
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x - state.cam, p.y, p.r, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.globalAlpha = 1;

        ctx.font = '600 14px "Noto Sans SC", sans-serif';
        ctx.textAlign = 'center';
        state.floats.forEach(function (f) {
            ctx.globalAlpha = Math.max(0, f.life / f.max);
            ctx.fillStyle = f.color;
            ctx.fillText(f.text, f.x - state.cam, f.y);
        });
        ctx.globalAlpha = 1;
        ctx.textAlign = 'left';

        // 距离标尺
        if (state.mode === 'playing' || state.mode === 'paused') {
            ctx.fillStyle = 'rgba(28,26,23,.35)';
            ctx.font = '11px "Noto Sans SC", sans-serif';
            ctx.fillText('西行 ' + Math.round(state.monk.x / 10) + ' 里', 14, H - 14);
        }

        ctx.restore();
    }

    function loop(ts) {
        if (!lastTs) lastTs = ts;
        var dt = Math.min(0.033, (ts - lastTs) / 1000);
        lastTs = ts;
        if (state.mode === 'playing' && panelVisible() && !document.hidden) update(dt);
        if (panelVisible()) render();
        rafId = window.requestAnimationFrame(loop);
    }

    function jump() {
        var p = state.player;
        if (!p || state.mode !== 'playing') return;
        if (p.jumps < 2) {
            p.vy = -640;
            p.jumps += 1;
            p.onGround = false;
            XG.audio.play('jump');
            addPart(p.x, p.y + p.h, '#8E7D62', 5, 90);
        }
    }

    function attack() {
        var p = state.player;
        if (!p || state.mode !== 'playing') return;
        if (p.atkCd > 0 || p.dash > 0) return;
        p.atk = 0.22;
        p.atkCd = 0.3;
        p.attackDone = false;
        XG.audio.play('swing');
    }

    function dash() {
        var p = state.player;
        if (!p || state.mode !== 'playing') return;
        if (p.dashCd > 0) return;
        p.dash = 0.16;
        p.dashCd = 1.6;
        p.inv = Math.max(p.inv, 0.3);
        p.vy = Math.min(p.vy, 0);
        XG.audio.play('dash');
        addPart(p.x, p.y + 30, '#C0392B', 8, 130);
    }

    function onKeyDown(e) {
        if (!panelVisible()) return;
        if (state.mode !== 'playing' && state.mode !== 'paused' && state.mode !== 'ready') return;
        var code = e.code;
        if (code === 'ArrowLeft' || code === 'KeyA') { keys.left = true; e.preventDefault(); }
        else if (code === 'ArrowRight' || code === 'KeyD') { keys.right = true; e.preventDefault(); }
        else if (code === 'ArrowUp' || code === 'Space' || code === 'KeyW') {
            e.preventDefault();
            if (!e.repeat && state.mode === 'playing') jump();
        } else if (code === 'KeyJ') {
            if (!e.repeat) attack();
        } else if (code === 'KeyK') {
            if (!e.repeat) dash();
        } else if (code === 'Escape') {
            if (state.mode === 'playing') pauseGame();
            else if (state.mode === 'paused') resumeGame();
            e.preventDefault();
        }
    }

    function onKeyUp(e) {
        if (!panelVisible()) return;
        var code = e.code;
        if (code === 'ArrowLeft' || code === 'KeyA') keys.left = false;
        else if (code === 'ArrowRight' || code === 'KeyD') keys.right = false;
    }

    function bindTouch() {
        var box = document.getElementById('act-touch');
        if (!box) return;
        box.querySelectorAll('button').forEach(function (btn) {
            var action = btn.getAttribute('data-touch');
            btn.addEventListener('pointerdown', function (e) {
                e.preventDefault();
                if (action === 'left') keys.left = true;
                else if (action === 'right') keys.right = true;
                else if (action === 'jump') jump();
                else if (action === 'atk') attack();
                else if (action === 'dash') dash();
            });
            btn.addEventListener('pointerup', function (e) {
                e.preventDefault();
                if (action === 'left') keys.left = false;
                else if (action === 'right') keys.right = false;
            });
            btn.addEventListener('pointercancel', function () {
                if (action === 'left') keys.left = false;
                else if (action === 'right') keys.right = false;
            });
            btn.addEventListener('pointerleave', function () {
                if (action === 'left') keys.left = false;
                else if (action === 'right') keys.right = false;
            });
        });
    }

    function init() {
        canvas = document.getElementById('act-canvas');
        if (!canvas) return;
        ctx = canvas.getContext('2d');
        els = {
            hp: document.getElementById('act-hp'),
            hpNum: document.getElementById('act-hp-num'),
            monk: document.getElementById('act-monk'),
            monkNum: document.getElementById('act-monk-num'),
            combo: document.getElementById('act-combo'),
            score: document.getElementById('act-score'),
            best: document.getElementById('act-best'),
            stage: document.getElementById('act-stage'),
            progress: document.getElementById('act-progress'),
            overlay: document.getElementById('act-overlay')
        };
        state.best = XG.storage.get(BEST_KEY, 0);
        setText(els.best, XG.fmt(state.best));

        state.monk = { x: 120, hp: 100, maxHp: 100, w: 26, h: 58, t: 0, hurt: 0 };
        state.player = makePlayer(180);

        document.getElementById('act-start').addEventListener('click', function () {
            XG.audio.play('click');
            startGame(false);
        });
        var hardBtn = document.getElementById('act-start-hard');
        if (hardBtn) {
            hardBtn.addEventListener('click', function () {
                XG.audio.play('click');
                startGame(true);
            });
        }
        var endlessBtn = document.getElementById('act-start-endless');
        if (endlessBtn) {
            endlessBtn.addEventListener('click', function () {
                XG.audio.play('click');
                startEndless();
            });
        }
        document.getElementById('act-pause').addEventListener('click', function () {
            if (state.mode === 'playing') pauseGame();
            else if (state.mode === 'paused') resumeGame();
        });
        document.getElementById('act-restart').addEventListener('click', function () {
            state.score = state.stageStartScore;
            resetStage(state.stage, true);
        });
        var fullBtn = document.getElementById('act-full');
        if (fullBtn) {
            if (!document.documentElement.requestFullscreen) {
                fullBtn.hidden = true;
            } else {
                fullBtn.addEventListener('click', function () {
                    var stage = canvas.parentElement;
                    if (document.fullscreenElement) {
                        document.exitFullscreen();
                    } else if (stage && stage.requestFullscreen) {
                        stage.requestFullscreen();
                    }
                });
                document.addEventListener('fullscreenchange', function () {
                    fullBtn.textContent = document.fullscreenElement ? '退出全屏' : '全屏';
                });
            }
        }
        document.addEventListener('keydown', onKeyDown);
        document.addEventListener('keyup', onKeyUp);
        document.addEventListener('visibilitychange', function () {
            if (document.hidden && state.mode === 'playing') pauseGame();
        });
        bindTouch();
        state.active = true;
        updateHud();
        render();
        rafId = window.requestAnimationFrame(loop);
    }

    XG.registerMode('action', {
        init: init,
        pause: function () {
            keys.left = false;
            keys.right = false;
            pauseGame();
        }
    });
})();
