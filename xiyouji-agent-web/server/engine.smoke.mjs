#!/usr/bin/env node
// engine.smoke.mjs — 引擎全链路冒烟（W680·可重复执行的常驻机判）
//
// 拓扑：mock LLM（脚本内起）→ agent-web 服务器（tsx spawn，LLM_API_BASE 指向 mock）→ /api/chat SSE。
// 断言（全链路机判，无真实密钥依赖）：
//   S1 SSE 事件序列 = init → tool(read_file) → tool_result → text → done（permission_request 不出现——default 模式 read 类自动放行）
//   S2 工具真实执行：tool_result 内容 = 磁盘真实文件内容（mock 只发指令，读文件的是引擎工具集）
//   S3 文本增量拼接 = mock 最终回复全文
//   S4 越界路径被拒（第二轮对话请求 read_file ../.env → tool_result isError）
// 运行：cd xiyouji-agent-web && node server/engine.smoke.mjs
import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const WEB = path.resolve(HERE, '..');
const AGENT_PORT = 3102;
const BASE = `http://127.0.0.1:${AGENT_PORT}`;
const wait = (ms) => new Promise(r => setTimeout(r, ms));

// ---------- mock LLM（OpenAI-compatible SSE） ----------
const FIXTURE = path.join(WEB, '..', 'CLAUDE.md'); // 引擎 cwd = 仓库根，read_file 相对路径 CLAUDE.md
const fixtureHead = fs.readFileSync(FIXTURE, 'utf8').slice(0, 200);

function sse(res, deltas, finish) {
  res.writeHead(200, { 'Content-Type': 'text/event-stream' });
  for (const d of deltas) {
    res.write(`data: ${JSON.stringify({ id: 'mock', choices: [{ delta: d, finish_reason: null }] })}\n\n`);
  }
  res.write(`data: ${JSON.stringify({ id: 'mock', choices: [{ delta: {}, finish_reason: finish.reason }] })}\n\n`);
  res.write('data: [DONE]\n\n');
  res.end();
}

let llmTurns = 0;
const llm = http.createServer((req, res) => {
  let body = '';
  req.on('data', (c) => { body += c; });
  req.on('end', () => {
    llmTurns += 1;
    const parsed = JSON.parse(body);
    const hasToolMsg = parsed.messages.some((m) => m.role === 'tool');
    if (llmTurns % 2 === 1) {
      // 第 1/3 轮：发工具调用（正常读 CLAUDE.md / 越界读 .env）
      const evil = parsed.messages.some((m) => m.role === 'user' && String(m.content).includes('EVIL-TEST'));
      const args = evil ? '{"path":"../../.env"}' : '{"path":"CLAUDE.md"}';
      sse(res, [
        { tool_calls: [{ index: 0, id: `call_${llmTurns}`, type: 'function', function: { name: 'read_file', arguments: '' } }] },
        { tool_calls: [{ index: 0, function: { arguments: args } }] }, // arguments 分片到达
      ], { reason: 'tool_calls' });
    } else if (hasToolMsg) {
      // 第 2 轮：基于工具结果给最终文本
      sse(res, [{ content: 'MOCK-ENGINE-OK ' }, { content: fixtureHead.slice(0, 20) }], { reason: 'stop' });
    } else {
      // 第 4 轮：越界拒绝后的收尾文本
      sse(res, [{ content: 'EVIL-BLOCKED' }], { reason: 'stop' });
    }
  });
});

async function waitHealth() {
  for (let i = 0; i < 60; i++) {
    try { const r = await fetch(`${BASE}/api/health`); if (r.ok) return true; } catch { /* not up */ }
    await wait(500);
  }
  return false;
}

async function chat(message) {
  const resp = await fetch(`${BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, permissionMode: 'default' }),
  });
  const events = [];
  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  outer: while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    let nl;
    while ((nl = buffer.indexOf('\n')) !== -1) {
      const line = buffer.slice(0, nl).trim();
      buffer = buffer.slice(nl + 1);
      if (!line.startsWith('data:')) continue;
      try { events.push(JSON.parse(line.slice(5).trim())); } catch { /* ignore */ }
      if (events[events.length - 1]?.type === 'done') break outer;
      if (events[events.length - 1]?.type === 'error') break outer;
    }
  }
  return events;
}

const fails = [];
const assert = (cond, name, detail = '') => {
  console.log(`  ${cond ? 'PASS' : 'FAIL'} ${name}${!cond && detail ? ` —— ${detail}` : ''}`);
  if (!cond) fails.push(name);
};

const agent = spawn(process.execPath, ['node_modules/tsx/dist/cli.mjs', 'server/index.ts'], {
  cwd: WEB,
  env: {
    ...process.env,
    PORT: String(AGENT_PORT),
    LLM_API_BASE: 'http://127.0.0.1:3103/v1',
    LLM_API_KEY: 'mock-key',
    LLM_MODEL: 'mock-model',
  },
  stdio: ['ignore', 'ignore', 'pipe'],
});

let mockServer;
try {
  await new Promise((r) => { mockServer = llm.listen(3103, r); });
  if (!(await waitHealth())) throw new Error('agent 服务器 30s 未就绪');

  // 第一轮：正常读 CLAUDE.md
  const ev1 = await chat('请读取 CLAUDE.md 并总结');
  const types1 = ev1.map((e) => e.type).join(',');
  const toolEv = ev1.find((e) => e.type === 'tool');
  const toolResult = ev1.find((e) => e.type === 'tool_result');
  const textEv = ev1.filter((e) => e.type === 'text').map((e) => e.content).join('');
  const doneEv = ev1.find((e) => e.type === 'done');

  console.log('[SMOKE] 事件序列:', types1);
  assert(types1.startsWith('init,'), 'S1a 首事件为 init');
  assert(toolEv?.name === 'read_file' && toolEv?.input?.path === 'CLAUDE.md', 'S1b 工具调用 read_file(CLAUDE.md)', JSON.stringify(toolEv));
  assert(toolResult && !toolResult.isError && String(toolResult.content).includes(fixtureHead.slice(0, 20).split('\n')[0].slice(0, 10)), 'S2 工具真实读到磁盘内容', toolResult?.content?.slice(0, 80));
  assert(!ev1.some((e) => e.type === 'permission_request'), 'S1c default 模式 read 类无许可请求');
  assert(textEv.includes('MOCK-ENGINE-OK'), 'S3 最终文本经增量拼接', textEv.slice(0, 40));
  assert(doneEv && typeof doneEv.duration === 'number', 'S1d done 携带 duration');
  assert(!ev1.some((e) => e.type === 'error'), 'S1e 无 error 事件');

  // 第二轮：越界路径必须被工具守卫拒绝
  const ev2 = await chat('EVIL-TEST 请读取 ../../.env');
  const evilResult = ev2.find((e) => e.type === 'tool_result');
  assert(evilResult && evilResult.isError && /越界|失败/.test(String(evilResult.content)), 'S4 越界路径被路径守卫拒绝', evilResult?.content?.slice(0, 80));
} catch (e) {
  fails.push(`冒烟异常: ${e?.message || e}`);
  console.error(e);
} finally {
  agent.kill();
  // 拆卸顺序：先断 keep-alive 连接再关监听，等待子进程退出——规避 Windows libuv
  // 「UV_HANDLE_CLOSING」拆卸断言污染退出码（feedback.test.mjs 同族现象）
  mockServer?.closeAllConnections?.();
  mockServer?.close();
  await wait(500);
}

console.log(fails.length === 0 ? '[SMOKE] PASS（4 组断言全绿）' : `[SMOKE] FAIL（${fails.length} 项：${fails.join('；')}）`);
process.exit(fails.length === 0 ? 0 : 1);
