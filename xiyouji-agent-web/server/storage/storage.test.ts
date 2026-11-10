/**
 * storage.test.ts — 存储层契约测试（W934 · D-2a · M12）
 *
 * 目的：证明「同一套语义」在 **SQLite** 与 **PostgreSQL** 两个后端上都成立。
 *
 * 为什么必须有两套：抽象层的价值全在「换后端不动业务逻辑」上。
 * 若两个后端各写各的测试，抽象层就只是一层**转发**——没人能证明换后端后行为不变。
 * 所以这里是**同一份用例**跑两个后端（参数化），任何一侧语义漂移都会被抓住。
 *
 * 覆盖的语义（与 `server/storage/types.ts` 的「语义约定」逐条对应）：
 *  1. createSession / createMessage 返回入参对象本身
 *  2. updateSession / updateMessage 返回是否命中行（0 行 ⇒ false）
 *  3. insertFeedback 同 message_id 覆盖旧 verdict（upsert）
 *  4. deleteSession 级联删除其 messages 与 feedback
 *  5. clearAllData 清空三表且幂等
 *  6. feedbackSummary 只统计窗口内
 *  7. 时间列读出是 ISO-8601 UTC 毫秒精度字符串
 *  8. listSessionsWithMessageCount 同时给 message_count 与 messageCount
 *  9. healthCheck 可用
 *
 * PG 后端的前置条件（**不满足则跳过而不是失败**）：
 *  PG 可达 + 应用账号可连 + 业务三表已建（由 `deploy/pg/bin/migrate-sqlite-to-pg.ts`
 *  应用迁移序列时建好）。本机无 PG 时，本组用例报 skip——
 *  **但 SQLite 侧永远全跑**（SQLite 后端无外部依赖，是契约的基准线）。
 *
 * 运行：cd xiyouji-agent-web && node --import tsx --test server/storage/storage.test.ts
 */
import { test, before, after } from "node:test";
import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Pool } from "pg";
import Database from "better-sqlite3";
import { createSqliteBackend } from "./sqlite.js";
import { createPostgresBackend, resolvePostgresConfig } from "./postgres.js";
import type { DbMessage, DbSession, StorageBackend } from "./types.js";
import { ComplianceError, ComplianceErrorCode } from "../compliance/errors.js";
import { pgComplianceDdl } from "../compliance/schema.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));

/** 统一的用例执行器：两个后端跑同一份断言。 */
async function runContractSuite(
  name: string,
  makeBackend: () => Promise<StorageBackend>
): Promise<void> {
  const b = await makeBackend();

  const sid = "sess-1";
  const mid = "msg-1";
  const now = "2026-01-02T03:04:05.000Z";

  const session: DbSession = {
    id: sid,
    title: "契约会话",
    model: "test-model",
    sdk_session_id: null,
    created_at: now,
    updated_at: now,
    data_class: "L3",
  };
  const message: DbMessage = {
    id: mid,
    session_id: sid,
    role: "user",
    content: "契约消息",
    model: null,
    created_at: now,
    tool_calls: null,
    data_class: "L3",
  };

  // ---- ① 建会话：返回入参对象本身 ----
  const created = await b.createSession(session);
  assert.deepEqual(created, session, "createSession 应返回入参对象本身");

  // ---- ② 读回：字段逐项一致（尤其时间列形态） ----
  const got = await b.getSession(sid);
  assert.ok(got, "刚建的会话应能读回");
  assert.equal(got.id, sid);
  assert.equal(got.title, session.title);
  assert.equal(got.model, session.model);
  assert.equal(got.sdk_session_id, null);
  assert.equal(got.created_at, now, "时间列应逐字节相等（ISO-8601 UTC 毫秒精度）");
  assert.equal(got.updated_at, now, "时间列应逐字节相等");

  // ---- ③ 不存在的会话 ⇒ undefined ----
  assert.equal(await b.getSession("no-such-session"), undefined);

  // ---- ④ 建消息 + 读回 ----
  const cm = await b.createMessage(message);
  assert.deepEqual(cm, message, "createMessage 应返回入参对象本身");
  const msgs = await b.getMessagesBySession(sid);
  assert.equal(msgs.length, 1);
  assert.equal(msgs[0].content, message.content);
  assert.equal(msgs[0].created_at, now, "消息时间列应逐字节相等");
  assert.equal(msgs[0].tool_calls, null);

  // ---- ⑤ update 命中 / 未命中 ----
  assert.equal(await b.updateSession(sid, { title: "改后的标题" }), true, "命中行应返回 true");
  assert.equal(await b.updateSession("no-such-session", { title: "x" }), false, "未命中应返回 false");
  assert.equal((await b.getSession(sid))?.title, "改后的标题");
  // 空更新集 ⇒ false（不触发写入）
  assert.equal(await b.updateSession(sid, {}), false, "空更新集应返回 false");

  assert.equal(await b.updateMessage(mid, { content: "改后的内容" }), true);
  assert.equal(await b.updateMessage("no-such-msg", { content: "x" }), false);
  assert.equal((await b.getMessagesBySession(sid))[0].content, "改后的内容");

  // ---- ⑥ 会话列表含 message_count / messageCount 两个别名 ----
  const list = await b.listSessionsWithMessageCount(10);
  const row = list.find((r) => r.id === sid) as Record<string, unknown> | undefined;
  assert.ok(row, "列表应含该会话");
  assert.equal(Number(row!.message_count), 1, "message_count 应为该会话的消息数");
  assert.equal(Number(row!.messageCount), 1, "messageCount 别名列应同值");

  // ---- ⑦ 反馈 upsert：同 message_id 覆盖 ----
  await b.insertFeedback({
    id: "fb-1",
    session_id: sid,
    message_id: mid,
    verdict: "up",
    comment: "第一次",
    data_class: "L2",
  });
  await b.insertFeedback({
    id: "fb-2",
    session_id: sid,
    message_id: mid,
    verdict: "down",
    comment: "第二次",
    data_class: "L2",
  });
  const sum1 = await b.feedbackSummary(30);
  assert.equal(sum1.up, 0, "同 message_id 覆盖后不应残留 up");
  assert.equal(sum1.down, 1, "同 message_id 覆盖后应为 down");

  // ---- ⑧ 级联删除：删会话 ⇒ 消息与反馈一并消失 ----
  assert.equal(await b.deleteSession(sid), true);
  assert.equal(await b.getSession(sid), undefined);
  assert.equal((await b.getMessagesBySession(sid)).length, 0, "消息应随会话级联删除");
  assert.equal((await b.feedbackSummary(30)).down, 0, "反馈应随会话级联删除");

  // ---- ⑨ clearAllData 幂等 ----
  await b.createSession(session);
  await b.createMessage(message);
  await b.clearAllData();
  await b.clearAllData(); // 幂等
  assert.equal((await b.getAllSessions()).length, 0, "清库后不应有残留会话");

  // ---- ⑨' 写入权威时间（双写期两侧必须落同一个时间戳）----
  // W1204 真实 PG 实测抓到的真缺陷的**契约闸门**：
  //   写路径上的时间戳若由后端各自生成 ⇒ 双写期两侧副本差几毫秒
  //   ⇒ 集合级对账判「内容不等」⇒ 切读被永久阻断（实测读数：时间列 149/150）。
  const pinned = "2026-01-02T03:04:05.678Z";
  await b.createSession(session); // 上一步 clearAllData 已清空 ⇒ 先重建再验时间戳
  await b.updateSession(sid, { title: "钉时间的标题" }, { now: pinned });
  assert.equal(
    (await b.getSession(sid))?.updated_at,
    pinned,
    "updateSession 刷的 updated_at 应逐字节等于指定的权威时间",
  );
  await b.createMessage(message, { now: pinned });
  assert.equal(
    (await b.getSession(sid))?.updated_at,
    pinned,
    "createMessage 刷的会话 updated_at 应逐字节等于指定的权威时间",
  );
  await b.insertFeedback(
    { id: "fb-pinned", session_id: sid, message_id: mid, verdict: "up", comment: "钉到 2020 年" },
    { now: "2020-01-01T00:00:00.000Z" },
  );
  assert.equal(
    (await b.feedbackSummary(36500)).up,
    1,
    "insertFeedback 应落指定时间（否则 100 年窗口里查不到 ⇒ 说明后端忽略了权威时间）",
  );
  assert.equal(
    (await b.feedbackSummary(1)).up,
    0,
    "钉到 2020 年的反馈不该落进 1 天窗口（否则说明后端仍用自己的当前时间）",
  );

  // ---- ⑩ healthCheck ----
  const health = await b.healthCheck();
  assert.equal(health.ok, true, `健康探针应通过：${health.detail}`);
  assert.ok(health.detail.length > 0, "探针应给出可读依据");

  // ---- ⑪ C-6 合规契约（缺标签被拒 / 带标签通过 / 非法标签被拒）----
  await runComplianceCases(b);

  await b.close();
  console.log(`  ✔ 契约套件通过：${name}`);
}

/**
 * C-6 入库强制校验用例（**两个后端跑同一份断言**）。
 *
 * 四条口径：
 *  ① 非强制模式（默认）：缺标签 ⇒ 按分级目录推导并**落库**（现役调用点不被破坏）；
 *  ② 强制模式：缺标签 ⇒ **拒绝入库**，报可枚举错误码 COMPLIANCE_DATA_CLASS_MISSING；
 *  ③ 强制模式：带标签 ⇒ 通过，且标签原样落库可读回；
 *  ④ 非法标签值 ⇒ **一律拒绝**（COMPLIANCE_DATA_CLASS_INVALID，不因开关而放宽）。
 */
async function runComplianceCases(b: StorageBackend): Promise<void> {
  const now = "2026-02-03T04:05:06.000Z";
  const prev = process.env.AGENT_WEB_COMPLIANCE_ENFORCE;
  const mk = (id: string, over: Partial<DbSession> = {}): DbSession => ({
    id,
    title: "合规用例会话",
    model: "test-model",
    sdk_session_id: null,
    created_at: now,
    updated_at: now,
    ...over,
  });
  try {
    // ① 非强制模式：缺标签 ⇒ 推导并落库
    delete process.env.AGENT_WEB_COMPLIANCE_ENFORCE;
    const derived = await b.createSession(mk("sess-derived"));
    assert.equal(derived.data_class, "L3", "非强制模式：会话应按分级目录推导为 L3");
    assert.equal(
      (await b.getSession("sess-derived"))?.data_class,
      "L3",
      "推导出的分级标签应落库并可读回（不是只在内存里过一遍）",
    );

    // ② 强制模式：缺标签 ⇒ 拒绝入库
    process.env.AGENT_WEB_COMPLIANCE_ENFORCE = "1";
    await assert.rejects(
      () => b.createSession(mk("sess-no-class")),
      (err: unknown) => {
        assert.ok(err instanceof ComplianceError, "缺标签应抛 ComplianceError（可按类渲染）");
        assert.equal(err.code, ComplianceErrorCode.DATA_CLASS_MISSING, "错误码应为 DATA_CLASS_MISSING");
        return true;
      },
      "强制模式：缺分级标签必须拒绝入库",
    );
    assert.equal(await b.getSession("sess-no-class"), undefined, "被拒的行不应入库");

    // ③ 强制模式：带标签 ⇒ 通过
    const tagged = await b.createSession(mk("sess-tagged", { data_class: "L2" }));
    assert.equal(tagged.data_class, "L2", "显式标签应原样返回");
    assert.equal(
      (await b.getSession("sess-tagged"))?.data_class,
      "L2",
      "显式标签应落库并可读回",
    );

    // ④ 非法标签值 ⇒ 一律拒绝（不因开关而放宽）
    await assert.rejects(
      () => b.createSession(mk("sess-bad-class", { data_class: "L9" as never })),
      (err: unknown) => {
        assert.ok(err instanceof ComplianceError, "非法标签应抛 ComplianceError");
        assert.equal(err.code, ComplianceErrorCode.DATA_CLASS_INVALID, "错误码应为 DATA_CLASS_INVALID");
        return true;
      },
      "非法分级标签值必须拒绝入库",
    );
    assert.equal(await b.getSession("sess-bad-class"), undefined, "被拒的行不应入库");

    // ⑤ 消息与反馈同样受约束（L3 / L2）
    await assert.rejects(
      () => b.createMessage({ id: "msg-no-class", session_id: "sess-tagged", role: "user", content: "x", model: null, created_at: now, tool_calls: null }),
      (err: unknown) => err instanceof ComplianceError && err.code === ComplianceErrorCode.DATA_CLASS_MISSING,
      "强制模式：消息缺标签同样拒绝",
    );
    await assert.rejects(
      () => b.insertFeedback({ id: "fb-no-class", session_id: "sess-tagged", message_id: "msg-x", verdict: "up", comment: null }),
      (err: unknown) => err instanceof ComplianceError && err.code === ComplianceErrorCode.DATA_CLASS_MISSING,
      "强制模式：反馈缺标签同样拒绝",
    );
  } finally {
    if (prev === undefined) delete process.env.AGENT_WEB_COMPLIANCE_ENFORCE;
    else process.env.AGENT_WEB_COMPLIANCE_ENFORCE = prev;
  }
}

// ============= SQLite 后端（永远全跑） =============

test("契约：SQLite 后端满足 StorageBackend 全部语义", async () => {
  const tmp = path.join(os.tmpdir(), `xiyouji-storage-contract-${process.pid}-${Date.now()}.db`);
  try {
    await runContractSuite("SQLite", async () => createSqliteBackend(tmp));
  } finally {
    for (const suffix of ["", "-wal", "-shm"]) {
      const f = tmp + suffix;
      // 清理失败不得掩盖真正的断言失败（Windows 上文件仍被打开时会 EBUSY）
      try {
        if (fs.existsSync(f)) fs.unlinkSync(f);
      } catch {
        /* 临时文件残留不影响结论 */
      }
    }
  }
});

// ============= PG 后端（环境不满足则 skip） =============

/** 契约测试专用的 PG schema 名（与业务 schema 隔离·避免污染真实数据）。 */
const CONTRACT_SCHEMA = "storage_contract_test";

/**
 * 探测 PG 是否可用。
 *
 * 注意：**不在这里建业务表**——契约测试跑在自己的 schema 里（见下），
 * 业务库的数据（迁移过来的真实会话等）**不受影响**。
 *
 * 为什么要 schema 隔离而不是「先清空再测」：
 *   首版契约测试直接在业务 schema 上跑，清库动作把**已迁移的真实数据**也清了，
 *   且 `feedbackSummary` 把既有行算进断言 ⇒ 断言失败却不代表后端有缺陷
 *   （实测首跑即如此：actual=4 来自迁移进来的 4 行反馈）。
 *   ⇒ 隔离测试数据是**前提**，不是洁癖。
 */
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
    return { ok: false, reason: `PG 不可达：${err instanceof Error ? err.message : String(err)}` };
  } finally {
    await pool.end().catch(() => undefined);
  }
}

/** 在契约专用 schema 里建业务表（用 0002 迁移文件·与应用真实路径同一份 schema 定义）。 */
async function prepareContractSchema(): Promise<void> {
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
  try {
    await admin.query(`DROP SCHEMA IF EXISTS ${CONTRACT_SCHEMA} CASCADE`);
    await admin.query(`CREATE SCHEMA ${CONTRACT_SCHEMA}`);
    const scoped = new Pool({
      host: cfg.host,
      port: cfg.port,
      user: cfg.user,
      password: cfg.password,
      database: cfg.database,
      max: 1,
      options: `-c search_path=${CONTRACT_SCHEMA}`,
      connectionTimeoutMillis: 5_000,
    });
    try {
      const sql = fs.readFileSync(
        path.resolve(HERE, "..", "..", "deploy", "pg", "migrations", "0002_app_tables.sql"),
        "utf-8"
      );
      await scoped.query(sql);
      // W1205（D-3 合规批）：业务表补 data_class 列——
      //   DDL 事实源在 server/compliance/schema.ts（生产侧由控制器落成 0003_compliance_columns.sql，
      //   内容必须与 pgComplianceDdl() 逐字一致 ⇒ 测试 schema 与生产 schema 不漂移）。
      await scoped.query(pgComplianceDdl());
    } finally {
      await scoped.end().catch(() => undefined);
    }
  } finally {
    await admin.end().catch(() => undefined);
  }
}

test("迁移：存量 SQLite 库（无 data_class 列）打开即补列并可写可读", async () => {
  const tmp = path.join(os.tmpdir(), `xiyouji-legacy-migrate-${process.pid}-${Date.now()}.db`);
  try {
    // 造一个「旧形态」库：只有 W919 之前的表定义（无 data_class 列）
    const legacy = new Database(tmp);
    legacy.exec(`
      CREATE TABLE sessions (id TEXT PRIMARY KEY, title TEXT NOT NULL, model TEXT NOT NULL,
        sdk_session_id TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
      CREATE TABLE messages (id TEXT PRIMARY KEY, session_id TEXT NOT NULL, role TEXT NOT NULL,
        content TEXT NOT NULL, model TEXT, created_at TEXT NOT NULL, tool_calls TEXT);
      CREATE TABLE feedback (id TEXT PRIMARY KEY, session_id TEXT NOT NULL, message_id TEXT NOT NULL,
        verdict TEXT NOT NULL, comment TEXT, created_at TEXT NOT NULL);
    `);
    legacy.close();

    // 打开后端 ⇒ 迁移框架应补上 data_class 列（存量行按目录默认值回填）
    const backend = createSqliteBackend(tmp);
    try {
      const now = "2026-04-05T06:07:08.000Z";
      const created = await backend.createSession({
        id: "legacy-1",
        title: "存量库会话",
        model: "m",
        sdk_session_id: null,
        created_at: now,
        updated_at: now,
      });
      assert.equal(created.data_class, "L3", "存量库补列后应带分级标签");
      assert.equal((await backend.getSession("legacy-1"))?.data_class, "L3", "分级标签应落库可读回");
    } finally {
      await backend.close();
    }
  } finally {
    for (const suffix of ["", "-wal", "-shm"]) {
      const f = tmp + suffix;
      try {
        if (fs.existsSync(f)) fs.unlinkSync(f);
      } catch {
        /* 临时文件残留不影响结论 */
      }
    }
  }
});

test("PG 缺合规列 ⇒ 抛可枚举错误 SCHEMA_OUT_OF_DATE（提示补迁移，而非裸 SQL 错）", async (t) => {
  const probe = await probePostgres();
  if (!probe.ok) {
    t.skip(`跳过（${probe.reason}）`);
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
  try {
    // 只建 0002 的业务表（**不建**合规列）⇒ 模拟「迁移未落」
    await admin.query("DROP SCHEMA IF EXISTS " + CONTRACT_SCHEMA + " CASCADE");
    await admin.query("CREATE SCHEMA " + CONTRACT_SCHEMA);
    const scoped = new Pool({
      host: cfg.host,
      port: cfg.port,
      user: cfg.user,
      password: cfg.password,
      database: cfg.database,
      max: 1,
      options: `-c search_path=${CONTRACT_SCHEMA}`,
      connectionTimeoutMillis: 5_000,
    });
    try {
      const sql = fs.readFileSync(
        path.resolve(HERE, "..", "..", "deploy", "pg", "migrations", "0002_app_tables.sql"),
        "utf-8"
      );
      await scoped.query(sql);
    } finally {
      await scoped.end().catch(() => undefined);
    }
    const backend = createPostgresBackend({ ...resolvePostgresConfig(), schema: CONTRACT_SCHEMA });
    try {
      const now = "2026-04-05T06:07:08.000Z";
      await assert.rejects(
        () =>
          backend.createSession({
            id: "pg-missing-col",
            title: "缺列",
            model: "m",
            sdk_session_id: null,
            created_at: now,
            updated_at: now,
          }),
        (err: unknown) => {
          assert.ok(err instanceof ComplianceError, "应为 ComplianceError");
          assert.equal(err.code, ComplianceErrorCode.SCHEMA_OUT_OF_DATE, "错误码应为 SCHEMA_OUT_OF_DATE");
          assert.match(String(err.detail.hint), /0003_compliance_columns/, "应提示补哪份迁移");
          return true;
        },
        "PG 业务表缺 data_class 列时必须给出可枚举的部署缺陷错误",
      );
    } finally {
      await backend.close();
    }
  } finally {
    await admin.query("DROP SCHEMA IF EXISTS " + CONTRACT_SCHEMA + " CASCADE").catch(() => undefined);
    await admin.end().catch(() => undefined);
  }
});

test("契约：PostgreSQL 后端满足 StorageBackend 全部语义", async (t) => {
  const probe = await probePostgres();
  if (!probe.ok) {
    t.skip(`跳过（${probe.reason}）`);
    return;
  }
  await prepareContractSchema();
  try {
    await runContractSuite("PostgreSQL", async () =>
      createPostgresBackend({ ...resolvePostgresConfig(), schema: CONTRACT_SCHEMA })
    );
  } finally {
    // 收尾：清掉契约 schema（只删自己的·不碰业务 schema）
    const cfg = resolvePostgresConfig();
    const admin = new Pool({
      host: cfg.host,
      port: cfg.port,
      user: cfg.user,
      password: cfg.password,
      database: cfg.database,
      max: 1,
      connectionTimeoutMillis: 5_000,
    });
    try {
      await admin.query(`DROP SCHEMA IF EXISTS ${CONTRACT_SCHEMA} CASCADE`);
    } catch {
      /* 清理失败不影响结论 */
    } finally {
      await admin.end().catch(() => undefined);
    }
  }
});
