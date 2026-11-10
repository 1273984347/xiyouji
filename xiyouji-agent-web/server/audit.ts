// audit.ts — 审计流水（结构化 · 只追加 · 合规降级可见）（W752 起 · W1205 D-3 合规批改写）
//
// 动机（沿用 W752）：acceptEdits 模式下 write_file/edit_file 由权限桥自动放行，
// 除可关闭的 console 日志外没有任何持久化留痕——LLM 对仓库做过什么写操作事后不可复核。
//
// W1205（D-3 合规批）把本模块从「单文件 JSONL + 静默 fail-open」升级为：
//  1) **结构化事件**（方案 §12.3 的 11 个必填字段 + 既有字段只增不改·C-7）；
//  2) **F10 合规降级**（§9.2）：写入失败 ⇒ 告警 + 标记「合规降级」+ 如实记录缺口窗口，
//     **不再静默**（§5.4 禁止依赖形态第 4 条：审计写失败时静默吞错且不告警）；
//  3) **只追加 + 留存期销毁**（§12.3/§12.5）：留存期内不修改；删除只允许按留存期
//     批量销毁，且**销毁动作本身写一条新事件**（销毁留证）。
//
// 四条纪律：
//  1) **审计失败绝不带崩工具调用**（fail-open 保留）——但**必须可见**：告警 + 降级标记
//     + 缺口窗口（F10：服务继续但标记「合规降级」，审计缺失期间不可补，只如实记录）；
//  2) 防自读——data/audit.jsonl 已进 tools.ts 的 DENY_READ，LLM 不能读回自己的操作史；
//  3) 零依赖 + 读写都不抛——只用 node 内置模块；读侧坏行/缺文件一律容忍；
//  4) **字段集只增不改**（C-7）——既有字段名与语义一字不动，新字段一律可选地由调用方
//     提供、服务端派生默认值 ⇒ 存量日志行仍可解析。
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import {
  AUDIT_SCHEMA_VERSION,
  newEventId,
  type AuditAction,
  type AuditDecision,
  type AuditEvent,
  type AuditGap,
  type AuditResult,
} from "./compliance/audit-event.js";
import { isDataClass, type DataClass } from "./compliance/data-class.js";
import { resolveRetention } from "./compliance/retention.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const AUDIT_READ_MAX_BYTES = 8 * 1024 * 1024; // 单次回读字节上限（只从尾部读，超大日志不撑爆内存）
const AUDIT_REASON_MAX = 200; // 原因字段截断长度
const AUDIT_COMMAND_MAX = 500; // 命令字段截断长度
const AUDIT_LIMIT_MAX = 1000; // 单次返回条数上限
const AUDIT_DEFAULT_CLASS: DataClass = "L4"; // 审计事件自身的级别（§12.1：审计事件 = L4 敏感）

/**
 * 审计条目（JSONL 每行一条；字段名即对外契约，/api/audit 原样返回）。
 *
 * 既有字段（ts/sessionId/tool/phase/decision/kind/path/command/bytes/isError/reason）
 * **逐字保留**；新增的 §12.3 字段在此为**可选**（调用方可显式给，服务端也会派生），
 * 原因：既有调用点（server/index.ts 权限桥）不被要求改签名，且存量日志行仍可解析。
 */
export interface AuditEntry {
  /** ISO 时间戳。 */
  ts: string;
  /** 会话 ID（index.ts 权限桥传入；无法归属时为空串）。 */
  sessionId: string;
  /** 工具名。 */
  tool: string;
  /** 留痕阶段：permission=权限桥决策；result=工具执行结果（含工具层拒绝）。 */
  phase: "permission" | "result";
  /** allow=放行/成功；deny=权限拒绝或工具执行报错（含受保护路径/越界/白名单/允许域拒绝）。 */
  decision: "allow" | "deny";
  /** 权限分类：read|write|command。 */
  kind: string;
  /** 目标相对路径（write_file/edit_file/read_file 等）。 */
  path?: string;
  /** 目标命令（run_command）。 */
  command?: string;
  /** 写入字节数（write_file 取输入内容长度；其余取结果文本长度）。 */
  bytes?: number;
  /** 执行结果是否报错（仅 result 阶段有意义）。 */
  isError?: boolean;
  /** 决策/拒绝原因（截断至 AUDIT_REASON_MAX）。 */
  reason?: string;
  // ---- §12.3 新增字段（只增不改·C-7；缺省由服务端派生）----
  /** 结构版本。 */
  schema_version?: number;
  /** 事件唯一标识（UUID）。 */
  event_id?: string;
  /** 行为主体（用户/服务/批号）。缺省＝会话 ID。 */
  actor?: string;
  /** 动作（读/写/删/权限决策/运维/销毁）。缺省＝按阶段与分类派生。 */
  action?: AuditAction;
  /** 目标资源标识。缺省＝路径/命令/工具名。 */
  target?: string;
  /** 结果（ok/error）。缺省＝按 isError 派生。 */
  result?: AuditResult;
  /** 数据分级标签。缺省＝L4（审计事件本身）。 */
  data_class?: DataClass;
  /** 请求关联 ID。 */
  trace_id?: string;
  /** 来源 IP。 */
  source_ip?: string;
  /** 缺口窗口（仅补记事件带）。 */
  gap?: AuditGap;
}

export interface AuditReadResult {
  /** 最近 limit 条（按写入顺序，旧→新）。 */
  entries: AuditEntry[];
  /** 日志内可解析条目总数（不等于 entries.length）。 */
  total: number;
  /** 坏行（JSON 解析失败或缺关键字段）条数——容忍并计数，不抛。 */
  skipped: number;
}

/** 审计文件路径：默认 <xiyouji-agent-web>/data/audit.jsonl（相对本模块解析，与 cwd 无关）；
 *  AGENT_WEB_AUDIT_LOG 可覆盖（测试隔离 / 多实例分文件）。 */
export function auditLogPath(): string {
  const custom = (process.env.AGENT_WEB_AUDIT_LOG || "").trim();
  return custom || path.resolve(HERE, "..", "data", "audit.jsonl");
}

/** 降级标记文件路径（与审计日志同目录）。 */
export function auditDegradationMarkerPath(): string {
  return path.join(path.dirname(auditLogPath()), "audit.degraded.json");
}

/** 合规降级状态（F10·§9.2）。 */
export interface AuditDegradationState {
  /** 当前是否处于合规降级（审计写入曾失败且尚未恢复）。 */
  degraded: boolean;
  /** 缺口窗口起点（最后一次成功写入的时刻）。 */
  gapStart: string | null;
  /** 最近一次成功写入的时刻。 */
  lastSuccessTs: string | null;
  /** 累计失败次数。 */
  failures: number;
  /** 最近一次失败原因（禁含秘密·只带错误消息）。 */
  lastError: string | null;
  /** 最近一次失败时刻。 */
  lastErrorAt: string | null;
  /** 降级标记文件路径。 */
  markerPath: string;
}

/** 进程内降级状态（模块级单例·与审计日志同生命周期）。 */
let degradation: AuditDegradationState = {
  degraded: false,
  gapStart: null,
  lastSuccessTs: null,
  failures: 0,
  lastError: null,
  lastErrorAt: null,
  markerPath: auditDegradationMarkerPath(),
};

/** 读取当前合规降级状态（供健康探针/运维查询）。 */
export function auditDegradation(): AuditDegradationState {
  return { ...degradation };
}

/** 从工具输入提取审计目标（路径/命令/写入字节数）——集中在此，避免 index.ts 各处重复取值。 */
export function auditTarget(input: Record<string, unknown> | undefined): Pick<AuditEntry, "path" | "command" | "bytes"> {
  const out: Pick<AuditEntry, "path" | "command" | "bytes"> = {};
  if (!input || typeof input !== "object") return out;
  if (typeof input.path === "string" && input.path) out.path = input.path;
  if (typeof input.command === "string" && input.command) out.command = input.command.slice(0, AUDIT_COMMAND_MAX);
  if (typeof input.content === "string") out.bytes = Buffer.byteLength(input.content, "utf8");
  return out;
}

/** 由阶段与权限分类派生动作（§12.3：读/写/删/权限决策/运维/销毁）。 */
function deriveAction(entry: AuditEntry): AuditAction {
  if (entry.action) return entry.action;
  if (entry.phase === "permission") return "permission";
  if (entry.kind === "read") return "read";
  if (entry.kind === "write") return "write";
  return "ops";
}

/** 派生目标资源标识。 */
function deriveTarget(entry: AuditEntry): string {
  if (entry.target !== undefined) return entry.target;
  if (entry.path) return entry.path;
  if (entry.command) return entry.command;
  return entry.tool || "";
}

/**
 * 由既有条目派生一条**完整**的 §12.3 事件（11 个必填字段齐全）。
 *
 * 派生失败（分级标签非法）⇒ 抛错 ⇒ 调用方按「写入失败」处理（不得静默落盘）。
 */
export function buildAuditEvent(entry: AuditEntry): AuditEvent {
  const dataClass = entry.data_class === undefined ? AUDIT_DEFAULT_CLASS : entry.data_class;
  if (!isDataClass(dataClass)) {
    throw new Error("审计事件分级标签非法（仅允许 L1/L2/L3/L4）");
  }
  const event: AuditEvent = {
    schema_version: entry.schema_version ?? AUDIT_SCHEMA_VERSION,
    ts: entry.ts || new Date().toISOString(),
    event_id: entry.event_id || newEventId(),
    actor: entry.actor ?? entry.sessionId ?? "unknown",
    action: deriveAction(entry),
    target: deriveTarget(entry),
    decision: entry.decision,
    result: entry.result ?? (entry.isError ? "error" : "ok"),
    data_class: dataClass,
    trace_id: entry.trace_id ?? "",
    source_ip: entry.source_ip ?? "",
    sessionId: entry.sessionId ?? "",
    tool: entry.tool ?? "",
    phase: entry.phase,
    kind: entry.kind,
    ...(entry.path !== undefined ? { path: entry.path } : {}),
    ...(entry.command !== undefined ? { command: entry.command } : {}),
    ...(entry.bytes !== undefined ? { bytes: entry.bytes } : {}),
    ...(entry.isError !== undefined ? { isError: entry.isError } : {}),
    ...(entry.reason ? { reason: entry.reason.slice(0, AUDIT_REASON_MAX) } : {}),
    ...(entry.gap !== undefined ? { gap: entry.gap } : {}),
  };
  return event;
}

/** 直接追加一行（不经过降级状态机；供缺口补记与销毁留证复用）。 */
function writeAuditLine(event: AuditEvent): void {
  const file = auditLogPath();
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, JSON.stringify(event) + "\n", "utf8");
}

/** 写入降级标记文件（失败也不抛——标记写不进去也要继续告警）。 */
function persistDegradationMarker(): void {
  const marker = auditDegradationMarkerPath();
  try {
    fs.mkdirSync(path.dirname(marker), { recursive: true });
    fs.writeFileSync(
      marker,
      JSON.stringify(
        {
          degraded: degradation.degraded,
          gap_start: degradation.gapStart,
          last_success_ts: degradation.lastSuccessTs,
          failures: degradation.failures,
          last_error: degradation.lastError,
          last_error_at: degradation.lastErrorAt,
          updated_at: new Date().toISOString(),
        },
        null,
        2
      ),
      "utf8"
    );
  } catch {
    /* 标记写不进去也不抛：主告警（console.error）已在别处发出 */
  }
}

/** 清除降级标记文件（恢复后）。 */
function clearDegradationMarker(): void {
  try {
    fs.rmSync(auditDegradationMarkerPath(), { force: true });
  } catch {
    /* 清不掉不影响主流程 */
  }
}

/**
 * 记录一次审计写入失败（F10·合规降级）。
 *
 * 四件事（缺一不可，否则等于「静默」）：
 *  1) console.error 告警（既有测试钉住 "[audit] 写入失败" 前缀）；
 *  2) 置「合规降级」标记（进程内 + 落标记文件⇒重启后仍可见）；
 *  3) 开/延**缺口窗口**（起点＝最后一次成功写入）；
 *  4) 缺口窗口**如实记录**（恢复时补记一条缺口事件；**期间不可补**——F10 明文）。
 */
function recordAuditFailure(message: string): void {
  const now = new Date().toISOString();
  if (!degradation.degraded) {
    degradation.degraded = true;
    degradation.gapStart = degradation.lastSuccessTs;
  }
  degradation.failures += 1;
  degradation.lastError = message;
  degradation.lastErrorAt = now;
  degradation.markerPath = auditDegradationMarkerPath();
  persistDegradationMarker();
  console.error("[audit] 写入失败（F10·合规降级·缺口窗口自 " + (degradation.gapStart || now) + " 起）：" + message);
}

/**
 * 写入成功后的恢复处理：若此前处于降级 ⇒ 补记缺口窗口事件并解除降级。
 *
 * 补记事件只陈述「窗口有多长、失败几次」，**不补造丢失的事件**（F10：缺失期间不可补）。
 */
function onAuditSuccess(event: AuditEvent): void {
  degradation.lastSuccessTs = event.ts;
  if (!degradation.degraded) return;
  const gap: AuditGap = {
    start: degradation.gapStart || event.ts,
    end: event.ts,
    failures: degradation.failures,
  };
  const evidence: AuditEvent = {
    schema_version: AUDIT_SCHEMA_VERSION,
    ts: event.ts,
    event_id: newEventId(),
    actor: "system:audit",
    action: "ops",
    target: "audit-log",
    decision: "allow",
    result: "ok",
    data_class: AUDIT_DEFAULT_CLASS,
    trace_id: event.trace_id || "",
    source_ip: event.source_ip || "",
    sessionId: "",
    tool: "audit",
    phase: "result",
    kind: "audit_gap",
    reason:
      "审计写入失败 " +
      gap.failures +
      " 次·缺口窗口 " +
      gap.start +
      " ~ " +
      gap.end +
      "（期间审计不可补·如实记录）",
    gap,
  };
  try {
    writeAuditLine(evidence);
  } catch (err) {
    // 连补记都写不进去 ⇒ 继续保持降级状态（并告警）
    console.error("[audit] 写入失败（F10·合规降级·缺口补记亦失败）：" + (err instanceof Error ? err.message : String(err)));
    return;
  }
  degradation.degraded = false;
  degradation.gapStart = null;
  degradation.failures = 0;
  degradation.lastError = null;
  degradation.lastErrorAt = null;
  clearDegradationMarker();
}

/**
 * 追加一条审计。
 *
 * fail-open 保留（审计失败绝不带崩工具调用），但**不再静默**：写入失败 ⇒ 告警 +
 * 标记「合规降级」+ 记录缺口窗口（F10·§9.2）。
 */
export function appendAudit(entry: Omit<AuditEntry, "ts"> & { ts?: string }): void {
  let event: AuditEvent;
  try {
    event = buildAuditEvent({ ...entry, ts: entry.ts || new Date().toISOString() } as AuditEntry);
  } catch (err) {
    recordAuditFailure(err instanceof Error ? err.message : String(err));
    return;
  }
  try {
    writeAuditLine(event);
  } catch (e) {
    recordAuditFailure(e instanceof Error ? e.message : String(e));
    return;
  }
  onAuditSuccess(event);
}

/** 读取最近 limit 条（旧→新）。坏行容忍；文件不存在=空；任何异常=空（绝不抛）。 */
export function readAudit(limit = 100): AuditReadResult {
  const cap = Number.isFinite(limit) && limit > 0 ? Math.min(Math.floor(limit), AUDIT_LIMIT_MAX) : 100;
  const file = auditLogPath();
  let raw = "";
  try {
    const st = fs.statSync(file);
    const start = Math.max(0, st.size - AUDIT_READ_MAX_BYTES);
    const len = st.size - start;
    const buf = Buffer.alloc(len);
    const fh = fs.openSync(file, "r");
    try {
      if (len > 0) fs.readSync(fh, buf, 0, len, start);
    } finally {
      fs.closeSync(fh);
    }
    raw = buf.toString("utf8");
    if (start > 0) {
      // 尾部读取可能截断首行——丢弃残行（坏行容忍的另一面）
      const nl = raw.indexOf("\n");
      raw = nl === -1 ? "" : raw.slice(nl + 1);
    }
  } catch {
    return { entries: [], total: 0, skipped: 0 }; // 文件不存在/不可读=空日志
  }

  const entries: AuditEntry[] = [];
  let skipped = 0;
  for (const line of raw.split("\n")) {
    const t = line.trim();
    if (!t) continue;
    try {
      const o = JSON.parse(t) as AuditEntry;
      if (!o || typeof o !== "object" || typeof o.ts !== "string" || typeof o.tool !== "string") {
        skipped += 1; // 结构不合契约=坏行
        continue;
      }
      entries.push(o);
    } catch {
      skipped += 1; // JSON 解析失败=坏行
    }
  }
  return { entries: entries.slice(-cap), total: entries.length, skipped };
}

/** 到期销毁结果。 */
export interface AuditPurgeResult {
  /** 截止时刻（早于它的被销毁）。 */
  cutoff: string;
  /** 被销毁的条数。 */
  removed: number;
  /** 保留的条数。 */
  kept: number;
  /** 审计日志路径。 */
  logPath: string;
  /** 销毁留证事件 ID。 */
  evidenceEventId: string;
}

/**
 * 按留存期批量销毁审计（**只允许这一种删除**·§12.3）。
 *
 * 语义：
 *  - 只删 ts < cutoff 的行（留存期内的一律不动 ⇒ 只追加）；
 *  - 时间不可解析的行**保留**（不擅自销毁无法判龄的数据）；
 *  - 原子替换（临时文件 + rename）⇒ 不会留下半截文件；
 *  - **销毁留证**：销毁动作本身写一条新审计事件（action=destroy）。
 */
export function purgeAuditBefore(cutoffIso: string): AuditPurgeResult {
  const file = auditLogPath();
  const cutoff = new Date(cutoffIso);
  if (Number.isNaN(cutoff.getTime())) {
    throw new Error("审计销毁截止时刻非法：" + cutoffIso);
  }
  let raw = "";
  try {
    raw = fs.readFileSync(file, "utf-8");
  } catch {
    // 文件不存在 ⇒ 无可销毁；仍写销毁留证（销毁了 0 条也是一次受控动作）
    const evidence = buildDestroyEvidence(0, 0, cutoff);
    writeAuditLine(evidence);
    return { cutoff: cutoff.toISOString(), removed: 0, kept: 0, logPath: file, evidenceEventId: evidence.event_id };
  }
  const lines = raw.split("\n").filter((l) => l.trim() !== "");
  const keptLines: string[] = [];
  let removed = 0;
  for (const line of lines) {
    let ts: string | null = null;
    try {
      const o = JSON.parse(line) as { ts?: unknown };
      if (typeof o.ts === "string") ts = o.ts;
    } catch {
      ts = null;
    }
    if (ts !== null) {
      const t = Date.parse(ts);
      if (!Number.isNaN(t) && t < cutoff.getTime()) {
        removed += 1;
        continue;
      }
    }
    keptLines.push(line);
  }
  const tmp = file + ".purge.tmp";
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(tmp, keptLines.length ? keptLines.join("\n") + "\n" : "", "utf-8");
  fs.renameSync(tmp, file);
  const evidence = buildDestroyEvidence(removed, keptLines.length, cutoff);
  writeAuditLine(evidence);
  return {
    cutoff: cutoff.toISOString(),
    removed,
    kept: keptLines.length,
    logPath: file,
    evidenceEventId: evidence.event_id,
  };
}

/** 构造销毁留证事件（action=destroy·data_class=L4）。 */
function buildDestroyEvidence(removed: number, kept: number, cutoff: Date): AuditEvent {
  return {
    schema_version: AUDIT_SCHEMA_VERSION,
    ts: new Date().toISOString(),
    event_id: newEventId(),
    actor: "system:retention",
    action: "destroy",
    target: "audit-log",
    decision: "allow",
    result: "ok",
    data_class: AUDIT_DEFAULT_CLASS,
    trace_id: "",
    source_ip: "",
    sessionId: "",
    tool: "audit",
    phase: "result",
    kind: "audit_purge",
    reason:
      "留存期到期销毁：移除 " +
      removed +
      " 条，保留 " +
      kept +
      " 条，截止 " +
      cutoff.toISOString(),
  };
}

/**
 * 按生效留存期策略销毁到期审计（§12.5：审计默认 180 天）。
 *
 * 留存期下限由 compliance/retention.ts 守住（审计 < 180 天 ⇒ 启动期就拒绝）。
 */
export function purgeExpiredAudit(nowMs: number = Date.now()): AuditPurgeResult {
  const retention = resolveRetention();
  const days = retention.audit.retentionDays;
  if (days === null) {
    throw new Error("审计留存期为永久·不可按期销毁");
  }
  const cutoff = new Date(nowMs - days * 86400000);
  return purgeAuditBefore(cutoff.toISOString());
}

/**
 * 清除进程内降级状态（运维处置完成时调用；或测试隔离用）。
 *
 * 不会删除既有日志行——降级标记只描述「审计写不进去的那段时间」。
 */
export function clearAuditDegradation(): void {
  degradation.degraded = false;
  degradation.gapStart = null;
  degradation.failures = 0;
  degradation.lastError = null;
  degradation.lastErrorAt = null;
  clearDegradationMarker();
}
