/**
 * permissions.ts — 工具权限桥（W803-D 自 index.ts 提取·策略语义逐字保留）
 *
 * 职责边界：实现「工具名 + 权限模式 → allow/deny/询问前端」的决策，
 * 并负责权限请求的挂起登记与审计留痕。**不放行任何受保护路径**
 * （路径黑名单/允许域在 engine/tools.ts，本层只做模式级放行，两者叠加生效）。
 *
 * 四模式策略（与重构前 index.ts canUseTool 内联实现一致）：
 *   bypassPermissions（仅 AGENT_WEB_ALLOW_BYPASS=1 时经净化可达）→ 直接放行
 *   read 类工具                                                  → 各模式一律放行
 *   plan                                                         → 只读规划：写入与命令拒绝
 *   acceptEdits                                                  → 写面自动放行、命令仍询问
 *   default                                                      → 写面与命令均询问前端
 */
import { v4 as uuidv4 } from "uuid";
import { appendAudit, auditTarget } from "./audit.js";
import { logger } from "./logger.js";
import { TOOL_PERMISSION_KIND } from "./engine/tools.js";
import type { CanUseTool, PermissionDecision } from "./engine/types.js";
import type { PermissionMode } from "./security.js";
import { sendError } from "./http.js";
import type { PermissionRequestPayload } from "./sse.js";
import { PERMISSION_TIMEOUT, VERBOSE_LOG } from "./config.js";
import type { Response } from "express";

/** 待处理的权限请求（Promise 结算函数 + 展示用元数据）。 */
export interface PendingPermission {
  resolve: (result: PermissionDecision) => void;
  reject: (error: Error) => void;
  toolName: string;
  input: Record<string, unknown>;
  sessionId: string;
  timestamp: number;
}

/**
 * W536 安全加固：无原型对象存储（键经 safeKey 白名单防原型污染）。
 * 用独立容器而非模块级裸对象：便于 createPermissionBroker 的多实例隔离与测试注入。
 */
export interface PendingPermissionStore {
  map: Record<string, PendingPermission>;
  safeKey(k: unknown): string | null;
}

/** 建一个无原型 + 键白名单的挂起表（安全语义同 W536）。 */
export function createPendingPermissionStore(): PendingPermissionStore {
  return {
    map: Object.create(null) as Record<string, PendingPermission>,
    safeKey: (k: unknown): string | null =>
      typeof k === "string" && k !== "__proto__" && k !== "constructor" && k !== "prototype" ? k : null,
  };
}

/** 权限桥运行期依赖（结构化注入·便于单测与后续拆分）。 */
export interface PermissionBrokerDeps {
  sessionId: string;
  permissionMode: PermissionMode;
  store: PendingPermissionStore;
  /** 写出 permission_request 事件（由 chat 路由注入，保持本层不依赖 res）。 */
  emitPermissionRequest: (payload: PermissionRequestPayload) => void;
  /** W752：被拒绝的工具调用 id 集合——agent-loop 对拒绝回执 isError 恒 false，需借此区分「权限拒绝」与「执行成功」。 */
  deniedToolUseIds: Set<string>;
}

/**
 * 权限桥工厂：返回可直接交给 engine 的 canUseTool。
 * 审计留痕（W752）在决策阶段完成：写/命令面 allow 与 deny 都落；read 类自动放行不落（噪声大且非写面风险）。
 */
export function createPermissionBroker(deps: PermissionBrokerDeps): CanUseTool {
  const { sessionId, permissionMode, store, emitPermissionRequest, deniedToolUseIds } = deps;

  return async (toolName, input, options) => {
    logger.info("工具请求", { tool: toolName });
    if (VERBOSE_LOG) logger.debug("工具入参", { tool: toolName, input }); // P3-1

    const kind = TOOL_PERMISSION_KIND[toolName] ?? "command";
    const auditTargetInfo = auditTarget(input);

    const audited = (decision: PermissionDecision, reason: string): PermissionDecision => {
      if (kind === "read") return decision;
      if (decision.behavior === "deny") deniedToolUseIds.add(options.toolUseID);
      appendAudit({
        sessionId,
        tool: toolName,
        phase: "permission",
        decision: decision.behavior,
        kind,
        ...auditTargetInfo,
        reason: decision.message ?? reason,
      });
      return decision;
    };

    // bypassPermissions 模式直接放行（仅当 AGENT_WEB_ALLOW_BYPASS=1 时经净化可达）
    if (permissionMode === "bypassPermissions") {
      logger.warn("bypassPermissions 模式放行工具调用", { tool: toolName, session_id: sessionId });
      return audited({ behavior: "allow", updatedInput: input }, "bypassPermissions 模式放行");
    }

    if (kind === "read") return { behavior: "allow", updatedInput: input };
    if (permissionMode === "plan") {
      return audited({ behavior: "deny", message: "plan 模式为只读规划：写入与命令执行被拒绝" }, "plan 模式只读");
    }
    if (kind === "write" && permissionMode === "acceptEdits") {
      return audited({ behavior: "allow", updatedInput: input }, "acceptEdits 写面自动放行");
    }

    // default 的写操作与各模式（除 bypass）的命令执行 → 请求前端许可
    const requestId = uuidv4();
    emitPermissionRequest({
      requestId,
      toolUseId: options.toolUseID,
      toolName,
      input,
      sessionId,
      timestamp: Date.now(),
    });

    // 创建 Promise 等待用户响应
    return new Promise<PermissionDecision>((resolve, reject) => {
      // 前端许可（/api/permission-response 以单参调用）与超时两条出口都经 audited 留痕
      const settle = (decision: PermissionDecision, why = "前端许可决策") => resolve(audited(decision, why));
      const pending: PendingPermission = {
        resolve: settle,
        reject,
        toolName,
        input,
        sessionId,
        timestamp: Date.now(),
      };

      const reqKey = store.safeKey(requestId);
      if (reqKey) store.map[reqKey] = pending;

      // 设置超时
      setTimeout(() => {
        if (reqKey && store.map[reqKey] !== undefined) {
          delete store.map[reqKey];
          logger.warn("权限请求超时", { request_id: requestId, tool: toolName });
          settle({ behavior: "deny", message: "权限请求超时" }, "权限请求超时");
        }
      }, PERMISSION_TIMEOUT);
    });
  };
}

/**
 * 处理前端的权限响应（POST /api/permission-response）。
 * 行为逐字保留：请求不存在 → 404；允许 → 用挂起时的 input 原样回填 updatedInput；拒绝 → 用请求体 message 或默认文案。
 */
export function handlePermissionResponse(
  store: PendingPermissionStore,
  body: Record<string, unknown>,
  res: Response
): void {
  const requestId = body.requestId;
  const behavior = body.behavior;
  // 请求体非可信输入：message 按 string|undefined 使用（真值判定与重构前 `message || '用户拒绝了此操作'` 一致）
  const message = body.message as string | undefined;

  logger.info("收到权限回执", { request_id: requestId, behavior });

  const reqKey = store.safeKey(requestId);
  const pending = reqKey ? store.map[reqKey] : undefined;
  if (!pending) {
    logger.warn("权限请求不存在或已超时", { request_id: requestId });
    return sendError(res, 404, "权限请求不存在或已超时");
  }

  // 清除请求
  if (reqKey) delete store.map[reqKey];

  if (behavior === "allow") {
    pending.resolve({ behavior: "allow", updatedInput: pending.input });
  } else {
    pending.resolve({ behavior: "deny", message: message || "用户拒绝了此操作" });
  }

  res.json({ success: true });
}

/** 接口形状守卫：/api/permission-response 只在请求体是对象时取值（等价于原 `req.body || {}` 解构的健壮性）。 */
export function asRecord(value: unknown): Record<string, unknown> {
  return value !== null && typeof value === "object" ? (value as Record<string, unknown>) : {};
}
