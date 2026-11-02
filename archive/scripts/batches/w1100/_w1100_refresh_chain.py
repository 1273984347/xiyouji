# -*- coding: utf-8 -*-
"""W1100 生成链顺序收敛脚本（仓内可复用·把顺序固化为机器知识）。

**顺序（为什么必须是这个顺序）**：
  1) git add 本批改动（生成器按 Git 索引收集文件 ⇒ refresh 晚于 add 才不漏新件）
  2) gen_folder_docs.py --refresh   （目录文档清单）
  3) _gen_search_index.py           （搜索索引含新文档）
  4) generate_csp.py                （搜索索引改动 ⇒ 两个 search.html 内联脚本哈希变化）
  5) docs_index.py                  （文档索引·含新报告）
  6) _gen_search_index.py **再跑一次**（docs/INDEX.md 变了 ⇒ 搜索索引须跟着刷新）
  7) generate_csp.py **再跑一次**（第 6 步改了搜索页内联脚本 ⇒ 哈希要重算）
  8) git add 再收一次

⚠️ 第 5~7 步的「再跑一次」是 W1099 与 W1100 **连续两次**踩到的坑
（test_check_search_index_fresh::test_g1_repo_fresh 失败 ⇒ 搜索索引陈旧）。
⚠️ 只跑到第 4 步会留下「文档索引已更新但搜索索引陈旧」的半状态 ⇒ 门禁第 46 槽与
   单测 test_check_search_index_fresh 会判红。
"""
import json
import subprocess
import sys

ROOT = r"D:\xiyouji"
SPEC = r"scripts\output\_w1100_spec.json"


def git(*a):
    return subprocess.run(["git", "-c", "core.quotePath=false", "-C", ROOT] + list(a),
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")


def spec_paths():
    with open(ROOT + "\\" + SPEC, encoding="utf-8") as f:
        spec = json.load(f)
    out = set()
    for row in spec["file_index_rows"]:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if cells and cells[0] not in ("文件", ""):
            out.add(cells[0].replace("\\", "/"))
    return out


def run(*args):
    r = subprocess.run([sys.executable] + list(args), cwd=ROOT, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    tail = (r.stdout or "").strip().splitlines()[-1:]
    print("$ %s -> exit=%d  %s" % (" ".join(args), r.returncode, tail[0][:110] if tail else ""))
    return r.returncode


def stage(paths_set):
    st = git("status", "--porcelain").stdout.splitlines()
    todo = []
    for line in st:
        if not line.strip():
            continue
        code, path = line[:2].strip(), line[3:].strip()
        norm = path.replace("\\", "/")
        if code == "??":
            if norm in paths_set:
                todo.append(path)
        else:
            todo.append(path)
    if todo:
        r = git("add", "--", *todo)
        print("git add %d 件 -> exit=%d" % (len(todo), r.returncode))
    return len(todo)


def main():
    paths_set = spec_paths()
    stage(paths_set)
    run("scripts/gen_folder_docs.py", "--refresh")
    stage(paths_set)
    run("scripts/_gen_search_index.py")
    run("scripts/generate_csp.py")
    run("scripts/docs_index.py")
    # ↓↓↓ 关键二次刷新（W1099/W1100 连续两次踩坑点）↓↓↓
    run("scripts/_gen_search_index.py")
    run("scripts/generate_csp.py")
    stage(paths_set)
    run("scripts/generate_csp.py", "--check")
    idx = set(git("diff", "--cached", "--name-only").stdout.split())
    bad = [p for p in idx if p.replace("\\", "/") not in paths_set]
    print("索引 %d 件·超出 spec：%s" % (len(idx), "、".join(bad) if bad else "无"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
