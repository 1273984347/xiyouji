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
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAX_DOC_BYTES = 262144   # W1119：治理文档正本体积上限（256KiB）
ARCHIVE_CHUNK = 50       # W1119：体积模式每批迁出的段数（最后一批可不足）
LEDGER_WINDOW = 60       # W1119：台账正本数据行窗口

STEPS = [
    ('archive',    '腾窗（**须在 precheck 之前**：体积阈值 262144B·每批 50 段·两面同 W 号下界 + 台账行窗口·W1119）'),
    ('precheck',   '台账预检（正本同号多行 / 行数窗口）'),
    ('selfref',    'CSS 变量自引用体检（引用第 57 槽既有判据·只引用不复制）'),
    ('add',        'git add 本批改动（生成器按索引收集·须先 add）'),
    ('refresh',    'gen_folder_docs --refresh（迭代至收敛）'),
    ('stats',      'stats.py --w <批号>'),
    ('versions',   '版本面推进（跨文件字面量·幂等·只引用 version_surface）'),
    ('index',      '搜索索引 + 文档索引（**须在 versions 之后**：版本面推进会改 README/STRUCTURE/项目说明等 docs 条目·索引早于推进则内嵌索引陈旧·W1117 修）'),
    ('docnums',    '文案数字 ↔ 证据件对表闸（清单驱动·读最终产物·W1116）'),
    ('regsurface', '登记面一致性闸（六项·W1116）'),
    ('csp',        'generate_csp（**csp/cspcheck 仍为末两步**：前面步骤会改内联脚本）'),
    ('cspcheck',   'generate_csp --check（零漂移校验）'),
]


def _run_archive():
    """腾窗步（W1119）：**必须排在 precheck 之前**。

    W1117 实证：precheck 是 fail-closed 中止（台账数据行 > 窗口即 return 1）⇒
    若腾窗步排在其后，台账超窗时流水线在预检就中止 ⇒ 永远到不了腾窗步 ⇒ 死路径。
    ⇒ 顺序：先修窗（腾窗）再体检（precheck）。

    ① 体积阈值：CHANGELOG 与 file-index 正本各 ≤ MAX_DOC_BYTES 字节；每批 ARCHIVE_CHUNK 段，
       循环到达标；两面迁到**同一 W 号下界**（迁完断言·W1119）。
    ② 台账行窗口：正本数据行 > LEDGER_WINDOW 时迁出最老行（--keep = 窗口-1）。
    两步皆幂等：未超阈值时工具自身报 SKIP 且 rc=0 ⇒ 零动作。
    """
    import sys
    rc, out = run([sys.executable, os.path.join('scripts', 'archive_segments.py'),
                   '--target', 'both', '--max-bytes', str(MAX_DOC_BYTES),
                   '--chunk', str(ARCHIVE_CHUNK), '--apply'])
    sys.stdout.write(out)
    if rc != 0:
        return False
    led = os.path.join(ROOT, 'docs', '00-导读', 'W批次编号对账表.md')
    rows = 0
    try:
        import archive_ledger_rows
        for line in io.open(led, encoding='utf-8').read().split(chr(10)):
            if archive_ledger_rows.ROW_RE.match(line):
                rows += 1
    except Exception as e:
        print('[archive] 台账行数读取失败（跳过行窗口）: %s' % e)
        return True
    if rows > LEDGER_WINDOW:
        rc2, out2 = run([sys.executable, os.path.join('scripts', 'archive_ledger_rows.py'),
                         '--keep', str(LEDGER_WINDOW - 1), '--apply'])
        sys.stdout.write(out2)
        if rc2 != 0:
            return False
    else:
        print('[archive] 台账 %d 行 <= 窗口 %d·行窗口未触发' % (rows, LEDGER_WINDOW))
    return True


def run(args, cwd=None):
    p = subprocess.run(args, cwd=cwd or ROOT, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def step_order():
    """返回步骤名序列（供单测断言顺序）。"""
    return [name for name, _desc in STEPS]


def ledger_duplicate_rows(ledger_text):
    """返回台账正本里「同号多行」的号列表（回窗工具的中止条件）。"""
    import archive_ledger_rows
    seen = {}
    for line in ledger_text.split('\n'):
        if not archive_ledger_rows.ROW_RE.match(line):
            continue
        parts = line.split('|')
        num = parts[1].strip() if len(parts) > 1 else ''
        if num:
            seen[num] = seen.get(num, 0) + 1
    return sorted(k for k, v in seen.items() if v > 1)


def precheck_ledger(ledger_path, window=60):
    """台账预检：返回 (ok, messages)。

    **行数口径（W1114 根修 off-by-one）**：原实现用 startswith('| W') 逐行计数 ⇒ 台账**表头行**
    （形如「| W 号 | 批次标题 | …」）同样以「| W」开头 ⇒ 被计入 ⇒ 读数恒比真实数据行多 1
    ⇒ 窗口 60（= 数据行 ≤ 60·口径见 scripts/archive_ledger_rows.py 的 ROW_RE 与
    check_doc_size_budget C5 硬判据）被误判为「61 行超窗」⇒ **收官链恒判超窗、实际不可用**
    （W1112 批把该假阳记成正面案例·W1114 订正）。⇒ 现复用 archive_ledger_rows.ROW_RE 的
    **数据行**口径（单一事实源·不另写正则），阈值语义明确为「数据行 ≤ window」。
    """
    msgs = []
    if not os.path.isfile(ledger_path):
        return False, ['台账不存在：' + ledger_path]
    text = open(ledger_path, encoding='utf-8').read()
    dups = ledger_duplicate_rows(text)
    if dups:
        msgs.append('台账正本同号多行（回窗工具会中止）：' + '、'.join(dups))
    import archive_ledger_rows
    rows = sum(1 for line in text.split('\n') if archive_ledger_rows.ROW_RE.match(line))
    if rows > window:
        msgs.append('台账正本 %d **数据行**超过窗口 %d（数据行口径·表头不计·同 archive_ledger_rows.py）'
                    '=> 须先 archive_ledger_rows.py --apply 腾窗' % (rows, window))
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
    """取索引快照：**仅 Git 索引**（git ls-files）·**不含未跟踪件**。

    ⇒ 未跟踪文件不在快照内 ⇒ 收敛判定对未跟踪件不敏感；故 add 步必须先执行
    （生成器按索引收集，未 add 的新件不会被纳入刷新范围）。
    """
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
        # fail-closed（W1112 收官笔·独立盲审 M3）：判据缺失 = 该步**静默失效**，
        # 收官链照样绿 ⇒ 判据被删/改名时无任何红灯。⇒ 缺失即中止。
        return False, ['未找到 scripts/check_css_var_selfref.py => 判据缺失，收官链中止（fail-closed·不得静默跳过）']
    rc, out = run([sys.executable, script, '--gate'])
    if rc == 0:
        return True, ['CSS 变量自引用体检：通过']
    return False, ['CSS 变量自引用体检未过（详见下方输出）', out.strip()[-600:]]


def collect_paths(spec_path, extra):
    """待 add 的路径集合：spec 的 file_index_rows + 显式 --paths（禁 git add -A·防代提他方在途件）。"""
    paths = []
    if spec_path and os.path.isfile(spec_path):
        import json
        sp = json.loads(open(spec_path, encoding='utf-8').read())
        for row in sp.get('file_index_rows', []):
            p = row.strip().strip('|').split('|')[0].strip()
            if p:
                paths.append(p)
    for p in extra:
        if p not in paths:
            paths.append(p)
    return paths


def _run_prechecks(ledger_path):
    """前置体检：台账预检（行数窗口/同号多行）+ CSS 变量自引用体检。

    两者任一不过即中止（fail-closed）——W1114 起独立成函数（main 加 versions 步后
    复杂度超 ruff 结构档阈值 15）。
    """
    ok, msgs = precheck_ledger(ledger_path)
    for m in msgs:
        print('[precheck] ' + m)
    if not ok:
        print('[precheck] 预检未过 => 中止（先修上述项再跑）')
        return False
    ok2, msgs2 = selfref_precheck()
    for m in msgs2:
        print('[selfref] ' + m)
    if not ok2:
        print('[selfref] 自引用体检未过 => 中止（先修自引用再落段）')
        return False
    return True


def _add_paths(paths):
    """add 步：按显式 pathspec 暂存（禁 git add -A·防代提他方在途件）。

    **W1114 根修（静默失效）**：原实现不检查 git add 的退出码 ⇒ 当 pathspec 里有
    **尚不存在的路径**（如报告文件还没写）时，git add 报「pathspec did not match any
    files」并**整体放弃**（不做部分暂存）⇒ 收官链打印「已 add N 件」而实际 0 件入库
    ⇒ 末位产物漏进提交（C4-f 判「工作树未提交残留」判红）。⇒ 现：① 过滤尚不存在的路径
    并如实报告跳过数；② 检查退出码·失败即中止（fail-closed）。
    """
    exist = [p for p in paths if os.path.exists(os.path.join(ROOT, p))]
    missing = [p for p in paths if p not in exist]
    if missing:
        print('[add] 跳过 %d 个尚不存在的路径（尚未创建·如报告件未落盘）：%s'
              % (len(missing), '、'.join(missing[:5])))
    if not exist:
        print('[add] 无待 add 路径（spec.file_index_rows 为空？请用 --paths 显式指定）')
        return True
    rc, out = run(['git', 'add', '--'] + exist)
    if rc != 0:
        print('[add] git add 失败 => 中止：' + out.strip()[-400:])
        return False
    print('[add] 已 add %d 件' % len(exist))
    return True


def _run_index():
    """index 步：搜索索引 + 文档索引。"""
    for cmd in ('_gen_search_index.py', 'docs_index.py'):
        rc, out = run([sys.executable, 'scripts/' + cmd])
        print('[index] %s -> %s' % (cmd, 'OK' if rc == 0 else 'FAIL'))
        if rc != 0:
            print(out.strip()[-400:])
            return False
    return True


def _run_stats(batch):
    """stats 步：实体化计数（缺批号则跳过）。"""
    if not batch:
        return True
    rc, out = run([sys.executable, 'scripts/stats.py', '--w', batch])
    print('[stats] --w %s -> %s' % (batch, 'OK' if rc == 0 else 'FAIL'))
    if rc != 0:
        print(out.strip()[-400:])
        return False
    return True


def _run_versions(spec_path, batch):
    """版本面推进步（W1114）+ **add 收尾**（把本链已改动的文件纳入暂存）。

    * 版本面 = 跨文件字面量（README / STRUCTURE / 项目说明 / CITATION / workflows README /
      交接文档）⇒ 幂等（已是目标态则零变化）⇒ 与「CHANGELOG 段插入」彻底解耦
      ⇒ rebase / 回退 / 返工场景可单独重跑。
    * **add 收尾**：add 步在链首（生成器按索引收集⇒须前置），但 refresh / index / stats /
      versions 都会在其后改文件 ⇒ 末位产物会漏进提交（C4-f 判「工作树未提交残留」判红）
      ⇒ 此处按 spec.file_index_rows 再 add 一次（显式 pathspec·禁 git add -A）。
    """
    import json
    spec = {}
    if spec_path and os.path.isfile(spec_path):
        with open(spec_path, encoding='utf-8') as f:
            spec = json.load(f)
    desc = spec.get('desc') or ''
    date = spec.get('date') or ''
    head_sentence = spec.get('head_sentence') or desc
    if not (batch and desc and date):
        print('[versions] 缺 spec 的 batch/desc/date => 跳过版本面推进（幂等·不影响其余步）')
        return True
    import version_surface
    results = version_surface.advance_all(batch, date, desc, head_sentence)
    for rel, changed in results:
        print('[versions] %s %s' % ('已推进' if changed else '已是目标态', rel))
    if not _add_paths(collect_paths(spec_path, [])):
        return False
    print('[versions] 中段 add 完成（refresh/index/stats 的产物纳入暂存）')
    return True


def _run_csp(spec_path=None):
    """csp 步：重算内联脚本哈希（写文件的最后一步）+ 暂存本步产物。

    **W1114 修正**：csp 是**最后一个会改文件**的步骤 ⇒ 若只在 versions 步做「收尾 add」，
    csp 改动的页面（内联脚本哈希变化 ⇒ CSP meta 变）会落在暂存之后 ⇒ 判「工作树未提交残留」
    ⇒ 故收尾 add 落到**本步内**（重算后立即按 spec.file_index_rows 再 add 一次），
    既让末位产物进暂存，又保持 csp/cspcheck 仍为最后两步（cspcheck 只读校验·不改文件）。
    """
    rc, out = run([sys.executable, 'scripts/generate_csp.py'])
    print('[csp] 重算 -> %s' % ('OK' if rc == 0 else 'FAIL'))
    if rc != 0:
        print(out.strip()[-400:])
        return False
    if spec_path:
        if not _add_paths(collect_paths(spec_path, [])):
            return False
        print('[csp] 本步产物已暂存（末位产物纳入提交）')
    return True


def _run_docnums(spec_path):
    """文案数字 ↔ 证据件对表闸（W1116·只引用不复制·判据在 scripts/check_doc_numbers.py）。

    为什么在收官链里：W1113~W1115 实证「批收官后结论文案里的数字仍与证据件不一致」（25 处漂移·
    其中 3 处阻断级），而**没有任何机器判据会抓这类漂移** ⇒ 本闸把「人工对表」变成机器断言：
    每批在 spec 的 doc_numbers 段声明「哪处文案 ↔ 哪个证据键」，末位逐项断言。
    未声明 ⇒ 跳过（不伪造红）；声明了但取不到真值/对不上 ⇒ 判红并给出 文件:行号 + 期望 + 实际。
    """
    import json
    if not (spec_path and os.path.isfile(spec_path)):
        print('[docnums] 无 spec ⇒ 跳过（判据不可执行·不伪造红）')
        return True
    with open(spec_path, encoding='utf-8') as f:
        spec = json.load(f)
    if not (spec.get('doc_numbers') or []):
        print('[docnums] spec 无 doc_numbers 声明 ⇒ 跳过（未声明即不判）')
        return True
    script = os.path.join(ROOT, 'scripts', 'check_doc_numbers.py')
    if not os.path.isfile(script):
        print('[docnums] 判据缺失 => 中止（fail-closed·不得静默跳过）')
        return False
    rc, out = run([sys.executable, script, '--spec', spec_path])
    print('[docnums] ' + ('OK' if rc == 0 else 'FAIL'))
    if rc != 0:
        print(out.strip()[-800:])
        return False
    return True


def _run_regsurface(batch):
    """登记面一致性闸（W1116·六项·判据在 scripts/check_registration_surface.py）。

    六项：① 台账本批认领行存在 ② HANDOVER 最后更新链首 == CHANGELOG 现役段
    ③ CHANGELOG 编号规则段上限 == 现役段 ④ HANDOVER 最后更新链条目 ≤3
    ⑤ file-index 含本批段 ⑥ 台账正本数据行 ≤ 窗口（行口径复用 archive_ledger_rows.ROW_RE）。
    """
    script = os.path.join(ROOT, 'scripts', 'check_registration_surface.py')
    if not os.path.isfile(script):
        print('[regsurface] 判据缺失 => 中止（fail-closed·不得静默跳过）')
        return False
    if not batch:
        print('[regsurface] 缺批号 ⇒ 跳过（不伪造红）')
        return True
    rc, out = run([sys.executable, script, '--batch', batch])
    print('[regsurface] ' + ('OK' if rc == 0 else 'FAIL'))
    if rc != 0:
        print(out.strip()[-800:])
        return False
    return True


def _run_cspcheck():
    """cspcheck 步：零漂移校验（恒为最后一步）。"""
    rc, out = run([sys.executable, 'scripts/generate_csp.py', '--check'])
    tail = [line for line in out.splitlines() if 'CSP' in line]
    print('[cspcheck] ' + (tail[-1] if tail else 'OK'))
    if rc != 0:
        print(out.strip()[-400:])
        return False
    return True


def _run_content_stage(a, batch):
    """内容生成段：refresh -> stats -> versions -> index（W1117 抽函数·降 main 复杂度）。

    顺序要点（W1117 实测修）：**index 必须在 versions 之后**——版本面推进会改
    README / STRUCTURE / 项目说明 等 docs 条目，索引若早于推进生成 ⇒ 内嵌索引不含推进后的内容
    ⇒ 第 46 槽「搜索索引新鲜度」判红（字段漂移 + 内嵌索引陈旧）。
    """
    good, logs = refresh_until_stable()
    for line in logs:
        print('[refresh] ' + line)
    if not good:
        return False
    if not _run_stats(batch):
        return False
    if not _run_versions(a.spec, batch):
        return False
    return _run_index()


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
        batch = json.loads(open(a.spec, encoding='utf-8').read()).get('batch')
    led = os.path.join(ROOT, 'docs', '00-导读', 'W批次编号对账表.md')
    if not _run_archive():
        return 1
    if not _run_prechecks(led):
        return 1
    if a.dry_run:
        print('[dry-run] 预检通过，未落盘')
        return 0
    if not _add_paths(collect_paths(a.spec, a.paths)):
        return 1
    if not _run_content_stage(a, batch):
        return 1
    if not _run_docnums(a.spec):
        return 1
    if not _run_regsurface(batch):
        return 1
    if not _run_csp(a.spec):
        return 1
    if not _run_cspcheck():
        return 1
    print('---- 收官链完成：顺序 ' + ' -> '.join(step_order()) + ' ----')
    return 0


if __name__ == '__main__':
    sys.exit(main())
