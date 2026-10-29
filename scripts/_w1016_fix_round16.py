# -*- coding: utf-8 -*-
"""_w1016_fix_round16.py — W1016 一次修：下载器 DEST round15→round16 + 迁移误落原件 + 成品处理

首测踩坑：派生下载器时只改了 manifest 名与批号串，**漏改 DEST 目录**（仍指向 round15）
⇒ 12 张原件全部误落 round15 ⇒ prepare 报「round16 下无出图原件」。
⇒ 本脚本一次修齐并跑完成品处理。
"""
import io
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D15 = os.path.join(REPO, "assets", "promo", "plate-set", "raw", "round15")
D16 = os.path.join(REPO, "assets", "promo", "plate-set", "raw", "round16")
PY = sys.executable


def main() -> int:
    # ① 修下载器 DEST（round15 → round16）
    p = os.path.join(REPO, "scripts", "_w1016_download.py")
    s = io.open(p, encoding="utf-8").read()
    if "round15" in s:
        s = s.replace("round15", "round16")
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        print("OK   下载器 DEST round15 -> round16")
    else:
        print("SKIP  下载器 DEST 已是 round16")

    # ② 迁移误落原件（只迁本批 73–84 ⇒ 文件名前缀 plate-line-7 / 8 里的 73–84 号）
    os.makedirs(D16, exist_ok=True)
    moved = 0
    for f in sorted(os.listdir(D15)) if os.path.isdir(D15) else []:
        if not f.startswith("plate-line-"):
            continue
        num = f.split("-")[2]
        if num in ("73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84"):
            src = os.path.join(D15, f)
            dst = os.path.join(D16, f)
            if os.path.exists(src):
                shutil.move(src, dst)
                moved += 1
    print("OK   迁移 %d 件 → round16（现有 %d 件）" % (moved, len(os.listdir(D16))))

    # ③ 成品处理
    r = subprocess.run([PY, os.path.join(REPO, "scripts", "_w1016_prepare.py")],
                       cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    out = (r.stdout or "") + (r.stderr or "")
    for ln in out.splitlines():
        if any(k in ln for k in ("母版 ", "站点版", "拼图", "FAIL", "Traceback", "Error")):
            print("  " + ln[:150])
    print("prepare rc =", r.returncode)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
