#!/usr/bin/env python3
"""w1333_a1_crossref.py — A1 逐回解读交叉引用补全（W1333·内容质量深化）。

## 为什么做

A1 100 回逐回解读（docs/01-全书逐回解读/）此前只有 11 处 SD 小节内交叉引用，跨页
可达性靠 footer/导航；逐回「上一回/下一回 + 主要人物分析」的关联行缺失 ⇒ 读者在
回目正文里无法直达相邻回与人物页。本脚本按 chapter-meta（num / main_characters）
机器生成关联行，确定性映射、零内容改写。

## 关联口径（只链确定性目标，不猜主题）

- 上一回 / 下一回：按 num 排序的相邻文件（首尾各缺一侧）。
- 人物：chapter-meta.main_characters 中有**同名主文件**（docs/02-人物深度分析/<名>.md）
  或别名表命中者；外传/深化专题等衍生文件不作为主链接（避免语义误导）。
- 标记 `<!-- w1333-crossref -->` 幂等：重跑替换该行，不重复插入。

## 用法

  py -3 scripts/w1333_a1_crossref.py --dry     # 只报告
  py -3 scripts/w1333_a1_crossref.py --apply   # 写入
  py -3 scripts/w1333_a1_crossref.py --check   # 门禁：每回恰一条 + 链接文件存在
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D1 = os.path.join(ROOT, "docs", "01-全书逐回解读")
D2 = os.path.join(ROOT, "docs", "02-人物深度分析")
MARK = "<!-- w1333-crossref -->"
META_RE = re.compile(r"<!-- chapter-meta:\s*(\{.*?\})\s*-->", re.S)
LINE_RE = re.compile(r"^> 关联：.*%s\s*$" % re.escape(MARK), re.M)
# 人物名 → 02 主文件名的显式别名（仅收录人工核对过的主文件；外传/深化不映射）
ALIAS = {"观世音": "观音", "如来佛祖": "如来"}


def load_pages():
    out = []
    for p in sorted(glob.glob(os.path.join(D1, "*.md"))):
        name = os.path.basename(p)
        if name == "README.md":
            continue
        t = open(p, encoding="utf-8", errors="ignore").read()
        m = META_RE.search(t)
        if not m:
            continue
        meta = json.loads(m.group(1))
        out.append({"path": p, "name": name, "num": int(meta.get("num") or 0),
                    "chars": meta.get("main_characters") or [], "text": t})
    out.sort(key=lambda x: x["num"])
    return out


def person_file(name):
    target = ALIAS.get(name, name)
    p = os.path.join(D2, target + ".md")
    return (target, p) if os.path.exists(p) else (None, None)


def build_line(page, prev, nxt):
    parts = []
    if prev:
        parts.append("[第%03d回](%s)" % (prev["num"], prev["name"]))
    if nxt:
        parts.append("[第%03d回](%s)" % (nxt["num"], nxt["name"]))
    for c in page["chars"]:
        target, p = person_file(c)
        if target:
            parts.append("[%s](../02-人物深度分析/%s.md)" % (c, target))
    if not parts:
        return None
    return "> 关联：" + " · ".join(parts) + " " + MARK


def apply_page(page, line):
    t = page["text"]
    if LINE_RE.search(t):
        return LINE_RE.sub(line, t, count=1), "update"
    m = re.search(r"^> 数据指标：.*$", t, re.M)
    if not m:
        return t, "no-anchor"
    insert = m.end()
    return t[:insert] + "\n" + line + t[insert:], "insert"


def check(pages):
    issues = []
    for i, pg in enumerate(pages):
        n = len(LINE_RE.findall(pg["text"]))
        if n != 1:
            issues.append("%s: 关联行 %d 条（应恰 1）" % (pg["name"], n))
            continue
        line = LINE_RE.search(pg["text"]).group(0)
        for target in re.findall(r"\]\(([^)]+)\)", line):
            full = os.path.normpath(os.path.join(os.path.dirname(pg["path"]), target))
            if not os.path.exists(full):
                issues.append("%s: 死链 %s" % (pg["name"], target))
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    pages = load_pages()
    if args.check:
        issues = check(pages)
        for x in issues[:20]:
            print("FAIL", x)
        print("---- A1 交叉引用核验：%d 页 · 问题 %d ----" % (len(pages), len(issues)))
        return 0 if not issues else 1
    changed = 0
    stats = {"insert": 0, "update": 0, "skip": 0}
    for i, pg in enumerate(pages):
        prev = pages[i - 1] if i > 0 else None
        nxt = pages[i + 1] if i + 1 < len(pages) else None
        line = build_line(pg, prev, nxt)
        if not line:
            stats["skip"] += 1
            continue
        new, action = apply_page(pg, line)
        if action == "no-anchor":
            stats["skip"] += 1
            continue
        if new != pg["text"]:
            changed += 1
            stats[action] = stats.get(action, 0) + 1
            if args.apply:
                with open(pg["path"], "w", encoding="utf-8", newline="\n") as f:
                    f.write(new)
    print("页 %d · 改动 %d（insert %d / update %d / skip %d）%s"
          % (len(pages), changed, stats.get("insert", 0), stats.get("update", 0),
             stats["skip"], "（dry-run）" if args.dry or not args.apply else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
