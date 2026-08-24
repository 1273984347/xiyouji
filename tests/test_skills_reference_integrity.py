"""check_skills_index.py 第 5 检查单元测试：skill 正文引用资产存在性（W515 新增）

背景（W509-X4 教训）：xiyouji-day-review 两处引用 scripts/_shot_check.js，
文件本体已删除，check_skills_index 只查索引一致性不查正文引用路径，
失效指针静默存活多批。

覆盖三个核心函数：
- collect_script_refs：从 Markdown 提取 scripts/*.py|js 引用（含 .json 边界回归）
- find_missing_refs：对引用清单做磁盘存在性断言（含允许清单豁免）
- DEFAULT_ALLOWED_MISSING：文档示意命令占位名冻结基线

工具来源：scripts/check_skills_index.py
"""
from pathlib import Path

import pytest

from check_skills_index import (
    DEFAULT_ALLOWED_MISSING,
    collect_script_refs,
    find_missing_refs,
)


# ---------------- collect_script_refs ----------------

class TestCollectScriptRefs:
    def test_extracts_simple_ref(self):
        """反引号内的 scripts/py|js 引用应被完整提取。"""
        text = "运行 `python scripts/check_skills_index.py` 核查"
        assert collect_script_refs(text) == {"scripts/check_skills_index.py"}

    def test_multiple_refs_dedup(self):
        """同一引用多次出现应去重；不同引用各自保留。"""
        text = "`scripts/a.py` 与 scripts/b.js，再次提到 scripts/a.py"
        assert collect_script_refs(text) == {"scripts/a.py", "scripts/b.js"}

    def test_json_suffix_not_misextracted(self):
        """.json 结尾的引用不得被切成 .js（W515 取证实测回归：
        perf-budget.json 曾被无边界正则误提为 perf-budget.js）。"""
        text = "`cat scripts/output/perf-budget.json` 与 scripts/output/perf-baseline.json"
        assert collect_script_refs(text) == set()

    def test_subdirectory_and_archive_refs(self):
        """子目录引用（archive/、audit/）同样提取。"""
        text = "`scripts/archive/w334_font_subset.py`、scripts/audit/line_check.py"
        assert collect_script_refs(text) == {
            "scripts/archive/w334_font_subset.py",
            "scripts/audit/line_check.py",
        }


# ---------------- find_missing_refs ----------------

@pytest.fixture
def skill_tree(tmp_path: Path) -> Path:
    """构造最小 skills 树：一个 skill 目录 + 一个引用不存在脚本的 md。"""
    d = tmp_path / "skills" / "demo-skill"
    d.mkdir(parents=True)
    return tmp_path


class TestFindMissingRefs:
    def test_reports_absent_ref(self, skill_tree: Path):
        md = skill_tree / "skills" / "demo-skill" / "SKILL.md"
        md.write_text("用 `scripts/_gone_tool.js` 抽查\n", encoding="utf-8")
        mds = sorted((skill_tree / "skills").rglob("*.md"))
        missing = find_missing_refs(mds, skill_tree)
        assert missing == [("skills/demo-skill/SKILL.md", "scripts/_gone_tool.js")]

    def test_silent_when_file_exists(self, skill_tree: Path):
        md = skill_tree / "skills" / "demo-skill" / "SKILL.md"
        md.write_text("用 `scripts/tool.py` 抽查\n", encoding="utf-8")
        real = skill_tree / "scripts"
        real.mkdir()
        (real / "tool.py").write_text("# ok\n", encoding="utf-8")
        mds = sorted((skill_tree / "skills").rglob("*.md"))
        assert find_missing_refs(mds, skill_tree) == []

    def test_allowlist_exempts_placeholder(self, skill_tree: Path):
        """允许清单内路径即使磁盘不存在也不报（文档示意命令占位名）。"""
        md = skill_tree / "skills" / "demo-skill" / "SKILL.md"
        md.write_text("示例：`ls scripts/脚本A.py`\n", encoding="utf-8")
        mds = sorted((skill_tree / "skills").rglob("*.md"))
        assert find_missing_refs(
            mds, skill_tree, allowed=frozenset({"scripts/脚本A.py"})
        ) == []

    def test_default_allowlist_covers_known_placeholders(self):
        """冻结基线必须恰好覆盖三个已知占位名，不多不少。"""
        assert DEFAULT_ALLOWED_MISSING == frozenset({
            "scripts/xx.py",
            "scripts/脚本A.py",
            "scripts/脚本B.py",
        })


# ---------------- 真实仓库冒烟 ----------------

class TestRealRepo:
    def test_no_unexpected_missing_refs_in_skills(self):
        """真实仓库冒烟：skills/ 全部 md 扫描后，除允许清单外不允许任何缺失。

        W515 落地前该测试因 xiyouji-day-review 的 _shot_check.js 失效指针而红；
        指针修复后转绿，并长期防同类腐化。
        """
        root = Path(__file__).resolve().parent.parent
        mds = sorted((root / "skills").rglob("*.md"))
        assert find_missing_refs(mds, root) == []
