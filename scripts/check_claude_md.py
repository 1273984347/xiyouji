#!/usr/bin/env python3
"""CLAUDE.md 速查层完整性门禁（第 32 门禁 · W667/S-02）——防速查层断链与数字腐烂。

四项检查（evaluate 纯函数·合成输入可自测）：
  C1 指针文件存在：CLAUDE.md 提及的每个 .md/.py 路径必须真实存在
  C2 章节锚点对拍：每条「<file> §N」/「§N-M」——目标文件须有 N 节标题；带 -M 时该节内须有 M. 条目
  C3 行数 ≤ 60（CLAUDE.md 维护契约）
  C4 禁漂移字面量：不得出现现役版本号 vX.Y.Z / W### / W001-Wxxx（速查层零漂移设计·指针化取数）
用法：默认=只读校验（0 FAIL 才过）；--self-test 注入式负样本 5 例。本脚本绝不修改任何文件。
"""

import os
import re
import sys

from utils.gate_common import ROOT, SelfTestTally, cli_main, read_text_strict

LINE_LIMIT = 60


def section_exists(text, topnum):
    return re.search(r"(?m)^#{2,6}\s*" + re.escape(topnum) + r"(?:\.|\s)", text) is not None


def subitem_exists(text, topnum, sub):
    m = re.search(r"(?m)^#{2,6}\s*" + re.escape(topnum) + r"(?:\.|\s)[^\n]*", text)
    if not m:
        return False
    nxt = re.search(r"(?m)^#{2,6}\s", text[m.end():])
    seg = text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]
    return re.search(r"(?m)^%s\. " % re.escape(sub), seg) is not None


def evaluate(claude, files):
    """files: {相对路径: 文件内容}；返回 (issues, notes)。issues 以前缀 C1:/C2:/C3:/C4: 定性。"""
    issues, notes = [], []
    # C3 行数：以「逻辑行数」计——结尾换行不算一行（`a\nb\n` 与 `a\nb` 同为 2 行）。
    # W803 清理：此处原有两行连续赋值，第 1 行算法含两项恒为 0 的加法（`+ 0` 与
    # `+ (1 if … else 0)` 的 `+ 0` 分支），其结果立即被第 2 行覆盖、从未被读取——
    # 属死代码。已用 7 个边界样本（空串/无尾换行/有尾换行/仅换行/双换行）+ 真实
    # CLAUDE.md 实算旧新等值（0 处不一致）后删除，保留实际生效的算法。
    n = claude.count("\n") + 1 if claude and not claude.endswith("\n") else claude.count("\n")
    if n > LINE_LIMIT:
        issues.append("C3: CLAUDE.md %d 行 > 上限 %d（维护契约）" % (n, LINE_LIMIT))
    # C4 禁漂移字面量（只扫正文；头部引用行=元信息块血缘记录·按第 18 门禁要求带批次溯源·豁免）
    body_lines = [ln for ln in claude.splitlines() if not ln.startswith(">")]
    body = "\n".join(body_lines)
    if re.search(r"\bv\d+\.\d+\.\d+\b", body):
        issues.append("C4: 正文出现现役版本号字面量（速查层零漂移设计·一律指针化）")
    for pat, name in ((r"\bW\d{3,4}\b", "W###"), (r"W001-W\d+", "W 区间")):
        if re.search(pat, body):
            issues.append("C4: 正文出现 %s 字面量（禁写会漂移的现役值）" % name)
    # C1 文件指针存在
    tokens = set(re.findall(r"(AGENTS\.md|CHANGELOG\.md|(?:scripts|docs)/[^\s（）」，。]*?\.(?:py|md))", claude))
    for tk in sorted(tokens):
        if tk not in files:
            issues.append("C1: 指针目标不存在：%s" % tk)
    # C2 章节锚点对拍（形如「AGENTS.md §6-2」「文档规范.md §4.9」——文件与 § 同现一行）
    for line in claude.splitlines():
        for m in re.finditer(r"(AGENTS\.md|CHANGELOG\.md|(?:docs)/[^\s（）」，。]*?\.md)\s*§([\d.]+)(?:-([\d]+))?", line):
            path, top, sub = m.group(1), m.group(2), m.group(3)
            body = files.get(path)
            if body is None:
                continue  # C1 已报
            if not section_exists(body, top):
                issues.append("C2: %s 缺 %s 节标题（指针悬空）" % (path, top))
            elif sub and not subitem_exists(body, top, sub):
                issues.append("C2: %s §%s 节内缺 %s. 条目（指针悬空）" % (path, top, sub))
    return issues, notes


def gather():
    def rd(p):
        """读治理档（严格 UTF-8：本门禁读的是仓自有文件，编码坏了应当立刻炸出来，
        不像站点扫描型门禁那样需要容错跳过——见 utils/gate_common.read_text_strict 注释）。"""
        return read_text_strict(os.path.join(ROOT, p))

    claude = rd("CLAUDE.md")
    files = {}
    for tk in sorted(set(re.findall(r"(AGENTS\.md|CHANGELOG\.md|(?:scripts|docs)/[^\s（）」，。]*?\.(?:py|md))", claude))):
        p = os.path.join(ROOT, tk)
        files[tk] = read_text_strict(p) if os.path.exists(p) else None
    return claude, files


def run_check():
    claude, files = gather()
    issues, notes = evaluate(claude, files)
    for it in issues:
        print("FAIL  " + it)
    for nt in notes:
        print("NOTE  " + nt)
    print("---- 第 32 门禁 CLAUDE.md 速查层：%d FAIL（C1 指针存在/C2 锚点对拍/C3 行数≤%d/C4 禁漂移值）----"
          % (len(issues), LINE_LIMIT))
    return 1 if issues else 0


def run_self_test():
    """注入式负样本自测：在合成 CLAUDE.md 上打变异，断言对应检查项必红。

    计数与收尾行交给 SelfTestTally（W803 收敛）；逐例输出形态（`PASS  <用例名>`
    与失败时的 `      -> <issue>` 明细）是本门禁自有文案，保留在本地。
    T7 是「反向断言」用例（`absent=True`）：断言某检查项**不得**触发（元信息块血缘豁免）。
    """
    agents = read_text_strict(os.path.join(ROOT, "AGENTS.md"))
    gf = read_text_strict(os.path.join(ROOT, "docs", "00-导读", "文档规范.md"))
    good = ("1. **E1 铁律**：声明≠落地 → AGENTS.md §6-2\n"
            "2. **写作纪律**：禁模糊措辞 → docs/00-导读/文档规范.md §4.9\n"
            "3. 常用命令 `python scripts/verify_delivery.py` 与 `scripts/_cite_probe.py`\n")
    files = {"AGENTS.md": agents, "docs/00-导读/文档规范.md": gf,
             "scripts/verify_delivery.py": "x", "scripts/_cite_probe.py": "x"}
    cases = []

    def case(name, claude, expect, absent=False):
        cases.append((name, claude, expect, absent))

    case("T1 干净输入零误报", good, None)
    case("T2 指针文件缺失必红", good + "4. 见 scripts/不存在.py\n", "C1")
    case("T3 章节锚点悬空必红（§6-99 无条目）", good + "5. 见 AGENTS.md §6-99\n", "C2")
    case("T4 行数超限必红", good + "x\n" * 70, "C3")
    case("T5 现役版本字面量必红", good + "6. 当前版本 v2.3.262\n", "C4")
    case("T6 W 区间字面量必红", good + "7. 覆盖 W001-W999\n", "C4")
    case("T7 元信息块血缘豁免", "> 生成来源：人工撰写·W664\n" + good, "C4", True)

    tally = SelfTestTally("CLAUDE.md 门禁")
    for name, claude, expect, absent in cases:
        issues, _ = evaluate(claude, files)
        ok = (not issues) if expect is None else (
            any(i.startswith(expect) for i in issues) if not absent
            else not any(i.startswith(expect) for i in issues))
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
        if not tally.add(ok):
            for i in issues:
                print("      -> " + i)
    return tally.report()


def main():
    return cli_main(run_check, run_self_test)


if __name__ == "__main__":
    sys.exit(main())
