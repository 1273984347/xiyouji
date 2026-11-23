"""W1308 单元测试·收官链 add 步的分组行展开（ignore 口径 + 中文路径）

背景：分组登记行（「<目录>/（<N 件>」）展开为待 add 路径集合。W1308 根修两处：
  ① 原实现用 os.walk 递归**磁盘** ⇒ .gitignore 忽略目录也被纳入 ⇒ git add 报
     「paths are ignored」⇒ 收官链 add 步整链中止；
  ② git ls-files 默认对非 ASCII 路径**转义**（八进制）⇒ 展开出的路径在磁盘上不存在
     ⇒ 「尚不存在」跳过 ⇒ 中文路径文件漏 add。

本文件自证：展开结果不含忽略面 + 含真实中文路径 + 精确行返回 None。

运行：py -3 -m pytest tests/unit/test_batch_closeout_group_expand.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import batch_closeout as bc  # noqa: E402


def test_expand_group_row_excludes_ignored_paths():
    """分组行展开 ⇒ 不含 .gitignore 忽略目录（否则 add 步整链中止）。"""
    out = bc._expand_group_row("docs/（1 件）")
    assert out is not None
    assert not [x for x in out if "S2-" in x]


def test_expand_group_row_keeps_real_chinese_paths():
    """展开结果含真实中文路径（非 git 的八进制转义形态）。"""
    out = bc._expand_group_row("docs/00-导读/（3 件）")
    assert out is not None
    assert any("\u6279\u6b21\u7f16\u53f7\u5bf9\u8d26\u8868" in x for x in out)


def test_exact_row_returns_none():
    """非分组行 ⇒ None（不展开）。"""
    assert bc._expand_group_row("HANDOVER.md") is None
