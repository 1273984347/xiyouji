/**
 * index.ts — M12 存储层工厂（W934 · D-2a）
 *
 * 职责：按环境变量选出**唯一**活跃后端，并把 `StorageBackend` 契约的每个方法
 * 转发出去。调用方（`server/db.ts` 门面 → 业务代码）只认门面，不认后端。
 *
 * 后端选择口径（决策 D-07 / R-10）：
 *  - `AGENT_WEB_DB_BACKEND` 未设 ⇒ **sqlite**（现役行为逐字不变·本批是加法不是换法）；
 *  - `AGENT_WEB_DB_BACKEND=postgres` ⇒ 走 PG 后端；
 *  - 取值非法 ⇒ **启动失败并报错**，不静默回落 sqlite——
 *    静默回落会把「以为在用 PG、其实在用 SQLite」变成静默的口径漂移。
 *
 * 创建时机：模块加载时即创建（与现役 `db.ts` 的「import 即建库并跑迁移」时点一致）——
 * 集成测试与 E2E 都依赖这个时序（它们在起服后直接打开 SQLite 文件断言）。
 */
import { createSqliteBackend, resolveSqlitePath } from "./sqlite.js";
import { createPostgresBackend } from "./postgres.js";
import type {
  BackendKind,
  DbFeedback,
  DbMessage,
  DbSession,
  MessageUpdates,
  SessionUpdates,
  StorageBackend,
  StorageHealth,
} from "./types.js";

export type { BackendKind, StorageBackend, StorageHealth } from "./types.js";
// W934：DbSession / DbMessage / DbFeedback 是**接口（纯类型）**——必须用 `export type`。
//   写成值导出会在 ESM 运行时抛「does not provide an export named ...」，
//   而 `tsc` 在未开 isolatedModules 时**不会**报错 ⇒ 靠集成测试的实跑才暴露。
export type { DbSession, DbMessage, DbFeedback } from "./types.js";

/**
 * 解析后端种类。
 *
 * 非法取值 ⇒ 抛错（fail-closed）。这是有意的：**「配错了却跑起来了」比「起不来」危险**。
 */
export function resolveBackendKind(): BackendKind {
  const raw = (process.env.AGENT_WEB_DB_BACKEND || "").trim().toLowerCase();
  if (raw === "" || raw === "sqlite") return "sqlite";
  if (raw === "postgres" || raw === "postgresql" || raw === "pg") return "postgres";
  throw new Error(
    `AGENT_WEB_DB_BACKEND 取值非法：${JSON.stringify(raw)}（允许 sqlite | postgres）`
  );
}

/** 活跃后端（模块加载时创建·单例）。 */
export const backend: StorageBackend = (() => {
  const kind = resolveBackendKind();
  return kind === "postgres" ? createPostgresBackend() : createSqliteBackend();
})();

/** 活跃后端种类（运行时可查·用于日志与断言）。 */
export function backendKind(): BackendKind {
  return backend.kind;
}

// ============= 契约转发 =============
// 逐个显式转发而不是 `export const x = backend.x.bind(backend)`：
// 显式写法在 IDE 与 grep 里都能看出「这层是转发」，且类型由 StorageBackend 契约把关。

export async function listSessionsWithMessageCount(
  limit: number
): Promise<Array<Record<string, unknown>>> {
  return backend.listSessionsWithMessageCount(limit);
}

export async function getAllSessions(): Promise<DbSession[]> {
  return backend.getAllSessions();
}

export async function getSession(id: string): Promise<DbSession | undefined> {
  return backend.getSession(id);
}

export async function createSession(session: DbSession): Promise<DbSession> {
  return backend.createSession(session);
}

export async function updateSession(id: string, updates: SessionUpdates): Promise<boolean> {
  return backend.updateSession(id, updates);
}

export async function deleteSession(id: string): Promise<boolean> {
  return backend.deleteSession(id);
}

export async function getMessagesBySession(sessionId: string): Promise<DbMessage[]> {
  return backend.getMessagesBySession(sessionId);
}

export async function createMessage(message: DbMessage): Promise<DbMessage> {
  return backend.createMessage(message);
}

export async function updateMessage(id: string, updates: MessageUpdates): Promise<boolean> {
  return backend.updateMessage(id, updates);
}

export async function deleteMessage(id: string): Promise<boolean> {
  return backend.deleteMessage(id);
}

export async function createMessages(messages: DbMessage[]): Promise<void> {
  return backend.createMessages(messages);
}

export async function insertFeedback(feedback: Omit<DbFeedback, "created_at">): Promise<number> {
  return backend.insertFeedback(feedback);
}

export async function feedbackSummary(days = 30): Promise<{ up: number; down: number }> {
  return backend.feedbackSummary(days);
}

export async function clearAllData(): Promise<void> {
  return backend.clearAllData();
}

export async function healthCheck(): Promise<StorageHealth> {
  return backend.healthCheck();
}

export async function closeDatabase(): Promise<void> {
  return backend.close();
}

/**
 * SQLite 库路径（备份层用它定位「同一个库」）。
 *
 * 非 SQLite 后端下该值**仍然指向 SQLite 的默认路径**——它是一个**配置事实**
 * （「若用 SQLite，库在哪」），不是「当前活跃库的路径」。备份层据此判断
 * 是否要做文件级快照：PG 后端不做（PG 走 `pg_basebackup` + PITR，见 deploy/pg/）。
 */
export function databasePath(): string {
  // 动态解析而非模块级常量：契约测试要在同一进程里开临时库实例
  return resolveSqlitePath();
}
