#!/usr/bin/env python3
"""W926 报告数字 · 机器对拍（报告文本 ↔ 证据 JSON 逐项断言）

用法：py -3 scripts/_w926_verify_numbers.py
判据：needle 必须出现在报告中；若给出 expected，则归一化后 needle 必须包含 expected 的值。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "docs" / "11-方案报告" / "审查与评审" / "站点交互流程审查复核报告-2026-10-25.md"
A = json.loads((ROOT / "scripts/output/_w926_ia_audit.json").read_text(encoding="utf-8"))
E = json.loads((ROOT / "scripts/output/_w926_ia_evidence.json").read_text(encoding="utf-8"))
L = json.loads((ROOT / "scripts/output/_w926_visible_leak.json").read_text(encoding="utf-8"))

text = REPORT.read_text(encoding="utf-8")
meta, ap, cf, ds, bs = A["meta"], A["A_paths"], A["C_forms"], A["D_states"], A["B_buttons"]


def norm(s) -> str:
    return re.sub(r"[,\s*`：，、]", "", str(s))


CHECKS = [
    ("N-01", "857 页", meta["pages_total"], "meta.pages_total"),
    ("N-02", "2,847 个控件", meta["controls_total"], "meta.controls_total"),
    ("N-04", "796/857", L["pages_with_leak"], "visible_leak.pages_with_leak"),
    ("N-05", "6,823 处", L["visible_batch_terms"], "visible_leak.visible_batch_terms"),
    ("N-06", "814 处", L["visible_jargon_terms"], "visible_leak.visible_jargon_terms"),
    ("N-07", "最重页 134", L["rows"][0]["batch_n"], "visible_leak.rows[0].batch_n"),
    ("N-08", "118 个 fetch 页", ds["fetch_pages_count"], "D_states.fetch_pages_count"),
    ("N-09", "html_only_false_dead_count` = 17", ap["html_only_false_dead_count"], "A_paths.html_only_false_dead_count"),
    ("N-10", "broken_count` = 5", ap["broken_count"], "A_paths.broken_count"),
    ("N-12", "可点击 `div/span` 共 **22** 个", bs["clickable_div_span"], "B_buttons.clickable_div_span"),
    ("N-13", "缺 role/tabindex 的假按钮 = 0", bs["clickables_missing_role_or_tabindex_count"], "B_buttons.clickables_missing_role_or_tabindex_count"),
    ("N-14", "当前 22", cf["controls_without_label_count"], "C_forms.controls_without_label_count"),
    ("N-15", "fetch_no_catch` = **0**", len(ds["fetch_no_catch"]), "D_states.fetch_no_catch 长度"),
    ("N-16", "页内锚点失效 = 0", ap["anchor_miss_count"], "A_paths.anchor_miss_count"),
    ("N-17", "外域新窗口缺 `rel=noopener` = 0", len(ap["external_blank_no_noopener"]), "A_paths.external_blank_no_noopener 长度"),
    ("N-18", "缺 viewport meta = 0", len(ds["pages_without_viewport"]), "D_states.pages_without_viewport 长度"),
    ("N-19", "`img` 缺 alt = 0", ds["imgs_no_alt_total"], "D_states.imgs_no_alt_total"),
    ("N-20", "211 链", E["hubs"]["reader/themes-hub.html"]["n_links"], "evidence.hubs[themes-hub].n_links"),
    ("N-21", "**622** 条链接", E["hubs"]["reader/index.html"]["n_links"], "evidence.hubs[reader/index].n_links"),
    ("N-22", "209 链", E["hubs"]["reader/themes/index.html"]["n_links"], "evidence.hubs[themes/index].n_links"),
]

fails = []
for cid, needle, value, src in CHECKS:
    in_report = needle in text
    val_ok = (norm(value) in norm(needle)) if value is not None else True
    if in_report and val_ok:
        print(f"OK  {cid}  「{needle}」↔ 证据 {value}（{src}）")
    else:
        fails.append((cid, needle, value, src, in_report, val_ok))
        print(f"FAIL {cid}  「{needle}」 在报告={in_report} 含证据值={val_ok}（{src} = {value}）")

# --- 结构性断言 ---
rows = re.findall(r"^\| \*\*R-(\d+)\*\* \|", text, re.M)
head = re.search(r"### 0\.2 问题清单（(\d+) 条", text)
print(f"\n清单 R- 条数 = {len(rows)}（编号 {','.join(rows)}）· 节头 = {head.group(1) if head else '未找到'}")
if len(rows) != 12 or not head or int(head.group(1)) != 12:
    fails.append(("S-01", "R- 条数 / 节头", 12, "报告结构", True, True))

# 排序断言：P1 组内 R-12 必须排在 R-05 之后、R-11（P3）之前
order = {rid: pos for pos, rid in enumerate(rows)}
if not (order.get("05", -1) < order.get("12", 99) < order.get("11", 99)):
    fails.append(("S-02", "排序 R-05 < R-12 < R-11", "05<12<11", "报告排序", True, True))
else:
    print("OK  S-02  排序：R-05(P1) → R-12(P1) → R-11(P3)")

# 证据自洽：R-12 的前提 —— site/data/ 无 index.html
data_index_exists = E["hubs"]["data/index.html"]["exists"]
if data_index_exists is False and "site/data/index.html" in text:
    print("OK  S-03  证据：site/data/index.html 不存在（= R-12 前提成立）")
else:
    fails.append(("S-03", "site/data/index.html 不存在", False, "evidence.hubs[data/index].exists", True, True))

# 证据自洽：按钮数 ≤ 控件数
if meta["buttons_total"] <= meta["controls_total"]:
    print(f"OK  S-04  证据自洽：按钮 {meta['buttons_total']} ≤ 控件 {meta['controls_total']}")
else:
    fails.append(("S-04", "buttons <= controls", "≤", "meta", True, True))

print("\n=== 对拍结果 ===")
if fails:
    print(f"{len(fails)} 项不一致：")
    for f in fails:
        print("  ", f)
    raise SystemExit(1)
print(f"全部 {len(CHECKS)} 项数字 + 4 项结构断言通过")
