/**
 * logger.ts — 结构化 JSON 日志（W808 新建）
 *
 * 职责边界：唯一的日志出口——把「事件 + 字段」序列化成一行 JSON 写到 stdout/stderr。
 * **不决定记什么**（调用点决定），只负责格式化与级别路由。
 *
 * 动因（W808）：重构前 server/ 用裸 `console.log` / `console.error` 记日志，共 20+ 处，
 * 文本不可解析、无法按 request 回溯、级别缺失。W808 起统一为结构化 JSON：
 *   { level, msg, ts, request_id?, ...fields }
 *
 * 三条纪律：
 *   ① 级别路由——error/warn → stderr；info/debug → stdout（便于容器侧分流采集）；
 *   ② 脱敏——字段键命中 PASSWORD/TOKEN/SECRET/KEY/API_KEY 等模式时，值一律替换为
 *      `***`（W412 遗留纪律：绝不把凭证写进日志）；
 *   ③ 永不抛错——日志失败绝不能带崩业务（与 audit.ts 的 fail-open 纪律一致）。
 */
import { AsyncLocalStorage } from "node:async_hooks";

/** 日志级别（与常见 JSON 日志约定一致）。 */
export type LogLevel = "error" | "warn" | "info" | "debug";

/** 单条日志的字段集合（除固定键外均可自由扩展）。 */
export type LogFields = Record<string, unknown>;

/** 级别序——数值越大越严重。 */
const LEVEL_WEIGHT: Record<LogLevel, number> = { error: 0, warn: 1, info: 2, debug: 3 };

/** 运行期允许输出的最低级别（debug 默认关闭——与重构前 VERBOSE_LOG 的收敛纪律一致）。 */
const MIN_LEVEL: LogLevel =
  process.env.AGENT_WEB_LOG_LEVEL === "debug"
    ? "debug"
    : process.env.AGENT_WEB_LOG_LEVEL === "info"
      ? "info"
      : process.env.AGENT_WEB_LOG_LEVEL === "warn"
        ? "warn"
        : process.env.AGENT_WEB_LOG_LEVEL === "error"
          ? "error"
          : "info";

/** 需脱敏的字段键（大小写不敏感的子串匹配）。 */
const SECRET_KEY_PATTERN = /(password|passwd|token|secret|apikey|api_key|authorization|credential|cookie)/i;

/** 脱敏后的占位值。 */
const REDACTED = "***";

/**
 * 请求上下文存储：让日志调用点无需层层传参即可带上当前 request ID。
 * （SSE 流式响应跨越多个异步回调，正是 AsyncLocalStorage 的适用面。）
 */
const requestContext = new AsyncLocalStorage<{ requestId: string }>();

/**
 * 在给定上下文内执行回调——期间所有 logger 调用自动携带 request ID。
 */
export function withRequestContext<T>(requestId: string, fn: () => T): T {
  return requestContext.run({ requestId }, fn);
}

/** 取当前上下文的 request ID（无上下文时返回 undefined）。 */
export function currentRequestId(): string | undefined {
  return requestContext.getStore()?.requestId;
}

/** 脱敏：命中密钥模式的字段值替换为 `***`（递归处理嵌套对象/数组）。 */
function redact(value: unknown, depth = 0): unknown {
  if (depth > 4) return value;
  if (Array.isArray(value)) return value.map((v) => redact(v, depth + 1));
  if (value && typeof value === "object") {
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
      out[k] = SECRET_KEY_PATTERN.test(k) ? REDACTED : redact(v, depth + 1);
    }
    return out;
  }
  return value;
}

/** 序列化一行日志并写到对应流（永不抛错）。 */
function emit(level: LogLevel, msg: string, fields?: LogFields): void {
  try {
    if (LEVEL_WEIGHT[level] > LEVEL_WEIGHT[MIN_LEVEL]) return;

    // 固定键顺序：level / ts / msg 在前，request_id 紧随其后（便于日志侧按前缀过滤）
    const record: Record<string, unknown> = {
      level,
      ts: new Date().toISOString(),
      msg,
    };
    const rid = fields?.request_id ?? currentRequestId();
    if (rid) record.request_id = rid;

    if (fields) {
      for (const [k, v] of Object.entries(fields)) {
        if (k === "request_id") continue; // 已在上方处理（显式值优先于上下文值）
        record[k] = redact(v);
      }
    }

    const line = JSON.stringify(record);
    if (level === "error" || level === "warn") process.stderr.write(line + "\n");
    else process.stdout.write(line + "\n");
  } catch {
    // 日志失败绝不外抛（fail-open：日志不得带崩业务）
  }
}

/** 结构化日志器（单例·全进程共用）。 */
export const logger = {
  error(msg: string, fields?: LogFields): void {
    emit("error", msg, fields);
  },
  warn(msg: string, fields?: LogFields): void {
    emit("warn", msg, fields);
  },
  info(msg: string, fields?: LogFields): void {
    emit("info", msg, fields);
  },
  debug(msg: string, fields?: LogFields): void {
    emit("debug", msg, fields);
  },
  /** 是否会输出该级别（供调用点省掉昂贵的字段构造）。 */
  enabled(level: LogLevel): boolean {
    return LEVEL_WEIGHT[level] <= LEVEL_WEIGHT[MIN_LEVEL];
  },
};

export default logger;
