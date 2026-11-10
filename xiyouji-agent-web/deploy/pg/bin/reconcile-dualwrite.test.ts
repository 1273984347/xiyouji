/**
 * reconcile-dualwrite.test.ts — 对账器契约测试（W1204 · v2 §8.2 档 2 · D-2 第二子批）
 *
 * 三条关键语义（两个临时 SQLite 实例互为两侧⇒无外部依赖全跑）：
 *  1. 一致时三重对账全等（行数 + 主键集合 + 逐行内容摘要）
 *  2. **假对账被抓住**：行数相等但内容错位（删一行补一行）⇒ 判不等
 *     —— D-08「对账要比集合，不能只比计数」的核心场景
 *  3. 时间列规范化：同一时刻不同串（带时区 vs UTC）⇒ 内容判等
 */
import assert from "node:assert/strict";
import { test } from "node:test";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import Database from "better-sqlite3";

import { BUSINESS_TABLES, canon, normIso, reconcileAll, reconcileTable } from "../../../server/storage/reconcile-core.js";

function tempDb(tag: string): string {
  return path.join(fs.mkdtempSync(path.join(os.tmpdir(), "reconcile-")), tag + ".db");
}

const S = { id: "s1", title: "标题", model: "m", sdk_session_id: null, created_at: "2026-11-10T08:00:00.000Z", updated_at: "2026-11-10T08:00:00.000Z" };

function seed(dbPath: string, sessions: Array<Record<string, unknown>>) {
  const db = new Database(dbPath);
  db.exec("CREATE TABLE sessions (id TEXT PRIMARY KEY, title TEXT, model TEXT, sdk_session_id TEXT, created_at TEXT, updated_at TEXT)");
  const ins = db.prepare("INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?)");
  for (const s of sessions) {
    ins.run(String(s.id), String(s.title), String(s.model), s.sdk_session_id, String(s.created_at), String(s.updated_at));
  }
  db.close();
}

function readSessions(dbPath: string): Array<Record<string, unknown>> {
  const db = new Database(dbPath, { readonly: true });
  try {
    return db.prepare("SELECT id, title, model, sdk_session_id, created_at, updated_at FROM sessions").all() as Array<Record<string, unknown>>;
  } finally {
    db.close();
  }
}

test("一致时三重对账全等", () => {
  const a = tempDb("a");
  const b = tempDb("b");
  seed(a, [S]);
  seed(b, [S]);
  const r = reconcileTable(BUSINESS_TABLES[0], readSessions(a), readSessions(b));
  assert.equal(r.rows_equal, true);
  assert.equal(r.pk_sets_equal, true);
  assert.equal(r.content_equal, true);
  assert.equal(r.timestamp_raw_equal_total, 2);
});

test("假对账被抓住：行数相等但主键错位 ⇒ 判不等", () => {
  const a = tempDb("a");
  const b = tempDb("b");
  seed(a, [S]);
  seed(b, [{ ...S, id: "s2" }]);
  const r = reconcileTable(BUSINESS_TABLES[0], readSessions(a), readSessions(b));
  assert.equal(r.rows_equal, true, "行数确实相等（这正是假对账的伪装）");
  assert.equal(r.pk_sets_equal, false, "主键集合必须不等（只比计数会误判为一致）");
  assert.deepEqual(r.pk_only_in_source, ["s1"]);
  assert.deepEqual(r.pk_only_in_target, ["s2"]);
});

test("内容错位（同行主键·不同内容）⇒ 内容判不等", () => {
  const a = tempDb("a");
  const b = tempDb("b");
  seed(a, [S]);
  seed(b, [{ ...S, title: "另一个标题" }]);
  const r = reconcileTable(BUSINESS_TABLES[0], readSessions(a), readSessions(b));
  assert.equal(r.rows_equal, true);
  assert.equal(r.pk_sets_equal, true);
  assert.equal(r.content_equal, false, "同行内容不同必须被判出");
  assert.ok(r.content_mismatch_sample.length >= 1);
});

test("编排层 reconcileAll：异步读两侧逐表对账 ⇒ 全等", async () => {
  const a = tempDb("a");
  const b = tempDb("b");
  seed(a, [S]);
  seed(b, [S]);
  const res = await reconcileAll(
    [BUSINESS_TABLES[0]],
    async () => readSessions(a),
    async () => readSessions(b),
  );
  assert.equal(res.length, 1);
  assert.equal(res[0].source_rows, 1, "读函数是异步的⇒编排层必须 await 到真实行数（拿到 Promise 对象时此处不是 1）");
  assert.equal(res[0].target_rows, 1);
  assert.equal(res[0].pk_sets_equal, true);
  assert.equal(res[0].content_equal, true);
});

test("编排层 reconcileAll：两侧内容不同 ⇒ 编排层判不等（不吞差异）", async () => {
  const a = tempDb("a");
  const b = tempDb("b");
  seed(a, [S]);
  seed(b, [{ ...S, title: "另一个标题" }]);
  const res = await reconcileAll(
    [BUSINESS_TABLES[0]],
    async () => readSessions(a),
    async () => readSessions(b),
  );
  assert.equal(res[0].rows_equal, true);
  assert.equal(res[0].content_equal, false, "编排层不得把差异吞掉");
});

test("时间列规范化：同一时刻不同串 ⇒ 内容判等", () => {
  const spec = BUSINESS_TABLES[0];
  const a = { ...S, created_at: "2026-11-10T08:00:00.000Z" };
  const b = { ...S, created_at: new Date("2026-11-10T16:00:00.000+08:00") };
  assert.equal(canon(a as Record<string, unknown>, spec), canon(b as Record<string, unknown>, spec));
  assert.equal(normIso("2026-11-10T16:00:00.000+08:00"), "2026-11-10T08:00:00.000Z");
});
