// feedback.test.mjs — W600 反馈闭环集成测试（真实起服→HTTP POST→直查 chat.db→清理）
// 运行：cd xiyouji-agent-web && node server/feedback.test.mjs
// 无需 CODEBUDDY_API_KEY（不触发 LLM）。测试行用完即删，不污染真实数据。
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import Database from 'better-sqlite3';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const WEB = path.resolve(HERE, '..');
const PORT = 3101;
const BASE = `http://127.0.0.1:${PORT}`;
const MARK = `test-msg-${Date.now()}`;

const wait = (ms) => new Promise(r => setTimeout(r, ms));

async function waitHealth() {
  for (let i = 0; i < 30; i++) {
    try {
      const r = await fetch(`${BASE}/api/health`);
      if (r.ok) return true;
    } catch { /* not up yet */ }
    await wait(500);
  }
  return false;
}

const child = spawn(process.execPath, ['node_modules/tsx/dist/cli.mjs', 'server/index.ts'], {
  cwd: WEB,
  env: { ...process.env, PORT: String(PORT) },
  stdio: 'ignore',
});
let failed = 0;
try {
  if (!(await waitHealth())) { console.log('FAIL server 未就绪'); process.exit(1); }

  // 1) 合法反馈：首次 inserted=1
  let r = await fetch(`${BASE}/api/feedback`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sessionId: 'test-sess', messageId: MARK, verdict: 'up' }),
  });
  const j1 = await r.json();
  const ok1 = r.status === 200 && j1.inserted === 1;
  console.log(`${ok1 ? 'PASS' : 'FAIL'} 首次反馈 inserted=1`, ok1 ? '' : JSON.stringify(j1));
  if (!ok1) failed++;

  // 2) 幂等：重复提交 inserted=0
  r = await fetch(`${BASE}/api/feedback`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sessionId: 'test-sess', messageId: MARK, verdict: 'up' }),
  });
  const j2 = await r.json();
  const ok2 = r.status === 200 && j2.inserted === 0;
  console.log(`${ok2 ? 'PASS' : 'FAIL'} 幂等 inserted=0`);
  if (!ok2) failed++;

  // 3) 非法 verdict → 400
  r = await fetch(`${BASE}/api/feedback`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sessionId: 's', messageId: 'm', verdict: 'meh' }),
  });
  const ok3 = r.status === 400;
  console.log(`${ok3 ? 'PASS' : 'FAIL'} 非法 verdict 400`);
  if (!ok3) failed++;

  // 4) summary 端点
  r = await fetch(`${BASE}/api/feedback/summary`);
  const j4 = await r.json();
  const ok4 = r.status === 200 && j4.ok === true && typeof j4.up === 'number';
  console.log(`${ok4 ? 'PASS' : 'FAIL'} summary 端点`, ok4 ? JSON.stringify(j4) : '');
  if (!ok4) failed++;

  // 5) 直查 sqlite：MARK 恰 1 行
  const db = new Database(path.join(WEB, 'data', 'chat.db'), { readonly: true });
  const n = db.prepare('SELECT COUNT(*) c FROM feedback WHERE message_id = ?').get(MARK).c;
  db.close();
  const ok5 = n === 1;
  console.log(`${ok5 ? 'PASS' : 'FAIL'} sqlite 行数=${n}`);
  if (!ok5) failed++;
} finally {
  child.kill();
  // 清理测试行
  try {
    const db = new Database(path.join(WEB, 'data', 'chat.db'));
    db.prepare('DELETE FROM feedback WHERE message_id = ?').run(MARK);
    db.close();
    console.log('cleanup ok');
  } catch (e) { console.log('cleanup skip:', e.message); }
}
console.log(failed ? `RESULT ${5 - failed}/5 PASS` : 'RESULT 5/5 PASS');
process.exit(failed ? 1 : 0);
