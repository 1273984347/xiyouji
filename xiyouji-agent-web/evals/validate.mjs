#!/usr/bin/env node
// validate.mjs — golden-50.jsonl 结构与真实性校验（无 LLM·CI 安全，W598）
// 校验面：50 条 / 分类配比 / id 唯一 / schema 完整 / expect_source_paths 磁盘真实存在 / must_mention 非空
// 用法：node evals/validate.mjs   （违例即退出码 1）
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..'); // 仓库根（xiyouji-agent-web 的上级）
const FILE = path.join(HERE, 'golden-50.jsonl');

const EXPECT_COUNTS = { chapter: 15, character: 10, theme: 10, dataset: 10, ops: 5 };
const lines = fs.readFileSync(FILE, 'utf-8').split('\n').filter(l => l.trim());
const errors = [];
const cases = lines.map((l, i) => {
  try { return JSON.parse(l); } catch (e) { errors.push(`line ${i + 1} JSON 解析失败: ${e.message}`); return null; }
});

const valid = cases.filter(Boolean);
const counts = {};
const ids = new Set();
for (const c of valid) {
  counts[c.category] = (counts[c.category] || 0) + 1;
  if (!c.id || ids.has(c.id)) errors.push(`id 缺失或重复: ${c.id}`);
  ids.add(c.id);
  if (typeof c.question !== 'string' || c.question.length < 8) errors.push(`${c.id} question 过短`);
  if (!Array.isArray(c.expect_source_paths) || c.expect_source_paths.length < 1) errors.push(`${c.id} expect_source_paths 空`);
  else for (const p of c.expect_source_paths) {
    if (!fs.existsSync(path.join(ROOT, p))) errors.push(`${c.id} 路径不存在: ${p}`);
  }
  if (!Array.isArray(c.must_mention) || c.must_mention.length < 1) errors.push(`${c.id} must_mention 空`);
  if (!Array.isArray(c.forbid)) errors.push(`${c.id} forbid 非数组`);
}
for (const [cat, n] of Object.entries(EXPECT_COUNTS)) {
  if ((counts[cat] || 0) !== n) errors.push(`分类 ${cat} 期望 ${n} 实得 ${counts[cat] || 0}`);
}
if (valid.length !== 50) errors.push(`总条数 ${valid.length} != 50`);

if (errors.length) {
  console.log(`[EVALS VALIDATE] FAIL ${errors.length} 项`);
  for (const e of errors.slice(0, 20)) console.log('  FAIL', e);
  process.exit(1);
}
console.log(`[EVALS VALIDATE] 50/50 通过（分类 ${JSON.stringify(counts)}·路径全部真实存在）`);
