#!/usr/bin/env node
/**
 * py_launch.js — Python 解释器候选表解析（W1014 提取共享·原实现见 check_chart_values.js W753）
 *
 * 背景（W1014 体检）：`batch_screenshots.js` 曾硬编码 `execFileSync('python', …)`，
 * 在本机 PowerShell 语境 `python` 是应用执行存根（调用即 exit 9009），且调用点包在
 * `catch{console.error}` 里 ⇒ 切片静默 fail-open（截图链产物缺 slices/ 仍报成功）。
 * 同仓 `check_chart_values.js` 已有正确候选表范式，按「同一判据禁两处实现」铁则
 * （pitfalls·W909）提取为本模块，两处只调用不重写。
 *
 * 候选序（AGENTS §4.3 三语境）：PYTHON 环境变量 → py -3（Windows launcher）→
 * python3（Linux/macOS 主流）→ python（git-bash 实解释器）。逐个探活
 * `-c "import sys;print(sys.version_info[0])"`，输出以 3 开头才采信。
 *
 * 用法：
 *   const { resolvePython } = require('./lib/py_launch');
 *   const py = resolvePython();            // {cmd, args} 或 null
 *   execFileSync(py.cmd, py.args.concat(['script.py']), …)
 */
'use strict';

const { execFileSync } = require('child_process');

/**
 * 解析可用的 Python 3 解释器。
 * @returns {{cmd: string, args: string[]}|null} 探活成功的候选；全失败返回 null（调用方必须判红，禁静默）
 */
function resolvePython() {
  const cands = [];
  if (process.env.PYTHON) cands.push([process.env.PYTHON, []]);
  cands.push(['py', ['-3']], ['python3', []], ['python', []]);
  for (const [cmd, args] of cands) {
    try {
      const o = execFileSync(cmd, args.concat(['-c', 'import sys;print(sys.version_info[0])']), {
        stdio: 'pipe',
        timeout: 15000,
      })
        .toString()
        .trim();
      if (o.startsWith('3')) return { cmd, args };
    } catch {
      /* 本候选不可用 → 试下一个 */
    }
  }
  return null;
}

module.exports = { resolvePython };
