# -*- coding: utf-8 -*-
"""_w1005_probe_changelog_files.py — 解码 CHANGELOG W1005 段的「**文件**」行并核对提交树存在性

用途：第 31 门禁 C4-f 判「文件清单有工作树未提交残留 / 未入提交树」。本探针在提交前
独立复核同一件事，并**解码**该行的八进制转义串（段里是 JSON 字符串形态·人工读不出真实路径）。

只读脚本：不改任何文件。

用法：py -3 scripts/_w1005_probe_changelog_files.py
"""
import io
import json
import os
import re
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = "W1005"


def main() -> int:
    s = io.open(os.path.join(REPO, "CHANGELOG.md"), encoding="utf-8").read()
    i = s.find("### " + BATCH)
    assert i != -1, "CHANGELOG 未找到 %s 段" % BATCH
    j = s.find("### W", i + 5)
    seg = s[i: j if j != -1 else len(s)]

    m = re.search(r"\*\*文件\*\*：(.+)", seg)
    assert m, "%s 段缺「**文件**」行" % BATCH
    raw = m.group(1).strip().rstrip("。")
    # 段里的路径是 **Python bytes 八进制转义**（\346\211…），JSON 只认 \uXXXX ⇒ 先把八进制字节
    # 按**连续字节组**还原并按 UTF-8 解码（中文是多字节序列，不能逐字节单独解），再做 JSON 解析。
    try:
        text = re.sub(
            r"((?:\\[0-7]{3})+)",
            lambda mm: bytes(int(x, 8) for x in re.findall(r"\\([0-7]{3})", mm.group(1))).decode("utf-8"),
            raw,
        )
    except Exception as e:  # noqa: BLE001
        print("[PROBE] 八进制还原失败：%r ⇒ 原文前 200 字符：%r" % (e, raw[:200]))
        return 1
    # 该行是「"a"、"b"、c、d」混合引号形态（分隔符为全角「、」）⇒ 按顿号切分 + 去引号
    files = [x.strip().strip('"').strip() for x in text.split("、") if x.strip()]
    files = [x for x in files if x]
    print("[PROBE] %s 段「文件」行共 %d 条" % (BATCH, len(files)))

    # git 对非 ASCII 路径默认加引号并转义（core.quotepath=true）⇒ 必须用 -z 取原始路径，
    # 否则中文路径全部匹配不上（首测即误报 3 个 TREE-MISS·实为转义假象）。
    def _git_paths(args):
        out = subprocess.run(
            ["git", "-c", "core.quotepath=false"] + args + ["-z"],
            cwd=REPO, capture_output=True, check=True).stdout.decode("utf-8")
        return set(p for p in out.split("\0") if p)

    tracked = _git_paths(["ls-files"])
    staged = _git_paths(["diff", "--cached", "--name-only"])
    disk = set()
    for root, _d, fs in os.walk(REPO):
        if any(x in root for x in (os.sep + ".git", os.sep + "node_modules", os.sep + "tmpe")):
            continue
        for f in fs:
            disk.add(os.path.relpath(os.path.join(root, f), REPO).replace("\\", "/"))

    missing_tree, missing_disk, missing_stage = [], [], []
    for p in files:
        p2 = p.replace("\\", "/")
        if p2 not in tracked:
            missing_tree.append(p2)
        if p2 not in disk:
            missing_disk.append(p2)
        if p2 not in staged and p2 not in tracked:
            missing_stage.append(p2)

    print("[PROBE] 未入提交树（tracked ∪ staged 皆无）：%d" % len(missing_tree))
    for p in missing_tree:
        print("   [TREE-MISS] %s" % p)
    print("[PROBE] 磁盘不存在：%d" % len(missing_disk))
    for p in missing_disk:
        print("   [DISK-MISS] %s" % p)
    print("[PROBE] 既未 tracked 又未 staged：%d" % len(missing_stage))
    for p in missing_stage:
        print("   [STAGE-MISS] %s" % p)
    print("---- 结论：%s ----" % ("全在提交树内" if not (missing_tree or missing_stage) else "有缺口"))
    return 1 if (missing_tree or missing_stage) else 0


if __name__ == "__main__":
    raise SystemExit(main())
