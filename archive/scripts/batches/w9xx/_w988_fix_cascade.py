# -*- coding: utf-8 -*-
"""_w988_fix_cascade.py — W988 级联后定向订正（「文件」行 / file-index 段补齐 115 个新资产）

背景：`batch_cascade` 的幂等保护（第二次跑断言「批次号应为 W989」）使级联**不能重跑**；
而首次级联用的 spec 在 `git add -A` 之后生成，「本批新增资产」的判定误用了索引（`git ls-files`）
⇒ 115 个新资产没进「文件」行与 file-index 段。

本脚本做**段内定向订正**（只改 W988 段·不碰历史段）：
  ① CHANGELOG.md 的 W988 段「文件」行 → 完整 259 项
  ② scripts/output/file-index.md 的 W988 段表格 → 完整 259 行

用法：py -3 scripts/_w988_fix_cascade.py [--dry-run]
"""
import io
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.replace("\r\n", "\n").replace("\n", nl).encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in os.sys.argv
    with open(os.path.join(OUT, "_w988_spec.json"), encoding="utf-8") as fh:
        spec = json.load(fh)
    body = spec["changelog_body"]
    m = re.search(r"^> - \*\*文件\*\*：(.+)$", body, re.M)
    file_line = "> - **文件**：" + m.group(1) + "。"
    rows = spec["file_index_rows"]

    # ① CHANGELOG W988 段
    cp = os.path.join(REPO, "CHANGELOG.md")
    t, n = read(cp)
    i = t.find("### W988")
    j = t.find("### W987")
    assert i >= 0 and j > i, "未定位 W988 段"
    seg = t[i:j]
    seg2 = re.sub(r"^> - \*\*文件\*\*：.+$", lambda mm: file_line, seg, count=1, flags=re.M)
    t2 = t[:i] + seg2 + t[j:]
    if dry:
        print("DRY  CHANGELOG W988 段「文件」行：%d 项 → %d 项"
              % (seg.count("、"), file_line.count("、")))
    else:
        write(cp, t2, n)
        print("OK   CHANGELOG W988 段「文件」行已补齐：%d 项" % (file_line.count("、") + 1))

    # ② file-index W988 段
    fp = os.path.join(OUT, "file-index.md")
    t, n = read(fp)
    i = t.find("## W988 ")
    j = t.find("\n## W987 ")
    assert i >= 0 and j > i, "未定位 file-index 的 W988 段"
    seg = t[i:j]
    head = seg.split("|---|---|")[0]
    new_seg = head + "|---|---|---|\n" + "\n".join(rows) + "\n"
    t2 = t[:i] + new_seg + t[j:]
    if dry:
        print("DRY  file-index W988 段：%d 行 → %d 行"
              % (seg.count("\n| site/") + seg.count("\n| docs/") + seg.count("\n| scripts/")
                 + seg.count("\n| AGENTS") + seg.count("\n| HANDOVER") + seg.count("\n| CHANGELOG")
                 + seg.count("\n| README") + seg.count("\n| STRUCTURE") + seg.count("\n| CITATION")
                 + seg.count("\n| archive/") + seg.count("\n| site/index")
                 + seg.count("\n| site/data") + seg.count("\n| site/dukou")
                 + seg.count("\n| .github"), len(rows)))
    else:
        write(fp, t2, n)
        print("OK   file-index W988 段已补齐：%d 行" % len(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
