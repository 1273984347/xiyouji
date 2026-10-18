/**
 * routes.ts — 非聊天类 /api 路由注册（W803-D 自 index.ts 拆分）
 *
 * 职责边界：会话 CRUD / 反馈 / 健康检查 / 审计回放 / 引擎配置状态 / 模型列表。
 * **聊天流式路由不在本模块**（见 chat.ts）——它是唯一写 SSE 的入口，单独成文件便于对照契约。
 *
 * 契约红线（路径/方法/字段名/状态码逐字保留）：
 *   POST   /api/feedback              400 invalid body | { ok, inserted }
 *   GET    /api/feedback/summary      { ok, up, down }
 *   GET    /api/health                { status, timestamp }
 *   GET    /api/audit                 { ok, limit, total, skipped, entries }
 *   GET    /api/check-login           LoginStatusResponse（apiKey 脱敏 `****` + 末四位）
 *   GET    /api/models                { models:[{modelId,name}], defaultModel }
 *   GET    /api/sessions              { sessions:[…+messageCount] }
 *   GET    /api/sessions/:sessionId   { session, messages } | 404 | 500
 *   POST   /api/sessions              { session }
 *   PATCH  /api/sessions/:sessionId   { success:true } | 404 | 500
 *   DELETE /api/sessions/:sessionId   { success:true } | 404 | 500
 *   POST   /api/permission-response   { success:true } | 404
 */
import type { Express, Request, Response } from "express";
import { v4 as uuidv4 } from "uuid";
import * as db from "./db.js";
import { readAudit } from "./audit.js";
import { sendError, errorMessage } from "./http.js";
import {
  LLM_API_BASE,
  LLM_API_KEY,
  LLM_MODEL,
  defaultModel,
  engineConfigured,
} from "./config.js";
import { asRecord, handlePermissionResponse, type PendingPermissionStore } from "./permissions.js";

/**
 * 引擎配置状态（W680：原厂商 CLI 登录检查退役——路径保留以免前端 404）。
 * 字段名即前端 SettingsPage 的 LoginStatus 契约（含历史遗留的 cliConfigured）。
 */
interface LoginStatusResponse {
  isLoggedIn: boolean;
  method?: "env" | "none";
  envConfigured?: boolean;
  cliConfigured?: boolean;
  error?: string;
  apiKey?: string; // 脱敏后的 Key
  envVars?: {
    apiKey?: string;
    baseUrl?: string;
    model?: string;
  };
}

/** 会话与消息列表（含 messageCount；tool_calls 由 JSON 文本解析回数组）。 */
function listSessionsWithCount(): Array<Record<string, unknown>> {
  return db.getAllSessions().map((session) => ({
    ...session,
    messageCount: db.getMessagesBySession(session.id).length,
  }));
}

/** 注册所有非流式 /api 路由。 */
export function registerApiRoutes(app: Express, permissions: PendingPermissionStore): void {
  // 健康检查（W600 反馈闭环起，本路由即 W791 集成测试的探活点）
  app.post("/api/feedback", (req, res) => {
    const { sessionId, messageId, verdict, comment } = (req.body || {}) as Record<string, unknown>;
    if (typeof sessionId !== "string" || typeof messageId !== "string" || (verdict !== "up" && verdict !== "down")) {
      return sendError(res, 400, "invalid body");
    }
    const c = typeof comment === "string" ? comment.slice(0, 500) : "";
    const inserted = db.insertFeedback({ id: uuidv4(), session_id: sessionId, message_id: messageId, verdict, comment: c });
    res.json({ ok: true, inserted });
  });

  app.get("/api/feedback/summary", (_req, res) => {
    res.json({ ok: true, ...db.feedbackSummary(30) });
  });

  app.get("/api/health", (req, res) => {
    res.json({ status: "ok", timestamp: new Date().toISOString() });
  });

  // W752 写操作审计回放（只读）：返回最近 limit 条（默认 100，上限 1000）。
  // 与其余 /api/* 同受 AGENT_WEB_TOKEN 中间件与 30 req/min 限流保护；
  // 审计文件本体在工具层禁读（tools.ts DENY_READ），LLM 无法读回自己的操作史。
  app.get("/api/audit", (req, res) => {
    const raw = Number(req.query.limit);
    const limit = Number.isFinite(raw) && raw > 0 ? Math.min(Math.floor(raw), 1000) : 100;
    const result = readAudit(limit);
    res.json({ ok: true, limit, total: result.total, skipped: result.skipped, entries: result.entries });
  });

  app.get("/api/check-login", (req, res) => {
    const response: LoginStatusResponse = {
      isLoggedIn: engineConfigured(),
      method: "none",
      envConfigured: false,
      cliConfigured: false,
      envVars: {},
    };

    if (LLM_API_KEY) {
      response.envConfigured = true;
      response.method = "env";
      response.apiKey = "****" + LLM_API_KEY.slice(-4); // W537 脱敏口径
      response.envVars!.apiKey = response.apiKey;
    }
    if (LLM_API_BASE) response.envVars!.baseUrl = LLM_API_BASE;
    if (process.env.LLM_MODEL) response.envVars!.model = LLM_MODEL;
    if (!response.isLoggedIn) {
      response.error = "未配置引擎：请在服务端 .env 设置 LLM_API_BASE / LLM_API_KEY / LLM_MODEL 后重启";
    }

    res.json(response);
  });

  // （W680：原 /api/save-env-config 运行时凭证配置端点随引擎更换整体退役——
  //   LLM_API_BASE / LLM_API_KEY / LLM_MODEL 仅从服务端 .env 读取，重启生效。）

  // 获取可用模型列表（W680：从环境变量静态读取，不再起 SDK 会话探测）
  app.get("/api/models", (req, res) => {
    const list = (process.env.LLM_MODELS || process.env.LLM_MODEL || "default-model")
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean)
      .map((id) => ({ modelId: id, name: id }));
    res.json({ models: list, defaultModel });
  });

  registerSessionRoutes(app);
  registerPermissionRoute(app, permissions);
}

// ============= 会话 API =============

/** 会话 CRUD（五个方法同一错误兜底骨架：console.error + 500 + error.message）。 */
function registerSessionRoutes(app: Express): void {
  // 获取所有会话（包含消息数量）
  app.get("/api/sessions", (req, res) => {
    try {
      res.json({ sessions: listSessionsWithCount() });
    } catch (error) {
      console.error("[Sessions] Error:", error);
      sendError(res, 500, errorMessage(error, "获取会话失败"));
    }
  });

  // 获取单个会话及其消息
  app.get("/api/sessions/:sessionId", (req, res) => {
    try {
      const { sessionId } = req.params;
      const session = db.getSession(sessionId);

      if (!session) {
        return sendError(res, 404, "会话不存在");
      }

      const messages = db.getMessagesBySession(sessionId);

      // 解析 tool_calls JSON
      const parsedMessages = messages.map((msg) => ({
        ...msg,
        tool_calls: msg.tool_calls ? JSON.parse(msg.tool_calls) : null,
      }));

      res.json({ session, messages: parsedMessages });
    } catch (error) {
      console.error("[Session] Error:", error);
      sendError(res, 500, errorMessage(error, "获取会话失败"));
    }
  });

  // 创建新会话
  app.post("/api/sessions", (req, res) => {
    try {
      const { model = defaultModel, title = "新对话" } = req.body;
      const now = new Date().toISOString();

      const session = db.createSession({
        id: uuidv4(),
        title,
        model,
        sdk_session_id: null,
        created_at: now,
        updated_at: now,
      });

      res.json({ session });
    } catch (error) {
      console.error("[Create Session] Error:", error);
      sendError(res, 500, errorMessage(error, "创建会话失败"));
    }
  });

  // 更新会话
  app.patch("/api/sessions/:sessionId", (req, res) => {
    try {
      const { sessionId } = req.params;
      const { title, model } = req.body;

      const success = db.updateSession(sessionId, { title, model });

      if (!success) {
        return sendError(res, 404, "会话不存在");
      }

      res.json({ success: true });
    } catch (error) {
      console.error("[Update Session] Error:", error);
      sendError(res, 500, errorMessage(error, "更新会话失败"));
    }
  });

  // 删除会话
  app.delete("/api/sessions/:sessionId", (req, res) => {
    try {
      const { sessionId } = req.params;
      const success = db.deleteSession(sessionId);

      if (!success) {
        return sendError(res, 404, "会话不存在");
      }

      res.json({ success: true });
    } catch (error) {
      console.error("[Delete Session] Error:", error);
      sendError(res, 500, errorMessage(error, "删除会话失败"));
    }
  });
}

// ============= 权限响应 API =============

/** 前端许可卡回执（决策与挂起表语义在 permissions.ts）。 */
function registerPermissionRoute(app: Express, permissions: PendingPermissionStore): void {
  app.post("/api/permission-response", (req: Request, res: Response) => {
    handlePermissionResponse(permissions, asRecord(req.body), res);
  });
}
