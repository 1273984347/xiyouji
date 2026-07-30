"""aliases.py 测试：35 人物别名表 + resolve_alias 别名解析。

aliases.py 仅依赖内置类型（无外部依赖），测试可独立运行。
"""
from utils.aliases import CHARACTER_ALIASES, resolve_alias


def test_aliases_count():
    """别名表应包含 35 位主要人物（与 character_nlp.py CHARACTERS 一致）。"""
    assert len(CHARACTER_ALIASES) == 35


def test_aliases_structure():
    """每位人物的别名列表非空，且主名自身在别名列表中。"""
    for canonical, aliases in CHARACTER_ALIASES.items():
        assert isinstance(aliases, list)
        assert len(aliases) > 0, f"{canonical} 别名列表为空"
        assert canonical in aliases, f"{canonical} 主名应在其别名列表中"


def test_resolve_alias_known():
    """已知别名应正确解析为主名。"""
    assert resolve_alias("行者") == "孙悟空"
    assert resolve_alias("齐天大圣") == "孙悟空"
    assert resolve_alias("猴王") == "孙悟空"
    assert resolve_alias("三藏") == "唐僧"
    assert resolve_alias("玄奘") == "唐僧"
    assert resolve_alias("八戒") == "猪八戒"
    assert resolve_alias("呆子") == "猪八戒"
    assert resolve_alias("菩萨") == "观音"
    assert resolve_alias("佛祖") == "如来"
    assert resolve_alias("灵感大王") == "金鱼精"


def test_resolve_alias_canonical_self():
    """主名自身应解析为自身。"""
    assert resolve_alias("孙悟空") == "孙悟空"
    assert resolve_alias("唐僧") == "唐僧"
    assert resolve_alias("白骨精") == "白骨精"


def test_resolve_alias_unknown():
    """未知别名应原样返回，不抛异常（容错设计）。"""
    assert resolve_alias("未知人物") == "未知人物"
    assert resolve_alias("") == ""
    assert resolve_alias("路人甲") == "路人甲"
    assert resolve_alias("白骨") == "白骨"  # "白骨" 不是别名（"白骨精"/"白骨夫人" 才是）


def test_resolve_alias_idempotent():
    """resolve_alias 二次调用应返回相同结果（反向索引懒构建后稳定）。"""
    once = resolve_alias("行者")
    twice = resolve_alias("行者")
    assert once == twice == "孙悟空"
