# PG 部署基线（PostgreSQL 16 · 自建单机）

> **批次**：W927 · D-1 基础设施批（离线施工件）
> **来源**：[系统架构方案 v2 §7 存储选型 · §9 容灾 · §12 合规](../../../11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md)
> **状态**：**离线施工件 —— 尚未在真实 PG 实例上实跑**（本机无 `psql`/`pg_ctl`，Docker daemon 未启动）。机器背书来自静态校验器（66/66）与反向验证（11/11 变异可证伪），**不等于**运行时验证。
> **读者**：私有化部署的实施者 / 后续 Agent（默认无对话上下文，可独立执行）

---

## 0. 这个目录解决什么

方案 v2 §7.1 裁定采用 **PostgreSQL 16 自建单机**（不上托管：成本敏感 + 私有化 + 等保）。
本目录是**档 2 的 D-1 基础设施批**产出物，把「装一个 PG」这件事从口头方案变成可评审、可复跑的施工件：

| 文件 | 作用 | 跑在哪 |
|:---|:---|:---|
| `postgresql.conf.base` | 服务端配置基线（WAL 归档 / TLS / 内存 / 日志 / 编码） | 目标机 `$PGDATA` |
| `pg_hba.conf.base` | 认证基线（最小权限 + 兜底 reject） | 目标机 `$PGDATA` |
| `bin/initdb-bootstrap.sh` | 幂等初始化：角色 / 数据库 / 权限 / 迁移记账表 | 目标机 |
| `bin/backup.sh` | 每日全量备份（`pg_basebackup`）+ 保留期轮转 + 空壳自检 | 目标机（cron） |
| `bin/restore-drill.sh` | 恢复演练：恢复临时实例 → 断言行数 → 销毁 | 目标机（每月） |
| `bin/verify-baseline.py` | **静态校验器**：无 PG 环境即可跑（本批实跑 66/66） | 开发机 / CI |
| `bin/_mutation_test.py` | **反向验证**：改坏副本 ⇒ 断言校验器必红（本批 11/11） | 开发机 / CI |
| `migrations/0001_baseline.sql` | 迁移序列骨架（记账表 + 审计归档表） | 目标机（psql 执行） |

---

## 1. 关键设计口径（逐条对应方案）

| 口径 | 方案出处 | 本目录的落地 |
|:---|:---|:---|
| 备份必须用 `pg_basebackup`（免停机一致性快照），**禁文件拷贝** | §9.4 | `backup.sh` 用 `pg_basebackup -X none -R`；校验器**禁** `cp -r ... PGDATA` 形态 |
| WAL 归档是 PITR 的唯一来源 ⇒ 归档必须开、目录必须分盘 | §9.2 F9 / §9.4 | `archive_mode = on` + `archive_timeout = 300`（RPO ≤ 5 min）+ 备份脚本校验归档目录与数据目录**不同盘** |
| 备份要**被恢复过**才算验证过 | §9.4「每月一次恢复演练」 | `restore-drill.sh` 恢复到独立端口的临时实例并断言表数/列数/行数 |
| 服务端 ↔ PG 必须 TLS；内网也不豁免 | §12.4 | `ssl = on` + `ssl_min_protocol_version = TLSv1.2`；`pg_hba` 无 `trust`（除本机 peer） |
| 最小权限：应用账号 ≠ 超级用户 | §12.2 缺口 2 | `initdb-bootstrap.sh` 建三角色（app / ro / postgres），只读角色 `NOSUPERUSER NOCREATEDB NOREPLICATION` |
| 数据分级标签入库即校验 | §12.1 / §12.5 | `audit_archive.data_class` 带 `CHECK (IN ('L1','L2','L3','L4'))` |
| 迁移必须可逆且留证 | §5.3 铁律 6 | 迁移文件**单事务**包裹（失败整段回滚）+ `schema_migrations` 记账（version 单调 + checksum） |
| 审计只追加、销毁须留证 | §12.3 | `audit_archive` 只提供追加表；留存期与销毁事件由 D-3 合规批实现 |

---

## 2. 怎么用（目标机执行顺序）

```bash
# ① 前提：已装 PostgreSQL 16，已 initdb，PGDATA 与归档目录/备份目录分盘
export PGDATA=/var/lib/pgsql/16/data
export ARCHIVE_DIR=/var/lib/pgsql/archive
export BACKUP_ROOT=/var/lib/pgsql/backup
export DRILL_ROOT=/var/lib/pgsql/drill

# ② 注入占位符（禁把口令写进基线文件）
#    @@INTERNAL_CIDR@@ @@SSL_CERT@@ @@SSL_KEY@@ @@SSL_CA@@
sed -e "s|@@INTERNAL_CIDR@@|10.0.0.0/8|" \
    -e "s|@@SSL_CERT@@|/etc/pgsql/ssl/server.crt|" \
    -e "s|@@SSL_KEY@@|/etc/pgsql/ssl/server.key|" \
    -e "s|@@SSL_CA@@|/etc/pgsql/ssl/ca.crt|" \
    postgresql.conf.base > "$PGDATA/postgresql.conf"
cp pg_hba.conf.base "$PGDATA/pg_hba.conf"   # 同样需替换 @@INTERNAL_CIDR@@
pg_ctl reload

# ③ 幂等初始化（角色 / 库 / 权限 / 迁移记账表）
APP_PASSWORD='...' RO_PASSWORD='...' bash bin/initdb-bootstrap.sh

# ④ 迁移序列（业务表属 D-2 批；本批只有骨架）
psql -v ON_ERROR_STOP=1 -U postgres -d xiyouji -f migrations/0001_baseline.sql

# ⑤ 备份（每日 cron）
bash bin/backup.sh

# ⑥ 恢复演练（每月）
bash bin/restore-drill.sh
```

---

## 3. 机器背书（本批实跑结果）

| 校验 | 命令 | 结果 |
|:---|:---|:---|
| 静态基线校验 | `py -3 bin/verify-baseline.py` | **66/66 通过 · 0 FAIL**（证据：`scripts/output/_w927_pg_baseline.json`） |
| 反向验证 | `py -3 bin/_mutation_test.py` | **11/11 变异可证伪**（含基线未变异必须绿） |
| Shell 语法 | `bash -n`（三个 .sh） | **3/3 通过**（经 git-bash；WSL 的 `bash.exe` 是坏转发器，不可信） |

### 3.1 反向验证的变异矩阵

| 变异 | 改坏什么 | 期望 | 实测 |
|:--|:---|:---|:---|
| M1 | `archive_mode = off` | 必红 | ✅ 抓住 |
| M2 | `fsync = off` | 必红 | ✅ 抓住 |
| M3 | `ssl = off` | 必红 | ✅ 抓住 |
| M4 | `listen_addresses = '*'` | 必红 | ✅ 抓住 |
| M5 | 认证放开全网段 `trust` | 必红 | ✅ 抓住 |
| M6 | 备份改用文件拷贝 | 必红 | ✅ 抓住（**首跑漏检·已修**） |
| M7 | 删空壳备份自检 | 必红 | ✅ 抓住（**首跑漏检·已修**） |
| M8 | 去掉 `set -euo pipefail` | 必红 | ✅ 抓住 |
| M9 | 迁移去掉单事务包裹 | 必红 | ✅ 抓住 |
| M10 | 迁移引入 `DROP TABLE` | 必红 | ✅ 抓住 |

> **M6/M7 首跑漏检的教训（已沉淀）**：两条断言最初写成「文件里出现过 `pg_basebackup` / `backup_label` 即可」——但这两个词在**注释与元数据行**里也会先命中，于是变异改了真正的代码、断言却仍读到了别处的词 ⇒ **假阴性**。修法：断言必须锚定**代码构造**（`pg_basebackup\s+-D\s+"?\$\{?TARGET`、`\[ -f "\$\{TARGET\}/backup_label" \]`），而不是裸词。
> 推广：任何「某文件必须包含 X」的断言，若 X 是常见词，必须同时给出**上下文锚点**或**禁形态**，否则变异测试会告诉你它是恒真的。

---

## 4. 实跑状态（2026-10-25 · 真实 PostgreSQL 16.4 实例）

> **环境**：Windows 11 + **PostgreSQL 16.4 免安装二进制**（官方 EDB zip，解压即用，**不需要 Docker / 不需要管理员 / 不进仓库**）。本机无 Docker ⇒ 该路径是可行替代。
> **完整原始输出**：`scripts/output/_w927_pg_runtime_evidence.txt`（111 行机器证据）。

### 4.1 已实跑通过（6 项）

| # | 项 | 实测结果 |
|:--:|:---|:---|
| 1 | `initdb-bootstrap.sh` 幂等性 | ✅ 连跑两次：第一次建角色/库/权限，第二次全部「已存在，跳过创建」 |
| 2 | `backup.sh` 真实备份 | ✅ `pg_basebackup` rc=0；自检通过（`backup_label` + `postgresql.conf` + `base/` 均在位）；保留期轮转 + WAL 归档轮转正常 |
| 3 | **恢复演练行数一致** | ✅ **真·PITR 演练**：PG 经 `restore_command` 从归档取回 `000000010000000000000019`；**逐表比对源库 == 恢复实例**：`sessions 6==6` · `messages 50==50` · `feedback 20==20` · `schema_migrations 1==1` |
| 4 | WAL 归档连续性 | ✅ 段 `…0001` → `…001B` **连续无缺口**（27 段） |
| 5 | 备份/归档**分盘校验** | ✅ **两次都验到**：同盘（C: vs C:）被脚本**如实拦下**（`FATAL: 备份目录与 PGDATA 同盘`）；分盘（C: vs D:）通过 |
| 6 | TLS 实握手 | ✅ `pg_stat_ssl.ssl = true` · **TLSv1.3** · cipher `TLS_AES_256_GCM_SHA384` |

基线参数生效核验（实读 `pg_settings`）：`archive_mode=on` · `ssl=on` · `ssl_min_protocol_version=TLSv1.2` · `wal_level=replica` · `max_connections=200` · `client_encoding=UTF8` · `fsync=on` · `synchronous_commit=on` · `full_page_writes=on` · `log_min_duration_statement=1000` · `logging_collector=on` · `statement_timeout=30000`。

### 4.2 实跑抓出的 4 个真缺陷（静态校验查不出 · 已全部修掉并固化为守卫）

| # | 缺陷 | 症状 | 固化守卫 |
|:--:|:---|:---|:---|
| 1 | `server_encoding` 写进 `postgresql.conf` | PG **直接 FATAL 拒绝启动**（`parameter "server_encoding" cannot be changed`）——它是 initdb 固定参数 | 静态校验器列**禁形态** + 变异 M11 |
| 2 | 迁移文件用 `#` 注释 | `psql` **语法错误**（`syntax error at or near "#"`）——PG 的 SQL 只认 `--` | 静态校验器列**禁形态** + 变异 M12 |
| 3 | `pg_basebackup -D` 配 `-z` | 备份报错（`only tar mode backups can be compressed`） | 静态校验器列**禁形态** + 变异 M13 |
| 4 | 恢复演练对备份目录结构的假设错 | 演练实例起不来（`could not open file ".../global/pg_control"`）——`pg_basebackup -D` 的输出目录**本身就是 PGDATA 镜像**（`base/` 与 `global/` 是**兄弟**） | 恢复脚本内自校验（缺 `PG_VERSION` / `global/pg_control` 即 FATAL） |

> 第 4 项连**变异测试都测不出来**（它是语义误解，不是文本形态）⇒ **只有真跑能暴露**。这是「静态背书 ≠ 运行时可用」的第一份实证。

### 4.3 仍待实跑（3 项 · 不得当作已验证）

| # | 待实跑项 | 验收判据 | 计划批次 |
|:--:|:---|:---|:---|
| 7 | **迁移器端到端** | `0001_baseline.sql` 经**迁移器**（非 psql 直跑）执行后，记账表 version/checksum 正确、失败可整段回滚 | **D-2 批**（迁移器在 D-2 实现） |
| 8 | **容量实测** | 按 §7.2 测算的读/写 QPS 压测，PG 单实例余量 ≥ 1 个数量级 | D-2 批 |
| 9 | **审计留存与销毁留证** | `audit_archive` 分级 CHECK 生效；留存期 ≥ 180 天与销毁留证跑通 | **D-3 批** |

> **结论**：D-1 的**基础设施层**（配置 / 初始化 / 备份 / 恢复演练 / 分盘 / TLS / 归档）已在真实 PG 16.4 上验证通过；**应用迁移器、容量、审计留存**三项属 D-2 / D-3 范围，仍未验证。

### 4.4 本次验证跑的平台适配（**产品基线保持 Linux 形态不变**）

| 项 | 验证跑（Windows） | 产品基线（Linux） |
|:---|:---|:---|
| `archive_command` | cmd 等价式 | POSIX `test ! -f … && cp` |
| `restore_command` | 薄包装批处理（cmd 的 `copy` + `%p` 正斜杠适配） | `cp` |
| `shared_buffers` | 1GB（本机空闲内存 5 GB） | 2GB（4C8G 目标机） |
| `unix_socket_directories` | **不设**（Windows 版 PG 不支持） | 设（真类 Unix） |

> ⚠ **跨平台判据坑**：**git-bash 的 `uname -s` 返回 `MINGW64_NT-…` 而不是 `Windows`** ⇒ 只写 `= "Windows"` 判等会误判为类 Unix ⇒ 把 POSIX 路径（`/c/Users/…`）写给 Windows 版 PG ⇒ 启动即 FATAL（`could not create lock file`）。判据必须覆盖 `MINGW*` / `MSYS*` / `CYGWIN*` / `Windows*` 全族。
> ⚠ **PG 配置串里反斜杠是转义符** ⇒ Windows 路径在配置里要双写 `\`。

---

## 5. 边界声明

- 本目录**不含任何口令、密钥、私钥**；`@@占位符@@` 一律由部署期注入。
- 本目录**不改 `xiyouji-agent-web/` 的任何应用代码**（`server/`、`src/` 一行未动）——D-1 只做基础设施。
- 本目录**不引入任何新的运行时依赖**（只用 PG 自带工具 + bash + Python 标准库）。
- 本目录**不做容器编排**（compose 属 D-1 实跑后的可选形态，私有化默认裸机 + systemd）。
- 本批**未改任何管控脚本**（`scripts/verify_delivery.py` 等一行未动）。
