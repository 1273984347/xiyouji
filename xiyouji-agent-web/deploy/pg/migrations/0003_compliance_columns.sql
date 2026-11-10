-- ==============================================================================
-- 0003_compliance_columns.sql — 合规列（分级标签）与审计只追加授权
--   （W1205 · D-3 合规批 · 架构方案 v2 §12 合规与数据分级）
-- ==============================================================================
-- 职责：给会话 / 消息 / 反馈三张业务表加 data_class 分级标签列（§12.1 + C-6），
--       并把 audit_archive 收成「只追加」授权（§12.3）。
--
-- 对应方案：§12.1 数据分级四级 · §12.3 审计事件结构（只增不改）· §5.5 C-6/C-7
--
-- 纪律（与 0001 / 0002 一致）：
--   1) **单事务**：整文件 BEGIN/COMMIT 包住 ⇒ 失败整段回滚（§5.3 铁律 6）
--   2) **幂等**：ADD COLUMN IF NOT EXISTS ⇒ 可重复执行
--   3) **禁破坏性语句**：只加列，不改既有列 ⇒ 存量行按分级目录默认值自动回填
--      （会话 / 消息 = L3 · 反馈 = L2；取值受 CHECK 约束 ⇒ 绕过应用层也写不进非法标签）
--   4) PG 的 SQL 注释只认 '--'
--
-- **本文件由 scripts/gen_compliance_migration.mjs 从 server/compliance/schema.ts 的
--   DDL 事实源生成 ⇒ DDL 部分逐字一致；手改即漂移 ⇒ 请改事实源后重跑生成。
--
-- 执行方式（**以应用账号执行**）：
--   psql -v ON_ERROR_STOP=1 -U xiyouji_app -d xiyouji -f 0003_compliance_columns.sql

BEGIN;

-- ---- 分级标签列（data_class）：会话 / 消息 = L3，反馈 = L2 ----
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS data_class TEXT NOT NULL DEFAULT 'L3' CHECK (data_class IN ('L1','L2','L3','L4'));
ALTER TABLE messages ADD COLUMN IF NOT EXISTS data_class TEXT NOT NULL DEFAULT 'L3' CHECK (data_class IN ('L1','L2','L3','L4'));
ALTER TABLE feedback ADD COLUMN IF NOT EXISTS data_class TEXT NOT NULL DEFAULT 'L2' CHECK (data_class IN ('L1','L2','L3','L4'));

-- ---- audit_archive 只追加授权（REVOKE UPDATE/DELETE · GRANT INSERT/SELECT）----
REVOKE UPDATE, TRUNCATE ON audit_archive FROM xiyouji_app;
GRANT INSERT, SELECT, DELETE ON audit_archive TO xiyouji_app;

COMMIT;
