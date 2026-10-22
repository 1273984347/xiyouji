/**
 * apiTypes.ts — 前后端共享的 API 契约类型（W808 新建）
 *
 * 职责边界：定义**跨边界流动**的数据形状——请求体与响应体。
 * **不含**任何业务逻辑或运行时行为（纯类型，编译后零字节）。
 *
 * 动因（W808）：重构前服务端在 routes.ts 里各自定义响应形状（如 LoginStatusResponse），
 * 前端在 hooks 里用 `(s: any)` 反推——两端各写各的，字段改名不会报错，只在运行时炸。
 * 本文件把契约收敛成**单一事实源**：服务端用它标注响应，前端用它标注 fetch 返回值，
 * 字段改名即编译期错误。
 *
 * 契约红线：字段名与 server/routes.ts 的响应形状**逐字对应**——改一处必须改两处
 * （TS 的结构类型会在编译期强制这一点）。
 */

// ============= 请求体 =============

/** POST /api/feedback 请求体。 */
export interface FeedbackRequest {
  sessionId: string;
  messageId: string;
  verdict: "up" | "down";
  comment?: string;
}

/** POST /api/sessions 请求体。 */
export interface CreateSessionRequest {
  model?: string;
  title?: string;
}

/** PATCH /api/sessions/:sessionId 请求体。 */
export interface UpdateSessionRequest {
  title?: string;
  model?: string;
}

/** POST /api/chat 请求体（SSE 流式入口）。 */
export interface ChatRequest {
  sessionId?: string | null;
  message: string;
  model?: string;
  systemPrompt?: string;
  cwd?: string;
  permissionMode?: string;
}

/** POST /api/permission-response 请求体。 */
export interface PermissionResponseRequest {
  requestId: string;
  behavior: "allow" | "deny";
  message?: string;
}

// ============= 响应体 =============

/** 服务端统一错误体形状（重构前 sendError 与 W808 全局错误处理器共用）。 */
export interface ApiErrorBody {
  error: string;
}

/** POST /api/feedback 响应体。 */
export interface FeedbackResponse {
  ok: boolean;
  inserted: number;
}

/** GET /api/feedback/summary 响应体。 */
export interface FeedbackSummaryResponse {
  ok: boolean;
  up: number;
  down: number;
}

/** GET /api/health 响应体。 */
export interface HealthResponse {
  status: string;
  timestamp: string;
}

/** GET /api/ready 响应体（W808 新增）。 */
export interface ReadyResponse {
  status: "ok" | "degraded";
  checks: Record<string, { status: "ok" | "error"; detail?: string }>;
}

/** 审计条目（GET /api/audit 的元素形状·与服务端 server/audit.ts 对应）。 */
export interface AuditEntry {
  ts: string;
  sessionId: string;
  tool: string;
  phase: "permission" | "result";
  decision: "allow" | "deny";
  kind: string;
  path?: string;
  command?: string;
  bytes?: number;
  isError?: boolean;
  reason?: string;
}

/** GET /api/audit 响应体。 */
export interface AuditResponse {
  ok: boolean;
  limit: number;
  total: number;
  skipped: number;
  entries: AuditEntry[];
}

/** GET /api/check-login 响应体（与服务端 LoginStatusResponse 对应）。 */
export interface LoginStatusResponse {
  isLoggedIn: boolean;
  method?: "env" | "none";
  envConfigured?: boolean;
  cliConfigured?: boolean;
  error?: string;
  apiKey?: string;
  envVars?: {
    apiKey?: string;
    baseUrl?: string;
    model?: string;
  };
}

/** GET /api/models 响应体。 */
export interface ModelsResponse {
  models: Array<{ modelId: string; name: string }>;
  defaultModel: string;
}

/** 会话行（GET /api/sessions 的元素·与 SQLite sessions 表对应）。 */
export interface SessionRow {
  id: string;
  title: string;
  model: string;
  sdk_session_id: string | null;
  created_at: string;
  updated_at: string;
  /** 仅列表接口附带的消息条数。 */
  messageCount?: number;
}

/** 消息行（GET /api/sessions/:id 的元素·与 SQLite messages 表对应）。 */
export interface MessageRow {
  id: string;
  session_id: string;
  role: "user" | "assistant";
  content: string;
  model: string | null;
  created_at: string;
  tool_calls: string | null;
}

/** GET /api/sessions 响应体。 */
export interface SessionListResponse {
  sessions: SessionRow[];
}

/** GET /api/sessions/:sessionId 响应体。 */
export interface SessionDetailResponse {
  session: SessionRow;
  messages: Array<Omit<MessageRow, "tool_calls"> & { tool_calls: unknown }>;
}

/** POST /api/sessions 响应体。 */
export interface CreateSessionResponse {
  session: SessionRow;
}

/** PATCH/DELETE /api/sessions/:sessionId 响应体。 */
export interface SessionMutationResponse {
  success: boolean;
}

/** POST /api/permission-response 响应体。 */
export interface PermissionResponseResult {
  success: boolean;
}
