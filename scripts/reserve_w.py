#!/usr/bin/env python3
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
import hashlib
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
# W1121：预约表的**共享面**此前只覆盖「本工作树」（tmpe/ 随仓不随 git）⇒
# 跨 worktree / 跨克隆并行时互相不可见 ⇒ 实测双方各占 W1120（2026-11-04·同机两克隆）。
# ⇒ 取号集合改为「所有可达预约表」的并集：① 本仓 tmpe/ ② 同机兄弟克隆的 tmpe/
# ③ 用户级共享表（跨克隆主共享面）；写入同时落 ① 与 ③（① 留给既有读取方）。
SHARED_RES_FILE = os.path.join(os.path.expanduser("~"), ".mavis", "xiyouji_w_reservations.json")
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


def _read_one(path):
    """读单个预约表；文件缺失/损坏/非 dict 一律视空（不阻断取号）。"""
    try:
        data = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def sibling_repo_roots():
    """同机兄弟克隆目录（仓名前缀相同 **且** 内含 scripts/reserve_w.py ⇒ 才认）。"""
    out = []
    parent = os.path.dirname(ROOT)
    prefix = os.path.basename(ROOT)
    try:
        names = sorted(os.listdir(parent))
    except OSError:
        return out
    for name in names:
        if not name.startswith(prefix):
            continue
        cand = os.path.join(parent, name)
        if cand == ROOT or not os.path.isdir(cand):
            continue
        if os.path.isfile(os.path.join(cand, "scripts", "reserve_w.py")):
            out.append(cand)
    return out


def res_paths():
    """所有可达预约表路径（去重·顺序：本仓 → 兄弟克隆 → 用户级共享表）。"""
    paths = [RES_FILE]
    for root in sibling_repo_roots():
        paths.append(os.path.join(root, "tmpe", "_w_reservations.json"))
    paths.append(SHARED_RES_FILE)
    seen, uniq = set(), []
    for p in paths:
        key = os.path.normcase(os.path.abspath(p))
        if key not in seen:
            seen.add(key)
            uniq.append(p)
    return uniq


def merge_res(paths=None):
    """合并所有可达预约表（同号取 ts 最新者）⇒ 取号集合跨克隆完整（W1121）。"""
    merged = {}
    for p in (res_paths() if paths is None else paths):
        for w, info in _read_one(p).items():
            if not isinstance(info, dict):
                continue
            old = merged.get(w)
            if old is None or info.get("ts", 0) >= old.get("ts", 0):
                merged[w] = info
    return merged


def load_res():
    return merge_res()


def save_res(d):
    """写预约表：本仓表 + 用户级共享表；写共享表时先合并他人记录（不覆盖）。"""
    for target in (RES_FILE, SHARED_RES_FILE):
        merged = merge_res([target])
        merged.update(d)
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            tmp = target + ".tmp"
            json.dump(merged, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.replace(tmp, target)  # 同文件系统原子替换
        except OSError:
            continue


def active_res(paths=None):
    now = time.time()
    return {w: info for w, info in merge_res(paths).items()
            if now - info.get("ts", 0) <= TTL}


def conflict_res(paths=None):
    """同一号被**多个会话**预约 ⇒ 跨克隆撞号（返回 {号: [会话…]}）。"""
    owners = {}
    now = time.time()
    for p in (res_paths() if paths is None else paths):
        for w, info in _read_one(p).items():
            if not isinstance(info, dict) or now - info.get("ts", 0) > TTL:
                continue
            owners.setdefault(w, set()).add(info.get("session", "?"))
    return {w: sorted(s) for w, s in owners.items() if len(s) > 1}


def session_id():
    """会话标识：WB_SESSION 优先；否则 hostname+仓路径指纹 ⇒ 跨克隆可辨（W1121）。"""
    env = os.environ.get("WB_SESSION")
    if env:
        return env
    host = socket.gethostname() or "unknown"
    tag = hashlib.sha1(os.path.abspath(ROOT).encode("utf-8")).hexdigest()[:6]
    return "%s@%s-%s" % (host, os.path.basename(ROOT), tag)


def reserve():
    warn_unclaimed()
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


def unclaimed_in_ledger(ledger_text, reservations):
    """注入式判定：台账「在途（认领·未收官）」行中不被有效预约支撑的号集合。

    台账行形态：| W### | 描述 | hash | 级联 | 状态 | 会话 | touches |——状态列=split("|")[5]。
    """
    out = set()
    for ln in ledger_text.splitlines():
        m = re.match(r"^\|\s*W(\d{3,4})\s*\|", ln)
        if not m:
            continue
        cells = ln.split("|")
        status = cells[5].strip() if len(cells) > 5 else ""
        if "在途" not in status:
            continue
        w = "W%s" % m.group(1)
        if w not in reservations:
            out.add(w)
    return out


def warn_unclaimed():
    """reserve/list 时顺带检测：台账在途认领行无占号支撑 ⇒ WARN（提醒不阻断——
    铁律 17 逃避形态·W1050 撞号复盘的机器化教训：占号面与认领面是两套机制，必须对拍）。"""
    try:
        txt = open(LEDGER, encoding="utf-8").read()
    except OSError:
        txt = ""
    ghost = unclaimed_in_ledger(txt, active_res())
    for w in sorted(ghost):
        print("WARN  台账 %s 在途认领行无占号支撑（未跑 reserve_w 先登记＝绕过铁律 17）——"
              "请补占号或改状态列" % w)
    for w, sessions in sorted(conflict_res().items()):
        print("WARN  跨克隆撞号预警：%s 被多个会话预约（%s）——按「先落地者保留」仲裁"
              % (w, " / ".join(sessions)))


def list_res():
    warn_unclaimed()
    res = active_res()
    if not res:
        print("（无有效预约）")
        return
    for w in sorted(res, key=lambda x: int(x.lstrip("W"))):
        info = res[w]
        print("%s  session=%s  ts=%s" % (w, info.get("session"),
                                         time.ctime(info.get("ts", 0))))


def release(w):
    """只释放**本工作树**登记的号——绝不误删其它克隆/会话的预约（W1121）。"""
    res = _read_one(RES_FILE)
    info = res.pop(w, None)
    if info is None:
        print("%s 不在本工作树预约表中（若为其它克隆所占·勿释放）" % w)
        return
    shared = _read_one(SHARED_RES_FILE)
    if shared.get(w, {}).get("session") == info.get("session"):
        shared.pop(w, None)
        try:
            os.makedirs(os.path.dirname(SHARED_RES_FILE), exist_ok=True)
            tmp = SHARED_RES_FILE + ".tmp"
            json.dump(shared, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.replace(tmp, SHARED_RES_FILE)
        except OSError:
            pass
    save_res(res)
    print("已释放 %s" % w)


def self_test():
    """三例：无支撑在途行必中 / 已占号在途行放行 / 已收官行放行。"""
    led = (
        "| W901 | 甲批 | h1 | — | **已收官**（h1） | s | t |\n"
        "| W902 | 乙批 | — | — | 在途（认领·未收官） | s | t |\n"
        "| W903 | 丙批 | — | — | 在途（认领·未收官） | s | t |\n"
    )
    res = {"W903": {"session": "x", "ts": time.time(), "status": "reserved"}}
    ghost = unclaimed_in_ledger(led, res)
    ok1 = ghost == {"W902"}
    print("%s  T1 在途无占号支撑必中（G-07）" % ("PASS" if ok1 else "FAIL"))
    ok2 = not unclaimed_in_ledger(led, {"W902": {}, "W903": {}})
    print("%s  T2 已占号在途行放行（G-07）" % ("PASS" if ok2 else "FAIL"))
    ok3 = "W901" not in unclaimed_in_ledger(led, {})
    print("%s  T3 已收官行放行（G-07）" % ("PASS" if ok3 else "FAIL"))
    return 0 if (ok1 and ok2 and ok3) else 1


def main():
    if "--self-test" in sys.argv:
        return self_test()
    mode = sys.argv[1] if len(sys.argv) > 1 else "reserve"
    if mode == "list":
        list_res()
    elif mode == "release":
        if len(sys.argv) < 3:
            print("用法: reserve_w.py release <W号>")
            sys.exit(2)
        release(sys.argv[2])
    elif mode == "reserve":
        reserve()
    else:
        print("未知模式: %s（可用 reserve / list / release）" % mode)
        sys.exit(2)


if __name__ == "__main__":
    main()
