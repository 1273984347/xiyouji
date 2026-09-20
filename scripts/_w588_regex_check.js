// 检查 PAGE_ANALYSIS_FN 模板字面量解析后的 alpha 正则实况
const fs = require('fs');
const file = fs.readFileSync(__dirname + '/_audit_render_states.js', 'utf8');
// 提取 PAGE_ANALYSIS_FN = `...`; 的字面量并按模板规则求值
const m = file.match(/const PAGE_ANALYSIS_FN = `([\s\S]*?)`;/);
if (!m) { console.log('FN not found'); process.exit(1); }
const cooked = eval('`' + m[1] + '`');
const reMatch = cooked.match(/const am = (\/[^;]+\/)\.exec\(cfill\)/);
if (!reMatch) { console.log('alpha regex not found in resolved FN'); process.exit(1); }
console.log('resolved regex source:', reMatch[1]);
const re = eval(reMatch[1]);
const t1 = re.exec('rgba(0, 0, 0, 0)');
console.log('alpha on rgba(0,0,0,0):', t1 ? t1[1] : null);
const t2 = re.exec('rgb(92, 0, 0)');
console.log('alpha on rgb(92,0,0):', t2 ? t2[1] : 'null(不匹配·不透明跳过逻辑不触发)');
