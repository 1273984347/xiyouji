#!/usr/bin/env python3
"""safe_commit.py — 并行会话 ref-lock 竞争安全提交（W698·P2-2）

场景：单工作树多会话并行交付时，`git commit` 的 pre-commit 门禁要跑数十秒到数分钟，
期间并行会话先行落库 → 本提交更新 HEAD 时报
`cannot lock ref 'HEAD': is at X but expected Y`（2026-10-11 BL-20 批实证，重试即过）。

本工具封装「提交 + 竞争检测 + 至多一次受控重试」：

    python scripts/safe_commit.py -F <msgfile> [--] <pathspec...>
    python scripts/safe_commit.py -m "message" <pathspec...>
    python scripts/safe_commit.py -F <msgfile> --expect-spec scripts/output/_w####_spec.json
    python scripts/safe_commit.py --self-test

--expect-spec（W1006·防代提硬拦）：提交前把**索引态路径集**与本批 spec 的
`file_index_rows` 求差，出现 spec 之外的文件即拒绝提交（并列出前若干项与改法）。
语义：spec 是「本批应该动哪些文件」的声明，差集非空就说明索引里混进了他方在途件
（W989 / W1002 / W1004 三次代提实证）。给 `--expect-spec` 时可省略 pathspec
（索引态提交，前提是索引 ⊆ spec）。

重试安全规则：重试前核对 old..HEAD 并行增量与本次 pathspec 的文件交集——
无交集（对方没碰我要提交的文件）才重试一次；有交集则放弃并打印分析，
由人决定合并方式，绝不静默吞掉对方提交或把对方改动卷进本提交。

退出码：成功 0；ref-lock 竞争且不可安全重试 2；其他 git 失败 1。
"""
import subprocess
import sys

LOCK_MARK = "cannot lock ref"

# W821：§8 干扰日志的机器触发点提示（真触发才输出·用户裁决 2026-10-20）。
# 背景同 preflight_check.py：两周干扰日志无机器防线 → 断档 4 天零登记，
# 而该期间实际发生 ≥2 次强制触发事件。本提示在 **ref-lock 竞争真正发生** 时喊一声，
# 把「靠人记得写日志」变成「机器在真发生时喊一声」，**不改变任何判定与退出码**。
INTERFERENCE_LOG_HINT = (
    "⚠     §8 干扰日志待登记：本次命中强制录入触发（路线图 §8·窗口 2026-10-14 → 10-28）"
    "——请在 docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md "
    "的 §8 表追加一行（日期/会话/事件类/共享面/读时状态/写时状态/损失返工）"
)


def interference_log_hint(reason):
    """构造 §8 干扰日志待登记提示行（带命中原因）。返回单行字符串。"""
    return "%s（命中：%s）" % (INTERFERENCE_LOG_HINT, reason)


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


def _spec_paths(spec):
    """从级联 spec 取「本批应动文件」全集——**统一走 batch_spec**（W1009 合并重复实现）。

    W1007 踩过：两处各自解析 spec 行，一处取 cells[0] 一处取 cells[1]，改一处另一处还错。
    """
    import batch_spec
    return batch_spec.spec_paths_from_spec(spec)

def _plan_spec(staged, spec_paths):
    """纯逻辑：索引态 ⊆ spec？返回 (ok, extra, missing)。供 --self-test 与单测。"""
    staged_set = {p.replace("\\", "/") for p in staged}
    spec_set = {p.replace("\\", "/") for p in spec_paths}
    extra = sorted(staged_set - spec_set)
    missing = sorted(spec_set - staged_set)
    return (not extra and bool(spec_set)), extra, missing


def _guard_staged(staged_names, pathspecs, expect_spec=None):
    """W991 守卫：无 pathspec 且索引有暂存件 → 拒绝（防扫入他方暂存·W989 实证）。

    pathspec 形态提交走临时索引（HEAD+worktree·W649 口径），只取声明路径的
    worktree 态——他方已暂存未提交的件天然隔离在外。
    """
    if pathspecs or expect_spec:
        return True, ""
    if not staged_names:
        return True, ""
    return False, (
        "[safe_commit] 拒绝：索引含 %d 个暂存件且未指 pathspec——无 pathspec 提交会扫入全部暂存件"
        "（含并行会话的·W989 实证混入级联十四面）。改用：safe_commit -F <msg> -- <逐文件路径>" % len(staged_names))


def commit(msg_args, pathspecs, max_retry=1, expect_spec=None):
    staged = []
    r = subprocess.run(["git", "-c", "core.quotePath=false", "-c", "diff.renames=false",
                        "diff", "--cached", "--name-only"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode == 0:
        staged = [x.strip().replace("\\", "/") for x in r.stdout.split("\n") if x.strip()]
    spec_paths = None
    if expect_spec:
        import json
        try:
            spec = json.load(open(expect_spec, encoding="utf-8"))
        except (OSError, ValueError) as e:
            print("[safe_commit] 拒绝：--expect-spec 读不出（%s）：%s" % (expect_spec, e))
            return 1
        spec_paths = _spec_paths(spec)
        ok_spec, extra, missing = _plan_spec(staged, spec_paths)
        if not spec_paths:
            print("[safe_commit] 拒绝：spec 的 file_index_rows 为空（判据不可执行·fail-closed）")
            return 1
        if extra:
            print("[safe_commit] 拒绝：索引含 %d 个 **spec 之外** 的文件（代提风险·W989/W1002/W1004 三次实证）"
                  % len(extra))
            for name in extra[:10]:
                print("      extra: " + name)
            if len(extra) > 10:
                print("      …另 %d 件" % (len(extra) - 10))
            print("      改法：git restore --staged <路径> 摘出；或把该件写入本批 spec 后再提交")
            return 1
        if missing:
            print("[safe_commit] NOTE：spec 声明了 %d 件但索引里没有（可能已入库/无需改）：%s%s"
                  % (len(missing), ", ".join(missing[:5]), " …" if len(missing) > 5 else ""))
    ok, why = _guard_staged(staged, pathspecs, expect_spec)
    if not ok:
        print(why)
        for name in staged[:8]:
            print("      staged: " + name)
        if len(staged) > 8:
            print("      …另 %d 件" % (len(staged) - 8))
        return 1
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
                # W821：触发②（safe_commit 触发重试）——真触发才提示登记 §8 干扰日志
                print(interference_log_hint("safe_commit ref-lock 竞争触发重试"))
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
            (LOCK_MARK + ": is at X but expected Y", A, B, ["HANDOVER.md"], True,
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
    # --expect-spec 判据（W1006）：4 例纯逻辑
    spec_cases = [
        ("索引 ⊆ spec", ["a.py", "b.md"], ["a.py", "b.md", "c.md"], True),
        ("索引多出他方件", ["a.py", "other.py"], ["a.py"], False),
        ("spec 空（fail-closed）", ["a.py"], [], False),
        ("索引为空但 spec 非空（缺件只提示）", [], ["a.py"], True),
    ]
    for name, staged, spec, expect in spec_cases:
        ok_spec, extra, missing = _plan_spec(staged, spec)
        mark = "OK " if (ok_spec if extra or spec else False) == expect else "FAIL"
        fails += 0 if mark == "OK " else 1
        cases += 1
        print("%s  spec：%s（extra=%s missing=%s）" % (mark, name, extra, missing))
    print("self-test: %d/%d 通过" % (cases - fails, cases))
    return 1 if fails else 0


def main():
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return _self_test()
    msg_args = []
    pathspecs = []
    expect_spec = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "-F" and i + 1 < len(argv):
            msg_args = ["-F", argv[i + 1]]
            i += 2
        elif a == "-m" and i + 1 < len(argv):
            msg_args = ["-m", argv[i + 1]]
            i += 2
        elif a == "--expect-spec" and i + 1 < len(argv):
            expect_spec = argv[i + 1]
            i += 2
        elif a.startswith("--expect-spec="):
            expect_spec = a.split("=", 1)[1]
            i += 1
        elif a == "--":
            pathspecs.extend(argv[i + 1:])
            break
        elif a.startswith("-"):
            print("[safe_commit] 不支持的参数: %s（仅支持 -F/-m/--expect-spec/-- 与 pathspec）" % a)
            return 1
        else:
            pathspecs.append(a)
            i += 1
    if not msg_args:
        print("[safe_commit] 缺提交信息（-F <file> 或 -m \"msg\"；多行信息按 AGENTS §4.3 走 -F）")
        return 1
    return commit(msg_args, pathspecs, expect_spec=expect_spec)


if __name__ == "__main__":
    sys.exit(main())
