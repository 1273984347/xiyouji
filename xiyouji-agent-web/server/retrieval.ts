/**
 * retrieval.ts — 检索层接入（O-4 · W1205 · D-2 批）
 *
 * 职责边界（本模块只做「检索 + 引用守卫 + 降级判定」三件事）：
 *   ① 检索适配器：把仓内现役检索实现（scripts/rag/xiyouji_rag.py）包成可注入的后端；
 *   ② 引用守卫：**每条返回给客户端的引用必须可溯源**（文件存在 + 摘录逐字出自该文件段落），
 *      不可溯源的命中一律拦截、不下发；
 *   ③ 降级判定：按架构方案 v2 §9.2 F1 的两种形态区分「同源降级」与「异源降级」。
 *
 * 契约红线：
 *   - 静态层（L2）不依赖本模块（v2 §6.6 读路径契约）：L3 不可达时静态站仍完整可用；
 *     本模块自身失败**不得**表现为整站 500，检索接口的失败降级为可枚举错误类。
 *   - 引用可溯源是不可让渡的底线：命中数 > 0 但全部不可溯源时，等价于「没有检索结果」。
 *
 * 降级两形态（v2 §9.2 F1 · W927 R-06 补注）：
 *   同源降级（same_source）：产出源未换（仍是仓内语料），只是没有生成层回答。
 *                            引用仍可溯源 ⇒ 合规降级=false。
 *   异源降级（cross_source）：产出源已换（模板/LLM 自由生成，非语料检索所得），
 *                            既不满足引用可溯源，也与「检索结果」的承诺不符。
 *                            ⇒ 必须 UI 明示 + 计入合规降级事件（complianceDegraded=true）。
 *
 * 判定点（全部落在 runRetrieval 内，逐条标注）：
 *   D1 检索层不可达        → 异源降级（cross_source）
 *   D2 无任何可溯源引用    → 异源降级（cross_source，禁止产出无据文本）
 *   D3 生成层不可用/失败   → 同源降级（same_source，引用照常下发）
 *   D4 未请求生成          → 非降级（retrieval_only）
 */
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { applyCitationGuard } from "./citationGuard.js";
import { logger } from "./logger.js";
import { LLM_API_BASE, LLM_API_KEY, LLM_MODEL, PROJECT_CWD, engineConfigured } from "./config.js";
import { streamChat } from "./engine/openai-compat.js";

/** 检索层错误码（可枚举 · v2 契约 C-4：前端按类分派，不解析文案）。 */
export const RETRIEVAL_ERROR_CODES = {
  /** 检索层不可达（索引不可达 / 解释器缺失 / 超时 / 载荷损坏）⇒ 异源降级。 */
  RETRIEVAL_UNAVAILABLE: "RETRIEVAL_UNAVAILABLE",
  /** 生成层不可用（未配置引擎 / 上游不可达）⇒ 同源降级。 */
  ANSWER_UNAVAILABLE: "ANSWER_UNAVAILABLE",
  /** 入参非法（缺检索词 / 超长）⇒ 400。 */
  BAD_QUERY: "BAD_QUERY",
} as const;

/** 同源降级时的 UI 明示文案（引用仍可溯源，仅缺生成层回答）。 */
export const SAME_SOURCE_NOTICE = "仅检索结果（未生成回答）：以下引用均可溯源到仓内语料。";

/** 异源降级时的 UI 明示文案（v2 §9.2 F1 ②：产出源已换，必须明示「这不是检索结果」）。 */
export const CROSS_SOURCE_NOTICE = "这不是检索结果：检索层不可达或无可溯源语料，当前内容并非仓内语料检索所得。";

/** 一条检索命中（尚未经引用守卫判定）。 */
export interface RetrievalHit {
  /** 仓库相对路径（正斜杠分隔）。 */
  path: string;
  /** 相关度分（BM25 加权 RRF 口径）。 */
  score: number;
  /** 语料摘录（取自命中段落，必要时带【小标题】前缀）。 */
  excerpt: string;
}

/** 一条可溯源引用（守卫通过后才存在）。 */
export interface RetrievalCitation {
  /** 仓库相对路径（正斜杠分隔）。 */
  path: string;
  /** 相关度分。 */
  score: number;
  /** 段落锚点（归一化摘录前 60 字）——定位到真源段落。 */
  anchor: string;
  /** 归一化后的摘录正文（已剥离【小标题】前缀）。 */
  excerpt: string;
  /** 命中小标题（若有）。 */
  heading: string | null;
}

/** 降级种类。 */
export type DegradationKind = "none" | "same_source" | "cross_source";

/** 检索结果模式（四态，客户端据此渲染）。 */
export type RetrievalMode = "full" | "retrieval_only" | "same_source_degraded" | "cross_source_degraded";

/** 检索结果（对外契约）。 */
export interface RetrievalOutcome {
  ok: boolean;
  query: string;
  mode: RetrievalMode;
  /** 是否处于降级态（同源/异源皆为 true）。 */
  degraded: boolean;
  /** 是否为「合规降级」——仅异源降级为 true（须计入合规降级事件）。 */
  complianceDegraded: boolean;
  /** 降级详情（未降级时为 null）。 */
  degradation: { kind: DegradationKind; reason: string; detail?: string } | null;
  /** UI 明示文案（降级时必填；非降级为 null）。 */
  notice: string | null;
  /** 通过引用守卫的命中。 */
  hits: RetrievalHit[];
  /** 通过引用守卫的引用（与 hits 一一对应，顺序一致）。 */
  citations: RetrievalCitation[];
  /** 守卫统计：检查数 / 通过数 / 拦截数。 */
  guard: { checked: number; verified: number; dropped: number };
  /** 生成层回答（仅 full 模式非空）。 */
  answer: string | null;
  elapsedMs: number;
}

/** 检索后端（可注入 ⇒ 单测不依赖 Python 进程）。 */
export interface RetrievalBackend {
  retrieve(query: string, topK: number): Promise<RetrievalHit[]>;
}

/** 生成层（可注入）。 */
export interface AnswerLayer {
  generate(query: string, hits: RetrievalHit[]): Promise<string>;
}

/** 检索层不可达（⇒ 异源降级）。 */
export class RetrievalUnavailableError extends Error {
  readonly reason: string;
  readonly detail: string | undefined;
  constructor(reason: string, detail?: string) {
    super("检索层不可达：" + reason);
    this.name = "RetrievalUnavailableError";
    this.reason = reason;
    this.detail = detail;
    Object.setPrototypeOf(this, new.target.prototype);
  }
}

/** 生成层不可用（⇒ 同源降级）。 */
export class AnswerUnavailableError extends Error {
  readonly reason: string;
  readonly detail: string | undefined;
  constructor(reason: string, detail?: string) {
    super("生成层不可用：" + reason);
    this.name = "AnswerUnavailableError";
    this.reason = reason;
    this.detail = detail;
    Object.setPrototypeOf(this, new.target.prototype);
  }
}

/** 解析 Python 解释器命令（Windows 侧 python 是静默失败存根 ⇒ 用 py -3）。 */
export function resolvePythonCommand(): string[] {
  const custom = (process.env.XIJ_RAG_PYTHON || "").trim();
  if (custom) return custom.split(/\s+/).filter(Boolean);
  return process.platform === "win32" ? ["py", "-3"] : ["python3"];
}

/** 检索 CLI 脚本路径（仓内 scripts/rag/retrieval_cli.py）。 */
export function retrievalScriptPath(cwd: string = PROJECT_CWD): string {
  return path.join(cwd, "scripts", "rag", "retrieval_cli.py");
}

/** 检索超时（毫秒）——实测缓存索引单次检索约 1.5 s，20 s 留足冷建索引余量。 */
export const RETRIEVAL_TIMEOUT_MS = Number(process.env.XIJ_RAG_TIMEOUT_MS) || 20000;

/**
 * Python 检索后端：每次请求 spawn 一次 scripts/rag/retrieval_cli.py，
 * stdout 一行 JSON ⇒ 解析成命中列表。
 *
 * 失败一律抛 RetrievalUnavailableError（携带 reason），由上层判 D1 异源降级。
 */
export function createPythonRetrievalBackend(
  opts: { cwd?: string; timeoutMs?: number; command?: string[] } = {}
): RetrievalBackend {
  const cwd = opts.cwd ?? PROJECT_CWD;
  const timeoutMs = opts.timeoutMs ?? RETRIEVAL_TIMEOUT_MS;
  const command = opts.command ?? resolvePythonCommand();
  const script = retrievalScriptPath(cwd);

  return {
    async retrieve(query: string, topK: number): Promise<RetrievalHit[]> {
      const raw = await runPythonJson(command, script, ["--query", query, "--top-k", String(topK)], timeoutMs);
      if (!raw || raw.ok !== true || !Array.isArray(raw.hits)) {
        throw new RetrievalUnavailableError("bad_payload", String(raw && raw.error ? raw.error : "载荷形状异常"));
      }
      return raw.hits as RetrievalHit[];
    },
  };
}

/** 执行 Python 脚本并解析 stdout 的单行 JSON（失败 → RetrievalUnavailableError）。 */
function runPythonJson(
  command: string[],
  script: string,
  args: string[],
  timeoutMs: number
): Promise<Record<string, unknown> | null> {
  return new Promise((resolve, reject) => {
    let child: ReturnType<typeof spawn>;
    try {
      child = spawn(command[0], [...command.slice(1), script, ...args], {
        cwd: path.dirname(path.dirname(script)),
        windowsHide: true,
        stdio: ["ignore", "pipe", "pipe"],
      });
    } catch (err) {
      reject(new RetrievalUnavailableError("python_missing", err instanceof Error ? err.message : String(err)));
      return;
    }

    let stdout = "";
    let stderr = "";
    let settled = false;
    const timer = setTimeout(() => {
      if (settled) return;
      settled = true;
      try {
        child.kill();
      } catch {
        /* 进程可能已退出 */
      }
      reject(new RetrievalUnavailableError("timeout", "检索超时 " + timeoutMs + " ms"));
    }, timeoutMs);
    if (typeof timer.unref === "function") timer.unref();

    child.stdout?.on("data", (d) => {
      stdout += String(d);
    });
    child.stderr?.on("data", (d) => {
      stderr += String(d);
    });
    child.on("error", (err) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      reject(new RetrievalUnavailableError("python_missing", err.message));
    });
    child.on("close", (code) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      if (code !== 0) {
        reject(new RetrievalUnavailableError("nonzero_exit", "退出码 " + String(code) + " · " + stderr.slice(0, 200)));
        return;
      }
      const line = stdout.trim().split(/\r?\n/).filter(Boolean).pop() || "";
      try {
        resolve(JSON.parse(line) as Record<string, unknown>);
      } catch (err) {
        reject(new RetrievalUnavailableError("bad_payload", err instanceof Error ? err.message : String(err)));
      }
    });
  });
}

/** 归一化用于匹配的文本（折叠所有空白）。 */
function normalizeForMatch(text: string): string {
  return text.replace(/\s+/g, " ").trim();
}

/** 剥掉摘录的【小标题】前缀，返回 [标题, 正文]。 */
function splitHeading(excerpt: string): [string | null, string] {
  const m = /^\u3010([^\u3011]*)\u3011\s*/.exec(excerpt);
  if (!m) return [null, excerpt.trim()];
  return [m[1].trim(), excerpt.slice(m[0].length).trim()];
}

/** 引用判定结果。 */
export interface CitationVerdict {
  verified: boolean;
  /** 未通过的原因（verified=true 时为 null）。 */
  reason: string | null;
  anchor: string;
  heading: string | null;
  excerpt: string;
}

/**
 * 引用守卫：判定一条命中是否**可溯源**（指向真源文件/段落）。
 *
 * 四道判据（任一不通过即拦截，不得下发）：
 *   ① 路径形态：相对路径、无越界（..）、必须落在真源目录（docs/ 或 source/）内；
 *   ② 文件存在且是普通文件（复用既有 citationGuard 的路径核实，复用其 unverified 判据）；
 *   ③ 摘录非空；
 *   ④ 段落级溯源：归一化后的摘录正文逐字出现在该文件内容中（防止索引与文件漂移）。
 */
export function verifyCitation(hit: RetrievalHit, cwd: string = PROJECT_CWD): CitationVerdict {
  const rel = String(hit.path || "").replace(/\\/g, "/").replace(/^\.\//, "");
  const [heading, body] = splitHeading(String(hit.excerpt || ""));
  const normalizedBody = normalizeForMatch(body);
  const anchor = normalizedBody.slice(0, 60);

  const reject = (reason: string): CitationVerdict => ({
    verified: false,
    reason,
    anchor,
    heading,
    excerpt: body,
  });

  if (!rel) return reject("empty_path");
  if (path.isAbsolute(rel) || /^[A-Za-z]:/.test(rel)) return reject("absolute_path");
  if (rel.split("/").some((seg) => seg === "..")) return reject("path_traversal");
  if (!/^(docs|source)\//.test(rel)) return reject("not_source_dir");

  const abs = path.resolve(cwd, rel);
  const rootAbs = path.resolve(cwd);
  if (abs !== rootAbs && !abs.startsWith(rootAbs + path.sep)) return reject("outside_repo");

  let stat: fs.Stats;
  try {
    stat = fs.statSync(abs);
  } catch {
    return reject("file_missing");
  }
  if (!stat.isFile()) return reject("not_a_file");

  // 复用既有引用守卫（server/citationGuard.ts）的路径核实判据：unverified 非空即未核实。
  const guarded = applyCitationGuard(rel, cwd);
  if (guarded.unverified.length > 0) return reject("path_not_found");

  if (!normalizedBody) return reject("empty_excerpt");

  let content: string;
  try {
    content = fs.readFileSync(abs, "utf-8");
  } catch {
    return reject("file_unreadable");
  }
  if (!normalizeForMatch(content).includes(normalizedBody)) return reject("excerpt_not_in_file");

  return { verified: true, reason: null, anchor, heading, excerpt: body };
}

/** 检索系统提示词（仅依据给定语料作答 + 标注来源）。 */
const RETRIEVAL_SYSTEM_PROMPT =
  "你是《详解西游记》的检索助手。只依据用户给出的语料摘录作答；" +
  "每条结论后用〔文件名〕标注来源；摘录不足以回答时直接说明「语料中未找到相关记载」；" +
  "不得凭记忆补充未在摘录中出现的内容。";

/** 构造用户消息（检索词 + 语料摘录）。 */
function buildUserMessage(query: string, hits: RetrievalHit[]): string {
  const blocks = hits.map((h, i) => "[" + String(i + 1) + "] " + h.path + "\n" + String(h.excerpt || ""));
  return "检索词：" + query + "\n\n语料摘录：\n" + blocks.join("\n\n");
}

/**
 * 生成层（OpenAI 兼容）：复用 engine/openai-compat.ts 的流式驱动，收集文本增量。
 * 未配置引擎或上游不可达 ⇒ 抛 AnswerUnavailableError（⇒ 同源降级）。
 */
export function createLlmAnswerLayer(
  opts: { timeoutMs?: number; baseUrl?: string; apiKey?: string; model?: string } = {}
): AnswerLayer {
  const timeoutMs = opts.timeoutMs ?? 30000;
  return {
    async generate(query: string, hits: RetrievalHit[]): Promise<string> {
      if (!engineConfigured()) {
        throw new AnswerUnavailableError("engine_not_configured", "未配置 LLM_API_BASE / LLM_API_KEY");
      }
      const baseUrl = opts.baseUrl ?? LLM_API_BASE;
      const apiKey = opts.apiKey ?? LLM_API_KEY;
      const model = opts.model ?? LLM_MODEL;
      let text = "";
      try {
        const stream = streamChat({
          baseUrl,
          apiKey,
          model,
          messages: [
            { role: "system", content: RETRIEVAL_SYSTEM_PROMPT },
            { role: "user", content: buildUserMessage(query, hits) },
          ],
          signal: AbortSignal.timeout(timeoutMs),
        });
        for await (const ev of stream) {
          if (ev.type === "text_delta") text += ev.delta;
        }
      } catch (err) {
        throw new AnswerUnavailableError(
          "llm_unreachable",
          err instanceof Error ? err.message.slice(0, 200) : String(err).slice(0, 200)
        );
      }
      if (!text.trim()) throw new AnswerUnavailableError("empty_answer", "生成层返回空正文");
      return text.trim();
    },
  };
}

/** 依赖注入容器（单测注入假后端，不依赖 Python 进程与 LLM）。 */
export interface RetrievalDeps {
  backend?: RetrievalBackend;
  /** 显式传 null 表示「本部署不提供生成层」⇒ 同源降级。 */
  answerLayer?: AnswerLayer | null;
  cwd?: string;
  now?: () => number;
}

/**
 * 检索主编排：检索 → 引用守卫 → 降级判定。
 *
 * 降级判定点（v2 §9.2 F1）：
 *   D1 检索层不可达       → cross_source（异源·合规降级=true）
 *   D2 无任何可溯源引用   → cross_source（异源·合规降级=true）
 *   D3 生成层不可用/失败  → same_source（同源·合规降级=false）
 *   D4 未请求生成         → retrieval_only（非降级）
 */
export async function runRetrieval(
  query: string,
  opts: { topK: number; withAnswer: boolean },
  deps: RetrievalDeps = {}
): Promise<RetrievalOutcome> {
  const now = deps.now ?? (() => Date.now());
  const cwd = deps.cwd ?? PROJECT_CWD;
  const backend = deps.backend ?? createPythonRetrievalBackend({ cwd });
  const started = now();

  // 注意：base **不含 query**——query 由各返回分支显式给出，避免与展开重复（同 key 覆盖报错）。
  const base = {
    hits: [] as RetrievalHit[],
    citations: [] as RetrievalCitation[],
    guard: { checked: 0, verified: 0, dropped: 0 },
    answer: null as string | null,
  };

  // ---- D1：检索层不可达 ⇒ 异源降级（不产出任何语料文本）----
  let rawHits: RetrievalHit[];
  try {
    rawHits = await backend.retrieve(query, opts.topK);
  } catch (err) {
    const reason = err instanceof RetrievalUnavailableError ? err.reason : "backend_error";
    const detail = err instanceof Error ? err.message.slice(0, 200) : undefined;
    logger.warn("检索层不可达（异源降级·合规降级）", {
      query,
      reason,
      detail,
      compliance_degraded: true,
      degradation: "cross_source",
    });
    return {
      ok: false,
      query,
      mode: "cross_source_degraded",
      degraded: true,
      complianceDegraded: true,
      degradation: { kind: "cross_source", reason, detail },
      notice: CROSS_SOURCE_NOTICE,
      ...base,
      elapsedMs: now() - started,
    };
  }

  // ---- 引用守卫：逐条判定，不可溯源者拦截不下发 ----
  const checked = rawHits.length;
  const hits: RetrievalHit[] = [];
  const citations: RetrievalCitation[] = [];
  for (const hit of rawHits) {
    const verdict = verifyCitation(hit, cwd);
    if (!verdict.verified) {
      logger.warn("引用不可溯源（已拦截·不下发）", {
        path: hit.path,
        reason: verdict.reason,
        query,
      });
      continue;
    }
    hits.push(hit);
    citations.push({
      path: String(hit.path).replace(/\\/g, "/"),
      score: hit.score,
      anchor: verdict.anchor,
      excerpt: verdict.excerpt,
      heading: verdict.heading,
    });
  }

  const guard = { checked, verified: citations.length, dropped: checked - citations.length };
  const answered = { ...base, hits, citations, guard };

  // ---- D4：未请求生成 ⇒ 仅检索（非降级）----
  if (!opts.withAnswer) {
    return {
      ok: true,
      query,
      mode: "retrieval_only",
      degraded: false,
      complianceDegraded: false,
      degradation: null,
      notice: null,
      ...answered,
      elapsedMs: now() - started,
    };
  }

  // ---- D2：无任何可溯源引用 ⇒ 异源降级（禁止产出无据文本）----
  if (citations.length === 0) {
    const reason = checked > 0 ? "no_traceable_citation" : "no_hit";
    logger.warn("检索无任何可溯源引用（异源降级·合规降级）", {
      query,
      reason,
      checked,
      compliance_degraded: true,
      degradation: "cross_source",
    });
    return {
      ok: false,
      query,
      mode: "cross_source_degraded",
      degraded: true,
      complianceDegraded: true,
      degradation: { kind: "cross_source", reason },
      notice: CROSS_SOURCE_NOTICE,
      ...answered,
      elapsedMs: now() - started,
    };
  }

  // ---- D3：生成层不可用/失败 ⇒ 同源降级（引用照常下发，仍可溯源）----
  const answerLayer = deps.answerLayer === undefined ? createLlmAnswerLayer() : deps.answerLayer;
  if (!answerLayer) {
    logger.warn("生成层未提供（同源降级·仅检索）", {
      query,
      reason: "answer_layer_absent",
      degradation: "same_source",
    });
    return {
      ok: true,
      query,
      mode: "same_source_degraded",
      degraded: true,
      complianceDegraded: false,
      degradation: { kind: "same_source", reason: "answer_layer_absent" },
      notice: SAME_SOURCE_NOTICE,
      ...answered,
      elapsedMs: now() - started,
    };
  }

  try {
    const answer = await answerLayer.generate(query, hits);
    return {
      ok: true,
      query,
      mode: "full",
      degraded: false,
      complianceDegraded: false,
      degradation: null,
      notice: null,
      ...answered,
      answer,
      elapsedMs: now() - started,
    };
  } catch (err) {
    const reason = err instanceof AnswerUnavailableError ? err.reason : "answer_failed";
    const detail = err instanceof Error ? err.message.slice(0, 200) : undefined;
    logger.warn("生成层不可用（同源降级·仅检索）", {
      query,
      reason,
      detail,
      degradation: "same_source",
    });
    return {
      ok: true,
      query,
      mode: "same_source_degraded",
      degraded: true,
      complianceDegraded: false,
      degradation: { kind: "same_source", reason, detail },
      notice: SAME_SOURCE_NOTICE,
      ...answered,
      elapsedMs: now() - started,
    };
  }
}
