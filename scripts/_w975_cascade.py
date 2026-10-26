# -*- coding: utf-8 -*-
"""_w975_cascade.py — W975 四面登记（跨 Agent 经验沉淀入仓批）

基底 = **索引版**（`git show :<file>`）——W975 之前本批已对 AGENTS/HANDOVER/台账等做过精确暂存，
用 HEAD 作底会丢掉本批前几次改动 ⇒ 叠加后再 `git update-index --cacheinfo` 写回索引。

四面：CHANGELOG 段 / file-index 段 / README 当前批次行 / HANDOVER 进度与最后更新链。
"""
import io
import os
import subprocess
import sys

REPO = r"D:\xiyouji"
BATCH = "W975"
LEDGER_REL = "docs/00-导读/W批次编号对账表.md"
CHANGELOG_REL = "CHANGELOG.md"
FILE_INDEX_REL = "scripts/output/file-index.md"
README_REL = "README.md"
HANDOVER_REL = "HANDOVER.md"

FILE_LIST = [
    "docs/agent/pitfalls.md", "AGENTS.md", "HANDOVER.md",
    "docs/10-方法论沉淀/README.md", "docs/10-方法论沉淀/素材批处理与判据自证方法论.md",
    "scripts/_w975_sink_experience.py", "scripts/_w975_cascade.py", "scripts/_w975_tweak.py",
    "scripts/output/_cascade_files_W975.txt", "scripts/output/file-index.md",
    "CHANGELOG.md", "README.md", LEDGER_REL,
]
FILE_LINE = "> - **文件**：" + "、".join(FILE_LIST)

CHANGELOG_SEG = """### W975（2026-10-27）：跨 Agent 经验沉淀入仓批（坑表 57 → 63 条 + 深度篇 1 篇 + 计数链同步）

> **来源**：用户 2026-10-27 纠正「你不能只沉淀进你自己的 Memory 文件，本项目是多 Agent 协作的项目所以需要你同样沉淀进本项目内」。
>
> **问题定性**：W974 批的 9 条经验只写进 Agent 私有 Memory ⇒ **仓内其他 Agent 读不到** ⇒ 正是坑表既有条目「共享机制必须写入仓库内文件（git tracked）」的**复发实证**（该条目本批已补注复发）。

%s

**入仓面（四处载体）**：① 坑表 `docs/agent/pitfalls.md` **6 条新条目**（CSS/视觉渲染 +2「器物形状类别 > 数量计数」「落位页先验」· git/提交/并发 +1「写既有文件须临时文件 + 原子替换」· 数据/内容可信度 +2「bbox 顶 ≠ 主体顶」「校验/自检代码必须自证」· 流程/协作/取证 +1「端口占用是假故障」）+ 4 处节标题条数 + 共享机制条目补 W974 复发注；② **深度篇**《素材批处理与判据自证方法论.md》（`docs/10-方法论沉淀/` 编号 26·含问题背景/方法论/复现案例/修复策略/关联文档五段）；③ `AGENTS.md` §4.3 主题视图与计数声明；④ `HANDOVER.md` 两处指针。

**计数链同步**：坑位 **57 → 63 条**（AGENTS §4.3 与 HANDOVER 的条数声明同批订正·门禁 N4 核对「AGENTS 声明 == pitfalls 实数」⇒ 复验一致）。

**纪律**：共享面按内容粒度精确暂存（`git update-index --cacheinfo`·基底为索引版以叠加本批前几次改动）⇒ 并行会话在途内容既不入本批提交、也不被抹掉。

> - **验证**：（见本批脚本输出与对账表回填）
> - **状态**：在途（认领登记 W975·待提交入库）

""" % FILE_LINE

FILE_INDEX_SEG = (
    "## W975 跨 Agent 经验沉淀入仓批（2026-10-27）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    "| docs/agent/pitfalls.md | W975 | 坑表 +6 条（57→63·四节标题条数同步·共享机制条目补 W974 复发注） |\n"
    "| AGENTS.md | W975 | §4.3 主题视图 + 坑位条数声明 57→63（门禁 N4 口径） |\n"
    "| HANDOVER.md | W975 | 「三、方法论沉淀」与「雷区权威」两处指针 57→63 |\n"
    "| docs/10-方法论沉淀/素材批处理与判据自证方法论.md | W975 | 新增深度篇（编号 26·五段结构） |\n"
    "| docs/10-方法论沉淀/README.md | W975 | 目录索引登记编号 26 |\n"
    "| scripts/_w975_sink_experience.py | W975 | 入仓同步器（坑表/AGENTS/HANDOVER/深篇登记/台账认领行） |\n"
    "| scripts/_w975_tweak.py | W975 | 通用「字面替换 + 精确暂存」工具（基底取索引版） |\n"
    "| scripts/_w975_cascade.py | W975 | 四面登记 + 当前态指针 |\n"
    "| scripts/output/_cascade_files_W975.txt | W975 | 当批级联清单 |\n"
    "| CHANGELOG.md | W975 | W975 版段 |\n"
    "| docs/00-导读/W批次编号对账表.md | W975 | W975 认领行 |\n"
    "\n"
)

README_LINE = ("> **当前批次 W975（2026-10-27）**：跨 Agent 经验沉淀入仓批（坑表 57→63 条、"
               "深度篇《素材批处理与判据自证方法论》、计数链同步）·A1-A6<!--doc-sync:exempt-->")

HANDOVER_PROGRESS = (
    "## 一、当前进度（W975 跨 Agent 经验沉淀入仓批；更早批次详见 CHANGELOG.md）\n"
    "- **W975 跨 Agent 经验沉淀入仓批**：把 W974 批的 9 条经验从 Agent 私有 Memory 搬进仓内——"
    "坑表 `docs/agent/pitfalls.md` +6 条（57→63）、深度篇《素材批处理与判据自证方法论》（10-方法论沉淀 编号 26）、"
    "AGENTS §4.3 主题视图与计数声明、HANDOVER 两处指针同批同步（门禁 N4「AGENTS 声明 == pitfalls 实数」复验一致）。\n"
)


def read_base(rel):
    """基底 = 索引版（叠加本批前几次改动）⇒ 空则用 HEAD"""
    p = subprocess.run(["git", "show", ":" + rel], cwd=REPO, capture_output=True)
    if p.returncode == 0 and p.stdout:
        return p.stdout.decode("utf-8").replace("\r\n", "\n")
    p = subprocess.run(["git", "show", "HEAD:" + rel], cwd=REPO, capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout.decode("utf-8").replace("\r\n", "\n")


def write_atomic(rel, text, nl):
    p = os.path.join(REPO, rel.replace("/", os.sep))
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


def t_changelog(t):
    if ("### " + BATCH + "（") in t:
        return t
    import re
    m = re.search(r"^### W\d+", t, re.M)
    pos = m.start() if m else len(t)
    t = t[:pos] + CHANGELOG_SEG + t[pos:]
    return re.sub(r"（W001-W\d+）", "（W001-W975）", t, count=1)


def t_file_index(t):
    if ("## " + BATCH + " ") in t:
        return t
    import re
    m = re.search(r"^## W\d+", t, re.M)
    pos = m.start() if m else len(t)
    return t[:pos] + FILE_INDEX_SEG + t[pos:]


def t_readme(t):
    import re
    return re.sub(r"> \*\*当前批次 W\d+（\d{4}-\d{2}-\d{2}）\*\*：[^\n]*", README_LINE, t, count=1)


def t_handover(t):
    import re
    lines = t.split("\n")
    out = []
    for ln in lines:
        if ln.startswith("- **W975 "):
            continue
        if ln.startswith("## 一、当前进度（W"):
            out.extend(HANDOVER_PROGRESS.rstrip("\n").split("\n"))
            continue
        out.append(ln)
    t = "\n".join(out)
    t = re.sub(r"> 最后更新：\d{4}-\d{2}-\d{2}[^\n]*",
               "> 最后更新：2026-10-27（W975 跨 Agent 经验沉淀入仓批）·2026-10-27（W974 内页题图成套批·第三组）·"
               "2026-10-26（W973 HANDOVER 五区清理批）·（W449-W549 及更早批次详见 CHANGELOG.md）", t, count=1)
    t = re.sub(r"每次完成新 W### 后更新。最后更新：[^\n]*",
               "每次完成新 W### 后更新。最后更新：2026-10-27（W975 跨 Agent 经验沉淀入仓批）", t, count=1)
    return t


TARGETS = [(CHANGELOG_REL, t_changelog), (FILE_INDEX_REL, t_file_index),
           (README_REL, t_readme), (HANDOVER_REL, t_handover)]


def main() -> int:
    cl = os.path.join(REPO, "scripts", "output", "_cascade_files_W975.txt")
    with io.open(cl, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(FILE_LIST) + "\n")
    print("级联清单：scripts/output/_cascade_files_W975.txt（%d 项）" % len(FILE_LIST))
    for rel, fn in TARGETS:
        base = read_base(rel)
        if base is None:
            print("SKIP（无基底）：%s" % rel)
            continue
        new = fn(base)
        if new == base:
            print("OK   无需改动：%s" % rel)
            continue
        p = os.path.join(REPO, rel.replace("/", os.sep))
        raw = io.open(p, "rb").read()
        nl = "\r\n" if b"\r\n" in raw else "\n"
        write_atomic(rel, new, nl)
        stage_exact(rel, new)
        print("OK   %s：已改写并精确暂存" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
