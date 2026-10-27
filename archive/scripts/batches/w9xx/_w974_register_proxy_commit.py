# -*- coding: utf-8 -*-
"""_w974_register_proxy_commit.py — 并发登记（代他人 staged 生成件入库）

事实：会话开始时 `scripts/index.md` 已在索引中处于 staged 状态（**非本批产出**·属此前会话遗留）。
本批的 `gen_folder_docs.py --refresh` 按当前 Git 索引重算目录生成件 ⇒ 该文件的工作树版被刷新为
「411 → 431 篇」（新增 20 个本批 `_w974_*.py` 脚本）。收口提交时按显式 pathspec 把它一并入库
⇒ **该文件是「代他人 staged 面」入库**：内容正确（生成件·反映本批全量），但归属方并非本批原创。

登记动作：
  ① 台账 W974 行的 touches 列追加 `scripts/index.md`（如实登记共享面实情）
  ② 收官报告追加「并发登记」小节（事实 + 处置 + 影响评估）

两处均为共享面 ⇒ 以 HEAD 为基底精确暂存。
用法：py -3 scripts/_w974_register_proxy_commit.py [--dry-run]
"""
import io
import os
import subprocess
import sys

REPO = r"D:\xiyouji"
LEDGER_REL = "docs/00-导读/W批次编号对账表.md"
REPORT_REL = "docs/11-方案报告/计划方案/T29-任务计划执行与经验沉淀报告-2026-10-27.md"

REPORT_SEG = """
### 12.7 并发登记（代他人 staged 生成件入库）

| 事项 | 事实 | 处置 | 影响评估 |
|---|---|---|---|
| `scripts/index.md` 属**他人 staged 面** | 会话开始时该文件已在索引中处于 staged 状态（非本批产出）；本批 `gen_folder_docs.py --refresh` 按当前 Git 索引重算目录生成件 ⇒ 其工作树版被刷新为「411 → 431 篇」（新增 20 个本批 `_w974_*.py` 脚本） | 收口提交按显式 pathspec 将其一并入库 ⇒ **如实登记为「代他人 staged 面入库」**；内容为生成件、反映本批全量，无语义改动 | 低：文件是目录索引生成件（按 Git 索引机械生成）·无语义风险；若原 staged 方另有改动意图，以其后续提交为准 |

**其余共享面（台账 / CHANGELOG / README / HANDOVER / file-index / 报告 README / STRUCTURE /
两份架构方案 / CITATION.cff / `.github/workflows/README.md`）一律按内容粒度精确暂存**
（`git update-index --cacheinfo`·HEAD 基底叠加本批段）⇒ 并行会话在途内容既不入本批提交、也不被抹掉。
"""


def git_show(rel):
    p = subprocess.run(["git", "show", "HEAD:" + rel], cwd=REPO, capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout.decode("utf-8").replace("\r\n", "\n")


def write_atomic(rel, text):
    p = os.path.join(REPO, rel.replace("/", os.sep))
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    tmp = p + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(text.replace("\n", nl).encode("utf-8"))
    os.replace(tmp, p)


def stage_exact(rel, text):
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO,
                          input=text.encode("utf-8"), capture_output=True)
    if blob.returncode != 0:
        raise SystemExit("FATAL hash-object 失败")
    b = blob.stdout.decode().strip()
    p = subprocess.run(["git", "update-index", "--cacheinfo", "100644," + b + "," + rel],
                       cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("FATAL update-index 失败: " + p.stderr.decode("utf-8", "replace")[:200])
    print("  精确暂存 %s（blob %s）" % (rel, b[:8]))


def t_ledger(text):
    """台账 W974 行的 touches 列末尾追加 `scripts/index.md`

    ⚠️ 幂等判定必须**在 W974 行内**做——扫全文会因其它批次行也含该路径而误判「已登记」。
    """
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("| W974 |"):
            if "`scripts/index.md`" in ln:
                return text
            if not ln.rstrip().endswith("|"):
                raise SystemExit("FATAL 台账 W974 行格式异常")
            lines[i] = ln.rstrip()[:-1].rstrip() + " · `scripts/index.md` |"
            return "\n".join(lines)
    raise SystemExit("FATAL 台账未找到 W974 行")


def t_report(text):
    if "12.7 并发登记" in text:
        return text
    return text.rstrip("\n") + "\n" + REPORT_SEG


def main() -> int:
    dry = "--dry-run" in sys.argv
    for rel, fn in ((LEDGER_REL, t_ledger), (REPORT_REL, t_report)):
        head = git_show(rel)
        if head is None:
            print("SKIP（HEAD 无此文件）：%s" % rel)
            continue
        new = fn(head)
        if new == head:
            print("OK   无需改动：%s" % rel)
            continue
        if dry:
            print("DRY  %s：将改动 %d 字符" % (rel, len(new) - len(head)))
            continue
        write_atomic(rel, new)
        stage_exact(rel, new)
        print("OK   %s：已登记并精确暂存" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
