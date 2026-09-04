import 'dotenv/config';
import express from "express";
import { query as sdkQuery, unstable_v2_createSession, unstable_v2_authenticate, PermissionResult, CanUseTool, PermissionMode } from "@tencent-ai/agent-sdk";
import { v4 as uuidv4 } from "uuid";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
import * as db from "./db.js";

// 待处理的权限请求
interface PendingPermission {
  resolve: (result: PermissionResult) => void;
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
// 默认工作目录指向项目根，Agent 可在其上读取 docs/、运行 scripts/、写入 dataset/ 等。
// 可用环境变量 PROJECT_CWD 覆盖（如指向其他副本）。
const PROJECT_CWD = process.env.PROJECT_CWD || 'D:/1/xiyouji';

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

function sanitizePermissionMode(input: unknown): PermissionMode {
  if (typeof input === "string" && SAFE_PERMISSION_MODES.has(input)) return input as PermissionMode;
  if (ALLOW_BYPASS && input === "bypassPermissions") return "bypassPermissions";
  return "default";
}

// P0-1/W536：工作目录钳制逻辑已内联至 /api/chat 调用点（realpath 规范化 + PROJECT_CWD 前缀校验）。

// 缓存可用模型列表
let cachedModels: Array<{ modelId: string; name: string; description?: string }> = [];
const defaultModel = "claude-sonnet-4";

// 健康检查
app.get("/api/health", (req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

// 登录方式类型
type LoginMethod = 'env' | 'cli' | 'none';

interface LoginStatusResponse {
  isLoggedIn: boolean;
  method?: LoginMethod;
  envConfigured?: boolean;
  cliConfigured?: boolean;
  error?: string;
  apiKey?: string; // 脱敏后的 API Key
  envVars?: {
    apiKey?: string;
    authToken?: string;
    internetEnv?: string;
    baseUrl?: string;
  };
}

// 检查 CodeBuddy CLI 登录状态
app.get("/api/check-login", async (req, res) => {
  const response: LoginStatusResponse = {
    isLoggedIn: false,
    envConfigured: false,
    cliConfigured: false,
    envVars: {},
  };
  
  // 1. 检查环境变量
  const apiKey = process.env.CODEBUDDY_API_KEY;
  const authToken = process.env.CODEBUDDY_AUTH_TOKEN;
  const internetEnv = process.env.CODEBUDDY_INTERNET_ENVIRONMENT;
  const baseUrl = process.env.CODEBUDDY_BASE_URL;
  
  if (apiKey || authToken) {
    response.envConfigured = true;
    // 脱敏显示
    if (apiKey) {
      response.envVars!.apiKey = '****' + apiKey.slice(-4); // W537 脱敏收敛：不再回显前 8 位
      response.apiKey = response.envVars!.apiKey;
    }
    if (authToken) {
      response.envVars!.authToken = '****' + authToken.slice(-4);
    }
    if (internetEnv) {
      response.envVars!.internetEnv = internetEnv;
    }
    if (baseUrl) {
      response.envVars!.baseUrl = baseUrl;
    }
  }
  
  // 2. 使用 unstable_v2_authenticate 检查登录状态（更可靠）
  try {
    let needsLogin = false;
    
    const result = await unstable_v2_authenticate({
      environment: 'external',
      onAuthUrl: async (authState) => {
        // 如果执行到这个回调，说明未登录
        needsLogin = true;
        console.log('[Check Login] 需要登录，认证 URL:', authState.authUrl);
        // 将认证 URL 返回给前端（如果需要）
        response.error = '未登录，请先登录 CodeBuddy CLI';
      }
    });
    
    // 如果没有触发 onAuthUrl 回调，说明已登录
    if (!needsLogin && result?.userinfo) {
      response.isLoggedIn = true;
      response.cliConfigured = true;
      
      // 判断登录方式
      if (response.envConfigured) {
        response.method = 'env';
      } else {
        response.method = 'cli';
      }
      
      console.log('[Check Login] 已登录用户:', result.userinfo.userName);
    } else if (!needsLogin) {
      // result 存在但没有 userinfo，仍然认为已登录
      response.isLoggedIn = true;
      response.cliConfigured = true;
      response.method = response.envConfigured ? 'env' : 'cli';
    }
  } catch (error: any) {
    console.error("[Check Login] SDK Error:", error);
    
    // 如果有环境变量配置，仍然认为是登录状态
    if (response.envConfigured) {
      response.isLoggedIn = true;
      response.method = 'env';
    } else {
      response.error = error?.message || String(error);
      response.method = 'none';
    }
  }
  
  res.json(response);
});

// 保存环境变量配置（P0-2 修复：禁运行时覆盖 API_KEY/BASE_URL——密钥与端点仅从服务端 .env 读取，重启生效）
app.post("/api/save-env-config", (req, res) => {
  const { apiKey, authToken, internetEnv, baseUrl } = req.body;

  // P0-2：拒绝运行时覆盖密钥/端点（防密钥劫持 + SSRF；仅从服务端 .env 读取）
  if (apiKey || baseUrl) {
    return res.status(400).json({
      error: "CODEBUDDY_API_KEY / CODEBUDDY_BASE_URL 禁止运行时覆盖（P0-2）：请在服务端 .env 配置后重启生效",
      refused: ["CODEBUDDY_API_KEY", "CODEBUDDY_BASE_URL"],
    });
  }

  if (!authToken && !internetEnv) {
    return res.status(400).json({ error: '请至少配置 Auth Token 或网络环境' });
  }

  const configuredVars: string[] = [];

  if (authToken) {
    process.env.CODEBUDDY_AUTH_TOKEN = authToken;
    configuredVars.push('CODEBUDDY_AUTH_TOKEN');
  }
  if (internetEnv) {
    process.env.CODEBUDDY_INTERNET_ENVIRONMENT = internetEnv;
    configuredVars.push('CODEBUDDY_INTERNET_ENVIRONMENT');
  }

  // 清除模型缓存，以便重新获取
  cachedModels = [];

  res.json({
    success: true,
    message: `已设置: ${configuredVars.join(', ')}`,
    note: '环境变量仅在当前服务器进程有效，重启后需重新设置；API_KEY/BASE_URL 由服务端 .env 配置（P0-2）'
  });
});

// 获取可用模型列表
app.get("/api/models", async (req, res) => {
  try {
    if (cachedModels.length === 0) {
      console.log("[Models] Creating session to fetch available models...");
      
      const session = await unstable_v2_createSession({ 
        cwd: process.cwd()
      });
      
      console.log("[Models] Session created, calling getAvailableModels()...");
      const models = await session.getAvailableModels();
      console.log("[Models] Got", models.length, "models");
      
      if (models && Array.isArray(models)) {
        cachedModels = models;
      }
    }
    
    res.json({ 
      models: cachedModels.length > 0 ? cachedModels : [
        { modelId: "claude-sonnet-4", name: "Claude Sonnet 4" }
      ],
      defaultModel 
    });
  } catch (error: any) {
    console.error("[Models] Error:", error);
    res.json({
      models: [
        { modelId: "claude-sonnet-4", name: "Claude Sonnet 4" },
        { modelId: "claude-opus-4", name: "Claude Opus 4" }
      ],
      defaultModel,
      error: error?.message || String(error)
    });
  }
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
      sdk_session_id: null,  // 稍后从 SDK 获取
      created_at: now,
      updated_at: now
    });
  } else {
    console.log(`[Chat] 使用现有会话, SDK Session: ${session.sdk_session_id || 'none'}`);
  }

  const selectedModel = model || session.model;
  
  // 获取 SDK session ID（用于恢复对话）
  const sdkSessionId = session.sdk_session_id;

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
    try { res.end(); } catch { /* 已断开 */ }
  };
  req.on("close", abortStream);

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
- 项目版本、门禁与统计口径以仓库 README.md 顶部与 CHANGELOG.md 现役段为准，勿依赖本提示内嵌版本号。`;

  // 工作目录：已由 W536 内联钳制净化（realpath 规范化，仅 PROJECT_CWD 内）

  try {
    console.log(`[Chat] 调用 SDK query...`);
    console.log(`[Chat] - Model: ${selectedModel}`);
    console.log(`[Chat] - Resume: ${sdkSessionId || 'none'}`);
    console.log(`[Chat] - CWD: ${workingDir}`);
    console.log(`[Chat] - PermissionMode: ${effectivePermissionMode}`);
    
    // 创建 canUseTool 回调
    const canUseTool: CanUseTool = async (toolName, input, options) => {
      console.log(`[Permission] Tool request: ${toolName}`);
      if (VERBOSE_LOG) console.log(`[Permission] Input:`, JSON.stringify(input, null, 2)); // P3-1
      
      // bypassPermissions 模式直接放行（仅当 AGENT_WEB_ALLOW_BYPASS=1 时经净化可达）
      if (effectivePermissionMode === 'bypassPermissions') {
        console.log(`[Permission] Bypassing permissions for ${toolName}`);
        return { behavior: 'allow', updatedInput: input };
      }
      
      // 创建权限请求
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
      return new Promise<PermissionResult>((resolve, reject) => {
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
    
    // 使用 Query API 发送消息
    // 如果有 sdk_session_id，使用 resume 恢复对话上下文
    const stream = sdkQuery({
      prompt: message,
      options: {
        cwd: workingDir,
        model: selectedModel,
        maxTurns: 10,
        systemPrompt: systemPrompt || defaultSystemPrompt,
        permissionMode: effectivePermissionMode,
        canUseTool,
        ...(sdkSessionId ? { resume: sdkSessionId } : {})  // 使用 resume 恢复对话
      }
    });

    let fullResponse = "";
    let toolCalls: Array<{ 
      id: string; 
      name: string; 
      input?: Record<string, unknown>;
      status: string; 
      result?: string;
      isError?: boolean;
    }> = [];
    let newSdkSessionId: string | null = null;  // 用于存储 SDK 返回的 session_id

    // 发送会话ID和消息ID
    res.write(`data: ${JSON.stringify({ 
      type: "init", 
      sessionId: session.id, 
      userMessageId, 
      assistantMessageId,
      model: selectedModel 
    })}\n\n`);

    // 当前正在执行的工具 ID（用于匹配 tool_result）
    let currentToolId: string | null = null;

    // 处理流式响应
    for await (const msg of stream) {
      if (aborted) break; // P2-3：客户端断开/超时后停止消费与写入
      if (VERBOSE_LOG) console.log("[Stream] Message type:", msg.type, msg); // P3-1
      
      // 处理 system 消息，获取 SDK 的 session_id
      if (msg.type === "system" && (msg as any).subtype === "init") {
        newSdkSessionId = (msg as any).session_id;
        console.log(`[Stream] Got SDK session_id: ${newSdkSessionId}`);
        
        // 保存 SDK session_id 到数据库（如果是新的）
        if (newSdkSessionId && newSdkSessionId !== sdkSessionId) {
          db.updateSession(session.id, { sdk_session_id: newSdkSessionId });
          console.log(`[Stream] Saved SDK session_id to database`);
        }
      } else if (msg.type === "assistant") {
        const content = msg.message.content;

        if (typeof content === "string") {
          fullResponse += content;
          res.write(`data: ${JSON.stringify({ type: "text", content })}\n\n`);
        } else if (Array.isArray(content)) {
          for (const block of content) {
            if (block.type === "text") {
              fullResponse += block.text;
              res.write(`data: ${JSON.stringify({ type: "text", content: block.text })}\n\n`);
            } else if (block.type === "tool_use") {
              currentToolId = block.id || uuidv4();
              const toolInput = (block as any).input || {};
              console.log(`[Stream] Tool use: id=${currentToolId}, name=${block.name}`);
              if (VERBOSE_LOG) console.log(`[Stream] Tool input:`, JSON.stringify(toolInput, null, 2)); // P3-1
              
              const toolCall = { 
                id: currentToolId, 
                name: block.name, 
                input: toolInput,
                status: "running" 
              };
              toolCalls.push(toolCall);
              res.write(`data: ${JSON.stringify({ 
                type: "tool", 
                id: toolCall.id,
                name: toolCall.name,
                input: toolCall.input,
                status: toolCall.status
              })}\n\n`);
            }
          }
        }
      } else if ((msg as any).type === "tool_result") {
        // 处理工具结果（独立的消息类型）
        const msgAny = msg as any;
        const toolId = msgAny.tool_use_id || currentToolId;
        const isError = msgAny.is_error || false;
        const content = msgAny.content;
        
        console.log(`[Stream] Tool result: tool_use_id=${toolId}, is_error=${isError}`);
        if (VERBOSE_LOG) { // P3-1：详细结果内容默认不打印
          console.log(`[Stream] Tool result content type:`, typeof content);
          console.log(`[Stream] Tool result content:`, typeof content === 'string' ? content.slice(0, 500) : JSON.stringify(content, null, 2)?.slice(0, 500));
        }
        
        const tool = toolCalls.find(t => t.id === toolId) || toolCalls[toolCalls.length - 1];
        if (tool) {
          tool.status = isError ? "error" : "completed";
          tool.isError = isError;
          tool.result = typeof content === 'string' 
            ? content 
            : JSON.stringify(content);
          res.write(`data: ${JSON.stringify({ 
            type: "tool_result", 
            toolId: tool.id, 
            content: tool.result,
            isError: isError
          })}\n\n`);
        }
        currentToolId = null;
      } else if (msg.type === "result") {
        // 完成时确保所有工具都标记为完成
        toolCalls.forEach(tool => {
          if (tool.status === "running") {
            tool.status = "completed";
            res.write(`data: ${JSON.stringify({ type: "tool_result", toolId: tool.id, content: tool.result || "已完成" })}\n\n`);
          }
        });
        res.write(`data: ${JSON.stringify({ type: "done", duration: (msg as any).duration, cost: (msg as any).cost })}\n\n`);
      }
    }

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
