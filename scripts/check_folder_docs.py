#!/usr/bin/env python3
"""check_folder_docs.py — 目录文档新鲜度门禁（W780 建立·verify_delivery 第 45 槽）。

背景（W779 落地即登记的漂移面）：gen_folder_docs.py@W779 为全仓在管目录写
index.md（逐文件清单·机器可读）与 README.md（目录导读），两者均为「生成时点快照」
——目录内容增删后清单即过期，且此前无任何机器防线（生成器自述「新增文件后
index.md 不会自动更新」）。本槽把该漂移面关进可验证的笼子：清单与磁盘实况逐项对拍。

检查项（全过 exit 0，任一 FAIL exit 1）：
C1 在管目录两件套存在性：index.md 与 README.md 均在（新目录落地未跑生成器即拦）
C2 index.md「## 子目录（N）」段清单 == list_subdirs() 实算（成员与计数双对拍）
C3 index.md「## 文件（N）」段清单 == list_files() 实算（跨分组成员并集·计数对拍）
C4 index.md H1 标题尾部目录名 == 实际目录名（防目录改名后标题滞留）

豁免（设计裁定）：README.md 正文不校验——其数字声明全部带「生成时点」时点限定
（文档规范 §4.9/§4.10 形态·禁裸聚合现役值），过期不构成谎报；index.md 是唯一
机器可读清单主张，故为唯一对拍面。

单一事实源：在管目录集、gitignored 过滤、清单算法全部 import 自
scripts/gen_folder_docs.py（GOVERNED_SKIP/in_scope 已提升模块级）——生成器改口径
本门禁自动跟随，两处维护即漂移被结构性排除。

跨平台断言纪律（pitfalls「latent 三问 + 双平台断言禁例」）：全部比对基于名字符串
（sorted(str)=码点序·两平台一致）；零 os.name/盘符/大小写语义断言；负样本用系统
临时目录注入（合成树两平台同构·不触仓库），真实执行位=CI（Linux）与本地（Windows）
同断言。

用法：
    python scripts/check_folder_docs.py             # 门禁模式（= --gate）
    python scripts/check_folder_docs.py --gate      # 同上（verify_delivery 调用形态）
    python scripts/check_folder_docs.py --self-test # 注入式自测（1 正 6 负·不触仓库）

退出码：0 全过；1 有 FAIL；2 参数/环境错误。
"""

from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gen_folder_docs as gen  # noqa: E402  单一事实源：在管目录集与清单算法全在此

MARKER = "---- 第 45 门禁 目录文档新鲜度："

_H1_RE = re.compile(r"^# 文件索引 · (.+?)\s*$")
_SUBSEC_RE = re.compile(r"^## 子目录（(\d+)）\s*$")
_FILESEC_RE = re.compile(r"^## 文件（(\d+)）\s*$")
_ITEM_DIR_RE = re.compile(r"^- `(.+)/`\s*$")
_ITEM_FILE_RE = re.compile(r"^- `(.+?)`\s*$")

# 大小写冲突豁免：目录内已有 INDEX.md 等变体时，生成器因 NTFS 覆写守卫（W779 判重·
# gen.case_collides 全模式跳过）不管理该目录，门禁同口径豁免。判定在生成器模块
# （单一事实源）：os.listdir 真名小写比对，两平台同构——否则 Windows 把 INDEX.md
# 当 index.md 读到异构内容、Linux 报缺件，同一目录两平台两种红法（W780 首跑实证 docs/）。
def _case_collides(abs_dir: str) -> bool:
    return gen.case_collides(abs_dir)


def parse_index(text: str) -> dict | None:
    """解析 index.md → {title, sub_n, file_n, subdirs, files}；结构不合模板返回 None。"""
    title = None
    sub_n = file_n = None
    subdirs: list[str] = []
    files: list[str] = []
    section = None
    for ln in text.splitlines():
        m = _H1_RE.match(ln)
        if m:
            if title is None:
                title = m.group(1)
            continue
        m = _SUBSEC_RE.match(ln)
        if m:
            sub_n = int(m.group(1))
            section = "sub"
            continue
        m = _FILESEC_RE.match(ln)
        if m:
            file_n = int(m.group(1))
            section = "file"
            continue
        if ln.startswith("## ") or ln.startswith("---"):
            section = None
            continue
        if section == "sub":
            m = _ITEM_DIR_RE.match(ln)
            if m:
                subdirs.append(m.group(1))
        elif section == "file":
            m = _ITEM_FILE_RE.match(ln)
            if m:
                files.append(m.group(1))
    if title is None or sub_n is None or file_n is None:
        return None
    return {"title": title, "sub_n": sub_n, "file_n": file_n,
            "subdirs": subdirs, "files": files}


def check_dir(abs_dir: str) -> list[str]:
    """单目录四项检查，返回 FAIL 行列表（空=过）。"""
    rel = gen.rel_of(abs_dir)
    label = rel or "<root>"
    fails: list[str] = []
    idx_path = os.path.join(abs_dir, "index.md")
    rdm_path = os.path.join(abs_dir, "README.md")
    if not os.path.isfile(idx_path):
        fails.append("C1 缺 index.md：%s" % label)
    if not os.path.isfile(rdm_path):
        fails.append("C1 缺 README.md：%s" % label)
    if not os.path.isfile(idx_path):
        return fails  # 清单不在，对拍无意义
    with open(idx_path, encoding="utf-8") as f:
        parsed = parse_index(f.read())
    if parsed is None:
        fails.append("C2 index.md 结构不合生成器模板（疑手改/旧版/截断）：%s" % label)
        return fails
    want_sub = gen.list_subdirs(abs_dir)
    want_files = gen.list_files(abs_dir)
    if parsed["sub_n"] != len(want_sub) or sorted(parsed["subdirs"]) != sorted(want_sub):
        miss = sorted(set(want_sub) - set(parsed["subdirs"]))[:5]
        extra = sorted(set(parsed["subdirs"]) - set(want_sub))[:5]
        fails.append("C2 子目录清单漂移：%s（文档 %d 项/实算 %d 项·盘上多 %r·文档多 %r）"
                     % (label, len(parsed["subdirs"]), len(want_sub), miss, extra))
    if parsed["file_n"] != len(want_files) or sorted(parsed["files"]) != sorted(want_files):
        miss = sorted(set(want_files) - set(parsed["files"]))[:5]
        extra = sorted(set(parsed["files"]) - set(want_files))[:5]
        fails.append("C3 文件清单漂移：%s（文档 %d 项/实算 %d 项·盘上多 %r·文档多 %r）"
                     % (label, len(parsed["files"]), len(want_files), miss, extra))
    want_title = os.path.basename(abs_dir) if rel else "仓库根目录"
    if parsed["title"] != want_title:
        fails.append("C4 H1 标题漂移：%s（文档 %r/实际 %r）" % (label, parsed["title"], want_title))
    return fails


def run_gate() -> int:
    """门禁主流程：逐在管目录对拍，汇总行恒输出（防静默跳过）。"""
    gen._GITIGNORED_DIRS = gen._build_gitignored_dirs()
    dirs_all = [d for d in gen.scan_dirs() if gen.in_scope(d)]
    dirs = [d for d in dirs_all if not _case_collides(d)]
    exempt = len(dirs_all) - len(dirs)
    all_fails: list[str] = []
    for d in dirs:
        all_fails.extend(check_dir(d))
    for f in all_fails:
        print("FAIL " + f)
    print("%s%d FAIL / %d 目录（大小写冲突豁免 %d）----"
          % (MARKER, len(all_fails), len(dirs), exempt))
    return 1 if all_fails else 0


def self_test() -> int:
    """注入式自测：合成树 1 正 6 负（全部两平台可判）。"""
    import shutil
    import tempfile

    base = tempfile.mkdtemp(prefix="cfd_selftest_")
    old_root, old_ignored = gen.ROOT, gen._GITIGNORED_DIRS
    try:
        gen.ROOT = base
        gen._GITIGNORED_DIRS = set()  # 合成树无 git 仓·gitignored 过滤自然为空集
        d1 = os.path.join(base, "alpha")
        os.makedirs(d1)
        for name in ("a.md", "b.py"):
            with open(os.path.join(d1, name), "w"):
                pass
        for kind in ("index.md", "README.md"):
            with open(os.path.join(d1, kind), "w", encoding="utf-8", newline="\n") as f:
                f.write(gen.render(d1, kind))

        def write_idx(content: str) -> None:
            with open(os.path.join(d1, "index.md"), "w", encoding="utf-8", newline="\n") as f:
                f.write(content)

        def fresh_idx() -> str:
            with open(os.path.join(d1, "index.md"), encoding="utf-8") as f:
                return f.read()

        cases: list[tuple[str, list[str], list[str]]] = []
        cases.append(("fresh-pass", check_dir(d1), []))

        with open(os.path.join(d1, "c.py"), "w"):
            pass
        cases.append(("added-file-must-red", check_dir(d1), ["C3"]))
        os.remove(os.path.join(d1, "c.py"))

        os.remove(os.path.join(d1, "b.py"))
        cases.append(("removed-file-must-red", check_dir(d1), ["C3"]))
        with open(os.path.join(d1, "b.py"), "w"):
            pass

        os.makedirs(os.path.join(d1, "sub"))
        cases.append(("added-subdir-must-red", check_dir(d1), ["C2"]))
        os.rmdir(os.path.join(d1, "sub"))

        os.remove(os.path.join(d1, "README.md"))
        cases.append(("missing-readme-must-red", check_dir(d1), ["C1"]))
        with open(os.path.join(d1, "README.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write(gen.render(d1, "README.md"))

        write_idx(fresh_idx().replace("- `a.md`\n", ""))
        cases.append(("tampered-list-must-red", check_dir(d1), ["C3"]))
        write_idx(gen.render(d1, "index.md"))

        write_idx(fresh_idx().replace("# 文件索引 · alpha", "# 文件索引 · alpha-old"))
        cases.append(("title-drift-must-red", check_dir(d1), ["C4"]))

        ok = True
        for name, fails, expect in cases:
            hit = (len(fails) == 0 if not expect
                   else len(fails) > 0 and all(any(e in f for f in fails) for e in expect))
            print(("PASS " if hit else "RED-MISS ") + name + ("" if hit else " → %r" % (fails,)))
            ok = ok and hit
        print("%sself-test 7 例（1 正 6 负）：%s ----" % (MARKER, "全过" if ok else "有红"))
        return 0 if ok else 1
    finally:
        gen.ROOT, gen._GITIGNORED_DIRS = old_root, old_ignored
        shutil.rmtree(base, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="目录文档新鲜度门禁（第 45 槽）")
    ap.add_argument("--gate", action="store_true", help="门禁模式（默认）")
    ap.add_argument("--self-test", action="store_true", help="注入式自测（合成树·不触仓库）")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    return run_gate()


if __name__ == "__main__":
    sys.exit(main())
