import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import batch_closeout as bc  # noqa: E402
import version_surface as vs  # noqa: E402

BATCH = 'W1114'
DATE = '2026-11-03'
DESC = '落段收官链加版本面幂等推进步并修交接文档当前 HEAD 句缺失缺陷'


def _sample_readme():
    return '> **当前批次 W1113（2026-11-03）**：旧描述·A1-A6<!--doc-sync:exempt-->'


def _sample_structure():
    return '> 当前批次：W1113（2026-11-03）— 旧描述—A1-A6'


def _sample_project_note():
    return '''> 当前批次 W1113（2026-11-03）：旧描述·详细变更见 CHANGELOG
- **当前版本**：W1113（2026-11-03）— 旧描述'''


def _sample_citation():
    return '''version: "W1113" # 批次号形态
date-released: "2026-11-03"'''


def _sample_workflows():
    return '''> **W234-E1 → W450-W1113** — 西游记解读项目（''' + vs.WINPATH + '''，W1113）的 GitHub Actions 工作流层。
> **W450-W1113**：verify 门禁体系扩展'''


def _sample_handover():
    return '''前文 当前 HEAD = W1113（旧描述；详见 CHANGELOG）。
## 一、当前进度（W1113 旧描述；更早批次详见 CHANGELOG.md）'''


def test_readme_version_line_advanced():
    out, changed = vs.advance_readme(_sample_readme(), BATCH, DATE, DESC)
    assert changed is True
    assert '> **当前批次 W1114（2026-11-03）**：' + DESC + '·A1-A6' in out
    assert '<!--doc-sync:exempt-->' in out, '尾部豁免标记必须保留'


def test_structure_version_line_advanced():
    out, changed = vs.advance_structure(_sample_structure(), BATCH, DATE, DESC)
    assert changed is True
    assert '> 当前批次：W1114（2026-11-03）— ' + DESC + '—A1-A6' in out


def test_project_note_two_lines_advanced():
    out, changed = vs.advance_project_note_head(_sample_project_note(), BATCH, DATE, DESC)
    assert changed is True
    assert '> 当前批次 W1114（2026-11-03）：' + DESC + '·详细变更见' in out
    out2, changed2 = vs.advance_project_note_item(out, BATCH, DATE, DESC)
    assert changed2 is True
    assert '- **当前版本**：W1114（2026-11-03）— ' + DESC in out2


def test_citation_advanced():
    out, changed = vs.advance_citation(_sample_citation(), BATCH, DATE)
    assert changed is True
    assert 'version: "W1114"' in out and 'date-released: "2026-11-03"' in out
    assert '# 批次号形态' in out, 'CITATION 行尾注释必须保留'


def test_workflows_interval_advanced():
    out, changed = vs.advance_workflows_readme(_sample_workflows(), BATCH)
    assert changed is True
    assert 'W450-W1114' in out
    assert 'W450-WW1114' not in out, '区间号不得出现双 W（纯数字拼接）'
    assert '，W1114）的 GitHub Actions' in out


def test_handover_literals_advanced():
    out, changed = vs.advance_handover_current_head(_sample_handover(), BATCH, DESC)
    assert changed is True
    assert '当前 HEAD = W1114（' + DESC + '；详见 CHANGELOG）' in out
    out2, changed2 = vs.advance_handover_progress(out, BATCH, DESC)
    assert changed2 is True
    assert '## 一、当前进度（W1114 ' + DESC + '；更早批次详见 CHANGELOG.md）' in out2


def test_advance_is_idempotent():
    """幂等核心：同一目标推进两次 ⇒ 第二次零变化（rebase/返工可重复跑）。"""
    for fn, args in (
        (vs.advance_readme, (_sample_readme(), BATCH, DATE, DESC)),
        (vs.advance_structure, (_sample_structure(), BATCH, DATE, DESC)),
        (vs.advance_citation, (_sample_citation(), BATCH, DATE)),
        (vs.advance_workflows_readme, (_sample_workflows(), BATCH)),
        (vs.advance_handover_current_head, (_sample_handover(), BATCH, DESC)),
        (vs.advance_handover_progress, (_sample_handover(), BATCH, DESC)),
    ):
        out, changed = fn(*args)
        assert changed is True, fn.__name__
        out2, changed2 = fn(out, *args[1:])
        assert changed2 is False, '%s 第二次推进仍有变化（非幂等）' % fn.__name__
        assert out2 == out, '%s 第二次推进内容漂移' % fn.__name__


def test_missing_anchor_fails_closed():
    """锚点缺失必须 fail-closed（不得静默当作「已是目标」）。"""
    for fn, args in (
        (vs.advance_readme, ('无锚点', BATCH, DATE, DESC)),
        (vs.advance_structure, ('无锚点', BATCH, DATE, DESC)),
        (vs.advance_citation, ('无锚点', BATCH, DATE)),
        (vs.advance_workflows_readme, ('无锚点', BATCH)),
        (vs.advance_handover_current_head, ('无锚点', BATCH, DESC)),
        (vs.advance_handover_progress, ('无锚点', BATCH, DESC)),
    ):
        try:
            fn(*args)
        except AssertionError:
            continue
        raise AssertionError('%s 锚点缺失未 fail-closed' % fn.__name__)


def test_closeout_steps_put_versions_between_stats_and_csp():
    """版本面推进步必须在 stats 之后、csp 之前（csp/cspcheck 仍末两步·既有承诺不破）。"""
    order = bc.step_order()
    assert 'versions' in order
    assert order.index('versions') == order.index('stats') + 1
    assert order.index('versions') == order.index('csp') - 1
    assert order[-2:] == ['csp', 'cspcheck']
    assert order[0] == 'precheck'


def test_closeout_main_runs_versions_step(monkeypatch):
    """行为锁：main() 实际调用链里 versions 步被执行（防 STEPS 声明与实现双写漂移）。"""
    calls = []

    def fake_run(args, cwd=None):
        calls.append(' '.join(str(a) for a in args))
        return 0, 'CSP ok'

    monkeypatch.setattr(bc, 'run', fake_run)
    monkeypatch.setattr(bc, 'snapshot_index', lambda: ['x'])
    monkeypatch.setattr(bc, 'precheck_ledger', lambda *a, **k: (True, []))
    monkeypatch.setattr(bc, 'selfref_precheck', lambda: (True, ['通过']))
    monkeypatch.setattr(vs, 'advance_all',
                        lambda batch, date, desc, head_sentence, check=False:
                        [('README.md', True)])
    rc = bc.main(['--batch', 'W9999', '--paths', 'a.py'])
    assert rc == 0
    i_stats = next(i for i, c in enumerate(calls) if 'stats.py' in c)
    i_csp = next(i for i, c in enumerate(calls) if 'generate_csp.py' in c and '--check' not in c)
    assert i_stats < i_csp, 'stats 必须在 csp 之前'


def test_closeout_versions_step_does_final_add(monkeypatch, tmp_path):
    """add 收尾：versions 步必须按 spec.file_index_rows 再 add 一次（末位产物纳入暂存）。"""
    spec = tmp_path / 'spec.json'
    spec.write_text(json.dumps({
        'batch': 'W9999', 'date': '2026-11-03', 'desc': '测试描述',
        'head_sentence': '测试描述',
        'file_index_rows': ['| README.md | W9999 | x |', '| STRUCTURE.md | W9999 | x |'],
    }), encoding='utf-8')
    adds = []

    def fake_run(args, cwd=None):
        if args[0] == 'git' and args[1] == 'add':
            adds.append(args[3:])
        return 0, 'ok'

    monkeypatch.setattr(bc, 'run', fake_run)
    monkeypatch.setattr(vs, 'advance_all',
                        lambda batch, date, desc, head_sentence, check=False:
                        [('README.md', True)])
    ok = bc._run_versions(str(spec), 'W9999')
    assert ok is True
    assert adds, 'versions 步未做收尾 add'
    assert 'README.md' in adds[-1] and 'STRUCTURE.md' in adds[-1]


def test_precheck_ledger_counts_data_rows_only(tmp_path):
    """负样本（W1114 根修 off-by-one）：表头行不计入；数据行 60 PASS / 61 FAIL。

    原实现用 startswith('| W') 计数 ⇒ 台账表头行（形如「| W 号 | 主题 | …」）被计入
    ⇒ 读数恒多 1 ⇒ 窗口 60（数据行 ≤ 60）被误判超窗 ⇒ 收官链恒判超窗、实际不可用
    （W1112 批把该假阳记成正面案例·W1114 订正）。
    """
    head = '| W 号 | 主题 | 关联 commit | CHANGELOG 版段 | 状态 | 认领会话 | touches |'
    led = tmp_path / 'ledger.md'
    body60 = ''.join('| W%04d | x |' % (i,) + chr(10) for i in range(1, 61))
    led.write_text(head + chr(10) + body60, encoding='utf-8')
    ok, msgs = bc.precheck_ledger(str(led))
    assert ok is True, '数据行 60 应 PASS（表头行不计入）· msgs=%s' % msgs

    body61 = ''.join('| W%04d | x |' % (i,) + chr(10) for i in range(1, 62))
    led.write_text(head + chr(10) + body61, encoding='utf-8')
    ok2, msgs2 = bc.precheck_ledger(str(led))
    assert ok2 is False, '数据行 61 应 FAIL'
    assert any('数据行' in m for m in msgs2), msgs2
