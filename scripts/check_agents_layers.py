#!/usr/bin/env python3
"""AGENTS 分层完整性门禁（第 41 槽 · W709）——L1 摘要层与 L2 主题层的结构防线。

BL-24 搬迁后 AGENTS §4.2/§4.3/§4.4 为摘要层，全量定义在 docs/agent/。本门禁四查：
  C1 L2 三件存在且含阅读契约与「何时」引导
  C2 两方编号对账：gates.md 门禁条目 max == verify_delivery 实况最高槽位 ＋ AGENTS 路由表含 gates.md 触发行
  C3 AGENTS 行数上限（≤200·W1279 地图预算）
  C4 L1 指针目标存在（AGENTS 引用的 docs/agent/ 文件）
豁免：无（结构防线）。用法：--check（默认）/ --self-test（注入式负样本）。
"""

import os
import re
import sys

from utils.gate_common import ROOT, SCRIPTS_DIR, SelfTestTally, cli_main, read_text_strict

L2_FILES = ["docs/agent/gates.md", "pitfalls.md", "docs/agent/agent-web.md"]  # pitfalls W1157 正本迁根
RE_AGENT_ITEM = re.compile(r"^(\d+)\. \*\*", re.M)
RE_GATE_ITEM = re.compile(r"^(\d+)\. \*\*", re.M)
RE_VERIFY_SLOT = re.compile(r"第\s*(\d+)\s*(?:槽|门禁)")
AGENTS_MAX_LINES = 200  # W1279 地图预算


def rd(p):
    """读治理档（严格 UTF-8：本门禁读的是仓自有文件，编码坏了应当立刻炸出来，
    不像站点扫描型门禁那样需要容错跳过——见 utils/gate_common.read_text_strict 注释）。"""
    return read_text_strict(os.path.join(ROOT, p))


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
    # C2 两方编号对账（W1279：AGENTS 地图化后不再复制槽位摘要——对账锚移 gates.md）
    #   ＋ AGENTS 路由表必须含 gates.md 触发行（地图缺主路由即红）
    gates_items = RE_GATE_ITEM.findall(inp["files"].get("docs/agent/gates.md", ""))
    gates_max = max([int(x) for x in gates_items] or [0]) or None
    verify_max = max([int(x) for x in RE_VERIFY_SLOT.findall(inp["verify_src"])] or [0]) or None
    if not (gates_max and verify_max):
        issues.append("C2: 解析失败（gates=%s / verify=%s · fail-closed）" % (gates_max, verify_max))
    elif gates_max != verify_max:
        issues.append("C2: gates.md=%s ≠ verify=%s（全量定义与实况必须一致）" % (gates_max, verify_max))
    if "docs/agent/gates.md" not in inp["agents"] or "任何写操作" not in inp["agents"]:
        issues.append("C2: AGENTS 路由表缺 gates.md 触发行（地图主路由缺失）")
    # C3 行数
    n = inp["agents_lines"]
    if n > AGENTS_MAX_LINES:
        issues.append("C3: AGENTS.md %d 行 > 上限 %d（L1 瘦身守恒）" % (n, AGENTS_MAX_LINES))
    # C4 指针目标
    # W1279：地图形态指针 = 路由表表格行（| docs/agent/x.md |）＋ 括号引用，两形态都核验
    for m in re.finditer(r"(?:\(|\|\s*)(docs/agent/[a-z-]+\.md)", inp["agents"]):
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
        "verify_src": rd(os.path.join(SCRIPTS_DIR, "verify_delivery.py")),
    }


def run_check():
    issues = evaluate(gather())
    for it in issues:
        print("FAIL  " + it)
    print("---- 第 41 门禁 AGENTS 分层完整性：%d FAIL ----" % len(issues))
    return 1 if issues else 0


def run_self_test():
    """注入式负样本自测：每个用例在干净输入上打一处变异，断言对应检查项必红。

    计数与收尾行交给 SelfTestTally（W803 收敛）；逐例输出形态（`PASS  <用例名>`
    与失败时的 `      -> <issue>` 明细）是本门禁自有文案，保留在本地。
    """
    base = gather()
    cases = []

    def case(name, mutate, expect):
        cases.append((name, mutate, expect))

    case("T1 干净态零误报", lambda d: None, None)
    case("T2 gates.md 缺失必红", lambda d: d["files"].pop("docs/agent/gates.md"), "C1")
    # W1279：对账锚移 gates.md——verify 侧槽位数变异即失配（旧 AGENTS §4.2 侧变异随摘要退役删除）
    case("T3 gates/verify 编号失配必红", lambda d: d.update(verify_src=d["verify_src"].replace("第 83 槽", "第 82 槽", 1)), "C2")
    case("T4 AGENTS 超行必红", lambda d: d.update(agents_lines=201), "C3")
    case("T5 路由缺 gates 行必红", lambda d: d.update(agents=d["agents"].replace("docs/agent/gates.md | **任何写操作前**", "docs/agent/gates-x.md | **任何写操作前**", 1)), "C2")
    case("T6 指针悬空必红", lambda d: d.update(agents=d["agents"].replace("(docs/agent/agent-web.md)", "(docs/agent/nope.md)", 1)), "C4")

    tally = SelfTestTally("agents-layers")
    for name, mutate, expect in cases:
        d = dict(base)
        d["files"] = dict(base["files"])
        mutate(d)
        issues = evaluate(d)
        ok = (not issues) if expect is None else any(i.startswith(expect) for i in issues)
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
        if not tally.add(ok):
            for i in issues:
                print("      -> " + i)
    return tally.report()


def main():
    return cli_main(run_check, run_self_test)


if __name__ == "__main__":
    sys.exit(main())
