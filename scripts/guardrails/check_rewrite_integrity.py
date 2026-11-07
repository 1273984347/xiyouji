#!/usr/bin/env python3
"""check_rewrite_integrity.py — 改写完整性判据（W1159·guardrails 第 3.5 步接线）。

坑表 E-199（W1158 实证）的机器判据面：对既有 .py 做「大块程序化改写」（Edit 半段替换 /
行扫描切除 / 整段拼接）时，两类破坏形态语法合法、py_compile 与 ruff 风格档双绿、唯有
结构档复杂度红灯且易被误读——本判据把它们变成确定性红灯：

  C1 语法可编译：py_compile 逐文件（切崩文件即拦·本次「整文件切剩 4 行」事故形态）。
  C2 公开函数集不得缩水：HEAD 版模块级公开 def（非 _ 前缀）在当前版必须仍存在——
     防整函数被删/切除（本次行扫描事故会把 HEAD 全部 def 切光·当场红）。
     缩水即 FAIL 并列出消失清单；改名场景由提交说明声明（人工复核闸）。
  C3 模块级同名 def 不得重复：顶层（零缩进）同名 def 出现 ≥2 即 FAIL（本次「旧 main
     后半段粘连成第二定义」的拼接残留形态；条件定义请移入 try/if 块使其缩进·不误报）。

用法：check_rewrite_integrity.py <file.py>...；--self-test 注入式负样本 4 例。
退出码：0 通过 / 1 判红 / 2 自测失败。只读不改任何文件。
"""
from __future__ import annotations

import os
import py_compile
import re
import subprocess
import sys

DEF_RE = re.compile(r"(?m)^def\s+(\w+)\s*\(")


def module_defs(text):
    """模块级（零缩进）def 名集合与重名统计。"""
    names = DEF_RE.findall(text)
    seen, dup = {}, []
    for n in names:
        seen[n] = seen.get(n, 0) + 1
    for n, c in seen.items():
        if c > 1:
            dup.append(n)
    return set(seen), sorted(dup)


def head_text(path):
    r = subprocess.run(["git", "show", "HEAD:%s" % path.replace(os.sep, "/")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout if r.returncode == 0 else None


def check_one(path):
    """→ (fails, notes)：单文件三判据。新文件（HEAD 无）只跑 C1/C3。"""
    fails, notes = [], []
    # C1 语法可编译
    try:
        py_compile.compile(path, doraise=True)
    except py_compile.PyCompileError as e:
        fails.append("C1: %s 语法不可编译：%s" % (path, str(e).splitlines()[0][:120]))
        return fails, notes  # 后续判据依赖可解析文本
    with open(path, encoding="utf-8") as f:
        cur = f.read()
    cur_defs, cur_dups = module_defs(cur)
    # C3 模块级同名 def 重复（拼接残留形态）
    for n in cur_dups:
        fails.append("C3: %s 模块级 def %r 出现多次（拼接残留形态·E-199）——确认是否旧体残留" % (path, n))
    # C2 公开函数集 vs HEAD
    old = head_text(path)
    if old is None:
        notes.append("NOTE  %s HEAD 无此文件（新增文件·C2 跳过）" % path)
        return fails, notes
    old_defs, _ = module_defs(old)
    vanished = sorted(n for n in (old_defs & set(re.findall(r"\w+", "")) | old_defs)
                      if n not in cur_defs and not n.startswith("_"))
    for n in vanished:
        fails.append("C2: %s 公开函数 %r 在 HEAD 存在而当前版消失（切除/误删形态·E-199）——"
                     "若属有意改名须在提交说明声明" % (path, n))
    return fails, notes


def main(argv):
    if "--self-test" in argv:
        return _self_test()
    files = [a for a in argv if a.endswith(".py")]
    if not files:
        print("NOTE  无 .py 改动（改写完整性判据跳过）")
        return 0
    fails, notes = [], []
    for p in files:
        f, n = check_one(p)
        fails += f
        notes += n
    for n_ in notes:
        print(n_)
    for f_ in fails:
        print("FAIL  " + f_)
    if not fails:
        print("NOTE  改写完整性：语法/函数集/重复定义 三判据全过（%d 文件）" % len(files))
    print("---- 改写完整性判据（E-199）：%d FAIL ----" % len(fails))
    return 1 if fails else 0


def _self_test():
    """注入式负样本 4 例：切崩文件/函数消失/双定义/干净输入。"""
    import tempfile
    tally = []

    def run_case(name, head_src, cur_src, expect):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "mod.py")
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(cur_src)
            os.makedirs(os.path.join(td, ".git"), exist_ok=True)
            # head_text 走 git show·自测内直接注入替换
            orig = check_one.__globals__.get("head_text")
            check_one.__globals__["head_text"] = lambda _p: head_src
            try:
                fails, _ = check_one(p)
            finally:
                check_one.__globals__["head_text"] = orig
            ok = (not fails) if expect is None else any(f.startswith(expect) for f in fails)
            tally.append(ok)
            print("%s  %s" % ("PASS" if ok else "FAIL", name))
            if not ok:
                for f_ in fails:
                    print("      -> " + f_)

    run_case("T1 干净输入零误报",
             "def main():\n    return 0\n", "def main():\n    return 0\n", None)
    run_case("T2 切崩文件必红（C1）",
             "def main():\n    return 0\n", "    return 0\n", "C1")
    run_case("T3 公开函数消失必红（C2）",
             "def main():\n    return 0\n\ndef helper():\n    return 1\n",
             "def main():\n    return 0\n", "C2")
    run_case("T4 双定义必红（C3）",
             "def main():\n    return 0\n",
             "def main():\n    return 0\n\n\ndef main():\n    return 1\n", "C3")
    # 私有函数消失放行（C2 只守公开面）
    run_case("T5 私有函数消失放行（C2 不越权）",
             "def main():\n    return 0\n\ndef _helper():\n    return 1\n",
             "def main():\n    return 0\n", None)
    print("---- 改写完整性自测：%d/%d 过 ----" % (sum(tally), len(tally)))
    return 0 if all(tally) else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
