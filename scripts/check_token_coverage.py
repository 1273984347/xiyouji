#!/usr/bin/env python3
"""check_token_coverage.py — Phase E E6 转正门禁（M2/M3：页面私有 <style> 令牌覆盖率）

口径：
- 只扫页面**私有 <style> 块**（跳过 INLINED tokens/system 副本：块内含 "tokens.css —" 注释特征）。
- UI 裸色 = background/border/box-shadow/color/outline 属性值中的裸 hex/rgba/hsl（排除 var()/color-mix 派生）。
- 图表数据色豁免：页面 <style> 顶部 `/* e-track-exempt: chart-data-colors N 处 */` 注释登记 N。
  - 无注释页：UI 裸色必须 = 0。
  - 有注释页：UI 裸色 ≤ 注释 N（存量登记；新增会超 N 触发 FAIL）。
- M3：真裸 box-shadow（无 var/color-mix/none/inset）全站 = 0，豁免不适用。

用法：python scripts/check_token_coverage.py
退出码：0 = 通过；1 = FAIL
"""
import re
import sys
from pathlib import Path

from utils.gate_common import iter_private_style_blocks

ROOT = Path(__file__).resolve().parent.parent

# W803: 强制使用统一站点页面枚举；实现简化且与现役全版（834+ 页）相符。避免每个脚本重复写同一套 `glob(site/*.html) + glob(site/data/*.html) + glob(site/en/*.html)`。
UI_ATTR = re.compile(
    r"(background|border(?:-[a-z]+)?|box-shadow|color|outline)\s*:\s*"
    r"([#][0-9a-fA-F]{3,8}|rgba?\([^)]*\)|hsl[a-z]*\([^)]*\))"
)
SHADOW = re.compile(r"box-shadow\s*:\s*([^;!}]+)")
EXEMPT = re.compile(r"e-track-exempt: chart-data-colors (\d+) 处")


def check_page(path: Path):
    s = path.read_text(encoding="utf-8", errors="ignore")
    ui_n, shadow_n = 0, 0
    for st, _ln in iter_private_style_blocks(s):  # 跳过 INLINED 副本（按标记配对判定）
        for m in UI_ATTR.finditer(st):
            v = m.group(2)
            if re.match(r"var\(|color-mix", v):
                continue
            ui_n += 1
        for m in SHADOW.finditer(st):
            v = m.group(1).strip().replace("\n", " ")
            if "var(" in v or "color-mix" in v or v == "none" or "inset" in v:
                continue
            shadow_n += 1
    m = EXEMPT.search(s)
    allowed = int(m.group(1)) if m else 0
    return ui_n, allowed, shadow_n, bool(m)


def main():
    fails = []
    total_ui = total_shadow = 0
    from utils.gate_common import site_pages as gc_site_pages
    for f in gc_site_pages(data=True, root=True, en=True):
        f_path = Path(f)
        ui, allowed, sh, has_ex = check_page(f_path)
        total_ui += ui
        total_shadow += sh
        if sh:
            fails.append(f"{f_path.name}: 真裸 box-shadow {sh} 处（M3 必须 0）")
        if has_ex:
            if ui > allowed:
                fails.append(f"{f_path.name}: UI 裸色 {ui} > 豁免登记 {allowed}")
        else:
            if ui:
                fails.append(f"{f_path.name}: 无豁免注释但 UI 裸色 {ui} 处")
    print(f"token 覆盖率门禁：UI 裸色总 {total_ui} · 真裸 box-shadow 总 {total_shadow} · FAIL {len(fails)}")
    for msg in fails[:15]:
        print("  FAIL", msg)
    if fails:
        print("FAIL 详情见上（超 15 条仅显示前 15）")
        return 1
    print("OK   token 覆盖率门禁通过（私有块裸色全部豁免登记或为零）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
