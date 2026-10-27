"""W757 一次性级联：docs/11-报告复盘 → docs/11-方案报告 现役面引用替换。

范围纪律：只改**现役面**（工具脚本/索引生成器/现役治理文档/新目录自身）与**断链**；
CHANGELOG 历史段、archive/ 冻结档、报告正文中的历史性叙述（如「W737 新建 docs/11-报告复盘/」）
一律不动——历史事实不可改。

两类改动分别处理：
  A 目录改名：`11-报告复盘` → `11-方案报告`（白名单内文件全部出现均指该目录）
  B 相对深度：报告下移一级后 `../` 需补一层（仅 2026-10-13.md 存在跨目录链接）
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# A 类：目录改名（白名单=现役面文件）
RENAME_FILES = [
    "docs/10-方法论沉淀/README.md",
    "docs/10-方法论沉淀/多Agent干扰治理与touches纪律.md",
    "docs/10-方法论沉淀/治理文档分层与按需查表.md",
    "docs/00-导读/文档规范.md",
]

OLD, NEW = "11-报告复盘", "11-方案报告"

# B 类：相对深度修正（文件 → [(旧, 新, 期望次数)]）
DEPTH_JOBS = [
    ("docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-13.md", [
        ("(../10-方法论沉淀/README.md)", "(../../10-方法论沉淀/README.md)", 1),
        ("(../../CHANGELOG.md)", "(../../../CHANGELOG.md)", 1),
        ("(../../HANDOVER.md)", "(../../../HANDOVER.md)", 1),
        ("(../../archive/README.md)", "(../../../archive/README.md)", 1),
        ("(../../scripts/batch_cascade.py)", "(../../../scripts/batch_cascade.py)", 1),
        ("(../00-导读/W批次编号对账表.md)", "(../../00-导读/W批次编号对账表.md)", 1),
    ]),
]


def main():
    total_a = 0
    for rel in RENAME_FILES:
        p = ROOT / rel
        s = p.read_text(encoding="utf-8")
        n = s.count(OLD)
        assert n > 0, "%s: 未找到 %r（白名单失效？）" % (rel, OLD)
        p.write_text(s.replace(OLD, NEW), encoding="utf-8")
        total_a += n
        print("A  %-62s %d 处" % (rel, n))

    total_b = 0
    for rel, subs in DEPTH_JOBS:
        p = ROOT / rel
        s = p.read_text(encoding="utf-8")
        for old, new, expect in subs:
            got = s.count(old)
            assert got == expect, "%s: 期望 %d 处 %r，实得 %d" % (rel, expect, old, got)
            s = s.replace(old, new)
            total_b += got
        p.write_text(s, encoding="utf-8")
        print("B  %-62s %d 处" % (rel, len(subs)))

    print("合计：A %d 处 + B %d 处" % (total_a, total_b))


if __name__ == "__main__":
    main()
