import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import batch_closeout as bc  # noqa: E402


def test_step_order_puts_csp_last():
    """CSP 重算与 --check 必须是最后两步（前面步骤会改内联脚本）。"""
    order = bc.step_order()
    assert order[0] == 'precheck'
    assert order[-2:] == ['csp', 'cspcheck']
    assert order.index('csp') > order.index('stats')
    assert order.index('csp') > order.index('index')
    assert order.index('csp') > order.index('refresh')


def test_selfref_step_is_after_precheck_and_before_csp():
    """自引用前置体检排在台账预检之后、CSP 之前。"""
    order = bc.step_order()
    assert order.index('selfref') == order.index('precheck') + 1
    assert order.index('selfref') < order.index('csp')


def test_ledger_duplicate_rows_detected():
    text = '| W1100 | a |\n| W1101 | b |\n| W1101 | c |\n'
    assert bc.ledger_duplicate_rows(text) == ['W1101']


def test_ledger_precheck_blocks_over_window(tmp_path):
    led = tmp_path / 'ledger.md'
    rows = ''.join('| W%04d | x |\n' % i for i in range(1, 62))
    led.write_text(rows, encoding='utf-8')
    ok, msgs = bc.precheck_ledger(str(led), window=60)
    assert ok is False
    assert any('腾窗' in m for m in msgs)


def test_ledger_precheck_blocks_duplicate(tmp_path):
    led = tmp_path / 'ledger.md'
    led.write_text('| W1100 | a |\n| W1100 | b |\n', encoding='utf-8')
    ok, msgs = bc.precheck_ledger(str(led))
    assert ok is False
    assert any('同号多行' in m for m in msgs)


def test_refresh_until_stable_converges(monkeypatch):
    """refresh 迭代：快照不再变化即判定收敛。"""
    seq = [['a'], ['a'], ['b'], ['b']]
    calls = {'n': 0}

    def fake_run(args, cwd=None):
        if args[1].endswith('gen_folder_docs.py'):
            calls['n'] += 1
            return 0, 'ok'
        return 0, ''

    def fake_snapshot():
        idx = min(calls['n'], len(seq)) - 1
        return seq[idx]

    monkeypatch.setattr(bc, 'run', fake_run)
    monkeypatch.setattr(bc, 'snapshot_index', fake_snapshot)
    good, logs = bc.refresh_until_stable(max_rounds=4)
    assert good is True
    assert any('收敛' in l for l in logs)


def test_selfref_precheck_skips_when_judgement_missing(monkeypatch):
    """只引用既有判据（不复制实现）：判据缺失时跳过而非误报。"""
    monkeypatch.setattr(bc.os.path, 'isfile', lambda p: False)
    ok, msgs = bc.selfref_precheck()
    assert ok is True
    assert any('跳过' in m for m in msgs)
