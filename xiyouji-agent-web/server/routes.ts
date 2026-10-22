/**
 * routes.ts — 非聊天类 /api 路由注册（W803-D 自 index.ts 拆分；W808 增补边界校验与类型化错误）
 *
 * 职责边界：会话 CRUD / 反馈 / 健康检查 / 审计回放 / 引擎配置状态 / 模型列表。
 * **聊天流式路由不在本模块**（见 chat.ts）——它是唯一写 SSE 的入口，单独成文件便于对照契约。
 *
 * 契约红线（路径/方法/字段名/状态码逐字保留）：
 *   POST   /api/feedback              400 invalid body | { ok, inserted }
 *   GET    /api/feedback/summary      { ok, up, down }
 *   GET    /api/health                { status, timestamp }
 *   GET    /api/ready                 { status, checks }        ← W808 新增（就绪探针）
 *   GET    /api/audit                 { ok, limit, total, skipped, entries }
 *   GET    /api/metrics               { ok, first_token:{count,window,p50,p95,min,max,sloMs} } ← W844 新增（OBS-14）
 *   GET    /api/check-login           LoginStatusResponse（apiKey 脱敏 `****` + 末四位）
 *   GET    /api/models                { models:[{modelId,name}], defaultModel }
 *   GET    /api/sessions              { sessions:[…+messageCount] }
 *   GET    /api/sessions/:sessionId   { session, messages } | 404 | 500
 *   POST   /api/sessions              { session }
 *   PATCH  /api/sessions/:sessionId   { success:true } | 404 | 500
 *   DELETE /api/sessions/:sessionId   { success:true } | 404 | 500
 *   POST   /api/permission-response   { success:true } | 404
 *
 * W808 变更说明（对外形状零改动）：
 *   ① 入参改由 server/validation.ts 的 Zod schema 统一校验，失败抛 ValidationError（422），
 *      由全局错误处理器序列化——**响应体形状仍为 `{ error: string }`**（与重构前 sendError 一致）；
 *   ② 「资源不存在」由 NotFoundError 表达（404 + 与重构前逐字一致的中文文案）；
 *   ③ 「数据未落库」等非预期异常由全局错误处理器收敛为 500 + 通用文案（不泄细节）。
 */
import type { Express, Request, Response } from "express";
import { v4 as uuidv4 } from "uuid";
import * as db from "./db.js";
import { readAudit } from "./audit.js";
import { firstTokenSummary } from "./metrics.js";
import { NotFoundError } from "./errors.js";
import { logger } from "./logger.js";
import {
  createSessionBodySchema,
  feedbackBodySchema,
  parseBody,
  updateSessionBodySchema,
} from "./validation.js";
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

/**
 * 数据库可达性探针（W808 新增）：供 /api/ready 使用。
 * 语义：执行一条最小查询（SELECT 1）确认 SQLite 连接可用。
 */
function checkDatabase(): { status: "ok" | "error"; detail?: string } {
  try {
    db.getAllSessions();
    return { status: "ok" };
  } catch (error) {
    // W829：不回显底层异常原文（含 SQLite 库文件绝对路径）——形状不变·取值固定·原文进日志
    logger.error("数据库可达性探针失败", {
      error: error instanceof Error ? error.message : String(error),
    });
    return { status: "error", detail: "数据库不可用" };
  }
}

/** 注册所有非流式 /api 路由。 */
export function registerApiRoutes(app: Express, permissions: PendingPermissionStore): void {
  // 健康检查（W600 反馈闭环起，本路由即 W791 集成测试的探活点）
  app.post("/api/feedback", (req, res) => {
    // W808：入参经 Zod 校验；失败保持既有契约 `400 invalid body`（状态码与文案逐字不变·
    // feedback.test.mjs 第 3 项断言即钉此契约），字段级明细仅进日志不进响应体。
    const body = parseBody(feedbackBodySchema, req.body, { statusCode: 400, message: "invalid body" });
    const inserted = db.insertFeedback({
      id: uuidv4(),
      session_id: body.sessionId,
      message_id: body.messageId,
      verdict: body.verdict,
      comment: body.comment ?? "",
    });
    res.json({ ok: true, inserted });
  });

  app.get("/api/feedback/summary", (_req, res) => {
    res.json({ ok: true, ...db.feedbackSummary(30) });
  });

  app.get("/api/health", (req, res) => {
    res.json({ status: "ok", timestamp: new Date().toISOString() });
  });

  // W808 新增：就绪探针（与 /api/health 的分工——health 只证明进程活着，ready 证明依赖可用）。
  // 任一依赖不可用返回 503（供容器编排判定「暂不可接流量」）。
  app.get("/api/ready", (_req, res) => {
    const checks = { database: checkDatabase() };
    const ok = Object.values(checks).every((c) => c.status === "ok");
    res.status(ok ? 200 : 503).json({ status: ok ? "ok" : "degraded", checks });
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

  // W844 · OBS-14：问答首 token 延迟的只读窗口摘要。
  // 与其余 /api/* 同受 token 中间件与限流保护；只读进程内滚动窗口，
  // **不落盘、不外发**——长期分布看结构化日志（logger 已记 first_token_ms）。
  app.get("/api/metrics", (_req, res) => {
    res.json({ ok: true, first_token: firstTokenSummary() });
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
    if (process.env.LLM_MODEL) response.envVars!.model = process.env.LLM_MODEL;
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

/**
 * 会话 CRUD。
 *
 * W808 变更：入参经 Zod 校验；「会话不存在」改抛 NotFoundError（404 + 与重构前逐字一致的中文文案）。
 * 非预期的落库异常不再由各路由自行 catch 拼装——交全局错误处理器统一收敛为 500 通用文案。
 */
function registerSessionRoutes(app: Express): void {
  // 获取所有会话（包含消息数量）
  app.get("/api/sessions", (_req, res) => {
    res.json({ sessions: listSessionsWithCount() });
  });

  // 获取单个会话及其消息
  app.get("/api/sessions/:sessionId", (req, res) => {
    const { sessionId } = req.params;
    const session = db.getSession(sessionId);

    if (!session) {
      throw new NotFoundError("会话", sessionId);
    }

    const messages = db.getMessagesBySession(sessionId);

    // 解析 tool_calls JSON
    const parsedMessages = messages.map((msg) => ({
      ...msg,
      tool_calls: msg.tool_calls ? JSON.parse(msg.tool_calls) : null,
    }));

    res.json({ session, messages: parsedMessages });
  });

  // 创建新会话
  app.post("/api/sessions", (req, res) => {
    const body = parseBody(createSessionBodySchema, req.body);
    const now = new Date().toISOString();

    const session = db.createSession({
      id: uuidv4(),
      title: body.title ?? "新对话",
      model: body.model ?? defaultModel,
      sdk_session_id: null,
      created_at: now,
      updated_at: now,
    });

    res.json({ session });
  });

  // 更新会话
  app.patch("/api/sessions/:sessionId", (req, res) => {
    const { sessionId } = req.params;
    const body = parseBody(updateSessionBodySchema, req.body);

    const success = db.updateSession(sessionId, { title: body.title, model: body.model });

    if (!success) {
      throw new NotFoundError("会话", sessionId);
    }

    res.json({ success: true });
  });

  // 删除会话
  app.delete("/api/sessions/:sessionId", (req, res) => {
    const { sessionId } = req.params;
    const success = db.deleteSession(sessionId);

    if (!success) {
      throw new NotFoundError("会话", sessionId);
    }

    res.json({ success: true });
  });
}

// ============= 权限响应 API =============

/** 前端许可卡回执（决策与挂起表语义在 permissions.ts）。 */
function registerPermissionRoute(app: Express, permissions: PendingPermissionStore): void {
  app.post("/api/permission-response", (req: Request, res: Response) => {
    handlePermissionResponse(permissions, asRecord(req.body), res);
  });
}
