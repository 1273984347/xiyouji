#!/usr/bin/env python3
"""
pre-commit-validate.py — E3 收尾文档同步铁律·自动化校验门禁

校验三项一致性，任一失败则阻断 commit（返回非零退出码）：
1. 版本号一致性：从 CHANGELOG.md 提取最新版本号，校验 6 个必检文档是否都包含
2. 文件计数一致性：从 README.md 头部解析期望计数，与实际目录 .md 文件数对比
3. 声明计数一致性：README / STRUCTURE / 项目说明.md 三文档头部声明数是否一致

用法：
    py -3 scripts/pre-commit-validate.py          # 完整校验
    py -3 scripts/pre-commit-validate.py --quiet   # 只输出错误

配合 .git/hooks/pre-commit 钩子自动调用，见脚本末尾安装说明。
"""

import re
import sys
from pathlib import Path

# 项目根目录（本脚本位于 scripts/ 下）
ROOT = Path(__file__).resolve().parent.parent

# E3 铁律规定的 6 个必检文档（相对项目根目录）
DOCS = [
    "CHANGELOG.md",
    "README.md",
    "STRUCTURE.md",
    "docs/00-导读/项目说明.md",
    "交接文档.md",
    "scripts/output/file-index.md",
]

# 文件计数校验配置：(目录相对路径, README 头部声明正则, 描述)
COUNT_SPECS = [
    ("docs/01-全书逐回解读", r"A1 逐回\s*(\d+)\s*回", "A1 逐回解读"),
    ("docs/06-个人随笔", r"A2 随笔\s*(\d+)\s*篇", "A2 个人随笔"),
    ("docs/02-人物深度分析", r"A3 人物深化\s*(\d+)\s*篇", "A3 人物深化"),
    ("docs/03-主题与情节专题", r"A4 主题专题\s*(\d+)\s*篇", "A4 主题专题"),
    ("docs/04-文化与历史背景", r"A5 文化\s*(\d+)\s*篇", "A5 文化背景"),
    ("docs/05-诗词歌赋", r"A6 诗词\s*(\d+)\s*篇", "A6 诗词"),
]

# 排除的索引/合集文件名（不计入内容计数）
# 如需追加，在此集合添加文件名即可
EXCLUDE_FILES = {
    "README.md",
    "现代视角解读.md",  # A2 合集文件（含 3 篇，不计入 43 篇独立随笔）
}

# CHANGELOG.md 中提取最新版本号的正则（首个 ### vX.Y.Z 段，兼容全角/半角括号）
VERSION_RE = re.compile(r"###\s+(v\d+\.\d+\.\d+[a-z]?)\s*[（(]")

errors = []
warnings = []
quiet = False


def log(msg):
    if not quiet:
        print(msg)


def read_text(rel_path):
    p = ROOT / rel_path
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8")


def extract_latest_version(changelog_text):
    """从 CHANGELOG.md 提取最新版本号（首个 ### vX.Y.Z 段）"""
    m = VERSION_RE.search(changelog_text)
    return m.group(1) if m else None


def extract_expected_counts(text):
    """从文档头部解析期望文件计数（A1-A6）"""
    expected = {}
    for _, pattern, desc in COUNT_SPECS:
        m = re.search(pattern, text)
        if m:
            expected[desc] = int(m.group(1))
    return expected


def count_md_files(dir_rel):
    """统计目录下的 .md 文件数（排除 EXCLUDE_FILES）"""
    d = ROOT / dir_rel
    if not d.exists():
        return None
    return sum(1 for f in d.glob("*.md") if f.name not in EXCLUDE_FILES)


def check_version_consistency(expected_version):
    """校验 6 文档是否都包含期望版本号"""
    for doc in DOCS:
        content = read_text(doc)
        if content is None:
            errors.append(f"[缺失] 文档不存在: {doc}")
            continue
        if expected_version and expected_version not in content:
            errors.append(f"[版本号] {doc} 缺少 {expected_version}")


def check_file_counts(expected_counts):
    """校验实际文件计数与 README 声明期望值"""
    for dir_rel, _, desc in COUNT_SPECS:
        if desc not in expected_counts:
            continue
        expected = expected_counts[desc]
        actual = count_md_files(dir_rel)
        if actual is None:
            errors.append(f"[计数] 目录不存在: {dir_rel}（{desc}）")
        elif actual != expected:
            errors.append(
                f"[计数] {desc}: {dir_rel} 实际 {actual} 篇，"
                f"README 声明 {expected} 篇"
            )


def check_declared_counts_consistency(readme_counts):
    """校验 README / STRUCTURE / 项目说明.md 三文档头部声明数是否一致"""
    others = [
        ("STRUCTURE.md", "STRUCTURE.md"),
        ("docs/00-导读/项目说明.md", "项目说明.md"),
    ]
    for rel, name in others:
        content = read_text(rel)
        if content is None:
            continue
        other_counts = extract_expected_counts(content)
        for desc, expected in readme_counts.items():
            if desc in other_counts and other_counts[desc] != expected:
                errors.append(
                    f"[声明计数] {name} 的 {desc} 声明 "
                    f"{other_counts[desc]}，与 README.md 的 {expected} 不一致"
                )


def main():
    global quiet
    if "--quiet" in sys.argv:
        quiet = True

    log("=" * 60)
    log("E3 收尾文档同步铁律·pre-commit 自动化校验")
    log("=" * 60)

    # 基准源 1：CHANGELOG.md 提取版本号
    changelog = read_text("CHANGELOG.md")
    if changelog is None:
        print("✗ CHANGELOG.md 不存在，无法提取基准版本号")
        sys.exit(2)
    expected_version = extract_latest_version(changelog)
    log(f"\n基准版本号（CHANGELOG.md）: {expected_version or '未找到'}")

    # 基准源 2：README.md 提取期望文件计数
    readme = read_text("README.md")
    if readme is None:
        print("✗ README.md 不存在，无法提取期望计数")
        sys.exit(2)
    expected_counts = extract_expected_counts(readme)
    log("期望文件计数（README.md 头部）:")
    for desc, c in expected_counts.items():
        log(f"  {desc}: {c}")

    # 三项校验
    log("\n[1/3] 校验 6 文档版本号一致性...")
    check_version_consistency(expected_version)

    log("[2/3] 校验文件计数一致性（README 声明 vs 实际目录）...")
    check_file_counts(expected_counts)

    log("[3/3] 校验声明计数一致性（README vs STRUCTURE vs 项目说明）...")
    check_declared_counts_consistency(expected_counts)

    # 结果输出
    log("\n" + "-" * 60)
    if errors:
        print(f"✗ 校验失败: {len(errors)} 个错误")
        for e in errors:
            print(f"  - {e}")
        print("\n阻断 commit。请修复以上问题后再提交。")
        print("必检 6 文档: CHANGELOG / README / STRUCTURE / 项目说明 / 交接文档 / file-index")
        print("提示: 文件计数不一致时，二选一处理：")
        print("  (a) 修改 README 头部声明数以匹配实际")
        print("  (b) 检查目录是否缺文件或多文件")
        sys.exit(1)
    if warnings:
        print(f"⚠ 警告: {len(warnings)} 个")
        for w in warnings:
            print(f"  - {w}")
    log("✓ 校验通过")
    sys.exit(0)


if __name__ == "__main__":
    main()


# =============================================================================
# 安装说明（一次性配置）
# =============================================================================
#
# 1. 创建 Git pre-commit 钩子文件: .git/hooks/pre-commit
# 2. 写入以下内容（Windows 用 sh 兼容写法）:
#
#    #!/bin/sh
#    py -3 scripts/pre-commit-validate.py --quiet
#
# 3. 赋予执行权限（Git Bash 中）: chmod +x .git/hooks/pre-commit
#
# 之后每次 git commit 前会自动校验，不一致则阻断提交。
# 如需临时跳过（不推荐）: git commit --no-verify
