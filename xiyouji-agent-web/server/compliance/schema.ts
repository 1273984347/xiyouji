/**
 * schema.ts — 合规列的**权威 DDL**（W1205 · D-3 合规批）
 *
 * 背景：本仓 PG 迁移序列在 deploy/pg/migrations/（属另一子任务的地盘·本批不可写）。
 * 但「业务表要落分级标签」这件事的 DDL 只有一个事实源，否则测试 schema 与生产 schema
 * 会漂移（漂移的代价是：测试全绿、生产一写就炸）。
 * ⇒ 本文件持有 DDL 事实源，控制器把 pgComplianceDdl() 的内容落成
 *   deploy/pg/migrations/0003_compliance_columns.sql（内容必须与本文件逐字一致）。
 *
 * SQLite 侧不需要外部迁移文件：sqlite.ts 内置的迁移框架（v4）引用本文件的列定义。
 *
 * 一条纪律：**只加列，不改既有列**（§5.4 禁破坏性语句）⇒ 存量数据按目录默认值回填。
 */
import type { DataClass } from "./data-class.js";

/** 合规列规格（业务表的分级标签列）。 */
export interface ComplianceColumnSpec {
  /** 目标表。 */
  table: string;
  /** 列名。 */
  column: string;
  /** 存量行的回填默认值（取自分级目录的落点映射）。 */
  defaultClass: DataClass;
}

/**
 * 三张业务表的分级标签列（默认值取自分级目录：会话/消息 = L3，反馈 = L2）。
 *
 * 注意：PG 侧 0001 基线的 audit_archive **已有** data_class 列且带 CHECK 约束 ⇒
 * 本清单只管业务三表，不重复造 audit_archive 的列。
 */
export const COMPLIANCE_COLUMNS: readonly ComplianceColumnSpec[] = [
  { table: "sessions", column: "data_class", defaultClass: "L3" },
  { table: "messages", column: "data_class", defaultClass: "L3" },
  { table: "feedback", column: "data_class", defaultClass: "L2" },
];

/** 分级标签列的取值约束（与 PG 0001 基线 audit_archive 的 CHECK 完全一致）。 */
export const DATA_CLASS_CHECK_SQL = "data_class IN ('L1','L2','L3','L4')";

/**
 * PG 侧合规列 DDL（幂等 · 可重复执行）。
 *
 * 形态：ALTER TABLE ... ADD COLUMN IF NOT EXISTS（PG 9.6+ 支持）⇒ 重复执行不报错。
 * NOT NULL + DEFAULT ⇒ 存量行自动回填；CHECK ⇒ 绕过应用层也写不进非法标签。
 */
export function pgComplianceDdl(): string {
  return COMPLIANCE_COLUMNS.map(
    (spec) =>
      "ALTER TABLE " +
      spec.table +
      " ADD COLUMN IF NOT EXISTS " +
      spec.column +
      " TEXT NOT NULL DEFAULT '" +
      spec.defaultClass +
      "' CHECK (" +
      DATA_CLASS_CHECK_SQL +
      ");"
  ).join("\n");
}

/**
 * SQLite 侧补列 DDL（供 sqlite.ts 的迁移 v4 逐表执行）。
 *
 * SQLite 的 ALTER TABLE ADD COLUMN 限制：不能加 PRIMARY KEY/UNIQUE；
 * NOT NULL 必须带非空默认值；CHECK 约束允许（不引用其它列即可）。
 */
export function sqliteAddColumnDdl(spec: ComplianceColumnSpec): string {
  return (
    "ALTER TABLE " +
    spec.table +
    " ADD COLUMN " +
    spec.column +
    " TEXT NOT NULL DEFAULT '" +
    spec.defaultClass +
    "' CHECK (" +
    DATA_CLASS_CHECK_SQL +
    ")"
  );
}

/**
 * 审计归档表的「只追加」授权 SQL（**由控制器在迁移里落·应用不执行**）。
 *
 * 口径（W1205 控制器裁决）：
 *   - **REVOKE UPDATE**（防篡改是「只追加」的核心）⇒ 应用账号改不了既有审计行；
 *   - **DELETE 权限保留**——§12.3 明确允许「按留存期批量销毁」⇒ 销毁路径需要 DELETE 权限；
 *     初版这里一并 REVOKE 掉了 DELETE ⇒ 与销毁留证口径**自相矛盾**（销毁入口必然失败）⇒ 已订正。
 *     删除约束改由**代码路径**保证：应用层不提供任意删除入口，只有「到期销毁」入口，
 *     且销毁动作本身写一条新审计事件（销毁留证）。
 *   - 应用账号名经环境变量覆盖，避免把部署名写死在代码里。
 */
export function pgAuditAppendOnlyGrants(appRole: string): string {
  return [
    // REVOKE UPDATE **与 TRUNCATE**：W1205 实测实证——UPDATE 被 REVOKE 后确实报
    // permission denied（owner 隐含权限可被显式收回），但 TRUNCATE 是**独立权限**（ACL 里的 D），
    // 不在 REVOKE 列表里就仍可用 ⇒ 应用账号能一次性清空整个审计归档 ⇒「只追加」被绕过。
    // ⇒ 两者都要显式收回；DELETE 保留（§12.3 的「按留存期批量销毁」需要它）。
    "REVOKE UPDATE, TRUNCATE ON audit_archive FROM " + appRole + ";",
    "GRANT INSERT, SELECT, DELETE ON audit_archive TO " + appRole + ";",
  ].join("\n");
}
