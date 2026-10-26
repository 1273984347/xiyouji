#!/usr/bin/env python3
"""_w823_db_schema_probe.py — agent-web SQLite 存储层表设计审查取证脚本（W823）。

本脚本是《数据库表设计审查报告-2026-10-20》的**可复算证据源**：
报告 §三~§六 的每一项缺陷判定，均由本脚本在**库副本**上实跑产出，
读者无需回看会话历史即可复算。

四组取证（子命令）：

    schema   现役库结构 / PRAGMA 态 / 行数 / 外键孤儿行实况 / 索引清单
    faults   13 项缺陷复现（全部在副本上做，原库只读不改）
    bench    查询模式代价实测（N+1 vs GROUP BY / 索引有无 / 会话列表代价模型）
    hygiene  数据卫生实测（时间戳格式 / JSON 合法性 / 排序稳定性 / 悬空行）

**安全约定（不可放宽）**：

1. 凡涉及写入的取证（faults）**一律先复制库再操作**，原库只读；
2. 副本操作前先 `PRAGMA wal_checkpoint(TRUNCATE)` 并用 sqlite3 backup API 落副本，
   保证副本与原库一致且不产生半截 WAL；
3. 任一子命令的判据未执行（目录/文件不存在、库不可读）一律**非零退出**，
   禁静默跳过（对齐 W816「门禁自报 100% 却扫到 0 篇」同类缺陷的修法）；
4. 不依赖第三方库（仅标准库 sqlite3），可在 Windows / Linux / macOS 直接跑。

用法（Windows PowerShell 侧 `python` 是应用执行存根，用 `py -3`）：

    py -3 scripts/_w823_db_schema_probe.py schema
    py -3 scripts/_w823_db_schema_probe.py faults
    py -3 scripts/_w823_db_schema_probe.py bench
    py -3 scripts/_w823_db_schema_probe.py hygiene
    py -3 scripts/_w823_db_schema_probe.py all --db "<chat.db 路径>"

退出码：0 = 全部子命令执行完毕；2 = 输入错误（库不存在 / 不可读 / 副本失败）。
"""
import argparse
import datetime
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import time

DEFAULT_DB = os.path.join("xiyouji-agent-web", "data", "chat.db")


def resolve_db(path):
    """相对路径按脚本自身 ROOT 解析（禁按调用方 cwd——W816 同类缺陷修法）。"""
    if os.path.isabs(path):
        return path
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, path)


def open_ro(db_path):
    """只读打开现役库；不存在或不可读一律 raise（由 main 收敛为 exit 2）。"""
    if not os.path.exists(db_path):
        raise FileNotFoundError("库文件不存在：%s" % db_path)
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    return con


def make_copy(db_path):
    """落一份库副本（sqlite3 backup API）；返回副本路径。调用方负责删除。"""
    tmpdir = tempfile.mkdtemp(prefix="w823_dbprobe_")
    copy_path = os.path.join(tmpdir, "chat_copy.db")
    src = sqlite3.connect(db_path)
    src.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    dst = sqlite3.connect(copy_path)
    src.backup(dst)
    dst.close()
    src.close()
    return copy_path


def drop_copy(copy_path):
    shutil.rmtree(os.path.dirname(copy_path), ignore_errors=True)


def hr(title):
    print("\n" + "=" * 72)
    print("== %s" % title)
    print("=" * 72)


# ---------------------------------------------------------------- schema
def cmd_schema(db_path):
    con = open_ro(db_path)
    cur = con.cursor()
    hr("现役库结构（sqlite_master 全量）")
    for typ, name, sql in cur.execute(
            "SELECT type, name, sql FROM sqlite_master ORDER BY type, name"):
        print("[%s] %s" % (typ, name))
        if sql:
            print("    " + sql.replace("\n", " "))

    hr("PRAGMA 关键状态")
    for label, sql in [
        ("foreign_keys（0 = 外键强制关闭）", "PRAGMA foreign_keys"),
        ("journal_mode", "PRAGMA journal_mode"),
        ("user_version（0 = 无迁移版本追踪）", "PRAGMA user_version"),
        ("page_size", "PRAGMA page_size"),
        ("page_count", "PRAGMA page_count"),
        ("freelist_count", "PRAGMA freelist_count"),
    ]:
        print("  %-34s = %s" % (label, cur.execute(sql).fetchone()[0]))
    print("  %-34s = %s" % ("integrity_check", cur.execute("PRAGMA integrity_check").fetchone()[0]))

    hr("行数与外键孤儿行实况")
    for t in ("sessions", "messages", "feedback"):
        try:
            print("  %-10s 行数 = %d" % (t, cur.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]))
        except sqlite3.Error as exc:
            print("  %-10s 读表失败：%s" % (t, exc))
    checks = [
        ("messages 无父会话", "SELECT COUNT(*) FROM messages m LEFT JOIN sessions s"
                              " ON m.session_id=s.id WHERE s.id IS NULL"),
        ("feedback 无父消息", "SELECT COUNT(*) FROM feedback f LEFT JOIN messages m"
                               " ON f.message_id=m.id WHERE m.id IS NULL"),
        ("feedback 无父会话", "SELECT COUNT(*) FROM feedback f LEFT JOIN sessions s"
                               " ON f.session_id=s.id WHERE s.id IS NULL"),
    ]
    for label, sql in checks:
        print("  孤儿行 %-20s = %d" % (label, cur.execute(sql).fetchone()[0]))

    hr("索引清单")
    for name, tbl, sql in cur.execute(
            "SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index' ORDER BY tbl_name, name"):
        print("  [%s] %s :: %s" % (tbl, name, sql or "(auto index)"))

    hr("EXPLAIN QUERY PLAN（现役库真实计划）")
    plans = [
        ("会话列表 ORDER BY updated_at DESC",
         "SELECT * FROM sessions ORDER BY updated_at DESC"),
        ("会话消息 ORDER BY created_at",
         "SELECT * FROM messages WHERE session_id = ? ORDER BY created_at ASC"),
        ("反馈 30 天窗口 GROUP BY",
         "SELECT verdict, COUNT(*) FROM feedback WHERE created_at >= ? GROUP BY verdict"),
    ]
    for label, sql in plans:
        print("-- %s" % label)
        for row in cur.execute("EXPLAIN QUERY PLAN " + sql, ("x",) if "?" in sql else ()):
            print("     %s" % row[3])
    con.close()


# ---------------------------------------------------------------- faults
def cmd_faults(db_path):
    copy_path = make_copy(db_path)
    con = sqlite3.connect(copy_path)
    cur = con.cursor()
    try:
        hr("F-01 外键强制关闭 → ON DELETE CASCADE 不触发")
        print("  PRAGMA foreign_keys = %d（0 = 关闭·SQLite 默认值）"
              % cur.execute("PRAGMA foreign_keys").fetchone()[0])
        sid = cur.execute(
            "SELECT session_id FROM messages GROUP BY session_id HAVING COUNT(*)>0 LIMIT 1"
        ).fetchone()[0]
        before = cur.execute("SELECT COUNT(*) FROM messages WHERE session_id=?", (sid,)).fetchone()[0]
        cur.execute("DELETE FROM sessions WHERE id=?", (sid,))
        after = cur.execute("SELECT COUNT(*) FROM messages WHERE session_id=?", (sid,)).fetchone()[0]
        print("  删除会话 %s：消息 before=%d after=%d → %s"
              % (sid, before, after,
                 "级联生效" if after == 0 else "★ 级联未触发·孤儿行留存"))
        try:
            cur.execute("INSERT INTO messages (id, session_id, role, content, model,"
                        " created_at, tool_calls) VALUES"
                        " ('ghost-1','no-such-session','user','x',NULL,"
                        "'2026-01-01T00:00:00.000Z',NULL)")
            print("  写入悬空消息（父会话不存在）→ ★ 成功·外键未生效")
        except sqlite3.IntegrityError as exc:
            print("  写入悬空消息 → 被拒：%s" % exc)

        hr("F-02 clearAllData 不清 feedback → 悬空反馈行")
        # 先播下可判定的种子（原库 feedback 为空行·不播种则本项测不出任何东西）
        cur.execute("INSERT INTO sessions (id,title,model,created_at,updated_at) VALUES"
                    " ('fx-s1','种子会话','m','2026-01-01T00:00:00.000Z','2026-01-01T00:00:00.000Z')")
        cur.execute("INSERT INTO messages (id,session_id,role,content,model,created_at,tool_calls)"
                    " VALUES ('fx-m1','fx-s1','user','seed',NULL,'2026-01-01T00:00:00.000Z',NULL)")
        cur.execute("INSERT INTO feedback (id,session_id,message_id,verdict,comment,created_at)"
                    " VALUES ('fx-f1','fx-s1','fx-m1','up','','2026-01-01T00:00:00.000Z')")
        seed_fb = cur.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
        print("  播种后 feedback 行数 = %d（seed fx-f1 → 消息 fx-m1）" % seed_fb)
        # 等价于 db.ts clearAllData()：只删 messages 与 sessions，不动 feedback
        cur.execute("DELETE FROM messages")
        cur.execute("DELETE FROM sessions")
        for t in ("sessions", "messages", "feedback"):
            print("  %-10s 余 %d 行" % (t, cur.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]))
        orphan = cur.execute(
            "SELECT COUNT(*) FROM feedback f LEFT JOIN messages m"
            " ON f.message_id=m.id WHERE m.id IS NULL").fetchone()[0]
        print("  feedback 悬空行 = %d → %s"
              % (orphan, "★ 清库后 feedback 全部悬空（父消息已删）" if orphan else "无悬空"))

        hr("F-03 feedback 唯一索引维度错 → 同一消息可同时 up + down")
        cur.execute("INSERT INTO sessions (id,title,model,created_at,updated_at)"
                    " VALUES ('s1','t','m','2026-01-01T00:00:00.000Z','2026-01-01T00:00:00.000Z')")
        cur.execute("INSERT INTO messages (id,session_id,role,content,model,created_at,tool_calls)"
                    " VALUES ('m1','s1','user','hello',NULL,'2026-01-01T00:00:00.000Z',NULL)")
        cur.execute("INSERT OR IGNORE INTO feedback (id,session_id,message_id,verdict,comment,created_at)"
                    " VALUES ('f1','s1','m1','up','','2026-01-01T00:00:00.000Z')")
        cur.execute("INSERT OR IGNORE INTO feedback (id,session_id,message_id,verdict,comment,created_at)"
                    " VALUES ('f2','s1','m1','down','','2026-01-01T00:00:00.000Z')")
        rows = cur.execute("SELECT id, verdict FROM feedback WHERE message_id='m1'").fetchall()
        print("  同一 message_id 的反馈行 = %s" % rows)
        print("  → %s" % ("★ up 与 down 并存·语义矛盾状态可达" if len(rows) > 1 else "单一 verdict 生效"))

        hr("F-04 客户端可控主键 + 孤儿行 → 旧会话历史泄漏进新会话")
        cur.executescript("""
        CREATE TABLE s2 (id TEXT PRIMARY KEY, title TEXT, model TEXT,
                         created_at TEXT, updated_at TEXT);
        CREATE TABLE m2 (id TEXT PRIMARY KEY, session_id TEXT NOT NULL, role TEXT,
                         content TEXT, model TEXT, created_at TEXT, tool_calls TEXT,
                         FOREIGN KEY (session_id) REFERENCES s2(id) ON DELETE CASCADE);
        """)
        cur.execute("INSERT INTO s2 VALUES ('client-chosen-id','old','m',"
                    "'2026-01-01T00:00:00.000Z','2026-01-01T00:00:00.000Z')")
        cur.execute("INSERT INTO m2 VALUES ('old-msg','client-chosen-id','user',"
                    "'SECRET OLD CONTENT',NULL,'2026-01-01T00:00:00.000Z',NULL)")
        cur.execute("DELETE FROM s2 WHERE id='client-chosen-id'")
        print("  删会话后残留孤儿消息 = %d"
              % cur.execute("SELECT COUNT(*) FROM m2 WHERE session_id='client-chosen-id'").fetchone()[0])
        cur.execute("INSERT INTO s2 VALUES ('client-chosen-id','new','m',"
                    "'2026-02-01T00:00:00.000Z','2026-02-01T00:00:00.000Z')")
        bleed = cur.execute("SELECT id, content FROM m2 WHERE session_id='client-chosen-id'").fetchall()
        for row in bleed:
            print("  重建同 id 后 getMessagesBySession 返回：%s" % (row,))
        print("  → %s" % ("★ 旧正文泄漏进新会话" if bleed else "无泄漏"))

        hr("F-05 created_at 格式漂移 → 30 天窗口静默漏行")
        boundary = "2026-09-20T18:00:00.000Z"
        cur.execute("DELETE FROM feedback")
        samples = [
            ("iso_newer", "2026-09-20T19:00:00.000Z", True),
            ("space_newer", "2026-09-20 19:00:00", True),
            ("space_exact", "2026-09-20 18:00:00", True),
            ("slash_form", "2026/09/20 19:00:00", True),
        ]
        for i, (name, ts, _fresh) in enumerate(samples, 1):
            cur.execute("INSERT INTO feedback (id,session_id,message_id,verdict,comment,created_at)"
                        " VALUES (?,'s',?,'up','',?)", (name, "mm%d" % i, ts))
        visible = {r[0] for r in cur.execute(
            "SELECT id FROM feedback WHERE created_at >= ?", (boundary,))}
        print("  窗口边界 = %s" % boundary)
        for name, ts, fresh in samples:
            ok = name in visible
            flag = "INCLUDED" if ok else ("★ EXCLUDED（误排除·实际%s）" % ("更新" if fresh else "等于边界"))
            print("    %-12s %-26s → %s" % (name, ts, flag))
        print("  → 空格(0x20) < 'T'(0x54) ⇒ 同一时刻的非 ISO 写法排在窗口边界之前")

        hr("F-06 CREATE TABLE IF NOT EXISTS 对已有库永不生效")
        cur.execute("CREATE TABLE t_ddl (id TEXT PRIMARY KEY, a TEXT)")
        cur.execute("INSERT INTO t_ddl VALUES ('x','y')")
        cur.execute("CREATE TABLE IF NOT EXISTS t_ddl (id TEXT PRIMARY KEY, a TEXT NOT NULL"
                    " DEFAULT 'z', extra TEXT)")
        cols = [c[1] for c in cur.execute("PRAGMA table_info(t_ddl)")]
        print("  重跑改过定义的 CREATE TABLE 后列 = %s" % cols)
        print("  → %s" % ("★ 定义未套用到已有表（改表定义对旧库零效果）"
                          if "extra" not in cols else "定义已套用"))
    finally:
        con.close()
        drop_copy(copy_path)


# ---------------------------------------------------------------- bench
def cmd_bench(db_path):
    copy_path = make_copy(db_path)
    con = sqlite3.connect(copy_path)
    cur = con.cursor()
    try:
        hr("B-01 会话列表 N+1 vs GROUP BY（现役数据实跑）")
        sessions = [r[0] for r in cur.execute("SELECT id FROM sessions").fetchall()]
        t0 = time.perf_counter()
        rows = 0
        for sid in sessions:
            rows += len(cur.execute(
                "SELECT * FROM messages WHERE session_id=? ORDER BY created_at ASC", (sid,)).fetchall())
        n1 = time.perf_counter() - t0
        t0 = time.perf_counter()
        cur.execute("SELECT session_id, COUNT(*) FROM messages GROUP BY session_id").fetchall()
        grp = time.perf_counter() - t0
        print("  会话数 = %d" % len(sessions))
        print("  N+1 路径   : %.2f ms·%d 次查询·物化 %d 行消息" % (n1 * 1000, len(sessions) + 1, rows))
        print("  GROUP BY   : %.2f ms·1 次查询" % (grp * 1000))

        hr("B-02 会话列表代价模型（合成 5 万会话）")
        cur.execute("CREATE TABLE big_s (id TEXT PRIMARY KEY, title TEXT, model TEXT,"
                    " created_at TEXT, updated_at TEXT)")
        base = datetime.datetime(2026, 1, 1)
        for i in range(50000):
            ts = (base + datetime.timedelta(seconds=i)).isoformat() + "Z"
            cur.execute("INSERT INTO big_s VALUES (?,?,?,?,?)", ("i%d" % i, "t", "m", ts, ts))
        con.commit()

        def bench(label, sql, n=20, expect_rows=None):
            """计时辅助：**秒→毫秒必须显式 ×1000**（首版漏乘导致 1000× 低估），
            且**每次计时都打印实返行数**——行数与预期不符即说明测的不是目标数据集，
            数字作废（防「单位错/口径错」型假数）。"""
            t0 = time.perf_counter()
            rows = 0
            for _ in range(n):
                rows = len(cur.execute(sql).fetchall())
            dt = (time.perf_counter() - t0) / n
            print("  %-52s %9.2f ms·返回 %d 行" % (label, dt * 1000, rows))
            if expect_rows is not None and rows != expect_rows:
                print("     ★ 行数与预期不符（预期 %d）——该行数字作废" % expect_rows)
            return dt * 1000

        bench("无索引·全量 ORDER BY updated_at DESC", "SELECT * FROM big_s ORDER BY updated_at DESC",
              expect_rows=50000)
        bench("无索引·LIMIT 50", "SELECT * FROM big_s ORDER BY updated_at DESC LIMIT 50",
              expect_rows=50)
        cur.execute("CREATE INDEX ix ON big_s(updated_at DESC)")
        bench("有索引·全量 ORDER BY updated_at DESC", "SELECT * FROM big_s ORDER BY updated_at DESC",
              expect_rows=50000)
        bench("有索引·LIMIT 50", "SELECT * FROM big_s ORDER BY updated_at DESC LIMIT 50",
              expect_rows=50)
        bench("有索引·keyset（WHERE updated_at<? · LIMIT 50）",
              "SELECT * FROM big_s WHERE updated_at < '2026-06-01T00:00:00Z'"
              " ORDER BY updated_at DESC LIMIT 50", expect_rows=50)
        print("  EXPLAIN QUERY PLAN（有索引）：")
        for row in cur.execute("EXPLAIN QUERY PLAN SELECT * FROM big_s"
                               " ORDER BY updated_at DESC LIMIT 50"):
            print("     %s" % row[3])

        hr("B-03 messages 复合索引消除临时排序")
        cur.execute("CREATE TABLE big_m (id TEXT PRIMARY KEY, session_id TEXT, created_at TEXT)")
        cur.execute("CREATE INDEX ix1 ON big_m(session_id)")
        print("  单列索引 (session_id)：")
        for row in cur.execute("EXPLAIN QUERY PLAN SELECT * FROM big_m"
                               " WHERE session_id='x' ORDER BY created_at ASC"):
            print("     %s" % row[3])
        cur.execute("CREATE INDEX ix2 ON big_m(session_id, created_at)")
        print("  复合索引 (session_id, created_at)：")
        for row in cur.execute("EXPLAIN QUERY PLAN SELECT * FROM big_m"
                               " WHERE session_id='x' ORDER BY created_at ASC"):
            print("     %s" % row[3])

        hr("B-04 会话列表 N+1 的规模化代价（合成 2000 会话 × 5 消息 × 2KB blob）")
        cur.execute("CREATE TABLE n1_s (id TEXT PRIMARY KEY, title TEXT, model TEXT,"
                    " created_at TEXT, updated_at TEXT)")
        cur.execute("CREATE TABLE n1_m (id TEXT PRIMARY KEY, session_id TEXT, role TEXT,"
                    " content TEXT, model TEXT, created_at TEXT, tool_calls TEXT)")
        cur.execute("CREATE INDEX n1_m_sid ON n1_m(session_id)")
        blob = 'x' * 2000
        ts = '2026-01-01T00:00:00.000Z'
        for i in range(2000):
            cur.execute("INSERT INTO n1_s VALUES (?,?,?,?,?)", ("s%d" % i, 't', 'm', ts, ts))
            for j in range(5):
                cur.execute("INSERT INTO n1_m VALUES (?,?,?,?,?,?,?)",
                            ("m%d_%d" % (i, j), "s%d" % i, 'assistant', blob, 'm', ts, blob))
        con.commit()

        def timed(fn):
            t0 = time.perf_counter()
            n = fn()
            return (time.perf_counter() - t0) * 1000, n

        def n1_path():
            total = 0
            for (sid,) in cur.execute("SELECT id FROM n1_s").fetchall():
                total += len(cur.execute(
                    "SELECT * FROM n1_m WHERE session_id=? ORDER BY created_at ASC", (sid,)).fetchall())
            return total

        def grp_path():
            return len(cur.execute("SELECT session_id, COUNT(*) FROM n1_m GROUP BY session_id").fetchall())

        ms_n1, rows_n1 = timed(n1_path)
        ms_grp, rows_grp = timed(grp_path)
        print("  N+1 路径   : %.1f ms·%d 次查询·物化 %d 行消息"
              % (ms_n1, 2000 + 1, rows_n1))
        print("  GROUP BY   : %.1f ms·1 次查询·返回 %d 行" % (ms_grp, rows_grp))
        print("  倍数       : %.0f×" % (ms_n1 / ms_grp if ms_grp else 0))
    finally:
        con.close()
        drop_copy(copy_path)


# ---------------------------------------------------------------- hygiene
def cmd_hygiene(db_path):
    con = open_ro(db_path)
    cur = con.cursor()
    hr("H-01 时间戳格式合规性（严格 ISO-8601 Z）")
    import re
    pat = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")
    for table, col in (("sessions", "created_at"), ("sessions", "updated_at"),
                       ("messages", "created_at"), ("feedback", "created_at")):
        vals = [r[0] for r in cur.execute("SELECT %s FROM %s" % (col, table))]
        bad = [v for v in vals if not pat.match(v or "")]
        print("  %-10s %-11s 共 %d 行·不合规 %d 行 %s"
              % (table, col, len(vals), len(bad), bad[:3] if bad else ""))

    hr("H-02 tool_calls JSON 合法性")
    total = 0
    bad = 0
    for (tc,) in cur.execute("SELECT tool_calls FROM messages WHERE tool_calls IS NOT NULL"):
        total += 1
        try:
            parsed = json.loads(tc)
            if not isinstance(parsed, list):
                bad += 1
        except (ValueError, TypeError):
            bad += 1
    print("  非空 tool_calls 行 = %d·非法/非数组 = %d" % (total, bad))

    hr("H-03 会话内 created_at 并列（并列则排序不确定）")
    ties = cur.execute(
        "SELECT COUNT(*) FROM (SELECT session_id, created_at FROM messages"
        " GROUP BY session_id, created_at HAVING COUNT(*)>1)").fetchone()[0]
    print("  存在并列时间戳的会话 = %d（0 = 排序稳定）" % ties)

    hr("H-04 悬空行与索引覆盖")
    for label, sql in [
        ("messages 无父会话", "SELECT COUNT(*) FROM messages m LEFT JOIN sessions s"
                              " ON m.session_id=s.id WHERE s.id IS NULL"),
        ("feedback 无父消息", "SELECT COUNT(*) FROM feedback f LEFT JOIN messages m"
                               " ON f.message_id=m.id WHERE m.id IS NULL"),
        ("feedback 无父会话", "SELECT COUNT(*) FROM feedback f LEFT JOIN sessions s"
                               " ON f.session_id=s.id WHERE s.id IS NULL"),
    ]:
        print("  %-20s = %d" % (label, cur.execute(sql).fetchone()[0]))
    n = cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index'"
                     " AND tbl_name='feedback' AND sql LIKE '%session_id%'").fetchone()[0]
    print("  feedback 上含 session_id 的索引数 = %d" % n)
    con.close()


def main():
    ap = argparse.ArgumentParser(description="agent-web SQLite 表设计审查取证（W823）")
    ap.add_argument("mode", choices=["schema", "faults", "bench", "hygiene", "all"])
    ap.add_argument("--db", default=DEFAULT_DB, help="库路径（默认现役 chat.db）")
    args = ap.parse_args()
    db_path = resolve_db(args.db)
    if not os.path.exists(db_path):
        print("FAIL 库不存在：%s" % db_path)
        return 2
    try:
        if args.mode in ("schema", "all"):
            cmd_schema(db_path)
        if args.mode in ("hygiene", "all"):
            cmd_hygiene(db_path)
        if args.mode in ("faults", "all"):
            cmd_faults(db_path)
        if args.mode in ("bench", "all"):
            cmd_bench(db_path)
    except (sqlite3.Error, OSError) as exc:
        print("FAIL 取证中断：%s" % exc)
        return 2
    print("\nDONE —— 全部子命令执行完毕（原库只读·写入类取证均在副本上进行）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
