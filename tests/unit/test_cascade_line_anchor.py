"""W1005 单元测试·级联改写面「行锚定」不变量（第 42 门禁 C1 的四面引用面之一）。

背景：W1005 实证 `batch_cascade._face_three_docs` 的项目说明「当前版本」列表行正则用
`[^·]*` 且**无尾锚点** ⇒ Python 字符类匹配换行 ⇒ 匹配区间跨行 ⇒ `re.sub` 替换整个匹配区间
⇒ 项目说明.md 103 行→102 行，第 49 行「当前阶段」行首被静默删掉，而级联报「写后自检全部通过」。

覆盖：
  1. 判据脚本自检 0 FAIL（`check_cascade_line_anchor.check()` 不产出 issue）；
  2. 负样本有效性——复刻的旧正则**必须**在合成样本上复现跨行吞行（否则 ① 是恒真的检查）；
  3. 三面行锚定不变量——替换后行数不变且紧邻行首内容在位；
  4. 真实文件侧复核——对仓内真实 `docs/00-导读/项目说明.md` 跑被测实现，行数亦不变。

运行：py -m pytest tests/unit/test_cascade_line_anchor.py -v
"""
import io
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = REPO / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import batch_cascade as bc  # noqa: E402
import check_cascade_line_anchor as ccl  # noqa: E402

REAL_XIANGMU = REPO / "docs" / "00-导读" / "项目说明.md"


def test_judge_selfcheck_has_no_issue():
    """① 判据自检 0 FAIL——判据本身可跑且当下无违例。"""
    notes, issues = ccl.check()
    assert issues == [], "判据自检产出 issue：%r" % (issues,)
    assert len(notes) >= 4, "判据 NOTE 少于预期（行锚定 3 面 + 负样本有效性 1 条）：%r" % (notes,)


def test_negative_sample_is_effective():
    """② 负样本有效性——旧正则在合成样本上确实跨行吞行 ⇒ 行数断言非恒真。"""
    src = ccl.FAKE["docs/00-导读/项目说明.md"]
    m = ccl.OLD_LIST_LINE.search(src)
    assert m is not None, "旧正则未命中合成样本（样本形态已变）"
    assert "\n" in m.group(0), "旧正则未复现跨行匹配（样本已不能触发旧缺陷）"
    after = ccl.OLD_LIST_LINE.sub(r"\g<1>替换", src, count=1)
    assert after.count("\n") < src.count("\n"), "旧正则未复现吞行（行数未减少）"


def test_line_anchor_invariant_three_faces():
    """③ 三面行锚定不变量——行数不变 + 紧邻行首内容在位 + 版本行已更新。"""
    out = ccl._run()
    for path, src in ccl.FAKE.items():
        assert path in out, "被测实现未产出 %s 的改写结果" % path
        assert out[path].count("\n") == src.count("\n"), (
            "%s 替换后行数变化（跨行吞并复发）：%d → %d"
            % (path, src.count("\n"), out[path].count("\n")))
    proj = out["docs/00-导读/项目说明.md"]
    assert "- **当前阶段**：丙阶段内容·尾巴" in proj, "项目说明.md 紧邻行首被吞"
    assert "- **关键产出**：甲产出" in proj, "项目说明.md 次行内容被吞"
    assert "- **当前版本**：W1005（2026-10-29）— 丁、戊、己" in proj, "列表行未更新为当批"


def test_real_file_line_count_unchanged():
    """④ 真实文件侧复核——对仓内真实项目说明.md 跑被测实现，行数不变。"""
    assert REAL_XIANGMU.exists(), "真实项目说明.md 不存在：%s" % REAL_XIANGMU
    real_text = io.open(str(REAL_XIANGMU), encoding="utf-8").read()
    real_nl = "\r\n" if "\r\n" in real_text else "\n"

    def _load(path):
        if path == "docs/00-导读/项目说明.md":
            return real_text, real_nl
        return ccl.FAKE[path], "\n"

    orig_load = bc.load
    bc.load = _load
    try:
        ctx = ccl._Ctx("W1005", "2026-10-29", "丁、戊、己")
        bc._face_three_docs(ctx)
    finally:
        bc.load = orig_load
    new_text = dict((p, t) for p, t, _nl in ctx.pend)["docs/00-导读/项目说明.md"]
    assert new_text.count("\n") == real_text.count("\n"), (
        "真实项目说明.md 行数变化：%d → %d" % (real_text.count("\n"), new_text.count("\n")))


def test_module_loadable_after_promote():
    """⑤ 转正后模块名与文件名同步（去 `_` 前缀后 import 名变了·承 W1002 先例）。"""
    assert os.path.exists(str(SCRIPTS_DIR / "check_cascade_line_anchor.py")), "脚本文件缺失"
    assert hasattr(ccl, "check") and hasattr(ccl, "_run"), "判据公开接口缺失"
