/**
 * chat.ts — POST /api/chat 流式编排（W803-D 自 index.ts 拆分）
 *
 * 职责边界：本模块是**唯一写 SSE 的路由**，负责把「请求校验 → 会话落库 → 引擎主循环 →
 * 流式事件 → 引用校验 → 助手消息落库」串成一条链路。事件构造在 sse.ts、权限决策在
 * permissions.ts、路径钳制在 security.ts——本层只做编排与状态跟踪。
 *
 * 契约红线（前端 useChat 逐帧消费，任何一处改动都等价于改了对外接口）：
 *   校验顺序：请求日志 → 空消息 400 → 引擎未配置 400 → 建会话 → 存用户消息 500 → 开 SSE；
 *   事件序：init → (tool | tool_result | text | permission_request)* → citation_guard? → done | error；
 *   两个 400/500 都在 SSE 之前以 JSON 返回（前端按 `response.body` 仍可读，但我们保持原状不推广）。
 */
import express from "express";
import { v4 as uuidv4 } from "uuid";
import type { Request, Response } from "express";
import type { z } from "zod";
import * as db from "./db.js";
import { applyCitationGuard } from "./citationGuard.js";
import { runAgentTurn } from "./engine/agent-loop.js";
import { createToolset, TOOL_PERMISSION_KIND } from "./engine/tools.js";
import { appendAudit, auditTarget } from "./audit.js";
import type { ChatMessage } from "./engine/types.js";
import { sanitizePermissionMode, resolveWorkingDir, createSseGuard } from "./security.js";
import { sendError } from "./http.js";
import { logger } from "./logger.js";
import { recordFirstToken } from "./metrics.js";
import { chatBodySchema, parseBody } from "./validation.js";
import { createSseWriter, setSseHeaders } from "./sse.js";
import {
  createPermissionBroker,
  type PendingPermissionStore,
} from "./permissions.js";
import {
  ALLOW_BYPASS,
  DEFAULT_SYSTEM_PROMPT,
  LLM_API_BASE,
  LLM_API_KEY,
  LLM_MAX_TURNS,
  PROJECT_CWD,
  VERBOSE_LOG,
  defaultModel,
  engineConfigured,
} from "./config.js";

/** 会话内展示用工具调用轨迹（与前端 ToolCall 同构；直接序列化进 messages.tool_calls）。 */
interface TrailToolCall {
  id: string;
  name: string;
  input?: Record<string, unknown>;
  status: string;
  result?: string;
  isError?: boolean;
}

/** 从 SQLite 重建本轮消息序列（W680：替代 SDK resume）。 */
function rebuildHistory(sessionId: string): ChatMessage[] {
  const rows = db.getMessagesBySession(sessionId);
  const history: ChatMessage[] = [];
  for (const m of rows.slice(-21)) { // 最近 20 条 + 本轮 user 消息，控 token 上限
    if (m.role === "user" && m.content) history.push({ role: "user", content: m.content });
    else if (m.role === "assistant" && m.content) history.push({ role: "assistant", content: m.content });
  }
  return history;
}

/** 首条消息的会话标题口径（建会话与「首轮后回填标题」两处共用）。 */
function titleFromMessage(message: string): string {
  return message.slice(0, 30) + (message.length > 30 ? "..." : "");
}

/**
 * 工具结果阶段的审计留痕（W752）：工具层拒绝（受保护路径/越界/白名单/允许域，tools.ts 抛出即 isError）
 * 与权限拒绝（deniedToolUseIds）统一记 deny + 原因；成功记 allow。审计自身 fail-open，不影响 SSE。
 */
function auditToolResult(params: {
  sessionId: string;
  tool: TrailToolCall;
  toolId: string;
  content: string;
  isError: boolean;
  deniedToolUseIds: Set<string>;
}): void {
  const { sessionId, tool, toolId, content, isError, deniedToolUseIds } = params;
  const wasDenied = deniedToolUseIds.has(toolId);
  const target = auditTarget(tool.input);
  appendAudit({
    sessionId,
    tool: tool.name,
    phase: "result",
    decision: wasDenied || isError ? "deny" : "allow",
    kind: TOOL_PERMISSION_KIND[tool.name] ?? "command",
    ...target,
    bytes: target.bytes ?? Buffer.byteLength(content ?? "", "utf8"),
    isError,
    reason: wasDenied ? `权限拒绝：${content}` : isError ? content : "执行成功",
  });
}

/**
 * 注册 POST /api/chat。
 * permissions 为进程级挂起表（与 /api/permission-response 共享同一实例）。
 */
export function registerChatRoute(app: express.Express, permissions: PendingPermissionStore): void {
  app.post("/api/chat", async (req: Request, res: Response) => {
    // W844：OBS-14 计时起点。取在 handler 最前——入参校验、会话读写都属「用户等待」的一部分，
    // 从更靠后开始计时会系统性低估首 token 延迟。
    const reqStartedAt = Date.now();
    let firstTokenMs: number | null = null;

    // W808：入参经 Zod 边界校验（server/validation.ts）。
    // 契约红线：**「消息为空」仍返 400 +「消息不能为空」**（既有契约逐字保留·
    // 本路由在 SSE 之前以 JSON 返回，前端按 response.body 读——状态码不可改）。
    // 其余字段（cwd / permissionMode）只做**类型**校验，语义净化仍归
    // server/security.ts 的 resolveWorkingDir 与 sanitizePermissionMode（两处规则不重复实现）。
    const raw = (req.body ?? {}) as Record<string, unknown>;

    // ① 消息为空——单独判定，保留既有契约的逐字文案（其余字段是否合法与本条无关）
    if (typeof raw.message !== "string" || raw.message.length === 0) {
      logger.warn("聊天请求消息为空", { request_id: req.requestId });
      return sendError(res, 400, "消息不能为空");
    }

    // ② 其余字段的形状校验（失败文案与①区分，避免「model 非法」也被报成「消息不能为空」）
    let body: z.infer<typeof chatBodySchema>;
    try {
      body = parseBody(chatBodySchema, raw);
    } catch (err) {
      logger.warn("聊天请求入参非法", {
        request_id: req.requestId,
        error: err instanceof Error ? err.message : String(err),
      });
      return sendError(res, 400, "请求参数不合法");
    }

    const { sessionId, message, model, systemPrompt, cwd, permissionMode } = body;

    // P0-1 修复：工作目录仅允许 PROJECT_CWD 内 + 权限模式白名单净化（不信任请求体原值）
    // P0-1 + W536 安全加固：工作目录钳制（realpath 规范化后仅允许 PROJECT_CWD 内，非法输入回落默认）
    // 提取至 server/security.ts（W791 BL-29·逻辑逐字保留）
    const workingDir = resolveWorkingDir(cwd, PROJECT_CWD);
    const effectivePermissionMode = sanitizePermissionMode(permissionMode, ALLOW_BYPASS);

    // 请求日志（W808：改走结构化日志·request ID 贯穿·凭证字段自动脱敏）
    logger.info("聊天请求", {
      request_id: req.requestId,
      session_id: sessionId ?? null,
      model: model ?? null,
      message_preview: message.slice(0, 100),
      cwd: cwd || "default",
    });

    // W680：引擎未配置时快速失败（400 JSON，不进 SSE 流）
    if (!engineConfigured()) {
      return sendError(res, 400, "引擎未配置：请在服务端 .env 设置 LLM_API_BASE / LLM_API_KEY / LLM_MODEL 后重启生效");
    }

    // 获取或创建会话
    let session = sessionId ? db.getSession(sessionId) : null;
    const now = new Date().toISOString();

    if (!session) {
      // 创建新会话
      logger.info("创建新会话", { request_id: req.requestId, session_id: sessionId ?? null });
      session = db.createSession({
        id: sessionId || uuidv4(),
        title: titleFromMessage(message),
        model: model || defaultModel,
        sdk_session_id: null, // W680：SDK resume 退役，历史从 SQLite 重建
        created_at: now,
        updated_at: now,
      });
    } else {
      logger.info("使用现有会话", { request_id: req.requestId, session_id: session.id });
    }

    const selectedModel = model || session.model;

    // 创建用户消息 ID 和助手消息 ID
    const userMessageId = uuidv4();
    const assistantMessageId = uuidv4();

    // 保存用户消息到数据库
    try {
      db.createMessage({
        id: userMessageId,
        session_id: session.id,
        role: "user",
        content: message,
        model: null,
        created_at: now,
        tool_calls: null,
      });
      logger.info("用户消息已保存", { request_id: req.requestId, message_id: userMessageId });
    } catch (dbError) {
      logger.error("保存用户消息失败", {
        request_id: req.requestId,
        error: dbError instanceof Error ? dbError.message : String(dbError),
      });
      // W829：不回显底层异常原文（SQLite 错误含库文件绝对路径等内部信息）——
      // 形状不变（detail 字段仍在），取值换固定文案；原文已在上面的 logger 里。
      return sendError(res, 500, "保存消息失败", { detail: "数据库写入失败" });
    }

    // 设置 SSE 头（事件帧格式见 sse.ts）
    setSseHeaders(res);
    const sse = createSseWriter(res);

    // P2-3 修复：SSE 断开清理 + 总时长上限（防客户端断开后流继续运行、pending 权限请求悬挂）
    // 守卫提取至 server/security.ts（W791 BL-29·逻辑逐字保留·maxMs 可注入供测试）
    const sseGuard = createSseGuard({ res, sessionId: session.id, pendingPermissions: permissions.map });
    const abortStream = sseGuard.abortStream;
    // W568 修复：Express 5 / Node 20+ 下 req 的 'close' 在「请求体读取完毕」即触发（并非连接断开），
    // abortStream 会立刻 res.end() 吞掉后续全部 SSE 事件（实证：init 之后 error 事件整段丢失）。
    // 改挂 res 'close'——仅在客户端提前断开或响应正常完成时触发；完成态重复 res.end() 为无害空操作。
    res.on("close", abortStream);

    try {
      logger.info("调用引擎", {
        request_id: req.requestId,
        model: selectedModel,
        cwd: workingDir,
        permission_mode: effectivePermissionMode,
      });

      // 会话历史（W680：从 SQLite 重建，替代 SDK resume——消息表已存全量 user/assistant 文本）
      const history = rebuildHistory(session.id);
      const toolset = createToolset(workingDir);
      // W752：被权限桥拒绝的工具调用 id——agent-loop 对拒绝回执的 isError 恒为 false，
      // 故工具结果处需借此区分「权限拒绝（根本没执行）」与「执行成功」（见 auditToolResult）。
      const deniedToolUseIds = new Set<string>();

      // 工具权限桥（策略：bypass 直通 / read 类放行 / plan 只读 / acceptEdits 放行写 / 其余走前端许可）
      const canUseTool = createPermissionBroker({
        sessionId: session.id,
        permissionMode: effectivePermissionMode,
        store: permissions,
        emitPermissionRequest: (payload) => sse.permissionRequest(payload),
        deniedToolUseIds,
      });

      // 发送会话ID和消息ID（引擎启动前，SSE 事件序契约第一事件）
      sse.init({ sessionId: session.id, userMessageId, assistantMessageId, model: selectedModel });

      const toolCalls: TrailToolCall[] = [];
      let fullResponse = "";

      // W680 引擎主循环（替代 SDK query 流消费）
      const result = await runAgentTurn({
        config: { baseUrl: LLM_API_BASE, apiKey: LLM_API_KEY, model: selectedModel },
        messages: [
          { role: "system", content: systemPrompt || DEFAULT_SYSTEM_PROMPT },
          ...history,
        ],
        toolset,
        canUseTool,
        maxTurns: LLM_MAX_TURNS,
        signal: sseGuard.signal,
        handlers: {
          onText: (delta) => {
            // W844：OBS-14——首个 text delta 即「首 token」。sse.init 是会话元信息帧，不计。
            if (firstTokenMs === null) {
              firstTokenMs = Date.now() - reqStartedAt;
              recordFirstToken(firstTokenMs);
              logger.info("问答首 token 计时", {
                request_id: req.requestId,
                first_token_ms: firstTokenMs,
                model: selectedModel,
                session_id: session.id,
              });
            }
            fullResponse += delta;
            sse.text(delta);
          },
          onToolCall: (call) => {
            logger.info("工具调用", { request_id: req.requestId, tool_call_id: call.id, tool: call.name });
            // P3-1：工具入参属敏感信息，仅在显式 verbose 模式下输出
            if (VERBOSE_LOG) logger.debug("工具入参", { request_id: req.requestId, input: call.input });
            toolCalls.push({ id: call.id, name: call.name, input: call.input, status: "running" });
            sse.tool(call);
          },
          onToolResult: (toolId, content, isError) => {
            logger.info("工具结果", { request_id: req.requestId, tool_call_id: toolId, is_error: isError });
            const tool = toolCalls.find((t) => t.id === toolId) ?? toolCalls[toolCalls.length - 1];
            if (tool) {
              tool.status = isError ? "error" : "completed";
              tool.isError = isError;
              tool.result = content;
            }
            if (tool?.name) {
              auditToolResult({ sessionId: session.id, tool, toolId, content, isError, deniedToolUseIds });
            }
            sse.toolResult({ toolId, content, isError });
          },
        },
      });

      // W844：OBS-14——整轮无文本增量（纯工具调用）时明确记「无样本」，
      // 而不是留空让下游把「缺数据」读成「0 ms」。SLO 只对文本回答有意义。
      if (firstTokenMs === null) {
        logger.info("问答首 token 无样本", {
          request_id: req.requestId,
          reason: "no_text_delta",
          model: selectedModel,
          session_id: session.id,
        });
      }

      // 完成时兜底：仍未终结的工具标记完成（对齐旧 result 分支语义）
      toolCalls.forEach((tool) => {
        if (tool.status === "running") {
          tool.status = "completed";
          sse.toolResult({ toolId: tool.id, content: tool.result || "已完成" });
        }
      });
      // W599 引用校验：最终文本路径核实（存在→GitHub 链接；不存在→文末警示），SSE done 前执行
      const guarded = applyCitationGuard(fullResponse, PROJECT_CWD);
      if (guarded.text !== fullResponse) {
        sse.citationGuard({ text: guarded.text, unverified: guarded.unverified });
      }
      sse.done(result.durationMs);

      // P2-3：清理 SSE 定时器与 close 监听（正常完成路径）
      sseGuard.clearTimer();
      res.off("close", abortStream); // W791：注销侧修正为 res（监听注册在 res·W568 改挂时漏改注销）

      // 保存助手消息到数据库
      db.createMessage({
        id: assistantMessageId,
        session_id: session.id,
        role: "assistant",
        content: fullResponse,
        model: selectedModel,
        created_at: new Date().toISOString(),
        tool_calls: toolCalls.length > 0 ? JSON.stringify(toolCalls) : null,
      });

      // 更新会话标题（如果是第一条消息）
      const messages = db.getMessagesBySession(session.id);
      if (messages.length <= 2) {
        db.updateSession(session.id, {
          title: titleFromMessage(message),
          model: selectedModel,
        });
      }

      logger.info("请求完成", { request_id: req.requestId, session_id: session.id });
      res.end();
    } catch (error) {
      sseGuard.clearTimer(); // P2-3：异常路径同样清理定时器与 close 监听
      res.off("close", abortStream); // W791：注销侧修正为 res（监听注册在 res·W568 改挂时漏改注销）
      logger.error("聊天请求失败", {
        request_id: req.requestId,
        error_name: (error as Error)?.name,
        error: (error as Error)?.message,
        error_code: (error as NodeJS.ErrnoException)?.code,
        stack: (error as Error)?.stack,
      });

      // W829：对外只给固定文案——上游 LLM 错误体可能回显请求内容/账号信息
      // （openai-compat.ts 取上游前 300 字原文），原文已进上面的 logger。
      sse.error("服务器内部错误");
      res.end();
    }
  });
}
