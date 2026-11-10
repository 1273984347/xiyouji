// gen_compliance_migration.mjs — 从 DDL 事实源生成 PG 合规列迁移（W1205 · D-3 合规批）
//
// 为什么要有这个脚本：分级标签列与审计只追加授权的 DDL **只有一个事实源**
//   （server/compliance/schema.ts 的 pgComplianceDdl / pgAuditAppendOnlyGrants）。
//   手抄进 .sql ⇒ 两份副本必然漂移 ⇒ 漂移代价是「测试 schema 与生产 schema 不一致」
//   ⇒ 测试全绿、生产一写就炸（W934 实跑抓过同类：所有权错 ⇒ 迁移序列根本跑不起来）。
//
// 用法（任意 cwd）：
//   node scripts/gen_compliance_migration.mjs
//   node scripts/gen_compliance_migration.mjs --check    # 只校验不落盘（可作门禁）
//
// 环境变量：
//   PG_APP_ROLE —— 审计只追加授权的应用账号名（默认 xiyouji_app）
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");

// tsx 只装在 xiyouji-agent-web/node_modules ⇒ 自解析 loader 路径（不依赖 cwd 与 node 解析）
const TSX_LOADER = path.join(ROOT, "xiyouji-agent-web", "node_modules", "tsx", "dist", "loader.mjs");
if (!fs.existsSync(TSX_LOADER)) {
  console.error("FAIL 找不到 tsx loader：" + TSX_LOADER);
  process.exit(1);
}
await import(pathToFileURL(TSX_LOADER).href);

const { pgComplianceDdl, pgAuditAppendOnlyGrants } = await import(
  pathToFileURL(path.join(ROOT, "xiyouji-agent-web", "server", "compliance", "schema.ts")).href
);

const APP_ROLE = process.env.PG_APP_ROLE || "xiyouji_app";
const OUT = path.join(ROOT, "xiyouji-agent-web", "deploy", "pg", "migrations", "0003_compliance_columns.sql");

const header = [
  "-- ==============================================================================",
  "-- 0003_compliance_columns.sql — 合规列（分级标签）与审计只追加授权",
  "--   （W1205 · D-3 合规批 · 架构方案 v2 §12 合规与数据分级）",
  "-- ==============================================================================",
  "-- 职责：给会话 / 消息 / 反馈三张业务表加 data_class 分级标签列（§12.1 + C-6），",
  "--       并把 audit_archive 收成「只追加」授权（§12.3）。",
  "--",
  "-- 对应方案：§12.1 数据分级四级 · §12.3 审计事件结构（只增不改）· §5.5 C-6/C-7",
  "--",
  "-- 纪律（与 0001 / 0002 一致）：",
  "--   1) **单事务**：整文件 BEGIN/COMMIT 包住 ⇒ 失败整段回滚（§5.3 铁律 6）",
  "--   2) **幂等**：ADD COLUMN IF NOT EXISTS ⇒ 可重复执行",
  "--   3) **禁破坏性语句**：只加列，不改既有列 ⇒ 存量行按分级目录默认值自动回填",
  "--      （会话 / 消息 = L3 · 反馈 = L2；取值受 CHECK 约束 ⇒ 绕过应用层也写不进非法标签）",
  "--   4) PG 的 SQL 注释只认 '--'",
  "--",
  "-- **本文件由 scripts/gen_compliance_migration.mjs 从 server/compliance/schema.ts 的",
  "--   DDL 事实源生成 ⇒ DDL 部分逐字一致；手改即漂移 ⇒ 请改事实源后重跑生成。",
  "--",
  "-- 执行方式（**以应用账号执行**）：",
  "--   psql -v ON_ERROR_STOP=1 -U xiyouji_app -d xiyouji -f 0003_compliance_columns.sql",
  "",
  "BEGIN;",
  "",
  "-- ---- 分级标签列（data_class）：会话 / 消息 = L3，反馈 = L2 ----",
  "",
].join("\n");

const body = [
  pgComplianceDdl(),
  "",
  "-- ---- audit_archive 只追加授权（REVOKE UPDATE/DELETE · GRANT INSERT/SELECT）----",
  pgAuditAppendOnlyGrants(APP_ROLE),
  "",
  "COMMIT;",
  "",
].join("\n");

const content = header + body;
if (process.argv.includes("--check")) {
  const cur = fs.existsSync(OUT) ? fs.readFileSync(OUT, "utf-8") : "";
  if (cur !== content) {
    console.error("FAIL 0003 与事实源不一致（请重跑生成）");
    process.exit(1);
  }
  console.log("OK 0003 与 schema.ts 事实源逐字一致");
} else {
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, content, "utf-8");
  console.log("written:", OUT);
}
