#!/usr/bin/env node
/**
 * check_js_syntax.js — 全站内联 <script> 语法门禁（node 单进程批量编译，秒级）
 *
 * 背景（W457）：原 check_js_syntax.py 每块 spawn 一次 `node --check`，
 * 全站 233 页 1200+ 块在 pre-commit 时限内跑不完。本脚本用 vm.Script
 * 单进程内批量编译，覆盖 site/ 根 + data + en 全部 HTML（排除 _ 前缀模板）。
 * 拦截 EN 引号/撇号/键名腐蚀导致的 SyntaxError（W457 曾 7 页漏网）。
 *
 * 用法：node scripts/check_js_syntax.js
 * 退出码：0 = 全部通过；1 = 发现语法错误
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');

function collectHtml(dir) {
  const out = [];
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) out.push(...collectHtml(p));
    else if (name.endsWith('.html') && !name.startsWith('_')) out.push(p);
  }
  return out;
}

const SCRIPT_RE = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g;

function checkFile(file) {
  const html = fs.readFileSync(file, 'utf-8');
  const rel = path.relative(ROOT, file).replace(/\\/g, '/');
  let m, idx = 0, errors = [];
  SCRIPT_RE.lastIndex = 0;
  while ((m = SCRIPT_RE.exec(html))) {
    idx++;
    const code = m[1].replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
    if (!code.trim()) continue;
    try { new vm.Script(code); }
    catch (e) {
      const lm = String(e.stack).match(/<anonymous>:(\d+)/);
      const line = lm ? +lm[1] : -1;
      errors.push({ rel, idx, msg: e.message, line });
    }
  }
  return errors;
}

const files = collectHtml(SITE);
const allErrors = [];
for (const f of files) allErrors.push(...checkFile(f));

if (allErrors.length) {
  console.log('=== 全站内联脚本语法错误 ' + allErrors.length + ' 处 ===');
  for (const e of allErrors) {
    console.log('[FAIL] ' + e.rel + ' script ' + e.idx + ' (行 ' + e.line + '): ' + e.msg);
  }
  process.exit(1);
}
console.log('OK    全站内联脚本语法通过（' + files.length + ' 文件）');
process.exit(0);
