"""W1130 批：归档迁出不得吞掉正本末尾文件级块（含编号规则串）。

背景：两面下界对齐会触发 CHANGELOG 段归档迁出；原实现迁出块取 s[cut:]
（一路到文件末尾）=> 末尾文件级块（# 更新日志标题 / 阅读契约 / Unreleased /
编号规则行 / 全站页数口径 / 维护契约）被一起搬走 => 正本不再含编号规则串
=> 版本面推进器 fail-closed「编号规则段上限未找到锚点」=> 整条收官链停摆。
根修：迁出块边界止于末尾文件级块起点，末尾块留在正本。
"""
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
if os.path.join(ROOT, "scripts") not in sys.path:
    sys.path.insert(0, os.path.join(ROOT, "scripts"))


def _load():
    spec = importlib.util.spec_from_file_location(
        "archive_segments_w1130", os.path.join(ROOT, "scripts", "archive_segments.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


SAMPLE = (
    "### W1130（2026-11-04）：新段" + chr(10) + chr(10) +
    "内容 A" + chr(10) + chr(10) +
    "### W1129（2026-11-04）：旧段" + chr(10) + chr(10) +
    "内容 B" + chr(10) + chr(10) +
    "### W1128（2026-11-04）：更旧段" + chr(10) + chr(10) +
    "内容 C" + chr(10) + chr(10) +
    "# 更新日志" + chr(10) + chr(10) +
    "> **阅读契约**：只读顶段。" + chr(10) +
    ">" + chr(10) +
    "> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W1130）。" + chr(10) + chr(10) +
    "> **维护契约**：历史段只增不删。" + chr(10)
)


def test_tail_block_start_found():
    m = _load()
    assert m._tail_block_start(SAMPLE) == SAMPLE.index("# 更新日志")


def test_tail_block_start_absent():
    m = _load()
    assert m._tail_block_start("### W1（x）：a" + chr(10) + chr(10) + "正文" + chr(10)) is None


def test_split_keeps_tail_block_in_kept():
    m = _load()
    cut = SAMPLE.index("### W1128")
    moved, kept = m.split_tail_block(SAMPLE, cut, m._tail_block_start(SAMPLE))
    assert "（W001-W1130）" not in moved
    assert "# 更新日志" not in moved
    assert "（W001-W1130）" in kept
    assert "# 更新日志" in kept
    assert "### W1128" in moved
    assert "### W1128" not in kept


def test_split_without_tail_block_is_legacy_behavior():
    m = _load()
    cut = 5
    moved, kept = m.split_tail_block(SAMPLE, cut, None)
    assert moved == SAMPLE[cut:]
    assert kept == SAMPLE[:cut]


def test_split_tail_block_stays_file_tail():
    m = _load()
    cut = SAMPLE.index("### W1129")
    tail = m._tail_block_start(SAMPLE)
    moved, kept = m.split_tail_block(SAMPLE, cut, tail)
    assert moved == SAMPLE[cut:tail]
    assert kept == SAMPLE[:cut] + SAMPLE[tail:]
    assert kept.endswith("> **维护契约**：历史段只增不删。" + chr(10))


# W1192：_a3_ok 的末尾块分支原写成 `not new_src.endswith(src_text[tail:])`，
#   与 split_tail_block「末尾块留在正本末尾」的行为相互矛盾 ⇒ 该分支恒假 ⇒
#   CHANGELOG 体积模式迁移必红（W1192 实测：264907 B 超上限触发迁移后 A3 AssertionError）。
#   下列三例把判据语义钉死：末尾块逐字节留在正本末尾 = 通过；前缀被改 = 拦截；
#   末尾块被搬走 = 拦截。
def test_a3_ok_accepts_tail_block_kept_at_file_end():
    m = _load()
    cut = SAMPLE.index("### W1129")
    tail = m._tail_block_start(SAMPLE)
    moved, kept = m.split_tail_block(SAMPLE, cut, tail)
    assert m._a3_ok(kept, SAMPLE, cut, tail) is True


def test_a3_ok_rejects_modified_prefix():
    m = _load()
    cut = SAMPLE.index("### W1129")
    tail = m._tail_block_start(SAMPLE)
    moved, kept = m.split_tail_block(SAMPLE, cut, tail)
    tampered = "X" + kept
    assert m._a3_ok(tampered, SAMPLE, cut, tail) is False


def test_a3_ok_rejects_tail_block_moved_away():
    m = _load()
    cut = SAMPLE.index("### W1129")
    tail = m._tail_block_start(SAMPLE)
    moved, kept = m.split_tail_block(SAMPLE, cut, tail)
    without_tail = kept[: len(kept) - len(SAMPLE[tail:])]
    assert m._a3_ok(without_tail, SAMPLE, cut, tail) is False
