/**
 * types.ts — M12 存储层抽象：接口与数据契约（W934 · 架构方案 v2 §8.2 档 2 · D-2a）
 *
 * 为什么有这一层（方案 §8.2 表「存储后端切换 → M12 抽象隔离 PG 与 SQLite」）：
 * 档 2 把存储从 SQLite 换成 PostgreSQL 16 自建单机。若不抽象，切换会同时改写
 * **所有**调用点的 SQL 语义；有了抽象，切换只影响「选哪个后端」这一件事。
 *
 * **为什么接口是异步的**（这是一个会改变调用点形态的决定，不是随手选的）：
 * SQLite 走 better-sqlite3 是同步 API，PG 走网络协议——Node 的 socket 只有异步
 * 接口，**不存在**同步的 PG 驱动。若把接口定成同步，PG 后端就只能是假的
 * （只能靠内存镜像或阻塞式自研协议栈）。因此接口统一定为异步：
 * SQLite 后端的实现体仍是同步的（better-sqlite3 调用原样保留），
 * 只是包在 async 函数里；调用点多一个 `await`。
 *
 * 代价与收益（决策 D-10）：调用点形态变化（3 个文件加 `await` / `async`），
 * 换来「换后端不动业务逻辑」与「契约测试可对两个后端跑同一套用例」。
 *
 * 时间列契约（决策 D-03 / ASM-15 / ASM-16）：
 * 接口层一律用 **ISO-8601 UTC 毫秒精度字符串**（`2026-10-25T08:00:00.000Z`），
 * 与现役 SQLite 的 `new Date().toISOString()` 形态**逐字节一致**。
 * PG 侧列类型用 `TIMESTAMPTZ`（原生日期算术，服务 §7.4 生命周期 7 阶段需要），
 * 边界处显式转换 ⇒ 应用契约不变，存储又能用原生日期类型。
 */

/** 存储后端种类。 */
export type BackendKind = "sqlite" | "postgres";

/** 会话行（与现役 SQLite `sessions` 表同构）。 */
export interface DbSession {
  id: string;
  title: string;
  model: string;
  sdk_session_id: string | null;
  /** ISO-8601 UTC 毫秒精度字符串。 */
  created_at: string;
  /** ISO-8601 UTC 毫秒精度字符串。 */
  updated_at: string;
}

/** 消息行（与现役 SQLite `messages` 表同构）。 */
export interface DbMessage {
  id: string;
  session_id: string;
  role: "user" | "assistant";
  content: string;
  model: string | null;
  /** ISO-8601 UTC 毫秒精度字符串。 */
  created_at: string;
  /** JSON 字符串或 null（与现役一致，不做结构化解析）。 */
  tool_calls: string | null;
}

/** 反馈行（与现役 SQLite `feedback` 表同构）。 */
export interface DbFeedback {
  id: string;
  session_id: string;
  message_id: string;
  verdict: string;
  comment: string | null;
  /** ISO-8601 UTC 毫秒精度字符串。 */
  created_at: string;
}

/** 可更新字段集合（与现役函数签名一致）。 */
export type SessionUpdates = Partial<Pick<DbSession, "title" | "model" | "sdk_session_id">>;
export type MessageUpdates = Partial<Pick<DbMessage, "content" | "tool_calls">>;

/** 健康探针结果（方案 §5.1 M12「健康探针」）。 */
export interface StorageHealth {
  ok: boolean;
  /** 人类可读的判定依据（禁含口令 / 连接串）。 */
  detail: string;
}

/**
 * 存储后端契约。
 *
 * 方法集 = 现役 `server/db.ts` 的全部业务导出（12 个调用面函数）
 * ∪ 抽象层新增的 `kind` / `healthCheck` / `close`。
 *
 * 语义约定（两个后端必须一致，由 `storage.test.ts` 契约测试逐条守住）：
 *  1. `createSession` / `createMessage` 返回**入参对象本身**（与现役一致）。
 *  2. `updateSession` / `updateMessage` 返回**是否命中行**（0 行 ⇒ false）。
 *  3. `insertFeedback` 命中 `message_id` 唯一约束时**覆盖**旧 verdict（upsert），
 *     返回受影响行数。
 *  4. `deleteSession` 级联删除其 messages 与 feedback（外键级联）。
 *  5. `clearAllData` 按 `feedback → messages → sessions` 依赖序清空（幂等）。
 *  6. `feedbackSummary(days)` 只统计 `created_at` 在窗口内的行。
 *  7. 所有 SQL **禁字符串拼接**——全部走参数化查询。
 */
export interface StorageBackend {
  /** 后端种类（运行时可查，用于日志与断言）。 */
  readonly kind: BackendKind;

  /** 会话列表（含 message_count / messageCount 两个别名列，与现役一致）。 */
  listSessionsWithMessageCount(limit: number): Promise<Array<Record<string, unknown>>>;

  /** 全部会话（按 updated_at 倒序）。 */
  getAllSessions(): Promise<DbSession[]>;

  /** 单个会话（不存在 ⇒ undefined）。 */
  getSession(id: string): Promise<DbSession | undefined>;

  /** 创建会话。 */
  createSession(session: DbSession): Promise<DbSession>;

  /** 更新会话（不存在 ⇒ false）。 */
  updateSession(id: string, updates: SessionUpdates): Promise<boolean>;

  /** 删除会话（级联删 messages / feedback）。 */
  deleteSession(id: string): Promise<boolean>;

  /** 会话的全部消息（按 created_at 升序）。 */
  getMessagesBySession(sessionId: string): Promise<DbMessage[]>;

  /** 创建消息（并更新所属会话的 updated_at）。 */
  createMessage(message: DbMessage): Promise<DbMessage>;

  /** 更新消息（不存在 ⇒ false）。 */
  updateMessage(id: string, updates: MessageUpdates): Promise<boolean>;

  /** 删除消息。 */
  deleteMessage(id: string): Promise<boolean>;

  /** 批量创建消息（单事务）。 */
  createMessages(messages: DbMessage[]): Promise<void>;

  /** 写入反馈（同 message_id 覆盖）。 */
  insertFeedback(feedback: Omit<DbFeedback, "created_at">): Promise<number>;

  /** 反馈汇总（窗口内 up / down 计数）。 */
  feedbackSummary(days?: number): Promise<{ up: number; down: number }>;

  /** 清空全部业务数据（幂等）。 */
  clearAllData(): Promise<void>;

  /** 健康探针。 */
  healthCheck(): Promise<StorageHealth>;

  /** 关闭底层连接（SQLite：WAL checkpoint + close；PG：池关闭）。 */
  close(): Promise<void>;
}
