/**
 * http.ts — HTTP 响应构造复用层（W803-D 新建·收敛 index.ts 内重复的错误响应骨架）
 *
 * 职责边界：只负责「把错误/响应写成既有对外形状」，**不判断业务语义**。
 * 收敛动因：重构前 server/index.ts 在 12 处手写 `res.status(4xx).json({ error: … })`
 * 与 6 处手写 `error?.message || "…失败"` 兜底文案；字段名/状态码属对外契约，
 * 集中一处可保证所有分支形状一致。
 *
 * 契约红线：`{ error, ...extra }` 的键序与取值必须与手写版逐字等价——
 * 前端按字段名取值，故键序不敏感，但**取值与状态码零容忍**。
 */
import type { Response } from "express";

/**
 * 统一错误响应：`res.status(status).json({ error, ...extra })`。
 * extra 用于既有带附加字段的分支（如保存消息失败的 `detail`），未传时响应体恰为 `{ error }`。
 */
export function sendError(
  res: Response,
  status: number,
  error: string,
  extra?: Record<string, unknown>
): void {
  res.status(status).json(extra ? { error, ...extra } : { error });
}

/**
 * 取异常的可读消息：`unknown` 笼统捕获下的既有口径 `error?.message || fallback`。
 * （重构前各 catch 块写作 `error: any` + 可选链取值；此处保持同一回落语义。）
 */
export function errorMessage(error: unknown, fallback: string): string {
  const message = (error as { message?: unknown } | null | undefined)?.message;
  return typeof message === "string" && message ? message : fallback;
}
