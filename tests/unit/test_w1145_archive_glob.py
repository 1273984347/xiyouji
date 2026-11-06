"""W1145：第 31 门禁归档登记面须覆盖 W995 拆分出的 tier2 分册（C4 误红根修锁）。

锁两条：分册在读取面内；分册内的历史版段（W492）可被 C4 登记集合识别。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_doc_sync as c  # noqa: E402


def test_archive_glob_covers_tier2_volume():
    names = [Path(p).name for p in c.ARCHIVE_CHANGELOGS]
    assert "CHANGELOG-ARCHIVE-tier2-W400-W559.md" in names


def test_w492_section_is_recognized():
    volume = ROOT / "archive" / "docs" / "CHANGELOG-ARCHIVE-tier2-W400-W559.md"
    sections = c.changelog_section_ws(volume.read_text(encoding="utf-8"))
    assert "492" in sections
