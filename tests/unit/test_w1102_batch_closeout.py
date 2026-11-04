import io
import json
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
    assert any('收敛' in line for line in logs)


def test_selfref_precheck_skips_when_judgement_missing(monkeypatch):
    """判据缺失必须**中止**（fail-closed）而非静默跳过。

    W1112 收官笔·独立盲审 M3：原实现「缺失 => 跳过 => 收官链照样绿」⇒ 判据被删/改名时
    该步静默失效且全链无红灯。⇒ 缺失即 return False。

    **函数名沿用旧名**：guardrails 的 api_diff 判据把 tests/ 下的 test 函数也当「公开 API」
    ⇒ 改名即被判「破坏性删除」而阻断提交（仓内实测）。名实不符之处以本 docstring 说明；
    待下一批把 tests/ 排除出「公开 API」范围后再改名为 ..._blocks_when_judgement_missing。
    """
    monkeypatch.setattr(bc.os.path, 'isfile', lambda p: False)
    ok, msgs = bc.selfref_precheck()
    assert ok is False, '判据缺失未中止（静默失效）'
    assert any('fail-closed' in m or '中止' in m for m in msgs)


def test_collect_paths_uses_spec_rows_and_extras(tmp_path):
    """防代提：待 add 集合 = spec.file_index_rows 第 1 列 + 显式 --paths。"""
    spec = tmp_path / 'spec.json'
    spec.write_text(json.dumps({'file_index_rows': [
        '| a.py | W1 | x |', '| b.py | W1 | x |']}), encoding='utf-8')
    assert bc.collect_paths(str(spec), ['c.py']) == ['a.py', 'b.py', 'c.py']


def test_source_has_no_git_add_all():
    """防代提承诺的行为锁：脚本内不得出现全量暂存参数（'-A' / '--all' 字符串字面量）。"""
    src = open(bc.__file__, encoding='utf-8').read()
    assert "'-A'" not in src
    assert '"-A"' not in src
    assert "'--all'" not in src
    assert '"--all"' not in src


def test_main_executes_steps_in_declared_order(monkeypatch):
    """行为锁：main() 实际调用序列必须与 STEPS 声明顺序一致。

    W1112 收官笔·独立盲审 M1：STEPS 常量与 main() 实现是**双写** ⇒ 只断言 STEPS 顺序时，
    改 main() 顺序而不动 STEPS 仍全绿。⇒ 此例锁**实际调用序列**：
    add -> refresh -> stats -> index(搜索/文档) -> csp -> cspcheck。

    **W1117 订正**（跨批改动·留痕见 CHANGELOG W1117 段与 T68 §2.2 B-06）：
    原断言把 index 排在 stats **之前**；W1117 实测该序致**内嵌索引陈旧**——
    版本面推进（versions）会改 README/STRUCTURE/项目说明等 docs 条目 ⇒ 索引若早于 versions 生成，
    内嵌索引不含推进后的内容 ⇒ 第 46 槽「搜索索引新鲜度」判红（本批实测：字段漂移 + 内嵌索引陈旧）。
    ⇒ index 步改到 versions 之后（versions 仍紧邻 stats 之后 ⇒ 并行会话 W1116 的四条顺序断言全成立）。
    """
    calls = []

    def fake_run(args, cwd=None):
        calls.append(' '.join(str(a) for a in args))
        return 0, 'CSP ok'

    monkeypatch.setattr(bc, 'run', fake_run)
    monkeypatch.setattr(bc, 'snapshot_index', lambda: ['x'])
    monkeypatch.setattr(bc, 'precheck_ledger', lambda *a, **k: (True, []))
    monkeypatch.setattr(bc, 'selfref_precheck', lambda: (True, ['通过']))

    rc = bc.main(['--batch', 'W9999', '--paths', 'README.md'])
    assert rc == 0

    def first(pred):
        return next(i for i, c in enumerate(calls) if pred(c))

    i_add = first(lambda c: c.startswith('git add'))
    i_ref = first(lambda c: 'gen_folder_docs.py' in c)
    i_idx = first(lambda c: '_gen_search_index.py' in c)
    i_doc = first(lambda c: 'docs_index.py' in c)
    i_stat = first(lambda c: 'stats.py' in c)
    i_csp = first(lambda c: 'generate_csp.py' in c and '--check' not in c)
    i_chk = first(lambda c: 'generate_csp.py' in c and '--check' in c)
    assert i_add < i_ref < i_stat < i_idx < i_doc < i_csp < i_chk, calls
    # index 步须在 versions 步之后（见 docstring·W1117）⇒ versions 不经 run() 可见，故断言声明位置
    order = bc.step_order()
    assert order.index('index') > order.index('versions')
    assert order.index('versions') == order.index('stats') + 1
    assert order[-2:] == ['csp', 'cspcheck']
