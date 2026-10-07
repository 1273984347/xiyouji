#!/usr/bin/env node
// run_eval.mjs — Agent 黄金评估运行器（W598 建置·W680 引擎更换重写）
//
// 被测对象：本仓 xiyouji-agent-web 引擎（OpenAI-compatible）经 /api/chat 全链路
//   （含 SSE 事件流、工具调用、citationGuard——与用户真实路径一致）。
// 运行器自动起服（tsx spawn，同 feedback.test.mjs 模式），无需手工开服。
//
// 三模式：
//   node evals/run_eval.mjs --self-check        判分器自检（无 LLM·无网络，4 个内置用例）
//   node evals/run_eval.mjs --limit 5           本地真跑前 5 条
//   node evals/run_eval.mjs                     全量 50 条真跑
//
// 前置：xiyouji-agent-web/.env 配置 LLM_API_BASE / LLM_API_KEY / LLM_MODEL（引擎协议兼容
//       所有主流大模型；评估以 bypassPermissions 运行——运行器以 AGENT_WEB_ALLOW_BYPASS=1 起服）。
//
// 判分三规则（机判，W598 口径不变）：
//   ① 回答文本包含每条 expect_source_path（相对路径字符串，/ 与 \ 均认可）且路径磁盘存在
//   ② must_mention 全部命中
//   ③ forbid 零命中
// 输出：evals/results-<日期>.json（score = 通过数 / 总数 + 逐条明细）
// 基线规则：首跑仅建基线不设阈值；连续两批 score 下降 ≥10 个百分点为回归告警。
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const WEB = path.resolve(HERE, '..');            // xiyouji-agent-web/
const ROOT = path.resolve(WEB, '..');            // 仓库根
const PORT = 3210;
const BASE = `http://127.0.0.1:${PORT}`;
const CASE_TIMEOUT_MS = 180 * 1000;              // 单例超时（含多轮工具调用余量）

const CASES = fs.readFileSync(path.join(HERE, 'golden-50.jsonl'), 'utf-8')
  .split('\n').filter(l => l.trim()).map(l => JSON.parse(l));

function normalize(s) { return String(s).replace(/\\/g, '/'); }

// 判分器（--self-check 的被测对象）
export function judge(text, c) {
  const t = normalize(text);
  const missingPaths = c.expect_source_paths.filter(p => !t.includes(normalize(p)));
  const missingMention = c.must_mention.filter(m => !t.includes(m));
  const hitForbid = c.forbid.filter(f => t.includes(f));
  return {
    pass: missingPaths.length === 0 && missingMention.length === 0 && hitForbid.length === 0,
    missingPaths, missingMention, hitForbid,
  };
}

async function selfCheck() {
  const c = { expect_source_paths: ['docs/a.md'], must_mention: ['心猿'], forbid: ['大概'] };
  const t1 = judge('见 docs/a.md，此喻心猿。', c);
  const t2 = judge('见 docs\\a.md，此喻心猿。', c);
  const t3 = judge('此喻心猿，但没给路径。', c);
  const t4 = judge('docs/a.md 中心猿，大概如此。', c);
  const ok = t1.pass && t2.pass && !t3.pass && !t4.pass;
  console.log(`[SELF-CHECK] ${ok ? '4/4 通过' : 'FAIL'} (正/反斜杠路径·缺路径拒判·forbid 拒判)`);
  process.exit(ok ? 0 : 1);
}

const wait = (ms) => new Promise(r => setTimeout(r, ms));

async function waitHealth() {
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch(`${BASE}/api/health`);
      if (r.ok) return true;
    } catch { /* not up yet */ }
    await wait(500);
  }
  return false;
}

/** 消费 /api/chat SSE，返回 {text, error}。 */
async function chatOnce(message) {
  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), CASE_TIMEOUT_MS);
  let text = '';
  let error = '';
  try {
    const resp = await fetch(`${BASE}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        permissionMode: 'bypassPermissions', // 评估为本地无人值守跑批（服务端以 AGENT_WEB_ALLOW_BYPASS=1 起服）
      }),
      signal: ac.signal,
    });
    if (!resp.ok) {
      const detail = await resp.text().catch(() => '');
      return { text: '', error: `HTTP ${resp.status}: ${detail.slice(0, 200)}` };
    }
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
        let ev;
        try { ev = JSON.parse(line.slice(5).trim()); } catch { continue; }
        if (ev.type === 'text') text += ev.content;
        else if (ev.type === 'citation_guard') text = ev.text;
        else if (ev.type === 'error') { error = ev.message || '引擎错误'; break outer; }
        else if (ev.type === 'done') break outer;
      }
    }
  } catch (e) {
    error = e?.name === 'AbortError' ? `单例超时（${CASE_TIMEOUT_MS / 1000}s）` : (e?.message || String(e));
  } finally {
    clearTimeout(timer);
  }
  return { text, error };
}

async function main() {
  const argv = process.argv.slice(2);
  if (argv.includes('--self-check')) return selfCheck();
  const li = argv.indexOf('--limit');
  const limit = li >= 0 ? Number(argv[li + 1]) : CASES.length;
  const cases = CASES.slice(0, limit);

  // 起服（W600 feedback.test.mjs 同款模式）：AGENT_WEB_ALLOW_BYPASS=1 使评估请求可 bypass 无人值守
  const child = spawn(process.execPath, ['node_modules/tsx/dist/cli.mjs', 'server/index.ts'], {
    cwd: WEB,
    env: { ...process.env, PORT: String(PORT), AGENT_WEB_ALLOW_BYPASS: '1' },
    stdio: ['ignore', 'ignore', 'pipe'],
  });
  child.stderr.on('data', () => { /* 服务器日志静默（错误经 SSE error 事件回传） */ });

  try {
    if (!(await waitHealth())) {
      console.error('FAIL 服务器未在 30s 内就绪（检查依赖安装与 tsx）');
      process.exit(1);
    }

    const results = [];
    for (const c of cases) {
      process.stdout.write(`[run] ${c.id} ... `);
      const { text, error } = await chatOnce(
        `${c.question}\n（回答要求：给出可对照的仓库内相对路径；不确定就明说，禁止编造路径。）`
      );
      if (error && !text) console.log(`引擎异常: ${error}`);
      const r = judge(text, c);
      results.push({ id: c.id, ...r, textLen: text.length, ...(error ? { error } : {}) });
      console.log(r.pass ? 'PASS' : `FAIL (缺路径 ${r.missingPaths.length}·缺提及 ${r.missingMention.length}·犯禁 ${r.hitForbid.length}${error ? '·异常' : ''})`);
    }

    const score = results.filter(r => r.pass).length;
    const date = new Date().toISOString().slice(0, 10);
    const out = path.join(HERE, `results-${date}.json`);
    fs.writeFileSync(out, JSON.stringify({ date, total: results.length, score, engine: 'openai-compatible', results }, null, 2) + '\n');
    console.log(`[BASELINE] score=${score}/${results.length} → ${path.relative(ROOT, out)}`);
  } finally {
    child.kill();
  }
}

main().catch(e => { console.error('FATAL', e); process.exit(1); });
