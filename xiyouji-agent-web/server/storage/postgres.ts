/**
 * postgres.ts — PostgreSQL 16 存储后端（W934 · D-2a · M12 存储层抽象）
 *
 * 目标后端：架构方案 v2 §7.1 S4「PostgreSQL 16（自建单机）」·§8.2 档 2 ·§7.3 迁移映射。
 *
 * 五条硬纪律（违反任一条即为实现缺陷，不是风格问题）：
 *  1. **禁字符串拼接 SQL**——全部走 `$1/$2` 参数化查询。表名/列名是编译期常量，
 *     直接写进 SQL 字面量（不来自用户输入），因此无需动态拼接。
 *  2. **时间列边界转换**——列类型 `TIMESTAMPTZ`（服务 §7.4 生命周期的日期算术），
 *     接口契约是 ISO-8601 字符串 ⇒ 读出转字符串、写入转 Date。
 *  3. **写入前校验时间串**——非法时间串必须**报错并指出原值**，不得静默跳过
 *     （ASM-20：脏数据要暴露，不能被"修"掉）。
 *  4. **口令不出现在任何输出**——错误信息只带 host/port/db/user，不带连接串与口令。
 *  5. **外键级联依赖数据库**——`feedback` / `messages` 的 `ON DELETE CASCADE`
 *     由 PG 强制（SQLite 侧靠 `foreign_keys=ON` pragma，语义一致）。
 *
 * 与 SQLite 后端的**语义等价性**由 `server/storage/storage.test.ts` 的
 * 同一套契约用例守住（两个后端跑同一份断言）。
 */
import { Pool, type PoolClient } from "pg";
import type {
  DbFeedback,
  DbMessage,
  DbSession,
  MessageUpdates,
  SessionUpdates,
  StorageBackend,
  StorageHealth,
  WriteTimeOpts,
} from "./types.js";
import { isDataClass, resolveWriteDataClass } from "../compliance/data-class.js";
import { ComplianceError, ComplianceErrorCode } from "../compliance/errors.js";
import { decryptSensitiveColumns, encryptSensitiveColumns } from "./encryption.js";

/** PG 后端配置（全部有默认值；口令只从环境变量取，绝不落盘）。 */
export interface PostgresConfig {
  host: string;
  port: number;
  user: string;
  password: string;
  database: string;
  /** 连接池上限（方案 §5.1 M12「连接池」）。 */
  max: number;
  /** 是否启用 TLS（方案 §12.4：服务端 ↔ PG 必须 TLS·内网不豁免）。 */
  ssl: boolean;
  /**
   * 目标 schema（可选）。设置后连接以 `search_path` 指向该 schema。
   *
   * 两个用途：
   *  ① **测试隔离**——契约测试跑在自己的 schema 里，不碰业务数据；
   *  ② **多租户/分库分 schema 隔离**（未来的演进方向）。
   * 空 = 用连接的默认 search_path（`"$user", public`）。
   */
  schema?: string;
}

/**
 * 从环境变量解析 PG 配置。
 *
 * 口径：`AGENT_WEB_PG_*` 优先；未设时回落到 libpq 标准环境变量（`PGHOST` 等），
 * 再回落到本机默认值。**口令只从环境变量读**（`AGENT_WEB_PG_PASSWORD` / `PGPASSWORD`）。
 */
export function resolvePostgresConfig(): PostgresConfig {
  const num = (v: string | undefined, dflt: number): number => {
    const n = Number(v);
    return Number.isFinite(n) && n > 0 ? n : dflt;
  };
  return {
    host: process.env.AGENT_WEB_PG_HOST || process.env.PGHOST || "127.0.0.1",
    port: num(process.env.AGENT_WEB_PG_PORT || process.env.PGPORT, 5432),
    user: process.env.AGENT_WEB_PG_USER || process.env.PGUSER || "postgres",
    password: process.env.AGENT_WEB_PG_PASSWORD || process.env.PGPASSWORD || "",
    database: process.env.AGENT_WEB_PG_DATABASE || process.env.PGDATABASE || "xiyouji",
    max: num(process.env.AGENT_WEB_PG_POOL_MAX, 10),
    ssl: (process.env.AGENT_WEB_PG_SSL || "disable").toLowerCase() === "require",
    schema: (process.env.AGENT_WEB_PG_SCHEMA || "").trim() || undefined,
  };
}

/** 供日志与探针使用的**无口令**连接标识。 */
export function describeTarget(cfg: PostgresConfig): string {
  return `${cfg.host}:${cfg.port}/${cfg.database}（user=${cfg.user}）`;
}

/**
 * 时间串 → Date（严格校验）。
 *
 * 非法值必须抛出并带上原值与定位信息（纪律 3）——
 * 迁移期这类值是**脏数据信号**，被静默吞掉就再也发现不了。
 */
export function toDate(iso: string, where: string): Date {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) {
    throw new Error(`时间值非法（${where}）：${JSON.stringify(iso)}`);
  }
  return d;
}

/** Date → ISO-8601 UTC 毫秒精度字符串（接口契约形态）。 */
export function toIso(v: unknown): string {
  if (v instanceof Date) return v.toISOString();
  if (typeof v === "string") return v;
  if (v === null || v === undefined) return "";
  return String(v);
}

/**
 * 单字段加密（更新路径用；幂等——已是密文信封的值原样保留）。
 */
function encryptField(table: string, column: string, value: string): string {
  const row = encryptSensitiveColumns({ [column]: value } as Record<string, unknown>, table);
  return String(row[column]);
}

/**
 * 把 PG 的「缺列」错误翻译成可枚举的合规错误（部署缺陷提示）。
 *
 * 业务表的 data_class 列由 deploy/pg/migrations 下的合规迁移提供；
 * 迁移未落 ⇒ 写入报 PG 的 column does not exist ⇒ 翻译成 SCHEMA_OUT_OF_DATE，
 * 免得运维看到一条裸 SQL 错误猜不出是「迁移没跑」。
 */
function assertNoMissingComplianceColumn(err: unknown): void {
  const msg = err instanceof Error ? err.message : String(err);
  if (/column "data_class".*does not exist/i.test(msg)) {
    throw new ComplianceError(
      ComplianceErrorCode.SCHEMA_OUT_OF_DATE,
      "业务表缺少 data_class 列（缺合规迁移）",
      { hint: "apply deploy/pg/migrations/0003_compliance_columns.sql" }
    );
  }
}

/** PG 的 `COUNT(*)` 是 int8 ⇒ 驱动默认给字符串 ⇒ 统一转 number。 */
function toCount(v: unknown): number {
  if (typeof v === "number") return v;
  if (typeof v === "string") {
    const n = Number(v);
    return Number.isFinite(n) ? n : 0;
  }
  return 0;
}

/** PG 后端实例。 */
export interface PostgresBackend extends StorageBackend {
  readonly kind: "postgres";
  /** 无口令的连接标识（供日志）。 */
  readonly target: string;
}

export function createPostgresBackend(cfg: PostgresConfig = resolvePostgresConfig()): PostgresBackend {
  const pool = new Pool({
    host: cfg.host,
    port: cfg.port,
    user: cfg.user,
    password: cfg.password,
    database: cfg.database,
    max: cfg.max,
    ssl: cfg.ssl ? { rejectUnauthorized: false } : undefined,
    // schema 隔离：连接建立时即把 search_path 指到目标 schema
    // （schema 名来自部署配置·非用户输入·不做拼接注入风险评估）
    options: cfg.schema ? `-c search_path=${cfg.schema}` : undefined,
    // 连接串与口令**禁进日志**（纪律 4）
    connectionTimeoutMillis: 10_000,
  });
  // 空闲连接错误不炸进程（池回收时的偶发错误不应中断服务）
  pool.on("error", (err) => {
    console.error(`[PG] 空闲连接错误：${err instanceof Error ? err.message : String(err)}`);
  });

  const target = describeTarget(cfg);

  /** 在一个事务里执行（失败回滚）。 */
  async function inTransaction<T>(fn: (client: PoolClient) => Promise<T>): Promise<T> {
    const client = await pool.connect();
    try {
      await client.query("BEGIN");
      const out = await fn(client);
      await client.query("COMMIT");
      return out;
    } catch (err) {
      try {
        await client.query("ROLLBACK");
      } catch {
        /* 回滚失败不掩盖原始错误 */
      }
      throw err;
    } finally {
      client.release();
    }
  }

  /** 行 → DbSession（时间列转 ISO 字符串 + 敏感列解密）。 */
  function toSession(row: Record<string, unknown>): DbSession {
    const decrypted = decryptSensitiveColumns(row, "sessions");
    return {
      id: String(decrypted.id),
      title: String(decrypted.title),
      model: String(decrypted.model),
      sdk_session_id: decrypted.sdk_session_id === null || decrypted.sdk_session_id === undefined
        ? null
        : String(decrypted.sdk_session_id),
      created_at: toIso(decrypted.created_at),
      updated_at: toIso(decrypted.updated_at),
      data_class: isDataClass(decrypted.data_class) ? decrypted.data_class : undefined,
    };
  }

  /** 行 → DbMessage。 */
  function toMessage(row: Record<string, unknown>): DbMessage {
    const decrypted = decryptSensitiveColumns(row, "messages");
    return {
      id: String(decrypted.id),
      session_id: String(decrypted.session_id),
      role: decrypted.role === "assistant" ? "assistant" : "user",
      content: String(decrypted.content),
      model: decrypted.model === null || decrypted.model === undefined ? null : String(decrypted.model),
      created_at: toIso(decrypted.created_at),
      tool_calls: decrypted.tool_calls === null || decrypted.tool_calls === undefined
        ? null
        : String(decrypted.tool_calls),
      data_class: isDataClass(decrypted.data_class) ? decrypted.data_class : undefined,
    };
  }

  const backend: PostgresBackend = {
    kind: "postgres",
    target,

    async listSessionsWithMessageCount(limit: number): Promise<Array<Record<string, unknown>>> {
      // LATERAL 子查询取 message_count（与 SQLite 版的单 SQL 口径等价·W919 B-DB-02）
      const { rows } = await pool.query(
        `SELECT s.id, s.title, s.model, s.sdk_session_id, s.created_at, s.updated_at,
                c.cnt AS message_count, c.cnt AS "messageCount"
           FROM (SELECT * FROM sessions ORDER BY updated_at DESC LIMIT $1) s
           LEFT JOIN LATERAL (
                SELECT COUNT(*)::bigint AS cnt FROM messages m WHERE m.session_id = s.id
           ) c ON TRUE`,
        [limit]
      );
      return rows.map((r) => {
        const sess = toSession(r);
        const cnt = toCount(r.message_count);
        return {
          id: sess.id,
          title: sess.title,
          model: sess.model,
          sdk_session_id: sess.sdk_session_id,
          created_at: sess.created_at,
          updated_at: sess.updated_at,
          message_count: cnt,
          messageCount: cnt,
        };
      });
    },

    async getAllSessions(): Promise<DbSession[]> {
      const { rows } = await pool.query("SELECT * FROM sessions ORDER BY updated_at DESC");
      return rows.map(toSession);
    },

    async getSession(id: string): Promise<DbSession | undefined> {
      const { rows } = await pool.query("SELECT * FROM sessions WHERE id = $1", [id]);
      return rows.length ? toSession(rows[0]) : undefined;
    },

    async createSession(session: DbSession): Promise<DbSession> {
      const cls = resolveWriteDataClass(session.data_class, "sessions", "sessions.insert");
      const prepared = encryptSensitiveColumns({ ...session, data_class: cls }, "sessions");
      try {
        await pool.query(
          `INSERT INTO sessions (id, title, model, sdk_session_id, created_at, updated_at, data_class)
         VALUES ($1, $2, $3, $4, $5, $6, $7)`,
          [
            prepared.id,
            prepared.title,
            prepared.model,
            prepared.sdk_session_id,
            toDate(prepared.created_at, "sessions.created_at"),
            toDate(prepared.updated_at, "sessions.updated_at"),
            cls,
          ]
        );
      } catch (err) {
        assertNoMissingComplianceColumn(err);
        throw err;
      }
      return { ...session, data_class: cls };
    },

    async updateSession(id: string, updates: SessionUpdates, opts?: WriteTimeOpts): Promise<boolean> {
      const fields: string[] = [];
      const values: unknown[] = [];
      if (updates.title !== undefined) {
        values.push(encryptField("sessions", "title", updates.title));
        fields.push(`title = $${values.length}`);
      }
      if (updates.model !== undefined) {
        values.push(updates.model);
        fields.push(`model = $${values.length}`);
      }
      if (updates.sdk_session_id !== undefined) {
        values.push(updates.sdk_session_id);
        fields.push(`sdk_session_id = $${values.length}`);
      }
      if (fields.length === 0) return false;

      // W1204 实测修根：权威时间由调用方给（双写期两侧同值）⇒ 缺省才取当前时间（现役语义不变）
      values.push(toDate(opts?.now ?? new Date().toISOString(), "sessions.updated_at"));
      fields.push(`updated_at = $${values.length}`);
      values.push(id);

      const res = await pool.query(
        `UPDATE sessions SET ${fields.join(", ")} WHERE id = $${values.length}`,
        values
      );
      return (res.rowCount ?? 0) > 0;
    },

    async deleteSession(id: string): Promise<boolean> {
      // messages / feedback 由外键 ON DELETE CASCADE 级联删
      const res = await pool.query("DELETE FROM sessions WHERE id = $1", [id]);
      return (res.rowCount ?? 0) > 0;
    },

    async getMessagesBySession(sessionId: string): Promise<DbMessage[]> {
      const { rows } = await pool.query(
        "SELECT * FROM messages WHERE session_id = $1 ORDER BY created_at ASC",
        [sessionId]
      );
      return rows.map(toMessage);
    },

    async createMessage(message: DbMessage, opts?: WriteTimeOpts): Promise<DbMessage> {
      const cls = resolveWriteDataClass(message.data_class, "messages", "messages.insert");
      const prepared = encryptSensitiveColumns({ ...message, data_class: cls }, "messages");
      // 建消息 + 刷会话 updated_at 必须在同一事务里（否则可能出现「消息已建但时间未刷」）
      await inTransaction(async (client) => {
        try {
          await client.query(
            `INSERT INTO messages (id, session_id, role, content, model, created_at, tool_calls, data_class)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
            [
              prepared.id,
              prepared.session_id,
              prepared.role,
              prepared.content,
              prepared.model,
              toDate(prepared.created_at, "messages.created_at"),
              prepared.tool_calls,
              cls,
            ]
          );
        } catch (err) {
          assertNoMissingComplianceColumn(err);
          throw err;
        }
        // W1204 实测修根：会话 updated_at 的权威时间两侧同传（见 types.ts 的 WriteTimeOpts）
        await client.query("UPDATE sessions SET updated_at = $1 WHERE id = $2", [
          toDate(opts?.now ?? new Date().toISOString(), "sessions.updated_at"),
          prepared.session_id,
        ]);
      });
      return { ...message, data_class: cls };
    },

    async updateMessage(id: string, updates: MessageUpdates): Promise<boolean> {
      const fields: string[] = [];
      const values: unknown[] = [];
      if (updates.content !== undefined) {
        values.push(encryptField("messages", "content", updates.content));
        fields.push(`content = $${values.length}`);
      }
      if (updates.tool_calls !== undefined) {
        values.push(updates.tool_calls);
        fields.push(`tool_calls = $${values.length}`);
      }
      if (fields.length === 0) return false;

      values.push(id);
      const res = await pool.query(
        `UPDATE messages SET ${fields.join(", ")} WHERE id = $${values.length}`,
        values
      );
      return (res.rowCount ?? 0) > 0;
    },

    async deleteMessage(id: string): Promise<boolean> {
      const res = await pool.query("DELETE FROM messages WHERE id = $1", [id]);
      return (res.rowCount ?? 0) > 0;
    },

    async createMessages(messages: DbMessage[]): Promise<void> {
      if (messages.length === 0) return;
      await inTransaction(async (client) => {
        for (const msg of messages) {
          const cls = resolveWriteDataClass(msg.data_class, "messages", "messages.insertMany");
          const prepared = encryptSensitiveColumns({ ...msg, data_class: cls }, "messages");
          try {
            await client.query(
              `INSERT INTO messages (id, session_id, role, content, model, created_at, tool_calls, data_class)
             VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
              [
                prepared.id,
                prepared.session_id,
                prepared.role,
                prepared.content,
                prepared.model,
                toDate(prepared.created_at, "messages.created_at"),
                prepared.tool_calls,
                cls,
              ]
            );
          } catch (err) {
            assertNoMissingComplianceColumn(err);
            throw err;
          }
        }
      });
    },

    async insertFeedback(f: Omit<DbFeedback, "created_at">, opts?: WriteTimeOpts): Promise<number> {
      const cls = resolveWriteDataClass(f.data_class, "feedback", "feedback.insert");
      // 同 message_id 覆盖（W917 B-DB-01 的单维唯一口径）
      let res;
      try {
        res = await pool.query(
          `INSERT INTO feedback (id, session_id, message_id, verdict, comment, created_at, data_class)
         VALUES ($1, $2, $3, $4, $5, $6, $7)
         ON CONFLICT (message_id) DO UPDATE
           SET verdict = EXCLUDED.verdict,
               comment = EXCLUDED.comment,
               created_at = EXCLUDED.created_at`,
          // W1204 实测修根：feedback.created_at 的权威时间两侧同传（见 types.ts 的 WriteTimeOpts）
          [
            f.id,
            f.session_id,
            f.message_id,
            f.verdict,
            f.comment ?? null,
            toDate(opts?.now ?? new Date().toISOString(), "feedback.created_at"),
            cls,
          ]
        );
      } catch (err) {
        assertNoMissingComplianceColumn(err);
        throw err;
      }
      return res.rowCount ?? 0;
    },

    async feedbackSummary(days = 30): Promise<{ up: number; down: number }> {
      const since = new Date(Date.now() - days * 86400000);
      const { rows } = await pool.query(
        "SELECT verdict, COUNT(*)::bigint AS n FROM feedback WHERE created_at >= $1 GROUP BY verdict",
        [since]
      );
      const find = (v: string) => toCount(rows.find((r) => r.verdict === v)?.n);
      return { up: find("up"), down: find("down") };
    },

    async clearAllData(): Promise<void> {
      // 依赖序清空（feedback → messages → sessions）·幂等
      await inTransaction(async (client) => {
        await client.query("DELETE FROM feedback");
        await client.query("DELETE FROM messages");
        await client.query("DELETE FROM sessions");
      });
    },

    async healthCheck(): Promise<StorageHealth> {
      try {
        const res = await pool.query("SELECT 1 AS ok");
        const ok = toCount(res.rows[0]?.ok) === 1;
        return ok
          ? { ok: true, detail: `postgres 正常（${target}）` }
          : { ok: false, detail: `postgres 探针返回异常（${target}）` };
      } catch (err) {
        return {
          ok: false,
          detail: `postgres 探针失败（${target}）：${err instanceof Error ? err.message : String(err)}`,
        };
      }
    },

    async close(): Promise<void> {
      await pool.end();
    },
  };

  return backend;
}
