# -*- coding: utf-8 -*-
"""_w975_backfill.py — W975 收官回填（台账状态 + 关联 commit + touches）

基底 = **索引版台账**（W975 认领行由 `_w975_sink_experience.py` 精确暂存进索引·HEAD 版没有该行）
→ 复制到临时文件 → 调 `scripts/ledger_backfill.py`（按列定位回填）→ 读回 → 精确暂存。
CHANGELOG 段的「验证 / 状态」两行同样在索引版基底上替换 ⇒ 并行会话在途内容不入本批提交。

用法：py -3 scripts/_w975_backfill.py --hash <本批主体提交 hash>
"""
import argparse
import io
import os
import subprocess
import sys
import tempfile

REPO = r"D:\xiyouji"
LEDGER_REL = "docs/00-导读/W批次编号对账表.md"
CHANGELOG_REL = "CHANGELOG.md"
BATCH = "W975"

STATUS = (
    "已收官（REPLACE_HASH·坑表 57 → **63 条**（+6：CSS/视觉渲染 +2 器物形状类别>数量计数·落位页先验 / "
    "git/提交/并发 +1 写既有文件须临时文件+原子替换 / 数据/内容可信度 +2 bbox 顶≠主体顶·校验与自检代码必须自证 / "
    "流程/协作/取证 +1 端口占用是假故障）+ 共享机制条目补 W974 复发注（经验只进 Agent 私有 Memory ⇒ 仓内其他 Agent 读不到）·"
    "深度篇《素材批处理与判据自证方法论》落 docs/10-方法论沉淀 编号 26 + 该目录 README 索引登记·"
    "计数链同步（AGENTS §4.3 主题视图与条数声明 57→63 · HANDOVER 两处指针 · STRUCTURE 的 methodology_docs 24→25）·"
    "门禁 N4「AGENTS 声明 == pitfalls 实数」复验一致（63=63）·第 31/第 45 门禁 0 FAIL·CSP 0 漂移·lint_links 0 broken·"
    "共享面按内容粒度精确暂存（update-index --cacheinfo·基底取索引版以叠加本批前几次改动）·"
    "**归属自检**：提交后 git log --oneline -1 -- docs/agent/pitfalls.md 确认落在本批）"
)

TOUCHES = (
    "docs/agent/pitfalls.md, AGENTS.md, HANDOVER.md, docs/10-方法论沉淀/README.md, "
    "docs/10-方法论沉淀/素材批处理与判据自证方法论.md, docs/00-导读/W批次编号对账表.md, "
    "CHANGELOG.md, README.md, scripts/output/file-index.md, scripts/_w975_*.py, "
    "scripts/output/_cascade_files_W975.txt, scripts/output/stats.json, scripts/output/stats-changelog.json, "
    "scripts/output/stats-index.md, scripts/output/index.md, scripts/output/README.md, "
    "docs/INDEX.md, STRUCTURE.md, scripts/index.md, assets/promo/plate-set/zoom-w974/"
)

VERIFY = (
    "> - **验证**：坑表条目实数 **63** == AGENTS §4.3 声明 63（门禁 N4 一致）·第 31 / 第 45 门禁 0 FAIL · "
    "第 48 门禁 0 FAIL · CSP 0 漂移 · lint_links 0 broken · 深篇《素材批处理与判据自证方法论》已登记入 "
    "`docs/10-方法论沉淀/README.md` 编号 26 · docs/INDEX.md 重建（768 篇）"
)

CSTATUS = (
    "> - **状态**：已收官（`REPLACE_HASH`·**协作纪律**：本批共享面按内容粒度**精确暂存**——"
    "基底取**索引版**以叠加本批前几次改动、`git update-index --cacheinfo` 写入索引、工作树同步 ⇒ "
    "并行会话在途内容既不入我的提交也不被我抹掉）"
)


def base_of(rel):
    p = subprocess.run(["git", "show", ":" + rel], cwd=REPO, capture_output=True)
    if p.returncode == 0 and p.stdout:
        return p.stdout.decode("utf-8").replace("\r\n", "\n")
    p = subprocess.run(["git", "show", "HEAD:" + rel], cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("FATAL 无基底：%s" % rel)
    return p.stdout.decode("utf-8").replace("\r\n", "\n")


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


def write_atomic(rel, text):
    p = os.path.join(REPO, rel.replace("/", os.sep))
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    tmp = p + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(text.replace("\n", nl).encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hash", required=True)
    args = ap.parse_args()
    h = args.hash

    # ---- 台账 ----
    base = base_of(LEDGER_REL)
    if "| W975 |" not in base:
        raise SystemExit("FATAL 台账基底无 W975 行")
    tmp = os.path.join(tempfile.gettempdir(), "w975_ledger_base.md")
    io.open(tmp, "w", encoding="utf-8", newline="").write(base)
    cmd = [sys.executable, os.path.join(REPO, "scripts", "ledger_backfill.py"),
           "--w", "975", "--hash", h, "--status", STATUS.replace("REPLACE_HASH", h),
           "--touches", TOUCHES, "--ledger", tmp]
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    print((p.stdout.strip() or p.stderr.strip())[-300:])
    if p.returncode != 0:
        raise SystemExit("FATAL ledger_backfill 失败")
    new_ledger = io.open(tmp, encoding="utf-8").read()
    if new_ledger != base:
        write_atomic(LEDGER_REL, new_ledger)
        stage_exact(LEDGER_REL, new_ledger)

    # ---- CHANGELOG ----
    cl = base_of(CHANGELOG_REL)
    new_cl = cl
    if "> - **验证**：（见本批脚本输出与对账表回填）" in new_cl:
        new_cl = new_cl.replace("> - **验证**：（见本批脚本输出与对账表回填）", VERIFY, 1)
    if "> - **状态**：在途（认领登记 W975·待提交入库）" in new_cl:
        new_cl = new_cl.replace("> - **状态**：在途（认领登记 W975·待提交入库）",
                                CSTATUS.replace("REPLACE_HASH", h), 1)
    if new_cl != cl:
        write_atomic(CHANGELOG_REL, new_cl)
        stage_exact(CHANGELOG_REL, new_cl)
    else:
        print("  CHANGELOG 无变化")
    return 0


if __name__ == "__main__":
    sys.exit(main())
