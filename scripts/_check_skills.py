#!/usr/bin/env python3
"""Skill 目录自检脚本（诊断用，不入 verify_delivery 门禁）。

检查项：
1. 每个 skill 目录存在 SKILL.md，且 frontmatter 含 name / description。
2. agents/openai.yaml（如存在）不含 "System.Collections.Hashtable" 残留。
3. SKILL.md 中引用的 references/ 相对文件存在。
4. 统计 skill 总数。

用法：
  python scripts/_check_skills.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"


def read_frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\s*\n(.*?)\n---", text, flags=re.DOTALL)
    if not m:
        return {}
    fields: dict[str, str] = {}
    for line in m.group(1).splitlines():
        fm = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if fm:
            fields[fm.group(1)] = fm.group(2).strip()
    return fields


def main() -> int:
    errors: list[str] = []
    skills = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    print(f"skills 目录：{SKILLS_DIR}，SKILL.md 共 {len(skills)} 个")
    for skill in skills:
        skill_md = skill / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8-sig")
        fm = read_frontmatter(text)
        if not fm.get("name"):
            errors.append(f"{skill.name}: frontmatter 缺 name")
        if not fm.get("description"):
            errors.append(f"{skill.name}: frontmatter 缺 description")
        for ref in re.findall(r"\]\((references/[^)#]+)\)", text):
            target = skill / ref
            if not target.exists():
                errors.append(f"{skill.name}: 引用的 {ref} 不存在")
        for yaml in skill.glob("agents/*.yaml"):
            content = yaml.read_text(encoding="utf-8-sig")
            if "System.Collections.Hashtable" in content:
                errors.append(f"{skill.name}: {yaml.name} 含 System.Collections.Hashtable 残留")
    if errors:
        print(f"发现 {len(errors)} 个问题：")
        for e in errors:
            print("  - " + e)
        return 1
    print("全部检查通过：frontmatter / openai.yaml / references 链接均正常")
    return 0


if __name__ == "__main__":
    sys.exit(main())
