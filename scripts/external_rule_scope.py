#!/usr/bin/env python3
"""external_rule_scope.py — W1197：外部规则扫描面的共享识别。

为什么单独抽一个模块
------------------
本仓有两个守卫都需要判定「某个文件是否属于 Scorecard 的 shell 扫描面」：

  scripts/check_install_pins.py   —— 安装命令面（W1197 扩到全仓 shell）
  scripts/check_action_refs.py    —— action 引用面（W1197 扩到全仓 shell）

若两者各写一套识别规则，就会形成「口径分裂」——一个守卫认得是 shell、另一个认不得，
对同一个文件给出相反结论。因此识别规则只有这一份实现。

识别规则（与 OSSF Scorecard 源码同源）
------------------------------------
Scorecard `checks/raw/shell_download_validate.go` 的 `isSupportedShellScriptFile` →
`isMatchingShellScriptFile`：

  1. 文件扩展名属于 shell 家族 → 是 shell 文件（不看内容）
  2. 否则看**首行 shebang**：`#!/bin/bash` / `#!/usr/bin/env bash` 等匹配 shell 家族 → 是
  3. 否则不是

shell 家族（Scorecard `supportedShells` 的等价集）：sh / bash / zsh / ksh / csh / fish / dash / ash

用法
----
  from external_rule_scope import find_shell_files, is_shell_file
  find_shell_files(root)      # 返回仓内 shell 面文件的仓内相对路径（排序后的列表）
  is_shell_file(path, name)   # 单个文件判定
"""
import os
import re

# Scorecard `supportedShells` 的等价集——扩展名与 shebang 两条路径共用
SHELL_FAMILY = ["sh", "bash", "zsh", "ksh", "csh", "fish", "dash", "ash"]

# Scorecard 扫描面是 Pattern:"*"，但仓内不应把归档/构建产物等内容当源码
SKIP_DIRS = {"node_modules", ".git", "archive", "dist", "release", "site",
             "tmpe", "__pycache__", ".venv", "docs", "spark-output"}

_SHEBANG_RE = {s: re.compile((r"(^|[/\s])%s(\s|$)" % s).encode()) for s in SHELL_FAMILY}


def is_shell_file(path, name=None):
    """按 Scorecard 的识别规则判定单个文件是否属于 shell 扫描面。

    规则（与 Scorecard `isMatchingShellScriptFile` 同源）：
      1. 扩展名属于 shell 家族 → 是（不看内容）
      2. 否则看首行 shebang 是否匹配 shell 家族 → 是
      3. 否则不是
    """
    if name is None:
        name = os.path.basename(path)
    if "." in name:
        if name.rsplit(".", 1)[-1].lower() in SHELL_FAMILY:
            return True
    try:
        with open(path, "rb") as fh:
            first = fh.readline(400)
    except OSError:
        return False
    if not first.startswith(b"#!"):
        return False
    for shell in SHELL_FAMILY:
        if _SHEBANG_RE[shell].search(first):
            return True
    return False


def find_shell_files(root, skip_dirs=None):
    """产出仓内属于 Scorecard shell 扫描面的文件（仓内相对路径·排序后的列表）。"""
    skips = SKIP_DIRS if skip_dirs is None else skip_dirs
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skips]
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            if is_shell_file(path, fn):
                out.append(os.path.relpath(path, root).replace(os.sep, "/"))
    return sorted(out)
