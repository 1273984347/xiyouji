"""character_nlp.py 核心测试：别名解析、引语归属、共现、统计。

character_nlp.py 位于 scripts/B_人物/ 目录下，目录名含非 ASCII 字符，
故采用 importlib 按文件路径加载模块，避免命名空间包导入的潜在问题。
"""
import importlib.util
from pathlib import Path

import pytest

# ---- 通过文件路径加载 character_nlp 模块 ----
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
_SPEC = importlib.util.spec_from_file_location(
    "character_nlp", _SCRIPTS_DIR / "B_人物" / "character_nlp.py"
)
character_nlp = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(character_nlp)

# 导出被测对象
CHARACTERS = character_nlp.CHARACTERS
build_alias_regex = character_nlp.build_alias_regex
find_characters_in_text = character_nlp.find_characters_in_text
find_dialogues_in_text = character_nlp.find_dialogues_in_text
build_cooccurrence = character_nlp.build_cooccurrence
build_character_stats = character_nlp.build_character_stats
build_dialogue_attribution = character_nlp.build_dialogue_attribution


@pytest.fixture(scope="module")
def alias_patterns():
    """预构建别名正则，供多数测试复用。"""
    return build_alias_regex(CHARACTERS)


# ====================================================================
# 1. 别名解析
# ====================================================================

def test_alias_resolution(alias_patterns):
    """别名→主名解析：'行者'→孙悟空、'八戒'→猪八戒、'猴王'→孙悟空。"""
    text = "行者与八戒同行，猴王大笑。"
    occ = find_characters_in_text(text, alias_patterns)
    # alias_used -> canonical 映射
    alias_to_canonical = {a: c for c, _, _, a in occ}
    assert alias_to_canonical.get("行者") == "孙悟空"
    assert alias_to_canonical.get("八戒") == "猪八戒"
    assert alias_to_canonical.get("猴王") == "孙悟空"
    # canonicals 集合应包含两位人物
    canonicals = {c for c, _, _, _ in occ}
    assert {"孙悟空", "猪八戒"}.issubset(canonicals)


def test_alias_resolution_all_canonicals_present():
    """CHARACTERS 表应包含 35 位人物（与 aliases.py 单一数据源一致）。"""
    assert len(CHARACTERS) == 35
    # 每位人物的别名列表非空且包含主名自身
    for canonical, aliases in CHARACTERS.items():
        assert len(aliases) > 0
        assert canonical in aliases


# ====================================================================
# 2. 引语归属
# ====================================================================

def test_quote_attribution_basic(alias_patterns):
    """标准引语模式：XXX道："..." 应正确归属 speaker 与 quote。"""
    text = "孙悟空道：\u201c俺老孙去也！\u201d"
    dialogues = find_dialogues_in_text(text, alias_patterns, CHARACTERS)
    assert len(dialogues) == 1
    d = dialogues[0]
    assert d["speaker"] == "孙悟空"
    assert d["alias_used"] == "孙悟空"
    assert d["quote"] == "俺老孙去也！"
    assert "道" in d["pattern"]
    assert d["quote_length"] == len("俺老孙去也！")


def test_quote_attribution_with_middle(alias_patterns):
    """标准引语 + middle 副词：'八戒笑道' 应归属猪八戒。"""
    text = "八戒笑道：\u201c师父，我饿了。\u201d"
    dialogues = find_dialogues_in_text(text, alias_patterns, CHARACTERS)
    assert len(dialogues) == 1
    d = dialogues[0]
    assert d["speaker"] == "猪八戒"
    assert d["alias_used"] == "八戒"
    assert "笑" in d["pattern"]
    assert "道" in d["pattern"]


def test_quote_attribution_inverted(alias_patterns):
    """倒装引语模式："..."XXX道 应归属正确 speaker（与标准模式去重）。"""
    text = "\u201c大师兄，等等我！\u201d猪八戒喊道。"
    dialogues = find_dialogues_in_text(text, alias_patterns, CHARACTERS)
    # 应至少识别到一条倒装引语
    inverted = [d for d in dialogues if "倒装" in d["pattern"]]
    assert len(inverted) >= 1
    d = inverted[0]
    assert d["speaker"] == "猪八戒"
    assert "等等我" in d["quote"]
    # 不应同时存在标准模式重复匹配同一引语
    assert len(dialogues) == len(inverted)


def test_sample_text_dialogues(alias_patterns, sample_text):
    """sample_text fixture 应同时识别标准与倒装引语，speaker 含孙悟空/猪八戒。"""
    dialogues = find_dialogues_in_text(sample_text, alias_patterns, CHARACTERS)
    speakers = {d["speaker"] for d in dialogues}
    assert "孙悟空" in speakers
    assert "猪八戒" in speakers
    assert len(dialogues) >= 2


# ====================================================================
# 3. 共现网络
# ====================================================================

def test_cooccurrence_basic(alias_patterns, sample_chapters):
    """同回共现：第 2 回孙悟空+猪八戒+沙僧 应产生共现边。"""
    co = build_cooccurrence(
        sample_chapters, CHARACTERS, alias_patterns, mode="chapter"
    )
    pairs = {(e["source"], e["target"]) for e in co["edges"]}
    # 边按 sorted pair 存储：孙(\u5b59) < 沙(\u6c99) < 猪(\u732a)
    assert ("孙悟空", "猪八戒") in pairs
    assert ("孙悟空", "沙僧") in pairs
    # node_counts 应统计人物出场回数
    node_names = {n["id"] for n in co["nodes"]}
    assert {"孙悟空", "猪八戒", "沙僧"}.issubset(node_names)


def test_cooccurrence_empty(alias_patterns):
    """空 chapters 列表应返回空共现网络，不崩溃。"""
    co = build_cooccurrence([], CHARACTERS, alias_patterns, mode="chapter")
    assert co["nodes"] == []
    assert co["edges"] == []


# ====================================================================
# 4. 人物统计
# ====================================================================

def test_character_count(alias_patterns, sample_chapters):
    """人物出场计数：appear_chapters / first_appear / total_mentions 正确。"""
    stats = build_character_stats(sample_chapters, CHARACTERS, alias_patterns)
    by_name = {c["name"]: c for c in stats["characters"]}
    assert by_name["孙悟空"]["appear_chapters"] == 2
    assert by_name["孙悟空"]["first_appear"] == 1
    assert by_name["孙悟空"]["total_mentions"] >= 3  # 猴王+孙悟空+行者+孙悟空
    assert by_name["猪八戒"]["appear_chapters"] == 1
    assert by_name["猪八戒"]["first_appear"] == 2
    assert by_name["沙僧"]["appear_chapters"] == 1
    assert stats["total_chapters"] == 2


def test_chapter_range(alias_patterns):
    """回目范围：first_appear 与 appear_in_chapters 应正确反映出场回目序列。"""
    chapters = [
        (5, "第五回", "唐僧出现。"),
        (10, "第十回", "唐僧又出现。沙僧也在。"),
        (15, "第十五回", "路人甲走过，无人物。"),
    ]
    stats = build_character_stats(chapters, CHARACTERS, alias_patterns)
    by_name = {c["name"]: c for c in stats["characters"]}
    assert by_name["唐僧"]["first_appear"] == 5
    assert by_name["唐僧"]["appear_in_chapters"] == [5, 10]
    assert by_name["沙僧"]["first_appear"] == 10
    assert by_name["沙僧"]["appear_in_chapters"] == [10]


# ====================================================================
# 5. 健壮性
# ====================================================================

def test_empty_text(alias_patterns):
    """空文本不应导致任何函数崩溃。"""
    assert find_characters_in_text("", alias_patterns) == []
    assert find_dialogues_in_text("", alias_patterns, CHARACTERS) == []
    stats = build_character_stats([], CHARACTERS, alias_patterns)
    assert stats["character_count"] == 0
    assert stats["characters"] == []


def test_unknown_character(alias_patterns):
    """未知人物不应被识别；已知妖怪别名应正确归属。"""
    # 白骨夫人是白骨精的别名，应识别为白骨精
    occ = find_characters_in_text("白骨夫人是妖怪。", alias_patterns)
    canonicals = {c for c, _, _, _ in occ}
    assert "白骨精" in canonicals
    # 真正未知的人物不应出现
    occ2 = find_characters_in_text("路人甲与路人乙走过。", alias_patterns)
    assert occ2 == []


def test_sanzang_exclusion_rule(alias_patterns):
    """上下文排除规则（W101/W102）：'三藏真经' 中的 '三藏' 不应识别为唐僧。

    参考 character_nlp.py find_characters_in_text docstring：
      - 规则 1：alias=='三藏' 且后接 '真经' 跳过
      - 规则 2：alias=='三藏' 且后接 '共计' 跳过
    """
    text = "如来造了三藏真经，三藏共计三十五部。"
    occ = find_characters_in_text(text, alias_patterns)
    canonicals = {c for c, _, _, _ in occ}
    # "如来" 应被识别
    assert "如来" in canonicals
    # "三藏" 在 "三藏真经" 与 "三藏共计" 中均应被排除，不识别为唐僧
    assert "唐僧" not in canonicals


def test_dialogue_attribution_chapter_tag(alias_patterns, sample_chapters):
    """build_dialogue_attribution 应为每条引语附加 chapter/chapter_title。"""
    result = build_dialogue_attribution(
        sample_chapters, CHARACTERS, alias_patterns
    )
    assert result["total_dialogues"] == len(result["dialogues"])
    for d in result["dialogues"]:
        assert "chapter" in d
        assert "chapter_title" in d
        assert d["chapter"] in (1, 2)
    # speaker_ranking 应按发言条数降序
    counts = [s["count"] for s in result["speaker_ranking"]]
    assert counts == sorted(counts, reverse=True)
