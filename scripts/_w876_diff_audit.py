#!/usr/bin/env python3
"""_w876_diff_audit.py — W876 静态 diff 分类审计（一次性件·收尾验证第一轨）。

**做什么**：把 `git diff HEAD -- site/` 的每一处增删行归入三类预期改动——
  A. C 渠规则换色：`color: var(--accent)` → `color: var(--accent-text)`
     （页面自有 CSS 与 INLINED 块副本同口径·只动 color 声明）
  B. chart-3 值切换：`--chart-3: #C9A063` → `--chart-3: #B38F58`（2.42→3.01:1）
  C. 暗色 accent 值切换：`--accent: #E0604F` → `--accent: #E46250`（4.35→4.50:1）
归不入三类的增删行 = 未预期改动 → FAIL 并逐条列出（文件 + 行号 + 内容）。

**为什么这一轨是生死线**：W876 收尾时实证——`inline_css.py --force` 会把 W864-W875
迁进页面内联块的规则整段冲掉（system.css 自 W856 起未随迁移更新·regenerate 即回吞）。
本审计 = 「除三类外与 HEAD 逐字节一致」的机器证明：所有迁移成果（容器令牌化 /
.seal 淡底 / KPI 顶条收敛 / 间距令牌化）完好无损，且换色与值切换零越界。

**配对口径（强判据）**：同一 hunk 内，added 行把新值换回旧值后必须与 removed 行
逐字符相等（rstrip 后）——即「只换了该换的那个 token，同行其余内容零变动」。
纯增行/纯删行（无配对）一律判未预期。

用法：py -3 scripts/_w876_diff_audit.py [--path site/] [--ref HEAD]
退出码：0 = 全部归三类 · 1 = 有未预期改动（或 git diff 执行失败）
"""

import re
import subprocess
import sys

# 三类预期改动：(类名, 旧值正则, 新值正则, 新→旧回代串)
# 正则只做「路由」——行内可含选择器/注释等其余内容（单行规则与带尾注释的令牌行均合法），
# 强判据是配对时的回代相等（只换该换的 token·同行其余内容零变动）。
# A 类负向查视 (?<![-\w])：禁把 border-color / background-color 等 *-color 属性路由进
# 「只动文本 color」类——W876 实证 swap 脚本的 color\s*:\s*var\(--accent\) 子串正则会
# 误伤 border-color（6 处·已回退），此查视是回归防线。
CLASSES = [
    ("A·C渠换色", re.compile(r"(?<![-\w])color\s*:\s*var\(--accent\)"),
     re.compile(r"(?<![-\w])color\s*:\s*var\(--accent-text\)"),
     lambda s: s.replace("var(--accent-text)", "var(--accent)")),
    ("B·chart-3值", re.compile(r"--chart-3\s*:\s*#C9A063"),
     re.compile(r"--chart-3\s*:\s*#B38F58"),
     lambda s: s.replace("#B38F58", "#C9A063")),
    ("C·暗色accent值", re.compile(r"--accent\s*:\s*#E0604F"),
     re.compile(r"--accent\s*:\s*#E46250"),
     lambda s: s.replace("#E46250", "#E0604F")),
]

_HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def _classify(removed, added):
    """removed/added 为剥掉前导 +/- 的行文本。返回类名或 None。"""
    for name, old_re, new_re, back in CLASSES:
        if old_re.search(removed) and new_re.search(added) and back(added) == removed:
            return name
    return None


def main(argv):
    path = "site/"
    ref = "HEAD"
    if "--path" in argv:
        path = argv[argv.index("--path") + 1]
    if "--ref" in argv:
        ref = argv[argv.index("--ref") + 1]

    p = subprocess.run(["git", "diff", ref, "-U0", "--", path],
                       capture_output=True, text=True, encoding="utf-8")
    if p.returncode != 0:
        print("[FAIL] git diff 执行失败：%s" % p.stderr.strip()[:200])
        return 1

    counts = {name: 0 for name, _, _, _ in CLASSES}
    files = set()
    unexplained = []
    cur_file = None
    line_no = 0
    removed, added = [], []  # [(行号, 文本)]

    def flush():
        nonlocal removed, added
        pool = list(added)
        for rno, rtxt in removed:
            hit = None
            for i, (ano, atxt) in enumerate(pool):
                cls = _classify(rtxt, atxt)
                if cls:
                    hit = (i, cls)
                    break
            if hit is None:
                unexplained.append((cur_file, rno, "-" + rtxt))
            else:
                counts[hit[1]] += 1
                pool.pop(hit[0])
        for ano, atxt in pool:
            unexplained.append((cur_file, ano, "+" + atxt))
        removed, added = [], []

    for raw in p.stdout.splitlines():
        if raw.startswith("diff --git"):
            flush()
            m = re.match(r'diff --git a/(.*) b/(.*)$', raw)
            cur_file = m.group(2) if m else raw
            files.add(cur_file)
            continue
        if raw.startswith("index ") or raw.startswith("--- ") or raw.startswith("+++ "):
            continue
        m = _HUNK.match(raw)
        if m:
            flush()
            line_no = int(m.group(3))
            continue
        if raw.startswith("-") and not raw.startswith("---"):
            removed.append((line_no, raw[1:].rstrip("\r")))
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            added.append((line_no, raw[1:].rstrip("\r")))
            line_no += 1
            continue
    flush()

    print("=== W876 静态 diff 分类审计（%s vs %s · %s）===" % (path, ref, "工作树"))
    print("改动文件数：%d" % len(files) if files else "改动文件数：见 git")
    for name, n in counts.items():
        print("  %-14s %d 处" % (name, n))
    total = sum(counts.values())
    if unexplained:
        print("[FAIL] 未预期改动 %d 处——三类之外的任何变动都不允许：" % len(unexplained))
        for f, no, txt in unexplained[:40]:
            print("  %s:%s  %s" % (f, no, txt[:150]))
        if len(unexplained) > 40:
            print("  ... 共 %d 处" % len(unexplained))
        return 1
    print("[PASS] 全部 %d 处增删行归三类·三类之外与 %s 逐字节一致" % (total, ref))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
