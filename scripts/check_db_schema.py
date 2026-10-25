#!/usr/bin/env python3
"""check_db_schema.py — DB schema 门禁（W917 建置·B-DB-05 清偿）。

背景（W823 审查四 P0 长期无回归防线）：agent-web SQLite 层的四项正确性不变量
此前靠人工维持，W917 修复后本门禁静态锁定（宁窄勿误·只断言不变量形态）：

  P1 外键强制在位：db.ts 含 pragma('foreign_keys = ON')（DDL 声明 FOREIGN KEY 而不开启 = 从未生效）
  P2 clearAllData 三表全清：函数体含 feedback/messages/sessions 三条 DELETE
  P3 反馈唯一索引单维：UNIQUE INDEX ... ON feedback(message_id)（无 verdict 第二维）
  P4 会话主键服务端生成：chat.ts 无「id: sessionId ||」形态（客户端可控主键 = 串档路径）

fail-closed：目标文件缺失/读取失败按 FAIL。agent-web 侧行为正确性由其自有
npm 测试链覆盖，本门禁锁「不变量不被回退删除」。

用法：
    python scripts/check_db_schema.py --gate
    python scripts/check_db_schema.py --self-test
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_TS = ROOT / "xiyouji-agent-web" / "server" / "db.ts"
CHAT_TS = ROOT / "xiyouji-agent-web" / "server" / "chat.ts"


def check(verbose: bool = True) -> int:
    fails: list[str] = []
    try:
        db = DB_TS.read_text(encoding="utf-8")
        chat = CHAT_TS.read_text(encoding="utf-8")
    except OSError as e:
        print("FAIL  P1: 目标文件读取失败（fail-closed）：%s" % e)
        return 1
    if "foreign_keys = ON" not in db:
        fails.append("P1: db.ts 缺 pragma foreign_keys = ON（外键声明不开启=级联从未生效）")
    m = re.search(r"function clearAllData\(\)[^}]*}", db, re.S)
    if not m or not all(("DELETE FROM %s" % t) in m.group(0) for t in ("feedback", "messages", "sessions")):
        fails.append("P2: clearAllData 未覆盖 feedback/messages/sessions 三表")
    if not re.search(r"UNIQUE INDEX[^;]*ON feedback\(message_id\)", db) or re.search(
            r"UNIQUE INDEX[^;]*ON feedback\(message_id,\s*verdict\)", db):
        fails.append("P3: 反馈唯一索引非 (message_id) 单维（矛盾并存回退）")
    if re.search(r"id:\s*sessionId\s*\|\|", chat):
        fails.append("P4: chat.ts 会话主键含客户端可控形态（串档路径回退）")
    if verbose:
        for f in fails:
            print("FAIL ", f)
        print("---- DB schema 门禁：%d FAIL ----" % len(fails))
    return 1 if fails else 0


def self_test() -> int:
    import tempfile
    cases = []
    with tempfile.TemporaryDirectory() as td:
        global DB_TS, CHAT_TS
        old_db, old_chat = DB_TS, CHAT_TS
        try:
            DB_TS = Path(td) / "db.ts"
            CHAT_TS = Path(td) / "chat.ts"
            good_db = ("pragma('journal_mode = WAL');\npragma('foreign_keys = ON');\n"
                       "CREATE UNIQUE INDEX IF NOT EXISTS idx_feedback_message ON feedback(message_id);\n"
                       "function clearAllData() { db.exec('DELETE FROM feedback');"
                       "db.exec('DELETE FROM messages');db.exec('DELETE FROM sessions'); }")
            DB_TS.write_text(good_db, encoding="utf-8")
            CHAT_TS.write_text("id: uuidv4(),", encoding="utf-8")
            cases.append(("T1 四不变量全绿", check(verbose=False) == 0))
            DB_TS.write_text(good_db.replace("foreign_keys = ON", "x = ON"), encoding="utf-8")
            cases.append(("T2 摘除外键 pragma 必红", check(verbose=False) == 1))
            DB_TS.write_text(good_db, encoding="utf-8")
            CHAT_TS.write_text("id: sessionId || uuidv4(),", encoding="utf-8")
            cases.append(("T3 客户端可控主键必红", check(verbose=False) == 1))
        finally:
            DB_TS, CHAT_TS = old_db, old_chat
    bad = [n for n, ok in cases if not ok]
    for n, ok in cases:
        print("%s  %s" % ("PASS" if ok else "FAIL", n))
    print("---- DB schema 门禁 self-test：%d/%d ----" % (len(cases) - len(bad), len(cases)))
    return 1 if bad else 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    return check()


if __name__ == "__main__":
    sys.exit(main())
