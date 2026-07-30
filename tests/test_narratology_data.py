"""narratology-13d-network.html 数据契约单元测试（P0）。

依据 docs/10-方法论沉淀/可视化测试计划-十七维叙事学图谱.md 的 Coverage Map。
从 HTML 内嵌的 EMBEDDED_DATA 抽取数据，纯 Python 断言，不依赖浏览器。

覆盖范围：
- 顶层 7 个 key 完备性
- dimensions 字段完备性 + 类型 + 值域 + W### 范围
- dimensions.id 唯一性 + 日期戳一致性
- 七感/文本/新增四维完整性
- externalNodes 字段与数量
- links 引用完整性 + 类型枚举 + 强度值域
- sankey 三层结构（维度→理论家→应用案例）
- theorists id 唯一性 + 字段完备性
- timeline 里程碑 + 日期戳一致性
- KPI 一致性（28 边/7 类别/4 新增维度）
- 编辑差异文档化（17 维度/64 理论家为概念口径）
"""
import json
import re
from pathlib import Path

import pytest

HTML_PATH = Path(__file__).resolve().parent.parent / "site" / "data" / "narratology-13d-network.html"


def _extract_embedded_data(html_text: str) -> dict:
    """从 HTML 抽取 EMBEDDED_DATA = {...}; 块并解析为 dict。

    EMBEDDED_DATA 是 JS 对象字面量（含 // 注释 + unquoted keys），需清洗为合法 JSON。
    转换步骤：
    1. 抽取 EMBEDDED_DATA = {...}; 块
    2. 剥离 // 行注释（数据内无 // 字符串值，安全）
    3. 将 [{,] 后的裸标识符 key 加双引号
    """
    m = re.search(r'const EMBEDDED_DATA\s*=\s*(\{.*?\n\});', html_text, re.DOTALL)
    assert m, "未找到 EMBEDDED_DATA 块"
    block = m.group(1)
    # 剥离 // 行注释（从 // 到行尾）
    block = re.sub(r'//[^\n]*', '', block)
    # 将 [{,]\s* 后的裸标识符（含中文）key 加双引号
    block = re.sub(
        r'([{,]\s*)([A-Za-z\u4e00-\u9fff_][A-Za-z0-9\u4e00-\u9fff_]*)(\s*:)',
        r'\1"\2"\3',
        block,
    )
    return json.loads(block)


@pytest.fixture(scope="module")
def embedded_data():
    """加载 HTML 内嵌的 EMBEDDED_DATA。"""
    assert HTML_PATH.exists(), f"HTML 文件不存在：{HTML_PATH}"
    html_text = HTML_PATH.read_text(encoding="utf-8")
    return _extract_embedded_data(html_text)


@pytest.fixture(scope="module")
def narratology(embedded_data):
    """narratology 子对象。"""
    return embedded_data["narratology"]


# ===== 顶层 key 完备性 =====

def test_top_level_keys(narratology):
    """EMBEDDED_DATA.narratology 应含 7 个顶层 key。"""
    expected = {
        "dimensions", "externalNodes", "links", "sankey",
        "sankeyTheoristColors", "theorists", "timeline",
    }
    assert set(narratology.keys()) == expected


# ===== dimensions 数据契约 =====

def test_dimensions_count(narratology):
    """dimensions 数组应有 16 条（W161-W185，W191 网络叙事学独立专题未入数组）。"""
    assert len(narratology["dimensions"]) == 16


def test_dimensions_ids_unique(narratology):
    """dimensions.id 应唯一。"""
    ids = [d["id"] for d in narratology["dimensions"]]
    assert len(ids) == len(set(ids))


def test_dimensions_fields_complete(narratology):
    """每条 dimension 应含 15 个必填字段。"""
    required = {
        "id", "code", "维度", "name", "english", "category", "theorists",
        "术语数", "案例", "理论深度", "西游应用", "学术影响", "color", "日期", "日期戳",
    }
    for d in narratology["dimensions"]:
        assert set(d.keys()) == required, f"{d.get('id')} 字段不完整: {set(d.keys()) ^ required}"


def test_dimensions_metric_ranges(narratology):
    """术语数/理论深度/西游应用/学术影响 应在 1-10 区间。"""
    metrics = ["术语数", "理论深度", "西游应用", "学术影响"]
    for d in narratology["dimensions"]:
        for m in metrics:
            v = d[m]
            assert isinstance(v, int), f"{d['id']}.{m} 应为 int，实际 {type(v).__name__}"
            assert 1 <= v <= 10, f"{d['id']}.{m}={v} 超出 1-10"


def test_dimensions_categories(narratology):
    """dimensions[*].category 应为七类之一。"""
    valid = {
        "七感叙事学", "文本叙事学", "性别叙事学", "文化叙事学",
        "情感叙事学", "历史叙事学", "元叙事学",
    }
    for d in narratology["dimensions"]:
        assert d["category"] in valid, f"{d['id']}.category={d['category']} 不在七类中"


def test_dimensions_theorists_nonempty(narratology):
    """dimensions[*].theorists 应为非空数组。"""
    for d in narratology["dimensions"]:
        assert isinstance(d["theorists"], list), f"{d['id']}.theorists 应为 list"
        assert len(d["theorists"]) > 0, f"{d['id']}.theorists 为空"


def test_dimensions_w_range(narratology):
    """dimensions[*].id 应在 W161-W185 范围内。"""
    for d in narratology["dimensions"]:
        num = int(d["id"][1:])
        assert 161 <= num <= 185, f"{d['id']} 超出 W161-W185 范围"


def test_dimensions_date_stamp_consistency(narratology):
    """dimensions[*].日期戳 应与 日期 字符串一致。"""
    for d in narratology["dimensions"]:
        date_str = d["日期"].replace("-", "")
        assert int(date_str) == d["日期戳"], (
            f"{d['id']}: 日期={date_str} 日期戳={d['日期戳']} 不一致"
        )


def test_dimensions_color_format(narratology):
    """dimensions[*].color 应为 #RRGGBB 格式。"""
    hex_re = re.compile(r'^#[0-9A-Fa-f]{6}$')
    for d in narratology["dimensions"]:
        assert hex_re.match(d["color"]), f"{d['id']}.color={d['color']} 非 #RRGGBB 格式"


# ===== 七感/文本/新增四维完整性 =====

def test_seven_senses_complete(narratology):
    """七感叙事学应齐全：时/空/听/嗅/触/视/味。"""
    seven = {"时", "空", "听", "嗅", "触", "视", "味"}
    actual = {d["维度"] for d in narratology["dimensions"] if d["category"] == "七感叙事学"}
    assert actual == seven


def test_text_narratology_complete(narratology):
    """文本叙事学应齐全：文/修/知。"""
    text = {"文", "修", "知"}
    actual = {d["维度"] for d in narratology["dimensions"] if d["category"] == "文本叙事学"}
    assert actual == text


def test_new_four_dims_complete(narratology):
    """W182-W185 新增四维应齐全：情感/历史/元叙事/不可靠。"""
    new = {"情感", "历史", "元叙事", "不可靠"}
    actual = {d["维度"] for d in narratology["dimensions"] if d["id"] in {"W182", "W183", "W184", "W185"}}
    assert actual == new


# ===== externalNodes 数据契约 =====

def test_external_nodes_count(narratology):
    """externalNodes 应有 6 条。"""
    assert len(narratology["externalNodes"]) == 6


def test_external_nodes_fields(narratology):
    """externalNodes 字段完备性。"""
    required = {"id", "维度", "name", "category", "color"}
    for n in narratology["externalNodes"]:
        assert set(n.keys()) == required


def test_external_nodes_ids_unique(narratology):
    """externalNodes.id 应唯一。"""
    ids = [n["id"] for n in narratology["externalNodes"]]
    assert len(ids) == len(set(ids))


# ===== links 数据契约 =====

def test_links_count(narratology):
    """links 应有 28 条（与 KPI 一致）。"""
    assert len(narratology["links"]) == 28


def test_links_referential_integrity(narratology):
    """links[*].source/target 应在 dimensions.id ∪ externalNodes.id 中。"""
    valid_ids = (
        {d["id"] for d in narratology["dimensions"]}
        | {n["id"] for n in narratology["externalNodes"]}
    )
    for link in narratology["links"]:
        assert link["source"] in valid_ids, f"link source={link['source']} 不存在"
        assert link["target"] in valid_ids, f"link target={link['target']} 不存在"


def test_links_type_enum(narratology):
    """links[*].type 应为三种之一。"""
    valid = {"时空感官", "理论文本", "扩展跨域"}
    for link in narratology["links"]:
        assert link["type"] in valid, f"link type={link['type']} 不在枚举中"


def test_links_strength_range(narratology):
    """links[*].强度 应在 1-100。"""
    for link in narratology["links"]:
        assert 1 <= link["强度"] <= 100, f"link 强度={link['强度']} 超出 1-100"


# ===== sankey 数据契约 =====

def test_sankey_count(narratology):
    """sankey 应有 32 条（16 维度→理论家 + 16 理论家→应用案例）。"""
    assert len(narratology["sankey"]) == 32


def test_sankey_three_layer(narratology):
    """sankey 应为三层结构：前 16 条 维度名→理论家，后 16 条 理论家→应用案例。"""
    dim_names = {d["维度"] for d in narratology["dimensions"]}
    theorist_names = {t["name"] for t in narratology["theorists"]}
    # 注意：sankey 中理论家名可能用简称（如"德罗布尼克" vs theorists.name "吉姆·德罗布尼克"）
    # 因此检查 sankey 前段 source 必为维度名，后段 source 必出现在 sankeyTheoristColors 的 key 中
    color_keys = set(narratology["sankeyTheoristColors"].keys())

    for link in narratology["sankey"][:16]:
        assert link["source"] in dim_names, (
            f"sankey 前段 source={link['source']} 不是维度名"
        )
        assert link["target"] in color_keys, (
            f"sankey 前段 target={link['target']} 不在 sankeyTheoristColors 中"
        )
    for link in narratology["sankey"][16:]:
        assert link["source"] in color_keys, (
            f"sankey 后段 source={link['source']} 不在 sankeyTheoristColors 中"
        )


# ===== theorists 数据契约 =====

def test_theorists_count(narratology):
    """theorists 应有 16 位。"""
    assert len(narratology["theorists"]) == 16


def test_theorists_ids_unique(narratology):
    """theorists.id 应唯一。"""
    ids = [t["id"] for t in narratology["theorists"]]
    assert len(ids) == len(set(ids))


def test_theorists_fields(narratology):
    """theorists 字段完备性。"""
    required = {
        "id", "name", "英文名", "国籍", "理论", "代表作",
        "活跃年代", "color", "学派", "关联维度",
    }
    for t in narratology["theorists"]:
        assert set(t.keys()) == required


def test_theorists_names_unique(narratology):
    """theorists.name 应唯一。"""
    names = [t["name"] for t in narratology["theorists"]]
    assert len(names) == len(set(names))


# ===== timeline 数据契约 =====

def test_timeline_count(narratology):
    """timeline 应有 20 项（含 W168/W172/W175/W186 可视化里程碑）。"""
    assert len(narratology["timeline"]) == 20


def test_timeline_milestones(narratology):
    """timeline 应含 4 个可视化里程碑。"""
    viz = [t for t in narratology["timeline"] if t["类型"] == "可视化"]
    assert len(viz) == 4
    viz_ids = {t["编号"] for t in viz}
    assert viz_ids == {"W168", "W172", "W175", "W186"}


def test_timeline_date_stamp_consistency(narratology):
    """timeline[*].日期戳 应与 日期 一致。"""
    for t in narratology["timeline"]:
        date_str = t["日期"].replace("-", "")
        assert int(date_str) == t["日期戳"], (
            f"{t['编号']}: 日期={date_str} 日期戳={t['日期戳']} 不一致"
        )


def test_timeline_categories(narratology):
    """timeline[*].类别 应与 dimensions[*].category 体系一致或为'集成'。"""
    valid = {
        "七感叙事学", "文本叙事学", "性别叙事学", "文化叙事学",
        "情感叙事学", "历史叙事学", "元叙事学", "集成",
    }
    for t in narratology["timeline"]:
        assert t["类别"] in valid, f"{t['编号']}.类别={t['类别']} 不在有效集合中"


# ===== sankeyTheoristColors 数据契约 =====

def test_sankey_theorist_colors_count(narratology):
    """sankeyTheoristColors 应覆盖 16 位理论家。"""
    assert len(narratology["sankeyTheoristColors"]) == 16


def test_sankey_theorist_colors_cover_sankey(narratology):
    """sankey 前段 target 必出现在 sankeyTheoristColors 中。"""
    color_keys = set(narratology["sankeyTheoristColors"].keys())
    sankey_theorist_targets = {link["target"] for link in narratology["sankey"][:16]}
    for t_name in sankey_theorist_targets:
        assert t_name in color_keys, f"sankey 理论家 {t_name} 缺少配色"


# ===== KPI 一致性 =====

def test_kpi_links_consistency(narratology):
    """KPI '28 关联边' 应与 links 数组长度一致。"""
    assert len(narratology["links"]) == 28


def test_kpi_categories_consistency(narratology):
    """KPI '7 维度类别' 应与 dimensions[*].category 去重数一致。"""
    cats = {d["category"] for d in narratology["dimensions"]}
    assert len(cats) == 7


def test_kpi_new_dims_consistency(narratology):
    """KPI '4 新增维度' 应与 W182-W185 数量一致。"""
    new = [d for d in narratology["dimensions"] if d["id"] in {"W182", "W183", "W184", "W185"}]
    assert len(new) == 4


def test_kpi_17_dimensions_documented():
    """KPI '17 叙事学维度' 为概念口径（16 数据维度 + W191 网络叙事学专题）。

    编辑决策文档化：W191 在 docs/03-主题与情节专题/取经网络叙事学专题.md 中独立展开，
    未加入 EMBEDDED_DATA.dimensions 数组。此测试不实际断言 17，仅文档化差异。
    若未来将 W191 纳入 dimensions 数组，需更新此测试与 dimensions_count 期望值。
    """
    # 此测试为文档化目的，不做实际断言
    # 详见 docs/10-方法论沉淀/可视化测试计划-十七维叙事学图谱.md "已知问题" 段
