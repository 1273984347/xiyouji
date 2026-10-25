#!/usr/bin/env bash
# ==============================================================================
# initdb-bootstrap.sh — 幂等初始化（xiyouji 架构方案 v2 · D-1 批）
# ==============================================================================
# 职责：在一台已 initdb 的 PG 16 实例上，幂等地建立「角色 + 数据库 + 扩展 + 权限」。
# 幂等要求：**重复执行结果必须一致，且不破坏既有数据**（重跑安全）。
#
# 对应方案：§5.1 M12 PG 存储层 · §7.3 SQLite→PG 迁移映射 · §12.2 缺口 2（强制鉴权）
#
# 用法：
#   PGDATA=/var/lib/pgsql/16/data \
#   ARCHIVE_DIR=/var/lib/pgsql/archive \
#   APP_PASSWORD='...'  RO_PASSWORD='...' \
#   bash bin/initdb-bootstrap.sh
#
# 纪律：
#   - 口令从环境变量读，**禁写本文件、禁写 shell 历史**。
#   - 全部操作幂等：CREATE ... IF NOT EXISTS 语义 或「先查后建」。
#   - 禁 DROP / 禁 TRUNCATE / 禁删库（本脚本只增不删）。
# ==============================================================================
set -euo pipefail

: "${PGDATA:?必须设置 PGDATA}"
: "${APP_PASSWORD:?必须设置 APP_PASSWORD（应用层业务账号口令）}"
: "${RO_PASSWORD:?必须设置 RO_PASSWORD（只读账号口令）}"

APP_USER="${APP_USER:-xiyouji_app}"
RO_USER="${RO_USER:-xiyouji_ro}"
APP_DB="${APP_DB:-xiyouji}"
RO_DB="${RO_DB:-xiyouji_ro}"

# 目标机上的 psql 连接参数（本地维护通道 · peer 认证）
PSQL_LOCAL=(psql -v ON_ERROR_STOP=1 -U postgres -d postgres)

log() { printf '[bootstrap] %s\n' "$*"; }
die() { printf '[bootstrap] FATAL: %s\n' "$*" >&2; exit 1; }

# --- ① 前置检查：PG 版本必须 ≥ 16（方案 §7.1 裁定 PG 16 自建单机）----------------
PGVER="$("${PSQL_LOCAL[@]}" -tAc 'SHOW server_version_num')"
[ "${PGVER}" -ge 160000 ] || die "PG 版本过低：${PGVER}（要求 ≥ 160000，即 PG 16）"
log "PG 版本检查通过：server_version_num=${PGVER}"

# --- ② 角色（幂等：先查后建）--------------------------------------------------
ensure_role() {
  local user="$1" password="$2" can_login="$3"
  if "${PSQL_LOCAL[@]}" -tAc "SELECT 1 FROM pg_roles WHERE rolname='${user}'" | grep -q 1; then
    log "角色已存在，跳过创建：${user}"
    # 口令同步：部署期轮换时需要能改口令 ⇒ 用 ALTER（幂等：同值即无变化）
    "${PSQL_LOCAL[@]}" -c "ALTER ROLE ${user} WITH LOGIN PASSWORD '${password}'" >/dev/null
  else
    log "创建角色：${user}（can_login=${can_login}）"
    "${PSQL_LOCAL[@]}" -c "CREATE ROLE ${user} WITH LOGIN PASSWORD '${password}'" >/dev/null
  fi
}

ensure_role "${APP_USER}" "${APP_PASSWORD}" yes
ensure_role "${RO_USER}"  "${RO_PASSWORD}"  yes

# 只读账号的权限收紧：禁建库/禁超级用户/禁复制
"${PSQL_LOCAL[@]}" -c "ALTER ROLE ${RO_USER} NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION" >/dev/null
log "只读角色权限收紧：${RO_USER}"

# --- ③ 数据库（幂等）----------------------------------------------------------
if "${PSQL_LOCAL[@]}" -tAc "SELECT 1 FROM pg_database WHERE datname='${APP_DB}'" | grep -q 1; then
  log "数据库已存在，跳过创建：${APP_DB}"
else
  log "创建数据库：${APP_DB}（owner=${APP_USER}）"
  "${PSQL_LOCAL[@]}" -c "CREATE DATABASE ${APP_DB} OWNER ${APP_USER} ENCODING 'UTF8' TEMPLATE template0" >/dev/null
fi

if "${PSQL_LOCAL[@]}" -tAc "SELECT 1 FROM pg_database WHERE datname='${RO_DB}'" | grep -q 1; then
  log "只读数据库已存在，跳过创建：${RO_DB}"
else
  log "创建只读数据库：${RO_DB}（owner=${RO_USER}）"
  "${PSQL_LOCAL[@]}" -c "CREATE DATABASE ${RO_DB} OWNER ${RO_USER} ENCODING 'UTF8' TEMPLATE template0" >/dev/null
fi

# --- ④ 应用库内的对象与权限 ---------------------------------------------------
PSQL_APP=(psql -v ON_ERROR_STOP=1 -U postgres -d "${APP_DB}")

# 迁移序列表（迁移机制的记账表 · 见 migrations/README.md）
"${PSQL_APP[@]}" -c "
CREATE TABLE IF NOT EXISTS schema_migrations (
  version     INTEGER     PRIMARY KEY,
  name        TEXT        NOT NULL,
  checksum    TEXT        NOT NULL,
  applied_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  applied_by  TEXT        NOT NULL DEFAULT current_user
);
COMMENT ON TABLE schema_migrations IS '迁移序列记账（version 单调递增·与 SQLite user_version 同职能但换机制）';
" >/dev/null
log "迁移序列表就绪：schema_migrations"

# 业务账号的库级权限（最小权限：只给 CONNECT + 未来建表权，不给超级用户）
"${PSQL_APP[@]}" -c "GRANT CONNECT ON DATABASE ${APP_DB} TO ${APP_USER}" >/dev/null
"${PSQL_APP[@]}" -c "GRANT CONNECT ON DATABASE ${APP_DB} TO ${RO_USER}" >/dev/null

# 只读账号：只给 CONNECT + schema USAGE + 表 SELECT（未来表由默认权限覆盖）
"${PSQL_APP[@]}" -c "GRANT USAGE ON SCHEMA public TO ${RO_USER}" >/dev/null
"${PSQL_APP[@]}" -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO ${RO_USER}" >/dev/null

# 应用账号在 public schema 的建表权（迁移脚本需要 DDL）
"${PSQL_APP[@]}" -c "GRANT ALL ON SCHEMA public TO ${APP_USER}" >/dev/null
"${PSQL_APP[@]}" -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${APP_USER}" >/dev/null
"${PSQL_APP[@]}" -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${APP_USER}" >/dev/null
log "权限矩阵就绪（§12.2 缺口 2 对应：应用层账号与超级用户分离）"

# --- ⑤ 只读库连接挂载（供报表/巡检直连）---------------------------------------
# 只读库与写库同实例不同库 ⇒ 通过只读账号 + 只读库实现「只读视角」，不额外起实例。
log "只读视角就绪：${RO_USER}@${RO_DB}"

# --- ⑥ 收尾自检 --------------------------------------------------------------
TBL_COUNT="$("${PSQL_APP[@]}" -tAc "SELECT count(*) FROM information_schema.tables WHERE table_schema='public'")"
log "完成。public schema 表数 = ${TBL_COUNT}（含 schema_migrations）"
log "下一步：跑 migrations/ 下的迁移序列（见 migrations/README.md）"
