#!/usr/bin/env python3
"""safe_commit.py — 并行会话 ref-lock 竞争安全提交（W698·P2-2）

场景：单工作树多会话并行交付时，`git commit` 的 pre-commit 门禁要跑数十秒到数分钟，
期间并行会话先行落库 → 本提交更新 HEAD 时报
`cannot lock ref 'HEAD': is at X but expected Y`（2026-10-11 BL-20 批实证，重试即过）。

本工具封装「提交 + 竞争检测 + 至多一次受控重试」：

    python scripts/safe_commit.py -F <msgfile> [--] <pathspec...>
    python scripts/safe_commit.py -m "message" <pathspec...>
    python scripts/safe_commit.py --self-test

重试安全规则：重试前核对 old..HEAD 并行增量与本次 pathspec 的文件交集——
无交集（对方没碰我要提交的文件）才重试一次；有交集则放弃并打印分析，
由人决定合并方式，绝不静默吞掉对方提交或把对方改动卷进本提交。

退出码：成功 0；ref-lock 竞争且不可安全重试 2；其他 git 失败 1。
"""
import subprocess
import sys

LOCK_MARK = "cannot lock ref"


def _run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def _head():
    r = _run(["git", "rev-parse", "HEAD"])
    return r.stdout.strip() if r.returncode == 0 else None


def _range_files(old, new):
    """old..new 区间改动的文件集合（并行增量核对用）。"""
    r = _run(["git", "-c", "core.quotePath=false", "diff", "--name-only",
              "%s..%s" % (old, new)])
    return {ln.strip().replace("\\", "/") for ln in r.stdout.splitlines() if ln.strip()}


def _plan_retry(err_text, old, new, pathspecs):
    """纯逻辑：ref-lock 失败后是否可安全重试。返回 (bool, 原因)。供 --self-test。"""
    if LOCK_MARK not in err_text:
        return False, "非 ref-lock 失败"
    if not old or not new or old == new:
        return False, "HEAD 未前进（非并行竞争，重试无意义）"
    norm_paths = {p.replace("\\", "/") for p in pathspecs}
    clash = _range_files(old, new) & norm_paths
    if clash:
        return False, "并行提交与本次 pathspec 文件交集: %s" % sorted(clash)
    return True, "并行增量与本次 pathspec 无交集，可安全重试"


def commit(msg_args, pathspecs, max_retry=1):
    attempted = 0
    while True:
        attempted += 1
        old = _head()
        cmd = ["git", "commit"] + list(msg_args)
        if pathspecs:
            cmd += ["--"] + list(pathspecs)
        r = subprocess.run(cmd, capture_output=True, text=True)
        out = (r.stdout or "") + (r.stderr or "")
        if r.returncode == 0:
            print(out.strip())
            return 0
        new = _head()
        if attempted <= max_retry:
            retry, reason = _plan_retry(out, old, new, pathspecs)
            if retry:
                print("[safe_commit] ref-lock 竞争（HEAD %s → %s）：%s，重试第 %d 次"
                      % ((old or "?")[:9], (new or "?")[:9], reason, attempted))
                continue
            if LOCK_MARK in out:
                print("[safe_commit] 竞争不可自动重试：%s" % reason)
        print(out.strip())
        return 1 if LOCK_MARK not in out else 2


def _self_test():
    """纯逻辑负样本 4 例：非竞争 / HEAD 未前进 / 无交集可重试 / 有交集拒重试。"""
    A = "0123456789abcdef0123456789abcdef01234567"
    B = "fedcba9876543210fedcba9876543210fedcba98"
    FAKE_FILES = {"CHANGELOG.md", "site/data/x.html"}
    orig = _range_files
    globals()["_range_files"] = lambda old, new: set(FAKE_FILES) if old != new else set()
    fails = 0
    cases = 0
    try:
        cases_list = [
            ("error: failed to push some refs", A, B, [], False, "非 ref-lock 失败"),
            (LOCK_MARK + ": is at X but expected Y", A, A, [], False, "HEAD 未前进"),
            (LOCK_MARK + ": is at X but expected Y", A, B, ["交接文档.md"], True,
             "并行增量无交集可重试"),
            (LOCK_MARK + ": is at X but expected Y", A, B, ["CHANGELOG.md"], False,
             "并行增量有交集拒重试"),
        ]
        for i, (err, old, new, paths, expect, note) in enumerate(cases_list, 1):
            got, reason = _plan_retry(err, old, new, paths)
            mark = "OK " if got == expect else "FAIL"
            fails += 0 if got == expect else 1
            cases += 1
            print("%s  case%d expect=%s got=%s（%s | %s）" % (mark, i, expect, got, note, reason))
    finally:
        globals()["_range_files"] = orig
    print("self-test: %d/%d 通过" % (cases - fails, cases))
    return 1 if fails else 0


def main():
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return _self_test()
    msg_args = []
    pathspecs = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "-F" and i + 1 < len(argv):
            msg_args = ["-F", argv[i + 1]]
            i += 2
        elif a == "-m" and i + 1 < len(argv):
            msg_args = ["-m", argv[i + 1]]
            i += 2
        elif a == "--":
            pathspecs.extend(argv[i + 1:])
            break
        elif a.startswith("-"):
            print("[safe_commit] 不支持的参数: %s（仅支持 -F/-m/-- 与 pathspec）" % a)
            return 1
        else:
            pathspecs.append(a)
            i += 1
    if not msg_args:
        print("[safe_commit] 缺提交信息（-F <file> 或 -m \"msg\"；多行信息按 AGENTS §4.3 走 -F）")
        return 1
    return commit(msg_args, pathspecs)


if __name__ == "__main__":
    sys.exit(main())
