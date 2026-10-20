/**
 * index.ts — API 服务器入口（W803-D 拆分后的装配层；W808 增补优雅关闭 / 就绪探针 / 全局错误处理）
 *
 * 本文件只做三件事，顺序即语义：
 *   ① 建 Express 实例、装全局中间件（middleware.ts：request ID → 限流 → 安全头 → 可选 token 鉴权 → 访问日志）
 *   ② 建进程级共享状态（待处理权限请求表·/api/chat 与 /api/permission-response 共用同一实例）
 *   ③ 注册路由并监听回环地址（P0-1：仅绑定 127.0.0.1，默认不暴露到局域网/公网）
 *
 * 拆分前本文件 646 行，混杂「配置读取 / 中间件 / 会话 CRUD / SSE 事件构造 / 权限桥 / 引擎编排」六层；
 * 现按职责分为：
 *   config.ts       启动期配置与环境事实（含默认系统提示词）
 *   http.ts         错误响应与异常消息复用层
 *   middleware.ts   request ID / 限流 / 安全头 / 可选 token 鉴权 / 访问日志
 *   routes.ts       会话 CRUD / 反馈 / 健康检查 / 就绪探针 / 审计 / 引擎配置状态 / 模型列表
 *   permissions.ts  权限桥（四模式策略）+ 挂起表 + 前端许可回执
 *   sse.ts          SSE 帧构造（事件名与数据形态即对外契约）
 *   chat.ts         POST /api/chat 流式编排
 *   errors.ts       类型化错误层级 + 全局错误处理中间件（W808 新建）
 *   logger.ts       结构化 JSON 日志 + request ID 上下文（W808 新建）
 *   requestId.ts    request ID 生成与传播（W808 新建）
 *   validation.ts   Zod 边界校验（W808 新建）
 * 对外契约（路径/方法/字段名/状态码/SSE 事件）零改动。
 */
import express from "express";
import { installMiddleware } from "./middleware.js";
import { createPendingPermissionStore } from "./permissions.js";
import { registerApiRoutes } from "./routes.js";
import { registerChatRoute } from "./chat.js";
import { errorHandler, notFoundHandler } from "./errors.js";
import { logger } from "./logger.js";
import { closeDatabase } from "./db.js";
import { registerShutdownHandlers } from "./shutdown.js";
import { PORT } from "./config.js";

const app = express();

// Middleware（含 express.json 之外的四道关卡；json 解析在最前，与重构前一致）
app.use(express.json());
installMiddleware(app);

// 进程级共享状态：待处理的权限请求（无原型对象存储·键白名单防原型污染·W536）
const pendingPermissions = createPendingPermissionStore();

registerApiRoutes(app, pendingPermissions);
registerChatRoute(app, pendingPermissions);

// W808：/api 未命中路由 → JSON 404（此前落到 Express 默认 HTML 404，前端 client 无法一致解析）。
// 注意只兜 /api——非 /api 路径仍走 Express 默认行为（保持既有语义）。
app.use("/api", notFoundHandler);

// W808：全局错误处理（必须最后注册·Express 按注册顺序匹配）。
// 运营错误按其状态码返回原始语义；编程错误记日志后返回通用 500（不泄堆栈）。
app.use(errorHandler);

// 启动服务器（P0-1 修复：仅绑定回环地址，默认不暴露到局域网/公网）
const server = app.listen(PORT, "127.0.0.1", () => {
  logger.info("API 服务器已启动", {
    port: PORT,
    host: "127.0.0.1",
    database: "SQLite (data/chat.db)",
  });
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

/**
 * W808：优雅关闭（SIGTERM / SIGINT）。
 *
 * 语义：停止接收新连接 → 关闭 HTTP server（等待在途请求完成）→ 关闭 SQLite 连接 → 退出。
 * 超时兜底：10 秒内未排空则强制退出（防挂死拖住容器停止流程）。
 */
registerShutdownHandlers({
  server,
  closeDatabase,
  log: (level, message, fields) => logger[level](message, fields),
});
