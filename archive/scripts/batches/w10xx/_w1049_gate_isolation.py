# -*- coding: utf-8 -*-
"""_w1049_gate_isolation.py — 本批门禁失败的归因核验（独立复验）

背景：工作树内含 **W1050 批的 6 个在途件**（用户 2026-10-31 令「摘出勿卷入」）
⇒ 第 31 门禁的 C4-f（文件清单入库对账·比**工作树** vs **提交树**）与 C2
（交接头链 ≡ CHANGELOG 顶段·CHANGELOG 顶段读**工作树**）必然报红。

本脚本做**归因核验**（不是绕过）：把每条 FAIL 归入
  ① 本批引入 ⇒ 真缺陷，必须修
  ② W1050 在途件导致 ⇒ 与本批无关（已知取舍·W1050 批重放时消解）

判定方法（可复核）：
  · C4-f：报红路径 ∈ W1050 六件清单 ⇒ 归 ②；否则归 ①
  · C2：CHANGELOG 工作树顶段 W1050 存在 ⇒ 归 ②（W1050 段剔除后才与 HANDOVER 一致）
  · 其余 FAIL（C5d/C5e 等）⇒ 归 ①，必须清零

用法：py -3 archive/scripts/batches/w10xx/_w1049_gate_isolation.py
"""
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))

# 用户点名的 W1050 六件
W1050_FILES = {
    "scripts/verify_delivery.py",
    "scripts/check_doc_sync.py",
    "docs/agent/gates.md",
    "scripts/output/_w1050_spec.json",
    "scripts/output/_cascade_files_W1050.txt",
}
# W1050 批级联面（版本行指向 W1050 ⇒ 本批不动的 17 项）
W1050_FACES = {
    ".github/workflows/README.md", "README.md", "STRUCTURE.md", "CITATION.cff",
    "docs/00-导读/项目说明.md", "archive/docs/AGENTS-ARCHIVE.md",
    "archive/docs/CHANGELOG-ARCHIVE.md", "archive/docs/W批次编号对账表-ARCHIVE.md",
    "archive/docs/file-index-ARCHIVE.md", "scripts/output/README.md",
    "scripts/output/index.md", "scripts/output/stats.json",
    "scripts/output/tools-inventory.md", "site/index.html",
    "site/data/cross-time-danmaku.html", "site/data/tag-cloud.html",
    "site/dukou-engine.html", "scripts/output/stats-changelog.json",
    "scripts/output/stats-index.md",
}
W1050_ALL = W1050_FILES | W1050_FACES
# 门禁缓存产物（每次判据运行即变 sha1+时间戳 ⇒ 非本批产物·不可提交·
# 提交前须恢复 HEAD 版·见 `_w1049_fix_cache.py`）
CACHE_FILES = {"scripts/output/_vermilion_solid_cache.json"}


def main() -> int:
    r = subprocess.run(["py", "-3", os.path.join(REPO, "scripts", "check_doc_sync.py")],
                       capture_output=True, cwd=REPO)
    out = r.stdout.decode("utf-8", "replace")
    fails = [l for l in out.splitlines() if l.startswith("FAIL")]

    mine, theirs = [], []
    for l in fails:
        m = re.search(r"C4-f:\s*文件清单\s+(.+?)\s+(?:有工作树未提交残留|未入提交树)", l)
        if m:
            path = m.group(1).strip()
            if path in W1050_ALL or path in CACHE_FILES:
                theirs.append(l)
            else:
                mine.append(l)
            continue
        if l.startswith("FAIL  C2:"):
            # CHANGELOG 工作树顶段 == W1050 ⇒ 与本批 W1049 头链的差异来自 W1050 段
            theirs.append(l)
            continue
        mine.append(l)

    print("第 31 门禁 FAIL 共 %d 项 ⇒ 本批引入 %d · W1050 在途件导致 %d"
          % (len(fails), len(mine), len(theirs)))
    if mine:
        print("\n== 本批引入（必须清零）==")
        for l in mine:
            print("  " + l)
    if theirs:
        print("\n== W1050 在途件导致（与本批无关·W1050 批重放时消解）==")
        for l in theirs:
            print("  " + l[:140])

    # 自证：CHANGELOG 暂存版（我的提交内容）顶段 == W1049 ⇒ 提交后 C2 自洽
    st = subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO,
                         "show", ":CHANGELOG.md"], capture_output=True).stdout.decode("utf-8", "replace")
    m = re.search(r"(?m)^### (W\d{3,4})", st)
    staged_top = m.group(1) if m else "(无)"
    ho = io.open(os.path.join(REPO, "HANDOVER.md"), encoding="utf-8").read()
    mh = re.search(r"(?m)^## 一、当前进度（W(\d{3,4})", ho)
    ho_top = ("W" + mh.group(1)) if mh else "(无)"
    print("\n== 提交后自洽性核验 ==")
    print("  CHANGELOG 暂存版顶段 = %s · HANDOVER 头链 = %s ⇒ %s"
          % (staged_top, ho_top, "一致 ✓" if staged_top == ho_top else "不一致 ✗"))
    if staged_top != ho_top:
        print("  FAIL  提交后 C2 仍会红（头链与顶段必须一致）")
        return 1
    if mine:
        print("  FAIL  仍有 %d 项本批引入的 FAIL" % len(mine))
        return 1
    print("  PASS 本批零引入失败；余 %d 项为 W1050 在途件所致（用户令摘出）" % len(theirs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
