/**
 * _csp_guard.js — 探针/截图脚本启动前的 CSP 漂移自检（W560 S2）。
 *
 * 背景：改内联脚本后遗忘 `generate_csp.py` 重生成 → 浏览器拒绝执行全部内联脚本
 * → 探针观察到「截图空白 / 图表全空」的假象（W553-W558 会话内 3 次，各误诊 5-10 分钟）。
 *
 * 用法：在探针/截图脚本入口（require 之后、launch 之前）加一行：
 *   require('./_csp_guard').guard();
 * 行为：实跑 generate_csp.py --check；漂移 > 0 时打印修复指引并 exit 1。
 * 豁免：确需在漂移状态下探查时，设环境变量 CSP_GUARD=off 跳过。
 */
const { execFileSync, spawnSync } = require('child_process');
const path = require('path');

// Windows 下 PATH 首位可能是无扩展名的 Git Bash 包装脚本（CreateProcess 9009），
// 依次探测候选命令，取第一个能执行 --help 的。
function resolvePython() {
  for (const cmd of ['python', 'python3', 'py']) {
    try {
      const r = spawnSync(cmd, ['--version'], { encoding: 'utf-8', timeout: 15000 });
      if (r.status === 0) return cmd;
    } catch (e) { /* try next */ }
  }
  return 'python';
}

function guard(root) {
  if (process.env.CSP_GUARD === 'off') return;
  const ROOT = path.resolve(root || path.join(__dirname, '..'));
  let out = '';
  try {
    out = execFileSync(
      resolvePython(),
      [path.join(__dirname, 'generate_csp.py'), '--check'],
      { encoding: 'utf-8', cwd: ROOT, stdio: ['ignore', 'pipe', 'pipe'], timeout: 300000 }
    );
  } catch (e) {
    out = String((e && e.stdout) || '') + String((e && e.stderr) || '');
    console.error('[CSP-GUARD] CSP 漂移：内联脚本哈希与磁盘不一致——页面脚本会被浏览器整体拒绝执行');
    console.error('           （症状：截图空白 / 图表全空 / 元素计数为 0 的探针假象）。');
    const m = out.match(/漂移\/缺失 (\d+) 页/);
    if (m) console.error('[CSP-GUARD] 漂移/缺失页数：' + m[1]);
    console.error('[CSP-GUARD] 修复：python scripts/generate_csp.py && python scripts/generate_csp.py --check');
    console.error('[CSP-GUARD] （确需在漂移状态探查：CSP_GUARD=off 跳过本守卫）');
    process.exit(1);
  }
  const m = out.match(/漂移\/缺失 (\d+) 页/);
  console.log('[CSP-GUARD] ' + (m ? '漂移/缺失 ' + m[1] + ' 页' : out.trim().split('\n').pop()));
}

module.exports = { guard };
