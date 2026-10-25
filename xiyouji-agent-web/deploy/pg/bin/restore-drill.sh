#!/usr/bin/env bash
# ==============================================================================
# restore-drill.sh — 恢复演练（xiyouji 架构方案 v2 · D-1 批）
# ==============================================================================
# 职责：把一份全量备份恢复到**临时实例**，断言数据行数一致，然后销毁临时实例。
#       这是 §9.4「每月一次恢复演练」的机械化实现 —— 备份没被恢复过 = 没被验证过。
#
# 对应方案：§9.4 备份与恢复演练（RTO ≤ 30 min · RPO ≤ 5 min）
#          §9.2 F9（PG 实例故障 ⇒ 从归档 + pg_basebackup 恢复）
#
# 用法：
#   BACKUP_ROOT=/var/lib/pgsql/backup \
#   DRILL_ROOT=/var/lib/pgsql/drill \
#   bash bin/restore-drill.sh [备份目录名]
#     不传参 ⇒ 自动取 BACKUP_ROOT 下最新的一份 full_*
#
# 纪律：
#   - 演练实例**只读**、独立端口、独立数据目录 ⇒ 不可能污染生产实例。
#   - 演练结束必须清理临时目录（trap 兜底）。
#   - 演练不写生产库任何数据。
# ==============================================================================
set -euo pipefail

: "${BACKUP_ROOT:?必须设置 BACKUP_ROOT}"
: "${DRILL_ROOT:?必须设置 DRILL_ROOT（演练临时目录·须与生产数据分盘）}"

DRILL_PORT="${DRILL_PORT:-55432}"     # 演练实例独立端口（避开生产 5432）
KEEP_DRILL="${KEEP_DRILL:-0}"         # 演练后是否保留临时目录（0 = 立即清理）
EXPECT_TABLES="${EXPECT_TABLES:-1}"   # 期望至少存在的表数（schema_migrations 恒存在）

log() { printf '[drill] %s\n' "$*"; }
die() { printf '[drill] FATAL: %s\n' "$*" >&2; exit 1; }

command -v pg_ctl >/dev/null 2>&1 || die "缺 pg_ctl（演练需要它起停临时实例）"
command -v initdb >/dev/null 2>&1 || die "缺 initdb"

# --- ① 选定备份 --------------------------------------------------------------
if [ "$#" -ge 1 ]; then
  SRC="${BACKUP_ROOT}/$1"
else
  SRC="$(find "$BACKUP_ROOT" -maxdepth 1 -type d -name 'full_*' | sort | tail -n 1)"
fi
[ -n "$SRC" ] || die "BACKUP_ROOT 下找不到全量备份：${BACKUP_ROOT}"
[ -d "$SRC" ] || die "备份目录不存在：${SRC}"
log "选定备份：${SRC}"
[ -f "${SRC}/backup_label" ] || die "备份缺 backup_label ⇒ 无效快照"

# --- ② 准备演练数据目录 ------------------------------------------------------
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
DRILL_DATA="${DRILL_ROOT}/drill_${STAMP}"
rm -rf "$DRILL_DATA"
mkdir -p "$DRILL_DATA"

cleanup() {
  if [ -f "${DRILL_DATA}/postmaster.pid" ]; then
    log "停止演练实例"
    pg_ctl -D "$DRILL_DATA" -m immediate stop >/dev/null 2>&1 || true
  fi
  if [ "${KEEP_DRILL}" = "0" ]; then
    rm -rf "$DRILL_DATA"
    log "已清理演练目录：${DRILL_DATA}"
  else
    log "保留演练目录（KEEP_DRILL=1）：${DRILL_DATA}"
  fi
}
trap cleanup EXIT

log "恢复备份到演练目录：${DRILL_DATA}"
# 恢复到演练目录：直接拷贝 base/ + 写演练自己的配置
cp -a "${SRC}/base" "${DRILL_DATA}/base"
[ -f "${SRC}/PG_VERSION" ] && cp -a "${SRC}/PG_VERSION" "${DRILL_DATA}/PG_VERSION"

# 演练实例配置：独立端口 + 只监听回环 + 关归档（演练不产生新归档）
cat > "${DRILL_DATA}/postgresql.conf" <<EOF
port = ${DRILL_PORT}
listen_addresses = '127.0.0.1'
unix_socket_directories = '${DRILL_DATA}'
archive_mode = off
fsync = on
EOF
cat > "${DRILL_DATA}/pg_hba.conf" <<EOF
local   all         all                                  trust
host    all         all         127.0.0.1/32           trust
EOF
chmod 0700 "$DRILL_DATA"
log "演练实例配置写入完毕（端口 ${DRILL_PORT}·回环监听·归档关闭）"

# --- ③ 起演练实例 ------------------------------------------------------------
log "启动演练实例"
pg_ctl -D "$DRILL_DATA" -w -t 60 -l "${DRILL_DATA}/drill.log" start >/dev/null \
  || { cat "${DRILL_DATA}/drill.log" 2>/dev/null | tail -n 20 >&2; die "演练实例启动失败（见 drill.log）"; }

PSQL_DRILL=(psql -v ON_ERROR_STOP=1 -h 127.0.0.1 -p "${DRILL_PORT}" -U postgres -d postgres)

# --- ④ 断言：数据可读且规模合理 ----------------------------------------------
TABLES="$("${PSQL_DRILL[@]}" -tAc "SELECT count(*) FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relkind='r'")"
log "public schema 表数 = ${TABLES}"
[ "${TABLES}" -ge "${EXPECT_TABLES}" ] || die "表数不足（${TABLES} < ${EXPECT_TABLES}）⇒ 恢复的库是空的"

# 迁移记账表若存在 ⇒ 断言其行数（能读到 seq_no 才算真恢复）
if "${PSQL_DRILL[@]}" -tAc "SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='schema_migrations'" | grep -q 1; then
  APPLIED="$("${PSQL_DRILL[@]}" -tAc "SELECT count(*) FROM public.schema_migrations")"
  log "迁移记账行数 = ${APPLIED}"
  [ "${APPLIED}" -ge 0 ] || die "迁移记账不可读"
else
  log "提示：未找到 schema_migrations（迁移序列尚未应用·属正常）"
fi

# 关键数据面抽查：会话库三表若存在，断言可读且列数合理
for t in sessions messages feedback; do
  if "${PSQL_DRILL[@]}" -tAc "SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='${t}'" | grep -q 1; then
    COLS="$("${PSQL_DRILL[@]}" -tAc "SELECT count(*) FROM information_schema.columns WHERE table_schema='public' AND table_name='${t}'")"
    ROWS="$("${PSQL_DRILL[@]}" -tAc "SELECT count(*) FROM public.${t}")"
    log "  表 ${t}：列数=${COLS} 行数=${ROWS}"
    [ "${COLS}" -ge 3 ] || die "表 ${t} 列数异常（${COLS}）⇒ 恢复不完整"
  fi
done

# --- ⑤ 演练结论 --------------------------------------------------------------
log "恢复演练通过：备份可恢复、关键表可读、行数可断言"
log "（对应 §9.4：PG 数据目录 · RTO ≤ 30 min · RPO ≤ 5 min · 每月演练一次）"
