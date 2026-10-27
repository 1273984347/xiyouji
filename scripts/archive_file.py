#!/usr/bin/env python
"""archive_file.py — 项目归档工具（W735 建·文档规范 §5 配套执行器）。

将退役文件按归档规范迁入 archive/ 统一归档区，一次完成三件事：
  1. git mv 归位（分类自动判定或 --to 手动指定）
  2. 活引用扫描（排除历史登记类）——输出需人工核对的引用提示
  3. archive/README.md 台账登记（追加组行/单件行）

用法：
    python scripts/archive_file.py <path>... [--batch W###] [--reason "..."]
                                   [--to archive/xxx] [--dry-run] [--no-ledger]

示例：
    python scripts/archive_file.py <文件路径> --batch W### --reason "批次完结归档"
    python scripts/archive_file.py <目录路径> --to archive/scripts/<组名> --batch W### --reason "整组归档"
    python scripts/archive_file.py <文件路径> --batch W### --dry-run

归位判定（--to 未指定时自动，规则见文档规范 §5）：
    .md/.txt/.rst   → archive/docs/{原名}
    文件名含 W 号    → archive/scripts/batches/w{N段}/（如 w5xx/w6xx/w7xx）
    其余             → archive/scripts/{原名}

退出码：0=全部成功；1=有错误；2=参数错误。
"""
import argparse
import os
import re
import subprocess
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "archive", "README.md")
DOC_EXT = {".md", ".txt", ".rst", ".text"}
# 活引用扫描时排除的历史登记类文件（引用它们是历史记录·无需同步）
EXCLUDE_FILES = {"CHANGELOG.md", "HANDOVER.md", "file-index.md",
                 "W批次编号对账表.md", "package-lock.json", "README.md",
                 "archive_file.py"}


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", **kw)


def git(*args):
    return run(["git"] + list(args))


def classify(path, to=None):
    """归位判定：返回目标绝对路径。"""
    name = os.path.basename(path)
    if to:
        target_dir = os.path.join(ROOT, to)
    else:
        ext = os.path.splitext(name)[1].lower()
        m = re.search(r"[_\-\s]w(\d{3,4})", name, re.IGNORECASE)
        if ext in DOC_EXT:
            target_dir = os.path.join(ROOT, "archive", "docs")
        elif m:
            seg = f"w{int(m.group(1)) // 100}xx"
            target_dir = os.path.join(ROOT, "archive", "scripts", "batches", seg)
        else:
            target_dir = os.path.join(ROOT, "archive", "scripts")
    return os.path.join(target_dir, name)


def check_preconditions(path):
    """校验：存在 + git 跟踪 + 工作树干净。返回 (ok, message)。"""
    if not os.path.exists(path):
        return False, "不存在"
    base = path.replace("\\", "/")
    # 跟踪状态
    r = git("ls-files", "--error-unmatch", base)
    if r.returncode != 0:
        return False, "未被 git 跟踪（可重建产物/本地文件不归档）"
    # 工作树干净（该路径无未提交改动）
    r = git("status", "--porcelain", "--", base)
    if r.stdout.strip():
        return False, f"工作树有未提交改动：{r.stdout.strip().splitlines()[0][:60]}"
    # 递归文件数（目录）
    if os.path.isdir(path):
        n = sum(len(fs) for _, _, fs in os.walk(path))
        return True, f"目录（{n} 文件）"
    return True, "文件"


def scan_refs(path):
    """活引用扫描：全仓 grep basename，排除历史登记类与归档区。返回命中列表。"""
    name = os.path.basename(path)
    if len(name) < 6:
        return []
    cmd = ["grep", "-rnF", name, ROOT,
           "--exclude-dir=.git", "--exclude-dir=node_modules", "--exclude-dir=__pycache__",
           "--exclude-dir=archive", "--exclude-dir=tmpe",
           "--exclude-dir=hyperframes", "--exclude-dir=.playwright", "--exclude-dir=.pw-browsers"]
    for f in EXCLUDE_FILES:
        cmd.append(f"--exclude={f}")
    r = run(cmd)
    hits = []
    self_abs = os.path.abspath(path)
    for line in r.stdout.splitlines():
        src = line.split(":", 1)[0]
        if os.path.abspath(src) == self_abs:
            continue  # 文件自身
        hits.append(line[:150])
    return hits


def append_ledger(rows, batch, reason, dry_run=False):
    """向 archive/README.md 台账表末尾追加行。rows: [(新路径, 原路径)]"""
    if not os.path.exists(README):
        print("  [warn] archive/README.md 不存在，跳过台账登记")
        return
    with open(README, encoding="utf-8") as fh:
        text = fh.read()
    anchor = "## 三、引用与检索约定"
    if anchor not in text:
        print("  [warn] 台账锚点未找到，跳过（请手工登记）")
        return
    today = date.today().isoformat()
    new_lines = []
    for new_path, old_path in rows:
        new_lines.append(f"| `{new_path}` | `{old_path}` | {batch} | {today} | {reason} |")
    block = "\n".join(new_lines)
    # 插入到锚点前的最后一个空行前（即台账表末尾）
    head, sep, tail = text.partition(anchor)
    head = head.rstrip("\n") + "\n" + block + "\n\n---\n\n"
    text = head + sep + tail
    if dry_run:
        print(f"  [dry-run] 台账将追加 {len(new_lines)} 行")
    else:
        with open(README, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"  台账已追加 {len(new_lines)} 行")


def main():
    ap = argparse.ArgumentParser(description="项目归档工具（文档规范 §5 配套）")
    ap.add_argument("paths", nargs="+", help="待归档的文件/目录路径")
    ap.add_argument("--batch", default="W735", help="归档批次号（默认 W735）")
    ap.add_argument("--reason", default="退役归档", help="归档原因（默认：退役归档）")
    ap.add_argument("--to", default=None, help="手动指定目标目录（相对仓库根·如 archive/scripts/attic）")
    ap.add_argument("--dry-run", action="store_true", help="只打印计划不执行")
    ap.add_argument("--no-ledger", action="store_true", help="跳过台账登记")
    args = ap.parse_args()

    os.chdir(ROOT)
    ledger_rows = []
    errors = []

    for p in args.paths:
        p = p.replace("\\", "/").rstrip("/")
        print(f"■ {p}")
        ok, msg = check_preconditions(p)
        if not ok:
            print(f"  [错误] {msg}")
            errors.append(p)
            continue
        print(f"  校验通过：{msg}")

        target = classify(p, args.to)
        target_rel = os.path.relpath(target, ROOT).replace("\\", "/")
        if os.path.exists(target):
            print(f"  [错误] 目标已存在：{target_rel}")
            errors.append(p)
            continue
        print(f"  归位 → {target_rel}")

        refs = scan_refs(p)
        if refs:
            print(f"  ⚠ 活引用 {len(refs)} 处（需人工核对是否同步）：")
            for h in refs[:5]:
                print(f"      {h}")
            if len(refs) > 5:
                print(f"      …另 {len(refs) - 5} 处")
        else:
            print("  活引用：无")

        if args.dry_run:
            print("  [dry-run] 跳过 git mv")
        else:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            r = git("mv", p, target_rel)
            if r.returncode != 0:
                print(f"  [错误] git mv 失败：{r.stderr.strip()[:120]}")
                errors.append(p)
                continue
            print("  git mv 完成")

        ledger_rows.append((target_rel, p))

    if ledger_rows and not args.no_ledger:
        append_ledger(ledger_rows, args.batch, args.reason, dry_run=args.dry_run)

    print()
    print(f"完成：{len(ledger_rows)} 件处理" + (f"·{len(errors)} 件失败" if errors else ""))
    if not args.dry_run and ledger_rows:
        print("提醒：提交前跑 git status 核对 + 更新相关引用（如有引用提示）")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
