/**
 * requestId.ts — request ID 生成与传播中间件（W808 新建）
 *
 * 职责边界：为每个进入服务的请求分配（或沿用上游给的）唯一 ID，并贯穿：
 *   请求头 `X-Request-Id` → `req.requestId` → 响应头 `X-Request-Id` → 结构化日志。
 *
 * 设计取舍：
 *   ① **沿用上游 ID**：若客户端带了 `X-Request-Id`，直接沿用（跨服务链路串联时不至于断链）；
 *   ② **限长净化**：上游 ID 是不可信输入——截断到 64 字符并只保留可打印 ASCII，
 *      防日志注入（换行伪造日志行）与超长字段污染；
 *   ③ **不进响应体**：ID 只走响应头，不改既有 `{ error }` body 形状（契约红线）。
 */
import { randomUUID } from "node:crypto";
import type { NextFunction, Request, Response } from "express";
import { withRequestContext } from "./logger.js";

/** 请求 ID 头名（入站与出站同名）。 */
export const REQUEST_ID_HEADER = "X-Request-Id";

/** request ID 最大长度（超长截断·防日志污染）。 */
const MAX_REQUEST_ID_LENGTH = 64;

/**
 * 净化上游提供的 request ID：只保留可打印 ASCII（0x20-0x7E），截断到上限。
 * 非法输入（空/全非可打印）返回 undefined，由调用方生成新 ID。
 */
export function sanitizeRequestId(raw: unknown): string | undefined {
  if (typeof raw !== "string") return undefined;
  // eslint-disable-next-line no-control-regex
  const cleaned = raw.replace(/[^\x20-\x7E]/g, "").trim();
  if (!cleaned) return undefined;
  return cleaned.slice(0, MAX_REQUEST_ID_LENGTH);
}

/**
 * request ID 中间件：分配 ID → 挂到 req → 回写响应头 → 建立日志上下文。
 *
 * 注意：`withRequestContext` 包裹的是 `next()` 调用——Express 的后续处理（含异步 handler
 * 的同步段）在此上下文内运行，日志调用点无需传参即可带上 request ID。
 */
export function requestIdMiddleware(req: Request, res: Response, next: NextFunction): void {
  const incoming = req.headers[REQUEST_ID_HEADER.toLowerCase()];
  const requestId = sanitizeRequestId(Array.isArray(incoming) ? incoming[0] : incoming) ?? randomUUID();

  req.requestId = requestId;
  res.setHeader(REQUEST_ID_HEADER, requestId);

  withRequestContext(requestId, () => next());
}
