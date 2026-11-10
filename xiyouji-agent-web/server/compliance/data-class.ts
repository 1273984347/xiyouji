/**
 * data-class.ts — 数据分级四级目录（W1205 · D-3 合规批 · 架构方案 v2 §12.1）
 *
 * **本文件是分级标签的唯一事实源**（单一事实源要求）：枚举、判定标准、本项目落点、
 * 存储要求、传输要求、默认留存期、以及「本项目的资源种类 → 级别」映射，全部在此。
 * 别处（文档 / SQL / 测试 / 路由）都**引用**本文件，不得另抄一份——
 * 抄第二份就会漂移（这正是仓内反复出现的「同一事实多副本」教训）。
 *
 * 四级（方案 §12.1 原文口径）：
 *   L1 公开 / L2 内部 / L3 受限 / L4 敏感
 *
 * 与既有资产的关系：
 *  - PG 侧 audit_archive.data_class 的 CHECK 约束就是 IN (L1,L2,L3,L4)（0001 基线已建）；
 *  - 业务表的 data_class 列由本目录的 RESOURCE_CLASS 推导默认值（见 schema.ts）。
 */
import { ComplianceError, ComplianceErrorCode } from "./errors.js";

/** 数据分级级别（四级 · §12.1）。 */
export type DataClass = "L1" | "L2" | "L3" | "L4";

/** 全部级别（有序 · 由低到高）。 */
export const DATA_CLASSES: readonly DataClass[] = ["L1", "L2", "L3", "L4"];

/** 级别规格（§12.1 一行一列的机器可读形态）。 */
export interface DataClassSpec {
  /** 级别标识。 */
  level: DataClass;
  /** 名称（公开/内部/受限/敏感）。 */
  name: string;
  /** 判定标准（§12.1 原义）。 */
  criteria: string;
  /** 本项目落点（§12.1 原义）。 */
  projectScope: string[];
  /** 存储要求（§12.1 原义）。 */
  storage: string;
  /** 传输要求（§12.1 原义）。 */
  transmission: string;
  /** 该级是否要求列级加密（§12.4：PG 静态数据 L3/L4 列级加密）。 */
  columnEncryptionRequired: boolean;
  /** 该级是否要求只追加（§12.1：L4 加密存储 + 只追加）。 */
  appendOnlyRequired: boolean;
  /** 默认留存期天数（§12.5）；null = 永久（如 L1 公开内容在 Git 里不可再生）。 */
  defaultRetentionDays: number | null;
}

/**
 * 分级目录（**唯一事实源**）。
 *
 * 字段逐字对齐方案 §12.1 的表格；改这里 = 改口径，须同步更新方案文档与迁移文件。
 */
export const DATA_CLASS_CATALOG: Readonly<Record<DataClass, DataClassSpec>> = {
  L1: {
    level: "L1",
    name: "公开",
    criteria: "已公开发布、泄露无损失",
    projectScope: ["原著原文", "解读文档", "公开可视化数据"],
    storage: "Git 明文",
    transmission: "无特殊要求",
    columnEncryptionRequired: false,
    appendOnlyRequired: false,
    defaultRetentionDays: null,
  },
  L2: {
    level: "L2",
    name: "内部",
    criteria: "仅内部可见、泄露有轻微损失",
    projectScope: ["反馈数据", "构建元数据", "内部报告"],
    storage: "DB 明文或列级加密",
    transmission: "内网即可",
    columnEncryptionRequired: false,
    appendOnlyRequired: false,
    defaultRetentionDays: 365,
  },
  L3: {
    level: "L3",
    name: "受限",
    criteria: "泄露有实际损失",
    projectScope: ["会话与消息（含用户提问内容）", "检索上下文"],
    storage: "列级加密（敏感列）",
    transmission: "必须 TLS",
    columnEncryptionRequired: true,
    appendOnlyRequired: false,
    defaultRetentionDays: 90,
  },
  L4: {
    level: "L4",
    name: "敏感",
    criteria: "泄露有重大损失或触法",
    projectScope: ["审计事件", "密钥", "凭证"],
    storage: "加密存储 + 只追加",
    transmission: "必须 TLS",
    columnEncryptionRequired: true,
    appendOnlyRequired: true,
    defaultRetentionDays: 180,
  },
};

/** 本项目的资源种类（分级目录的「落点」侧）。 */
export type ResourceKind = "sessions" | "messages" | "feedback" | "audit" | "keys" | "content";

/**
 * 资源种类 → 级别（§12.1 落点映射的机器形态）。
 *
 * 判定依据（逐条对应 §12.1「本项目落点」列）：
 *  - sessions/messages → L3（会话与消息，含用户提问内容）；
 *  - feedback        → L2（反馈数据）；
 *  - audit           → L4（审计事件）；
 *  - keys            → L4（密钥、凭证）；
 *  - content         → L1（原著原文、解读文档、公开可视化数据）。
 */
export const RESOURCE_CLASS: Readonly<Record<ResourceKind, DataClass>> = {
  sessions: "L3",
  messages: "L3",
  feedback: "L2",
  audit: "L4",
  keys: "L4",
  content: "L1",
};

/**
 * 各表的**敏感列**（需要列级加密的列 · §12.1「列级加密（敏感列）」）。
 *
 * 为什么只有这几列：分级是**表级**的，但加密是**列级**的——
 * 会话行里的 id/model/时间戳不是敏感内容，用户可见的会话标题与消息正文才是。
 * L2 反馈表按 §12.1「DB 明文或列级加密」→ 不强制加密（comment 是内部反馈，不是敏感列）。
 */
export const SENSITIVE_COLUMNS: Readonly<Record<string, string[]>> = {
  sessions: ["title"],
  messages: ["content", "tool_calls"],
  feedback: [],
};

/** 判定一个值是不是合法级别。 */
export function isDataClass(value: unknown): value is DataClass {
  return typeof value === "string" && (DATA_CLASSES as readonly string[]).includes(value);
}

/**
 * 强制校验分级标签（**入库必带**·C-6）。
 *
 * 两条拒绝路径（都报可枚举错误类 · C-4）：
 *  - 缺失（undefined/null/空串）⇒ COMPLIANCE_DATA_CLASS_MISSING；
 *  - 值非法（不在 L1–L4）      ⇒ COMPLIANCE_DATA_CLASS_INVALID。
 *
 * 拒绝即抛（不静默补默认值）：静默补默认值会让「没定级」的数据以合法标签落库，
 * 等于把合规缺口伪装成合规——比直接失败危险得多。
 */
export function requireDataClass(value: unknown, where: string): DataClass {
  if (value === undefined || value === null || value === "") {
    throw new ComplianceError(
      ComplianceErrorCode.DATA_CLASS_MISSING,
      "入库缺少分级标签（C-6）",
      { where }
    );
  }
  if (!isDataClass(value)) {
    throw new ComplianceError(
      ComplianceErrorCode.DATA_CLASS_INVALID,
      "分级标签取值非法（允许 L1/L2/L3/L4）",
      { where, value: String(value) }
    );
  }
  return value;
}

/** 由资源种类推导级别（分级目录的落点映射）。 */
export function resolveDataClass(kind: ResourceKind): DataClass {
  return RESOURCE_CLASS[kind];
}

/** 该级别是否要求列级加密（§12.4：L3/L4 列级加密）。 */
export function requiresColumnEncryption(level: DataClass): boolean {
  return DATA_CLASS_CATALOG[level].columnEncryptionRequired;
}

/** 该级别是否要求只追加（§12.1：L4 加密存储 + 只追加）。 */
export function requiresAppendOnly(level: DataClass): boolean {
  return DATA_CLASS_CATALOG[level].appendOnlyRequired;
}

/**
 * 合规强制模式是否开启。
 *
 * 口径（**默认不改变现役行为**）：
 *  - AGENT_WEB_COMPLIANCE_BASELINE=1 ⇒ 开启（整套合规基线姿态，见 baseline.ts）；
 *  - AGENT_WEB_COMPLIANCE_ENFORCE=1 ⇒ 开启（只开「入库强制校验」这一项，便于灰度）。
 * 两者任一为 "1" 即开。
 *
 * 关闭时（默认）：缺标签**不拒绝**，而是由分级目录按资源种类推导并落库（见 resolveWriteDataClass）。
 * 开启时：缺标签 ⇒ 拒绝入库（§12.2 缺口 5「入库强制校验」的严格口径）。
 */
export function dataClassEnforcementEnabled(env: NodeJS.ProcessEnv = process.env): boolean {
  return (env.AGENT_WEB_COMPLIANCE_BASELINE || "") === "1" || (env.AGENT_WEB_COMPLIANCE_ENFORCE || "") === "1";
}

/**
 * 写入路径的分级标签解析（**两个后端共用这一条口径**）。
 *
 * @param value 调用方显式带的标签（可空）
 * @param kind  资源种类（用于目录推导）
 * @param where 定位串（进错误明细，便于排查是哪条写入）
 * @param env   环境（便于测试注入）
 * @returns 合法级别（**显式值非法时一律拒绝**；显式值缺失时按开关决定拒绝还是推导）
 */
export function resolveWriteDataClass(
  value: unknown,
  kind: ResourceKind,
  where: string,
  env: NodeJS.ProcessEnv = process.env
): DataClass {
  if (value !== undefined && value !== null && value !== "") {
    return requireDataClass(value, where);   // 显式值非法 ⇒ 永远拒绝（不因开关而放宽）
  }
  if (dataClassEnforcementEnabled(env)) {
    throw new ComplianceError(
      ComplianceErrorCode.DATA_CLASS_MISSING,
      "入库缺少分级标签（C-6·强制模式）",
      { where, kind }
    );
  }
  return resolveDataClass(kind);   // 非强制模式：按分级目录推导（现役调用点不破坏）
}
