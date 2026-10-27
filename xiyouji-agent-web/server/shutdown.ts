/**
 * shutdown.ts — 优雅关闭（W808 新建）
 *
 * 职责边界：把「停止接收新连接 → 等待在途请求 → 关闭数据库 → 退出」这套流程
 * 收敛成**可单测**的一个单元，与信号注册分离。
 *
 * 动因（W808）：重构前 server/index.ts 只有 `app.listen(...)`——进程收到 SIGTERM 时
 * 直接被杀死，SSE 流被硬切、SQLite 连接不关（WAL 未 checkpoint 留残余文件）。
 *
 * 平台说明（重要·双平台断言纪律）：
 *   Windows 上 `child.kill('SIGTERM')` 与 `process.kill(pid, 'SIGTERM')` 都是
 *   **无条件终止**（Node 文档：Windows 无信号语义，SIGTERM/SIGINT/SIGKILL 一律
 *   TerminateProcess），故 Windows 下**本模块的信号处理器根本不会被触发**——
 *   这是操作系统限制而非实现缺陷。真实执行位=CI（Linux）+ Docker 部署面。
 *   故本模块把关闭流程抽成可直接调用的 `gracefulShutdown()`（跨平台可测），
 *   信号注册只是它的一个薄封装。
 */
import type { Server } from "node:http";

/** 关闭流程的依赖（结构化注入·便于单测替身化）。 */
export interface GracefulShutdownDeps {
  /** HTTP server（用于停止接收新连接并等待在途请求）。 */
  server: Pick<Server, "close">;
  /** 关闭数据库连接（SQLite：WAL checkpoint + close；PG：连接池关闭）。
   *  W934：存储层抽象后可为异步（PG 池关闭是 Promise）⇒ 类型放宽并 await。 */
  closeDatabase: () => void | Promise<void>;
  /** 记录关闭过程的日志出口。 */
  log: (level: "info" | "error", message: string, fields?: Record<string, unknown>) => void;
  /** 退出码回调（默认 process.exit·单测可替身化）。 */
  exit?: (code: number) => void;
  /** 强制退出超时（毫秒·默认 10s）。 */
  timeoutMs?: number;
}

/** 强制退出超时默认值（10 秒·防挂死拖住容器停止流程）。 */
export const SHUTDOWN_FORCE_TIMEOUT_MS = 10_000;

/**
 * 执行优雅关闭：停服 → 关库 → 退出。
 *
 * @returns 退出码（0 = 正常，1 = 关闭过程出错或超时）
 */
export async function gracefulShutdown(
  signal: string,
  deps: GracefulShutdownDeps
): Promise<number> {
  const {
    server,
    closeDatabase,
    log,
    exit = (code: number) => process.exit(code),
    timeoutMs = SHUTDOWN_FORCE_TIMEOUT_MS,
  } = deps;

  log("info", "收到关闭信号，开始优雅关闭", { signal });

  // 强制退出兜底：超时未排空则强制退出（防挂死拖住容器停止流程）
  const forceTimer = setTimeout(() => {
    log("error", "优雅关闭超时，强制退出", { signal, timeout_ms: timeoutMs });
    exit(1);
  }, timeoutMs);
  forceTimer.unref(); // 不因该定时器阻止进程退出

  try {
    // 停止接收新连接并等待在途请求结束
    await new Promise<void>((resolve, reject) => {
      server.close((err) => (err ? reject(err) : resolve()));
    });
    // 关闭数据库连接（WAL 模式需 checkpoint，避免留下未落盘的 WAL）
    // W934：可能是 Promise（PG 池关闭）⇒ 必须 await，否则进程会在池关闭前就 exit
    await closeDatabase();
    log("info", "优雅关闭完成", { signal });
    clearTimeout(forceTimer);
    exit(0);
    return 0;
  } catch (error) {
    log("error", "优雅关闭失败", {
      signal,
      error: error instanceof Error ? error.message : String(error),
    });
    clearTimeout(forceTimer);
    exit(1);
    return 1;
  }
}

/**
 * 注册信号处理器（SIGTERM / SIGINT）。
 *
 * 幂等：重复信号只触发一次关闭流程（避免并发关闭导致「关闭两次」类竞态）。
 */
export function registerShutdownHandlers(deps: GracefulShutdownDeps): void {
  let shuttingDown = false;
  const handle = (signal: string) => {
    if (shuttingDown) return;
    shuttingDown = true;
    void gracefulShutdown(signal, deps);
  };
  process.on("SIGTERM", () => handle("SIGTERM"));
  process.on("SIGINT", () => handle("SIGINT"));
}
