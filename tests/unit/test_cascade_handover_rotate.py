"""W1308 单元测试·交接文档里程碑块的 W1144 超限补滚

背景（W1308 实测）：补滚此前**形同虚设**——
  ① 触发面：滚动只在「本批块 **inserted**」路径触发 ⇒ 「replaced」（spec 里程碑内容
     变更·同批号替换）路径永不动 ⇒ 概要块只增不减（实测 11 块 ⇒ C7 体积窗判红）；
  ② 滚动量：原每次只淘汰 1 块 ⇒ 窗口已超限时滚完仍超限。

治本：新增 _rotate_until_window（inserted/replaced 都触发·滚到窗口 ≤6 为止），
本文件自证「收敛（≤6）+ 幂等（再跑零变化）」。

运行：py -3 -m pytest tests/unit/test_cascade_handover_rotate.py -v
"""
import re
import sys
from pathlib import Path
from types import SimpleNamespace

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import batch_cascade as bc  # noqa: E402

ROOT = SCRIPTS_DIR.parent
# 与门禁 C7 / _handover_rotate_oldest 同口径的严格块正则（双星号 + 全角冒号尾约束）
BLOCK_RE = re.compile(r"^- \*\*(?:v[\d.]+ )?W(\d+)[^*]*\*+[^\r\n:*]{0,30}：", re.M)
WINDOW = 6


def _blocks(text):
    """「一、当前进度」段内的里程碑块批号列表。"""
    i = text.find("## 一、当前进度")
    j = text.find("## 二、", i)
    assert i != -1 and j > i, "未找到「一、当前进度」段边界"
    return BLOCK_RE.findall(text[i:j])


def _ctx():
    return SimpleNamespace(
        batch="W1308",
        cl_src=(ROOT / "CHANGELOG.md").read_text(encoding="utf-8"),
    )


def test_rotate_until_window_converges_to_window():
    """超限窗口下反复补滚 ⇒ 收敛到 ≤6 块。"""
    s, nl = bc.load("HANDOVER.md")
    h1pos = s.find("## 一、当前进度")
    assert h1pos != -1
    out = bc._rotate_until_window(s, _ctx(), nl, h1pos)
    assert len(_blocks(out)) <= WINDOW


def test_rotate_until_window_is_idempotent():
    """再跑一次 ⇒ 零变化（不重复淘汰·信息不丢）。"""
    s, nl = bc.load("HANDOVER.md")
    h1pos = s.find("## 一、当前进度")
    out = bc._rotate_until_window(s, _ctx(), nl, h1pos)
    out2 = bc._rotate_until_window(out, _ctx(), nl, h1pos)
    assert out2 == out


def test_rotate_until_window_preserves_history_pointer():
    """滚动后「历史概要」指针仍在（信息不丢·不悬空）。"""
    s, nl = bc.load("HANDOVER.md")
    h1pos = s.find("## 一、当前进度")
    out = bc._rotate_until_window(s, _ctx(), nl, h1pos)
    assert re.search(r"> 历史概要（W\d+ 及更早）的详细记录见", out)
