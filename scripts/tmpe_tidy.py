#!/usr/bin/env python
"""tmpe_tidy.py — tmpe 本地临时区策略化治理工具（W738 起·策略源=tmpe/policy.yml）。

定位：tmpe 是 gitignore 本地临时区（过程产物可弃）。本工具是策略的执行臂——
规则唯一权威源在 policy.yml，本文件只实现机制，不硬编码分类判断。

机制清单：
  · 默认 dry-run；--apply 必须配 --confirm（双闸门）
  · --plan --json 机器可读计划；--apply --from-plan plan.json 按计划执行（防中途规则漂移）
  · journal（.journal/*.jsonl 记 src/dst/sha1/mtime/rule）+ --undo 反向恢复
  · 运行锁 .locks/tmpe_tidy.lock（防并行会话双写）+ 活跃热区锁 .locks/*.json（会话声明制）
  · 目标冲突加时间戳后缀，禁覆盖；同分区 os.rename，跨分区拒绝（禁 copy+delete）
  · 优先级链：protect > active_lock > freeze > standard_bucket > classify_rule > _inbox
  · --report 落 _reports/（md+json）；--older N 只处置 N 天前写入
  · --tool-candidates 工具晋升评估（v1.1）：只读扫描+九维评分+候选报告，禁自动晋升/禁执行
  · 零删除：一切删除经主人确认+系统回收站

用法：
    python scripts/tmpe_tidy.py                      # 盘点（只读）
    python scripts/tmpe_tidy.py --plan [--json] [--older N]
    python scripts/tmpe_tidy.py --apply --confirm    # 按当前规则执行归桶
    python scripts/tmpe_tidy.py --apply --from-plan plan.json --confirm
    python scripts/tmpe_tidy.py --undo .journal/xxx.jsonl
    python scripts/tmpe_tidy.py --report
    python scripts/tmpe_tidy.py --tool-candidates [--json]
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMPE = os.path.join(ROOT, "tmpe")
POLICY_PATH = os.path.join(TMPE, "policy.yml")
LOCK_DIR = os.path.join(TMPE, ".locks")
RUN_LOCK = os.path.join(LOCK_DIR, "tmpe_tidy.lock")
JOURNAL_DIR = os.path.join(TMPE, ".journal")
REPORT_DIR = os.path.join(TMPE, "_reports")
PROTECTED_DB = os.path.join(TMPE, ".protected.json")

STDLIB_HINT = set("""os sys re json time argparse datetime hashlib shutil pathlib collections itertools
math random subprocess typing dataclasses enum functools io csv sqlite3 urllib http socket threading
multiprocessing logging traceback tempfile glob fnmatch unicodedata string textwrap difflib""".split())


# ---------- 策略加载 ----------

def load_policy(path=POLICY_PATH):
    """policy.yml 采用 JSON 兼容语法（=YAML 子集）：json 直读，yaml 兜底，零硬依赖。"""
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except ValueError:
        try:
            import yaml  # type: ignore
            with open(path, encoding="utf-8") as fh:
                return yaml.safe_load(fh)
        except ImportError as exc:
            raise SystemExit(f"FAIL policy.yml 非 JSON 兼容语法且无 yaml 库：{exc}") from exc


# ---------- 基础工具 ----------

def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def sha1_of(path):
    h = hashlib.sha1()
    try:
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()[:12]
    except OSError:
        return ""


def item_stat(path):
    """(size, nfiles, newest_mtime)。"""
    size, nfiles, newest = 0, 0, 0.0
    if os.path.isdir(path):
        for dirpath, _dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(dirpath, f)
                try:
                    st = os.stat(fp)
                    size += st.st_size
                    newest = max(newest, st.st_mtime)
                    nfiles += 1
                except OSError:
                    pass
    else:
        st = os.stat(path)
        size, nfiles, newest = st.st_size, 1, st.st_mtime
    return size, nfiles, newest


def read_active_locks(policy):
    """读 .locks/*.json（排除运行锁本身）→ {顶层名: (session, expires_ts)}；TTL 过期忽略。"""
    locks = {}
    if not os.path.isdir(LOCK_DIR):
        return locks
    now = time.time()
    for fn in os.listdir(LOCK_DIR):
        if not fn.endswith(".json"):
            continue
        try:
            data = json.load(open(os.path.join(LOCK_DIR, fn), encoding="utf-8"))
        except (OSError, ValueError):
            continue
        since = data.get("since_ts", now)
        ttl_h = float(data.get("ttl_hours", 48))
        if now - since > ttl_h * 3600:
            continue  # 过期锁不生效
        for p in data.get("paths", []):
            locks[p.strip("/")] = (data.get("session", fn), since + ttl_h * 3600)
    return locks


# ---------- 扫描与分类（优先级链） ----------

def _match_classify_rule(name, ext, is_dir, policy):
    """⑤ classify_rule 匹配（files_only 规则跳过目录）→ (bucket, rule_name, note) 或 None。

    自 scan() 优先级链外提（W761）：本分支是链中唯一含内层循环的一段，
    独立后 scan 主体只剩优先级判定本身。
    """
    for rule in policy.get("classify_rules", []):
        if rule.get("files_only") and is_dir:
            continue
        if re.search(rule["match"], name, re.IGNORECASE):
            return rule["bucket"], rule["name"], rule.get("note", "")
        if rule.get("files_only") and re.search(rule["match"], ext, re.IGNORECASE):
            return rule["bucket"], rule["name"], rule.get("note", "")
    return None


def scan(policy, freeze_hours=None):
    """扫描 tmpe 顶层项。优先级链：protect > active_lock > freeze > w### > classify_rule > _inbox。"""
    fh = freeze_hours if freeze_hours is not None else policy["freeze"]["mtime_hours"]
    now = time.time()
    exclude = set(policy.get("exclude", []))
    protect_res = [re.compile(g, re.IGNORECASE) for g in policy.get("protect_globs", [])]
    locks = read_active_locks(policy)
    rows = []
    for name in sorted(os.listdir(TMPE)):
        if name in exclude:
            continue
        path = os.path.join(TMPE, name)
        if not os.path.exists(path):
            continue
        is_dir = os.path.isdir(path)
        size, nfiles, newest = item_stat(path)
        row = {
            "name": name, "is_dir": is_dir, "size": size, "files": nfiles,
            "mtime": newest, "bucket": None, "rule": None, "action": None, "note": "",
        }
        if any(r.search(name) for r in protect_res):  # ① protect
            row.update(bucket="_hold", rule="protect", action="PROTECT", note="个人稿件保护（禁动）")
        elif name in locks:  # ② active_lock
            sess, exp = locks[name]
            row.update(bucket="_hold", rule="active_lock", action="LOCK",
                       note=f"活跃锁·会话 {sess}（至 {datetime.datetime.fromtimestamp(exp):%m-%d %H:%M}）")
        elif (now - newest) < fh * 3600:  # ③ freeze
            row.update(bucket="_hold", rule="freeze", action="FREEZE",
                       note=f"{fh}h 内有写入（并行/本地在用）")
        elif re.match(r"^w\d{3}", name, re.IGNORECASE):  # ④ standard_bucket
            row.update(bucket="w###", rule="w_batch", action="MOVE", note="批次桶")
        else:  # ⑤ classify_rule → ⑥ fallback _inbox
            hit = _match_classify_rule(name, os.path.splitext(name)[1].lower(), is_dir, policy)
            if hit:
                row.update(bucket=hit[0], rule=hit[1], action="MOVE", note=hit[2])
            else:
                row.update(bucket="_inbox", rule="fallback", action="MOVE", note="未分类·入收件箱")
        rows.append(row)
    return rows


# ---------- 计划与执行 ----------

def build_plan(rows, older_days=None):
    now = time.time()
    actions = []
    for r in rows:
        if r["action"] != "MOVE":
            continue
        if older_days is not None and (now - r["mtime"]) < older_days * 86400:
            continue
        actions.append({"action": "MOVE", "name": r["name"], "dest": r["bucket"] + "/", "rule": r["rule"]})
    return actions


def resolve_dest(root, name, dest, policy):
    """目标冲突加时间戳后缀（禁覆盖）。"""
    dst_dir = os.path.join(root, dest)
    dst = os.path.join(dst_dir, name)
    if not os.path.exists(dst):
        return dst
    stem, ext = os.path.splitext(name)
    stamp = datetime.datetime.now().strftime(policy.get("conflict_suffix", "-%Y%m%d-%H%M%S"))
    return os.path.join(dst_dir, f"{stem}{stamp}{ext}")


def check_same_volume(src, dst):
    a = os.path.splitdrive(os.path.abspath(src))[0].lower()
    b = os.path.splitdrive(os.path.abspath(dst))[0].lower()
    return a == b


def _pid_alive(pid: int) -> bool:
    """进程存活探针（跨平台安全·W890）。

    POSIX：`os.kill(pid, 0)` = 只检查存在性（不杀进程）。
    **Windows：`os.kill(pid, 0)` 走 TerminateProcess ⇒ 会真的杀掉目标进程
    （含调用方自己）**——W889 实证：pytest 跑到 test_tmpe_tidy 的 RunLock 复验时，
    锁文件里存的是**当前 pytest 进程的 pid**（锁被 monkeypatch 失效后写到真路径），
    `os.kill(pid, 0)` 把 pytest 自己杀了 → 表现为「pytest 静默退出·无任何输出·
    exit 1」的本地红 / CI 绿分歧族（CI 跑 ubuntu-latest 走 POSIX 分支不受影响）。
    故 Windows 侧改用非终止式的存在性查询：OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION)
    + GetExitCodeProcess（进程已结束则退出码非 STILL_ACTIVE）。
    """
    if pid <= 0:
        return False
    if os.name == "posix":
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True  # 存在·但无权发信号（仍算存活）
        except OSError:
            return False
        return True
    try:  # pragma: no cover - Windows 分支（CI 在 ubuntu-latest 不覆盖）
        import ctypes

        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        STILL_ACTIVE = 259
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
        if not handle:
            return False
        try:
            code = ctypes.c_ulong()
            if not kernel32.GetExitCodeProcess(handle, ctypes.byref(code)):
                return False
            return code.value == STILL_ACTIVE
        finally:
            kernel32.CloseHandle(handle)
    except Exception:
        return False


class RunLock:
    """运行锁：防两个会话同时归桶。stale 锁（pid 死）自动接管。

    W890：`path` 默认值改为**运行时**解析（`path=None` → 取模块级 RUN_LOCK）。
    原实现 `def __init__(self, path=RUN_LOCK)` 的默认参数在**类定义时**求值，
    后续 `monkeypatch.setattr(tt, "RUN_LOCK", ...)` 对已绑定的默认值无效 →
    测试构造 `RunLock()` 会落到**真**锁路径（读写仓库真实 tmpe/.locks/），
    既污染真实锁又让测试与真实状态耦合（本次即因此触发 os.kill 自杀）。
    """

    def __init__(self, path=None):
        self.path = path if path is not None else RUN_LOCK
        self.acquired = False

    def acquire(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if os.path.exists(self.path):
            try:
                data = json.load(open(self.path, encoding="utf-8"))
                if _pid_alive(int(data.get("pid", -1))):
                    raise SystemExit(
                        f"FAIL 运行锁被占用：pid={data.get('pid')} since={data.get('ts')}（另会话在跑）")
            except SystemExit:
                raise
            except (ValueError, OSError):
                pass  # pid 已死或锁损坏 → 接管
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump({"pid": os.getpid(), "ts": datetime.datetime.now().isoformat(timespec="seconds")}, fh)
        self.acquired = True

    def release(self):
        if self.acquired and os.path.exists(self.path):
            os.remove(self.path)
            self.acquired = False


def apply_actions(actions, root, policy):
    """执行 MOVE（只移动·零删除·带 journal）。"""
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    os.makedirs(JOURNAL_DIR, exist_ok=True)
    journal_path = os.path.join(JOURNAL_DIR, f"{stamp}-{os.getpid()}.jsonl")
    moved = skipped = 0
    with open(journal_path, "w", encoding="utf-8") as jh:
        for a in actions:
            if a["action"] != "MOVE":
                continue
            src = os.path.join(root, a["name"])
            if not os.path.exists(src):
                print(f"SKIP  {a['name']}：源不存在")
                skipped += 1
                continue
            dst = resolve_dest(root, a["name"], a["dest"], policy)
            if os.path.exists(dst):
                print(f"CONFLICT {a['name']}：目标已存在→改用 {os.path.basename(dst)}")
            if not check_same_volume(src, dst):
                print(f"FAIL  {a['name']}：跨分区移动被拒（禁 copy+delete·请人工处置）")
                skipped += 1
                continue
            size, nfiles, mtime = item_stat(src)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.rename(src, dst)
            moved += 1
            print(f"MOVED {a['name']} → {a['dest']}")
            jh.write(json.dumps({
                "ts": datetime.datetime.now().isoformat(timespec="seconds"),
                "action": "MOVE", "src": src, "dst": dst, "size": size, "files": nfiles,
                "sha1": sha1_of(dst) if os.path.isfile(dst) else "",
                "mtime": mtime, "rule": a.get("rule", ""), "session": os.environ.get("WB_SESSION", "manual"),
            }, ensure_ascii=False) + "\n")
    print(f"完成：{moved} 项归桶 / {skipped} 项跳过（零删除）·journal={_rel(journal_path)}")
    return journal_path


def _rel(path):
    """相对仓库根展示；跨盘/异常时回落绝对路径（健壮性·tmp 测试实证）。"""
    try:
        return os.path.relpath(path, ROOT)
    except ValueError:
        return path


def undo_journal(journal_file, root):
    """读 journal 反向移动（dst→src）。src 已存在则加后缀防覆盖。"""
    lines = [json.loads(ln) for ln in open(journal_file, encoding="utf-8") if ln.strip()]
    restored = failed = 0
    for rec in reversed(lines):
        src, dst = rec["src"], rec["dst"]
        if not os.path.exists(dst):
            print(f"SKIP  恢复 {os.path.basename(dst)}：已被再移动/不存在")
            failed += 1
            continue
        target = src
        if os.path.exists(target):
            stem, ext = os.path.splitext(src)
            target = f"{stem}-restored-{datetime.datetime.now():%Y%m%d-%H%M%S}{ext}"
            print(f"CONFLICT {os.path.basename(src)} 已存在→恢复到 {os.path.basename(target)}")
        if not check_same_volume(dst, target):
            print(f"FAIL  跨分区恢复被拒：{os.path.basename(dst)}")
            failed += 1
            continue
        os.makedirs(os.path.dirname(target), exist_ok=True)
        os.rename(dst, target)
        restored += 1
        print(f"RESTORED {os.path.basename(dst)} → {os.path.relpath(target, root)}")
    print(f"undo 完成：{restored} 项恢复 / {failed} 项失败")
    return restored, failed


# ---------- 工具晋升评估（v1.1·只读·禁自动晋升/禁执行） ----------

def _read_text(path, limit=200000):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read(limit)
    except OSError:
        return ""


def _iter_tool_files(policy):
    """遍历 tmpe 内候选脚本文件（只读·含桶内一层·禁执行）。"""
    exts = set(policy.get("tool_promotion", {}).get("scan_extensions", [".py", ".sh", ".ps1", ".js", ".ts"]))
    scan_dirs = policy.get("tool_promotion", {}).get("scan_dirs", ["w###", "_misc", "_shot", "_bak", "_inbox"])
    for d in scan_dirs:
        base = os.path.join(TMPE, d)
        if not os.path.isdir(base):
            continue
        for dirpath, _dirs, files in os.walk(base):
            for f in sorted(files):
                if os.path.splitext(f)[1].lower() in exts:
                    yield os.path.join(dirpath, f)


def _score_dim(name, text, lines, stem, root):
    """九维评分（每维 0-2·总分 18）。保守估计：证据不足给低分。"""
    dim = {}
    low = text.lower()
    # 1 复用频率（0=一次性特征 1=中性 2=有跨批/外部引用）
    if re.search(r"^w\d{3}", name, re.IGNORECASE):
        dim["复用频率"] = 0
    else:
        dim["复用频率"] = 1
    # 2 通用性（argparse/参数化=2·硬编码路径=0）
    dim["通用性"] = 2 if ("argparse" in low or "add_argument" in low or "click" in low) else (
        0 if re.search(r"[A-Za-z]:\\\\|/Users/|/home/|D:\\\\", text) else 1)
    # 3 依赖（纯 stdlib=2）
    imports = set(re.findall(r"^\s*(?:import|from)\s+([a-zA-Z_][\w.]*)", text, re.M))
    third = {i.split(".")[0] for i in imports} - STDLIB_HINT - {"__future__"}
    dim["依赖"] = 0 if len(third) > 4 else (2 if not third else 1)
    # 4 可测试
    dim["可测试"] = 0
    # 5 文档（docstring 完整=2）
    has_doc = bool(re.match(r'^\s*("""|\'\'\'|#)', text)) and len(text.splitlines()[0] if text else "") > 0
    dim["文档"] = 2 if (text.lstrip().startswith(('"""', "'''")) and len(text) > 400) else (1 if has_doc else 0)
    # 6 入口（CLI=2·main=1·无=0）
    dim["入口"] = 2 if ("argparse" in low and "__main__" in low) else (1 if "def main(" in low or "__main__" in low else 0)
    # 7 维护成本（行数）
    dim["维护成本"] = 2 if lines < 100 else (1 if lines <= 300 else 0)
    # 8 安全影响（只读=2·凭证/网络/删除=0）
    if re.search(r"token|api[_-]?key|password|secret|credential", low):
        dim["安全影响"] = 0
    elif re.search(r"shutil\.rmtree|os\.remove|os\.unlink|requests\.|urllib|socket", low):
        dim["安全影响"] = 1
    else:
        dim["安全影响"] = 2
    # 9 替代品（scripts/ 已有同 stem=0）
    scripts_dir = os.path.join(root, "scripts")
    dup = os.path.isdir(scripts_dir) and any(
        os.path.splitext(f)[0] == stem for f in os.listdir(scripts_dir) if f.endswith(".py"))
    dim["替代品"] = 0 if dup else 2
    return dim


def _find_callers(name, stem, root):
    """调用者/被引用扫描（仓内 import 名或路径提及·只读 grep）→ 相对路径列表。

    自 scan_tool_candidates 外提（W761）：scripts/ tools/ tmpe/ 三树逐文件读 50KB
    找 stem 提及；候选文件自身（f==name）跳过。
    """
    callers = []
    for base in (os.path.join(root, "scripts"), os.path.join(root, "tools"), os.path.join(root, "tmpe")):
        if not os.path.isdir(base):
            continue
        for dirpath, _dirs, files in os.walk(base):
            for f in files:
                if f == name or not f.endswith((".py", ".md", ".json", ".js", ".ts")):
                    continue
                t = _read_text(os.path.join(dirpath, f), 50000)
                if stem in t:
                    callers.append(os.path.relpath(os.path.join(dirpath, f), root))
    return callers


def scan_tool_candidates(policy, root=ROOT):
    """只读扫描工具候选（禁执行·禁自动晋升）。返回评分行。"""
    cfg = policy.get("tool_promotion", {})
    if not cfg.get("enabled", False):
        return []
    rows = []
    for fp in _iter_tool_files(policy):
        text = _read_text(fp)
        if not text.strip():
            continue
        lines = text.count("\n") + 1
        name = os.path.basename(fp)
        stem = os.path.splitext(name)[0]
        rel = os.path.relpath(fp, TMPE)
        size, _nf, mtime = item_stat(fp)
        dim = _score_dim(name, text, lines, stem, root)
        callers = _find_callers(name, stem, root)  # 调用者/被引用（只读 grep·W761 外提）
        has_test = os.path.exists(os.path.join(os.path.dirname(fp), f"test_{stem}.py"))
        if has_test:
            dim["可测试"] = 2
        total = sum(dim.values())
        promote = cfg.get("promote_threshold", 14)
        watch = cfg.get("min_reuse_score", 8)
        verdict = "晋升候选（人工评审后移 scripts/ 或 tools/）" if total >= promote else (
            "观察（补 README/测试后再评）" if total >= watch else "不晋升（按 TTL 进 _trash）")
        purpose = ""
        m = re.search(r'"""(.*?)(?:"""|\n)', text, re.S)
        if m:
            purpose = " ".join(m.group(1).split())[:80]
        rows.append({
            "path": rel, "name": name, "purpose": purpose, "size": size, "lines": lines,
            "mtime": mtime, "callers": sorted(set(callers))[:5], "has_test": has_test,
            "score": total, "max": 18, "dim": dim, "verdict": verdict,
        })
    rows.sort(key=lambda r: -r["score"])
    return rows


def write_tool_report(rows, policy):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    md = ["# tmpe 工具晋升候选报告 " + stamp, "",
          "> 只读评估·禁自动晋升·禁执行未知脚本。晋升流程=人工评审→试运行→移动（不复制）→补 README/测试/owner→入 git→原副本移 _trash。",
          "", "| 路径 | 用途 | 行数 | 调用者 | 测试 | 评分 | 判定 |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        callers = "、".join(r["callers"]) if r["callers"] else "—"
        md.append(f"| {r['path']} | {r['purpose'] or '—'} | {r['lines']} | {callers} | "
                  f"{'有' if r['has_test'] else '无'} | {r['score']}/{r['max']} | {r['verdict']} |")
    md.append("")
    for r in rows:
        if r["score"] >= policy.get("tool_promotion", {}).get("promote_threshold", 14):
            md.append(f"## {r['path']}（{r['score']}/18）九维明细")
            md.append("")
            for k, v in r["dim"].items():
                md.append(f"- {k}：{v}/2")
            md.append("")
    md_path, _json_path = _write_report_pair(
        "tool_candidates", md, {"stamp": stamp, "rows": rows}, stamp)
    print(f"工具候选报告已落：_reports/tool_candidates-{stamp}.md（+json）")
    return md_path


# ---------- 报告 ----------

def _group_by_bucket(rows):
    """按 bucket 聚合行（未分类归「未分」·保持行序）——print_rows/write_report 共用（W761 去重）。"""
    agg = {}
    for r in rows:
        agg.setdefault(r["bucket"] or "未分", []).append(r)
    return agg


def _write_report_pair(prefix, md_lines, json_obj, stamp):
    """落 _reports/ 双件（md+json·同 stamp）——write_report/write_tool_report 共用（W761 去重）。"""
    os.makedirs(REPORT_DIR, exist_ok=True)
    md_path = os.path.join(REPORT_DIR, f"{prefix}-{stamp}.md")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md_lines))
    json_path = os.path.join(REPORT_DIR, f"{prefix}-{stamp}.json")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(json_obj, fh, ensure_ascii=False, indent=2, default=str)
    return md_path, json_path


def write_report(rows, policy):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    total = sum(r["size"] for r in rows)
    agg = _group_by_bucket(rows)
    md = [f"# tmpe 盘点报告 {stamp}", "",
          f"- 顶层项 {len(rows)} · 总体积 {human_size(total)} · 冻结窗 {policy['freeze']['mtime_hours']}h", ""]
    for b in list(dict.fromkeys(policy["buckets"] + ["_hold"])):
        if b not in agg:
            continue
        items = agg[b]
        md.append(f"## {b}（{len(items)} 项 · {human_size(sum(i['size'] for i in items))}）")
        md.append("")
        md.append("| 项 | 类型 | 体积 | 文件数 | 最后写 | 规则 | 动作 |")
        md.append("|---|---|---|---|---|---|---|")
        for r in sorted(items, key=lambda x: -x["size"]):
            when = datetime.datetime.fromtimestamp(r["mtime"]).strftime("%m-%d %H:%M")
            md.append(f"| {r['name']} | {'D' if r['is_dir'] else 'F'} | {human_size(r['size'])} | {r['files']} | {when} | {r['rule']} | {r['action']} |")
        md.append("")
    lim = policy.get("limits", {})
    misc = agg.get("_misc", [])
    if len(misc) > lim.get("_misc_warn_files", 100) or sum(i["size"] for i in misc) > lim.get("_misc_warn_mb", 5) * 1048576:
        md.append(f"⚠ **_misc 超额告警**：{len(misc)} 项 / {human_size(sum(i['size'] for i in misc))}"
                  f"（阈值 {lim.get('_misc_warn_files')} 项 / {lim.get('_misc_warn_mb')}MB）——需分流 _trash 或评估归档")
        md.append("")
    md_path, _json_path = _write_report_pair(
        "tmpe-report", md, {"stamp": stamp, "total_bytes": total, "rows": rows}, stamp)
    print(f"报告已落：_reports/tmpe-report-{stamp}.md（+json）")
    return md_path


# ---------- CLI ----------

def print_rows(rows, policy):
    total = sum(r["size"] for r in rows)
    print("== tmpe 盘点（策略源=policy.yml·只读）==")
    print(f"顶层项 {len(rows)} · 总体积 {human_size(total)} · 冻结窗 {policy['freeze']['mtime_hours']}h")
    agg = _group_by_bucket(rows)
    shown = list(dict.fromkeys(policy["buckets"] + ["_hold"]))
    for b in shown:
        if b not in agg:
            continue
        print(f"── {b}（{len(agg[b])} 项·{human_size(sum(i['size'] for i in agg[b]))}）")
        for r in agg[b]:
            when = datetime.datetime.fromtimestamp(r["mtime"]).strftime("%m-%d %H:%M")
            print(f"   {'D' if r['is_dir'] else ' '} {r['name']:<34} {human_size(r['size']):>9} {r['files']:>5} 件  {when}  [{r['action']}] {r['note']}")
    # 桶内实况（scan 只扫顶层·桶内项在此汇总）
    print("── 桶内实况（已归位项）")
    for b in shown:
        bpath = os.path.join(TMPE, b)
        if not os.path.isdir(bpath):
            continue
        size, nfiles, _ = item_stat(bpath)
        ntop = len([n for n in os.listdir(bpath) if n != ".DS_Store"])
        print(f"   {b:<10} {ntop:>4} 项 / {nfiles:>5} 件 / {human_size(size):>9}")


# ---------- CLI 模式处理器（main 分发用·W761 外提） ----------

def _cmd_tool_candidates(policy, as_json):
    """--tool-candidates：只读评估 + 报告落盘（禁自动晋升·禁执行未知脚本）。"""
    rows = scan_tool_candidates(policy)
    if as_json:
        print(json.dumps({"rows": rows}, ensure_ascii=False, indent=2, default=str))
    else:
        print(f"== 工具晋升候选（只读评估·{len(rows)} 个脚本）==")
        for r in rows:
            print(f"   {r['score']:>2}/18  {r['path']:<44} {r['verdict']}")
        if rows:
            print("（报告落 _reports/：--tool-candidates 已自动生成）")
        write_tool_report(rows, policy)
    return 0


def _cmd_plan(rows, older, as_json):
    """--plan [--json]：输出迁移计划（不执行·--json 为机器可读形态）。"""
    if as_json:
        print(json.dumps({"actions": build_plan(rows, older), "rows": rows},
                         ensure_ascii=False, indent=2, default=str))
        return 0
    actions = build_plan(rows, older)
    print(f"== 迁移计划（{len(actions)} 项·未执行）==")
    for a in actions:
        print(f"   [MOVE] {a['name']}  →  {a['dest']}   (rule={a['rule']})")
    if not actions:
        print("   （无可归桶项）")
    return 0


def _cmd_apply(rows, args, policy):
    """--apply：双闸门执行归桶（--confirm 必备·--from-plan 防中途规则漂移）。"""
    if not args.confirm:
        print("FAIL --apply 必须配 --confirm（双闸门·防误触）。先 --plan 审清单。")
        return 1
    if args.from_plan:
        data = json.load(open(args.from_plan, encoding="utf-8"))
        actions = data["actions"] if isinstance(data, dict) else data
    else:
        actions = build_plan(rows, args.older)
    apply_actions(actions, TMPE, policy)
    return 0


def main():
    ap = argparse.ArgumentParser(description="tmpe 临时区策略化治理（默认 dry-run·apply 需 --confirm")
    ap.add_argument("--plan", action="store_true", help="输出迁移计划")
    ap.add_argument("--json", action="store_true", help="计划/盘点用 JSON 输出")
    ap.add_argument("--apply", action="store_true", help="执行归桶（必须配 --confirm）")
    ap.add_argument("--confirm", action="store_true", help="确认执行 apply（双闸门）")
    ap.add_argument("--from-plan", metavar="FILE", help="按计划 JSON 执行（防中途规则漂移）")
    ap.add_argument("--undo", metavar="JOURNAL", help="按 journal 反向恢复")
    ap.add_argument("--report", action="store_true", help="生成盘点报告（_reports/）")
    ap.add_argument("--tool-candidates", action="store_true", help="工具晋升候选评估（只读·禁自动晋升）")
    ap.add_argument("--older", type=int, default=None, metavar="N", help="只处置 N 天前写入的项")
    ap.add_argument("--freeze-hours", type=int, default=None, help="覆盖 policy 冻结窗（小时）")
    args = ap.parse_args()
    if not os.path.isdir(TMPE):
        print("FAIL tmpe/ 不存在")
        return 2
    policy = load_policy()

    if args.undo:
        undo_journal(args.undo, TMPE)
        return 0

    lock = RunLock()
    lock.acquire()
    try:
        if args.tool_candidates:
            return _cmd_tool_candidates(policy, args.json)
        rows = scan(policy, args.freeze_hours)
        if args.report:
            write_report(rows, policy)
            return 0
        if args.plan:
            return _cmd_plan(rows, args.older, args.json)
        if args.apply:
            return _cmd_apply(rows, args, policy)
        print_rows(rows, policy)
        return 0
    finally:
        lock.release()


if __name__ == "__main__":
    sys.exit(main())
