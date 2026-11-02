import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import agent_start  # noqa: E402


def test_stats_missing_is_reported(tmp_path):
    stats_path = tmp_path / 'stats.json'
    cl = tmp_path / 'CHANGELOG.md'
    cl.write_text('x', encoding='utf-8')
    stats, warns = agent_start.load_stats_with_warnings(str(stats_path), str(cl))
    assert stats == {}
    assert len(warns) == 1
    assert '缺失' in warns[0]


def test_stats_corrupt_is_reported(tmp_path):
    stats_path = tmp_path / 'stats.json'
    stats_path.write_text('{not json', encoding='utf-8')
    cl = tmp_path / 'CHANGELOG.md'
    cl.write_text('x', encoding='utf-8')
    stats, warns = agent_start.load_stats_with_warnings(str(stats_path), str(cl))
    assert stats == {}
    assert warns and '损坏' in warns[0]


def test_stats_empty_object_is_reported(tmp_path):
    stats_path = tmp_path / 'stats.json'
    stats_path.write_text('{}', encoding='utf-8')
    cl = tmp_path / 'CHANGELOG.md'
    cl.write_text('x', encoding='utf-8')
    stats, warns = agent_start.load_stats_with_warnings(str(stats_path), str(cl))
    assert warns and ('空' in warns[0] or '非对象' in warns[0])


def test_stats_stale_is_reported(tmp_path):
    stats_path = tmp_path / 'stats.json'
    stats_path.write_text(json.dumps({'html_total': 1}), encoding='utf-8')
    cl = tmp_path / 'CHANGELOG.md'
    cl.write_text('x', encoding='utf-8')
    os.utime(stats_path, (1000, 1000))
    os.utime(cl, (2000, 2000))
    stats, warns = agent_start.load_stats_with_warnings(str(stats_path), str(cl))
    assert stats == {'html_total': 1}
    assert warns and '陈旧' in warns[0]


def test_stats_fresh_is_not_reported(tmp_path):
    stats_path = tmp_path / 'stats.json'
    stats_path.write_text(json.dumps({'html_total': 1}), encoding='utf-8')
    cl = tmp_path / 'CHANGELOG.md'
    cl.write_text('x', encoding='utf-8')
    os.utime(stats_path, (2000, 2000))
    os.utime(cl, (1000, 1000))
    stats, warns = agent_start.load_stats_with_warnings(str(stats_path), str(cl))
    assert warns == []
