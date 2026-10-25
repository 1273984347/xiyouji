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

## 4. **待实跑清单（本批未验证项 · 不得当作已验证）**

以下每一项都**必须**在有 PG 16 环境后实跑并留证；未做之前，对外不得声称「PG 已验证」。

| # | 待实跑项 | 验收判据 | 计划批次 |
|:--|:---|:---|:---|
| 1 | `initdb-bootstrap.sh` 幂等性 | 连跑两次，第二次输出全为「已存在，跳过创建」，且表/角色/库数量不变 | D-1 实跑 |
| 2 | `backup.sh` 真实备份 | 产出目录含 `backup_label` + `base/` + `PG_VERSION`；`pg_basebackup` rc=0 | D-1 实跑 |
| 3 | **恢复演练** | `restore-drill.sh` 恢复后 `schema_migrations` 行数与源库一致（**这是 §9.4 RTO/RPO 的唯一实证**） | D-1 实跑 · 每月 |
| 4 | WAL 归档连续性 | 归档目录有连续段、无缺口；`archive_timeout` 生效（切段间隔 ≤ 5 min） | D-1 实跑 |
| 5 | 备份/归档**分盘校验** | 备份脚本的同盘检查在本机拓扑上真的能拦住（构造同盘场景） | D-1 实跑 |
| 6 | TLS 实握手 | `ssl_is_used` 在应用连接上为 on；证书链有效 | D-1 实跑 |
| 7 | 迁移器端到端 | `0001_baseline.sql` 经迁移器执行后记账表有正确 version/checksum | **D-2 批**（迁移器在 D-2 实现） |
| 8 | 容量实测 | 按 §7.2 测算的读/写 QPS 压测，PG 单实例余量 ≥ 1 个数量级 | D-2 批 |
| 9 | 审计归档表 | `audit_archive` 分级 CHECK 生效；留存期 ≥ 180 天与销毁留证跑通 | **D-3 批** |

---

## 5. 边界声明

- 本目录**不含任何口令、密钥、私钥**；`@@占位符@@` 一律由部署期注入。
- 本目录**不改 `xiyouji-agent-web/` 的任何应用代码**（`server/`、`src/` 一行未动）——D-1 只做基础设施。
- 本目录**不引入任何新的运行时依赖**（只用 PG 自带工具 + bash + Python 标准库）。
- 本目录**不做容器编排**（compose 属 D-1 实跑后的可选形态，私有化默认裸机 + systemd）。
- 本批**未改任何管控脚本**（`scripts/verify_delivery.py` 等一行未动）。
