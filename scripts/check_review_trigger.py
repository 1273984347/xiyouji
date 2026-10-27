#!/usr/bin/env python3
"""check_review_trigger.py — 复盘触发器（W956 建 · W954 复盘报告 P-43-02 / WF-08-b）。

背景：第 42→43 篇复盘之间断档 6 天 23 小时 / 159 个 W 号零复盘——该系列建立以来最长空窗，
而仓内对「复盘周期」没有任何机器防线：触发条款只写在复盘报告里、靠人记得，与 W824 干扰日志
「无机器触发点必掉档」同构（那条的实证 = 条款写得很硬仍断档 4 天 128 提交零登记）。
本脚本把「该复盘了」变成机器提示：任一判据成立即输出触发清单。

判据（三选一即触发，源自 P-43-02；与 P-43-01 登记面机器化同批落地——登记面状态不可信时
触发器会同样误判，故批次数口径自带排除规则、提交口径直接读 git 不经登记面）：
  T1 距上篇复盘 ≥ 3 天（上篇复盘 = CHANGELOG 现役+归档两面中标题含「工作复盘」的最高段）；
  T2 上篇复盘之后的台账批次 ≥ 30（排除让号留痕 / 已停止行——不是批次）；
  T3 上篇复盘之后的提交数 ≥ 80（git log --since 上篇复盘日期 00:00，含复盘批当日提交，
     边界最多多计复盘批自己的收官提交·相对 80 阈值可忽略）。

只提示不拦截：exit 恒 0，供 preflight 提示位（W956 接线·W822「只提示不改判定」语义）与
批收尾手工调用；「待复盘」的台账标注由下一个批次按提示以认领流程执行——本脚本**不持台账
写面**（检查器写共享面会引入新的并发写风险，W820 教训）。

用法：
  py -3 scripts/check_review_trigger.py            # 打印状态（exit 0）
  py -3 scripts/check_review_trigger.py --self-test
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANGELOG = os.path.join("CHANGELOG.md")
CHANGELOG_ARCHIVE = os.path.join("archive", "docs", "CHANGELOG-ARCHIVE.md")

RE_SEG_HEAD = re.compile(r"^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（(20\d{2}-\d{2}-\d{2})）：)([^\n]*)", re.M)
RE_LEDGER_ROW = re.compile(r"^\|\s*W(\d{3,4})\s*\|")
# 非批次行：让号留痕（占号无产出属合规登记）与已停止（零提交会话终止·W954 标注口径）
NON_BATCH_MARKS = ("让号留痕", "已停止")
THRESHOLDS = {"days": 3, "batches": 30, "commits": 80}


def find_last_review(changelog_text):
    """CHANGELOG 文本（现役+归档拼接·降序）→ 上篇复盘 (w, date, title)；无则 None。

    纯函数：识别口径 = 段标题含「工作复盘」（第 N 篇工作复盘批的段标题均含此四字）。
    """
    for m in RE_SEG_HEAD.finditer(changelog_text):
        w = int(m.group(1) or m.group(2))
        date = m.group(3) or ""
        title = m.group(4) or ""
        if "工作复盘" in title:
            return {"w": w, "date": date, "title": title.strip()}
    return None


def batches_since(ledger_text, last_w):
    """上篇复盘之后的台账批次行数（排除让号留痕 / 已停止行）——纯函数。

    排除标记只扫**行尾状态区**（split 后末 4 格：状态/会话/touches/尾空）——
    描述列散文提及「让号留痕」（如本工具自己的批次行）不构成非批次行。
    """
    n = 0
    for line in ledger_text.splitlines():
        m = RE_LEDGER_ROW.match(line)
        if not m or int(m.group(1)) <= last_w:
            continue
        cells = line.split("|")
        status_zone = "|".join(cells[-4:]) if len(cells) >= 6 else line
        if any(mark in status_zone for mark in NON_BATCH_MARKS):
            continue
        n += 1
    return n


def evaluate(today, last_date, batches, commits, thresholds=None):
    """三判据评估 → 触发原因清单（空 = 未触发）——纯函数（today 由调用方注入·可测）。"""
    th = thresholds or THRESHOLDS
    triggered = []
    try:
        d0 = datetime.date.fromisoformat(last_date)
        days = (today - d0).days
    except (ValueError, TypeError):
        days = None
    if days is None:
        triggered.append("T1 距上篇复盘 ≥{} 天（上篇日期不可解析：{}——按已触发处理·人工核对）".format(
            th["days"], repr(last_date)))
    elif days >= th["days"]:
        triggered.append("T1 距上篇复盘 %d 天 ≥ %d 天" % (days, th["days"]))
    if batches >= th["batches"]:
        triggered.append("T2 上篇复盘后批次 %d ≥ %d" % (batches, th["batches"]))
    if commits >= th["commits"]:
        triggered.append("T3 上篇复盘后提交 %d ≥ %d" % (commits, th["commits"]))
    return triggered


def _git_commits_since(git, date):
    """git log --since 计数（读 git 不经登记面——P-43-01 口径）。失败返回 None（调用方降级）。"""
    try:
        r = subprocess.run([git, "log", "--since=%s 00:00" % date, "--format=%h"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=60)
        if r.returncode != 0:
            return None
        return len([x for x in r.stdout.splitlines() if x.strip()])
    except (OSError, subprocess.TimeoutExpired):
        return None


def collect(git):
    """实盘取数（CHANGELOG 两面合看·台账全量·git 计数）→ 信息 dict（供 render/单测）。"""
    texts = []
    for rel in (CHANGELOG, CHANGELOG_ARCHIVE):
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                texts.append(f.read())
    review = find_last_review("\n".join(texts)) if texts else None
    info = {"review": review, "days": None, "batches": None, "commits": None, "errors": []}
    if review is None:
        info["errors"].append("现役+归档两面均未找到「工作复盘」段——复盘系列定位失败")
        return info
    ledger_p = os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md")
    ledger = open(ledger_p, encoding="utf-8").read() if os.path.exists(ledger_p) else ""
    info["batches"] = batches_since(ledger, review["w"])
    try:
        d0 = datetime.date.fromisoformat(review["date"])
        info["days"] = (datetime.date.today() - d0).days
    except (ValueError, TypeError):
        info["errors"].append("上篇复盘日期不可解析：%r" % review["date"])
    info["commits"] = _git_commits_since(git, review["date"])
    if info["commits"] is None:
        info["errors"].append("git 提交计数失败——T3 判据本回合不可判定")
    return info


def render(info):
    """信息 dict → 提示行清单（触发行以 ⚠ 开头·preflight 提示位据此升 WARN）。"""
    lines = []
    rv = info.get("review")
    if rv is None:
        for e in info.get("errors", []):
            lines.append("⚠ 复盘触发器不可判定：" + e)
        if not info.get("errors"):
            lines.append("复盘触发器：未找到上篇复盘段（仓内尚无工作复盘系列）")
        return lines
    lines.append("复盘触发器：上篇 = %s（W%d·%s）" % (rv["title"][:40], rv["w"], rv["date"]))
    errs = info.get("errors", [])
    for e in errs:
        lines.append("⚠ " + e)
    parts = []
    if info.get("days") is not None:
        parts.append("距今 %d 天" % info["days"])
    if info.get("batches") is not None:
        parts.append("后续批次 %d" % info["batches"])
    if info.get("commits") is not None:
        parts.append("后续提交 %d" % info["commits"])
    lines.append("复盘触发器现状：%s（判据：≥%d 天 / ≥%d 批 / ≥%d 提交·三选一）"
                 % (" · ".join(parts) or "（取数失败）",
                    THRESHOLDS["days"], THRESHOLDS["batches"], THRESHOLDS["commits"]))
    triggered = evaluate(datetime.date.today(), rv["date"],
                         info.get("batches") or 0,
                         info.get("commits") or 0)
    if triggered:
        lines.append("⚠ 复盘触发：{} ——请认领复盘批（对账表登记·触发清单与周期栏带入报告）：{}".format(
            "；".join(triggered),
            "；".join(x.split(" ")[0] for x in triggered)))
    else:
        lines.append("复盘触发器：未触发")
    return lines


def notice_lines(git):
    """preflight 提示位入口：返回提示行（异常由调用方兜底）。"""
    return render(collect(git))


def _self_test() -> int:
    """自测：正例必绿 + 负例必红（负例红不了 ⇒ 判据无效）。"""
    fails = []

    # find_last_review：复盘段与非复盘段混排（降序）→ 取最高复盘段
    sample = "\n".join([
        "### W960（2026-10-30）：某功能批",
        "### W956（2026-10-26）：第 44 篇工作复盘与优化分析报告入库批",
        "### W940（2026-10-25）：素材批",
        "### W795（2026-10-19）：第 42 篇工作复盘与优化分析报告入库批",
    ])
    rv = find_last_review(sample)
    if not rv or rv["w"] != 956 or rv["date"] != "2026-10-26":
        fails.append("find_last_review 应取最高工作复盘段 W956")
    if find_last_review("### W900（2026-10-20）：普通批\n") is not None:
        fails.append("无复盘段应返回 None")

    # batches_since：排除让号留痕 / 已停止 / ≤last_w
    ledger = "\n".join([
        "| W958 | 新批 | a | b | 在途 | s | x |",
        "| W957 | 让号留痕批 | — | — | 已收官（让号留痕·最终 W958） | s | — |",
        "| W956 | 停止批 | — | — | 已停止（零提交） | s | — |",
        "| W955 | 旧批 | a | b | 已收官 | s | y |",
    ])
    if batches_since(ledger, 955) != 1:
        fails.append("batches_since 应计 1（W958）——让号留痕/已停止/≤last 全部排除")
    if batches_since(ledger, 958) != 0:
        fails.append("batches_since 无后续行应计 0")

    # evaluate：三判据各自触发 + 全不触发的负样本
    today = datetime.date(2026, 10, 30)
    if evaluate(today, "2026-10-26", 0, 0) != ["T1 距上篇复盘 4 天 ≥ 3 天"]:
        fails.append("T1 应单独触发（4 天）")
    if evaluate(today, "2026-10-29", 30, 0) != ["T2 上篇复盘后批次 30 ≥ 30"]:
        fails.append("T2 应单独触发（30 批）")
    if evaluate(today, "2026-10-29", 0, 81) != ["T3 上篇复盘后提交 81 ≥ 80"]:
        fails.append("T3 应单独触发（81 提交）")
    if evaluate(today, "2026-10-29", 5, 10) != []:
        fails.append("负样本：2 天 5 批 10 提交必须不触发（空清单）")
    if evaluate(today, "", 0, 0)[0][:2] != "T1":
        fails.append("日期不可解析应按 T1 触发处理（fail-closed）")

    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：定位/计数/三判据/负样本全过（判据可证伪）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="复盘触发器（W956·P-43-02）")
    ap.add_argument("--self-test", action="store_true", help="自测")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    git = "git"
    if os.path.exists(r"C:\Program Files\Git\bin\git.exe"):
        git = r"C:\Program Files\Git\bin\git.exe"
    for line in render(collect(git)):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
