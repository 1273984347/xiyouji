#!/usr/bin/env python3
"""Skills 索引一致性门禁（W498 转正，verify_delivery 第 16 门禁）。

背景（W497 教训）：day-review 创建后从未 git add（建了没入库），AGENTS.md §4.5 与
skills/README.md 索引也漏收录——三个 P1 均因"skills 目录无一致性门禁"漏网。

检查项（全通过 exit 0，任一失败 exit 1 阻断提交）：
1. skills/ 目录名集合 == skills/README.md 表格首列集合（索引不遗漏、不多列）
2. skills/ 目录短名集合（去 xiyouji- 前缀）== AGENTS.md §4.5 段出现的 skill 短名集合
3. skills/ 下全部文件均被 git tracked（git ls-files 差集为空，防"建了没 add"）
4. 每个 SKILL.md frontmatter name == 目录名（防目录与标识漂移）

与 scripts/_check_skills.py 分工：后者查 frontmatter 字段/引用/残留（诊断用），
本门禁只查索引与入库一致性（可进 CI，纯仓库内检查，不依赖本机全局目录）。
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
README = SKILLS_DIR / "README.md"
AGENTS = ROOT / "AGENTS.md"

# 目录名 → 短名（AGENTS.md §4.5 用短名列举，如 xiyouji-sun-wukong → sun-wukong）
def short_name(dir_name: str) -> str:
    return dir_name.removeprefix("xiyouji-")


def git_ls_files(rel_dir: str) -> set[str]:
    r = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", rel_dir],
        capture_output=True, text=True, timeout=60,
    )
    if r.returncode != 0:
        raise RuntimeError("git ls-files 失败: %s" % r.stderr.strip()[:200])
    return {ln.strip().replace("\\", "/") for ln in r.stdout.splitlines() if ln.strip()}


def read_frontmatter_name(text: str) -> str:
    m = re.match(r"^---\s*\n(.*?)\n---", text, flags=re.DOTALL)
    if not m:
        return ""
    for line in m.group(1).splitlines():
        fm = re.match(r"^name:\s*(\S+)\s*$", line)
        if fm:
            return fm.group(1)
    return ""


def main() -> int:
    errors: list[str] = []

    dirs = sorted(p.name for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    if not dirs:
        errors.append("skills/ 目录下未发现任何含 SKILL.md 的 skill 目录")
        print("\n".join(errors))
        return 1
    print(f"skills 目录共 {len(dirs)} 个：{', '.join(dirs)}")

    # ---- 检查 1：目录名集合 == README 表格首列集合 ----
    readme_text = README.read_text(encoding="utf-8-sig")
    table_names = set(re.findall(r"^\| ([a-z0-9-]+) \|", readme_text, flags=re.M))
    only_dir = set(dirs) - table_names
    only_rm = table_names - set(dirs)
    if only_dir:
        errors.append(f"README 索引缺 {len(only_dir)} 个 skill：{sorted(only_dir)}")
    if only_rm:
        errors.append(f"README 索引多列 {len(only_rm)} 个：{sorted(only_rm)}")
    print(f"检查1 README 表格行数 {len(table_names)} vs 目录 {len(dirs)}：{'一致' if not only_dir and not only_rm else '不一致'}")

    # ---- 检查 2：目录短名集合 ⊆ AGENTS.md §4.5 段文本（每个 skill 都必须被提及）----
    agents_text = AGENTS.read_text(encoding="utf-8-sig")
    m45 = re.search(r"### 4\.5 项目级 Skills（skills/）(.*?)(?:\n### 4\.6|\Z)", agents_text, flags=re.DOTALL)
    sec45 = m45.group(1) if m45 else ""
    if not sec45:
        errors.append("AGENTS.md §4.5 段未找到")
    else:
        dir_short = {short_name(d) for d in dirs}
        missing_in_agents = sorted(d for d in dir_short if d not in sec45)
        if missing_in_agents:
            errors.append(f"AGENTS.md §4.5 未提及 {len(missing_in_agents)} 个 skill：{missing_in_agents}")
        print(f"检查2 AGENTS §4.5 提及 {len(dir_short) - len(missing_in_agents)}/{len(dir_short)}：{'全提及' if not missing_in_agents else '有遗漏'}")

    # ---- 检查 3：skills/ 下全部文件均 git tracked ----
    tracked = git_ls_files("skills/")
    on_disk = set()
    for p in SKILLS_DIR.rglob("*"):
        if p.is_file():
            on_disk.add(p.relative_to(ROOT).as_posix())
    untracked = sorted(on_disk - tracked)
    if untracked:
        errors.append(f"skills/ 下 {len(untracked)} 个文件未 git tracked（建了没 add）：{untracked}")
    print(f"检查3 git tracked {len(tracked)} vs 磁盘 {len(on_disk)}：{'全入库' if not untracked else '有未跟踪'}")

    # ---- 检查 4：frontmatter name == 目录名 ----
    for d in dirs:
        name = read_frontmatter_name((SKILLS_DIR / d / "SKILL.md").read_text(encoding="utf-8-sig"))
        if name != d:
            errors.append(f"{d}: frontmatter name '{name}' != 目录名 '{d}'")
    print(f"检查4 frontmatter name 与目录名：{'全一致' if not errors or not any('name' in e for e in errors) else '有不一致'}")

    if errors:
        print(f"\n发现 {len(errors)} 个问题：")
        for e in errors:
            print("  - " + e)
        return 1
    print("Skills 索引一致性门禁通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
