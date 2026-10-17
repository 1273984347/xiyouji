#!/usr/bin/env node
/**
 * gate_common.js — 门禁脚本公共工具（W775 重构提取）
 *
 * 被 check_chart_values / check_data_drift / check_screenshot_gates 共用：
 * 路径规范化、HTML 枚举、脚本注释剥离、worker 池、门禁汇总行格式。
 *
 * 约束：只含纯工具函数，不含任何门禁判据逻辑——判据留在各门禁脚本内，
 * 避免公共模块变成大杂烩。
 */
'use strict';

const fs = require('fs');
const path = require('path');

const PROJECT_ROOT = path.resolve(__dirname, '..', '..');

/** 统一路径分隔符为 POSIX 风格（报告与基线文件跨平台可读）。 */
function toPosixPath(p) {
  return String(p).replace(/\\/g, '/');
}

/** 相对项目根目录的路径（用于日志与基线文件）。 */
function relativeToRoot(absPath) {
  return toPosixPath(path.relative(PROJECT_ROOT, absPath));
}

/**
 * 递归枚举目录下所有 .html 文件。
 * @param {string} baseDir 绝对路径
 * @param {string} [relPrefix=''] 结果中拼接的相对前缀
 * @returns {string[]} 排序后的相对路径列表
 */
function listHtmlFilesRecursive(baseDir, relPrefix = '') {
  const out = [];
  const entries = fs
    .readdirSync(baseDir, { withFileTypes: true })
    .sort((a, b) => a.name.localeCompare(b.name));
  for (const entry of entries) {
    const rel = relPrefix ? `${relPrefix}/${entry.name}` : entry.name;
    const abs = path.join(baseDir, entry.name);
    if (entry.isDirectory()) {
      out.push(...listHtmlFilesRecursive(abs, rel));
    } else if (entry.name.endsWith('.html')) {
      out.push(rel);
    }
  }
  return out;
}

/**
 * 枚举单层目录下所有 .html 文件（不递归）。
 * @param {string} dir 绝对路径
 * @returns {string[]} 排序后的文件名列表
 */
function listHtmlFilesFlat(dir) {
  return fs.readdirSync(dir).filter((f) => f.endsWith('.html')).sort();
}

/**
 * 剥离 <script> 内注释与 HTML 注释，用于静态签名匹配。
 * 保留脚本内容本身（仅去注释），避免把数据字面量里的关键词误判为代码特征。
 */
function stripScriptComments(html) {
  return html
    .replace(/<script[\s\S]*?<\/script[^>]*>/gi, (block) =>
      block.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/\/\/.*$/gm, ' ')
    )
    .replace(/<!--[\s\S]*?-->/g, ' ');
}

/** 门禁末行固定格式（挂门禁靠这行；缺行 = 未真正扫描 = 未通过）。 */
function gateSummaryLine(gateName, failCount) {
  return `---- ${gateName}：${failCount} FAIL ----`;
}

/**
 * 并发 worker 池：对 items 逐个调用 handler，最多 concurrency 个在飞。
 * 完成顺序不保证（与原脚本 probes.push 语义一致）。
 * @template T,R
 * @param {T[]} items
 * @param {number} concurrency
 * @param {(item: T, index: number) => Promise<R>} handler
 * @returns {Promise<R[]>}
 */
async function runWorkerPool(items, concurrency, handler) {
  const results = [];
  let next = 0;
  async function worker() {
    for (;;) {
      const i = next++;
      if (i >= items.length) break;
      results.push(await handler(items[i], i));
    }
  }
  const n = Math.max(1, Math.min(concurrency, items.length));
  await Promise.all(Array.from({ length: n }, () => worker()));
  return results;
}

module.exports = {
  PROJECT_ROOT,
  toPosixPath,
  relativeToRoot,
  listHtmlFilesRecursive,
  listHtmlFilesFlat,
  stripScriptComments,
  gateSummaryLine,
  runWorkerPool,
};
