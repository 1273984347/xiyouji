/**
 * errors.ts — 合规错误契约（W1205 · D-3 合规批 · 架构方案 v2 §5.5 C-4）
 *
 * 为什么单独成文件：C-4 要求「服务端对外错误**分类可枚举**」。
 * 合规面会产生一批**新的**失败形态（缺分级标签、密钥缺失、解密失败、基线不满足……），
 * 若把它们混进现役 server/errors.ts 的通用错误体系，就分不清「业务错误」与
 * 「合规面拒绝」——合规拒绝必须能被调用方**按类**渲染，不能退化成 500。
 *
 * 三条纪律：
 *  1) **错误码是枚举**（ComplianceErrorCode）⇒ 可枚举、可穷举、可做门禁断言；
 *  2) **消息禁含秘密**——密钥、口令、连接串、明文业务数据一律不进 message/detail；
 *  3) **错误对象带 code**——调用方按 err.code 分支，不靠匹配消息文本（文本会变）。
 */

/** 合规错误码（可枚举 · C-4 对齐）。 */
export enum ComplianceErrorCode {
  /** 入库缺少分级标签（C-6）。 */
  DATA_CLASS_MISSING = "COMPLIANCE_DATA_CLASS_MISSING",
  /** 分级标签值非法（不在 L1–L4 枚举内）。 */
  DATA_CLASS_INVALID = "COMPLIANCE_DATA_CLASS_INVALID",
  /** 列级加密密钥缺失（基线要求 L3/L4 落库加密 ⇒ 密钥必须存在）。 */
  ENCRYPTION_KEY_MISSING = "COMPLIANCE_ENCRYPTION_KEY_MISSING",
  /** 列级加密密钥形态非法（长度/编码不对）。 */
  ENCRYPTION_KEY_INVALID = "COMPLIANCE_ENCRYPTION_KEY_INVALID",
  /** 解密失败（密钥不匹配或密文被篡改）——**不得泄露明文**。 */
  ENCRYPTION_DECRYPT_FAILED = "COMPLIANCE_DECRYPT_FAILED",
  /** 部署基线自检不通过（fail-closed ⇒ 拒绝启动）。 */
  BASELINE_VIOLATION = "COMPLIANCE_BASELINE_VIOLATION",
  /** 留存期配置非法（如审计留存期 < 180 天的下限）。 */
  RETENTION_INVALID = "COMPLIANCE_RETENTION_INVALID",
  /** 审计归档（PG）写入失败。 */
  AUDIT_ARCHIVE_FAILED = "COMPLIANCE_AUDIT_ARCHIVE_FAILED",
  /** 业务表缺少合规列（PG 侧缺迁移）——属部署缺陷。 */
  SCHEMA_OUT_OF_DATE = "COMPLIANCE_SCHEMA_OUT_OF_DATE",
}

/** 合规错误的结构化明细（**禁含秘密**：禁放密钥/口令/明文业务数据）。 */
export type ComplianceErrorDetail = Record<string, string | number | boolean | undefined>;

/**
 * 合规错误（带可枚举错误码）。
 *
 * 与现役 server/errors.ts 的 NotFoundError 等并存，互不替代：
 * 合规拒绝是「按类渲染」的一等公民，不是「内部错误」。
 */
export class ComplianceError extends Error {
  /** 可枚举错误码（对外契约）。 */
  readonly code: ComplianceErrorCode;
  /** 结构化明细（禁含秘密）。 */
  readonly detail: ComplianceErrorDetail;

  constructor(code: ComplianceErrorCode, message: string, detail: ComplianceErrorDetail = {}) {
    super(message);
    this.name = "ComplianceError";
    this.code = code;
    this.detail = detail;
  }
}

/** 判定一个异常是不是合规错误。 */
export function isComplianceError(err: unknown): err is ComplianceError {
  return err instanceof ComplianceError;
}

/**
 * 全部合规错误码（可枚举清单）。
 *
 * 供门禁/测试穷举比对用：新增错误码若忘了登记，这里会露出来。
 */
export function complianceErrorCodes(): ComplianceErrorCode[] {
  return Object.values(ComplianceErrorCode);
}

/**
 * 合规错误的 HTTP 语义映射（供路由层渲染用）。
 *
 * 口径：**数据类拒绝是 400（请求不合契约）**，基线/部署类拒绝是 503（服务不具备运行基线）。
 * 不映射成 500——500 会让前端把「配置缺失」显示成「服务端炸了」，掩盖部署缺陷。
 */
export function complianceHttpStatus(code: ComplianceErrorCode): 400 | 503 {
  switch (code) {
    case ComplianceErrorCode.DATA_CLASS_MISSING:
    case ComplianceErrorCode.DATA_CLASS_INVALID:
      return 400;
    default:
      return 503;
  }
}
