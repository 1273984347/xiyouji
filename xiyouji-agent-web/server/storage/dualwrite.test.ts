/**
 * dualwrite.test.ts — 双写后端契约测试（W1203 · 架构方案 v2 §8.2 档 2 · D-2 第二子批）
 *
 * 目的：证明双写层的三条关键语义成立——
 *  1. **写两侧**：一次写之后两侧都能读到；
 *  2. **读只走主库**：只写副库的数据，读不到（读侧不会「两边混读」）；
 *  3. **副库写失败 ⇒ fail-closed**：抛错而不是静默吞掉。
 *
 * 为什么用两个 SQLite 实例互为双写两侧：双写层是**运行期**机制，与后端种类无关；
 * 用 SQLite 互为两侧可让本组用例**无外部依赖**地全跑（本机无 PG 时也能证语义），
 * PG 侧的实跑属「真实后端互写」范畴，留给对账批次。
 */
import assert from "node:assert/strict";
import { test } from "node:test";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

import { createDualWriteBackend } from "./dualwrite.js";
import { createSqliteBackend } from "./sqlite.js";
import type { StorageBackend } from "./types.js";

function tempDbPath(tag: string): string {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "dualwrite-"));
  return path.join(dir, tag + ".db");
}

function session(id: string, title: string) {
  return {
    id,
    title,
    model: "test-model",
    sdk_session_id: null,
    created_at: "2026-11-10T08:00:00.000Z",
    updated_at: "2026-11-10T08:00:00.000Z",
  };
}

function message(id: string, sessionId: string) {
  return {
    id,
    session_id: sessionId,
    role: "user" as const,
    content: "hello",
    created_at: "2026-11-10T08:00:01.000Z",
  };
}

test("双写：写两侧 · 两侧都能读到", async () => {
  const primaryPath = tempDbPath("primary");
  const secondaryPath = tempDbPath("secondary");
  const primary = createSqliteBackend(primaryPath);
  const secondary = createSqliteBackend(secondaryPath);
  const dual = createDualWriteBackend(primary, secondary);

  await dual.createSession(session("s1", "标题"));
  await dual.createMessage(message("m1", "s1"));

  const primaryDirect = createSqliteBackend(primaryPath);
  const secondaryDirect = createSqliteBackend(secondaryPath);
  const inPrimary = await primaryDirect.getSession("s1");
  const inSecondary = await secondaryDirect.getSession("s1");
  assert.ok(inPrimary, "主库应有该会话");
  assert.ok(inSecondary, "副库应也被写入（双写语义）");
  assert.equal(inSecondary?.title, "标题");
  const msgs = await secondaryDirect.getMessagesBySession("s1");
  assert.equal(msgs.length, 1, "副库应也被写入消息");

  await dual.close();
  await primaryDirect.close();
  await secondaryDirect.close();
});

test("双写：读只走主库（只写副库的数据读不到）", async () => {
  const primaryPath = tempDbPath("primary");
  const secondaryPath = tempDbPath("secondary");
  const primary = createSqliteBackend(primaryPath);
  const secondary = createSqliteBackend(secondaryPath);
  const dual = createDualWriteBackend(primary, secondary);

  // 直接写副库（绕过双写层）⇒ 读侧不应看到它
  await secondary.createSession(session("ghost", "只写在副库"));
  const seen = await dual.getSession("ghost");
  assert.equal(seen, undefined, "读只走主库：只写在副库的会话不应被读到");
  const all = await dual.getAllSessions();
  assert.equal(all.length, 0, "会话列表同样只反映主库");

  await dual.close();
});

test("双写：副库写失败 ⇒ fail-closed（抛错不静默吞）", async () => {
  const primaryPath = tempDbPath("primary");
  const primary = createSqliteBackend(primaryPath);
  const failing: StorageBackend = {
    ...primary,
    kind: "sqlite",
    async createSession() {
      throw new Error("secondary unavailable");
    },
  };
  const dual = createDualWriteBackend(primary, failing);

  await assert.rejects(
    () => dual.createSession(session("s2", "标题")),
    /secondary unavailable/,
    "副库写失败必须抛出（fail-closed）",
  );
  const health = (dual as unknown as { dualWriteState(): { secondaryHealthy: boolean | null } }).dualWriteState();
  assert.equal(health.secondaryHealthy, false, "副库不健康状态须可查");

  await dual.close();
});

test("双写：clearAllData 清两侧 · healthCheck 可用", async () => {
  const primaryPath = tempDbPath("primary");
  const secondaryPath = tempDbPath("secondary");
  const primary = createSqliteBackend(primaryPath);
  const secondary = createSqliteBackend(secondaryPath);
  const dual = createDualWriteBackend(primary, secondary);

  await dual.createSession(session("s3", "标题"));
  await dual.clearAllData();

  const primaryDirect = createSqliteBackend(primaryPath);
  const secondaryDirect = createSqliteBackend(secondaryPath);
  assert.equal((await primaryDirect.getAllSessions()).length, 0, "主库应被清空");
  assert.equal((await secondaryDirect.getAllSessions()).length, 0, "副库应被清空");
  const health = await dual.healthCheck();
  assert.ok(health, "healthCheck 应可用");

  await dual.close();
  await primaryDirect.close();
  await secondaryDirect.close();
});
