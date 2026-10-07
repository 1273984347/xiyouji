import 'dotenv/config';
import express from "express";
import { v4 as uuidv4 } from "uuid";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
import * as db from "./db.js";
import { applyCitationGuard } from "./citationGuard.js";
import { runAgentTurn } from "./engine/agent-loop.js";
import { createToolset, TOOL_PERMISSION_KIND } from "./engine/tools.js";
import type { ChatMessage, CanUseTool, PermissionDecision } from "./engine/types.js";

// 待处理的权限请求
interface PendingPermission {
  resolve: (result: PermissionDecision) => void;
  reject: (error: Error) => void;
  toolName: string;
  input: Record<string, unknown>;
  sessionId: string;
  timestamp: number;
}

// W536 安全加固：无原型对象存储（键经 _safeKey 白名单防原型污染）
const pendingPermissions: Record<string, PendingPermission> = Object.create(null);
const _safeKey = (k: unknown): string | null =>
  typeof k === "string" && k !== "__proto__" && k !== "constructor" && k !== "prototype" ? k : null;

// 权限请求超时时间（5分钟）
const PERMISSION_TIMEOUT = 5 * 60 * 1000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT: number = Number(process.env.PORT) || 3000;

// 适配项目：详解西游记（xiyouji）
// 默认工作目录=仓库根：向上探测「AGENTS.md + site/tokens.css」锚点自动解析。
// （W596：旧实现写死已不存在的双副本绝对路径，默认值悬空。）
// 可用环境变量 PROJECT_CWD 覆盖（如指向其他副本）。
function resolveProjectCwd(): string {
  if (process.env.PROJECT_CWD) return process.env.PROJECT_CWD;
  let dir = path.resolve(__dirname);
  for (let i = 0; i < 6; i++) {
    if (fs.existsSync(path.join(dir, "AGENTS.md")) && fs.existsSync(path.join(dir, "site", "tokens.css"))) {
      return dir;
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return path.resolve(__dirname, "..", "..");
}
const PROJECT_CWD = resolveProjectCwd();
if (!fs.existsSync(PROJECT_CWD)) {
  console.error(`[FATAL] PROJECT_CWD 不存在: ${PROJECT_CWD}（请用环境变量 PROJECT_CWD 指向有效仓库副本）`);
  process.exit(1);
}
console.log(`[boot] PROJECT_CWD = ${PROJECT_CWD}`);

// Middleware
app.use(express.json());

// 安全头（与 site/_headers 一致：防点击劫持 / MIME 嗅探 / Referer 泄露，P0-1 修复）
app.use((_req, res, next) => {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
  res.setHeader("Permissions-Policy", "geolocation=(), microphone=(), camera=()");
  next();
});

// 可选认证（P0-1 修复）：设置 AGENT_WEB_TOKEN 后，所有 /api/* 需携带
// x-agent-token 或 Authorization: Bearer <token>；未设置则保持本地免认证模式。
const AGENT_WEB_TOKEN = process.env.AGENT_WEB_TOKEN || "";
if (AGENT_WEB_TOKEN) {
  app.use((req, res, next) => {
    const auth = String(req.headers["x-agent-token"] || "").trim()
      || String(req.headers.authorization || "").replace(/^Bearer\s+/i, "").trim();
    if (auth === AGENT_WEB_TOKEN) return next();
    res.status(401).json({ error: "未授权：请在请求头携带 AGENT_WEB_TOKEN（x-agent-token 或 Authorization: Bearer）" });
  });
}

// P0-1 修复：权限模式白名单——外部请求体不可直接传入 bypassPermissions（防未授权 RCE）
const SAFE_PERMISSION_MODES = new Set(["default", "acceptEdits", "plan"]);
// 仅当显式设置 AGENT_WEB_ALLOW_BYPASS=1 时启用 bypassPermissions（本地单人模式）
const ALLOW_BYPASS = process.env.AGENT_WEB_ALLOW_BYPASS === "1";
// P3-1：详细日志（工具输入/流消息）默认关闭，仅 AGENT_WEB_VERBOSE=1 时打印（防敏感信息泄露）
const VERBOSE_LOG = process.env.AGENT_WEB_VERBOSE === "1";

function sanitizePermissionMode(input: unknown): "default" | "acceptEdits" | "plan" | "bypassPermissions" {
  if (typeof input === "string" && SAFE_PERMISSION_MODES.has(input)) return input as "default" | "acceptEdits" | "plan";
  if (ALLOW_BYPASS && input === "bypassPermissions") return "bypassPermissions";
  return "default";
}

// P0-1/W536：工作目录钳制逻辑已内联至 /api/chat 调用点（realpath 规范化 + PROJECT_CWD 前缀校验）。

// 引擎配置（W680）：OpenAI-compatible 端点，全部由服务端 .env 提供（P0-2 同款纪律：禁运行时覆盖）。
// 兼容所有主流大模型：GLM/DeepSeek/Kimi/Qwen/OpenAI/Gemini/Claude-compat/ollama/vLLM 等。
const LLM_API_BASE = process.env.LLM_API_BASE || "";
const LLM_API_KEY = process.env.LLM_API_KEY || "";
const LLM_MODEL = process.env.LLM_MODEL || "default-model";
const LLM_MAX_TURNS = Number(process.env.LLM_MAX_TURNS) > 0 ? Number(process.env.LLM_MAX_TURNS) : 10;
const defaultModel = LLM_MODEL;

// 健康检查
// W600 反馈闭环
app.post("/api/feedback", (req, res) => {
  const { sessionId, messageId, verdict, comment } = (req.body || {}) as Record<string, unknown>;
  if (typeof sessionId !== "string" || typeof messageId !== "string" || (verdict !== "up" && verdict !== "down")) {
    return res.status(400).json({ error: "invalid body" });
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

// 引擎配置状态（W680：原厂商 CLI 登录检查退役——路径保留以免前端 404）
interface LoginStatusResponse {
  isLoggedIn: boolean;
  method?: 'env' | 'none';
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

app.get("/api/check-login", (req, res) => {
  const response: LoginStatusResponse = {
    isLoggedIn: Boolean(LLM_API_KEY && LLM_API_BASE),
    method: 'none',
    envConfigured: false,
    cliConfigured: false,
    envVars: {},
  };

  if (LLM_API_KEY) {
    response.envConfigured = true;
    response.method = 'env';
    response.apiKey = '****' + LLM_API_KEY.slice(-4); // W537 脱敏口径
    response.envVars!.apiKey = response.apiKey;
  }
  if (LLM_API_BASE) response.envVars!.baseUrl = LLM_API_BASE;
  if (process.env.LLM_MODEL) response.envVars!.model = LLM_MODEL;
  if (!response.isLoggedIn) {
    response.error = '未配置引擎：请在服务端 .env 设置 LLM_API_BASE / LLM_API_KEY / LLM_MODEL 后重启';
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

// ============= 会话 API =============

// 获取所有会话（包含消息数量）
app.get("/api/sessions", (req, res) => {
  try {
    const sessions = db.getAllSessions();
    const sessionsWithMessages = sessions.map(session => {
      const messages = db.getMessagesBySession(session.id);
      return {
        ...session,
        messageCount: messages.length
      };
    });
    res.json({ sessions: sessionsWithMessages });
  } catch (error: any) {
    console.error("[Sessions] Error:", error);
    res.status(500).json({ error: error?.message || "获取会话失败" });
  }
});

// 获取单个会话及其消息
app.get("/api/sessions/:sessionId", (req, res) => {
  try {
    const { sessionId } = req.params;
    const session = db.getSession(sessionId);
    
    if (!session) {
      return res.status(404).json({ error: "会话不存在" });
    }
    
    const messages = db.getMessagesBySession(sessionId);
    
    // 解析 tool_calls JSON
    const parsedMessages = messages.map(msg => ({
      ...msg,
      tool_calls: msg.tool_calls ? JSON.parse(msg.tool_calls) : null
    }));
    
    res.json({ session, messages: parsedMessages });
  } catch (error: any) {
    console.error("[Session] Error:", error);
    res.status(500).json({ error: error?.message || "获取会话失败" });
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
      updated_at: now
    });
    
    res.json({ session });
  } catch (error: any) {
    console.error("[Create Session] Error:", error);
    res.status(500).json({ error: error?.message || "创建会话失败" });
  }
});

// 更新会话
app.patch("/api/sessions/:sessionId", (req, res) => {
  try {
    const { sessionId } = req.params;
    const { title, model } = req.body;
    
    const success = db.updateSession(sessionId, { title, model });
    
    if (!success) {
      return res.status(404).json({ error: "会话不存在" });
    }
    
    res.json({ success: true });
  } catch (error: any) {
    console.error("[Update Session] Error:", error);
    res.status(500).json({ error: error?.message || "更新会话失败" });
  }
});

// 删除会话
app.delete("/api/sessions/:sessionId", (req, res) => {
  try {
    const { sessionId } = req.params;
    const success = db.deleteSession(sessionId);
    
    if (!success) {
      return res.status(404).json({ error: "会话不存在" });
    }
    
    res.json({ success: true });
  } catch (error: any) {
    console.error("[Delete Session] Error:", error);
    res.status(500).json({ error: error?.message || "删除会话失败" });
  }
});

// ============= 聊天 API =============

// 权限响应 API
app.post("/api/permission-response", (req, res) => {
  const { requestId, behavior, message } = req.body;
  
  console.log(`[Permission] Response received: requestId=${requestId}, behavior=${behavior}`);
  
  const reqKey = _safeKey(requestId);
  const pending = reqKey ? pendingPermissions[reqKey] : undefined;
  if (!pending) {
    console.log(`[Permission] Request not found: ${requestId}`);
    return res.status(404).json({ error: "权限请求不存在或已超时" });
  }
  
  // 清除请求
  if (reqKey) delete pendingPermissions[reqKey];
  
  if (behavior === 'allow') {
    pending.resolve({
      behavior: 'allow',
      updatedInput: pending.input
    });
  } else {
    pending.resolve({
      behavior: 'deny',
      message: message || '用户拒绝了此操作'
    });
  }
  
  res.json({ success: true });
});

// 发送消息并获取流式响应
app.post("/api/chat", async (req, res) => {
  const { sessionId, message, model, systemPrompt, cwd, permissionMode } = req.body;

  // P0-1 修复：工作目录仅允许 PROJECT_CWD 内 + 权限模式白名单净化（不信任请求体原值）
  // P0-1 + W536 安全加固：工作目录钳制（realpath 规范化后仅允许 PROJECT_CWD 内，非法输入回落默认）
  let workingDir = path.resolve(PROJECT_CWD);
  try { workingDir = fs.realpathSync(workingDir); } catch { /* 保持 resolve 结果 */ }
  if (typeof cwd === "string" && cwd.trim()) {
    let candidate = path.resolve(cwd);
    try { candidate = fs.realpathSync(candidate); } catch { candidate = ""; }
    if (candidate && (candidate === workingDir || candidate.startsWith(workingDir + path.sep))) workingDir = candidate;
  }
  const effectivePermissionMode = sanitizePermissionMode(permissionMode);
  
  // 请求日志
  console.log(`\n[Chat] ========== 新请求 ==========`);
  console.log(`[Chat] SessionId: ${sessionId}`);
  console.log(`[Chat] Model: ${model}`);
  console.log(`[Chat] Message: ${message?.slice(0, 100)}${message?.length > 100 ? '...' : ''}`);
  console.log(`[Chat] CWD: ${cwd || 'default'}`);

  if (!message) {
    console.log(`[Chat] 错误: 消息为空`);
    return res.status(400).json({ error: "消息不能为空" });
  }

  // W680：引擎未配置时快速失败（400 JSON，不进 SSE 流）
  if (!LLM_API_BASE || !LLM_API_KEY) {
    return res.status(400).json({ error: "引擎未配置：请在服务端 .env 设置 LLM_API_BASE / LLM_API_KEY / LLM_MODEL 后重启生效" });
  }

  // 获取或创建会话
  let session = sessionId ? db.getSession(sessionId) : null;
  const now = new Date().toISOString();
  
  if (!session) {
    // 创建新会话
    console.log(`[Chat] 创建新会话`);
    session = db.createSession({
      id: sessionId || uuidv4(),
      title: message.slice(0, 30) + (message.length > 30 ? '...' : ''),
      model: model || defaultModel,
      sdk_session_id: null,  // W680：SDK resume 退役，历史从 SQLite 重建
      created_at: now,
      updated_at: now
    });
  } else {
    console.log(`[Chat] 使用现有会话`);
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
      role: 'user',
      content: message,
      model: null,
      created_at: now,
      tool_calls: null
    });
    console.log(`[Chat] 用户消息已保存: ${userMessageId}`);
  } catch (dbError: any) {
    console.error(`[Chat] 保存用户消息失败:`, dbError);
    return res.status(500).json({ error: "保存消息失败", detail: dbError?.message });
  }

  // 设置 SSE 头
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  // P2-3 修复：SSE 断开清理 + 总时长上限（防客户端断开后流继续运行、pending 权限请求悬挂）
  let aborted = false;
  const SSE_MAX_MS = 10 * 60 * 1000; // 10 分钟总时长上限
  const sseTimer = setTimeout(() => {
    if (aborted) return;
    aborted = true;
    engineAbort.abort(); // W680 复核：超时路径同样中止引擎（与 abortStream 对齐，不再烧 token）
    for (const rid of Object.keys(pendingPermissions)) {
      const p = pendingPermissions[rid];
      if (p.sessionId === session.id) {
        delete pendingPermissions[rid];
        p.reject(new Error("SSE 超时"));
      }
    }
    try {
      res.write(`data: ${JSON.stringify({ type: "error", message: "请求超时（10 分钟上限）" })}\n\n`);
      res.end();
    } catch { /* 客户端可能已断开 */ }
  }, SSE_MAX_MS);
  const abortStream = () => {
    if (aborted) return;
    aborted = true;
    clearTimeout(sseTimer);
    for (const rid of Object.keys(pendingPermissions)) {
      const p = pendingPermissions[rid];
      if (p.sessionId === session.id) {
        delete pendingPermissions[rid];
        p.reject(new Error("客户端断开连接"));
      }
    }
    engineAbort.abort(); // W680：中止引擎（终止 LLM 流消费，不再为已断开的客户端烧 token）
    try { res.end(); } catch { /* 已断开 */ }
  };
  const engineAbort = new AbortController();
  // W568 修复：Express 5 / Node 20+ 下 req 的 'close' 在「请求体读取完毕」即触发（并非连接断开），
  // abortStream 会立刻 res.end() 吞掉后续全部 SSE 事件（实证：init 之后 error 事件整段丢失）。
  // 改挂 res 'close'——仅在客户端提前断开或响应正常完成时触发；完成态重复 res.end() 为无害空操作。
  res.on("close", abortStream);

  // 默认系统提示词（适配「详解西游记」xiyouji 项目）
  const defaultSystemPrompt = `你是「详解西游记」项目的专属智能助手，代号「渡口问津」。

【项目背景】
本项目（位于 ${PROJECT_CWD}）是一座关于《西游记》的混合型解读知识库，以「一源多形」方式组织：
- docs/：Markdown 文档主体，含十大学生板块（01 全书逐回解读、02 人物深度分析、03 主题与情节专题、04 文化与历史背景、05 诗词歌赋、06 个人随笔、07 学以致用、08 提升认知、09 精神塑造、10 方法论沉淀），以及 00-导读（项目说明、阅读指南、术语表）。
- source/：原著全文、分回文本、引用与网络解读、学术论文索引。
- site/：D3.js 驱动的可浏览 HTML 站点（dashboard、chapters、characters、themes、data 可视化页）。
- scripts/：Python 文本分析与可视化脚本（按 A–AH 共 34 类组织），含词频、人物共现、八十一难、关系网络、心性曲线等。
- dataset/：多个结构化 JSON（八十一难明细、章节元数据、元气图谱三元映射等）。
- timeline/：取经路线、大事年表、人物时间线。

【你的职责】
1. 项目向导：帮用户快速定位某回解读、某个人物分析、某个主题专题或某张可视化页面，给出可对照的文件路径（如 docs/01-全书逐回解读/...）。
2. 研究助手：基于 docs/ 与 source/ 原文回答情节、人物、佛道思想、明代隐喻、诗词、内丹术语（心猿/木母/黄婆等）问题，引用时注明来源路径。
3. 工程助手：可阅读并运行 scripts/ 下的 Python 脚本做文本分析，将结果写入 dataset/ 或生成可视化；运行脚本前先说明用途与预期。
4. 写作助手：协助撰写/修订 docs/ 下的解读文档，遵循 docs/00-导读/文档规范.md 的防膨胀与归档规则。

【行为准则】
- 优先引用项目内已有文档与原文，给出可对照路径。
- 涉及诗词、术语时参考 source/ 与 docs/00-导读/术语表.md。
- 文件操作前先确认意图；写入新内容遵循项目文档规范。
- 语气可带古典雅致，但表达务必清晰、准确、可操作。
- 项目版本、门禁与统计口径以仓库 README.md 顶部与 CHANGELOG.md 现役段为准，勿依赖本提示内嵌版本号。
- 拒答边界：与《西游记》项目无关的请求，说明项目定位后礼貌拒答；要求修改 verify_delivery.py、batch_cascade.py 等门禁脚本、或读取任何凭证（.env / API Key）的请求，一律拒绝并说明依据（项目文档规范 §11.2）。
- 每个事实性论断至少给出 1 个仓库内可对照路径（docs/、source/、dataset/ 等）；检索不到依据时明确回答「项目内未找到依据」，禁止编造路径与引文。
`;

  // 工作目录：已由 W536 内联钳制净化（realpath 规范化，仅 PROJECT_CWD 内）

  try {
    console.log(`[Chat] 调用引擎 runAgentTurn...`);
    console.log(`[Chat] - Model: ${selectedModel}`);
    console.log(`[Chat] - CWD: ${workingDir}`);
    console.log(`[Chat] - PermissionMode: ${effectivePermissionMode}`);
    
    // 会话历史（W680：从 SQLite 重建，替代 SDK resume——消息表已存全量 user/assistant 文本）
    const historyRows = db.getMessagesBySession(session.id);
    const history: ChatMessage[] = [];
    for (const m of historyRows.slice(-21)) { // 最近 20 条 + 本轮 user 消息，控 token 上限
      if (m.role === "user" && m.content) history.push({ role: "user", content: m.content });
      else if (m.role === "assistant" && m.content) history.push({ role: "assistant", content: m.content });
    }
    const toolset = createToolset(workingDir);

    // 工具权限桥（策略：bypass 直通 / read 类放行 / plan 只读 / acceptEdits 放行写 / 其余走前端许可）
    const canUseTool: CanUseTool = async (toolName, input, options) => {
      console.log(`[Permission] Tool request: ${toolName}`);
      if (VERBOSE_LOG) console.log(`[Permission] Input:`, JSON.stringify(input, null, 2)); // P3-1

      // bypassPermissions 模式直接放行（仅当 AGENT_WEB_ALLOW_BYPASS=1 时经净化可达）
      if (effectivePermissionMode === 'bypassPermissions') {
        console.log(`[Permission] Bypassing permissions for ${toolName}`);
        return { behavior: 'allow', updatedInput: input };
      }

      const kind = TOOL_PERMISSION_KIND[toolName] ?? "command";
      if (kind === "read") return { behavior: 'allow', updatedInput: input };
      if (effectivePermissionMode === 'plan') {
        return { behavior: 'deny', message: 'plan 模式为只读规划：写入与命令执行被拒绝' };
      }
      if (kind === "write" && effectivePermissionMode === 'acceptEdits') {
        return { behavior: 'allow', updatedInput: input };
      }

      // default 的写操作与各模式（除 bypass）的命令执行 → 请求前端许可
      const requestId = uuidv4();
      const permissionRequest = {
        requestId,
        toolUseId: options.toolUseID,
        toolName,
        input,
        sessionId: session.id,
        timestamp: Date.now()
      };

      // 发送权限请求到前端
      res.write(`data: ${JSON.stringify({
        type: "permission_request",
        ...permissionRequest
      })}\n\n`);

      // 创建 Promise 等待用户响应
      return new Promise<PermissionDecision>((resolve, reject) => {
        const pending: PendingPermission = {
          resolve,
          reject,
          toolName,
          input,
          sessionId: session.id,
          timestamp: Date.now()
        };

        const reqKey2 = _safeKey(requestId);
        if (reqKey2) pendingPermissions[reqKey2] = pending;

        // 设置超时
        setTimeout(() => {
          if (reqKey2 && pendingPermissions[reqKey2] !== undefined) {
            delete pendingPermissions[reqKey2];
            console.log(`[Permission] Request timeout: ${requestId}`);
            resolve({
              behavior: 'deny',
              message: '权限请求超时'
            });
          }
        }, PERMISSION_TIMEOUT);
      });
    };
    
    // 发送会话ID和消息ID（引擎启动前，SSE 事件序契约第一事件）
    res.write(`data: ${JSON.stringify({
      type: "init",
      sessionId: session.id,
      userMessageId,
      assistantMessageId,
      model: selectedModel
    })}\n\n`);

    const toolCalls: Array<{
      id: string;
      name: string;
      input?: Record<string, unknown>;
      status: string;
      result?: string;
      isError?: boolean;
    }> = [];
    let fullResponse = "";

    // W680 引擎主循环（替代 SDK query 流消费）
    const result = await runAgentTurn({
      config: { baseUrl: LLM_API_BASE, apiKey: LLM_API_KEY, model: selectedModel },
      messages: [
        { role: "system", content: systemPrompt || defaultSystemPrompt },
        ...history,
      ],
      toolset,
      canUseTool,
      maxTurns: LLM_MAX_TURNS,
      signal: engineAbort.signal,
      handlers: {
        onText: (delta) => {
          fullResponse += delta;
          res.write(`data: ${JSON.stringify({ type: "text", content: delta })}\n\n`);
        },
        onToolCall: (call) => {
          console.log(`[Stream] Tool use: id=${call.id}, name=${call.name}`);
          if (VERBOSE_LOG) console.log(`[Stream] Tool input:`, JSON.stringify(call.input, null, 2)); // P3-1
          toolCalls.push({ id: call.id, name: call.name, input: call.input, status: "running" });
          res.write(`data: ${JSON.stringify({
            type: "tool",
            id: call.id,
            name: call.name,
            input: call.input,
            status: "running"
          })}\n\n`);
        },
        onToolResult: (toolId, content, isError) => {
          console.log(`[Stream] Tool result: tool_use_id=${toolId}, is_error=${isError}`);
          const tool = toolCalls.find((t) => t.id === toolId) ?? toolCalls[toolCalls.length - 1];
          if (tool) {
            tool.status = isError ? "error" : "completed";
            tool.isError = isError;
            tool.result = content;
          }
          res.write(`data: ${JSON.stringify({
            type: "tool_result",
            toolId,
            content,
            isError
          })}\n\n`);
        },
      },
    });

    // 完成时兜底：仍未终结的工具标记完成（对齐旧 result 分支语义）
    toolCalls.forEach((tool) => {
      if (tool.status === "running") {
        tool.status = "completed";
        res.write(`data: ${JSON.stringify({ type: "tool_result", toolId: tool.id, content: tool.result || "已完成" })}\n\n`);
      }
    });
    // W599 引用校验：最终文本路径核实（存在→GitHub 链接；不存在→文末警示），SSE done 前执行
    const guarded = applyCitationGuard(fullResponse, PROJECT_CWD);
    if (guarded.text !== fullResponse) {
      res.write(`data: ${JSON.stringify({ type: "citation_guard", text: guarded.text, unverified: guarded.unverified })}\n\n`);
    }
    res.write(`data: ${JSON.stringify({ type: "done", duration: result.durationMs })}\n\n`);

    // P2-3：清理 SSE 定时器与 close 监听（正常完成路径）
    clearTimeout(sseTimer);
    req.off("close", abortStream);

    // 保存助手消息到数据库
    db.createMessage({
      id: assistantMessageId,
      session_id: session.id,
      role: 'assistant',
      content: fullResponse,
      model: selectedModel,
      created_at: new Date().toISOString(),
      tool_calls: toolCalls.length > 0 ? JSON.stringify(toolCalls) : null
    });

    // 更新会话标题（如果是第一条消息）
    const messages = db.getMessagesBySession(session.id);
    if (messages.length <= 2) {
      db.updateSession(session.id, { 
        title: message.slice(0, 30) + (message.length > 30 ? '...' : ''),
        model: selectedModel
      });
    }

    console.log(`[Chat] 请求完成 ✓`);
    res.end();
  } catch (error: any) {
    clearTimeout(sseTimer); // P2-3：异常路径同样清理定时器与 close 监听
    req.off("close", abortStream);
    console.error(`\n[Chat] ========== 错误 ==========`);
    console.error(`[Chat] Error Name:`, error?.name);
    console.error(`[Chat] Error Message:`, error?.message);
    console.error(`[Chat] Error Code:`, error?.code);
    console.error(`[Chat] Error Stack:`, error?.stack);
    console.error(`[Chat] Full Error:`, JSON.stringify(error, null, 2));
    
    const errorMessage = error?.message || "处理请求时发生错误";
    res.write(`data: ${JSON.stringify({ type: "error", message: errorMessage })}\n\n`);
    res.end();
  }
});

// 启动服务器（P0-1 修复：仅绑定回环地址，默认不暴露到局域网/公网）
app.listen(PORT, "127.0.0.1", () => {
  console.log(`
╔════════════════════════════════════════════╗
║                                            ║
║     ◉ API 服务器已启动                      ║
║                                            ║
║     地址: http://127.0.0.1:${PORT}            ║
║     数据库: SQLite (data/chat.db)          ║
║                                            ║
╚════════════════════════════════════════════╝
  `);
});
