#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_plan_template.py — 第 48 门禁：计划方案模板符合性（增量口径·W860）

判据：`docs/11-方案报告/计划方案/*.md` 对《任务计划、执行与经验沉淀系统提示词（AI Agent 专用版）》
的结构符合性。判据表（32 项结构判据 + 件型分流 + 等效形式识别 + 自指/引文排除）复用
`scripts/_w857_plan_template_review.py`，本脚本只做**增量判定**与**门禁协议**。

增量口径（避免存量 8 份不合规文档一上线即全红）：
  · 新增文件（HEAD 无此路径）：全部适用判据须符合 → 任一「不符合」判红；
  · 修改文件：取 HEAD 版本同判据求差集 → 仅「本次引入的新不符合项」判红；存量不符合项只提示（NOTE）；
  · 未变更文件：不看（存量豁免）。
  · 「部分符合」不计硬失格（内容多在，只判「整项缺失」）。

用法：
  py -3 scripts/check_plan_template.py --gate       # 门禁模式：退出码 0/1 + 汇总行（末行）
  py -3 scripts/check_plan_template.py --self-test  # 负样本自证（5 例纯逻辑 + 1 例 git 端到端）

门禁挂载：scripts/verify_delivery.py 第 48 槽（_StrictGate·crash 即拦 + 汇总行防静默跳过）。
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _w857_plan_template_review as R  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN_REL = 'docs/11-方案报告/计划方案'
MARKER = '---- 第 48 门禁 计划方案合规：'


def _git(args, cwd=ROOT):
    return subprocess.run(['git'] + args, cwd=cwd, capture_output=True, text=True,
                          errors='replace', timeout=60)


def changed_plan_files():
    """本次变更涉及的 计划方案/*.md（暂存 + 未暂存 + 未跟踪；-z 防中文路径被八进制转义）"""
    r = _git(['status', '--porcelain', '-z', '--', PLAN_REL])
    if r.returncode != 0:
        return []
    out = []
    for rec in r.stdout.split('\0'):
        if not rec.strip():
            continue
        # 形如 "XY path"：前 2 字符为状态位，其后为路径（-z 模式不加引号）
        path = rec[3:].strip()
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
        if path.endswith('.md') and '计划方案' in path:
            out.append(path)
    return sorted(set(out))


def head_text(path):
    """HEAD 版本内容；None = 该路径在 HEAD 不存在（新增文件）"""
    r = _git(['show', 'HEAD:' + path])
    if r.returncode != 0:
        return None
    return r.stdout


def judge_file(rel_path):
    """返回 (verdict, detail_dict)：verdict ∈ {'PASS','FAIL'}；detail 含新增缺项与存量缺项"""
    full = os.path.join(ROOT, rel_path)
    try:
        new_text = R.io.open(full, encoding='utf-8').read()
    except OSError as e:
        return 'FAIL', {'error': '读取失败：%s' % e, 'new_fail': [], 'old_fail': []}
    name = os.path.basename(rel_path)
    judged_new = R.judge(new_text, name)
    new_fail = R.fail_set(judged_new)
    old_text = head_text(rel_path)
    if old_text is None:
        return ('FAIL' if new_fail else 'PASS'), {
            'is_new': True, 'new_fail': sorted(new_fail), 'old_fail': [],
            'detail': {cid: judged_new['criteria'][cid]['desc'] for cid in sorted(new_fail)},
        }
    judged_old = R.judge(old_text, name)
    old_fail = R.fail_set(judged_old)
    introduced = new_fail - old_fail
    remaining = new_fail & old_fail
    return ('FAIL' if introduced else 'PASS'), {
        'is_new': False, 'new_fail': sorted(introduced), 'old_fail': sorted(remaining),
        'detail': {cid: judged_new['criteria'][cid]['desc'] for cid in sorted(introduced)},
    }


def run_gate():
    files = changed_plan_files()
    fails = 0
    notes = 0
    lines = []
    for rel in files:
        verdict, d = judge_file(rel)
        if d.get('error'):
            fails += 1
            lines.append('  FAIL %s：%s' % (rel, d['error']))
            continue
        if verdict == 'FAIL':
            fails += 1
            for cid in d['new_fail']:
                lines.append('  FAIL %s：%s（%s）' % (rel, cid, d['detail'].get(cid, '')))
        else:
            lines.append('  PASS %s%s' % (rel, '（新增文件·全项符合）' if d['is_new'] else ''))
        if d['old_fail']:
            notes += len(d['old_fail'])
            lines.append('  NOTE %s：存量不符合项 %d 项（不判红·存量豁免）：%s'
                         % (rel, len(d['old_fail']), '、'.join(d['old_fail'])))
    for l in lines:
        print(l)
    print('%s%d FAIL / %d 文件（存量缺项 %d 项仅提示）'
          % (MARKER, fails, len(files), notes))
    return 1 if fails else 0


# ---------------- 负样本自证 ----------------
GOOD = """# T-XX《执行前计划》— 自证样本

## 目录
- 摘要

## 0. 任务背景（读者无需回看会话即可理解）
一句话交代本批针对的问题。

## 5.1 任务标识
| 字段 | 内容 |
|---|---|
| 任务编号 | T-XX |
| 任务名称 | 自证样本 |
| 任务来源 | 自证 |
| 任务类型 | 分析 |
| 创建时间 | 2026-10-22 00:00 |
| 计划版本 | V1.0 |
| 负责人 | MCode |
| 验收人 | 用户 |

## 5.2 目标与完成标准
**G-01 目标**：任务目标一句话。
**完成标准**：AC-01 可判据。
**不完成定义**：① 无产出。

## 5.3 范围与边界
| 类型 | 内容 |
|---|---|
| 做什么 | 做什么 |
| 不做什么 | 不做什么 |
| 输入 | 输入 |
| 输出 | 输出 |
| 依赖 | 依赖 |
| 权限 | 权限 |
| 环境 | 环境 |
| 版本 | 版本 |
| 合规要求 | 合规要求 |

## 5.4 信息基础与假设
| 编号 | 类型 | 内容 | 影响范围 | 验证方法 | 验证责任人 | 验证时间 | 状态 |
|---|---|---|---|---|---|---|---|
| ASM-01 | 事实 | 内容 | 范围 | 方法 | MCode | 2026-10-22 | 已确认 |

## 5.5 执行步骤
| 步骤编号 | 动作 | 输入 | 工具/命令及参数 | 输出物 | 验收标准 | 预计耗时 | 失败处理 | 状态 | 证据位置 |
|---|---|---|---|---|---|---|---|---|---|
| ST-01 | 动作 | 输入 | `cmd` | 输出物 | 判据 | 1 分钟 | 回滚 | 未开始 | 证据 |

## 5.6 量化指标与追踪看板
| 指标编号 | 指标名称 | 计算公式 | 目标值 | 统计周期 | 数据来源 | 当前值 | 状态 | 预警规则 |
|---|---|---|---|---|---|---|---|---|
| V-01 | 指标 | 公式 | 目标 | 每日 | 来源 | 0 | 进行中 | 超阈报警 |

## 5.7 风险与备选
| 风险编号 | 风险描述 | 触发条件 | 影响 | 概率 | 缓解措施 | 备选方案 | 责任人 | 监控指标 |
|---|---|---|---|---|---|---|---|---|
| R-01 | 风险 | 触发 | 影响 | 低 | 缓解 | 备选 | MCode | V-01 |

## 5.8 决策记录与理由
| 决策编号 | 决策事项 | 备选方案 | 选择方案 | 选择理由 | 依据 | 权衡 | 影响 | 可复用结论 |
|---|---|---|---|---|---|---|---|---|
| D-01 | 事项 | 备选 | 选择 | 理由 | 依据 | 权衡 | 影响 | 结论 |

## 5.9 自包含检查
| # | 检查项 | 结果 | 说明 |
|---|---|---|---|
| 1 | 目标是否可验证 | ✅ | 量化 |

## 附录 A：数据表
表格。
"""

BAD = GOOD.replace('## 5.7 风险与备选', '## 5.7 风险') \
           .replace('## 5.8 决策记录与理由', '## 5.8 决策') \
           .replace('## 5.9 自包含检查', '## 5.9 检查') \
           .replace('## 附录 A：数据表\n表格。\n', '')


def self_test():
    """5 例纯逻辑 + 1 例 git 端到端。返回 0 全过。"""
    cases = []

    def add(name, cond, detail=''):
        cases.append((name, bool(cond), detail))

    # ① 新增文件且合规 → 无不符合项
    g = R.judge(GOOD, '执行前计划-TXX.md')
    add('① 新增·合规文件 → 无不符合项', not R.fail_set(g), 'fail_set=%s' % sorted(R.fail_set(g)))
    # ② 新增文件缺整项（§5.7/§5.8/§5.9 标题与表头被删）→ 必判红
    b = R.judge(BAD, '执行前计划-TXX.md')
    add('② 新增·缺项文件 → 必判红', bool(R.fail_set(b)), 'fail_set=%s' % sorted(R.fail_set(b)))
    # ③ 存量不合规 → 只改别处 → 差集为空（不误判）
    add('③ 存量缺项 + 仅改别处 → 差集为空（不误判红）',
        not (R.fail_set(b) - R.fail_set(b)), '')
    # ④ 存量合规 → 改出缺项 → 差集非空（必红）
    add('④ 存量合规 → 改出缺项 → 差集非空（必红）',
        bool(R.fail_set(b) - R.fail_set(g)), 'diff=%s' % sorted(R.fail_set(b) - R.fail_set(g)))
    # ⑤ 存量不合规 → 补齐（GOOD 比 BAD 不再缺项）→ 差集为空（恢复必绿）
    add('⑤ 存量缺项 → 补齐 → 差集为空（恢复必绿）',
        not (R.fail_set(g) - R.fail_set(b)), 'diff=%s' % sorted(R.fail_set(g) - R.fail_set(b)))

    # ⑥ git 端到端：造一个未跟踪的缺项文件 → 变更集命中且判红 → 删除后不再命中
    tmp_rel = PLAN_REL + '/_self_test_tmp_probe.md'
    tmp_abs = os.path.join(ROOT, tmp_rel)
    try:
        with open(tmp_abs, 'w', encoding='utf-8') as f:
            f.write(BAD)
        files = changed_plan_files()
        hit = tmp_rel in files or any(f.endswith('_self_test_tmp_probe.md') for f in files)
        verdict, d = judge_file(tmp_rel) if hit else ('FAIL', {'error': '未进入变更集'})
        add('⑥ 端到端：未跟踪缺项文件 → 进变更集且判红',
            hit and verdict == 'FAIL' and bool(d.get('new_fail')),
            'hit=%s verdict=%s' % (hit, verdict))
    finally:
        if os.path.exists(tmp_abs):
            os.remove(tmp_abs)
    after = changed_plan_files()
    add('⑦ 端到端：清理后不再命中', not any('T_tmp_probe' in f or '_self_test_tmp_probe' in f for f in after),
        'after=%s' % after)

    ok = True
    for name, passed, detail in cases:
        print('  %s %s%s' % ('PASS' if passed else 'FAIL', name, ('  [%s]' % detail) if detail else ''))
        ok = ok and passed
    print('SELF_TEST_%s（%d/%d 例通过）' % ('OK' if ok else 'FAIL', sum(1 for _, p, _ in cases if p), len(cases)))
    return 0 if ok else 1


def main():
    args = sys.argv[1:]
    if '--self-test' in args:
        return self_test()
    if '--gate' in args:
        return run_gate()
    print(__doc__)
    print('用法: --gate | --self-test')
    return 0


if __name__ == '__main__':
    sys.exit(main())
