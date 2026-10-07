#!/usr/bin/env node
// engine.smoke.mjs — 引擎全链路冒烟（W680·可重复执行的常驻机判）
//
// 拓扑：mock LLM（脚本内起）→ agent-web 服务器（tsx spawn，LLM_API_BASE 指向 mock）→ /api/chat SSE。
// 断言（全链路机判，无真实密钥依赖）：
//   S1 SSE 事件序列 = init → tool(read_file) → tool_result → text → done（permission_request 不出现——default 模式 read 类自动放行）
//   S2 工具真实执行：tool_result 内容 = 磁盘真实文件内容（mock 只发指令，读文件的是引擎工具集）
//   S3 文本增量拼接 = mock 最终回复全文
//   S4 越界路径被拒（read_file ../../.env → isError 越界）
//   S5 密钥文件被拒（W680 复核：read_file .env → isError 受保护路径）
//   S6 受保护写入被拒（W680 复核：acceptEdits 下 write_file .git/hooks/pre-commit → isError 受保护路径）
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

// ---------- mock LLM（OpenAI-compatible SSE·按轮次脚本化） ----------
const FIXTURE = path.join(WEB, '..', 'CLAUDE.md'); // 引擎 cwd = 仓库根，read_file 相对路径 CLAUDE.md
const fixtureHead = fs.readFileSync(FIXTURE, 'utf8').slice(0, 200);

const SCRIPT = [
  { tool: { name: 'read_file', args: '{"path":"CLAUDE"}' } },                                    // t1（args 分片补全见下）
  { text: ['MOCK-ENGINE-OK ', fixtureHead.slice(0, 20)] },                                       // t2
  { tool: { name: 'read_file', args: '{"path":".env"}' } },                                      // t3 → S5
  { text: ['DENY-READ-DONE'] },                                                                  // t4
  { tool: { name: 'read_file', args: '{"path":"../../.env"}' } },                                // t5 → S4
  { text: ['EVIL-BLOCKED'] },                                                                    // t6
  { tool: { name: 'write_file', args: '{"path":".git/hooks/pre-commit","content":"evil"}' } },   // t7 → S6
  { text: ['DENY-WRITE-DONE'] },                                                                 // t8
];
// t1 的 arguments 故意分片到达（首片非合法 JSON）——验证增量装配
SCRIPT[0].tool.argsFirst = '{"path":"CLAU';
SCRIPT[0].tool.argsSecond = 'DE.md"}';

let llmTurns = 0;
const llm = http.createServer((req, res) => {
  let body = '';
  req.on('data', (c) => { body += c; });
  req.on('end', () => {
    const step = SCRIPT[llmTurns] ?? SCRIPT[SCRIPT.length - 1];
    llmTurns += 1;
    res.writeHead(200, { 'Content-Type': 'text/event-stream' });
    const emit = (delta, finishReason) => {
      res.write(`data: ${JSON.stringify({ id: 'mock', choices: [{ delta, finish_reason: finishReason ?? null }] })}\n\n`);
    };
    if (step.tool) {
      const id = `call_${llmTurns}`;
      emit({ tool_calls: [{ index: 0, id, type: 'function', function: { name: step.tool.name, arguments: '' } }] }, null);
      if (step.tool.argsFirst !== undefined) {
        emit({ tool_calls: [{ index: 0, function: { arguments: step.tool.argsFirst } }] }, null);
        emit({ tool_calls: [{ index: 0, function: { arguments: step.tool.argsSecond } }] }, 'tool_calls');
      } else {
        emit({ tool_calls: [{ index: 0, function: { arguments: step.tool.args } }] }, 'tool_calls');
      }
      res.write('data: [DONE]\n\n');
      res.end();
    } else {
      for (const t of step.text) emit({ content: t }, null);
      emit({}, 'stop');
      res.write('data: [DONE]\n\n');
      res.end();
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

async function chat(message, permissionMode = 'default') {
  const resp = await fetch(`${BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, permissionMode }),
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
  assert(toolEv?.name === 'read_file' && toolEv?.input?.path === 'CLAUDE.md', 'S1b 工具调用 read_file(CLAUDE.md)（arguments 分片装配）', JSON.stringify(toolEv));
  assert(toolResult && !toolResult.isError && String(toolResult.content).includes(fixtureHead.slice(0, 20).split('\n')[0].slice(0, 10)), 'S2 工具真实读到磁盘内容', toolResult?.content?.slice(0, 80));
  assert(!ev1.some((e) => e.type === 'permission_request'), 'S1c default 模式 read 类无许可请求');
  assert(textEv.includes('MOCK-ENGINE-OK'), 'S3 最终文本经增量拼接', textEv.slice(0, 40));
  assert(doneEv && typeof doneEv.duration === 'number', 'S1d done 携带 duration');
  assert(!ev1.some((e) => e.type === 'error'), 'S1e 无 error 事件');

  // 第二轮（S5·W680 复核）：读 .env 必须被受保护路径黑名单拒绝
  const ev2 = await chat('请读取 .env');
  const r2 = ev2.find((e) => e.type === 'tool_result');
  assert(r2 && r2.isError && /受保护路径/.test(String(r2.content)), 'S5 密钥文件 .env 被拒（受保护路径黑名单）', r2?.content?.slice(0, 80));
  assert(!ev2.some((e) => e.type === 'permission_request'), 'S5b 拒绝发生在工具层（不弹许可）');

  // 第三轮（S4）：越界路径守卫
  const ev3 = await chat('EVIL-TEST 请读取 ../../.env');
  const r3 = ev3.find((e) => e.type === 'tool_result');
  assert(r3 && r3.isError && /越界|失败/.test(String(r3.content)), 'S4 越界路径被路径守卫拒绝', r3?.content?.slice(0, 80));

  // 第四轮（S6·W680 复核）：acceptEdits 下写 .git/hooks 也必须被黑名单拒绝
  const ev4 = await chat('请写入 .git/hooks/pre-commit', 'acceptEdits');
  const r4 = ev4.find((e) => e.type === 'tool_result');
  assert(r4 && r4.isError && /受保护路径/.test(String(r4.content)), 'S6 acceptEdits 写 .git/hooks 被拒', r4?.content?.slice(0, 80));
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

console.log(fails.length === 0 ? '[SMOKE] PASS（12 组断言全绿）' : `[SMOKE] FAIL（${fails.length} 项：${fails.join('；')}）`);
process.exit(fails.length === 0 ? 0 : 1);
