#!/usr/bin/env node
/**
 * check_data_drift.js — M2 双源漂移检查（W424）
 *
 * 背景：可视化页按 file:// 铁律内嵌数据副本（EMBEDDED_DATA / EMBEDDED），
 * 同时运行时 fetch scripts/output/data/*.json（或 dataset/*.json）——
 * 同一份数字存在两个独立维护的源。本检查对比内嵌块与 fetch 目标的
 * 顶层数组长度，把"声明 ≠ 落地"变成机器可查的门禁。
 *
 * v2（W424 扩展）：不再只认 fetch('...') 字面路径——页面常以 `base = '...'`
 * + `fetch(base + f)` / `fetch(path)` 形态加载，但文件名仍是字面量。故改为扫描
 * 页面源码中引用的全部 *.json（指向 scripts/output/data 或 dataset），逐个比对。
 *
 * v3（W767·W760 F-2 修复）：顶层长度口径对深层漂移全失明（实证 85 项 0 捕获）。
 * 增补共路深比对——递归遍历双方皆有的键（仅一侧有之键不计·内嵌子集/复合属设计形态），
 * 数组按位对齐、标量严格比对；声明式基线 `scripts/output/data-drift-baseline.txt`
 * （`页面 ⇄ 源 路径`·[N]→[*] 归一）豁免双形态设计项。语义：基线内豁免、基线外任何
 * 新深层漂移即失败（no-new-drift）。
 *
 * 用法：node scripts/check_data_drift.js
 * 退出码：0 = 通过（或全部不可比）；1 = 发现漂移
 * 仅依赖 Node 标准库。不可比页面（无内嵌块/无对应 JSON）计为跳过，不阻断。
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT } = require('./lib/gate_common');

const SITE_DATA_DIR = path.join(PROJECT_ROOT, 'site', 'data');
const DATASET_DIR = path.join(PROJECT_ROOT, 'dataset');
const OUTPUT_DATA_DIR = path.join(PROJECT_ROOT, 'scripts', 'output', 'data');
const DEPLOYED_COPY_DIR = path.join(SITE_DATA_DIR, 'json');
const DRIFT_BASELINE_PATH = path.join(PROJECT_ROOT, 'scripts', 'output', 'data-drift-baseline.txt');

/** 部署副本数基线（新增 fetch 目标须同步副本后更新此值）。 */
const EXPECTED_DEPLOYED_COPY_COUNT = 47;
const EMBEDDED_BLOCK_RE = /const\s+(EMBEDDED_DATA|EMBEDDED)\s*=\s*(\{[\s\S]*?\n\s*\});/;
const JSON_REF_RE = /['"]([A-Za-z0-9_/.-]+\.json)['"]/g;
const DEPLOYED_COPY_REF_RE = /['"](?:\.\.\/)*(?:\.\/)?(?:data\/)?json\/([A-Za-z0-9_/.-]+\.json)['"]/g;
const FETCH_LITERAL_RE = /fetch\(\s*['"]([^'"]+\.json)['"]\s*\)/g;

// ---------------- JS 字面量 → JSON 规范化 ----------------

/** 逐字符扫描，把 JS 对象字面量中的单引号字符串统一为双引号并剥离注释。 */
function normalizeJsStringLiterals(raw) {
  let out = '';
  let code = '';
  const flushCode = () => { if (code) { out += code; code = ''; } };
  let i = 0;
  while (i < raw.length) {
    const ch = raw[i];
    if (ch === '"' || ch === "'") {
      const quote = ch;
      let j = i + 1;
      let content = '';
      while (j < raw.length && raw[j] !== quote) {
        if (raw[j] === '\\') {
          if (raw[j + 1] === "'") { content += "'"; j += 2; continue; }
          content += raw[j] + (raw[j + 1] || '');
          j += 2;
          continue;
        }
        content += raw[j];
        j += 1;
      }
      if (j >= raw.length) return null;
      flushCode();
      out += '"' + content.replace(/\\/g, '\\\\').replace(/"/g, '\"') + '"';
      i = j + 1;
      continue;
    }
    if (ch === '/' && raw[i + 1] === '/') {
      while (i < raw.length && raw[i] !== '\n') i += 1;
      continue;
    }
    if (ch === '/' && raw[i + 1] === '*') {
      i += 2;
      while (i < raw.length && !(raw[i] === '*' && raw[i + 1] === '/')) i += 1;
      i += 2;
      continue;
    }
    code += ch;
    i += 1;
  }
  flushCode();
  return out;
}

/** 给无引号键加引号，修复数组/对象尾逗号。 */
function quoteBareKeysAndDropTrailingCommas(jsonish) {
  return jsonish
    .replace(/([{,]\s*)([\w$\u00C0-\uFFFF][\w$\u00C0-\uFFFF]*?)(\s*:)/g, '$1"$2"$3')
    .replace(/,,\s*([}\]])/g, '$1');
}

/** JS 对象字面量 → JSON 字符串。失败返回 null。 */
function jsLiteralToJson(raw) {
  const normalized = normalizeJsStringLiterals(raw);
  if (normalized === null) return null;
  return quoteBareKeysAndDropTrailingCommas(normalized);
}

/** 提取页面内嵌数据对象。解析失败返回 null。 */
function extractEmbedded(html) {
  const m = html.match(EMBEDDED_BLOCK_RE);
  if (!m) return null;
  const jsonish = jsLiteralToJson(m[2]);
  if (jsonish === null) return null;
  try {
    return JSON.parse(jsonish);
  } catch {
    return null;
  }
}

// ---------------- 比对 ----------------

/** 顶层数组长度比对（W424 口径）。 */
function compareTopLevelArrayLengths(label, embedded, json) {
  const issues = [];
  const keys = new Set([...Object.keys(embedded), ...Object.keys(json)]);
  for (const k of keys) {
    if (Array.isArray(embedded[k]) && Array.isArray(json[k]) && embedded[k].length !== json[k].length) {
      issues.push(`${label}.${k}: embedded=${embedded[k].length} json=${json[k].length}`);
    }
  }
  return issues;
}

/**
 * 共路深比对（W767）：递归遍历双方皆有的键，数组按位对齐，标量严格比。
 * 仅一侧有的键不计（内嵌为源之子集属设计形态）。深度上限 8 防环。
 */
function deepDiff(embedded, json, label, acc, depth = 0) {
  if (depth > 8) return;
  if (embedded === null || json === null) {
    if (embedded !== json) acc.push(`${label}: null 不一致`);
    return;
  }
  const typeA = typeof embedded;
  const typeB = typeof json;
  if (typeA !== typeB) {
    acc.push(`${label}: 类型 embedded=${typeA} json=${typeB}`);
    return;
  }
  if (typeA === 'object') {
    if (Array.isArray(embedded) && Array.isArray(json)) {
      if (embedded.length !== json.length) {
        acc.push(`${label}: 数组长度 embedded=${embedded.length} json=${json.length}`);
        return;
      }
      for (let i = 0; i < embedded.length; i++) {
        deepDiff(embedded[i], json[i], `${label}[${i}]`, acc, depth + 1);
      }
      return;
    }
    const keys = new Set([...Object.keys(embedded), ...Object.keys(json)]);
    for (const k of keys) {
      if (!(k in embedded) || !(k in json)) continue;
      deepDiff(embedded[k], json[k], `${label}.${k}`, acc, depth + 1);
    }
    return;
  }
  if (embedded !== json) {
    acc.push(`${label}: embedded=${JSON.stringify(embedded)} json=${JSON.stringify(json)}`);
  }
}

// ---------------- 基线 ----------------

function loadDriftBaseline() {
  const set = new Set();
  if (!fs.existsSync(DRIFT_BASELINE_PATH)) return set;
  for (const line of fs.readFileSync(DRIFT_BASELINE_PATH, 'utf-8').split(/\r?\n/)) {
    const s = line.trim();
    if (s && !s.startsWith('#')) set.add(s);
  }
  return set;
}

const normalizeDriftPath = (s) => s.replace(/\[\d+\]/g, '[*]');

// ---------------- 候选 JSON 收集 ----------------

/**
 * 把页面引用的路径解析为候选绝对路径集合（按优先级去重）。
 * 覆盖：字面 fetch、源码中 *.json 引用、-view 页 dataset 回退、EMBEDDED 单源页回退。
 */
function collectCandidateJsonPaths(html, pageName) {
  const candidates = new Set();

  // 1) 字面 fetch 路径
  for (const m of html.matchAll(FETCH_LITERAL_RE)) {
    const rel = m[1].replace(/^\.\.\/\.\.\//, '').replace(/^\.\.\//, '');
    candidates.add(path.join(PROJECT_ROOT, rel));
  }

  // 2) 源码中引用的全部 *.json
  for (const m of html.matchAll(JSON_REF_RE)) {
    const ref = m[1];
    if (ref.startsWith('scripts/output/data/')) {
      candidates.add(path.join(PROJECT_ROOT, ref));
    } else if (ref.startsWith('dataset/')) {
      candidates.add(path.join(PROJECT_ROOT, ref));
    } else if (
      /^(?:\.\.\/)?(?:\.\/)?data\/json\/[A-Za-z0-9_/.-]+\.json$/.test(ref) ||
      /^json\/[A-Za-z0-9_/.-]+\.json$/.test(ref)
    ) {
      const copyPath = path.join(DEPLOYED_COPY_DIR, ref.split('/').pop());
      candidates.add(fs.existsSync(copyPath) ? copyPath : path.join(OUTPUT_DATA_DIR, ref.split('/').pop()));
    } else if (ref.includes('/')) {
      const cleaned = ref
        .replace(/^\.\.\/\.\.\//, '')
        .replace(/^\.\.\//, '')
        .replace(/^output\/data\//, 'scripts/output/data/');
      if (cleaned.startsWith('scripts/output/data/') || cleaned.startsWith('dataset/')) {
        candidates.add(path.join(PROJECT_ROOT, cleaned));
      }
    } else if (/^[A-Za-z0-9_-]+\.json$/.test(ref)) {
      const copyPath = path.join(DEPLOYED_COPY_DIR, ref);
      if (fs.existsSync(copyPath)) {
        candidates.add(copyPath);
      } else {
        for (const base of [DATASET_DIR, OUTPUT_DATA_DIR]) {
          const p = path.join(base, ref);
          if (fs.existsSync(p)) { candidates.add(p); break; }
        }
      }
    }
  }

  // 3) -view 页 → dataset/<kebab>.json
  const datasetFile = path.join(DATASET_DIR, pageName + '.json');
  if (fs.existsSync(datasetFile)) candidates.add(datasetFile);

  // 4) EMBEDDED 单源页回退：页名 kebab→snake 同名原件
  const hasOutputData = [...candidates].some((p) => p.startsWith(OUTPUT_DATA_DIR));
  if (!candidates.size || !hasOutputData) {
    const snakeFile = path.join(OUTPUT_DATA_DIR, pageName.replace(/-/g, '_') + '.json');
    if (fs.existsSync(snakeFile)) candidates.add(snakeFile);
  }

  return candidates;
}

// ---------------- 页面级比对 ----------------

/**
 * 对单个页面与单个 JSON 执行顶层 + 深层比对。
 * JSON 解析失败返回 null（调用方跳过该对比项，与原语义一致）。
 */
function comparePageAgainstJson(embedded, jsonPath, pageStem, driftBaseline, deepIssues, topLevelIssues) {
  let json;
  try {
    json = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
  } catch {
    return null;
  }
  const label = `${pageStem} ⇄ ${path.basename(jsonPath)}`;
  topLevelIssues.push(...compareTopLevelArrayLengths(label, embedded, json));

  const acc = [];
  deepDiff(embedded, json, '$', acc);
  let baselined = 0;
  for (const item of acc) {
    const colon = item.indexOf(': ');
    const pth = normalizeDriftPath(item.slice(0, colon));
    if (driftBaseline.has(`${label} ${pth}`)) baselined++;
    else deepIssues.push(`${label} ${item}`);
  }
  return { baselined };
}

// ---------------- 部署副本对账（W563 D1-a） ----------------

function checkDeployedCopies(pages) {
  const issues = [];
  if (!fs.existsSync(DEPLOYED_COPY_DIR)) return issues;

  const copies = fs.readdirSync(DEPLOYED_COPY_DIR).filter((f) => f.endsWith('.json'));
  const copySet = new Set(copies);

  for (const f of copies) {
    const orig = path.join(OUTPUT_DATA_DIR, f);
    if (!fs.existsSync(orig)) continue; // 原件缺席（个别分析器不在 run_all 产出口径内）跳过
    try {
      const copy = JSON.parse(fs.readFileSync(path.join(DEPLOYED_COPY_DIR, f), 'utf-8'));
      const original = JSON.parse(fs.readFileSync(orig, 'utf-8'));
      issues.push(...compareTopLevelArrayLengths(`副本⇄原件 ${f}`, copy, original));
    } catch {
      issues.push(`副本/原件 JSON 解析失败: ${f}`);
    }
  }

  if (copies.length !== EXPECTED_DEPLOYED_COPY_COUNT) {
    issues.push(`副本数 ${copies.length} != ${EXPECTED_DEPLOYED_COPY_COUNT}（新增 fetch 目标须同步副本后更新该基线）`);
  }

  for (const pg of pages) {
    const html = fs.readFileSync(path.join(SITE_DATA_DIR, pg), 'utf-8');
    for (const m of html.matchAll(DEPLOYED_COPY_REF_RE)) {
      if (!copySet.has(m[1])) issues.push(`${pg} 引用的副本不存在: ${m[1]}`);
    }
  }

  return issues;
}

// ---------------- 主流程 ----------------

function main() {
  const pages = fs.readdirSync(SITE_DATA_DIR).filter((f) => f.endsWith('.html')).sort();
  const driftBaseline = loadDriftBaseline();

  let comparable = 0;
  let skipped = 0;
  let pairs = 0;
  let deepBaselined = 0;
  const topLevelIssues = [];
  const deepIssues = [];
  const skips = [];

  for (const pg of pages) {
    const html = fs.readFileSync(path.join(SITE_DATA_DIR, pg), 'utf-8');
    const embedded = extractEmbedded(html);
    if (!embedded) {
      skipped++;
      skips.push(`${pg} (无内嵌块)`);
      continue;
    }

    const pageStem = pg.replace(/-view\.html$/, '').replace(/\.html$/, '');
    const candidates = [...collectCandidateJsonPaths(html, pageStem)].filter((p) => fs.existsSync(p));
    if (!candidates.length) {
      skipped++;
      skips.push(`${pg} (无可比 JSON)`);
      continue;
    }

    let pageCompared = false;
    for (const jp of candidates) {
      const r = comparePageAgainstJson(embedded, jp, pageStem, driftBaseline, deepIssues, topLevelIssues);
      if (r) {
        pairs++;
        pageCompared = true;
        deepBaselined += r.baselined;
      }
    }
    if (pageCompared) comparable++;
    else {
      skipped++;
      skips.push(`${pg} (JSON 解析失败)`);
    }
  }

  console.log(`数据漂移检查：可比 ${comparable} 页（${pairs} 个 JSON 对比项）/ 跳过 ${skipped} 页`);
  if (skips.length && process.env.DEBUG) {
    skips.forEach((s) => console.log('  -', s));
  }

  const copyIssues = checkDeployedCopies(pages);
  if (copyIssues.length) {
    console.log('副本对账异常：');
    copyIssues.forEach((i) => console.log('  ✗', i));
    process.exit(1);
  }
  console.log(`副本对账 ✓（${EXPECTED_DEPLOYED_COPY_COUNT} 个副本数组长度比对一致 · 页面引用无缺失）`);

  if (deepIssues.length) {
    console.log('发现深层漂移（共路标量·非基线）：');
    deepIssues.forEach((i) => console.log('  ✗', i));
    process.exit(1);
  }
  console.log(`深层比对 ✓（共路标量逐层一致 · 基线豁免 ${deepBaselined} 项）`);

  if (topLevelIssues.length) {
    console.log('发现漂移：');
    topLevelIssues.forEach((i) => console.log('  ✗', i));
    process.exit(1);
  }
  console.log('未发现数组长度漂移 ✓');
}

main();
