// -*- coding: utf-8 -*-
// 一次性：修复 7 个 EN 页内联 script 中字符串字面量内的裸双引号（英化腐蚀残留）。
// 策略：状态机逐行扫描——在双引号字符串内遇到未转义 " 时，向后看判定：
//   若后随字符属于 {, } ) : ; 行尾} 或 空白+其中之一 => 字符串结束定界符（保留）
//   否则 => 字符串内部裸引号 => 替换为弯引号 “/”
// 迭代「编译-定位-修复」直至整页 0 语法错误。全程打印修复留痕。
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const PAGES = ['century-dialogue', 'famous-time-travel', 'mbti-evolution', 'narrative-experiment', 'perf-canvas-rendering', 'relationships', 'search']
  .map(f => path.join(ROOT, 'site/en', f + '.html'));

function compileErrLine(code) {
  try { new vm.Script(code); return null; }
  catch (e) {
    const m = String(e.stack).match(/<anonymous>:(\d+)/);
    return m ? +m[1] : -1;
  }
}

// 修复单行内的裸双引号，返回 {fixed, count}
function fixLine(line) {
  let out = '', inStr = null, esc = false, count = 0;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (inStr) {
      if (esc) { esc = false; out += c; continue; }
      if (c === '\\') { esc = true; out += c; continue; }
      if (c === inStr) {
        // 向后看判定定界符（双引号与单引号字符串同规则）
        let j = i + 1;
        while (j < line.length && line[j] === ' ') j++;
        const next = j >= line.length ? '' : line[j];
        const isTerminator = next === '' || ',}):;+]'.includes(next);
        if (!isTerminator) {
          if (inStr === '"') {
            const prev = out.trimEnd().slice(-1) || '';
            out += /[\w).,;:!?-]/.test(prev) ? '”' : '“';
            count++;
            continue;
          } else {
            // 单引号字符串内的裸撇号（Laojun's / Chang'e 类）→ 右单弯引号
            out += '’';
            count++;
            continue;
          }
        }
        inStr = null; out += c; continue;
      }
      out += c; continue;
    }
    if (c === '"' || c === "'") { inStr = c; out += c; continue; }
    out += c;
  }
  return { fixed: out, count };
}

let totalFix = 0;
for (const pagePath of PAGES) {
  let html = fs.readFileSync(pagePath, 'utf-8');
  const re = /<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/g;
  let m, blockIdx = 0, pageFix = 0;
  let rebuilt = '', last = 0;
  while ((m = re.exec(html))) {
    blockIdx++;
    const code = m[1];
    if (!code.trim()) continue;
    let lines = code.split('\n');
    let guard = 0;
    while (guard++ < 50) {
      const cur = lines.join('\n');
      const errLn = compileErrLine(cur);
      if (errLn === null) break;
      if (errLn < 1 || errLn > lines.length) { console.log('[无法定位]', pagePath, '块', blockIdx); break; }
      const before = lines[errLn - 1];
      const { fixed, count } = fixLine(before);
      if (count === 0) { console.log('[规则未命中]', path.basename(pagePath), '块', blockIdx, '行', errLn, ':', before.trim().slice(0, 100)); break; }
      lines[errLn - 1] = fixed;
      pageFix += count;
      console.log('[修复]', path.basename(pagePath), '块' + blockIdx + ' 行' + errLn, '·', count, '处');
      console.log('  前:', before.trim().slice(0, 130));
      console.log('  后:', fixed.trim().slice(0, 130));
    }
    rebuilt += html.slice(last, m.index) + m[0].replace(code, lines.join('\n'));
    last = re.lastIndex;
  }
  rebuilt += html.slice(last);
  if (pageFix > 0) fs.writeFileSync(pagePath, rebuilt, 'utf-8');
  totalFix += pageFix;
  console.log('==', path.basename(pagePath), '修复', pageFix, '处 ==');
}
console.log('---- 全部完成，共修复', totalFix, '处 ----');
