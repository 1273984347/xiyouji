#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w857_plan_template_review.py — 计划方案对《任务计划、执行与经验沉淀系统提示词》模板的符合性复核探针

用途：对 docs/11-方案报告/计划方案/ 下的 8 份文档，按模板（用户 2026-10-21 23:44 提供）
逐项判定 32 项结构判据 + 「计划件 + 报告件」配对并集的 §12 十项覆盖，输出结构化矩阵。

用法：
    py -3 scripts/_w857_plan_template_review.py                          # 打印矩阵
    py -3 scripts/_w857_plan_template_review.py --json <out.json>        # 落盘 JSON

判据口径（机械判定，可复算）：
  · 字段类判据：把该章要求的表头字段拆成 token，逐 token 在全文做命中检查。
  · 件型分判：模板 §12 要求「一份报告含十项」，仓内惯例拆成《执行前计划》+《任务计划执行与经验沉淀报告》两件
    → §5.1~§5.9 判计划件，§6/§7/§8/§12 判报告件，不适用项判 N/A（不计不符合）。
  · 配对并集：另判「计划件 + 报告件」合并后是否覆盖 §12 十项（真正的符合性口径）。
  · 编号类判据：统计 G-/AC-/ASM-/ST-/D-/R-/V-/E-/P-/A-/WF-/SC-/PRE- 前缀去重计数。
  · 模糊词判据：按模板 §10 的 11 个禁词逐词计数；排除三类非违规行——引用模板替换表的行、
    以 '>' 开头的引用块、文档自身的「模糊词」自检行。
  · 结论：本探针只判「结构在不在」，不判语义质量；语义抽查由人工做（复核记录见 W857 报告）。

一次性诊断件·不入 CI。
"""
import argparse
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN_DIR = os.path.join(ROOT, 'docs', '11-方案报告', '计划方案')

# ---- 模板结构要求（§4 输出格式 / §5 执行前计划 / §6 执行记录 / §7 验收自评 / §8 经验 / §12 交付物）----
# (判据编号, 模板出处, 要求说明, 必现 token 列表)
CRITERIA = [
    ('C01', '§4.2', '目录', ['目录']),
    ('C02', '§4.2', '执行摘要', ['执行摘要']),
    ('C03', '§4.2', '附录', ['附录']),
    ('C04', '§5.1', '任务标识·任务编号', ['任务编号']),
    ('C05', '§5.1', '任务标识·任务名称', ['任务名称']),
    ('C06', '§5.1', '任务标识·任务来源', ['任务来源']),
    ('C07', '§5.1', '任务标识·任务类型', ['任务类型']),
    ('C08', '§5.1', '任务标识·创建时间', ['创建时间']),
    ('C09', '§5.1', '任务标识·计划版本', ['计划版本']),
    ('C10', '§5.1', '任务标识·负责人', ['负责人']),
    ('C11', '§5.1', '任务标识·验收人', ['验收人']),
    ('C12', '§5.2', '目标与完成标准', ['任务目标', '完成标准']),
    ('C13', '§5.2', '不完成定义', ['不完成定义']),
    ('C14', '§5.3', '范围与边界·做什么/不做什么', ['做什么', '不做什么']),
    ('C15', '§5.3', '范围与边界·输入/输出/依赖', ['输入', '输出', '依赖']),
    ('C16', '§5.4', '信息基础与假设·ASM 表', ['ASM-', '影响范围', '验证方法', '验证责任人', '验证时间']),
    ('C17', '§5.5', '执行步骤·ST 表', ['ST-', '动作', '输出物', '验收标准', '失败处理', '证据位置']),
    ('C18', '§5.5', '执行步骤·工具命令与耗时', ['工具/命令', '预计耗时']),
    ('C19', '§5.6', '量化指标·V 表', ['V-', '计算公式', '目标值', '数据来源', '预警规则']),
    ('C20', '§5.7', '风险·R 表', ['R-', '触发条件', '概率', '缓解措施', '备选方案', '监控指标']),
    ('C21', '§5.8', '决策记录·D 表', ['D-', '备选方案', '选择方案', '选择理由', '权衡', '可复用结论']),
    ('C22', '§5.9', '自包含检查（12 项逐项）', ['自包含']),
    ('C23', '§6', '执行记录·ST 状态/偏差/修正', ['执行记录', '偏差']),
    ('C24', '§7.1', '验收表·AC', ['AC-', '验收项', '实际结果', '结论', '整改措施']),
    ('C25', '§7.2', '可行性自评·A 表', ['A-', '可行性', '实施风险', '依赖条件', '自评结论']),
    ('C26', '§7.2', '总体自评结论', ['总体自评结论']),
    ('C27', '§8', '经验沉淀·E 表', ['E-', '适用场景与边界', '量化效果', '证据来源', '可迁移性']),
    ('C28', '§12', '最终交付物·风险与偏差记录', ['风险与偏差']),
    ('C29', '§12', '最终交付物·决策记录与理由', ['决策记录']),
    ('C30', '§12', '最终交付物·经验沉淀', ['经验沉淀']),
    ('C31', '§12', '最终交付物·方案可行性自评', ['可行性自评']),
    ('C32', '§4.4', '每章结论与待确认事项（等效形式亦计）', ['本章结论', '待确认事项']),
]

# 模板 §12 要求「一份报告含十项」；仓内惯例把它拆成《执行前计划》+《任务计划执行与经验沉淀报告》两件落库。
# 故按件型分判：
#   计划件（PLAN）  承载 §5.1~§5.9（计划本体）
#   报告件（REPORT） 承载 §6 执行记录 / §7 验收与自评 / §8 经验沉淀 / §12 落项（执行侧）
# 两件之外的判据判 N/A（不计不符合）；真正的问题是「配对并集是否覆盖 §12 十项」→ 由 pair_check 单独判定。
PLAN_ONLY = {'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11',
             'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22'}
REPORT_ONLY = {'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31'}

# 配对并集需覆盖的 §12 十项（用于 pair_check）
PAIRS = [
    ('T01', '执行前计划-T01.md', 'T01-任务计划执行与经验沉淀报告-2026-10-14.md'),
    ('T03', '执行前计划-T03-全项目审查第一批修复.md', 'T03-任务计划执行与经验沉淀报告-2026-10-20.md'),
    ('T04', '执行前计划-T04-站内阅读入口打通与阅读页体验封装.md', 'T04-任务计划执行与经验沉淀报告-2026-10-21.md'),
]
# §12 十项 → 判据映射（用于并集覆盖判定）
PAIRS_UNION = [
    ('执行摘要', ['C02']),
    ('信息基础与假设', ['C16']),
    ('执行前计划', ['C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13',
                    'C14', 'C15', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22']),
    ('执行记录', ['C23']),
    ('验收证据', ['C24']),
    ('风险与偏差记录', ['C20', 'C28']),
    ('决策记录与理由', ['C21', 'C29']),
    ('经验沉淀', ['C27', 'C30']),
    ('方案可行性自评', ['C25', 'C26', 'C31']),
    ('附录', ['C03']),
]

# 「本章结论 / 待确认事项」的等效形式（仓内实际写法）
CONCL_EQUIV = ['本章结论', '本章小结', '本节结论', '小结', '本批不做', '不做项', '不做']
PENDING_EQUIV = ['待确认事项', '待验证', '待用户', '待批准', '待决']
# 「执行摘要」的等效形式（计划件多用「0. 任务背景（读者无需回看会话即可理解）」承担同一职能）
SUMMARY_EQUIV = ['执行摘要', '任务背景', '本批针对', '一页速览', '速览', '摘要', '核心判定']

NUM_PREFIXES = ['G-', 'AC-', 'ASM-', 'ST-', 'D-', 'R-', 'V-', 'E-', 'P-', 'A-', 'WF-', 'SC-', 'PRE-']

BANNED = ['大概', '可能', '较好', '差不多', '尽快', '尽量', '合理', '适当', '优化一下', '详细', '及时']
# 引用模板替换表/正文的行不计违规（避免自指假红）
QUOTE_HINT = ('模糊表述', '必须替换为', '模糊词替换', '替换为')


def load(path):
    return io.open(path, encoding='utf-8').read()


def in_table_row(line, token):
    """token 出现在以 | 开头的行（表格行/表头）里"""
    if '|' not in line:
        return False
    return token in line


def hit_any(lines, token, table_only=False):
    for ln in lines:
        if token in ln:
            if not table_only or in_table_row(ln, token):
                return True
    return False


def count_prefix(text, pfx):
    return len(set(re.findall(re.escape(pfx) + r'(\d{2})', text)))


def banned_hits(lines):
    """返回 {词: 命中行数}，排除：① 引用模板替换表的行 ② 引用块（以 > 开头）③ 文档自身的「模糊词」自检行"""
    out = {w: 0 for w in BANNED}
    ctx = []
    for i, ln in enumerate(lines, 1):
        if any(h in ln for h in QUOTE_HINT):
            continue
        if ln.strip().startswith('>'):
            continue
        if '模糊词' in ln:
            continue
        for w in BANNED:
            if w in ln:
                out[w] += ln.count(w)
                ctx.append((i, w, ln.strip()[:110]))
    return ({w: n for w, n in out.items() if n}, ctx)


def detect_kind(text, name):
    """件型判定（内容优先·文件名兜底）。

    W860 实证的坑：仓内存在「审查 + 计划」双合一报告（文件名带「任务计划执行与经验沉淀报告」
    却内含完整 §5.1~§5.9 计划半边）——若只按文件名判 REPORT，计划半边永不被判（假绿口子）。
    故按内容判定：计划特征 = 有 §5.x 小节标题或「任务标识」；报告特征 = 有执行记录 / 验收证据 /
    可行性自评 / 经验沉淀等章节。
    """
    heads = re.findall(r'^#{1,4}\s*(.+)$', text, re.M)
    # 报告半边只看「章节标题」不看正文提及——纯计划件常在自检表/证据列里提到「验收证据」「经验沉淀」，
    # 那是引用不是章节（实证：执行前计划-T03 正文出现「经验沉淀」6 次但无该章节）。
    report_head = [h for h in heads
                   if any(k in h for k in ('验收证据', '可行性自评', '经验沉淀', '风险与偏差'))]
    has_plan = ('执行前计划' in name
                or re.search(r'^#{1,4}\s*5\.[1-9]', text, re.M) is not None
                or '任务标识' in text)
    has_report = ('任务计划执行与经验沉淀报告' in name) or bool(report_head)
    if has_plan and has_report:
        return 'BOTH'
    if has_plan:
        return 'PLAN'
    return 'REPORT'


def judge(text, name='<text>'):
    """纯函数判据：按件型分流判 32 项结构判据，返回判据判定表。

    供两处复用：① 本探针的全量矩阵输出；② 第 48 门禁 scripts/check_plan_template.py
    （门禁取其「不符合项集合」做增量差集）。

    返回：{'kind': 'PLAN'|'REPORT'|'BOTH', 'criteria': {cid: {...}}}
    """
    lines = text.splitlines()
    kind = detect_kind(text, name)
    out = {}
    for cid, src, desc, tokens in CRITERIA:
        if (cid in PLAN_ONLY and kind == 'REPORT') or (cid in REPORT_ONLY and kind == 'PLAN'):
            out[cid] = {'src': src, 'desc': desc, 'present': None, 'need': len(tokens),
                        'missing': [], 'verdict': 'N/A', 'note': '按件型不适用'}
            continue
        if cid == 'C02':
            # 执行摘要：认等效形式（计划件用「0. 任务背景」承担同一职能）
            hit = [t for t in SUMMARY_EQUIV if hit_any(lines, t)]
            out[cid] = {
                'src': src, 'desc': desc,
                'present': 1 if hit else 0, 'need': 1,
                'missing': [] if hit else ['执行摘要'],
                'verdict': '符合' if hit else '不符合',
                'note': '等价形式命中：%s' % ('、'.join(hit) or '无'),
            }
            continue
        if cid == 'C32':
            concl = [t for t in CONCL_EQUIV if hit_any(lines, t)]
            pend = [t for t in PENDING_EQUIV if hit_any(lines, t)]
            miss = []
            if not concl:
                miss.append('本章结论')
            if not pend:
                miss.append('待确认事项')
            out[cid] = {
                'src': src, 'desc': desc,
                'present': (2 - len(miss)), 'need': 2, 'missing': miss,
                'verdict': '符合' if not miss else '部分符合',
                'note': '等价形式命中：%s / %s' % ('、'.join(concl) or '无', '、'.join(pend) or '无'),
            }
            continue
        missing = [t for t in tokens if not hit_any(lines, t)]
        out[cid] = {
            'src': src, 'desc': desc,
            'present': len(tokens) - len(missing), 'need': len(tokens),
            'missing': missing,
            'verdict': '符合' if not missing else ('部分符合' if len(missing) < len(tokens) else '不符合'),
        }
    return {'kind': kind, 'criteria': out}


def fail_set(judged):
    """取「不符合」判据的集合（部分符合不计——内容多在，只判「整项缺失」为硬失格）。"""
    return set(cid for cid, v in judged['criteria'].items() if v['verdict'] == '不符合')


def review(path):
    text = load(path)
    lines = text.splitlines()
    name = os.path.basename(path)
    judged = judge(text, name)
    res = {'file': name, 'kind': judged['kind'], 'bytes': len(text.encode('utf-8')),
           'lines': len(lines), 'criteria': judged['criteria'], 'numbers': {}, 'banned': {}, 'banned_ctx': []}
    for p in NUM_PREFIXES:
        res['numbers'][p.rstrip('-')] = count_prefix(text, p)
    res['banned'], res['banned_ctx'] = banned_hits(lines)
    res['banned_total'] = sum(res['banned'].values())
    # 章结论覆盖：统计 '## ' 级标题数 vs 结论标记数
    h2 = len([l for l in lines if re.match(r'^##\s+\S', l)])
    res['chapters'] = {'h2': h2, 'conclusion_marks': text.count('本章结论'),
                       'pending_marks': text.count('待确认事项')}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', default=None, help='落盘 JSON 路径')
    args = ap.parse_args()

    files = sorted(f for f in os.listdir(PLAN_DIR) if f.endswith('.md') and f != 'README.md')
    results = [review(os.path.join(PLAN_DIR, f)) for f in files]

    # 文本矩阵
    hdr = ['文件', '行数', '字节', '符合', '部分', '不符合', '编号种类', '模糊词命中', '章结论覆盖']
    print('| ' + ' | '.join(hdr) + ' |')
    print('|' + '---|' * len(hdr))
    for r in results:
        c = r['criteria']
        ok = sum(1 for v in c.values() if v['verdict'] == '符合')
        part = sum(1 for v in c.values() if v['verdict'] == '部分符合')
        bad = sum(1 for v in c.values() if v['verdict'] == '不符合')
        kinds = sum(1 for n in r['numbers'].values() if n > 0)
        cc = r['chapters']
        print('| %s | %d | %d | %d | %d | %d | %d/13 | %d | %d/%d 章 |' % (
            r['file'], r['lines'], r['bytes'], ok, part, bad, kinds, r['banned_total'],
            cc['conclusion_marks'], cc['h2']))

    print('\n=== 逐判据缺口（仅列部分符合/不符合）===')
    for r in results:
        for cid, v in sorted(r['criteria'].items()):
            if v['verdict'] != '符合':
                print('| %s | %s | %s | 缺: %s |' % (r['file'], cid, v['desc'], '、'.join(v['missing'])))

    print('\n=== 编号覆盖（去重编号个数）===')
    for r in results:
        print('| %s | %s |' % (r['file'], ' '.join('%s:%d' % (k, v) for k, v in r['numbers'].items() if v)))

    print('\n=== 模糊词命中（排除模板替换表引用行）===')
    for r in results:
        if r['banned']:
            print('| %s | %s |' % (r['file'], ' '.join('%s×%d' % (k, v) for k, v in r['banned'].items())))

    print('\n=== 模糊词命中上下文（供人工判定真伪）===')
    for r in results:
        for c in r['banned_ctx'][:8]:
            print('| %s:%d | %s | %s |' % (r['file'], c[0], c[1], c[2]))

    print('\n=== C32 等效形式明细 ===')
    for r in results:
        v = r['criteria']['C32']
        print('| %s | %s | %s |' % (r['file'], v['verdict'], v.get('note', '')))

    print('\n=== 配对并集（模板 §12 十项 · 计划件 + 报告件 合并判定）===')
    for p in pair_check(results):
        if 'error' in p:
            print('| %s | %s |' % (p['tag'], p['error']))
            continue
        print('| %s | %s + %s | 十项全符合 %d/%d |' % (p['tag'], p['plan'], p['report'], p['full'], p['need']))
        for it in p['items']:
            print('   | %-16s | %-6s | %d/%d 判据全符合（部分符合 %d） |' % (
                it['item'], it['verdict'], it['ok'], it['need'], it['partial']))

    if args.json:
        io.open(args.json, 'w', encoding='utf-8', newline='').write(
            json.dumps({'docs': results, 'pairs': pair_check(results)}, ensure_ascii=False, indent=1))
        print('\nJSON -> %s' % args.json)
    return 0


def pair_check(results):
    """配对并集：模板 §12 十项在「计划件 + 报告件」两件合并后的覆盖情况"""
    by_file = {r['file']: r for r in results}
    out = []
    for tag, plan_f, rep_f in PAIRS:
        plan = by_file.get(plan_f)
        rep = by_file.get(rep_f)
        if not plan or not rep:
            out.append({'tag': tag, 'plan': plan_f, 'report': rep_f, 'error': '件缺失'})
            continue
        merged = {}
        for cid, v in plan['criteria'].items():
            if v['verdict'] != 'N/A':
                merged[cid] = v
        for cid, v in rep['criteria'].items():
            if v['verdict'] != 'N/A':
                merged[cid] = v
        items = []
        for name, cids in PAIRS_UNION:
            got = [c for c in cids if c in merged and merged[c]['verdict'] == '符合']
            partial = [c for c in cids if c in merged and merged[c]['verdict'] == '部分符合']
            items.append({'item': name, 'ok': len(got), 'need': len(cids),
                          'partial': len(partial),
                          'verdict': '符合' if len(got) == len(cids) else ('部分符合' if got or partial else '不符合')})
        full = sum(1 for i in items if i['verdict'] == '符合')
        out.append({'tag': tag, 'plan': plan_f, 'report': rep_f, 'items': items,
                    'full': full, 'need': len(items)})
    return out


if __name__ == '__main__':
    sys.exit(main())
