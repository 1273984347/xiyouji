#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""W954 第 43 篇工作复盘 · 三源取证脚本（区间 W795–W953）

用途：把「工作复盘」所需的事实从三个权威面抽出来，产出机器可读 JSON，
      避免报告里的任何统计数字靠人工估计（本脚本是数字的唯一源头）。

三源口径：
  ① CHANGELOG 现役段标题 `### W###（YYYY-MM-DD）：标题` —— 批次主题与日期的权威登记；
  ② W 批次编号对账表 —— 并发对账与状态列的权威（状态以本表为准）；
  ③ git 提交图 —— 实际提交面（含 body 里的 W 标记），用于统计每批提交数与每日节奏。

输出：scripts/output/_w954_review_evidence.json
用法：py -3 scripts/_w954_review_evidence.py [--from-w 795] [--to-w 953] [--quiet]
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
# 归档面：W736 起分批归档 CHANGELOG 段——现役 + 归档两面合看才是完整登记面（W954 取证发现）
CHANGELOG_ARCHIVE = os.path.join(ROOT, "archive", "docs", "CHANGELOG-ARCHIVE.md")
LEDGER = os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md")
OUT_JSON = os.path.join(ROOT, "scripts", "output", "_w954_review_evidence.json")

# 复盘起点 = 第 42 篇复盘收官时刻（2026-10-19 01:10 · W795 入库）
SINCE = "2026-10-19 01:10"

SEG_RE = re.compile(r"^###\s*W(\d{3,4})\s*[（(](\d{4}-\d{2}-\d{2})[）)]\s*[：:]\s*(.+?)\s*$", re.M)
SEG_LOOSE_RE = re.compile(r"^###\s*W(\d{3,4})\b.*$", re.M)
LEDGER_ROW_RE = re.compile(r"^\|\s*W(\d{3,4})\s*\|", re.M)
COMMIT_W_RE = re.compile(r"[wW](\d{3,4})")

# 主题分组规则（按序匹配，命中即止；关键词取自本区间 141 个实测段标题词面）
GROUPS = [
    ("素材图与题图流水线", ["题图", "素材图", "素材", "插画", "hero", "plate", "图标", "emoji", "拼图", "封面", "配图", "画廊", "图集", "题图", "图审查"]),
    ("设计迁移与视觉令牌", ["设计迁移", "令牌", "朱砂", "对比度", "间距", "容器归并", "迁移", "色", "调色", "版式"]),
    ("阅读页重建与内容回灌", ["阅读页", "回灌", "阅读入口", "正文"]),
    ("交互与界面走查", ["交互", "界面", "布局", "导航", "动线", "可访问", "首屏"]),
    ("审查与评审", ["审查", "走查", "评审", "审计", "复核", "对抗", "复审", "盘点", "核查", "治理"]),
    ("架构与设计方案", ["架构", "选型", "设计语言", "取经编制表", "编制表"]),
    ("递延补段与元规则门禁", ["递延", "补段", "补写", "对账", "门禁", "元规则", "护栏", "规则", "收敛", "机制", "口径", "规范", "登记"]),
    ("工具链与工程加固", ["工具链", "加固", "ci", "工作流", "暴露面", "安装包", "热修", "守卫", "agent-web", "服务端", "测试", "shell", "坑"]),
    ("品牌与宣传物料", ["logo", "品牌", "宣传", "单页", "物料", "投放", "社媒"]),
    ("索引与搜索", ["索引", "搜索", "检索"]),
    ("数据与观测", ["数据", "取数", "观测", "退役", "采样", "统计", "postgresql"]),
    ("计划与执行报告", ["执行前计划", "任务计划", "待办", "计划方案"]),
]


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def git_lines(args):
    r = subprocess.run(["git"] + args, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=120)
    return r.stdout.splitlines()


def classify(title):
    t = title.lower()
    for name, kws in GROUPS:
        for kw in kws:
            if kw.lower() in t:
                return name
    return "其他"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-w", type=int, default=795)
    ap.add_argument("--to-w", type=int, default=953)
    ap.add_argument("--quiet", action="store_true")
    args, _unknown = ap.parse_known_args()

    # ① CHANGELOG 两面（现役 + 归档）：归档段同样计入登记面——只读现役会漏 W795 等已归档段
    segs = {}
    loose_only = {}
    for src, path in (("现役", CHANGELOG), ("归档", CHANGELOG_ARCHIVE)):
        if not os.path.exists(path):
            continue
        cl = read_text(path)
        bounds = [(m.start(), m.group(1), m.group(2), m.group(3))
                  for m in SEG_RE.finditer(cl)]
        strict_ws = {int(b[1]) for b in bounds}
        for m in SEG_LOOSE_RE.finditer(cl):
            lw = int(m.group(1))
            if args.from_w <= lw <= args.to_w and lw not in strict_ws:
                loose_only.setdefault(lw, m.group(0)[:90])
        for i, (pos, w_s, d, title) in enumerate(bounds):
            w = int(w_s)
            if not (args.from_w <= w <= args.to_w):
                continue
            end = bounds[i + 1][0] if i + 1 < len(bounds) else len(cl)
            body = cl[pos:end]
            st_m = re.search(r"\*\*状态\*\*[：:]\s*(.+)", body)
            st_txt = st_m.group(1).strip() if st_m else ""
            rec = {"w": w, "date": d, "title": title.strip(),
                   "changelog_status": st_txt[:200],
                   # 口径漂移：现役段写「已收官/已闭环」，归档段写「已落地」——三词同义
                   "changelog_closed": any(k in st_txt for k in ("已收官", "已闭环", "已落地")),
                   "segment_source": src}
            if w not in segs:          # 现役优先
                segs[w] = rec
            else:
                rec["segment_source"] = "现役+归档"
                segs[w] = rec

    # ② 对账表状态列
    led = read_text(LEDGER)
    status = {}
    for line in led.splitlines():
        m = LEDGER_ROW_RE.match(line)
        if not m:
            continue
        w = int(m.group(1))
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5:
            st = cells[4]
            closed = "已收官" in st or "已闭环" in st
            # 在途判定只看状态字段「开头」的标记词——描述正文里出现的「在途」二字不算
            head = st[:24]
            in_flight = (head.startswith("在途") or head.startswith("**进行中**")
                         or "认领·未收官" in head)
            status[w] = {"raw": st[:400], "closed": closed, "in_flight": in_flight}

    # ③ 提交图
    raw = git_lines(["log", f"--since={SINCE}", "--format=%H\t%ad\t%s", "--date=format:%Y-%m-%d %H:%M"])
    commits = []
    per_batch = defaultdict(list)
    daily = Counter()
    type_cnt = Counter()
    multi_w = []
    for line in raw:
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        sha, when, subject = parts[0], parts[1], parts[2]
        commits.append({"sha": sha[:8], "when": when, "subject": subject})
        daily[when[:10]] += 1
        m = re.match(r"^(\w+)(?:\(([^)]*)\))?:", subject)
        if m:
            type_cnt[m.group(1)] += 1
        ws = [int(x) for x in COMMIT_W_RE.findall(subject)]
        if ws:
            per_batch[ws[0]].append(sha[:8])
            if len(set(ws)) > 1:
                multi_w.append({"sha": sha[:8], "ws": ws, "subject": subject[:80]})

    # 合并
    rows = []
    for w in sorted(segs):
        s = segs[w]
        st = status.get(w, {})
        rows.append({
            "w": w,
            "date": s["date"],
            "title": s["title"],
            "group": classify(s["title"]),
            "segment_source": s["segment_source"],
            "changelog_closed": s["changelog_closed"],
            "ledger_closed": st.get("closed"),
            "ledger_in_flight": st.get("in_flight"),
            "commits": len(per_batch.get(w, [])),
        })

    groups = defaultdict(list)
    for r in rows:
        groups[r["group"]].append(r["w"])

    # ④ 登记面漂移分类（事实源 = git；声明源 = 台账 / CHANGELOG 段状态字段）
    drift = {"A_台账滞后": [], "B_CHANGELOG状态滞后": [], "C_零提交未收官": [],
             "D_台账有行无段": [], "E_有段台账无行": []}
    row_by_w = {r["w"]: r for r in rows}
    for w in sorted(status):
        if not (args.from_w <= w <= args.to_w):
            continue
        n_commits = len(per_batch.get(w, []))
        st = status[w]
        r = row_by_w.get(w)
        if n_commits == 0:
            drift["C_零提交未收官"].append(w)
        else:
            if st["in_flight"]:
                drift["A_台账滞后"].append(w)
            if r is not None and not r["changelog_closed"]:
                drift["B_CHANGELOG状态滞后"].append(w)
    drift["D_台账有行无段"] = [w for w in status
                              if args.from_w <= w <= args.to_w and w not in segs]
    drift["E_有段台账无行"] = [w for w in segs if w not in status]

    out = {
        "range": {"from_w": args.from_w, "to_w": args.to_w, "since": SINCE},
        "totals": {
            "changelog_segments": len(rows),
            "ledger_rows_in_range": sum(1 for w in status if args.from_w <= w <= args.to_w),
            "commits_since": len(commits),
            "days": len(daily),
            "closed_batches": sum(1 for r in rows if r["ledger_closed"]),
            "in_flight_batches": sum(1 for r in rows if r["ledger_in_flight"]),
        },
        "only_changelog": sorted(w for w in segs if w not in status),
        "only_ledger": sorted(w for w in status if args.from_w <= w <= args.to_w and w not in segs),
        "loose_segment_titles": {str(k): v for k, v in sorted(loose_only.items())},
        "drift": drift,
        "daily_commits": dict(sorted(daily.items())),
        "commit_types": dict(type_cnt.most_common()),
        "groups": {g: {"count": len(ws), "w_list": ws} for g, ws in sorted(groups.items(), key=lambda kv: -len(kv[1]))},
        "rows": rows,
        "commits": commits,
        "multi_w_commits": multi_w,
    }

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    if not args.quiet:
        t = out["totals"]
        print("== W954 复盘取证摘要 ==")
        print(f"区间 W{args.from_w}–W{args.to_w}：CHANGELOG 段 {t['changelog_segments']} 条 · "
              f"对账表行 {t['ledger_rows_in_range']} 行 · 提交 {t['commits_since']} 笔 / {t['days']} 天")
        print(f"状态：已收官/已闭环 {t['closed_batches']} 批 · 标「在途/进行中」{t['in_flight_batches']} 批")
        print("\n-- 每日提交 --")
        for d, c in out["daily_commits"].items():
            print(f"  {d}  {'#' * min(c, 60)} {c}")
        print("\n-- 主题分组 --")
        for g, info in out["groups"].items():
            wl = info["w_list"]
            print(f"  {g}（{info['count']} 批）: W{wl[0]}–W{wl[-1]}  {wl}")
        print("\n-- 在途/进行中（台账状态，需回写或说明）--")
        for r in rows:
            if r["ledger_in_flight"]:
                print(f"  W{r['w']} {r['date']} 提交{r['commits']}  {r['title'][:56]}")
        print("\n-- 登记面漂移分类（事实源=git·声明源=登记面）--")
        for k, v in out["drift"].items():
            print(f"  {k}: {len(v)} 批 {v}")
        print("\n-- 提交类型分布 --")
        for k, v in out["commit_types"].items():
            print(f"  {k}: {v}")
        print("\n-- 提交数 TOP 12 --")
        for r in sorted(rows, key=lambda x: -x["commits"])[:12]:
            print(f"  W{r['w']} {r['date']} 提交{r['commits']}  {r['title'][:56]}")
        print("\n-- 零提交批次（有登记但 git 无提交 ⇒ 未收官）--")
        zero = [r["w"] for r in rows if r["commits"] == 0]
        print(f"  {zero}")
        print("\n-- CHANGELOG 段状态未标「已收官/已闭环」--")
        nc = [(r["w"], r["title"][:38]) for r in rows if not r["changelog_closed"]]
        for w, t in nc:
            print(f"  W{w}  {t}")
        print(f"  合计 {len(nc)} 批")
        print("\n-- 登记面差集 --")
        print(f"  有段·台账无行: {out['only_changelog']}")
        print(f"  台账有行·两面都无段: {out['only_ledger']}")
        if out["loose_segment_titles"]:
            print(f"  段标题格式变体（严格正则未命中）: {out['loose_segment_titles']}")
        print("\n-- 每日批次分布（CHANGELOG 段）--")
        per_day = defaultdict(list)
        for r in rows:
            per_day[r["date"]].append(r["w"])
        for d in sorted(per_day):
            print(f"  {d}  {len(per_day[d])} 批  {per_day[d]}")
        if "--dump-other" in sys.argv:
            print("\n-- 未归组批次的段标题（供扩关键词）--")
            for r in rows:
                if r["group"] == "其他":
                    print(f"  W{r['w']} {r['date']}  {r['title'][:72]}")
        print(f"\nJSON → {os.path.relpath(OUT_JSON, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
