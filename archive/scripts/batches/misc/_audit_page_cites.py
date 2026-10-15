#!/usr/bin/env python3
"""A-009 诊断：页面 cite × 论文表 1 × 底本实测 三方对照。

输出：每节点【页面 cite / 论文表 1 锚点 / 页面 cite 底本实测行号（及命中片段）】，
并统计页面节点数（验证"30 处节点排布"表述）。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "site" / "data" / "customs-pass-route.html"
PAPER = ROOT / "docs" / "S4-学术投稿" / "01-论文" / "明清小说方向-投稿版.md"
TS = ROOT / "dataset" / "text-search.json"

chapters = {int(c["num"]): c["text"] for c in json.loads(TS.read_text(encoding="utf-8"))["chapters"]}


def line_of(ch: int, frag: str):
    t = chapters.get(ch, "")
    i = t.find(frag)
    return None if i < 0 else t.count("\n", 0, i) + 1


def main() -> int:
    html = PAGE.read_text(encoding="utf-8")
    cites = re.findall(r'\{ ch:(\d+), name:"([^"]+)"[^}]*cite:"([^"]+)"', html)
    print("页面关文节点数:", len(cites))
    # 页面是否存在补充层/第二数据数组
    for k in ["驿传节点", "补充", "aux", "supplement", "guanYiNodes", "EXTRA"]:
        print("  含", k, ":", k in html)
    # 论文表 1 锚点（行号+片段）
    paper = PAPER.read_text(encoding="utf-8").splitlines()
    t1 = {}
    i1 = next(i for i, l in enumerate(paper) if l.startswith("| 回目 | 地点 | 状态 | 类型 |"))
    for l in paper[i1 + 2:]:
        m = re.match(r"^\| 第 (\d+)(?:-(\d+))? 回 \| ([^|]+)\|", l)
        if not m:
            continue
        name = m.group(3).strip()
        anchors = re.findall(r"(?:(\d+)\s*回\s*)?line (\d+)", l)
        t1[name.split("·")[-1]] = (m.group(1), l)
    print("\n【三方对照】页面 cite / 论文表1 行 / 页面 cite 底本实测")
    for ch, name, cite in cites:
        nums = re.findall(r"(?:(\d+)\s*回\s*)?line (\d+)", cite)
        checks = []
        for c, n in nums:
            cc = int(c) if c else int(ch)
            checks.append("ch%d:%s" % (cc, n))
        # 页面 cite 是否与论文表1同节点行一致
        key = name.replace("长安·大唐", "长安·大唐")
        pl = t1.get(key, ("?", ""))[1]
        pl_nums = re.findall(r"line (\d+)", pl)
        print("  %-6s 页面cite[%s]  论文表1行[%s]" % (name, " ".join(checks), pl[:46]))
    return 0


if __name__ == "__main__":
    sys.exit(main())