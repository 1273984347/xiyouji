#!/usr/bin/env python3
"""check_capacity_budget.py — 架构方案 v2 §8.3「容量阈值（10 条）」实算门禁（W1205）。

背景：v2 §8.3 的 10 条容量阈值自 2026-10-25 起全部是静态条文——旧值（站点 51.81 MB /
搜索脚本 2.18 MB / 门禁 143.7–156.7 s / .git 260.5 MB）写死在方案文档里，无人复算、无人
在越过阈值时提醒。本脚本把该表逐条变成可复跑的机器判据：每条用当前磁盘/数据库事实实算当前值
→ 与阈值比对 → 输出余量（绝对值 + 百分比）→ 有项越线则退出码 1。

取数口径（每条都能被第三方按同一口径复算；口径与 v2 §8.3 原文逐条对应，不自行放宽）：

  # 1 单页 HTML 体积 > 200 KB
     口径：site/**/*.html 逐个文件 os.path.getsize()，取最大值（不是平均、不是抽样）。
     200 KB 按 200*1024 = 204800 B 判定（与仓内 check_inlined_css.py 的 KiB 口径一致）。
  # 2 单页内联 CSS > 60 KB
     口径：site/**/*.html 逐页解析 <style>...</style> 全部内联样式块，累加其 UTF-8 字节数，
     取最大值。60 KB = 60*1024 = 61440 B。
  # 3 全站体积 > 120 MB
     口径：site/**/*.html 字节和（沿用 v2 §3.1 资产表「site/**/*.html 857 页 / 51.81 MB」的
     同一路径，见 docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md
     §3.1 表 + B-03 取数命令 Get-ChildItem site -Recurse -File -Filter *.html | Measure-Object
     Length -Sum）。120 MB 按 120*1024*1024 = 125829120 B 判定。
  # 4 站内搜索脚本 > 3 MB
     口径：站内搜索功能所加载的自有脚本（排除第三方库 .min.js）——当前实现为
     site/static/js/text-search-app.js 单文件，取其字节数（若仓内出现多个搜索脚本则求和）。
     3 MB = 3*1024*1024 = 3145728 B。
  # 5 门禁全量耗时 > 600 s
     口径：不跑全量 verify_delivery.py（由控制器收官时统一跑）。本脚本只读仓内已有的门禁耗时
     记录：优先读环境变量 CAPACITY_GATE_SECONDS（控制器收官时传入本批实测秒数）；其次读
     scripts/output/_w1205_capacity_gate_seconds.json（若存在，取其 elapsed_seconds 与 source
     字段）；都没有时标记为「待控制器回填」，不编造数字。600 s 判定。
  # 6 仓库体积 > 1 GB
     口径：.git 目录 os.walk 实算全部文件字节和（含 pack/loose/lost-found 等全部内容）。
     1 GB = 1024^3 = 1073741824 B。
  # 7 单批提交文件数 > 500
     口径：本批 = git diff --name-only <base>..HEAD 的文件数（base 由 --batch-base 指定，默认
     取 HEAD~1 以覆盖本批已落地提交；并叠加 git status --porcelain 中未提交的新增/修改文件数，
     得到「本批工作树口径」）。历史最大值对照给两个口径：① 遍历 HEAD 可达提交历史，对每个
     提交取 git show --name-only 的文件数最大值（单提交口径）；② 扫 scripts/output/_w*_spec.json
     的 file_index_rows 条数最大值（仓内批次级事实源·每批 spec 登记该批触碰文件清单）。
     注：工作树在途件可能含同批其他子任务/并行会话产物⇒精确文件数以控制器收官时的
     spec/touches 为准，本脚本给出的是「可复跑的上界口径」。
  # 8 PG 主库体量 > 200 GB
     口径：真实 PG 实例查询 SELECT pg_database_size(current_database())（字节）。
     200 GB = 200*1024^3 = 214748364800 B。
  # 9 PG 单表行数 > 5000 万
     口径：真实 PG 实例查询 SELECT count(*) FROM <业务表>（逐表），取最大值；业务表清单 =
     sessions/messages/feedback 三类（排除 schema_migrations/audit_archive 等基础设施表）。
     5000 万行判定。
  # 10 问答并发连接数 > 500
     口径：真实 PG 实例查询 SHOW max_connections（实例允许的最大并发连接数上限）与
     SELECT count(*) FROM pg_stat_activity WHERE datname = current_database()（当前库实连数）。
     取「上限」作为并发能力当前值（阈值 > 500 的语义是「并发连接能力达到 500 即需多副本 +
     负载均衡」），同时报告当前实连数作对照。

退出码：0 = 10 条全部未触发；1 = 至少一条触发（越线）；2 = 取数失败（PG 不可达等）——
     2 表示「测不出」，不得当作 0（不许把不可测当未触发）。

口令纪律：PG 凭据只从环境变量读（PGHOST/PGPORT/PGUSER/PGPASSWORD/PG_APP_DB，来源为仓外
%LOCALAPPDATA%/pg16/w934_pg.env，由调用方先注入进程环境）。本脚本不读仓内任何凭据文件、
不写出口令、不把口令落进 JSON 证据；连接信息只记录 host/port/db/user（非敏感部分）。

用法：
  py -3 scripts/check_capacity_budget.py                     # 实算 + 打印 + 写 JSON 证据
  py -3 scripts/check_capacity_budget.py --no-json            # 不写证据文件
  py -3 scripts/check_capacity_budget.py --batch-base <rev>   # 指定第 7 条的 base commit
  py -3 scripts/check_capacity_budget.py --gate-seconds 158.3  # 第 5 条：显式给门禁实测秒数
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from datetime import UTC, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT_JSON = os.path.join(ROOT, "scripts", "output", "_w1205_capacity_audit.json")
GATE_SECONDS_FILE = os.path.join(ROOT, "scripts", "output", "_w1205_capacity_gate_seconds.json")

KB = 1024
MB = 1024 * 1024
GB = 1024 * 1024 * 1024

# v2 §8.3 阈值表（权威来源：docs/11-方案报告/设计与架构方案/
# 系统架构方案v2-目标态与落地路线-2026-10-25.md §8.3「容量阈值」）。
# W1224 裁决批修订（用户批准·评估报告 W1222 §5.2）：#1 硬线 200→512 KB + 软线
# 200 KB（越软线报页清单与计数·不判红）；#2 口径改「页特有内联 CSS」（扣除
# INLINED 共享块——共享块是全站机制常数，不应记在页面头上），配套机制线 2b
# 共享基线块 ≤ 56 KB（ breaches 计入触发与退出码）；#1/#2 增报越线页清单与计数。
THRESHOLDS = {
    1: {"metric": "单页 HTML 体积", "limit": 512 * KB, "unit": "bytes",
        "action": "拆包评审（不得直接引入框架运行时）·软线 200 KB 预警清单随附"},
    2: {"metric": "单页页特有内联 CSS", "limit": 60 * KB, "unit": "bytes",
        "action": "页特有样式瘦身评审（须保证 file:// 仍可开）·共享块走 2b 机制线"},
    3: {"metric": "全站体积", "limit": 120 * MB, "unit": "bytes",
        "action": "资源分片评审"},
    4: {"metric": "站内搜索脚本", "limit": 3 * MB, "unit": "bytes",
        "action": "索引分片或改为按页加载"},
    5: {"metric": "门禁全量耗时", "limit": 600, "unit": "seconds",
        "action": "引入按 scope 增量门禁"},
    6: {"metric": "仓库体积", "limit": 1 * GB, "unit": "bytes",
        "action": "git gc + 归档复核"},
    7: {"metric": "单批提交文件数", "limit": 500, "unit": "files",
        "action": "拆分批次"},
    8: {"metric": "PG 主库体量", "limit": 200 * GB, "unit": "bytes",
        "action": "归档分区 + 评估读副本"},
    9: {"metric": "PG 单表行数", "limit": 50_000_000, "unit": "rows",
        "action": "评估分区表"},
    10: {"metric": "问答并发连接数", "limit": 500, "unit": "connections",
         "action": "Node 多副本 + 负载均衡"},
}

# 第 9 条只统计三类业务表（会话/消息/反馈），基础设施表不计入。
BUSINESS_TABLES = ("sessions", "messages", "feedback")

# 站内搜索自有字节（排除第三方库 .min.js）。W1223 执行批 E 起含两份索引数据件
# （search-index-zh/en.js·自 search 两页外置而来）——诚实口径：索引字节从容量 #1
# （单页 HTML）搬到本条，不得因「搬家」而在本条盲区里隐形。
SEARCH_SCRIPT_PATTERNS = (
    os.path.join("site", "static", "js", "text-search-app.js"),
    os.path.join("site", "js", "text-search-app.js"),
    os.path.join("site", "data", "search-index-zh.js"),
    os.path.join("site", "en", "search-index-en.js"),
)

STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
# W1224：#2 口径的共享块识别——与 W1019 判据同源（`<!-- INLINED CSS … -->` 标记
# 紧邻其后的 style 块 = inline_css.py 注入的 tokens+system 副本）。
INLINED_MARKER_RE = re.compile(r"<!--[^>]*INLINED CSS[^>]*-->")
# W1224：#1 软线（越线报清单不判红）与 #2b 共享基线块机制线（v2 §8.3 修订配套）。
SOFT_LIMIT_1 = 200 * KB
SHARED_INLINE_CSS_LIMIT = 56 * KB
SEP = chr(31)


# ---------------------------------------------------------------- helpers


def human_bytes(n: int) -> str:
    if n >= GB:
        return "%.2f GB" % (n / GB)
    if n >= MB:
        return "%.2f MB" % (n / MB)
    if n >= KB:
        return "%.2f KB" % (n / KB)
    return "%d B" % n


def rel_path(path: str) -> str:
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def git(*args: str) -> str:
    """跑 git 命令取 stdout（失败抛异常 → 上层记为取数失败）。"""
    proc = subprocess.run(
        ["git", "-C", ROOT] + list(args),
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), proc.stderr.strip()[:300]))
    return proc.stdout


def html_files() -> list:
    out = []
    for dirpath, _dirs, files in os.walk(SITE):
        for name in files:
            if name.endswith(".html"):
                out.append(os.path.join(dirpath, name))
    return sorted(out)


def row(idx: int, value, source: str, note: str = "", pending: bool = False,
        extra: dict | None = None) -> dict:
    """构造一条阈值判定的结构化结果。value=None → 取数不可得（pending）。"""
    t = THRESHOLDS[idx]
    limit = t["limit"]
    if value is None:
        return {
            "no": idx, "metric": t["metric"], "threshold": limit,
            "threshold_unit": t["unit"], "action_if_triggered": t["action"],
            "measured": None, "measured_display": "待控制器回填",
            "headroom_abs": None, "headroom_pct": None,
            "triggered": None, "pending": True,
            "source": source, "note": note, "extra": extra or {},
        }
    headroom = limit - value
    headroom_pct = (headroom / limit * 100.0) if limit else None
    if t["unit"] == "bytes":
        display = human_bytes(value)
    elif t["unit"] == "seconds":
        display = "%.1f s" % value
    else:
        display = "%d %s" % (value, t["unit"])
    return {
        "no": idx, "metric": t["metric"], "threshold": limit,
        "threshold_unit": t["unit"], "action_if_triggered": t["action"],
        "measured": value, "measured_display": display,
        "headroom_abs": headroom, "headroom_pct": round(headroom_pct, 2),
        "triggered": value > limit, "pending": False,
        "source": source, "note": note, "extra": extra or {},
    }


# ---------------------------------------------------------------- measurements


def measure_1_single_page_html() -> dict:
    files = html_files()
    biggest = None
    biggest_size = -1
    total = 0
    hard_over = []
    soft_over = []
    for f in files:
        size = os.path.getsize(f)
        total += size
        if size > biggest_size:
            biggest_size, biggest = size, f
        if size > THRESHOLDS[1]["limit"]:
            hard_over.append({"file": rel_path(f), "bytes": size})
        elif size > SOFT_LIMIT_1:
            soft_over.append({"file": rel_path(f), "bytes": size})
    hard_over.sort(key=lambda x: -x["bytes"])
    soft_over.sort(key=lambda x: -x["bytes"])
    note = "最大页：%s" % rel_path(biggest)
    if hard_over or soft_over:
        note += "｜硬线越线 %d 页·软线越线 %d 页（清单见 extra/结论区）" % (
            len(hard_over), len(soft_over))
    return row(1, biggest_size,
               "site/**/*.html 逐个 os.path.getsize() 取最大值（%d 个文件）" % len(files),
               note=note,
               extra={"file": rel_path(biggest), "file_count": len(files),
                      "site_html_total_bytes": total,
                      "hard_over_pages": hard_over[:20],
                      "soft_over_pages": soft_over[:20],
                      "soft_over_count": len(soft_over)})


def _inline_css_split(text: str) -> tuple[int, int]:
    """拆一页的内联 CSS 为 (页特有字节, 共享块字节)。

    共享块判定与 W1019 消费者同源：`<!-- INLINED CSS … -->` 标记与其后**仅隔空白**的
    style 块配对（inline_css.py 注入形态实测）。
    """
    shared_spans = set()
    for mk in INLINED_MARKER_RE.finditer(text):
        sm = STYLE_BLOCK_RE.search(text, mk.end())
        if sm and not text[mk.end():sm.start()].strip():
            shared_spans.add(sm.start())
    total = 0
    shared = 0
    for m in STYLE_BLOCK_RE.finditer(text):
        b = len(m.group(1).encode("utf-8"))
        total += b
        if m.start() in shared_spans:
            shared += b
    return total - shared, shared


def measure_2_inline_css() -> dict:
    files = html_files()
    biggest = None
    biggest_size = -1
    shared_biggest = None
    shared_biggest_size = -1
    over_pages = []
    for f in files:
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        specific, shared = _inline_css_split(text)
        if specific > biggest_size:
            biggest_size, biggest = specific, f
        if shared > shared_biggest_size:
            shared_biggest_size, shared_biggest = shared, f
        if specific > THRESHOLDS[2]["limit"]:
            over_pages.append({"file": rel_path(f), "bytes": specific})
    over_pages.sort(key=lambda x: -x["bytes"])
    note = "页特有最多页：%s｜共享基线块最大 %s（%s）" % (
        rel_path(biggest), human_bytes(shared_biggest_size), rel_path(shared_biggest))
    if over_pages:
        note += "｜越线 %d 页（清单见 extra）" % len(over_pages)
    return row(2, biggest_size,
               "site/**/*.html 逐页拆 (页特有, 共享块) 并取页特有最大值（%d 个文件·W1224 口径）"
               % len(files),
               note=note,
               extra={"file": rel_path(biggest),
                      "shared_block_max_bytes": shared_biggest_size,
                      "shared_block_max_file": rel_path(shared_biggest),
                      "shared_block_triggered": shared_biggest_size > SHARED_INLINE_CSS_LIMIT,
                      "over_threshold_pages": over_pages[:20],
                      "over_threshold_count": len(over_pages)})


def measure_3_site_total() -> dict:
    files = html_files()
    total = sum(os.path.getsize(f) for f in files)
    return row(3, total,
               "site/**/*.html 字节和（沿用 v2 §3.1 资产表 / B-03 取数命令同路径）",
               note="%d 个 HTML 页" % len(files),
               extra={"file_count": len(files),
                      "source_doc": "docs/11-方案报告/设计与架构方案/"
                                    "系统架构方案v2-目标态与落地路线-2026-10-25.md §3.1 + B-03"})


def measure_4_search_script() -> dict:
    found = []
    total = 0
    for pattern in SEARCH_SCRIPT_PATTERNS:
        p = os.path.join(ROOT, pattern)
        if os.path.isfile(p):
            size = os.path.getsize(p)
            found.append({"file": rel_path(p), "bytes": size})
            total += size
    if not found:
        return row(4, None, "site/static/js/text-search-app.js（站内搜索自有脚本）",
                   note="未找到站内搜索脚本，无法实算")
    return row(4, total,
               "站内搜索自有脚本字节（排除第三方 .min.js）",
               note="；".join("%s = %s" % (x["file"], human_bytes(x["bytes"]))
                              for x in found),
               extra={"files": found})


def measure_5_gate_seconds(explicit) -> dict:
    """门禁全量耗时：本脚本不跑全量 verify_delivery（控制器收官统一跑）。

    取值优先级：--gate-seconds > 环境变量 CAPACITY_GATE_SECONDS >
    scripts/output/_w1205_capacity_gate_seconds.json。都没有 → 标记待回填（不编造）。
    """
    src = None
    value = None
    note = ""
    if explicit is not None:
        value = float(explicit)
        src = "命令行 --gate-seconds（调用方传入本批实测值）"
    elif os.environ.get("CAPACITY_GATE_SECONDS"):
        value = float(os.environ["CAPACITY_GATE_SECONDS"])
        src = "环境变量 CAPACITY_GATE_SECONDS（调用方注入本批实测值）"
    elif os.path.isfile(GATE_SECONDS_FILE):
        with open(GATE_SECONDS_FILE, encoding="utf-8") as fh:
            payload = json.load(fh)
        value = float(payload["elapsed_seconds"])
        src = "scripts/output/_w1205_capacity_gate_seconds.json（source=%s）" %               payload.get("source", "未标注")
        note = payload.get("note", "")
    else:
        src = ("未取到本批门禁全量耗时实测值：脚本不跑全量 verify_delivery（由控制器收官时统一跑）；"
               "请用 --gate-seconds <秒> 或环境变量 CAPACITY_GATE_SECONDS 传入后复跑")
        return row(5, None, src, note=note)
    return row(5, value, src, note=note)


def measure_6_repo_size() -> dict:
    git_dir = os.path.join(ROOT, ".git")
    total = 0
    count = 0
    for dirpath, _dirs, files in os.walk(git_dir):
        for name in files:
            try:
                total += os.path.getsize(os.path.join(dirpath, name))
                count += 1
            except OSError:
                continue
    pack = 0
    pack_dir = os.path.join(git_dir, "objects", "pack")
    if os.path.isdir(pack_dir):
        for name in os.listdir(pack_dir):
            p = os.path.join(pack_dir, name)
            if os.path.isfile(p):
                pack += os.path.getsize(p)
    ratio = (pack / total * 100.0) if total else 0.0
    return row(6, total,
               ".git 目录 os.walk 实算全部文件字节和（含 pack/loose/lost-found）",
               note="pack 子目录 %s（占 %.1f%%）" % (human_bytes(pack), ratio),
               extra={"file_count": count, "pack_bytes": pack,
                      "pack_ratio_pct": round(ratio, 2)})


def _batch_file_count(base: str) -> dict:
    """本批文件数 = git diff --name-only <base>..HEAD ∪ 工作树未提交改动（去重）。"""
    committed = [x for x in git("diff", "--name-only", base + "..HEAD").splitlines()
                 if x.strip()]
    status_lines = [x for x in git("status", "--porcelain").splitlines() if x.strip()]
    worktree = []
    for line in status_lines:
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        path = path.strip('"')
        if path:
            worktree.append(path)
    uniq = sorted(set(committed) | set(worktree))
    return {"base": base, "committed_count": len(committed),
            "worktree_count": len(worktree), "total_count": len(uniq),
            "files": uniq}


def _history_max_commit_files() -> dict:
    """历史最大单提交文件数 = 遍历 HEAD 可达历史，逐提交取 --name-only 行数最大值。"""
    best = {"count": -1, "commit": None, "subject": None}
    raw = git("log", "--format=%H" + SEP + "%s", "--name-only", "--no-merges")
    commit = None
    subject = None
    files = set()
    for line in raw.splitlines():
        if SEP in line:
            if commit is not None and len(files) > best["count"]:
                best = {"count": len(files), "commit": commit, "subject": subject}
            commit, subject = line.split(SEP, 1)
            files = set()
            continue
        s = line.strip()
        if s:
            files.add(s)
    if commit is not None and len(files) > best["count"]:
        best = {"count": len(files), "commit": commit, "subject": subject}
    return best


def _history_max_batch_spec_files() -> dict:
    """历史批次「文件数」对照：扫 scripts/output/_w*_spec.json 的 file_index_rows 条数。

    这是仓内已有的批次级事实源（每批 spec 落盘时登记该批触碰文件清单）⇒ 取最大值即
    「历史批次的最大文件数」。与「单提交最大文件数」并列给出，两口径互为对照。
    """
    best = {"count": -1, "spec": None, "batch": None}
    pattern = os.path.join(ROOT, "scripts", "output", "_w*_spec.json")
    for path in glob.glob(pattern):
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            continue
        rows = data.get("file_index_rows") or []
        if len(rows) > best["count"]:
            best = {"count": len(rows), "spec": os.path.basename(path),
                    "batch": data.get("batch")}
    return best


def measure_7_batch_files(base: str) -> dict:
    batch = _batch_file_count(base)
    hist = _history_max_commit_files()
    spec = _history_max_batch_spec_files()
    return row(7, batch["total_count"],
               "git diff --name-only " + base + "..HEAD ∪ git status --porcelain（去重）",
               note="已提交 %d + 工作树未提交 %d = %d；历史最大单提交 %d 个（%s）；"
                    "历史最大批次 spec 登记文件数 %d（%s）" % (
                       batch["committed_count"], batch["worktree_count"],
                       batch["total_count"], max(hist["count"], 0),
                       (hist["commit"] or "")[:12], max(spec["count"], 0),
                       spec["batch"] or "-"),
               extra={"batch_base": base, "committed_count": batch["committed_count"],
                      "worktree_count": batch["worktree_count"],
                      "files": batch["files"],
                      "history_max_single_commit_files": max(hist["count"], 0),
                      "history_max_commit": hist["commit"],
                      "history_max_subject": hist["subject"],
                      "history_max_batch_spec_files": max(spec["count"], 0),
                      "history_max_batch_spec": spec["spec"],
                      "history_max_batch_id": spec["batch"],
                      "worktree_note": "工作树在途件可能含同批其他子任务/并行会话产物；"
                                       "本批精确文件数以控制器收官时的 spec/touches 为准"})


# ---------------------------------------------------------------- PG


def _pg_query_psql(sql: str, host: str, port: str, user: str,
                   password: str, db: str) -> str:
    psql = os.path.join(os.environ.get("LOCALAPPDATA", ""), "pg16", "pgsql", "bin", "psql.exe")
    if not os.path.isfile(psql):
        raise RuntimeError("未找到 psql.exe（%s）" % psql)
    env = dict(os.environ)
    env.update({"PGHOST": host, "PGPORT": port, "PGUSER": user,
                "PGPASSWORD": password, "PGDATABASE": db})
    proc = subprocess.run(
        [psql, "-t", "-A", "-F", "|", "-v", "ON_ERROR_STOP=1", "-c", sql],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
    )
    if proc.returncode != 0:
        raise RuntimeError("psql failed: %s" % proc.stderr.strip()[:300])
    return proc.stdout.strip()


def pg_query(sql: str) -> str:
    """跑一条 SQL 并返回纯文本结果（口令只来自进程环境变量·不进命令行）。

    优先用 psycopg2（本机已安装）；否则回落到 psql.exe（%LOCALAPPDATA%/pg16/pgsql/bin）。
    """
    host = os.environ.get("PGHOST", "127.0.0.1")
    port = os.environ.get("PGPORT", "5432")
    user = os.environ.get("PGUSER", "")
    password = os.environ.get("PGPASSWORD", "")
    db = os.environ.get("PG_APP_DB") or os.environ.get("PGDATABASE") or ""
    if not (user and password and db):
        raise RuntimeError("PG 凭据未在进程环境变量中设置"
                           "（PGHOST/PGPORT/PGUSER/PGPASSWORD/PG_APP_DB）")

    try:
        import psycopg2
    except ImportError:
        return _pg_query_psql(sql, host, port, user, password, db)

    conn = psycopg2.connect(host=host, port=int(port), user=user,
                            password=password, dbname=db, connect_timeout=10)
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            lines = []
            for r in rows:
                cells = ["" if v is None else str(v) for v in r]
                lines.append("|".join(cells))
            return chr(10).join(lines)
    finally:
        conn.close()


def measure_8_9_10_pg() -> tuple:
    conn_meta = {
        "host": os.environ.get("PGHOST", ""), "port": os.environ.get("PGPORT", ""),
        "db": os.environ.get("PG_APP_DB") or os.environ.get("PGDATABASE", ""),
        "user": os.environ.get("PGUSER", ""),
    }
    db_size = int(pg_query("SELECT pg_database_size(current_database())").strip())
    r8 = row(8, db_size,
             "真实 PG 查询 SELECT pg_database_size(current_database())",
             note="当前库 %s @ %s:%s" % (conn_meta["db"], conn_meta["host"],
                                        conn_meta["port"]),
             extra={"connection": conn_meta})

    counts = {}
    for table in BUSINESS_TABLES:
        out = pg_query('SELECT count(*) FROM "' + table + '"').strip()
        counts[table] = int(out.splitlines()[0])
    max_table = max(counts, key=lambda k: counts[k])
    r9 = row(9, counts[max_table],
             "真实 PG 查询 SELECT count(*) FROM <业务表>（逐表，取最大值）",
             note="；".join("%s = %d 行" % (k, v) for k, v in counts.items()),
             extra={"per_table_rows": counts, "max_table": max_table,
                    "business_tables": list(BUSINESS_TABLES), "connection": conn_meta})

    max_conn = int(pg_query("SHOW max_connections").strip())
    cur_conn = int(pg_query(
        "SELECT count(*) FROM pg_stat_activity WHERE datname = current_database()"
    ).strip())
    r10 = row(10, max_conn,
              "真实 PG 查询 SHOW max_connections（并发连接能力上限）"
              " + SELECT count(*) FROM pg_stat_activity（当前库实连数）",
              note="max_connections = %d；当前库实际连接数 = %d" % (max_conn, cur_conn),
              extra={"max_connections": max_conn, "current_connections": cur_conn,
                     "connection": conn_meta})
    return r8, r9, r10


# ---------------------------------------------------------------- main


def run_pg(rows: list, failures: list) -> None:
    """第 8/9/10 条：真实 PG 实查（三条同源·一次连接）。失败即三条皆标不可测。"""
    try:
        r8, r9, r10 = measure_8_9_10_pg()
        rows.extend([r8, r9, r10])
    except Exception as exc:  # noqa: BLE001
        failures.append("第 8/9/10 条 PG 取数失败：%s" % exc)
        for idx in (8, 9, 10):
            rows.append(row(idx, None, "PG 取数失败：%s" % exc))


def _print_over_lines(rows: list, shared_breach: bool) -> None:
    """打印 #1 软/硬线与 #2 页特有的越线页清单（W1224：登记面不再止步 max 单页）。"""
    r1 = next((r for r in rows if r["no"] == 1), None)
    r2 = next((r for r in rows if r["no"] == 2), None)
    if r1 and (r1["extra"].get("hard_over_pages") or r1["extra"].get("soft_over_pages")):
        print("[#1] 硬线（>%s）越线页：%s" % (
            human_bytes(r1["threshold"]),
            "；".join("%s=%s" % (x["file"], human_bytes(x["bytes"]))
                      for x in r1["extra"]["hard_over_pages"]) or "无"))
        print("[#1] 软线（>%s，预警不判红）越线 %d 页：%s" % (
            human_bytes(SOFT_LIMIT_1), r1["extra"]["soft_over_count"],
            "；".join("%s=%s" % (x["file"], human_bytes(x["bytes"]))
                      for x in r1["extra"]["soft_over_pages"])))
    if r2 and r2["extra"].get("over_threshold_pages"):
        print("[#2] 页特有（>%s）越线 %d 页：%s" % (
            human_bytes(r2["threshold"]), r2["extra"]["over_threshold_count"],
            "；".join("%s=%s" % (x["file"], human_bytes(x["bytes"]))
                      for x in r2["extra"]["over_threshold_pages"])))
    if shared_breach:
        r2e = r2["extra"] if r2 else {}
        print("[#2b] 共享基线块越线：最大 %s（%s）> 机制线 %s" % (
            human_bytes(r2e.get("shared_block_max_bytes", 0)),
            r2e.get("shared_block_max_file", "?"),
            human_bytes(SHARED_INLINE_CSS_LIMIT)))


def main() -> int:
    ap = argparse.ArgumentParser(description="架构方案 v2 §8.3 容量阈值（10 条）实算门禁")
    ap.add_argument("--no-json", action="store_true",
                    help="不写 scripts/output/_w1205_capacity_audit.json")
    ap.add_argument("--batch-base", default=None,
                    help="第 7 条的 base commit（默认 HEAD~1）")
    ap.add_argument("--gate-seconds", type=float, default=None,
                    help="第 5 条：显式传入本批门禁全量实测秒数（不跑全量 verify_delivery）")
    args = ap.parse_args()

    base = args.batch_base or "HEAD~1"

    rows = []
    failures = []

    def run(idx: int, fn, *fn_args):
        try:
            rows.append(fn(*fn_args))
        except Exception as exc:  # noqa: BLE001
            failures.append("第 %d 条取数失败：%s" % (idx, exc))
            rows.append(row(idx, None, "取数失败：%s" % exc))

    run(1, measure_1_single_page_html)
    run(2, measure_2_inline_css)
    run(3, measure_3_site_total)
    run(4, measure_4_search_script)
    run(5, measure_5_gate_seconds, args.gate_seconds)
    run(6, measure_6_repo_size)
    run(7, measure_7_batch_files, base)
    run_pg(rows, failures)

    rows.sort(key=lambda r: r["no"])
    triggered = [r for r in rows if r["triggered"] is True]
    pending = [r for r in rows if r["pending"]]

    payload = {
        "tool": "scripts/check_capacity_budget.py",
        "tool_version": "w1205-capacity-audit-v1",
        "batch": "W1205",
        "task": "v2 §8.3 容量阈值（10 条）实算",
        "generated_at": datetime.now(UTC).astimezone().isoformat(timespec="seconds"),
        "threshold_source": "docs/11-方案报告/设计与架构方案/"
                            "系统架构方案v2-目标态与落地路线-2026-10-25.md §8.3（10 条）",
        "unit_convention": "KB/MB/GB 均为二进制（1 KB = 1024 B · 1 MB = 1024^2 B · 1 GB = 1024^3 B）",
        "gate_seconds_note": "第 5 条不跑全量 verify_delivery.py（控制器收官统一跑）；"
                             "取值须由调用方用 --gate-seconds / CAPACITY_GATE_SECONDS 传入",
        "credential_policy": "PG 口令只从进程环境变量读；本文件不含也不记录口令",
        "items": rows,
        "summary": {
            "total": len(rows),
            "triggered": [r["no"] for r in triggered],
            "pending": [r["no"] for r in pending],
            "unmeasurable": [r["no"] for r in rows if r["measured"] is None],
            "failures": failures,
        },
    }

    if not args.no_json:
        os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
        with open(OUT_JSON, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.write(chr(10))

    print("=" * 78)
    print("架构方案 v2 §8.3 容量阈值（10 条）实算 · W1205")
    print("生成时间：%s" % payload["generated_at"])
    print("=" * 78)
    print("%-3s %-14s %-13s %-13s %-9s %s" % ("#", "指标", "实测值", "阈值", "余量", "判定"))
    for r in rows:
        headroom = "-" if r["headroom_pct"] is None else "%.1f%%" % r["headroom_pct"]
        if r["triggered"] is True:
            verdict = "触发 → " + r["action_if_triggered"]
        elif r["triggered"] is False:
            verdict = "未触发"
        else:
            verdict = "待回填（不可测）"
        if r["threshold_unit"] == "bytes":
            limit_display = human_bytes(r["threshold"])
        elif r["threshold_unit"] == "seconds":
            limit_display = "%d s" % r["threshold"]
        else:
            limit_display = "%d %s" % (r["threshold"], r["threshold_unit"])
        print("%-3s %-14s %-13s %-13s %-9s %s" % (
            r["no"], r["metric"], r["measured_display"], limit_display,
            headroom, verdict))
    print("-" * 78)
    for r in rows:
        print("[%d] %s｜取数口径：%s" % (r["no"], r["metric"], r["source"]))
        if r["note"]:
            print("     %s" % r["note"])
    print("-" * 78)
    shared_breach = any(r["extra"].get("shared_block_triggered") for r in rows)
    if triggered or shared_breach:
        parts = ["#%d %s" % (r["no"], r["metric"]) for r in triggered]
        if shared_breach:
            parts.append("#2b 共享基线块（机制线 %s）" % human_bytes(SHARED_INLINE_CSS_LIMIT))
        print("结论：%d 项已触发阈值 → %s" % (len(triggered) + (1 if shared_breach else 0),
                                              "；".join(parts)))
    else:
        print("结论：无项触发阈值。")
    # W1224：越线页清单（#1 软/硬线 + #2 页特有）——登记面不再止步 max 单页
    _print_over_lines(rows, shared_breach)
    if pending:
        print("待回填（不可测，不得当作未触发）：%s"
              % "、".join("#%d %s" % (r["no"], r["metric"]) for r in pending))
    if failures:
        print("取数失败：%s" % "；".join(failures))
    print("证据文件：%s" % rel_path(OUT_JSON))
    code = 2 if failures else (1 if (triggered or shared_breach) else 0)
    print("退出码：%d（0 = 无项触发 / 1 = 有项触发 / 2 = 取数失败）" % code)
    return code


if __name__ == "__main__":
    sys.exit(main())
