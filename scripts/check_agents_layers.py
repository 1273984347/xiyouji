#!/usr/bin/env python3
"""AGENTS 分层完整性门禁（第 41 槽 · W709）——L1 摘要层与 L2 主题层的结构防线。

BL-24 搬迁后 AGENTS §4.2/§4.3/§4.4 为摘要层，全量定义在 docs/agent/。本门禁四查：
  C1 L2 三件存在且含阅读契约与「何时」引导
  C2 三方编号对账：AGENTS §4.2 摘要条目 max == gates.md 门禁条目 max == verify_delivery 实况最高槽位
  C3 AGENTS 行数上限（≤450·L1 瘦身守恒防线）
  C4 L1 指针目标存在（AGENTS 引用的 docs/agent/ 文件）
豁免：无（结构防线）。用法：--check（默认）/ --self-test（注入式负样本）。
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
L2_FILES = ["docs/agent/gates.md", "docs/agent/pitfalls.md", "docs/agent/agent-web.md"]
RE_AGENT_ITEM = re.compile(r"^(\d+)\. \*\*", re.M)
RE_GATE_ITEM = re.compile(r"^(\d+)\. \*\*", re.M)
RE_VERIFY_SLOT = re.compile(r"第\s*(\d+)\s*(?:槽|门禁)")
AGENTS_MAX_LINES = 450


def rd(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def evaluate(inp):
    issues = []
    # C1 L2 存在 + 契约
    for p in L2_FILES:
        if p not in inp["files"]:
            issues.append("C1: %s 缺失（L2 主题层不完整）" % p)
            continue
        txt = inp["files"][p]
        if "阅读契约" not in txt:
            issues.append("C1: %s 缺阅读契约头部" % p)
        if p.endswith(("gates.md", "pitfalls.md")) and "何时" not in txt:
            issues.append("C1: %s 缺「何时读/何时触发」引导" % p)
    # C2 三方编号对账
    agents_max = max([int(x) for x in RE_AGENT_ITEM.findall(inp["agents_sec42"])] or [0]) or None
    gates_items = RE_GATE_ITEM.findall(inp["files"].get("docs/agent/gates.md", ""))
    gates_max = max([int(x) for x in gates_items] or [0]) or None
    verify_max = max([int(x) for x in RE_VERIFY_SLOT.findall(inp["verify_src"])] or [0]) or None
    if not (agents_max and gates_max and verify_max):
        issues.append("C2: 解析失败（AGENTS=%s / gates=%s / verify=%s · fail-closed）" % (agents_max, gates_max, verify_max))
    elif not (agents_max == gates_max == verify_max):
        issues.append("C2: 三方编号失配 AGENTS=%s / gates.md=%s / verify=%s（摘要与全量与实况必须一致）" % (agents_max, gates_max, verify_max))
    # C3 行数
    n = inp["agents_lines"]
    if n > AGENTS_MAX_LINES:
        issues.append("C3: AGENTS.md %d 行 > 上限 %d（L1 瘦身守恒）" % (n, AGENTS_MAX_LINES))
    # C4 指针目标
    for m in re.finditer(r"\((docs/agent/[a-z-]+\.md)\)", inp["agents"]):
        if m.group(1) not in inp["files"]:
            issues.append("C4: AGENTS 指针目标不存在：%s" % m.group(1))
    return issues


def gather():
    agents = rd("AGENTS.md")
    i42 = agents.find("### 4.2")
    i43 = agents.find("### 4.3")
    files = {p: rd(p) for p in L2_FILES if os.path.exists(os.path.join(ROOT, p))}
    return {
        "agents": agents,
        "agents_sec42": agents[i42:i43] if i42 != -1 and i43 != -1 else "",
        "agents_lines": agents.count("\n") + 1,
        "files": files,
        "verify_src": rd(os.path.join(HERE, "verify_delivery.py")),
    }


def run_check():
    issues = evaluate(gather())
    for it in issues:
        print("FAIL  " + it)
    print("---- 第 41 门禁 AGENTS 分层完整性：%d FAIL ----" % len(issues))
    return 1 if issues else 0


def run_self_test():
    base = gather()
    cases = []

    def case(name, mutate, expect):
        cases.append((name, mutate, expect))

    case("T1 干净态零误报", lambda d: None, None)
    case("T2 gates.md 缺失必红", lambda d: d["files"].pop("docs/agent/gates.md"), "C1")
    case("T3 编号三方失配必红", lambda d: d.update(agents_sec42=d["agents_sec42"].replace("40. **", "41. **", 1)), "C2")
    case("T4 AGENTS 超行必红", lambda d: d.update(agents_lines=999), "C3")
    case("T5 指针悬空必红", lambda d: d.update(agents=d["agents"].replace("(docs/agent/gates.md)", "(docs/agent/nope.md)", 1)), "C4")
    fails = 0
    for name, mutate, expect in cases:
        d = dict(base)
        d["files"] = dict(base["files"])
        mutate(d)
        issues = evaluate(d)
        ok = (not issues) if expect is None else any(i.startswith(expect) for i in issues)
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            fails += 1
            for i in issues:
                print("      -> " + i)
    print("---- agents-layers self-test：%d/%d 通过 ----" % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


def main():
    if "--self-test" in sys.argv:
        return run_self_test()
    return run_check()


if __name__ == "__main__":
    sys.exit(main())
