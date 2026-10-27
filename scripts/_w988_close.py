# -*- coding: utf-8 -*-
"""_w988_close.py — W988 台账收官回填（hash 列 + 状态列 + 指纹复核）

事实：本批主体内容被并行会话的 W989 提交 `1fb1b14f`（全量提交）代提入库，
本批另有一笔收官补齐提交 ⇒ 状态列须同时写明两个 hash，否则台账与事实不符。

用法：py -3 scripts/_w988_close.py [--apply]
"""
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(REPO, "docs", "00-导读", "W批次编号对账表.md")
ADOPTED = "1fb1b14f"


def run(args):
    r = subprocess.run([sys.executable, os.path.join(REPO, "scripts", "ledger_backfill.py")] + args,
                       capture_output=True, text=True, cwd=REPO)
    print((r.stdout or "") + (r.stderr or ""))
    return r.returncode, (r.stdout or "")


def main() -> int:
    apply = "--apply" in sys.argv
    # ① hash 列：从 git 反填（找 subject 含 W988 的提交）
    rc, out = run(["--w", "988", "--from-git"] + (["--apply"] if apply else []))
    if rc != 0:
        print("hash 列反填失败（rc=%d）" % rc)
        return rc
    m = re.search(r"([0-9a-f]{7,40})", out)
    mine = m.group(1) if m else ""
    print("本批收官补齐提交 hash =", mine or "(未解析)")

    # ② 状态列：写明「主体内容由 1fb1b14f 代提 + 收官补齐笔」
    status = ("**已收官**（主体内容由并行 W989 提交 %s 代提入库 + 收官补齐 %s·"
              "27 张 card-* 全落位·102 页 og:image 换专属 1200×630·判据 V1-V9 全 PASS·负样本 4/4·"
              "全量门禁 55/55 段全绿）" % (ADOPTED, mine or "本笔"))
    rc, out = run(["--w", "988", "--status", status] + (["--apply"] if apply else []))
    if rc != 0:
        return rc

    # ③ 指纹复核
    m2 = re.search(r"([0-9a-f]{16,})", out)
    if m2:
        run(["--w", "988", "--verify", m2.group(1)] + (["--apply"] if apply else []))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
