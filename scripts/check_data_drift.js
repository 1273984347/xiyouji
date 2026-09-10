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
      } else if (/^(?:\.\.\/)?(?:\.\/)?data\/json\/[A-Za-z0-9_/.-]+\.json$/.test(ref) || /^json\/[A-Za-z0-9_/.-]+\.json$/.test(ref)) {
        // W563：A-3 改写后的部署副本形态（site/data/json/）→ 对账回原件
        candidates.add(path.join(OUT_DATA_DIR, ref.split('/').pop()));
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
    // W563：EMBEDDED 单源页（无 fetch）回退——页名 kebab→snake 同名原件存在即纳入对账
    if (!candidates.size || ![...candidates].some((p) => p.startsWith(OUT_DATA_DIR))) {
      const snake = path.join(OUT_DATA_DIR, name.replace(/-/g, '_') + '.json');
      if (fs.existsSync(snake)) candidates.add(snake);
    }

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

  // W563（D1-a）：部署副本对账——site/data/json/ ↔ scripts/output/data/，
  // 比对语义沿用本门禁 W424 惯例（顶层数组长度）：run_all 再生成产物跨环境字节不稳定
  // （CI Linux/本地 Windows 行尾与遍历序差异），字节级强对账由 scripts/_check_json_copies.py
  // 本地自检承担。原件在 CI 缺席时（个别分析器不在 run_all 产出口径内）跳过，对齐
  // 既有「无可比 JSON」语义。另：页面引用的每个副本目标必须存在（防新增 fetch 漏复制）。
  const copiesDir = path.join(ROOT, 'site', 'data', 'json');
  const copyIssues = [];
  if (fs.existsSync(copiesDir)) {
    const copies = fs.readdirSync(copiesDir).filter((f) => f.endsWith('.json'));
    const copySet = new Set(copies);
    let comparedCopies = 0;
    let skippedCopies = 0;
    for (const f of copies) {
      const orig = path.join(OUT_DATA_DIR, f);
      if (!fs.existsSync(orig)) {
        skippedCopies++;
        continue;
      }
      try {
        const c = JSON.parse(fs.readFileSync(path.join(copiesDir, f), 'utf-8'));
        const o = JSON.parse(fs.readFileSync(orig, 'utf-8'));
        comparedCopies++;
        copyIssues.push(...compareArrays(`副本⇄原件 ${f}`, c, o));
      } catch {
        copyIssues.push(`副本/原件 JSON 解析失败: ${f}`);
      }
    }
    if (copies.length !== 47) {
      copyIssues.push(`副本数 ${copies.length} != 47（新增 fetch 目标须同步副本后更新该基线）`);
    }
    const copyRefRe = /['"](?:\.\.\/)*(?:\.\/)?(?:data\/)?json\/([A-Za-z0-9_/.-]+\.json)['"]/g;
    for (const pg of pages) {
      const html = fs.readFileSync(path.join(DATA_DIR, pg), 'utf-8');
      for (const m of html.matchAll(copyRefRe)) {
        if (!copySet.has(m[1])) {
          copyIssues.push(`${pg} 引用的副本不存在: ${m[1]}`);
        }
      }
    }
  }

  if (copyIssues.length) {
    console.log('副本对账异常：');
    copyIssues.forEach((i) => console.log('  ✗', i));
    process.exit(1);
  }
  console.log(`副本对账 ✓（47 个副本数组长度比对一致 · 页面引用无缺失）`);
  if (allIssues.length) {
    console.log('发现漂移：');
    allIssues.forEach((i) => console.log('  ✗', i));
    process.exit(1);
  }
  console.log('未发现数组长度漂移 ✓');
}

main();
