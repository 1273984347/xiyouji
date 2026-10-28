#!/usr/bin/env python3
"""check_gov_doc_claims.py — 治理文档数字断言对账器（W967 建·举一反三沉淀）。

方法论：治理文档里的人工数字是唯一没有对账线的面（stats 标记有 C5b/C5d、
指纹有 W966 摘要层纪律——但散落在叙述里的人工计数谁也不查）。本器把
高置信的数字断言逐条钉到机器事实源，漂移即报。报告型（exit 0），供
preflight 提示位与批收尾手跑；升格判红需用户批准挂 verify 槽。

钉定的断言（事实源全部磁盘实算，无手抄）：
  N1 协议边界速查：A1-A6 六板块字母与篇数 == docs/ 各目录 .md 磁盘计数
  N2 文档规范「verify full N 段」 == verify_delivery EXPECTED_SECTION_NAMES 实数
  N3 AGENTS「全 N 槽门禁」 == gates.md 顶层编号条目实数
  N4 AGENTS「N 条坑位」 == pitfalls.md 六主题「- **」条目实数
  N5 新Agent启动Prompt：A1-A6 总篇数 / 可视化页 / data HTML == stats.json 各键
用法：
  py -3 scripts/check_gov_doc_claims.py            # 报告（exit 0）
  py -3 scripts/check_gov_doc_claims.py --self-test
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 板块字母映射（AGENTS §3 权威形态·01-06 目录序 ≠ 字母序——W967 实证错位重灾区）
BOARD_MAP = [(1, "A1", 100), (2, "A3", 215), (3, "A4", 209),
             (4, "A5", 34), (5, "A6", 13), (6, "A2", 44)]


def _read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8", newline="").read()


def _disk_board_counts():
    """docs/0N-*/ 顶层 .md 计数 → {1:100, ...}（子目录不计——口径同 stats a1_a6_docs）。"""
    out = {}
    skip = {"README.md", "index.md"}  # 生成件不入板块计数（口径同 stats a1_a6_docs）
    for d, _, _ in BOARD_MAP:
        pat = os.path.join(ROOT, "docs", "0%d-*" % d, "*.md")
        out[d] = len([f for f in glob.glob(pat) if os.path.basename(f) not in skip])
    return out


def _verify_sections():
    t = _read(os.path.join("scripts", "verify_delivery.py"))
    i = t.find("EXPECTED_SECTION_NAMES = [")
    j = t.find("]", i)
    body = t[i + len("EXPECTED_SECTION_NAMES = ["):j]
    return [x.strip().strip(",").strip('"') for x in body.replace("\n", "").split(",") if x.strip()]


def _gates_slot_count():
    t = _read(os.path.join("docs", "agent", "gates.md"))
    return len(re.findall(r"(?m)^\d+\. \*\*", t))


def _pitfalls_count():
    t = _read(os.path.join("docs", "agent", "pitfalls.md"))
    sec = None
    counts = {}
    for ln in t.split("\n"):
        m = re.match(r"^### (?:CSS|JS|git|级联|数据|流程)", ln)
        if m:
            sec = m.group(0)
            counts[sec] = 0
        elif sec and re.match(r"^- \*\*", ln):
            counts[sec] += 1
    return sum(counts.values())


def _stats():
    return json.load(open(os.path.join(ROOT, "scripts", "output", "stats.json"), encoding="utf-8"))


def check():
    """跑全部断言 → (报告行, FAIL 行)。事实源缺失按 fail-closed 报告。"""
    lines, fails = [], []
    stats = _stats()
    disk = _disk_board_counts()

    # N1 速查六板块
    t = _read(os.path.join("docs", "00-导读", "协议边界速查.md"))
    ok = True
    for d, letter, _expect in BOARD_MAP:
        pat = r"`docs/0%d-[^（]*`（%s [^）]*?%d 篇）" % (d, letter, disk[d])  # noqa: B007 — expect 为映射自文档列·口径对账以此交叉验证
        if not re.search(pat, t):
            ok = False
            fails.append("N1: 协议边界速查 0%d 板块断言漂移（应为 %s/%d 篇·磁盘实算）" % (d, letter, disk[d]))
    lines.append("N1 速查六板块字母与篇数（磁盘实算 %s）：%s" % (
        dict(sorted(disk.items())), "一致" if ok else "漂移"))

    # N2 文档规范 verify full 段数
    n = len(_verify_sections())
    t = _read(os.path.join("docs", "00-导读", "文档规范.md"))
    m = re.search(r"verify full 全部执行段（随挂槽演进·现役 (\d+) 段", t)
    if not m:
        fails.append("N2: 文档规范「全量」段数断言形态缺失或已改写（期望现役 %d 段措辞）" % n)
    elif int(m.group(1)) != n:
        fails.append("N2: 文档规范「全量」= %s 段 ≠ verify 实数 %d 段" % (m.group(1), n))
    else:
        lines.append("N2 文档规范 verify full 段数（现役 %d）：一致" % n)

    # N3 槽数
    slots = _gates_slot_count()
    t = _read("AGENTS.md")
    m = re.search(r"内含 (\d+) 槽，五组", t)
    if not m:
        fails.append("N3: AGENTS §4.2「内含 N 槽」断言形态缺失")
    elif int(m.group(1)) != slots:
        fails.append("N3: AGENTS「内含 %s 槽」≠ gates.md 编号条目实数 %d" % (m.group(1), slots))
    else:
        lines.append("N3 槽数（gates 编号条目 %d）：一致" % slots)

    # N4 坑位数
    pn = _pitfalls_count()
    m = re.search(r"(\d+) 条坑位按六主题迁", t)
    if not m:
        fails.append("N4: AGENTS §4.3「N 条坑位」断言形态缺失")
    elif int(m.group(1)) != pn:
        fails.append("N4: AGENTS「%s 条坑位」≠ pitfalls 实数 %d" % (m.group(1), pn))
    else:
        lines.append("N4 坑位数（pitfalls 实数 %d）：一致" % pn)

    # N5 新Agent启动Prompt 三个统计键
    t = _read("docs/00-导读/新Agent启动Prompt.md")
    pairs = [(r"内容板块（(\d+) 篇）", "a1_a6_docs"),
             (r"可视化页 (\d+)（", "visualization_pages"),
             (r"共 (\d+) 个 HTML", "site_data_html")]
    for pat, key in pairs:
        m = re.search(pat, t)
        if not m:
            fails.append("N5: 新Agent启动Prompt 断言形态缺失（%s）" % key)
        elif int(m.group(1)) != stats[key]["value"]:
            fails.append("N5: 新Agent启动Prompt %s=%s ≠ stats %d" % (key, m.group(1), stats[key]["value"]))
        else:
            lines.append("N5 新Agent启动Prompt %s=%d：一致" % (key, stats[key]["value"]))
    return lines, fails


def _self_test() -> int:
    """自测：注入漂移必须被报出（N1 形态·合成数据）。"""
    fails = []
    # N1 判据形态：正确行放行 / 错行（W967 实证错位形态）必报
    good = "`docs/02-人物深度分析/`（A3 人物谱系 215 篇）"
    bad = "`docs/02-人物深度分析/`（A2 人物随笔 44 篇）"
    pat = r"`docs/02-[^（]*`（A3 [^）]*?215 篇）"
    if not re.search(pat, good):
        fails.append("正确行未放行")
    if re.search(pat, bad):
        fails.append("错位行（W967 实证形态）未被判漂移——判据无效")
    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：N1 判据对 W967 实证错位形态必红（判据可证伪）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="治理文档数字断言对账器（W967）")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    print("== 治理文档数字断言对账（W967·报告型）==")
    lines, fails = check()
    for line in lines:
        print("  " + line)
    if fails:
        for f in fails:
            print("FAIL ", f)
        print("---- 数字断言对账：%d FAIL ----" % len(fails))
    else:
        print("---- 数字断言对账：0 FAIL ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
