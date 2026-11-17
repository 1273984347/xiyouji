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

扫描面（W1266 批二线 C 三轮扩面）：site/data + **site 根页** + site/en。
  原实现只扫 site/data ⇒ EN 138 页零徽标（W1265 批一已补）· ZH 根页 9 页零徽标
  （本轮补）。根页曾零覆盖 ⇒ 「该页无徽标」是**扫描面盲区**而非合规证据。
  根页形态与 ZH data 页同款（ds-label 逐字取正本中文文案·防行话回潮）。
  _template.html（骨架模板）跳过·_shell.html 跳过——模板不是页面。
"""
import importlib.util
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from lib import freeze_gate  # noqa: E402

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "site/data"
SITE_ROOT = ROOT / "site"
EN = ROOT / "site/en"
BASELINE = ROOT / "scripts" / "output" / "data-badge-baseline.txt"
MARKER = "---- 第 66 门禁 数据徽标："
SKIP = {"_shell.html", "_template.html"}

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


def check_en_page(mod, zh_name: str, txt: str):
    """EN 页徽标判据（E1-E3·与 ZH 对应页同态）。

    W1265 批一（判据补盲 1-4）：原实现只扫 site/data ⇒ EN 138 页**零徽标**
    （审查报告 P2-4 实测：EN 仅 CSS 样式存在·无徽标元素）。
    判据：① MARK 恰一次 ② 徽标结构存在且 data-status 合法 ③ 态与 ZH 对应页一致
    （正本 classify 是文件名函数⇒中英同名页同态）④ ds-label 非空且不含行话。
    ※ ds-label 的**语言**未判（正本 STATUS_TEXT 只有中文文案·无英文正本）——留给页面线。
    """
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
    want = mod.classify(zh_name)
    if status != want:
        errs.append(f"data-status={status} ≠ ZH 对应页正本 classify={want}")
    lab = LABEL.search(m.group(0))
    if not lab or not lab.group(1).strip():
        errs.append("ds-label 缺失/为空")
    elif re.search(r"(?i)embedded|mock", lab.group(1)):
        errs.append(f"ds-label 含行话：{lab.group(1)[:40]!r}")
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


def scan_zh(mod, scope="all"):
    """扫 ZH 面（site/data + site 根页）→ (违例键, 扫描页数)。

    W1266 批二线 C 三轮（判据补盲 5）：原实现只扫 site/data ⇒ **ZH 根页 9 页
    零徽标**（根页曾不在任何扫描面 ⇒ 「该页无徽标」是盲区而非合规证据）。
    根页判据与 ZH data 页同款（ds-label 逐字取正本中文文案·防行话回潮）。
    """
    viol = []
    files = []
    if scope in ("zh", "all"):
        files += [f for f in sorted(DATA.glob("*.html")) if f.name not in SKIP]
    if scope in ("root", "zh", "all"):
        files += [f for f in sorted(SITE_ROOT.glob("*.html")) if f.name not in SKIP]
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        errs = check_page(mod, f.name, f.read_text(encoding="utf-8", errors="replace"))
        for e in errs:
            viol.append("%s|Z|%s" % (rel, e))
    return viol, len(files)


def scan_en(mod):
    """扫 EN 面 → (违例键, 违例页数)。"""
    viol = []
    if not EN.is_dir():
        return viol, 0
    files = [f for f in sorted(EN.glob("*.html")) if f.name not in SKIP]
    for f in files:
        errs = check_en_page(mod, f.name, f.read_text(encoding="utf-8", errors="replace"))
        for e in errs:
            viol.append("site/en/%s|E|%s" % (f.name, e))
    return viol, len(files)


def self_test_en(mod):
    """EN 面负样本自测：无徽标必红·徽标齐平必绿·态不一致必红。"""
    good = mod.build_badge("snapshot")
    cases = [
        ("正样本-EN 徽标齐平", good, "any.html", 0),
        ("负样本-EN 无徽标", "<p>裸页</p>", "any.html", 1),
        ("负样本-EN 态与 ZH 不一致", good.replace('data-status="snapshot"', 'data-status="live"'), "any.html", 1),
        ("负样本-EN ds-label 为空", good.replace("内嵌快照", ""), "any.html", 1),
    ]
    fails = 0
    for name, txt, fn, expect in cases:
        errs = check_en_page(mod, fn, txt)
        got = 1 if errs else 0
        if got != expect:
            fails += 1
            print(f"  [WRONG] {name}: got={got} expect={expect} {errs}")
        else:
            print(f"  [OK] {name}")
    print(f"EN 自测 {'PASS' if fails == 0 else 'FAIL'}（{len(cases)} 例）")
    return fails


def _parse_args(argv):
    """解析命令行参数（抽出以控 main 复杂度）。"""
    scope = "all"
    if "--scope" in argv:
        i = argv.index("--scope")
        if i + 1 < len(argv) and argv[i + 1] in ("zh", "root", "en", "all"):
            scope = argv[i + 1]
    return scope, ("--strict" in argv), ("--report" in argv)


def main():
    try:
        mod = _load_truth()
    except Exception as e:
        print(f"{MARKER}基础设施缺失（正本模块不可读）: {e}")
        sys.exit(2)
    argv = sys.argv[1:]
    scope, strict, report_only = _parse_args(argv)

    viol = []
    zh_viol = []
    zh_pages = 0
    if scope in ("zh", "root", "all"):
        zh_viol, zh_pages = scan_zh(mod, scope)
        viol.extend(zh_viol)
    en_viol = []
    en_pages = 0
    if scope in ("en", "all"):
        en_viol, en_pages = scan_en(mod)
        viol.extend(en_viol)

    if "--generate-baseline" in argv:
        n = freeze_gate.write_baseline(
            BASELINE,
            viol,
            [
                "# 第 66 门禁 · 数据徽标覆盖基线（W1265 建立·存量违例冻结）",
                "# 生成命令：py -3 scripts/check_data_badge_coverage.py --generate-baseline",
                "# 格式：<页面>|<Z|E>|<细节>；Z=ZH 面·E=EN 面",
                "# 语义：基线内违例记「存量基线」不计 FAIL；基线外新增 = FAIL；零容忍：--strict",
            ],
        )
        print(f"基线已写入 {BASELINE}（{n} 条）")
        return 0

    baseline, problems = freeze_gate.read_baseline(BASELINE)
    if problems:
        if report_only:
            for p in problems:
                print("NOTE " + p + "（报告档不判红）")
            baseline = set()
        else:
            for p in problems:
                print("FAIL " + p)
            print(f"{MARKER}基线缺失/不可读·fail-closed·拒绝通过 ----")
            return 1

    res = freeze_gate.evaluate(viol, baseline, strict=strict)
    for k in res["new_fail"][:15]:
        print("  ✗ " + k)
    if len(res["new_fail"]) > 15:
        print(f"  …其余 {len(res['new_fail']) - 15} 条略")
    verdict = "FAIL" if res["new_fail"] else "OK"
    print(
        f"{MARKER}页面 ZH {zh_pages} + EN {en_pages}（scope={scope}）· 违例 {res['total']} 条 · "
        f"{freeze_gate.FROZEN_LABEL} {len(res['frozen'])} 条 · 基线外新增 {len(res['new_fail'])} 条 · {verdict} ----"
    )
    if report_only:
        return 0
    return 1 if res["new_fail"] else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        mod = _load_truth()
        rc = self_test(mod)
        rc += self_test_en(mod)
        sys.exit(0 if rc == 0 else 2)
    main()
