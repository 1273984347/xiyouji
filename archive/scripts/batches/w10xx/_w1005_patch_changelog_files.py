# -*- coding: utf-8 -*-
"""_w1005_patch_changelog_files.py — W1005 段「**文件**」行定向订正（补本批新增件）

背景：`batch_cascade` 有幂等保护（段已落盘不能重跑级联）⇒ 段内订正只能做**定向替换**
（W988 批先例）。本脚本只做一件事：把 W1005 段「**文件**」行的**末项后**追加本批新增件路径。

安全约束（fail-closed）：
  ① 只在 `### W1005` 段范围内定位该行（段止于下一个 `### W` 标题）；
  ② 追加前逐路径查重（已在清单内则跳过 ⇒ 幂等）；
  ③ 只允许追加白名单内的路径（`ALLOW` 集合），其它路径一律中止；
  ④ 写盘走「临时文件 + os.replace」原子替换 + 写后行数/行尾不变断言。

用法：py -3 scripts/_w1005_patch_changelog_files.py [--dry-run]
"""
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(REPO, "CHANGELOG.md")
BATCH = "W1005"

# 本批新增件白名单（只允许追加这些路径）
ALLOW = [
    "docs/11-方案报告/计划方案/T36-任务计划执行与经验沉淀报告-2026-10-29.md",
    "scripts/_w1005_fix_tail_sep.py",
    "scripts/_w1005_probe_asset_sizes.py",
    "scripts/_w1005_probe_cascade_line.py",
    "scripts/_w1005_probe_changelog_files.py",
    "scripts/_w1005_patch_changelog_files.py",
    "scripts/check_cascade_line_anchor.py",
    "tests/unit/test_cascade_line_anchor.py",
]


def decode_octal(s):
    return re.sub(
        r"((?:\\[0-7]{3})+)",
        lambda mm: bytes(int(x, 8) for x in re.findall(r"\\([0-7]{3})", mm.group(1))).decode("utf-8"),
        s,
    )


def main() -> int:
    dry = "--dry-run" in sys.argv
    raw = io.open(P, "rb").read()
    text = raw.decode("utf-8")

    i = text.find("### " + BATCH)
    assert i != -1, "CHANGELOG 未找到 %s 段" % BATCH
    j = text.find("\n### W", i + 5)
    seg = text[i: j if j != -1 else len(text)]
    assert "**文件**" in seg, "%s 段缺「**文件**」行" % BATCH

    lines = seg.split("\n")
    idx = next(k for k, l in enumerate(lines) if "**文件**" in l)
    line = lines[idx]
    decoded = decode_octal(line)
    items = [x.strip().strip('"').strip() for x in decoded.split("、") if x.strip()]

    todo = []
    for p in ALLOW:
        assert p in ALLOW, "白名单校验失败"
        if p not in items:
            todo.append(p)
    if not todo:
        print("SKIP  清单已含全部本批新增件（幂等）")
        return 0

    body = line.rstrip()
    assert body.endswith("。"), "该行尾部形态与预期不符（末字非「。」）：%r" % body[-20:]
    body = body[:-1]
    new_line = body + "、" + "、".join(todo) + "。"

    out = text[:i] + seg.replace(line, new_line, 1) + text[j if j != -1 else len(text):]
    assert out.count("\n") == text.count("\n"), "行数变化（异常）"

    print("追加 %d 条：%s" % (len(todo), "、".join(todo)))
    if dry:
        print("DRY  将写入 %d 行" % (sum(1 for _ in [0])))
        return 0

    tmp = P + ".tmp"
    io.open(tmp, "wb").write(out.encode("utf-8"))
    os.replace(tmp, P)
    raw2 = io.open(P, "rb").read()
    assert raw2.count(b"\r\r\n") == 0, "写后 CRCRLF ≠ 0"
    assert raw2.count(b"\n") == raw.count(b"\n"), "写后行数变化"
    print("OK   W1005 段「文件」行 +%d 条（原子替换·行尾与行数不变）" % len(todo))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
