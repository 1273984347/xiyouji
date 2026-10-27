#!/usr/bin/env python3
"""check_archive_health.py — 归档区健康探针（W994 建·报告型 exit 0）。

背景（W824 定律再实证）：文档规范 §11.2 的「归档件超 1MB → 二级归档」自 W513 执行一次后
掉档——W994 体检实测 CHANGELOG-ARCHIVE 1198KB / file-index-ARCHIVE 1070KB 双双破线零反应。
本探针把三条纯文字条款机器化：
  T1 tier-2 判距：一级归档件 vs 1MB（§11.2）——≥800KB WARN·破线 ⚠（修法=archive_tier2.py）
  T2 归档 scripts 台账对账：顶层散件须有单件行；batches/ 段目录须有组行覆盖（archive/README.md）
  T3 冷存储语义标注：batches/README.md 须含冷存储/禁运行警告（W836 教训：归档件 ROOT 上溯
     失效·直接运行会错——无标注则后来者可能误跑）
  T4 汇总：归档区 tracked 体积/件数

用法：
  py -3 scripts/check_archive_health.py            # 报告（exit 0·破线行 ⚠ 前缀）
  py -3 scripts/check_archive_health.py --strict   # 破线/缺标注 exit 1（门禁候选）
  py -3 scripts/check_archive_health.py --self-test
"""
from __future__ import annotations

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LIMIT = 1024 * 1024          # §11.2 一级归档 1MB 线
WARN = 800 * 1024            # 判距预警线（80%）
T1_FILES = (
    "CHANGELOG-ARCHIVE.md",
    "file-index-ARCHIVE.md",
    "HANDOVER-ARCHIVE.md",
    "AGENTS-ARCHIVE.md",
    "STRUCTURE-ARCHIVE.md",
    "W批次编号对账表-ARCHIVE.md",
)
COLD_MARKS = ("冷存储", "禁运行", "不可直接运行", "ROOT 上溯")
BATCHES_SEG = ("misc", "w4xx", "w5xx", "w6xx", "w7xx", "w8xx", "w9xx")


def _kb(n: int) -> str:
    return "%.0fKB" % (n / 1024)


def t1_sizes(arch_dir):
    """T1：一级归档件体积 → [(名, 字节, 超线?, 预警?)]（纯函数·供单测）。"""
    rows = []
    for name in T1_FILES:
        p = os.path.join(arch_dir, name)
        size = os.path.getsize(p) if os.path.exists(p) else -1
        rows.append((name, size, size > LIMIT, WARN <= size <= LIMIT))
    return rows


def t2_coverage(tracked, readme_text):
    r"""T2：归档 scripts 台账对账（纯函数·W994 语义：组行/计数对账而非逐件行——
    W735 存量 200+ 件从未逐件登记是既定形态，逐件检查会误报风暴）。

    tracked = archive/scripts/ 下全部 tracked 相对路径（repo 根相对·posix）。
    检查三面：
      ① 顶层文件（depth-1）：README 须有顶层存量组行 `| \`archive/scripts/\`（顶层存量 +N 件）`
         且 N == 磁盘实数（计数漂移即报）；
      ② 子目录（attic/audit/review-pass3 等）：README 须提及 `archive/scripts/<dir>`；
      ③ batches/<段>/：README 须有 `archive/scripts/batches/<段>` 组行或结构树提及。
    返回 dict(top_disk, top_row, subdirs_missing, segs_missing)。
    """
    top, subdirs, segs = [], set(), set()
    for rel in tracked:
        rest = rel[len("archive/scripts/"):]
        if rest.startswith("batches/"):
            parts = rest.split("/")
            if len(parts) >= 3 and parts[1]:
                segs.add(parts[1])  # batches/<段>/<文件> 才算段成员；batches 自身 README/index 不算
        elif "/" in rest:
            subdirs.add(rest.split("/", 1)[0])
        elif rest:
            top.append(rest)
    m = re.search(r"\|\s*`archive/scripts/`（顶层存量 \+(\d+) 件）", readme_text)
    top_row = int(m.group(1)) if m else None
    subdirs_missing = sorted(d for d in subdirs if (d + "/") not in readme_text
                             and ("archive/scripts/%s" % d) not in readme_text)
    segs_missing = sorted(s for s in segs
                          if ("batches/%s" % s) not in readme_text)
    return {"top_disk": len(top), "top_row": top_row,
            "subdirs_missing": subdirs_missing, "segs_missing": segs_missing}


def t3_cold_warning(readme_text):
    return any(m in readme_text for m in COLD_MARKS)


def run(strict=False):
    import tracked_files as tf

    lines, problems = [], []
    arch = os.path.join(ROOT, "archive")

    # T1
    for name, size, over, warn in t1_sizes(arch and os.path.join(arch, "docs")):
        if size < 0:
            continue
        mark = ""
        if over:
            mark = "  ⚠ 破 1MB 线——修法=py -3 scripts/archive_tier2.py"
            problems.append("T1 %s %s 破线" % (name, _kb(size)))
        elif warn:
            # 判距预警只标记不入 problems——W994 review 修正：回线后两件常驻 800KB+ 预警带，
            # strict 若判红则门禁候选永红（语义对齐 docstring「破线/缺标注 exit 1」）
            mark = "  (判距预警 ≥800KB)"
        lines.append("T1  %-38s %8s%s" % (name, _kb(size), mark))
    # T1b：tier2 容器体积报告（§11.2 无 tier-3 形态·>1MB 打「登记观察」浮出待政策）
    for name in sorted(os.listdir(os.path.join(arch, "docs"))):
        if not name.endswith("-tier2.md"):
            continue
        p = os.path.join(arch, "docs", name)
        size = os.path.getsize(p)
        note = "  ⚠ 破 1MB——§11.2 无 tier-3 形态·登记观察（容器只增不删·待政策定夺）" if size > LIMIT else ""
        lines.append("T1b %-38s %8s%s" % (name, _kb(size), note))

    # T2
    tracked = sorted(r.replace(os.sep, "/") for r in tf.tracked_files()
                     if r.replace(os.sep, "/").startswith("archive/scripts/"))
    readme_p = os.path.join(arch, "README.md")
    readme = open(readme_p, encoding="utf-8", errors="replace").read() if os.path.exists(readme_p) else ""
    cov = t2_coverage(tracked, readme)
    if cov["top_row"] is None:
        problems.append("T2 顶层存量组行缺失")
        lines.append("T2  ⚠ 顶层存量组行缺失（磁盘 %d 件）——修法=archive/README.md 台账补 `archive/scripts/`（顶层存量 +N 件）行" % cov["top_disk"])
    elif cov["top_row"] != cov["top_disk"]:
        problems.append("T2 顶层计数漂移：台账 %d ≠ 磁盘 %d" % (cov["top_row"], cov["top_disk"]))
        lines.append("T2  ⚠ 顶层计数漂移：台账 + %d 件 ≠ 磁盘 %d 件——修法=更新顶层组行计数" % (cov["top_row"], cov["top_disk"]))
    else:
        lines.append("T2  顶层存量对账一致（%d 件）·子目录缺 %s·段目录缺 %s"
                     % (cov["top_disk"], cov["subdirs_missing"] or "无", cov["segs_missing"] or "无"))
    if cov["subdirs_missing"]:
        problems.append("T2 子目录未登记：%s" % cov["subdirs_missing"])
        lines.append("T2  ⚠ 子目录缺结构树/台账提及：%s" % "、".join(cov["subdirs_missing"]))
    if cov["segs_missing"]:
        problems.append("T2 段目录缺组行：%s" % cov["segs_missing"])
        lines.append("T2  ⚠ 段目录缺组行：%s" % "、".join(cov["segs_missing"]))

    # T3
    batches_readme = os.path.join(arch, "scripts", "batches", "README.md")
    btxt = open(batches_readme, encoding="utf-8", errors="replace").read() if os.path.exists(batches_readme) else ""
    if t3_cold_warning(btxt):
        lines.append("T3  冷存储/禁运行警告在位（batches/README.md）")
    else:
        problems.append("T3 batches/README 缺冷存储警告")
        lines.append("T3  ⚠ batches/README.md 缺冷存储/禁运行警告（W836：归档件 ROOT 上溯失效·误跑会错）")

    # T4
    total = sum(os.path.getsize(os.path.join(dp, f))
                for dp, _dn, fs in os.walk(arch) for f in fs) if os.path.isdir(arch) else 0
    lines.append("T4  归档区合计 %s（tracked %d 件·archive/scripts 下）" % (_kb(total), len(tracked)))

    for ln in lines:
        print(ln)
    print("---- 归档健康探针：%d 项待办（报告型·修法见各行）----" % len(problems))
    if strict and problems:
        return 1
    return 0


def _self_test() -> int:
    import tempfile

    fails = []
    # t1_sizes：超线/预警/正常
    td = tempfile.mkdtemp()
    for name, kb in (("CHANGELOG-ARCHIVE.md", 1100), ("file-index-ARCHIVE.md", 850), ("AGENTS-ARCHIVE.md", 10)):
        open(os.path.join(td, name), "wb").write(b"x" * (kb * 1024))
    rows = dict((n, (s, o, w)) for n, s, o, w in t1_sizes(td))
    if (not rows["CHANGELOG-ARCHIVE.md"][1]) or (not rows["file-index-ARCHIVE.md"][2]) or rows["AGENTS-ARCHIVE.md"][1]:
        fails.append("T1 判定错")
    # t2_coverage：顶层计数对账/子目录/段目录
    tracked = ["archive/scripts/_old_a.py", "archive/scripts/legacy.py",
               "archive/scripts/attic/x.py", "archive/scripts/batches/w9xx/_b.py"]
    readme = ("| `archive/scripts/`（顶层存量 +2 件） | … | W | d | r |\n"
              "结构树提及 archive/scripts/attic 与 archive/scripts/batches/w9xx 组行")
    cov = t2_coverage(tracked, readme)
    if cov["top_disk"] != 2 or cov["top_row"] != 2 or cov["subdirs_missing"] or cov["segs_missing"]:
        fails.append("T2 齐备态判定错：%s" % cov)
    cov2 = t2_coverage(tracked + ["archive/scripts/new_orphan.py"], readme)
    if cov2["top_row"] != 2 or cov2["top_disk"] != 3:
        fails.append("T2 计数漂移判定错：%s" % cov2)
    cov3 = t2_coverage(tracked, readme.replace("batches/w9xx", "batches/w8xx"))
    if cov3["segs_missing"] != ["w9xx"]:
        fails.append("T2 段缺组行判定错：%s" % cov3)
    # t3
    if t3_cold_warning("无警告文本") or not t3_cold_warning("本目录为冷存储·禁运行"):
        fails.append("T3 判定错")
    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：tier-2 判距/orphan/冷存储判定（判据可证伪）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="归档区健康探针（W994·报告型）")
    ap.add_argument("--strict", action="store_true", help="破线/缺标注 exit 1（门禁候选）")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    return run(strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())
