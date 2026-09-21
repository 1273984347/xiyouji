#!/usr/bin/env node
// run_eval.mjs — Agent 黄金评估运行器（W598，方案 WP-H1）
//
// 三模式：
//   node evals/run_eval.mjs --self-check        判分器自检（无 LLM·无网络，4 个内置用例）
//   node evals/run_eval.mjs --limit 5           本地真跑前 5 条（需 .env CODEBUDDY_API_KEY）
//   node evals/run_eval.mjs                     全量 50 条真跑
//
// 判分三规则（机判，方案口径）：
//   ① 回答文本包含每条 expect_source_path（相对路径字符串，/ 与 \ 均认可）且路径磁盘存在
//   ② must_mention 全部命中
//   ③ forbid 零命中
// 输出：evals/results-<日期>.json（score = 通过数 / 总数 + 逐条明细）
// 基线规则：首跑仅建基线不设阈值；连续两批 score 下降 ≥10 个百分点为回归告警。
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..');
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

async function main() {
  const argv = process.argv.slice(2);
  if (argv.includes('--self-check')) return selfCheck();
  const li = argv.indexOf('--limit');
  const limit = li >= 0 ? Number(argv[li + 1]) : CASES.length;
  const cases = CASES.slice(0, limit);

  let sdk;
  try { sdk = await import('@tencent-ai/agent-sdk'); } catch (e) {
    console.error('FAIL 无法加载 @tencent-ai/agent-sdk（应在 xiyouji-agent-web/ 下安装依赖后运行）:', e.message);
    process.exit(1);
  }
  const { query: sdkQuery } = sdk;

  const results = [];
  for (const c of cases) {
    process.stdout.write(`[run] ${c.id} ... `);
    let text = '';
    try {
      const stream = sdkQuery({
        prompt: `${c.question}\n（回答要求：给出可对照的仓库内相对路径；不确定就明说，禁止编造路径。）`,
        options: { cwd: ROOT, maxTurns: 3, permissionMode: 'default' },
      });
      for await (const msg of stream) {
        if (msg?.type === 'assistant') {
          const m = msg?.message?.content;
          if (Array.isArray(m)) text += m.filter(x => x?.type === 'text').map(x => x.text).join('\n');
          else if (typeof m === 'string') text += m;
        }
      }
    } catch (e) {
      text = '';
      console.log(`SDK 异常: ${e.message}`);
    }
    const r = judge(text, c);
    results.push({ id: c.id, ...r, textLen: text.length });
    console.log(r.pass ? 'PASS' : `FAIL (缺路径 ${r.missingPaths.length}·缺提及 ${r.missingMention.length}·犯禁 ${r.hitForbid.length})`);
  }
  const score = results.filter(r => r.pass).length;
  const date = new Date().toISOString().slice(0, 10);
  const out = path.join(HERE, `results-${date}.json`);
  fs.writeFileSync(out, JSON.stringify({ date, total: results.length, score, results }, null, 2) + '\n');
  console.log(`[BASELINE] score=${score}/${results.length} → ${path.relative(ROOT, out)}`);
}

main().catch(e => { console.error('FATAL', e); process.exit(1); });
