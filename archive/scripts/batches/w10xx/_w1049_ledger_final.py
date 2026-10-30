# -*- coding: utf-8 -*-
"""_w1049_ledger_final.py — 台账 W1049 行收官回填（状态 + hash）

用 `scripts/ledger_backfill.py` 回填（该脚本已处理「显式参数优先」与「零代提」）：
  ① 先用 safe_commit 提交本批（拿到 commit hash）
  ② 再用 `ledger_backfill.py --w 1049 --hash <hash> --status "..."` 回填
  ③ 再精确暂存台账（W1049 行）并提交回填笔

用法：py -3 archive/scripts/batches/w10xx/_w1049_ledger_final.py <commit-hash>
"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))

STATUS = "**已收官**（%s·共 1 笔·12 张 og 扩量落地·独立盲审 3 P0+4 P1 已处置·P-43-01）"


def main() -> int:
    if len(sys.argv) < 2:
        print("用法：py -3 %s <commit-hash>" % os.path.basename(__file__))
        return 2
    h = sys.argv[1].strip()
    assert len(h) >= 7, "commit hash 形态异常：%s" % h
    r = subprocess.run(["py", "-3", os.path.join(REPO, "scripts", "ledger_backfill.py"),
                        "--w", "1049", "--hash", h, "--status", STATUS % h],
                       capture_output=True, cwd=REPO)
    out = (r.stdout or b"").decode("utf-8", "replace")
    err = (r.stderr or b"").decode("utf-8", "replace")
    print(out[-1500:])
    if err.strip():
        print("STDERR:", err[-500:])
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
