#!/usr/bin/env node
// trace-report.mjs — 本地问答 trace 聚合（W1339 · 方案 D D-4）
//
// 输入：<xiyouji-agent-web>/data/trace.jsonl（或 --file / AGENT_WEB_TRACE_LOG）
// 输出：人读表（默认）或 --json（机读）。
//
// 口径纪律（与 server/trace.ts 一致）：
//   - 缺样本 ≠ 0：usage_reported=false 的记录不计入 token 均值，只计入 reported 比例；
//   - 成本只在**配置了单价**时估算（AGENT_WEB_TOKEN_PRICE_INPUT_PER_1K /
//     AGENT_WEB_TOKEN_PRICE_OUTPUT_PER_1K，单位：每 1K token 的价格）——未配置则 cost=null，
//     不拿 0 冒充「免费」；
//   - 分位数用最近秩法（与 metrics.ts 同口径），样本少时 p95=最大值属正常，必须同时看 count。
//
// 用法：
//   node scripts/trace-report.mjs                 # 人读表
//   node scripts/trace-report.mjs --json          # 机读 JSON
//   node scripts/trace-report.mjs --top 10        # 会话 Top 10
//   node scripts/trace-report.mjs --since 2026-11-27
//   node scripts/trace-report.mjs --session <id>
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");

function argValue(name, fallback = "") {
  const i = process.argv.indexOf(name);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

const file = argValue("--file", process.env.AGENT_WEB_TRACE_LOG || path.join(ROOT, "data", "trace.jsonl"));
const asJson = process.argv.includes("--json");
const topN = Number(argValue("--top", "5")) || 5;
const since = argValue("--since", "");
const sessionFilter = argValue("--session", "");
const priceIn = Number(process.env.AGENT_WEB_TOKEN_PRICE_INPUT_PER_1K || "");
const priceOut = Number(process.env.AGENT_WEB_TOKEN_PRICE_OUTPUT_PER_1K || "");
const priceConfigured = Number.isFinite(priceIn) && Number.isFinite(priceOut) && (priceIn > 0 || priceOut > 0);

function quantile(sorted, q) {
  if (sorted.length === 0) return null;
  const idx = Math.min(sorted.length - 1, Math.max(0, Math.ceil(q * sorted.length) - 1));
  return sorted[idx];
}

function stats(values) {
  const s = values.filter((v) => Number.isFinite(v) && v >= 0).sort((a, b) => a - b);
  return { count: s.length, p50: quantile(s, 0.5), p95: quantile(s, 0.95), min: s[0] ?? null, max: s[s.length - 1] ?? null };
}

function readRecords() {
  let raw = "";
  try {
    raw = fs.readFileSync(file, "utf8");
  } catch {
    return { records: [], skipped: 0, missing: true };
  }
  const records = [];
  let skipped = 0;
  for (const line of raw.split("\n")) {
    const t = line.trim();
    if (!t) continue;
    try {
      const o = JSON.parse(t);
      if (!o || typeof o !== "object" || typeof o.ts !== "string" || typeof o.request_id !== "string") {
        skipped += 1;
        continue;
      }
      records.push(o);
    } catch {
      skipped += 1;
    }
  }
  return { records, skipped, missing: false };
}

const { records: all, skipped, missing } = readRecords();
const sinceMs = since ? Date.parse(since) : NaN;
const records = all.filter((r) => {
  if (sessionFilter && r.session_id !== sessionFilter) return false;
  if (Number.isFinite(sinceMs)) {
    const ts = Date.parse(r.ts);
    if (!Number.isFinite(ts) || ts < sinceMs) return false;
  }
  return true;
});

const durations = records.map((r) => r.duration_ms);
const turnDurations = records.flatMap((r) => (Array.isArray(r.turn_trace) ? r.turn_trace.map((t) => t.durationMs) : []));

const byModel = new Map();
const bySession = new Map();
const toolAgg = new Map();
let reported = 0;
let inTokens = 0;
let outTokens = 0;
let totalTokens = 0;
let errors = 0;

for (const r of records) {
  if (r.level === "error") errors += 1;
  const m = byModel.get(r.model || "(未知)") || { model: r.model || "(未知)", requests: 0, errors: 0, reported: 0, input: 0, output: 0, total: 0, durations: [] };
  m.requests += 1;
  if (r.level === "error") m.errors += 1;
  m.durations.push(r.duration_ms);
  if (r.usage_reported) {
    reported += 1;
    m.reported += 1;
    const i = Number(r.input_tokens) || 0;
    const o = Number(r.output_tokens) || 0;
    const t = Number(r.total_tokens) || i + o;
    m.input += i;
    m.output += o;
    m.total += t;
    inTokens += i;
    outTokens += o;
    totalTokens += t;
  }
  byModel.set(m.model, m);

  const sid = r.session_id || "(无会话)";
  const s = bySession.get(sid) || { session_id: sid, requests: 0, errors: 0, turns: 0, durations: [] };
  s.requests += 1;
  if (r.level === "error") s.errors += 1;
  s.turns += Number(r.turns) || 0;
  s.durations.push(r.duration_ms);
  bySession.set(sid, s);

  for (const t of Array.isArray(r.tool_calls) ? r.tool_calls : []) {
    const name = t?.name || "(未知)";
    const a = toolAgg.get(name) || { name, calls: 0, errors: 0 };
    a.calls += 1;
    if (t.status === "error") a.errors += 1;
    toolAgg.set(name, a);
  }
}

const cost = priceConfigured
  ? {
      input: (inTokens / 1000) * priceIn,
      output: (outTokens / 1000) * priceOut,
      total: (inTokens / 1000) * priceIn + (outTokens / 1000) * priceOut,
      currency_note: "按 AGENT_WEB_TOKEN_PRICE_*_PER_1K 配置估算（币种由配置口径决定）",
    }
  : null;

const report = {
  file,
  missing,
  skipped,
  filter: { since: since || null, session: sessionFilter || null },
  totals: {
    requests: records.length,
    errors,
    usage_reported: reported,
    usage_reported_ratio: records.length ? Number((reported / records.length).toFixed(4)) : null,
    input_tokens: reported ? inTokens : null,
    output_tokens: reported ? outTokens : null,
    total_tokens: reported ? totalTokens : null,
    duration_ms: stats(durations),
    turn_duration_ms: stats(turnDurations),
  },
  cost,
  by_model: [...byModel.values()]
    .map((m) => ({
      model: m.model,
      requests: m.requests,
      errors: m.errors,
      usage_reported_ratio: m.requests ? Number((m.reported / m.requests).toFixed(4)) : null,
      input_tokens: m.reported ? m.input : null,
      output_tokens: m.reported ? m.output : null,
      total_tokens: m.reported ? m.total : null,
      duration_ms: stats(m.durations),
    }))
    .sort((a, b) => b.requests - a.requests),
  by_session: [...bySession.values()]
    .map((s) => ({
      session_id: s.session_id,
      requests: s.requests,
      errors: s.errors,
      avg_turns: s.requests ? Number((s.turns / s.requests).toFixed(2)) : null,
      duration_ms: stats(s.durations),
    }))
    .sort((a, b) => (b.duration_ms.p95 || 0) - (a.duration_ms.p95 || 0))
    .slice(0, topN),
  tools: [...toolAgg.values()].sort((a, b) => b.calls - a.calls),
};

if (asJson) {
  console.log(JSON.stringify(report, null, 2));
  process.exit(0);
}

if (missing) {
  console.log(`无 trace 数据：${file} 不存在（问答发生后由 server/trace.ts 自动创建）`);
  process.exit(0);
}

console.log(`trace 报告  file=${file}`);
console.log(`筛选        since=${report.filter.since || "-"}  session=${report.filter.session || "-"}`);
console.log(`总量        requests=${records.length}  errors=${errors}  usage_reported=${reported}/${records.length}  skipped=${skipped}`);
console.log(
  `耗时(ms)     p50=${report.totals.duration_ms.p50 ?? "-"}  p95=${report.totals.duration_ms.p95 ?? "-"}  min=${report.totals.duration_ms.min ?? "-"}  max=${report.totals.duration_ms.max ?? "-"}`
);
console.log(
  `token        input=${report.totals.input_tokens ?? "未测到"}  output=${report.totals.output_tokens ?? "未测到"}  total=${report.totals.total_tokens ?? "未测到"}`
);
console.log(
  cost ? `成本估算     input=${cost.input.toFixed(4)}  output=${cost.output.toFixed(4)}  total=${cost.total.toFixed(4)}` : "成本估算     未配置单价（AGENT_WEB_TOKEN_PRICE_INPUT_PER_1K / _OUTPUT_PER_1K）⇒ 不估算"
);
console.log("");
console.log("按模型：");
for (const m of report.by_model) {
  console.log(
    `  ${m.model}  requests=${m.requests}  errors=${m.errors}  reported=${m.usage_reported_ratio ?? "-"}  tokens=${m.total_tokens ?? "未测到"}  p95=${m.duration_ms.p95 ?? "-"}ms`
  );
}
console.log("");
console.log(`会话 Top ${topN}（按 p95 耗时）：`);
for (const s of report.by_session) {
  console.log(`  ${s.session_id}  requests=${s.requests}  errors=${s.errors}  avg_turns=${s.avg_turns ?? "-"}  p95=${s.duration_ms.p95 ?? "-"}ms`);
}
console.log("");
console.log("工具调用：");
for (const t of report.tools) {
  console.log(`  ${t.name}  calls=${t.calls}  errors=${t.errors}`);
}
if (report.tools.length === 0) console.log("  （无）");
