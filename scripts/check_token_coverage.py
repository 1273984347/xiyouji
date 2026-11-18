#!/usr/bin/env python3
"""check_token_coverage.py — Phase E E6 转正门禁（M2/M3：页面私有 <style> 令牌覆盖率）

口径：
- 只扫页面**私有 <style> 块**（跳过 INLINED tokens/system 副本：按 `<!-- INLINED CSS … -->`
  标记与紧随 `<style>` 的**配对**识别，见 `utils/gate_common.iter_private_style_blocks`）。
  W1022 订正：原文写「块内含 "tokens.css —" 注释特征」是 W1019 已废掉的脆弱判据——
  剥注释即失效（228 页误判实证），文档与实现必须同口径。
- UI 裸色 = background/border/box-shadow/color/outline 属性值中的裸 hex/rgba/hsl（排除 var()/color-mix 派生）。
- 图表数据色豁免：页面 <style> 顶部 `/* e-track-exempt: chart-data-colors N 处 */` 注释登记 N。
  - 无注释页：UI 裸色必须 = 0。
  - 有注释页：UI 裸色 ≤ 注释 N（存量登记；新增会超 N 触发 FAIL）。
- M3：真裸 box-shadow（无 var/color-mix/none/inset）全站 = 0，豁免不适用。

用法：python scripts/check_token_coverage.py
退出码：0 = 通过；1 = FAIL
"""
import os
import re
import sys
from pathlib import Path

# W1276：与 relink / inline_css 同源（公共层索引口径·禁再抄一份）
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from inline_css import strip_comments  # noqa: E402
from relink_public_css import _top_rules  # noqa: E402
from utils.gate_common import iter_private_style_blocks  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# W803: 强制使用统一站点页面枚举；实现简化且与现役全版（834+ 页）相符。避免每个脚本重复写同一套 `glob(site/*.html) + glob(site/data/*.html) + glob(site/en/*.html)`。
UI_ATTR = re.compile(
    r"(background|border(?:-[a-z]+)?|box-shadow|color|outline)\s*:\s*"
    r"([#][0-9a-fA-F]{3,8}|rgba?\([^)]*\)|hsl[a-z]*\([^)]*\))"
)
SHADOW = re.compile(r"box-shadow\s*:\s*([^;!}]+)")
EXEMPT = re.compile(r"e-track-exempt: chart-data-colors (\d+) 处")
RE_RULE_SPAN = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)

# W1276：公共层「管辖」口径索引（与 relink 公共层索引同源）
_PUBLIC_SCOPE = None


def _rule_spans(css: str):
    """规则级切分 → [(选择器文本, 声明体, start, end)]"""
    out = []
    for m in RE_RULE_SPAN.finditer(css):
        out.append((" ".join(m.group(1).split()), m.group(2), m.start(), m.end()))
    return out


def _decl_props(body: str) -> set:
    """单条规则的声明属性集。"""
    props = set()
    for part in body.split(";"):
        if ":" in part:
            props.add(part.split(":", 1)[0].strip())
    return props


def _public_scope_props():
    """公共层「管辖」的 (选择器集合 → 声明属性集) 索引（W1276 口径·与 relink 同源）。"""
    global _PUBLIC_SCOPE
    if _PUBLIC_SCOPE is None:
        scope = {}
        for name in ("tokens.css", "system.css"):
            p = Path(ROOT) / "site" / name
            if not p.exists():
                continue
            css = strip_comments(p.read_text(encoding="utf-8"))
            for sels, body, _st, _en in _top_rules(css):
                scope.setdefault(sels, set()).update(_decl_props(body))
        _PUBLIC_SCOPE = scope
    return _PUBLIC_SCOPE


def _is_public_scope(sel_text: str, body: str) -> bool:
    """该规则是否由公共层「管辖」（同选择器 + 属性交集非空）⇒ 不计入页私有裸色。"""
    sels = frozenset(s.strip() for s in sel_text.split(",") if s.strip())
    scope = _public_scope_props()
    if sels not in scope:
        return False
    return bool(_decl_props(body) & scope[sels])


def _count_bare(st: str) -> int:
    """私有块内的 UI 裸色计数（剔除「公共层管辖」规则·W1276 口径）。"""
    n = 0
    for _sels, _body, _st, _en in _rule_spans(st):
        if _is_public_scope(_sels, _body):
            continue
        for m in UI_ATTR.finditer(_body):
            v = m.group(2)
            if re.match(r"var\(|color-mix", v):
                continue
            n += 1
    return n

def check_page(path: Path):
    s = path.read_text(encoding="utf-8", errors="ignore")
    ui_n, shadow_n = 0, 0
    for st, _ln in iter_private_style_blocks(s):  # 跳过 INLINED 副本（按标记配对判定）
        # W1276：规则级解析——「公共层管辖」的规则整条剔除（口径与 relink 变体判定同源），
        # 其余规则的裸色照旧计入（判定强度不降：真私有裸色仍受豁免上限约束）。
        ui_n += _count_bare(st)
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
