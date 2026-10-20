/**
 * errors.ts — 类型化错误层级（W808 新建）
 *
 * 职责边界：定义「业务可预期的失败」的统一表达，并提供全局错误处理中间件。
 * **不判断业务语义**（哪个路由该报哪个错由路由层决定），只提供「怎么表达 + 怎么序列化」。
 *
 * 动因（W808）：重构前 server/ 各路由用裸字符串 `sendError(res, 400, "invalid body")` 表达失败，
 * 错误信息与状态码在 14 处散落、无法集中治理，且缺少 request ID 回溯链路。W808 起：
 *   ① 失败以类型化错误类表达（NotFound / Validation / Unauthorized / …），语义与状态码绑定；
 *   ② 全局错误处理中间件统一序列化——运营错误（isOperational）结构化返回原始语义，
 *      编程错误（未知异常）只记日志并返回通用 500，**绝不把堆栈泄给客户端**。
 *
 * 契约红线（对外响应形状）：
 *   运营错误 → `{ error: string }`（与重构前 sendError 的形状一致，**键名与取值零改动**）；
 *   编程错误 → `{ error: "服务器内部错误" }`（不泄细节·与重构前各路由 catch 的兜底文案语义一致）。
 *   框架层 4xx（W813 修）→ `{ error: string }` + **原状态码**（此前被误降为 500，见下）。
 *   request ID 经 `X-Request-Id` 响应头透出（不塞进 body，避免改变既有 body 形状）。
 *
 * W813 修（契约回归）：`express.json()` 的请求体解析失败抛的是 SyntaxError
 * （body-parser 附带 status=400），既非 AppError 也无 isOperational 语义，
 * 此前被本文件的错误收敛逻辑归入「编程错误」分支 → 客户端收到 **500** +「服务器内部错误」，
 * 而重构前（无全局错误处理器）Express 默认处理器返回的是 **400**。
 * 即：W808 新增全局错误处理器的瞬间，把一类客户端错误升格成了服务端故障——
 * 前端据此把「请求体畸形」误判为「服务端出错，请稍后重试」并可能重试（errorMessage.ts
 * 的 isRetryable 对 5xx 判 true、对 4xx 判 false）。
 * 现改为：异常自带 4xx 状态码即按该状态码返回，文案用固定表（不回显原始解析消息·防细节外泄）。
 */
import type { NextFunction, Request, Response } from "express";
import { logger } from "./logger.js";

/** 错误基类：所有可预期的业务失败都继承它。 */
export class AppError extends Error {
  /** 机器可读错误码（前端可据此分派，不解析文案）。 */
  readonly code: string;
  /** HTTP 状态码。 */
  readonly statusCode: number;
  /** 是否为「运营错误」——true 表示可安全地把 message 返回给客户端。 */
  readonly isOperational: boolean;
  /** 附加的结构化上下文（记日志用·不进响应体）。 */
  readonly meta?: Record<string, unknown>;

  constructor(
    message: string,
    code: string,
    statusCode: number,
    isOperational = true,
    meta?: Record<string, unknown>
  ) {
    super(message);
    this.name = new.target.name;
    this.code = code;
    this.statusCode = statusCode;
    this.isOperational = isOperational;
    this.meta = meta;
    // 修正原型链（ES2020 target 下继承内置 Error 需显式修正，否则 instanceof 可能失效）
    Object.setPrototypeOf(this, new.target.prototype);
  }
}

/** 资源不存在（404）。 */
export class NotFoundError extends AppError {
  constructor(resource: string, id?: string) {
    super(id ? `${resource}不存在：${id}` : `${resource}不存在`, "NOT_FOUND", 404);
  }
}

/**
 * 入参校验失败（默认 422）——由 Zod 边界校验产出。
 *
 * 状态码可覆盖：若某端点已有**文档化的既有契约**（如 /api/feedback 的 `400 invalid body`），
 * 调用方传 statusCode 保持对外契约零改动（见 server/validation.ts 的 parseBody 第三参）。
 */
export class ValidationError extends AppError {
  /** 字段级错误明细（前端可定位到具体表单项）。 */
  readonly fields: Array<{ path: string; message: string }>;

  constructor(
    fields: Array<{ path: string; message: string }>,
    message = "请求参数校验失败",
    statusCode = 422
  ) {
    super(message, "VALIDATION_ERROR", statusCode, true, { fields });
    this.fields = fields;
  }
}

/** 未认证（401）——缺失或错误的共享 token。 */
export class UnauthorizedError extends AppError {
  constructor(message = "未授权：请求缺少有效的访问凭据") {
    super(message, "UNAUTHORIZED", 401);
  }
}

/** 已认证但无权限（403）。 */
export class ForbiddenError extends AppError {
  constructor(message = "无权访问该资源") {
    super(message, "FORBIDDEN", 403);
  }
}

/** 与既有资源冲突（409）。 */
export class ConflictError extends AppError {
  constructor(message = "与既有资源冲突") {
    super(message, "CONFLICT", 409);
  }
}

/** 触发限流（429）。 */
export class RateLimitError extends AppError {
  constructor(message = "请求过于频繁，请稍后再试") {
    super(message, "RATE_LIMITED", 429);
  }
}

/**
 * 业务失败（400）——语义良好但请求本身不合法。
 * 与 ValidationError 的分工：本类用于「单个字段值非法」且字段级明细无意义时
 * （如引擎未配置、工作目录越界）；字段级明细有意义时用 ValidationError（422）。
 */
export class BadRequestError extends AppError {
  constructor(message: string, code = "BAD_REQUEST") {
    super(message, code, 400);
  }
}

/**
 * 把任意异常收敛为「可安全返回给客户端」的形状。
 *
 * @param err 捕获到的异常
 * @returns 状态码 + 响应体（body 形状恒为 `{ error: string }`）
 */
export function toErrorResponse(err: unknown): { statusCode: number; body: { error: string } } {
  if (err instanceof AppError && err.isOperational) {
    return { statusCode: err.statusCode, body: { error: err.message } };
  }
  // W813 修：框架层 4xx 保真——express.json() 的请求体解析失败抛的是 SyntaxError
  // （body-parser 附带 status=400），不是 AppError。此前本函数只认 AppError，
  // 于是这类**客户端错误**被归入「编程错误」分支返回 500 + 通用文案，
  // 违反本文件既有的「对外契约零改动」红线（重构前 Express 默认处理器返 400）。
  // 判据：异常自带 4xx 状态码（body-parser / 框架层错误）→ 按该状态码返回，
  // 但**仍不泄细节**（客户端错误的具体文案由服务端固定，不回显原始异常消息）。
  const frameworkStatus = frameworkErrorStatus(err);
  if (frameworkStatus !== null) {
    return { statusCode: frameworkStatus, body: { error: FRAMEWORK_ERROR_MESSAGES[frameworkStatus] ?? "请求内容有误" } };
  }
  // 编程错误：兜底 500 + 通用文案（细节只进日志）
  return { statusCode: 500, body: { error: "服务器内部错误" } };
}

/**
 * 从异常对象上取「框架层 4xx 状态码」。
 *
 * body-parser 的错误对象带 `status` / `statusCode` 属性（400 = 请求体解析失败、
 * 413 = 请求体过大、415 = 不支持的 Content-Type）。Express 4/5 均如此。
 *
 * 只认 4xx：5xx 属服务端问题，一律走 500 通用文案（不把内部状态码直接外泄）。
 *
 * @param err 捕获到的异常
 * @returns 4xx 状态码；非框架层 4xx 返回 null
 */
function frameworkErrorStatus(err: unknown): number | null {
  if (typeof err !== "object" || err === null) return null;
  const candidate = err as { status?: unknown; statusCode?: unknown };
  for (const value of [candidate.status, candidate.statusCode]) {
    if (typeof value === "number" && Number.isInteger(value) && value >= 400 && value <= 499) {
      return value;
    }
  }
  return null;
}

/** 框架层 4xx 的固定文案（不回显原始异常消息·防细节外泄）。 */
const FRAMEWORK_ERROR_MESSAGES: Record<number, string> = {
  400: "请求内容格式有误，无法解析",
  413: "请求内容过大",
  415: "不支持的请求内容类型",
};

/**
 * 全局错误处理中间件：Express 错误处理四参签名（`next` 必传，否则 Express 不会识别为错误处理器）。
 *
 * 行为：
 *   - 运营错误 → 按其 statusCode 返回原始语义文案（对前端而言与重构前逐字一致）；
 *   - 框架层 4xx（W813 新增：body-parser 请求体解析失败等）→ 按其状态码返回固定文案
 *     并记 warn 级日志（客户端问题，不是编程错误，不记堆栈）；
 *   - 编程错误 → 记 error 级结构化日志（含 request ID 与堆栈）后返回通用 500；
 *   - 响应已发出（SSE 流中途抛错）→ 只记日志，不再尝试写响应体（避免 ERR_HTTP_HEADERS_SENT）。
 */
export function errorHandler(err: unknown, req: Request, res: Response, next: NextFunction): void {
  if (res.headersSent) {
    logger.error("请求处理失败（响应已发出·仅记日志）", {
      request_id: req.requestId,
      method: req.method,
      path: req.originalUrl,
      error: err instanceof Error ? err.message : String(err),
      stack: err instanceof Error ? err.stack : undefined,
    });
    next(err);
    return;
  }

  const { statusCode, body } = toErrorResponse(err);
  const isOperational = err instanceof AppError && err.isOperational;
  // W813：框架层 4xx 单列——客户端问题（请求体畸形/过大/类型不支持），
  // 与「运营错误」同类（都是 4xx）但不是本项目定义的语义错误，故记 warn 不记堆栈。
  const isFrameworkClientError = !isOperational && frameworkErrorStatus(err) !== null;

  if (isOperational) {
    logger.warn("请求被拒绝（运营错误）", {
      request_id: req.requestId,
      method: req.method,
      path: req.originalUrl,
      status: statusCode,
      code: (err as AppError).code,
      error: err instanceof Error ? err.message : String(err),
    });
  } else if (isFrameworkClientError) {
    logger.warn("请求被拒绝（框架层客户端错误）", {
      request_id: req.requestId,
      method: req.method,
      path: req.originalUrl,
      status: statusCode,
      error: err instanceof Error ? err.message : String(err),
    });
  } else {
    logger.error("请求处理失败（编程错误）", {
      request_id: req.requestId,
      method: req.method,
      path: req.originalUrl,
      status: statusCode,
      error: err instanceof Error ? err.message : String(err),
      stack: err instanceof Error ? err.stack : undefined,
    });
  }

  res.status(statusCode).json(body);
}

/**
 * 404 兜底中间件：未命中任何路由的 /api 请求。
 * 与 Express 默认的 HTML 404 不同——本项目统一走 JSON 契约，前端 client 才能一致解析。
 */
export function notFoundHandler(req: Request, res: Response): void {
  res.status(404).json({ error: `接口不存在：${req.method} ${req.path}` });
}
