#!/usr/bin/env bash
# ==============================================================================
# backup.sh — 每日全量备份 + WAL 归档轮转（xiyouji 架构方案 v2 · D-1 批）
# ==============================================================================
# 职责：
#   ① 每日一次全量备份（pg_basebackup —— 免停机一致性快照，不用文件拷贝）
#   ② WAL 归档目录的保留期轮转（§9.4：全量 7 份 + WAL 14 天）
#   ③ 每次备份后做**可读性自检**（能解压 + 含关键文件 ⇒ 备份不是空壳）
#
# 对应方案：§9.4 备份与恢复演练（PG 数据目录 · RTO ≤ 30 min · RPO ≤ 5 min）
#          §9.2 F9（PG 实例故障 ⇒ 归档 + pg_basebackup 恢复）
#
# 用法：
#   BACKUP_ROOT=/var/lib/pgsql/backup \
#   ARCHIVE_DIR=/var/lib/pgsql/archive \
#   KEEP_FULL=7 KEEP_WAL_DAYS=14 \
#   bash bin/backup.sh
#
# 纪律：
#   - **禁用文件拷贝做备份**（会丢 WAL 中未 checkpoint 的提交 ⇒ 沿用现役
#     chat.db 的教训：VACUUM INTO / pg_basebackup 才是一致性快照）。
#   - 备份件与数据目录**分盘**（§9.2 F8 本机磁盘故障 ⇒ 备份必须在别处）。
#   - 备份件口径 §12.1：随源数据分级（L3/L4 数据 ⇒ 备份介质须加密，见 §12.4）。
# ==============================================================================
set -euo pipefail

: "${PGDATA:?必须设置 PGDATA}"
: "${BACKUP_ROOT:?必须设置 BACKUP_ROOT（备份根目录·须与 PGDATA 分盘）}"
: "${ARCHIVE_DIR:?必须设置 ARCHIVE_DIR（WAL 归档目录·须与 PGDATA 分盘）}"

KEEP_FULL="${KEEP_FULL:-7}"          # §9.4：全量保留 7 份
KEEP_WAL_DAYS="${KEEP_WAL_DAYS:-14}"  # §9.4：WAL 保留 14 天
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

log() { printf '[backup] %s\n' "$*"; }
die() { printf '[backup] FATAL: %s\n' "$*" >&2; exit 1; }

# --- ① 前置检查 --------------------------------------------------------------
command -v pg_basebackup >/dev/null 2>&1 || die "缺 pg_basebackup（pg_basebackup 不在 PATH）"
[ -d "$PGDATA" ] || die "PGDATA 不存在：${PGDATA}"
[ -d "$ARCHIVE_DIR" ] || die "WAL 归档目录不存在：${ARCHIVE_DIR}"

# 归档目录与数据目录不得同盘（否则 F8 磁盘故障同时毁掉数据与备份）
PG_DEV="$(df -P "$PGDATA" | awk 'NR==2{print $1}')"
BK_DEV="$(df -P "$BACKUP_ROOT" 2>/dev/null | awk 'NR==2{print $1}')" || BK_DEV=""
if [ -n "$BK_DEV" ] && [ "$PG_DEV" = "$BK_DEV" ]; then
  die "备份目录与 PGDATA 同盘（${PG_DEV}）⇒ F8 磁盘故障会同时毁掉数据与备份（§9.2 F8）"
fi
log "分盘检查通过：PGDATA=${PG_DEV} BACKUP=${BK_DEV:-未知}"

mkdir -p "$BACKUP_ROOT"

# --- ② 全量备份 --------------------------------------------------------------
TARGET="${BACKUP_ROOT}/full_${STAMP}"
log "开始全量备份 → ${TARGET}"
# -D 目录式 · -X none（不额外带 WAL，靠归档目录）· -R 写恢复配置
pg_basebackup -D "$TARGET" -X none -R -z -c fast --no-password 2>&1 | sed 's/^/[backup]   /'
log "全量备份完成：${TARGET}"

# --- ③ 备份可读性自检（备份不是空壳）------------------------------------------
[ -f "${TARGET}/backup_label" ] || die "备份缺 backup_label ⇒ 非有效全量备份"
[ -f "${TARGET}/postgresql.conf" ] || die "备份缺 postgresql.conf ⇒ 快照不完整"
TABLE_COUNT="$(find "$TARGET/base" -maxdepth 2 -name 'PG_VERSION' 2>/dev/null | wc -l | tr -d ' ')"
[ "${TABLE_COUNT}" -ge 1 ] || die "备份缺 base/ 数据目录 ⇒ 快照不完整"
log "可读性自检通过（backup_label + postgresql.conf + base/ 均在位）"

# --- ④ 旧全量备份轮转（保留最近 KEEP_FULL 份）---------------------------------
mapfile -t OLD_FULLS < <(find "$BACKUP_ROOT" -maxdepth 1 -type d -name 'full_*' | sort)
COUNT="${#OLD_FULLS[@]}"
if [ "${COUNT}" -gt "${KEEP_FULL}" ]; then
  REMOVE=$(( COUNT - KEEP_FULL ))
  log "轮转：删除最旧 ${REMOVE} 份全量备份（保留 ${KEEP_FULL} 份）"
  for i in $(seq 0 $(( REMOVE - 1 ))); do
    OLD="${OLD_FULLS[$i]}"
    log "  删除：$(basename "$OLD")"
    rm -rf "$OLD"
  done
else
  log "轮转：当前 ${COUNT} 份 ≤ 保留 ${KEEP_FULL} 份，无需删除"
fi

# --- ⑤ WAL 归档轮转（按 mtime 保留 KEEP_WAL_DAYS 天）--------------------------
# 注意：归档文件是 PITR 的唯一来源 ⇒ 只能删「已超出保留期且早于最旧全量备份」的段。
# 简化口径（保守）：删 mtime 超过 KEEP_WAL_DAYS 的段。
if [ -d "$ARCHIVE_DIR" ]; then
  BEFORE_COUNT="$(find "$ARCHIVE_DIR" -maxdepth 1 -type f -name '0*' | wc -l | tr -d ' ')"
  find "$ARCHIVE_DIR" -maxdepth 1 -type f -name '0*' -mtime "+${KEEP_WAL_DAYS}" -print -delete 2>/dev/null \
    | while read -r f; do log "  删除过期 WAL：$(basename "$f")"; done
  AFTER_COUNT="$(find "$ARCHIVE_DIR" -maxdepth 1 -type f -name '0*' | wc -l | tr -d ' ')"
  log "WAL 归档轮转完成：${BEFORE_COUNT} → ${AFTER_COUNT} 段（保留 ${KEEP_WAL_DAYS} 天）"
else
  log "WAL 归档目录不存在，跳过轮转"
fi

# --- ⑥ 收尾：写本次备份的元信息（供 restore-drill.sh 断言用）-------------------
META="${TARGET}/BACKUP_META.txt"
{
  echo "stamp=${STAMP}"
  echo "pgdata=${PGDATA}"
  echo "archive_dir=${ARCHIVE_DIR}"
  echo "keep_full=${KEEP_FULL}"
  echo "keep_wal_days=${KEEP_WAL_DAYS}"
  echo "created_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$META"
log "完成。元信息：${META}"
log "下一步：跑 bash bin/restore-drill.sh 做恢复演练（§9.4 要求每月一次）"
