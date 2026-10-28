#!/usr/bin/env python3
"""check_repo_layout.py — 第 52 门禁：仓库布局（W1011 挂槽·用户 2026-10-29「全都做」）

## 为什么要有这道门禁

「整理分类」如果只做一次性搬家，三个月后又会长出新的错位文件——W1011 盘点时就在**根目录**
逮到 `_tmp_chap_sheet.py`（临时脚本）与散落的 `tools/`、`references/`、`timeline/`（各只装
一个真文件 + 生成物）。分类要长期成立，必须把「哪个目录装什么」变成可执行判据。

## 判据（三条）

1. **L1 根目录只放治理与配置**：根下的**文件**必须 ∈ `ROOT_FILES`（白名单含生成物
   `index.md` 与各类配置）。出现未声明文件 → FAIL（提示该去哪儿：临时件 tmpe/、
   脚本 scripts/、文档 docs/、退役件 archive/）。
2. **L2 顶层目录必须已声明角色**：顶层目录 ∈ `TOP_DIRS`（前导 `.` 的隐藏目录不计）。
   新增顶层目录 = 必须先在本文件与 `STRUCTURE.md` 声明角色 → 否则 FAIL。
3. **L3 白名单不得陈腐**：声明了但磁盘不存在的条目 → FAIL（防白名单变垃圾场；
   可选目录用 `OPTIONAL_DIRS` 单独登记，允许缺席）。

判据纯本地、零依赖、毫秒级，故登记 `_SCOPE_CORE` 恒跑（布局与 scope 无关）。

## 用法

    py -3 scripts/check_repo_layout.py --gate       # 门禁模式（末行恒为汇总行）
    py -3 scripts/check_repo_layout.py --report     # 列现状与差异（不判退出码）
    py -3 scripts/check_repo_layout.py --self-test  # 纯逻辑 5 例
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKER = "---- 第 52 门禁 仓库布局："

# 根目录允许的**文件**（目录另算）。新增根文件必须先在此声明并写进 STRUCTURE.md。
ROOT_FILES = {
    # 治理与契约
    "AGENTS.md", "CLAUDE.md", "DESIGN.md", "HANDOVER.md", "STRUCTURE.md",
    "CHANGELOG.md", "README.md", "README.en.md", "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md", "SECURITY.md", "LICENSE", "LICENSE-CONTENT.md", "CITATION.cff",
    # 工程配置
    "Makefile", "pyproject.toml", "pytest.ini", "mypy.ini", "eslint.config.mjs",
    ".gitignore", ".gitattributes", ".git-blame-ignore-revs", ".pre-commit-config.yaml",
    ".env.example",
    # 生成物（gen_folder_docs）
    "index.md",
}

# 顶层目录角色（与 STRUCTURE.md「目录职责」表一一对应）
TOP_DIRS = {
    "archive": "退役件与历史批次",
    "assets": "设计母版与素材",
    "dataset": "结构化数据（从站点提取）",
    "docs": "内容与方法论（编号板块 + 00-导读 + agent）",
    "hyperframes": "视频化架构（Compositions）",
    "mcp-server": "MCP 服务端",
    "packaging": "打包与分发",
    "scripts": "生成器 / 门禁 / 工具",
    "site": "交付站点（855 页）",
    "source": "原文语料",
    "tests": "单元与 E2E 测试",
    "xiyouji-agent-web": "Web Agent 应用",
    "xiyouji-desktop": "桌面客户端",
}
OPTIONAL_DIRS = {"tmpe": "临时区（.gitignore）", ".github": "CI 配置"}


def judge(root_files, dirs, root_allow=None, dir_allow=None, optional=None):
    """纯逻辑：→ (ok, extra_files, extra_dirs, missing)。"""
    root_allow = set(ROOT_FILES if root_allow is None else root_allow)
    dir_allow = set(TOP_DIRS if dir_allow is None else dir_allow)
    optional = set(OPTIONAL_DIRS if optional is None else optional)
    extra_files = sorted(f for f in root_files if f not in root_allow)
    extra_dirs = sorted(d for d in dirs if not d.startswith(".") and d not in dir_allow
                        and d not in optional)
    missing = sorted((root_allow - set(root_files)) | (dir_allow - set(dirs)))
    ok = not extra_files and not extra_dirs
    return ok, extra_files, extra_dirs, missing


def _ignored(names):
    """git 视角的忽略集（.env / .coverage / 审计包这类本地件不该算「布局」）。"""
    import subprocess
    if not names:
        return set()
    # 二进制喂 stdin：Windows 文本模式会把 \n 翻成 \r\n，git 便匹配不上（W1011 实测踩坑）
    payload = ("\n".join(names) + "\n").encode("utf-8")
    r = subprocess.run(["git", "check-ignore", "--stdin"], input=payload,
                       capture_output=True, cwd=ROOT)
    return {x.strip() for x in (r.stdout or b"").decode("utf-8", "replace").splitlines() if x.strip()}


def scan():
    """→ (根文件, 顶层目录)——**只算版本库视角**：被 .gitignore 忽略的本地件不计入。"""
    entries = os.listdir(ROOT)
    ignored = _ignored(entries)
    root_files = [e for e in entries
                  if os.path.isfile(os.path.join(ROOT, e)) and e not in ignored]
    dirs = [e for e in entries
            if os.path.isdir(os.path.join(ROOT, e)) and e not in ignored]
    return sorted(root_files), sorted(dirs)


def _hint(name):
    if name.endswith((".py", ".js", ".mjs")):
        return "→ scripts/（入库工具）或 tmpe/（一次性·不入库）"
    if name.endswith((".md", ".txt")):
        return "→ docs/（内容或方法论）或 docs/00-导读/"
    if name.startswith("_tmp") or name.startswith("tmp_"):
        return "→ tmpe/（临时区·不入库）"
    return "→ 归档 archive/ 或先在本门禁显式声明"


def run_gate():
    root_files, dirs = scan()
    ok, extra_files, extra_dirs, missing = judge(root_files, dirs)
    fails = []
    for f in extra_files:
        fails.append("L1 根目录出现未声明文件：%s  %s" % (f, _hint(f)))
    for d in extra_dirs:
        fails.append("L2 顶层出现未声明目录：%s/  ——先在 TOP_DIRS 与 STRUCTURE.md 声明角色" % d)
    for m in missing:
        fails.append("L3 白名单条目在磁盘不存在：%s（删声明或补文件·防白名单陈腐）" % m)
    for it in fails:
        print("FAIL  " + it)
    if not fails:
        print("NOTE  根文件 %d 个 / 顶层目录 %d 个，全部在声明内" % (len(root_files), len(dirs)))
    print("%s%d FAIL ----" % (MARKER, len(fails)))
    return 1 if fails else 0


def run_report():
    root_files, dirs = scan()
    ok, extra_files, extra_dirs, missing = judge(root_files, dirs)
    print("根目录文件 %d 个：" % len(root_files))
    print("  " + "、".join(root_files))
    print("顶层目录 %d 个：" % len(dirs))
    print("  " + "、".join(dirs))
    print("未声明文件：%s" % (extra_files or "无"))
    print("未声明目录：%s" % (extra_dirs or "无"))
    print("陈腐声明：%s" % (missing or "无"))
    return 0 if ok else 1


def _self_test():
    """5 例：干净态 / 根文件多出 / 顶层目录多出 / 隐藏目录豁免 / 白名单陈腐可检出。"""
    A_F = {"README.md", "index.md"}
    A_D = {"docs", "scripts", "site"}
    cases = [
        # 名称, 磁盘文件, 磁盘目录, 允许文件, 允许目录, 期望 extra_files, extra_dirs, missing
        ("干净态放行", ["README.md", "index.md"], ["docs", "scripts", "site"], A_F, A_D, 0, 0, 0),
        ("根目录多出临时脚本", ["README.md", "index.md", "_tmp_x.py"], ["docs", "scripts", "site"], A_F, A_D, 1, 0, 0),
        ("顶层多出未声明目录", ["README.md", "index.md"], ["docs", "scripts", "site", "junk"], A_F, A_D, 0, 1, 0),
        ("隐藏目录不计", ["README.md", "index.md"], ["docs", "scripts", "site", ".git", ".ruff_cache"], A_F, A_D, 0, 0, 0),
        ("白名单陈腐可检出", ["README.md", "index.md"], ["docs", "scripts", "site"],
         A_F | {"ghost.md"}, A_D | {"ghost"}, 0, 0, 2),
    ]
    fails = 0
    for name, f, d, af, ad, nf, nd, nm in cases:
        ok, ef, ed, ms = judge(f, d, af, ad, set())
        good = (len(ef) == nf and len(ed) == nd and len(ms) == nm)
        mark = "OK " if good else "FAIL"
        fails += 0 if good else 1
        print("%s  %s（extra_files=%d extra_dirs=%d missing=%d）"
              % (mark, name, len(ef), len(ed), len(ms)))
    print("self-test: %d/%d 通过" % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


def main():
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return _self_test()
    if "--report" in argv:
        return run_report()
    return run_gate()


if __name__ == "__main__":
    sys.exit(main())
