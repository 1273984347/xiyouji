#!/usr/bin/env python3
"""ledger_backfill.py — 台账登记行的**独占回填**工具（W931 共享面串行化机制·层 2 判据 B）

背景（病根）
------------
台账（`docs/00-导读/W批次编号对账表.md`）是多会话共享面，两类操作性质完全不同：

- **纯追加**（新增认领行）：行级独立，**可并发**（各自新增一行不覆盖彼此）；
- **回填**（改既有行的 hash / 状态 / touches 列）：**会 lost update** ——
  两方都按自己读到的旧行改，后写者静默覆盖先写者，而台账里看不出谁覆盖了谁。

本工具只管第二类：**回填前锁定目标行的内容指纹，回填后输出新指纹，提交前可复核**。

用法
----
  # 1) 回填：改 hash / 状态 / touches 三列（其余列逐字不动）
  py -3 scripts/ledger_backfill.py --w W931 --hash 57762fa3 --status "**已收官**（57762fa3·…）"

  # 2) 提交前复核：确认目标行自上一步起没被他人改动（指纹一致才 PASS）
  py -3 scripts/ledger_backfill.py --w W931 --verify <上一步输出的新指纹>

  # 3) 带基线断言的回填：--expect 给出你**读到**的旧指纹，不一致则拒绝改写
  py -3 scripts/ledger_backfill.py --w W931 --hash … --expect <读到的旧指纹>

  # 4) 追加认领行（纯追加·不改任何既有行）
  py -3 scripts/ledger_backfill.py --append-claim --w W931 --desc "…" --session "主会话 2026-10-25" --touches "a.py · b.md"

  # 5) 干跑 / 自测
  py -3 scripts/ledger_backfill.py --w W931 --hash x --dry-run
  py -3 scripts/ledger_backfill.py --self-test

退出码：0=成功；1=判红（指纹不符 / 行不存在 / 列定位失败 / 自测失败）。
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import tempfile

from preflight_check import wnum_commit_index  # W956/P-43-01：提交识别判据单源（复用 preflight 同一函数）

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER_REL = "docs/00-导读/W批次编号对账表.md"
LEDGER = os.path.join(ROOT, LEDGER_REL)

RE_W_ROW = re.compile(r"^\|\s*W(\d{3})\s*\|")
RE_STATUS_CELL = re.compile(r"^(?:已收官|已闭环|在途|进行中|未复核)")
PLACEHOLDER_HASH = "—（待回填）"

SYSTEM_GIT = r"C:\Program Files\Git\bin\git.exe"


def _git_bin():
    """与 preflight_check 同口径：Windows 优先系统 Git，其余回退 PATH。"""
    return SYSTEM_GIT if os.path.exists(SYSTEM_GIT) else "git"


def git_commit_index():
    """git log --all（%h %s）→ wnum_commit_index 索引；git 不可用抛 RuntimeError。"""
    git = _git_bin()
    r = subprocess.run([git, "log", "--all", "--format=%h %s"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=120)
    if r.returncode != 0:
        raise RuntimeError("git log 失败（rc=%s）：%s" % (r.returncode, (r.stderr or "").strip()[:120]))
    return wnum_commit_index(r.stdout.splitlines())


def compose_git_status(w, index):
    """P-43-01 后半：由提交索引合成收官状态文本（不再人工手写「已收官（hash…）」）。

    返回 None = 该 W 号在 git 无批次标签提交——**不能**反填收官状态（可能仍在途·判红不走此路）。
    """
    rec = index.get(w)
    if not rec:
        return None
    count, first = rec
    return "**已收官**（%s·git 反填·共 %d 笔·P-43-01）" % (first, count)


def fingerprint(text: str) -> str:
    """行指纹：sha256 前 12 位（对行首尾空白不敏感，对内容敏感）。"""
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:12]


def locate_cells(cells: list[str]) -> dict[str, int]:
    """从右起定位各列下标（摘要含裸竖线时前列右移，末列不动）。

    与 preflight_check.py 的列定位同策略：touches=末格、session=右起第 3、
    status=右起首个状态形态格（否则右起第 4）、hash=右起第 5、级联=右起第 6。
    """
    n = len(cells)
    if n < 9:
        raise ValueError("行格数不足 9（标准 7 格 + 首尾空）·实得 %d" % n)
    # 标准 7 格的列序（cells 含首尾两个空元素）：
    #   1=编号 2=描述 3=hash 4=级联hash 5=状态 6=认领会话 7=touches
    #   ⇒ touches=n-2 · session=n-3 · status=n-4 · cascade=n-5 · hash=n-6
    #   （hash 与级联两列的下标不可互换——W931 自测实测抓出过一次错位）
    loc = {"touches": n - 2, "session": n - 3, "status": n - 4,
           "cascade": n - 5, "hash": n - 6}
    for i in range(n - 2, 5, -1):
        norm = re.sub(r"[\s*]+", "", cells[i])
        if RE_STATUS_CELL.match(norm):
            loc["status"] = i
            break
    return loc


def read_ledger(path: str) -> list[str]:
    with open(path, encoding="utf-8", newline="") as f:
        return f.read().split("\n")


def write_ledger(path: str, lines: list[str]) -> None:
    """写回台账（W965 修：按文件主导行尾重建全部边界）。

    病根：`"\\n".join` 对 CRLF 文件的**新插入行**留下裸 LF 尾边界（原既有行的 \\r
    挂在行尾幸存、新行没有）——每次 append-claim 引入一个裸 LF，五次认领五处混行尾。
    现按主导行尾 rstrip 后统一重建：内容零变化、行尾全量归一。
    """
    joined = "\n".join(lines)
    nl = "\r\n" if joined.count("\r\n") * 20 >= joined.count("\n") else "\n"
    out = nl.join(ln.rstrip("\r\n") for ln in lines)
    if not out.endswith(nl):
        out += nl
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(out)


def find_row(lines: list[str], wnum: int) -> int:
    for i, ln in enumerate(lines):
        m = RE_W_ROW.match(ln)
        if m and int(m.group(1)) == wnum:
            return i
    return -1


def cmd_backfill(args, path: str) -> int:
    lines = read_ledger(path)
    idx = find_row(lines, args.w)
    if idx < 0:
        print("FAIL  台账中不存在 W%03d 行" % args.w)
        return 1
    line = lines[idx]
    old_fp = fingerprint(line)
    cells = line.split("|")
    try:
        loc = locate_cells(cells)
    except ValueError as exc:
        print("FAIL  列定位失败：%s" % exc)
        return 1

    if args.verify:
        if old_fp != args.verify:
            print("FAIL  指纹复核不符：期望 %s·实得 %s ⇒ 该行自回填后已被他人改动（W%03d）"
                  % (args.verify, old_fp, args.w))
            print("      处理：重读该行 → 确认他方改动内容 → 重新回填（勿覆盖）")
            return 1
        print("OK    指纹复核一致：W%03d = %s（可提交）" % (args.w, old_fp))
        return 0

    if args.expect and args.expect != old_fp:
        print("FAIL  基线指纹不符：--expect %s·实得 %s ⇒ 你读到的行已过期（他方已改）"
              % (args.expect, old_fp))
        print("      处理：重读该行 → 确认他方改动内容 → 再回填")
        return 1

    changes = []
    if args.from_git:
        # P-43-01 后半：状态/hash 由 git 反填（机器事实源·人工不再手写「已收官（hash…）」）。
        # 显式 --hash/--status 仍可覆盖（机器反填是默认值不是强制值）。
        # 注意：此处变量名用 cidx——cmd_backfill 的 idx 是行下标（W956 首版曾被 dict 遮蔽·
        # 干跑路径不落盘故未暴露，实跑在 lines[idx] 处 TypeError）
        cidx = git_commit_index()
        auto_status = compose_git_status(args.w, cidx)
        if auto_status is None:
            print("FAIL  W%03d 在 git 无批次标签提交（type(w###): 形态）——不能反填收官状态"
                  "（批次可能仍在途·先落库再回填）" % args.w)
            return 1
        if args.status is None:
            args.status = auto_status
            changes.append(("status", loc["status"], args.status))
        if args.hash is None:
            args.hash = cidx[args.w][1]
            changes.append(("hash", loc["hash"], args.hash))
    else:
        if args.hash is not None:
            changes.append(("hash", loc["hash"], args.hash))
        if args.cascade is not None:
            changes.append(("cascade", loc["cascade"], args.cascade))
        if args.status is not None:
            changes.append(("status", loc["status"], args.status))
    if args.touches is not None:
        changes.append(("touches", loc["touches"], args.touches))
    if not changes:
        print("FAIL  未指定任何要改的列（--hash/--cascade/--status/--touches/--from-git）")
        return 1

    new_cells = list(cells)
    for name, i, val in changes:
        old_val = new_cells[i].strip()
        new_cells[i] = " %s " % val.strip()
        print("  · %-8s : 「%s」→「%s」" % (name, old_val, val.strip()))
    new_line = "|".join(new_cells)
    new_fp = fingerprint(new_line)

    if args.dry_run:
        print("OK    干跑完成（未写盘）·旧指纹 %s → 新指纹 %s" % (old_fp, new_fp))
        return 0

    lines[idx] = new_line
    write_ledger(path, lines)
    print("OK    已回填 W%03d·旧指纹 %s → 新指纹 %s" % (args.w, old_fp, new_fp))
    print("      提交前请复核：py -3 scripts/ledger_backfill.py --w %03d --verify %s" % (args.w, new_fp))
    return 0


def cmd_append_claim(args, path: str) -> int:
    lines = read_ledger(path)
    if find_row(lines, args.w) >= 0:
        print("FAIL  台账已存在 W%03d 行（不可重复认领）" % args.w)
        return 1
    if not args.desc or not args.session:
        print("FAIL  --append-claim 需要 --desc 与 --session")
        return 1
    row = "| W%03d | %s | %s | %s | 在途（认领·未收官） | %s | %s |" % (
        args.w, args.desc.strip(), PLACEHOLDER_HASH, PLACEHOLDER_HASH,
        args.session.strip(), args.touches.strip() if args.touches else "—")
    # 插入到最后一个 W 行之后（表尾），不改任何既有行
    last = -1
    for i, ln in enumerate(lines):
        if RE_W_ROW.match(ln):
            last = i
    if last < 0:
        print("FAIL  台账中找不到任何 W 行（结构异常）")
        return 1
    lines.insert(last + 1, row)
    write_ledger(path, lines)
    print("OK    已追加 W%03d 认领行（纯追加·未改任何既有行）·新行指纹 %s" % (args.w, fingerprint(row)))
    print("      提交提示：若工作树同时有他方未提交的台账行，用 git update-index --cacheinfo 精确暂存本行，"
          "勿整文件 git add")
    return 0


def _self_test() -> int:
    """自测：正例必绿 + 负例必红（负例红不了 ⇒ 判据无效，不算通过）。"""
    fails = []
    tmpdir = tempfile.mkdtemp(prefix="w931_backfill_")
    sample = (
        "# 台账样本\n\n"
        "| W930 | 布局批 | —（待回填） | —（待回填） | 在途（认领·未收官） | 主会话 | a.py · b.md |\n"
        "| W929 | 素材批 | —（待回填） | —（待回填） | 在途（认领·未收官） | 主会话 | c.py |\n"
    )
    path = os.path.join(tmpdir, "ledger.md")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(sample)

    # 正例 1：回填 hash + 状态 → 成功、指纹变化
    rc = cmd_backfill(argparse.Namespace(w=930, hash="abc1234", cascade=None,
                                        status="**已收官**（abc1234·全绿）", touches=None,
                                        expect=None, verify=None, dry_run=True, from_git=False),
                      path)
    if rc != 0:
        fails.append("正例1 回填干跑应成功")
    # 正例 2：回填后 --verify 新指纹 → 通过
    lines = read_ledger(path)
    idx = find_row(lines, 930)
    new_fp = fingerprint(lines[idx])
    rc = cmd_backfill(argparse.Namespace(w=930, hash=None, cascade=None, status=None,
                                        touches=None, expect=None, verify=new_fp, dry_run=False,
                                        from_git=False),
                      path)
    if rc != 0:
        fails.append("正例2 指纹复核应通过")
    # 负例 1：--verify 旧指纹（行已变）→ 必须红
    rc = cmd_backfill(argparse.Namespace(w=930, hash=None, cascade=None, status=None,
                                        touches=None, expect=None, verify="deadbeef0000", dry_run=False,
                                        from_git=False),
                      path)
    if rc == 0:
        fails.append("负例1 陈旧指纹必须判红")
    # 负例 2：--expect 基线不符 → 必须红
    rc = cmd_backfill(argparse.Namespace(w=930, hash="zzz", cascade=None, status=None,
                                        touches=None, expect="deadbeef0000", verify=None, dry_run=False,
                                        from_git=False),
                      path)
    if rc == 0:
        fails.append("负例2 基线指纹不符必须判红")
    # 负例 3：不存在的 W 号 → 必须红
    rc = cmd_backfill(argparse.Namespace(w=777, hash="zzz", cascade=None, status=None,
                                        touches=None, expect=None, verify=None, dry_run=False,
                                        from_git=False),
                      path)
    if rc == 0:
        fails.append("负例3 行不存在必须判红")
    # W956/P-43-01：compose_git_status 纯函数（正例绿 + 无提交负例 None）
    _idx = wnum_commit_index(["d093bf64 docs(w955): GSAP 计划子批", "e5b262e7 docs(w884): 审计落盘",
                             "92175003 chore(w884): 收官回填"])
    if compose_git_status(884, _idx) != "**已收官**（e5b262e7·git 反填·共 2 笔·P-43-01）":
        fails.append("compose_git_status 正例应合成 2 笔收官文本")
    if compose_git_status(777, _idx) is not None:
        fails.append("compose_git_status 无提交号必须返回 None（不可反填）")
    if wnum_commit_index(["chore: 提及 W940 教训但不带批次标签"]):
        fails.append("散文提及 W 号（无 type(w###): 标签）不得计入提交索引")
    # 正例 3：追加认领行（纯追加）
    rc = cmd_append_claim(argparse.Namespace(w=931, desc="机制批", session="主会话", touches="x.py"),
                           path)
    if rc != 0:
        fails.append("正例3 追加认领行应成功")
    # 负例 4：重复认领同号 → 必须红
    rc = cmd_append_claim(argparse.Namespace(w=931, desc="重复", session="主会话", touches="x.py"),
                           path)
    if rc == 0:
        fails.append("负例4 重复认领必须判红")

    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：3 正例绿 + 4 负例红 + git 反填纯函数 3 例（判据可证伪）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="台账登记行独占回填工具（W931 判据 B）")
    ap.add_argument("--w", type=int, default=0, help="W 号（如 931）")
    ap.add_argument("--hash", default=None, help="回填：提交 hash 列")
    ap.add_argument("--cascade", default=None, help="回填：级联 hash 列")
    ap.add_argument("--status", default=None, help="回填：状态列（须以「已收官/已闭环」开头才算收官）")
    ap.add_argument("--from-git", action="store_true",
                    help="P-43-01：状态/hash 由 git 反填（读该 W 号的 type(w###): 批次标签提交·"
                         "自动生成「已收官（首笔hash·git 反填·共 N 笔）」）；显式 --hash/--status 可覆盖")
    ap.add_argument("--touches", default=None, help="回填：touches 列")
    ap.add_argument("--expect", default=None, help="基线指纹断言：与当前行指纹不符则拒绝改写")
    ap.add_argument("--verify", default=None, help="提交前复核：当前行指纹是否等于给定值")
    ap.add_argument("--dry-run", action="store_true", help="只演练不写盘")
    ap.add_argument("--append-claim", action="store_true", help="追加认领行（纯追加）")
    ap.add_argument("--desc", default="", help="--append-claim 的描述")
    ap.add_argument("--session", default="", help="--append-claim 的认领会话")
    ap.add_argument("--ledger", default=LEDGER, help="台账路径（默认仓内）")
    ap.add_argument("--self-test", action="store_true", help="自测")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    if args.append_claim:
        return cmd_append_claim(args, args.ledger)
    if not args.w:
        print("FAIL  需要 --w <W 号>")
        return 1
    return cmd_backfill(args, args.ledger)


if __name__ == "__main__":
    raise SystemExit(main())
