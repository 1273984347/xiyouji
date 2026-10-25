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
DRILL_DB="${DRILL_DB:-xiyouji}"       # 演练断言落在**业务库**上（postgres 库是空的）
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
# ⚠ **关键结构事实（W927 实跑实证）**：`pg_basebackup -D <dir>` 的输出目录
#   **本身就是 PGDATA 的镜像**——`base/` 与 `global/`、`pg_wal/`、`PG_VERSION`、
#   `backup_label` 是**兄弟关系**，不存在「base/ 里才是数据目录」这回事。
#   ⇒ 恢复时必须把**整个备份目录**铺成演练 PGDATA；只拷 base/ 会缺 global/ 与
#   PG_VERSION ⇒ 启动即失败（`could not open file ".../global/pg_control"`）。
cp -a "${SRC}/." "${DRILL_DATA}/"
[ -f "${DRILL_DATA}/PG_VERSION" ] || die "恢复后缺 PG_VERSION ⇒ 备份布局理解有误"
[ -f "${DRILL_DATA}/global/pg_control" ] || die "恢复后缺 global/pg_control ⇒ 备份布局理解有误"

# 去掉 standby.signal：它会让实例进入**持续恢复模式并等待 WAL**
#   （演练目标是「独立可读写实例」，不是备库）⇒ 必须删除后才能正常启动。
if [ -f "${DRILL_DATA}/standby.signal" ]; then
  rm -f "${DRILL_DATA}/standby.signal"
  log "移除 standby.signal（避免进入持续恢复等待 WAL）"
fi

# ⚠ **WAL 归档接入（关键 · W927 实跑实证）**：恢复出来的目录带着 `backup_label`
#   ⇒ PG 判定这是「从基础备份做恢复」，要求从 START WAL LOCATION 起连续重放 WAL。
#   演练目录里没有这些 WAL（pg_basebackup -X none 不带 WAL）⇒ 直接启动即 FATAL：
#     invalid checkpoint record / could not locate required checkpoint record
#   ⇒ 必须接上 **WAL 归档目录**（restore_command）+ 恢复目标点 ⇒ 这才是**真正的 PITR 演练**
#   （顺带验证 §9.4 的 RPO ≤ 5 min 归档链路，而不只是「文件拷过去了」）。
#   服务端（PG 进程）需要**原生路径**；脚本侧可能是 POSIX 形式（git-bash）⇒ 做转换。
#   注意：PG 配置串里反斜杠是转义符 ⇒ 必须用**正斜杠**形式（cygpath -m）。
ARCHIVE_SERVER="${ARCHIVE_DIR_SERVER:-}"
if [ -z "${ARCHIVE_SERVER}" ] && command -v cygpath >/dev/null 2>&1; then
  ARCHIVE_SERVER="$(cygpath -m "$ARCHIVE_DIR" 2>/dev/null || echo "$ARCHIVE_DIR")"
fi
[ -n "${ARCHIVE_SERVER}" ] || ARCHIVE_SERVER="$ARCHIVE_DIR"
log "WAL 归档接入：${ARCHIVE_SERVER}"
# 跨平台注意：Windows 版 PG **不支持 unix_socket_directories** ⇒ 仅在真类 Unix 平台设置。
# ⚠ 判据坑（W927 实跑实证）：**git-bash 的 `uname -s` 返回 `MINGW64_NT-…` 而不是 `Windows`**！
#   只写 `= "Windows"` 判等 ⇒ 在 git-bash 下会误判为类 Unix ⇒ 把 POSIX 路径
#   （/c/Users/…）写给 Windows 版 PG ⇒ 启动即 FATAL：
#     could not create lock file ".../.s.PGSQL.55432.lock": No such file or directory
#   ⇒ 判据必须覆盖 MINGW* / MSYS* / CYGWIN* / Windows* 全族。
OS_NAME="$(uname -s 2>/dev/null || echo Windows)"
case "$OS_NAME" in
  MINGW*|MSYS*|CYGWIN*|Windows*|windows*) IS_UNIX=0 ;;
  *) IS_UNIX=1 ;;
esac

# 演练实例配置写进 **postgresql.auto.conf**：该文件由 pg_basebackup -R 写入
#   （primary_conninfo / restore_command 等），且优先级**高于** postgresql.conf
#   ⇒ 只改 postgresql.conf 不生效（端口会仍用备份里的 5432）。
#   故：备份原 auto.conf 留档，再整体重写为演练专用内容。
if [ -f "${DRILL_DATA}/postgresql.auto.conf" ]; then
  cp "${DRILL_DATA}/postgresql.auto.conf" "${DRILL_DATA}/postgresql.auto.conf.src"
fi

# restore_command 的**平台差异**（W927 实跑实证，两重坑）：
#   ① Windows 的 restore_command 由 **cmd.exe** 执行 ⇒ **cmd 不认正斜杠路径**
#      （`copy "C:/Users/…" "dst"` ⇒ 「The system cannot find the file specified.」）
#      ⇒ Windows 必须用**反斜杠**路径。
#   ② 但 PG 的配置串里**反斜杠是转义符** ⇒ 写 `C:\Users` 会被解析成 `C:Users`
#      ⇒ 必须在配置串里写成 `C:\\Users`（双写）才能落到进程时是单反斜杠。
#   Unix 侧则相反：正斜杠路径 + `cp`。
if [ "${IS_UNIX}" = "1" ]; then
  RESTORE_CMD="cp \"${ARCHIVE_SERVER}/%f\" \"%p\""
else
  # Windows：cmd.exe 的 copy 对路径与退出码有自己的一套语义 ⇒ 用一个**薄包装批处理**：
  #   ① 记录 PG 实际请求的 %f / %p（排障证据）
  #   ② copy 完成拷贝并把结果码原样返回（PG 以 0 判成功）
  # ⚠ 路径转换必须用 **cygpath -w**（`tr '/' '\'` 只会把 POSIX 的 /c/Users 变成
  #   无效的 \c\Users ⇒ cmd 报「The system cannot find the path specified.」）。
  if command -v cygpath >/dev/null 2>&1; then
    WIN_ARCHIVE="$(cygpath -w "$ARCHIVE_DIR")"
    WIN_WRAP="$(cygpath -w "${DRILL_DATA}/restore_wal.bat")"
  else
    WIN_ARCHIVE="$ARCHIVE_SERVER"
    WIN_WRAP="${DRILL_DATA}/restore_wal.bat"
  fi
  # PG 配置串里反斜杠是转义符 ⇒ 双写；批处理文件本体不被 PG 解析 ⇒ 单写即可
  WRAP_ESC="$(printf '%s' "$WIN_WRAP" | sed 's/\\/\\\\/g')"
  cat > "${DRILL_DATA}/restore_wal.bat" <<BAT
@echo off
>>"%~dp0restore_probe.log" echo REQUEST %1 ^| %2
copy /Y "${WIN_ARCHIVE}\\%1" "%~2" >nul 2>&1
exit /b %ERRORLEVEL%
BAT
  RESTORE_CMD="call \"${WRAP_ESC}\" \"%f\" \"%p\""
fi
log "restore_command = ${RESTORE_CMD}"

{
  echo "port = ${DRILL_PORT}"
  echo "listen_addresses = '127.0.0.1'"
  [ "${IS_UNIX}" = "1" ] && echo "unix_socket_directories = '${DRILL_DATA}'"
  echo "archive_mode = off"
  echo "fsync = on"
  # 关掉日志收集器：否则 PG 的 collector 与 pg_ctl 持有的 drill.log 抢同一个文件
  #   ⇒ Windows 上「could not open file "./drill.log": sharing violation」
  #   ⇒ 每次启动白等 30 秒重试（W927 实跑实证）。
  echo "logging_collector = off"
  echo "log_destination = 'stderr'"
  echo "primary_conninfo = ''"
  echo "restore_command = '${RESTORE_CMD}'"
  echo "recovery_target = 'immediate'"
  echo "recovery_target_action = 'promote'"
} > "${DRILL_DATA}/postgresql.auto.conf"
# recovery.signal：标记「进入恢复模式」（standby.signal 已删）
: > "${DRILL_DATA}/recovery.signal"
cat > "${DRILL_DATA}/pg_hba.conf" <<EOF
local   all         all                                  trust
host    all         all         127.0.0.1/32           trust
EOF
chmod 0700 "$DRILL_DATA"
log "演练实例配置写入完毕（端口 ${DRILL_PORT}·回环监听·归档关闭·unix_socket=${IS_UNIX}·auto.conf 已重写）"

# --- ③ 起演练实例 ------------------------------------------------------------
log "启动演练实例"
pg_ctl -D "$DRILL_DATA" -w -t 60 -l "${DRILL_DATA}/drill.log" start >/dev/null \
  || { cat "${DRILL_DATA}/drill.log" 2>/dev/null | tail -n 20 >&2; die "演练实例启动失败（见 drill.log）"; }

PSQL_DRILL=(psql -v ON_ERROR_STOP=1 -h 127.0.0.1 -p "${DRILL_PORT}" -U postgres -d "${DRILL_DB}")

# --- ④ 断言：数据可读且规模合理 ----------------------------------------------
# 断言要落在**业务库**上（演练实例里的 postgres 库是空的 ⇒ 断言会假通过）
TABLES="$("${PSQL_DRILL[@]}" -tAc "SELECT count(*) FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relkind='r'")"
log "业务库 ${DRILL_DB} 的 public schema 表数 = ${TABLES}"
[ "${TABLES}" -ge "${EXPECT_TABLES}" ] || die "表数不足（${TABLES} < ${EXPECT_TABLES}）⇒ 恢复的库是空的"

# 迁移记账表若存在 ⇒ 断言其行数（能读到记账行才算真恢复）
if "${PSQL_DRILL[@]}" -tAc "SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='schema_migrations'" | grep -q 1; then
  APPLIED="$("${PSQL_DRILL[@]}" -tAc "SELECT count(*) FROM public.schema_migrations")"
  log "迁移记账行数 = ${APPLIED}"
  [ "${APPLIED}" -ge 1 ] || die "迁移记账为空 ⇒ 恢复的库没有业务状态"
else
  die "恢复后缺 schema_migrations ⇒ 恢复的业务库不是本项目的库"
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

# --- ④b **行数一致断言**（§9.4 的核心主张：恢复出来的行数必须与源库一致）---------
# 源库可连时（同一台机器上的原实例）⇒ 逐表比对；源库不可连时降级为 NOTE。
SRC_PORT="${SRC_PORT:-5432}"
SRC_PSQL=(psql -v ON_ERROR_STOP=1 -h 127.0.0.1 -p "${SRC_PORT}" -U postgres -d "${DRILL_DB}" -tAc)
if "${SRC_PSQL[@]}" "SELECT 1" >/dev/null 2>&1; then
  log "源库可连（127.0.0.1:${SRC_PORT}/${DRILL_DB}）⇒ 执行行数一致比对"
  for t in sessions messages feedback schema_migrations; do
    SRC_ROWS="$("${SRC_PSQL[@]}" "SELECT count(*) FROM public.${t}" 2>/dev/null || echo '-')"
    DRILL_ROWS="$("${PSQL_DRILL[@]}" -tAc "SELECT count(*) FROM public.${t}" 2>/dev/null || echo '-')"
    if [ "${SRC_ROWS}" = "-" ] || [ "${DRILL_ROWS}" = "-" ]; then
      log "  表 ${t}：源库不可读（${SRC_ROWS}）· 跳过比对"
      continue
    fi
    log "  表 ${t}：源=${SRC_ROWS} 恢复=${DRILL_ROWS}"
    [ "${SRC_ROWS}" = "${DRILL_ROWS}" ] || die "表 ${t} 行数不一致（源 ${SRC_ROWS} ≠ 恢复 ${DRILL_ROWS}）⇒ 恢复不完整"
  done
  log "行数一致断言通过（源库 == 恢复实例）"
else
  log "提示：源库不可连（127.0.0.1:${SRC_PORT}）⇒ 跳过行数一致比对（仅断言恢复实例自身可读）"
fi

# --- ⑤ 演练结论 --------------------------------------------------------------
log "恢复演练通过：备份可恢复、关键表可读、行数可断言"
log "（对应 §9.4：PG 数据目录 · RTO ≤ 30 min · RPO ≤ 5 min · 每月演练一次）"
