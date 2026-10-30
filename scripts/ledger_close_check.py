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
# 级联段源（W996 判据 C2）：现役 + 归档一级 + tier2 容器/范围件——「查历史 W 号 grep 可见」的全体
CASCADE_SOURCES = (
    CHANGELOG_REL,
    os.path.join("archive", "docs", "CHANGELOG-ARCHIVE.md"),
    os.path.join("archive", "docs", "CHANGELOG-ARCHIVE-tier2.md"),
    os.path.join("archive", "docs", "CHANGELOG-ARCHIVE-tier2-W400-W559.md"),
)
# 合规零段形态（状态列含这些标记=有意不立段·豁免）
RE_NO_SEG_EXEMPT = re.compile(r"让号|并号|已停止|空壳|作废|补录|追记")

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


# ---- C3（W1053 P-01/P-02·W1046 方案）：修复类批 spec 五问 + 回归锁 ----
FIX_INTERROGATION_KEYS = ("why_red", "is_misjudge", "data_truth", "layer_changed", "prevention")


def is_fix_batch(w: int, subjects: list[str]) -> bool:
    """修复类判定：该批任一提交主题以 fix(w<号> 开头。"""
    return any(subj.lower().startswith("fix(w%d)" % w) for subj in subjects)


def check_fix_interrogation(w: int, spec_path: str, subjects: list[str]) -> list[str]:
    """C3：修复类顶段批的 spec 必填五问与回归锁（P-01/P-02·缺失即红）。"""
    why = []
    if not os.path.isfile(spec_path):
        return ["[C3] 修复类批但 spec 不存在：%s（P-01）" % spec_path]
    try:
        with open(spec_path, encoding="utf-8") as f:
            spec = json.load(f)
    except (OSError, ValueError) as e:
        return ["[C3] spec 解析失败：%s" % e]
    fi = spec.get("fix_interrogation")
    if not isinstance(fi, dict):
        why.append("[C3] 修复类批缺 fix_interrogation 五问对象（P-01·判据为何红/是否误判/数据真错/改哪层/防复发载体）")
    else:
        for k in FIX_INTERROGATION_KEYS:
            if not str(fi.get(k, "")).strip():
                why.append("[C3] 五问缺 %s（P-01）" % k)
    rl = spec.get("regression_lock")
    if not isinstance(rl, dict) or not str(rl.get("carrier", "")).strip():
        why.append("[C3] 缺回归锁载体 regression_lock.carrier（P-02·self-test case 或 tests/unit 文件）")
    elif not str(rl.get("case", "")).strip():
        why.append("[C3] 回归锁缺 case 标识（P-02）")
    return why


def check_cascade_segments(rows: dict[int, dict], seg_nums: set[int]) -> list[dict]:
    """C2 判据（W996 建·W995 形态回归锁）：**反向迭代台账**——已收官且 hash 落地（有 commit）
    的行，必须在级联段源（现役+归档两面）里有自己的段；没有 = 漏跑 batch_cascade（W995 实证：
    工具/拆分全入库而十面落点从未写入，C4 因台账认领行豁免放行、本工具旧判据因「无段不查」放行，
    双双漏过）。

    豁免（RE_NO_SEG_EXEMPT）：让号/并号/已停止/空壳/作废/补录/追记——有意不立段的合规形态。
    hash 占位行不查（无 commit 的记号行·归 preflight 在途态管）。
    """
    issues = []
    for w, r in sorted(rows.items()):
        if "error" in r:
            continue
        if not RE_DONE.match(re.sub(r"[\s*]+", "", r["status"])):
            continue  # 未收官行=在途态·归 preflight 管
        if RE_HASH_PLACEHOLDER.search(r["hash"].strip()):
            continue  # 无 commit·跳过
        if RE_NO_SEG_EXEMPT.search(r["status"]):
            continue  # 合规零段形态
        if w not in seg_nums:
            issues.append({"w": w, "ok": False,
                           "why": "已收官且 hash=%s 有 commit·但级联段源无自己的段——漏跑 batch_cascade（W995 形态）" % r["hash"][:20]})
    return issues


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

    # ---- C2 判据（W996·W995 形态回归锁）：已收官+有 commit+无级联段 → 红 ----
    rows_c2 = ledger_rows(
        "| W200 | 正常批 | def5678 | def5678 | **已收官**（def5678） | s | x |\n"
        "| W201 | 漏级联批 | aaa1111 | aaa1111 | **已收官**（aaa1111） | s | x |\n"
        "| W202 | 让号批 | — | — | **已收官**（让号留痕·取 W203） | s | — |\n"
        "| W203 | 并号批 | bbb2222 | bbb2222 | **已闭环**（并号入 W200） | s | x |\n"
    )
    seg_nums_c2 = {200}  # 段源只有 W200（W201 漏跑·W202 让号豁免·W203 并号豁免）
    issues = check_cascade_segments(rows_c2, seg_nums_c2)
    if [i["w"] for i in issues] != [201]:
        fails.append("C2 应只抓 W201（漏级联）：%s" % [i["w"] for i in issues])
    # 段源补上 W201 后必须转绿
    if check_cascade_segments(rows_c2, {200, 201}):
        fails.append("C2 段源补齐后应全绿")
    # 无 hash 行（让号占位）不查
    rows_c2b = ledger_rows("| W205 | 记号行 | —（待回填） | — | 已收官（记号） | s | — |\n")
    if check_cascade_segments(rows_c2b, set()):
        fails.append("C2 无 hash 行应跳过")

    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    # ---- C3（W1053 P-01/P-02）：修复类 spec 五问 + 回归锁 ----
    import tempfile
    with tempfile.TemporaryDirectory() as _td:
        _spec = os.path.join(_td, "s.json")
        _full = {"fix_interrogation": {"why_red": "x", "is_misjudge": "n", "data_truth": "y",
                                       "layer_changed": "判据层", "prevention": "C8"},
                 "regression_lock": {"carrier": "check_doc_sync.py --self-test T30", "case": "T30"}}
        with open(_spec, "w", encoding="utf-8") as f:
            json.dump(_full, f, ensure_ascii=False)
        if check_fix_interrogation(9999, _spec, ["fix(w9999): x"]):
            fails.append("C3 全字段 spec 应绿")
        _thin = {"fix_interrogation": {"why_red": "x"}, "regression_lock": {"carrier": "a"}}
        with open(_spec, "w", encoding="utf-8") as f:
            json.dump(_thin, f)
        _miss = check_fix_interrogation(9999, _spec, ["fix(w9999): x"])
        if not _miss or len(_miss) < 2:
            fails.append("C3 缺四问+缺 case 应两条红：%s" % _miss)
        if check_fix_interrogation(9999, os.path.join(_td, "nope.json"), ["feat(w9999): x"]):
            fails.append("C3 非修复类应跳过")
    print("自测通过：2 正例绿 + 4 负例红 + C2 三态（漏级联/让号并号豁免/无hash跳过）+ C3 三例（全绿/缺项红/非修复跳过）")
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
    # C2 判据（W996）：反向迭代台账——已收官+有 commit 的行必须有级联段（现役+归档两面合看）
    cascade_seg_nums = set()
    for rel in CASCADE_SOURCES:
        p = os.path.join(ROOT, rel)
        if os.path.isfile(p):
            cascade_seg_nums.update(section_w_nums(read_text(p)))
    cascade_issues = check_cascade_segments(ledger_rows(lg), cascade_seg_nums)
    for i in cascade_issues:
        # 已收官批次的漏级联是确定性缺陷（非在途态）——--allow-open 也不豁免
        bad.append({"w": i["w"], "ok": False, "why": i["why"], "cascade": True})
    # C3（W1053 P-01/P-02）：顶段号修复类 ⇒ spec 五问 + 回归锁必填
    c3_issues = []
    if not args.allow_open and nums:
        import subprocess as _sp
        _r = _sp.run(["git", "-c", "core.quotePath=false", "log", "--format=%s", "-40"],
                     cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        _subjects = (_r.stdout or "").splitlines()
        for _w in nums:
            if is_fix_batch(_w, _subjects):
                c3_issues.extend(check_fix_interrogation(
                    _w, os.path.join(ROOT, "scripts", "output", "_w%d_spec.json" % _w), _subjects))
    for why in c3_issues:
        bad.append({"w": nums[0] if nums else 0, "ok": False, "why": why, "c3": True})
    if args.json:
        print(json.dumps({"checked": len(results), "bad": len(bad),
                          "cascade_issues": cascade_issues, "results": results},
                         ensure_ascii=False, indent=1))
    else:
        for r in results:
            print(("OK   " if r["ok"] else "FAIL ") + "W%03d  %s" % (
                r["w"], ("hash=%s·状态=%s" % (r.get("hash", ""), r.get("status", ""))) if r["ok"]
                else r["why"]))
        for i in cascade_issues:
            print("FAIL  W%03d  [C2] %s" % (i["w"], i["why"]))
        for why in c3_issues:
            print("FAIL  [C3] %s" % why)
        print("---- 台账收官回填自检：%d 项检查·%d 项未收官·C2 漏级联 %d·C3 五问/回归锁 %d ----"
              % (len(results), len([r for r in results if not r["ok"]]), len(cascade_issues),
                 len(c3_issues)))
    # --allow-open 只豁免「未收官」伪阻塞态（在途批次自检用）；
    # C2 漏级联是已收官批次的确定性缺陷——连 --allow-open 也不豁免
    if (bad and not args.allow_open) or cascade_issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
