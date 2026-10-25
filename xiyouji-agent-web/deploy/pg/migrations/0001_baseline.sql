# ==============================================================================
-- 0001_baseline.sql — 迁移序列骨架（xiyouji 架构方案 v2 · D-1 批）
-- ==============================================================================
-- 职责：建立「迁移机制本身」与最小记账表，不含业务表（业务表属 D-2 应用迁移批）。
--
-- 对应方案：§7.3 SQLite → PostgreSQL 迁移映射 · §5.1 M12 PG 存储层（迁移 + 事务）
--
-- 纪律：
--   1) **单事务**：整文件 BEGIN/COMMIT 包住 ⇒ 失败整段回滚（§5.3 铁律 6「迁移必须可逆且留证」）
--   2) **幂等**：CREATE TABLE IF NOT EXISTS / CREATE INDEX IF NOT EXISTS
--   3) **版本单调**：文件名四位版本号严格递增（由 verify-baseline.py 断言）
--   4) **禁破坏性语句**：DROP / TRUNCATE 一律禁（数据只增不删，见 §5.4 禁止依赖形态）
--   5) 迁移记账：应用层迁移器执行本文件后，把 version/checksum 写入 schema_migrations
--
-- 执行方式（D-2 批实现迁移器后生效；本批为离线施工件）：
--   psql -v ON_ERROR_STOP=1 -U postgres -d xiyouji -f 0001_baseline.sql
-- ==============================================================================

BEGIN;

-- 迁移记账表（幂等；initdb-bootstrap.sh 已建过则此处为 no-op）
CREATE TABLE IF NOT EXISTS schema_migrations (
    version    INTEGER     PRIMARY KEY,
    name       TEXT        NOT NULL,
    checksum   TEXT        NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    applied_by TEXT        NOT NULL DEFAULT current_user
);

COMMENT ON TABLE schema_migrations IS
    '迁移序列记账：version 单调递增且唯一（与 SQLite user_version 同职能·换机制）·checksum 记录执行时的文件摘要（改已应用的迁移必须新增版本而非原地改）';

-- 记账表自索引（按应用时间倒序查最近应用）
CREATE INDEX IF NOT EXISTS idx_schema_migrations_applied_at
    ON schema_migrations (applied_at DESC);

-- 审计留痕骨架（§12.3 审计事件结构 · 字段集只增不改）
-- 说明：运行时审计走 JSONL 流水（server/audit.ts），本表只存「结构化归档副本」，
--       供合规检索与留存期管理（§12.5）。写入方是 D-3 合规批的应用侧。
CREATE TABLE IF NOT EXISTS audit_archive (
    id          UUID        PRIMARY KEY,
    ts          TIMESTAMPTZ NOT NULL,
    actor       TEXT        NOT NULL,
    action      TEXT        NOT NULL,
    target      TEXT        NOT NULL,
    decision    TEXT        NOT NULL,
    result      TEXT        NOT NULL,
    data_class  TEXT        NOT NULL CHECK (data_class IN ('L1', 'L2', 'L3', 'L4')),
    trace_id    TEXT,
    source_ip   TEXT,
    payload     JSONB
);

COMMENT ON TABLE audit_archive IS
    '运行期审计事件的归档副本：data_class 为四级数据分级标签（§12.1）·留存期 ≥ 180 天（§12.5）·到期销毁须留销毁事件';

CREATE INDEX IF NOT EXISTS idx_audit_archive_ts ON audit_archive (ts DESC);
CREATE INDEX IF NOT EXISTS idx_audit_archive_data_class ON audit_archive (data_class, ts DESC);
CREATE INDEX IF NOT EXISTS idx_audit_archive_trace ON audit_archive (trace_id);

COMMIT;
