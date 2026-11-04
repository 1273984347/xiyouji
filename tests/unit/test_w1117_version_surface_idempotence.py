import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import version_surface as vs  # noqa: E402

BATCH = 'W1117'
DATE = '2026-11-04'
DESC_PLAIN = '不含分号的描述'
DESC_SEMI = '含分号的描述；带分号'


def _samples(desc):
    """各版本面点的合成样本（desc 可含「；」·W1117 的修复目标）。"""
    return {
        'CHANGELOG.md': (
            '# 更新日志\n'
            '\n'
            '**W### 编号规则**：W001-W0900 对应 v0.1-v2.0.72；W100+ 对应 v2.1.0+（W001-W0900）\n'
            '\n'
            '### W0900（2026-01-01）：旧段\n'
        ),
        'README.md': (
            '> **当前批次 W0900（2026-01-01）**：' + desc + '·A1-A6<!--doc-sync:exempt-->\n'
            '# 标题\n'
            '正文行\n'
        ),
        'STRUCTURE.md': (
            '> 当前批次：W0900（2026-01-01）— ' + desc + '—A1-A6\n'
            '# 标题\n'
            '正文行\n'
        ),
        'docs/00-导读/项目说明.md': (
            '> 当前批次 W0900（2026-01-01）：' + desc + '·详细变更见 CHANGELOG\n'
            '- **当前版本**：W0900（2026-01-01）— ' + desc + '\n'
            '- **当前阶段**：阶段内容·尾巴\n'
            '- **关键产出**：产出\n'
        ),
        'CITATION.cff': 'version: "W0900" # 批次号形态\ndate-released: "2026-01-01"\n',
        '.github/workflows/README.md': (
            '> **W234-E1 → W450-W0900** — 西游记解读项目（' + vs.WINPATH + '，W0900）的 GitHub Actions 工作流层。\n'
            '> **W450-W0900**：verify 门禁体系扩展\n'
        ),
        'HANDOVER.md': (
            '前文 当前 HEAD = W0900（' + desc + '；详见 CHANGELOG）。\n'
            '## 一、当前进度（W0900 ' + desc + '；更早批次详见 CHANGELOG.md）\n'
        ),
    }


def _advance_all(texts, batch, date, desc):
    """按 POINTS 顺序把各文件的版本面点推进一次（返回新文本 dict）。"""
    out = dict(texts)
    for rel, fn in vs.POINTS:
        if rel not in out:
            continue
        if fn is vs.advance_changelog_rule:
            out[rel], _c = fn(out[rel], batch)
        elif fn is vs.advance_citation:
            out[rel], _c = fn(out[rel], batch, date)
        elif fn is vs.advance_workflows_readme:
            out[rel], _c = fn(out[rel], batch)
        elif fn is vs.advance_handover_current_head:
            out[rel], _c = fn(out[rel], batch, desc)
        elif fn is vs.advance_handover_progress:
            out[rel], _c = fn(out[rel], batch, desc)
        else:
            out[rel], _c = fn(out[rel], batch, date, desc)
    return out


def test_second_pass_is_idempotent_plain_desc():
    """二次推进零变化（desc 不含分号）。"""
    texts = _samples(DESC_PLAIN)
    once = _advance_all(texts, BATCH, DATE, DESC_PLAIN)
    twice = _advance_all(once, BATCH, DATE, DESC_PLAIN)
    assert once == twice, '第二次推进有内容漂移'
    assert 'W1117' in once['README.md']


def test_second_pass_is_idempotent_desc_with_semicolon():
    """二次推进零变化（desc **含分号**·W1117 修复目标·此前 fail-closed）。"""
    texts = _samples(DESC_SEMI)
    once = _advance_all(texts, BATCH, DATE, DESC_SEMI)
    twice = _advance_all(once, BATCH, DATE, DESC_SEMI)
    assert once == twice, 'desc 含分号时第二次推进有漂移'
    assert once['HANDOVER.md'].count('；更早批次详见 CHANGELOG.md）') == 1
    assert DESC_SEMI in once['HANDOVER.md']


def test_changelog_rule_limit_advanced_and_idempotent():
    """CHANGELOG 编号规则段上限推进到本批号且二次幂等。"""
    text = '规则（W001-W0900）\n'
    out, changed = vs.advance_changelog_rule(text, BATCH)
    assert changed is True
    assert '（W001-W1117）' in out
    out2, changed2 = vs.advance_changelog_rule(out, BATCH)
    assert changed2 is False
    assert out2 == out


def test_desc_with_right_paren_fails_closed():
    """desc 含右括号 ⇒ 尾部锚点异常 ⇒ 必须 fail-closed（不得静默产出坏文本）。"""
    texts = _samples('含右括号的描述）')
    try:
        _advance_all(texts, BATCH, DATE, '含右括号的描述）')
    except AssertionError:
        return
    raise AssertionError('desc 含「）」未 fail-closed')


def test_all_points_are_idempotent_on_every_sample_file():
    """逐文件逐点：第一次推进必变（除已就位者）·第二次必零变化。"""
    for desc in (DESC_PLAIN, DESC_SEMI):
        texts = _samples(desc)
        once = _advance_all(texts, BATCH, DATE, desc)
        twice = _advance_all(once, BATCH, DATE, desc)
        for rel in texts:
            assert once[rel] == twice[rel], '%s（desc=%s）第二次推进漂移' % (rel, desc)
            assert once[rel].count('\n') == texts[rel].count('\n'), '%s 行数变化（吞行）' % rel


# ---------------------------------------------------------------------------
# W1117 追加：批次级单调守卫（低号批不得回退现役面）
#
# 场景：并行会话乱序合并——对方 W1118 先合入 main，我方 W1117 后落段。
# 版本面表达「现在是什么」⇒ 只能指向最高号 ⇒ 低号批收官时必须零变化，
# 否则会把 README/STRUCTURE/项目说明/CITATION/workflows README/HANDOVER/
# 编号规则段全部回退到低号（与 backfill_changelog.py 的「当前态指向最高号」相悖）。
# ---------------------------------------------------------------------------


def test_current_batch_extraction():
    """现役批号提取：命中现役位；旧形态（无 W 号）⇒ None。"""
    assert vs._current_batch('README.md',
                             '> **当前批次 W1118（2026-11-04）**：x·A1-A6\n') == 1118
    assert vs._current_batch('CHANGELOG.md', '规则（W001-W1118）\n') == 1118
    assert vs._current_batch('CITATION.cff', 'version: "W1118" # c\n') == 1118
    assert vs._current_batch('README.md',
                             '> **当前版本 v2.3.17（2026-01-01）**：x\n') is None


def test_advance_text_does_not_regress_higher_current_surface():
    """目标批号低于该文件现役批号 ⇒ 零变化（不回退·单调守卫）。"""
    high = {rel: t.replace('W0900', 'W1118')
            for rel, t in _samples(DESC_PLAIN).items()}
    for rel, t in high.items():
        out, changed = vs.advance_text(t, rel, BATCH, DATE, DESC_PLAIN, DESC_PLAIN)
        assert changed is False, '%s：目标批号更低却发生了推进（版本面回退）' % rel
        assert out == t, '%s：低号批改写了现役面' % rel
        assert 'W1118' in out


def test_advance_text_advances_when_target_is_higher():
    """目标批号高于现役批号 ⇒ 正常推进（守卫不误伤·不阻断正常路径）。"""
    for rel, t in _samples(DESC_PLAIN).items():
        out, changed = vs.advance_text(t, rel, 'W1120', DATE, DESC_PLAIN, DESC_PLAIN)
        assert changed is True, '%s：高号目标未推进（守卫误伤）' % rel
        assert 'W1120' in out


def test_changelog_rule_never_regresses():
    """编号规则段上限只升不降（目标号低于当前 ⇒ 零变化）。"""
    text = '规则（W001-W1118）\n'
    out, changed = vs.advance_changelog_rule(text, BATCH)
    assert changed is False
    assert '（W001-W1118）' in out
