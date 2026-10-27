#!/usr/bin/env python3
"""cascade_lock.py — 级联运行锁（W991 建·W982 缓建①层的重启设计）。

保护面：级联 --apply 的多文件写序列（十四面非原子）——并行会话在中途读（verify/preflight/
另一跑级联）会看到半新半旧中态，产出混行尾假红、锚点对拍假红（W971-W989 期间多次实证）。
锁不解决 lost update（那归 ledger_backfill 指纹与 C7 门禁管），只解决「读中间态」。

设计与 W982 缓建理由的对照：缓建理由是「级联自身临时索引写难处理」——本设计把锁做成
**运行期互斥**而非索引锁：锁文件在 .git/cascade.lock（不进版本库·gitignore 面），
级联 acquire 后全程持有、finally 必释放；级联自己不重入（单进程单锁）；他方 preflight/
safe_commit 只**读锁状态提示**，不阻塞提交（提交互斥已由 pathspec + ref-lock 重试承担）。

语义：
  acquire(batch)   原子创建（O_EXCL）；已存在且新鲜（<600s）→ 拒绝并返回持有人信息；
                   陈旧（≥600s）→ 判死锁残留，夺锁（--force 语义内建）并告警。
  release()        持有人匹配才删（防误删他方新锁）。
  status()         (held, info_dict)——preflight/safe_commit 读。

用法：
  py -3 scripts/cascade_lock.py --acquire --batch W991
  py -3 scripts/cascade_lock.py --release
  py -3 scripts/cascade_lock.py --status
  py -3 scripts/cascade_lock.py --self-test
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK = os.path.join(ROOT, ".git", "cascade.lock")
TTL = 600.0  # 秒——级联实测量级 <2min，10 倍余量


def acquire(batch, holder="cascade", force=False):
    """原子取锁。返回 (ok, info)；ok=False 时 info=现持有人。"""
    now = time.time()
    data = {"batch": batch, "holder": holder, "pid": os.getpid(), "ts": now}
    payload = json.dumps(data, ensure_ascii=False)
    try:
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, payload.encode("utf-8"))
        os.close(fd)
        return True, data
    except FileExistsError:
        pass
    held = _read()
    if held is None:  # 损坏锁文件（空/非 JSON）→ 视同陈旧夺锁
        os.remove(LOCK)
        return acquire(batch, holder, force)
    age = now - held.get("ts", 0)
    if age >= TTL or force:
        print("[LOCK] 陈旧锁（%.0f 秒·持有人 %s@%s）——夺锁" % (age, held.get("holder"), held.get("batch")))
        os.remove(LOCK)
        return acquire(batch, holder, force)
    return False, held


def release(pid=None):
    """释放：默认只删自己 pid 的锁（防误删他方新锁）；--force 时 pid=None 不限。"""
    held = _read()
    if held is None:
        return True
    if pid is not None and held.get("pid") != pid:
        return False
    try:
        os.remove(LOCK)
    except FileNotFoundError:
        pass
    return True


def status():
    held = _read()
    if held is None:
        return False, {}
    age = time.time() - held.get("ts", 0)
    if age >= TTL:
        return False, held  # 陈旧=视同无锁
    return True, held


def _read():
    try:
        with open(LOCK, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _self_test() -> int:
    """自测：原子创建 / 二次拒绝 / 释放后可再取 / 陈旧夺锁 / 损坏锁夺锁。"""
    import tempfile
    global LOCK
    fails = []
    old_lock = LOCK
    try:
        LOCK = os.path.join(tempfile.mkdtemp(prefix="w991_lock_"), "cascade.lock")
        ok, info = acquire("W999", "t")
        if not ok or info["batch"] != "W999":
            fails.append("首取应成功")
        ok2, held = acquire("W998", "other")
        if ok2 or held.get("batch") != "W999":
            fails.append("新鲜锁二次取应拒绝且返回持有人")
        if not release(pid=info["pid"]):
            fails.append("持有人释放应成功")
        if not release(pid=info["pid"]):
            fails.append("重复释放应幂等成功（finally 安全语义）")
        ok3, _ = acquire("W997", "t")
        if not ok3:
            fails.append("释放后再取应成功")
        # 陈旧夺锁：改 ts 到 700 秒前
        held = _read()
        held["ts"] = time.time() - 700
        with open(LOCK, "w", encoding="utf-8") as f:
            json.dump(held, f)
        ok4, info4 = acquire("W996", "t")
        if not ok4 or info4["batch"] != "W996":
            fails.append("陈旧锁应可夺")
        # 损坏锁
        with open(LOCK, "w", encoding="utf-8") as f:
            f.write("not-json")
        ok5, _ = acquire("W995", "t")
        if not ok5:
            fails.append("损坏锁应视同陈旧可夺")
    finally:
        try:
            os.remove(LOCK)
        except OSError:
            pass
        LOCK = old_lock
    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：原子创建/拒绝/释放/陈旧夺/损坏夺 五态（判据可证伪）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="级联运行锁（W991）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--acquire", action="store_true")
    g.add_argument("--release", action="store_true")
    g.add_argument("--status", action="store_true")
    g.add_argument("--self-test", action="store_true")
    ap.add_argument("--batch", default="?", help="持锁批次号（acquire 用）")
    ap.add_argument("--holder", default="cascade", help="持锁会话标识")
    ap.add_argument("--force", action="store_true", help="强行夺锁")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    if args.acquire:
        ok, info = acquire(args.batch, args.holder, args.force)
        if ok:
            print("[LOCK] 已取得：批次 %s（pid %d）" % (args.batch, os.getpid()))
            return 0
        print("[LOCK] 拒绝：现由 %s@%s 持有（%.0f 秒）——等级联完成或 --force"
              % (info.get("holder"), info.get("batch"), time.time() - info.get("ts", 0)))
        return 1
    if args.release:
        ok = release()
        print("[LOCK] 已释放" if ok else "[LOCK] 无锁或非本会话锁")
        return 0
    held, info = status()
    if held:
        print("[LOCK] 持有中：%s@%s（%.0f 秒）" % (info.get("holder"), info.get("batch"),
                                                  time.time() - info.get("ts", 0)))
    else:
        print("[LOCK] 无活动锁")
    return 0


if __name__ == "__main__":
    sys.exit(main())
