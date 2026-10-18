/**
 * index.ts — API 服务器入口（W803-D 拆分后的装配层）
 *
 * 本文件只做三件事，顺序即语义：
 *   ① 建 Express 实例、装全局中间件（middleware.ts：限流 → 安全头 → 可选 token 鉴权）
 *   ② 建进程级共享状态（待处理权限请求表·/api/chat 与 /api/permission-response 共用同一实例）
 *   ③ 注册路由并监听回环地址（P0-1：仅绑定 127.0.0.1，默认不暴露到局域网/公网）
 *
 * 拆分前本文件 646 行，混杂「配置读取 / 中间件 / 会话 CRUD / SSE 事件构造 / 权限桥 / 引擎编排」六层；
 * 现按职责分为：
 *   config.ts       启动期配置与环境事实（含默认系统提示词）
 *   http.ts         错误响应与异常消息复用层
 *   middleware.ts   限流 / 安全头 / 可选 token 鉴权
 *   routes.ts       会话 CRUD / 反馈 / 健康检查 / 审计 / 引擎配置状态 / 模型列表
 *   permissions.ts  权限桥（四模式策略）+ 挂起表 + 前端许可回执
 *   sse.ts          SSE 帧构造（事件名与数据形态即对外契约）
 *   chat.ts         POST /api/chat 流式编排
 * 对外契约（路径/方法/字段名/状态码/SSE 事件）零改动。
 */
import express from "express";
import { installMiddleware } from "./middleware.js";
import { createPendingPermissionStore } from "./permissions.js";
import { registerApiRoutes } from "./routes.js";
import { registerChatRoute } from "./chat.js";
import { PORT } from "./config.js";

const app = express();

// Middleware（含 express.json 之外的三道关卡；json 解析在最前，与重构前一致）
app.use(express.json());
installMiddleware(app);

// 进程级共享状态：待处理的权限请求（无原型对象存储·键白名单防原型污染·W536）
const pendingPermissions = createPendingPermissionStore();

registerApiRoutes(app, pendingPermissions);
registerChatRoute(app, pendingPermissions);

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
