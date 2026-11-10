/**
 * audit-archive.ts — 审计归档（PG audit_archive · W1205 · D-3 合规批）
 *
 * 方案 §12.2 缺口 3 的整改：「审计流水 + PG 归档 + 只追加 + ≥ 180 天留存」。
 *
 * **表结构复用既有基线**：deploy/pg/migrations/0001_baseline.sql 已建 audit_archive
 * （id UUID / ts / actor / action / target / decision / result / data_class CHECK /
 * trace_id / source_ip / payload JSONB）⇒ 本模块**不另起一套**（已在本机 PG 16.4
 * 实测确认该表存在且列一致）。
 *
 * 两条纪律：
 *  1) **只追加**：INSERT ... ON CONFLICT (id) DO NOTHING（幂等重放，不覆盖旧事件）；
 *     禁止 UPDATE。删除只允许按留存期批量销毁（见 purgeAuditArchiveBefore），
 *     且销毁动作本身写一条新事件（销毁留证）。
 *  2) **不吞错**：归档失败抛 COMPLIANCE_AUDIT_ARCHIVE_FAILED（调用方决定是否降级）。
 */
import { Pool } from "pg";
import { ComplianceError, ComplianceErrorCode } from "./errors.js";
import { resolvePostgresConfig, type PostgresConfig } from "../storage/postgres.js";
import { newEventId, type AuditEvent } from "./audit-event.js";

/** 归档选项（可注入池子·便于测试隔离）。 */
export interface AuditArchiveOptions {
  /** 已建好的连接池（不给则按环境变量自建）。 */
  pool?: Pool;
  /** PG 配置（不给则按环境变量解析）。 */
  config?: PostgresConfig;
}

/** 自建连接池（调用方负责 close）。 */
async function withPool<T>(
  opts: AuditArchiveOptions,
  fn: (pool: Pool) => Promise<T>
): Promise<T> {
  if (opts.pool) return fn(opts.pool);
  const cfg = opts.config ?? resolvePostgresConfig();
  const pool = new Pool({
    host: cfg.host,
    port: cfg.port,
    user: cfg.user,
    password: cfg.password,
    database: cfg.database,
    max: 1,
    ssl: cfg.ssl ? { rejectUnauthorized: false } : undefined,
    options: cfg.schema ? "-c search_path=" + cfg.schema : undefined,
    connectionTimeoutMillis: 10_000,
  });
  try {
    return await fn(pool);
  } finally {
    await pool.end().catch(() => undefined);
  }
}

/**
 * 把审计事件归档进 PG（只追加 · 幂等）。
 *
 * @returns 实际写入行数（已存在的 event_id 计入 0——幂等重放不重复写）
 */
export async function archiveAuditEvents(
  events: AuditEvent[],
  opts: AuditArchiveOptions = {}
): Promise<number> {
  if (!events || events.length === 0) return 0;
  return withPool(opts, async (pool) => {
    let written = 0;
    for (const e of events) {
      try {
        const res = await pool.query(
          "INSERT INTO audit_archive (id, ts, actor, action, target, decision, result, data_class, trace_id, source_ip, payload) " +
            "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) " +
            "ON CONFLICT (id) DO NOTHING",
          [
            e.event_id,
            e.ts,
            e.actor,
            e.action,
            e.target,
            e.decision,
            e.result,
            e.data_class,
            e.trace_id || null,
            e.source_ip || null,
            JSON.stringify(e),
          ]
        );
        written += res.rowCount ?? 0;
      } catch (err) {
        throw new ComplianceError(
          ComplianceErrorCode.AUDIT_ARCHIVE_FAILED,
          "审计归档写入失败：" + (err instanceof Error ? err.message : String(err)),
        );
      }
    }
    return written;
  });
}

/** 到期销毁结果。 */
export interface AuditArchivePurgeResult {
  /** 删除行数。 */
  deleted: number;
  /** 销毁留证事件（已写入归档表）。 */
  evidence: AuditEvent;
}

/**
 * 按留存期批量销毁归档（**销毁留证**：销毁动作本身写一条新事件）。
 *
 * 顺序：先删过期行，再写销毁事件 ⇒ 销毁事件本身不在被删区间内（ts = 现在）。
 */
export async function purgeAuditArchiveBefore(
  cutoff: Date,
  opts: AuditArchiveOptions = {},
  actor = "system:retention",
): Promise<AuditArchivePurgeResult> {
  return withPool(opts, async (pool) => {
    const res = await pool.query("DELETE FROM audit_archive WHERE ts < $1", [cutoff]);
    const deleted = res.rowCount ?? 0;
    const evidence: AuditEvent = {
      schema_version: 1,
      ts: new Date().toISOString(),
      event_id: newEventId(),
      actor,
      action: "destroy",
      target: "audit_archive",
      decision: "allow",
      result: "ok",
      data_class: "L4",
      trace_id: "",
      source_ip: "",
      reason: "留存期到期销毁：移除 " + deleted + " 条，截止 " + cutoff.toISOString(),
    };
    await pool.query(
      "INSERT INTO audit_archive (id, ts, actor, action, target, decision, result, data_class, trace_id, source_ip, payload) " +
        "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) ON CONFLICT (id) DO NOTHING",
      [
        evidence.event_id,
        evidence.ts,
        evidence.actor,
        evidence.action,
        evidence.target,
        evidence.decision,
        evidence.result,
        evidence.data_class,
        evidence.trace_id || null,
        evidence.source_ip || null,
        JSON.stringify(evidence),
      ]
    );
    return { deleted, evidence };
  });
}
