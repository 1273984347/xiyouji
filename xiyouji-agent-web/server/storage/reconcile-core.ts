/**
 * reconcile-core.ts — 集合级三重对账的**与数据源无关**核心（W1204 · 架构方案 v2 §8.2 档 2 · D-2 第二子批）
 *
 * 为什么核心与读法分离：双写期要对账的两侧可能是（SQLite, SQLite）或（SQLite, PostgreSQL）——
 * 读法不同，但「怎么算一致」必须**只有一份实现**，否则两套判定会各自漂移
 * （这正是 D-08「对账要比集合，不能只比计数」要防的：行数相等但内容错位是假对账）。
 *
 * 三重对账（与 W934 迁移器的 reconcile() 同语义）：
 *  ① 行数相等
 *  ② **主键集合**逐位相等（不是只比数量）
 *  ③ 逐行内容摘要相等（时间列先规范化再比 ⇒ 比的是「同一时刻」而非「同一串」）
 * 另附：时间列逐字节相等抽样数（抓「同一时刻但不同串」的漂移）。
 */
import { createHash } from "node:crypto";

export interface TableSpec {
  name: string;
  pk: string;
  timeCols: string[];
  cols: string[];
}

export interface ReconcileResult {
  table: string;
  source_rows: number;
  target_rows: number;
  rows_equal: boolean;
  pk_sets_equal: boolean;
  content_equal: boolean;
  pk_only_in_source: string[];
  pk_only_in_target: string[];
  content_mismatch_sample: Array<{ pk: string; source: string; target: string }>;
  timestamp_raw_equal_sampled: number;
  timestamp_raw_equal_total: number;
}

/** 任意可解析的时间值 → 规范 ISO 字符串（无法解析时按原串参与比对）。 */
export function normIso(v: unknown): string {
  if (v instanceof Date) return v.toISOString();
  if (typeof v === "number") return new Date(v).toISOString();
  const d = new Date(String(v));
  return Number.isNaN(d.getTime()) ? String(v) : d.toISOString();
}

/** 行 → 规范摘要串（时间列走 normIso；其余列按字符串原值；列序固定 ⇒ 摘要可比）。 */
export function canon(row: Record<string, unknown>, spec: TableSpec): string {
  const parts: string[] = [];
  for (const c of spec.cols) {
    const raw = row[c];
    parts.push(spec.timeCols.includes(c) ? normIso(raw) : String(raw ?? ""));
  }
  return sha256(parts.join("\u0001"));
}

export function sha256(text: string): string {
  return createHash("sha256").update(text, "utf-8").digest("hex");
}

/**
 * 三重对账：行数 + 主键集合 + 逐行内容摘要。
 * sourceRows / targetRows 是两侧**同一张表**的全量行。
 */
export function reconcileTable(
  spec: TableSpec,
  sourceRows: Array<Record<string, unknown>>,
  targetRows: Array<Record<string, unknown>>,
): ReconcileResult {
  const srcMap = new Map<string, Record<string, unknown>>();
  for (const r of sourceRows) srcMap.set(String(r[spec.pk]), r);
  const tgtMap = new Map<string, Record<string, unknown>>();
  for (const r of targetRows) tgtMap.set(String(r[spec.pk]), r);

  const srcPks = [...srcMap.keys()].sort();
  const tgtPks = [...tgtMap.keys()].sort();
  const pkOnlyInSource = srcPks.filter((k) => !tgtMap.has(k));
  const pkOnlyInTarget = tgtPks.filter((k) => !srcMap.has(k));
  const pkSetsEqual =
    pkOnlyInSource.length === 0 && pkOnlyInTarget.length === 0 && srcPks.length === tgtPks.length;

  const contentMismatches: Array<{ pk: string; source: string; target: string }> = [];
  let tsRawEqual = 0;
  let tsRawTotal = 0;
  for (const pk of srcPks) {
    const s = srcMap.get(pk)!;
    const g = tgtMap.get(pk);
    if (!g) continue;
    const sc = canon(s, spec);
    const gc = canon(g, spec);
    if (sc !== gc && contentMismatches.length < 10) {
      contentMismatches.push({ pk, source: sc, target: gc });
    }
    for (const tc of spec.timeCols) {
      tsRawTotal++;
      if (String(s[tc]) === normIso(g[tc])) tsRawEqual++;
    }
  }

  return {
    table: spec.name,
    source_rows: sourceRows.length,
    target_rows: targetRows.length,
    rows_equal: sourceRows.length === targetRows.length,
    pk_sets_equal: pkSetsEqual,
    content_equal: contentMismatches.length === 0,
    pk_only_in_source: pkOnlyInSource.slice(0, 20),
    pk_only_in_target: pkOnlyInTarget.slice(0, 20),
    content_mismatch_sample: contentMismatches,
    timestamp_raw_equal_sampled: tsRawEqual,
    timestamp_raw_equal_total: tsRawTotal,
  };
}

/** 三张业务表的规格（与现役 SQLite 同构；PG 侧由 0002_app_tables.sql 建同构表）。 */
export const BUSINESS_TABLES: TableSpec[] = [
  {
    name: "sessions",
    pk: "id",
    timeCols: ["created_at", "updated_at"],
    cols: ["id", "title", "model", "sdk_session_id", "created_at", "updated_at"],
  },
  {
    name: "messages",
    pk: "id",
    timeCols: ["created_at"],
    cols: ["id", "session_id", "role", "content", "model", "tool_calls", "created_at"],
  },
  {
    name: "feedback",
    pk: "id",
    timeCols: ["created_at"],
    cols: ["id", "session_id", "message_id", "verdict", "comment", "created_at"],
  },
];

/**
 * 全表对账入口：三张表逐张三重对账（**两侧读都是异步的** ⇒ 本函数是 async）。
 *
 * 为什么必须是 async：PG 走网络协议·**没有同步形态**⇒「把异步读塞进同步编排」
 * 是这类对账器最容易写出的假实现（原实现正是如此：把 Promise 强转成数组——
 * 类型层会报 TS2352，运行期拿到的会是 Promise 对象而不是行数组）。
 *
 * 逐表**串行**（不 Promise.all）：同一张表的两侧要一起比对，且串行省连接/不抢 SQLite 写锁。
 */
export async function reconcileAll(
  specs: TableSpec[],
  readSource: (spec: TableSpec) => Promise<Array<Record<string, unknown>>>,
  readTarget: (spec: TableSpec) => Promise<Array<Record<string, unknown>>>,
): Promise<ReconcileResult[]> {
  const out: ReconcileResult[] = [];
  for (const spec of specs) {
    out.push(reconcileTable(spec, await readSource(spec), await readTarget(spec)));
  }
  return out;
}
