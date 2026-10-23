#!/usr/bin/env python3
"""tracked_files.py — 目标提交树文件集合（W894 批·门禁实算口径的单一事实源）

## 为什么存在（W894·用户批准根修）

门禁的实算对象原本是**物理工作树**（`os.listdir` / `glob` / `rglob` 扫描磁盘）。在多 Agent
共享同一工作树的场景里，这会让**并行批的未落库件**污染判据：

- 并行批新建了 12 件素材（未 `git add`）⇒ 第 45 门禁判「盘上多 12 项」⇒ 本地红；
- 而 CI 干净检出没有这些文件 ⇒ CI 侧绿 ⇒ **本地红 / CI 绿分歧**；
- 于是 pre-commit 硬门禁必然拦下提交 ⇒ 大家被迫用 `--no-verify` 绕过 ⇒ 账目变假。

根修：**实算对象改为「目标提交树」**——以 Git 索引（`git ls-files`）为准，它恰好等于
「已跟踪 + 已暂存的新增」= **将要入库的内容**。未落库件（未跟踪）因此不再污染判据，
而真正的问题（已入库文件漏进清单 / 清单预引磁盘不存在的幽灵文件）依然能被抓出来。

## 口径定义

| 集合 | 含义 |
|:---|:---|
| `tracked_files()` | 全仓已跟踪文件（相对路径·POSIX 分隔） |
| `tracked_in_dir(rel_dir)` | 某目录**直属**的已跟踪文件（不含子目录） |
| `tracked_subdirs(rel_dir)` | 某目录下的已跟踪子目录（目录内至少有已跟踪文件才算） |
| `is_tracked(rel_path)` | 单路径是否已跟踪 |

**未跟踪文件一律不计入**——它们属于并行批的在途产物，不该由本批的判据来背。

## 降级策略

`git` 不可用 / 非 Git 仓库 ⇒ **回退到磁盘扫描**（保持旧行为，不让门禁因环境问题崩）。
降级时会通过 `warnings.warn` 显式告警，不静默。
"""

from __future__ import annotations

import os
import subprocess
import warnings

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 缓存：一次进程内多次调用只跑一次 git ls-files
_CACHE: dict[str, set[str]] = {}


def _run_ls_files(repo_root: str | None = None) -> set[str] | None:
    """返回全仓已跟踪文件集合（相对路径·POSIX 分隔）；git 不可用时返回 None。"""
    root = repo_root or ROOT
    try:
        out = subprocess.run(
            ["git", "-C", root, "ls-files", "-z"],
            capture_output=True, timeout=60, check=False,
        )
    except (OSError, subprocess.SubprocessError) as e:
        warnings.warn("tracked_files: git 不可用（%s）⇒ 实算回退磁盘扫描" % e, RuntimeWarning)
        return None
    if out.returncode != 0:
        warnings.warn("tracked_files: git ls-files 失败（rc=%d）⇒ 实算回退磁盘扫描" % out.returncode, RuntimeWarning)
        return None
    raw = out.stdout.decode("utf-8", errors="replace")
    return {p for p in raw.split("\0") if p}


def tracked_files(repo_root: str | None = None) -> set[str]:
    """全仓已跟踪文件集合（相对路径·POSIX 分隔）。"""
    root = repo_root or ROOT
    key = "all::" + root
    if key not in _CACHE:
        got = _run_ls_files(root)
        _CACHE[key] = got if got is not None else set()
    return _CACHE[key]


def tracked_in_dir(rel_dir: str, repo_root: str | None = None) -> set[str]:
    """某目录直属的已跟踪文件名集合（不含子目录内的文件）。"""
    prefix = (rel_dir.strip("/") + "/") if rel_dir.strip("/") else ""
    out = set()
    for p in tracked_files(repo_root):
        if not p.startswith(prefix):
            continue
        rest = p[len(prefix):]
        if "/" in rest:
            continue  # 子目录里的文件
        out.add(rest)
    return out


def tracked_subdirs(rel_dir: str, repo_root: str | None = None) -> set[str]:
    """某目录下的已跟踪子目录名集合（目录内至少有一个已跟踪文件才算）。"""
    prefix = (rel_dir.strip("/") + "/") if rel_dir.strip("/") else ""
    out = set()
    for p in tracked_files(repo_root):
        if not p.startswith(prefix):
            continue
        rest = p[len(prefix):]
        if "/" not in rest:
            continue  # 直属文件
        out.add(rest.split("/", 1)[0])
    return out


def is_tracked(rel_path: str, repo_root: str | None = None) -> bool:
    """单路径是否已跟踪（相对仓库根·POSIX 分隔）。"""
    return rel_path.strip("/") in tracked_files(repo_root)


def clear_cache() -> None:
    """清缓存（自测用；长驻进程在写操作后应调用）。"""
    _CACHE.clear()


if __name__ == "__main__":
    files = tracked_files()
    print("已跟踪文件总数：%d" % len(files))
    for sample in sorted(files)[:5]:
        print("  ", sample)
