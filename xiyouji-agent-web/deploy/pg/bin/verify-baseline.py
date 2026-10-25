#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify-baseline.py — PG 部署基线静态校验器（xiyouji 架构方案 v2 · D-1 批）

为什么需要它
------------
D-1 批是**离线施工件**批：目标机上的 PG 16 尚未实跑（本机无 psql/pg_ctl），
所以「配置与脚本是否正确」这件事必须先有机器背书，否则本批交付物等于
「一堆看起来对的文本」。

本脚本在**没有 PG 实例**的环境下校验以下四类不变量：

  C1 配置基线不变量  —— postgresql.conf.base / pg_hba.conf.base 的关键项存在且取值合规
  C2 认证基线不变量  —— pg_hba 禁 trust（除本机维护通道）、禁口令明文、兜底 reject 在位
  C3 脚本安全不变量  —— 三个 .sh 禁危险操作、必带关键安全开关、语法可解析
  C4 迁移序列不变量  —— migrations/ 版本号单调递增、每个文件单事务、记账表口径一致

用法
----
    python bin/verify-baseline.py              # 门禁模式（exit 1 = 有 FAIL）
    python bin/verify-baseline.py --report     # 报告模式（打印清单·不判退出码）
    python bin/verify-baseline.py --json <out> # 落 JSON 证据

对应方案：§9.4 备份与恢复演练 · §12.2 合规缺口 2/3 · §7.3 迁移映射
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PG_ROOT = HERE.parent


def resolve_root(explicit: str | None) -> Path:
    """基线根目录。

    `--root` 覆盖用于**反向验证**（把基线拷到临时目录后故意改坏，断言校验器必红）
    ——断言恒真是比「没写断言」更危险的状态，必须能证伪。
    """
    if explicit:
        return Path(explicit).resolve()
    return PG_ROOT


CONF = PG_ROOT / "postgresql.conf.base"
HBA = PG_ROOT / "pg_hba.conf.base"
MIGRATIONS = PG_ROOT / "migrations"

SH_SCRIPTS = ["initdb-bootstrap.sh", "backup.sh", "restore-drill.sh"]

# 危险操作：这些词一旦出现且未带安全开关，就必须 FAIL
FORBIDDEN_PG_PATTERNS = [
    (r"^\s*DROP\s+DATABASE", "禁 DROP DATABASE（脚本只增不删）"),
    (r"^\s*DROP\s+SCHEMA", "禁 DROP SCHEMA（脚本只增不删）"),
    (r"^\s*TRUNCATE\b", "禁 TRUNCATE（会毁数据且不可回滚）"),
    (r"rm\s+-rf\s+\"?\$\{?PGDATA", "禁 rm -rf PGDATA"),
    (r"rm\s+-rf\s+\"?\$BACKUP_ROOT\"?\s*$", "禁对备份根目录整体 rm -rf（轮转须逐份删）"),
    (r"^\s*cp\s+-[a-zA-Z]*r.*PGDATA", "禁以文件拷贝做备份（会丢 WAL 中未 checkpoint 的提交）"),
    # W927 实跑实证：目录格式（-D）配压缩（-z）会直接报错
    #   「pg_basebackup: only tar mode backups can be compressed」⇒ 禁二者同现。
    (r"pg_basebackup[^\n]*\s-D[^\n]*\s-z", "禁目录格式(-D)配压缩(-z)（PG 只允许 tar 格式压缩）"),
]

# 必须在脚本中出现的安全开关
#
# ⚠ 断言必须锚定**代码构造**而非裸词：只匹配 `pg_basebackup` / `backup_label`
# 这类字符串，会在注释与元数据行里先命中 ⇒ 变异改了真正的代码却仍报绿（假阴性）。
# 反向验证 M6/M7 首跑实犯此错 ⇒ 下面一律用带上下文的正则。
REQUIRED_SAFETY = {
    "backup.sh": [
        (r"pg_basebackup\s+-D\s+\"?\$\{?TARGET", "必须真的调用 pg_basebackup -D（不是只在注释里提）"),
        (r"pg_basebackup\s+", "备份必须走 pg_basebackup（禁文件拷贝做备份）"),
        (r"\[ -f \"\$\{TARGET\}/backup_label\" \]", "必须有 backup_label 空壳备份自检（实际守卫语句）"),
        (r"BACKUP_ROOT", "必须使用 BACKUP_ROOT 环境变量（不写死路径）"),
    ],
    "initdb-bootstrap.sh": [
        (r"CREATE TABLE IF NOT EXISTS|IF NOT EXISTS", "必须幂等（IF NOT EXISTS / 先查后建）"),
        (r"server_version_num", "必须校验 PG 版本（方案裁定 PG 16）"),
        (r"NOSUPERUSER", "必须收紧只读角色权限（最小权限）"),
    ],
    "restore-drill.sh": [
        (r"DRILL_PORT:-", "演练实例必须用独立端口（不碰生产实例）"),
        (r"trap cleanup EXIT", "演练必须注册清理 trap（异常路径不留垃圾）"),
        (r"127\.0\.0\.1", "演练实例必须只监听回环"),
    ],
}

# 配置基线必须存在且取值合规的项：(键, 允许值正则, 说明)
CONF_REQUIRED = [
    ("archive_mode", r"^on$", "WAL 归档必须开启（PITR 的唯一来源）"),
    ("wal_level", r"^replica$", "WAL 级别需 replica（支持归档与 PITR）"),
    ("fsync", r"^on$", "fsync 必须开（提交落盘）"),
    ("synchronous_commit", r"^on$", "同步提交（等保向：不接受已确认但未落盘）"),
    ("full_page_writes", r"^on$", "全页写（防断电页撕裂）"),
    ("ssl", r"^on$", "SSL 必须开（§12.4 服务端↔PG 必须 TLS）"),
    ("ssl_min_protocol_version", r"^'?TLSv1\.2'?$", "TLS 下限 1.2"),
    ("listen_addresses", r"^'127\.0\.0\.1,", "监听必须含回环且禁 '*'（私有化不暴露公网）"),
    ("max_connections", r"^\d+$", "必须显式设上限"),
    ("statement_timeout", r"^\d+(ms|s|min|h)$", "必须设语句超时（防慢查询占满连接）"),
    ("idle_in_transaction_session_timeout", r"^\d+(ms|s|min|h)$", "必须设空闲事务超时"),
    ("log_min_duration_statement", r"^\d+$", "必须开慢查询日志"),
    ("logging_collector", r"^on$", "必须开日志收集（§12.3 审计面技术前置）"),
    ("client_encoding", r"^'?'?UTF8'?$", "编码必须 UTF8（中文语料）·client_encoding 可运行时设置"),
    # 注：server_encoding **不在此列**——它是 initdb 固定参数，写进 conf 致 PG FATAL
    #   （W927 实跑实证）⇒ 改列为禁形态（见 CONF_FORBIDDEN），不是必备项。
]

# 禁出现的配置项
CONF_FORBIDDEN = [
    (r"^\s*listen_addresses\s*=\s*'\*'", "禁 listen_addresses='*'（私有化禁暴露）"),
    (r"^\s*ssl\s*=\s*off", "禁 ssl=off（§12.4 必须 TLS）"),
    (r"^\s*fsync\s*=\s*off", "禁 fsync=off（会丢已确认事务）"),
    (r"^\s*synchronous_commit\s*=\s*off", "禁 synchronous_commit=off"),
    # W927 实跑实证：server_encoding 是 initdb 固定参数（GUC_POSTMASTER），
    # 写进 postgresql.conf ⇒ PG 直接 FATAL「parameter "server_encoding" cannot be changed」。
    # 这条是**静态校验查不出、只有真跑能暴露**的缺陷 ⇒ 固化为禁形态防复发。
    (r"^\s*server_encoding\s*=", "禁 server_encoding（initdb 固定参数·写进 conf 致 PG 拒绝启动）"),
    # 同族：unified 写进 conf 同样触发 FATAL
    (r"^\s*unified\s*=", "禁 unified（initdb 固定参数·同 server_encoding）"),
]

# pg_hba 必须满足
HBA_FORBIDDEN = [
    (r"^\s*host\s+all\s+all\s+0\.0\.0\.0/0\s+trust", "禁全网段 trust（明文无认证）"),
    (r"^\s*local\s+all\s+all\s+trust", "禁 local all trust（本地也须身份校验）"),
    (r"^\s*host\s+all\s+all\s+0\.0\.0\.0/0\s+(password|md5)", "禁明文口令认证（须 scram-sha-256）"),
]
HBA_REQUIRED = [
    (r"scram-sha-256", "必须使用 scram-sha-256"),
    (r"reject", "必须有兜底 reject 规则"),
    (r"127\.0\.0\.1/32", "必须显式放行回环"),
]


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def parse_conf(text: str) -> dict:
    """解析 postgresql.conf 的 key=value。

    注意：PG 的配置语法允许**行尾注释**（`key = value  # 说明`），
    故取值时必须先剥掉行尾注释，否则 `fsync = on  # 说明` 会被读成
    `'on  # 说明'` 而误判为不合规（这是本校验器首跑实犯的错）。
    """
    out = {}
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "=" not in s:
            continue
        k, v = s.split("=", 1)
        # 剥行尾注释：找第一个未引号包裹的 '#'
        cut = -1
        in_quote = None
        for i, ch in enumerate(v):
            if in_quote:
                if ch == in_quote:
                    in_quote = None
            elif ch in ("'", '"'):
                in_quote = ch
            elif ch == "#":
                cut = i
                break
        if cut >= 0:
            v = v[:cut]
        out[k.strip()] = v.strip()
    return out


def bash_candidates() -> list[str]:
    """候选 bash 可执行文件（按可用性排序）。

    坑（首跑实犯）：Windows 上 `shutil.which("bash")` 常命中
    `C:\\Windows\\system32\\bash.exe`（WSL 转发器）——**它在没装 WSL 的机器上
    存在但一调用就报 `execvpe(/bin/bash) failed`**。故必须：
      ① 先试 git-bash 的绝对路径（真 POSIX 环境）；
      ② 再试 PATH 里的 bash，但**实际探一次**能否跑（不能跑就跳过）。
    """
    cands: list[str] = []
    for p in (r"C:\Program Files\Git\bin\bash.exe",
              r"C:\Program Files\Git\usr\bin\bash.exe"):
        if Path(p).exists():
            cands.append(p)
    w = shutil.which("bash")
    if w:
        cands.append(w)
    return cands


def bash_available() -> bool:
    """是否有**真能跑**的 bash（探一次，不靠存在性判断）。"""
    for exe in bash_candidates():
        try:
            r = subprocess.run([exe, "-c", "echo ok"], capture_output=True,
                               text=True, errors="replace", timeout=30)
            if r.returncode == 0 and "ok" in (r.stdout or ""):
                return True
        except Exception:  # noqa: BLE001
            continue
    return False


def run_bash_n(path: Path) -> tuple[bool, str]:
    """用 bash -n 做语法检查（不执行）。逐个候选试，第一个能跑的就用它。"""
    errs = []
    for exe in bash_candidates():
        try:
            r = subprocess.run(
                [exe, "-n", str(path)],
                capture_output=True, text=True, errors="replace", timeout=60,
            )
        except Exception as e:  # noqa: BLE001
            errs.append("%s: exec-failed %s" % (exe, e))
            continue
        if r.returncode == 0:
            return True, ""
        errs.append("%s: %s" % (exe, (r.stderr or r.stdout).strip()))
    return False, " | ".join(errs) or "no-usable-bash"


class Result:
    def __init__(self) -> None:
        self.checks: list[dict] = []

    def add(self, cid: str, name: str, ok: bool, detail: str = "") -> None:
        self.checks.append({"id": cid, "name": name, "ok": bool(ok), "detail": detail})

    @property
    def fails(self) -> list[dict]:
        return [c for c in self.checks if not c["ok"]]


def check_conf(res: Result, root: Path) -> None:
    conf = root / "postgresql.conf.base"
    if not conf.exists():
        res.add("C1", "配置基线存在", False, "缺文件：%s" % conf.name)
        return
    text = read_text(conf)
    kv = parse_conf(text)
    for key, val_re, desc in CONF_REQUIRED:
        got = kv.get(key)
        ok = got is not None and re.match(val_re, got) is not None
        res.add("C1", "配置 %s（%s）" % (key, desc), ok,
                "" if ok else "实际值=%r" % got)
    for pat, desc in CONF_FORBIDDEN:
        hit = re.search(pat, text, re.M)
        res.add("C1", "配置禁项（%s）" % desc, hit is None,
                "" if hit is None else "命中：%s" % hit.group(0).strip())
    # 占位符必须在配置里被显式标注（部署期注入）
    res.add("C1", "配置含 @@ 占位符（部署期注入·禁把口令写进文件）",
            "@@" in text, "")


def check_hba(res: Result, root: Path) -> None:
    hba = root / "pg_hba.conf.base"
    if not hba.exists():
        res.add("C2", "认证基线存在", False, "缺文件：%s" % hba.name)
        return
    text = read_text(hba)
    for pat, desc in HBA_FORBIDDEN:
        hit = re.search(pat, text, re.M)
        res.add("C2", "认证禁项（%s）" % desc, hit is None,
                "" if hit is None else "命中：%s" % hit.group(0).strip())
    for pat, desc in HBA_REQUIRED:
        res.add("C2", "认证必备（%s）" % desc, re.search(pat, text, re.M) is not None)
    # 禁把口令写进认证文件
    res.add("C2", "认证文件不含明文口令赋值",
            re.search(r"PASSWORD\s*=\s*['\"][^'\"$]{6,}", text, re.I) is None)


def check_scripts(res: Result, root: Path) -> None:
    if not bash_available():
        res.add("C3", "bash 可用（语法检查前提）", False, "本机无 bash，语法检查跳过")
        return
    for name in SH_SCRIPTS:
        p = root / "bin" / name
        if not p.exists():
            res.add("C3", "脚本存在 %s" % name, False, "缺文件")
            continue
        text = read_text(p)
        for pat, desc in FORBIDDEN_PG_PATTERNS:
            hit = re.search(pat, text, re.M)
            res.add("C3", "%s 禁危险操作（%s）" % (name, desc), hit is None,
                    "" if hit is None else "命中：%s" % hit.group(0).strip())
        for pat, desc in REQUIRED_SAFETY.get(name, []):
            res.add("C3", "%s 必备安全项（%s）" % (name, desc),
                    re.search(pat, text, re.M) is not None)
        ok, detail = run_bash_n(p)
        res.add("C3", "%s 语法检查（bash -n）" % name, ok, detail)
        # 严格模式：set -euo pipefail 必须开（错误不静默继续）
        res.add("C3", "%s 开启严格模式（set -euo pipefail）" % name,
                re.search(r"^set\s+-euo\s+pipefail", text, re.M) is not None)


def check_migrations(res: Result, root: Path) -> None:
    migrations = root / "migrations"
    if not migrations.exists():
        res.add("C4", "迁移目录存在", False, "缺目录：%s" % migrations.name)
        return
    sqls = sorted(migrations.glob("*.sql"))
    res.add("C4", "迁移序列非空（至少 1 个 .sql）", len(sqls) >= 1,
            "实际 %d 个" % len(sqls))
    if not sqls:
        return
    versions = []
    for p in sqls:
        m = re.match(r"^(\d{4})_", p.name)
        if m:
            versions.append((int(m.group(1)), p.name))
    res.add("C4", "迁移文件版本号四位零填充且可解析", len(versions) == len(sqls),
            "可解析 %d / 共 %d" % (len(versions), len(sqls)))
    nums = [v for v, _ in versions]
    res.add("C4", "迁移版本号单调递增（无重复·无倒序）",
            nums == sorted(nums) and len(set(nums)) == len(nums),
            "版本序列=%s" % nums)
    for p in sqls:
        text = read_text(p)
        # 单事务：PG 的 DDL 本身事务性 ⇒ 迁移文件应显式 BEGIN/COMMIT 包住
        has_begin = re.search(r"^\s*BEGIN\s*;", text, re.M | re.I) is not None
        has_commit = re.search(r"^\s*COMMIT\s*;", text, re.M | re.I) is not None
        res.add("C4", "%s 单事务包裹（BEGIN/COMMIT）" % p.name,
                has_begin and has_commit,
                "BEGIN=%s COMMIT=%s" % (has_begin, has_commit))
        # 禁破坏性语句
        res.add("C4", "%s 禁 DROP/TRUNCATE" % p.name,
                re.search(r"^\s*(DROP\s+(TABLE|SCHEMA|DATABASE)|TRUNCATE)\b", text, re.M | re.I) is None)
        # W927 实跑实证：PG 的 SQL 注释只认 `--`；`#` 会让 psql 直接语法错误
        #   `ERROR: syntax error at or near "#"` ⇒ 固化为禁形态防复发。
        hash_comments = re.findall(r"^\s*#.*$", text, re.M)
        res.add("C4", "%s 禁 `#` 注释（PG 只认 `--`·否则 psql 语法错误）" % p.name,
                not hash_comments,
                "" if not hash_comments else "命中 %d 行：%s" % (len(hash_comments), hash_comments[0].strip()[:60]))


def main() -> int:
    ap = argparse.ArgumentParser(description="PG 部署基线静态校验器")
    ap.add_argument("--report", action="store_true", help="报告模式（不判退出码）")
    ap.add_argument("--json", metavar="OUT", help="落 JSON 证据到指定路径")
    ap.add_argument("--root", metavar="DIR",
                    help="基线根目录覆盖（用于反向验证：改坏副本后断言本校验器必红）")
    args = ap.parse_args()

    root = resolve_root(args.root)

    res = Result()
    check_conf(res, root)
    check_hba(res, root)
    check_scripts(res, root)
    check_migrations(res, root)

    total = len(res.checks)
    failed = len(res.fails)
    passed = total - failed

    for c in res.checks:
        if not c["ok"]:
            print("  FAIL  %-6s %s%s" % (c["id"], c["name"],
                                         ("（%s）" % c["detail"]) if c["detail"] else ""))
    print("---- D-1 部署基线静态校验：%d/%d 通过 · %d FAIL ----" % (passed, total, failed))

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({
            "total": total, "passed": passed, "failed": failed,
            "checks": res.checks,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print("证据已落：%s" % out)

    if args.report:
        return 0
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
