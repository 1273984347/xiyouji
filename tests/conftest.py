"""pytest 全局配置：sys.path 设置 + 公共 fixtures。

将 scripts/ 加入 sys.path，使 `utils` 包与 `B_人物` 命名空间包可被 import。
"""
import sys
from pathlib import Path

# 将 scripts/ 加入 sys.path（character_nlp.py 内部 `from utils.text_loader import ...` 依赖此设置）
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


import pytest


@pytest.fixture
def sample_text():
    """含人物名 + 标准引语 + 倒装引语的测试文本。

    使用 \u201c / \u201d（中文左右双引号）匹配 character_nlp.py 的引语正则。
    """
    return (
        "第一回 灵根育孕源流出。\n"
        "那猴王在山中游玩，忽见行者走来。\n"
        "孙悟空道：\u201c俺老孙去也！\u201d\n"
        "八戒笑道：\u201c师父，我饿了。\u201d\n"
        "\u201c大师兄，等等我！\u201d猪八戒喊道。\n"
    )


@pytest.fixture
def sample_chapters():
    """两回测试文本：[(num, title, text), ...]。

    - 第 1 回：仅孙悟空（猴王/孙悟空别名）
    - 第 2 回：孙悟空 + 猪八戒 + 沙僧（用于共现与统计测试）
    """
    return [
        (1, "第一回 灵根育孕源流出", "那猴王孙悟空在花果山游玩。"),
        (2, "第二回 悟彻菩提真妙理", "行者孙悟空与八戒同行。沙僧挑担。"),
    ]
