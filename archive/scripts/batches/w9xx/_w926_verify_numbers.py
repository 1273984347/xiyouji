#!/usr/bin/env python3
"""W926 报告数字 · 机器对拍（报告文本 ↔ 证据 JSON 逐项断言）

用法：py -3 scripts/_w926_verify_numbers.py

判据（v2 · 经独立盲审一轮强化）：
  · 数字断言 = **等值判定**：从报告 needle 抽出数字集合，要求证据值 ∈ 集合。
    v1 用「子串包含」，证据 JSON 掉一位数字就会假通过（如 pages_total=85 vs 报告「857」、
    html_only_false_dead_count=7 vs 报告「= 17」），故废止。
  · 结构断言：按**小节标题**统计覆盖，不按「全文提及」统计（v1 的 S-05 以「提及」代「覆盖」，
    放过了一条没有详述小节的 R-05）。
  · 分段解析失败一律记具名 FAIL，不抛裸 traceback。
"""
from __future__ import annotations

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

fails: list[tuple] = []


def nums_in(needle: str) -> set[float]:
    """抽出 needle 里的全部数字（去千分位逗号，支持小数）。"""
    out = set()
    for s in re.findall(r"\d[\d,]*(?:\.\d+)?", needle):
        out.add(float(s.replace(",", "")))
    return out


def section(body: str, start: str, end: str) -> str | None:
    """取 [start, end) 段；段头缺失返回 None（由调用方记具名 FAIL）。"""
    if start not in body:
        return None
    tail = body.split(start, 1)[1]
    if end not in tail:
        return None
    return tail.split(end, 1)[0]


# ---------------------------------------------------------------- 数字断言
CHECKS = [
    ("N-01", "857 页", meta["pages_total"], "meta.pages_total"),
    ("N-02", "2,847 个控件", meta["controls_total"], "meta.controls_total"),
    ("N-03", "92.9%", round(L["pages_with_leak"] / meta["pages_total"] * 100, 1), "visible_leak 占比"),
    ("N-04", "796/857", L["pages_with_leak"], "visible_leak.pages_with_leak"),
    ("N-05", "6,827 处", L["visible_batch_terms"], "visible_leak.visible_batch_terms"),
    ("N-06", "814 处", L["visible_jargon_terms"], "visible_leak.visible_jargon_terms"),
    ("N-07", "最重页 134", L["rows"][0]["batch_n"], "visible_leak.rows[0].batch_n"),
    ("N-08", "118 个 fetch 页", ds["fetch_pages_count"], "D_states.fetch_pages_count"),
    ("N-09", "html_only_false_dead_count` = 17", ap["html_only_false_dead_count"], "A_paths.html_only_false_dead_count"),
    ("N-10", "broken_count` = 5", ap["broken_count"], "A_paths.broken_count"),
    ("N-11", "3 个表单", cf["forms_total"], "C_forms.forms_total"),
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

for cid, needle, value, src in CHECKS:
    in_report = needle in text
    nums = nums_in(needle)
    val_ok = float(value) in nums
    if in_report and val_ok:
        print(f"OK  {cid}  「{needle}」↔ 证据 {value}（{src}）")
    else:
        fails.append((cid, needle, value, src, in_report, val_ok))
        print(f"FAIL {cid}  「{needle}」 在报告={in_report} 含证据值={val_ok}（{src} = {value}）")

# ------------------------------------------------------------ 结构性断言
rows = re.findall(r"^\| \*\*R-(\d+)\*\* \|", text, re.M)
listed = set(rows)
head = re.search(r"### 0\.2 问题清单（(\d+) 条", text)
print(f"\n清单 R- 条数 = {len(rows)}（编号 {','.join(rows)}）· 节头 = {head.group(1) if head else '未找到'}")
if len(rows) != 12 or not head or int(head.group(1)) != 12:
    fails.append(("S-01", "R- 条数 / 节头", 12, "报告结构", True, True))
else:
    print("OK  S-01  §0.2 清单 12 行 · 节头声明 12 条")

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

# S-05：§2 详述必须**按小节标题**覆盖清单全部编号，且不得出现清单外编号
sec2 = section(text, "## 2. 问题清单详述", "## 3.")
if sec2 is None:
    fails.append(("S-05", "§2 详述覆盖 12 编号", "段落缺失", "报告 §2", False, False))
    print("FAIL S-05  §2 段落缺失（标题被改或删除）")
else:
    titles = re.findall(r"^### 2\.\d+ (.+)$", sec2, re.M)
    title_ids: set[str] = set()
    for t in titles:
        title_ids.update(re.findall(r"R-(\d+)", t))
    missing = sorted(listed - title_ids)
    extra = sorted(title_ids - listed)
    if not missing and not extra and len(title_ids) == 12:
        print(f"OK  S-05  §2 详述按小节标题覆盖全部 12 个编号（{len(titles)} 个小节·无遗漏·无清单外编号）")
    else:
        fails.append(("S-05", "§2 详述覆盖 12 编号", f"缺 {missing}·多 {extra}", "报告 §2", True, True))
        print(f"FAIL S-05  §2 缺 {missing}·多 {extra}")

# S-06：§1.3 判据自纠的表行数必须与节头声明的条数一致
sec13 = section(text, "### 1.3 判据自纠", "### 1.4")
m13 = re.search(r"判据自纠(.)条", text)
m13b = re.search(r"有(.)条是我的判据错", text)
if sec13 is None:
    fails.append(("S-06", "§1.3 条数自洽", "段落缺失", "报告 §1.3", False, False))
    print("FAIL S-06  §1.3 段落缺失")
else:
    n13_rows = len(re.findall(r"^\| \d+ \|", sec13, re.M))
    declared13 = m13.group(1) if m13 else ""
    if n13_rows == 4 and declared13 == "四" and m13b and m13b.group(1) == "四":
        print("OK  S-06  §1.3 判据自纠：表行数 4 == 节头声明「四条」== 正文「有四条」")
    else:
        fails.append(("S-06", "§1.3 条数自洽", f"表 {n13_rows} 行·声明「{declared13}条」", "报告 §1.3", True, True))
        print(f"FAIL S-06  §1.3 表 {n13_rows} 行·声明「{declared13}条」")

# S-07：§0.3 三批建议必须覆盖清单全部 12 个编号，且不得出现清单外编号
sec03 = section(text, "### 0.3 建议路线", "### 0.4 执行序重排")
if sec03 is None:
    sec03 = section(text, "### 0.3 建议路线", "## 1. 审查范围")
if sec03 is None:
    fails.append(("S-07", "§0.3 覆盖 12 编号", "段落缺失", "报告 §0.3", False, False))
    print("FAIL S-07  §0.3 段落缺失")
else:
    plan_ids = set(re.findall(r"R-(\d+)", sec03))
    missing_plan = sorted(listed - plan_ids)
    extra_plan = sorted(plan_ids - listed)
    if not missing_plan and not extra_plan:
        print("OK  S-07  §0.3 三批建议覆盖清单全部 12 个 R- 编号（无遗漏·无清单外编号）")
    else:
        fails.append(("S-07", "§0.3 覆盖 12 编号", f"缺 {missing_plan}·多 {extra_plan}", "报告 §0.3", True, True))
        print(f"FAIL S-07  §0.3 缺 {missing_plan}·多 {extra_plan}")

# S-08：§0.3 每个编号只出现一次（一个 R- 不得同时落进两批）
sec03b = section(text, "### 0.3 建议路线", "### 0.4 执行序重排")
if sec03b is None:
    sec03b = section(text, "### 0.3 建议路线", "## 1. 审查范围")
if sec03b is None:
    fails.append(("S-08", "§0.3 编号不重", "段落缺失", "报告 §0.3", False, False))
else:
    dup = sorted({r for r in re.findall(r"R-(\d+)", sec03b) if re.findall(r"R-(\d+)", sec03b).count(r) > 1})
    if not dup:
        print("OK  S-08  §0.3 每个 R- 编号只出现 1 次（无跨批重复）")
    else:
        fails.append(("S-08", "§0.3 编号不重", f"重复 {dup}", "报告 §0.3", True, True))
        print(f"FAIL S-08  §0.3 重复编号 {dup}")

# S-09：§2.9 的 17 条 JSON 下载链接明细必须与证据 JSON 逐条相等，且目标文件真实存在
sec29 = section(text, "### 2.9 R-09 / R-10", "## 3.")
if sec29 is None:
    fails.append(("S-09", "§2.9 17 条明细", "段落缺失", "报告 §2.9", False, False))
    print("FAIL S-09  §2.9 段落缺失")
else:
    rep_pairs = re.findall(r"`([0-9A-Za-z\-]+)`\s*→\s*`(json/[0-9A-Za-z_\-]+\.json)`", sec29)
    aud_map: dict[str, list[str]] = {}
    for x in ap["html_only_false_dead"]:
        aud_map.setdefault(x["page"].replace("data/", "").replace(".html", ""), []).append(x["href"])
    rep_map: dict[str, list[str]] = {}
    for page, href in rep_pairs:
        rep_map.setdefault(page, []).append(href)
    same = (len(rep_pairs) == 17
            and set(rep_map) == set(aud_map)
            and all(sorted(rep_map.get(k, [])) == sorted(v) for k, v in aud_map.items()))
    exists = all((ROOT / "site" / x["resolved"]).is_file() for x in ap["html_only_false_dead"])
    if same and exists:
        print("OK  S-09  §2.9 的 17 条 JSON 下载链接明细与证据 JSON 逐条相等·目标文件 17/17 存在")
    else:
        fails.append(("S-09", "§2.9 17 条明细", f"逐条一致={same}·文件存在={exists}", "报告 §2.9 vs A_paths", True, True))
        print(f"FAIL S-09  逐条一致={same}·文件存在={exists}")

# S-10：R-09 的两个内部工具页必须真实存在、零入链、且不在 sitemap
zero = set(ap["inbound_zero_pages"])
sitemap_file = ROOT / "site" / "sitemap.xml"
sitemap_text = sitemap_file.read_text(encoding="utf-8", errors="replace") if sitemap_file.is_file() else ""
sitemap = set(re.findall(r"<loc>([^<]+)</loc>", sitemap_text))
tools = ["rum-viewer.html", "visit-viewer.html"]
tools_exist = all((ROOT / "site" / t).is_file() for t in tools)
tools_zero = all(any(p.endswith(t) for p in zero) for t in tools)
tools_not_sitemap = all(not any(t in loc for loc in sitemap) for t in tools)
tools_in_report = all(f"`site/{t}`" in text for t in tools)
if tools_exist and tools_zero and tools_not_sitemap and tools_in_report:
    print("OK  S-10  R-09 两内部工具页：文件存在·零入链·不在 sitemap·报告路径写法一致")
else:
    fails.append(("S-10", "R-09 工具页", f"存在={tools_exist}·零入链={tools_zero}·不在sitemap={tools_not_sitemap}·报告路径={tools_in_report}", "site/ + A_paths + 报告", True, True))
    print(f"FAIL S-10  存在={tools_exist}·零入链={tools_zero}·不在sitemap={tools_not_sitemap}·报告路径={tools_in_report}")

# S-11：报告 §2.3 列出的 6 个不可达页必须都在证据的不可达清单内
unreach = set(ap["unreachable_from_index"])
r03_pages = ["reader/themes/index.html", "reader/culture/index.html", "reader/people/index.html",
             "data/customs-pass-route.html", "data/story-timeline.html", "en/customs-pass-route.html"]
sec23 = section(text, "### 2.3 R-03 / R-04", "### 2.4")
in_report = sec23 is not None and all(f"`{p}`" in sec23 for p in r03_pages)
in_evidence = all(p in unreach for p in r03_pages)
if in_report and in_evidence:
    print(f"OK  S-11  R-03 的 6 个不可达页：报告 §2.3 已列·且全在证据不可达清单（共 {len(unreach)} 页）内")
else:
    fails.append(("S-11", "R-03 6 页不可达", f"报告={in_report}·证据={in_evidence}", "报告 §2.3 vs A_paths", True, True))
    print(f"FAIL S-11  报告={in_report}·证据={in_evidence}")

# S-12：R-09 的零入链算式（9 = 2 内部工具 + 2 模板壳 + 1 404 + 4 个 R-03 页）
templates = {p for p in zero if p.endswith("_template.html") or p.endswith("_shell.html")}
r03_in_zero = {p for p in r03_pages if any(p.endswith(q) for q in zero)}
formula_ok = (len(zero) == 9 and len(tools) == 2 and len(templates) == 2
              and any(p.endswith("404.html") for p in zero) and len(r03_in_zero) == 4)
if formula_ok:
    print("OK  S-12  零入链 9 页算式成立：2 内部工具 + 2 模板壳 + 1 页 404 + 4 个 R-03 页")
else:
    fails.append(("S-12", "零入链算式", f"共 {len(zero)}·模板壳 {len(templates)}·R-03 {len(r03_in_zero)}", "A_paths.inbound_zero_pages", True, True))
    print(f"FAIL S-12  共 {len(zero)}·模板壳 {len(templates)}·R-03 {len(r03_in_zero)}")

# S-13：R-11 的 10 个真缺陷控件（5 个 id × 中英两份）必须真实存在且无任何标签关联
r11 = [("cross-time-danmaku.html", "user-message"),
       ("graph-explorer.html", "graphSel"),
       ("graph-explorer.html", "search"),
       ("journey-map-interactive.html", "routeSlider"),
       ("narrative-rhythm-curve.html", "chapterSlider")]
r11_problems: list[str] = []
r11_found = 0
for fname, cid_ in r11:
    for d in ("data", "en"):
        f = ROOT / "site" / d / fname
        if not f.is_file():
            r11_problems.append(f"{d}/{fname} 缺文件")
            continue
        html = f.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"<[a-zA-Z][^>]*\bid=\"" + re.escape(cid_) + r"\"[^>]*>", html)
        if not m:
            r11_problems.append(f"{d}/{fname}#{cid_} 不存在")
            continue
        tag = m.group(0)
        if re.search(r"aria-label|aria-labelledby|\btitle\s*=", tag):
            r11_problems.append(f"{d}/{fname}#{cid_} 带标签关联")
            continue
        r11_found += 1
if r11_found == 10 and not r11_problems:
    print("OK  S-13  R-11 的 10 个真缺陷控件（5 id × 中英各一份）均存在且无 aria-label/aria-labelledby/title")
else:
    fails.append(("S-13", "R-11 十控件", f"命中 {r11_found}/10·{r11_problems[:3]}", "site/ 实读", True, True))
    print(f"FAIL S-13  命中 {r11_found}/10·{r11_problems[:3]}")

# S-14：§0.4 执行序重排必须覆盖清单全部 12 个编号，且不得出现清单外编号
sec04 = section(text, "### 0.4 执行序重排", "## 1. 审查范围")
plan04: dict[str, set[str]] = {}
if sec04 is None:
    fails.append(("S-14", "§0.4 覆盖 12 编号", "段落缺失", "报告 §0.4", False, False))
    print("FAIL S-14  §0.4 段落缺失")
else:
    for ln in sec04.split("\n"):
        if re.match(r"^\| \*\*P\d\*\* \|", ln):
            cc = ln.split("|")
            plan04[cc[1].strip().strip("*")] = set(re.findall(r"R-(\d+)", cc[3]))
    all04 = set().union(*plan04.values()) if plan04 else set()
    missing04 = sorted(listed - all04)
    extra04 = sorted(all04 - listed)
    if not missing04 and not extra04 and len(all04) == 12:
        print(f"OK  S-14  §0.4 执行序覆盖清单全部 12 个编号（{len(plan04)} 个序位·无遗漏·无清单外编号）")
    else:
        fails.append(("S-14", "§0.4 覆盖 12 编号", f"缺 {missing04}·多 {extra04}", "报告 §0.4", True, True))
        print(f"FAIL S-14  §0.4 缺 {missing04}·多 {extra04}")

# S-15：守住两条排序原则 —— 阻断项（R-01）必须在首序；低成本项（R-05）不得被埋进多批次
if sec04 is not None and plan04:
    p0 = plan04.get("P0", set())
    p1 = plan04.get("P1", set())
    seq_ok = set(plan04) == {"P0", "P1", "P2", "P3", "P4"}
    if "01" in p0 and "05" in p1 and seq_ok:
        print("OK  S-15  §0.4 排序原则成立：R-01（唯一 100% 阻断）在 P0·R-05（10 分钟项）单列 P1·序位 P0–P4 完整")
    else:
        fails.append(("S-15", "§0.4 排序原则", f"P0={sorted(p0)}·P1={sorted(p1)}·序位={sorted(plan04)}", "报告 §0.4", True, True))
        print(f"FAIL S-15  P0={sorted(p0)}·P1={sorted(p1)}·序位={sorted(plan04)}")

N_STRUCT = 15
print("\n=== 对拍结果 ===")
if fails:
    print(f"{len(fails)} 项不一致：")
    for f in fails:
        print("  ", f)
    raise SystemExit(1)
print(f"全部 {len(CHECKS)} 项数字 + {N_STRUCT} 项结构断言通过")
