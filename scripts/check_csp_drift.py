#!/usr/bin/env python3
"""check_csp_drift.py — 内联脚本 CSP 零漂移**增量**判据（W1110 新增第 56 槽）。

## 为什么需要它（与既有第 8 槽的分工）

既有第 8 槽 `generate_csp.py --check` 是**全站**校验：任一页内联脚本与 CSP meta 哈希失配
即退出 1。它能抓住「改完没重算」，但有两个盲区：

1. **不知「谁改的」**：全站漂移与本批漂移混在一起 ⇒ 存量漂移会掩盖本批真问题，
   本批漂移也会被存量噪音淹没（改前基点缺失 ⇒ 无法判定「本批是否引入」）。
2. **无归因信息**：只打印 `DRIFT <page>`，不说「哪一段内联块变了」「改前基点是什么」
   ⇒ 开发者需自行 diff 才能定位，W1108 批实证的「元素数 750→112」级塌缩因此排查昂贵。

本槽按**交集判红**口径补上增量视角：

- **FAIL 条件 = 本批改动页 ∩ CSP 漂移页 ≠ ∅**（交集为空即通过——存量漂移不归本批）。
- **命中判定**：以「改前基点」与「改后」的内联 `<script>` 块**逐段字节比对**，
  字节变化的段即「本批碰过的内联块」⇒ 只对这些段判 CSP 哈希是否同步。
- **改前基点**：优先 `git merge-base origin/main HEAD`（本批开叉点）；
  不可得时回退 `HEAD`（CI 浅克隆 `fetch-depth: 1` 场景——此时无基点可比，
  退化为「本批改动页全段判漂移」，仍不漏判）。

## 失败信息三要素（缺一即判据不可用）

1. **漂移页清单**（哪些页）；
2. **命中段标识**（第几段内联块 / 该段哈希前 12 位）；
3. **修复命令**（`python scripts/generate_csp.py`）。

## 用法

    py -3 scripts/check_csp_drift.py --gate     # 门禁态（verify_delivery 调用）
    py -3 scripts/check_csp_drift.py --self-test  # 注入式负样本自测
    py -3 scripts/check_csp_drift.py --report     # 只报告不判红

退出码：0 通过 · 1 有 FAIL · 2 判据不可执行（git 不可用等）。
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 内联脚本块：与 generate_csp.py 的 SCRIPT_RE 同口径（无 src 的 <script>）——
# **必须逐字一致**，否则哈希口径分叉（哈希化 CSP 的口径由 generate_csp 定义）。
SCRIPT_RE = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", re.DOTALL)
META_RE = re.compile(
    r'<meta\s+http-equiv=["\']Content-Security-Policy["\']\s+content="([^"]*)"\s*/?>',
    re.IGNORECASE,
)
FIX_CMD = "python scripts/generate_csp.py"


def _git(*args):
    r = subprocess.run(
        ["git", "-c", "core.quotePath=false", "-C", ROOT] + list(args),
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
    )
    return r.stdout if r.returncode == 0 else ""


def inline_blocks(html):
    """返回该页内联脚本块正文列表（与 generate_csp 同口径：纯空白块跳过）。"""
    out = []
    for m in SCRIPT_RE.finditer(html):
        body = m.group(1)
        if not body.strip(" \t\r\n"):
            continue
        out.append(body)
    return out


def block_hash(body):
    return "sha256-" + base64.b64encode(
        hashlib.sha256(body.encode("utf-8")).digest()).decode("ascii")


def meta_hashes(html):
    """从 CSP meta 的 content 里提取全部 sha256 令牌（保持出现序·**去外层单引号**）。

    口径说明：meta 内形如 `'sha256-XXX='`（CSP 语法要求带引号），而 block_hash 返回
    **不带引号**的 `sha256-XXX=` ⇒ 两者比较前必须归一，否则永不相等（假红）。
    """
    m = META_RE.search(html)
    if not m:
        return []
    return [t.strip("'\"") for t in re.findall(r"'sha256-[^']+'", m.group(1))]


def resolve_base():
    """返回 (基点 ref, 说明)。优先 merge-base（开叉点），不可得回退 origin/main。

    **W1110 收官笔修（阻断 #1）**：原实现回退 `HEAD` ⇒ 在 CI 浅克隆（`fetch-depth: 1`）
    下 `git merge-base origin/main HEAD` 无输出 ⇒ 回退 HEAD ⇒ `changed_pages(HEAD)` 在
    干净检出实测为 `[]` ⇒ **该槽对任何页面都不判**（静默失效·与 gates.md 承诺相反）。
    ⇒ 回退链改为 **merge-base → origin/main → HEAD**：
      · `origin/main` 在浅克隆下**仍可用**（checkout 必带 origin 引用）⇒ 相对 origin/main 的
        改动页可算 ⇒ 判据仍有检出能力；
      · `HEAD` 仅作最后兜底（此时若改动页为空 ⇒ 明确记 NOTE 而非静默通过）。
    """
    mb = _git("merge-base", "origin/main", "HEAD").strip()
    if mb:
        return mb, "merge-base origin/main HEAD"
    om = _git("rev-parse", "origin/main").strip()
    if om:
        return om, "origin/main（无 merge-base：CI 浅克隆 fetch-depth 1）"
    head = _git("rev-parse", "HEAD").strip()
    if head:
        return head, "HEAD（无 merge-base 且无 origin/main）"
    return None, "无基点"


def changed_pages(base):
    """本批改动的 HTML 页（相对基点）——含工作树未提交改动。

    **W1110 收官笔修（阻断 #1）**：基点退化为 `HEAD`（CI 浅克隆）时，
    `git diff HEAD` 在干净检出 = 空 ⇒ 改动页为空 ⇒ 判据不判。
    ⇒ 此处补一层：**基点为 HEAD 且结果为空时**，再按「相对 origin/main」取一次
    （浅克隆下 origin/main 引用仍在 ⇒ 相对 main 的改动页可算）。
    """
    out = set()

    def _collect(ref):
        acc = set()
        for args in (["diff", "--name-only", ref],
                     ["diff", "--name-only", "--cached", ref],
                     ["diff", "--name-only", ref, "HEAD"]):
            for ln in _git(*args).splitlines():
                q = ln.strip().replace("\\", "/")
                if q.endswith(".html") and q.startswith("site/"):
                    acc.add(q)
        return acc

    out |= _collect(base)
    # 兜底：基点是 HEAD（提交后/干净检出）且无改动页 ⇒ 相对 origin/main 再取一次
    if not out and base == _git("rev-parse", "HEAD").strip():
        om = _git("rev-parse", "origin/main").strip()
        if om:
            out |= _collect(om)
    for ln in _git("ls-files", "--others", "--exclude-standard").splitlines():
        q = ln.strip().replace("\\", "/")
        if q.endswith(".html") and q.startswith("site/"):
            out.add(q)
    return sorted(out)


def read_page_at(ref, rel):
    r = subprocess.run(
        ["git", "-C", ROOT, "show", "%s:%s" % (ref, rel)],
        capture_output=True, timeout=60,
    )
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8", errors="replace")


def read_page_worktree(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def evaluate(pages, base_html, cur_html):
    """纯函数判定 —— 返回 (issues, notes)。

    pages: 本批改动页列表（相对路径）
    base_html: {rel: 基点 HTML 或 None}
    cur_html:  {rel: 改后 HTML 或 None}
    """
    issues, notes = [], []
    for rel in pages:
        cur = cur_html.get(rel)
        if cur is None:
            notes.append("%s：改后内容不可读（文件已删？）·跳过" % rel)
            continue
        cur_blocks = inline_blocks(cur)
        cur_hashes = [block_hash(b) for b in cur_blocks]
        declared = meta_hashes(cur)
        drift = [h for h in cur_hashes if h not in declared]
        if not drift:
            continue
        # 交集判红：只对「本批碰过的内联段」判漂移 ⇒ 需基点对比
        base = base_html.get(rel)
        if base is None:
            touched = list(range(len(cur_blocks)))  # 无基点 ⇒ 全段判（不漏判）
            note = "无基点内容（全段判定）"
        else:
            base_blocks = inline_blocks(base)
            base_hashes = [block_hash(b) for b in base_blocks]
            touched = [i for i, h in enumerate(cur_hashes) if h not in base_hashes]
            note = ""
        for idx in touched:
            if idx >= len(cur_blocks):
                continue
            h = cur_hashes[idx]
            if h in declared:
                continue
            seg = "%s 第 %d 段内联块（哈希 %s）" % (rel, idx + 1, h[:19])
            issues.append(
                "CSP 漂移：%s —— 本批改动页 ∩ 漂移页命中；该段内联脚本字节已变但 CSP meta 未同步"
                "%s｜修复：%s" % (seg, ("（%s）" % note if note else ""), FIX_CMD))
    return issues, notes


def run_check(report_only=False):
    base_ref, base_desc = resolve_base()
    if base_ref is None:
        print("FAIL  判据不可执行：无法确定改前基点（git 不可用）")
        print("---- CSP 增量漂移：不可执行（fail-closed）----")
        return 2
    pages = changed_pages(base_ref)
    base_html, cur_html = {}, {}
    for rel in pages:
        base_html[rel] = read_page_at(base_ref, rel)
        cur_html[rel] = read_page_worktree(rel)
    issues, notes = evaluate(pages, base_html, cur_html)
    print("基点：%s（%s）·本批改动页 %d 个" % (base_ref[:12], base_desc, len(pages)))
    for n in notes:
        print("NOTE  " + n)
    for it in issues:
        print("FAIL  " + it)
    n_fail = len(issues)
    if report_only:
        print("---- CSP 增量漂移（报告态）：%d 项 ----" % n_fail)
        return 0
    print("---- 第 56 门禁 CSP 增量漂移：%d FAIL ----" % n_fail)
    return 1 if n_fail else 0


def _self_test():
    """注入式负样本自测：改后漂移必红 / 已同步不红 / 存量漂移不归本批 / 失败信息三要素齐全。"""
    fails = []

    def html_with(body, meta):
        return ("<html><head><meta http-equiv=\"Content-Security-Policy\" content=\"%s\"></head>"
                "<body><script>%s</script></body></html>" % (meta, body))

    good_meta = "default-src 'self'; script-src 'self' 'sha256-AAA='"
    base = html_with("var a = 1;", good_meta)
    b_blocks = inline_blocks(base)
    b_hash = block_hash(b_blocks[0])

    # T1 改后内联块变了 + meta 未更新 ⇒ 必红
    cur = html_with("var a = 2;", good_meta)
    issues, _ = evaluate(["p.html"], {"p.html": base}, {"p.html": cur})
    if not issues:
        fails.append("T1 改后漂移必红未命中")
    else:
        # T2 失败信息三要素齐全（页 / 段标识 / 修复命令）
        msg = issues[0]
        if "p.html" not in msg:
            fails.append("T2 失败信息缺漂移页")
        if "第 1 段" not in msg:
            fails.append("T2 失败信息缺命中段标识")
        if FIX_CMD not in msg:
            fails.append("T2 失败信息缺修复命令")
    # T3 meta 已同步（meta 含**改后**内容的正确哈希）⇒ 不红
    cur_blocks3 = inline_blocks(html_with("var a = 2;", good_meta))
    h3 = block_hash(cur_blocks3[0])
    cur_ok = html_with("var a = 2;", "default-src 'self'; script-src 'self' '%s'" % h3)
    issues3, _ = evaluate(["p.html"], {"p.html": base}, {"p.html": cur_ok})
    if issues3:
        fails.append("T3 meta 已同步不应误报：%s" % issues3)
    # T4 存量漂移页不在本批改动页集合 ⇒ 不判红（交集判红）
    issues4, _ = evaluate([], {}, {"other.html": html_with("var x=1;", good_meta)})
    if issues4:
        fails.append("T4 存量漂移不应归本批：%s" % issues4)
    # T5 无基点 ⇒ 全段判（不漏判）
    issues5, _ = evaluate(["p.html"], {"p.html": None}, {"p.html": cur})
    if not issues5:
        fails.append("T5 无基点时须全段判定（不漏判）")
    # T6 内联块与 generate_csp 口径一致（字节相同 ⇒ 哈希相同）
    if block_hash(b_blocks[0]) != b_hash:
        fails.append("T6 哈希口径自洽性破坏")
    # T7 未改动的内联块漂移但 meta 里有其旧哈希 ⇒ 段落级命中（本批碰过的那段）
    cur_mix = html_with("var a = 2;", good_meta)
    issues7, _ = evaluate(["p.html"], {"p.html": base}, {"p.html": cur_mix})
    if not issues7:
        fails.append("T7 段级命中失败")

    for f in fails:
        print("FAIL  " + f)
    total = 7
    print("---- 第 56 门禁 CSP 增量漂移 self-test：%d/%d 通过 ----" % (total - len(fails), total))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description="内联脚本 CSP 零漂移增量判据（第 56 槽）")
    ap.add_argument("--gate", action="store_true", help="门禁态（默认行为）")
    ap.add_argument("--report", action="store_true", help="只报告不判红")
    ap.add_argument("--self-test", action="store_true", help="注入式负样本自测")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    return run_check(report_only=args.report)


if __name__ == "__main__":
    sys.exit(main())
