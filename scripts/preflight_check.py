#!/usr/bin/env python
"""preflight_check.py — 批次开工前置核验器（S-33 落地 · W736 建 · 复盘第 38 篇 §3）。

并发场景动工前跑一次，把「取号并发族」事故（W659/W660 → W726 两代）拦在开工之前。
六项核验：
  1. fetch origin —— 远端可达（Windows 走系统 Git；fetch 失败自动降级 GitHub API 通道·W732 实证备路）
  2. origin/main 顶部 —— 提交哈希 + 标题（供撞号判定）
  3. 对账表取号 —— 已认领最大 W 号 + 现势下一自由号（二者不衔接时告警）
  4. touches 在途盘点 + 交集拒绝 —— W739 建：在途批次 touches 列盘点；
     传 --touches 声明本批手工共享面，与在途批次有交集 → FAIL（拒绝并行·等对方收官）
  5. 工作树态 —— staged / 未暂存 / 未跟踪 简表（.workbuddy 排除）
  6. 环境 —— 仓库根校验 + python/pytest/ruff 可用性

用法：
    python scripts/preflight_check.py [--no-fetch] [--touches <逗号分隔的共享文件清单>] [--self W###]

典型动工流（认领 W739 后）：
    python scripts/preflight_check.py --touches "AGENTS.md, docs/agent/pitfalls.md" --self W739

退出码：0=无风险项；1=有风险（fetch 双通道失败 / 取号异常 / touches 交集冲突 / 不在仓库根）。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join("docs", "00-导读", "W批次编号对账表.md")
REPO_SLUG = "1273984347/xiyouji"  # GitHub API 降级通道用（W732 实证）
SYSTEM_GIT = r"C:\Program Files\Git\bin\git.exe"


def git_bin():
    """Windows 优先系统 Git（规避 schannel）；其余平台/环境回退 PATH。"""
    return SYSTEM_GIT if os.path.exists(SYSTEM_GIT) else "git"


def run(args, timeout=60):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout)


def parse_ledger(text):
    """解析对账表：返回 {max_w, bullet_w, rows}。

    权威取号规则=表头「下一自由号 = 本表 max(W#)+1」（W663 规则）；
    bullet_w=最末一条「现势下一自由号」豁免 bullet（轮换制·供交叉核验；
    表顶部 L8 的「现势」块系上一代机制遗留（末次维护 W720），不参与解析）。
    rows=[{w, status, touches}]——touches 列自 W739 起（历史行空·空集不参与交集判定）；
    兼容缺列旧格式（无第 7 列时 touches=空集）与历史不齐行（W687/W688 补空列后同为 7 列）。
    """
    rows_table = [int(x) for x in re.findall(r"^\|\s*W(\d{3})\s*\|", text, re.M)]
    bullets = re.findall(r"\*\*W(\d{3})\*\*：现势下一自由号", text)
    rows = []
    for line in text.splitlines():
        m = re.match(r"^\|\s*W(\d{3})\s*\|", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        status = cells[4] if len(cells) > 4 else ""
        touches = set()
        if len(cells) > 6 and cells[6]:
            touches = {t.strip() for t in cells[6].split(",") if t.strip()}
        rows.append({"w": int(m.group(1)), "status": status, "touches": touches})
    return {"max_w": max(rows_table) if rows_table else None,
            "bullet_w": int(bullets[-1]) if bullets else None,
            "rows": rows}


DONE_PREFIXES = ("已收官", "已闭环")


def is_inflight(status):
    """在途判定：状态列非「已收官/已闭环」开头即在途（含进行中/待收官/认领占位）。

    状态列可能带 Markdown 强调符（**已收官**）——先剥离再判定（W739 狗粮实证：
    不剥离则收官行被误报在途，touches 永久挡路）。
    W681 式「进行中（剩余=真端点联调待用户三键）」判在途——但其 touches 为空（历史行），
    空集与任何清单交集为空，天然不挡路（旧在途批次无害化）。
    """
    return not status.replace("**", "").strip().startswith(DONE_PREFIXES)


def touches_conflict(inflight_touches, mine):
    """纯函数：在途批次 touches ∩ 本批 touches → 排序冲突清单（空=可并行）。"""
    return sorted(set(inflight_touches) & set(mine))


def summarize_porcelain(text):
    """porcelain -z 输出 → {staged, unstaged, untracked, items}（.workbuddy 排除）。"""
    out = {"staged": 0, "unstaged": 0, "untracked": 0, "items": []}
    for item in text.split("\0"):
        if len(item) < 4:
            continue
        status, path = item[:2], item[3:]
        if path.startswith(".workbuddy"):
            continue
        out["items"].append((status.strip() or "??", path))
        if status == "??":
            out["untracked"] += 1
        else:
            if status[0] not in " ?":
                out["staged"] += 1
            if status[1] not in " ?":
                out["unstaged"] += 1
    return out


def step_fetch(git, no_fetch):
    """fetch origin；失败时降级 GitHub API。返回 (ok, 描述行)。"""
    if no_fetch:
        return True, "（--no-fetch 跳过·未核验远端）"
    r = run([git, "fetch", "origin"])
    if r.returncode == 0:
        return True, "OK（系统 Git）"
    try:
        url = f"https://api.github.com/repos/{REPO_SLUG}/commits?sha=main&per_page=1"
        req = urllib.request.Request(url, headers={"User-Agent": "xiyouji-preflight"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
        sha = data[0]["sha"][:8]
        msg = data[0]["commit"]["message"].splitlines()[0][:60]
        return True, f"fetch 失败（rc={r.returncode}）→ GitHub API 降级通道：main@{sha} {msg}"
    except Exception as exc:  # noqa: BLE001 — 报告原始异常即可
        return False, f"fetch 失败（rc={r.returncode}）且 API 降级通道失败：{exc}"


def step_env():
    """环境核验：返回 (ok, [报告行])。"""
    lines = []
    ok = True
    lines.append(f"python（本脚本）={sys.version.split()[0]}")
    launcher = "py" if shutil.which("py") else sys.executable
    for name, cmd in (("pytest", [launcher, "-m", "pytest", "--version"]),
                      ("ruff", [launcher, "-m", "ruff", "--version"])):
        try:
            r = run(cmd, timeout=30)
            if r.returncode == 0:
                lines.append(f"{name}={r.stdout.strip().splitlines()[0]}")
            else:
                ok = False
                lines.append(f"{name}=不可用（rc={r.returncode}·复跑门禁前需修复）")
        except Exception:  # noqa: BLE001
            ok = False
            lines.append(f"{name}=不可用（调用异常）")
    return ok, lines


def main():
    ap = argparse.ArgumentParser(description="批次开工前置核验（S-33）")
    ap.add_argument("--no-fetch", action="store_true", help="跳过 fetch（离线/已核验时）")
    ap.add_argument("--touches", default="",
                    help="本批计划手工修改的共享文件清单（逗号分隔）——与在途批次 touches 取交集，"
                         "非空即拒绝并行（级联面由 batch_cascade 单写路径保护·无需声明）")
    ap.add_argument("--self", dest="self_w", default="",
                    help="本批 W 号（如 W739）——交集检查时排除自己的认领行（自己的 touches 不挡自己）")
    args = ap.parse_args()

    problems = []
    print("== 批次开工前置核验（preflight_check · S-33）==")

    # 0) 仓库根校验
    if not os.path.exists(os.path.join(ROOT, "scripts", "batch_cascade.py")):
        print("FAIL  非 xiyouji 仓库根（scripts/batch_cascade.py 缺失）")
        return 1
    print(f"OK    仓库根：{ROOT}")
    git = git_bin()

    # 1) fetch / 降级通道
    fetch_ok, fetch_line = step_fetch(git, args.no_fetch)
    print(("OK    fetch：") if fetch_ok else "FAIL  fetch：", fetch_line)
    if not fetch_ok:
        problems.append("远端核验失败——撞号风险不可判")
    if args.no_fetch:
        print("WARN  --no-fetch：远端状态以本地 origin/main 引用为准（可能滞后）")

    # 2) origin/main 顶部
    r = run([git, "log", "--oneline", "-1", "origin/main"])
    remote_top = r.stdout.strip()[:100] if r.returncode == 0 else "（读取失败）"
    print(f"OK    origin/main 顶部：{remote_top}")

    # 3) 对账表取号
    try:
        text = open(os.path.join(ROOT, LEDGER), encoding="utf-8").read()
        ledger = parse_ledger(text)
    except OSError as exc:
        ledger = {"max_w": None, "bullet_w": None, "rows": []}
        print("FAIL  对账表读取失败：", exc)
        problems.append("对账表不可读")
    if ledger["max_w"]:
        next_free = ledger["max_w"] + 1
        print(f"OK    取号：已认领 max=W{ledger['max_w']} → 下一自由号 W{next_free}（表头规则 max+1）")
        b = ledger["bullet_w"]
        if b == next_free:
            print(f"OK    现势 bullet 交叉核验：W{b} 与 max+1 一致")
        elif b == ledger["max_w"]:
            print(f"NOTE  现势 bullet（W{b}）指向 max 号——该号已认领/进行中窗口（收官 chore 后轮换）")
        else:
            print(f"WARN  现势 bullet（W{b}）与 max+1（W{next_free}）不衔接——人工核对台账")
        print(f"TIP   建议动工批次号 = W{next_free}（认领后先登记对账表再施工）")
    else:
        print("FAIL  取号解析失败（未找到 W 行）")
        problems.append("取号异常")

    # 3.5) touches 在途盘点 + 交集拒绝（W739）
    self_norm = args.self_w.strip().lstrip("Ww")
    self_num = int(self_norm) if self_norm.isdigit() else None
    inflight_all = [r for r in ledger.get("rows", []) if is_inflight(r["status"]) and r["touches"]]
    inflight = [r for r in inflight_all if self_num is None or r["w"] != self_num]
    if inflight_all:
        for r in inflight_all:
            print(f"NOTE  在途批次 W{r['w']} touches：{', '.join(sorted(r['touches']))}"
                  + ("（本批自己·交集检查已排除）" if r["w"] == self_num else ""))
    else:
        print("OK    touches：无在途批次声明 touches（级联面由 batch_cascade 单写路径保护·无需声明）")
    if args.touches:
        mine = {t.strip() for t in args.touches.split(",") if t.strip()}
        bad = [(r["w"], touches_conflict(r["touches"], mine)) for r in inflight]
        bad = [(w, c) for w, c in bad if c]
        for w, c in bad:
            print(f"FAIL  touches 交集（在途 W{w}）：{', '.join(c)}——共享文件并行写风险·等对方收官或人工裁决")
            problems.append(f"touches 与在途批次 W{w} 冲突：{', '.join(c)}")
        if not bad:
            print(f"OK    touches 交集检查：本批声明 {len(mine)} 项·与在途批次（{len(inflight)} 个声明方）无交集")

    # 4) 工作树态
    r = run([git, "status", "--porcelain", "-z"])
    tree = summarize_porcelain(r.stdout)
    print(f"OK    工作树：staged={tree['staged']} 未暂存={tree['unstaged']} 未跟踪={tree['untracked']}")
    for status, path in tree["items"][:8]:
        print(f"       [{status}] {path}")
    if len(tree["items"]) > 8:
        print(f"       ……另 {len(tree['items']) - 8} 项")

    # 5) 环境
    env_ok, env_lines = step_env()
    for line in env_lines:
        print(("OK    " if env_ok else "WARN  ") + line)
    if not env_ok:
        problems.append("环境缺件（pytest/ruff）")

    print("== 结论 ==")
    if problems:
        for p in problems:
            print("FAIL  " + p)
        return 1
    print("PREFLIGHT PASS——无风险项，可动工（认领流程：对账表登记 → 施工）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
