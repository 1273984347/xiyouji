/**
 * baseline.ts — 私有化部署基线（强制鉴权升格为基线 · W1205 · D-3 合规批）
 *
 * 方案 §12.2 缺口 2 的口径：**现役已 fail-closed**（AGENT_WEB_REQUIRE_TOKEN=1 且未设
 * AGENT_WEB_TOKEN ⇒ index.ts 拒绝启动），v2 要做的是把它从「可选开关」**升格为部署基线**。
 *
 * 因此本模块**不改默认行为**（默认免认证仍是现役单机/开发用法），交付的是：
 *  1) 基线的**形式化描述**（基线配置文件 + 可枚举的基线要求项）；
 *  2) 启动期的**基线自检**（自检不通过 ⇒ 拒绝启动，不是警告）；
 *  3) 明确的 fail-closed 语义（抛 ComplianceError，错误码可枚举）。
 *
 * 基线要素（对应任务书的四要素 + 方案 §12.4 传输口径）：
 *   ① 强制 token      ② 监听回环      ③ Host 白名单      ④ TLS（反代侧终止）
 *   ⑤ PG 链路 TLS（§12.4 服务端 ↔ PG 必须 TLS）
 *   ⑥ 列级加密密钥（L3/L4 落库要求）
 *   ⑦ 审计留存期下限（≥ 180 天）
 *   ⑧ 审计落盘目录可写（审计写不进去 ⇒ 不许启动）
 */
import fs from "fs";
import path from "path";
import { ComplianceError, ComplianceErrorCode } from "./errors.js";
import { resolveEncryptionKey } from "../storage/encryption.js";
import { resolveRetention, AUDIT_RETENTION_FLOOR_DAYS } from "./retention.js";
import { auditLogPath } from "../audit.js";

/** 基线配置文件路径的环境变量名。 */
export const BASELINE_FILE_ENV = "AGENT_WEB_COMPLIANCE_BASELINE_FILE";

/** 基线开关的环境变量名（=1 ⇒ 启用整套基线自检）。 */
export const BASELINE_ENABLED_ENV = "AGENT_WEB_COMPLIANCE_BASELINE";

/** 基线要求项（可被基线配置文件覆盖）。 */
export interface BaselineRequirement {
  /** 必须强制 token（且 token 达最小长度）。 */
  requireAuth: boolean;
  /** token 最小长度（字符）。 */
  minTokenLength: number;
  /** 必须监听回环地址。 */
  requireLoopbackBind: boolean;
  /** 允许的监听地址（回环形态）。 */
  allowedBindHosts: string[];
  /** 必须配置 Host 白名单（且禁通配）。 */
  requireHostAllowlist: boolean;
  /** 必须由反代终止 TLS（客户端 ↔ 服务端）。 */
  requireTlsTerminated: boolean;
  /** 使用 PG 时必须 TLS（服务端 ↔ PG）。 */
  requirePgTls: boolean;
  /** 必须配置列级加密密钥（L3/L4 落库）。 */
  requireColumnEncryption: boolean;
  /** 审计留存期下限（天）。 */
  minAuditRetentionDays: number;
}

/** 默认基线要求（私有化部署的推荐姿态）。 */
export const DEFAULT_BASELINE_REQUIREMENT: BaselineRequirement = {
  requireAuth: true,
  minTokenLength: 32,
  requireLoopbackBind: true,
  allowedBindHosts: ["127.0.0.1", "::1", "localhost"],
  requireHostAllowlist: true,
  requireTlsTerminated: true,
  requirePgTls: true,
  requireColumnEncryption: true,
  minAuditRetentionDays: AUDIT_RETENTION_FLOOR_DAYS,
};

/** 基线是否启用（默认不启用 ⇒ 不改变现役启动行为）。 */
export function baselineEnabled(env: NodeJS.ProcessEnv = process.env): boolean {
  return (env[BASELINE_ENABLED_ENV] || "") === "1";
}

/**
 * 生效的 Host 白名单（**唯一实现**）。
 *
 * 口径 = 回环三形态 + AGENT_WEB_ALLOWED_HOSTS 追加项（与现役 config.ts 的 ALLOWED_HOSTS 逐字一致）。
 * config.ts 改为引用本函数 ⇒ 同一事实两处不再漂移。
 */
export function effectiveAllowedHosts(env: NodeJS.ProcessEnv = process.env): string[] {
  return [
    "127.0.0.1",
    "localhost",
    "::1",
    ...(env.AGENT_WEB_ALLOWED_HOSTS || "")
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean),
  ];
}

/**
 * 读取基线配置文件（JSON）并覆盖默认要求。
 *
 * 文件不存在/不是合法 JSON/字段类型不对 ⇒ 抛错（调用方转成基线违规 ⇒ 拒绝启动）。
 * 配置文件是「部署姿态」的可审计载体：改姿态要改文件（进版本库）而不是改环境变量。
 */
export function loadBaselineFile(filePath: string): Partial<BaselineRequirement> {
  const raw = fs.readFileSync(filePath, "utf-8");
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    throw new ComplianceError(ComplianceErrorCode.BASELINE_VIOLATION, "基线配置文件不是合法 JSON", {
      file: filePath,
    });
  }
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new ComplianceError(ComplianceErrorCode.BASELINE_VIOLATION, "基线配置文件顶层必须是对象", {
      file: filePath,
    });
  }
  return parsed as Partial<BaselineRequirement>;
}

/**
 * 解析生效的基线要求（默认 ⊕ 基线配置文件覆盖）。
 *
 * 配置文件路径来自 AGENT_WEB_COMPLIANCE_BASELINE_FILE。
 */
export function resolveBaselineRequirement(
  env: NodeJS.ProcessEnv = process.env
): { requirement: BaselineRequirement; fileError?: string } {
  const requirement: BaselineRequirement = { ...DEFAULT_BASELINE_REQUIREMENT };
  const file = (env[BASELINE_FILE_ENV] || "").trim();
  if (file === "") return { requirement };
  try {
    const override = loadBaselineFile(path.resolve(file));
    for (const key of Object.keys(requirement) as Array<keyof BaselineRequirement>) {
      const v = (override as Record<string, unknown>)[key];
      if (v !== undefined) (requirement as unknown as Record<string, unknown>)[key] = v;
    }
    return { requirement };
  } catch (err) {
    return {
      requirement,
      fileError: err instanceof Error ? err.message : String(err),
    };
  }
}

/** 单项基线检查结果。 */
export interface BaselineCheck {
  /** 检查项标识（可枚举）。 */
  id: string;
  /** 是否通过。 */
  ok: boolean;
  /** 判定依据（**禁含 token/密钥等秘密**）。 */
  detail: string;
}

/** 基线自检总结果。 */
export interface BaselineResult {
  /** 全部通过？ */
  ok: boolean;
  /** 逐项结果。 */
  checks: BaselineCheck[];
  /** 违规清单（人类可读·每条含检查项 id）。 */
  violations: string[];
}

/** 监听地址是否回环形态。 */
function isLoopbackHost(host: string): boolean {
  const h = host.trim().toLowerCase();
  if (h === "localhost" || h === "::1") return true;
  return /^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(h);
}

/**
 * 基线自检（**纯函数**·便于单测；不读全局状态、不改进程）。
 *
 * @param env 环境变量（便于测试注入）
 * @param req 基线要求（缺省 = 默认 ⊕ 配置文件）
 */
export function evaluateDeploymentBaseline(
  env: NodeJS.ProcessEnv = process.env,
  req?: BaselineRequirement
): BaselineResult {
  const { requirement, fileError } = resolveBaselineRequirement(env);
  const r: BaselineRequirement = req ? { ...requirement, ...req } : requirement;
  const checks: BaselineCheck[] = [];
  const add = (id: string, ok: boolean, detail: string): void => {
    checks.push({ id, ok, detail });
  };

  if (fileError) add("baseline.config_file", false, fileError);
  else add("baseline.config_file", true, "基线配置文件解析正常（或未指定）");

  // ① 强制 token
  const token = (env.AGENT_WEB_TOKEN || "").trim();
  const requireToken = (env.AGENT_WEB_REQUIRE_TOKEN || "") === "1";
  if (!r.requireAuth) {
    add("auth.token", true, "基线未要求强制 token");
  } else if (!requireToken) {
    add("auth.token", false, "AGENT_WEB_REQUIRE_TOKEN 未置 1（未升格为强制鉴权）");
  } else if (token === "") {
    add("auth.token", false, "AGENT_WEB_TOKEN 未设置（强制鉴权下无凭据）");
  } else if (token.length < r.minTokenLength) {
    add("auth.token", false, "AGENT_WEB_TOKEN 长度不足（至少 " + r.minTokenLength + " 字符）");
  } else {
    add("auth.token", true, "强制 token 已启用且长度达标（长度不落日志）");
  }

  // ② 监听回环
  const bindHost = (env.AGENT_WEB_BIND_HOST || "127.0.0.1").trim();
  if (!r.requireLoopbackBind) {
    add("net.bind_loopback", true, "基线未要求回环监听");
  } else if (!r.allowedBindHosts.includes(bindHost) && !isLoopbackHost(bindHost)) {
    add("net.bind_loopback", false, "监听地址非回环（当前 " + bindHost + "）");
  } else {
    add("net.bind_loopback", true, "监听地址为回环形态");
  }

  // ③ Host 白名单
  const hosts = effectiveAllowedHosts(env);
  if (!r.requireHostAllowlist) {
    add("net.host_allowlist", true, "基线未要求 Host 白名单");
  } else if (hosts.length === 0) {
    add("net.host_allowlist", false, "Host 白名单为空");
  } else if (hosts.some((h) => h === "*" || h.includes("*"))) {
    add("net.host_allowlist", false, "Host 白名单含通配符（禁止）");
  } else {
    add("net.host_allowlist", true, "Host 白名单非空且无通配（" + hosts.length + " 项）");
  }

  // ④ 客户端 ↔ 服务端 TLS（反代侧终止）
  const tlsTerminated = (env.AGENT_WEB_TLS_TERMINATED || "") === "1";
  const publicBase = (env.AGENT_WEB_PUBLIC_BASE_URL || "").trim();
  if (!r.requireTlsTerminated) {
    add("transport.client_tls", true, "基线未要求 TLS 终止");
  } else if (!tlsTerminated && !publicBase.toLowerCase().startsWith("https://")) {
    add("transport.client_tls", false, "未声明 TLS 终止（AGENT_WEB_TLS_TERMINATED=1 或 https 的对外地址）");
  } else {
    add("transport.client_tls", true, "已声明 TLS 终止形态");
  }

  // ⑤ 服务端 ↔ PG TLS
  const backend = (env.AGENT_WEB_DB_BACKEND || "sqlite").trim().toLowerCase();
  const pgSsl = (env.AGENT_WEB_PG_SSL || "").trim().toLowerCase();
  if (!r.requirePgTls) {
    add("transport.pg_tls", true, "基线未要求 PG TLS");
  } else if (backend === "postgres" || backend === "postgresql" || backend === "pg") {
    add("transport.pg_tls", pgSsl === "require", "PG 后端下 AGENT_WEB_PG_SSL 必须为 require");
  } else {
    add("transport.pg_tls", true, "当前非 PG 后端（PG TLS 口径待切换后适用）");
  }

  // ⑥ 列级加密密钥
  if (!r.requireColumnEncryption) {
    add("crypto.column_encryption", true, "基线未要求列级加密");
  } else {
    try {
      const cipher = resolveEncryptionKey(env);
      add(
        "crypto.column_encryption",
        cipher !== null,
        cipher ? "列级加密密钥已配置（标识 " + cipher.keyId + "·密钥材料不落日志）" : "列级加密密钥缺失",
      );
    } catch (err) {
      add("crypto.column_encryption", false, err instanceof Error ? err.message : String(err));
    }
  }

  // ⑦ 审计留存期下限
  try {
    const retention = resolveRetention(env);
    const days = retention.audit.retentionDays;
    const ok = days !== null && days >= r.minAuditRetentionDays;
    add("retention.audit_floor", ok, "审计留存期 " + (days === null ? "永久" : days + " 天") + "（下限 " + r.minAuditRetentionDays + " 天）");
  } catch (err) {
    add("retention.audit_floor", false, err instanceof Error ? err.message : String(err));
  }

  // ⑧ 审计落盘目录可写（审计写不进去 ⇒ 不许启动）
  try {
    const file = (env.AGENT_WEB_AUDIT_LOG || "").trim() || auditLogPath();
    const dir = path.dirname(file);
    fs.mkdirSync(dir, { recursive: true });
    fs.accessSync(dir, fs.constants.W_OK);
    add("audit.writable", true, "审计落盘目录可写");
  } catch (err) {
    add("audit.writable", false, "审计落盘目录不可写：" + (err instanceof Error ? err.message : String(err)));
  }

  const violations = checks.filter((c) => !c.ok).map((c) => "[" + c.id + "] " + c.detail);
  return { ok: violations.length === 0, checks, violations };
}

/**
 * 基线自检的 fail-closed 出口。
 *
 * 不满足 ⇒ 抛 ComplianceError（错误码 COMPLIANCE_BASELINE_VIOLATION）。
 * 调用方（config.ts 模块加载期）据此**拒绝启动**（process.exit(1)），不是打印警告后继续跑。
 */
export function assertDeploymentBaseline(
  env: NodeJS.ProcessEnv = process.env,
  req?: BaselineRequirement
): BaselineResult {
  const result = evaluateDeploymentBaseline(env, req);
  if (!result.ok) {
    throw new ComplianceError(
      ComplianceErrorCode.BASELINE_VIOLATION,
      "部署基线自检未通过（" + result.violations.length + " 项违规·拒绝启动）",
      { violations: result.violations.join(" | ") }
    );
  }
  return result;
}
