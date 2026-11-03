#!/usr/bin/env python3
"""batch_closeout.py —— 落段收官一键脚本（工具层·不碰门禁脚本）。

把批收官反复踩的三个坑固化为脚本内建步骤，而不是靠人记：
  ① 生成器按 **Git 索引**收集 => 新增件必须**先 add 再 refresh**；
  ② refresh 自身产出的新清单件又让索引变化 => **一轮不收敛** => 迭代到稳定；
  ③ docs_index / 搜索索引生成会改写搜索页内联脚本 => **CSP 重算必须置于最后一步**；
  ④ 台账回窗工具自带「正本同号多行即中止」断言 => 落段前须预检。

用法：
  python scripts/batch_closeout.py --spec scripts/output/_w####_spec.json
  python scripts/batch_closeout.py --steps           # 只打印顺序（自检用）

退出码：0 全链完成且末位自检通过；1 失败（打印失败步骤与修复建议）。
"""
import argparse
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STEPS = [
    ('precheck',   '台账预检（正本同号多行 / 行数窗口）'),
    ('selfref',    'CSS 变量自引用体检（引用第 57 槽既有判据·只引用不复制）'),
    ('add',        'git add 本批改动（生成器按索引收集·须先 add）'),
    ('refresh',    'gen_folder_docs --refresh（迭代至收敛）'),
    ('index',      '搜索索引 + 文档索引'),
    ('stats',      'stats.py --w <批号>'),
    ('csp',        'generate_csp（**必须最后**：前面步骤会改内联脚本）'),
    ('cspcheck',   'generate_csp --check（零漂移校验）'),
]


def run(args, cwd=None):
    p = subprocess.run(args, cwd=cwd or ROOT, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def step_order():
    """返回步骤名序列（供单测断言顺序）。"""
    return [name for name, _desc in STEPS]


def ledger_duplicate_rows(ledger_text):
    """返回台账正本里「同号多行」的号列表（回窗工具的中止条件）。"""
    seen = {}
    for line in ledger_text.split('\n'):
        if not line.startswith('| W'):
            continue
        parts = line.split('|')
        num = parts[1].strip() if len(parts) > 1 else ''
        if num:
            seen[num] = seen.get(num, 0) + 1
    return sorted(k for k, v in seen.items() if v > 1)


def precheck_ledger(ledger_path, window=60):
    """台账预检：返回 (ok, messages)。"""
    msgs = []
    if not os.path.isfile(ledger_path):
        return False, ['台账不存在：' + ledger_path]
    text = io.open(ledger_path, encoding='utf-8').read()
    dups = ledger_duplicate_rows(text)
    if dups:
        msgs.append('台账正本同号多行（回窗工具会中止）：' + '、'.join(dups))
    rows = sum(1 for l in text.split('\n') if l.startswith('| W'))
    if rows > window:
        msgs.append('台账正本 %d 行超过窗口 %d => 须先 archive_ledger_rows.py --apply 腾窗' % (rows, window))
    return (not msgs), msgs


def refresh_until_stable(max_rounds=3):
    """迭代 refresh 直到清单不再变化（解决「一轮不收敛」）。"""
    logs = []
    prev = None
    for i in range(1, max_rounds + 1):
        rc, out = run([sys.executable, 'scripts/gen_folder_docs.py', '--refresh'])
        if rc != 0:
            return False, logs + ['refresh 第 %d 轮失败：%s' % (i, out.strip()[-300:])]
        cur = snapshot_index()
        logs.append('refresh 第 %d 轮完成' % i)
        if cur == prev:
            return True, logs + ['清单已收敛（第 %d 轮无变化）' % i]
        prev = cur
    return True, logs + ['警告：%d 轮内未收敛，请检查生成器是否产出非确定内容' % max_rounds]


def snapshot_index():
    """取索引快照（git 索引里的文件清单 + 工作树文件清单）。"""
    rc, out = run(['git', '-c', 'core.quotepath=false', 'ls-files'])
    files = sorted(out.splitlines())
    return files


def selfref_precheck():
    """落段前置：CSS 变量自引用体检。

    **只引用不复制**：直接调用仓内既有判据 scripts/check_css_var_selfref.py（主会话 W1110
    已挂为第 57 槽）⇒ 全站单一事实源，避免两份扫描实现漂移。
    """
    script = os.path.join(ROOT, 'scripts', 'check_css_var_selfref.py')
    if not os.path.isfile(script):
        return True, ['未找到 scripts/check_css_var_selfref.py => 跳过自引用体检']
    rc, out = run([sys.executable, script, '--gate'])
    if rc == 0:
        return True, ['CSS 变量自引用体检：通过']
    return False, ['CSS 变量自引用体检未过（详见下方输出）', out.strip()[-600:]]


def collect_paths(spec_path, extra):
    """待 add 的路径集合：spec 的 file_index_rows + 显式 --paths（禁 git add -A·防代提他方在途件）。"""
    paths = []
    if spec_path and os.path.isfile(spec_path):
        import json
        sp = json.loads(io.open(spec_path, encoding='utf-8').read())
        for row in sp.get('file_index_rows', []):
            p = row.strip().strip('|').split('|')[0].strip()
            if p:
                paths.append(p)
    for p in extra:
        if p not in paths:
            paths.append(p)
    return paths


def main(argv=None):
    ap = argparse.ArgumentParser(description='落段收官一键脚本')
    ap.add_argument('--spec', help='本批 spec json 路径')
    ap.add_argument('--batch', help='批号（缺省从 spec 读）')
    ap.add_argument('--paths', nargs='*', default=[], help='额外需 add 的路径')
    ap.add_argument('--steps', action='store_true', help='只打印执行顺序')
    ap.add_argument('--dry-run', action='store_true', help='只做预检不落盘')
    a = ap.parse_args(argv)
    if a.steps:
        for n, d in STEPS:
            print('%-10s %s' % (n, d))
        return 0
    batch = a.batch
    if not batch and a.spec and os.path.isfile(a.spec):
        import json
        batch = json.loads(io.open(a.spec, encoding='utf-8').read()).get('batch')
    led = os.path.join(ROOT, 'docs', '00-导读', 'W批次编号对账表.md')
    ok, msgs = precheck_ledger(led)
    if msgs:
        for m in msgs:
            print('[precheck] ' + m)
    if not ok:
        print('[precheck] 预检未过 => 中止（先修上述项再跑）')
        return 1
    ok2, msgs2 = selfref_precheck()
    for m in msgs2:
        print('[selfref] ' + m)
    if not ok2:
        print('[selfref] 自引用体检未过 => 中止（先修自引用再落段）')
        return 1
    if a.dry_run:
        print('[dry-run] 预检通过，未落盘')
        return 0
    paths = collect_paths(a.spec, a.paths)
    if paths:
        run(['git', 'add', '--'] + paths)
        print('[add] 已 add %d 件' % len(paths))
    else:
        print('[add] 无待 add 路径（spec.rows 为空？请用 --paths 显式指定）')
    good, logs = refresh_until_stable()
    for l in logs:
        print('[refresh] ' + l)
    if not good:
        return 1
    for cmd in (['_gen_search_index.py'], ['docs_index.py']):
        rc, out = run([sys.executable, 'scripts/' + cmd[0]])
        print('[index] %s -> %s' % (cmd[0], 'OK' if rc == 0 else 'FAIL'))
        if rc != 0:
            print(out.strip()[-400:])
            return 1
    if batch:
        rc, out = run([sys.executable, 'scripts/stats.py', '--w', batch])
        print('[stats] --w %s -> %s' % (batch, 'OK' if rc == 0 else 'FAIL'))
        if rc != 0:
            print(out.strip()[-400:])
            return 1
    rc, out = run([sys.executable, 'scripts/generate_csp.py'])
    print('[csp] 重算 -> %s' % ('OK' if rc == 0 else 'FAIL'))
    if rc != 0:
        print(out.strip()[-400:])
        return 1
    rc, out = run([sys.executable, 'scripts/generate_csp.py', '--check'])
    tail = [l for l in out.splitlines() if 'CSP' in l]
    print('[cspcheck] ' + (tail[-1] if tail else 'OK'))
    if rc != 0:
        print(out.strip()[-400:])
        return 1
    print('---- 收官链完成：顺序 ' + ' -> '.join(step_order()) + ' ----')
    return 0


if __name__ == '__main__':
    sys.exit(main())
