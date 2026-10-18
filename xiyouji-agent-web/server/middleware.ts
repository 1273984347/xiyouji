/**
 * middleware.ts — Express 中间件装配（W803-D 自 index.ts 提取·纯搬移零语义改写）
 *
 * 职责边界：本模块只负责「请求进入路由之前」的三道关卡，按原 index.ts 的注册顺序装配：
 *   ① /api 限流（W681 · 内存桶 · 每 IP 30 req/min → 429）
 *   ② 安全响应头（与 site/_headers 一致：防点击劫持 / MIME 嗅探 / Referer 泄露）
 *   ③ 可选 token 鉴权（设置 AGENT_WEB_TOKEN 时对 /api/* 生效；未设置＝本地免认证）
 *
 * 顺序即语义：限流在鉴权之前（未授权请求同样计入配额），与重构前一致。
 * 注册条件亦保留原样——未设 token 时**不注册**鉴权中间件（而非注册一个直通件）。
 */
import type { Express, NextFunction, Request, Response } from "express";
import { AGENT_WEB_TOKEN, RATE_LIMIT_MAX, RATE_LIMIT_WINDOW_MS } from "./config.js";

/** 限流桶：ip → 窗口内计数与窗口结束时刻。 */
interface RateBucket {
  count: number;
  resetAt: number;
}

/**
 * W681 CodeQL 处置（missing-rate-limiting）：/api/* 无依赖内存限流（每 IP 30 req/min·429）。
 * 第 1 次请求开桶直接放行；桶过期即重置；超限返回 429（文案属前端可见契约）。
 */
function createRateLimiter(): (req: Request, res: Response, next: NextFunction) => void {
  const buckets = new Map<string, RateBucket>();
  const timer = setInterval(() => {
    const now = Date.now();
    for (const [ip, b] of buckets) if (now >= b.resetAt) buckets.delete(ip);
  }, RATE_LIMIT_WINDOW_MS);
  timer.unref(); // 不因清理定时器阻止进程退出（与重构前 .unref() 一致）

  return (req, res, next) => {
    const ip = req.ip || req.socket.remoteAddress || "unknown";
    const now = Date.now();
    const b = buckets.get(ip);
    if (!b || now >= b.resetAt) {
      buckets.set(ip, { count: 1, resetAt: now + RATE_LIMIT_WINDOW_MS });
      return next();
    }
    b.count += 1;
    if (b.count > RATE_LIMIT_MAX) {
      return res.status(429).json({ error: "请求过于频繁（每分钟 30 次上限），请稍后再试" });
    }
    next();
  };
}

/** 安全头（与 site/_headers 一致：防点击劫持 / MIME 嗅探 / Referer 泄露，P0-1 修复）。 */
function securityHeaders(_req: Request, res: Response, next: NextFunction): void {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
  res.setHeader("Permissions-Policy", "geolocation=(), microphone=(), camera=()");
  next();
}

/**
 * 可选认证（P0-1 修复）：设置 AGENT_WEB_TOKEN 后，所有 /api/* 需携带
 * x-agent-token 或 Authorization: Bearer <token>；未设置则保持本地免认证模式。
 */
function apiTokenAuth(req: Request, res: Response, next: NextFunction): void {
  const auth =
    String(req.headers["x-agent-token"] || "").trim() ||
    String(req.headers.authorization || "")
      .replace(/^Bearer\s+/i, "")
      .trim();
  if (auth === AGENT_WEB_TOKEN) return next();
  res.status(401).json({ error: "未授权：请在请求头携带 AGENT_WEB_TOKEN（x-agent-token 或 Authorization: Bearer）" });
}

/** 按原 index.ts 顺序装配全局中间件（限流 → 安全头 → 可选鉴权）。 */
export function installMiddleware(app: Express): void {
  app.use("/api", createRateLimiter());
  app.use(securityHeaders);
  if (AGENT_WEB_TOKEN) app.use(apiTokenAuth);
}
