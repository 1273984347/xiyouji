"""W1314 交接文档结构断言判据校正（尾链 / 四段骨架）。

两条存量假阳性（W1312/W1313 收官链连续误报「需人工核查」的根因）：
  ① 尾链：原实现 `txt[rfind("最后更新："):]` 命中「维护契约」段内的**引用行**
     ⇒ 尾链 = 整篇正文 ⇒ 日期计数恒 >3 / 首条 W 取自正文进度 ⇒ 每批必误报。
     正确判据 = 同一条 `> 最后更新：` 行内的日期条目 ≤3（维护契约②「最新 1–3 批」）。
  ② 九段：原实现要求 `## 九、使用说明`，该段已随 W707 结构收敛退役；现役维护契约
     明确「零 / 一 / 二 / 三」四段骨架 ⇒ 判据改为四段存在且有序。

口径：这两条是**判据校正**（对齐文档现行契约），不是放宽阈值。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

import batch_cascade as bc  # noqa: E402

BATCH = "W1314"

SECTIONS = (
    "## ⚠️ 零、当前阻塞",
    "## 一、当前进度",
    "## 二、下一步方向候选清单",
    "## 三、方法论沉淀",
)


def _doc(last_updated=None, sections=SECTIONS):
    """构造一份符合现行契约的最小交接文档（含两条「最后更新」引用行以复现旧假阳性）。"""
    if last_updated is None:
        last_updated = (
            "> 最后更新：2026-11-24（W1314 判据校正）·2026-11-24（W1313 CSP 治本）"
            "·（W1260 及更早批次详见 CHANGELOG.md）"
        )
    head = "# 交接文档\n\n"
    contract = (
        '> **阅读契约**：只读「零、当前阻塞」+「一、当前进度」+ 文件末尾「最后更新」链。\n'
        '> **维护契约**：「最后更新」行只写最新 1–3 批摘要。\n'
    )
    body = "\n".join(f"{s}\n\n正文\n" for s in sections)
    pointer = "> 历史概要（W1308 及更早）的详细记录见 [CHANGELOG.md](CHANGELOG.md)\n"
    return head + contract + last_updated + "\n\n" + body + pointer


def test_clean_doc_has_no_issues():
    """基准样本零告警——旧实现在此样本上会误报「尾链异常」（尾链取到维护契约后的正文）。"""
    assert bc.audit_handover_text(_doc(), BATCH) == []


def test_tail_counts_only_last_updated_line():
    """尾链只量 `> 最后更新：` 行：正文里出现日期不影响判定。"""
    txt = _doc().replace("正文", "正文（2026-01-01 的旧记录）")
    assert bc.audit_handover_text(txt, BATCH) == []


def test_last_updated_over_three_batches_flags():
    """`最后更新` 行超过 3 条日期 ⇒ 判红（维护契约②）。"""
    line = (
        "> 最后更新：2026-11-24（W1314 甲）·2026-11-24（W1313 乙）"
        "·2026-11-24（W1312 丙）·2026-11-23（W1311 丁）"
    )
    issues = bc.audit_handover_text(_doc(last_updated=line), BATCH)
    assert any("尾链" in s for s in issues), issues


def test_last_updated_first_entry_must_be_batch():
    """`最后更新` 行首条 W 必须等于本批号。"""
    line = "> 最后更新：2026-11-24（W1313 旧批）·2026-11-24（W1312 更旧）"
    issues = bc.audit_handover_text(_doc(last_updated=line), BATCH)
    assert any("头链" in s for s in issues), issues


def test_missing_third_section_flags():
    """四段骨架缺「三、方法论沉淀」⇒ 判红（替代旧「九、使用说明」判据）。"""
    sections = tuple(s for s in SECTIONS if "三、" not in s)
    issues = bc.audit_handover_text(_doc(sections=sections), BATCH)
    assert any("四段骨架" in s for s in issues), issues


def test_section_order_broken_flags():
    """段序破坏（一在零前）⇒ 判红。"""
    sections = (SECTIONS[1], SECTIONS[0], SECTIONS[2], SECTIONS[3])
    issues = bc.audit_handover_text(_doc(sections=sections), BATCH)
    assert any("四段骨架" in s for s in issues), issues


def test_ninth_section_no_longer_required():
    """文档没有「九、使用说明」也不得告警（该段已退役·旧判据的假阳性本体）。"""
    issues = bc.audit_handover_text(_doc(), BATCH)
    assert not any("九、" in s for s in issues), issues
