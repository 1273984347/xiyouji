# -*- coding: utf-8 -*-
"""_w1001_stage.py — W1001 级联准备：移除手工插入的临时段 + 生成 W1001 spec

背景：级联（`batch_cascade`）的幂等保护是「现役段号 + 1 = 本批号」⇒ 我手工插入 `### W1001`
段后，级联会以为下一个批号是 W1002 ⇒ 断言失败、**14 个版本面无法推进**（门禁 6 处红：
HANDOVER 里程碑 / workflows README 头部与里程碑 / CHANGELOG 编号规则与「最后更新」链首 /
CITATION.cff version / 索引健康 / 目录文档新鲜度）。

正解：**先把手工插入的 W1001 段摘掉** ⇒ 级联看到现役段 = W1000 ⇒ new_w = 1001 ⇒
断言通过 ⇒ 由级联**正式插入 W1001 段并推进全部版本面**（这才是版本面推进的唯一正确路径）。

步骤：
  ① 摘除 CHANGELOG / file-index 里手工插入的 W1001 段（幂等·可重复跑）
  ② 生成 scripts/output/_w1001_spec.json（batch=W1001·文件行按 git 现状全量列出）

用法：py -3 scripts/_w1001_stage.py [--dry-run]
"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _w999_closeout import BODY, FILES  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
CH = os.path.join(REPO, "CHANGELOG.md")
FI = os.path.join(OUT, "file-index.md")
SPEC = os.path.join(OUT, "_w1001_spec.json")

MY_HDR = "### W1001（2026-10-28）：回次 og:image 全覆盖批·第一轮试点（12 张线描立像/场面）"
MY_FI = "## W1001 回次 og:image 全覆盖批·第一轮试点（2026-10-28）"


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def strip_changelog(text):
    """摘除手工插入的 W1001 段（从段标题到下一个 `### W` 段之前）。"""
    if MY_HDR not in text:
        return text, False
    i = text.index(MY_HDR)
    j = text.find("\n### W", i + 1)
    if j < 0:
        j = len(text)
    else:
        j += 1
    return text[:i] + text[j:], True


def strip_fileindex(text):
    if MY_FI not in text:
        return text, False
    i = text.index(MY_FI)
    j = text.find("\n## W", i + 1)
    if j < 0:
        j = len(text)
    else:
        j += 1
    return text[:i] + text[j:], True


def main() -> int:
    dry = "--dry-run" in sys.argv

    # ① 摘除临时段
    for p, fn in ((CH, strip_changelog), (FI, strip_fileindex)):
        t, n = read(p)
        t2, removed = fn(t)
        if removed:
            if dry:
                print("DRY  %s：摘除手工插入的 W1001 段" % os.path.basename(p))
            else:
                write(p, t2, n)
                print("OK   %s：已摘除手工插入的 W1001 段" % os.path.basename(p))
        else:
            print("SKIP  %s 无手工 W1001 段" % os.path.basename(p))

    # ② 生成 W1001 spec（文件行按 git 现状全量列出）
    st = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=REPO).stdout
    df = subprocess.run(["git", "diff", "--name-only", "HEAD"], capture_output=True, text=True, cwd=REPO).stdout
    tracked = set(x.strip() for x in df.splitlines() if x.strip())
    for ln in st.splitlines():
        if ln[:2] == "??":
            tracked.add(ln[3:].strip().strip('"').replace("\\", "/"))
    files = sorted(f for f in tracked if not any(
        s in f for s in ("_commit_msg", "_serve.log", "_serve.err", "_w1000_spec", "_cascade_files_W1000")))
    files = [f for f in files if f not in ("docs/agent/adversarial-audit-prompt.md",
                                           "scripts/check_audit_trigger.py")]
    # 补上被并行会话提交入库的本批资产与页面（HEAD 树里有·工作树已干净）
    for f in FILES:
        if f not in files and os.path.exists(os.path.join(REPO, f.replace("/", os.sep))):
            files.append(f)
    files = sorted(set(files))

    rows = []
    for f in files:
        note = "本批新增/修改"
        if f.startswith("site/reader/ch"):
            note = "回目页接入题图 + 换专属 1200×630 og:image"
        elif f.startswith("site/static/images/og-"):
            note = "专属 og:image（1200×630·由母版裁切）"
        elif f.startswith("site/static/images/plate-line-"):
            note = "站点版（母版裁切·只裁上部留白）"
        elif f.startswith("assets/promo/plate-set/raw/"):
            note = "出图原件（12 张·含重出）"
        elif f.startswith("assets/promo/plate-set/plate-line-"):
            note = "新增母版（1200×1600）"
        elif f.startswith("scripts/"):
            note = "本批工具/产物"
        elif f.startswith("docs/"):
            note = "登记面（报告/坑表/计数链/方法论/台账）"
        rows.append("| %s | W1001 | %s |" % (f, note))

    body = BODY.replace("**W999**", "**W1001**").replace("让号 **W999**", "再让号 **W1001**")
    spec = {
        "batch": "W1001",
        "date": "2026-10-28",
        "title": "W1001 回次 og:image 全覆盖批·第一轮试点（12 张线描立像/场面）",
        "desc": "回次 og:image 全覆盖批 第一轮试点：12 张线描立像/场面接入 12 个回目页并换专属 1200×630 og:image",
        "head_entry": "2026-10-28（W1001 回次 og:image 全覆盖批 第一轮试点 12 张）",
        "head_sentence": "回次 og:image 全覆盖首轮试点：12 张线描立像/场面接入 12 个回目页并换专属 og:image",
        "changelog_body": body,
        "milestone_block": ("- **W1001 回次 og:image 全覆盖批·第一轮试点**（12 张线描立像/场面）：\n"
                            "  - 缺口实读修正：80 回（初查 92 系盘点正则过严）· 回目覆盖 8 → 20 回\n"
                            "  - 母版段两变体：立像段逐字 249 字符 + 场面段仅改 3 处\n"
                            "  - 12 张主体全部避开已出的 34 个角色 · 5 张重出（1 张判据红 + 4 张人眼抓）\n"
                            "  - 裁切判据改主体口径（连通簇）消除假红 · 坑表 +4 条"),
        "agents_note": ("2026-10-28（W1001）给回目页补 og:image，出了 12 张试点。"
                        "先扫已出主体清单，主体全挑没出现过的角色或新场面；"
                        "母版段只改三处派生场面变体；裁切判据会假红——它把朱砂点睛当成了主体。"
                        "最要紧：判据也要被复核。"),
        "file_index_rows": rows,
    }
    with open(SPEC, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(spec, ensure_ascii=False, indent=1))
    print("spec 写出 · %s · 文件清单 %d 项 · file_index %d 行"
          % (os.path.basename(SPEC), len(files), len(rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
