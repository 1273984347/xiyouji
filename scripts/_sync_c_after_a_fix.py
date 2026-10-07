#!/usr/bin/env python3
"""C 轨稿数字同步 + 新案例沉淀（2026-09-27·A 轨修复的连带影响）。

A 轨门禁加固后，全库引文行 430→433（匿名稿 3 条漂移行新纳入分母）。
同步 C 轨论文与大纲的快照数，并在 §4（一）补一段"三条引文行隐身与分母修复"
的实录（C 轨论证的核心主题：空真）。每处断言唯一命中。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "docs" / "S4-学术投稿" / "01-论文" / "可验证性方向-投稿版.md"
OUTLINE = ROOT / "docs" / "S4-学术投稿" / "可验证性方向-论文三大纲.md"

Q = chr(34)
SNIPPET = ("这一批数字在 2026-09-27 又有一处小规模变动：同批完成的 A 轨稿件修复中，"
           "核验脚本被加固——凡疑似引文行而语法漂移者一律判失败（此前会被静默跳过）。"
           "加固后，三条此前" + Q + "隐身" + Q + "的引文行（某匿名稿因回目号带空格与半角引号而从未被识别）"
           "进入核验分母并全部逐字命中，全库引文行数由 430 升至 433。三条引文的" + Q + "失而复得" + Q + ""
           "恰好说明这类基础设施的第一道风险：不是判错，而是分母里根本没有它——没有任何一处"
           "报错，也没有任何一条被核验，报告却写着" + Q + "100% 命中" + Q + "。")

PAPER_PAIRS = [
    ("430 条引文行全部命中（含本文自带的 4 条），覆盖 841 个文件，亚秒级完成（本机复测 0.47–0.81 秒）",
     "433 条引文行全部命中（含本文自带的 4 条；另 3 条为门禁加固后新纳入核验分母者），覆盖 841 个文件，亚秒级完成（本机复测 0.47–0.81 秒）"),
    ("Results: 430 quotation lines (including the four in this paper) achieved a 100% hit rate across 841 files in under a second.",
     "Results: 433 quotation lines (including the four in this paper and three that entered the denominator after the gate was hardened) achieved a 100% hit rate across 841 files in under a second."),
    ("（430 条引文行、841 个文件、亚秒级、100% 命中）", "（433 条引文行、841 个文件、亚秒级、100% 命中）"),
    ("目录全量扫描覆盖 841 个文件（含本批新增的审计报告，文档增删会使该数漂移）；通过核验的原著引文行 430 条（含本文自带的 4 条），命中率 100%；",
     "目录全量扫描覆盖 841 个文件（含本批新增的审计报告，文档增删会使该数漂移）；通过核验的原著引文行 433 条（含本文自带的 4 条，以及门禁加固后新纳入分母的 3 条），命中率 100%；"),
    ("三个数字值得分别解读。430 条引文意味着", "三个数字值得分别解读。433 条引文意味着"),
    ("当批实测给出 430 条引文行 100% 命中、841 个文件、亚秒级的成绩",
     "当批实测给出 433 条引文行 100% 命中、841 个文件、亚秒级的成绩"),
    ("（615 篇 / 841 文件 / 430 条引文 / 100% / 亚秒级 / 105 篇）为 2026-09-26 终测快照",
     "（615 篇 / 841 文件 / 433 条引文 / 100% / 亚秒级 / 105 篇）为 2026-09-27 终测快照（A 轨修复后复跑）"),
    # 新案例段：插在 §4（一）第二段之后（"…边际成本趋近于零…放在流程的哪个位置。"段尾）
    ("两者的共同启示是：核验能否常态化，不取决于技术难度，而取决于它被放在流程的哪个位置。",
     "两者的共同启示是：核验能否常态化，不取决于技术难度，而取决于它被放在流程的哪个位置。\n\n" + SNIPPET),
]

OUTLINE_PAIRS = [
    ("**430 条引文行 100% 命中（2026-09-26 终测快照·841 文件·含本文自带 4 条）**",
     "**433 条引文行 100% 命中（2026-09-27 终测快照·841 文件·含本文自带 4 条与门禁加固新纳入 3 条）**"),
]


def apply(path: Path, pairs) -> None:
    t = path.read_text(encoding="utf-8")
    for old, new in pairs:
        n = t.count(old)
        assert n == 1, "%s: count=%d: %s" % (path.name, n, old[:50])
        t = t.replace(old, new)
    path.write_text(t, encoding="utf-8")
    print("ok:", path.name)


def main() -> int:
    apply(PAPER, PAPER_PAIRS)
    apply(OUTLINE, OUTLINE_PAIRS)
    return 0


if __name__ == "__main__":
    sys.exit(main())