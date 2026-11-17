# -*- coding: utf-8 -*-
"""Playwright 截图与版式断言：3 页 × 明暗 × {1280, 375} = 12 张。

断言：
  · 12 张截图齐备
  · 375px 四组 scrollWidth == clientWidth（无横向滚动）
  · 明暗两态截图字节数必须不同（否则暗态没生效）
  · 零 console error / page error

用法：py -3 _shoot.py
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SHOT_DIR = ROOT / "shots"
FAILURES = []
COUNT = 0


def check(label, ok, detail=""):
    global COUNT
    COUNT += 1
    print("[%s] %-52s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILURES.append(label)
    return ok


def main():
    node = shutil_which("node")
    if node is None:
        print("[FAIL] 未找到 node，无法驱动 playwright")
        return 1
    proc = subprocess.run([node, str(ROOT / "_shoot.js")], cwd=str(ROOT),
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        print("[FAIL] node _shoot.js 退出码 %d" % proc.returncode)
        print(proc.stderr[-2000:])
        return 1
    try:
        data = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception as exc:
        print("[FAIL] 无法解析 node 输出：%s" % exc)
        print(proc.stdout[-1500:])
        return 1

    shots = data["shots"]
    check("截图：共 12 张", len(shots) == 12, "实得 %d 张" % len(shots))
    missing = [s["file"] for s in shots if not pathlib.Path(s["file"]).exists()]
    check("截图：文件全部落盘", not missing, "缺：%s" % (missing if missing else "无"))

    # 375px 无横向滚动
    for s in shots:
        if s["width"] == 375:
            m = s["metrics"]
            ok = m["scrollWidth"] == m["clientWidth"] and m["bodyScrollWidth"] <= m["clientWidth"]
            check("375px 无横向滚动 · %s/%s" % (s["page"], s["theme"]), ok,
                  "scrollWidth=%d clientWidth=%d" % (m["scrollWidth"], m["clientWidth"]))

    # 明暗字节数必须不同
    pairs = set()
    for s in shots:
        other = [o for o in shots if o["page"] == s["page"] and o["width"] == s["width"] and o["theme"] != s["theme"]]
        if not other:
            continue
        pairs.add((s["page"], s["width"]))
        o = other[0]
        check("明暗两态字节数不同 · %s @%dpx" % (s["page"], s["width"]),
              s["bytes"] != o["bytes"], "light=%d B / dark=%d B" % (o["bytes"], s["bytes"]))
    check("明暗配对覆盖 3 页 × 2 宽度", len(pairs) == 6, "%d 对" % len(pairs))

    # 主题属性确实落到 DOM 上
    wrong = [s for s in shots if s["metrics"]["theme"] != s["theme"]]
    check("data-theme 与截图主题一致", not wrong, "不一致：%d 张" % len(wrong))

    check("零 console error", not data["consoleErrors"], str(data["consoleErrors"][:3]))
    check("零 page error", not data["pageErrors"], str(data["pageErrors"][:3]))

    print("\n共 %d 项检查，失败 %d 项" % (COUNT, len(FAILURES)))
    if FAILURES:
        print("RESULT: FAIL")
        for f in FAILURES:
            print("  - " + f)
        return 1
    print("RESULT: PASS")
    return 0


def shutil_which(cmd):
    from shutil import which
    return which(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
