# -*- coding: utf-8 -*-
"""_w1005_handover_line.py — 代并行 W1004 补 HANDOVER §一 里程碑链首行

C2 判据（`check_doc_sync.py`）：交接文档头链**链首**（行首 `- **W###`）≡ CHANGELOG 顶段。
现状：CHANGELOG 顶段已是 W1004，但 HANDOVER §一 的里程碑列表链首仍是 `- **W1003 …`
⇒ 门禁红「交接文档 HEAD W1003 与 CHANGELOG 最新段 W1004 不一致」（治理契约 + 文档口径体检共 2 项）。

处置：代 W1004 补一条里程碑行（摘要据其 README 抬头「转正清零 + 审查触发器判据修正」）。
**若 W1004 会话收官时自行补同一条 ⇒ 以其为准（可能重复），本行不影响内容正确性。**

用法：py -3 scripts/_w1005_handover_line.py [--dry-run]
"""
import io
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAND = os.path.join(REPO, "HANDOVER.md")
LINE = ("- **W1004 转正清零 + 审查触发器判据修正批**：8 件硬保留全部转正（C4 配额 8→0）+ "
        "审查触发器改认事件 token「对抗审查已派发」（字样不再重置计数）+ last_audit_batch 改取 max"
        "（后补登记不再算歪 gap）+ 台账 W998 行按 CHANGELOG 归位 + 补幽灵测试\n")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in sys.argv
    t, n = read(HAND)
    if "- **W1004 " in t:
        print("SKIP  HANDOVER 已有 W1004 链首行")
        return 0
    lines = t.split("\n")
    pos = None
    for i, ln in enumerate(lines):
        if ln.startswith("- **W1003 "):
            pos = i
            break
    if pos is None:
        print("FAIL  未找到 W1003 链首行（锚点失配）")
        return 1
    lines.insert(pos, LINE)
    t = "\n".join(lines)
    if dry:
        print("DRY  HANDOVER 将加 W1004 链首行")
    else:
        write(HAND, t, n)
        print("OK   HANDOVER 已加 W1004 链首行")
    import re
    m = re.search(r"^-\s*\*\*(?:v\d+\.\d+\.\d+\s+)?W(\d+)", t, re.M)
    print("复核 链首 =", m.group(1) if m else "未解析")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
