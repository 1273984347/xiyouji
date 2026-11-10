/**
 * dualwrite.ts — 存储层双写后端（W1203 · 架构方案 v2 §8.2 档 2 · D-2 第二子批）
 *
 * 目的：让「切读」与「停写旧库」这两个动作**可回滚**。切读前必须有一段
 * 「两侧同时写」的时期；没有双写就无法在切读后证明旧库没落后，也就无法安全停写。
 *
 * 语义约定（与 types.ts 的接口契约逐条对应）：
 *  - **读只走主库**：双写期的读侧行为必须与切读后完全一致 ⇒ 读不能有两套语义。
 *  - **写两侧**：先主后副；副库写失败 ⇒ **抛错（fail-closed）**。
 *    宁可停写（可恢复），也不可「以为写成功了其实只写了一半」。
 *    主库已写而副库失败的窗口由**对账器**负责修复（下一批）。
 *  - **返回主库结果**：行数 / rowid / 命中与否一律以主库为准；副库 rowid 独立，
 *    不参与对外契约。
 *  - **kind 沿用主库**：不扩 BackendKind 枚举 ⇒ 既有断言与调用点零改动。
 *
 * 与 D-2a 的关系：D-2a 交付的是「换后端不动业务」的抽象层与一次性迁移；
 * 本件是抽象层之上的**运行期双写**——两者共用同一套 StorageBackend 契约。
 */
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

/**
 * 本次写入的**权威时间**（一次生成·两侧同传）。
 *
 * 为什么必须显式生成（types.ts 的 WriteTimeOpts 头注有完整背景）：写路径上
 * `updateSession` / `createMessage` / `insertFeedback` 的时间戳由**后端**生成 ⇒
 * 双写期两侧各生成一次 ⇒ 两个副本差几毫秒 ⇒ 对账判「内容不等」⇒ 切读被永久阻断。
 */
function writeTimeOpts(): WriteTimeOpts {
  return { now: new Date().toISOString() };
}

/** 双写态的运行时可查信息（供日志与断言；不并入 StorageBackend 契约以免扩枚举）。 */
export interface DualWriteState {
  /** 主库种类（sqlite | postgres）。 */
  primary: StorageBackend["kind"];
  /** 副库种类。 */
  secondary: StorageBackend["kind"];
  /** 副库最后是否健康（仅反映最近一次 healthCheck）。 */
  secondaryHealthy: boolean | null;
}

/**
 * 造一个双写后端：写两侧、读主库。
 *
 * @param primary  主库（读侧与返回值的权威）
 * @param secondary 副库（双写目标）
 */
export function createDualWriteBackend(
  primary: StorageBackend,
  secondary: StorageBackend,
): StorageBackend & { dualWriteState(): DualWriteState } {
  const state: DualWriteState = {
    primary: primary.kind,
    secondary: secondary.kind,
    secondaryHealthy: null,
  };

  /** 副库写：失败即抛（fail-closed）——不吞、不降级。 */
  async function mirrorWrite(fn: () => Promise<unknown>): Promise<void> {
    try {
      await fn();
      state.secondaryHealthy = true;
    } catch (err) {
      state.secondaryHealthy = false;
      throw err;
    }
  }

  return {
    kind: primary.kind,
    dualWriteState: () => ({ ...state }),

    // ---------- 读：只走主库 ----------
    async listSessionsWithMessageCount(limit: number) {
      return primary.listSessionsWithMessageCount(limit);
    },
    async getAllSessions() {
      return primary.getAllSessions();
    },
    async getSession(id: string) {
      return primary.getSession(id);
    },
    async getMessagesBySession(sessionId: string) {
      return primary.getMessagesBySession(sessionId);
    },
    async feedbackSummary(days?: number) {
      return primary.feedbackSummary(days);
    },

    // ---------- 写：主库 + 副库 ----------
    async createSession(session: DbSession) {
      const created = await primary.createSession(session);
      await mirrorWrite(() => secondary.createSession(session));
      return created;
    },
    async updateSession(id: string, updates: SessionUpdates) {
      // W1204 实测修根：本次写入的权威时间**一次生成·两侧同传**
      //   （否则两侧各取当前时间 ⇒ updated_at 差几毫秒 ⇒ 对账判「内容不等」⇒ 切读被永久阻断）
      const opts = writeTimeOpts();
      const hit = await primary.updateSession(id, updates, opts);
      // 主库未命中 ⇒ 两侧都不动（保持「未命中」语义一致）
      if (hit) await mirrorWrite(() => secondary.updateSession(id, updates, opts));
      return hit;
    },
    async deleteSession(id: string) {
      const hit = await primary.deleteSession(id);
      if (hit) await mirrorWrite(() => secondary.deleteSession(id));
      return hit;
    },
    async createMessage(message: DbMessage) {
      // W1204 实测修根：会话 updated_at 由**后端**刷 ⇒ 权威时间必须两侧同传（同上）
      const opts = writeTimeOpts();
      const created = await primary.createMessage(message, opts);
      await mirrorWrite(() => secondary.createMessage(message, opts));
      return created;
    },
    async updateMessage(id: string, updates: MessageUpdates) {
      const hit = await primary.updateMessage(id, updates);
      if (hit) await mirrorWrite(() => secondary.updateMessage(id, updates));
      return hit;
    },
    async deleteMessage(id: string) {
      const hit = await primary.deleteMessage(id);
      if (hit) await mirrorWrite(() => secondary.deleteMessage(id));
      return hit;
    },
    async createMessages(messages: DbMessage[]) {
      await primary.createMessages(messages);
      await mirrorWrite(() => secondary.createMessages(messages));
    },
    async insertFeedback(feedback: Omit<DbFeedback, "created_at">) {
      // W1204 实测修根：feedback.created_at 由**后端**生成 ⇒ 权威时间必须两侧同传（同上）
      const opts = writeTimeOpts();
      const rowId = await primary.insertFeedback(feedback, opts);
      await mirrorWrite(() => secondary.insertFeedback(feedback, opts));
      return rowId;
    },

    // ---------- 运维 ----------
    async clearAllData() {
      await primary.clearAllData();
      await mirrorWrite(() => secondary.clearAllData());
    },
    async healthCheck(): Promise<StorageHealth> {
      const health = await primary.healthCheck();
      try {
        const secondaryHealth = await secondary.healthCheck();
        state.secondaryHealthy = Boolean(secondaryHealth?.ok);
      } catch {
        state.secondaryHealthy = false;
      }
      return health;
    },
    async close() {
      // 两侧都要关：副库先关（它是影子），主库后关（业务仍在读它）
      try {
        await secondary.close();
      } finally {
        await primary.close();
      }
    },
  };
}
