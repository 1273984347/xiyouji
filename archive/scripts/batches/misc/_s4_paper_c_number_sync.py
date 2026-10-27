#!/usr/bin/env python3
"""S4 C 轨论文数字同步（2026-09-26 终测快照：新增本文后 430 条/839 文件/0.47 秒）。

背景：初稿写作时基线为 426 条/838 文件；本文自带 4 条引文行入库后，全库复跑
得到 430 条/839 文件/0.47 秒。为避免"论文数字与门禁复跑不符"，统一为终测快照
并标注口径（含本文 4 条）。任一处未命中即抛错。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "docs" / "S4-学术投稿" / "01-论文" / "可验证性方向-投稿版.md"
OUTLINE = ROOT / "docs" / "S4-学术投稿" / "可验证性方向-论文三大纲.md"

PAIRS = [
    ("全文 3 条原著引文行已过", "全文 4 条原著引文行已过"),
    ("426 条引文行全部命中，覆盖 838 个文件，耗时 0.48 秒",
     "430 条引文行全部命中（含本文自带的 4 条），覆盖 839 个文件，耗时 0.47 秒"),
    ("Results: 426 quotation lines achieved a 100% hit rate across 838 files in 0.48 seconds.",
     "Results: 430 quotation lines (including the four in this paper) achieved a 100% hit rate across 839 files in 0.47 seconds."),
    ("规模数据（426 条引文行、838 个文件、0.48 秒、100% 命中）",
     "规模数据（430 条引文行、839 个文件、0.47 秒、100% 命中）"),
    ("## 四、实证：615 篇文档中的 426 条引文", "## 四、实证：615 篇文档中的 430 条引文"),
    ("目录全量扫描覆盖 838 个文件；通过核验的原著引文行 426 条，命中率 100%；校验脚本全量运行耗时 0.48 秒。",
     "目录全量扫描覆盖 839 个文件；通过核验的原著引文行 430 条（含本文自带的 4 条），命中率 100%；校验脚本全量运行耗时 0.47 秒。"),
    ("三个数字值得分别解读。426 条引文意味着", "三个数字值得分别解读。430 条引文意味着"),
    ("838 个文件说明校验不是针对", "839 个文件说明校验不是针对"),
    ("0.48 秒说明核验成本在工程意义上可以忽略", "0.47 秒说明核验成本在工程意义上可以忽略"),
    ("当批实测给出 426 条引文行 100% 命中、838 个文件、0.48 秒的成绩",
     "当批实测给出 430 条引文行 100% 命中、839 个文件、0.47 秒的成绩"),
    ("- 量化数字（615 篇 / 838 文件 / 426 条引文 / 100% / 0.48 秒 / 105 篇）均为 2026-09-26 当批实测，命令与输出见项目交付门禁运行记录。",
     "- 量化数字（615 篇 / 839 文件 / 430 条引文 / 100% / 0.47 秒 / 105 篇）为 2026-09-26 终测快照（含本文自带的 4 条引文；文档增删会使总数漂移，复跑时以文末快照口径为准）。"),
]

OUTLINE_PAIRS = [
    ("**426 条引文行 100% 命中（2026-09-26 当批实测·838 文件）**",
     "**430 条引文行 100% 命中（2026-09-26 终测快照·839 文件·含本文自带 4 条）**"),
]


def apply(path: Path, pairs) -> None:
    t = path.read_text(encoding="utf-8")
    for old, new in pairs:
        assert t.count(old) == 1, "not unique/found in %s: %s" % (path.name, old[:50])
        t = t.replace(old, new)
    path.write_text(t, encoding="utf-8")
    print("ok:", path.name)


def main() -> int:
    apply(PAPER, PAIRS)
    apply(OUTLINE, OUTLINE_PAIRS)
    t = PAPER.read_text(encoding="utf-8")
    assert "426" not in t and "838" not in t and "0.48" not in t, "residual old numbers"
    print("residual_old_numbers: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
