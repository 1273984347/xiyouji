#!/usr/bin/env python3
"""仓库版 skills/ ↔ 全局安装版 ~/.qwenworkcn/skills/ 双向比对与同步工具（本地用，不入 CI）。

背景（W497 教训）：仓库版与全局安装版是独立副本，W478/W488 视觉批次演进只进全局版、
仓库 visual-batch 停 v1.0.0——两份真源无强制一致机制。本工具约定**仓库版为唯一真源**，
全局版只是部署副本，收尾时同步方向恒为 仓库 → 全局。

用法：
  python scripts/sync_skills.py --check   # 只比对，列出漂移清单（exit 0=无漂移，1=有漂移）
  python scripts/sync_skills.py --sync    # 仓库 → 全局 单向复制 + 覆盖后验证（输出 diff 前后对照）

与 check_skills_index.py 分工：后者是 CI 门禁（纯仓库内检查）；本工具比对仓库与全局，
依赖本机路径，仅本地跑。改任何 skill 后（含新增）收尾时运行 --sync。
"""

from __future__ import annotations

import argparse
import difflib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
GLOBAL_SKILLS = Path.home() / ".qwenworkcn" / "skills"


def repo_skill_files(skill_dir: Path) -> dict[str, Path]:
    """返回相对路径 → 仓库文件绝对路径 映射（含隐藏文件，如 .skill-metadata.yaml）。"""
    out: dict[str, Path] = {}
    for p in skill_dir.rglob("*"):
        if p.is_file():
            out[p.relative_to(skill_dir).as_posix()] = p
    return out


def collect() -> list[tuple[str, dict[str, Path], Path | None]]:
    """返回 [(skill 名, 仓库文件表, 全局目录或 None)]，覆盖仓库有/全局有两侧。"""
    items: list[tuple[str, dict[str, Path], Path | None]] = []
    repo_dirs = {p.name: p for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").exists()}
    global_dirs = {p.name: p for p in GLOBAL_SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").exists()} if GLOBAL_SKILLS.exists() else {}

    for name in sorted(set(repo_dirs) | set(global_dirs)):
        # 只处理仓库 skill 与全局 xiyouji-*（QwenWork 内置/其他项目 skill 如 docx/pdf 不在同步范围）
        if name not in repo_dirs and not name.startswith("xiyouji-"):
            continue
        repo_files = repo_skill_files(repo_dirs[name]) if name in repo_dirs else {}
        items.append((name, repo_files, global_dirs.get(name)))
    return items


def diff_file(global_path: Path, repo_path: Path) -> list[str]:
    gl = global_path.read_text(encoding="utf-8-sig").splitlines() if global_path.exists() else []
    rp = repo_path.read_text(encoding="utf-8-sig").splitlines()
    return list(difflib.unified_diff(gl, rp, fromfile=f"global:{global_path.name}", tofile=f"repo:{repo_path.name}", lineterm=""))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="只比对列漂移")
    ap.add_argument("--sync", action="store_true", help="仓库→全局单向复制")
    args = ap.parse_args()
    if not (args.check or args.sync):
        ap.error("必须指定 --check 或 --sync")

    if not GLOBAL_SKILLS.exists():
        print(f"全局 skills 目录不存在：{GLOBAL_SKILLS}")
        return 2

    drift: list[str] = []
    for name, repo_files, global_dir in collect():
        # 全局有、仓库无 → 孤儿
        if not repo_files:
            drift.append(f"[孤儿] 全局有 {name}/ 但仓库无（全局独有内容，仓库为真源时视为遗留）")
            continue
        # 仓库有、全局无 → 全新
        if global_dir is None:
            drift.append(f"[缺失] 仓库有 {name}/ 但全局无（--sync 将新建）")
            continue
        for rel, repo_path in sorted(repo_files.items()):
            gpath = global_dir / rel
            if not gpath.exists():
                drift.append(f"[缺文件] {name}/{rel} 全局缺失")
                continue
            if gpath.read_bytes() != repo_path.read_bytes():
                drift.append(f"[不同] {name}/{rel}")
                for line in diff_file(gpath, repo_path)[:8]:
                    drift.append("    " + line)

    if args.check:
        if drift:
            print(f"检测到 {len(drift)} 处漂移：")
            print("\n".join(drift))
            print("\n运行 `python scripts/sync_skills.py --sync` 将仓库版同步到全局版。")
            return 1
        print("仓库版与全局版完全一致，无漂移。")
        return 0

    # --sync：仓库 → 全局
    synced = 0
    for name, repo_files, global_dir in collect():
        if not repo_files:
            print(f"跳过孤儿 {name}/（全局独有，不动）")
            continue
        target = global_dir if global_dir is not None else GLOBAL_SKILLS / name
        target.mkdir(parents=True, exist_ok=True)
        for rel, repo_path in sorted(repo_files.items()):
            gpath = target / rel
            gpath.parent.mkdir(parents=True, exist_ok=True)
            if not gpath.exists() or gpath.read_bytes() != repo_path.read_bytes():
                shutil.copy2(repo_path, gpath)
                synced += 1
                print(f"同步 {name}/{rel}")
    print(f"\n同步完成：{synced} 个文件更新（仓库为真源）。")
    # 同步后自检
    import subprocess
    r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--check"], capture_output=True, text=True)
    print(r.stdout.strip())
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
