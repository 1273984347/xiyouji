/**
 * db.ts — 存储门面（W934 · D-2a · M12 存储层抽象）
 *
 * **本文件在 W934 之前是「SQLite 实现本体」**（建表 DDL + 3 版迁移 + 12 个业务函数）。
 * W934 起它**降为门面**：真正的实现搬进 `server/storage/`，这里只做转发。
 *
 * 为什么要门面化而不是直接改调用点（决策 D-02）：
 *  1. **导出名保持不变** ⇒ 现役调用方（`chat.ts` / `routes.ts` / `index.ts`）的
 *     import 语句一个字都不用改 ⇒ 现役行为与既有测试面完全不受影响；
 *  2. 后端切换（SQLite ↔ PG）收敛到 `server/storage/index.ts` 一处；
 *  3. 「当前用的是哪个后端」从此有唯一答案（`backendKind()`），
 *     而不是散落在各文件里的隐式假设。
 *
 * 抽象层带来的**唯一行为差异**：本文件导出的业务函数由**同步**变为**异步**
 * （PG 是网络库，Node 无同步 PG 驱动——见 `server/storage/types.ts` 头注）。
 * SQLite 后端的实现体仍是同步的 better-sqlite3 调用，未引入并发模型变化。
 *
 * 默认后端**仍是 SQLite**（`AGENT_WEB_DB_BACKEND` 未设即 sqlite）⇒
 * 本批是**加法不是换法**；切读与停写旧库属 W935 批。
 */

export {
  // 会话
  listSessionsWithMessageCount,
  getAllSessions,
  getSession,
  createSession,
  updateSession,
  deleteSession,
  // 消息
  getMessagesBySession,
  createMessage,
  updateMessage,
  deleteMessage,
  createMessages,
  // 反馈
  insertFeedback,
  feedbackSummary,
  // 运维
  clearAllData,
  closeDatabase,
  databasePath,
  // 抽象层新增（诊断与门禁用）
  backendKind,
  healthCheck,
} from "./storage/index.js";

export type {
  BackendKind,
  DbFeedback,
  DbMessage,
  DbSession,
  StorageBackend,
  StorageHealth,
} from "./storage/types.js";

import { backend } from "./storage/index.js";

/**
 * 默认导出 = **当前活跃的后端实例**。
 *
 * 语义变化（仓内消费者 0 处·grep 实证）：W934 之前默认导出是 better-sqlite3 的
 * 裸句柄；现在改为 `StorageBackend`——裸句柄在多后端下没有意义，
 * 而「当前后端」才是调用方真正可能想要的东西。
 */
export default backend;
