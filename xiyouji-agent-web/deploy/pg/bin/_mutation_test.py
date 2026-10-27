#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_mutation_test.py — verify-baseline.py 的反向验证（W927 · D-1 批）

为什么需要：断言恒真是比「没写断言」更危险的状态——它会一直报 OK，掩盖真缺陷。
本脚本把基线拷到临时目录后**故意改坏**，断言本校验器必红；再恢复，断言必绿。

用法（开发机 / CI 同轨）：
    python bin/_mutation_test.py
    python bin/_mutation_test.py --json <out.json>

退出码：0 = 全部变异均可证伪；1 = 有变异未被抓住（断言恒真）
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PG_ROOT = HERE.parent
VERIFIER = HERE / "verify-baseline.py"

# (变异名, 目标文件相对路径, 旧串, 新串, 期望被抓到的判据关键词)
MUTATIONS = [
    ("M1-配置：关掉归档", "postgresql.conf.base",
     "archive_mode = on", "archive_mode = off", "archive_mode"),
    ("M2-配置：关掉 fsync", "postgresql.conf.base",
     "fsync = on", "fsync = off", "fsync"),
    ("M3-配置：禁 TLS", "postgresql.conf.base",
     "ssl = on", "ssl = off", "ssl=off"),
    ("M4-配置：监听全网段", "postgresql.conf.base",
     "listen_addresses = '127.0.0.1,", "listen_addresses = '*',", "listen_addresses='*'"),
    ("M5-认证：放开全网段 trust", "pg_hba.conf.base",
     "host    all         all         0.0.0.0/0               reject",
     "host    all         all         0.0.0.0/0               trust", "trust"),
    ("M6-脚本：改用文件拷贝做备份", "bin/backup.sh",
     "pg_basebackup -D", "cp -r $PGDATA", "pg_basebackup"),
    ("M7-脚本：删掉空壳备份自检", "bin/backup.sh",
     '[ -f "${TARGET}/backup_label" ] || die "备份缺 backup_label ⇒ 非有效全量备份"',
     ':', "backup_label"),
    ("M8-脚本：去掉严格模式", "bin/initdb-bootstrap.sh",
     "set -euo pipefail", "set -u", "严格模式"),
    ("M9-迁移：去掉单事务包裹", "migrations/0001_baseline.sql",
     "BEGIN;", "-- BEGIN removed;", "单事务"),
    ("M10-迁移：破坏性语句", "migrations/0001_baseline.sql",
     "CREATE INDEX IF NOT EXISTS idx_schema_migrations_applied_at",
     "DROP TABLE schema_migrations CASCADE;\nCREATE INDEX IF NOT EXISTS idx_schema_migrations_applied_at",
     "DROP/TRUNCATE"),
    # W927 实跑实证：server_encoding 写进 conf ⇒ PG FATAL 拒绝启动（静态层原本查不出）
    ("M11-配置：写回 initdb 固定参数", "postgresql.conf.base",
     "client_encoding = 'UTF8'",
     "client_encoding = 'UTF8'\nserver_encoding = 'UTF8'", "server_encoding"),
    # W927 实跑实证：PG 的 SQL 注释只认 `--`；`#` 头注释让 psql 直接语法错误
    ("M12-迁移：混入 MySQL 风格 # 注释", "migrations/0001_baseline.sql",
     "-- 职责：建立「迁移机制本身」",
     "# 职责：建立「迁移机制本身」", "`#` 注释"),
    # W927 实跑实证：目录格式(-D)配压缩(-z) ⇒ pg_basebackup 直接报错
    ("M13-脚本：目录格式配压缩", "bin/backup.sh",
     'pg_basebackup -D "$TARGET" -X none -R -c fast',
     'pg_basebackup -D "$TARGET" -X none -R -z -c fast', "压缩"),
    # ---- W934 · D-2a：C5 组（应用迁移批不变量） ----
    # M14：去掉 role CHECK 约束 ⇒ 方案 §7.3 要求的等价约束丢失
    ("M14-迁移：去掉 role CHECK 约束", "migrations/0002_app_tables.sql",
     "role       TEXT        NOT NULL CHECK (role IN ('user', 'assistant')),",
     "role       TEXT        NOT NULL,", "role CHECK"),
    # M15：feedback 唯一维度退回普通索引 ⇒ W917 B-DB-01 的「同消息双 verdict」防线消失
    ("M15-迁移：feedback 唯一索引退化", "migrations/0002_app_tables.sql",
     "CREATE UNIQUE INDEX IF NOT EXISTS idx_feedback_message ON feedback (message_id);",
     "CREATE INDEX IF NOT EXISTS idx_feedback_message ON feedback (message_id);", "唯一维度"),
    # M16：时间列退回 TEXT ⇒ §7.4 生命周期的日期算术无从谈起
    ("M16-迁移：时间列退回 TEXT", "migrations/0002_app_tables.sql",
     "    created_at    TIMESTAMPTZ NOT NULL,",
     "    created_at    TEXT NOT NULL,", "TIMESTAMPTZ"),
    # M17：迁移器去掉只读 ⇒ 可能改坏全仓唯一不可重建的数据
    ("M17-迁移器：源库可写", "bin/migrate-sqlite-to-pg.ts",
     "new Database(sqlitePath, { readonly: true, fileMustExist: true })",
     "new Database(sqlitePath, { fileMustExist: true })", "只读"),
    # M18：默认权限漏一条 FOR ROLE ⇒ 该条只对执行者生效（静默失效）
    ("M18-授权：漏 FOR ROLE", "bin/initdb-bootstrap.sh",
     "ALTER DEFAULT PRIVILEGES FOR ROLE ${APP_USER}",
     "ALTER DEFAULT PRIVILEGES FOR ROLE postgres", "FOR ROLE"),
    # M19：把记账表的建表提到设权限之前 ⇒ 顺序反了，先建的表无授权
    ("M19-授权：建表早于设权限", "bin/initdb-bootstrap.sh",
     'log "设置权限矩阵（默认权限 FOR ROLE=${APP_USER}·先设权限后建表）"',
     'log "设置权限矩阵（默认权限 FOR ROLE=${APP_USER}·先设权限后建表）"\n'
     '"${PSQL_APP[@]}" -c "CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY)" >/dev/null',
     "先设默认权限后建表"),
    # M20：三重对账少一项 ⇒ 退化成「只比行数」的假对账
    ("M20-对账：少一项", "bin/migrate-sqlite-to-pg.ts",
     "content_equal: contentEqual,", "content_equality: contentEqual,", "三重对账"),
    # M21：迁移器改用模板串拼 SQL ⇒ 参数化防线被拆
    ("M21-迁移器：模板串拼 SQL", "bin/migrate-sqlite-to-pg.ts",
     '      "SELECT id, title, model, sdk_session_id, created_at, updated_at FROM sessions",',
     "      `SELECT ${cols.join(', ')} FROM sessions`,",
     "禁模板串拼 SQL"),
    # M22：去掉记账表的 owner 转移 ⇒ 迁移序列以应用账号跑时报「must be owner of table」
    #   （W934 实跑实证·静态层原本查不出——是所有权问题不是形态问题）
    ("M22-授权：不转记账表 owner", "bin/initdb-bootstrap.sh",
     "ALTER TABLE schema_migrations OWNER TO ${APP_USER}",
     "-- owner 不转移", "owner"),
]


def run_verifier(root: Path) -> tuple[int, str]:
    r = subprocess.run(
        [sys.executable, str(VERIFIER), "--root", str(root)],
        capture_output=True, text=True, errors="replace", timeout=180,
    )
    return r.returncode, r.stdout + r.stderr


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", metavar="OUT")
    args = ap.parse_args()

    results = []
    base_rc, base_out = run_verifier(PG_ROOT)
    ok_base = base_rc == 0
    results.append({
        "mutation": "M0-基线未变异", "caught": ok_base,
        "detail": "未变异基线 rc=%d（期望 0）" % base_rc,
    })
    print("  %s M0-基线未变异（rc=%d·期望 0）" % ("PASS" if ok_base else "FAIL", base_rc))

    for name, rel, old, new, keyword in MUTATIONS:
        with tempfile.TemporaryDirectory(prefix="w927_mut_") as td:
            tmp = Path(td) / "pg"
            shutil.copytree(PG_ROOT, tmp, ignore=shutil.ignore_patterns("__pycache__"))
            target = tmp / rel
            text = target.read_text(encoding="utf-8")
            if old not in text:
                results.append({"mutation": name, "caught": False,
                                "detail": "变异未生效：旧串未命中（假阴性风险）"})
                print("  FAIL %s：旧串未命中 ⇒ 变异没打准" % name)
                continue
            target.write_text(text.replace(old, new, 1), encoding="utf-8")
            rc, out = run_verifier(tmp)
            caught = rc != 0 and keyword in out
            results.append({
                "mutation": name, "caught": caught,
                "detail": "rc=%d·命中判据=%s" % (rc, keyword in out),
            })
            print("  %s %s（rc=%d·判据命中=%s）" % ("PASS" if caught else "FAIL", name, rc, keyword in out))

    total = len(results)
    caught = sum(1 for r in results if r["caught"])
    failed = total - caught
    print("---- 反向验证：%d/%d 变异可证伪 ----" % (caught, total))
    if args.json:
        outp = Path(args.json)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(json.dumps({"total": total, "caught": caught, "failed": failed,
                                    "results": results}, ensure_ascii=False, indent=2),
                        encoding="utf-8")
        print("证据已落：%s" % outp)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
