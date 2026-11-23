"""W1308 单元测试·收官链 L-11（台账 hash 回填 v2：空缺回填 / 错值修指 / 排除本批）

覆盖纯函数：
  - _parse_subject_w_ids   git log subject → 批次号集合（合并推送 subject 含多个 W 号 ⇒ 全取）
  - _prefix_sets          全量 sha 集合 → 短 hash 可达性查表
  - _hash_action          台账 hash 格 → fill / repair / keep / skip 四动作

运行：py -3 -m pytest tests/unit/test_batch_closeout_hash_repair.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import batch_closeout as bc  # noqa: E402


def test_parse_subject_scope_form():
    ids = bc._parse_subject_w_ids("fix(ci): W1301 L-02 探针跨run增量缓存（三重键）")
    assert 1301 in ids


def test_parse_subject_merge_push_multiple_ids():
    ids = bc._parse_subject_w_ids("feat: W1303 W1302 W1301 合并推送（三合一合集 + 绢本源件）")
    assert ids == {1301, 1302, 1303}


def test_parse_subject_no_batch_id():
    assert bc._parse_subject_w_ids("feat(games): 15 款西游小游戏移动端专项与 9:16 竖屏扩展") == set()


def test_prefix_sets_probe():
    probe = bc._prefix_sets({"48621ae3a" + "0" * 30, "0c926a0aa" + "0" * 30})
    assert probe("48621ae3a")
    assert probe("0c926a0aa")
    assert not probe("191e9607")


def test_hash_action_fill_placeholder():
    probe = bc._prefix_sets({"0c926a0aa" + "0" * 30})
    act, sha = bc._hash_action("—（待回填）", "0c926a0aa", probe, 1309, 1302)
    assert act == "fill" and sha == "0c926a0aa"


def test_hash_action_keep_valid_in_chain():
    probe = bc._prefix_sets({"48621ae3a" + "0" * 30})
    act, sha = bc._hash_action("48621ae3a", "48621ae3a", probe, 1309, 1300)
    assert act == "keep" and sha is None


def test_hash_action_repair_stale_value():
    probe = bc._prefix_sets({"0c926a0aa" + "0" * 30})
    act, sha = bc._hash_action("191e96078", "0c926a0aa", probe, 1309, 1301)
    assert act == "repair" and sha == "0c926a0aa"


def test_hash_action_skip_bad_shape():
    probe = bc._prefix_sets(set())
    act, sha = bc._hash_action("非hash形态", "0c926a0aa", probe, 1309, 1301)
    assert act == "skip" and sha is None
