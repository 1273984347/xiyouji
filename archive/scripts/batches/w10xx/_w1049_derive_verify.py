# -*- coding: utf-8 -*-
"""_w1049_derive_verify.py — 由 W1043 批验收脚本程序化派生 W1049 批验收脚本

派生纪律：程序化派生 + 残留断言（禁手抄改常量·坑表「派生脚本残留断言」）。

本批与 W1043 的两处口径差异（以替换表达）：
  ① 覆盖数：55 → 67 回（12 回全部新增题图·无「只换 og」例外回）
  ② 缺口：45 → 33 回（其中通用 og 43 → 31 回 + 既有 card-* 专属 2 回）

用法：py -3 archive/scripts/batches/w10xx/_w1049_derive_verify.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "_w1043_verify.py")
DST = os.path.join(HERE, "_w1049_verify.py")

JOBS = [
    ("ch016", "plate-line-97-ch016-jinchi-zhanglao.webp"),
    ("ch039", "plate-line-98-ch039-wenshu-pusa.webp"),
    ("ch046", "plate-line-99-ch046-luli-daxian.webp"),
    ("ch050", "plate-line-100-ch050-huode-xingjun.webp"),
    ("ch055", "plate-line-101-ch055-nvguo-guowang.webp"),
    ("ch084", "plate-line-102-ch084-miefo-guowang.webp"),
    ("ch005", "plate-line-103-ch005-sida-tianwang.webp"),
    ("ch018", "plate-line-104-ch018-gao-taigong.webp"),
    ("ch032", "plate-line-105-ch032-yinjiao-dawang.webp"),
    ("ch056", "plate-line-106-ch056-shidai-yanjun.webp"),
    ("ch067", "plate-line-107-ch067-honglin-damang.webp"),
    ("ch058", "plate-line-108-ch058-diting.webp"),
]

REPL = [
    # 标题与说明
    ('_w1043_verify.py — W1043 落位验收', '_w1049_verify.py — W1049 落位验收'),
    ('用法：py -3 scripts/_w1043_verify.py', '用法：py -3 archive/scripts/batches/w10xx/_w1049_verify.py'),
    ('④ 缺口复算：100 回中已有配图 44→55 回、缺口 56→45 回',
     '④ 缺口复算：100 回中已有配图 55→67 回、缺口 45→33 回'),
    ('⑤ **未覆盖页未回归**：其余 45 页的 og:image 仍为落位前的取值（43 通用图 + 2 张既有 card-* 专属）',
     '⑤ **未覆盖页未回归**：其余 88 页的 og:image 仍为落位前的取值（31 通用图 + 2 张既有 card-* 专属 + 55 回已落位专属）'),
    # 覆盖/缺口期望值
    ('if len(covered) != 55:\n        fails.append("有配图回数 %d ≠ 55（期望 44+11·ch086 已有旧题图只换 og）" % len(covered))',
     'if len(covered) != 67:\n        fails.append("有配图回数 %d ≠ 67（期望 55+12·本批 12 回全部新增题图）" % len(covered))'),
    ('if len(gap) != 45:\n        fails.append("缺口 %d ≠ 45" % len(gap))',
     'if len(gap) != 33:\n        fails.append("缺口 %d ≠ 33" % len(gap))'),
    ('if len(generic) != 43:\n        fails.append("缺口中通用 og 页 %d ≠ 43" % len(generic))',
     'if len(generic) != 31:\n        fails.append("缺口中通用 og 页 %d ≠ 31" % len(generic))'),
    # W1043 的「ch086 已有旧题图⇒本批只换 og」例外段：本批 12 回实读均无任何配图
    # ⇒ 例外不存在，注释与 PREEXISTING 声明一并改写
    ('# W1043：ch086 已有 W1001 批旧题图（plate-line-70-...-bichandawang）⇒ 本批**只换 og**·\n'
     '# 题图不覆盖（该回已有一张·同页两题图不被落位脚本支持）⇒ 断言对该回放宽。',
     '# W1049：本批 12 个目标回实读均无任何配图（`_w1049_pick_verify.py` ① 项判据）\n'
     '# ⇒ 无「已有旧题图只换 og」的例外回，PREEXISTING 为空集。'),
    # 收尾 print 的批次号
    ('---- W1043 落位验收：%d FAIL · %d NOTE ----', '---- W1049 落位验收：%d FAIL · %d NOTE ----'),
    # 判据沿用说明：上一批修正的「暗色隐藏规则用容忍空白正则」本批继续沿用（不改判据本身）
    ('# W1043：原判据用**整串字面量**匹配 ⇒ 页面 CSS 为多行排版时误判「缺暗色隐藏规则」\n'
     '# （实测 ch090 等 8 页明明含该规则却被判红）⇒ 改为容忍空白的正则（坑表 puti-shouye 第 5 条：\n'
     '#   判据禁止依赖脆弱特征）',
     '# 沿用上一批修正：原判据用**整串字面量**匹配 ⇒ 页面 CSS 为多行排版时误判「缺暗色隐藏规则」\n'
     '# ⇒ 改为容忍空白的正则（坑表 puti-shouye 第 5 条：判据禁止依赖脆弱特征）\n'
     '# 本批不修改该判据·仅继承'),
    # 落位前快照用于未覆盖页零回归
]

# 注：JOBS 块整块替换（见 derive()）⇒ 无需也不应单独删除其中某一行
# （旧版曾先删末行导致 `]` 形态被改·后续块匹配失配）。


def derive() -> str:
    src = open(SRC, encoding="utf-8").read()
    out = src
    for old, new in REPL:
        if old not in out:
            raise SystemExit("派生锚点失配：%r" % old[:70])
        out = out.replace(old, new)

    # 替换 JOBS 块（`]` 可能跟在最后一行元素后·不保证单独成行）
    m = re.search(r"^JOBS = \[.*?^\]", out, re.S | re.M)
    if not m:
        raise SystemExit("派生锚点失配：未找到 JOBS 块")
    lines = ["JOBS = ["]
    for ch, site_name in JOBS:
        lines.append('    (%r, %r),' % (ch, site_name))
    lines.append("]")
    out = out[:m.start()] + "\n".join(lines) + out[m.end():]

    # 本批无「已有旧题图」例外回
    out = out.replace(
        'PREEXISTING = {"ch086"}',
        "PREEXISTING = set()  # W1049：本批 12 回实读均无任何配图⇒无例外回")

    # 残留断言
    for bad in ("_w1043", "ch086", "plate-line-85", "plate-line-96", "W1043"):
        if bad in out:
            raise SystemExit("残留断言失败：产物仍含 %r" % bad)
    return out


def main() -> int:
    if not os.path.exists(DST):
        text = derive()
        tmp = DST + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        os.replace(tmp, DST)
        print("派生写出：%s" % os.path.relpath(DST, os.getcwd()))
    else:
        print("已存在，跳过派生：%s" % os.path.relpath(DST, os.getcwd()))
    ns = {"__name__": "__main__", "__file__": DST}
    try:
        exec(compile(open(DST, encoding="utf-8").read(), DST, "exec"), ns)
    except SystemExit as e:
        return e.code or 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
