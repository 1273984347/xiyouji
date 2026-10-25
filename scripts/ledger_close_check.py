#!/usr/bin/env python3
"""ledger_close_check.py — 台账**收官回填**自检（W931 共享面串行化机制·层 2 判据 C）

病根
----
`preflight_check.py` 的在途判定读**台账字段**（状态列不以「已收官/已闭环」开头即在途），
而不是 git 历史 ⇒ **「事实已收官、字段没回填」= 伪阻塞**：该批永久占着 touches 挡死后来者。

W930 实证：W928 早已提交收官（`57762fa3`），台账行状态列仍是「在途」⇒
W930 布局批全部工序就绪却被 preflight 拒绝开工，而门禁只显示「与在途 W928 冲突」，
看不出真实原因是对方早已收官。

本脚本 = 收官回填的**事后体检**：凡 CHANGELOG 现役段的 W 号，在台账里必须
① hash 列非占位、② 状态列以「已收官/已闭环」开头 —— 否则该批的收官回填漏了。

用法
----
  py -3 scripts/ledger_close_check.py               # 检查现役段（默认）
  py -3 scripts/ledger_close_check.py --all-sections # 检查全部 ### WNNN 段
  py -3 scripts/ledger_close_check.py --allow-open   # 只报告不判红（在途批次自检用）
  py -3 scripts/ledger_close_check.py --json         # 机器可读输出
  py -3 scripts/ledger_close_check.py --self-test    # 自测（3 正例 + 4 负例）

**挂载说明（重要）**：本脚本**默认不挂进 verify_delivery.py**——挂进去会让
「现役段未收官」直接把在途批次判红（等于把伪阻塞从 preflight 挪到门禁）。
正确挂载时机：**全部在途批次收官后**再挂，或只挂 `--allow-open` 的提示型用法。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ledger_backfill import locate_cells  # noqa: E402  同目录复用列定位（单一事实源）

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER_REL = "docs/00-导读/W批次编号对账表.md"
CHANGELOG_REL = "CHANGELOG.md"

RE_SECTION_HEAD = re.compile(r"^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（[^）]*）)", re.M)
RE_W_ROW = re.compile(r"^\|\s*W(\d{3,4})\s*\|")
RE_DONE = re.compile(r"^(?:已收官|已闭环)")
# hash 列的占位形态：空 / 破折号开头 / 含「待回填」/「认领登记」/「施工中」
#   用 search 而非 match——占位词常被包在括注里（如「—（待回填）」），match 只能匹配到串首。
RE_HASH_PLACEHOLDER = re.compile(r"^(?:—|-|－|无|\(空\)|（空）)|待回填|认领登记|施工中")


def read_text(path: str) -> str:
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def section_w_nums(changelog: str) -> list[int]:
    """CHANGELOG 里的 W 号段（按出现顺序）。"""
    out = []
    for m in RE_SECTION_HEAD.finditer(changelog):
        out.append(int(m.group(1) or m.group(2)))
    return out


def active_w(changelog: str) -> int | None:
    """现役段 W 号 = 第一个（最新）段。"""
    nums = section_w_nums(changelog)
    return nums[0] if nums else None


def ledger_rows(ledger: str) -> dict[int, dict]:
    rows: dict[int, dict] = {}
    for line in ledger.splitlines():
        m = RE_W_ROW.match(line)
        if not m:
            continue
        cells = line.split("|")
        try:
            loc = locate_cells(cells)
        except ValueError:
            rows[int(m.group(1))] = {"error": "列数不足·无法定位"}
            continue
        rows[int(m.group(1))] = {
            "hash": cells[loc["hash"]].strip(),
            "status": cells[loc["status"]].strip(),
            "touches": cells[loc["touches"]].strip(),
        }
    return rows


def check(changelog: str, ledger: str, targets: list[int]) -> list[dict]:
    rows = ledger_rows(ledger)
    results = []
    for w in targets:
        r = rows.get(w)
        if r is None:
            results.append({"w": w, "ok": False, "why": "台账中无该 W 行（认领行缺失）"})
            continue
        if "error" in r:
            results.append({"w": w, "ok": False, "why": r["error"]})
            continue
        h, s = r["hash"], r["status"]
        norm_s = re.sub(r"[\s*]+", "", s)
        if RE_HASH_PLACEHOLDER.search(h.strip()):
            results.append({"w": w, "ok": False, "why": "hash 列仍是占位：「%s」" % h})
            continue
        if not RE_DONE.match(norm_s):
            results.append({"w": w, "ok": False, "why": "状态列未以「已收官/已闭环」开头：「%s」" % s})
            continue
        results.append({"w": w, "ok": True, "hash": h, "status": s})
    return results


def _self_test() -> int:
    """自测：正例必绿 + 负例必红（负例红不了 ⇒ 判据无效）。"""
    fails = []
    good_ledger = (
        "| W100 | 已收官批 | abc1234（内容批） | abc1234（级联） | **已收官**（abc1234·全绿） | 主会话 | a.py |\n"
    )
    chg = "### W100（2026-10-25）：测试批\n\n内容\n"

    # 正例 1：已回填 → 绿
    res = check(chg, good_ledger, [100])
    if not (len(res) == 1 and res[0]["ok"]):
        fails.append("正例1 已回填应判绿")
    # 负例 1：hash 占位 → 红
    res = check(chg, good_ledger.replace("abc1234（内容批）", "—（待回填）"), [100])
    if res and res[0]["ok"]:
        fails.append("负例1 hash 占位必须判红")
    # 负例 2：状态未收官 → 红
    res = check(chg, good_ledger.replace("**已收官**（abc1234·全绿）", "在途（认领·未收官）"), [100])
    if res and res[0]["ok"]:
        fails.append("负例2 状态未收官必须判红")
    # 负例 3：台账无该行 → 红
    res = check(chg, "", [100])
    if res and res[0]["ok"]:
        fails.append("负例3 台账无该行必须判红")
    # 负例 4：状态列不以「已收官/已闭环」开头 → 红
    #   （口径与 preflight 的 is_inflight 一致：前缀匹配·「已收官计划中」仍算已收官·不判红）
    res = check(chg, good_ledger.replace("**已收官**（abc1234·全绿）", "收官中（待回填）"), [100])
    if res and res[0]["ok"]:
        fails.append("负例4 状态前缀不匹配必须判红")
    # 正例 2：现役段取号 = 第一个段
    if active_w("### W101（2026-10-25）：新\n\n### W100（2026-10-25）：旧\n") != 101:
        fails.append("正例2 现役段取号应为 101")

    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：2 正例绿 + 4 负例红（判据可证伪）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="台账收官回填自检（W931 判据 C）")
    ap.add_argument("--all-sections", action="store_true", help="检查全部 W 段（默认只查现役段）")
    ap.add_argument("--allow-open", action="store_true", help="只报告不判红（在途批次自检用）")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    ap.add_argument("--self-test", action="store_true", help="自测")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()

    cl_path = os.path.join(ROOT, CHANGELOG_REL)
    lg_path = os.path.join(ROOT, LEDGER_REL)
    for p in (cl_path, lg_path):
        if not os.path.isfile(p):
            print("FAIL  文件不存在：%s" % p)
            return 1
    cl = read_text(cl_path)
    lg = read_text(lg_path)
    nums = section_w_nums(cl) if args.all_sections else ([active_w(cl)] if active_w(cl) else [])
    if not nums:
        print("FAIL  CHANGELOG 未定位到任何 W 段")
        return 1
    results = check(cl, lg, nums)
    bad = [r for r in results if not r["ok"]]
    if args.json:
        print(json.dumps({"checked": len(results), "bad": len(bad), "results": results},
                         ensure_ascii=False, indent=1))
    else:
        for r in results:
            print(("OK   " if r["ok"] else "FAIL ") + "W%03d  %s" % (
                r["w"], ("hash=%s·状态=%s" % (r.get("hash", ""), r.get("status", ""))) if r["ok"]
                else r["why"]))
        print("---- 台账收官回填自检：%d 项检查·%d 项未收官 ----" % (len(results), len(bad)))
    if bad and not args.allow_open:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
