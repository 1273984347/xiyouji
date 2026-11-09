import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import backfill_changelog as bf  # noqa: E402


def test_changelog_block_glued_line_guard():
    """W1157 粘行根修锁：body 非空行开场 ⇒ 渲染点**规范化补空行**（不粘行·api_diff 零破坏）。

    粘行事故实证：rebuild_section 走共享渲染点无判据 ⇒「…错位归位）**本批要点**…」
    粘行段入库（batch_cascade PRECHECK 有判据而渲染点没有的同族缺口）。
    最终形态：渲染点自动补空行（规范化兜底比 raise 更稳——任何未来入口永不粘行）。
    """
    spec_bad = {"batch": "W1157", "date": "2026-11-07",
                "title": "W1157 测试批", "changelog_body": "**本批要点**：…"}
    block = bf.changelog_block(spec_bad)
    assert block.startswith("### W1157（2026-11-07）：测试批\n\n**本批要点**"), \
        "无空行 body 未被规范化（粘行复发）：%r" % block[:60]
    spec_ok = dict(spec_bad, changelog_body="\n\n**本批要点**：…\n")
    block2 = bf.changelog_block(spec_ok)
    assert block2.startswith("### W1157（2026-11-07）：测试批\n\n**本批要点**"), \
        "空行 body 渲染形态失真：%r" % block2[:60]
    # 前导单换行残留形态不双补空行
    spec_nl = dict(spec_bad, changelog_body="\n**本批要点**：…")
    block3 = bf.changelog_block(spec_nl)
    head3 = block3.split("**本批要点**")[0]
    assert "\n\n\n" not in head3, "前导单换行被双补空行：%r" % head3
