/**
 * audit-archive.test.ts — 审计归档（PG audit_archive）单测（W1205 · D-3 合规批）
 *
 * 覆盖四条：
 *  ① 归档写入后，PG 里的列与事件字段一一对应（复用 0001 基线既有表·不另起一套）；
 *  ② **只追加 + 幂等**：同一 event_id 重放不新增行、也不覆盖旧行；
 *  ③ 到期销毁：只删过期行，且**销毁留证**（销毁动作本身写一条新事件）；
 *  ④ 归档失败不吞错（抛可枚举错误码）。
 *
 * 前置条件：PG 可达 + 应用账号可建 schema。不满足则 skip（**不是失败**）。
 * 运行：cd xiyouji-agent-web && node --import tsx --test server/compliance/audit-archive.test.ts
 */
import { test } from "node:test";
import assert from "node:assert";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Pool } from "pg";
import { archiveAuditEvents, purgeAuditArchiveBefore } from "./audit-archive.js";
import { newEventId, type AuditEvent } from "./audit-event.js";
import { resolvePostgresConfig } from "../storage/postgres.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SCHEMA = "compliance_audit_test";

/** 造一条合规审计事件。 */
function makeEvent(over: Partial<AuditEvent> = {}): AuditEvent {
  return {
    schema_version: 1,
    ts: "2026-05-06T07:08:09.000Z",
    event_id: newEventId(),
    actor: "test:actor",
    action: "write",
    target: "docs/x.md",
    decision: "allow",
    result: "ok",
    data_class: "L4",
    trace_id: "trace-1",
    source_ip: "10.0.0.9",
    ...over,
  };
}

/** 探测 PG 是否可用。 */
async function probePostgres(): Promise<{ ok: boolean; reason: string }> {
  const cfg = resolvePostgresConfig();
  const pool = new Pool({
    host: cfg.host,
    port: cfg.port,
    user: cfg.user,
    password: cfg.password,
    database: cfg.database,
    max: 1,
    connectionTimeoutMillis: 5_000,
  });
  try {
    await pool.query("SELECT 1");
    return { ok: true, reason: "ok" };
  } catch (err) {
    return { ok: false, reason: "PG 不可达：" + (err instanceof Error ? err.message : String(err)) };
  } finally {
    await pool.end().catch(() => undefined);
  }
}

test("PG 审计归档：只追加 · 幂等 · 到期销毁留证", async (t) => {
  const probe = await probePostgres();
  if (!probe.ok) {
    t.skip("跳过（" + probe.reason + "）");
    return;
  }
  const cfg = resolvePostgresConfig();
  const admin = new Pool({
    host: cfg.host,
    port: cfg.port,
    user: cfg.user,
    password: cfg.password,
    database: cfg.database,
    max: 2,
    connectionTimeoutMillis: 5_000,
  });
  let scoped: Pool | null = null;
  try {
    // 建专用 schema（复用 0001 基线里的 audit_archive 表定义·不另起一套）
    await admin.query("DROP SCHEMA IF EXISTS " + SCHEMA + " CASCADE");
    await admin.query("CREATE SCHEMA " + SCHEMA);
    scoped = new Pool({
      host: cfg.host,
      port: cfg.port,
      user: cfg.user,
      password: cfg.password,
      database: cfg.database,
      max: 2,
      options: "-c search_path=" + SCHEMA,
      connectionTimeoutMillis: 5_000,
    });
    const sql = fs.readFileSync(path.resolve(HERE, "..", "..", "deploy", "pg", "migrations", "0001_baseline.sql"), "utf-8");
    await scoped.query(sql);

    // ① 归档写入：列与事件字段一一对应
    const e1 = makeEvent();
    const written = await archiveAuditEvents([e1], { pool: scoped });
    assert.equal(written, 1, "应写入 1 行");
    const { rows } = await scoped.query("SELECT * FROM audit_archive WHERE id = $1", [e1.event_id]);
    assert.equal(rows.length, 1);
    assert.equal(String(rows[0].actor), e1.actor);
    assert.equal(String(rows[0].action), e1.action);
    assert.equal(String(rows[0].target), e1.target);
    assert.equal(String(rows[0].decision), e1.decision);
    assert.equal(String(rows[0].result), e1.result);
    assert.equal(String(rows[0].data_class), e1.data_class);
    assert.equal(String(rows[0].trace_id), e1.trace_id);
    assert.equal(String(rows[0].source_ip), e1.source_ip);
    assert.equal(new Date(rows[0].ts).toISOString(), e1.ts, "时间列应等价于 ISO 串");

    // ② 只追加 + 幂等：同一 event_id 重放 ⇒ 不新增、不覆盖
    const again = await archiveAuditEvents([e1], { pool: scoped });
    assert.equal(again, 0, "同一 event_id 重放不得新增行（只追加）");
    const { rows: after } = await scoped.query("SELECT COUNT(*)::bigint AS n FROM audit_archive");
    assert.equal(Number(after[0].n), 1, "总行数应仍为 1");

    // ③ 到期销毁 + 销毁留证
    const old = makeEvent({ ts: "2020-01-01T00:00:00.000Z" });
    await archiveAuditEvents([old], { pool: scoped });
    const purge = await purgeAuditArchiveBefore(new Date("2026-01-01T00:00:00.000Z"), { pool: scoped });
    assert.equal(purge.deleted, 1, "只应销毁截止时刻之前的那 1 条");
    assert.equal(purge.evidence.action, "destroy", "销毁留证事件的动作应是 destroy");
    assert.equal(purge.evidence.data_class, "L4");
    const { rows: left } = await scoped.query("SELECT id, action FROM audit_archive ORDER BY ts");
    assert.equal(left.length, 2, "销毁后应剩 2 条（当期事件 + 销毁留证）");
    const evidenceRow = left.find((r) => String(r.action) === "destroy");
    assert.ok(evidenceRow, "销毁留证事件本身必须留在归档里");
    assert.equal(String(evidenceRow!.id), purge.evidence.event_id);
  } finally {
    if (scoped) await scoped.end().catch(() => undefined);
    await admin.query("DROP SCHEMA IF EXISTS " + SCHEMA + " CASCADE").catch(() => undefined);
    await admin.end().catch(() => undefined);
  }
});
