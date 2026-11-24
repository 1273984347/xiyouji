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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# W1315：体积窗/行窗下沉共享层（入口不再兼职常量持有方）
from utils.gate_common import LEDGER_WINDOW, MAX_DOC_BYTES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARCHIVE_CHUNK = 50       # W1119：体积模式每批迁出的段数（最后一批可不足）

STEPS = [
    ('cascade',    '级联落段（batch_cascade --apply --spec：段幂等 W1122 + 滚动超限补滚 W1144 ⇒ HANDOVER 旁路插块自动 catch-up·W1215）'),
    ('archive',    '腾窗（**须在 precheck 之前**：体积阈值 262144B·每批 50 段·两面同 W 号下界 + 台账行窗口·W1119）'),
    ('rebuild',    '幂等段重建（**须在 precheck 之前**：precheck fail-closed ⇒ 修复步排其后即死路径·W1124）'),
    ('precheck',   '台账预检（正本同号多行 / 行数窗口）'),
    ('selfref',    'CSS 变量自引用体检（引用第 57 槽既有判据·只引用不复制）'),
    ('add',        'git add 本批改动（生成器按索引收集·须先 add）'),
    ('pycompile',  'py_compile 语法自检（**须在 add 之后**：索引态 + 工作树态 + 未跟踪三态清单的 .py 逐件编译·任一 SyntaxError 即中止整链·W1128）'),
    ('refresh',    'gen_folder_docs --refresh（迭代至收敛）'),
    ('stats',      'stats.py --w <批号>'),
    ('versions',   '版本面推进（跨文件字面量·幂等·只引用 version_surface）'),
    ('index',      '搜索索引 + 文档索引（**须在 versions 之后**：版本面推进会改 README/STRUCTURE/项目说明等 docs 条目·索引早于推进则内嵌索引陈旧·W1117 修）'),
    ('docnums',    '文案数字 ↔ 证据件对表闸（清单驱动·读最终产物·W1116）'),
    ('regsurface', '登记面一致性闸（六项·W1116）'),
    ('csp',        'generate_csp（**csp/cspcheck 仍为末两步**：前面步骤会改内联脚本）'),
    ('cspcheck',   'generate_csp --check（零漂移校验）'),
    ('gate',       '真全量门禁（pre_push_gate：guardrails→verify→pytest→ci_sim·W1215·--skip-gate 可跳）'),
]


def _run_cascade(spec_path, batch, dry=False):
    """cascade 步（W1215）：batch_cascade --apply --spec 接进收官链**链首**。

    病根（W1214 C7 实证）：HANDOVER 里程碑块插块绕过 batch_cascade ⇒ 滚动淘汰不触发
    ⇒ 概要块只增不减（7>6），而该判据只在 pytest 面 ⇒ 收官链三绿仍 CI 红、补滚要单独
    想起 --rotate-only。⇒ 本步把级联纳入链首：段已存在且与 spec 一致 ⇒ 幂等零变化
    （W1122 守卫）；滚动守卫 W1144 在窗口 >6 时**超限补滚** ⇒ 旁路插块的 miss 在每批
    收官自动 catch-up，不再依赖人记。

    位置在 archive/rebuild 之前：建段归 cascade（rebuild 的 cl_has 判定才有着落）。
    无 spec ⇒ 跳过（非阻断·同 rebuild 语义）。
    **dry=True 时不传 --apply**（batch_cascade 默认只算不写）——否则 --dry-run 会实写段。
    """
    if not spec_path or not os.path.isfile(os.path.join(ROOT, spec_path)):
        print('[cascade] 无 spec 路径或文件不存在 ⇒ 跳过（非阻断）')
        return True
    cmd = [sys.executable, os.path.join('scripts', 'batch_cascade.py'), '--spec', spec_path]
    if not dry:
        cmd.append('--apply')
    rc, out = run(cmd)
    sys.stdout.write(out)
    if rc != 0:
        return False
    return True


def _run_gate(skip=False):
    """gate 步（W1215）：pre_push_gate 真全量（guardrails→verify→pytest→ci_sim）。

    病根（W1214 两轮 CI 浪费实证）：「全量门禁绿」不含 pytest 与 guardrails ⇒ 三绿
    不同源 ⇒ push 后 CI 两连红，而红灯本地各 0.5 s 可测。⇒ 收官链末位直接跑
    pre_push_gate（单一事实源·不在链内复刻步骤清单），一命令出推送判据。
    --skip-gate 供 dry-run/迭代期显式跳过（跳过时打印醒目 NOTE·不静默）。
    """
    if skip:
        print('[gate] --skip-gate 显式跳过（汇总面无推送判据·提交前须单跑 pre_push_gate）')
        return True
    script = os.path.join(ROOT, 'scripts', 'pre_push_gate.py')
    if not os.path.isfile(script):
        print('[gate] scripts/pre_push_gate.py 缺失 => 中止（fail-closed·不得静默跳过）')
        return False
    rc, out = run([sys.executable, script])
    sys.stdout.write(out)
    if rc != 0:
        return False
    return True


def _run_rebuild(spec_path, batch, dry=False):
    """幂等段重建步（W1124·T74 R-A）：把 scripts/rebuild_section.py 接进收官链主链。

    病根：rebuild_section.py 是**独立入口**（W1120 建）⇒ 段内容与 spec 不一致时只能人工
    想起单独跑它 ⇒ 「改完段内容后重建」这一步在流程里是断的 ⇒ 段与 spec 长期漂移。

    W1124：接入收官链 ⇒ 每批收官时对本批段自动做一次「就地重建 + 幂等零变化」：
      · 段已存在且内容一致 ⇒ 零变化（不写盘）
      · 段已存在但内容不一致 ⇒ 就地重建该段（只动本批段·历史段逐段比对不变）
      · 两面皆未立段 ⇒ 跳过（建段归 batch_cascade / backfill·本步不建段）
    **顺序须在 precheck 之前**：precheck 是 fail-closed 中止 ⇒ 修复步排其后即死路径
    （W1117 实证·同族教训：腾窗步前置）。
    """
    if not spec_path or not os.path.isfile(os.path.join(ROOT, spec_path)):
        print('[rebuild] 无 spec 路径或文件不存在 ⇒ 跳过（非阻断）')
        return True
    try:
        import backfill_changelog as bf
        bnum = int(str(batch).lstrip('Ww'))
        with open(os.path.join(ROOT, 'CHANGELOG.md'), encoding='utf-8') as fh:
            cl_text = fh.read()
        with open(os.path.join(ROOT, 'scripts', 'output', 'file-index.md'), encoding='utf-8') as fh:
            fi_text = fh.read()
        cl_has = any(w == bnum for w, _st in bf.segments(cl_text))
        fi_has = any(int(m.group(1)[1:]) == bnum
                     for m in bf.RE_FI_SEG.finditer(fi_text))
    except (ImportError, OSError, ValueError) as e:
        print('[rebuild] 立段判定依赖异常（跳过·非阻断）: %s' % e)
        return True
    if not (cl_has or fi_has):
        print('[rebuild] 本批段两面皆未立段 ⇒ 跳过（建段归 batch_cascade / backfill）')
        return True
    import sys
    cmd = [sys.executable, os.path.join('scripts', 'rebuild_section.py'),
           '--batch', str(batch), '--spec', spec_path]
    if not dry:  # dry=True ⇒ rebuild_section 默认 dry-run（只报不写）
        cmd.append('--apply')
    rc, out = run(cmd)
    sys.stdout.write(out)
    if rc != 0:
        return False
    return True


def _run_archive(dry=False):
    """腾窗步（W1119）：**必须排在 precheck 之前**。

    W1117 实证：precheck 是 fail-closed 中止（台账数据行 > 窗口即 return 1）⇒
    若腾窗步排在其后，台账超窗时流水线在预检就中止 ⇒ 永远到不了腾窗步 ⇒ 死路径。
    ⇒ 顺序：先修窗（腾窗）再体检（precheck）。

    ① 体积阈值：CHANGELOG 与 file-index 正本各 ≤ MAX_DOC_BYTES 字节；每批 ARCHIVE_CHUNK 段，
       循环到达标；两面迁到**同一 W 号下界**（迁完断言·W1119）。
    ② 台账行窗口：正本数据行 > LEDGER_WINDOW 时迁出最老行（--keep = 窗口-1）。
    两步皆幂等：未超阈值时工具自身报 SKIP 且 rc=0 ⇒ 零动作。
    **dry=True 时两步都改传 --dry-run**——否则 --dry-run 预检会实迁段/迁行。
    """
    import sys
    mode = '--dry-run' if dry else '--apply'
    rc, out = run([sys.executable, os.path.join('scripts', 'archive_segments.py'),
                   '--target', 'both', '--max-bytes', str(MAX_DOC_BYTES),
                   '--chunk', str(ARCHIVE_CHUNK), mode])
    sys.stdout.write(out)
    if rc != 0:
        return False
    led = os.path.join(ROOT, 'docs', '00-导读', 'W批次编号对账表.md')
    # W1121：原实现用 io.open 但**未 import io** ⇒ NameError 被同句宽 except 吞掉
    # ⇒ 台账行窗口腾窗**从未真正触发**（静默失效·每次都走「读取失败·跳过」分支）。
    # ⇒ 根修：改仓内主流 open(..., encoding=) 写法；except 收窄到 ImportError/OSError
    #    ⇒ 代码缺陷（NameError 等）不再被吞，直接暴露。
    try:
        import archive_ledger_rows
    except ImportError as e:
        print('[archive] 行数统计依赖缺失（跳过行窗口·非阻断）: %s' % e)
        return True
    try:
        with open(led, encoding='utf-8') as fh:
            rows = sum(1 for line in fh if archive_ledger_rows.ROW_RE.match(line))
    except OSError as e:
        # W1277 对抗审查 P3-5 修：台账不可读原样跳过行窗口（fail-open）⇒ 直接抛出（铁律 23）
        raise OSError('[archive] 台账行数读取失败（fail-closed·行窗口不可跳过）: %s' % e) from e
    if rows > LEDGER_WINDOW:
        rc2, out2 = run([sys.executable, os.path.join('scripts', 'archive_ledger_rows.py'),
                         '--keep', str(LEDGER_WINDOW - 1), '--dry-run' if dry else '--apply'])
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
    # W1277 对抗审查 P3-5 修：非收敛原样 True（铁律 23 违例·缺陷路径与正常路径同成功）⇒ 阻断
    return False, logs + ['FAIL：%d 轮内未收敛（生成器产出非确定内容）——修复后再收官' % max_rounds]


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


def _expand_group_row(p):
    """分组行 → 该目录下**可入库**文件（git 口径）。非分组行返回 None。

    W1142 立式：分组行（「<目录>/（<N 件>）」）展开为该目录的文件集合。
    W1308 根修：原实现用 os.walk 递归**磁盘** ⇒ 会把 .gitignore 忽略的目录
    （实测 docs/S2-外部分享、视觉重设计样板/*/_verify_shots）也纳入 ⇒ git add 报
    「paths are ignored by one of your .gitignore files」⇒ 收官链 add 步整链中止
    （分组行本为省登记面体积·反成阻塞）。
    ⇒ 改用 git 口径：已跟踪文件（ls-files）+ 未跟踪且**未被忽略**文件
    （ls-files --others --exclude-standard）⇒ 忽略面永不进 add 集合。
    """
    import batch_spec as _bs
    m = _bs._DIR_GROUP_RE.match(p)  # W1142（P2-3）：正则单一实现（batch_spec 唯一定义）
    if not m:
        return None
    d = m.group(1).replace('\\', '/')
    out = []
    for extra in ([], ["--others", "--exclude-standard"]):
        rc, so = run(["git", "-C", ROOT, "-c", "core.quotepath=false",
                       "ls-files"] + extra + ["--", d])
        if rc != 0:
            continue
        for line in so.splitlines():
            rel = line.strip()
            if rel and rel not in out:
                out.append(rel)
    return out


def collect_paths(spec_path, extra):
    """待 add 的路径集合：spec 的 file_index_rows + 显式 --paths（禁 git add -A·防代提他方在途件）。

    W1142 兼容：目录分组行（「<目录>/（<N> 件）」·batch_spec.fi_group_rows 立式）
    展开为该目录的磁盘现有文件——分组只在 spec 分组形态时出现（现役 spec 恒全量，
    本兜底防未来分组态让 add 静默跳过·W1139 实测「跳过 9 个 site/（10 件）」教训）。
    """
    paths = []
    if spec_path and os.path.isfile(spec_path):
        import json
        sp = json.loads(open(spec_path, encoding='utf-8').read())
        for row in sp.get('file_index_rows', []):
            p = row.strip().strip('|').split('|')[0].strip()
            if not p:
                continue

            expanded = _expand_group_row(p)
            if expanded is not None:
                paths.extend(x for x in expanded if x not in paths)
            elif p not in paths:
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
    **W1151 根修（WinError 206）**：巨批（全站 INLINED 副本同步 851 页）单条 `git add`
    命令行超 Windows CreateProcess 32767 字符上限 ⇒ FileNotFoundError 直接炸链
    ⇒ 分块 add（git add 暂存区跨调用累积·结果与单条等价）。
    """
    exist = [p for p in paths if os.path.exists(os.path.join(ROOT, p))]
    missing = [p for p in paths if p not in exist]
    if missing:
        print('[add] 跳过 %d 个尚不存在的路径（尚未创建·如报告件未落盘）：%s'
              % (len(missing), '、'.join(missing[:5])))
    if not exist:
        print('[add] 无待 add 路径（spec.file_index_rows 为空？请用 --paths 显式指定）')
        return True
    chunk = 200
    total = (len(exist) + chunk - 1) // chunk
    for i in range(0, len(exist), chunk):
        rc, out = run(['git', 'add', '--'] + exist[i:i + chunk])
        if rc != 0:
            print('[add] git add 失败（块 %d/%d）=> 中止：' % (i // chunk + 1, total)
                  + out.strip()[-400:])
            return False
    print('[add] 已 add %d 件（%d 块·防 WinError 206）' % (len(exist), total))
    return True


def _changed_py_files():
    """本批改动的 .py 清单：**三态并集**（索引态 + 工作树态 + 未跟踪）。

    为什么要三态：① 索引态 = 已暂存（add 步之后本批改动都在里面）；② 工作树态 =
    「改了就忘 add」的件；③ 未跟踪 = 新建但既未 add 也未 commit 的件
    （ls-files --others --exclude-standard 已排除 .gitignore 目录如 tmpe/）。
    只取 .py；非 .py 一律跳过（零成本）。
    """
    paths = set()
    for args in (['diff', '--cached', '--name-only'],
                 ['diff', '--name-only'],
                 ['ls-files', '--others', '--exclude-standard']):
        rc, out = run(['git', '-c', 'core.quotePath=false'] + args)
        if rc != 0:
            continue
        for ln in out.splitlines():
            p = ln.strip()
            if p.endswith('.py'):
                paths.add(p)
    return sorted(paths)


def _compile_check(rel_paths, root=None):
    """纯逻辑：逐件编译给定 .py 路径 ⇒ 返回 (ok, 错误清单)。

    非 .py 一律跳过（零成本）；只编译不落盘（不产生 __pycache__）。
    抽成独立函数以便单测直接喂临时文件（不依赖 git 仓库）。
    """
    base = root or ROOT
    bad = []
    checked = 0
    for rel in rel_paths:
        if not rel.endswith('.py'):
            continue
        checked += 1
        path = os.path.join(base, rel)
        try:
            with open(path, 'rb') as fh:
                src = fh.read()
            compile(src, rel, 'exec')
        except SyntaxError as exc:
            bad.append('%s:%s: %s' % (rel, exc.lineno, exc.msg))
        except OSError as exc:
            bad.append('%s: 读取失败: %s' % (rel, exc))
    return (not bad), bad, checked


def _run_pycompile():
    """py_compile 语法自检（W1128）：把「写盘出错」这类事故挡在提交之前。

    病根（2026-11-04 实测）：批量写 .py 后若落盘出现语法错（字面两字符反斜杠 n、
    缺引号、续行残缺），此前**无任何机器门禁拦截** ⇒ 坏文件直接进索引进提交；
    而本地跑的是好版本 ⇒ 本地全绿、提交里是坏版本 ⇒ 直到 CI 才暴露（本次 8 个
    文件同时触发 3 个 job 红灯）。

    ⇒ 本步对三态清单的全部 .py 逐件 compile()（**只编译不落盘**·不污染
    __pycache__），任一件 SyntaxError ⇒ 打印「文件:行号 + 错误」并**中止整条收官链**
    （fail-closed·宁可停在收官前也不让坏件进提交）。
    """
    files = _changed_py_files()
    if not files:
        print('[pycompile] 本批无 .py 改动（跳过）')
        return True
    ok, bad, _checked = _compile_check(files)
    if not ok:
        print('[pycompile] 发现 %d 件 .py 语法错 => 中止（先修语法再收官）' % len(bad))
        for b in bad:
            print('  ' + b)
        return False
    print('[pycompile] %d 件 .py 语法自检通过' % len(files))
    return True


def _run_index():
    """index 步：文档索引 + 搜索索引 + sitemap。"""
    # W1154（基础设施审计 §4-3）：index 步补 gen_sitemap——新增页面批次此前靠第 7 槽报红后手工补；幂等生成随批入库
    # W1216 根修（E-230 同族）：内部序对调为 docs_index 在前——搜索索引内嵌 docs/INDEX.md
    # 派生字段（「doc | docs/ 文档索引」），原序（搜索在前）遇新增文档批必留陈旧内嵌 ⇒
    # 第 46 槽 C2/C3 轮流补红（W1216 实测：复盘新篇即触发）。
    for cmd in ('docs_index.py', '_gen_search_index.py', 'gen_sitemap.py'):
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
        # W1155（深度审计 #14）：建闸后 208 份 spec 仅 1 份声明 ⇒ 文案数字漂移零判据。
        # 全量强制需历史 spec 逐份补声明（另批）——本批起前向要求：未声明打印 NOTE
        # 显性化（此前是静默跳过）·新 spec 由收官链自动带 doc_numbers 声明模板。
        print('[docnums] NOTE spec 无 doc_numbers 声明（W1155 起前向要求新批声明·'
              '历史 spec 另批补齐）——本批文案数字无对表闸')
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


def _run_refresh_artifacts(dry=False):
    """刷新入库产物（两口径探针 + 渲染复核两态）并纳入暂存（W1297·L-01 治本）。

    病根（git 历史实证）：版本面推进**每批改 4 个页面页脚各 1 行** ⇒ 页面 sha 必变 ⇒
    入库的探针报告 / 渲染档案**每批必过期** ⇒ 第 80/82 槽的 fail-closed 新鲜度检测必然判红
    （W1292→W1296 连续五批实证·此前每批靠人记得重跑）⇒ 固化进收官链 = 治本。

    位置：versions 之后（页脚定稿后）、index 之前；自带 add（产物须入暂存）。
    dry-run 时跳过（不跑浏览器·保持链的 dry 语义）。

    代价（诚实登记）：本步需跑两个浏览器探针 + 渲染复核（本地约 20 分钟）⇒
    收官链时长增加，但换掉「每批一次陈旧红灯 + 一轮返工 CI」（约 20 分钟）。
    """
    if dry:
        print("[refresh-artifacts] dry-run ⇒ 跳过（不跑浏览器）")
        return True
    import subprocess
    import sys
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    node = "node"
    py = sys.executable
    steps = [
        ("graphic 口径探针",
         [node, "scripts/svg_text_contrast_probe.js", "--bg-mode", "graphic", "--scope", "all",
          "--out", "scripts/output/svg_text_contrast_graphic_report.json"]),
        ("body 口径探针",
         [node, "scripts/svg_text_contrast_probe.js", "--bg-mode", "body", "--scope", "data,en",
          "--out", "scripts/output/svg_text_contrast_report.json"]),
        ("渲染复核（豁免页模式）", [py, "scripts/output/_w1266_render_legend.py"]),
        ("渲染复核（--all 全量）", [py, "scripts/output/_w1266_render_legend.py", "--all"]),
    ]
    for name, cmd in steps:
        print("[refresh-artifacts] %s ..." % name)
        try:
            r = subprocess.run(cmd, cwd=root)
        except Exception as exc:  # noqa: BLE001 — 采集异常须显式留痕
            print("[refresh-artifacts] FAIL %s（%r）" % (name, exc))
            return False
        if r.returncode != 0:
            print("[refresh-artifacts] FAIL %s（rc=%s）" % (name, r.returncode))
            return False
    artifacts = [
        "scripts/output/svg_text_contrast_graphic_report.json",
        "scripts/output/svg_text_contrast_report.json",
        "scripts/output/chart-legend-render-audit.json",
        "scripts/output/chart-legend-render-audit.md",
        "scripts/output/_w1266_allrender.json",
    ]
    r = subprocess.run(["git", "add", "--"] + artifacts, cwd=root)
    if r.returncode != 0:
        print("[refresh-artifacts] FAIL 产物入暂存（rc=%s）" % r.returncode)
        return False
    for chk in ("scripts/check_svg_text_contrast.py", "scripts/check_chart_content_completeness.py"):
        r = subprocess.run([py, chk], cwd=root, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode != 0:
            print("[refresh-artifacts] FAIL 新鲜度校验 %s（rc=%s）" % (chk, r.returncode))
            print((r.stdout or "")[-600:])
            return False
    print("[refresh-artifacts] PASS 产物已刷新并入暂存 + 新鲜度校验绿")
    return True



# ===== 台账 hash 回填：共享纯函数（v1/v2 共用·W1308 结构档拆分） =====


def _ledger_rows(lines):
    """台账正文数据行 → [(W 号, 单元格列表)]（非数据行跳过）。纯函数。"""
    import re as _re
    out = []
    for line in lines:
        m = _re.match(r"^\|\s*W(\d{3,4})\s*\|", line)
        if not m:
            continue
        out.append((int(m.group(1)),
                    [c.strip() for c in line.strip().strip("|").split("|")]))
    return out


def _status_cell(cells):
    """定位状态列 → (下标, 是否已收官)；未找到 ⇒ (None, False)。纯函数。

    W1298：状态列滞后（已推提交但状态列未翻「已收官」）也纳入回填面（hash 是机械事实）
    ⇒ 但**不自动翻状态列**（避免把真未完成的批次标成已收官）⇒ 仅打印 WARN 提示人工翻。
    """
    import re as _re
    for i, c in enumerate(cells):
        if _re.match(r"^(?:\*\*)?(?:已收官|已闭环|已合并)", c):
            return i, True
        if _re.match(r"^在途", c):
            return i, False
    return None, False


def _hash_col_index(cells, status_idx):
    """hash 列下标 = 状态列 -2（台账列序约定）；越界 ⇒ None。纯函数。"""
    h_idx = status_idx - 2
    if h_idx < 0 or h_idx >= len(cells):
        return None
    return h_idx


def _git_w_map_v1(root):
    """v1 口径：git log --all --reverse --format=%h %s → {W 号: 短 hash}。

    注意：--all **含不在 main 历史链上的提交** ⇒ v2 改用 HEAD 口径（见 _git_w_map_v2）。
    """
    import re as _re
    import subprocess as _sp
    gl = _sp.run(["git", "-C", root, "log", "--all", "--reverse", "--format=%h %s"],
                 capture_output=True, text=True, encoding="utf-8", errors="replace")
    subjects = gl.stdout.splitlines()
    _pat = _re.compile(r"^(?:[0-9a-f]{7,12}\s+)?[a-z0-9._-]+\(([^)]*)\):", _re.I)
    _pat2 = _re.compile(r"^(?:[0-9a-f]{7,12}\s+)?[a-z0-9._-]+(?:\([^)]*\))?:\s*w(\d{3,4})\b", _re.I)
    by_w = {}
    for line in subjects:
        w = None
        m = _pat.match(line)
        if m:
            for part in m.group(1).split(","):
                tok = part.strip()
                if _re.match(r"^w\d{3,4}$", tok, _re.I):
                    w = int(tok[1:])
                    break
        if w is None:
            m2 = _pat2.match(line)
            if m2:
                w = int(m2.group(1))
        if w is not None and w not in by_w:
            by_w[w] = line.split(" ", 1)[0]
    return by_w


def _git_w_map_v2(root):
    """v2 口径：只取 HEAD 历史链 → ({W 号: 全 sha}, 祖先 sha 集合)。

    L-11 根修：候选源必须是**当前历史链**（--all 会把已失效 commit 再次写回台账）。
    """
    import subprocess as _sp
    gl = _sp.run(["git", "-C", root, "log", "--reverse", "--format=%H %s", "HEAD"],
                 capture_output=True, text=True, encoding="utf-8", errors="replace")
    subjects = gl.stdout.splitlines()
    rl = _sp.run(["git", "-C", root, "rev-list", "HEAD"],
                 capture_output=True, text=True, encoding="utf-8", errors="replace")
    ancestors = set(rl.stdout.split())
    by_w = {}
    for line in subjects:
        parts = line.split(" ", 1)
        sha = parts[0]
        subject = parts[1] if len(parts) > 1 else ""
        for w in _parse_subject_w_ids(subject):
            if w not in by_w:
                by_w[w] = sha
    return by_w, ancestors


def _apply_backfill(root, todo, dry):
    """执行回填（todo 元素 = (w, sha, closed[, kind])）——v1/v2 共用。

    W1318 根修：子进程改走本模块 `run()`（可注入面）——原 `_sp.run` 直连绕过单测
    mock ⇒ `bc.main()` 的单测会真实执行 ledger_backfill.py 并回填本仓台账
    （W1315 连带发现/W1317 实证：每跑一次 pytest 就多一笔幽灵台账改动）。
    """
    for item in todo:
        w, sha, closed = item[0], item[1], item[2]
        kind = item[3] if len(item) > 3 else "回填"
        if dry:
            print("[backfill-prev-hash] dry-run ⇒ 跳过 W%d（%s·%s）" % (w, sha, kind))
            continue
        if not closed:
            print("[backfill-prev-hash] WARN W%d 状态列仍非「已收官」⇒ 已%s hash（%s）但状态列须人工翻"
                  % (w, kind, sha))
        rc, out = run([sys.executable, os.path.join(root, "scripts", "ledger_backfill.py"),
                       "--w", str(w), "--hash", sha], cwd=root)
        if rc != 0:
            print("[backfill-prev-hash] WARN ledger_backfill W%d 失败（rc=%d）：%s"
                  % (w, rc, out.strip()[:200]))
        else:
            print("[backfill-prev-hash] %s W%d ⇒ %s" % (kind, w, sha))


def _run_backfill_prev_hash(dry=False):
    """自动回填台账「已收官但 hash 列空缺」的行（W1298·L-03·v1 保留可回退）。

    背景（物理约束·不可消除）：提交内容含自身 hash ⇒ 同笔内写不对自己的 hash
    ⇒ 台账 hash 列**每批必然欠一笔回填**（E-311 纪律：hash 由下一批的第一动作回填）⇒
    此前靠**人工**记着做 ⇒ 常态化漏 ⇒ 本步把它**机器化**：收官链开头自动回填。

    取值口径：hash 列语义 = **该批最早一笔**（首笔）⇒ 用 git log --reverse 取首个批次标签提交。
    状态列**不动**（只用 --hash，不传 --status）⇒ 详细终态结论不丢（W1289 教训）。
    W1308：函数体拆分（共享纯函数 helpers）⇒ ruff 结构档复杂度/分支数回落（原 24/23 超限）。
    """
    import re as _re
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ledger = os.path.join(root, "docs", "00-导读", "W批次编号对账表.md")
    if not os.path.exists(ledger):
        print("[backfill-prev-hash] 台账不存在 ⇒ 跳过")
        return True
    with open(ledger, encoding="utf-8", newline="") as fh:
        lines = fh.read().split("\n")
    try:
        by_w = _git_w_map_v1(root)
    except Exception as exc:  # noqa: BLE001
        print("[backfill-prev-hash] git 读取失败 ⇒ 跳过（%r）" % exc)
        return True
    todo = []
    for w, cells in _ledger_rows(lines):
        if w not in by_w:
            continue
        idx, closed = _status_cell(cells)
        if idx is None:
            continue
        h_idx = _hash_col_index(cells, idx)
        if h_idx is None:
            continue
        h = cells[h_idx]
        if h and not (h.startswith("—") or h.startswith("-") or "待回填" in h or h in ("—", "")):
            continue
        # 内容锚点复核：hash 列应是短 hex / 占位形态 ⇒ 否则列定位可能错位（同表多形态·防误写列）
        if not (_re.match(r"^[0-9a-f]{7,12}$", h) or h.startswith("—") or h.startswith("-")
                or "待回填" in h or h == ""):
            print("[backfill-prev-hash] WARN W%d 的 hash 列形态异常（%r）⇒ 跳过（防列错位）" % (w, h))
            continue
        todo.append((w, by_w[w], closed))
    if not todo:
        print("[backfill-prev-hash] 无需回填（无「已收官 + hash 空缺」行）")
        return True
    _apply_backfill(root, todo, dry)
    return True


def _run_content_stage(a, batch):
    # W1298（L-03）：自动回填台账「已收官但 hash 空缺」的行——提交含自身 hash ⇒ 同笔内写不对
    #   自己的 hash ⇒ **每批必然欠一笔回填**（E-311 纪律）⇒ 此前靠人工记着做 ⇒ 常态化漏
    #   ⇒ 此处机器化（只用 --hash·不动状态列 ⇒ 终态结论不丢·W1289 教训）。
    if not _run_backfill_prev_hash_v2(dry=getattr(a, "dry_run", False), batch=batch):
        return False
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
    # W1297（L-01 治本）：版本面推进每批改 4 个页面页脚各 1 行 ⇒ 入库的探针报告 + 渲染档案
    #   **每批必过期** ⇒ 第 80/82 槽的 fail-closed 新鲜度检测必然判红（W1292→W1296 连续五批实证·
    #   此前每批靠人记得重跑）⇒ 此处固化刷新步（自带 add）⇒ 收官后入库产物必然新鲜。
    if not _run_refresh_artifacts(dry=getattr(a, "dry_run", False)):
        return False
    return _run_index()


def _run_finalize(a, batch):
    """链尾段（W1215 抽函数控 main 复杂度）：docnums → regsurface → csp → cspcheck → gate。"""
    if not _run_docnums(a.spec):
        return False
    if not _run_regsurface(batch):
        return False
    if not _run_csp(a.spec):
        return False
    if not _run_cspcheck():
        return False
    return _run_gate(getattr(a, 'skip_gate', False))


def main(argv=None):
    ap = argparse.ArgumentParser(description='落段收官一键脚本')
    ap.add_argument('--spec', help='本批 spec json 路径')
    ap.add_argument('--batch', help='批号（缺省从 spec 读）')
    ap.add_argument('--paths', nargs='*', default=[], help='额外需 add 的路径')
    ap.add_argument('--steps', action='store_true', help='只打印执行顺序')
    ap.add_argument('--dry-run', action='store_true', help='只做预检不落盘')
    ap.add_argument('--skip-gate', action='store_true',
                    help='跳过链尾 pre_push_gate 真全量（W1215·迭代期用·提交前须单跑）')
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
    if not _run_cascade(a.spec, batch, dry=a.dry_run):
        return 1
    if not _run_archive(dry=a.dry_run):
        return 1
    if not _run_rebuild(a.spec, batch, dry=a.dry_run):
        return 1
    if not _run_prechecks(led):
        return 1
    if a.dry_run:
        print('[dry-run] 预检通过，未落盘（cascade/archive/rebuild 均以 dry 模式运行）')
        return 0
    if not _add_paths(collect_paths(a.spec, a.paths)):
        return 1
    if not _run_pycompile():
        return 1
    if not _run_content_stage(a, batch):
        return 1
    if not _run_finalize(a, batch):
        return 1
    print('---- 收官链完成：顺序 ' + ' -> '.join(step_order()) + ' ----')
    return 0


# ===== W1308 · L-11：台账 hash 回填扩到「错值修指」（在链上口径 + 排除本批 + 悬空改指） =====


def _parse_subject_w_ids(line):
    """从一行 git log 输出解析其涉及的批次号（合并推送的 subject 含多个 W 号 ⇒ **全取**）。

    纯函数·W1308 可单测。口径：
      · scope 段（type(scope): …）内的 W 号优先（W1234/W1235 形态）；
      · 其次 subject 中出现的 W 号字样（W1303 W1302 W1301 合并推送形态）。
    """
    import re as _re
    ids = set()
    m = _re.match(r"^(?:[0-9a-f]{7,12}\s+)?[a-z0-9._-]+\(([^)]*)\):", line, _re.I)
    if m:
        for part in m.group(1).split(","):
            tok = part.strip()
            if _re.match(r"^w\d{3,4}$", tok, _re.I):
                ids.add(int(tok[1:]))
    if not ids:
        for mm in _re.finditer(r"\bW(\d{3,4})\b", line, _re.I):
            ids.add(int(mm.group(1)))
    return ids


def _prefix_sets(ancestors):
    """由全量 sha 集合构造「短 hash 前缀 → 是否可达」的查表器（一次遍历·O(1) 判定）。"""
    cache = {}

    def probe(short):
        length = len(short)
        if length not in cache:
            cache[length] = {a[:length] for a in ancestors}
        return short.lower() in cache[length]

    return probe


def _hash_action(cell, first_sha, probe, current_batch, w):
    """决定台账某行 hash 格的动作。

    纯函数·W1308 可单测。返回：
      ('skip',  None)      —— 该格不是可判定的 hash（占位/形态异常/列错位）
      ('keep',  None)      —— hash 有效且**在链上**（不动）
      ('fill',  first_sha) —— hash 空缺 ⇒ 回填该批链上首笔
      ('repair', first_sha)—— hash 非空但**不在链上**（被压缩/改写）⇒ 改指链上首笔
    """
    import re as _re
    h = (cell or "").strip()
    placeholder = (not h) or h.startswith("—") or h.startswith("-") or "待回填" in h
    if placeholder:
        if first_sha:
            return ("fill", first_sha)
        return ("skip", None)
    if not _re.match(r"^[0-9a-f]{7,12}$", h):
        return ("skip", None)
    if probe(h):
        return ("keep", None)
    if first_sha:
        return ("repair", first_sha)
    return ("skip", None)


def _run_backfill_prev_hash_v2(dry=False, batch=None):
    """台账 hash 回填 v2（W1308·L-11）：空缺回填 + **错值修指** + **排除本批**。

    L-11 病根（W1306 实测）：v1 的候选来源是 git log --all ⇒ **含不在 main 历史链上的提交**
    ⇒ 压缩推送后会把「已失效的 hash」再次写回台账 ⇒ 悬空引用复发。
    v2 三处口径变更：
      ① 候选来源改 HEAD（**只在当前历史链上取**）⇒ 承载 commit 必可达；
      ② subject 含**多个 W 号**时全部登记（合并推送形态）⇒ 逐批可得承载 commit；
      ③ **排除本批**（自指不可知 ⇒ 本批 hash 必留空待下一批）⇒ 避免「回填本批 → 随后 amend ⇒ 立即悬空」。
    另加：hash 非空但**不在链上** ⇒ 改指该批链上首笔（错值修指）。
    状态列**不动**（只用 --hash·不动终态结论·W1289 教训）。
    W1308：函数体拆分（共享纯函数 helpers）⇒ ruff 结构档复杂度/分支数回落（原 23/22 超限）。
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ledger = os.path.join(root, "docs", "00-导读", "W批次编号对账表.md")
    if not os.path.exists(ledger):
        print("[backfill-prev-hash] 台账不存在 ⇒ 跳过")
        return True
    with open(ledger, encoding="utf-8", newline="") as fh:
        lines = fh.read().split("\n")
    try:
        by_w, ancestors = _git_w_map_v2(root)
    except Exception as exc:  # noqa: BLE001
        print("[backfill-prev-hash] git 读取失败 ⇒ 跳过（%r）" % exc)
        return True
    probe = _prefix_sets(ancestors)
    cur = None
    if batch:
        try:
            cur = int(str(batch).lstrip("Ww"))
        except ValueError:
            cur = None
    todo = []
    for w, cells in _ledger_rows(lines):
        if cur is not None and w == cur:
            continue                      # ③ 排除本批（自指不可知）
        if w not in by_w:
            continue
        idx, closed = _status_cell(cells)
        if idx is None:
            continue
        h_idx = _hash_col_index(cells, idx)
        if h_idx is None:
            continue
        action, sha = _hash_action(cells[h_idx], by_w[w], probe, cur, w)
        if action == "fill":
            todo.append((w, sha, closed, "回填"))
        elif action == "repair":
            todo.append((w, sha, closed, "错值修指"))
    if not todo:
        print("[backfill-prev-hash] 无需回填/修指（无空缺或悬空行）")
        return True
    _apply_backfill(root, todo, dry)
    return True


if __name__ == '__main__':
    sys.exit(main())
