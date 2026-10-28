# -*- coding: utf-8 -*-
"""_w1005_probe_cascade_line.py — 探针：级联 _face_three_docs 第二个正则（项目说明「当前版本」列表行）

问题：batch_cascade._face_three_docs 的第 181 行正则用 `[^·]*` 匹配旧 desc，且**无尾锚点**。
Python 字符类 `[^·]` 匹配换行符 ⇒ 旧 desc 行内若无「·」，`[^·]*` 会一路吞到下一处「·」之前
⇒ 跨行吞掉紧随其后的行首 ⇒ re.sub 替换整段匹配 ⇒ 后续行首内容被静默删除。

本探针只读，不改文件：打印正则匹配区间、是否跨行、替换前后差异行数。

用法：py -3 scripts/_w1005_probe_cascade_line.py
"""
import io
import os
import re
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(REPO, "docs", "00-导读", "项目说明.md")

PAT = re.compile(
    r"(\*\*当前(?:版本|批次)\*\*：)(?:v[\d.]+|W\d+)（[^）]*）— (?:v[\d.]+\s+)?(?:W\d+\s+)?[^·]*"
)


def main() -> int:
    raw = io.open(P, "rb").read()
    s = raw.decode("utf-8")
    m = PAT.search(s)
    if not m:
        print("[PROBE] 正则未命中")
        return 1
    seg = m.group(0)
    nl = seg.count("\n")
    print("[PROBE] 命中区间 %d..%d（长度 %d）" % (m.start(), m.end(), len(seg)))
    print("[PROBE] 匹配段内换行数 = %d ⇒ %s" % (nl, "跨行（危险）" if nl else "行内（安全）"))
    print("[PROBE] 匹配段首 120 字符：%r" % seg[:120])
    print("[PROBE] 匹配段末 120 字符：%r" % seg[-120:])
    if nl:
        for i, l in enumerate(seg.split("\n")[:4]):
            print("[PROBE]   段内第 %d 行：%r" % (i + 1, l[:140]))

    # 模拟 re.sub（只算不写）
    out = PAT.sub(r"\g<1>W1005（2026-10-29）— <新desc>", s, count=1)
    a, b = s.split("\n"), out.split("\n")
    print("[PROBE] 行数：原 %d → 替换后 %d" % (len(a), len(b)))
    if len(a) != len(b):
        print("[PROBE] [!!] 行数变化 ⇒ 发生跨行吞并")
    # 逐行找差异
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            print("[PROBE] 第 %d 行原：%r" % (i + 1, a[i][:150]))
            print("[PROBE] 第 %d 行新：%r" % (i + 1, b[i][:150]))
    # 检查旧 desc 是否残留
    if "教训入库" in out and out.count("教训入库") > 1:
        print("[PROBE] [!!] 旧 desc 片段残留 ⇒ 替换区间未覆盖整行")

    # 历史形态：W1004 批提交前的项目说明列表行
    try:
        hist = subprocess.run(
            ["git", "show", "1ff008c3:docs/00-导读/项目说明.md"],
            cwd=REPO, capture_output=True, check=True).stdout.decode("utf-8")
        for i, l in enumerate(hist.split("\n"), 1):
            if "**当前版本**" in l:
                print("[PROBE] 历史(1ff008c3) 第 %d 行：%r" % (i, l[:220]))
                print("[PROBE]   该行含「·」：%s" % ("·" in l))
    except Exception as e:  # noqa: BLE001
        print("[PROBE] 历史读取失败：%r" % (e,))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
