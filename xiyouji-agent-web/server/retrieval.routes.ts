/**
 * retrieval.routes.ts — 检索层 HTTP 路由（W1205 · O-4 检索层接入）
 *
 * 对外契约：
 *   GET /api/retrieval?q=<检索词>[&k=<1..20>][&answer=0|1]
 *     200 → { ok, query, mode, degraded, complianceDegraded, degradation, notice,
 *             hits[], citations[], guard{checked,verified,dropped}, answer, elapsedMs }
 *     400 → { error }                     （缺检索词 / 超长·入参非法）
 *     503 → { error, ...同上, ok:false }  （检索层不可达或无可溯源引用 ⇒ 异源降级）
 *
 * 设计要点（v2 §6.6 读路径契约 · §5.4 禁止依赖形态 #8）：
 *   - 本路由是 L3 的**长尾**能力：静态层（L2）不依赖它，L3 不可达时静态站仍完整可用；
 *   - 检索失败**不冒泡成整站 500**：降级为可枚举的 503 + 明示文案（异源降级必须 UI 明示）；
 *   - 引用不可溯源的命中在模块层已被拦截，本路由只会看到通过守卫的引用。
 *
 * 挂载：本文件只导出注册函数，**不改 server/index.ts**（W1205 文件所有权约束）——
 *       由控制器在 index.ts 的 registerApiRoutes(app, pendingPermissions) 之后调用
 *       registerRetrievalRoutes(app) 即可接入。
 */
import type { Express, Request, Response } from "express";
import { BadRequestError } from "./errors.js";
import { logger } from "./logger.js";
import {
  RETRIEVAL_ERROR_CODES,
  RETRIEVAL_TIMEOUT_MS,
  resolvePythonCommand,
  retrievalScriptPath,
  runRetrieval,
  type RetrievalDeps,
} from "./retrieval.js";

/** 检索词长度上限（防 DoS·与 rag_server.py 的 k 钳制同量级）。 */
const MAX_QUERY_LEN = 200;
/** 返回条数上限（默认 5）。 */
const MAX_TOP_K = 20;

/** 解析并钳制 k（1..20，默认 5）。 */
function parseTopK(raw: unknown): number {
  const n = Number(raw);
  if (!Number.isFinite(n)) return 5;
  return Math.max(1, Math.min(Math.floor(n), MAX_TOP_K));
}

/** 解析 answer 开关（默认 0＝只检索，不调用生成层）。 */
function parseAnswerFlag(raw: unknown): boolean {
  const s = String(raw ?? "").trim().toLowerCase();
  return s === "1" || s === "true";
}

/** 注册检索路由。 */
export function registerRetrievalRoutes(app: Express, deps: RetrievalDeps = {}): void {
  app.get("/api/retrieval", async (req: Request, res: Response) => {
    const raw = req.query.q;
    const query = (typeof raw === "string" ? raw : Array.isArray(raw) ? String(raw[0] ?? "") : "").trim();
    if (!query) {
      throw new BadRequestError("缺少检索词 q（必填）", RETRIEVAL_ERROR_CODES.BAD_QUERY);
    }
    if (query.length > MAX_QUERY_LEN) {
      throw new BadRequestError("检索词过长（上限 " + MAX_QUERY_LEN + " 字）", RETRIEVAL_ERROR_CODES.BAD_QUERY);
    }
    const topK = parseTopK(req.query.k);
    const withAnswer = parseAnswerFlag(req.query.answer);

    const outcome = await runRetrieval(query, { topK, withAnswer }, deps);

    if (outcome.mode === "cross_source_degraded") {
      // 异源降级：产出源已换（或根本没有语料）⇒ 状态码 503 + 明示文案 + 合规降级标记。
      res.status(503).json({
        error: "检索层不可达（异源降级）：当前内容并非语料检索结果",
        ...outcome,
      });
      return;
    }
    res.json(outcome);
  });

  /**
   * 检索层配置面（无探测·只报事实）：供部署者核对「服务地址从哪来、后端走哪条命令」。
   * 不做存活性探测（探测会真跑一次检索，代价与 §6.6 的长尾定位不符）。
   */
  app.get("/api/retrieval/status", (_req: Request, res: Response) => {
    const command = resolvePythonCommand();
    logger.debug("检索层配置面查询", { backend: "python-cli" });
    res.json({
      ok: true,
      backend: "python-cli",
      command: command.join(" "),
      script: retrievalScriptPath(),
      timeoutMs: RETRIEVAL_TIMEOUT_MS,
      maxQueryLen: MAX_QUERY_LEN,
      maxTopK: MAX_TOP_K,
    });
  });
}
