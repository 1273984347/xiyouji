#!/usr/bin/env node
/**
 * check_vermilion_solid.js — 第 49 门禁 · 朱砂实底限额（W883 新建·v4 规格 §3.2 阶段 5 落地）
 *
 * ## 为什么需要它
 *
 * W826 裁决 2（朱砂实底每页 ≤3 处·严口径）自 W864 起由 B 渠迁移批逐页收敛，
 * 豁免登记簿（scripts/output/_w864_accent_exemptions.json）随批记「 justified 残留」。
 * 但**没有任何常驻门禁守着这条线**——回归（新实底、回吞、误改）只能靠人工发现。
 * 本门禁把裁决 2 变成机器断言：浏览器计算样式实测 + 豁免扣减 + 每页 >3 → FAIL。
 *
 * ## 判据（与豁免登记簿 criterion 逐字对齐·不另立口径）
 *
 * - 测量（浅色主题·file:// 直开·禁起 http 服务）：元素**自身**
 *   background-color == --accent（rgb(200,70,58)）且盒面积 >400px²；或
 *   border-top-color == --accent 且 border-top-width ≥2px 且条带面积（宽×边框宽）>400px²；
 * - 限额：每页**非豁免计数 >3 → FAIL**（v4 §3.2 严口径·白名单：文字/描边/≤3px 指示条/
 *   图表数据填充不属实底·其中指示条由 ≥2px 顶条判据自动排除）；
 * - 豁免：读登记簿·按 (page, tag.class) 计数扣减·扣成负数的页记 NOTE（陈旧豁免）；
 * - fail-closed：任何页面探针异常/超时 → 该页记 probe_error 且非豁免计数按超限处理
 *   （没有证据不许说通过·与第 43 门禁同族纪律）；
 * - 汇总行恒为 `---- 第 49 门禁 朱砂实底：N FAIL ----` 形态且为最后一行 stdout。
 *
 * ## 增量缓存（浏览器门禁的全站成本控制）
 *
 * 96 页全扫约 4-5 分钟——不能每提交都付。缓存按页内容 sha1 只重扫变页
 * （scripts/output/_vermilion_solid_cache.json·随批入库）；--full 强制全量。
 * 缓存命中即复用该页分类计数——判据是纯函数（judgePage）·测量与判定分离。
 *
 * ## 范围
 *
 * site/data/*.html（88·含模板壳 _shell）+ site/ 根 8 页（除 _template.html）= 96 页
 * （= W876 审计器同面·B 渠收敛面）。reader/en 待各自迁移批落地后扩范围（④ 顺带）。
 *
 * 用法：
 *   node scripts/check_vermilion_solid.js            # 增量跑（默认）
 *   node scripts/check_vermilion_solid.js --full     # 强制全量
 *   node scripts/check_vermilion_solid.js --pages data/81-hardships.html,index.html
 *   node scripts/check_vermilion_solid.js --self-test
 * 退出码：0 = 0 FAIL · 1 = 有 FAIL · 2 = 用法/环境错误（缺 marker·由 StrictGate 记 crash）
 */

'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const MARKER = '---- 第 49 门禁 朱砂实底：';
const CACHE_VERSION = 1;
const LIMIT = 3;
const AREA_MIN = 400;
const BORDER_MIN_PX = 2;
const ACCENT = 'rgb(200, 70, 58)';
const DEFAULT_EXEMPTIONS = 'scripts/output/_w864_accent_exemptions.json';
const DEFAULT_CACHE = 'scripts/output/_vermilion_solid_cache.json';
const DEFAULT_REPORT = 'scripts/output/_vermilion_solid_report.json';

// ---------- 纯逻辑（导出供单测·不触浏览器） ----------

/** 归一化类键：tag + '.' + class 属性各段（与豁免登记簿 "span.tag" 形态一致）。 */
function normalizeCls(tag, cls) {
  const parts = String(cls || '').trim().split(/\s+/).filter(Boolean);
  return parts.length ? `${tag}.${parts.join('.')}` : tag;
}

/**
 * 豁免键归一化：登记簿部分条目的 cls 带中文批注（如 "div.scene-bar（热力图行内）"
 * "span（无类名色片）"·W866/W870/W872 三批共 3 条），且同族条目用复合键
 * "span.tag / span.tag.palace"（计数为族合计）——批注是说明不是类名·逐段剥掉；
 * 复合键的 " / " 分隔保留（由 judgePage 展开分配·防「豁免在簿里却对不上账」的假红）。
 */
function normalizeExemptCls(cls) {
  return String(cls || '')
    .split(' / ')
    .map((seg) => seg.split('（')[0].trim())
    .filter(Boolean)
    .join(' / ');
}

/**
 * 判定一页：measuredByCls {cls: n} - exemptByCls {cls: n} → 每类扣减后求和非负。
 * exemptByCls 可含**复合键** "A / B"（登记簿同族合并条目·计数为族合计）——
 * 按各类实测量从大到小贪婪分配（页总口径下分配顺序不影响结果·W883 实证：
 * 登记簿 W864/W866 时代条目大量使用 "A / B" 合并计数·按单键匹配会整族丢豁免）。
 * 返回 {perCls: {cls: {measured, exempted, nonExempt}}, nonExempt, fail, staleExempt}。
 */
function judgePage(measuredByCls, exemptByCls) {
  const stale = [];
  // 1) 复合键展开（贪婪·按实测降序）
  const flat = {};
  for (const [key, n] of Object.entries(exemptByCls || {})) {
    const parts = key.split(' / ').map((s) => s.trim()).filter(Boolean);
    if (parts.length <= 1) {
      flat[key] = (flat[key] || 0) + n;
      continue;
    }
    let remain = n;
    for (const p of [...parts].sort((a, b) => (measuredByCls[b] || 0) - (measuredByCls[a] || 0))) {
      if (remain <= 0) break;
      const take = Math.min(remain, measuredByCls[p] || 0);
      if (take > 0) {
        flat[p] = (flat[p] || 0) + take;
        remain -= take;
      }
    }
    if (remain > 0) stale.push(`${key}（族合计 ${n}·实测不足 ${remain}）`);
  }
  // 2) 逐类扣减
  const perCls = {};
  let nonExempt = 0;
  const keys = new Set([...Object.keys(measuredByCls || {}), ...Object.keys(flat)]);
  for (const cls of keys) {
    const measured = measuredByCls[cls] || 0;
    const exempted = flat[cls] || 0;
    const rest = Math.max(0, measured - exempted);
    if (exempted > measured) stale.push(cls);
    perCls[cls] = { measured, exempted, nonExempt: rest };
    nonExempt += rest;
  }
  return { perCls, nonExempt, fail: nonExempt > LIMIT, staleExempt: stale };
}

/** 读豁免登记簿 → Map<`${page}|${cls}`, count>（跨批次分册求和·cls 批注剥离）。 */
function loadExemptions(file) {
  const abs = path.isAbsolute(file) ? file : path.join(ROOT, file);
  const data = JSON.parse(fs.readFileSync(abs, 'utf-8'));
  const out = new Map();
  const batches = data.batches || {};
  for (const [batch, rec] of Object.entries(batches)) {
    for (const e of rec.exemptions || []) {
      const key = `${e.page}|${normalizeExemptCls(e.cls)}`;
      out.set(key, (out.get(key) || 0) + (e.count || 0));
      if (batch && !e.reason) throw new Error(`豁免条目缺 reason（${batch} ${e.page} ${e.cls}）`);
    }
  }
  return out;
}

/**
 * 增量选页：scope rels × 缓存 × sha1 → {toScan, cached}。
 * sha1Of(rel) 返回该页内容哈希（注入式·单测可假造）。
 */
function selectPagesToScan(scopeRels, cache, sha1Of) {
  const pages = (cache && cache.pages) || {};
  const toScan = [];
  const cached = {};
  const seen = new Set();
  for (const rel of scopeRels) {
    seen.add(rel);
    const sha1 = sha1Of(rel);
    const hit = pages[rel];
    if (hit && hit.sha1 === sha1) {
      cached[rel] = { sha1, counts: hit.counts || {} };
    } else {
      toScan.push(rel);
    }
  }
  return { toScan, cached, pruned: Object.keys(pages).filter((r) => !seen.has(r)) };
}

/**
 * 页面内测量（真函数 + evaluate 传参·Node 版 playwright 对字符串表达式不自动调用·
 * W883 首跑实证「hits is not iterable」）：朱砂实底元素 → [{tag, cls, kind, area}]。
 * 口径同 accent_audit.py 与豁免登记簿 criterion。
 */
function measureInPage(cfg) {
  const { accent, areaMin, borderMin } = cfg;
  const transparent = (c) => c === 'rgba(0, 0, 0, 0)' || c === 'transparent';
  const out = [];
  for (const el of document.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const bgArea = (cs.backgroundColor === accent) ? r.width * r.height : 0;
    const bw = parseFloat(cs.borderTopWidth) || 0;
    const borderArea = (cs.borderTopColor === accent && bw >= borderMin)
      ? r.width * bw : 0;
    const area = Math.max(bgArea, borderArea);
    if (area > areaMin) {
      out.push({ tag: el.tagName.toLowerCase(), cls: el.getAttribute('class') || '',
                 kind: bgArea > 0 ? 'background' : 'border-top', area: Math.round(area) });
    }
  }
  return out;
}

/**
 * 幂等 JSON 写入：内容（除 generated_at）未变则不落盘——pre-commit 会实跑本门禁，
 * 若每次都重写时间戳，cache/report 在提交瞬间自造「工作树残留」把 C4-f 打红（W883 实证）。
 */
function writeJsonStable(file, obj) {
  let old = null;
  try { old = JSON.parse(fs.readFileSync(file, 'utf-8')); } catch (_) { /* 不存在/损坏 → 直写 */ }
  if (old) {
    const strip = (o) => { const c = { ...o }; delete c.generated_at; return JSON.stringify(c); };
    if (strip(old) === strip(obj)) return false;
  }
  fs.writeFileSync(file, JSON.stringify({ ...obj, generated_at: new Date().toISOString() }, null, 1) + '\n', 'utf-8');
  return true;
}

// ---------- 自检（注入式·无需浏览器） ----------

function selfTest() {
  const cases = [];
  const ok = (name, cond) => cases.push([name, !!cond]);

  // T1 临界：3 处非豁免 → 不过线
  let r = judgePage({ 'div.kpi-card': 3 }, {});
  ok('T1 每页 3 处非豁免 → PASS（临界不过线）', r.nonExempt === 3 && !r.fail);

  // T2 超限：4 处 → FAIL
  r = judgePage({ 'div.kpi-card': 4 }, {});
  ok('T2 每页 4 处非豁免 → FAIL', r.nonExempt === 4 && r.fail);

  // T3 全额豁免：实测 5·豁免 5 → 0
  r = judgePage({ 'span.tag': 5 }, { 'span.tag': 5 });
  ok('T3 全额豁免后 0 处 → PASS', r.nonExempt === 0 && !r.fail);

  // T4 部分豁免：实测 9·豁免 5 → 4 → FAIL；实测 7·豁免 5 → 2 → PASS
  r = judgePage({ 'span.tag': 9 }, { 'span.tag': 5 });
  ok('T4a 部分豁免 9-5=4 → FAIL', r.nonExempt === 4 && r.fail);
  r = judgePage({ 'span.tag': 7 }, { 'span.tag': 5 });
  ok('T4b 部分豁免 7-5=2 → PASS', r.nonExempt === 2 && !r.fail);

  // T5 陈旧豁免：豁免的类已不存在 → 不扣成负、不崩
  r = judgePage({ 'div.kpi-card': 2 }, { 'span.gone': 5 });
  ok('T5 陈旧豁免不产生负计数 → PASS', r.nonExempt === 2 && !r.fail
     && r.staleExempt.length === 1);

  // T6 多类合计：两类各 2 → 合计 4 → FAIL（限额按页合计·不按类）
  r = judgePage({ 'span.tag': 2, 'div.chip': 2 }, {});
  ok('T6 多类合计 4 → FAIL', r.nonExempt === 4 && r.fail);

  // T7 增量选页：同 hash 命中缓存·变 hash/新页进扫描·消失页被剪除
  const sel = selectPagesToScan(
    ['a.html', 'b.html', 'c.html'],
    { pages: { 'a.html': { sha1: 'h1', counts: {} }, 'gone.html': { sha1: 'x', counts: {} } } },
    (rel) => ({ 'a.html': 'h1', 'b.html': 'h2', 'c.html': 'h3' }[rel]));
  ok('T7 增量选页（命中/变hash/新页/剪除）',
     sel.toScan.join(',') === 'b.html,c.html'
     && Object.keys(sel.cached).join(',') === 'a.html'
     && sel.pruned.join(',') === 'gone.html');

  // T8 类键归一化：class 属性多段 → "tag.a.b"（与登记簿形态一致）
  ok('T8 类键归一化', normalizeCls('span', 'role-tag primary') === 'span.role-tag.primary'
     && normalizeCls('div', '') === 'div');

  // T9 登记簿跨批求和 + reason 必填
  const tmp = path.join(ROOT, 'scripts/output/_w883_selftest_exemptions.json');
  fs.writeFileSync(tmp, JSON.stringify({
    criterion: 't', batches: {
      W1: { exemptions: [{ page: 'p', cls: 'c', count: 2, reason: 'r' }] },
      W2: { exemptions: [{ page: 'p', cls: 'c', count: 3, reason: 'r' }] },
    },
  }), 'utf-8');
  const m = loadExemptions(tmp);
  fs.unlinkSync(tmp);
  ok('T9 登记簿跨批求和', m.get('p|c') === 5);

  // T11 复合键族合计贪婪分配（登记簿 "A / B" 形态·W883 实证错位修复）
  r = judgePage({ 'span.tag': 1, 'span.tag.palace': 2 }, { 'span.tag / span.tag.palace': 3 });
  ok('T11a 复合键全分配（1+2=3·族合计 3）→ 0 非豁免',
     r.nonExempt === 0 && !r.fail && r.perCls['span.tag'].exempted === 1
     && r.perCls['span.tag.palace'].exempted === 2);
  r = judgePage({ 'span.tag': 2, 'span.tag.palace': 2 }, { 'span.tag / span.tag.palace': 3 });
  ok('T11b 复合键超额（实测 4·族合计 3）→ 1 非豁免', r.nonExempt === 1 && !r.fail);
  ok('T11c 豁免键批注剥离', normalizeExemptCls('span（无类名色片）') === 'span'
     && normalizeExemptCls('div.scene-bar（热力图行内）') === 'div.scene-bar'
     && normalizeExemptCls('a / b（x）') === 'a / b');

  let bad = false;
  const tmp2 = path.join(ROOT, 'scripts/output/_w883_selftest_bad.json');
  try {
    fs.writeFileSync(tmp2, JSON.stringify({
      batches: { W1: { exemptions: [{ page: 'p', cls: 'c', count: 1 }] } },
    }), 'utf-8');
    loadExemptions(tmp2);
  } catch (e) { bad = true; } finally {
    if (fs.existsSync(tmp2)) fs.unlinkSync(tmp2);  // 抛错路径也清理（自检不留垃圾）
  }
  ok('T10 豁免条目缺 reason → 抛错（防无据豁免）', bad);

  let pass = 0;
  for (const [name, p] of cases) {
    console.log(`${p ? 'PASS' : 'FAIL'} ${name}`);
    if (p) pass++;
  }
  console.log('---- 第 49 门禁 朱砂实底自检：%d/%d ----', pass, cases.length);
  return pass === cases.length ? 0 : 1;
}

// ---------- 主流程 ----------

function scopePages(siteDir) {
  const rels = [];
  const dataDir = path.join(siteDir, 'data');
  for (const fn of fs.readdirSync(dataDir).sort()) {
    if (fn.endsWith('.html')) rels.push(`data/${fn}`);
  }
  for (const fn of fs.readdirSync(siteDir).sort()) {
    if (fn.endsWith('.html') && fn !== '_template.html') rels.push(fn);
  }
  // W887 收口：en 138 页并入范围（④ en 迁移完成·豁免分册 W886/W887 已入簿）
  const enDir = path.join(siteDir, 'en');
  if (fs.existsSync(enDir)) {
    for (const fn of fs.readdirSync(enDir).sort()) {
      if (fn.endsWith('.html')) rels.push(`en/${fn}`);
    }
  }
  return rels;
}

function sha1File(abs) {
  return crypto.createHash('sha1').update(fs.readFileSync(abs)).digest('hex');
}

async function probeOne(browser, absPath) {
  const ctx = await browser.newContext({ reducedMotion: 'reduce', colorScheme: 'light' });
  try {
    const page = await ctx.newPage();
    await page.goto('file:///' + absPath.replace(/\\/g, '/'),
                    { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    const hits = await page.evaluate(measureInPage,
      { accent: ACCENT, areaMin: AREA_MIN, borderMin: BORDER_MIN_PX });
    if (!Array.isArray(hits)) throw new Error(`探针返回非数组：${typeof hits}`);
    await page.close();
    return { ok: true, hits };
  } finally {
    await ctx.close();
  }
}

async function main() {
  const argv = process.argv.slice(2);
  if (argv.includes('--self-test')) return selfTest();

  const arg = (name, dflt) => {
    const i = argv.indexOf(name);
    return i >= 0 && argv[i + 1] ? argv[i + 1] : dflt;
  };
  const siteDir = path.resolve(ROOT, arg('--site', 'site'));
  const full = argv.includes('--full');
  const noCache = argv.includes('--no-cache'); // 忽略缓存读取·仍写新缓存
  // --gate：verify_delivery 委托模式（静默进度·只报 FAIL/NOTE + 汇总行）
  const quiet = argv.includes('--quiet') || argv.includes('--gate');
  const exeFile = arg('--exemptions', DEFAULT_EXEMPTIONS);
  const cacheFile = arg('--cache', DEFAULT_CACHE);
  const reportFile = arg('--report', DEFAULT_REPORT);
  const pagesArg = arg('--pages', '');

  let exemptions;
  try {
    exemptions = loadExemptions(exeFile);
  } catch (e) {
    console.error(`豁免登记簿读取失败：${e.message}`);
    return 2;
  }

  let scope = scopePages(siteDir);
  if (pagesArg) {
    const want = new Set(pagesArg.split(',').map((s) => s.trim()).filter(Boolean));
    scope = scope.filter((r) => want.has(r));
  }
  if (!scope.length) {
    console.error('扫描范围为空（--site 或 --pages 过滤后无页）');
    return 2;
  }

  let cache = { version: CACHE_VERSION, pages: {} };
  const cacheAbs = path.isAbsolute(cacheFile) ? cacheFile : path.join(ROOT, cacheFile);
  if (!full && !noCache && fs.existsSync(cacheAbs)) {
    try {
      const old = JSON.parse(fs.readFileSync(cacheAbs, 'utf-8'));
      if (old && old.version === CACHE_VERSION && old.pages) cache = old;
    } catch (_) { /* 缓存损坏 → 全量重扫（不静默用坏缓存） */ }
  }

  const missing = scope.filter((rel) => !fs.existsSync(path.join(siteDir, rel)));
  if (missing.length) {
    console.error(`扫描范围缺页：${missing.slice(0, 5).join('、')}`);
    return 2;
  }

  const sel = selectPagesToScan(scope, (full || noCache) ? { pages: {} } : cache, (rel) => sha1File(path.join(siteDir, rel)));
  if (!quiet) {
    console.log(`范围 ${scope.length} 页 · 增量：重扫 ${sel.toScan.length} · 缓存命中 ${Object.keys(sel.cached).length}`
      + (full ? '（--full 强制全量）' : noCache ? '（--no-cache 忽略缓存）' : ''));
  }

  const measuredByPage = {};   // rel -> {cls: n}
  const probeErrors = [];
  if (sel.toScan.length) {
    let pw;
    try {
      pw = require('playwright');
    } catch (e) {
      console.error(`playwright 不可用（${e.message}）——门禁拒绝在无浏览器环境下出具通过结论`);
      return 2;
    }
    let browser;
    try {
      browser = await pw.chromium.launch({ headless: true });
      for (const rel of sel.toScan) {
        const abs = path.join(siteDir, rel);
        // hash 先于探针计算：若文件在扫描期间被改（并行会话·W883 实证 dashboard
        // 修复与扫描竞态），存旧 hash → 下轮 hash 不匹配自动重扫（缓存不自欺）。
        const sha1 = sha1File(abs);
        try {
          const { hits } = await probeOne(browser, abs);
          const byCls = {};
          for (const h of hits) {
            const key = normalizeCls(h.tag, h.cls);
            byCls[key] = (byCls[key] || 0) + 1;
          }
          measuredByPage[rel] = { byCls, sha1 };
        } catch (e) {
          probeErrors.push({ page: rel, error: String(e && e.message || e).slice(0, 200) });
          measuredByPage[rel] = { byCls: { __probe_error__: 1 }, sha1 };
        }
        if (!quiet) console.log(`  扫 ${rel}${probeErrors.some((x) => x.page === rel) ? '  ← 探针异常' : ''}`);
      }
    } finally {
      if (browser) await browser.close();
    }
  }

  // 合并缓存 + 新测量 → 每页判定
  const newCachePages = {};
  const pageResults = {};
  const fails = [];
  const notes = [];
  for (const rel of scope) {
    const entry = measuredByPage[rel];
    const counts = entry ? entry.byCls : (sel.cached[rel]?.counts || {});
    const sha1 = entry ? entry.sha1 : sha1File(path.join(siteDir, rel));
    newCachePages[rel] = { sha1, counts };
    const isProbeError = !!counts.__probe_error__;
    const exemptByCls = {};
    for (const [key, n] of exemptions) {
      const [p, cls] = [key.slice(0, key.indexOf('|')), key.slice(key.indexOf('|') + 1)];
      if (p === rel) exemptByCls[cls] = n;
    }
    const cleanCounts = { ...counts };
    delete cleanCounts.__probe_error__;
    const j = judgePage(cleanCounts, exemptByCls);
    const fail = isProbeError || j.fail;
    pageResults[rel] = {
      measured: Object.values(cleanCounts).reduce((a, b) => a + b, 0),
      exempted: Object.values(exemptByCls).reduce((a, b) => a + b, 0),
      nonExempt: j.nonExempt, fail, probeError: isProbeError || undefined,
      perCls: j.perCls,
    };
    if (fail) fails.push(rel);
    if (j.staleExempt.length) notes.push(`${rel} 陈旧豁免（类已不在）：${j.staleExempt.join('、')}`);
  }

  // 落缓存与报告
  const cacheOut = { version: CACHE_VERSION, pages: newCachePages };
  writeJsonStable(cacheAbs, cacheOut);
  const report = {
    gate: '第 49 门禁 朱砂实底', criterion: `每页非豁免朱砂实底 ≤${LIMIT} 处`
      + `（背景=--accent 盒面积>${AREA_MIN}·或 ≥${BORDER_MIN_PX} 朱砂顶条条带面积>${AREA_MIN}）`,
    scope: scope.length,
    // scanned/cached 是每次运行的易变统计（增量 vs 缓存命中）·不入报告（只进 stdout），
    // 否则 pre-commit 实跑即自造「文件内容变化」把 C4-f 打红（W883 实证）。
    exemptions_file: exeFile, pages: pageResults, fails, notes,
  };
  const reportAbs = path.isAbsolute(reportFile) ? reportFile : path.join(ROOT, reportFile);
  writeJsonStable(reportAbs, report);

  if (!quiet) {
    for (const rel of fails.slice(0, 12)) {
      const r = pageResults[rel];
      console.log(`  FAIL ${rel}：非豁免 ${r.nonExempt} 处${r.probeError ? '（探针异常·fail-closed）' : ''}`
        + `（实测 ${r.measured}·豁免 ${r.exempted}）`);
    }
    if (fails.length > 12) console.log(`  …另 ${fails.length - 12} 页 FAIL`);
    for (const n of notes.slice(0, 6)) console.log(`  NOTE ${n}`);
    if (probeErrors.length) {
      for (const pe of probeErrors.slice(0, 5)) console.log(`  PROBE-ERR ${pe.page}：${pe.error}`);
    }
  }
  console.log(`${MARKER} ${fails.length} FAIL ----`);
  return fails.length ? 1 : 0;
}

if (require.main === module) {
  main().then((code) => process.exit(code)).catch((e) => {
    console.error(`门禁执行崩溃：${e && e.stack || e}`);
    process.exit(2);
  });
}

module.exports = { normalizeCls, normalizeExemptCls, judgePage, loadExemptions, selectPagesToScan, scopePages, LIMIT };
