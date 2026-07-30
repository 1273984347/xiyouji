r"""
aliases.py — 《西游记》人物别名表（单一数据源）

用途：
    集中管理 35 位主要人物的别名映射，供分析脚本统一引用。
    消除 character_nlp.py / character_appearance.py / character_network.py 中
    各自维护别名表的重复代码。

数据来源：
    d:\1\xiyouji\scripts\B_人物\character_nlp.py 中的 CHARACTERS 字典
    （基于 character_appearance.py + 扩展别名，35 人物别名表）

注意：
    本模块为新建的公共模块，未修改 character_nlp.py 等现有脚本以避免回归。
    未来 character_nlp.py 应改为 `from utils.aliases import CHARACTER_ALIASES`，
    并删除其内部的 CHARACTERS 字典，实现单一数据源。

导出：
    CHARACTER_ALIASES: dict[str, list[str]]  — 主名 -> 别名列表
    resolve_alias(name: str) -> str          — 别名 -> 主名（未知别名原样返回）

用法示例：

    from utils.aliases import CHARACTER_ALIASES, resolve_alias

    # 统计某人物所有别名的总出现次数
    count = sum(text.count(a) for a in CHARACTER_ALIASES["孙悟空"])

    # 别名归一化
    canonical = resolve_alias("行者")  # -> "孙悟空"
"""

from __future__ import annotations


# ====================================================================
# 人物别名表（35 位主要人物）
# 数据源：scripts/B_人物/character_nlp.py 的 CHARACTERS 字典
# ====================================================================
CHARACTER_ALIASES: dict[str, list[str]] = {
    # 取经五众
    "孙悟空": ["孙悟空", "行者", "齐天大圣", "美猴王", "斗战胜佛", "孙行者", "大圣", "猴王", "心猿", "金公"],
    "唐僧": ["唐僧", "玄奘", "三藏", "唐三藏", "旃檀功德佛", "圣僧", "唐长老", "御弟"],
    "猪八戒": ["猪八戒", "八戒", "天蓬元帅", "净坛使者", "呆子", "猪悟能", "木母"],
    "沙僧": ["沙僧", "沙悟净", "卷帘大将", "金身罗汉", "沙和尚", "黄婆"],
    "白龙马": ["白龙马", "敖烈", "八部天龙", "玉龙", "白马"],
    # 主要神佛
    "观音": ["观音", "观世音", "菩萨", "大慈大悲菩萨", "观自在"],
    "如来": ["如来", "释迦牟尼", "佛祖", "如来佛祖", "世尊"],
    "玉帝": ["玉帝", "玉皇大帝", "高天上圣", "玉皇"],
    "太上老君": ["太上老君", "老君", "道德天尊"],
    "菩提祖师": ["菩提祖师", "须菩提", "菩提"],
    # 天庭神将
    "二郎神": ["二郎神", "显圣二郎真君", "真君", "杨戬"],
    "哪吒": ["哪吒", "三太子", "哪吒太子"],
    "李靖": ["李靖", "托塔天王", "托塔李天王", "天王"],
    "王母": ["王母", "王母娘娘", "西王母"],
    "太白金星": ["太白金星", "太白"],
    "弥勒佛": ["弥勒佛", "弥勒"],
    "镇元子": ["镇元子", "镇元大仙"],
    # 主要妖怪
    "牛魔王": ["牛魔王", "平天大圣", "大力王"],
    "铁扇公主": ["铁扇公主", "罗刹女"],
    "红孩儿": ["红孩儿", "善财童子", "圣婴大王"],
    "白骨精": ["白骨精", "白骨夫人"],
    "六耳猕猴": ["六耳猕猴"],
    "黄袍怪": ["黄袍怪", "奎木狼"],
    "金角大王": ["金角大王", "金角"],
    "银角大王": ["银角大王", "银角"],
    "青牛精": ["青牛精", "独角兕", "兕大王"],
    "黄风怪": ["黄风怪", "黄毛貂鼠"],
    "黄眉童子": ["黄眉童子", "黄眉大王"],
    "金鱼精": ["金鱼精", "灵感大王"],
    "蝎子精": ["蝎子精", "琵琶精"],
    "蜘蛛精": ["蜘蛛精"],
    "青毛狮子": ["青毛狮子", "青狮", "狮王"],
    "白象": ["白象", "白象精"],
    "大鹏": ["大鹏", "大鹏金翅雕", "鹏王"],
    "白鹿精": ["白鹿精", "白鹿"],
}


# ====================================================================
# 别名 -> 主名 反向索引（懒构建）
# ====================================================================
_ALIAS_TO_CANONICAL: dict[str, str] | None = None


def _build_reverse_index() -> dict[str, str]:
    """构建 别名 -> 主名 的反向映射。

    若同一别名出现在多个人物的列表中，按 CHARACTER_ALIASES 的迭代顺序
    第一个匹配者胜出（已确认现有数据无冲突）。
    同时将主名自身也加入映射（resolve_alias("孙悟空") -> "孙悟空"）。
    """
    mapping: dict[str, str] = {}
    for canonical, aliases in CHARACTER_ALIASES.items():
        # 主名自身可解析
        if canonical not in mapping:
            mapping[canonical] = canonical
        # 别名指向主名
        for alias in aliases:
            if alias not in mapping:
                mapping[alias] = canonical
    return mapping


def resolve_alias(name: str) -> str:
    """将别名解析为主名。

    参数：
        name: 别名或主名

    返回：
        主名；若 name 不在别名表中，原样返回（不抛异常，便于调用方容错）

    示例：
        >>> resolve_alias("行者")
        '孙悟空'
        >>> resolve_alias("孙悟空")
        '孙悟空'
        >>> resolve_alias("未知人物")
        '未知人物'
    """
    global _ALIAS_TO_CANONICAL
    if _ALIAS_TO_CANONICAL is None:
        _ALIAS_TO_CANONICAL = _build_reverse_index()
    return _ALIAS_TO_CANONICAL.get(name, name)


if __name__ == "__main__":
    # 自检：打印别名表规模与样例
    print(f"CHARACTER_ALIASES: {len(CHARACTER_ALIASES)} 个人物")
    total_aliases = sum(len(v) for v in CHARACTER_ALIASES.values())
    print(f"别名总数：{total_aliases}")
    print(f"resolve_alias('行者') = {resolve_alias('行者')!r}")
    print(f"resolve_alias('三藏') = {resolve_alias('三藏')!r}")
    print(f"resolve_alias('未知') = {resolve_alias('未知')!r}")
