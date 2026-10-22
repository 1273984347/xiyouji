/**
 * types.ts — Express 请求类型增补（W808 新建）
 *
 * 职责边界：给 `Express.Request` 增补 `requestId` 字段。
 *
 * 动因：request ID 由 requestId.ts 中间件挂载（见 server/requestId.ts），
 * 但 Express 的 Request 类型不含该字段——用声明合并补齐，使 `req.requestId`
 * 在 logger / errorHandler / 路由层均有类型支撑（避免 `any` 逃逸）。
 *
 * 命名说明：文件名为 `types.ts` 而非 `express.d.ts`——仓内 .gitignore 忽略
 * `xiyouji-agent-web/server/*.d.ts`（tsc 编译产物面），声明文件会被误排除；
 * 改用普通 `.ts` 模块（`declare global` 在模块文件内同样生效）以确保入库。
 */
import "express";

declare global {
  namespace Express {
    interface Request {
      /**
       * 本次请求的唯一 ID（W808 新增）。
       * 由 requestIdMiddleware 挂载；未经过该中间件时为 undefined。
       */
      requestId?: string;
    }
  }
}

export {};
