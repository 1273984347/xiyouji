#!/usr/bin/env python3
"""check_chart_degrade.py — 第 30 门禁 · 窄屏降级声明（PD-1b · W654）

判据（DESIGN.md §4B 选型章配套）：site/data 每个可视化页必须在页内声明窄屏降级形态——
  <!-- chart-degrade: stacked | scroll-x | simplified | n/a -->
四值枚举（与 §4B 表「窄屏降级方案」列一致）。缺声明或值非法 = FAIL。
实现为静态解析，不启浏览器（PD-1 交付物 3）。

范围：site/data 86 页（_shell/_template 模板壳跳过·与其余门禁 SKIP_STEMS 同口径）。
声明位置：HTML 注释任意位置（推荐 dataSource 区上方）。

用法：
  python scripts/check_chart_degrade.py            # 门禁（verify_delivery 调用）
  python scripts/check_chart_degrade.py --self-test
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from lib import freeze_gate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE_DATA = ROOT / "site" / "data"
SITE_EN = ROOT / "site" / "en"
BASELINE = ROOT / "scripts" / "output" / "chart-degrade-baseline.txt"
MARKER = "---- 第 30 门禁 降级声明："
SKIP_STEMS = ("_shell", "_template")
VALID = ("stacked", "scroll-x", "simplified", "n/a")
RE_DECL = re.compile(r"chart-degrade:\s*(stacked|scroll-x|simplified|n/a)\b")


def scan_pages(scope: str = "all") -> list[Path]:
    """枚举待扫页面。

    W1265 批一（判据补盲 1-3）：原实现只扫 site/data ⇒ EN 138 页零覆盖
    （审查报告 P2-1：EN 138 页 chart-degrade 声明 0）。本槽扩面到 site/en。
    """
    dirs = []
    if scope in ("zh", "all"):
        dirs.append(SITE_DATA)
    if scope in ("en", "all"):
        dirs.append(SITE_EN)
    out: list[Path] = []
    for d in dirs:
        if not d.is_dir():
            continue
        out.extend(p for p in sorted(d.glob("*.html")) if p.stem not in SKIP_STEMS)
    return out


def check_page(path: Path) -> str | None:
    """返回违规描述；None = 通过。"""
    html = path.read_text(encoding="utf-8", errors="ignore")
    m = RE_DECL.search(html)
    if not m:
        # 容错：检测到其他写法（如全角冒号/旧值）时给出可行动提示
        loose = re.search(r"chart-degrade\s*[：:]\s*(\S{0,20})", html)
        if loose:
            return f"声明写法非法：{loose.group(0)[:40]!r}（须 <!-- chart-degrade: stacked|scroll-x|simplified|n/a -->）"
        return "缺 chart-degrade 声明"
    return None


def scan(scope: str = "all") -> tuple[list[str], int]:
    """扫描 → (违例键列表, 扫描页数)。违例键 = <页面>|D1|<细节>。"""
    viol: list[str] = []
    pages = scan_pages(scope)
    for p in pages:
        err = check_page(p)
        if err:
            viol.append("%s|D1|%s" % (p.relative_to(ROOT).as_posix(), err))
    return viol, len(pages)


def self_test() -> int:
    """负样本自测：缺声明必红·合法声明必绿·基线语义正确。"""
    cases = [
        ("正样本-合法声明", "<!-- chart-degrade: stacked -->", 0),
        ("正样本-四值枚举均可", "<!-- chart-degrade: scroll-x -->", 0),
        ("负样本-缺声明", "<p>无声明</p>", 1),
        ("负样本-非法值", "<!-- chart-degrade: banana -->", 1),
    ]
    tmp = ROOT / "scripts" / "output" / "_w1265_degrade_selftest.html"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    bad = 0
    for name, text, expect in cases:
        tmp.write_text(text, encoding="utf-8")
        try:
            err = check_page(tmp)
        finally:
            tmp.unlink(missing_ok=True)
        got = 1 if err else 0
        ok = got == expect
        print(f"{'OK  ' if ok else 'FAIL'} {name}：期望 {expect}·实得 {got} {err or ''}")
        bad += 0 if ok else 1
    viol = ["site/en/x.html|D1|缺 chart-degrade 声明"]
    res = freeze_gate.evaluate(viol, set(viol), strict=False)
    ok = not res["new_fail"]
    print(f"{'OK  ' if ok else 'FAIL'} 基线内违例不计 FAIL")
    bad += 0 if ok else 1
    res = freeze_gate.evaluate(viol, set(), strict=False)
    ok = len(res["new_fail"]) == 1
    print(f"{'OK  ' if ok else 'FAIL'} 基线外新增违例计 FAIL")
    bad += 0 if ok else 1
    res = freeze_gate.evaluate(viol, set(viol), strict=True)
    ok = len(res["new_fail"]) == 1
    print(f"{'OK  ' if ok else 'FAIL'} 零容忍模式存量全红")
    bad += 0 if ok else 1
    print(f"自测 {len(cases) + 3 - bad}/{len(cases) + 3} 通过")
    return 0 if bad == 0 else 2


def _parse_args(argv):
    """解析命令行参数（抽出以控 main 复杂度）。"""
    scope = "all"
    if "--scope" in argv:
        i = argv.index("--scope")
        if i + 1 < len(argv) and argv[i + 1] in ("zh", "en", "all"):
            scope = argv[i + 1]
    baseline_path = BASELINE
    if "--baseline" in argv:
        i = argv.index("--baseline")
        if i + 1 < len(argv):
            baseline_path = Path(argv[i + 1])
            if not baseline_path.is_absolute():
                baseline_path = ROOT / baseline_path
    return scope, ("--strict" in argv), ("--report" in argv), baseline_path


def main() -> int:
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return self_test()
    scope, strict, report_only, baseline_path = _parse_args(argv)

    viol, npages = scan(scope)
    if not npages:
        print(f"FAIL 未扫到页面：{SITE_DATA}")
        return 1
    if "--generate-baseline" in argv:
        n = freeze_gate.write_baseline(
            baseline_path,
            viol,
            [
                "# 第 30 门禁 · 窄屏降级声明基线（W1265 建立·存量违例冻结）",
                "# 生成命令：py -3 scripts/check_chart_degrade.py --generate-baseline",
                "# 格式：<页面>|<D1>|<细节>；D1=缺 chart-degrade 声明或写法非法",
                "# 语义：基线内违例记「存量基线」不计 FAIL；基线外新增 = FAIL；零容忍：--strict",
            ],
        )
        print(f"基线已写入 {baseline_path}（{n} 条）")
        return 0

    baseline, problems = freeze_gate.read_baseline(baseline_path)
    if problems:
        if report_only:
            for p in problems:
                print("NOTE " + p + "（报告档不判红）")
            baseline = set()
        else:
            for p in problems:
                print("FAIL " + p)
            print(f"{MARKER} 基线缺失/不可读·fail-closed·拒绝通过 ----")
            return 1

    res = freeze_gate.evaluate(viol, baseline, strict=strict)
    for k in res["new_fail"][:20]:
        print("FAIL " + k)
    if len(res["new_fail"]) > 20:
        print(f"FAIL …其余 {len(res['new_fail']) - 20} 页略")
    print(
        "%s 扫描 %d 页（scope=%s）· 违例 %d 条 · %s %d 条 · 基线外新增 %d 条 · %s ----"
        % (
            MARKER,
            npages,
            scope,
            res["total"],
            freeze_gate.FROZEN_LABEL,
            len(res["frozen"]),
            len(res["new_fail"]),
            "FAIL" if res["new_fail"] else "OK",
        )
    )
    if report_only:
        return 0
    return 1 if res["new_fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
