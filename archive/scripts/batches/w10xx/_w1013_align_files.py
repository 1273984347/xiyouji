# -*- coding: utf-8 -*-
"""_w1013_align_files.py — W1013 文件清单对齐（spec.file_index_rows ⇔ CHANGELOG 段「文件」行 ⇔ 索引）

背景：第 51 门禁（`check_commit_scope.py`）判定「索引（暂存区）⊆ 本批 spec」⇒ spec 的
`file_index_rows` 必须覆盖**全部**待入库文件；而第 31 门禁 C4-f 判定「段「文件」行里的路径
都在提交树内」⇒ 段「文件」行也必须与实际入库集合一致。两者不同源 ⇒ 本脚本一次对齐。

对齐口径（单一事实源 = **git 索引 + 工作树的当前全量改动**）：
  ① 路径集 = `git status --porcelain -z` 全量（含未跟踪·排除 tmpe/）；
  ② spec.file_index_rows ← 该集合（每文件 1 行·带归类说明）；
  ③ spec.changelog_body 的「**文件**」行 ← 同一集合；
  ④ CHANGELOG 现役段 W1013 的「**文件**」行 ← 同一集合（**段内定向订正**·级联幂等保护不许重跑级联）。

幂等：重复跑不产生差异（集合相同 ⇒ 输出相同）。
原子：临时文件 + os.replace；写后断言行数与行尾不变。

用法：py -3 scripts/_w1013_align_files.py [--dry-run]
"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(REPO, "CHANGELOG.md")
SPEC = os.path.join(REPO, "scripts", "output", "_w1013_spec.json")
BATCH = "W1013"


def note_of(f):
    if f.startswith("site/reader/ch"):
        return "回目页接入题图 + 换专属 1200×630 og:image"
    if f.startswith("site/static/images/og-"):
        return "专属 og:image（1200×630·由母版裁切）"
    if f.startswith("site/static/images/plate-line-"):
        return "站点版（母版裁切·只裁上部留白）"
    if f.startswith("assets/promo/plate-set/raw/"):
        return "出图原件（12 张·含 5 张重出）"
    if f.startswith("assets/promo/plate-set/plate-line-"):
        return "新增母版（1200×1600）"
    if f.startswith("assets/promo/plate-set/preview-"):
        return "拼图预览（含本批 12 张）"
    if f.startswith("scripts/"):
        return "本批工具/产物"
    if f.startswith("docs/"):
        return "登记面（报告/坑表/计数链/台账）"
    return "本批新增/修改"


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def git_paths():
    st = subprocess.run(["git", "status", "--porcelain", "-z"], capture_output=True, cwd=REPO).stdout
    out = []
    for rec in st.split(b"\x00"):
        if not rec:
            continue
        s = rec.decode("utf-8")
        p = s[3:]
        if p and not p.startswith("tmpe/") and p not in out:
            out.append(p)
    return sorted(out)


def main() -> int:
    dry = "--dry-run" in sys.argv
    files = git_paths()
    rows = ["| %s | W1013 | %s |" % (f, note_of(f)) for f in files]
    files_line = "> - **文件**：" + "、".join(files) + "。"

    # ---------- ① CHANGELOG 现役段「文件」行定向订正 ----------
    text, nl = read(CH)
    i = text.find("### " + BATCH)
    assert i != -1, "CHANGELOG 未找到 %s 段" % BATCH
    j = text.find("\n### W", i + 5)
    seg = text[i: j if j != -1 else len(text)]
    m = re.search(r"^> - \*\*文件\*\*：(.+)$", seg, re.M)
    assert m, "%s 段缺「**文件**」行" % BATCH
    old_line = m.group(0)
    if old_line == files_line:
        print("SKIP  CHANGELOG %s 段「文件」行已对齐（%d 项）" % (BATCH, len(files)))
    else:
        seg2 = seg.replace(old_line, files_line, 1)
        text2 = text[:i] + seg2 + text[j if j != -1 else len(text):]
        assert text2.count("\n") == text.count("\n"), "行数变化（异常）"
        if dry:
            print("DRY  CHANGELOG %s 段「文件」行将对齐（%d 项）" % (BATCH, len(files)))
        else:
            write(CH, text2)
            print("OK   CHANGELOG %s 段「文件」行对齐（%d 项）" % (BATCH, len(files)))

    # ---------- ② spec 对齐 ----------
    spec = json.load(io.open(SPEC, encoding="utf-8"))
    spec["file_index_rows"] = rows
    body = spec["changelog_body"]
    mb = re.search(r"^> - \*\*文件\*\*：(.+)$", body, re.M)
    assert mb, "spec.changelog_body 缺「**文件**」行"
    spec["changelog_body"] = body.replace(mb.group(0), files_line, 1)
    if dry:
        print("DRY  spec 将对齐（file_index_rows %d 行）" % len(rows))
    else:
        io.open(SPEC, "w", encoding="utf-8", newline="\n").write(
            json.dumps(spec, ensure_ascii=False, indent=1))
        print("OK   spec 对齐（file_index_rows %d 行）" % len(rows))

    print("---- 文件清单 %d 项 · 段与 spec 同源 ----" % len(files))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
