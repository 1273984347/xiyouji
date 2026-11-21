#!/usr/bin/env python3
"""check_gov_doc_claims.py — 治理文档数字断言对账器（W967 建·举一反三沉淀）。

方法论：治理文档里的人工数字是唯一没有对账线的面（stats 标记有 C5b/C5d、
指纹有 W966 摘要层纪律——但散落在叙述里的人工计数谁也不查）。本器把
高置信的数字断言逐条钉到机器事实源，漂移即报。报告型（exit 0），供
preflight 提示位与批收尾手跑；升格判红需用户批准挂 verify 槽。

钉定的断言（事实源全部磁盘实算，无手抄）：
  N1 协议边界速查：A1-A6 六板块字母与篇数 == docs/ 各目录 .md 磁盘计数
  N2 文档规范「verify full N 段」 == verify_delivery EXPECTED_SECTION_NAMES 实数
  N3 gates.md 标题「（N 槽」自声明 == gates.md 顶层编号条目实数（W1291：对账锚移 gates.md）
  N4 stats.json pitfalls_total == 六主题正本「- **」聚合实数（W1291：与 stats 同源）
  N5 新Agent启动Prompt：A1-A6 总篇数 / 可视化页 / data HTML == stats.json 各键
用法：
  py -3 scripts/check_gov_doc_claims.py            # 报告（exit 0）
  py -3 scripts/check_gov_doc_claims.py --self-test
"""
from __future__ import annotations

import argparse
import ast
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 板块字母映射（文档权威形态·01-06 目录序 ≠ 字母序——W967 实证错位重灾区）
# 第三位 = 文档声明值（仅作交叉核验参照；判定一律取磁盘实算 disk[d]，不取本表）
BOARD_MAP = [(1, "A1", 100), (2, "A3", 215), (3, "A4", 209),
             (4, "A5", 42), (5, "A6", 19), (6, "A2", 44)]

# 计数位已接 <!--stats:KEY--> 标记（stats sweep 自动跟随）——散文断言须在**剥标记后的文本**上匹配：
# 否则「71<!--stats:gate_count--> 槽」被标记隔开数字与量词 ⇒ 断言误报「形态缺失」而非比对数值
RE_STAT_MARK = re.compile(r"<!--stats:[a-z_0-9]+-->")


def _strip_stat_markers(text):
    """剥掉 <!--stats:KEY--> 标记，得到与渲染后一致的散文文本。"""
    return RE_STAT_MARK.sub("", text)


def _read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8", newline="").read()


def _disk_board_counts():
    """docs/0N-*/ 顶层 .md 计数 → {1:100, ...}（子目录不计——口径同 stats a1_a6_docs）。"""
    out = {}
    skip = {"README.md", "index.md", "INDEX.md"}  # 生成件不入板块计数（口径同 stats a1_a6_docs）
    for d, _, _ in BOARD_MAP:
        pat = os.path.join(ROOT, "docs", "0%d-*" % d, "*.md")
        out[d] = len([f for f in glob.glob(pat) if os.path.basename(f) not in skip])
    return out


def _verify_sections():
    """读 EXPECTED_SECTION_NAMES 实数（段数）。

    W1210 根修：原实现用 `find("]")` 切分 + 去换行 + 按逗号 split —— 列表项的**行尾注释**
    （如 `"产物服务地址",  # W1208：…`）会把注释与**下一项**黏成一项，使计数虚高 1
    （真实 75 段被读成 76 段 ⇒ N2「文档规范段数 == verify 实数」长期假红）。
    改用 ast 精确解析（注释天然被忽略·不再依赖去换行的字符串手术）。
    """
    t = _read(os.path.join("scripts", "verify_delivery.py"))
    i = t.index("EXPECTED_SECTION_NAMES = [")
    j = t.index("]", i)
    tree = ast.parse(t[i:j + 1])
    return list(ast.literal_eval(tree.body[0].value))


def _gates_slot_count():
    t = _read(os.path.join("docs", "agent", "gates.md"))
    return len(re.findall(r"(?m)^\d+\. \*\*", t))


def _gates_declared_slots(text):
    """gates.md 标题自声明的槽数 → int 或 None（形态缺失时 None）。

    W1291 建：N3 的对账锚由 AGENTS 迁到 gates.md 本身——AGENTS §4.2 已于 W1279 迁出
    （全量定义在 gates.md），AGENTS 地图化后**不复述**槽数 ⇒ 旧判据「AGENTS 内含 N 槽，
    五组」必然形态缺失（假红）。新口径取 gates.md 标题的「（N 槽」自声明值，
    与编号条目实数对拍 ⇒ **加槽忘改标题即红**。
    """
    m = re.search(r"（(\d+)\s*槽", text)
    return int(m.group(1)) if m else None


def _pitfalls_count():
    """坑表条目实数（N4 对拍取数面）。

    W1160（P1-1）：W1157 正本迁根时本函数仍读 docs/agent/pitfalls.md 跳转壳（0 条目）⇒ 对拍失效。
    W1290：正本按六主题拆分为 docs/agent/pitfalls-topics/*.md，根 pitfalls.md 降级为**索引壳**
    （不含 `- **` 条目行）⇒ 读它会得 0 ⇒ 改为**聚合六主题正本**的 `- **` 行数，
    与 check_doc_sync / check_pitfall_id_unique 同口径（单一事实源：六主题正本）。
    """
    n = 0
    for rel in (
        "css-visual.md", "js-csp-runtime.md", "git-concurrency.md",
        "cascade-changelog.md", "data-trust.md", "flow-collab.md",
    ):
        t = _read(os.path.join("docs", "agent", "pitfalls-topics", rel))
        n += len([ln for ln in t.split("\n") if ln.startswith("- **")])
    return n


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

    # N3 槽数（W1291 判据侧追平·对账锚移 gates.md·与第 41 槽 C2 同源不重复造判据）
    #   旧口径要求 AGENTS 复述「内含 N 槽，五组」——§4.2 已于 W1279 迁出 ⇒ 必然形态缺失（假红）。
    #   新口径：**gates.md 标题自声明槽数 == gates.md 编号条目实数** ⇒ 加槽忘改标题即红；
    #   AGENTS 侧「路由表含 gates.md 触发行」由第 41 槽 C2 守护，本器不重复。
    slots = _gates_slot_count()
    declared_slots = _gates_declared_slots(_read(os.path.join("docs", "agent", "gates.md")))
    if declared_slots is None:
        fails.append("N3: gates.md 标题「（N 槽」槽数声明形态缺失（期望现役 %d 槽措辞）" % slots)
    elif declared_slots != slots:
        fails.append("N3: gates.md 标题声明 %d 槽 ≠ 编号条目实数 %d（加槽忘改标题）"
                     % (declared_slots, slots))
    else:
        lines.append("N3 槽数（gates.md 标题 %d == 编号条目 %d）：一致" % (declared_slots, slots))

    # N4 坑位数（W1291 判据侧追平·与 stats 同源·有判别力不恒真）
    #   旧口径要求 AGENTS 复述「N 条坑位按六主题迁」——该散文形态随 W1279 地图化 /
    #   W1290 坑表六主题拆分一并退役 ⇒ 必然形态缺失（假红）。
    #   新口径：**stats.json pitfalls_total == 六主题正本「- **」聚合实数**
    #   ⇒ stats sweep 与正本脱钩（改正本忘 sweep / 改 sweep 忘改正本）即红；
    #   另查 AGENTS 是否保留 <!--stats:pitfalls_total--> 标记（禁人工硬写数字绕过 sweep）。
    pn = _pitfalls_count()
    stats_total = (stats.get("pitfalls_total") or {}).get("value")
    agents_raw = _read("AGENTS.md")
    if stats_total is None:
        fails.append("N4: stats.json 缺 pitfalls_total 键（fail-closed·无法对拍坑位数）")
    elif int(stats_total) != pn:
        fails.append("N4: stats pitfalls_total=%s ≠ 六主题正本聚合实数 %d（stats 与正本脱钩）"
                     % (stats_total, pn))
    elif "<!--stats:pitfalls_total-->" not in agents_raw:
        fails.append("N4: AGENTS 缺 <!--stats:pitfalls_total--> 标记"
                     "（坑位数须由 stats 承载·禁人工硬写绕过 sweep）")
    else:
        lines.append("N4 坑位数（stats %s == 六主题聚合 %d）：一致" % (stats_total, pn))

    # N5 新Agent启动Prompt 三个统计键
    t = _read("docs/00-导读/新Agent启动Prompt.md")
    pairs = [(r"内容板块（(\d+) 篇）", "a1_a6_docs"),
             (r"可视化页 (\d+)（", "visualization_pages"),
             (r"共 (\d+) 个 HTML", "site_data_html"),
             # W1291：第 5 步「现役口径」行的 A1-A6 真实计数——与第 1 步「内容板块」同值，
             # 但旧判据只覆盖前者 ⇒ 同族陈旧数（W1290 时的 616）静默漏网 ⇒ 覆盖面补齐。
             (r"真实计数：\*\*(\d+) 篇\*\*", "a1_a6_docs")]
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
    """自测：注入漂移必须被报出（N1/N3/N4/N5 形态·合成数据·判据可证伪）。"""
    fails = []
    # N1 判据形态：正确行放行 / 错行（W967 实证错位形态）必报
    good = "`docs/02-人物深度分析/`（A3 人物谱系 215 篇）"
    bad = "`docs/02-人物深度分析/`（A2 人物随笔 44 篇）"
    pat = r"`docs/02-[^（]*`（A3 [^）]*?215 篇）"
    if not re.search(pat, good):
        fails.append("正确行未放行")
    if re.search(pat, bad):
        fails.append("错位行（W967 实证形态）未被判漂移——判据无效")
    # N3 判据形态：带 stats 标记的散文句须剥标记后命中（标记一插不致误报「形态缺失」）
    marked = "内含 71<!--stats:gate_count--> 槽，五组"
    m = re.search(r"内含 (\d+) 槽，五组", _strip_stat_markers(marked))
    if not (m and m.group(1) == "71"):
        fails.append("带标记的 N3 句未命中——剥标记判据无效")
    # N3 新口径（W1291·对账锚移 gates.md）：标题自声明槽数解析 + 负样本
    if _gates_declared_slots("# 交付门禁体系全量定义（83 槽 · L2 主题层）") != 83:
        fails.append("N3 新口径：标题声明「83 槽」未被解析出来")
    if _gates_declared_slots("# 交付门禁体系全量定义（L2 主题层）") is not None:
        fails.append("N3 新口径：标题无槽数声明时应返回 None（形态缺失须可判）")
    if _gates_declared_slots("# 交付门禁体系全量定义（82 槽 · L2 主题层）") == 83:
        fails.append("N3 新口径：82 槽声明不应等于 83（判据不可证伪）")
    # N5 覆盖面（W1291）：第 5 步「真实计数」形态必须可命中，缺形态须可判
    m5 = re.search(r"真实计数：\*\*(\d+) 篇\*\*",
                   "A1–A6 真实计数：**629 篇**（门禁算法）")
    if not (m5 and m5.group(1) == "629"):
        fails.append("N5 新增对：第 5 步「真实计数」形态未命中——覆盖面补齐失效")
    if re.search(r"真实计数：\*\*(\d+) 篇\*\*", "A1–A6 真实计数：629 篇（无加粗）"):
        fails.append("N5 新增对：未加粗形态不应被匹配（正样本形态须精确·勿放宽正则）")
    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：N1 错位形态必红 + N3 带标记句可命中 + N3 新锚（标题槽数）解析与负样本"
          " + N5 新增对形态精确性（判据可证伪）")
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
