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
 * v4（W1231·审计专批「单侧键 1702 条 schema 分歧清理」）：W1155 的单侧键摘要通道把
 * 三类「配对形态差」误计为分歧（实测三态：零顶层键重叠复合包壳 889 / 数组↔对象 570 /
 * 部分重叠 243）⇒ ① 根级配对前置（pairForCompare）：零重叠包壳找「键集全等面板」、
 * 数组↔对象找「元素键集/长度同形数组成员」，唯一命中才降级配对（歧义即回落根级·不猜）；
 * ② 设计性单侧键族豁免（_schema / link_endpoint_schema / *_status——W1141 起 dataset
 * 溯源注记按设计只加在 JSON 面）；③ 单侧键摘要通道语义不变（NOTE 可见不判红），
 * 剩余 NOTE 即真 schema 分歧（数据面对齐另批）。自测：--self-test（8 例·含负样本）。
 *
 * 用法：node scripts/check_data_drift.js
 * 退出码：0 = 通过（或全部不可比）；1 = 发现漂移；2 = 自测失败（--self-test）
 * 仅依赖 Node 标准库。不可比页面（无内嵌块/无对应 JSON）计为跳过，不阻断。
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT } = require('./lib/gate_common');

const SITE_DATA_DIR = path.join(PROJECT_ROOT, 'site', 'data');
// W1265 批一（判据补盲 1-6）：扩面到 site/en（138 页）——原实现只扫 site/data。
const SITE_EN_DIR = path.join(PROJECT_ROOT, 'site', 'en');
// W1265（1-6）：单侧键由「只记 NOTE」升级为**判红**（基线冻结形态）。
const SINGLE_SIDE_BASELINE_PATH = path.join(PROJECT_ROOT, 'scripts', 'output', 'data-drift-singleside-baseline.txt');
const singleSideViolations = [];
const DATASET_DIR = path.join(PROJECT_ROOT, 'dataset');
const OUTPUT_DATA_DIR = path.join(PROJECT_ROOT, 'scripts', 'output', 'data');
const DEPLOYED_COPY_DIR = path.join(SITE_DATA_DIR, 'json');
const DRIFT_BASELINE_PATH = path.join(PROJECT_ROOT, 'scripts', 'output', 'data-drift-baseline.txt');

/** 部署副本数基线（新增 fetch 目标须同步副本后更新此值）。
 *  W1265 批一：47 → 158——并行页面线（W1265 批 C·审查报告 2-7 部署面）已把
 *  135 件真值原件全量部署到 site/data/json/（158 件）⇒ 本常量随部署面同步更新。
 */
const EXPECTED_DEPLOYED_COPY_COUNT = 158;
const EMBEDDED_BLOCK_RE = /const\s+(EMBEDDED_DATA|EMBEDDED)\s*=\s*(\{[\s\S]*?\n\s*\});/;
// W1231：单行形态回退——V8 执行式重写产出 compact 单行对象，多行正则（要求
// `\n\s*});`）对其失配 ⇒ 页面被误计「无内嵌块」跳过（保护面 60→43 实测）。
// 多行优先、失配再试单行（同一行内闭合·不含换行的 lazy 域）。
const EMBEDDED_BLOCK_RE_SINGLE_LINE = /const\s+(EMBEDDED_DATA|EMBEDDED)\s*=\s*(\{[^\n]*\})\s*;/;
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
      out += '"' + content.replace(/[\\"]/g, function (c) { return c === '\\' ? '\\\\' : '\"'; }) + '"';
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
    .replace(/,\s*([}\]])/g, '$1');
}

/** JS 对象字面量 → JSON 字符串。失败返回 null。 */
function jsLiteralToJson(raw) {
  const normalized = normalizeJsStringLiterals(raw);
  if (normalized === null) return null;
  return quoteBareKeysAndDropTrailingCommas(normalized);
}

/** 提取页面内嵌数据对象。解析失败返回 null。 */
function extractEmbedded(html) {
  // W1231：多行形态优先；匹配成功但规范化/解析失败时回退单行形态
  // （V8 执行式重写的 compact 单行对象——多行正则的 lazy 捕获可能提前截断）。
  for (const re of [EMBEDDED_BLOCK_RE, EMBEDDED_BLOCK_RE_SINGLE_LINE]) {
    const m = html.match(re);
    if (!m) continue;
    const jsonish = jsLiteralToJson(m[2]);
    if (jsonish === null) continue;
    try {
      return JSON.parse(jsonish);
    } catch {
      continue;
    }
  }
  return null;
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
// W1155（深度审计 #11）：单侧键摘要通道（计数可见·不进 FAIL·清理为后续批）
const singleSideNotes = [];

// W1231：设计性单侧键族——W1141 起 dataset 溯源注记按设计只加在 JSON 面
// （_schema 量纲声明 / sankey.link_endpoint_schema 端点索引 / *_status 溯源状态）。
// 这类键的「仅 json」不是分歧，记 NOTE 只会淹没真分歧。
function isDesignedSingleSideKey(k) {
  return k === '_schema' || k === 'link_endpoint_schema' || k.endsWith('_status');
}

function sameKeySet(a, b) {
  const ka = Object.keys(a).sort();
  const kb = Object.keys(b).sort();
  return ka.length === kb.length && ka.every((k, i) => k === kb[i]);
}

/** 对象数组成员的元素键集指纹（首元素非平面对象时返回 null）。 */
function elementKeySetFingerprint(arr) {
  if (!arr.length || !arr[0] || typeof arr[0] !== 'object' || Array.isArray(arr[0])) return null;
  return Object.keys(arr[0]).sort().join(',');
}

/**
 * W1231 根级配对前置：把「页面复合包壳 ⇄ 单文档」与「数组↔对象」两类形态差
 * 降级到真实同层的层上比（唯一命中才配对·歧义即回落根级·不猜）。
 * 返回 [{a, b, path}] —— 逐项走 deepDiff。
 */
function pairForCompare(embedded, json) {
  const root = '$';
  const embIsArr = Array.isArray(embedded);
  const jsonIsArr = Array.isArray(json);
  if (embIsArr !== jsonIsArr) {
    // 数组↔对象：在对象侧找与数组同形的数组成员（元素键集同形优先·长度一致兜底）
    const obj = embIsArr ? json : embedded;
    const arr = embIsArr ? embedded : json;
    let picked = null;
    const want = elementKeySetFingerprint(arr);
    if (want) {
      const byShape = Object.keys(obj).filter(
        (k) => Array.isArray(obj[k]) && elementKeySetFingerprint(obj[k]) === want
      );
      if (byShape.length === 1) picked = byShape[0];
    }
    if (picked === null) {
      const byLen = Object.keys(obj).filter((k) => Array.isArray(obj[k]) && obj[k].length === arr.length);
      if (byLen.length === 1) picked = byLen[0];
    }
    if (picked !== null) {
      return embIsArr
        ? [{ a: embedded, b: json[picked], path: root }]
        : [{ a: embedded[picked], b: json, path: `${root}.${picked}` }];
    }
    return [{ a: embedded, b: json, path: root }];
  }
  if (!embIsArr) {
    // 双对象：零顶层键重叠 ⇒ 找 embedded 中键集与 json 根键集全等的包壳面板
    const overlap = Object.keys(embedded).filter((k) => k in json).length;
    if (overlap > 0) return [{ a: embedded, b: json, path: root }];
    const panels = Object.keys(embedded).filter((k) => {
      const v = embedded[k];
      return v && typeof v === 'object' && !Array.isArray(v) && sameKeySet(v, json);
    });
    if (panels.length === 1) return [{ a: embedded[panels[0]], b: json, path: `${root}.${panels[0]}` }];
    return [{ a: embedded, b: json, path: root }];
  }
  return [{ a: embedded, b: json, path: root }];
}

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
      // W1155（深度审计 #11）：单侧键原实现直接 continue ⇒ 键漂移永不报。改记入
      // **单侧键摘要通道**（计数+样例可见·不进 FAIL）——首轮升 FAIL 实测命中 1702 条
      // 存量 schema 分歧，一刀 FAIL 不可执行。
      // W1231：设计性单侧键族（_schema/link_endpoint_schema/*_status）静默跳过——
      // W1141 起 dataset 溯源注记按设计只加在 JSON 面·非分歧；配对形态差已在
      // pairForCompare 降级，剩余 NOTE 即真 schema 分歧（数据面对齐另批）。
      if (!(k in embedded) || !(k in json)) {
        if (!isDesignedSingleSideKey(k)) {
          singleSideNotes.push(label + '.' + k + '（单侧键：' + (k in embedded ? '仅内嵌' : '仅 json') + '）');
        }
        continue;
      }
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

  // W1231：根级配对前置——包壳/数组形态差降级到真实同层再比（歧义回落根级）
  let baselined = 0;
  for (const pr of pairForCompare(embedded, json)) {
    topLevelIssues.push(...compareTopLevelArrayLengths(`${label}${pr.path === '$' ? '' : pr.path}`, pr.a, pr.b));

    const acc = [];
    deepDiff(pr.a, pr.b, pr.path, acc);
    if (singleSideNotes.length) {
      console.log(`  · 单侧键（schema 分歧·W1265 起升级判红·计 ${singleSideNotes.length}·样例：${singleSideNotes.slice(0, 3).join(' | ')}）`);
      // W1265（1-6）：单侧键不再「只记 NOTE」——登记为违例（基线内冻结·基线外判红）。
      for (const n of singleSideNotes) {
        const p = n.replace(/（单侧键：.*$/, '');
        singleSideViolations.push({
          key: `${label} ${normalizeDriftPath(p)}`,
          detail: `${label} ${n}`,
        });
      }
      singleSideNotes.length = 0;
    }
    for (const item of acc) {
      const colon = item.indexOf(': ');
      const pth = normalizeDriftPath(item.slice(0, colon));
      if (driftBaseline.has(`${label} ${pth}`)) baselined++;
      else deepIssues.push(`${label} ${item}`);
    }
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

// ---------------- EN 面比对（W1265·1-6） ----------------

/**
 * EN 页内嵌块 ↔ 真值 JSON 的**翻译容差**结构比对。
 *
 * 口径：EN 页内嵌的是英文副本 ⇒ 字符串值天然不同（翻译差异不是漂移）⇒ 只比：
 *   · 单侧键（键集差）→ 违例（与 ZH 面同判据·W1265 起判红）
 *   · 数组长度不等 → 违例
 *   · 数值标量不等 → 违例
 *   · 类型差（num ↔ str）→ 违例（审查报告 P3-2「单侧键 / 类型差」族）
 *   · 纯字符串值差异 → **不判**（翻译差异）
 * 深度上限 6·元素上限 100（防病态页面爆量）。
 */
function compareEnStructure(a, b, label, path = '$', out = [], depth = 0) {
  if (depth > 6) return out;
  const aObj = a && typeof a === 'object';
  const bObj = b && typeof b === 'object';
  if (!aObj && !bObj) {
    if (typeof a === 'number' && typeof b === 'number') {
      if (Math.abs(a - b) > 1e-9) out.push(`${label} ${path}: 内嵌=${a} 真值=${b}`);
    } else if (typeof a === 'number' !== (typeof b === 'number')) {
      out.push(`${label} ${path}: 类型差 内嵌=${typeof a} 真值=${typeof b}`);
    }
    return out;
  }
  if (!aObj || !bObj) {
    out.push(`${label} ${path}: 形态差 内嵌=${Array.isArray(a) ? 'array' : typeof a} 真值=${Array.isArray(b) ? 'array' : typeof b}`);
    return out;
  }
  const aArr = Array.isArray(a);
  const bArr = Array.isArray(b);
  if (aArr !== bArr) {
    out.push(`${label} ${path}: 形态差 内嵌=${aArr ? 'array' : 'object'} 真值=${bArr ? 'array' : 'object'}`);
    return out;
  }
  if (aArr) {
    if (a.length !== b.length) {
      out.push(`${label} ${path}: 数组长度 内嵌=${a.length} 真值=${b.length}`);
      return out;
    }
    for (let i = 0; i < Math.min(a.length, 100); i++) compareEnStructure(a[i], b[i], label, `${path}[${i}]`, out, depth + 1);
    return out;
  }
  const ak = Object.keys(a);
  const bk = Object.keys(b);
  // W1265 探针口径修正（两轮实测假阳性）：
  //  ① EN 页内嵌块的**对象键是英译标签**（by_cause 下 "Heavenly / Western steeds incarnate"），
  //     真值 JSON 同层键是中文标签 ⇒ 逐键比对把**每条翻译**误报成单侧键（81-hardships 一页 300+ 条）。
  //  ② 只留标识符形态的键仍不够：单字英译（Cave / Mountain / Guanyin）也是标识符形态。
  // ⇒ 最终口径：EN 面**不比键名**——只比「结构位次 + 数值」：
  //     键数不等 → 记 1 条「键数差」（不逐键列名）；键序位次一一对位递归；
  //     数组比长度并按位递归；数值不等 → 违例；字符串差异（翻译）→ 不判。
  if (ak.length !== bk.length) {
    out.push(`${label} ${path}: 键数差 内嵌=${ak.length} 真值=${bk.length}`);
    return out;
  }
  for (let i = 0; i < ak.length; i++) {
    compareEnStructure(a[ak[i]], b[bk[i]], label, `${path}.${ak[i]}`, out, depth + 1);
  }
  return out;
}

/** 扫 EN 面 → 违例列表（每条含 key 与 detail）。 */
function scanEnPages() {
  const viol = [];
  if (!fs.existsSync(SITE_EN_DIR)) return viol;
  const pages = fs.readdirSync(SITE_EN_DIR).filter((f) => f.endsWith('.html')).sort();
  for (const pg of pages) {
    const html = fs.readFileSync(path.join(SITE_EN_DIR, pg), 'utf-8');
    const embedded = extractEmbedded(html);
    if (!embedded) continue;
    const stem = pg.replace(/-view\.html$/, '').replace(/\.html$/, '');
    const candidates = [...collectCandidateJsonPaths(html, stem)].filter((p) => fs.existsSync(p));
    for (const jp of candidates) {
      let json;
      try {
        json = JSON.parse(fs.readFileSync(jp, 'utf-8'));
      } catch {
        continue;
      }
      const label = `site/en/${pg} ⇄ ${path.basename(jp)}`;
      for (const item of compareEnStructure(embedded, json, label)) {
        const colon = item.indexOf(': ');
        const pth = normalizeDriftPath(item.slice(0, colon));
        viol.push({ key: `${label} ${pth}`, detail: item });
      }
      break; // 每页只对第一个可比 JSON（与 ZH 面「可比页」口径一致）
    }
  }
  return viol;
}

// ---------------- 主流程 ----------------

// ---------------- 自测（W1231·8 例含负样本·不读真实仓） ----------------

function selfTest() {
  const acc = [];
  const notes = singleSideNotes;
  let fails = 0;
  let cases = 0;
  const check = (cond, note) => {
    cases++;
    if (!cond) { fails++; console.log('FAIL  ' + note); } else { console.log('OK    ' + note); }
  };
  const notesAfter = (fn) => {
    const before = notes.length;
    fn();
    const n = notes.splice(before).length;
    const accCopy = acc.slice();
    acc.length = 0;
    return { n, acc: accCopy };
  };

  // ① 零重叠包壳·唯一键集全等面板 → 降级配对·0 NOTE·0 acc
  const wrapped = { meta: { x: 1 }, panel: { a: 1, b: [1, 2] } };
  const doc = { a: 1, b: [1, 2] };
  let r = notesAfter(() => { const pr = pairForCompare(wrapped, doc)[0]; deepDiff(pr.a, pr.b, pr.path, acc); });
  check(r.n === 0 && r.acc.length === 0, '① 包壳面板配对：0 NOTE / 0 acc（实测 NOTE=' + r.n + ' acc=' + r.acc.length + '）');

  // ② 零重叠包壳·面板与文档有真值差 → 配对后共路标量差异进 acc
  const doc2 = { a: 1, b: [1, 9] };
  const pr2 = pairForCompare(wrapped, doc2)[0];
  r = notesAfter(() => deepDiff(pr2.a, pr2.b, pr2.path, acc));
  check(r.acc.length === 1 && /b\[1\]/.test(r.acc[0]), '② 包壳配对后真值漂移仍 FAIL 面（acc=' + r.acc.length + '）');

  // ③ 数组↔对象（元素键集唯一命中）→ 降级配对
  const embArrSide = { rhythm: [{ k: 1, v: 'a' }, { k: 2, v: 'b' }], other: 3 };
  const jsonArr = [{ k: 1, v: 'a' }, { k: 2, v: 'X' }];
  const pr3 = pairForCompare(embArrSide, jsonArr)[0];
  r = notesAfter(() => deepDiff(pr3.a, pr3.b, pr3.path, acc));
  check(pr3.path === '$.rhythm' && r.acc.length === 1 && r.n === 0, '③ 数组↔对象配对：路径 $.rhythm·真值差进 acc（path=' + pr3.path + '）');

  // ④ 数组↔对象歧义（两个同形数组成员）→ 回落根级·按单侧键记 NOTE
  const amb = { arr1: [{ k: 1 }], arr2: [{ k: 1 }] };
  r = notesAfter(() => { const pr4 = pairForCompare(amb, [{ k: 1 }])[0]; deepDiff(pr4.a, pr4.b, pr4.path, acc); });
  check(r.n >= 2, '④ 歧义回落根级：单侧键 NOTE 记录（NOTE=' + r.n + '）');

  // ⑤ 设计性单侧键族豁免：_schema / link_endpoint_schema / *_status 不记 NOTE
  r = notesAfter(() => deepDiff({ total: 1 }, { total: 1, _schema: { w: 'max' }, link_endpoint_schema: 'index', quote_status: 'verified' }, '$', acc));
  check(r.n === 0, '⑤ 设计性单侧键族豁免（_schema/link_endpoint_schema/*_status·NOTE=' + r.n + '）');

  // ⑥ 真实单侧键仍记 NOTE
  r = notesAfter(() => deepDiff({ onlyEmb: 1, shared: 2 }, { onlyJson: 2, shared: 2 }, '$', acc));
  check(r.n === 2, '⑥ 真实单侧键仍记 NOTE（NOTE=' + r.n + '）');

  // ⑦ 共路标量漂移仍进 acc（FAIL 面·语义不变）
  r = notesAfter(() => deepDiff({ v: 1 }, { v: 2 }, '$', acc));
  check(r.acc.length === 1 && r.n === 0, '⑦ 共路标量漂移进 acc（acc=' + r.acc.length + '）');

  // ⑧ 数组长度漂移进 acc
  r = notesAfter(() => deepDiff({ list: [1, 2, 3] }, { list: [1, 2] }, '$', acc));
  check(r.acc.length === 1 && /数组长度/.test(r.acc[0]), '⑧ 数组长度漂移进 acc（acc=' + r.acc.length + '）');

  console.log('self-test: ' + (cases - fails) + '/' + cases + ' 通过');
  return fails ? 2 : 0;
}

function main() {
  if (process.argv.includes('--self-test')) {
    process.exit(selfTest());
  }
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

  // W1265（1-6）：EN 面纳入漂移比对 + 单侧键升级判红（基线冻结形态）
  const enViol = scanEnPages();
  const allSingleSide = [...singleSideViolations, ...enViol];
  const ssBaseline = new Set();
  if (fs.existsSync(SINGLE_SIDE_BASELINE_PATH)) {
    for (const line of fs.readFileSync(SINGLE_SIDE_BASELINE_PATH, 'utf-8').split(/\r?\n/)) {
      const s = line.trim();
      if (s && !s.startsWith('#')) ssBaseline.add(s);
    }
  }
  const strict = process.argv.includes('--strict');
  const ssNew = strict ? allSingleSide : allSingleSide.filter((v) => !ssBaseline.has(v.key));
  const ssFrozen = strict ? [] : allSingleSide.filter((v) => ssBaseline.has(v.key));
  if (process.argv.includes('--generate-singleside-baseline')) {
    const lines = [
      '# 数据漂移门禁 · 单侧键基线（W1265 建立·存量 schema 分歧冻结）',
      '# 生成命令：node scripts/check_data_drift.js --generate-singleside-baseline',
      '# 格式：<页面 ⇄ JSON> <归一化路径>',
      '# 语义：基线内不计 FAIL；基线外新增 = FAIL；零容忍：--strict',
      ...allSingleSide.map((v) => v.key).sort(),
    ];
    fs.mkdirSync(path.dirname(SINGLE_SIDE_BASELINE_PATH), { recursive: true });
    fs.writeFileSync(SINGLE_SIDE_BASELINE_PATH, lines.join('\n') + '\n', 'utf-8');
    console.log(`单侧键基线已生成：${path.relative(PROJECT_ROOT, SINGLE_SIDE_BASELINE_PATH)} · ${allSingleSide.length} 条`);
    return;
  }
  console.log(
    `单侧键/EN 面：违例 ${allSingleSide.length} 条（EN 面 ${enViol.length} 条）· 存量基线 ${ssFrozen.length} 条 · ` +
      `基线外新增 ${ssNew.length} 条${strict ? '（零容忍模式·基线不参与判定）' : ''}`
  );

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

  if (ssNew.length) {
    console.log('发现单侧键/EN 面结构分歧（非基线）：');
    ssNew.slice(0, 40).forEach((i) => console.log('  ✗', i.detail));
    if (ssNew.length > 40) console.log(`  …其余 ${ssNew.length - 40} 条略`);
    process.exit(1);
  }

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
