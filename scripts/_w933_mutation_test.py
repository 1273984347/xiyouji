#!/usr/bin/env python3
"""_w933_mutation_test.py — W933 三个新判据的**可证伪性**验证（反向验证）

做法：把被测脚本复制到隔离目录 → 文本替换注入故障（变异）→ 跑被测脚本 →
      检查「该判据原本会判红的地方，变异后不再红」。

三条纪律（缺一条就可能把无效变异当成"测试有效"）：
  ① 变异前断言 `old in original`（目标串存在）；
  ② 变异后断言 `mutated != original` 且 `old not in mutated`（**替换真的发生了**，
     且打在了目标点——同名串在别处先命中会静默放过，见 W931 M11 实证）；
  ③ 每条都配「基线未变异 ⇒ 仍会红/自测仍通过」的对照组。

用法：py -3 scripts/_w933_mutation_test.py
退出码：0=全部按预期；1=有判据在变异后仍红（即该判据形同虚设）或基线异常。
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUT = os.path.join(ROOT, "tmpe", "_w933_mut")  # tmpe/ 为仓内既定临时区（gitignored·W771 先例）
PY = sys.executable


def read(p: str) -> str:
    """读文本并**统一换行为 \\n**——仓内文件为 CRLF（autocrlf），若保留原换行，
    目标串（以 \\n 书写）将永远匹配不上（判据 A 首跑即踩：变异目标串「不存在」）。"""
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p: str, s: str) -> None:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def mutate(src: str, dst: str, old: str, new: str) -> str:
    """复制并注入变异；返回变异后的文本。**三条断言齐全才允许继续**。"""
    text = read(src)
    if old not in text:
        raise SystemExit("ABORT: 变异目标串不存在：%r" % old[:70])
    mutated = text.replace(old, new, 1)
    if mutated == text:
        raise SystemExit("ABORT: 变异未生效（内容无变化）")
    if old in mutated:
        raise SystemExit("ABORT: 变异未打准（原串仍在·可能命中多处）")
    write(dst, mutated)
    return mutated


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def case_preflight_A():
    """判据 A（撞号检测·同号多行）：变异掉重复检测 ⇒ 原本报红的重复号不再被检出。

    注：W935 修订前，本判据语义是「登记后出现更晚登记号 ⇒ FAIL」；实战证明该语义会
    误伤**后补登记**（先落地者保留下的合法情形）⇒ 修订为「同号多行 = 撞号」+ 插队仅 NOTE。
    """
    src = os.path.join(ROOT, "scripts", "preflight_check.py")
    dst = os.path.join(MUT, "preflight_mut.py")
    old = "    return sorted(w for w, n in seen.items() if n > 1)\n"
    new = "    return []  # MUTATION: 同号多行检测被移除\n"
    mutate(src, dst, old, new)
    rows = "[{'w': 933}, {'w': 933}, {'w': 934}]"

    def probe(mod: str, path: str):
        code = ("import sys;sys.path.insert(0, %r);import %s as p;"
                "print(p.duplicate_wnums(%s))" % (path, mod, rows))
        return run([PY, "-c", code])

    _, base_out = probe("preflight_check", os.path.join(ROOT, "scripts"))
    _, mut_out = probe("preflight_mut", MUT)
    base_hit = "933" in base_out
    mut_hit = "933" in mut_out
    print("  基线（原脚本）检出同号多行 = %s ⇒ %s" % (base_hit, base_out.strip()[:60]))
    print("  变异（去重复检测）检出同号多行 = %s ⇒ %s" % (mut_hit, mut_out.strip()[:60]))
    return base_hit and (not mut_hit)

def case_backfill_B() -> bool:
    """判据 B（回填独占·基线指纹校验）：变异掉 expect 校验 ⇒ 自测的负例不再红。"""
    src = os.path.join(ROOT, "scripts", "ledger_backfill.py")
    dst = os.path.join(MUT, "ledger_backfill_mut.py")
    old = ('    if args.expect and args.expect != old_fp:\n'
           '        print("FAIL  基线指纹不符：--expect %s·实得 %s ⇒ 你读到的行已过期（他方已改）"\n'
           '              % (args.expect, old_fp))\n'
           '        print("      处理：重读该行 → 确认他方改动内容 → 再回填")\n'
           '        return 1\n')
    new = ('    if args.expect and args.expect != old_fp:\n'
           '        pass  # MUTATION: 基线指纹校验被移除\n')
    mutate(src, dst, old, new)
    base_rc, base_out = run([PY, src, "--self-test"])
    mut_rc, mut_out = run([PY, dst, "--self-test"])
    base_ok = base_rc == 0
    mut_ok = mut_rc == 0
    print("  基线（原脚本）自测通过 = %s" % base_ok)
    print("  变异（去 expect 校验）自测通过 = %s ⇒ %s" % (mut_ok, mut_out.strip().splitlines()[-1] if mut_out.strip() else ""))
    return base_ok and (not mut_ok)


def case_close_check_C() -> bool:
    """判据 C（收官回填自检）：变异掉 hash 占位检查 ⇒ 自测的负例不再红。"""
    src = os.path.join(ROOT, "scripts", "ledger_close_check.py")
    dst = os.path.join(MUT, "ledger_close_check_mut.py")
    # 依赖件同目录复制：否则变异副本 import ledger_backfill 失败而崩溃
    # ⇒ 「变异体崩了」会被误读成「判据被移除」（假阳性·W933 首跑实证）
    shutil.copy(os.path.join(ROOT, "scripts", "ledger_backfill.py"),
                os.path.join(MUT, "ledger_backfill.py"))
    old = ('        if RE_HASH_PLACEHOLDER.search(h.strip()):\n'
           '            results.append({"w": w, "ok": False, "why": "hash 列仍是占位：「%s」" % h})\n'
           '            continue\n')
    new = ('        if False:  # MUTATION: hash 占位检查被移除\n'
           '            pass\n')
    mutate(src, dst, old, new)
    base_rc, base_out = run([PY, src, "--self-test"])
    mut_rc, mut_out = run([PY, dst, "--self-test"])
    base_ok = base_rc == 0
    mut_ok = mut_rc == 0
    print("  基线（原脚本）自测通过 = %s" % base_ok)
    print("  变异（去 hash 占位检查）自测通过 = %s ⇒ %s" % (mut_ok, mut_out.strip().splitlines()[-1] if mut_out.strip() else ""))
    return base_ok and (not mut_ok)


def case_backtick_D():
    """判据 D（反引号剥离·W934 架构会话实测报出）：台账 touches 列的路径**带反引号**，
    且反引号内用「/」并列多文件 ⇒ 旧实现整段当一个 token ⇒ 与命令行无反引号路径
    字面不等 ⇒ touches 交集检查**假绿**（真实撞面却报「无交集」）。"""
    src = os.path.join(ROOT, "scripts", "preflight_check.py")
    dst = os.path.join(MUT, "preflight_backtick_mut.py")
    old = ('        if ch == "`":\n'
           '            flush()              # 反引号段切换前先收尾外层内容\n'
           '            in_code = not in_code\n'
           '            continue\n')
    new = ('        if ch == "`":\n'
           '            pass  # MUTATION: 反引号段解析被移除\n')
    mutate(src, dst, old, new)
    sample = "`docs/00-导读/W批次编号对账表.md`（本行）· `a.py` / `b.py`"

    def probe(mod: str, path: str) -> tuple[int, str]:
        code = ("import sys;sys.path.insert(0, %r);import %s as p;"
                "print(sorted(p._split_touches(%r)))" % (path, mod, sample))
        return run([PY, "-c", code])

    def ok(out: str) -> bool:
        return ("docs/00-导读/W批次编号对账表.md" in out and "a.py" in out
                and "b.py" in out and "`" not in out)

    _, base_out = probe("preflight_check", os.path.join(ROOT, "scripts"))
    _, mut_out = probe("preflight_backtick_mut", MUT)
    base_ok, mut_ok = ok(base_out), ok(mut_out)
    print("  基线（原脚本）反引号解析正确 = %s ⇒ %s" % (base_ok, base_out.strip()[:120]))
    print("  变异（去反引号解析）解析正确 = %s ⇒ %s" % (mut_ok, mut_out.strip()[:120]))
    return base_ok and (not mut_ok)


def main() -> int:
    if os.path.isdir(MUT):
        shutil.rmtree(MUT)
    os.makedirs(MUT, exist_ok=True)
    print("== W933 三判据可证伪性验证 ==")
    results = []
    for name, fn in (("判据A 乐观并发取号", case_preflight_A),
                     ("判据B 回填独占·行指纹", case_backfill_B),
                     ("判据C 收官回填自检", case_close_check_C),
                     ("判据D 反引号剥离·touches 假绿", case_backtick_D)):
        try:
            ok = fn()
        except SystemExit as exc:
            print("  FAIL %s：%s" % (name, exc))
            ok = False
        results.append((name, ok))
        print("  → %s %s" % ("OK  " if ok else "FAIL", name))
    shutil.rmtree(MUT, ignore_errors=True)
    bad = [n for n, ok in results if not ok]
    print()
    if bad:
        print("突变测试：%d/%d 项未按预期（%s）" % (len(bad), len(results), bad))
        return 1
    print("突变测试：%d/%d 项按预期（判据可证伪）" % (len(results), len(results)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
