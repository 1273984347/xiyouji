"""W1016 单元测试·check_doc_sync._parse_status_z（git status -z 解析）

为什么单独立测：W1014 修了 C4-f「中文路径被八进制转义误判漏 add」的 bug，但**没加测试**
——修复无回归锁（本次自审才发现）。本文件用合成 porcelain -z 串锁住三个易错点：
  ① 中文路径原样保留（不转义·不截断）；
  ② rename 是**两条**记录、次条（old path）**无 XY 前缀**，不得被当脏件（曾产出 "ipts/…"）；
  ③ 只收 **Y 位非空**（工作树态有改动）——已暂存件 `M ` 不属于 dirty（曾 78 件全误判）。

运行：py -3 -m pytest tests/unit/test_status_z_parse.py -q
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_doc_sync as cds  # noqa: E402


def _rec(status, path):
    return "%s %s" % (status, path)


def test_chinese_path_preserved_verbatim():
    """中文路径必须原样返回（不转义、不丢前缀）。"""
    raw = "\0".join([_rec(" M", "docs/00-导读/项目说明.md"), ""])
    assert cds._parse_status_z(raw) == ["docs/00-导读/项目说明.md"]


def test_staged_only_entry_is_not_dirty():
    """`M `（已暂存·Y 位空）不算 dirty——只有 ` M`/`MM` 等 Y 位非空才算。"""
    raw = "\0".join([_rec("M ", "scripts/a.py"), _rec(" M", "scripts/b.py"), ""])
    assert cds._parse_status_z(raw) == ["scripts/b.py"]


def test_rename_second_record_not_collected_as_dirty():
    """rename 双记录：次条 old path 无 XY 前缀，不得被收（曾产出 "ipts/…" 截断路径）。"""
    raw = "\0".join([
        _rec("R ", "archive/scripts/batches/w10xx/_w1013_a.py"),  # new
        "scripts/_w1013_a.py",                                     # old（无状态位）
        _rec(" M", "scripts/c.py"),
        "",
    ])
    out = cds._parse_status_z(raw)
    assert "scripts/_w1013_a.py" not in out, out
    assert all(not x.startswith("ipts/") for x in out), out
    # `R ` 的 Y 位为空（纯暂存 rename）⇒ 也不算 dirty
    assert out == ["scripts/c.py"], out


def test_untracked_and_modified_both_collected():
    raw = "\0".join([_rec("??", "scripts/_w1016_pick.py"), _rec("MM", "scripts/d.py"), ""])
    assert cds._parse_status_z(raw) == ["scripts/_w1016_pick.py", "scripts/d.py"]


def test_empty_and_none_input_safe():
    assert cds._parse_status_z("") == []
    assert cds._parse_status_z(None) == []
