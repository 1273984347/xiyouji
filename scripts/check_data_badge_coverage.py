"""check_data_badge_coverage.py — 第 66 门禁 · 数据徽标覆盖（W1167 · MVP 迁移批③）

背景：audit-6=fetch 回退时透明度不一致（旧「数据源：」行 11 种口径含 EMBEDDED 行话，
1 页完全缺失）。本批以 scripts/w1167_badge_inject.py 为正本对 88 页统一三态徽标，
本槽判据化 story-2 AC1（覆盖 100%）+ AC3（读者语言）+ AC4（离线恒在=静态 HTML 结构属性）。

判据（同源引用正本 STATUS_TEXT/classify，不复制）：
  B1 每页含 DATA-STATUS-BADGE MARK 恰一次（_shell.html 豁免）
  B2 data-status ∈ {live,snapshot,sample} 且 == 正本 classify 结果（防页面手改态）
  B3 ds-label 与正本 STATUS_TEXT[status] 逐字一致（防行话回潮，如 EMBEDDED）
退出码：0 / 1 / 2（fail-closed）。恒跑（_SCOPE_CORE·毫秒级）。
用法：py scripts/check_data_badge_coverage.py [--report] [--self-test]
"""
import importlib.util
import io
import re
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "site/data"
MARKER = "---- 第 66 门禁 数据徽标："
SKIP = {"_shell.html"}

# 结构判据按「属性集合」识别，不按「属性顺序 + 恰好这两个属性」：正本给徽标加属性
# （W1168 的 `data-goatcounter-view` 曝光面）不该把 88 页全判成「破损」——同族老坑见第 65 槽
# 「取 it[0] 不解包」，判据必须抗正本的字段增扩。
BADGE = re.compile(r'<div\b[^>]*class="[^"]*\bdata-status-badge\b[^"]*"[^>]*>.*?</div>', re.S)
STATUS = re.compile(r'\bdata-status="(live|snapshot|sample)"')
LABEL = re.compile(r'<span class="ds-label">([^<]+)</span>')


def _load_truth():
    spec = importlib.util.spec_from_file_location("badgetruth", Path(__file__).with_name("w1167_badge_inject.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_page(mod, name: str, txt: str):
    errs = []
    n = txt.count(mod.MARK)
    if n != 1:
        return [f"徽标 MARK 出现 {n} 次（应恰 1）"]
    m = BADGE.search(txt)
    if not m:
        return ["有 MARK 无徽标结构（破损）"]
    st = STATUS.search(m.group(0))
    if not st:
        return ["徽标结构内无合法 data-status（破损）"]
    status = st.group(1)
    want = mod.classify(name)
    if status != want:
        errs.append(f"data-status={status} ≠ 正本 classify={want}")
    lab = LABEL.search(m.group(0))
    if not lab or lab.group(1) != mod.STATUS_TEXT[status][0]:
        errs.append(f"ds-label 与正本文案不符（防行话回潮）：{lab.group(1) if lab else None!r}")
    return errs


def self_test(mod):
    good = mod.build_badge("snapshot")
    cases = [
        ("正样本-规范", "any.html", good, 0),
        ("负样本-缺徽标", "any.html", "<p>裸页</p>", 1),
        ("负样本-态越界", "any.html", good.replace('data-status="snapshot"', 'data-status="magic"'), 1),
        ("负样本-行话回潮", "any.html", good.replace("内嵌快照", "EMBEDDED"), 1),
        ("负样本-live误标", "any.html", mod.build_badge("live"), 1),  # any.html 正本=snapshot
    ]
    fails = 0
    for name, fn, txt, expect in cases:
        errs = check_page(mod, fn, txt)
        got = 1 if errs else 0
        if got != expect:
            fails += 1
            print(f"  [WRONG] {name}: got={got} expect={expect} {errs}")
        else:
            print(f"  [OK] {name}")
    print(f"自测 {'PASS' if fails == 0 else 'FAIL'}（{len(cases)} 例）")
    return 0 if fails == 0 else 1


def main():
    try:
        mod = _load_truth()
    except Exception as e:
        print(f"{MARKER}基础设施缺失（正本模块不可读）: {e}")
        sys.exit(2)
    files = [f for f in sorted(DATA.glob("*.html")) if f.name not in SKIP]
    viol = []
    for f in files:
        errs = check_page(mod, f.name, f.read_text(encoding="utf-8", errors="replace"))
        if errs:
            viol.append((f.name, errs))
    verdict = "OK" if not viol else "FAIL"
    print(f"{MARKER}页面 {len(files)} · 违规 {len(viol)} · {verdict}")
    for name, errs in viol[:15]:
        for e in errs:
            print(f"  ✗ {name}: {e}")
    sys.exit(1 if viol and "--report" not in sys.argv else 0)


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test(_load_truth()))
    main()
