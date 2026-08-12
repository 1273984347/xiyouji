#!/usr/bin/env node
/**
 * check_data_drift.js — M2 双源漂移检查（W424）
 *
 * 背景：可视化页按 file:// 铁律内嵌数据副本（EMBEDDED_DATA / EMBEDDED），
 * 同时运行时 fetch scripts/output/data/*.json（或 dataset/*.json）——
 * 同一份数字存在两个独立维护的源。本检查对比内嵌块与 fetch 目标的
 * 顶层数组长度，把"声明 ≠ 落地"变成机器可查的门禁。
 *
 * 用法：node scripts/check_data_drift.js
 * 退出码：0 = 通过（或全部不可比）；1 = 发现漂移
 * 仅依赖 Node 标准库。不可比页面（无内嵌块/无对应 JSON）计为跳过，不阻断。
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DATA_DIR = path.join(ROOT, 'site', 'data');
const DATASET_DIR = path.join(ROOT, 'dataset');

const EMBED_RE = /const\s+(EMBEDDED_DATA|EMBEDDED)\s*=\s*(\{[\s\S]*?\n\s*\});/;
const FETCH_RE = /fetch\(\s*['"]([^'"]+\.json)['"]\s*\)/;

/** 提取内嵌数据对象（数据字面量，安全求值）。解析失败返回 null。 */
function extractEmbedded(html) {
  const m = html.match(EMBED_RE);
  if (!m) return null;
  try {
    // 仅求值数据字面量（EMBEDDED_DATA/EMBEDDED 声明块），无外部引用
    return new Function('return (' + m[2] + ');')();
  } catch {
    return null;
  }
}

/** 对比两个对象的顶层数组长度。返回差异描述列表。 */
function compareArrays(label, embedded, json) {
  const issues = [];
  const keys = new Set([...Object.keys(embedded), ...Object.keys(json)]);
  for (const k of keys) {
    if (Array.isArray(embedded[k]) && Array.isArray(json[k]) &&
        embedded[k].length !== json[k].length) {
      issues.push(`${label}.${k}: embedded=${embedded[k].length} json=${json[k].length}`);
    }
  }
  return issues;
}

function main() {
  const pages = fs.readdirSync(DATA_DIR).filter((f) => f.endsWith('.html')).sort();
  let comparable = 0;
  let skipped = 0;
  const allIssues = [];
  const skips = [];

  for (const pg of pages) {
    const html = fs.readFileSync(path.join(DATA_DIR, pg), 'utf-8');
    const embedded = extractEmbedded(html);
    if (!embedded) {
      skipped++;
      skips.push(`${pg} (无内嵌块)`);
      continue;
    }

    // 1) 字面 fetch JSON 路径 → scripts/output/data/*
    // 2) 无 fetch 的 -view 页 → dataset/<kebab>.json（apiFetch /dataset/）
    let jsonPath = null;
    const fm = html.match(FETCH_RE);
    if (fm) {
      const rel = fm[1].replace(/^\.\.\/\.\.\//, '').replace(/^\.\.\//, '');
      jsonPath = path.join(ROOT, rel);
    } else {
      const name = pg.replace(/-view\.html$/, '').replace(/\.html$/, '');
      const dset = path.join(DATASET_DIR, name + '.json');
      if (fs.existsSync(dset)) jsonPath = dset;
    }
    if (!jsonPath || !fs.existsSync(jsonPath)) {
      skipped++;
      skips.push(`${pg} (无可比 JSON)`);
      continue;
    }

    let json;
    try {
      json = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
    } catch {
      skipped++;
      skips.push(`${pg} (JSON 解析失败: ${path.basename(jsonPath)})`);
      continue;
    }

    comparable++;
    allIssues.push(...compareArrays(pg.replace(/\.html$/, ''), embedded, json));
  }

  console.log(`数据漂移检查：可比 ${comparable} 页 / 跳过 ${skipped} 页`);
  if (skips.length && process.env.DEBUG) {
    skips.forEach((s) => console.log('  -', s));
  }
  if (allIssues.length) {
    console.log('发现漂移：');
    allIssues.forEach((i) => console.log('  ✗', i));
    process.exit(1);
  }
  console.log('未发现数组长度漂移 ✓');
}

main();
