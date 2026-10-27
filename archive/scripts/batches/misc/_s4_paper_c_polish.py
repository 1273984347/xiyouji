#!/usr/bin/env python3
"""S4 C 轨论文初稿一次性润饰脚本（2026-09-26·非入库门禁脚本）。

处理面：
1) 尾注注号重排：⑧-⑭ → ⑨-⑮（为新增 RefChecker 注 ⑧ 让位·高号先行防串位）；
2) 插入新注 ⑧（RefChecker·arXiv:2607.00738）；
3) 十二处措辞修正（归属更正/枚举去模板化/案例段去「第一步」式分步/题录提示）。

跑完打印全部断言结果；任一目标串未命中即抛错，防静默漏改。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "docs" / "S4-学术投稿" / "01-论文" / "可验证性方向-投稿版.md"

CIRCLED = {8: "\u2467", 9: "\u2468", 10: "\u2469", 11: "\u246a",
           12: "\u246b", 13: "\u246c", 14: "\u246d", 15: "\u246e"}


def main() -> int:
    t = TARGET.read_text(encoding="utf-8")
    orig = t

    # ---- 1) 注号重排（8-14 → 9-15，高号先行）----
    for n in range(14, 7, -1):
        t = t.replace(CIRCLED[n], CIRCLED[n + 1])

    # ---- 2) 插入新注 ⑧（RefChecker）----
    anchor = "blog.iclr.cc.\n"
    assert t.count(anchor) == 1, "anchor for note ⑧ not unique"
    t = t.replace(anchor, anchor + CIRCLED[8] + " Russinovich M, Siva Kumar R S, Salem A. Phantom References: Hallucinated Citations That Survive Peer Review at Top-Tier Conferences[EB/OL]. arXiv:2607.00738, 2026.（RefChecker 开源管线；写作前撞题检索发现的同域并行工作）\n")

    # ---- 3) 措辞修正（目标串逐一断言存在）----
    pairs = [
        # §2（一）归属更正：CITADEL 注应是 Lancet ①，RefChecker 数据注应是新增 ⑧
        ("。⑤更近期的一项顶会审计工作", "。①更近期的一项顶会审计工作"),
        ("每篇论文的边际成本约为四美分。①（该工作与本文同日域并行",
         "每篇论文的边际成本约为四美分。⑧（该工作与本文同域并行"),
        # §4（一）成本对比处同源更正
        ("上述顶会审计工作给出的成本是每篇论文约四美分①；",
         "上述顶会审计工作给出的成本是每篇论文约四美分⑧；"),
        # §2（四）去「其一其二」
        ("其一，\"中文古典文献\"。", "第一个限定词是\"中文古典文献\"。"),
        ("其二，\"强制门禁\"。", "第二个限定词是\"强制门禁\"。"),
        ("需要坦承两处波折：其一，本文原拟的贡献表述是",
         "需要坦承两处波折：第一处，本文原拟的贡献表述是"),
        ("其二，相邻工作的时间线相当密集", "第二处，相邻工作的时间线相当密集"),
        # §3（三）去「其一是其二是不」
        ("其一是\"只拦新增\"的基线策略。", "一个是\"只拦新增\"的基线策略。"),
        ("其二是不对称的交付纪律。", "另一个是不对称的交付纪律。"),
        # §3（三）语序
        ("项目的交付门禁是一个预提交钩子挂在版本控制上的校验入口",
         "项目的交付门禁是一个挂在版本控制预提交钩子上的校验入口"),
        # §4（二）案例段：去除「第一步/第二步/第三步」分步，改流动行文；补题录提示；当天
        ("它存活了三周，途径如下。第一步，它以\"项目索引已收录\"的形态获得了看似权威的出处；第二步，论文写作把它当作真实文献转述、引用；第三步，审读质疑触发了对抗性自查——对全部可验证声明做实测，对高风险参考文献逐条联网核验。",
         "它存活了三周。先是它以\"项目索引已收录\"的形态获得了看似权威的出处，随后被论文写作当作真实文献转述、引用；直到审读质疑触发对抗性自查——对全部可验证声明做实测，对高风险参考文献逐条联网核验。"),
        ("它的完整形制是：\"竺洪波, 张培恒.",
         "它的完整形制是（经核验为幻觉条目，切勿引用）：\"竺洪波, 张培恒."),
        ("第一道是 AI 率检测：", "一道是 AI 率检测："),
        ("第二道是人工抽查：", "另一道是人工抽查："),
        ("在一天内拼出来", "在当天拼出来"),
        # §5（四）去「第二种/第三种风险」
        ("第二种风险是维护负担的隐形转嫁。", "与之相伴的还有维护负担的隐形转嫁。"),
        ("第三种风险属于所有核验工具的固有局限：",
         "还有一种风险属于所有核验工具的固有局限："),
    ]
    for old, new in pairs:
        assert t.count(old) == 1, "target not unique/found: %s" % old[:40]
        t = t.replace(old, new)

    TARGET.write_text(t, encoding="utf-8")

    # ---- 验证输出 ----
    print("renumbered_notes_present:", all(CIRCLED[n] in t for n in range(8, 16)))
    print("note_8_entry:", "Phantom References" in t and "arXiv:2607.00738" in t)
    print("residual_qi_er:", t.count("其一，") + t.count("其二，"),
          t.count("第一步，") + t.count("第二步，"),
          t.count("第二种风险"), t.count("第三种风险"))
    print("chars_now:", len(re.sub(r"\s+", "", t)), "delta:", len(t) - len(orig))
    print("quotes_fmt:")
    for ln in t.splitlines():
        if ln.startswith("> 原文引文"):
            print("   ", ln)
    return 0


if __name__ == "__main__":
    sys.exit(main())
