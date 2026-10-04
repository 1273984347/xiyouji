#!/usr/bin/env python3
"""文档口径体检 doc-sync（第 31 门禁 · W663）——代码/提交是真值源，文档当前态声明是派生物。

移植自 GateKeeper / 千问大赛仓 doc-sync 机制（W663 经验移植批；D2 裁决：对账表登记即豁免）。
四类窄句式白名单（宁窄勿误，防误伤历史叙述——历史段/方案档/复盘档一律不进扫描面）：
  C1 README 抬头「当前版本 vX（日期）**： W###」 ≡ CHANGELOG 顶段三元组
  C2 交接文档头链链首「- **vX W###」 ≡ CHANGELOG 顶段（v + W）
  C3 AGENTS §4.2 门禁清单最高编号 == verify_delivery.py 实况最高槽位
  C4 提交-版段对账：近 15 条 commit subject 中的 W### ⊆ CHANGELOG 版段集合 ∪ 对账表登记行
豁免：行级 <!--doc-sync:exempt 原因-->；.git/shallow 存在时 C4 跳过（pre-commit 本地为主执行点）。
用法：--check（默认）只读校验，0 FAIL 才过；--self-test 注入式负样本 7 例（纯合成输入，不改真实文件）；
     --json 供 CI 消费。本脚本绝不修改任何文件。
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RE_CHANGELOG_TOP = re.compile(r"^###\s+v(\d+\.\d+\.\d+)（([^）]*)）：\s*W(\d+)", re.M)
RE_CHANGELOG_SECT = re.compile(r"^###\s+v\d+\.\d+\.\d+（[^）]*）：\s*W(\d+)", re.M)
RE_README_HEAD = re.compile(r"当前版本\s*v(\d+\.\d+\.\d+)（([^）]+)）\*\*：\s*W(\d+)")
RE_JIAOJIE_HEAD = re.compile(r"^-\s*\*\*v(\d+\.\d+\.\d+)\s+W(\d+)", re.M)
RE_AGENTS_ITEM = re.compile(r"^(\d+)\.\s\*\*", re.M)
RE_VERIFY_SLOT = re.compile(r"第\s*(\d+)\s*(?:槽|门禁)")
RE_COMMIT_W = re.compile(r"(?<![A-Za-z0-9])[Ww](\d{3})(?!\d)")
RE_TABLE_ROW_W = re.compile(r"^\|\s*W(\d{3})\s*\|", re.M)
RE_TABLE_DEFER = re.compile(r"^-\s*\*\*((?:W\d{3})(?:\s*/\s*W\d{3})*)\*\*", re.M)
EXEMPT_MARK = "<!--doc-sync:exempt"
ARCHIVE_CHANGELOGS = [
    os.path.join(ROOT, "docs", "archive", "CHANGELOG-ARCHIVE.md"),
    os.path.join(ROOT, "docs", "archive", "CHANGELOG-ARCHIVE-tier2.md"),
]


def changelog_top(text):
    m = RE_CHANGELOG_TOP.search(text)
    return (m.group(1), m.group(2), m.group(3)) if m else None


def changelog_section_ws(text):
    return set(RE_CHANGELOG_SECT.findall(text))


def table_registered_ws(text):
    ws = set(RE_TABLE_ROW_W.findall(text))
    for m in RE_TABLE_DEFER.finditer(text):
        ws |= set(RE_COMMIT_W.findall(m.group(1)))
    return ws


def agents_gate_list_max(agents_text):
    m = re.search(r"### 4\.2[^\n]*\n(.*?)### 4\.3", agents_text, re.S)
    if not m:
        return None
    nums = [int(x) for x in RE_AGENTS_ITEM.findall(m.group(1))]
    return max(nums) if nums else None


def verify_slot_max(verify_src):
    nums = [int(x) for x in RE_VERIFY_SLOT.findall(verify_src)]
    return max(nums) if nums else None


def line_has_exempt(text, match):
    line_start = text.rfind("\n", 0, match.start()) + 1
    line_end = text.find("\n", match.end())
    if line_end == -1:
        line_end = len(text)
    return EXEMPT_MARK in text[line_start:line_end]


def evaluate(inp):
    """纯函数核对：inputs 为注入真值与文档文本的 dict，返回 (issues, notes)。

    issues 元素以 C1:/C2:/C3:/C4: 前缀定性，供 --self-test 断言。
    """
    issues, notes = [], []
    top = changelog_top(inp["changelog"])
    if not top:
        issues.append("C1: CHANGELOG 未解析出现役顶段（期望 ### vX.Y.Z（日期）：W###）")
        top = ("?", "?", "?")
    ver, date, wnum = top

    # C1 README 抬头三元组
    m1 = RE_README_HEAD.search(inp["readme"])
    if not m1:
        issues.append("C1: README 未解析出「当前版本 vX（日期）**： W###」抬头句")
    elif line_has_exempt(inp["readme"], m1):
        notes.append("C1: README 抬头行带 doc-sync:exempt 豁免，跳过")
    elif (m1.group(1), m1.group(2), m1.group(3)) != top:
        issues.append(
            "C1: README 抬头 v%s（%s）W%s ≠ CHANGELOG 顶段 v%s（%s）W%s"
            % (m1.group(1), m1.group(2), m1.group(3), ver, date, wnum)
        )

    # C2 交接文档头链链首
    m2 = RE_JIAOJIE_HEAD.search(inp["jiaojie"])
    if not m2:
        issues.append("C2: 交接文档未解析出头链链首「- **vX W###」")
    elif line_has_exempt(inp["jiaojie"], m2):
        notes.append("C2: 交接头链行带 doc-sync:exempt 豁免，跳过")
    elif (m2.group(1), m2.group(2)) != (ver, wnum):
        issues.append(
            "C2: 交接头链 v%s W%s ≠ CHANGELOG 顶段 v%s W%s" % (m2.group(1), m2.group(2), ver, wnum)
        )

    # C3 AGENTS §4.2 门禁清单上限 == verify 实况最高槽位
    a_max = agents_gate_list_max(inp["agents"])
    v_max = verify_slot_max(inp["verify_src"])
    if a_max is None or v_max is None:
        issues.append("C3: 解析失败（AGENTS §4.2 清单=%s / verify 槽位=%s·fail-closed）" % (a_max, v_max))
    elif a_max != v_max:
        issues.append("C3: AGENTS §4.2 门禁清单止于 %d，verify 实况最高槽位 %d（声明落后于代码实况）" % (a_max, v_max))

    # C4 提交-版段对账（D2：对账表登记即豁免）
    if inp.get("shallow"):
        notes.append("C4: 浅克隆环境（.git/shallow），提交对账跳过（pre-commit 本地为主执行点）")
    else:
        reg = changelog_section_ws(inp["changelog"])
        for p in ARCHIVE_CHANGELOGS:
            if os.path.exists(p):
                reg |= changelog_section_ws(open(p, encoding="utf-8").read())
        reg |= table_registered_ws(inp["table"])
        for s in inp["subjects"]:
            for w in RE_COMMIT_W.findall(s):
                if w not in reg:
                    issues.append("C4: 提交「%s」的 W%s 无 CHANGELOG 版段且未在对账表登记" % (s[:60], w))
    return issues, notes


def gather():
    def rd(p):
        with open(p, encoding="utf-8") as f:
            return f.read()

    inputs = {
        "changelog": rd(os.path.join(ROOT, "CHANGELOG.md")),
        "readme": rd(os.path.join(ROOT, "README.md")),
        "jiaojie": rd(os.path.join(ROOT, "交接文档.md")),
        "agents": rd(os.path.join(ROOT, "AGENTS.md")),
        "verify_src": rd(os.path.join(HERE, "verify_delivery.py")),
        "table": rd(os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md")),
        "subjects": [],
        "shallow": os.path.exists(os.path.join(ROOT, ".git", "shallow")),
    }
    try:
        r = subprocess.run(
            ["git", "log", "--format=%s", "-15"], cwd=ROOT, capture_output=True, text=True, timeout=30
        )
        if r.returncode != 0:
            inputs.setdefault("git_err", r.stderr.strip()[:120])
        else:
            inputs["subjects"] = [ln for ln in r.stdout.splitlines() if ln.strip()]
    except Exception as e:  # noqa: BLE001 —— 环境无 git 时 fail-closed
        inputs["git_err"] = str(e)[:120]
    if inputs.get("git_err") and not inputs["shallow"]:
        # 无 git 且非浅克隆：无法对账即 fail-closed（浅克隆已有跳过通道）
        inputs["force_c4_fail"] = inputs["git_err"]
    return inputs


def run_check():
    inp = gather()
    if inp.get("force_c4_fail"):
        print("FAIL  C4: git log 不可得且非浅克隆，提交对账 fail-closed：%s" % inp["force_c4_fail"])
        print("---- 第 31 门禁 文档口径体检：1 FAIL（C4 fail-closed）----")
        return 1, ["C4: git log 不可得"], []
    issues, notes = evaluate(inp)
    for it in issues:
        print("FAIL  " + it)
    for nt in notes:
        print("NOTE  " + nt)
    print(
        "---- 第 31 门禁 文档口径体检：%d FAIL · %d NOTE（C1 README 抬头 / C2 交接头链 / C3 门禁清单上限 / C4 提交-版段对账）----"
        % (len(issues), len(notes))
    )
    return (1 if issues else 0), issues, notes


def run_self_test():
    """7 例注入式负样本/正样本（纯合成输入，不改真实文件）。"""
    base = {
        "changelog": "### v9.9.9（2026-10-05）：W999 自测顶段\n\n### v9.9.8（2026-10-04）：W998 旧段\n",
        "readme": "> **当前版本 v9.9.9（2026-10-05）**： W999 自测抬头行\n",
        "jiaojie": "- **v9.9.9 W999 自测链首**：\n",
        "agents": "### 4.2 交付门禁\n\n30. **甲门**\n31. **乙门**\n\n### 4.3 其他\n",
        "verify_src": "# ---- 第 30 槽 ----\n# ---- 第 31 槽 ----\n",
        "subjects": ["feat(w999): 自测提交"],
        "table": "| W999 | x | y | z | s | c |\n- **W659 / W660**：递延登记\n",
        "shallow": False,
    }
    cases = []

    def case(name, mutate, expect_prefix=None, expect_absent=False):
        cases.append((name, mutate, expect_prefix, expect_absent))

    case("T1 README 抬头改值必红", lambda d: d.update(readme=d["readme"].replace("W999", "W998")), "C1")
    case("T2 交接头链改值必红", lambda d: d.update(jiaojie=d["jiaojie"].replace("W999", "W997")), "C2")
    case(
        "T3 门禁清单上限失配必红",
        lambda d: d.update(agents=d["agents"].replace("31. **乙门**", "")),
        "C3",
    )
    case(
        "T4 提交带未登记 W 必红",
        lambda d: d.update(subjects=d["subjects"] + ["test(w777): 伪造未登记提交"]),
        "C4",
    )
    case(
        "T5 对账表登记即豁免（D2）",
        lambda d: d.update(subjects=["chore(w659): 递延批提交"]),
        "C4",
        expect_absent=True,
    )
    case(
        "T6 行级豁免标记生效",
        lambda d: d.update(readme="> **当前版本 v9.9.6（2026-10-05）**： W996 自测抬头行 <!--doc-sync:exempt 历史时点事实-->\n"),
        "C1",
        expect_absent=True,
    )
    case("T7 干净输入零误报", lambda d: None)

    fails = 0
    for name, mutate, expect_prefix, expect_absent in cases:
        data = dict(base)
        mutate(data)
        issues, _notes = evaluate(data)
        if expect_prefix is None:
            ok = not issues
        elif expect_absent:
            ok = not any(i.startswith(expect_prefix) for i in issues)
        else:
            ok = any(i.startswith(expect_prefix) for i in issues)
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            fails += 1
            for i in issues:
                print("      -> " + i)
    print("---- doc-sync self-test：%d/%d 通过 ----" % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


def main():
    if "--self-test" in sys.argv:
        return run_self_test()
    code, issues, notes = run_check()
    if "--json" in sys.argv:
        print(json.dumps({"issues": issues, "notes": notes}))
    return code


if __name__ == "__main__":
    sys.exit(main())
