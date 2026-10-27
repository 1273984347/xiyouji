#!/usr/bin/env python3
"""gen_tools_inventory.py — scripts/ 顶层工具清单生成器（W985 建·P-44-05 同族：登记面跟手工较劲的最后一块搬进机器）。

产出 scripts/output/tools-inventory.md：顶层跟踪态工具（*.py|*.js|*.mjs）逐件清单，
用途取模块 docstring 首行（Node 取首条注释），类别按精确名覆盖 + 前缀规则。
全量清单由机器产出而非人写——手写清单必掉档（W824 定律）；本文件随
`gen_folder_docs.py --refresh` 刷新链自动再生成，亦可直跑。

用法：
  py -3 scripts/gen_tools_inventory.py            # 生成/刷新（落盘）
  py -3 scripts/gen_tools_inventory.py --check    # 对账模式：漂移 exit 1（CI/门禁候选）
  py -3 scripts/gen_tools_inventory.py --self-test
"""
from __future__ import annotations

import argparse
import ast
import datetime
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "output", "tools-inventory.md")

# 精确名覆盖（前缀规则判不准的批次生命周期工具·与 check_doc_size_budget 同期演进时此处同步）
CATEGORY_OVERRIDES = {
    "verify_delivery.py": "门禁与校验",
    "sync_docs.py": "门禁与校验",
    "preflight_check.py": "批次与登记",
    "batch_cascade.py": "批次与登记",
    "check_review_trigger.py": "批次与登记",
    "ledger_backfill.py": "批次与登记",
    "ledger_close_check.py": "批次与登记",
    "archive_ledger_rows.py": "批次与登记",
    "archive_segments.py": "批次与登记",
    "archive_file.py": "批次与登记",
    "release.py": "批次与登记",
    "release_prep.py": "批次与登记",
    "stats.py": "统计与对账",
    "judge_gate.py": "统计与对账",
    "fetch_gate_stats.py": "统计与对账",
    "tmpe_tidy.py": "运维与临时区",
}
PREFIX_RULES = (
    ("check_", "门禁与校验"),
    ("validate_", "门禁与校验"),
    ("lint_", "门禁与校验"),
    ("detect_", "门禁与校验"),
    ("verify_", "门禁与校验"),
    ("generate_", "生成与索引"),
    ("gen_", "生成与索引"),
    ("archive_", "批次与登记"),
    ("ledger_", "批次与登记"),
)
CAT_ONE_OFF = "一次性（下划线前缀）"
CAT_MISC = "工具"
CAT_ORDER = ("门禁与校验", "批次与登记", "统计与对账", "生成与索引", "运维与临时区", CAT_MISC, CAT_ONE_OFF)


def categorize(name: str) -> str:
    """类别判定：下划线前缀 > 精确名覆盖 > 前缀规则 > 工具。"""
    if name.startswith("_"):
        return CAT_ONE_OFF
    if name in CATEGORY_OVERRIDES:
        return CATEGORY_OVERRIDES[name]
    for prefix, cat in PREFIX_RULES:
        if name.startswith(prefix):
            return cat
    return CAT_MISC


def purpose_of(name: str, text: str) -> str:
    """用途=模块 docstring 首行（py）/ 首条注释（js|mjs）；取不到归 —。"""
    if name.endswith(".py"):
        try:
            doc = ast.get_docstring(ast.parse(text))
        except SyntaxError:
            doc = None
        if not doc:
            m = re.search(r'"""(.*?)"""', text, re.S) or re.search(r"'''(.*?)'''", text, re.S)
            doc = m.group(1) if m else ""
    else:
        m = re.search(r"^\s*/\*\*(.*?)\*/", text, re.S) or re.search(r"^\s*//\s*(.+)", text, re.M)
        doc = m.group(1) if m else ""
    for ln in (doc or "").splitlines():
        ln = ln.strip().lstrip("*").strip()
        if ln:
            return ln[:72]
    return "—"


def build_inventory(entries) -> str:
    """纯函数：[(文件名, 全文)] → 完整 markdown（含分类分节表）。"""
    rows = [(n, categorize(n), purpose_of(n, t)) for n, t in entries]
    rows.sort(key=lambda r: (CAT_ORDER.index(r[1]) if r[1] in CAT_ORDER else 99, r[0]))
    lines = [
        "# scripts/ 顶层工具清单（机器生成）",
        "",
        "> **本文件由 `scripts/gen_tools_inventory.py` 生成——禁手改**；刷新=`py -3 scripts/gen_folder_docs.py --refresh`"
        "（随目录文档刷新链）或直跑该脚本（`--check` 可对账）。",
        "> 范围=git 跟踪态顶层 `*.py|*.js|*.mjs`（子目录与 gitignore 本地件不在内）；用途=模块 docstring 首行。",
        "> 场景化路由（要做什么→用哪个）见 [../README.md](../README.md) 场景速查表。",
        "",
        "生成时间：{GENERATED_AT}",
        "",
    ]
    by_cat = {}
    for n, cat, p in rows:
        by_cat.setdefault(cat, []).append((n, p))
    lines.append("共 **%d** 件（%s）" % (len(rows), " · ".join("%s %d" % (c, len(by_cat[c])) for c in CAT_ORDER if c in by_cat)))
    lines.append("")
    for cat in CAT_ORDER:
        if cat not in by_cat:
            continue
        lines.append("## %s（%d）" % (cat, len(by_cat[cat])))
        lines.append("")
        lines.append("| 脚本 | 用途 |")
        lines.append("|:---|:---|")
        for n, p in by_cat[cat]:
            lines.append("| `%s` | %s |" % (n, p))
        lines.append("")
    return "\n".join(lines)


def collect_entries():
    """实盘取数：tracked 顶层工具 → [(name, text)]。"""
    import tracked_files as tf

    entries = []
    for name in sorted(tf.tracked_in_dir("scripts")):
        if "/" in name or not name.endswith((".py", ".js", ".mjs")):
            continue
        with open(os.path.join(HERE, name), encoding="utf-8", errors="replace") as fh:
            entries.append((name, fh.read()))
    return entries


def regen() -> int:
    """生成并落盘。返回件数。"""
    entries = collect_entries()
    text = build_inventory(entries)
    text = text.replace("{GENERATED_AT}", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return len(entries)


def check() -> int:
    entries = collect_entries()
    want = build_inventory(entries)
    have = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    # 只对账「共 **」起的表格主体——头部生成时间戳每次刷新恒异，不入判定
    body_want = want[want.index("共 **"):] if "共 **" in want else want
    body_have = have[have.index("共 **"):] if "共 **" in have else ""
    if body_want != body_have:
        print("DRIFT  tools-inventory.md 与实盘漂移——跑 python scripts/gen_tools_inventory.py 刷新")
        return 1
    print("OK    tools-inventory.md 与实盘零差异")
    return 0


def _self_test() -> int:
    fails = []
    # categorize：覆盖/前缀/一次性/兜底
    if categorize("_w977_scan.py") != CAT_ONE_OFF:
        fails.append("_ 前缀应归一次性")
    if categorize("check_js_syntax.py") != "门禁与校验":
        fails.append("check_ 前缀应归门禁")
    if categorize("check_review_trigger.py") != "批次与登记":
        fails.append("精确名覆盖应压过 check_ 前缀")
    if categorize("generate_csp.py") != "生成与索引" or categorize("gen_folder_docs.py") != "生成与索引":
        fails.append("generate_/gen_ 前缀应归生成")
    if categorize("tmpe_tidy.py") != "运维与临时区":
        fails.append("tmpe_tidy 精确覆盖失效")
    # purpose_of：py docstring / node 注释 / 兜底
    if not purpose_of("a.py", '"""批次开工前置核验。\n\n第二行"""').startswith("批次开工前置核验"):
        fails.append("py docstring 首行提取失败")
    if purpose_of("b.js", "// Playwright 批量截图\nconst x = 1;") == "—":
        fails.append("js 注释提取失败")
    if purpose_of("c.py", "x = 1") != "—":
        fails.append("无 docstring 应回退 —")
    # build_inventory：分节与计数
    md = build_inventory([("check_x.py", '"""门禁 X。"""'), ("_y.py", '"""一次性 Y。"""')])
    if "共 **2** 件" not in md or "## 门禁与校验（1）" not in md or "## 一次性（下划线前缀）（1）" not in md:
        fails.append("清单分节/计数异常")
    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：分类规则/用途提取/分节渲染（判据可证伪）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="scripts/ 顶层工具清单生成器（W985）")
    ap.add_argument("--check", action="store_true", help="对账模式：与磁盘漂移 exit 1")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    if args.check:
        return check()
    n = regen()
    print("OK    -> %s（%d 件）" % (os.path.relpath(OUT, ROOT), n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
