#!/usr/bin/env python3
"""check_motion_ban.py — Phase E E6 转正门禁（D4 动效禁止清单）

扫描 site/ 全部 HTML（含 data/、en/）内联 CSS 与内联 JS 中的禁止动效模式：
- cubic-bezier 负值（回弹/过冲）
- rotate(360/720（旋转动画）
- animation 无限循环（infinite）
- parallax（视差滚动）
- d3 .duration(N) 数字形态 N > 600（DESIGN §5.1 全站硬指标·W769 补入·W760 F-4 实证
  en 站 19 页超限与门禁盲区；白名单：KPI count-up 900 需伴 easeOutExpo 上下文）

白名单（功能性/一次性）：
- .chart-loading 呼吸骨架（功能加载指示）
- .chart-fade-in 一次性入场
- 已登记豁免的动画（输出时注明）

用法：python scripts/check_motion_ban.py
退出码：0 = 通过；1 = FAIL
"""
import re
import sys
from pathlib import Path

from utils.gate_common import STYLE_BLOCK_RE, iter_private_style_blocks

ROOT = Path(__file__).resolve().parent.parent
BAN = [
    (re.compile(r"cubic-bezier\([^)]*-\d"), "cubic-bezier 负值（回弹）"),
    (re.compile(r"rotate\(36\d|rotate\(72\d"), "360°/720° 旋转"),
    (re.compile(r"animation\s*:\s*[^;]*infinite"), "无限循环动画"),
    (re.compile(r"parallax", re.I), "parallax 视差"),
]
WHITELIST_HINTS = ["chart-loading", "chart-fade-in"]
# 块级白名单：白名单命名的 @keyframes 整块（含嵌套层）+ 选择器含白名单词的规则块
WL_KEYFRAMES = re.compile(
    r"@keyframes\s+[\w-]*(?:chart-loading|chart-fade-in)[\w-]*\s*\{(?:[^{}]*|\{[^{}]*\})*\}")
WL_RULE = re.compile(r"[^{}@]*?(?:chart-loading|chart-fade-in)[^{}]*\{[^{}]*\}")


def strip_whitelist_blocks(css):
    return WL_RULE.sub("", WL_KEYFRAMES.sub("", css))


def scan_css(css, rel, fails):
    css = strip_whitelist_blocks(css)
    for pat, desc in BAN:
        for m in pat.finditer(css):
            ctx = css[max(0, m.start() - 40):m.end() + 20].replace("\n", " ")
            fails.append(f"{rel}: {desc} → …{ctx}…")


def main():
    fails = []
    # 共享 CSS 源文件单次扫描（块级白名单）；页面内 INLINED 副本跳过（同源不重扫）
    for src in ("site/tokens.css", "site/system.css"):
        p = ROOT / src
        if p.exists():
            scan_css(p.read_text(encoding="utf-8", errors="ignore"), src, fails)
    for f in sorted(ROOT.glob("site/**/*.html")):
        rel = str(f.relative_to(ROOT))
        s = f.read_text(encoding="utf-8", errors="ignore")
        rest = s
        private = {body for body, _ in iter_private_style_blocks(s)}
        # W1022 修（审查 P2-4）：块枚举必须与 `iter_private_style_blocks` 用同一正则形态。
        # 原用精确 `<style>` 字面量 ⇒ 168 个含属性页（`<style id="audit-halo">` 等）的私有块
        # 既不进 private 集合、也没被 rest.replace 摘除 ⇒ 落到「剩余文本」路径且失去白名单剥离
        # ⇒ 一旦禁用动效落进带属性块即假红（当前 0 命中，属潜伏）。
        for _m in STYLE_BLOCK_RE.finditer(s):
            st = _m.group(1)
            rest = rest.replace(st, "", 1)
            if st not in private:  # INLINED 副本跳过（共享 CSS 已在源文件扫过）
                continue
            scan_css(st, rel, fails)
        # 剔除白名单上下文行后再扫其余文本（内联 JS 等）
        lines = [ln for ln in rest.splitlines() if not any(h in ln for h in WHITELIST_HINTS)]
        body = "\n".join(lines)
        for pat, desc in BAN:
            for m in pat.finditer(body):
                ctx = body[max(0, m.start() - 40):m.end() + 20].replace("\n", " ")
                fails.append(f"{rel}: {desc} → …{ctx}…")
        # W769：d3 .duration(N) 硬指标 N ≤ 600（DESIGN §5.1·白名单 KPI count-up 900 伴 easeOutExpo）
        for m in re.finditer(r"\.duration\(\s*(\d+)\s*\)", body):
            n = int(m.group(1))
            if n <= 600:
                continue
            ctx0 = body[max(0, m.start() - 90):m.end() + 40]
            if n == 900 and "easeOutExpo" in ctx0:
                continue  # KPI count-up 白名单
            ctx = ctx0.replace("\n", " ")
            fails.append(f"{rel}: .duration({n}) 超 600（DESIGN §5.1 硬指标） → …{ctx}…")
    print(f"动效禁止清单门禁：命中 {len(fails)}")
    for msg in fails[:15]:
        print("  FAIL", msg)
    if fails:
        print("FAIL 详情见上（超 15 条仅显示前 15）")
        return 1
    print("OK   动效禁止清单门禁通过（无 bounce/旋转/无限循环/parallax·duration≤600）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
