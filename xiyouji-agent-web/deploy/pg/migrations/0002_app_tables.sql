-- ==============================================================================
-- 0002_app_tables.sql — 应用业务三表（xiyouji 架构方案 v2 · D-2 应用迁移批）
-- ==============================================================================
-- 职责：建立会话 / 消息 / 反馈三张业务表 + 索引 + 约束。
--       0001_baseline.sql 只建「迁移机制本身 + 审计归档骨架」，业务表属本文件。
--
-- 对应方案：§7.1 S4 PostgreSQL 16 自建单机 · §7.3 SQLite → PostgreSQL 迁移映射
--           §5.1 M12 PG 存储层（迁移 + 事务）· §7.4 会话数据生命周期
--
-- 纪律（与 0001 一致）：
--   1) **单事务**：整文件 BEGIN/COMMIT 包住 ⇒ 失败整段回滚（§5.3 铁律 6）
--   2) **幂等**：CREATE TABLE IF NOT EXISTS / CREATE INDEX IF NOT EXISTS
--   3) **禁破坏性语句**：DROP / TRUNCATE 一律禁（数据只增不删，见 §5.4 禁止依赖形态）
--   4) **版本单调**：文件名四位版本号严格递增（由 verify-baseline.py 断言）
--   5) PG 的 SQL 注释只认 `--`（`#` 是 MySQL/SQLite 风格·PG 报语法错·W927 实跑实证）
--
-- 与 SQLite 侧的**逐条对应**（方案 §7.3 映射表）：
--   sessions  : TEXT PRIMARY KEY → TEXT（保留 id 形态·不做 UUID 转换——迁移须 1:1 保真）
--               时间列 TEXT → TIMESTAMPTZ（§7.4 生命周期 7 阶段要做日期算术）
--   messages  : role CHECK 约束 → 同名 CHECK（方案 §7.3：enum 或 CHECK 二者等价·取 CHECK
--               以便「与 SQLite 逐字一致」在迁移对账时可核对）
--   feedback  : 保留 W919 已修的「同消息双 verdict」唯一维度 ⇒ message_id 唯一索引
--   外键      : SQLite 侧靠 `foreign_keys=ON` pragma 强制 ⇒ PG 侧用真 FOREIGN KEY 强制
--               （级联删除语义两后端一致·由 storage.test.ts 契约测试守住）
--
-- 执行方式：
--   psql -v ON_ERROR_STOP=1 -U xiyouji_app -d xiyouji -f 0002_app_tables.sql
--   （**以应用账号执行**——表归应用账号所有，后续由应用账号创建的表才会拿到
--     `ALTER DEFAULT PRIVILEGES ... FOR ROLE xiyouji_app` 的默认权限；
--     D-1 引导脚本原写法缺 FOR ROLE 子句 ⇒ 静默失效，W934 已修）
-- ==============================================================================

BEGIN;

-- ------------------------------------------------------------------------------
-- 会话表
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sessions (
    id            TEXT        PRIMARY KEY,
    title         TEXT        NOT NULL,
    model         TEXT        NOT NULL,
    sdk_session_id TEXT,
    created_at    TIMESTAMPTZ NOT NULL,
    updated_at    TIMESTAMPTZ NOT NULL
);

COMMENT ON TABLE sessions IS
    '会话：id 由服务端生成（UUID）·sdk_session_id 可空·created_at/updated_at 为 TIMESTAMPTZ（边界转 ISO-8601 毫秒精度字符串）';

-- 查询模式索引（对应 SQLite 侧 idx_sessions_updated_at）
CREATE INDEX IF NOT EXISTS idx_sessions_updated_at ON sessions (updated_at DESC);

-- ------------------------------------------------------------------------------
-- 消息表
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS messages (
    id         TEXT        PRIMARY KEY,
    session_id TEXT        NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    role       TEXT        NOT NULL CHECK (role IN ('user', 'assistant')),
    content    TEXT        NOT NULL,
    model      TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    tool_calls TEXT
);

COMMENT ON TABLE messages IS
    '消息：tool_calls 存 JSON 文本或 NULL（与 SQLite 侧同构·不在存储层做解析）';

CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages (session_id);
CREATE INDEX IF NOT EXISTS idx_messages_session_created ON messages (session_id, created_at);

-- ------------------------------------------------------------------------------
-- 反馈表
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS feedback (
    id         TEXT        PRIMARY KEY,
    session_id TEXT        NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    message_id TEXT        NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
    verdict    TEXT        NOT NULL CHECK (verdict IN ('up', 'down')),
    comment    TEXT,
    created_at TIMESTAMPTZ NOT NULL
);

COMMENT ON TABLE feedback IS
    '反馈：message_id 唯一（W917 B-DB-01 收紧维度——同消息只能有一条 verdict·冲突走 upsert 覆盖）';

-- 唯一维度（方案 §7.3：必须保留）
CREATE UNIQUE INDEX IF NOT EXISTS idx_feedback_message ON feedback (message_id);
CREATE INDEX IF NOT EXISTS idx_feedback_created_at ON feedback (created_at);
CREATE INDEX IF NOT EXISTS idx_feedback_session_id ON feedback (session_id);

COMMIT;
