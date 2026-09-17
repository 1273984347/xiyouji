// scripts/check_dark_state_gate.js — W579：暗色态门禁（O2 常驻化，挂 screenshot-review workflow）
// 判定：S2-desktop-dark 下同页同类型缺陷数「只增即 FAIL」——新增暗色缺陷在 CI 拦截，存量不追溯。
// 对比类型：pageError / lowContrast / invisible（暗色特异三类）；
//   hOverflow 不入本门禁（视口相关非主题相关，S1 截图门禁已覆盖——对方案口径的偏离已在 CHANGELOG 声明）。
// 状态回归：基线行暗色已应用（isDarkBg）而当前行未应用 → FAIL（自动暗色机制退化拦截）。
// 用法：
//   node scripts/check_dark_state_gate.js                    # 审计输出 vs 基线，FAIL 即 exit 1
//   node scripts/check_dark_state_gate.js --update-baseline  # 修复批刷新基线（拷贝当前审计输出）
//   node scripts/check_dark_state_gate.js --self-test        # 5 负样本自测
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const BASELINE = path.join(ROOT, 'scripts', 'output', 'render-state-audit-baseline.jsonl');
const CURRENT = path.join(ROOT, 'scripts', 'output', 'render-state-audit.jsonl');
const STATE = 'S2-desktop-dark';
const TYPES = ['pageError', 'lowContrast', 'invisible'];

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

function compare(base, cur) {
  const fails = [];
  for (const [page, c] of cur) {
    const b = base.get(page);
    if (!b) {
      const withDefect = TYPES.filter(t => c[t] > 0);
      if (withDefect.length) fails.push({ page, kind: 'new-page', detail: `基线外新页且有缺陷：${withDefect.join('/')}` });
      continue;
    }
    if (b.isDarkBg && !c.isDarkBg) fails.push({ page, kind: 'dark-not-applied', detail: `基线暗色已应用，当前未应用（dataTheme 退化）` });
    for (const t of TYPES) {
      if (c[t] > b[t]) fails.push({ page, kind: t, detail: `${b[t]} → ${c[t]}（新增 ${c[t] - b[t]}）` });
    }
  }
  return fails;
}

function selfTest() {
  const mk = (pe, lc, inv, dark = true) => ({ pageError: pe, lowContrast: lc, invisible: inv, isDarkBg: dark });
  const base = new Map([['a.html', mk(0, 2, 1)], ['b.html', mk(1, 0, 0)]]);
  const cases = [
    ['新增缺陷拦截', new Map([['a.html', mk(0, 3, 1)], ['b.html', mk(1, 0, 0)]]), true],
    ['缺陷下降放行', new Map([['a.html', mk(0, 1, 0)], ['b.html', mk(0, 0, 0)]]), false],
    ['完全持平放行', new Map([['a.html', mk(0, 2, 1)], ['b.html', mk(1, 0, 0)]]), false],
    ['基线外新页有缺陷拦截', new Map([['a.html', mk(0, 2, 1)], ['b.html', mk(1, 0, 0)], ['c.html', mk(0, 1, 0)]]), true],
    ['暗色未应用拦截', new Map([['a.html', mk(0, 2, 1, false)], ['b.html', mk(1, 0, 0)]]), true],
  ];
  let pass = 0;
  cases.forEach(([name, cur, expectFail], i) => {
    const fails = compare(base, cur);
    const gotFail = fails.length > 0;
    const ok = gotFail === expectFail;
    if (ok) pass++;
    console.log(`${ok ? 'OK  ' : 'FAIL'} 负样本${i + 1} ${name}: ${gotFail ? 'FAIL' : 'PASS'}（期望 ${expectFail ? 'FAIL' : 'PASS'}）`);
  });
  console.log(`${pass}/${cases.length} self-test PASS`);
  return pass === cases.length;
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
  console.log(`暗色门禁：基线 ${base.size} 页 / 当前 ${cur.size} 页（${STATE}）`);
  const fails = compare(base, cur);
  if (fails.length) {
    console.log(`FAIL ${fails.length} 项新增暗色缺陷/回归：`);
    for (const f of fails) console.log(`  - [${f.kind}] ${f.page}: ${f.detail}`);
    process.exit(1);
  }
  console.log('OK 同页同类型缺陷数零新增，暗色门禁通过');
}

main();
