#!/usr/bin/env python3
"""一次性：A 轨 §6「延伸核验注记」5 组散引号片段处置（2026-09-28·第二批）。

依据：数据核验与复现报告-A轨驿递稿-2026-09-28.md §6（已裁决处置：逐字化或去引号）。
投稿版 + 匿名稿同改，带断言（每串须恰 1 处命中，否则拒写）。

  Q1 §5.2 三处描述性引号（74/84/91 回·底本无连续串）→ 去引号（保留回目括注）
  Q2 §4.4 两处 → 逐字化：改「摇头摇手只叫："谨言！"」「直到被三藏扯住，"定要问个详细"」
  Q3 §4.1「入城先投馆驿」→ 去引号
  Q4 §4.3 第二落点「入城先投馆驿」→ 去引号（顺文补顿：之前，入城先投馆驿的程序仍在）
  Q5 §4.3「驿丞启奏、国王用印」→ 去引号

用法：py scripts/_s4a_quotes_fix.py [--check|--apply]（默认 --check 只读核查）
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
S4 = ROOT / "docs" / "S4-学术投稿"
A = S4 / "学术论文-西游记驿递交通书写的数字人文研究.md"
A_ANON = S4 / "学术论文-西游记驿递交通书写的数字人文研究-匿名稿.md"

REPLACEMENTS = [
    ("Q1", '——狮驼国"大鹏占城，文牒无处可验"（第 74 回）是制度被妖力击穿，灭法国"剃发改名混出"（第 84 回）是制度被暴政扭曲，金平府"观灯被掳"（第 91 回）是制度被欲望悬置。',
           '——狮驼国大鹏占城，文牒无处可验（第 74 回）是制度被妖力击穿，灭法国剃发改名混出（第 84 回）是制度被暴政扭曲，金平府观灯被掳（第 91 回）是制度被欲望悬置。'),
    ("Q2", '他"摇头摇手只叫：谨言"，直到被"扯住定要问个详细"，才',
           '他摇头摇手只叫："谨言！"，直到被三藏扯住，"定要问个详细"，才'),
    ("Q3", '亦沿"入城先投馆驿"的程序而行', '亦沿入城先投馆驿的程序而行'),
    ("Q4", '之前先"入城先投馆驿"的程序仍在', '之前，入城先投馆驿的程序仍在'),
    ("Q5", '须"驿丞启奏、国王用印"', '须驿丞启奏、国王用印'),
]


def process(path, apply):
    text = path.read_text(encoding="utf-8")
    ok = True
    for tag, old, new in REPLACEMENTS:
        n = text.count(old)
        print("  %s[%s] count=%d" % ("OK " if n == 1 else "!! ", tag, n))
        if n != 1:
            ok = False
        if n >= 1 and apply:
            text = text.replace(old, new)
    if apply and ok:
        path.write_text(text, encoding="utf-8")
        print("  -> 已写入 %s" % path.name)
    return ok


def main():
    apply = "--apply" in sys.argv
    print("== 模式：%s ==" % ("APPLY（写盘）" if apply else "CHECK（只读）"))
    all_ok = True
    for p in (A, A_ANON):
        print("#" * 20, p.name)
        all_ok &= process(p, apply)
    if not apply:
        print("== 残留扫描：--check 模式跳过（旧串仍在属预期，写盘后复核）==")
        print("== 结果：%s ==" % ("全部断言通过" if all_ok else "存在计数不符"))
        return 0 if all_ok else 1
    print("== 残留扫描（写盘后）==")
    for p in (A, A_ANON):
        t = p.read_text(encoding="utf-8")
        for k in ('"大鹏占城', '"剃发改名混出"', '"观灯被掳"', '"摇头摇手只叫：谨言"',
                  '"扯住定要问个详细"', '"入城先投馆驿"', '"驿丞启奏、国王用印"'):
            if k in t:
                all_ok = False
                print("  !! %s 残留 %s" % (p.name[:14], k))
        print("  [%s] 旧引号串残留：%s" % (p.name[:14],
              "无" if not any(k in t for k in ('"大鹏占城', '"剃发改名混出"', '"观灯被掳"',
                                              '"摇头摇手只叫：谨言"', '"扯住定要问个详细"',
                                              '"入城先投馆驿"', '"驿丞启奏、国王用印"')) else "有"))
    print("== 结果：%s ==" % ("全部断言通过" if all_ok else "存在计数不符/残留"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())