#!/usr/bin/env python3
"""acceptance_snapshot.py — W496 转正工具：验收数字当批现测速览。

背景（W495 教训）：W493 CHANGELOG 的「内联 28385B」系从 W489 复制的旧值，
提交时页面 INLINED 块已被同批脚本清空——跨批次复制验收数字是事故放大器。
本脚本把关键验收数字一次性现测输出，写 CHANGELOG/方案档时从这里抄，
禁止从上一批 CHANGELOG 抄。

输出项（均为当批实测）：
- 单页内联 CSS（INLINED 块 min/max B，M5 口径）
- token 覆盖率（UI 裸色总/真裸 shadow/FAIL，M2/M3）
- 动效禁止清单命中数（M4/D4）
- a11y E2-2 P0+P1（M1）
- 非白名单断点媒体查询数（W494 口径）

用法：python scripts/acceptance_snapshot.py [--no-a11y]（a11y 较慢，可跳过）
"""
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
BP_WHITE = {375, 480, 640, 768, 1024, 1280, 1536}


def inlined_sizes():
    sizes = []
    for f in glob.glob(os.path.join(ROOT, "site", "data", "*.html")) + \
             glob.glob(os.path.join(ROOT, "site", "en", "*.html")):
        if os.path.basename(f) in ("_shell.html", "_template.html"):
            continue
        t = open(f, encoding="utf-8").read()
        m = re.search(r"INLINED CSS.*?-->\s*<style>(.*?)</style>", t, re.S)
        if m:
            sizes.append(len(m.group(1).strip()))
    return sizes


def nonwhite_breakpoints():
    n = 0
    for f in glob.glob(os.path.join(ROOT, "site", "**", "*.html"), recursive=True) + \
             [os.path.join(ROOT, "site", "system.css")]:
        if not os.path.isfile(f) or os.path.basename(f) in ("_shell.html", "_template.html"):
            continue
        t = open(f, encoding="utf-8", errors="ignore").read()
        for mq in re.findall(r"@media[^{]*max-width:\s*(\d+)px", t):
            if int(mq) not in BP_WHITE:
                n += 1
    return n


def run_gate(script, extra=()):
    try:
        r = subprocess.run([sys.executable, os.path.join(HERE, script)] + list(extra),
                           capture_output=True, text=True, timeout=300)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return "EXEC-ERROR %s" % e


def main():
    fast = "--no-a11y" in sys.argv
    sizes = inlined_sizes()
    print("==== 验收现测速览（W496 acceptance_snapshot）====")
    if sizes:
        print("M5 单页内联 CSS：min %dB / max %dB（预算 33KB=33792B）" % (min(sizes), max(sizes)))
    else:
        print("M5 单页内联 CSS：无 INLINED 块（异常！）")
    tok = run_gate("check_token_coverage.py")
    m = re.search(r"UI 裸色总 (\d+) · 真裸 box-shadow 总 (\d+) · FAIL (\d+)", tok)
    print("M2/M3 token 覆盖率：%s" % ("UI 裸色总 %s · 真裸 shadow %s · FAIL %s" % m.groups() if m else "解析失败"))
    mot = run_gate("check_motion_ban.py")
    m = re.search(r"命中 (\d+)", mot)
    print("M4/D4 动效禁止清单：命中 %s" % (m.group(1) if m else "解析失败"))
    if not fast:
        a11y = run_gate("a11y_audit.py", ("--dir", "site", "--format", "json", "--quiet"))
        try:
            import json
            rep = json.loads(a11y[a11y.index("{"):])
            e22 = rep.get("summary", {}).get("E2-2", {})
            print("M1 a11y E2-2：P0=%s P1=%s" % (e22.get("P0", 0), e22.get("P1", 0)))
        except Exception:
            print("M1 a11y E2-2：解析失败（手动跑 a11y_audit.py）")
    print("断点白名单外媒体查询：%d 处（W494 口径，应 0）" % nonwhite_breakpoints())
    print("== 写 CHANGELOG/方案档验收数字时从本输出抄，禁跨批次复制 ==")


if __name__ == "__main__":
    main()
