#!/usr/bin/env python3
"""patch_ratio.py — 补丁比影子度量（W1053 M-01·W1046 方案 M-01·不挂槽不拦提交）。

比值 =（豁免面 + 行 ÷ 判据面 + 行）——衡量一个批次「加豁免」对「修判据+补锁」的成本比。
方案 D-04 裁决：新度量永远影子先行，观察数批再议挂槽；启发式分子有误报（字面 grep），
影子期只报告不拦截。

  分子：该批 diff 的 + 行中，① 豁免/白名单/基线登记文件（exemptions/allowlist/baseline）
       的新增行；② 代码行内含豁免/waive/白名单字样的新增行。
  分母：该批 diff 的 + 行中，判据/测试/机制文件（scripts/check_*.py|js、tests/、
       scripts/mcp-server）的新增行。

用法：
  python scripts/patch_ratio.py --w 1052   # 单批比值与分子分母明细
  python scripts/patch_ratio.py --recent 3 # 最近 N 个修复/混合批的走势
"""
import argparse
import re
import subprocess
import sys

ROOT = EXEMPT_FILES_PAT = None
ROOT_RE = re.compile(r"^\+\+\+ b/(.+)$", re.M)
EXEMPT_FILE_PAT = re.compile(r"exempt|allowlist|baseline|_w864_accent|_w949_icon", re.I)
EXEMPT_WORD_PAT = re.compile(r"豁免|waive|白名单|baseline|exempt", re.I)
CRITERION_FILE_PAT = re.compile(
    r"^(scripts/check_[\w-]+\.(py|js)|tests/|scripts/mcp-server/)", re.I)


def git(*args):
    r = subprocess.run(["git", "-c", "core.quotePath=false"] + list(args),
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return r.stdout or ""


def batch_commits(w: int) -> list[str]:
    """该批的提交短 hash 列表（主题含 (w<号>) 前缀·fix/feat/chore 收官回填一体计入）。"""
    out = git("log", "--format=%h %s", "-60")
    return [ln.split()[0] for ln in out.splitlines()
            if re.search(r"\(w%d\)" % w, ln, re.I)]


def ratio(w: int) -> dict:
    hashes = batch_commits(w)
    if not hashes:
        return {"w": w, "error": "未找到该批提交（主题 grep (w%d)）" % w}
    num_exempt_file = num_exempt_word = den = 0
    samples = []
    for h in hashes:
        diff = git("show", h, "--format=", "--unified=0")
        cur_file = ""
        for ln in diff.splitlines():
            m = ROOT_RE.match(ln)
            if m:
                cur_file = m.group(1)
                continue
            if not ln.startswith("+") or ln.startswith("+++"):
                continue
            body = ln[1:]
            if CRITERION_FILE_PAT.match(cur_file or ""):
                den += 1
            if EXEMPT_FILE_PAT.search(cur_file or ""):
                num_exempt_file += 1
            elif EXEMPT_WORD_PAT.search(body):
                num_exempt_word += 1
                if len(samples) < 8:
                    samples.append("%s %s: %s" % (h[:7], cur_file[-40:], body.strip()[:60]))
    num = num_exempt_file + num_exempt_word
    return {"w": w, "commits": len(hashes), "num_exempt_file": num_exempt_file,
            "num_exempt_word": num_exempt_word, "num": num, "den": den,
            "ratio": (round(num / den, 2) if den else None), "samples": samples}


def main() -> int:
    ap = argparse.ArgumentParser(description="补丁比影子度量（W1053 M-01·不挂槽）")
    ap.add_argument("--w", type=int, help="单批 W 号")
    ap.add_argument("--recent", type=int, default=0, help="最近 N 个含 fix 的批走势")
    args = ap.parse_args()
    ws: list[int] = []
    if args.w:
        ws = [args.w]
    elif args.recent:
        out = git("log", "--format=%s", "-200")
        seen = []
        for ln in out.splitlines():
            m = re.match(r"fix\(w(\d+)\)", ln, re.I)
            if m and int(m.group(1)) not in seen:
                seen.append(int(m.group(1)))
            if len(seen) >= args.recent:
                break
        ws = sorted(set(seen))
    else:
        ap.error("需要 --w 或 --recent")
    if not ws:
        print("影子报数：未定位到目标批（范围/关键词不符）")
        return 0
    print("---- 补丁比影子（W1053 M-01·只报数不拦截·分子=豁免面+行 分母=判据面+行）----")
    for w in ws:
        r = ratio(w)
        if "error" in r:
            print("W%d：跳过（%s）" % (w, r["error"]))
            continue
        print("W%d：提交 %d 笔 · 分子 %d（豁免文件 %d + 字样行 %d）· 分母 %d · 比值 %s"
              % (w, r["commits"], r["num"], r["num_exempt_file"], r["num_exempt_word"],
                 r["den"], r["ratio"]))
        for s in r["samples"]:
            print("    · " + s)
    print("（影子口径：字面 grep 有误报；累计数批后再议挂槽·W1046 D-04）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
