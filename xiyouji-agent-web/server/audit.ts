// audit.ts — 写操作持久化审计（W752）。
//
// 动机：`acceptEdits` 模式下 write_file/edit_file 由权限桥自动放行，除可关闭的 console 日志
// （AGENT_WEB_VERBOSE=1）外没有任何持久化留痕——LLM 对仓库做过什么写操作事后不可复核。
// 本模块把「谁（sessionId）在哪个会话、对哪个工具/路径/命令、允许还是拒绝、结果是否出错」
// 落成一行一条 JSONL，供 `GET /api/audit` 只读回放。
//
// 三条纪律：
//  1) fail-open——审计失败（磁盘满/权限/路径非法）只 console.error，绝不把工具调用带崩；
//  2) 防自读——`data/audit.jsonl` 已进 tools.ts 的 DENY_READ，LLM 不能读回自己的操作史；
//  3) 零依赖 + 读写都不抛——只用 node 内置模块；读侧坏行/缺文件一律容忍。
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const AUDIT_READ_MAX_BYTES = 8 * 1024 * 1024; // 单次回读字节上限（只从尾部读，超大日志不撑爆内存）
const AUDIT_REASON_MAX = 200; // 原因字段截断长度
const AUDIT_COMMAND_MAX = 500; // 命令字段截断长度
const AUDIT_LIMIT_MAX = 1000; // 单次返回条数上限

/** 审计条目（JSONL 每行一条；字段名即对外契约，/api/audit 原样返回）。 */
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
}

export interface AuditReadResult {
  /** 最近 limit 条（按写入顺序，旧→新）。 */
  entries: AuditEntry[];
  /** 日志内可解析条目总数（不等于 entries.length）。 */
  total: number;
  /** 坏行（JSON 解析失败或缺关键字段）条数——容忍并计数，不抛。 */
  skipped: number;
}

/** 审计文件路径：默认 `<xiyouji-agent-web>/data/audit.jsonl`（相对本模块解析，与 cwd 无关）；
 *  `AGENT_WEB_AUDIT_LOG` 可覆盖（测试隔离 / 多实例分文件）。 */
export function auditLogPath(): string {
  const custom = (process.env.AGENT_WEB_AUDIT_LOG || "").trim();
  return custom || path.resolve(HERE, "..", "data", "audit.jsonl");
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

/** 追加一条审计（fail-open：任何异常只 console.error，不向调用方抛出——审计绝不能带崩工具调用）。 */
export function appendAudit(entry: Omit<AuditEntry, "ts"> & { ts?: string }): void {
  try {
    const file = auditLogPath();
    fs.mkdirSync(path.dirname(file), { recursive: true });
    const line = JSON.stringify({
      ts: entry.ts || new Date().toISOString(),
      sessionId: entry.sessionId ?? "",
      tool: entry.tool ?? "",
      phase: entry.phase,
      decision: entry.decision,
      kind: entry.kind,
      ...(entry.path !== undefined ? { path: entry.path } : {}),
      ...(entry.command !== undefined ? { command: entry.command } : {}),
      ...(entry.bytes !== undefined ? { bytes: entry.bytes } : {}),
      ...(entry.isError !== undefined ? { isError: entry.isError } : {}),
      ...(entry.reason ? { reason: entry.reason.slice(0, AUDIT_REASON_MAX) } : {}),
    });
    fs.appendFileSync(file, line + "\n", "utf8");
  } catch (e) {
    console.error(`[audit] 写入失败（fail-open·忽略）：${e instanceof Error ? e.message : String(e)}`);
  }
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
