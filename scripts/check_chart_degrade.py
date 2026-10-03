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

ROOT = Path(__file__).resolve().parent.parent
SITE_DATA = ROOT / "site" / "data"
SKIP_STEMS = ("_shell", "_template")
VALID = ("stacked", "scroll-x", "simplified", "n/a")
RE_DECL = re.compile(r"chart-degrade:\s*(stacked|scroll-x|simplified|n/a)\b")


def scan_pages() -> list[Path]:
    return [p for p in sorted(SITE_DATA.glob("*.html")) if p.stem not in SKIP_STEMS]


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


def main() -> int:
    pages = scan_pages()
    if not pages:
        print(f"FAIL 未扫到页面：{SITE_DATA}")
        return 1
    fails = []
    for p in pages:
        err = check_page(p)
        if err:
            fails.append(f"{p.relative_to(ROOT)} :: {err}")
    for f in fails[:20]:
        print("FAIL " + f)
    if len(fails) > 20:
        print(f"FAIL …其余 {len(fails) - 20} 页略")
    print(f"---- 第 30 门禁 降级声明：扫描 {len(pages)} 页 · 未声明/非法 {len(fails)} ----")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
