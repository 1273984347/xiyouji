#!/usr/bin/env python
"""preflight_check.py — 批次开工前置核验器（S-33 落地 · W736 建 · 复盘第 38 篇 §3）。

并发场景动工前跑一次，把「取号并发族」事故（W659/W660 → W726 两代）拦在开工之前。
六项核验：
  1. fetch origin —— 远端可达（Windows 走系统 Git；fetch 失败自动降级 GitHub API 通道·W732 实证备路）
  2. origin/main 顶部 —— 提交哈希 + 标题（供撞号判定）
  3. 对账表取号 —— 已认领最大 W 号 + 现势下一自由号（二者不衔接时告警）
  4. touches 在途盘点 + 交集拒绝 —— W739 建：在途批次 touches 列盘点；
     传 --touches 声明本批手工共享面，与在途批次有交集 → FAIL（拒绝并行·等对方收官）
  5. 工作树态 —— staged / 未暂存 / 未跟踪 简表
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
        status = _locate_status(cells)
        touches = _locate_touches(cells)
        rows.append({"w": int(m.group(1)), "status": status, "touches": touches})
    return {"max_w": max(rows_table) if rows_table else None,
            "bullet_w": int(bullets[-1]) if bullets else None,
            "rows": rows}


DONE_PREFIXES = ("已收官", "已闭环")

# W825：状态列与 touches 列的**内容定位**（禁按固定下标 cells[4]/cells[6]）。
#
# 成因（实测 W764 行·8 格）：认领行的「主题/摘要」里若含裸竖线，Markdown 按竖线分列
# → 该行被切成 8/9 格（标准 7 格）→ 固定下标随即读错：
#   ① 状态读到别列（cells[4] 落在摘要残段上·把「W764」当状态）→ **已收官批次被永久
#      判为在途批次**（在途列表出现永不平息的幻影·误导后续批次判断）；
#   ② touches 读到认领会话列（cells[6] = 「DSH 2026-10-16」）→ 非路径垃圾串。
# 修法（三条，均不改变语义·只改定位方式）：
#   ① 状态 = 右起首个**紧匹配**「已收官/已闭环」形态的格（无则回退 cells[4]）——
#      紧匹配（整格即状态·可带 hash 括注）避免主题里偶然出现「已收官」三字被误认；
#   ② touches = **末格**（touches 是固定末列·摘要里的裸竖线只让前列右移·末格不动）；
#   ③ touches 占位符（—/-/无）归一为空集（历史「作废」行以「—」占位·原实现被当成
#      一个路径条目·使该行永久出现在在途列表）。
_TOUCHES_PLACEHOLDERS = {"—", "-", "－", "无", "n/a", "N/A", "(空)", "（空）"}
# W908 放宽：剥星去空后**前缀**匹配（允许嵌套括号证据长尾·如「已收官（hash·自测 33/33（T32/T33 双向锁）·…）」）——
# 原单层括号紧匹配把长尾收官格拒识别→回退固定下标 cells[4]→被含竖线碎行击穿（W908 认领拦截实测）；
# 主题误认由「右起扫描」防（状态列在主题列之右·右起首个命中即真状态格）。
_STATUS_CELL_RE = re.compile(r"^(?:已收官|已闭环)")


def _locate_status(cells):
    """状态列定位：右起首个「已收官/已闭环」前缀格；无则回退固定下标 cells[4]。

    右起扫描的原因：状态列在主题列之右·若主题里偶然出现「已收官」三字·
    右起扫描会优先命中真正的状态格。W908 起前缀匹配（允许证据长尾与嵌套括号）。
    """
    for c in reversed(cells):
        norm = re.sub(r"[\s*]+", "", c)
        if _STATUS_CELL_RE.match(norm):
            return c
    return cells[4] if len(cells) > 4 else ""


def _split_touches(text):
    """touches 串切分（**多分隔符兼容**·W897 修）+ 尾注归一（W903 修）。

    病根（实测 W896）：本函数与命令行解析**都只按逗号切分**，而台账的 touches 列
    自 W739 起实际用「**·**」（中点）分隔 ⇒ 整串被当成**一个** touches ⇒
    **交集检查恒空假绿**⇒「PREFLIGHT PASS·无交集」是无效结论，撞面防护形同虚设。

    兼容分隔符：逗号 `,` / 中文逗号 `，` / 顿号 `、` / 中点 `·` / 项目符号 `•`
    （**不含空白**——仓内文件名不含空格·避免把文件名本身切碎）。

    尾注归一（W903·机制审查报告 F1）：台账元素常带说明性尾注（如
    ``docs/11-方案报告/**（22 文件移动）``、``scripts/x.py（管控件·已批）``）——
    **全角括号内不切分且整段丢弃**（注记内常含中点·先切后剥必碎·W903 实现首版
    即踩此坑由负样本测试暴露）。安全性前提：仓内路径零全角括号（W903
    `git ls-files` 实证）；新文件名引入全角括号即破坏此前提。
    """
    out: set[str] = set()
    buf: list[str] = []
    depth = 0
    for ch in text or "":
        if ch == "（":
            depth += 1
            continue
        if ch == "）":
            depth = max(0, depth - 1)
            continue
        if depth > 0:
            continue  # 注记内容整体丢弃
        if ch in ",，、·•":
            tok = "".join(buf).strip()
            buf = []
            if tok:
                out.add(tok)
            continue
        buf.append(ch)
    tok = "".join(buf).strip()
    if tok:
        out.add(tok)
    return out


def _dir_base(tok):
    """目录形态归一：``X/**`` 与 ``X/`` → ``X``；文件路径返回 None。"""
    if tok.endswith("/**") and len(tok) > 3:
        return tok[:-3]
    if tok.endswith("/") and len(tok) > 1:
        return tok[:-1]
    return None


def _locate_touches(cells):
    """touches 列定位：末格（列序固定·末列恒为 touches）；占位符归一为空集。"""
    if len(cells) < 7:
        return set()
    last = cells[-1].strip()
    if last in _TOUCHES_PLACEHOLDERS:
        return set()
    return _split_touches(last)

# W821：§8 干扰日志的机器触发点提示（真触发才输出·用户裁决 2026-10-20）。
# 背景：W741 立的两周干扰日志（路线图 §8）自 2026-10-16 起断档 4 天 128 提交零登记，
# 而该期间实际发生 ≥2 次强制触发事件——根因是「该日志无任何机器防线·纯自觉动作」。
# 本提示把「靠人记得写日志」变成「机器在真发生时喊一声」，**不改变任何判定与退出码**。
INTERFERENCE_LOG_HINT = (
    "⚠     并行冲突事件待登记：本次命中机器触发点（§8 日志窗口已于 2026-10-24 收官归档·W922 裁决）"
    "——请在 docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md "
    "的 §8 表追加一行（日期/会话/事件类/共享面/读时状态/写时状态/损失返工）"
)


def interference_log_hint(reason):
    """构造 §8 干扰日志待登记提示行（带命中原因）。返回单行字符串。

    纯函数形态——供 --self-test 与单测直接断言。
    """
    return "%s（命中：%s）" % (INTERFERENCE_LOG_HINT, reason)


def is_inflight(status):
    """在途判定：状态列剥离全部星号与空白后，非「已收官/已闭环」开头即在途。

    加固史（W739→W741）：对账表状态列是 Markdown 自由文本——加粗（**已收官**）、
    单星（*已收官*）、多星、空白前缀都可能由排版引入。首版 startswith 被加粗击穿
    （狗粮实证）；二版 replace("**") 剥不到单星；本版 re.sub(r"[\\s*]+","") 全量剥离，
    任何强调/空白变体都不影响判定（回归形态见 test_inflight_with_bold_status 族）。
    W681 式「进行中（剩余=真端点联调待用户三键）」判在途——但其 touches 为空（历史行），
    空集与任何清单交集为空，天然不挡路（旧在途批次无害化）。
    """
    return not re.sub(r"[\s*]+", "", status).startswith(DONE_PREFIXES)


def touches_conflict(inflight_touches, mine):
    """纯函数：在途批次 touches 与本批 touches 的冲突元素清单（空=可并行）。

    W903 语义归一（机制审查报告 F1·用户批准）：由字面集合交集扩为**对称目录前缀
    匹配**——目录声明（``X/**`` / ``X/``）与对方集合中任一 ``X`` 本身或以 ``X/``
    开头的路径即命中；返回**参与命中的双方元素**（排序）。前缀锚定整段 ``X/``，
    兄弟同名路径（``docs/x`` vs ``docs2/y``）不误报。
    旧病根（W897 修分隔符后的同族语义残余）：通配/带注记声明与对方具体文件
    **字面不等恒不命中**——W900 认领行 ``docs/11-方案报告/**（…）`` 实证，
    W825/W893 两起真实撞面未被机器拦下与之相关。
    """
    hits = set()
    for a in set(inflight_touches):
        for b in set(mine):
            if a == b:
                hits.update((a, b))
                continue
            ab = _dir_base(a)
            if ab is not None and (b == ab or b.startswith(ab + "/")):
                hits.update((a, b))
                continue
            bb = _dir_base(b)
            if bb is not None and (a == bb or a.startswith(bb + "/")):
                hits.update((a, b))
    return sorted(hits)


def summarize_porcelain(text):
    """porcelain -z 输出 → {staged, unstaged, untracked, items}。"""
    out = {"staged": 0, "unstaged": 0, "untracked": 0, "items": []}
    for item in text.split("\0"):
        if len(item) < 4:
            continue
        status, path = item[:2], item[3:]
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
        mine = _split_touches(args.touches)
        bad = [(r["w"], touches_conflict(r["touches"], mine)) for r in inflight]
        bad = [(w, c) for w, c in bad if c]
        for w, c in bad:
            print(f"FAIL  touches 交集（在途 W{w}）：{', '.join(c)}——共享文件并行写风险·等对方收官或人工裁决")
            problems.append(f"touches 与在途批次 W{w} 冲突：{', '.join(c)}")
        # W821：触发③（preflight 交集拒绝）——真触发才提示登记 §8 干扰日志
        if bad:
            print(interference_log_hint("preflight 交集拒绝"))
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
    # W821 注：原拟的「触发①（开工 git status 发现非本会话变更）」已按用户裁决删除
    # （2026-10-20）——preflight 内无法可靠区分「本会话变更」与「他方变更」
    # （工作树里的已暂存件可能来自并行会话），按「staged>0 即提示」会在正常态误报，
    # 变成常态噪音。现役触发点只剩两个判据精确者：
    #   ② safe_commit ref-lock 竞争触发重试（safe_commit.py）
    #   ③ preflight touches 交集拒绝（本文件·上方）

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
