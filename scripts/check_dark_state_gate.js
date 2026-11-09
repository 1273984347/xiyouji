// scripts/check_dark_state_gate.js — W579：暗色态门禁（O2 常驻化，挂 screenshot-review workflow）
// 判定：S2-desktop-dark 下同页同类型缺陷数「只增即 FAIL」——新增暗色缺陷在 CI 拦截，存量不追溯。
// 对比类型：pageError / lowContrast / invisible（暗色特异三类）；
//   hOverflow 不入本门禁（视口相关非主题相关，S1 截图门禁已覆盖——对方案口径的偏离已在 CHANGELOG 声明）。
// 状态回归：基线行暗色已应用（isDarkBg）而当前行未应用 → FAIL（自动暗色机制退化拦截）。
//
// W1192：断言域改为「采集面内」（此前断言域 = 全部基线行 ⇒ 恒红 625 项）
//   背景：基线文件 render-state-audit-baseline.jsonl 混装两个采集面——
//     ① charts 面（W579 建门禁时采的 160 个含 <svg 的页面）；② reader 面（W662 事后并入的 621 行）。
//     CI 只采 charts 面（--scope charts），而 W1155 深度审计加的「基线页缺失 / 采集面萎缩」断言
//     遍历**全部**基线行 ⇒ reader 面 621 行 + 3 个已下线页被恒判「基线页缺失」625 项。
//     W662 段原文已定口径「gate compare 只遍历 charts scope 当前输出侧，reader 行不参与比对」，
//     W1155 的新增断言未按该口径限定 ⇒ 属实现偏离设计意图（W1192 实证）。
//   修法（**不降判据强度**，四项能力全部保留并加严）：
//     ① 采集面口径**单点来源**：scripts/_render_scope.js（listPages / chartsPages）——
//        采集端（_audit_render_states.js）与比对端（本脚本）共用同一实现，禁两处各自判 <svg。
//     ② 缺失断言只在「基线 ∩ 当前 charts 面」内成立 ⇒ CI 分片丢页 / upload 缺 always() 仍被拦。
//     ③ 采集面萎缩断言同域比较（当前页数 < 基线同面页数 ⇒ FAIL）——分片缺失仍被拦。
//     ④ **新增**：基线页若「磁盘已无」（页面下线）且未登记进 RETIRED_PAGES ⇒ FAIL
//        （防悄悄删页被 scope 限定放过；历史 3 个已下线页在白名单内）。
//     ⑤ reader 面遗留基线行（磁盘在、但不在 charts 面）不参与比对，但**计数输出**可见（非静默）。
//   基线不刷新（--update-baseline 会把 784 行砍到 168 行并抹掉 reader 面 621 行 ⇒ 属降判据·本批禁用）。
//
// 用法：
//   node scripts/check_dark_state_gate.js                    # 审计输出 vs 基线，FAIL 即 exit 1
//   node scripts/check_dark_state_gate.js --update-baseline  # 修复批刷新基线（拷贝当前审计输出）
//   node scripts/check_dark_state_gate.js --self-test        # 9 负样本自测
const fs = require('fs');
const path = require('path');
const { listPages, chartsPages } = require('./_render_scope.js');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const BASELINE = path.join(ROOT, 'scripts', 'output', 'render-state-audit-baseline.jsonl');
// W1066：--current <path>（分片并行时各分片产物合并后的文件）
const CURRENT = (() => {
  const i = process.argv.indexOf('--current');
  if (i > -1 && process.argv[i + 1]) {
    const v = process.argv[i + 1];
    return path.isAbsolute(v) ? v : path.join(ROOT, v);
  }
  return path.join(ROOT, 'scripts', 'output', 'render-state-audit.jsonl');
})();
const STATE = 'S2-desktop-dark';
const TYPES = ['pageError', 'lowContrast', 'invisible'];

// W1192：已下线页白名单（磁盘上已不存在的基线页）——页面下线属正常变更，
//   但必须**显式登记**才能通过门禁（防悄悄删页）。白名单外的下线页一律 FAIL。
//   来源：data/ 与 en/ 的 narratology-13d-network.html（W678「13d→16d 改名」后旧名下线）、
//        mobile-index.html（W669「mobile-index 退役」）。
const RETIRED_PAGES = [
  'data/narratology-13d-network.html',
  'en/narratology-13d-network.html',
  'mobile-index.html',
];

function loadRows(file) {
  if (!fs.existsSync(file)) return null;
  const rows = fs.readFileSync(file, 'utf8').split('\n')
    .filter(l => l.trim()).map(l => { try { return JSON.parse(l); } catch { return null; } })
    .filter(Boolean).filter(r => r.state === STATE);
  const m = new Map();
  for (const r of rows) {
    m.set(r.page, {
      pageError: (r.errors || []).length + (r.fatal ? 1 : 0),
      lowContrast: (r.lowContrastText || []).length,
      invisible: (r.invisibleShapes || []).length,
      isDarkBg: !!r.isDarkBg,
    });
  }
  return m;
}

// W1192：断言域限定在采集面内。
//   opts.scope      —— 当前 charts 面页集合（Set）：基线页在此集合内 ⇒ 本次采集本应覆盖它
//   opts.onDisk     —— 当前磁盘候选页集合（Set）：区分「页面已下线」与「只是不在 charts 面」
//   opts.retiredOk  —— 已下线页白名单（Set）
//   opts 缺省时退化为旧行为（不限定断言域）——仅供自测夹具使用。
function compare(base, cur, opts) {
  const scope = (opts && opts.scope) || null;
  const onDisk = (opts && opts.onDisk) || null;
  const retiredOk = (opts && opts.retiredOk) || new Set();
  const fails = [];
  // 期望被本次采集覆盖的基线页 = 基线 ∩ 当前 charts 面
  const expected = new Map();
  const retired = [];
  const legacy = [];
  if (scope) {
    for (const [page, v] of base) {
      if (scope.has(page)) { expected.set(page, v); continue; }
      if (onDisk && !onDisk.has(page)) retired.push(page);
      else legacy.push(page);
    }
  } else {
    for (const [page, v] of base) expected.set(page, v);
  }
  // ① 已下线页未登记 ⇒ FAIL（防悄悄删页被 scope 限定放过）
  for (const page of retired) {
    if (!retiredOk.has(page)) {
      fails.push({ page, kind: 'page-retired-unregistered', detail: '基线页在磁盘上已不存在且未登记进 RETIRED_PAGES（页面下线须显式登记）' });
    }
  }
  // ② 采集面萎缩（分片缺失 / upload 缺 always() ⇒ 页面静默丢失仍输出「零新增通过」）
  if (cur.size < expected.size) {
    fails.push({ page: '(采集面)', kind: 'size-mismatch', detail: `当前采集 ${cur.size} 页 < 基线同面 ${expected.size} 页（分片缺失或 upload 非 always·判据未执行）` });
  }
  // ③ 同面缺页
  for (const [page] of expected) {
    if (!cur.has(page)) {
      fails.push({ page, kind: 'base-page-missing', detail: '基线页在当前采集中缺失（分片缺失/upload 失败）' });
    }
  }
  // ④ 逐页缺陷比较（新页有缺陷 / 缺陷数增加 / 暗色未应用）
  for (const [page, c] of cur) {
    const b = base.get(page);
    if (!b) {
      const withDefect = TYPES.filter(t => c[t] > 0);
      if (withDefect.length) fails.push({ page, kind: 'new-page', detail: `基线外新页且有缺陷：${withDefect.join('/')}` });
      continue;
    }
    if (b.isDarkBg && !c.isDarkBg) fails.push({ page, kind: 'dark-not-applied', detail: '基线暗色已应用，当前未应用（dataTheme 退化）' });
    for (const t of TYPES) {
      if (c[t] > b[t]) fails.push({ page, kind: t, detail: `${b[t]} → ${c[t]}（新增 ${c[t] - b[t]}）` });
    }
  }
  return { fails, expected: expected.size, retired, legacy };
}

function selfTest() {
  const mk = (pe, lc, inv, dark = true) => ({ pageError: pe, lowContrast: lc, invisible: inv, isDarkBg: dark });
  const base = new Map([['a.html', mk(0, 2, 1)], ['b.html', mk(1, 0, 0)]]);
  // 自测夹具：a/b 均在采集面内且磁盘在
  const scope = new Set(['a.html', 'b.html']);
  const onDisk = new Set(['a.html', 'b.html']);
  const retiredOk = new Set(['gone.html']);
  const opts = { scope, onDisk, retiredOk };
  const cases = [
    ['新增缺陷拦截', new Map([['a.html', mk(0, 3, 1)], ['b.html', mk(1, 0, 0)]]), true],
    ['缺陷下降放行', new Map([['a.html', mk(0, 1, 0)], ['b.html', mk(0, 0, 0)]]), false],
    ['完全持平放行', new Map([['a.html', mk(0, 2, 1)], ['b.html', mk(1, 0, 0)]]), false],
    ['基线外新页有缺陷拦截', new Map([['a.html', mk(0, 2, 1)], ['b.html', mk(1, 0, 0)], ['c.html', mk(0, 1, 0)]]), true],
    ['暗色未应用拦截', new Map([['a.html', mk(0, 2, 1, false)], ['b.html', mk(1, 0, 0)]]), true],
    ['同面缺页拦截', new Map([['b.html', mk(1, 0, 0)]]), true],
    ['采集面萎缩拦截', new Map([['a.html', mk(0, 2, 1)]]), true],
  ];
  let pass = 0;
  cases.forEach(([name, cur, expectFail], i) => {
    const { fails } = compare(base, cur, opts);
    const gotFail = fails.length > 0;
    const ok = gotFail === expectFail;
    if (ok) pass++;
    console.log(`${ok ? 'OK  ' : 'FAIL'} 负样本${i + 1} ${name}: ${gotFail ? 'FAIL' : 'PASS'}（期望 ${expectFail ? 'FAIL' : 'PASS'}）`);
  });
  // W1192 新增两例：已下线页未登记 ⇒ 拦截；已下线页已登记 ⇒ 放行
  const baseWithGone = new Map([['a.html', mk(0, 2, 1)], ['gone.html', mk(0, 0, 0)]]);
  const scopeNoGone = new Set(['a.html']);
  const diskNoGone = new Set(['a.html']);
  const curNoGone = new Map([['a.html', mk(0, 2, 1)]]);
  const unregistered = compare(baseWithGone, curNoGone, { scope: scopeNoGone, onDisk: diskNoGone, retiredOk: new Set() });
  const regOk = unregistered.fails.length > 0
    && unregistered.fails.every(f => f.kind === 'page-retired-unregistered');
  console.log(`${regOk ? 'OK  ' : 'FAIL'} 负样本8 已下线页未登记拦截: ${unregistered.fails.length ? 'FAIL' : 'PASS'}（期望 FAIL）`);
  if (regOk) pass++;
  const registered = compare(baseWithGone, curNoGone, { scope: scopeNoGone, onDisk: diskNoGone, retiredOk: new Set(['gone.html']) });
  const regPass = registered.fails.length === 0;
  console.log(`${regPass ? 'OK  ' : 'FAIL'} 负样本9 已下线页已登记放行: ${registered.fails.length ? 'FAIL' : 'PASS'}（期望 PASS）`);
  if (regPass) pass++;
  console.log(`${pass}/${cases.length + 2} self-test PASS`);
  return pass === cases.length + 2;
}

function main() {
  if (process.argv.includes('--self-test')) {
    process.exit(selfTest() ? 0 : 1);
  }
  if (process.argv.includes('--update-baseline')) {
    if (!fs.existsSync(CURRENT)) { console.error('无当前审计输出：' + CURRENT); process.exit(2); }
    fs.copyFileSync(CURRENT, BASELINE);
    const n = fs.readFileSync(BASELINE, 'utf8').split('\n').filter(l => l.trim()).length;
    console.log(`基线已刷新：${BASELINE}（${n} 行）——仅限暗色缺陷修复批下降后使用`);
    return;
  }
  const base = loadRows(BASELINE);
  const cur = loadRows(CURRENT);
  if (!base) { console.error(`FAIL 无基线：${BASELINE}（先随批提交基线快照）`); process.exit(2); }
  if (!cur) { console.error(`FAIL 无当前审计输出：${CURRENT}（先跑 _audit_render_states.js --states ${STATE} --scope charts）`); process.exit(2); }
  // W1192：采集面口径单点来源（与采集端 _audit_render_states.js 共用 _render_scope.js）
  const scopePages = chartsPages(SITE);
  const scope = new Set(scopePages);
  const onDisk = new Set(listPages(SITE));
  const retiredOk = new Set(RETIRED_PAGES);
  console.log(`暗色门禁：基线 ${base.size} 页 / 当前 ${cur.size} 页（${STATE}·charts 面 ${scope.size} 页·磁盘候选 ${onDisk.size} 页）`);
  const { fails, expected, retired, legacy } = compare(base, cur, { scope, onDisk, retiredOk });
  console.log(`  断言域 = 基线 ∩ charts 面：${expected} 页｜已下线页 ${retired.length} 个（白名单内 ${retired.filter(p => retiredOk.has(p)).length}）｜reader 面遗留基线行 ${legacy.length} 行（不参与比对·计数可见）`);
  if (fails.length) {
    console.log(`FAIL ${fails.length} 项新增暗色缺陷/回归：`);
    for (const f of fails) console.log(`  - [${f.kind}] ${f.page}: ${f.detail}`);
    process.exit(1);
  }
  console.log('OK 同页同类型缺陷数零新增，暗色门禁通过');
}

main();
