#!/usr/bin/env python3
"""_w1076_cjk_value_marks.py — W1076 B1 手术 1（卡片 ②）：中文 KPI 值加 .value--cjk 标记。

卡片 ② 禁改项：「禁 .value 套等宽渲染中文」+「中文值改 --font-sans 600 26px」。
CSS 无法按字形判定语言 ⇒ 以标记类落地（DOM 加 `value--cjk`），样式由
dashboard.html 的 `.kpi-card .value--cjk` 规则承载（--font-sans / 26px / 600）。

口径：仅 `<div class="value">…</div>` 形态（dashboard 看板 60 个 KPI 值），
内容含 CJK 统一表意文字（U+4E00–U+9FFF）者加标记；纯数值不加。
幂等：已带 `value--cjk` 的不重复加。
"""
import re
import os
import sys

def _repo_root():
    """向上找仓库根（带 .git 的目录）——脚本归档到 archive/scripts/batches/w1076/ 后仍可用。"""
    cur = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("未找到仓库根（.git）")
        cur = parent


ROOT = _repo_root()
TARGET = os.path.join(ROOT, "site", "dashboard.html")
CJK = re.compile(r"[\u4e00-\u9fff]")
VAL_RE = re.compile(r'<div class="value">([^<]*)</div>')


def main():
    with open(TARGET, encoding="utf-8", newline="") as fh:
        html = fh.read()

    marked, total, cjk_total = [], 0, 0

    def _sub(m):
        nonlocal total, cjk_total
        total += 1
        text = m.group(1)
        if not CJK.search(text):
            return m.group(0)
        cjk_total += 1
        marked.append(text.strip())
        return '<div class="value value--cjk">%s</div>' % text

    new = VAL_RE.sub(_sub, html)
    print("KPI 值总数 %d · 含中文 %d" % (total, cjk_total))
    for t in marked:
        print("   标记：%s" % t)
    if "--apply" in sys.argv:
        if new == html:
            print("无变化（幂等）")
        else:
            with open(TARGET, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
            print("已落盘：%d 处加 value--cjk" % cjk_total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
