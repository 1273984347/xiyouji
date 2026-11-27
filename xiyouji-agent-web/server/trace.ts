// trace.ts — 本地零依赖问答 trace（W1339 · 方案 D D-1/D-2/D-3 载体）
//
// 决策来源：docs/11-方案报告/设计与架构方案/可观测性接入选型与决策-2026-11-27.md（方案 D）。
// 本模块与 audit.ts **同构但分表**，理由（该文档 §8 未验证项 1 的拍板）：
//   - **分表**：audit 是合规留证（L4·写入失败要标记合规降级），trace 是高频观测数据；
//     合表会让高频 trace 稀释审计面，也会把「trace 写失败」误升级成合规事件。
//   - **同构**：只追加 JSONL + 按留存期销毁 + 读侧坏行容忍 + 写入失败可见（不静默）。
//
// 三条纪律：
//  1) **写入绝不带崩问答**（fail-open）：appendTrace 内部吞错，但把失败计数与最后错误
//     暴露给 /api/trace 与日志——「不阻断」不等于「不可见」；
//  2) **只存元数据，不存正文**：记录轮次/耗时/token/工具名/错误名，**不落** prompt 与回答文本
//     （避免把 L3 会话内容复制到第二处存储面）；
//  3) **缺样本 ≠ 0**：上游未回传 usage 时 input/output/total 记 null 且 usage_reported=false
//     （与 metrics.ts / chat.ts 的 OBS-14 口径一致）。
import fs from "fs";
import path from "path";
import { randomUUID } from "crypto";
import { fileURLToPath } from "url";
import { resolveRetention } from "./compliance/retention.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const TRACE_READ_MAX_BYTES = 8 * 1024 * 1024;
const TRACE_LIMIT_MAX = 1000;
const TRACE_ERROR_MAX = 300;
const TRACE_MODEL_MAX = 120;
const TRACE_ID_MAX = 200;

/** trace 记录结构版本（字段只增不改）。 */
export const TRACE_SCHEMA_VERSION = 1;

/** token 用量（与引擎 TokenUsage 同形）。 */
export interface TraceUsage {
  inputTokens: number;
  outputTokens: number;
  totalTokens: number;
}

/** 单轮 trace（D-2：轮次、耗时、工具名、该轮 usage）。 */
export interface TraceTurn {
  /** 轮次序号（从 1 起）。 */
  turn: number;
  /** 该轮墙钟耗时（毫秒）。 */
  durationMs: number;
  /** 该轮文本增量字符数（不含 prompt/回答正文）。 */
  textChars: number;
  /** 该轮请求的工具名（按模型输出顺序）。 */
  toolCalls: string[];
  /** 该轮 usage；上游未回传 = null（缺样本，非 0）。 */
  usage: TraceUsage | null;
}

/** 错误摘要（只留名字与截断后的消息，不含 stack/路径）。 */
export interface TraceError {
  name: string;
  message: string;
}

/** 一次问答的 trace 记录（JSONL 每行一条）。 */
export interface TraceRecord {
  schema_version: number;
  /** ISO 时间戳。 */
  ts: string;
  /** 事件唯一标识。 */
  event_id: string;
  session_id: string;
  request_id: string;
  model: string;
  level: "info" | "error";
  turns: number;
  duration_ms: number;
  usage_reported: boolean;
  input_tokens: number | null;
  output_tokens: number | null;
  total_tokens: number | null;
  /** 工具执行结果摘要（name + status；不含入参与输出）。 */
  tool_calls: Array<{ name: string; status: "completed" | "error" }>;
  /** 逐轮明细。 */
  turn_trace: TraceTurn[];
  error: TraceError | null;
}

export interface TraceReadResult {
  entries: TraceRecord[];
  total: number;
  skipped: number;
}

/** 写入失败状态（观测面自身的可用性，不阻断问答）。 */
export interface TraceDegradationState {
  degraded: boolean;
  failures: number;
  lastError: string | null;
  lastErrorAt: string | null;
}

const degradation: TraceDegradationState = {
  degraded: false,
  failures: 0,
  lastError: null,
  lastErrorAt: null,
};

/**
 * trace 文件路径：默认 <xiyouji-agent-web>/data/trace.jsonl；
 * AGENT_WEB_TRACE_LOG 可覆盖（测试隔离 / 多实例分文件）。
 */
export function traceLogPath(): string {
  const custom = (process.env.AGENT_WEB_TRACE_LOG || "").trim();
  return custom || path.resolve(HERE, "..", "data", "trace.jsonl");
}

/** 当前写入失败状态（只读快照）。 */
export function traceDegradation(): TraceDegradationState {
  return { ...degradation };
}

/** 测试用：清空降级状态。 */
export function resetTraceDegradationForTest(): void {
  degradation.degraded = false;
  degradation.failures = 0;
  degradation.lastError = null;
  degradation.lastErrorAt = null;
}

/** 截断 + 脱敏（错误消息里可能带 sk- 凭证形态；只留名字与短消息）。 */
function sanitizeError(err: unknown): TraceError {
  const name = err instanceof Error && err.name ? err.name : "Error";
  const raw = err instanceof Error ? err.message : String(err);
  return sanitizeErrorText(name, raw);
}

/** 按「名字 + 消息」截断脱敏（append 入口与内部共用）。 */
function sanitizeErrorText(name: string, message: string): TraceError {
  const clippedMsg = message.length > TRACE_ERROR_MAX ? message.slice(0, TRACE_ERROR_MAX) + "…" : message;
  return { name, message: clippedMsg.replace(/sk-[A-Za-z0-9_-]{8,}/g, "sk-***") };
}

function clipped(value: string, max: number): string {
  return value.length > max ? value.slice(0, max) : value;
}

/** 追加一行（只追加；失败不抛——由调用方通过 degradation 观测）。 */
export function appendTrace(
  record: Omit<TraceRecord, "schema_version" | "ts" | "event_id"> & Partial<Pick<TraceRecord, "ts" | "event_id">>
): void {
  try {
    const full: TraceRecord = {
      schema_version: TRACE_SCHEMA_VERSION,
      ts: record.ts || new Date().toISOString(),
      event_id: record.event_id || randomUUID(),
      session_id: clipped(String(record.session_id || ""), TRACE_ID_MAX),
      request_id: clipped(String(record.request_id || ""), TRACE_ID_MAX),
      model: clipped(String(record.model || ""), TRACE_MODEL_MAX),
      level: record.level === "error" ? "error" : "info",
      turns: record.turns,
      duration_ms: record.duration_ms,
      usage_reported: record.usage_reported,
      input_tokens: record.input_tokens,
      output_tokens: record.output_tokens,
      total_tokens: record.total_tokens,
      tool_calls: record.tool_calls,
      turn_trace: record.turn_trace,
      error: record.error ? sanitizeErrorText(String(record.error.name || "Error"), String(record.error.message || "")) : null,
    };
    const file = traceLogPath();
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.appendFileSync(file, JSON.stringify(full) + "\n", "utf8");
    degradation.degraded = false;
  } catch (err) {
    degradation.degraded = true;
    degradation.failures += 1;
    degradation.lastError = err instanceof Error ? err.message : String(err);
    degradation.lastErrorAt = new Date().toISOString();
    // 观测数据写失败只告警，不影响问答主链路（fail-open·但可见）。
    console.warn("[trace] 写入失败（观测数据·不阻断问答）：" + degradation.lastError);
  }
}

/**
 * 读取最近 limit 条（旧→新）。
 * - 坏行容忍并计数；文件不存在=空；任何异常=空（绝不抛）。
 * - sessionId 过滤在读取后应用（仍按全量 total 计数，便于核对）。
 */
export function readTrace(limit = 100, filter?: { sessionId?: string }): TraceReadResult {
  const cap = Number.isFinite(limit) && limit > 0 ? Math.min(Math.floor(limit), TRACE_LIMIT_MAX) : 100;
  const file = traceLogPath();
  let raw = "";
  try {
    const st = fs.statSync(file);
    const start = Math.max(0, st.size - TRACE_READ_MAX_BYTES);
    const len = st.size - start;
    const buf = Buffer.alloc(len);
    const fh = fs.openSync(file, "r");
    try {
      if (len > 0) fs.readSync(fh, buf, 0, len, start);
    } finally {
      fs.closeSync(fh);
    }
    raw = buf.toString("utf8");
    if (start > 0) {
      const nl = raw.indexOf("\n");
      raw = nl === -1 ? "" : raw.slice(nl + 1);
    }
  } catch {
    return { entries: [], total: 0, skipped: 0 };
  }

  const entries: TraceRecord[] = [];
  let skipped = 0;
  for (const line of raw.split("\n")) {
    const t = line.trim();
    if (!t) continue;
    try {
      const o = JSON.parse(t) as TraceRecord;
      if (!o || typeof o !== "object" || typeof o.ts !== "string" || typeof o.request_id !== "string") {
        skipped += 1;
        continue;
      }
      entries.push(o);
    } catch {
      skipped += 1;
    }
  }
  const filtered = filter?.sessionId ? entries.filter((e) => e.session_id === filter.sessionId) : entries;
  return { entries: filtered.slice(-cap), total: entries.length, skipped };
}

export interface TracePurgeResult {
  /** 截止时刻（早于它的被销毁）。 */
  cutoff: string;
  removed: number;
  kept: number;
  logPath: string;
}

/**
 * 按留存期销毁（复用 audit 的 180 天硬下限策略）。
 *
 * 为什么不新增 retention 类别：方案 D 只要求「复用 retention.ts 的留存与销毁」；
 * 新增类别会把留存期开关扩散到观测面，而 trace 的元数据敏感度不高于审计事件。
 */
export function purgeExpiredTrace(nowMs: number = Date.now()): TracePurgeResult {
  const policy = resolveRetention().audit;
  const cutoffMs = nowMs - (policy.retentionDays ?? 180) * 86400000;
  const cutoff = new Date(cutoffMs).toISOString();
  const file = traceLogPath();
  let raw = "";
  try {
    raw = fs.readFileSync(file, "utf8");
  } catch {
    return { cutoff, removed: 0, kept: 0, logPath: file };
  }
  const keptLines: string[] = [];
  let removed = 0;
  for (const line of raw.split("\n")) {
    const t = line.trim();
    if (!t) continue;
    try {
      const o = JSON.parse(t) as TraceRecord;
      const ts = typeof o.ts === "string" ? Date.parse(o.ts) : NaN;
      if (Number.isFinite(ts) && ts < cutoffMs) {
        removed += 1;
        continue;
      }
      keptLines.push(t);
    } catch {
      // 坏行按留存期无法判定 ⇒ 保留（读侧会计 skipped，不因销毁误删）
      keptLines.push(t);
    }
  }
  if (removed > 0) {
    const tmp = file + ".tmp";
    fs.writeFileSync(tmp, keptLines.length ? keptLines.join("\n") + "\n" : "", "utf8");
    fs.renameSync(tmp, file);
  }
  return { cutoff, removed, kept: keptLines.length, logPath: file };
}
