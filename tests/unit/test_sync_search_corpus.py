"""W1316 建/W1317 扩·站内搜索语料生成器（sync_search_corpus）单元测试。

W1317（容量 #4）：内嵌形态改为 gzip(JSON)+base64 单串（`EMBEDDED_CORPUS_GZ_B64`），
本文件同步覆盖压缩载荷的生成/对拍语义。

覆盖：
  - 生成幂等：apply → check 零差异
  - 载荷往返：解码 == 权威 JSON 投影（num/title/fullTitle/text·键序固定）
  - 替换边界：载荷行重建 + 头注释更新，characters/artifacts 等其余键保留
  - 反引号 / ${ 等旧模板字面量危险序列不再构成限制（JSON+base64 管道天然安全）
  - fail-closed：章节数不为 100 → SystemExit（不写盘）
  - 载荷损坏 → check 判差异（并可由 sync 修复）
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
        '    const EMBEDDED_CORPUS_GZ_B64 = "";\n'
        "    const EMBEDDED_DATA = {\n"
        "        chapters: [],\n"
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


def _expected(texts):
    return [{"num": i + 1, "title": "题%d" % (i + 1),
             "fullTitle": "第%d回 题%d" % (i + 1, i + 1), "text": texts[i]}
            for i in range(100)]


def test_sync_applies_and_is_idempotent(tmp_path):
    texts = ["正文%d" % i for i in range(100)]
    _mk_root(tmp_path, texts)
    assert sync_search_corpus.sync(tmp_path, check=True)[0] is True, "初始载荷为空（待同步）"
    assert sync_search_corpus.sync(tmp_path)[0] is True
    out = (tmp_path / sync_search_corpus.JS_REL).read_text(encoding="utf-8")
    assert "old header" not in out
    assert 'characters: ["孙悟空"]' in out, "载荷块之外的键不得被替换"
    assert sync_search_corpus.decode_payload(out) == _expected(texts), "载荷往返须与权威 JSON 投影一致"
    assert sync_search_corpus.sync(tmp_path, check=True)[0] is False, "重建后应幂等（零差异）"


def test_check_mode_does_not_write(tmp_path):
    _mk_root(tmp_path, ["正文%d" % i for i in range(100)])
    before = (tmp_path / sync_search_corpus.JS_REL).read_text(encoding="utf-8")
    sync_search_corpus.sync(tmp_path, check=True)
    assert (tmp_path / sync_search_corpus.JS_REL).read_text(encoding="utf-8") == before


def test_dangerous_sequences_are_now_safe(tmp_path):
    """反引号 / ${ / 多行正文在 JSON+base64 管道下全部可安全往返（旧模板字面量限制解除）。"""
    texts = ["正文%d" % i for i in range(100)]
    texts[0] = "含`反引号与${模板}序列\n第二行"
    _mk_root(tmp_path, texts)
    assert sync_search_corpus.sync(tmp_path)[0] is True
    out = (tmp_path / sync_search_corpus.JS_REL).read_text(encoding="utf-8")
    assert sync_search_corpus.decode_payload(out)[0]["text"] == texts[0]


def test_rejects_wrong_chapter_count(tmp_path):
    _mk_root(tmp_path, ["正文%d" % i for i in range(100)])
    p = tmp_path / sync_search_corpus.JSON_REL
    data = json.loads(p.read_text(encoding="utf-8"))
    data["chapters"] = data["chapters"][:99]
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(SystemExit):
        sync_search_corpus.sync(tmp_path)


def test_corrupt_payload_detected_and_repairable(tmp_path):
    texts = ["正文%d" % i for i in range(100)]
    _mk_root(tmp_path, texts)
    sync_search_corpus.sync(tmp_path)
    js_path = tmp_path / sync_search_corpus.JS_REL
    broken = js_path.read_text(encoding="utf-8").replace(
        'const EMBEDDED_CORPUS_GZ_B64 = "', 'const EMBEDDED_CORPUS_GZ_B64 = "!!!', 1)
    js_path.write_text(broken, encoding="utf-8")
    assert sync_search_corpus.decode_payload(broken) == []
    assert sync_search_corpus.sync(tmp_path, check=True)[0] is True, "损坏载荷必须判差异（fail-closed）"
    assert sync_search_corpus.sync(tmp_path)[0] is True
    assert sync_search_corpus.sync(tmp_path, check=True)[0] is False


def test_real_tree_no_drift():
    changed, summary = sync_search_corpus.sync(sync_search_corpus.ROOT, check=True)
    assert changed is False, "真实仓树内嵌语料与 dataset/text-search.json 漂移（%s）" % summary
