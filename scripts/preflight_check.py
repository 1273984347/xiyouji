#!/usr/bin/env python
"""preflight_check.py — 批次开工前置核验器（S-33 落地 · W736 建 · 复盘第 38 篇 §3）。

并发场景动工前跑一次，把「取号并发族」事故（W659/W660 → W726 两代）拦在开工之前。
六项核验：
  1. fetch origin —— 远端可达（Windows 走系统 Git；fetch 失败自动降级 GitHub API 通道·W732 实证备路）
  2. origin/main 顶部 —— 提交哈希 + 标题（供撞号判定）
  3. 对账表取号 —— 已认领最大 W 号 + 现势下一自由号（二者不衔接时告警）
  4. touches 在途盘点 + 交集拒绝 —— W739 建：在途批次 touches 列盘点；
     传 --touches 声明本批手工共享面，与在途批次有交集 → FAIL（拒绝并行·等对方收官）；
     W956 起（P-43-01）「在途」加 git 条件：台账标在途而 git 已有该 W 提交 = 登记滞后，
     告警不拒绝（并发保护不再被自身历史欠账卡死——W954 开工 8 条 FAIL 实证）
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
    rows_table = [int(x) for x in re.findall(r"^\|\s*W(\d{3,4})\s*\|", text, re.M)]
    bullets = re.findall(r"\*\*W(\d{3,4})\*\*：现势下一自由号", text)
    rows = []
    for line in text.splitlines():
        m = re.match(r"^\|\s*W(\d{3,4})\s*\|", line)
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
    """touches 串切分（多分隔符兼容·W897 修）+ 尾注归一（W903 修）+ 反引号包裹解析（W934 修）。

    病根（实测 W896）：本函数与命令行解析**都只按逗号切分**，而台账的 touches 列
    自 W739 起实际用「**·**」（中点）分隔 ⇒ 整串被当成**一个** touches ⇒
    **交集检查恒空假绿**⇒「PREFLIGHT PASS·无交集」是无效结论，撞面防护形同虚设。

    尾注归一（W903·机制审查报告 F1）：台账元素常带说明性尾注（如
    ``docs/11-方案报告/**（22 文件移动）``、``scripts/x.py（管控件·已批）``）——
    **全角括号内不切分且整段丢弃**（注记内常含中点·先切后剥必碎·W903 实现首版
    即踩此坑由负样本测试暴露）。安全性前提：仓内路径零全角括号（W903
    `git ls-files` 实证）；新文件名引入全角括号即破坏此前提。

    反引号包裹解析（W934·架构会话实测报出）：台账 touches 列的路径**常被反引号包裹**
    （`` `docs/00-导读/W批次编号对账表.md` ``），且反引号内可能用「/」并列多个文件
    （`` `a.py` / `b.py` ``）⇒ 旧实现把整段当成**一个** token（还带着反引号）⇒
    与命令行传入的**无反引号**路径字面不等 ⇒ `touches_conflict` 恒返空 ⇒
    「PREFLIGHT PASS·无交集」在**真实撞面时假绿**。
    本版：**反引号内内容整体取一个 token**（内部分隔符不切），反引号外按分隔符切。
    """
    out: set[str] = set()
    buf: list[str] = []
    depth = 0        # 全角括号注记深度
    in_code = False  # 是否在反引号内

    def flush() -> None:
        tok = "".join(buf).strip()
        buf.clear()
        if not tok:
            return
        # 反引号段之间的连接残渣（如 " / "）不是路径 ⇒ 丢弃
        if not tok.strip("/ "):
            return
        out.add(tok)

    for ch in text or "":
        if ch == "（":
            depth += 1
            continue
        if ch == "）":
            depth = max(0, depth - 1)
            continue
        if depth > 0:
            continue  # 注记内容整体丢弃
        if ch == "`":
            flush()              # 反引号段切换前先收尾外层内容
            in_code = not in_code
            continue
        if in_code:
            buf.append(ch)       # 反引号内：分隔符一律不切
            continue
        if ch in ",，、·•":
            flush()
            continue
        buf.append(ch)
    flush()
    return out


def _dir_base(tok):
    """目录形态归一：``X/**`` 与 ``X/`` → ``X``；文件路径返回 None。"""
    if tok.endswith("/**") and len(tok) > 3:
        return tok[:-3]
    if tok.endswith("/") and len(tok) > 1:
        return tok[:-1]
    return None


# W935 判据 E：登记类共享面（台账认领行 + 方案报告 README 登记行）——**天然并发**，不得参与
#   touches 交集拒绝。病根：每个批次都要写这两面（登记自己那行）⇒ 交集检查对它们**恒红**
#   ⇒ 纪律在**准入阶段**被架空（实测 W930/W931/W934 三方在途时，任何新批次都撞台账）。
#   保障改由「纯追加 + 精确暂存（update-index --cacheinfo）+ 回填行指纹校验」承担
#   （规范 §11.0 规则二）；硬冲突（其它共享面）仍照旧拒绝。
_REGISTER_SURFACES = ("docs/00-导读/W批次编号对账表.md", "docs/11-方案报告/README.md")


def _is_register_surface(tok: str) -> bool:
    """该 touches token 是否属于登记类共享面（台账 / 方案报告 README）。"""
    t = (tok or "").strip().strip("`")
    return any(t == s or t.startswith(s + "/") for s in _REGISTER_SURFACES)


def duplicate_wnums(rows: list[dict]) -> list[int]:
    """台账中**同一 W 号出现多行**的号列表（W935 判据 A1 · 撞号的机器特征）。

    病根与修正（原判据 A 假定「登记顺序 = 号顺序」）：
      · 真撞号的**可机检特征**是「同一个号被登记了两行」（两方各写一行）；
      · 「本批登记前被更晚的号插队」属**插队**（可接受：先落地者保留·后补登记），
        不是撞号 ⇒ 旧判据把它判 FAIL 会误伤后补登记。
    ⇒ 撞号检测改为「同号多行」；插队改为 NOTE 提醒。
    """
    seen: dict[int, int] = {}
    for r in rows:
        w = r.get("w")
        if isinstance(w, int):
            seen[w] = seen.get(w, 0) + 1
    return sorted(w for w, n in seen.items() if n > 1)


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

    W956 起（P-43-01）本函数只答「登记面语义」；**是否参与 touches 交集拒绝**由
    main() 里的 git 条件二分（split_inflight_lagged）裁定——登记面说在途而 git 已有
    该 W 提交的行是「登记滞后」，告警不拒绝（W954 实证：8 个陈旧在途行曾把开工恒红卡死）。
    """
    return not re.sub(r"[\s*]+", "", status).startswith(DONE_PREFIXES)


# W956（P-43-01·WF-08-a）：登记面自愈——「在途」判定加 git 条件。
# 病根（W954 复盘报告 FAM-40 实证）：台账状态列是**声明**不是事实源——8 个陈旧「在途」
# 批次（实为 7 批已落库 + 1 批已停止）的 touches 与新批次交集非空 ⇒ preflight 被**自身的
# 历史欠账**恒红拒绝（并发保护被欠账卡死·本系列第一次开工即 8 条 FAIL）。
# 修法：参与交集拒绝的「在途」须同时满足「台账标在途 AND git 无该 W 提交」；
# 台账标在途但 git 已有提交 ⇒ **登记滞后**——告警不拒绝（不改退出码语义），
# 由该批自己按收官流程回填状态列（ledger_backfill.py --from-git 支持脚本反填）。
# 口径：git 提交识别只认 subject 的批次标签形态 ``type(w###):``（仓内提交信息统一形态·
# 大小写不敏感）——正文/散文里提及别批号（「承接 W###」「W### 教训」）**不计**，
# 防止引用性提及误降真在途批次的 touches 防护。
_RE_COMMIT_TAG = re.compile(r"\((w\d{3,4})\)", re.IGNORECASE)


def wnum_commit_index(subjects):
    """git log ``%h %s`` 行列表 → {W 号(int): [提交数, 首笔短 hash]}。

    只认 subject 内批次标签 ``type(w###):`` 形态（见 _RE_COMMIT_TAG 注释·防散文引用误计）；
    一笔提交含多个批次标签时各号各计一笔（跨批提交对每个被标签批次都是事实存在）。
    """
    idx = {}
    for line in subjects or []:
        m = _RE_COMMIT_TAG.search(line)
        if not m:
            continue
        rec = idx.setdefault(int(m.group(1)[1:]), [0, ""])
        rec[0] += 1
        if not rec[1]:
            rec[1] = line.split(" ", 1)[0]  # 首列 = %h 短 hash
    return idx


def split_inflight_lagged(inflight_all, committed, self_num=None):
    """登记面在途行二分为 (真在途, 登记滞后)——P-43-01 纯函数形态（供单测直接断言）。

    committed = wnum_commit_index 产物；self 行永不入 lagged（自己的在途行在主流程里
    本就排除出交集检查，lagged 告警只指向**他方**陈旧行）。
    """
    truly, lagged = [], []
    for r in inflight_all:
        if r["w"] != self_num and r["w"] in committed:
            lagged.append(r)
        else:
            truly.append(r)
    return truly, lagged


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


def rejection_pairs(inflight, mine_hard, self_num=None):
    """纯函数：交集拒绝集——排除本批自身（W976 修）。

    旧病根：认领行先入台账后，preflight 复跑时自己的在途行照进拒绝循环，必然
    自撞 FAIL——docstring 与 NOTE 文案都声称「本批自己·交集检查已排除」，代码却
    未排除（W976 实证：认领 W976 后自查即红）。
    """
    bad = []
    for r in inflight:
        if r["w"] == self_num:
            continue
        c = touches_conflict(r["touches"], mine_hard)
        if c:
            bad.append((r["w"], c))
    return bad


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

    # 3.4) W931 新增：共享面串行化机制 · 判据 A（撞号检测）+ 判据 B'（台账脏行提示）
    #   A 撞号检测（W935 修订）：**同一 W 号在台账里出现多行** = 撞号的机器特征
    #     （两方各登记一行）⇒ FAIL 并要求人工裁决。
    #     「本批登记前被更晚的号插队」属**插队**而非撞号（先落地者保留·后补登记合法）
    #     ⇒ 只出 NOTE（旧判据在此误伤后补登记）。
    #     未登记时出 NOTE 提示「先登记认领行并提交·再复跑本脚本」。
    #   B' 台账脏行提示：台账工作树有未提交改动时，提交必须**精确暂存**（禁整文件 git add），
    #     否则会把他方在途行代提交（lost update 族）。
    #     **只出 NOTE 不 FAIL**：台账的「纯追加认领行」行级独立、可并发，
    #     强行 FAIL 会卡死合法批次（W930 实证：台账脏但实为合法在途）。
    #     真正的互斥放在回填工具 scripts/ledger_backfill.py 的**行指纹校验**里。
    _sn = args.self_w.strip().lstrip("Ww")
    _self_num = int(_sn) if _sn.isdigit() else None
    if ledger.get("rows"):
        _dups = duplicate_wnums(ledger["rows"])
        if _dups:
            print(f"FAIL  撞号检测：台账中同一 W 号出现多行 {_dups}——"
                  "同一个号被两方各登记一行（撞号）·请人工裁决（先落地者保留·另一方让号）")
            problems.append(f"撞号：台账中 W{_dups} 出现多行")
        else:
            print("OK    撞号检测：台账无同号多行（未被两方重复登记）")
    if _self_num is not None and ledger.get("rows"):
        _self_row = next((r for r in ledger["rows"] if r["w"] == _self_num), None)
        if _self_row is None:
            print(f"NOTE  取号校验：本批 W{_self_num} 的认领行尚未登记——"
                  "按新规则应「先登记认领行并提交·再复跑本脚本」")
        elif ledger["max_w"] == _self_num:
            print(f"OK    取号校验：W{_self_num} 是台账最新登记号（无更晚登记）")
        else:
            _later = sorted(r["w"] for r in ledger["rows"] if r["w"] > _self_num)
            print(f"NOTE  取号校验：W{_self_num} 之后有更晚的登记号 {_later}——"
                  "本批属**后补登记**（先落地者保留·非撞号）·后续批次请以 max+1 为准")
    _r_led = run([git, "status", "--porcelain", "--", LEDGER])
    if _r_led.returncode == 0 and _r_led.stdout.strip():
        print(f"NOTE  台账工作树有未提交改动（{_r_led.stdout.strip()[:70]}）——"
              "提交时**勿整文件 git add**（会把他方在途行代提交）："
              "用 git update-index --cacheinfo 精确暂存本批行，或用 scripts/ledger_backfill.py 回填")

    # 3.5) touches 在途盘点 + 交集拒绝（W739）+ git 条件二分（W956·P-43-01）
    self_norm = args.self_w.strip().lstrip("Ww")
    self_num = int(self_norm) if self_norm.isdigit() else None
    inflight_all = [r for r in ledger.get("rows", []) if is_inflight(r["status"]) and r["touches"]]
    _r_log = run([git, "log", "--all", "--format=%h %s"])
    if _r_log.returncode == 0 and _r_log.stdout.strip():
        committed = wnum_commit_index(_r_log.stdout.splitlines())
    else:
        committed = {}
        print("WARN  git 提交面读取失败（rc=%s）——登记滞后判定退化：全部按真在途从严保护" % _r_log.returncode)
    inflight, lagged = split_inflight_lagged(inflight_all, committed, self_num)
    for lr in lagged:
        _n, _first = committed[lr["w"]]
        print(f"WARN  登记滞后 W{lr['w']}：台账标在途·git 已有 {_n} 笔提交（首笔 {_first}）——"
              "不计入在途拒绝（P-43-01·告警不拒绝）·请按收官流程回填状态列"
              "（ledger_backfill.py --from-git 可脚本反填）")
    if inflight_all:
        for r in inflight_all:
            print(f"NOTE  在途批次 W{r['w']} touches：{', '.join(sorted(r['touches']))}"
                  + ("（本批自己·交集检查已排除）" if r["w"] == self_num else "")
                  + ("（登记滞后·已退出拒绝集）" if any(lr is r for lr in lagged) else ""))
    else:
        print("OK    touches：无在途批次声明 touches（级联面由 batch_cascade 单写路径保护·无需声明）")
    if args.touches:
        mine = _split_touches(args.touches)
        # W935 判据 E：登记类共享面（台账 / 方案报告 README）**排除**出交集拒绝——
        #   每个批次都要写这两面（登记自己那行）⇒ 交集对它们恒红 ⇒ 纪律在准入阶段被架空。
        #   并发保障改由「纯追加 + 精确暂存 + 回填行指纹」承担（规范 §11.0 规则二）。
        mine_hard = {t for t in mine if not _is_register_surface(t)}
        mine_reg = {t for t in mine if _is_register_surface(t)}
        inflight_others = [r for r in inflight if r["w"] != self_num]
        reg_hits = []
        for r in inflight_others:
            c = touches_conflict(r["touches"], mine_reg)
            if c:
                reg_hits.append((r["w"], sorted(c)))
        bad = rejection_pairs(inflight, mine_hard, self_num)
        for w, c in bad:
            print(f"FAIL  touches 交集（在途 W{w}）：{', '.join(c)}——共享文件并行写风险·等对方收官或人工裁决")
            problems.append(f"touches 与在途批次 W{w} 冲突：{', '.join(c)}")
        if reg_hits:
            print("NOTE  登记类共享面命中（台账 / 方案报告 README）："
                  + "；".join("W%d×%s" % (w, ",".join(c)) for w, c in reg_hits)
                  + "——按 §11.0 规则二并发写保障：纯追加 + 精确暂存（update-index --cacheinfo）"
                    "+ 回填行指纹（scripts/ledger_backfill.py）·不计入拒绝")
        # W821：触发③（preflight 交集拒绝）——真触发才提示登记 §8 干扰日志
        if bad:
            print(interference_log_hint("preflight 交集拒绝"))
        if not bad:
            print(f"OK    touches 交集检查：本批声明 {len(mine)} 项·与在途批次（{len(inflight_others)} 个声明方）无交集")

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

    # 5.5) 复盘触发器提示位（W956·P-43-02）：只提示不拦截（W822「只输出提示行·不改任何
    # 判定与退出码」语义）——触发清单由 scripts/check_review_trigger.py 产出；提示位故障
    # 降级为 WARN 不阻断开工，但**禁静默跳过**（必须留下不可用痕迹）。
    try:
        import check_review_trigger as _crt

        for _line in _crt.notice_lines(git):
            print(("WARN  " if _line.startswith("⚠") else "NOTE  ") + _line)
    except Exception as _exc:  # noqa: BLE001 — 提示位兜底（W822 语义）
        print(f"WARN  复盘触发器不可用（{_exc}）——本回合跳过复盘周期提示")

    # 5.6) 治理文档体积窗口（W960·文档规范 §8 机器化）——硬判据：超窗 FAIL 拦截开工。
    # 修法唯一 = scripts/archive_segments.py 归档（守恒断言五道）；门禁故障降级 WARN 禁静默跳过。
    try:
        import check_doc_size_budget as _dsb

        _dsb_fails, _dsb_lines = _dsb.gate_lines()
        for _line in _dsb_lines:
            print(("FAIL  " if "超窗!" in _line else "NOTE  ") + _line)
        for _f in _dsb_fails:
            problems.append(_f)
    except Exception as _exc:  # noqa: BLE001 — 判据不可执行须留痕（W809 fail-closed 族）
        print(f"WARN  体积窗口门禁不可用（{_exc}）——本回合跳过（禁静默·W960 建置纪律）")

    # 5.7) 治理文档数字断言对账提示位（W967·报告型 WARN 不拦截·挂 verify 槽需另行批准）
    try:
        import check_gov_doc_claims as _gdc

        _gdc_lines, _gdc_fails = _gdc.check()
        for _line in _gdc_lines:
            print("NOTE  " + _line)
        for _f in _gdc_fails:
            print("WARN  " + _f)
    except Exception as _exc2:  # noqa: BLE001 — 提示位故障留痕不阻断
        print(f"WARN  数字断言对账器不可用（{_exc2}）——本回合跳过（禁静默）")

    print("== 结论 ==")
    if problems:
        for p in problems:
            print("FAIL  " + p)
        return 1
    print("PREFLIGHT PASS——无风险项，可动工（认领流程：对账表登记 → 施工）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
