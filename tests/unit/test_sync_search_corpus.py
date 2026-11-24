"""W1316 单元测试·站内搜索语料生成器（sync_search_corpus）。

覆盖：
  - 生成幂等：apply → check 零差异
  - 替换边界：章节块重建 + 头注释更新，characters/artifacts 等其余键保留
  - 危险序列 fail-closed：正文含反引号 → SystemExit（不写盘）
  - 方括号出现在正文中不破坏配对
  - 真实仓树零漂移（live-tree 干跑门禁）
"""
import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import sync_search_corpus


def _mk_root(tmp_path: Path, texts) -> None:
    js = (
        "\n"
        "    /* ==========================================================\n"
        "       old header\n"
        "       ========================================================== */\n"
        "    const EMBEDDED_DATA = {\n"
        "        chapters: [\n"
        "            {\n"
        "                num: 1,\n"
        '                title: "旧",\n'
        '                fullTitle: "第1回 旧",\n'
        "                text: `旧`\n"
        "            }\n"
        "\n"
        "        ],\n"
        '        characters: ["孙悟空"],\n'
        "        artifacts: []\n"
        "    };\n"
    )
    (tmp_path / "dataset").mkdir()
    (tmp_path / "site" / "static" / "js").mkdir(parents=True)
    (tmp_path / sync_search_corpus.JS_REL).write_text(js, encoding="utf-8")
    chapters = [
        {"num": i + 1, "title": "题%d" % (i + 1),
         "fullTitle": "第%d回 题%d" % (i + 1, i + 1),
         "text": texts[i]}
        for i in range(100)
    ]
    (tmp_path / sync_search_corpus.JSON_REL).write_text(
        json.dumps({"chapters": chapters}, ensure_ascii=False), encoding="utf-8")


def test_sync_applies_and_is_idempotent(tmp_path):
    _mk_root(tmp_path, ["正文%d" % i for i in range(100)])
    assert sync_search_corpus.sync(tmp_path, check=True)[0] is True, "初始内嵌块应为旧值（待同步）"
    assert sync_search_corpus.sync(tmp_path)[0] is True
    out = (tmp_path / sync_search_corpus.JS_REL).read_text(encoding="utf-8")
    assert "text: `正文0`" in out
    assert "old header" not in out
    assert 'characters: ["孙悟空"]' in out, "章节块之外的键不得被替换"
    assert sync_search_corpus.sync(tmp_path, check=True)[0] is False, "重建后应幂等（零差异）"


def test_check_mode_does_not_write(tmp_path):
    _mk_root(tmp_path, ["正文%d" % i for i in range(100)])
    before = (tmp_path / sync_search_corpus.JS_REL).read_text(encoding="utf-8")
    sync_search_corpus.sync(tmp_path, check=True)
    assert (tmp_path / sync_search_corpus.JS_REL).read_text(encoding="utf-8") == before


def test_rejects_backtick_in_text(tmp_path):
    texts = ["正文%d" % i for i in range(100)]
    texts[0] = "含`反引号"
    _mk_root(tmp_path, texts)
    with pytest.raises(SystemExit):
        sync_search_corpus.sync(tmp_path)


def test_bracket_in_text_does_not_break_span(tmp_path):
    texts = ["含]方括号" + str(i) for i in range(100)]
    _mk_root(tmp_path, texts)
    assert sync_search_corpus.sync(tmp_path)[0] is True
    out = (tmp_path / sync_search_corpus.JS_REL).read_text(encoding="utf-8")
    assert "text: `含]方括号0`" in out
    assert 'characters: ["孙悟空"]' in out


def test_real_tree_no_drift():
    changed, summary = sync_search_corpus.sync(sync_search_corpus.ROOT, check=True)
    assert changed is False, "真实仓树内嵌语料与 dataset/text-search.json 漂移（%s）" % summary
