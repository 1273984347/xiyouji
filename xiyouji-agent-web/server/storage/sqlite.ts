/**
 * sqlite.ts — SQLite 存储后端（W934 · D-2a · M12 存储层抽象）
 *
 * 本文件是现役 `server/db.ts` 的**搬迁**：建表 DDL、3 版迁移、12 个业务函数
 * **逐字保留**，只做两件事——
 *  ① 包进 `createSqliteBackend()` 工厂，返回 `StorageBackend` 契约；
 *  ② 补 `kind` 与 `healthCheck()` 两个抽象层新增成员。
 *
 * 搬迁纪律（AC-02 / R-02）：凡「搬迁前后语义可能漂移」的点，都在此显式登记：
 *  - `journal_mode = WAL` 保留 —— 写放大与并发读的既有行为不能变；
 *  - `foreign_keys = ON` 保留 —— W917 B-DB-01 把级联删除从「声明了但没生效」改成真生效；
 *  - `MIGRATIONS` 三版与 `user_version` 记账保留 —— W919 B-DB-04 的迁移框架是现役资产；
 *  - 迁移执行时机保留「**实例创建时**」——现役是模块加载时执行，搬迁后仍是
 *    「首次创建 backend 时执行」，对调用方而言时点不变（工厂在模块加载期被调用）；
 *  - WAL checkpoint 仍在 close 时执行（TRUNCATE），避免残留 WAL 文件。
 *
 * 抽象层带来的**唯一行为差异**：函数体从同步改为 async（见 types.ts 头注）。
 * better-sqlite3 调用本身仍是同步的，未引入任何并发模型变化。
 */
import Database from "better-sqlite3";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import type {
  DbFeedback,
  DbMessage,
  DbSession,
  MessageUpdates,
  SessionUpdates,
  StorageBackend,
  StorageHealth,
} from "./types.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * 数据库文件路径。
 *
 * W829：允许用环境变量覆盖（默认不变·生产形态零变化）——E2E 必须跑在**临时库**上：
 * 原实现库路径写死 → E2E 的清理逻辑（按「最近更新的 session」删 feedback/messages/sessions）
 * 会删掉开发者真实会话（历史含工具结果·不可逆）。
 *
 * W934：路径解析从模块级常量改为**函数**——因为后端变成可创建的实例，
 * 同一进程内若要开第二个 SQLite 实例（契约测试用临时库）不能被模块级常量绑死。
 */
export function resolveSqlitePath(): string {
  return process.env.AGENT_WEB_DB_PATH
    ? path.resolve(process.env.AGENT_WEB_DB_PATH)
    : path.join(__dirname, "..", "..", "data", "chat.db");
}

/** SQLite 后端实例（现役 db.ts 的整体搬迁）。 */
export interface SqliteBackend extends StorageBackend {
  readonly kind: "sqlite";
  /** 解析后的库路径（备份层用它定位同一个库）。 */
  readonly path: string;
}

export function createSqliteBackend(dbPath?: string): SqliteBackend {
  const resolved = dbPath ? path.resolve(dbPath) : resolveSqlitePath();

  // 确保 data 目录存在
  const dataDir = path.dirname(resolved);
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }

  // 创建数据库连接
  const db: Database.Database = new Database(resolved);

  // 启用 WAL 模式以提高性能
  db.pragma("journal_mode = WAL");
  db.pragma("foreign_keys = ON"); // W917 B-DB-01：外键强制（此前 DDL 声明 FOREIGN KEY 但 pragma 从未开启·级联删除从未生效——W823 审查四 P0 之一）

  // 初始化数据库表
  db.exec(`
  -- 会话表
  CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    model TEXT NOT NULL,
    sdk_session_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
  );

  -- 消息表
  CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    model TEXT,
    created_at TEXT NOT NULL,
    tool_calls TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
  );

  -- 为会话 ID 创建索引
  CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id);

  -- 反馈表（W600 H2）
  CREATE TABLE IF NOT EXISTS feedback (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    message_id TEXT NOT NULL,
    verdict TEXT NOT NULL CHECK (verdict IN ('up', 'down')),
    comment TEXT,
    created_at TEXT NOT NULL
  );
  -- 同一消息唯一 verdict（W917 B-DB-01：维度由 (message_id, verdict) 收紧为 (message_id)——
  -- 原维度允许同一消息同时存在赞与踩两条互相矛盾的记录·W823 审查 P0 之三；改判走 upsert 覆盖）
  CREATE UNIQUE INDEX IF NOT EXISTS idx_feedback_message ON feedback(message_id);
`);

  // 迁移框架（W919 B-DB-04·W823 包四）：version 单调·事务内执行·user_version 记账。
  // 教训固化：改表定义对已存在的库无效（SQLite 无 ADD CONSTRAINT）——一切 schema 变更走本清单。
  // v1 吸收原手写迁移（sdk_session_id 列·try/catch 形态按 W823 判定为「静默吞错」反模式）。
  const MIGRATIONS: Array<{ version: number; up(d: import("better-sqlite3").Database): void }> = [
    {
      version: 1,
      up(d) {
        const tableInfo = d.prepare("PRAGMA table_info(sessions)").all() as Array<{ name: string }>;
        if (!tableInfo.some((col) => col.name === "sdk_session_id")) {
          d.exec("ALTER TABLE sessions ADD COLUMN sdk_session_id TEXT");
        }
      },
    },
    // v2（W919 B-DB-02 包二）：查询模式索引——纯性能·IF NOT EXISTS 幂等
    {
      version: 2,
      up(d) {
        d.exec(`
        CREATE INDEX IF NOT EXISTS idx_sessions_updated_at ON sessions(updated_at DESC);
        CREATE INDEX IF NOT EXISTS idx_messages_session_created ON messages(session_id, created_at);
        CREATE INDEX IF NOT EXISTS idx_feedback_created_at ON feedback(created_at);
        CREATE INDEX IF NOT EXISTS idx_feedback_session_id ON feedback(session_id);
      `);
      },
    },
    // v3（W919 B-DB-03 包三）：feedback 表重建——旧库补外键引用与 message_id 单维唯一
    // （新库 DDL 已含·本迁移对存量库生效；重建期外键必须 OFF·W823 §7.1 口径）
    {
      version: 3,
      up(d) {
        d.pragma("foreign_keys = OFF");
        d.exec(`
        CREATE TABLE feedback_new (
          id TEXT PRIMARY KEY,
          session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
          message_id TEXT NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
          verdict TEXT NOT NULL CHECK (verdict IN ('up','down')),
          comment TEXT,
          created_at TEXT NOT NULL CHECK (created_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]Z')
        );
        INSERT INTO feedback_new SELECT id, session_id, message_id, verdict, comment, created_at FROM feedback;
        DROP TABLE feedback;
        ALTER TABLE feedback_new RENAME TO feedback;
        CREATE UNIQUE INDEX IF NOT EXISTS idx_feedback_message ON feedback(message_id);
      `);
        d.pragma("foreign_keys = ON");
      },
    },
  ];
  function migrate(d: import("better-sqlite3").Database): void {
    const cur = d.pragma("user_version", { simple: true }) as unknown as number;
    for (const m of MIGRATIONS) {
      if (m.version > cur) {
        d.transaction(() => m.up(d))();
        d.pragma(`user_version = ${m.version}`);
      }
    }
  }
  migrate(db);

  const backend: SqliteBackend = {
    kind: "sqlite",
    path: resolved,

    // ============= 会话操作 =============

    // 获取所有会话
    // W919 B-DB-02：会话列表单 SQL 版（含 message_count 子查询·ORDER BY updated_at DESC·LIMIT）
    async listSessionsWithMessageCount(limit: number): Promise<Array<Record<string, unknown>>> {
      return db.prepare(`
    SELECT s.*, (SELECT COUNT(*) FROM messages m WHERE m.session_id = s.id) AS message_count, message_count AS messageCount
    FROM (SELECT s2.*, (SELECT COUNT(*) FROM messages m2 WHERE m2.session_id = s2.id) AS message_count FROM sessions s2 ORDER BY s2.updated_at DESC LIMIT ?) AS s
  `).all(limit) as Array<Record<string, unknown>>;
    },

    async getAllSessions(): Promise<DbSession[]> {
      const stmt = db.prepare("SELECT * FROM sessions ORDER BY updated_at DESC");
      return stmt.all() as DbSession[];
    },

    async getSession(id: string): Promise<DbSession | undefined> {
      const stmt = db.prepare("SELECT * FROM sessions WHERE id = ?");
      return stmt.get(id) as DbSession | undefined;
    },

    async createSession(session: DbSession): Promise<DbSession> {
      const stmt = db.prepare(`
    INSERT INTO sessions (id, title, model, sdk_session_id, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
  `);
      stmt.run(
        session.id,
        session.title,
        session.model,
        session.sdk_session_id,
        session.created_at,
        session.updated_at
      );
      return session;
    },

    async updateSession(id: string, updates: SessionUpdates): Promise<boolean> {
      const fields: string[] = [];
      const values: unknown[] = [];

      if (updates.title !== undefined) {
        fields.push("title = ?");
        values.push(updates.title);
      }
      if (updates.model !== undefined) {
        fields.push("model = ?");
        values.push(updates.model);
      }
      if (updates.sdk_session_id !== undefined) {
        fields.push("sdk_session_id = ?");
        values.push(updates.sdk_session_id);
      }

      if (fields.length === 0) return false;

      fields.push("updated_at = ?");
      values.push(new Date().toISOString());
      values.push(id);

      const stmt = db.prepare(`UPDATE sessions SET ${fields.join(", ")} WHERE id = ?`);
      const result = stmt.run(...values);
      return result.changes > 0;
    },

    async deleteSession(id: string): Promise<boolean> {
      const stmt = db.prepare("DELETE FROM sessions WHERE id = ?");
      const result = stmt.run(id);
      return result.changes > 0;
    },

    // ============= 消息操作 =============

    async getMessagesBySession(sessionId: string): Promise<DbMessage[]> {
      const stmt = db.prepare("SELECT * FROM messages WHERE session_id = ? ORDER BY created_at ASC");
      return stmt.all(sessionId) as DbMessage[];
    },

    async createMessage(message: DbMessage): Promise<DbMessage> {
      const stmt = db.prepare(`
    INSERT INTO messages (id, session_id, role, content, model, created_at, tool_calls)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `);
      stmt.run(
        message.id,
        message.session_id,
        message.role,
        message.content,
        message.model,
        message.created_at,
        message.tool_calls
      );

      // 更新会话的 updated_at
      const updateStmt = db.prepare("UPDATE sessions SET updated_at = ? WHERE id = ?");
      updateStmt.run(new Date().toISOString(), message.session_id);

      return message;
    },

    async updateMessage(id: string, updates: MessageUpdates): Promise<boolean> {
      const fields: string[] = [];
      const values: unknown[] = [];

      if (updates.content !== undefined) {
        fields.push("content = ?");
        values.push(updates.content);
      }
      if (updates.tool_calls !== undefined) {
        fields.push("tool_calls = ?");
        values.push(updates.tool_calls);
      }

      if (fields.length === 0) return false;

      values.push(id);

      const stmt = db.prepare(`UPDATE messages SET ${fields.join(", ")} WHERE id = ?`);
      const result = stmt.run(...values);
      return result.changes > 0;
    },

    async deleteMessage(id: string): Promise<boolean> {
      const stmt = db.prepare("DELETE FROM messages WHERE id = ?");
      const result = stmt.run(id);
      return result.changes > 0;
    },

    async createMessages(messages: DbMessage[]): Promise<void> {
      const stmt = db.prepare(`
    INSERT INTO messages (id, session_id, role, content, model, created_at, tool_calls)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `);

      const insertMany = db.transaction((msgs: DbMessage[]) => {
        for (const msg of msgs) {
          stmt.run(
            msg.id,
            msg.session_id,
            msg.role,
            msg.content,
            msg.model,
            msg.created_at,
            msg.tool_calls
          );
        }
      });

      insertMany(messages);
    },

    // ============= 反馈 =============

    async insertFeedback(f: Omit<DbFeedback, "created_at">): Promise<number> {
      const r = db
        .prepare(
          "INSERT INTO feedback (id, session_id, message_id, verdict, comment, created_at) VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(message_id) DO UPDATE SET verdict = excluded.verdict, comment = excluded.comment, created_at = excluded.created_at"
        )
        .run(f.id, f.session_id, f.message_id, f.verdict, f.comment ?? null, new Date().toISOString());
      return r.changes;
    },

    async feedbackSummary(days = 30): Promise<{ up: number; down: number }> {
      const since = new Date(Date.now() - days * 86400000).toISOString();
      const rows = db
        .prepare("SELECT verdict, COUNT(*) AS n FROM feedback WHERE created_at >= ? GROUP BY verdict")
        .all(since) as Array<{ verdict: string; n: number }>;
      return {
        up: rows.find((r) => r.verdict === "up")?.n ?? 0,
        down: rows.find((r) => r.verdict === "down")?.n ?? 0,
      };
    },

    // ============= 清库与关闭 =============

    // 清空所有数据
    async clearAllData(): Promise<void> {
      // W917 B-DB-01：清库须含 feedback（此前漏清——反馈表跨「清空全部」存活·W823 审查 P0 之二）；
      // 外键已强制，sessions 级联删 messages，三表按依赖序显式清理（幂等）
      db.exec("DELETE FROM feedback");
      db.exec("DELETE FROM messages");
      db.exec("DELETE FROM sessions");
    },

    async healthCheck(): Promise<StorageHealth> {
      try {
        const row = db.prepare("SELECT 1 AS ok").get() as { ok: number } | undefined;
        return row?.ok === 1
          ? { ok: true, detail: `sqlite 正常（${resolved}）` }
          : { ok: false, detail: "sqlite 探针返回异常" };
      } catch (err) {
        return { ok: false, detail: `sqlite 探针失败：${err instanceof Error ? err.message : String(err)}` };
      }
    },

    /**
     * 关闭数据库连接（W808 新增·优雅关闭用）。
     *
     * 语义：先做 WAL checkpoint（把 WAL 内容合并回主库）再关闭连接——
     * 否则进程退出时可能留下未 checkpoint 的 WAL 文件（下次启动能恢复，但文件滞留）。
     * 关闭后本实例的其它函数不可再调用（better-sqlite3 会抛「连接已关闭」）。
     */
    async close(): Promise<void> {
      try {
        if (db.open) {
          db.pragma("wal_checkpoint(TRUNCATE)");
          db.close();
        }
      } catch (e) {
        // 关闭失败不外抛——关闭路径上不应因清理异常而崩溃
        console.error(`[DB] 关闭连接失败: ${e instanceof Error ? e.message : String(e)}`);
      }
    },
  };

  return backend;
}
