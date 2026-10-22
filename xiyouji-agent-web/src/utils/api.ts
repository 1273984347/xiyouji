/**
 * api.ts — 前端 HTTP 调用统一层（W803-D 新建；W808 全面加固）
 *
 * 职责边界：把「同一条 REST 契约」收敛成一处调用，**不含 React 状态**。
 *
 * W808 修掉的三个真实缺陷（重构前 `api.ts` 与各 hook 的实际行为）：
 *   ① **不判定 res.ok**——服务端返回 500 时，body 里的 `{ error: "..." }` 被当作
 *      成功数据返回（`await res.json()` 直接给调用方）。调用方拿到的是"成功的错误"，
 *      于是错误被静默吞掉、UI 显示为空。此为最隐蔽的一类跨边界 bug。
 *   ② **不注入 AGENT_WEB_TOKEN**——服务端一旦设置共享 token，全部 /api 请求 401，
 *      而前端毫无察觉（401 的 body 同样被当成成功数据）。
 *   ③ **基址硬编码**——相对路径 '/api' 写死在各调用点，Vite proxy 之外的部署形态
 *      （如后端独立域名）无法使用。
 *
 * W808 新增能力：
 *   - 类型化 `ApiError`（携带 status + body），失败一律 throw，**不返回"成功的错误"**；
 *   - 基址来自 `VITE_API_BASE_URL`（缺省空串 = 同源，走 Vite proxy）；
 *   - 共享 token 来自 `VITE_AGENT_WEB_TOKEN`（缺省不带）；
 *   - 204/空响应体安全处理（不因 `res.json()` 抛解析错）。
 *
 * 注意：聊天流（POST /api/chat 的 SSE 解析）不在本模块，见 src/utils/sseStream.ts。
 * 所有函数**不吞异常**：网络错误照常抛出，由调用方决定兜底文案（保持重构前各处的 catch 语义）。
 */
import type {
  ApiErrorBody,
  AuditResponse,
  CreateSessionRequest,
  CreateSessionResponse,
  FeedbackRequest,
  FeedbackResponse,
  FeedbackSummaryResponse,
  HealthResponse,
  LoginStatusResponse,
  ModelsResponse,
  PermissionResponseRequest,
  PermissionResponseResult,
  ReadyResponse,
  SessionDetailResponse,
  SessionListResponse,
  SessionMutationResponse,
  UpdateSessionRequest,
} from "./apiTypes";

/** API 基址（Vite 环境变量·缺省空串 = 同源相对路径）。 */
const BASE_URL = (import.meta.env?.VITE_API_BASE_URL as string | undefined)?.replace(/\/+$/, "") ?? "";

/** 共享 token（可选·服务端设了 AGENT_WEB_TOKEN 时前端必须带上）。 */
const AUTH_TOKEN = (import.meta.env?.VITE_AGENT_WEB_TOKEN as string | undefined) ?? "";

/**
 * 前端 API 错误：携带 HTTP 状态码与服务端响应体。
 *
 * 供调用点区分「4xx 客户端问题」与「5xx 服务端问题」——
 * 前者不该重试（skill 纪律：禁重试 4xx），后者可退避重试。
 */
export class ApiError extends Error {
  /** HTTP 状态码（网络层失败时为 0）。 */
  readonly status: number;
  /** 服务端响应体（通常是 `{ error: string }`）。 */
  readonly body: unknown;

  constructor(status: number, body: unknown, message?: string) {
    super(message ?? `API 请求失败（HTTP ${status}）`);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
    Object.setPrototypeOf(this, ApiError.prototype);
  }
}

/** 组装请求头（含共享 token 与 JSON 头）。 */
function buildHeaders(hasBody: boolean): Record<string, string> {
  const headers: Record<string, string> = {};
  if (hasBody) headers["Content-Type"] = "application/json";
  if (AUTH_TOKEN) headers["x-agent-token"] = AUTH_TOKEN;
  return headers;
}

/**
 * 解析响应体：2xx 且有内容则解析 JSON；204/空体返回 undefined。
 * 解析失败不抛——非 JSON 响应体按 undefined 处理（错误路径由状态码判定）。
 */
async function parseBody(res: Response): Promise<unknown> {
  if (res.status === 204) return undefined;
  const text = await res.text().catch(() => "");
  if (!text) return undefined;
  try {
    return JSON.parse(text) as unknown;
  } catch {
    return undefined;
  }
}

/**
 * 执行请求并归一化结果。
 *
 * - 2xx → 返回解析后的 body（无体则 undefined）；
 * - 非 2xx → 抛 ApiError（携带 status 与 body，**绝不把错误当成功数据返回**）。
 */
async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE_URL}${path}`, init);
  } catch (error) {
    // 网络层失败（后端未启动/断网）——原样抛出 TypeError，由 errorMessage.ts 归一为用户文案
    throw error;
  }

  const body = await parseBody(res);

  if (!res.ok) {
    const message =
      typeof body === "object" && body !== null && typeof (body as ApiErrorBody).error === "string"
        ? (body as ApiErrorBody).error
        : undefined;
    throw new ApiError(res.status, body, message);
  }

  return body as T;
}

/** 带 JSON 请求体的写请求（POST/PATCH/DELETE），返回解析后的 JSON。 */
export function postJson<T = unknown>(url: string, body: unknown): Promise<T> {
  return request<T>(url, {
    method: "POST",
    headers: buildHeaders(true),
    body: JSON.stringify(body),
  });
}

/** 带 JSON 请求体的 PATCH。 */
export function patchJson<T = unknown>(url: string, body: unknown): Promise<T> {
  return request<T>(url, {
    method: "PATCH",
    headers: buildHeaders(true),
    body: JSON.stringify(body),
  });
}

/** 无请求体的 DELETE。 */
export function del<T = unknown>(url: string): Promise<T> {
  return request<T>(url, { method: "DELETE", headers: buildHeaders(false) });
}

/** 无请求体的 GET。 */
export function getJson<T = unknown>(url: string): Promise<T> {
  return request<T>(url, { method: "GET", headers: buildHeaders(false) });
}

// ============= 端点封装（类型化·路径与字段名即契约） =============

export const api = {
  /** 健康检查（探活）。 */
  health: () => getJson<HealthResponse>("/api/health"),
  /** 就绪探针（W808 新增·含依赖检查）。 */
  ready: () => getJson<ReadyResponse>("/api/ready"),
  /** 引擎配置状态。 */
  checkLogin: () => getJson<LoginStatusResponse>("/api/check-login"),
  /** 可用模型列表。 */
  models: () => getJson<ModelsResponse>("/api/models"),
  /** 审计回放。 */
  audit: (limit?: number) =>
    getJson<AuditResponse>(limit === undefined ? "/api/audit" : `/api/audit?limit=${limit}`),

  /** 会话列表。 */
  listSessions: () => getJson<SessionListResponse>("/api/sessions"),
  /** 单个会话 + 消息。 */
  getSession: (sessionId: string) => getJson<SessionDetailResponse>(`/api/sessions/${sessionId}`),
  /** 新建会话。 */
  createSession: (body: CreateSessionRequest) => postJson<CreateSessionResponse>("/api/sessions", body),
  /** 更新会话。 */
  updateSession: (sessionId: string, body: UpdateSessionRequest) =>
    patchJson<SessionMutationResponse>(`/api/sessions/${sessionId}`, body),
  /** 删除会话。 */
  deleteSession: (sessionId: string) => del<SessionMutationResponse>(`/api/sessions/${sessionId}`),

  /** 提交反馈（赞/踩）。 */
  feedback: (body: FeedbackRequest) => postJson<FeedbackResponse>("/api/feedback", body),
  /** 反馈汇总。 */
  feedbackSummary: () => getJson<FeedbackSummaryResponse>("/api/feedback/summary"),

  /** 权限回执。 */
  permissionResponse: (body: PermissionResponseRequest) =>
    postJson<PermissionResponseResult>("/api/permission-response", body),
};
