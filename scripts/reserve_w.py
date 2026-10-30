#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reserve_w.py — 批次号预约（防并行会话撞号·W1041 立）

问题：台账是「事后登记」，两个并行会话各自从自己看到的台账 max 取号，
同时动手必撞（2026-10-30 实战撞过 W1039）。本脚本提供「开批先占号」机制：

  - 同一工作树内多会话共享 tmpe/_w_reservations.json（已被 .gitignore，天然共享、
    不污染提交），先占先得。
  - 占号 = 写入一条 `{w, session, ts, status:"reserved"}`，立即可见。
  - candidate = max(台账 max W, CHANGELOG 顶段 W, 已预约集合) + 1，跳过被占号。
  - 预约 24h 过期（TTL）：会话 abandon 不提交也不会永久占号。
  - 写文件用「临时文件 + os.replace」保证同文件系统原子性，降低双会话竞态。

用法：
  python scripts/reserve_w.py            # 占一个号，stdout 仅打印 W 号
  python scripts/reserve_w.py list       # 列出当前有效预约
  python scripts/reserve_w.py release W1040   # 收官后释放（可选；TTL 也会自动过期）

铁律 17（AGENTS.md）要求：开批第一步必须跑 reserve，未占号不动手。
"""
import json
import os
import re
import socket
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md")
RES_DIR = os.path.join(ROOT, "tmpe")
RES_FILE = os.path.join(RES_DIR, "_w_reservations.json")
TTL = 24 * 3600  # 预约 24h 过期

W_RE = re.compile(r"W(\d{3,4})")


def _git(*a):
    r = subprocess.run(
        ["git", "-c", "core.quotePath=false", "-C", ROOT] + list(a),
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return r.stdout if r.returncode == 0 else ""


def ledger_max():
    try:
        txt = open(LEDGER, encoding="utf-8").read()
    except OSError:
        return 0
    return max((int(m) for m in W_RE.findall(txt)), default=0)


def changelog_max():
    mx = 0
    try:
        txt = open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8").read()
    except OSError:
        txt = ""
    m = re.search(r"^### W(\d{3,4})", txt, re.M)
    if m:
        mx = max(mx, int(m.group(1)))
    # HEAD 版本（防止工作树尚未写段时漏算已提交批次）
    head = _git("show", "HEAD:CHANGELOG.md")
    m = re.search(r"^### W(\d{3,4})", head, re.M)
    if m:
        mx = max(mx, int(m.group(1)))
    return mx


def load_res():
    try:
        return json.load(open(RES_FILE, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_res(d):
    os.makedirs(RES_DIR, exist_ok=True)
    tmp = RES_FILE + ".tmp"
    json.dump(d, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, RES_FILE)  # 同文件系统原子替换


def active_res():
    now = time.time()
    return {w: info for w, info in load_res().items()
            if now - info.get("ts", 0) <= TTL}


def session_id():
    return os.environ.get("WB_SESSION", socket.gethostname() or "unknown")


def reserve():
    base = max(ledger_max(), changelog_max())
    taken = set(int(w.lstrip("W")) for w in active_res())
    cand = base + 1
    while cand in taken:
        cand += 1
    res = load_res()
    res["W%d" % cand] = {"session": session_id(), "ts": time.time(),
                         "status": "reserved"}
    save_res(res)
    print("W%d" % cand)


def list_res():
    res = active_res()
    if not res:
        print("（无有效预约）")
        return
    for w in sorted(res, key=lambda x: int(x.lstrip("W"))):
        info = res[w]
        print("%s  session=%s  ts=%s" % (w, info.get("session"),
                                         time.ctime(info.get("ts", 0))))


def release(w):
    res = load_res()
    if res.pop(w, None) is not None:
        save_res(res)
        print("已释放 %s" % w)
    else:
        print("%s 不在预约表中" % w)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "reserve"
    if mode == "list":
        list_res()
    elif mode == "release":
        if len(sys.argv) < 3:
            print("用法: reserve_w.py release <W号>"); sys.exit(2)
        release(sys.argv[2])
    elif mode == "reserve":
        reserve()
    else:
        print("未知模式: %s（可用 reserve / list / release）" % mode)
        sys.exit(2)


if __name__ == "__main__":
    main()
