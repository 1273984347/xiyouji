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
 *
 * v2（W424 扩展）：不再只认 fetch('...') 字面路径——页面常以 `base = '../../scripts/output/data/'`
 * + `fetch(base + f)` / `fetch(path)` 形态加载，但文件名仍是字面量。故改为扫描页面源码中
 * 引用的全部 *.json（指向 scripts/output/data 或 dataset），逐个与内嵌块比对顶层数组长度。
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DATA_DIR = path.join(ROOT, 'site', 'data');
const DATASET_DIR = path.join(ROOT, 'dataset');

const EMBED_RE = /const\s+(EMBEDDED_DATA|EMBEDDED)\s*=\s*(\{[\s\S]*?\n\s*\});/;
const FETCH_RE = /fetch\(\s*['"]([^'"]+\.json)['"]\s*\)/g;
const JSON_REF_RE = /['"]([A-Za-z0-9_/.-]+\.json)['"]/g;
const OUT_DATA_DIR = path.join(ROOT, 'scripts', 'output', 'data');

/** 字面量规范化：字符串归一双引号 + 去注释 + 无引号键加引号 + 尾逗号修复（W536：替代动态执行）。失败返回 null。 */
function jsLiteralToJson(raw) {
  let out = "";
  let code = "";
  const flush = () => { if (code) { out += code; code = ""; } };
  let i = 0;
  while (i < raw.length) {
    const c = raw[i];
    if (c === "" || c === '') {
      let j = i + 1;
      let content = "";
      while (j < raw.length && raw[j] !== c) {
        if (raw[j] === "\\") {
          if (raw[j + 1] === '') { content += ''; j += 2; continue; }
          content += raw[j] + (raw[j + 1] || ""); j += 2; continue;
        }
        content += raw[j]; j += 1;
      }
      if (j >= raw.length) return null;
      flush();
      out += "" + content.replace(/"/g, '\"') + "";
      i = j + 1;
      continue;
    }
    if (c === '/' && raw[i + 1] === '/') { while (i < raw.length && raw[i] !== "\n") i += 1; continue; }
    if (c === '/' && raw[i + 1] === '*') {
      i += 2;
      while (i < raw.length && !(raw[i] === '*' && raw[i + 1] === '/')) i += 1;
      i += 2;
      continue;
    }
    code += c;
    i += 1;
  }
  flush();
  out = out.replace(/([{,]\s*)([\w$\u00C0-\uFFFF][\w$\u00C0-\uFFFF]*?)(\s*:)/g, '$1"$2"$3');
  out = out.replace(/,,\s*([}\]])/g, '$1');
  return out;
}

/** 提取内嵌数据对象（W536：字面量规范化 + JSON.parse，无动态执行）。解析失败返回 null。 */
function extractEmbedded(html) {
  const m = html.match(EMBED_RE);
  if (!m) return null;
  const norm = jsLiteralToJson(m[2]);
  if (norm === null) return null;
  try {
    return JSON.parse(norm);
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
  let pairs = 0;
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

    // 收集候选 JSON：
    // 1) 字面 fetch 路径（../.. 相对 → ROOT 绝对）
    // 2) 页面源码中引用的全部 *.json（base-variable 形态的 fetch(base + f) 文件名仍是字面量）
    // 3) -view 页 → dataset/<kebab>.json（apiFetch /dataset/）
    const candidates = new Set();
    for (const m of html.matchAll(FETCH_RE)) {
      const rel = m[1].replace(/^\.\.\/\.\.\//, '').replace(/^\.\.\//, '');
      candidates.add(path.join(ROOT, rel));
    }
    for (const m of html.matchAll(JSON_REF_RE)) {
      const ref = m[1];
      if (ref.startsWith('scripts/output/data/')) {
        candidates.add(path.join(ROOT, ref));
      } else if (ref.startsWith('dataset/')) {
        candidates.add(path.join(ROOT, ref));
      } else if (ref.includes('/')) {
        // 相对引用（如 ../../scripts/output/data/xxx.json 或 output/data/xxx.json）
        const cleaned = ref.replace(/^\.\.\/\.\.\//, '').replace(/^\.\.\//, '').replace(/^output\/data\//, 'scripts/output/data/');
        if (cleaned.startsWith('scripts/output/data/') || cleaned.startsWith('dataset/')) {
          candidates.add(path.join(ROOT, cleaned));
        }
      }
    }
    const name = pg.replace(/-view\.html$/, '').replace(/\.html$/, '');
    const dset = path.join(DATASET_DIR, name + '.json');
    if (fs.existsSync(dset)) candidates.add(dset);

    const jsons = [...candidates].filter((p) => fs.existsSync(p));
    if (!jsons.length) {
      skipped++;
      skips.push(`${pg} (无可比 JSON)`);
      continue;
    }

    let pageCompared = false;
    for (const jp of jsons) {
      let json;
      try {
        json = JSON.parse(fs.readFileSync(jp, 'utf-8'));
      } catch {
        continue;
      }
      pageCompared = true;
      pairs++;
      allIssues.push(...compareArrays(
        `${pg.replace(/\.html$/, '')} ⇄ ${path.basename(jp)}`,
        embedded,
        json,
      ));
    }
    if (pageCompared) {
      comparable++;
    } else {
      skipped++;
      skips.push(`${pg} (JSON 解析失败)`);
    }
  }

  console.log(`数据漂移检查：可比 ${comparable} 页（${pairs} 个 JSON 对比项）/ 跳过 ${skipped} 页`);
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
