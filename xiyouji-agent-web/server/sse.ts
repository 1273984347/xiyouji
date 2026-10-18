/**
 * sse.ts — SSE 事件构造层（W803-D 自 index.ts 提取·事件名与数据形态逐字保留）
 *
 * 职责边界：把「领域事件」翻译成前端契约里的 SSE 帧字符串并写出。
 * **只做序列化与写出，不含任何业务判断**（谁该发什么由 chat 路由决定）。
 *
 * 契约红线（前端 useChat 按 type 分派，改名/改字段即破坏流式渲染）：
 *   事件名：init | text | tool | tool_result | citation_guard | done | error | permission_request
 *   帧格式：`data: <JSON>\n\n`（无 event: 行、无 id: 行——前端只切 `data: ` 前缀）
 *   字段顺序：JSON.stringify 的键序即帧字节序，本层按重构前字面量顺序书写。
 */
import type { Response } from "express";

/** GET /api/chat 的流式头（补丁在 SSE 之外的路由返回 JSON，故由本层统一设置）。 */
export function setSseHeaders(res: Response): void {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");
}

/** 权限请求载荷（先于 SSE 事件构造，用于登记 pendingPermissions）。 */
export interface PermissionRequestPayload {
  requestId: string;
  toolUseId: string;
  toolName: string;
  input: Record<string, unknown>;
  sessionId: string;
  timestamp: number;
}

/**
 * SSE 写出器：每个方法对应一个前端已消费的事件类型。
 * 之所以做成「对象而非散函数」：原 index.ts 在四处裸写 `res.write(...)`，
 * 字段拼装散落在 handler 与循环里；集中后事件形态可一眼比对。
 */
export interface SseWriter {
  /** 首事件：会话与消息 ID 落定（前端据此把临时 ID 换成真实 ID）。 */
  init(payload: { sessionId: string; userMessageId: string; assistantMessageId: string; model: string }): void;
  /** 文本增量。 */
  text(content: string): void;
  /** 工具开始执行。 */
  tool(call: { id: string; name: string; input: Record<string, unknown> | undefined }): void;
  /** 工具结果（isError 缺省＝undefined → 该键不出现，与重构前兜底分支一致）。 */
  toolResult(payload: { toolId: string; content: string; isError?: boolean }): void;
  /** W599 引用校验回写：最终文本块以校验结果为准。 */
  citationGuard(payload: { text: string; unverified: string[] }): void;
  /** 收尾事件（duration 为引擎耗时毫秒）。 */
  done(duration: number): void;
  /** 错误事件（前端据此把「思考中…」置为错误文案）。 */
  error(message: string): void;
  /** 工具权限请求（前端弹内联许可卡）。 */
  permissionRequest(payload: PermissionRequestPayload): void;
}

/** 构造写出器：所有帧统一走 `data: <JSON>\n\n`。 */
export function createSseWriter(res: Response): SseWriter {
  const send = (payload: Record<string, unknown>): void => {
    res.write(`data: ${JSON.stringify(payload)}\n\n`);
  };

  return {
    init(payload) {
      send({
        type: "init",
        sessionId: payload.sessionId,
        userMessageId: payload.userMessageId,
        assistantMessageId: payload.assistantMessageId,
        model: payload.model,
      });
    },
    text(content) {
      send({ type: "text", content });
    },
    tool(call) {
      send({ type: "tool", id: call.id, name: call.name, input: call.input, status: "running" });
    },
    toolResult(payload) {
      // isError 为 undefined 时不写该键（重构前兜底分支的帧形态即 `{type,toolId,content}`）
      send(
        payload.isError === undefined
          ? { type: "tool_result", toolId: payload.toolId, content: payload.content }
          : { type: "tool_result", toolId: payload.toolId, content: payload.content, isError: payload.isError }
      );
    },
    citationGuard(payload) {
      send({ type: "citation_guard", text: payload.text, unverified: payload.unverified });
    },
    done(duration) {
      send({ type: "done", duration });
    },
    error(message) {
      send({ type: "error", message });
    },
    permissionRequest(payload) {
      send({
        type: "permission_request",
        requestId: payload.requestId,
        toolUseId: payload.toolUseId,
        toolName: payload.toolName,
        input: payload.input,
        sessionId: payload.sessionId,
        timestamp: payload.timestamp,
      });
    },
  };
}
