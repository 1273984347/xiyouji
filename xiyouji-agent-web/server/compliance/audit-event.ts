/**
 * audit-event.ts — 审计事件结构（W1205 · D-3 合规批 · 架构方案 v2 §12.3）
 *
 * §12.3 原文：「每条审计事件**至少**含：ts（ISO 8601 UTC）· event_id（UUID）· actor
 * （用户/服务/批号）· action（读/写/删/权限决策/运维/销毁）· target（资源标识）·
 * decision（allow/deny）· result（ok/error）· data_class（L1–L4）· trace_id（与请求 ID
 * 关联）· source_ip。」
 *
 * **字段集只增不改**（C-7·对外契约）：既有字段（sessionId/tool/phase/kind/path/
 * command/bytes/isError/reason）一律保留，新增字段一律可选地由调用方提供、
 * 服务端派生默认值 ⇒ **存量日志行仍可解析**（老事件不失效）。
 *
 * 为什么在合规目录里而不放在 audit.ts：审计事件结构是**对外契约**（/api/audit 与
 * PG 归档共用），audit.ts 是写侧实现——契约与实现分开，契约才有唯一事实源。
 */
import { randomUUID } from "crypto";
import { DATA_CLASSES, isDataClass, type DataClass } from "./data-class.js";

/** 审计事件结构版本（只增不改 ⇒ 递增，不重排）。 */
export const AUDIT_SCHEMA_VERSION = 1;

/** 动作（§12.3：读/写/删/权限决策/运维/销毁）。 */
export type AuditAction = "read" | "write" | "delete" | "permission" | "ops" | "destroy";

/** 决策（§12.3：allow/deny）。 */
export type AuditDecision = "allow" | "deny";

/** 结果（§12.3：ok/error）。 */
export type AuditResult = "ok" | "error";

/** 缺口窗口（F10 合规降级期间审计缺失的区间）。 */
export interface AuditGap {
  /** 缺口起点（最后一次成功写入的时刻）。 */
  start: string;
  /** 缺口终点（恢复成功写入的时刻）。 */
  end: string;
  /** 期间失败次数。 */
  failures: number;
}

/** 审计事件核心字段（§12.3 的 11 个字段：10 个规定字段 + 结构版本）。 */
export interface AuditEventCore {
  /** 结构版本（只增不改）。 */
  schema_version: number;
  /** ISO 8601 UTC 时间戳。 */
  ts: string;
  /** 事件唯一标识（UUID）。 */
  event_id: string;
  /** 行为主体（用户/服务/批号）。 */
  actor: string;
  /** 动作。 */
  action: AuditAction;
  /** 目标资源标识。 */
  target: string;
  /** 决策。 */
  decision: AuditDecision;
  /** 结果。 */
  result: AuditResult;
  /** 数据分级标签（L1–L4）。 */
  data_class: DataClass;
  /** 请求关联 ID。 */
  trace_id: string;
  /** 来源 IP。 */
  source_ip: string;
}

/**
 * 完整审计事件（核心字段 + 既有兼容字段 + 缺口窗口）。
 *
 * 兼容字段全部可选：存量日志行没有它们 ⇒ 读侧必须容忍缺失（C-7）。
 */
export interface AuditEvent extends AuditEventCore {
  /** 会话 ID（既有字段）。 */
  sessionId?: string;
  /** 工具名（既有字段）。 */
  tool?: string;
  /** 留痕阶段（既有字段）。 */
  phase?: "permission" | "result";
  /** 权限分类（既有字段）。 */
  kind?: string;
  /** 目标相对路径（既有字段）。 */
  path?: string;
  /** 目标命令（既有字段）。 */
  command?: string;
  /** 写入字节数（既有字段）。 */
  bytes?: number;
  /** 执行是否报错（既有字段）。 */
  isError?: boolean;
  /** 原因（既有字段）。 */
  reason?: string;
  /** 缺口窗口（仅合规降级期间产生的补记事件带）。 */
  gap?: AuditGap;
}

/**
 * 必填字段清单（§12.3 的 11 个字段·可枚举）。
 *
 * 门禁/测试按此清单断言「新写入的事件字段齐全」，避免「以为带了其实没带」。
 */
export const AUDIT_REQUIRED_FIELDS: readonly string[] = [
  "schema_version",
  "ts",
  "event_id",
  "actor",
  "action",
  "target",
  "decision",
  "result",
  "data_class",
  "trace_id",
  "source_ip",
];

/** 新事件 ID（UUID v4）。 */
export function newEventId(): string {
  return randomUUID();
}

/**
 * 判定一个对象是否**带齐** §12.3 的 11 个必填字段（且类型正确）。
 *
 * 注意：这是「新写入事件」的判据；存量旧行只有旧字段 ⇒ 由读侧的宽松校验负责。
 */
export function isStructuredAuditEvent(value: unknown): value is AuditEvent {
  if (!value || typeof value !== "object") return false;
  const o = value as Record<string, unknown>;
  if (typeof o.schema_version !== "number") return false;
  if (typeof o.ts !== "string" || o.ts === "") return false;
  if (typeof o.event_id !== "string" || o.event_id === "") return false;
  if (typeof o.actor !== "string") return false;
  if (typeof o.action !== "string") return false;
  if (typeof o.target !== "string") return false;
  if (o.decision !== "allow" && o.decision !== "deny") return false;
  if (o.result !== "ok" && o.result !== "error") return false;
  if (!isDataClass(o.data_class)) return false;
  if (typeof o.trace_id !== "string") return false;
  if (typeof o.source_ip !== "string") return false;
  return true;
}

/**
 * 校验一条**新写入**的事件（字段齐全 + 级别合法）。
 *
 * 不合法 ⇒ 抛错（调用方按「写入失败」处理 ⇒ 走合规降级路径，不得静默落盘）。
 */
export function assertAuditEvent(event: AuditEvent): void {
  if (!isStructuredAuditEvent(event)) {
    const missing = AUDIT_REQUIRED_FIELDS.filter((f) => (event as Record<string, unknown>)[f] === undefined);
    throw new Error("审计事件字段不齐（缺 " + missing.join(",") + "）");
  }
  if (!DATA_CLASSES.includes(event.data_class)) {
    throw new Error("审计事件分级标签非法");
  }
}
