#!/usr/bin/env python3
"""创意三明治管线一致性轻量校验（P3-7，W508 沉淀）。

扫描 docs/01-06 中含「创意三明治管线」标记的文档，校验其元信息块 `> 生成来源`
是否与管线身份一致——管线产出必须记 `创意三明治管线@<commit>`，禁止写
`xiyouji-character-content@…`（W505 SKILL.md 配套要求：以留可追溯证据）。

校验项：
- C1 管线标记存在性：文档含「创意三明治管线」字样（正文或元信息块）
- C2 生成来源一致性：管线文档的 `> 生成来源` 必须以 `创意三明治管线@` 开头
- C3 引文底线：管线方向二/深化文档须 ≥3 条 `> 原文引文（第N回）`（对齐 W503 硬规则）

用法：
  py scripts/_check_pipeline_consistency.py            # 全量扫描 docs/01-06
  py scripts/_check_pipeline_consistency.py --file X   # 单文件

说明：诊断工具（_ 前缀），不入库门禁、不参与 CI；结果供人工/DRL 引用。
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = ["01-全书逐回解读", "02-人物深度分析", "03-主题与情节专题",
        "04-文化与历史背景", "05-诗词歌赋", "06-个人随笔"]
MARKER = "创意三明治管线"
CITE_RE = re.compile(r"^> 原文引文（第(\d+)回）", re.MULTILINE)


def check_file(path):
    """返回 (问题数, 检查项列表)。"""
    text = open(path, encoding="utf-8").read()
    problems = []
    if MARKER not in text:
        return 0, ["无管线标记，跳过"]
    checks = ["含管线标记"]
    m = re.search(r"^> 生成来源：([^\r\n]+)", text, re.M)
    if not m:
        problems.append("缺 生成来源 行")
    else:
        src = m.group(1).strip()
        if not src.startswith("创意三明治管线@"):
            problems.append("生成来源 %r 未以 创意三明治管线@ 开头（应记管线身份）" % src)
        else:
            checks.append("生成来源=%s" % src)
    cites = len(CITE_RE.findall(text))
    if cites < 3:
        problems.append("引文行 %d < 3（方向二/深化文档硬规则）" % cites)
    else:
        checks.append("引文 %d 条" % cites)
    return len(problems), checks + problems


def main():
    ap = argparse.ArgumentParser(description="创意三明治管线一致性轻量校验")
    ap.add_argument("--file", help="单文件模式")
    args = ap.parse_args()

    if args.file:
        files = [args.file]
    else:
        files = []
        for d in DIRS:
            dp = os.path.join(ROOT, "docs", d)
            if os.path.isdir(dp):
                files += [os.path.join("docs", d, f) for f in sorted(os.listdir(dp))
                          if f.endswith(".md") and f != "README.md"]

    total_problems = 0
    scanned = 0
    for rel in files:
        p = os.path.join(ROOT, rel) if not os.path.isabs(rel) else rel
        n, checks = check_file(p)
        scanned += 1
        if MARKER in open(p, encoding="utf-8").read():
            status = "FAIL" if n else "PASS"
            if n:
                total_problems += 1
            print("%s %s: %s" % (status, rel, " · ".join(checks)))

    if total_problems:
        print("管线一致性：扫描 %d 个文件 · %d 个管线文档存在违规" % (scanned, total_problems))
        return 1
    print("管线一致性通过：扫描 %d 个文件（管线文档全部 PASS）" % scanned)
    return 0


if __name__ == "__main__":
    sys.exit(main())
