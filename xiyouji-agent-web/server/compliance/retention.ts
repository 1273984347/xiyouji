/**
 * retention.ts — 留存期口径（W1205 · D-3 合规批 · 架构方案 v2 §12.5）
 *
 * 方案 §12.5 的留存期是**按数据类别**不同的：
 *   审计事件 ≥ 180 天 / 会话与消息 90 天（归档至 180 天）/ 反馈 365 天 / 公开内容永久。
 * ⇒ 留存期实现为**按类别可配**（环境变量覆盖），审计默认且**下限**为 180 天。
 *
 * 为什么审计要设「硬下限」：§12.5 写的是「≥ 180 天」，若允许用环境变量调到 30 天，
 * 那就等于把「等保通用要求」变成了一个可被随手关掉的开关。
 * ⇒ 下限是**代码常量**（要改必须改代码 ⇒ 走代码评审），不是环境变量。
 *   若备案方案另有规定，改这个常量并在方案文档里同步（留痕在版本历史里）。
 */
import { ComplianceError, ComplianceErrorCode } from "./errors.js";

/** 留存期类别（与 §12.5 的数据类别一一对应）。 */
export type RetentionCategory = "audit" | "session" | "message" | "feedback" | "content";

/** 留存期策略。 */
export interface RetentionPolicy {
  /** 类别。 */
  category: RetentionCategory;
  /** 留存天数；null = 永久（如 L1 公开内容在 Git 里不可再生）。 */
  retentionDays: number | null;
  /** 归档天数（活跃期过后仍保留的天数）；null = 无归档阶段。 */
  archiveDays: number | null;
  /** 硬下限（天）；配置低于它 ⇒ 拒绝（fail-closed）。null = 无下限。 */
  minDays: number | null;
  /** 依据（方案 §12.5 原文口径）。 */
  basis: string;
}

/** 审计留存的硬下限（天）——§12.5「审计事件 ≥ 180 天」。 */
export const AUDIT_RETENTION_FLOOR_DAYS = 180;

/** 留存期环境变量前缀（AGENT_WEB_RETENTION_<类别大写>_DAYS）。 */
export const RETENTION_ENV_PREFIX = "AGENT_WEB_RETENTION_";

/**
 * 默认留存期策略（§12.5 逐行落码）。
 *
 * 会话与消息：90 天活跃 + 归档至 180 天（§7.4 生命周期）。
 * 备份件不在此清单——备份是「全量 7 份 + WAL 14 天」（§9.5），不是按天数销毁的类别。
 */
export const RETENTION_POLICIES: Readonly<Record<RetentionCategory, RetentionPolicy>> = {
  audit: {
    category: "audit",
    retentionDays: AUDIT_RETENTION_FLOOR_DAYS,
    archiveDays: null,
    minDays: AUDIT_RETENTION_FLOOR_DAYS,
    basis: "§12.5 审计事件 ≥ 180 天（等保通用要求·以本单位定级备案与测评方案为准）",
  },
  session: {
    category: "session",
    retentionDays: 90,
    archiveDays: 180,
    minDays: 90,
    basis: "§12.5 会话与消息（L3）90 天活跃 / 归档至 180 天（§7.4 生命周期）",
  },
  message: {
    category: "message",
    retentionDays: 90,
    archiveDays: 180,
    minDays: 90,
    basis: "§12.5 会话与消息（L3）90 天活跃 / 归档至 180 天（§7.4 生命周期）",
  },
  feedback: {
    category: "feedback",
    retentionDays: 365,
    archiveDays: null,
    minDays: 365,
    basis: "§12.5 反馈（L2）365 天（用于长期质量分析）",
  },
  content: {
    category: "content",
    retentionDays: null,
    archiveDays: null,
    minDays: null,
    basis: "§12.5 公开内容（L1）永久（Git·不可再生）",
  },
};

/** 全部留存期类别（可枚举）。 */
export function retentionCategories(): RetentionCategory[] {
  return Object.keys(RETENTION_POLICIES) as RetentionCategory[];
}

/**
 * 解析生效的留存期策略（环境变量覆盖默认值）。
 *
 * 覆盖变量名：AGENT_WEB_RETENTION_AUDIT_DAYS / _SESSION_DAYS / _MESSAGE_DAYS /
 * _FEEDBACK_DAYS / _CONTENT_DAYS。
 *
 * 非法值（非法数字 / 低于硬下限）⇒ 抛 COMPLIANCE_RETENTION_INVALID（fail-closed）：
 * 留存期配错会让销毁任务删早或删晚，**必须在启动期就炸**，不能等到销毁时才发现。
 */
export function resolveRetention(env: NodeJS.ProcessEnv = process.env): Record<RetentionCategory, RetentionPolicy> {
  const out = {} as Record<RetentionCategory, RetentionPolicy>;
  for (const category of retentionCategories()) {
    const base = RETENTION_POLICIES[category];
    const raw = (env[RETENTION_ENV_PREFIX + category.toUpperCase() + "_DAYS"] || "").trim();
    if (raw === "") {
      out[category] = { ...base };
      continue;
    }
    const days = Number(raw);
    if (!Number.isFinite(days) || !Number.isInteger(days) || days <= 0) {
      throw new ComplianceError(
        ComplianceErrorCode.RETENTION_INVALID,
        "留存期配置非法（须为正整数天）",
        { category, value: raw }
      );
    }
    if (base.minDays !== null && days < base.minDays) {
      throw new ComplianceError(
        ComplianceErrorCode.RETENTION_INVALID,
        "留存期低于方案下限（拒绝启动·fail-closed）",
        { category, value: days, minDays: base.minDays }
      );
    }
    out[category] = { ...base, retentionDays: days };
  }
  return out;
}

/**
 * 留存期截止时刻（早于它即可销毁）。
 *
 * retentionDays = null（永久）⇒ 返回 null（永不销毁）。
 */
export function retentionCutoff(policy: RetentionPolicy, nowMs: number): Date | null {
  if (policy.retentionDays === null) return null;
  return new Date(nowMs - policy.retentionDays * 86400000);
}
